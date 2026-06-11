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


## V16 upload checklist

Also upload:

- wiki_fetcher.py

Also ensure requirements.txt includes:

- requests

Smoke test:

1. Choose Custom Topic
2. Type a topic not in local database, such as Photosynthesis
3. Keep "Use Wikipedia real data" checked
4. Start mission
5. Check source link appears in Brain Brief
6. Ask Smart QnA a question


## V16.1 upload checklist

Also upload:

- assets/team_preluma.jpg

Then open the app and check the new sidebar page:

- Project Team


## V16.2 upload note

This version updates the Project Team page and workload wording.
Upload streamlit_app.py and README.md at minimum.


## V16.3 upload checklist

Upload/replace:

- streamlit_app.py
- README.md
- DEPLOYMENT_GUIDE.md
- assets/team_preluma.jpg

Then open sidebar and click:

Project Team


## V16.4 Final Coach Verified
Verified before release: Project Team page route, TEAM_PHOTO loader, team image asset, compact Mission Control, feedback dropdown, and tests pass.
