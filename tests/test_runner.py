"""
test_runner.py — Master Automation Test Runner for QWEN Code Evaluator (48 Test Cases)

Runs all 48 test cases across all categories against the live /review API endpoint,
evaluates scoring precision, detects blind spots, and produces:
  - tests/test_report.md (Comprehensive Master Report)
  - tests/raw_results.json (Consolidated Raw API Responses)

Usage:
  python tests/test_runner.py
"""

import sys
import io

# Fix Windows console encoding for emoji/unicode characters
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

import os
import json
import time
import datetime
import requests

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tests.test_data import TEST_CASES

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
API_BASE = "http://127.0.0.1:8000"
REVIEW_ENDPOINT = f"{API_BASE}/review"
TIMEOUT_PER_REQUEST = 320

REPORT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "tests")
REPORT_PATH = os.path.join(REPORT_DIR, "test_report.md")
RAW_RESULTS_PATH = os.path.join(REPORT_DIR, "raw_results.json")


def send_review_request(test_case: dict) -> dict:
    """Send a single test case to the /review endpoint and return the parsed response."""
    payload = {
        "target_language": test_case["target_language"],
        "submissions": [
            {
                "question_text": test_case["question_text"],
                "code": test_case["code"],
            }
        ],
    }

    start = time.perf_counter()
    try:
        resp = requests.post(REVIEW_ENDPOINT, json=payload, timeout=TIMEOUT_PER_REQUEST)
        elapsed = time.perf_counter() - start
        resp.raise_for_status()
        data = resp.json()
        data["_elapsed_seconds"] = round(elapsed, 2)
        data["_http_status"] = resp.status_code
        return data
    except requests.exceptions.Timeout:
        return {"_error": "TIMEOUT", "_elapsed_seconds": round(time.perf_counter() - start, 2)}
    except requests.exceptions.ConnectionError:
        return {"_error": "CONNECTION_REFUSED", "_elapsed_seconds": 0.0}
    except Exception as e:
        return {"_error": str(e), "_elapsed_seconds": round(time.perf_counter() - start, 2)}


def extract_scores(response: dict) -> dict:
    """Extract individual review scores and feedback from the API response."""
    try:
        review = response["individual_reviews"][0]
        scores = review.get("scores", {})
        feedback = review.get("correctness_feedback", "")
        return {
            "completeness": scores.get("completeness_score", -1),
            "code_quality": scores.get("code_quality_score", -1),
            "approach": scores.get("approach_taken_score", -1),
            "overall": scores.get("overall_score", -1),
            "feedback": feedback,
        }
    except (KeyError, IndexError, TypeError):
        return {
            "completeness": -1,
            "code_quality": -1,
            "approach": -1,
            "overall": -1,
            "feedback": "(failed to parse)",
        }


def extract_summary(response: dict) -> dict:
    """Extract summary review from the API response."""
    try:
        summary = response.get("summary_review", {})
        if isinstance(summary, str):
            return {"label": summary, "avg_score": -1}
        return {
            "label": summary.get("overall_quality_label", "N/A"),
            "avg_score": summary.get("overall_average_score", -1),
            "common_errors": summary.get("common_errors", ""),
            "strengths": summary.get("strengths", ""),
            "weaknesses": summary.get("weaknesses", ""),
            "recommendations": summary.get("recommendations", ""),
        }
    except Exception:
        return {"label": "N/A", "avg_score": -1}


def evaluate_result(test_case: dict, scores: dict) -> dict:
    """Validate whether the overall score is within the expected ground-truth range."""
    overall = scores["overall"]
    exp_min = test_case["expected_overall_min"]
    exp_max = test_case["expected_overall_max"]

    if overall < 0:
        return {"passed": False, "reason": "Failed to extract overall score from response."}

    in_range = exp_min <= overall <= exp_max
    return {
        "passed": in_range,
        "reason": (
            f"overall_score={overall:.1f} is {'WITHIN' if in_range else 'OUTSIDE'} "
            f"expected range [{exp_min:.1f}, {exp_max:.1f}]"
        ),
    }


def detect_blind_spots(test_case: dict, scores: dict) -> list:
    """Detect known model blind-spot patterns."""
    flags = []
    vid = test_case["id"]
    overall = scores["overall"]
    feedback = scores["feedback"].lower()

    # Broken/buggy test cases
    broken_variants = {
        "V2", "V4", "V5", "V6", "V7", "V9", "V10", "V11", "V12", "V13", "V16",
        "V20", "V21", "V22", "V24", "V25", "V28", "V29", "V32", "V34", "V36", "V37", "V38",
        "V40", "V41", "V42", "V43", "V45", "V46", "V48"
    }
    correct_variants = {
        "V1", "V14", "V18", "V19", "V23", "V26", "V27", "V31", "V35", "V39", "V47"
    }

    # False positive on broken code
    if vid in broken_variants and overall >= 7.5:
        flags.append(f"⚠️ FALSE POSITIVE: {vid} scored {overall:.1f} — model may have missed the bug")

    # Praise on broken code
    if vid in broken_variants:
        praise_words = ["correct", "efficient", "best practices", "well-written", "no issues"]
        found_praise = [w for w in praise_words if w in feedback]
        if found_praise:
            flags.append(f"⚠️ PRAISE ON BROKEN CODE: {vid} feedback contains: {', '.join(found_praise)}")

    # False negative on valid code
    if vid in correct_variants and overall < 5.0:
        flags.append(f"⚠️ FALSE NEGATIVE: {vid} scored {overall:.1f} — model penalized correct code")

    # Specific recurring blind spots
    if vid in {"V17", "V42"} and overall >= 7.5:
        flags.append(f"⚠️ BLIND SPOT (0-Init): {vid} scored {overall:.1f} — missed 0-init bug on negative numbers")

    if vid in {"V12", "V22"} and overall >= 6.0:
        flags.append(f"⚠️ BLIND SPOT (Infinite Loop): {vid} scored {overall:.1f} — missed missing loop increment")

    if vid in {"V2", "V9", "V10", "V11", "V13", "V20", "V25", "V29", "V37"} and overall >= 5.0:
        flags.append(f"⚠️ BLIND SPOT (Compile Error): {vid} scored {overall:.1f} — missed syntax/compile error")

    if vid in {"V43", "V48"} and overall >= 7.0:
        flags.append(f"⚠️ BLIND SPOT (Missing Step): {vid} scored {overall:.1f} — missed missing Arrays.sort() step")

    if vid == "V40" and overall >= 7.0:
        flags.append(f"⚠️ BLIND SPOT (Pointer Overwrite): V40 scored {overall:.1f} — missed linked list pointer overwrite")

    return flags


def generate_report(results: list, total_time: float) -> str:
    """Generate the consolidated master markdown test report."""
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    total = len(results)
    passed = sum(1 for r in results if r["verdict"]["passed"])
    failed = total - passed
    accuracy = (passed / total * 100) if total > 0 else 0

    all_flags = []
    for r in results:
        all_flags.extend(r.get("blind_spots", []))

    times = [r["elapsed"] for r in results if r["elapsed"] > 0]
    avg_time = sum(times) / len(times) if times else 0
    min_time = min(times) if times else 0
    max_time = max(times) if times else 0

    # Category breakdown
    categories = {}
    for r in results:
        cat = r["category"]
        if cat not in categories:
            categories[cat] = {"total": 0, "passed": 0}
        categories[cat]["total"] += 1
        if r["verdict"]["passed"]:
            categories[cat]["passed"] += 1

    lines = []
    lines.append(f"# 📊 QWEN Evaluator — Unified Master Test Report (48 Variants)")
    lines.append(f"")
    lines.append(f"**Generated:** {now}")
    lines.append(f"**Model:** qwen2.5-coder:7b-instruct")
    lines.append(f"**Total Test Suite:** 48 Controlled Variants Across 16 Problem Contexts")
    lines.append(f"**Total Suite Runtime:** {total_time:.1f}s (~{total_time/60:.1f} min)")
    lines.append(f"")
    lines.append(f"---")
    lines.append(f"")

    # Overall Summary Table
    lines.append(f"## Overall Evaluation Summary")
    lines.append(f"")
    lines.append(f"| Metric | Value |")
    lines.append(f"|---|---|")
    lines.append(f"| Total Tests Executed | **{total}** |")
    lines.append(f"| ✅ Passed (Within Expected Range) | **{passed}** |")
    lines.append(f"| ❌ Failed (Outside Expected Range) | **{failed}** |")
    lines.append(f"| Overall Accuracy Rate | **{accuracy:.1f}%** |")
    lines.append(f"| Average Response Latency | **{avg_time:.1f}s** |")
    lines.append(f"| Min / Max Response Latency | **{min_time:.1f}s / {max_time:.1f}s** |")
    lines.append(f"| Blind Spot Warnings Triggered | **{len(all_flags)}** |")
    lines.append(f"")

    # Category Breakdown Table
    lines.append(f"---")
    lines.append(f"")
    lines.append(f"## Detection Rate by Category")
    lines.append(f"")
    lines.append(f"| Category | Tests | Passed | Pass Rate | Status |")
    lines.append(f"|---|---|---|---|---|")
    for cat, stats in sorted(categories.items()):
        cat_acc = (stats["passed"] / stats["total"] * 100) if stats["total"] > 0 else 0
        icon = "✅" if cat_acc >= 75 else ("🔶" if cat_acc >= 25 else "❌")
        status = "Optimal" if cat_acc >= 75 else ("Moderate" if cat_acc >= 25 else "Blind Spot")
        lines.append(f"| {icon} {cat} | {stats['total']} | {stats['passed']} | **{cat_acc:.0f}%** | {status} |")
    lines.append(f"")

    # Master Table of all 48 results
    lines.append(f"---")
    lines.append(f"")
    lines.append(f"## Complete 48-Variant Results Table")
    lines.append(f"")
    lines.append(f"| ID | Category | Ground Truth Summary | Score | Expected | Status | Time |")
    lines.append(f"|---|---|---|---|---|---|---|")
    for r in results:
        icon = "✅" if r["verdict"]["passed"] else "❌"
        gt_short = (r["ground_truth"][:50] + "...") if len(r["ground_truth"]) > 50 else r["ground_truth"]
        lines.append(
            f"| {icon} **{r['id']}** | {r['category']} | {gt_short} | "
            f"**{r['scores']['overall']:.1f}** | [{r['expected_min']:.1f}–{r['expected_max']:.1f}] | "
            f"{'PASS' if r['verdict']['passed'] else 'FAIL'} | {r['elapsed']:.1f}s |"
        )
    lines.append(f"")

    # Detailed Results for each variant
    lines.append(f"---")
    lines.append(f"")
    lines.append(f"## Detailed Individual Results (V1 – V48)")
    lines.append(f"")

    for r in results:
        icon = "✅" if r["verdict"]["passed"] else "❌"
        lines.append(f"### {icon} {r['id']} — {r['category']}")
        lines.append(f"")
        lines.append(f"**Question:** {r.get('question_text', 'N/A')}")
        lines.append(f"")
        lines.append(f"**Ground Truth:** {r['ground_truth']}")
        lines.append(f"")
        lines.append(f"| Score | Value | Expected Range |")
        lines.append(f"|---|---|---|")
        s = r["scores"]
        lines.append(f"| Completeness | {s['completeness']:.1f} | — |")
        lines.append(f"| Code Quality | {s['code_quality']:.1f} | — |")
        lines.append(f"| Approach | {s['approach']:.1f} | — |")
        lines.append(f"| **Overall** | **{s['overall']:.1f}** | **[{r['expected_min']:.1f} – {r['expected_max']:.1f}]** |")
        lines.append(f"")
        lines.append(f"**Verdict:** {r['verdict']['reason']}")
        lines.append(f"")
        lines.append(f"**Model Feedback:**")
        lines.append(f"> {s['feedback']}")
        lines.append(f"")

        if r.get("summary"):
            summ = r["summary"]
            lines.append(f"**Summary Review:** Quality={summ.get('label','N/A')}, AvgScore={summ.get('avg_score','N/A')}")
            if summ.get("common_errors"):
                lines.append(f"  - Common Errors: {summ['common_errors']}")
            if summ.get("weaknesses"):
                lines.append(f"  - Weaknesses: {summ['weaknesses']}")
            lines.append(f"")

        lines.append(f"**Response Latency:** {r['elapsed']:.1f}s")
        lines.append(f"")

        if r.get("blind_spots"):
            for flag in r["blind_spots"]:
                lines.append(f"> [!WARNING]")
                lines.append(f"> {flag}")
                lines.append(f"")

        if r.get("error"):
            lines.append(f"> [!CAUTION]")
            lines.append(f"> API Error: {r['error']}")
            lines.append(f"")

        lines.append(f"---")
        lines.append(f"")

    # Blind Spots Summary Section
    if all_flags:
        lines.append(f"## ⚠️ Comprehensive Blind Spot Flags")
        lines.append(f"")
        for i, flag in enumerate(all_flags, 1):
            lines.append(f"{i}. {flag}")
        lines.append(f"")

    return "\n".join(lines)


def main():
    print("=" * 75)
    print("  QWEN Code Evaluator — Unified Master Automation Test Suite")
    print(f"  {len(TEST_CASES)} Test Cases | Target Endpoint: {REVIEW_ENDPOINT}")
    print("=" * 75)
    print()

    # Check server availability
    try:
        r = requests.get(API_BASE, timeout=5)
        print(f"✅ Live FastAPI server is reachable (HTTP {r.status_code})")
    except Exception as e:
        print(f"❌ Cannot reach server at {API_BASE}: {e}")
        print("   Please make sure the server is running: uvicorn main:app --reload")
        sys.exit(1)

    print()
    results = []
    suite_start = time.perf_counter()

    for i, tc in enumerate(TEST_CASES, 1):
        print(f"[{i:2d}/{len(TEST_CASES)}] {tc['id']} — {tc['category']}", end="", flush=True)

        response = send_review_request(tc)
        elapsed = response.get("_elapsed_seconds", 0)

        if "_error" in response:
            print(f"  ❌ ERROR: {response['_error']} ({elapsed:.1f}s)")
            results.append({
                "id": tc["id"],
                "category": tc["category"],
                "question_text": tc["question_text"],
                "ground_truth": tc["ground_truth"],
                "expected_min": tc["expected_overall_min"],
                "expected_max": tc["expected_overall_max"],
                "scores": {"completeness": -1, "code_quality": -1, "approach": -1, "overall": -1, "feedback": ""},
                "summary": {},
                "verdict": {"passed": False, "reason": f"API Error: {response['_error']}"},
                "blind_spots": [],
                "elapsed": elapsed,
                "error": response["_error"],
            })
            continue

        scores = extract_scores(response)
        summary = extract_summary(response)
        verdict = evaluate_result(tc, scores)
        blind_spots = detect_blind_spots(tc, scores)

        icon = "✅" if verdict["passed"] else "❌"
        print(
            f"  {icon} overall={scores['overall']:.1f} "
            f"[{tc['expected_overall_min']:.1f}-{tc['expected_overall_max']:.1f}] "
            f"({elapsed:.1f}s)"
        )
        if blind_spots:
            for flag in blind_spots:
                print(f"      {flag}")

        results.append({
            "id": tc["id"],
            "category": tc["category"],
            "question_text": tc["question_text"],
            "ground_truth": tc["ground_truth"],
            "expected_min": tc["expected_overall_min"],
            "expected_max": tc["expected_overall_max"],
            "scores": scores,
            "summary": summary,
            "verdict": verdict,
            "blind_spots": blind_spots,
            "elapsed": elapsed,
            "error": None,
            "raw_response": response,
        })

    suite_time = time.perf_counter() - suite_start

    passed = sum(1 for r in results if r["verdict"]["passed"])
    failed = len(results) - passed
    accuracy = (passed / len(results) * 100) if results else 0

    print()
    print("=" * 75)
    print(f"  MASTER RESULTS: {passed}/{len(results)} passed ({accuracy:.1f}% accuracy)")
    print(f"  Total Suite Execution Time: {suite_time:.1f}s (~{suite_time/60:.1f} minutes)")
    print("=" * 75)

    # Generate consolidated report
    report = generate_report(results, suite_time)
    os.makedirs(os.path.dirname(REPORT_PATH), exist_ok=True)
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"\n📄 Consolidated Report saved to: {REPORT_PATH}")

    # Save consolidated raw results
    raw_for_save = []
    for r in results:
        entry = {k: v for k, v in r.items() if k != "raw_response"}
        raw_for_save.append(entry)
    with open(RAW_RESULTS_PATH, "w", encoding="utf-8") as f:
        json.dump(raw_for_save, f, indent=2, default=str)
    print(f"📦 Consolidated Raw Results saved to: {RAW_RESULTS_PATH}")


if __name__ == "__main__":
    main()
