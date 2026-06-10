# Preluma Deployment Guide

## Upload files

Replace these files in GitHub:

- streamlit_app.py
- engine.py
- topics.py
- teacher.py
- requirements.txt
- README.md
- DEPLOYMENT_GUIDE.md
- tests/test_engine.py
- tests/test_topics.py

Keep:

- assets/ynu_campus.jpg

## Commit message

Finalize Preluma V15 stable release

## Smoke check

1. Home page loads
2. Student Mission starts
3. Brain Brief appears
4. Quiz works
5. Mistake Clinic appears
6. UltraTutor works
7. Teacher Studio opens
8. Evidence Board opens

## Local testing

```bash
python -m pytest -q
streamlit run streamlit_app.py
```
