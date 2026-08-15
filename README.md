# QWEN Code Evaluator

AI-powered code review, scoring, and analysis engine built with **FastAPI**, **Ollama**, and **Qwen 2.5 Coder 7B Instruct**.

---

## Overview

The QWEN Code Evaluator is an automated code grading system that evaluates student submissions against problem statements. It uses a **Single-Pass Unified Prompt Architecture** — a consolidated LLM call that performs language detection, syntax analysis, logic evaluation, and scoring in a single inference pass.

### Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                SINGLE-PASS UNIFIED PROMPT                    │
│                                                              │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────────────┐  │
│  │ Language     │  │ Syntax &     │  │ Logic & Approach   │  │
│  │ Detection    │──│ Compile Gate │──│ Scoring (0-10)     │  │
│  │ Gate         │  │              │  │                    │  │
│  └─────────────┘  └──────────────┘  └────────────────────┘  │
│                                                              │
│  5-Gate Deterministic Rubric:                                │
│  1. Language Gate → 0.0 on mismatch                          │
│  2. Syntax Gate  → completeness ≤ 2.0 on compile errors      │
│  3. Execution Gate → caps infinite loops & dead code          │
│  4. Logic Gate   → penalizes boundary/duplicate flaws         │
│  5. Style Gate   → decouples formatting from correctness      │
└──────────────────────────────────────────────────────────────┘
```

### Key Features

- **Single-Pass Unified Evaluation**: Consolidated prompt performs language detection + code review in one LLM call
- **5-Gate Deterministic Rubric**: Language, Syntax, Execution, Logic, and Style gates with enforced score ceilings
- **Language Mismatch Detection**: Auto-rejects wrong-language submissions with 0.0 scores
- **Glassmorphism Web Interface**: Apple Vision Pro styled UI with Dark/Light modes, SVG radial progress meters, and interactive popup modals
- **Execution Metrics**: Real-time performance tracking — processed request count and running average response time
- **Optimized Inference**: Model persistence (`keep_alive: 5m`), context window tuning (`num_ctx: 2048`, `num_predict: 450`), and async timeout safety (`300s`)

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| **Language** | Python 3.x |
| **Web Framework** | FastAPI |
| **Validation** | Pydantic v2 |
| **LLM Runtime** | Ollama (local) |
| **Model** | `qwen2.5-coder:7b-instruct` |
| **Frontend** | Vanilla HTML/CSS/JS (Glassmorphism UI) |

---

## Project Structure

```
QWEN-Evaluator-with_FastAPI/
│
├── main.py                     # FastAPI app, routes, Ollama client, metrics
├── schemas.py                  # Pydantic request/response models & validation
├── prompts.py                  # Unified evaluation prompt builder & language detection
├── requirements.txt            # Python dependencies
├── .env                        # Environment configuration
├── .gitignore                  # Git ignore rules
├── app.log                     # Runtime application log (auto-generated)
│
├── templates/
│   └── index.html              # Glassmorphic responsive frontend UI
│
├── docs/
│   └── MASTER_EVALUATION_REPORT.md   # 3-Phase technical evaluation report
│
└── tests/
    ├── __init__.py              # Test package initializer
    ├── test_data.py             # Batch 1: 18 structural variants test data
    ├── test_data_batch2.py      # Batch 2: 20 multi-question test data
    ├── test_runner.py           # Batch 1 automated test runner
    ├── test_runner_batch2.py    # Batch 2 automated test runner
    ├── test_report.md           # Batch 1 test results (18 variants)
    ├── test_report_batch2.md    # Batch 2 test results (20 variants)
    ├── model_behavior_profile.md    # Consolidated model behavior analysis
    ├── raw_results.json         # Batch 1 raw API response data
    └── raw_results_batch2.json  # Batch 2 raw API response data
```

---

## Setup

### Prerequisites

- **Python 3.10+**
- **Ollama** installed and running — [Download Ollama](https://ollama.com)

### Installation

```bash
# Clone the repository
git clone https://github.com/srinurenangi-BL/QWEN-Evaluator-with_FastAPI.git
cd QWEN-Evaluator-with_FastAPI

# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\activate          # Windows
# source venv/bin/activate       # macOS/Linux

# Install dependencies
pip install -r requirements.txt
```

### Pull the model

```bash
ollama pull qwen2.5-coder:7b-instruct
```

---

## Run

```bash
uvicorn main:app --reload --port 8000
```

Open **http://localhost:8000** in your browser for the Web UI.

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Responsive Glassmorphism Web Interface |
| `POST` | `/review` | Single-pass code review & scoring API |
| `GET` | `/api/metrics` | Execution stats (total requests & running average time) |
| `GET` | `/docs` | Swagger UI — interactive API documentation |

### Example Request

```bash
curl -X POST http://localhost:8000/review \
  -H "Content-Type: application/json" \
  -d '{
    "target_language": "Java",
    "submissions": [
      {
        "question_text": "Write a program to find the second largest element in an array",
        "code": "import java.util.Scanner;\npublic class Main {\n  public static void main(String[] args) {\n    int[] arr = {3, 1, 4, 1, 5, 9};\n    // ... solution code\n  }\n}"
      }
    ]
  }'
```

### Example Response

```json
{
  "individual_reviews": [
    {
      "question_text": "Write a program to find the second largest element...",
      "correctness_feedback": "The code compiles and solves the problem correctly.",
      "scores": {
        "completeness_score": 10.0,
        "code_quality_score": 9.5,
        "approach_taken_score": 8.5,
        "overall_score": 9.4
      }
    }
  ],
  "summary_review": {
    "overall_average_score": 9.4,
    "overall_quality_label": "Excellent",
    "common_errors": "None",
    "strengths": "...",
    "weaknesses": "...",
    "recommendations": "..."
  },
  "execution_metrics": {
    "request_duration_seconds": 52.3,
    "lang_detection_duration_seconds": 0.0,
    "code_eval_duration_seconds": 51.8,
    "total_requests_processed": 1,
    "running_average_duration_seconds": 52.3
  }
}
```

---

## Environment Configuration (.env)

| Variable | Default | Description |
|----------|---------|-------------|
| `OLLAMA_MODEL` | `qwen2.5-coder:7b-instruct` | Ollama model name |
| `LLM_TEMPERATURE` | `0.1` | Sampling temperature (lower = more deterministic) |
| `LLM_TIMEOUT_SECONDS` | `300` | Maximum seconds to wait for LLM response |
| `DEFAULT_TARGET_LANGUAGE` | `Java` | Default target programming language |

---

## Testing & Evaluation

The project includes a comprehensive automated testing framework with **38 controlled test variants** across 2 batches:

### Batch 1 — Structural Variants (18 tests)
Focused on a single problem (Second Largest Distinct Element) with 18 structural variants covering:
syntax errors, infinite loops, runtime crashes, logic bugs, dead code, wrong language, poor style, and more.

**Result: 61.1% accuracy** (11/18 passed)

### Batch 2 — Multi-Question Variants (20 tests)  
Expanded to 5 different problem domains (Reverse String, Prime Check, Vowel Counter, GCD, Array Sort Check) with 4 variants each.

**Result: 40.0% accuracy** (8/20 passed)

### Running Tests

```bash
# Run Batch 1 tests
python -m tests.test_runner

# Run Batch 2 tests
python -m tests.test_runner_batch2
```

> **Note:** Tests make live API calls to the QWEN evaluator. Ensure the server is running first.

### Test Reports & Documentation

| Document | Location | Description |
|----------|----------|-------------|
| Batch 1 Test Report | [`tests/test_report.md`](tests/test_report.md) | Detailed results for 18 structural variants |
| Batch 2 Test Report | [`tests/test_report_batch2.md`](tests/test_report_batch2.md) | Detailed results for 20 multi-question variants |
| Model Behavior Profile | [`tests/model_behavior_profile.md`](tests/model_behavior_profile.md) | Consolidated strengths & blind spots analysis |
| Master Evaluation Report | [`docs/MASTER_EVALUATION_REPORT.md`](docs/MASTER_EVALUATION_REPORT.md) | 3-Phase technical architecture & evaluation report |

---

## Branch Structure

| Branch | Description |
|--------|-------------|
| `main` | Default branch (empty) |
| `old_code` | Original Phase 1 codebase (dual-call architecture) |
| `current_code` | Phase 2 codebase (single-pass unified prompt) |
| `Updated_code` | Latest development code with prompt refinements |

---

## Known Model Limitations

Based on extensive testing, `qwen2.5-coder:7b-instruct` has these confirmed blind spots:

| Category | Detection Rate | Details |
|----------|---------------|---------|
| 🟢 Wrong Language | **100%** (3/3) | Always catches Python/JS submitted as Java |
| 🟢 Correct Solutions | **100%** (6/6) | Consistently scores 9.2–9.8 |
| 🟢 Dead Code / No Call | **100%** (2/2) | Detects uncalled methods |
| 🔴 Compile Errors | **~11%** (1/9) | Cannot detect missing braces, semicolons, type errors |
| 🔴 Infinite Loops | **0%** (0/2) | Misses missing loop increments entirely |
| 🟡 Logic Bugs | **~30%** | Inconsistent — catches some, misses others |
| 🟡 Style vs Correctness | **Poor** | Sometimes conflates poor formatting with bugs |

> For the full analysis, see [`docs/MASTER_EVALUATION_REPORT.md`](docs/MASTER_EVALUATION_REPORT.md)

---

## License

This project is for internal evaluation and educational purposes.
