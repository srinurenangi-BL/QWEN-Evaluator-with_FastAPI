"""
test_runner.py — Automation test runner for QWEN Code Evaluator

Sends all 18 variants to the /review API, validates scores against expected ranges,
detects blind spots, and generates a comprehensive markdown report.

Usage: python tests/test_runner.py
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
from tests.test_data import TEST_CASES, QUESTION_TEXT

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
API_BASE = "http://127.0.0.1:8000"
REVIEW_ENDPOINT = f"{API_BASE}/review"
TIMEOUT_PER_REQUEST = 320  # seconds

# Output paths
REPORT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORT_PATH = os.path.join(REPORT_DIR, "tests", "test_report.md")
RAW_RESULTS_PATH = os.path.join(REPORT_DIR, "tests", "raw_results.json")


def send_review_request(test_case: dict) -> dict:
    """Send a single test case to the /review endpoint and return the full response."""
    payload = {
        "target_language": test_case["target_language"],
        "submissions": [
            {
                "question_text": QUESTION_TEXT,
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
            "completeness": -1,
            "code_quality": -1,
            "approach": -1,
            "overall": -1,
            "feedback": "(failed to parse)",
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
    """Check if the model's scores fall within expected range. Return pass/fail + reasoning."""
    overall = scores["overall"]
    exp_min = test_case["expected_overall_min"]
    exp_max = test_case["expected_overall_max"]

    if overall < 0:
        return {
            "passed": False,
            "reason": "Failed to extract overall score from response.",
        }

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

    # Blind spot: Model says "correct" on broken code
    broken_variants = {"V2", "V4", "V5", "V6", "V7", "V9", "V10", "V11", "V12", "V13", "V16"}
    if vid in broken_variants and overall >= 7.0:
        flags.append(f"⚠️ FALSE POSITIVE: {vid} scored {overall:.1f} — model may have missed the bug")

    # Blind spot: "correct" / "efficient" / "best practices" on broken code
    if vid in broken_variants:
        praise_words = ["correct", "efficient", "best practices", "well-written", "no issues"]
        found_praise = [w for w in praise_words if w in feedback]
        if found_praise:
            flags.append(
                f"⚠️ PRAISE ON BROKEN CODE: {vid} feedback contains: {', '.join(found_praise)}"
            )

    # Blind spot: Model penalizes correct code
    correct_variants = {"V1", "V14", "V18"}
    if vid in correct_variants and overall < 5.0:
        flags.append(f"⚠️ FALSE NEGATIVE: {vid} scored {overall:.1f} — model penalized correct code")

    # Key test: V17 (known Kadane-style init bug blind spot)
    if vid == "V17" and overall >= 7.5:
        flags.append(
            f"⚠️ CONFIRMED BLIND SPOT: V17 scored {overall:.1f} — model missed 0-init bug "
            f"(same failure pattern as Kadane's in prior tests)"
        )

    # Key test: V12 (infinite loop — correct shape trap)
    if vid == "V12" and overall >= 6.0:
        flags.append(
            f"⚠️ CONFIRMED BLIND SPOT: V12 scored {overall:.1f} — model missed infinite loop "
            f"(code body is correct, only missing i++)"
        )

    return flags


def generate_report(results: list, total_time: float) -> str:
    """Generate the full markdown test report."""
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    total = len(results)
    passed = sum(1 for r in results if r["verdict"]["passed"])
    failed = total - passed
    accuracy = (passed / total * 100) if total > 0 else 0

    # Collect all blind spot flags
    all_flags = []
    for r in results:
        all_flags.extend(r.get("blind_spots", []))

    # Response time stats
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

    # Build report
    lines = []
    lines.append(f"# 📊 QWEN Evaluator — Automation Test Report")
    lines.append(f"")
    lines.append(f"**Generated:** {now}")
    lines.append(f"**Model:** qwen2.5-coder:7b-instruct")
    lines.append(f"**Test Suite:** 18 Variants — Second Largest Distinct Element")
    lines.append(f"**Total Runtime:** {total_time:.1f}s")
    lines.append(f"")
    lines.append(f"---")
    lines.append(f"")

    # Summary box
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
        lines.append(f"### {icon} {r['id']} — {r['category']}")
        lines.append(f"")
        lines.append(f"**Ground Truth:** {r['ground_truth']}")
        lines.append(f"")
        lines.append(f"| Score | Value | Expected Range |")
        lines.append(f"|---|---|---|")
        s = r["scores"]
        lines.append(f"| Completeness | {s['completeness']:.1f} | — |")
        lines.append(f"| Code Quality | {s['code_quality']:.1f} | — |")
        lines.append(f"| Approach | {s['approach']:.1f} | — |")
        lines.append(
            f"| **Overall** | **{s['overall']:.1f}** | "
            f"**[{r['expected_min']:.1f} – {r['expected_max']:.1f}]** |"
        )
        lines.append(f"")
        lines.append(f"**Verdict:** {r['verdict']['reason']}")
        lines.append(f"")
        lines.append(f"**Model Feedback:**")
        lines.append(f"> {s['feedback']}")
        lines.append(f"")

        # Summary review info
        if r.get("summary"):
            summ = r["summary"]
            lines.append(f"**Summary Review:** Quality={summ.get('label','N/A')}, "
                         f"AvgScore={summ.get('avg_score','N/A')}")
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
        lines.append(f"The following issues were flagged during testing:")
        lines.append(f"")
        for i, flag in enumerate(all_flags, 1):
            lines.append(f"{i}. {flag}")
        lines.append(f"")

    # Cross-confirmation section
    lines.append(f"---")
    lines.append(f"")
    lines.append(f"## Cross-Confirmation Against Prior Model Profile")
    lines.append(f"")
    lines.append(f"### Previously Confirmed Strengths")
    lines.append(f"")

    # Check V15 (wrong language)
    v15 = next((r for r in results if r["id"] == "V15"), None)
    if v15:
        v15_ok = v15["scores"]["overall"] == 0.0
        lines.append(f"- **Wrong-language detection:** {'✅ CONFIRMED' if v15_ok else '❌ FAILED'} "
                      f"(V15 scored {v15['scores']['overall']:.1f})")

    # Check V8 (mismatched problem)
    v8 = next((r for r in results if r["id"] == "V8"), None)
    if v8:
        v8_ok = v8["scores"]["overall"] <= 3.0
        lines.append(f"- **Mismatched-question detection:** {'✅ CONFIRMED' if v8_ok else '❌ FAILED'} "
                      f"(V8 scored {v8['scores']['overall']:.1f})")

    lines.append(f"")
    lines.append(f"### Previously Identified Blind Spots")
    lines.append(f"")

    # Check V17 (known 0-init blind spot)
    v17 = next((r for r in results if r["id"] == "V17"), None)
    if v17:
        v17_missed = v17["scores"]["overall"] >= 7.5
        lines.append(
            f"- **Bad init value (0 instead of MIN_VALUE):** "
            f"{'⚠️ BLIND SPOT CONFIRMED — still missed' if v17_missed else '✅ IMPROVEMENT — caught this time'} "
            f"(V17 scored {v17['scores']['overall']:.1f})"
        )

    # Check V12 (infinite loop)
    v12 = next((r for r in results if r["id"] == "V12"), None)
    if v12:
        v12_missed = v12["scores"]["overall"] >= 6.0
        lines.append(
            f"- **Infinite loop (correct shape, missing i++):** "
            f"{'⚠️ BLIND SPOT CONFIRMED — still missed' if v12_missed else '✅ CAUGHT — detected missing increment'} "
            f"(V12 scored {v12['scores']['overall']:.1f})"
        )

    # Check V5 (off-by-one)
    v5 = next((r for r in results if r["id"] == "V5"), None)
    if v5:
        v5_missed = v5["scores"]["overall"] >= 7.0
        lines.append(
            f"- **Off-by-one (i < n-1):** "
            f"{'⚠️ BLIND SPOT — missed' if v5_missed else '✅ CAUGHT — detected skipped last element'} "
            f"(V5 scored {v5['scores']['overall']:.1f})"
        )

    # Check V6 (missing duplicate guard)
    v6 = next((r for r in results if r["id"] == "V6"), None)
    if v6:
        v6_missed = v6["scores"]["overall"] >= 7.0
        lines.append(
            f"- **Missing duplicate guard:** "
            f"{'⚠️ BLIND SPOT — missed' if v6_missed else '✅ CAUGHT — detected missing != largest check'} "
            f"(V6 scored {v6['scores']['overall']:.1f})"
        )

    lines.append(f"")
    lines.append(f"### New Findings From This Batch")
    lines.append(f"")

    # Check structural issues (V2, V3, V4, V9-V13)
    structural_ids = ["V2", "V3", "V4", "V9", "V10", "V11", "V13"]
    caught_structural = 0
    for vid in structural_ids:
        vr = next((r for r in results if r["id"] == vid), None)
        if vr and vr["scores"]["overall"] <= 4.0:
            caught_structural += 1
    lines.append(f"- **Structural/compile errors (V2,V3,V4,V9-V11,V13):** "
                  f"Caught {caught_structural}/{len(structural_ids)}")

    # Check V14 (style vs correctness separation)
    v14 = next((r for r in results if r["id"] == "V14"), None)
    if v14:
        s14 = v14["scores"]
        style_separated = s14["completeness"] > s14["code_quality"]
        lines.append(
            f"- **Style vs correctness separation (V14):** "
            f"{'✅ GOOD — completeness > code_quality' if style_separated else '❌ NOT SEPARATED'} "
            f"(completeness={s14['completeness']:.1f}, code_quality={s14['code_quality']:.1f})"
        )

    # Check V16 (empty stub)
    v16 = next((r for r in results if r["id"] == "V16"), None)
    if v16:
        v16_ok = v16["scores"]["overall"] <= 2.0
        lines.append(f"- **Empty stub detection (V16):** "
                      f"{'✅ CAUGHT' if v16_ok else '❌ MISSED'} "
                      f"(V16 scored {v16['scores']['overall']:.1f})")

    lines.append(f"")
    lines.append(f"---")
    lines.append(f"")
    lines.append(f"*Report generated by automated test runner. "
                 f"All results are from live API calls to the QWEN evaluator.*")

    return "\n".join(lines)


def main():
    print("=" * 70)
    print("  QWEN Code Evaluator — Automation Test Suite")
    print(f"  {len(TEST_CASES)} test cases | Target: {REVIEW_ENDPOINT}")
    print("=" * 70)
    print()

    # Check server is reachable
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

    for i, tc in enumerate(TEST_CASES, 1):
        print(f"[{i:2d}/{len(TEST_CASES)}] {tc['id']} — {tc['category']}", end="", flush=True)

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

    # Print summary
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

    # Save raw results (without raw_response for readability)
    raw_for_save = []
    for r in results:
        entry = {k: v for k, v in r.items() if k != "raw_response"}
        raw_for_save.append(entry)
    with open(RAW_RESULTS_PATH, "w", encoding="utf-8") as f:
        json.dump(raw_for_save, f, indent=2, default=str)
    print(f"📦 Raw results saved to: {RAW_RESULTS_PATH}")


if __name__ == "__main__":
    main()
