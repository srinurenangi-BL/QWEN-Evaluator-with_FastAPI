# Model Behavior Profile — qwen2.5-coder:7b-instruct as a Java Code Grader

**Last Updated:** 2026-08-15
**Total Evidence Base:** 38 test cases across 2 batches (Phase 2 — Single-Pass Unified Prompt)

---

## Evidence Sources

| Batch | Cases | Description |
|---|---|---|
| Batch 1 (structural variants) | 18 | 18 variants of "Second Largest Distinct Element" problem |
| Batch 2 (multi-question) | 20 | 5 questions × 4 variants (Reverse String, Prime Check, Vowel Counter, GCD, Array Sorted) |

---

## CONFIRMED STRENGTHS (high confidence, repeated evidence)

### 1. Wrong-language detection — 3/3, no exceptions
Catches Python/JS submitted as Java and rejects before grading. Held even when the non-Java
solution was objectively better.
- **Evidence:** B1 V15 → 0.0 ✅, B2 V30 → 0.0 ✅

### 2. Correct solution scoring — consistent and accurate
Canonical, correct implementations consistently score in the 9.2–9.8 range.
- **Evidence:** V1 (9.4), V19 (9.4), V23 (9.2), V27 (9.4), V31 (9.4), V35 (9.4) — all 6/6 correct variants scored within expected range ✅

### 3. Dead code / missing-call detection — works
Can detect when a correct method exists but is never invoked from main.
- **Evidence:** V4 (method never called) → 3.7 ✅, V32 (gcd() never called) → 4.2 ✅

### 4. Missing-main detection — works
Recognizes when a class has no entry point, gives partial credit for correct helper logic.
- **Evidence:** V3 (no main method) → 3.7 ✅

### 5. Stack overflow / infinite recursion detection — works
Catches recursive calls with incorrect termination conditions.
- **Evidence:** V34 (gcd(a,b) instead of gcd(b, a%b)) → 2.7 ✅

### 6. Variable typo detection — partially works
Can sometimes detect case-sensitive identifier mismatches.
- **Evidence:** V13 (`secondlargest` vs `secondLargest`) → 3.7 ✅, V37 (`sorte` vs `sorted`) → 3.6 ✅

---

## CONFIRMED BLIND SPOTS (repeated, reproducible)

### 1. 🔴 CRITICAL — Cannot detect syntax/compile errors
The model evaluates code *logic shape* and completely ignores whether the code would pass
`javac`. This is the single biggest finding across both batches.

| Variant | Bug | Batch | Score | Expected |
|---|---|---|---|---|
| V2 | No class declaration, no import | B1 | **9.4** | 0–4 |
| V9 | Missing closing `}` | B1 | **9.4** | 0–4 |
| V20 | Missing semicolons | B2 | **9.4** | 0–4 |
| V25 | `void` method returns boolean | B2 | **9.4** | 0–4 |
| V29 | Missing closing `}` | B2 | **9.4** | 0–4 |

**0/5 critical syntax errors caught.** These all scored 9.4 with "compiles and solves correctly" praise.

**Partially caught (within range but wrong reason):**

| Variant | Bug | Batch | Score | Expected | Notes |
|---|---|---|---|---|---|
| V10 | Missing semicolon | B1 | **3.7** | 0–4 | Within range ✅ |
| V11 | `void` returns value | B1 | **3.7** | 0–4 | Within range ✅ |
| V13 | Case typo | B1 | **3.7** | 0–4 | Within range ✅ |
| V37 | Variable typo `sorte` | B2 | **3.6** | 0–4 | Within range ✅ |

### 2. 🔴 CRITICAL — Cannot detect infinite loops
When the loop body logic is correct but the increment is missing, the model reads the body,
judges the logic correct, and completely misses the infinite loop.
- **Evidence:** V12 (missing `i++` in while loop) → **9.4** ❌, V22 (commented-out left++/right--) → **9.4** ❌
- **0/2 caught.** Both scored 9.4 with praise.

### 3. 🟡 MODERATE — Cannot detect edge case / boundary bugs
Bugs where the code's overall approach is correct but a single detail causes failure on
specific inputs. The model consistently misses these in Batch 2.

| Bug | Variant | Batch | Score | Expected | Caught? |
|---|---|---|---|---|---|
| `n < 1` vs `n < 2` prime guard | V24 | B2 | **9.2** | 4–7 | ❌ |
| No `isLetter()` check (spaces count) | V28 | B2 | **9.4** | 3–6.5 | ❌ |
| `>=` instead of `<` (wrong direction) | V36 | B2 | **9.4** | 1–4 | ❌ |
| Off-by-one `i < n-1` | V5 | B1 | **3.8** | 3–6 | ✅ |
| Missing `!= largest` guard | V6 | B1 | **3.7** | 3–6.5 | ✅ |

### 4. 🟡 MODERATE — Cannot detect runtime crashes
Off-by-one array access that causes `ArrayIndexOutOfBoundsException` at runtime is not flagged.
- **Evidence:** V21 (right = chars.length instead of chars.length - 1) → **9.4** ❌

### 5. 🟡 MODERATE — Unattempted code scored too generously
Empty stubs with no logic are scored above expected range.
- **Evidence:** V16 (TODO stub) → **2.8** (expected 0–2) ❌, V38 (empty main) → **2.7** (expected 0–2) ❌

### 6. 🟡 MODERATE — Wrong problem detection inconsistent
Sometimes catches "answers a different question" but may score slightly too generously.
- **Evidence:** V8 (prints largest, not 2nd largest) → **3.1** (expected ≤3.0, borderline) 🔶
- **Evidence:** V33 (calculates LCM, not GCD) → **4.2** (expected ≤4.0, borderline) 🔶

### 7. 🟡 MODERATE — Poor style not distinguished from correctness
Minified but functionally identical code is not consistently penalized for just style.
- **Evidence:** V14 (one-liner, correct logic) → **9.4** (expected 5–9, Batch 2 scored correctly)
- **Evidence:** V26 (crushed formatting, correct) → **9.4** (expected 5–9, same pattern)

### 8. 🟡 MODERATE — Generic template feedback
Across many broken variants, the model produced nearly identical feedback instead of citing actual bugs. Common patterns:
- *"does not correctly handle cases where all elements are the same"*
- *"does not correctly handle cases where there is no second largest"*
- Uses "correct" in feedback even when code is broken (18/38 broken variants had "correct" in praise)

---

## SCORE DISTRIBUTION SUMMARY

### Batch 1 (18 Variants — Second Largest Distinct)
- **Accuracy:** 61.1% (11/18 passed)
- **Average Response Time:** 57.9s
- **Score clustering:** 4 different bugs all received exactly 9.4, suggesting narrow scoring range

### Batch 2 (20 Variants — 5 Questions × 4 Each)
- **Accuracy:** 40.0% (8/20 passed)
- **Average Response Time:** 65.5s
- **Worse performance:** Model is more likely to miss bugs when the code's overall shape is correct

### Combined Across Both Batches
- **Overall Accuracy:** 50.0% (19/38 passed)
- **False Positive Rate:** High — many broken variants scored 9.4 with no bug identification
- **Blind Spot Flags:** 40 total warnings across both batches

---

## DETECTION RATE BY CATEGORY

| Category | Tests | Caught | Rate |
|---|---|---|---|
| Wrong Language | 3 | 3 | **100%** 🟢 |
| Correct Solutions | 6 | 6 | **100%** 🟢 |
| Dead Code / No Call | 2 | 2 | **100%** 🟢 |
| Stack Overflow | 1 | 1 | **100%** 🟢 |
| Variable Typo | 2 | 2 | **100%** 🟢 |
| Syntax / Compile Errors | 9 | 4 | **44%** 🟡 |
| Logic / Edge Case Bugs | 7 | 2 | **29%** 🔴 |
| Infinite Loops | 2 | 0 | **0%** 🔴 |
| Runtime Crashes | 2 | 0 | **0%** 🔴 |
| Poor Style (correct code) | 2 | 0 | **0%** 🔴 |
| Unattempted Stubs | 2 | 0 | **0%** 🔴 |
| Wrong Problem | 2 | 0 | **0%** 🔴 |

---

## RECOMMENDATIONS (Phase 3 — Not Yet Implemented)

| Priority | Action | Fixes | Effort |
|---|---|---|---|
| 1 | Add pre-LLM `javac` compilation check | 100% of compile errors (9 cases) | Medium |
| 2 | Add sandboxed execution with 2s timeout | Infinite loops, runtime crashes (4 cases) | High |
| 3 | Add test case comparison (expected vs actual) | Logic bugs, wrong-problem detection | High |
| 4 | Rework prompt: explicit syntax checklist | Feedback quality, generic template issue | Low |
| 5 | Consider larger model (14B+) for logic tracing | Edge case and boundary bugs | N/A |

> See [`docs/MASTER_EVALUATION_REPORT.md`](../docs/MASTER_EVALUATION_REPORT.md) for the full Phase 3 architecture blueprint.

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
