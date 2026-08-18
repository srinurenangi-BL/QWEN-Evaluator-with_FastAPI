# QWEN Code Evaluator

AI-powered code review, scoring, and analysis engine built with **FastAPI**, **Ollama**, and **Qwen 2.5 Coder 7B Instruct**.

---

## Overview

The QWEN Code Evaluator is an automated code grading system that evaluates student submissions against problem statements and expected criteria. It uses a **Single-Pass Unified Prompt Architecture** — a consolidated LLM inference pipeline that executes language detection, syntax analysis, logic evaluation, and scoring in a single call.

### Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       SINGLE-PASS UNIFIED EVALUATION                        │
│                                                                             │
│  ┌──────────────────┐    ┌─────────────────────┐    ┌────────────────────┐  │
│  │ Language Gate    │───>│ Syntax & Logic Gate │───>│ Score Rubric       │  │
│  │ (Target vs Code) │    │ (Compile, Loops, BS)│    │ (0.0 – 10.0 Scale) │  │
│  └──────────────────┘    └─────────────────────┘    └────────────────────┘  │
│                                                                             │
│  5-Gate Deterministic Rubric:                                               │
│  1. Language Gate   → 0.0 immediately on language mismatch                  │
│  2. Syntax Gate     → Completeness capped ≤ 2.0 on uncompilable syntax      │
│  3. Execution Gate  → Infinite loops, recursion, and dead code capped ≤ 3.0 │
│  4. Logic Gate      → Boundary, off-by-one, and edge cases scored 3.0–6.5   │
│  5. Style Decouple  → Minified/compressed code gets full completeness (9+)  │
│                       with deductions restricted to code quality only       │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Key Features

- **Single-Pass Unified Evaluation**: Consolidated prompt performs language validation + code scoring in one LLM call.
- **Flexible Payload Structure**: Supports discrete fields (`question_text`, `code`, `return_answer`, `specific_instructions`) with automatic alias normalization and flat payload support.
- **5-Gate Deterministic Rubric**: Strict score boundaries preventing false 9+ scores on uncompilable or infinite-loop submissions.
- **Automated Language Mismatch Handling**: Detects non-target languages (e.g. Python submitted for Java) and returns `0.0` with clear guidance.
- **Glassmorphic Web Interface**: Modern Apple Vision Pro / macOS styled UI (`index.html`) with Dark/Light modes, SVG radial score meters, and interactive popup modals.
- **Real-Time Execution Metrics**: Running statistics endpoint (`/api/metrics`) tracking total processed requests and running average latency.
- **Performance Optimized**: Model persistence (`keep_alive: 5m`), context window tuning (`num_ctx: 2048`, `num_predict: 450`), and async timeout safety (`300s`).

---

## Tech Stack

| Layer | Technology |
|---|---|
| **Backend Framework** | FastAPI (Python 3.10+) |
| **Data Validation & Serialization** | Pydantic v2 |
| **LLM Runtime Engine** | Ollama (Local) |
| **Evaluation Model** | `qwen2.5-coder:7b-instruct` |
| **Web UI** | Vanilla HTML5, Modern CSS (Glassmorphism), JavaScript |
| **ASGI Web Server** | Uvicorn |

---

## Project Structure

```
QWEN-Evaluator-with_FastAPI/
│
├── main.py                     # FastAPI app, routes, Ollama async client, telemetry
├── schemas.py                  # Pydantic request/response models & alias normalizers
├── prompts.py                  # Unified evaluation prompt builder & formatting utilities
├── requirements.txt            # Python dependencies
├── .env                        # Environment configuration
├── .gitignore                  # Git ignore rules
├── app.log                     # Application runtime log (auto-generated)
│
├── templates/
│   └── index.html              # Glassmorphic responsive web interface
│
└── tests/
    ├── __init__.py             # Test package marker
    ├── test_data.py            # Master test suite (48 controlled test variants)
    ├── test_runner.py          # Master automated test execution runner
    ├── test_report.md          # Comprehensive test results across all 48 test variants
    ├── model_behavior_profile.md # Empirical model strengths & blind spots analysis
    └── raw_results.json        # Raw JSON API response archive (48 test cases)
```

---

## Setup & Installation

### Prerequisites

1. **Python 3.10+**
2. **Ollama** installed and running — [Download Ollama](https://ollama.com)

### 1. Clone the Repository

```bash
git clone https://github.com/srinurenangi-BL/QWEN-Evaluator-with_FastAPI.git
cd QWEN-Evaluator-with_FastAPI
```

### 2. Set Up Virtual Environment

```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Pull the QWEN Coder Model

```bash
ollama pull qwen2.5-coder:7b-instruct
```

---

## Running the Application

Start the FastAPI server using Uvicorn:

```bash
uvicorn main:app --reload --port 8000
```

- **Web Interface:** [http://localhost:8000](http://localhost:8000)
- **Interactive Swagger Docs:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **Metrics Endpoint:** [http://localhost:8000/api/metrics](http://localhost:8000/api/metrics)

---

## API Documentation

### Endpoints

| Method | Route | Description |
|---|---|---|
| `GET` | `/` | Serves the Glassmorphic Web UI |
| `POST` | `/review` | Evaluates code submissions and returns scores & feedback |
| `GET` | `/api/metrics` | Returns total requests and running average latency |
| `GET` | `/docs` | Interactive Swagger API documentation |

---

### Request Payload Specifications

The `/review` endpoint supports both **batch submission** and **flat single submission** formats with automatic alias mapping.

#### Option A: Batch Submissions (Standard)

```json
{
  "target_language": "Java",
  "submissions": [
    {
      "question_text": "Write a Java program to find the second largest distinct value in an array.",
      "code": "import java.util.Scanner;\npublic class Main {\n  public static void main(String[] args) {\n    // solution code\n  }\n}",
      "return_answer": "Print second largest distinct integer or Integer.MIN_VALUE if none",
      "specific_instructions": "O(n) time complexity, no full array sorting"
    }
  ]
}
```

#### Option B: Flat Single Submission (Flexible Aliases)

```json
{
  "target_language": "Java",
  "question": "Write a program to reverse a string in Java.",
  "student_answer": "public class Main { public static void main(String[] args) { ... } }",
  "expected_output": "Reversed string output",
  "instructions": "Do not use StringBuilder.reverse()"
}
```

---

### Response Structure

```json
{
  "individual_reviews": [
    {
      "question_text": "Write a Java program to find the second largest distinct value in an array.",
      "correctness_feedback": "The code compiles and solves the problem correctly. It correctly identifies the second largest distinct value in the array.",
      "scores": {
        "completeness_score": 10.0,
        "code_quality_score": 9.5,
        "approach_taken_score": 8.5,
        "overall_score": 9.5
      }
    }
  ],
  "summary_review": {
    "overall_average_score": 9.5,
    "overall_quality_label": "Excellent",
    "common_errors": "None",
    "strengths": "The code is well-written, follows best practices, and correctly solves the problem.",
    "weaknesses": "None",
    "recommendations": "None"
  },
  "execution_metrics": {
    "request_duration_seconds": 32.65,
    "lang_detection_duration_seconds": 0.0,
    "code_eval_duration_seconds": 32.65,
    "total_requests_processed": 1,
    "running_average_duration_seconds": 32.65
  }
}
```

---

## Automated Testing & Validation

The codebase includes an automated test framework evaluating **48 controlled test cases** across 16 problem domains:

- **V1 – V18:** Structural, compile, loop, and boundary variants for *Second Largest Element*.
- **V19 – V38:** Multi-domain tests (*Reverse String*, *Prime Check*, *Vowel Counter*, *GCD*, *Array Sorted Check*).
- **V39 – V48:** Classic Data Structures & Algorithms (*Two Sum*, *Linked List*, *Valid Brackets*, *Kadane's*, *Merge Intervals*, *Coin Change DP*, *Longest Substring*, *Tree Traversal*, *Cycle Detection*, *Group Anagrams*).

### Run the Test Suite

```bash
# Ensure server is running on port 8000
python tests/test_runner.py
```

### Empirical Test Reports

| Report | Path | Description |
|---|---|---|
| **Master Test Report** | [`tests/test_report.md`](tests/test_report.md) | Individual score breakdowns, expected bounds, model feedback, and latency for all 48 test variants. |
| **Model Behavior Profile** | [`tests/model_behavior_profile.md`](tests/model_behavior_profile.md) | Detailed analysis of confirmed model strengths and empirical blind spots. |

---

## Environment Variables (`.env`)

| Variable | Default Value | Description |
|---|---|---|
| `OLLAMA_MODEL` | `qwen2.5-coder:7b-instruct` | Local Ollama model tag |
| `LLM_TEMPERATURE` | `0.1` | Sampling temperature (0.1 for high determinism) |
| `LLM_TIMEOUT_SECONDS` | `300` | Max duration per LLM request before async timeout |
| `DEFAULT_TARGET_LANGUAGE` | `Java` | Default programming language |

---

## Git Branch Structure

| Branch | Description |
|---|---|
| **`main`** | Default empty repository branch |
| **`old_code`** | Original dual-pass LLM pipeline |
| **`current_code`** | Single-pass prompt baseline |
| **`Updated_code`** | Latest codebase with discrete variable schema, alias normalizers, and 48-case master test suite |

---

## License

This project is developed for internal evaluation, benchmarking, and automated code grading.
