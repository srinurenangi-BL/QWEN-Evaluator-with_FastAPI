from typing import List, Optional
from schemas import CodeSubmission, DEFAULT_TARGET_LANGUAGE


def format_submissions(submissions: List[CodeSubmission]) -> str:
    parts = []
    for i, sub in enumerate(submissions, start=1):
        block = f"--- Question {i} ---\n"
        block += f"QUESTION: {sub.question_text}\n"
        if sub.specific_instructions:
            block += f"SPECIFIC INSTRUCTIONS: {sub.specific_instructions}\n"
        block += f"CODE:\n{sub.code}"
        parts.append(block)
    return "\n\n".join(parts)


def build_unified_evaluation_prompt(
    target_language: str = DEFAULT_TARGET_LANGUAGE,
    ques_ans_content_with_inst: str = "",
    summary_gen_flag: bool = True,
) -> str:
    return f"""You are an expert, rigorous, and deterministic automated code grader.
Your task is to evaluate the submitted code strictly against the target programming language and question requirements.

EXPECTED TARGET LANGUAGE: {target_language}

SUBMISSIONS TO EVALUATE:
{ques_ans_content_with_inst}

============================================================
EVALUATION PROTOCOL & SCORING RULES (MANDATORY):
============================================================

1. LANGUAGE VALIDATION GATE:
   - Check if the code is written in {target_language}.
   - If written in a DIFFERENT language (e.g., Python/C++ when {target_language} is requested):
     Set all scores (completeness, quality, approach, overall) to 0.0.
     In correctness_feedback state: "Language Mismatch: Submitted code is written in [Detected] instead of {target_language}."

2. SYNTAX & COMPILATION INTEGRITY:
   - Carefully inspect {target_language} syntax: missing semicolons, unmatched braces/parentheses, void methods returning values, invalid type conversions, undefined/misspelled identifiers, or missing class/wrapper declarations.
   - If code HAS SYNTAX/COMPILE ERRORS:
     * completeness_score MUST BE between 0.0 and 2.0 (DO NOT award 6+ to uncompilable code).
     * overall_score MUST BE <= 3.5.
     * correctness_feedback sentence 1 MUST name the exact syntax error.

3. EXECUTION, LOOP SAFETY & COMPLETENESS:
   - Infinite Loops/Recursion: Check while/for loops for variable increment/decrement. If loop variable never changes or recursion has no valid base case (hangs/infinite loop), completeness_score MUST BE <= 2.0.
   - Dead Code / Uncalled Methods: If a helper function solves the problem but is never called/printed in the main entry point (producing no output), completeness_score MUST BE <= 3.0.
   - Mismatched Problem: If code solves a different problem (e.g. prints largest instead of 2nd-largest, prints LCM instead of GCD), completeness_score MUST BE <= 3.0.
   - Empty / Stub Code: If submission contains only comments, TODOs, or empty boilerplate, completeness_score MUST BE <= 1.0.
   - Edge Cases & Logic Bugs: If code has subtle runtime bugs (off-by-one bounds, array index out of bounds, missing duplicate guards, wrong initial values), completeness_score should be 4.0 to 6.5.

4. SEPARATION OF STYLE VS CORRECTNESS:
   - If code logic is 100% correct but minified, compressed onto one line, or has poor variable names:
     * completeness_score MUST BE 9.0 - 10.0 (do NOT penalize correctness for style).
     * Deduct ONLY from code_quality_score (e.g. 4.0 - 6.0).

5. FORMULA & FEEDBACK FORMAT:
   - Scores must be floats between 0.0 and 10.0.
   - overall_score = (0.5 * completeness_score) + (0.3 * code_quality_score) + (0.2 * approach_taken_score)
   - correctness_feedback MUST be exactly 2 concise, factual sentences.
     Sentence 1: State whether the code compiles and solves the problem correctly, identifying any exact bug/syntax error.
     Sentence 2: Suggest a specific technical improvement or confirm optimality.

============================================================
OUTPUT FORMAT (JSON ONLY, NO MARKDOWN, NO FLUFF):
============================================================
{{
    "language_match": true,
    "detected_language": "{target_language}",
    "individual_reviews": [
        {{
            "question_text": "...",
            "correctness_feedback": "Sentence 1. Sentence 2.",
            "scores": {{
                "completeness_score": 0.0,
                "code_quality_score": 0.0,
                "approach_taken_score": 0.0,
                "overall_score": 0.0
            }}
        }}
    ],
    "summary_review": {{
        "overall_average_score": 0.0,
        "overall_quality_label": "Critical | Poor | Average | Good | Excellent",
        "common_errors": "Brief summary of errors or None",
        "strengths": "Key strengths",
        "weaknesses": "Key weaknesses",
        "recommendations": "Key recommendations"
    }}
}}"""


def build_evaluation_prompt(
    target_language: str = DEFAULT_TARGET_LANGUAGE,
    ques_ans_content_with_inst: str = "",
    summary_gen_flag: bool = True,
) -> str:
    return build_unified_evaluation_prompt(
        target_language=target_language,
        ques_ans_content_with_inst=ques_ans_content_with_inst,
        summary_gen_flag=summary_gen_flag,
    )


def build_language_detection_prompt(target_language: str, code: str) -> str:
    return f"""You are a programming language detector.
Check if this code is in {target_language}:
{code}
Return JSON only: {{"match": true/false, "detected_language": "name"}}"""