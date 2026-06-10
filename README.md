# Preluma V15 Final Stable

**Light Up Before Class**

Preluma is a Python-based pre-class study assistant. It prepares students before lectures through Brain Brief, quiz, Mistake Clinic, UltraTutor, class questions, and readiness score.

## Python-only stack

- Python
- Streamlit
- Pandas
- Plotly
- Dictionary-based topic data
- Rule-based tutor logic
- JSON study brief export
- Pytest tests

No React, Node.js, or separate JavaScript frontend is required.

## Team

- Mamunur Rashid — Lead, UI, Integration
- MD Fahim — Engine, Quiz, Testing
- MD Jiarul Islam — Topics, Data, Docs

## Required asset path

Keep this file in the repository:

```text
assets/ynu_campus.jpg
```

## Local run

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Run tests

```bash
python -m pytest -q
```

## Strong demo topics

- Quantum Mechanics
- Machine Learning
- Python Programming
- Data Structures

## Professor evaluation points

- Clear real educational problem
- Python implementation
- Structured data design
- Quiz and grading logic
- Mistake-based learning
- Teacher analytics
- Future product roadmap


## V15.1 Bugfix Compact

- Fixed Evidence Board Streamlit compatibility error
- Made Mission Control more compact
- Converted feedback style from radio to dropdown
- Removed unnecessary output-quality column from the form
- Kept the stable campus hero design unchanged


## V16 Real Data Upgrade

Three major upgrades were added:

1. Wikipedia real-data fetch for unknown/custom topics using Python `requests`.
2. Smart QnA that answers questions from curated topic data and fetched Wikipedia summary.
3. Expanded curated topic database for stronger offline demo reliability.

### Important academic note

Wikipedia is used as a public real-data preparation source, not as the final academic authority. The app clearly tells students to verify with teacher notes and course materials.

### New file

- wiki_fetcher.py

### New dependency

- requests
