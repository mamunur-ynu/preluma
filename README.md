# Preluma

Light Up Before Class.

Preluma is a pre-class learning assistant that helps students enter lectures prepared, confident, and ready to ask better questions.

## Core experience

- Brain Brief
- Pre-class Quiz
- Mistake Clinic
- Ask Me Tutor
- Concept Map
- Smart Class Questions
- Readiness Dashboard
- Teacher Studio
- Study Brief Export

## Run locally

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Deploy

Upload these root files to GitHub and deploy with Streamlit Cloud:

- streamlit_app.py
- engine.py
- topics.py
- teacher.py
- requirements.txt
- README.md

Main file path:

```text
streamlit_app.py
```

## Demo flow

1. Open Preluma.
2. Enter `Quantum Mechanics`.
3. Choose `Roast Mode`.
4. Show Brain Brief.
5. Intentionally give one wrong answer.
6. Show Mistake Clinic.
7. Ask the tutor: `I do not understand superposition`.
8. Show Teacher Studio.
