"""
llm.py  –  Claude API integration for Preluma V17
Provides intelligent, topic-aware answers using the Anthropic API.
Falls back gracefully to local data if the API is unavailable.
"""

import os
import json
import requests

ANTHROPIC_API_URL = "https://api.anthropic.com/v1/messages"
MODEL = "claude-sonnet-4-20250514"
MAX_TOKENS = 600


def _api_key() -> str:
    key = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    return key


def _call_claude(system: str, user: str) -> str:
    """Send one turn to the Claude API and return the text response."""
    key = _api_key()
    if not key:
        return ""

    headers = {
        "x-api-key": key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    }
    body = {
        "model": MODEL,
        "max_tokens": MAX_TOKENS,
        "system": system,
        "messages": [{"role": "user", "content": user}],
    }
    try:
        resp = requests.post(ANTHROPIC_API_URL, headers=headers, json=body, timeout=20)
        resp.raise_for_status()
        data = resp.json()
        for block in data.get("content", []):
            if block.get("type") == "text":
                return block["text"].strip()
    except Exception:
        return ""
    return ""


def llm_tutor(topic: str, question: str, style: str = "Normal Mode") -> dict | None:
    """
    Ask Claude to answer a student question about a topic.
    Returns a structured dict or None if the API is not available.

    Style options:
        Normal Mode  – clear and direct
        Coach Mode   – encouraging and supportive
        Roast Mode   – light humour with academic pressure
    """
    style_instructions = {
        "Coach Mode": "Be warm and encouraging. Celebrate the student's curiosity before explaining.",
        "Roast Mode": "Use light, respectful humour to keep the student engaged, but always give a correct and clear explanation.",
    }.get(style, "Be clear, direct, and academic.")

    system = (
        "You are Preluma UltraTutor, an AI teaching assistant helping university students "
        "prepare for lectures. You give short, structured answers. "
        f"{style_instructions} "
        "Never use bullet symbols like * or -. Use plain numbered lists when listing things. "
        "Keep the entire response under 200 words."
    )

    user = (
        f"Topic: {topic}\n"
        f"Student question: {question}\n\n"
        "Respond in this exact JSON structure:\n"
        '{"concept": "...", "tiny_answer": "...", "explain_simply": "...", '
        '"real_life_example": "...", "common_mistake": "...", "exam_angle": "..."}'
    )

    raw = _call_claude(system, user)
    if not raw:
        return None

    # Strip possible markdown fences before parsing
    clean = raw.strip()
    if clean.startswith("```"):
        clean = clean.split("```")[-2] if clean.count("```") >= 2 else clean.replace("```json", "").replace("```", "")

    try:
        parsed = json.loads(clean)
        required = {"concept", "tiny_answer", "explain_simply", "real_life_example", "common_mistake", "exam_angle"}
        if required.issubset(parsed.keys()):
            return parsed
    except Exception:
        pass

    # Fallback: wrap raw text in a basic structure
    return {
        "concept": topic,
        "tiny_answer": raw[:300],
        "explain_simply": "",
        "real_life_example": "",
        "common_mistake": "",
        "exam_angle": "",
    }


def llm_available() -> bool:
    """Return True if an API key is configured."""
    return bool(_api_key())
