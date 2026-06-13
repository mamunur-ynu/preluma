"""
llm.py  –  Preluma V17
Multi-provider LLM integration.
Priority: Anthropic Claude → Groq → Gemini → local fallback.
"""

import os
import json
import requests

_ANTHROPIC_URL = "https://api.anthropic.com/v1/messages"
_GROQ_URL      = "https://api.groq.com/openai/v1/chat/completions"
_GEMINI_URL    = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

_ANTHROPIC_MODEL = "claude-sonnet-4-20250514"
_GROQ_MODEL      = "llama-3.3-70b-versatile"
_TIMEOUT         = 20
_MAX_TOKENS      = 800


def _key(name: str) -> str:
    try:
        import streamlit as st
        val = st.secrets.get(name, "")
        if val:
            return str(val).strip()
    except Exception:
        pass
    return os.environ.get(name, "").strip()


def _call_anthropic(system: str, user: str) -> str:
    key = _key("ANTHROPIC_API_KEY")
    if not key:
        return ""
    try:
        resp = requests.post(
            _ANTHROPIC_URL,
            headers={"x-api-key": key, "anthropic-version": "2023-06-01", "content-type": "application/json"},
            json={"model": _ANTHROPIC_MODEL, "max_tokens": _MAX_TOKENS, "system": system,
                  "messages": [{"role": "user", "content": user}]},
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
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
            json={"model": _GROQ_MODEL, "max_tokens": _MAX_TOKENS,
                  "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}]},
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
                "contents": [{"role": "user", "parts": [{"text": f"{system}\n\n{user}"}]}],
                "generationConfig": {"maxOutputTokens": _MAX_TOKENS, "temperature": 0.5},
            },
            timeout=_TIMEOUT,
        )
        resp.raise_for_status()
        return resp.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
    except Exception:
        pass
    return ""


def active_provider() -> str:
    if _key("ANTHROPIC_API_KEY"): return "Claude (Anthropic)"
    if _key("GROQ_API_KEY"):      return "Groq (Llama 3.3)"
    if _key("GEMINI_API_KEY"):    return "Gemini 1.5 Flash"
    return "none"


def llm_available() -> bool:
    return active_provider() != "none"


def _call_llm(system: str, user: str) -> str:
    for fn in (_call_anthropic, _call_groq, _call_gemini):
        result = fn(system, user)
        if result:
            return result
    return ""


def _parse_json(raw: str) -> dict | None:
    clean = raw.strip()
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
        start, end = clean.find("{"), clean.rfind("}")
        if start != -1 and end != -1:
            try:
                return json.loads(clean[start:end+1])
            except Exception:
                pass
    return None


def _detect_question_style(question: str) -> str:
    """Detect how the student wants the answer delivered."""
    q = question.lower()
    if any(w in q for w in ["5 year", "5-year", "kid", "child", "simple", "easy", "beginner", "basic"]):
        return "child"
    if any(w in q for w in ["exam", "viva", "marks", "answer for", "write for", "definition"]):
        return "exam"
    if any(w in q for w in ["example", "real life", "real-life", "use case", "application"]):
        return "example"
    if any(w in q for w in ["difference", "vs", "compare", "versus", "between"]):
        return "compare"
    if any(w in q for w in ["why", "reason", "because", "how does", "how do"]):
        return "deep"
    return "normal"


def llm_tutor(topic: str, question: str, style: str = "Normal Mode") -> dict | None:
    q_style = _detect_question_style(question)

    # Build explanation style instruction based on BOTH persona and question style
    explanation_style = {
        "child": (
            "CRITICAL: The student is asking you to explain like they are 5 years old. "
            "You MUST use a fun story or toy analogy. NEVER use technical words. "
            "Example of what GOOD child-style sounds like: "
            "'Imagine computers are people in different cities. A protocol is like agreeing to speak the same language before talking — like both agreeing to speak English so they understand each other.' "
            "Your explain_simply field MUST sound exactly like this — fun, story-like, zero jargon. "
            "If your explanation sounds like a textbook, you have FAILED. Rewrite it until a 5-year-old would smile."
        ),
        "exam": (
            "The student needs a precise exam-ready answer. "
            "tiny_answer: one-line definition. "
            "explain_simply: 3 key points a student must mention in an exam answer, numbered. "
            "exam_angle: exact phrasing to use in a viva or written exam. "
            "Be structured, precise, and academic throughout."
        ),
        "example": (
            "The student wants to learn through examples. "
            "In explain_simply: give TWO vivid real-world examples first, then derive the concept from them. "
            "In real_life_example: give a third completely different example. "
            "Never start with the definition — always lead with the example."
        ),
        "compare": (
            "The student wants to compare two things. "
            "In explain_simply: write a clear side-by-side comparison. "
            "Start with what they have in common, then what makes them different. "
            "Be specific — name exact differences, not vague statements."
        ),
        "deep": (
            "The student wants to understand the deep reason WHY or HOW something works. "
            "In explain_simply: go beyond the definition — explain the mechanism, cause, and effect. "
            "Use a step-by-step logical flow. Use an analogy to make the reasoning click. "
            "Do not just repeat the definition — explain the underlying logic."
        ),
        "normal": (
            "Give a clear, direct, accurate explanation. "
            "Start with the core idea in one sentence, add one concrete example, then name one common mistake."
        ),
    }.get(q_style, "Give a clear and accurate explanation.")

    persona_instruction = {
        "Coach Mode": (
            "You are an encouraging coach. Start with a short motivating line, "
            "then give the explanation. Make the student feel capable."
        ),
        "Roast Mode": (
            "Use one clever, light joke about the question before explaining seriously. "
            "Keep the humour respectful. The explanation itself must be fully correct and complete."
        ),
    }.get(style, "Be clear, direct, and confident.")

    system = f"""You are Preluma UltraTutor — an expert AI teaching assistant for university students.

Your MOST IMPORTANT job: detect HOW the student is asking and match your answer style EXACTLY to that.

REQUIRED STYLE FOR THIS RESPONSE:
{explanation_style}

PERSONA:
{persona_instruction}

STRICT RULES — violating these means your answer is wrong:
1. The "explain_simply" field must FULLY match the required style above — not just partially
2. If the student asked for child-style: ZERO technical terms allowed in explain_simply
3. If the student asked for exam-style: EVERY sentence must be exam-appropriate
4. Never use bullet symbols (* or -)
5. Keep total response under 280 words
6. ONLY output a valid JSON object — absolutely no text before or after it, no markdown fences"""

    user = (
        f"Topic: {topic}\n"
        f"Student question: {question}\n\n"
        "Respond with exactly this JSON structure:\n"
        '{"concept": "short name of what you are explaining", '
        '"tiny_answer": "one sharp sentence that directly answers the question", '
        '"explain_simply": "explanation matched to how the student asked — simple if they asked simply, deep if they asked deeply", '
        '"real_life_example": "one concrete vivid real-world example", '
        '"common_mistake": "one mistake students make about this", '
        '"exam_angle": "what to say in an exam or viva about this"}'
    )

    raw = _call_llm(system, user)
    if not raw:
        return None

    parsed = _parse_json(raw)
    if parsed:
        required = {"concept", "tiny_answer", "explain_simply", "real_life_example", "common_mistake", "exam_angle"}
        if required.issubset(parsed.keys()):
            return parsed

    return {
        "concept": topic,
        "tiny_answer": raw[:300],
        "explain_simply": "",
        "real_life_example": "",
        "common_mistake": "",
        "exam_angle": "",
    }


def llm_brain_brief(topic: str, definition: str, concepts: list) -> dict | None:
    system = (
        "You are Preluma, a pre-class learning assistant. "
        "Generate a short, engaging brain brief to help a student prepare for a lecture. "
        "Be concrete. Avoid vague academic language. "
        "Respond with ONLY a valid JSON object — no markdown, no preamble."
    )
    user = (
        f"Topic: {topic}\nDefinition: {definition}\nKey concepts: {', '.join(concepts)}\n\n"
        'Generate:\n{"hook": "one engaging sentence that makes the topic feel interesting and relevant", '
        '"simple": "explain the topic in 2 sentences a 15-year-old would understand", '
        '"example": "one vivid real-life example that anyone can relate to", '
        '"misconception": "one common wrong belief students have about this topic", '
        '"study_tip": "one concrete action the student can take right now before class"}'
    )
    raw = _call_llm(system, user)
    if not raw:
        return None
    parsed = _parse_json(raw)
    if parsed and {"hook", "simple", "example", "misconception", "study_tip"}.issubset(parsed.keys()):
        return parsed
    return None


def llm_class_questions(topic: str, definition: str, concepts: list) -> list | None:
    system = (
        "You are Preluma, a pre-class learning assistant. "
        "Generate 5 smart questions a well-prepared student would ask a professor in class. "
        "Questions should be specific, insightful, and show genuine preparation — not just basic definitions. "
        "Respond with ONLY a JSON array of 5 strings — no markdown, no preamble."
    )
    user = (
        f"Topic: {topic}\nDefinition: {definition}\nKey concepts: {', '.join(concepts)}\n\n"
        'Respond as: ["Question 1?", "Question 2?", "Question 3?", "Question 4?", "Question 5?"]'
    )
    raw = _call_llm(system, user)
    if not raw:
        return None
    clean = raw.strip().replace("```json", "").replace("```", "").strip()
    try:
        result = json.loads(clean)
        if isinstance(result, list) and len(result) >= 3:
            return [str(q) for q in result[:5]]
    except Exception:
        pass
    return None
