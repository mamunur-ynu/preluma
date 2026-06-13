# Preluma V24 — Polished AI + Team Final

This build focuses on three high-impact corrections:

- Compact grouped sidebar: Learn, Teach, and Project/Presentation
- Premium team-photo background hero with all three members visible
- Intent-aware Preluma AI with natural paragraph answers, deep-answer mode, clarification for vague questions, chat history, and multi-provider fallback

## AI behavior

Preluma prioritizes the user's exact question over old mission context. It detects the topic and requested explanation style. Vague requests trigger one concise clarification. Clear requests receive a natural answer whose depth follows Short, Balanced, or Deep.

External providers are optional. Available providers are used through automatic fallback. Without keys, curated topic packs and Wikipedia-supported fallback remain available.

## Safe deployment

Never commit real API keys. Configure them only in Streamlit Cloud Secrets.
