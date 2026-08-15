"""
test_runner_batch2.py — Automation test runner for Batch 2 (Multi-Question)

5 different Java questions × 4 variants = 20 test cases.
Re-tests confirmed blind spots on fresh, unseen code.

Usage: python tests/test_runner_batch2.py
(Server must be running on http://127.0.0.1:8000)
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
from tests.test_data_batch2 import TEST_CASES_BATCH2, QUESTIONS, VARIANT_QUESTION_MAP

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
API_BASE = "http://127.0.0.1:8000"
REVIEW_ENDPOINT = f"{API_BASE}/review"
TIMEOUT_PER_REQUEST = 320

REPORT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "tests")
REPORT_PATH = os.path.join(REPORT_DIR, "test_report_batch2.md")
RAW_RESULTS_PATH = os.path.join(REPORT_DIR, "raw_results_batch2.json")


def send_review_request(test_case: dict) -> dict:
    """Send a single test case to the /review endpoint."""
    # Look up the question text for this variant
    q_key = VARIANT_QUESTION_MAP.get(test_case["id"], "Q1")
    question_text = QUESTIONS[q_key]

    payload = {
        "target_language": test_case["target_language"],
        "submissions": [
            {
                "question_text": question_text,
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
    """Pull individual review scores from the API response."""
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
            "completeness": -1, "code_quality": -1, "approach": -1,
            "overall": -1, "feedback": "(failed to parse)",
        }


def extract_summary(response: dict) -> dict:
    """Pull summary review from the API response."""
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
    """Check if the model's scores fall within expected range."""
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
    """Flag known blind-spot patterns."""
    flags = []
    vid = test_case["id"]
    overall = scores["overall"]
    feedback = scores["feedback"].lower()

    # Broken variants for this batch
    broken_variants = {"V20", "V21", "V22", "V24", "V25", "V28", "V29", "V32", "V33", "V34", "V36", "V37", "V38"}
    correct_variants = {"V19", "V23", "V26", "V27", "V31", "V35"}

    if vid in broken_variants and overall >= 7.0:
        flags.append(f"⚠️ FALSE POSITIVE: {vid} scored {overall:.1f} — model may have missed the bug")

    if vid in broken_variants:
        praise_words = ["correct", "efficient", "best practices", "well-written", "no issues"]
        found_praise = [w for w in praise_words if w in feedback]
        if found_praise:
            flags.append(f"⚠️ PRAISE ON BROKEN CODE: {vid} feedback contains: {', '.join(found_praise)}")

    if vid in correct_variants and overall < 5.0:
        flags.append(f"⚠️ FALSE NEGATIVE: {vid} scored {overall:.1f} — model penalized correct code")

    # Specific blind spot re-tests
    if vid == "V22" and overall >= 6.0:
        flags.append(f"⚠️ BLIND SPOT RETEST: V22 (infinite loop) scored {overall:.1f} — still missed?")
    if vid == "V34" and overall >= 6.0:
        flags.append(f"⚠️ BLIND SPOT RETEST: V34 (infinite recursion) scored {overall:.1f} — still missed?")
    if vid == "V20" and overall >= 5.0:
        flags.append(f"⚠️ BLIND SPOT RETEST: V20 (syntax error) scored {overall:.1f} — still missed?")
    if vid == "V25" and overall >= 5.0:
        flags.append(f"⚠️ BLIND SPOT RETEST: V25 (void+return) scored {overall:.1f} — still missed?")
    if vid == "V29" and overall >= 5.0:
        flags.append(f"⚠️ BLIND SPOT RETEST: V29 (missing brace) scored {overall:.1f} — still missed?")
    if vid == "V37" and overall >= 5.0:
        flags.append(f"⚠️ BLIND SPOT RETEST: V37 (variable typo) scored {overall:.1f} — still missed?")
    if vid == "V28" and overall >= 7.0:
        flags.append(f"⚠️ BLIND SPOT RETEST: V28 (space as consonant) scored {overall:.1f} — same as prior vowel test?")
    if vid == "V26" and overall < 5.0:
        flags.append(f"⚠️ BLIND SPOT RETEST: V26 (ugly but correct) scored {overall:.1f} — still penalized?")

    return flags


def generate_report(results: list, total_time: float) -> str:
    """Generate the full markdown test report."""
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

    # Question breakdown
    question_results = {}
    for r in results:
        q_key = VARIANT_QUESTION_MAP.get(r["id"], "?")
        if q_key not in question_results:
            question_results[q_key] = {"total": 0, "passed": 0, "variants": []}
        question_results[q_key]["total"] += 1
        if r["verdict"]["passed"]:
            question_results[q_key]["passed"] += 1
        question_results[q_key]["variants"].append(r)

    lines = []
    lines.append(f"# 📊 QWEN Evaluator — Batch 2 Test Report (Multi-Question)")
    lines.append(f"")
    lines.append(f"**Generated:** {now}")
    lines.append(f"**Model:** qwen2.5-coder:7b-instruct")
    lines.append(f"**Test Suite:** 5 Questions × 4 Variants = 20 Test Cases")
    lines.append(f"**Total Runtime:** {total_time:.1f}s")
    lines.append(f"")
    lines.append(f"---")
    lines.append(f"")

    # Summary
    lines.append(f"## Overall Results")
    lines.append(f"")
    lines.append(f"| Metric | Value |")
    lines.append(f"|---|---|")
    lines.append(f"| Total Tests | {total} |")
    lines.append(f"| ✅ Passed | {passed} |")
    lines.append(f"| ❌ Failed | {failed} |")
    lines.append(f"| Accuracy | **{accuracy:.1f}%** |")
    lines.append(f"| Avg Response Time | {avg_time:.1f}s |")
    lines.append(f"| Min / Max Response Time | {min_time:.1f}s / {max_time:.1f}s |")
    lines.append(f"| Blind Spot Flags | {len(all_flags)} |")
    lines.append(f"")

    # Question breakdown
    lines.append(f"---")
    lines.append(f"")
    lines.append(f"## Per-Question Breakdown")
    lines.append(f"")
    lines.append(f"| Question | Topic | Tests | Passed | Accuracy |")
    lines.append(f"|---|---|---|---|---|")
    q_names = {
        "Q1": "Reverse a String",
        "Q2": "Prime Number Check",
        "Q3": "Vowel/Consonant Counter",
        "Q4": "GCD (Euclidean)",
        "Q5": "Array Sorted Check",
    }
    for q_key in sorted(question_results.keys()):
        qr = question_results[q_key]
        q_acc = (qr["passed"] / qr["total"] * 100) if qr["total"] > 0 else 0
        icon = "✅" if q_acc >= 75 else ("🔶" if q_acc >= 25 else "❌")
        lines.append(f"| {icon} {q_key} | {q_names.get(q_key, '?')} | {qr['total']} | {qr['passed']} | {q_acc:.0f}% |")
    lines.append(f"")

    # Category breakdown
    lines.append(f"---")
    lines.append(f"")
    lines.append(f"## Category Breakdown")
    lines.append(f"")
    lines.append(f"| Category | Tests | Passed | Accuracy |")
    lines.append(f"|---|---|---|---|")
    for cat, stats in sorted(categories.items()):
        cat_acc = (stats["passed"] / stats["total"] * 100) if stats["total"] > 0 else 0
        icon = "✅" if cat_acc == 100 else ("🔶" if cat_acc > 0 else "❌")
        lines.append(f"| {icon} {cat} | {stats['total']} | {stats['passed']} | {cat_acc:.0f}% |")
    lines.append(f"")

    # Detailed results
    lines.append(f"---")
    lines.append(f"")
    lines.append(f"## Detailed Results")
    lines.append(f"")

    for r in results:
        icon = "✅" if r["verdict"]["passed"] else "❌"
        q_key = VARIANT_QUESTION_MAP.get(r["id"], "?")
        lines.append(f"### {icon} {r['id']} ({q_key}) — {r['category']}")
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

        lines.append(f"**Response Time:** {r['elapsed']:.1f}s")
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

    # Blind spots summary
    if all_flags:
        lines.append(f"## ⚠️ Blind Spot Summary")
        lines.append(f"")
        for i, flag in enumerate(all_flags, 1):
            lines.append(f"{i}. {flag}")
        lines.append(f"")

    # Cross-batch comparison
    lines.append(f"---")
    lines.append(f"")
    lines.append(f"## Cross-Batch Comparison (Batch 1 vs Batch 2)")
    lines.append(f"")
    lines.append(f"### Syntax/Compile Error Detection")
    lines.append(f"")
    lines.append(f"| Variant | Bug Type | Batch | Score | Caught? |")
    lines.append(f"|---|---|---|---|---|")

    # Batch 1 syntax errors (from prior run)
    lines.append(f"| V2 | No class wrapper | B1 | 7.5 | ❌ |")
    lines.append(f"| V9 | Missing brace | B1 | 6.4 | ❌ |")
    lines.append(f"| V10 | Missing semicolon | B1 | 7.4 | ❌ |")
    lines.append(f"| V11 | void+return | B1 | 7.4 | ❌ |")
    lines.append(f"| V13 | Case typo | B1 | 5.1 | ❌ |")

    # Batch 2 syntax errors
    syntax_ids = {"V20", "V25", "V29", "V37"}
    for r in results:
        if r["id"] in syntax_ids:
            caught = "✅" if r["scores"]["overall"] <= 4.0 else "❌"
            lines.append(f"| {r['id']} | {r['category']} | B2 | {r['scores']['overall']:.1f} | {caught} |")

    lines.append(f"")
    lines.append(f"### Infinite Loop / Hang Detection")
    lines.append(f"")
    lines.append(f"| Variant | Bug Type | Batch | Score | Caught? |")
    lines.append(f"|---|---|---|---|---|")
    lines.append(f"| V12 | Missing i++ (while) | B1 | 7.4 | ❌ |")

    hang_ids = {"V22", "V34"}
    for r in results:
        if r["id"] in hang_ids:
            caught = "✅" if r["scores"]["overall"] <= 4.0 else "❌"
            lines.append(f"| {r['id']} | {r['category']} | B2 | {r['scores']['overall']:.1f} | {caught} |")

    lines.append(f"")
    lines.append(f"### Shape-Correct Bug Detection")
    lines.append(f"")
    lines.append(f"| Variant | Bug Type | Batch | Score | Caught? |")
    lines.append(f"|---|---|---|---|---|")
    lines.append(f"| V5 | Off-by-one | B1 | 6.3 | ❌ |")
    lines.append(f"| V6 | Missing dup guard | B1 | 7.4 | ❌ |")
    lines.append(f"| V17 | Bad init value | B1 | 6.0 | ✅ |")

    shape_ids = {"V21", "V24", "V28", "V36"}
    for r in results:
        if r["id"] in shape_ids:
            exp_max = r["expected_max"]
            caught = "✅" if r["scores"]["overall"] <= exp_max else "❌"
            lines.append(f"| {r['id']} | {r['category']} | B2 | {r['scores']['overall']:.1f} | {caught} |")

    lines.append(f"")
    lines.append(f"---")
    lines.append(f"")
    lines.append(f"*Report generated by automated test runner (Batch 2). "
                  f"All results are from live API calls to the QWEN evaluator.*")

    return "\n".join(lines)


def main():
    print("=" * 70)
    print("  QWEN Code Evaluator — Batch 2: Multi-Question Test Suite")
    print(f"  {len(TEST_CASES_BATCH2)} test cases | 5 questions | Target: {REVIEW_ENDPOINT}")
    print("=" * 70)
    print()

    # Check server
    try:
        r = requests.get(API_BASE, timeout=5)
        print(f"✅ Server is reachable (HTTP {r.status_code})")
    except Exception as e:
        print(f"❌ Cannot reach server at {API_BASE}: {e}")
        print("   Make sure the server is running: uvicorn main:app --reload")
        sys.exit(1)

    print()
    results = []
    suite_start = time.perf_counter()

    for i, tc in enumerate(TEST_CASES_BATCH2, 1):
        q_key = VARIANT_QUESTION_MAP.get(tc["id"], "?")
        print(f"[{i:2d}/{len(TEST_CASES_BATCH2)}] {tc['id']} ({q_key}) — {tc['category']}", end="", flush=True)

        response = send_review_request(tc)
        elapsed = response.get("_elapsed_seconds", 0)

        if "_error" in response:
            print(f"  ❌ ERROR: {response['_error']} ({elapsed:.1f}s)")
            results.append({
                "id": tc["id"],
                "category": tc["category"],
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
    print("=" * 70)
    print(f"  RESULTS: {passed}/{len(results)} passed ({accuracy:.1f}% accuracy)")
    print(f"  Total time: {suite_time:.1f}s")
    print("=" * 70)

    # Generate report
    report = generate_report(results, suite_time)
    os.makedirs(os.path.dirname(REPORT_PATH), exist_ok=True)
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"\n📄 Report saved to: {REPORT_PATH}")

    # Save raw results
    raw_for_save = []
    for r in results:
        entry = {k: v for k, v in r.items() if k != "raw_response"}
        raw_for_save.append(entry)
    with open(RAW_RESULTS_PATH, "w", encoding="utf-8") as f:
        json.dump(raw_for_save, f, indent=2, default=str)
    print(f"📦 Raw results saved to: {RAW_RESULTS_PATH}")


if __name__ == "__main__":
    main()
