import ollama
import os
import json
import asyncio
import logging
import time
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, FileResponse

from schemas import (
    CodeReviewRequest,
    PromptDrivenCodeReviewResponse,
    IndividualReview,
    SummaryReview,
    ScoreBreakdown,
    ExecutionMetrics
)
from prompts import format_submissions, build_unified_evaluation_prompt

load_dotenv()

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5-coder:7b-instruct")
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.1"))
LLM_TIMEOUT_SECONDS = float(os.getenv("LLM_TIMEOUT_SECONDS", "300"))
DEFAULT_TARGET_LANGUAGE = os.getenv("DEFAULT_TARGET_LANGUAGE", "Java")
TEMPLATES_DIR = Path(__file__).resolve().parent / "templates"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("app.log", mode="a", encoding="utf-8")
    ]
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="QWEN Code Evaluator",
    description="LLM-powered code review and scoring API",
)

ollama_client = ollama.AsyncClient()

METRICS_STATS = {
    "total_requests": 0,
    "total_duration": 0.0
}
metrics_lock = asyncio.Lock()


async def record_metrics(req_duration: float):
    async with metrics_lock:
        METRICS_STATS["total_requests"] += 1
        METRICS_STATS["total_duration"] += req_duration
        avg = METRICS_STATS["total_duration"] / METRICS_STATS["total_requests"]
        return METRICS_STATS["total_requests"], round(avg, 2)


class LLMClientError(Exception):
    pass


async def send_prompt(prompt_text: str = "", json_mode: bool = True) -> str:
    options = {
        "temperature": LLM_TEMPERATURE,
        "num_ctx": 2048,
        "num_predict": 450,
    }
    kwargs = {
        "model": OLLAMA_MODEL,
        "messages": [
            {"role": "system", "content": "You are a fair, precise, and deterministic code evaluator. Return strictly valid JSON."},
            {"role": "user", "content": prompt_text},
        ],
        "options": options,
        "keep_alive": "5m",
    }

    if json_mode:
        kwargs["format"] = "json"

    max_attempts = 2
    for attempt in range(1, max_attempts + 1):
        try:
            response = await asyncio.wait_for(
                ollama_client.chat(**kwargs),
                timeout=LLM_TIMEOUT_SECONDS
            )
            content = response["message"]["content"]
            if content:
                return content.strip()
            raise LLMClientError("LLM returned empty content.")
        except LLMClientError:
            raise
        except asyncio.TimeoutError:
            logger.error(f"[TIMEOUT] LLM call timed out after {LLM_TIMEOUT_SECONDS}s (attempt {attempt}/{max_attempts})")
            if attempt < max_attempts:
                await asyncio.sleep(1.0)
                continue
            raise LLMClientError(f"Request timed out after {LLM_TIMEOUT_SECONDS} seconds.")
        except Exception as e:
            if attempt < max_attempts:
                await asyncio.sleep(1.0)
                continue
            raise LLMClientError(f"Failed after {max_attempts} attempts: {e}")
    raise LLMClientError("LLM call failed after all attempts.")


@app.get("/", response_class=HTMLResponse)
async def home():
    return FileResponse(TEMPLATES_DIR / "index.html", media_type="text/html")


@app.get("/api/metrics")
async def get_metrics():
    avg = (METRICS_STATS["total_duration"] / METRICS_STATS["total_requests"]) if METRICS_STATS["total_requests"] > 0 else 0.0
    return {
        "total_requests_processed": METRICS_STATS["total_requests"],
        "running_average_duration_seconds": round(avg, 2)
    }


@app.post("/review", response_model=PromptDrivenCodeReviewResponse)
async def review_code(request: CodeReviewRequest):
    req_start_time = time.perf_counter()
    logger.info("=== [PROCESS STARTED] Code Evaluation Request Received ===")

    if not request.submissions:
        logger.error("[REJECTED] No code submissions provided in request payload.")
        raise HTTPException(status_code=400, detail="No submissions provided.")

    logger.info(f"[INPUT RECEIVED] Target Language: {request.target_language} | Total Submissions: {len(request.submissions)}")

    formatted = format_submissions(request.submissions)
    eval_prompt = build_unified_evaluation_prompt(
        target_language=request.target_language,
        ques_ans_content_with_inst=formatted,
        summary_gen_flag=True,
    )

    logger.info(f"[STEP 1/2] Sending unified evaluation prompt ({len(eval_prompt)} chars) to model '{OLLAMA_MODEL}'...")
    eval_start = time.perf_counter()
    try:
        raw_response = await send_prompt(eval_prompt, json_mode=True)
        eval_duration = time.perf_counter() - eval_start
        logger.info(f"[LLM RESPONSE RECEIVED] Single-pass evaluation completed in {eval_duration:.2f} seconds.")
    except LLMClientError as e:
        logger.error(f"[ERROR] LLM evaluation call failed after {time.perf_counter() - eval_start:.2f}s: {e}")
        raise HTTPException(status_code=502, detail=f"LLM error: {e}")

    logger.info("[STEP 2/2] Parsing LLM response into structured output...")
    try:
        result = json.loads(raw_response)
    except json.JSONDecodeError as e:
        logger.error(f"[ERROR] Failed to parse JSON response from LLM: {e}")
        raise HTTPException(status_code=502, detail=f"LLM returned invalid JSON: {e}")

    is_lang_match = result.get("language_match", True)
    detected_lang = str(result.get("detected_language", request.target_language)).strip()
    target_clean = request.target_language.strip().lower()
    detected_clean = detected_lang.lower()

    if is_lang_match is False or (detected_clean != "unknown" and detected_clean != target_clean and not target_clean.startswith(detected_clean)):
        logger.warning(f"[LANGUAGE MISMATCH] Expected '{request.target_language}', but detected '{detected_lang}'. Enforcing 0.0 scores.")
        mismatch_msg = f"⚠️ Language Mismatch: Submitted code was detected as {detected_lang}, but expected {request.target_language}."
        
        reviews = []
        for sub in request.submissions:
            reviews.append(
                IndividualReview(
                    question_text=sub.question_text,
                    correctness_feedback=f"{mismatch_msg} Evaluation skipped and 0.0 score assigned.",
                    scores=ScoreBreakdown(
                        completeness_score=0.0,
                        code_quality_score=0.0,
                        approach_taken_score=0.0,
                        overall_score=0.0
                    )
                )
            )

        summary = SummaryReview(
            overall_average_score=0.0,
            overall_quality_label="Critical",
            common_errors=mismatch_msg,
            strengths="None",
            weaknesses=f"Submitted code is written in {detected_lang} instead of requested {request.target_language}.",
            recommendations=f"Please rewrite and submit your solution in {request.target_language}."
        )

        total_duration = time.perf_counter() - req_start_time
        total_reqs, running_avg = await record_metrics(total_duration)

        metrics = ExecutionMetrics(
            request_duration_seconds=round(total_duration, 2),
            lang_detection_duration_seconds=0.0,
            code_eval_duration_seconds=round(eval_duration, 2),
            total_requests_processed=total_reqs,
            running_average_duration_seconds=running_avg
        )

        return PromptDrivenCodeReviewResponse(
            individual_reviews=reviews,
            summary_review=summary,
            execution_metrics=metrics
        )

    result.pop("language_match", None)
    result.pop("detected_language", None)

    total_duration = time.perf_counter() - req_start_time
    total_reqs, running_avg = await record_metrics(total_duration)

    metrics = ExecutionMetrics(
        request_duration_seconds=round(total_duration, 2),
        lang_detection_duration_seconds=0.0,
        code_eval_duration_seconds=round(eval_duration, 2),
        total_requests_processed=total_reqs,
        running_average_duration_seconds=running_avg
    )

    logger.info(f"=== [PROCESS COMPLETED] Total Request Time: {total_duration:.2f}s | Total Requests Processed: {total_reqs} | Running Average Response Time: {running_avg:.2f}s ===")

    result["execution_metrics"] = metrics.model_dump()
    return PromptDrivenCodeReviewResponse(**result)
