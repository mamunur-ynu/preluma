# Preluma V26 — Final Course Submission Build

**Preluma** is a Python-based pre-class readiness platform and teacher diagnostic dashboard. It helps students prepare before class and helps teachers identify weak concepts through quiz data, statistics, sorting, searching, and visual analytics.

中文题目：**Preluma：基于 Python 的课前学习准备度诊断平台设计与实现**

## Why this project fits the course

The course requirement allows a public dataset project or any Python-related task such as website development, machine learning, deep learning, or game development. Preluma is a website-development style education software project with a standard-library algorithmic core.

## Course requirement mapping

| Requirement | Implementation |
|---|---|
| Load data from CSV | `data_loader.py`, `storage_core.py`, `dataset.csv`, `data/students.csv` |
| Statistical analysis | `analyzer.py`, `analytics_core.py` |
| Manual sorting algorithm | Merge Sort in `analyzer.py` and `algorithms_core.py` |
| Manual searching algorithm | Binary Search in `analyzer.py` and `algorithms_core.py` |
| Measure execution time | `perf_counter_ns()` in `analyzer.py` and `algorithms_core.py` |
| Save results to `result.txt` | `main.py`, `data_loader.py`, `storage_core.py` |
| At least 2 classes | `StudentRecord`, `AnalysisResult` in `models.py` |
| At least 6 functions | Implemented across `main.py`, `data_loader.py`, `analyzer.py`, and core modules |
| At least 3 modules | More than 3 modules included |
| Exception handling | CSV loading, numeric conversion, AI/Wikipedia fallback, app runtime guards |
| No pandas/numpy/sklearn in core | Core modules use only Python standard library |

## Third-party library policy

The teacher confirmed that third-party libraries are allowed. To keep the project safe for strict grading, Preluma separates the project into two layers:

1. **Assessed core layer:** CSV I/O, statistics, Merge Sort, Binary Search, timing, exception handling, and `result.txt` logging are implemented with the Python standard library.
2. **Presentation layer:** Streamlit and Plotly are used only for the web interface and charts.

No pandas, numpy, or sklearn is used for backend calculations.

## Project structure

```text
project/
├── main.py
├── data_loader.py
├── analyzer.py
├── models.py
├── dataset.csv
├── result.txt
├── README.md
├── streamlit_app.py
├── storage_core.py
├── algorithms_core.py
├── analytics_core.py
├── engine.py
├── teacher.py
├── homework_core.py
├── wiki_fetcher.py
├── llm.py
├── data/
│   └── students.csv
├── assets/
└── tests/
```

## How to run the pure-Python compliance demo

```bash
python main.py
```

This command loads `dataset.csv`, performs statistical analysis, runs manual Merge Sort and Binary Search, measures execution time, and writes the output to `result.txt`.

## How to run the web app

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## How to run tests

```bash
python -m pytest
```

If Streamlit is not installed in the environment, Streamlit runtime tests are skipped automatically, while pure-Python core tests still run.

## Main features

- Student Mission Control
- AI Brain Brief and concept explanation
- Readiness Quiz
- Mistake Clinic
- Smart class questions
- Homework Center
- Teacher Studio dashboard
- Evidence Board for algorithms, CSV persistence, and audit logs
- Professor Defense page

## Submission notes

Recommended files to submit:

- Full project folder or ZIP
- Final course report document
- Screenshots of running app
- Screenshot of `python main.py` output and `result.txt`
- Screenshot of `python -m pytest` test result

## Security

Do not upload `.streamlit/secrets.toml` to GitHub. Configure API keys using Streamlit Cloud Secrets when deployment is required.
