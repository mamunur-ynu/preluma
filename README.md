# Preluma V23 — Clean AI + Team Final

This build focuses on the two highest-priority quality issues: question-aware AI tutoring and a fully visible premium team page.

## AI upgrades

- Explicit user questions override old mission context.
- `about machine learning` now routes to **Machine Learning**, not an unrelated prior topic.
- Six provider-ready architecture:
  - OpenAI
  - Anthropic Claude
  - Google Gemini
  - Groq
  - OpenRouter
  - Together AI
- One provider answers while the next providers act as automatic fallbacks.
- If no API key is configured, Preluma uses the curated topic engine and Wikipedia-supported fallback.
- Chat-style history, context chips, explanation style, answer depth, clear chat, and provider status.

## Team page upgrades

- The real team photo is rendered as a full image instead of a cropped CSS background.
- All three people remain visible.
- Balanced role descriptions and equal member cards.
- Team photo path: `assets/team_preluma.jpg`.

## Secret setup

Do not upload a real `.streamlit/secrets.toml` to GitHub.
Copy values into Streamlit Cloud Secrets using `.streamlit/secrets.example.toml` as a template.

## Verification

- Python compilation
- Unit tests
- Streamlit startup
- Full guided mission flow
- Project Team page runtime
- Ask Preluma AI runtime
- Question/topic mismatch regression test
- Homework pages runtime
