"""
engine.py  –  Preluma V17
Core logic: build topic packs, generate quiz questions, grade answers, run tutor.
"""

import re
from topics import TOPICS, canonical_key
from wiki_fetcher import build_wiki_topic_pack, smart_answer_from_pack

SKILL_DEFINITION   = "Definition"
SKILL_CORE         = "Core Concept"
SKILL_APPLICATION  = "Application"
SKILL_MISCONCEPTION = "Misconception"

DEFAULT_CONCEPT = {
    "definition": "This is the main idea of the topic.",
    "kid": "Start with the simplest meaning first, then add examples.",
    "example": "Connect the idea to a real-life situation.",
    "mistake": "Do not memorize words without understanding meaning.",
    "exam": "Explain definition, example, and common mistake.",
}


def clean_text(text: str) -> str:
    return re.sub(r"\s+", " ", str(text).strip())


def make_generic_fallback(title: str) -> dict:
    return {
        "title": title,
        "hook": f"{title} becomes easier when we break it into small ideas.",
        "definition": (
            f"{title} is an academic topic that can be understood through "
            "definition, examples, applications, and common mistakes."
        ),
        "simple": f"Think of {title} like building blocks: first one block, then another.",
        "facts": [
            f"{title} has a main definition.",
            f"{title} becomes clearer through examples.",
            f"{title} can be discussed in class using smart questions.",
        ],
        "concepts": {
            "main idea": {
                "definition": f"The main idea of {title} is the first meaning a student should understand.",
                "kid": f"{title} is easier when we explain it in small steps.",
                "example": "A new topic is like a map: first see the big roads, then learn the details.",
                "mistake": "Do not memorize without examples.",
                "exam": "Give definition, simple example, and one common mistake.",
            }
        },
        "applications": {"class learning": "Helps students prepare before lectures."},
        "misconceptions": [
            f"{title} is not only memorization.",
            "A hard topic becomes easier with examples.",
            "Good preparation means asking better questions in class.",
        ],
        "class_questions": [
            f"What is the simplest definition of {title}?",
            f"Where is {title} used in real life?",
            f"What is the most common mistake in {title}?",
            f"How can I explain {title} to a beginner?",
            f"What should I ask the teacher about {title}?",
        ],
    }


def ensure_pack_schema(data: dict, requested_title: str) -> dict:
    pack = dict(data or {})
    pack.setdefault("title", requested_title)
    pack.setdefault("hook", f"{requested_title} becomes easier when the student sees the big picture first.")
    pack.setdefault("definition", f"{requested_title} is an academic topic.")
    pack.setdefault("simple", f"Think of {requested_title} as a map: first learn the main roads, then the details make sense.")
    pack.setdefault("facts", [])
    pack.setdefault("concepts", {})
    pack.setdefault("applications", {})
    pack.setdefault("misconceptions", [])
    pack.setdefault("class_questions", [])

    if not pack["concepts"]:
        pack["concepts"] = {"main idea": dict(DEFAULT_CONCEPT)}

    fixed = {}
    for name, c in pack["concepts"].items():
        d = dict(DEFAULT_CONCEPT)
        d.update(c or {})
        fixed[name] = d
    pack["concepts"] = fixed

    if not pack["facts"]:
        pack["facts"] = [
            f"{pack['title']} becomes easier when connected to examples.",
            f"{pack['title']} has academic value.",
            "Understanding the core idea improves class participation.",
        ]
    if not pack["misconceptions"]:
        lead = next(iter(pack["concepts"]), "the core idea")
        pack["misconceptions"] = [
            f"{pack['title']} is not only memorization.",
            f"{lead.title()} should be connected to examples.",
            f"Students understand {pack['title']} better when they ask questions.",
        ]
    if not pack["class_questions"]:
        pack["class_questions"] = [
            f"What is the simplest definition of {pack['title']}?",
            f"Where is {pack['title']} used?",
            "What is the most common mistake?",
            "How can I explain it simply?",
            "What should I ask in class?",
        ]
    return pack


def build_pack(topic: str) -> dict:
    requested = clean_text(topic) or "Machine Learning"
    key = canonical_key(requested)
    data = TOPICS.get(key) or make_generic_fallback(requested.title())
    return ensure_pack_schema(data, data.get("title", requested.title()))


def _first_concept(pack: dict) -> tuple:
    name = next(iter(pack["concepts"]))
    return name, pack["concepts"][name]


def best_concept_match(pack: dict, question: str) -> tuple:
    q = clean_text(question).lower()
    for name, c in pack["concepts"].items():
        if name.lower() in q:
            return name, c
    for name, c in pack["concepts"].items():
        if any(len(w) > 3 and w in q for w in name.lower().split()):
            return name, c
    return _first_concept(pack)


def _plausible_distractors(correct: str, pool: list[str]) -> list[str]:
    """
    Return up to 3 plausible wrong answers drawn from the pool,
    excluding the correct answer. Falls back to generic academic phrases.
    """
    fallback = [
        "A technique used only in advanced research with no practical application",
        "A method that works by storing all possible outcomes before execution",
        "A framework built on random guessing rather than structured reasoning",
        "A process that relies solely on human memory without any computation",
        "An approach that ignores data and relies on intuition alone",
        "A system that treats all inputs identically regardless of context",
    ]
    candidates = [p for p in pool if p and p.lower() != correct.lower()]
    if len(candidates) >= 3:
        return candidates[:3]
    # top up from fallback
    needed = 3 - len(candidates)
    return candidates + fallback[:needed]


def make_questions(pack: dict) -> list[dict]:
    concepts = list(pack["concepts"].items())
    apps = list(pack["applications"].keys())
    mis = pack["misconceptions"]

    # Build distractor pool from other concept definitions
    all_definitions = [c["definition"] for _, c in concepts]

    # Q1: Definition
    q1_answer = pack["definition"]
    q1_distractors = _plausible_distractors(
        q1_answer,
        [c["definition"] for _, c in concepts[1:]] if len(concepts) > 1 else [],
    )

    # Q2: Core concept name
    cname, concept = concepts[0]
    q2_answer = cname.title()
    other_concepts = [n.title() for n, _ in concepts[1:]]
    q2_distractors = _plausible_distractors(q2_answer, other_concepts)

    # Q3: Application
    q3_answer = apps[0].title() if apps else "Real-world practice"
    q3_distractors = _plausible_distractors(q3_answer, [a.title() for a in apps[1:]])

    # Q4: Misconception — student must identify the false belief
    q4_answer = mis[0] if mis else "This topic has no practical use"
    q4_distractors = [
        "Understanding examples improves learning",
        "Class questions help deepen knowledge",
        "Definitions give a clear starting point",
    ]

    def make_options(answer: str, distractors: list[str]) -> list[str]:
        import random
        opts = [answer] + distractors[:3]
        random.shuffle(opts)
        return opts

    return [
        {
            "skill": SKILL_DEFINITION,
            "q": f"Which statement best defines {pack['title']}?",
            "options": make_options(q1_answer, q1_distractors),
            "answer": q1_answer,
            "why": "The correct definition explains the core meaning of the topic clearly.",
        },
        {
            "skill": SKILL_CORE,
            "q": f"Which of the following is a key concept in {pack['title']}?",
            "options": make_options(q2_answer, q2_distractors),
            "answer": q2_answer,
            "why": f"{q2_answer} is a central concept that students must understand in this topic.",
        },
        {
            "skill": SKILL_APPLICATION,
            "q": f"In which area is {pack['title']} commonly applied?",
            "options": make_options(q3_answer, q3_distractors),
            "answer": q3_answer,
            "why": f"{q3_answer} is a real domain where this topic is actively used.",
        },
        {
            "skill": SKILL_MISCONCEPTION,
            "q": f"Which of the following is a common misunderstanding about {pack['title']}?",
            "options": make_options(q4_answer, q4_distractors),
            "answer": q4_answer,
            "why": "This is a misconception students should recognize and avoid.",
        },
    ]


def grade(questions: list[dict], answers: dict) -> dict:
    details = []
    score = 0
    skill_errors: dict[str, int] = {}

    for i, q in enumerate(questions):
        chosen = answers.get(i, "")
        correct = chosen == q["answer"]
        score += int(correct)
        if not correct:
            skill_errors[q["skill"]] = skill_errors.get(q["skill"], 0) + 1
        details.append({
            "q": q["q"],
            "chosen": chosen,
            "answer": q["answer"],
            "correct": correct,
            "skill": q["skill"],
            "why": q["why"],
        })

    total = len(questions)
    pct = round(score / total * 100, 1) if total else 0

    # Weakest skill = most errors; ties broken by order
    weakest = max(skill_errors, key=skill_errors.get) if skill_errors else "None"

    return {
        "score": score,
        "total": total,
        "pct": pct,
        "weakest": weakest,
        "skill_errors": skill_errors,
        "details": details,
    }


def tutor_sections(pack: dict, question: str, style: str = "Normal Mode") -> dict:
    """
    Returns a structured tutor response.
    Tries Claude API first; falls back to local concept data.
    """
    # Try Claude API
    try:
        from llm import llm_tutor, llm_available
        if llm_available():
            result = llm_tutor(pack["title"], question, style)
            if result:
                return result
    except ImportError:
        pass

    # Local fallback
    cname, c = best_concept_match(pack, question)
    return {
        "topic": pack["title"],
        "concept": cname.title(),
        "tiny_answer": c["definition"],
        "explain_simply": c["kid"],
        "real_life_example": c["example"],
        "common_mistake": c["mistake"],
        "exam_angle": c["exam"],
    }


def build_brain_brief(pack: dict) -> dict:
    cname, c = _first_concept(pack)
    return {
        "title": pack["title"],
        "tiny_answer": pack["definition"],
        "simple": pack["simple"],
        "hook": pack["hook"],
        "key_concept": cname.title(),
        "concept_simple": c["kid"],
        "example": c["example"],
        "misconception": pack["misconceptions"][0],
        "facts": pack["facts"][:3],
        "class_questions": pack["class_questions"][:5],
    }
