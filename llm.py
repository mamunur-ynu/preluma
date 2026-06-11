"""
llm.py  –  Preluma V17
Multi-provider LLM integration.
Priority: Anthropic Claude → Groq → Gemini → local fallback.
Set whichever API key(s) you have as environment variables:
    ANTHROPIC_API_KEY
    GROQ_API_KEY
    GEMINI_API_KEY
"""

import os
import json
import requests

# ── Provider configs ────────────────────────────────────────────────────────

_ANTHROPIC_URL = "https://api.anthropic.com/v1/messages"
_GROQ_URL      = "https://api.groq.com/openai/v1/chat/completions"
_GEMINI_URL    = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

_ANTHROPIC_MODEL = "claude-sonnet-4-20250514"
_GROQ_MODEL      = "llama-3.3-70b-versatile"

_TIMEOUT = 20
_MAX_TOKENS = 600


def _key(name: str) -> str:
    """Read API key from st.secrets first, then environment variable."""
    try:
        import streamlit as st
        val = st.secrets.get(name, "")
        if val:
            return str(val).strip()
    except Exception:
        pass
    return os.environ.get(name, "").strip()


# ── Provider call functions ─────────────────────────────────────────────────

def _call_anthropic(system: str, user: str) -> str:
    key = _key("ANTHROPIC_API_KEY")
    if not key:
        return ""
    try:
        resp = requests.post(
            _ANTHROPIC_URL,
            headers={
                "x-api-key": key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            json={
                "model": _ANTHROPIC_MODEL,
                "max_tokens": _MAX_TOKENS,
                "system": system,
                "messages": [{"role": "user", "content": user}],
            },
            timeout=_TIMEOUT,
        )
        resp.raise_for_status()
        for block in resp.json().get("content", []):
            if block.get("type") == "text":
                return block["text"].strip()
    except Exception:
        pass
    return ""


def _call_groq(system: str, user: str) -> str:
    key = _key("GROQ_API_KEY")
    if not key:
        return ""
    try:
        resp = requests.post(
            _GROQ_URL,
            headers={
                "Authorization": f"Bearer {key}",
                "Content-Type": "application/json",
            },
            json={
                "model": _GROQ_MODEL,
                "max_tokens": _MAX_TOKENS,
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user",   "content": user},
                ],
            },
            timeout=_TIMEOUT,
        )
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"].strip()
    except Exception:
        pass
    return ""


def _call_gemini(system: str, user: str) -> str:
    key = _key("GEMINI_API_KEY")
    if not key:
        return ""
    try:
        resp = requests.post(
            f"{_GEMINI_URL}?key={key}",
            headers={"Content-Type": "application/json"},
            json={
                "contents": [
                    {"role": "user", "parts": [{"text": f"{system}\n\n{user}"}]}
                ],
                "generationConfig": {"maxOutputTokens": _MAX_TOKENS, "temperature": 0.4},
            },
            timeout=_TIMEOUT,
        )
        resp.raise_for_status()
        return (
            resp.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
        )
    except Exception:
        pass
    return ""


# ── Active provider detection ───────────────────────────────────────────────

def active_provider() -> str:
    """Return the name of the first available provider, or 'none'."""
    if _key("ANTHROPIC_API_KEY"):
        return "Claude (Anthropic)"
    if _key("GROQ_API_KEY"):
        return "Groq (Llama 3.3)"
    if _key("GEMINI_API_KEY"):
        return "Gemini 1.5 Flash"
    return "none"


def llm_available() -> bool:
    return active_provider() != "none"


def _call_llm(system: str, user: str) -> str:
    """Try providers in priority order; return first non-empty response."""
    for fn in (_call_anthropic, _call_groq, _call_gemini):
        result = fn(system, user)
        if result:
            return result
    return ""


# ── JSON parse helper ───────────────────────────────────────────────────────

def _parse_json(raw: str) -> dict | None:
    clean = raw.strip()
    # Strip markdown fences if present
    if "```" in clean:
        parts = clean.split("```")
        for part in parts:
            part = part.strip().lstrip("json").strip()
            if part.startswith("{"):
                clean = part
                break
    try:
        return json.loads(clean)
    except Exception:
        # Try to find first { ... } block
        start = clean.find("{")
        end   = clean.rfind("}")
        if start != -1 and end != -1:
            try:
                return json.loads(clean[start:end+1])
            except Exception:
                pass
    return None


# ── Public API ──────────────────────────────────────────────────────────────

def llm_tutor(topic: str, question: str, style: str = "Normal Mode") -> dict | None:
    """
    Ask the LLM to answer a student question about a topic.
    Returns a structured dict or None if no provider is available.
    """
    style_instructions = {
        "Coach Mode": (
            "Be warm and encouraging. Start by acknowledging the student's question positively, "
            "then give a clear and correct explanation."
        ),
        "Roast Mode": (
            "Use light, respectful humour to keep the student engaged, "
            "but always give a correct and complete explanation."
        ),
    }.get(style, "Be clear, direct, and academic. No filler words.")

    system = (
        "You are Preluma UltraTutor, an AI teaching assistant for university students. "
        "You give short, structured, accurate answers to help students prepare for lectures. "
        f"{style_instructions} "
        "Do not use bullet symbols (* or -). Use plain prose or numbered lists only. "
        "Keep the entire response under 220 words. "
        "Always respond with ONLY a valid JSON object — no preamble, no markdown fences."
    )

    user = (
        f"Topic: {topic}\n"
        f"Student question: {question}\n\n"
        "Respond with this exact JSON structure:\n"
        '{"concept": "short concept name", '
        '"tiny_answer": "one clear sentence answer", '
        '"explain_simply": "2-3 sentences for a beginner", '
        '"real_life_example": "one concrete real-world example", '
        '"common_mistake": "one mistake students make", '
        '"exam_angle": "what to say in an exam or viva"}'
    )

    raw = _call_llm(system, user)
    if not raw:
        return None

    parsed = _parse_json(raw)
    if parsed:
        required = {"concept", "tiny_answer", "explain_simply",
                    "real_life_example", "common_mistake", "exam_angle"}
        if required.issubset(parsed.keys()):
            return parsed

    # Soft fallback: return raw text wrapped in structure
    return {
        "concept":         topic,
        "tiny_answer":     raw[:280],
        "explain_simply":  "",
        "real_life_example": "",
        "common_mistake":  "",
        "exam_angle":      "",
    }


def llm_brain_brief(topic: str, definition: str, concepts: list[str]) -> dict | None:
    """
    Generate an enriched Brain Brief using the LLM.
    concepts = list of concept names from the topic pack.
    Returns dict with keys: hook, simple, example, misconception, study_tip.
    """
    system = (
        "You are Preluma, a pre-class learning assistant. "
        "Generate a short, engaging brain brief to help a student prepare for a lecture. "
        "Be concrete. Avoid vague academic language. "
        "Respond with ONLY a valid JSON object — no markdown, no preamble."
    )

    user = (
        f"Topic: {topic}\n"
        f"Definition: {definition}\n"
        f"Key concepts: {', '.join(concepts)}\n\n"
        "Generate a Brain Brief JSON:\n"
        '{"hook": "one engaging sentence that makes the topic feel interesting", '
        '"simple": "explain the topic in 2 sentences a 15-year-old would understand", '
        '"example": "one vivid real-life example", '
        '"misconception": "one common wrong belief students have", '
        '"study_tip": "one concrete action the student can take before class"}'
    )

    raw = _call_llm(system, user)
    if not raw:
        return None

    parsed = _parse_json(raw)
    if parsed and {"hook", "simple", "example", "misconception", "study_tip"}.issubset(parsed.keys()):
        return parsed
    return None


def llm_class_questions(topic: str, definition: str, concepts: list[str]) -> list[str] | None:
    """
    Generate 5 smart class questions using the LLM.
    Returns a list of question strings or None.
    """
    system = (
        "You are Preluma, a pre-class learning assistant. "
        "Generate 5 smart questions a prepared student would ask a professor in class. "
        "Questions should be specific, insightful, and show the student has done preparation. "
        "Respond with ONLY a JSON array of 5 strings — no markdown, no preamble."
    )

    user = (
        f"Topic: {topic}\n"
        f"Definition: {definition}\n"
        f"Key concepts: {', '.join(concepts)}\n\n"
        'Respond as: ["Question 1?", "Question 2?", "Question 3?", "Question 4?", "Question 5?"]'
    )

    raw = _call_llm(system, user)
    if not raw:
        return None

    clean = raw.strip()
    if "```" in clean:
        clean = clean.replace("```json", "").replace("```", "").strip()
    try:
        result = json.loads(clean)
        if isinstance(result, list) and len(result) >= 3:
            return [str(q) for q in result[:5]]
    except Exception:
        pass
    return None
