import os
from typing import Any, List, Optional, Union
from dotenv import load_dotenv
from pydantic import BaseModel, Field, model_validator

load_dotenv()
DEFAULT_TARGET_LANGUAGE = os.getenv("DEFAULT_TARGET_LANGUAGE", "Java")


class CodeSubmission(BaseModel):
    question_text: str = Field(
        ...,
        description="The problem statement or question"
    )
    code: str = Field(
        ...,
        description="The student's submitted source code"
    )
    return_answer: Optional[str] = Field(
        None,
        description="Optional expected return value, output format, or reference answer"
    )
    specific_instructions: Optional[str] = Field(
        None,
        description="Optional extra constraints, edge cases, or instructions for this question"
    )

    @model_validator(mode="before")
    @classmethod
    def normalize_aliases(cls, data: Any) -> Any:
        if isinstance(data, dict):
            d = dict(data)
            # Question alias mapping
            if "question_text" not in d:
                if "question" in d:
                    d["question_text"] = d.pop("question")
                elif "problem" in d:
                    d["question_text"] = d.pop("problem")

            # Student code / answer alias mapping
            if "code" not in d:
                if "student_answer" in d:
                    d["code"] = d.pop("student_answer")
                elif "student_code" in d:
                    d["code"] = d.pop("student_code")
                elif "solution" in d:
                    d["code"] = d.pop("solution")

            # Return answer / expected output alias mapping
            if "return_answer" not in d:
                if "expected_output" in d:
                    d["return_answer"] = d.pop("expected_output")
                elif "expected_answer" in d:
                    d["return_answer"] = d.pop("expected_answer")
                elif "return_output" in d:
                    d["return_answer"] = d.pop("return_output")

            # Specific instructions alias mapping
            if "specific_instructions" not in d and "instructions" in d:
                d["specific_instructions"] = d.pop("instructions")

            return d
        return data


class CodeReviewRequest(BaseModel):
    target_language: str = Field(
        default=DEFAULT_TARGET_LANGUAGE,
        description="Programming language of the submitted code"
    )
    submissions: List[CodeSubmission] = Field(
        default_factory=list,
        description="List of question + code submissions to evaluate"
    )

    @model_validator(mode="before")
    @classmethod
    def normalize_flat_payload(cls, data: Any) -> Any:
        if isinstance(data, dict) and not data.get("submissions"):
            question_text = (
                data.get("question_text")
                or data.get("question")
                or data.get("problem")
            )
            code = (
                data.get("code")
                or data.get("student_answer")
                or data.get("student_code")
                or data.get("solution")
            )
            return_answer = (
                data.get("return_answer")
                or data.get("expected_output")
                or data.get("expected_answer")
            )
            instructions = (
                data.get("specific_instructions")
                or data.get("instructions")
            )

            if question_text and code:
                data = dict(data)
                data["submissions"] = [
                    {
                        "question_text": str(question_text),
                        "code": str(code),
                        "return_answer": str(return_answer) if return_answer else None,
                        "specific_instructions": str(instructions) if instructions else None,
                    }
                ]
        return data


class ScoreBreakdown(BaseModel):
    completeness_score: float = Field(0.0, ge=0.0, le=10.0)
    code_quality_score: float = Field(0.0, ge=0.0, le=10.0)
    approach_taken_score: float = Field(0.0, ge=0.0, le=10.0)
    overall_score: float = Field(0.0, ge=0.0, le=10.0)


class IndividualReview(BaseModel):
    question_text: str = ""
    correctness_feedback: str = ""
    scores: ScoreBreakdown = Field(default_factory=ScoreBreakdown)


class SummaryReview(BaseModel):
    overall_average_score: float = 0.0
    overall_quality_label: str = "Critical"
    common_errors: str = ""
    strengths: str = ""
    weaknesses: str = ""
    recommendations: str = ""


class ExecutionMetrics(BaseModel):
    request_duration_seconds: float = 0.0
    lang_detection_duration_seconds: float = 0.0
    code_eval_duration_seconds: float = 0.0
    total_requests_processed: int = 0
    running_average_duration_seconds: float = 0.0


class PromptDrivenCodeReviewResponse(BaseModel):
    individual_reviews: List[IndividualReview] = Field(default_factory=list)
    summary_review: Optional[Union[SummaryReview, str]] = None
    execution_metrics: Optional[ExecutionMetrics] = None