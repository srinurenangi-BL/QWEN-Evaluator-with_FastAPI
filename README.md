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
└── tests/
    ├── __init__.py              # Test package initializer
    ├── test_data.py             # Master test suite (all 48 controlled variants)
    ├── test_runner.py           # Master automated test runner
    ├── test_report.md           # Master automated test results (48 variants)
    ├── model_behavior_profile.md# Model behavior profile & empirical analysis
    └── raw_results.json         # Master raw API response data (48 variants)
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

---

## Testing & Evaluation

The project includes an automated testing framework with **48 controlled test variants** across 16 problem contexts:

- **Structural & Syntax Variants (V1–V18):** Syntax errors, infinite loops, runtime crashes, logic bugs, dead code, wrong language, and poor style on array problems.
- **Multi-Domain Variants (V19–V38):** Strings, prime numbers, vowel/consonant filtering, Euclidean GCD, and sorting checks.
- **Classic Algorithm Variants (V39–V48):** Two Sum, Reverse Linked List, Valid Brackets, Kadane's Subarray, Merge Intervals, Coin Change DP, Longest Substring, Binary Tree Traversal, Cycle Detection, and Group Anagrams.

**Master Benchmark Result: 41.7% accuracy** (20/48 passed within strict ground truth bounds)

### Running Tests

```bash
# Run the master test suite (48 tests)
python tests/test_runner.py
```

### Evaluation Reports

| Document | Location | Description |
|----------|----------|-------------|
| Master Test Report | [`tests/test_report.md`](tests/test_report.md) | Comprehensive results for all 48 test variants |
| Model Behavior Profile | [`tests/model_behavior_profile.md`](tests/model_behavior_profile.md) | Strengths & blind spots analysis across 48 cases |

---

## Branch Structure

| Branch | Description |
|--------|-------------|
| `main` | Default branch (empty) |
| `old_code` | Dual-call architecture codebase |
| `current_code` | Baseline single-pass prompt codebase |
| `Updated_code` | Single-pass codebase with 48-case master test suite |
