"""
engine.py  –  Preluma V17
Core logic: build topic packs, generate quiz questions, grade answers, run tutor.
"""

import re
import random
from functools import lru_cache
from topics import TOPICS, canonical_key

SKILL_DEFINITION    = "Definition"
SKILL_CORE          = "Core Concept"
SKILL_APPLICATION   = "Application"
SKILL_MISCONCEPTION = "Misconception"

DEFAULT_CONCEPT = {
    "definition": "This is the main idea of the topic.",
    "kid":        "Start with the simplest meaning first, then add examples.",
    "example":    "Connect the idea to a real-life situation.",
    "mistake":    "Do not memorize words without understanding meaning.",
    "exam":       "Explain definition, example, and common mistake.",
}


def clean_text(text: str) -> str:
    return re.sub(r"\s+", " ", str(text).strip())


def make_generic_fallback(title: str) -> dict:
    return {
        "title": title,
        "hook": f"{title} becomes easier when we break it into small ideas.",
        "definition": (
            f"{title} is an academic topic understood through "
            "definition, examples, applications, and common mistakes."
        ),
        "simple": f"Think of {title} like building blocks: start with one idea, then add the next.",
        "facts": [
            f"{title} has a core definition every student should know.",
            f"{title} becomes clearer when connected to real examples.",
            "Good preparation means arriving at class with smart questions.",
        ],
        "concepts": {
            "main idea": {
                "definition": f"The main idea of {title} is the first meaning a student should understand.",
                "kid": f"{title} is easier when explained step by step.",
                "example": "A new topic is like a map: see the big roads first, then learn the details.",
                "mistake": "Do not memorize without connecting to examples.",
                "exam": "Give definition, simple example, and one common mistake.",
            }
        },
        "applications": {"class learning": "Helps students prepare before lectures."},
        "misconceptions": [
            f"{title} is not only about memorization.",
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
    pack.setdefault("simple", f"Think of {requested_title} as a map: learn the main roads first.")
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
            f"{pack['title']} has real academic and practical value.",
            "Understanding the core idea improves class participation.",
        ]
    if not pack["misconceptions"]:
        lead = next(iter(pack["concepts"]), "the core idea")
        pack["misconceptions"] = [
            f"{pack['title']} is not only memorization.",
            f"{lead.title()} should be connected to real examples.",
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
    data = TOPICS.get(key)

    if data is None:
        # Try Wikipedia fallback for unknown topics
        try:
            from wiki_fetcher import build_wiki_topic_pack
            wiki = build_wiki_topic_pack(requested)
            if wiki:
                return ensure_pack_schema(wiki, wiki.get("title", requested.title()))
        except Exception:
            pass
        data = make_generic_fallback(requested.title())

    return ensure_pack_schema(data, data.get("title", requested.title()))


def _first_concept(pack: dict) -> tuple:
    name = next(iter(pack["concepts"]))
    return name, pack["concepts"][name]


def best_concept_match(pack: dict, question: str) -> tuple:
    q = clean_text(question).lower()
    # Exact name match
    for name, c in pack["concepts"].items():
        if name.lower() in q:
            return name, c
    # Word-level match
    for name, c in pack["concepts"].items():
        if any(len(w) > 3 and w in q for w in name.lower().split()):
            return name, c
    # Definition keyword match
    for name, c in pack["concepts"].items():
        def_words = set(w for w in c["definition"].lower().split() if len(w) > 4)
        q_words   = set(q.split())
        if def_words & q_words:
            return name, c
    return _first_concept(pack)


def _plausible_distractors(correct: str, pool: list) -> list:
    """Return 3 plausible wrong answers from pool, topped up with academic fallbacks."""
    academic_fallbacks = [
        "A technique used only in theoretical research with no real-world application",
        "A process that relies on random selection rather than structured reasoning",
        "A framework that produces identical results regardless of input data",
        "A method that bypasses all prior knowledge and starts from scratch each time",
        "A system designed to memorize inputs rather than generalize from them",
        "An approach that treats all problems as equivalent regardless of context",
    ]
    candidates = [p for p in pool if p and p.lower().strip() != correct.lower().strip()]
    if len(candidates) >= 3:
        return candidates[:3]
    needed = 3 - len(candidates)
    return candidates + academic_fallbacks[:needed]


def make_questions(pack: dict) -> list:
    """
    Generate 4 quiz questions — one per skill type.
    Draws from all available concepts, not just the first.
    """
    concepts  = list(pack["concepts"].items())
    apps      = list(pack["applications"].keys())
    mis       = pack["misconceptions"]

    # Rotate concept selection so repeated runs feel varied
    c_index = random.randint(0, len(concepts) - 1)
    cname, concept = concepts[c_index]

    # Q1: Definition
    q1_answer      = pack["definition"]
    other_defs     = [c["definition"] for n, c in concepts if n != cname]
    q1_distractors = _plausible_distractors(q1_answer, other_defs)

    # Q2: Core concept — pick a different concept if possible
    c2_index = (c_index + 1) % len(concepts)
    cname2, _ = concepts[c2_index]
    q2_answer      = cname2.title()
    other_names    = [n.title() for n, _ in concepts if n != cname2]
    q2_distractors = _plausible_distractors(q2_answer, other_names)

    # Q3: Application
    a_index        = random.randint(0, len(apps) - 1) if apps else 0
    q3_answer      = apps[a_index].title() if apps else "Real-world practice"
    other_apps     = [a.title() for a in apps if a != apps[a_index]]
    q3_distractors = _plausible_distractors(q3_answer, other_apps)

    # Q4: Misconception — student identifies the false belief
    m_index        = random.randint(0, len(mis) - 1)
    q4_answer      = mis[m_index]
    q4_distractors = [
        "Understanding examples always improves learning outcomes",
        "Class questions help students engage with the material more deeply",
        "Connecting definitions to context makes concepts easier to remember",
    ]

    def make_options(answer: str, distractors: list) -> list:
        opts = [answer] + distractors[:3]
        random.shuffle(opts)
        return opts

    return [
        {
            "skill":   SKILL_DEFINITION,
            "q":       f"Which statement best defines {pack['title']}?",
            "options": make_options(q1_answer, q1_distractors),
            "answer":  q1_answer,
            "why":     "The correct definition captures the essential meaning of the topic.",
        },
        {
            "skill":   SKILL_CORE,
            "q":       f"Which of the following is a key concept in {pack['title']}?",
            "options": make_options(q2_answer, q2_distractors),
            "answer":  q2_answer,
            "why":     f"{q2_answer} is a central concept students must understand in this topic.",
        },
        {
            "skill":   SKILL_APPLICATION,
            "q":       f"In which area is {pack['title']} commonly applied?",
            "options": make_options(q3_answer, q3_distractors),
            "answer":  q3_answer,
            "why":     f"{q3_answer} is a real domain where this topic is actively used.",
        },
        {
            "skill":   SKILL_MISCONCEPTION,
            "q":       f"Which of the following is a common misunderstanding about {pack['title']}?",
            "options": make_options(q4_answer, q4_distractors),
            "answer":  q4_answer,
            "why":     "Recognizing misconceptions helps students avoid the most common errors.",
        },
    ]


def grade(questions: list, answers: dict) -> dict:
    details      = []
    score        = 0
    skill_errors: dict = {}

    for i, q in enumerate(questions):
        chosen  = answers.get(i, "")
        correct = chosen == q["answer"]
        score  += int(correct)
        if not correct:
            skill_errors[q["skill"]] = skill_errors.get(q["skill"], 0) + 1
        details.append({
            "q":       q["q"],
            "chosen":  chosen,
            "answer":  q["answer"],
            "correct": correct,
            "skill":   q["skill"],
            "why":     q["why"],
        })

    total   = len(questions)
    pct     = round(score / total * 100, 1) if total else 0
    weakest = max(skill_errors, key=skill_errors.get) if skill_errors else "None"

    return {
        "score":        score,
        "total":        total,
        "pct":          pct,
        "weakest":      weakest,
        "skill_errors": skill_errors,
        "details":      details,
    }


def tutor_sections(pack: dict, question: str, style: str = "Normal Mode") -> dict:
    """
    Returns a structured tutor response.
    Tries LLM first (Claude → Groq → Gemini); falls back to local concept data.
    """
    try:
        from llm import llm_tutor, llm_available
        if llm_available():
            result = llm_tutor(pack["title"], question, style)
            if result:
                return result
    except ImportError:
        pass

    # Local fallback — match best concept to the question
    cname, c = best_concept_match(pack, question)
    return {
        "topic":            pack["title"],
        "concept":          cname.title(),
        "tiny_answer":      c["definition"],
        "explain_simply":   c["kid"],
        "real_life_example": c["example"],
        "common_mistake":   c["mistake"],
        "exam_angle":       c["exam"],
    }


def build_brain_brief(pack: dict) -> dict:
    """
    Build an enriched Brain Brief.
    Tries LLM for hook/simple/example/misconception/study_tip;
    falls back to local data.
    """
    cname, c   = _first_concept(pack)
    all_names  = list(pack["concepts"].keys())

    # Try LLM enrichment
    llm_data = {}
    try:
        from llm import llm_brain_brief, llm_available
        if llm_available():
            result = llm_brain_brief(pack["title"], pack["definition"], all_names)
            if result:
                llm_data = result
    except ImportError:
        pass

    return {
        "title":           pack["title"],
        "tiny_answer":     pack["definition"],
        "simple":          llm_data.get("simple")        or pack["simple"],
        "hook":            llm_data.get("hook")          or pack["hook"],
        "key_concept":     cname.title(),
        "concept_simple":  c["kid"],
        "example":         llm_data.get("example")       or c["example"],
        "misconception":   llm_data.get("misconception") or pack["misconceptions"][0],
        "study_tip":       llm_data.get("study_tip")     or "Read the definition, find one example, then write one question to ask in class.",
        "facts":           pack["facts"][:3],
        "all_concepts":    {n: pack["concepts"][n] for n in all_names},
        "class_questions": pack["class_questions"][:5],
    }


def build_enriched_class_questions(pack: dict) -> list:
    """Return LLM-generated smart class questions, or fall back to local ones."""
    try:
        from llm import llm_class_questions, llm_available
        if llm_available():
            all_names = list(pack["concepts"].keys())
            result = llm_class_questions(pack["title"], pack["definition"], all_names)
            if result:
                return result
    except ImportError:
        pass
    return pack["class_questions"][:5]
