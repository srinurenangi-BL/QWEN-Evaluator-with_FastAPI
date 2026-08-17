from typing import List, Optional
from schemas import CodeSubmission, DEFAULT_TARGET_LANGUAGE


def format_submission_block(
    question_text: str,
    student_code: str,
    return_answer: Optional[str] = None,
    specific_instructions: Optional[str] = None,
    index: Optional[int] = None,
) -> str:
    """Format an individual submission into clearly demarcated sections for question, return specification, and student code."""
    header = f"--- Question {index} ---\n" if index is not None else ""
    parts = [header]
    parts.append(f"QUESTION / PROBLEM STATEMENT:\n{question_text.strip()}")

    if return_answer:
        parts.append(f"EXPECTED RETURN / OUTPUT SPECIFICATION:\n{return_answer.strip()}")

    if specific_instructions:
        parts.append(f"SPECIFIC INSTRUCTIONS & CONSTRAINTS:\n{specific_instructions.strip()}")

    parts.append(f"STUDENT'S SUBMITTED CODE:\n{student_code.strip()}")
    return "\n\n".join([p for p in parts if p])


def format_submissions(submissions: List[CodeSubmission]) -> str:
    """Format a list of CodeSubmission objects into distinct question/answer blocks."""
    blocks = []
    for i, sub in enumerate(submissions, start=1):
        idx = i if len(submissions) > 1 else None
        blocks.append(
            format_submission_block(
                question_text=sub.question_text,
                student_code=sub.code,
                return_answer=getattr(sub, "return_answer", None),
                specific_instructions=sub.specific_instructions,
                index=idx,
            )
        )
    return "\n\n".join(blocks)


def build_unified_evaluation_prompt(
    target_language: str = DEFAULT_TARGET_LANGUAGE,
    question_text: Optional[str] = None,
    student_code: Optional[str] = None,
    return_answer: Optional[str] = None,
    specific_instructions: Optional[str] = None,
    submissions: Optional[List[CodeSubmission]] = None,
    ques_ans_content_with_inst: Optional[str] = None,
    summary_gen_flag: bool = True,
) -> str:
    """
    Build the unified single-pass evaluation prompt.
    Accepts individual variables (question_text, student_code, return_answer, specific_instructions),
    a structured list of submissions, or a pre-formatted string for full backward compatibility.
    """
    # 1. Resolve content block from separate variables or pre-formatted input
    if question_text and student_code:
        content_block = format_submission_block(
            question_text=question_text,
            student_code=student_code,
            return_answer=return_answer,
            specific_instructions=specific_instructions,
        )
    elif submissions:
        content_block = format_submissions(submissions)
    elif ques_ans_content_with_inst:
        content_block = ques_ans_content_with_inst
    else:
        content_block = "No code submissions provided."

    return f"""You are an expert, rigorous, and deterministic automated code grader.
Your task is to evaluate the submitted code strictly against the target programming language and question requirements.

EXPECTED TARGET LANGUAGE: {target_language}

SUBMISSIONS TO EVALUATE:
{content_block}

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
    question_text: Optional[str] = None,
    student_code: Optional[str] = None,
    return_answer: Optional[str] = None,
    specific_instructions: Optional[str] = None,
    submissions: Optional[List[CodeSubmission]] = None,
    ques_ans_content_with_inst: Optional[str] = None,
    summary_gen_flag: bool = True,
) -> str:
    """Evaluation prompt builder wrapper."""
    return build_unified_evaluation_prompt(
        target_language=target_language,
        question_text=question_text,
        student_code=student_code,
        return_answer=return_answer,
        specific_instructions=specific_instructions,
        submissions=submissions,
        ques_ans_content_with_inst=ques_ans_content_with_inst,
        summary_gen_flag=summary_gen_flag,
    )


def build_language_detection_prompt(target_language: str, code: str) -> str:
    return f"""You are a programming language detector.
Check if this code is in {target_language}:
{code}
Return JSON only: {{"match": true/false, "detected_language": "name"}}"""