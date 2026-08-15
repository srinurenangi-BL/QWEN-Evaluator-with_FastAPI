# Model Behavior Profile — qwen2.5-coder:7b-instruct as a Java Code Grader

**Last Updated:** 2026-08-14
**Total Evidence Base:** 57 test cases across 7 batches

---

## Evidence Sources

| Batch | Cases | Description |
|---|---|---|
| Batch 1 (basics) | 10 | Basic algorithm problems |
| Batch 2 (LeetCode-style) | 10 | LeetCode-difficulty problems |
| Batch 3 (matched pairs) | 10 | 5 matched correct/buggy pairs |
| Isolation re-test | 4 | Single-question retests of missed bugs |
| Disguised re-test | 4 | Renamed/reframed retests |
| Vowel/consonant | 1 | Non-algorithm domain test |
| **Structural variants** | **18** | **18 variants of one question (second-largest distinct)** |

---

## CONFIRMED STRENGTHS (high confidence, repeated evidence)

### 1. Wrong-language detection — 3/3, no exceptions
Catches Python/JS submitted as Java and rejects before grading. Held even when the non-Java
solution was objectively better.
- **Evidence:** Batch 1 coin change, Batch 2 coin change, **V15 (Python) → 0.0** ✅

### 2. Empty/unattempted detection — reliable
Correctly identifies submissions with no logic implemented.
- **Evidence:** **V16 (TODO stub) → 1.5** ✅

### 3. Dead code / missing-call detection — works
Can detect when a correct method exists but is never invoked from main.
- **Evidence:** **V4 (method never called) → 2.6** ✅

### 4. Missing-main detection — partially works
Recognizes when a class has no entry point, though gives partial credit for correct helper logic.
- **Evidence:** **V3 (no main method) → 4.8** ✅

### 5. Doesn't over-penalize valid alternatives — confirmed
HashSet-based cycle detection scored correctly despite not being the "textbook" Floyd's approach.
Correct code with minor dead code (unused import, unused variable) scored within range.
- **Evidence:** Batch 3 cycle detection, **V18 (correct + dead code) → 7.4** ✅

### 6. Wrong-approach / wrong-algorithm detection — 5/5 in matched pairs
Reliably catches: linear vs binary search, descending vs ascending sort, first/last char vs
full palindrome, plain recursion vs DP, O(n) vs O(1).
- **Evidence:** All 5 Batch 3 structural pairs

### 7. Mismatched-question detection — mostly works (weakened)
Catches "answers a different question" but may score slightly too generously.
- **Evidence:** Batch 3 (2/2), **V8 (prints largest, not 2nd largest) → 4.0** (expected ≤3.0, borderline)

---

## CONFIRMED BLIND SPOTS (repeated, reproducible)

### 1. 🔴 CRITICAL — Cannot detect syntax/compile errors
The model evaluates code *logic shape* and completely ignores whether the code would pass
`javac`. This is the single biggest finding from the structural variant batch.

| Variant | Bug | Score | Expected |
|---|---|---|---|
| V2 | No class declaration, no import | **7.5** | 0–4 |
| V9 | Missing closing `}` | **6.4** | 0–4 |
| V10 | Missing semicolon | **7.4** | 0–4 |
| V11 | `void` method has `return secondLargest` | **7.4** | 0–4 |
| V13 | `secondlargest` ≠ `secondLargest` (case typo) | **5.1** | 0–4 |

**0/5 caught.** Not a single compile-error variant scored within expected range.

### 2. 🔴 CRITICAL — Cannot detect infinite loops
When the loop body logic is correct but the increment is missing, the model reads the body,
judges the logic correct, and completely misses the infinite loop.
- **Evidence:** **V12 (missing `i++` in while loop) → 7.4** with feedback praising the code

### 3. 🟡 MODERATE — "Correct shape" bugs inconsistently caught
Bugs where the code's overall approach is correct but a single detail causes failure on
specific inputs. Sometimes caught, sometimes missed — no reliable predictor.

| Bug | Caught? | Score | Evidence |
|---|---|---|---|
| Binary search `<` vs `<=` | ✅ Yes | — | Batch 3 |
| Two-stack push/pop desync | ✅ Yes | — | Batch 3 |
| Fibonacci DP array-sizing | ✅ Yes | — | Batch 3 |
| Kadane's `0` init (negative arrays) | ❌ No (prior), **✅ Yes (this batch)** | 6.0 | V17 |
| Reverse linked list pointer order | ❌ No (3x) | — | Batch 3 + isolation + disguised |
| Merge intervals missing sort | ❌ No (3x) | — | Batch 3 + isolation + disguised |
| Sliding window single-step shrink | ❌ No (3x) | — | Batch 3 + isolation + disguised |
| Vowel counter — space as consonant | ❌ No | — | Vowel/consonant test |
| **Off-by-one `i < n-1`** | **🔶 Borderline** | **6.3** | **V5 (expected ≤6.0)** |
| **Missing `!= largest` guard** | **❌ No** | **7.4** | **V6** |

### 4. 🟡 MODERATE — Penalizes correct but poorly formatted code
Minified but functionally identical code (V14) was scored 4.8 with false claims that it
"doesn't handle duplicates correctly" — the model conflates unreadable style with incorrect
logic.
- **Evidence:** **V14 (one-liner, correct logic) → 4.8, with fabricated bug claim**

### 5. 🟡 MODERATE — Generic template feedback (doesn't identify actual bugs)
Across 10 different broken variants, the model produced nearly identical feedback:
- *"does not correctly handle cases where all elements are the same"* (V5, V7, V9, V14, V17)
- *"does not correctly handle cases where there is no second largest"* (V6, V10, V11, V12, V18)

The actual bugs were: off-by-one, missing brace, missing semicolon, void return, infinite
loop, case typo — none of which were identified. The feedback is a **generic edge-case
critique** that sounds plausible but is unrelated to the real issue.

### 6. 🟡 MODERATE — Praise on broken code
10/18 broken variants had the word "correct" appear in feedback. This is the same pattern
observed in the prior profile where "correct, efficient, best practices" was issued on
genuinely broken code, including one case with a fabricated variable name.

---

## SCORE DISTRIBUTION — Structural Variants Batch (18 Variants)

```
Score   Variant  Ground Truth
──────  ───────  ────────────────────────────
 9.7    V1       ✅ Fully correct
 7.5    V2       ❌ Won't compile (no class)
 7.4    V6       ❌ Missing dup guard
 7.4    V10      ❌ Won't compile (no semicolon)
 7.4    V11      ❌ Won't compile (void return)
 7.4    V12      ❌ Infinite loop
 7.4    V18      ✅ Correct + dead code
 6.4    V9       ❌ Won't compile (missing brace)
 6.3    V5       ❌ Off-by-one
 6.3    V7       ✅ Edge case crash (scored in range)
 6.0    V17      ✅ Bad init (scored in range)
 5.1    V13      ❌ Won't compile (case typo)
 4.8    V3       ✅ No main method
 4.8    V14      ❌ Correct but ugly (false negative)
 4.0    V8       ❌ Wrong problem (scored too high)
 2.6    V4       ✅ Dead code / no call
 1.5    V16      ✅ Empty stub
 0.0    V15      ✅ Wrong language
```

Notice the **clustering at 7.4** — four completely different bugs (missing semicolon,
void return, infinite loop, correct code with dead imports) all received exactly 7.4. This
suggests the model has a narrow scoring range and defaults to ~7 when the code "looks
approximately right."

---

## RECOMMENDATIONS (not yet implemented — awaiting decision)

| Priority | Action | Fixes | Effort |
|---|---|---|---|
| 1 | Add pre-LLM `javac` compilation check | V2, V9, V10, V11, V13 (5 cases) | Medium |
| 2 | Add pre-LLM execution with timeout | V12 infinite loop, runtime crashes | High |
| 3 | Rework prompt: explicit syntax checklist | Feedback quality, V14 false negative | Low |
| 4 | Rework prompt: require line-number citations | Generic feedback problem | Low |
| 5 | Consider larger model (14B+) for logic tracing | V5, V6 shape-correct bugs | N/A |

---

## TESTING COVERAGE GAPS

Areas **not yet tested** that would complete the profile:

- [ ] Multi-submission batches (3+ submissions in one request) — only tested 1-per-request
- [ ] Concurrency / load testing — how does scoring change under parallel requests?
- [ ] Repeated runs — consistency check (same input → same score?)
- [ ] Non-Java languages (Python, C++) — does the evaluator work for other target languages?
- [ ] Very long code (500+ lines) — does quality degrade with length?
- [ ] Code with intentional security vulnerabilities — does the model flag them?
- [ ] Questions requiring specific data structures (trees, graphs) — different domain

---

*This profile is the single source of truth for all QWEN evaluator testing data.
Update this document as new batches are run.*
