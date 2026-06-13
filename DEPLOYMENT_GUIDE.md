# Deploy Preluma V22

## Replace/upload

- streamlit_app.py
- engine.py
- topics.py
- teacher.py
- wiki_fetcher.py
- llm.py
- analytics_core.py
- algorithms_core.py
- storage_core.py
- homework_core.py
- requirements.txt
- tests/
- assets/
- .streamlit/config.toml

Do not upload a real secrets.toml.

## Commit message

Add guided mission and homework learning loop

## Test after reboot

### Guided mission
1. Open Student Mission.
2. Start a mission.
3. Confirm setup form disappears.
4. Move through all five steps.
5. Submit the mock test.
6. Confirm the final overview appears.

### Homework
1. Open Homework Center.
2. Publish homework.
3. Set the active student in the sidebar.
4. Open My Homework.
5. Submit homework.
6. Review captured mistakes.
7. Open Homework Center → Class Overview.

### AI
1. Complete a mission or make a homework mistake.
2. Open Ask Preluma AI.
3. Try child-level and step-by-step explanation modes.
