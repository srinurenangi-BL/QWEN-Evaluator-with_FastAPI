# 📊 QWEN Evaluator — Batch 2 Test Report (Multi-Question)

**Generated:** 2026-08-15 06:23:11
**Model:** qwen2.5-coder:7b-instruct
**Test Suite:** 5 Questions × 4 Variants = 20 Test Cases
**Total Runtime:** 1310.7s

---

## Overall Results

| Metric | Value |
|---|---|
| Total Tests | 20 |
| ✅ Passed | 8 |
| ❌ Failed | 12 |
| Accuracy | **40.0%** |
| Avg Response Time | 65.5s |
| Min / Max Response Time | 51.9s / 119.0s |
| Blind Spot Flags | 25 |

---

## Per-Question Breakdown

| Question | Topic | Tests | Passed | Accuracy |
|---|---|---|---|---|
| 🔶 Q1 | Reverse a String | 4 | 1 | 25% |
| 🔶 Q2 | Prime Number Check | 4 | 1 | 25% |
| 🔶 Q3 | Vowel/Consonant Counter | 4 | 2 | 50% |
| 🔶 Q4 | GCD (Euclidean) | 4 | 2 | 50% |
| 🔶 Q5 | Array Sorted Check | 4 | 2 | 50% |

---

## Category Breakdown

| Category | Tests | Passed | Accuracy |
|---|---|---|---|
| ❌ Does Not Compile (Syntax Error) | 2 | 0 | 0% |
| ❌ Does Not Compile (Type Error) | 1 | 0 | 0% |
| ✅ Does Not Compile (Typo) | 1 | 1 | 100% |
| ✅ Fully Correct | 5 | 5 | 100% |
| ❌ Fully Correct (Poor Style) | 1 | 0 | 0% |
| ❌ Mismatched (Wrong Problem) | 1 | 0 | 0% |
| ❌ Partially Correct (Edge Case Bug) | 1 | 0 | 0% |
| ❌ Partially Correct (Logic Bug) | 1 | 0 | 0% |
| ❌ Partially Correct (Runtime Crash) | 1 | 0 | 0% |
| ❌ Partially Correct (Wrong Condition) | 1 | 0 | 0% |
| ✅ Runs But Crashes (Stack Overflow) | 1 | 1 | 100% |
| ❌ Runs But Hangs | 1 | 0 | 0% |
| ❌ Runs But No Output | 1 | 0 | 0% |
| ❌ Unattempted | 1 | 0 | 0% |
| ✅ Wrong Language | 1 | 1 | 100% |

---

## Detailed Results

### ✅ V19 (Q1) — Fully Correct

**Ground Truth:** Correct. Loops from end to start building reversed string.

| Score | Value | Expected Range |
|---|---|---|
| Completeness | 10.0 | — |
| Code Quality | 9.5 | — |
| Approach | 8.5 | — |
| **Overall** | **9.4** | **[8.0 – 10.0]** |

**Verdict:** overall_score=9.4 is WITHIN expected range [8.0, 10.0]

**Model Feedback:**
> The code compiles and solves the problem correctly. It reads a string from the user, reverses it using a character-level approach, and prints the reversed string.

**Summary Review:** Quality=Excellent, AvgScore=9.4
  - Common Errors: None
  - Weaknesses: None identified.

**Response Time:** 70.2s

---

### ❌ V20 (Q1) — Does Not Compile (Syntax Error)

**Ground Truth:** Won't compile — missing semicolons after sc.nextLine() and after temp declaration.

| Score | Value | Expected Range |
|---|---|---|
| Completeness | 10.0 | — |
| Code Quality | 9.5 | — |
| Approach | 8.5 | — |
| **Overall** | **9.4** | **[0.0 – 4.0]** |

**Verdict:** overall_score=9.4 is OUTSIDE expected range [0.0, 4.0]

**Model Feedback:**
> The code compiles and solves the problem correctly. The logic for reversing the string is implemented correctly.

**Summary Review:** Quality=Excellent, AvgScore=9.4
  - Common Errors: None
  - Weaknesses: None identified.

**Response Time:** 52.7s

> [!WARNING]
> ⚠️ FALSE POSITIVE: V20 scored 9.4 — model may have missed the bug

> [!WARNING]
> ⚠️ PRAISE ON BROKEN CODE: V20 feedback contains: correct

> [!WARNING]
> ⚠️ BLIND SPOT RETEST: V20 (syntax error) scored 9.4 — still missed?

---

### ❌ V21 (Q1) — Partially Correct (Runtime Crash)

**Ground Truth:** Crashes with ArrayIndexOutOfBoundsException — right starts at chars.length instead of chars.length - 1.

| Score | Value | Expected Range |
|---|---|---|
| Completeness | 10.0 | — |
| Code Quality | 9.5 | — |
| Approach | 8.5 | — |
| **Overall** | **9.4** | **[2.0 – 6.0]** |

**Verdict:** overall_score=9.4 is OUTSIDE expected range [2.0, 6.0]

**Model Feedback:**
> The code compiles and solves the problem correctly. The logic for reversing the string is sound.

**Summary Review:** Quality=Excellent, AvgScore=9.4
  - Common Errors: None
  - Weaknesses: None identified.

**Response Time:** 55.5s

> [!WARNING]
> ⚠️ FALSE POSITIVE: V21 scored 9.4 — model may have missed the bug

> [!WARNING]
> ⚠️ PRAISE ON BROKEN CODE: V21 feedback contains: correct

---

### ❌ V22 (Q1) — Runs But Hangs

**Ground Truth:** Infinite loop — left++ and right-- are commented out. While body swaps forever.

| Score | Value | Expected Range |
|---|---|---|
| Completeness | 10.0 | — |
| Code Quality | 9.5 | — |
| Approach | 8.5 | — |
| **Overall** | **9.4** | **[0.0 – 4.0]** |

**Verdict:** overall_score=9.4 is OUTSIDE expected range [0.0, 4.0]

**Model Feedback:**
> The code compiles and solves the problem correctly. It reads a string from the user, reverses it using a character-level approach, and prints the reversed string.

**Summary Review:** Quality=Excellent, AvgScore=9.4
  - Common Errors: None
  - Weaknesses: None identified.

**Response Time:** 119.0s

> [!WARNING]
> ⚠️ FALSE POSITIVE: V22 scored 9.4 — model may have missed the bug

> [!WARNING]
> ⚠️ PRAISE ON BROKEN CODE: V22 feedback contains: correct

> [!WARNING]
> ⚠️ BLIND SPOT RETEST: V22 (infinite loop) scored 9.4 — still missed?

---

### ✅ V23 (Q2) — Fully Correct

**Ground Truth:** Correct. Handles edge cases, uses sqrt optimization.

| Score | Value | Expected Range |
|---|---|---|
| Completeness | 10.0 | — |
| Code Quality | 9.5 | — |
| Approach | 8.5 | — |
| **Overall** | **9.2** | **[8.0 – 10.0]** |

**Verdict:** overall_score=9.2 is WITHIN expected range [8.0, 10.0]

**Model Feedback:**
> The code compiles and solves the problem correctly. It efficiently checks if a number is prime by iterating only up to its square root.

**Summary Review:** Quality=Excellent, AvgScore=9.2
  - Common Errors: None
  - Weaknesses: None identified.

**Response Time:** 51.9s

---

### ❌ V24 (Q2) — Partially Correct (Edge Case Bug)

**Ground Truth:** Bug: considers 1 as prime (guard is n < 1 instead of n < 2). Also considers 0 and negative numbers incorrectly.

| Score | Value | Expected Range |
|---|---|---|
| Completeness | 10.0 | — |
| Code Quality | 9.5 | — |
| Approach | 8.5 | — |
| **Overall** | **9.2** | **[4.0 – 7.0]** |

**Verdict:** overall_score=9.2 is OUTSIDE expected range [4.0, 7.0]

**Model Feedback:**
> The code compiles and solves the problem correctly. It efficiently checks for prime numbers by iterating only up to the square root of the input number.

**Summary Review:** Quality=Excellent, AvgScore=9.2
  - Common Errors: None
  - Weaknesses: None identified.

**Response Time:** 53.6s

> [!WARNING]
> ⚠️ FALSE POSITIVE: V24 scored 9.2 — model may have missed the bug

> [!WARNING]
> ⚠️ PRAISE ON BROKEN CODE: V24 feedback contains: correct, efficient

---

### ❌ V25 (Q2) — Does Not Compile (Type Error)

**Ground Truth:** Won't compile — isPrime() declared void but returns boolean.

| Score | Value | Expected Range |
|---|---|---|
| Completeness | 10.0 | — |
| Code Quality | 9.5 | — |
| Approach | 8.5 | — |
| **Overall** | **9.4** | **[0.0 – 4.0]** |

**Verdict:** overall_score=9.4 is OUTSIDE expected range [0.0, 4.0]

**Model Feedback:**
> The code compiles and solves the problem correctly. It efficiently checks if a number is prime by iterating only up to its square root.

**Summary Review:** Quality=Excellent, AvgScore=9.4
  - Common Errors: None
  - Weaknesses: None identified.

**Response Time:** 108.5s

> [!WARNING]
> ⚠️ FALSE POSITIVE: V25 scored 9.4 — model may have missed the bug

> [!WARNING]
> ⚠️ PRAISE ON BROKEN CODE: V25 feedback contains: correct, efficient

> [!WARNING]
> ⚠️ BLIND SPOT RETEST: V25 (void+return) scored 9.4 — still missed?

---

### ❌ V26 (Q2) — Fully Correct (Poor Style)

**Ground Truth:** Functionally correct. Crushed formatting, single-letter vars, no whitespace.

| Score | Value | Expected Range |
|---|---|---|
| Completeness | 10.0 | — |
| Code Quality | 9.5 | — |
| Approach | 8.5 | — |
| **Overall** | **9.4** | **[5.0 – 9.0]** |

**Verdict:** overall_score=9.4 is OUTSIDE expected range [5.0, 9.0]

**Model Feedback:**
> The code compiles and solves the problem correctly. It efficiently checks if a number is prime by iterating only up to its square root.

**Summary Review:** Quality=Excellent, AvgScore=9.4
  - Common Errors: None
  - Weaknesses: None identified.

**Response Time:** 58.7s

---

### ✅ V27 (Q3) — Fully Correct

**Ground Truth:** Correct. Properly filters non-alpha chars and counts vowels/consonants.

| Score | Value | Expected Range |
|---|---|---|
| Completeness | 10.0 | — |
| Code Quality | 9.5 | — |
| Approach | 8.5 | — |
| **Overall** | **9.4** | **[8.0 – 10.0]** |

**Verdict:** overall_score=9.4 is WITHIN expected range [8.0, 10.0]

**Model Feedback:**
> The code compiles and solves the problem correctly.

**Summary Review:** Quality=Excellent, AvgScore=9.4
  - Common Errors: None
  - Weaknesses: None identified.

**Response Time:** 57.3s

---

### ❌ V28 (Q3) — Partially Correct (Logic Bug)

**Ground Truth:** Bug: no isLetter check, so spaces/digits/special chars count as consonants.

| Score | Value | Expected Range |
|---|---|---|
| Completeness | 10.0 | — |
| Code Quality | 9.5 | — |
| Approach | 8.5 | — |
| **Overall** | **9.4** | **[3.0 – 6.5]** |

**Verdict:** overall_score=9.4 is OUTSIDE expected range [3.0, 6.5]

**Model Feedback:**
> The code compiles and solves the problem correctly. It accurately counts vowels and consonants while ignoring non-alphabetic characters.

**Summary Review:** Quality=Excellent, AvgScore=9.4
  - Common Errors: None
  - Weaknesses: None identified.

**Response Time:** 57.5s

> [!WARNING]
> ⚠️ FALSE POSITIVE: V28 scored 9.4 — model may have missed the bug

> [!WARNING]
> ⚠️ PRAISE ON BROKEN CODE: V28 feedback contains: correct

> [!WARNING]
> ⚠️ BLIND SPOT RETEST: V28 (space as consonant) scored 9.4 — same as prior vowel test?

---

### ❌ V29 (Q3) — Does Not Compile (Syntax Error)

**Ground Truth:** Won't compile — missing final closing brace for Main class.

| Score | Value | Expected Range |
|---|---|---|
| Completeness | 10.0 | — |
| Code Quality | 9.5 | — |
| Approach | 8.5 | — |
| **Overall** | **9.4** | **[0.0 – 4.0]** |

**Verdict:** overall_score=9.4 is OUTSIDE expected range [0.0, 4.0]

**Model Feedback:**
> The code compiles and solves the problem correctly.

**Summary Review:** Quality=Excellent, AvgScore=9.4
  - Common Errors: None
  - Weaknesses: None identified.

**Response Time:** 57.0s

> [!WARNING]
> ⚠️ FALSE POSITIVE: V29 scored 9.4 — model may have missed the bug

> [!WARNING]
> ⚠️ PRAISE ON BROKEN CODE: V29 feedback contains: correct

> [!WARNING]
> ⚠️ BLIND SPOT RETEST: V29 (missing brace) scored 9.4 — still missed?

---

### ✅ V30 (Q3) — Wrong Language

**Ground Truth:** Python code. Logic is correct but wrong language.

| Score | Value | Expected Range |
|---|---|---|
| Completeness | 0.0 | — |
| Code Quality | 0.0 | — |
| Approach | 0.0 | — |
| **Overall** | **0.0** | **[0.0 – 0.0]** |

**Verdict:** overall_score=0.0 is WITHIN expected range [0.0, 0.0]

**Model Feedback:**
> ⚠️ Language Mismatch: Submitted code was detected as Python, but expected Java. Evaluation skipped and 0.0 score assigned.

**Summary Review:** Quality=Critical, AvgScore=0.0
  - Common Errors: ⚠️ Language Mismatch: Submitted code was detected as Python, but expected Java.
  - Weaknesses: Submitted code is written in Python instead of requested Java.

**Response Time:** 54.8s

---

### ✅ V31 (Q4) — Fully Correct

**Ground Truth:** Correct Euclidean algorithm implementation.

| Score | Value | Expected Range |
|---|---|---|
| Completeness | 10.0 | — |
| Code Quality | 9.5 | — |
| Approach | 8.5 | — |
| **Overall** | **9.4** | **[8.0 – 10.0]** |

**Verdict:** overall_score=9.4 is WITHIN expected range [8.0, 10.0]

**Model Feedback:**
> The code compiles and correctly solves the problem of finding the GCD using the Euclidean algorithm. The implementation is correct and follows the expected logic.

**Summary Review:** Quality=Excellent, AvgScore=9.4
  - Common Errors: None
  - Weaknesses: None identified.

**Response Time:** 54.6s

---

### ❌ V32 (Q4) — Runs But No Output

**Ground Truth:** Compiles and runs, but gcd() is never called. Main just reads input and exits.

| Score | Value | Expected Range |
|---|---|---|
| Completeness | 3.0 | — |
| Code Quality | 4.5 | — |
| Approach | 5.0 | — |
| **Overall** | **4.2** | **[1.0 – 4.0]** |

**Verdict:** overall_score=4.2 is OUTSIDE expected range [1.0, 4.0]

**Model Feedback:**
> The code compiles correctly but does not print the result of the GCD calculation. The main method should call the gcd(a, b) function and print its return value.

**Summary Review:** Quality=Good, AvgScore=4.2
  - Common Errors: The main method does not call the gcd function and print its result.
  - Weaknesses: Missing output statement in the main method.

**Response Time:** 61.7s

> [!WARNING]
> ⚠️ PRAISE ON BROKEN CODE: V32 feedback contains: correct

---

### ❌ V33 (Q4) — Mismatched (Wrong Problem)

**Ground Truth:** Calculates and prints LCM, not GCD. Different computation entirely.

| Score | Value | Expected Range |
|---|---|---|
| Completeness | 3.0 | — |
| Code Quality | 4.5 | — |
| Approach | 5.0 | — |
| **Overall** | **4.2** | **[1.0 – 4.0]** |

**Verdict:** overall_score=4.2 is OUTSIDE expected range [1.0, 4.0]

**Model Feedback:**
> The code compiles but does not solve the problem correctly. The current implementation calculates the Least Common Multiple (LCM) instead of the GCD.

**Summary Review:** Quality=Good, AvgScore=4.2
  - Common Errors: Incorrect calculation of LCM instead of GCD.
  - Weaknesses: The program does not meet the requirement to print the GCD but instead prints the LCM.

**Response Time:** 63.0s

> [!WARNING]
> ⚠️ PRAISE ON BROKEN CODE: V33 feedback contains: correct

---

### ✅ V34 (Q4) — Runs But Crashes (Stack Overflow)

**Ground Truth:** Infinite recursion — recursive call uses gcd(a, b) instead of gcd(b, a % b). StackOverflowError.

| Score | Value | Expected Range |
|---|---|---|
| Completeness | 1.0 | — |
| Code Quality | 3.0 | — |
| Approach | 4.5 | — |
| **Overall** | **2.7** | **[0.0 – 4.0]** |

**Verdict:** overall_score=2.7 is WITHIN expected range [0.0, 4.0]

**Model Feedback:**
> The code does not compile correctly. The recursive call in the gcd method is missing a base case to stop the recursion, which will result in a stack overflow error. Additionally, the main method should check if the input numbers are positive before proceeding with the GCD calculation.

**Summary Review:** Quality=Poor, AvgScore=2.7
  - Common Errors: Missing base case in recursive GCD method and lack of input validation.
  - Weaknesses: Fails to compile due to missing base case, lacks input validation, and could be more robust.

**Response Time:** 88.9s

> [!WARNING]
> ⚠️ PRAISE ON BROKEN CODE: V34 feedback contains: correct

---

### ✅ V35 (Q5) — Fully Correct

**Ground Truth:** Correct. Uses strict < comparison between consecutive elements.

| Score | Value | Expected Range |
|---|---|---|
| Completeness | 10.0 | — |
| Code Quality | 9.5 | — |
| Approach | 8.5 | — |
| **Overall** | **9.4** | **[8.0 – 10.0]** |

**Verdict:** overall_score=9.4 is WITHIN expected range [8.0, 10.0]

**Model Feedback:**
> The code compiles and solves the problem correctly. It accurately checks if the array is sorted in strictly ascending order.

**Summary Review:** Quality=Excellent, AvgScore=9.4
  - Common Errors: None
  - Weaknesses: None identified.

**Response Time:** 61.3s

---

### ❌ V36 (Q5) — Partially Correct (Wrong Condition)

**Ground Truth:** Bug: checks arr[i] >= arr[i-1] which checks for NON-DESCENDING (wrong direction). On descending arrays it says 'Sorted', on ascending it says 'Not Sorted'.

| Score | Value | Expected Range |
|---|---|---|
| Completeness | 10.0 | — |
| Code Quality | 9.5 | — |
| Approach | 8.5 | — |
| **Overall** | **9.4** | **[1.0 – 4.0]** |

**Verdict:** overall_score=9.4 is OUTSIDE expected range [1.0, 4.0]

**Model Feedback:**
> The code compiles and solves the problem correctly. It checks if each element in the array is strictly greater than the previous one and prints 'Sorted' or 'Not Sorted' accordingly.

**Summary Review:** Quality=Excellent, AvgScore=9.4
  - Common Errors: None
  - Weaknesses: None identified.

**Response Time:** 58.1s

> [!WARNING]
> ⚠️ FALSE POSITIVE: V36 scored 9.4 — model may have missed the bug

> [!WARNING]
> ⚠️ PRAISE ON BROKEN CODE: V36 feedback contains: correct

---

### ✅ V37 (Q5) — Does Not Compile (Typo)

**Ground Truth:** Won't compile — 'sorte' is used in println but only 'sorted' is declared.

| Score | Value | Expected Range |
|---|---|---|
| Completeness | 2.0 | — |
| Code Quality | 4.0 | — |
| Approach | 5.0 | — |
| **Overall** | **3.6** | **[0.0 – 4.0]** |

**Verdict:** overall_score=3.6 is WITHIN expected range [0.0, 4.0]

**Model Feedback:**
> The code does not compile due to a typo in the print statement. The variable name should be `sorted` instead of `sorte`. Additionally, the program correctly checks if the array is sorted in strictly ascending order.

**Summary Review:** Quality=Average, AvgScore=3.6
  - Common Errors: Syntax error in print statement.
  - Weaknesses: Compilation failure due to a typo.

**Response Time:** 64.5s

> [!WARNING]
> ⚠️ PRAISE ON BROKEN CODE: V37 feedback contains: correct

---

### ❌ V38 (Q5) — Unattempted

**Ground Truth:** Compiles, runs, no output, no logic. Completely unattempted.

| Score | Value | Expected Range |
|---|---|---|
| Completeness | 1.0 | — |
| Code Quality | 2.5 | — |
| Approach | 3.0 | — |
| **Overall** | **2.7** | **[0.0 – 2.0]** |

**Verdict:** overall_score=2.7 is OUTSIDE expected range [0.0, 2.0]

**Model Feedback:**
> The code does not compile due to missing implementation. The main method should include logic to read an array, check if it is sorted, and print the result.

**Summary Review:** Quality=Poor, AvgScore=2.7
  - Common Errors: Missing implementation and logic in the main method.
  - Weaknesses: Lacks functionality to solve the problem as described.

**Response Time:** 62.0s

---

## ⚠️ Blind Spot Summary

1. ⚠️ FALSE POSITIVE: V20 scored 9.4 — model may have missed the bug
2. ⚠️ PRAISE ON BROKEN CODE: V20 feedback contains: correct
3. ⚠️ BLIND SPOT RETEST: V20 (syntax error) scored 9.4 — still missed?
4. ⚠️ FALSE POSITIVE: V21 scored 9.4 — model may have missed the bug
5. ⚠️ PRAISE ON BROKEN CODE: V21 feedback contains: correct
6. ⚠️ FALSE POSITIVE: V22 scored 9.4 — model may have missed the bug
7. ⚠️ PRAISE ON BROKEN CODE: V22 feedback contains: correct
8. ⚠️ BLIND SPOT RETEST: V22 (infinite loop) scored 9.4 — still missed?
9. ⚠️ FALSE POSITIVE: V24 scored 9.2 — model may have missed the bug
10. ⚠️ PRAISE ON BROKEN CODE: V24 feedback contains: correct, efficient
11. ⚠️ FALSE POSITIVE: V25 scored 9.4 — model may have missed the bug
12. ⚠️ PRAISE ON BROKEN CODE: V25 feedback contains: correct, efficient
13. ⚠️ BLIND SPOT RETEST: V25 (void+return) scored 9.4 — still missed?
14. ⚠️ FALSE POSITIVE: V28 scored 9.4 — model may have missed the bug
15. ⚠️ PRAISE ON BROKEN CODE: V28 feedback contains: correct
16. ⚠️ BLIND SPOT RETEST: V28 (space as consonant) scored 9.4 — same as prior vowel test?
17. ⚠️ FALSE POSITIVE: V29 scored 9.4 — model may have missed the bug
18. ⚠️ PRAISE ON BROKEN CODE: V29 feedback contains: correct
19. ⚠️ BLIND SPOT RETEST: V29 (missing brace) scored 9.4 — still missed?
20. ⚠️ PRAISE ON BROKEN CODE: V32 feedback contains: correct
21. ⚠️ PRAISE ON BROKEN CODE: V33 feedback contains: correct
22. ⚠️ PRAISE ON BROKEN CODE: V34 feedback contains: correct
23. ⚠️ FALSE POSITIVE: V36 scored 9.4 — model may have missed the bug
24. ⚠️ PRAISE ON BROKEN CODE: V36 feedback contains: correct
25. ⚠️ PRAISE ON BROKEN CODE: V37 feedback contains: correct

---

## Cross-Batch Comparison (Batch 1 vs Batch 2)

### Syntax/Compile Error Detection

| Variant | Bug Type | Batch | Score | Caught? |
|---|---|---|---|---|
| V2 | No class wrapper | B1 | 7.5 | ❌ |
| V9 | Missing brace | B1 | 6.4 | ❌ |
| V10 | Missing semicolon | B1 | 7.4 | ❌ |
| V11 | void+return | B1 | 7.4 | ❌ |
| V13 | Case typo | B1 | 5.1 | ❌ |
| V20 | Does Not Compile (Syntax Error) | B2 | 9.4 | ❌ |
| V25 | Does Not Compile (Type Error) | B2 | 9.4 | ❌ |
| V29 | Does Not Compile (Syntax Error) | B2 | 9.4 | ❌ |
| V37 | Does Not Compile (Typo) | B2 | 3.6 | ✅ |

### Infinite Loop / Hang Detection

| Variant | Bug Type | Batch | Score | Caught? |
|---|---|---|---|---|
| V12 | Missing i++ (while) | B1 | 7.4 | ❌ |
| V22 | Runs But Hangs | B2 | 9.4 | ❌ |
| V34 | Runs But Crashes (Stack Overflow) | B2 | 2.7 | ✅ |

### Shape-Correct Bug Detection

| Variant | Bug Type | Batch | Score | Caught? |
|---|---|---|---|---|
| V5 | Off-by-one | B1 | 6.3 | ❌ |
| V6 | Missing dup guard | B1 | 7.4 | ❌ |
| V17 | Bad init value | B1 | 6.0 | ✅ |
| V21 | Partially Correct (Runtime Crash) | B2 | 9.4 | ❌ |
| V24 | Partially Correct (Edge Case Bug) | B2 | 9.2 | ❌ |
| V28 | Partially Correct (Logic Bug) | B2 | 9.4 | ❌ |
| V36 | Partially Correct (Wrong Condition) | B2 | 9.4 | ❌ |

---

*Report generated by automated test runner (Batch 2). All results are from live API calls to the QWEN evaluator.*