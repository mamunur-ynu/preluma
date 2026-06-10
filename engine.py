import re
import random
from topics import TOPICS, canonical_key

SKILL_DEFINITION = "Definition"
SKILL_CORE = "Core Concept"
SKILL_APPLICATION = "Application"
SKILL_MISCONCEPTION = "Misconception"

DEFAULT_CONCEPT = {
    "definition": "This is the main idea of the topic.",
    "kid": "Start with the simplest meaning first, then add examples.",
    "example": "Connect the idea to a real-life situation.",
    "mistake": "Do not memorize words without understanding meaning.",
    "exam": "Explain definition, example, and common mistake."
}


def clean_text(text):
    return re.sub(r"\s+", " ", str(text).strip())


def fetch_from_wikipedia(topic):
    try:
        import wikipediaapi
        wiki = wikipediaapi.Wikipedia(
            language="en",
            user_agent="Preluma/1.0 (educational project; yunnan university)"
        )
        page = wiki.page(topic)
        if not page.exists():
            return None
        summary = page.summary[:1200]
        full_text = page.text[:6000]
        return {"title": page.title, "summary": summary, "full_text": full_text}
    except Exception:
        return None


STOP_WORDS = {
    "the", "a", "an", "is", "it", "in", "on", "at", "to", "of", "and",
    "or", "but", "for", "with", "this", "that", "are", "was", "were",
    "be", "been", "being", "have", "has", "had", "do", "does", "did",
    "will", "would", "could", "should", "may", "might", "can", "its",
    "their", "they", "we", "you", "he", "she", "as", "by", "from",
    "which", "who", "when", "where", "what", "how", "if", "not", "also",
    "than", "then", "so", "such", "more", "most", "other", "into",
    "about", "after", "before", "between", "through", "during", "while",
    "used", "use", "using", "one", "two", "three", "many", "some",
    "these", "those", "each", "both", "all", "any", "few", "same"
}


def extract_keywords(text, count=10):
    text = text.lower()
    text = re.sub(r"[^a-z\s]", "", text)
    words = text.split()
    freq = {}
    for word in words:
        if word not in STOP_WORDS and len(word) > 3:
            freq[word] = freq.get(word, 0) + 1
    sorted_words = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    return [w for w, _ in sorted_words[:count]]


def extract_key_sentences(text, keywords, count=5):
    sentences = re.split(r"(?<=[.!?])\s+", text)
    scored = []
    for s in sentences:
        sl = s.lower()
        score = sum(1 for kw in keywords if kw in sl)
        if score > 0 and 10 < len(s.split()) < 60:
            scored.append((score, s.strip()))
    scored.sort(key=lambda x: x[0], reverse=True)
    unique = []
    seen = set()
    for _, s in scored:
        key = s[:40]
        if key not in seen:
            unique.append(s)
            seen.add(key)
    return unique[:count]


def build_wikipedia_pack(topic, wiki_data):
    title = wiki_data["title"]
    summary = wiki_data["summary"]
    full_text = wiki_data["full_text"]
    keywords = extract_keywords(summary + " " + full_text[:2000], count=12)
    sentences = extract_key_sentences(full_text, keywords, count=6)

    definition = summary.split(".")[0].strip() + "."
    if len(definition) < 30:
        definition = summary[:200].strip()

    simple = (
        f"Think of {title} as a key idea that can be broken down into "
        f"smaller pieces. Each piece connects to the others and builds "
        f"a full picture."
    )

    facts = []
    for s in sentences[:3]:
        if len(s) > 40:
            facts.append(s)
    if len(facts) < 3:
        fallback_sentences = [s for s in summary.split(".") if len(s.strip()) > 40]
        for s in fallback_sentences:
            if len(facts) >= 3:
                break
            facts.append(s.strip() + ".")

    concepts = {}
    for i, kw in enumerate(keywords[:4]):
        related = [
            s for s in sentences
            if kw.lower() in s.lower() and len(s.split()) > 8
        ]
        if related:
            explanation = related[0]
        else:
            explanation = f"{kw.title()} is a key concept within {title}."

        concepts[kw] = {
            "definition": explanation,
            "kid": (
                f"Think of {kw} like this: it is one of the important "
                f"building blocks of {title}. Once you understand it, "
                f"the bigger picture becomes clearer."
            ),
            "example": (
                f"For example, when studying {title}, {kw} appears "
                f"in practical situations and real-world applications "
                f"that connect theory to practice."
            ),
            "mistake": (
                f"A common mistake is confusing {kw} with a surface-level "
                f"definition. Try to understand what it means in context, "
                f"not just what the word says."
            ),
            "exam": (
                f"In an exam, explain what {kw} means, give one clear "
                f"example, and mention how it connects to {title}."
            )
        }

    applications = {}
    for i, kw in enumerate(keywords[4:8]):
        applications[kw] = (
            f"{kw.title()} is one real-world area where {title} "
            f"plays a role and has practical impact."
        )

    misconceptions = [
        f"{title} is not just about memorizing definitions. "
        f"Understanding the connections between ideas matters more.",
        f"Do not assume {title} is only theoretical. "
        f"It has practical applications in many fields.",
        f"A surface-level understanding of {title} is not enough. "
        f"Ask why each concept matters and how it is used."
    ]

    class_questions = [
        f"What is the core principle behind {title}?",
        f"How does {title} connect to what we studied before?",
        f"What are the main limitations or challenges related to {title}?",
        f"Can you give a real-world example of {title} in action?",
        f"What would change if {title} did not exist or was applied differently?"
    ]

    return {
        "title": title,
        "hook": (
            f"{title} becomes much clearer once we understand "
            f"the key ideas and see how they connect to the real world."
        ),
        "definition": definition,
        "simple": simple,
        "facts": facts[:3],
        "concepts": concepts,
        "applications": applications,
        "misconceptions": misconceptions,
        "class_questions": class_questions,
        "source": "wikipedia"
    }


def make_generic_fallback(title):
    return {
        "title": title,
        "hook": f"{title} becomes easier when we break it into small ideas.",
        "definition": (
            f"{title} is an academic topic that can be understood through "
            f"definition, examples, applications, and common mistakes."
        ),
        "simple": (
            f"Think of {title} like building blocks: "
            f"first one block, then another until the picture is complete."
        ),
        "facts": [
            f"{title} has a main definition worth knowing clearly.",
            f"{title} becomes much clearer through real examples.",
            f"{title} can be discussed confidently using smart questions."
        ],
        "concepts": {
            "main idea": {
                "definition": (
                    f"The main idea of {title} is the first meaning "
                    f"a student should understand before anything else."
                ),
                "kid": (
                    f"{title} is easier when we explain it in tiny steps "
                    f"with examples from everyday life."
                ),
                "example": (
                    "A new topic is like a map: first see the big roads, "
                    "then learn the smaller details one by one."
                ),
                "mistake": (
                    "Do not memorize without examples. "
                    "Understanding why matters more than remembering what."
                ),
                "exam": (
                    "Give a clear definition, one simple example, "
                    "and one common mistake students make."
                )
            }
        },
        "applications": {
            "class learning": (
                "Helps students prepare before lectures "
                "and participate more actively."
            )
        },
        "misconceptions": [
            f"{title} is not only about memorization.",
            "A hard topic becomes easier with worked examples.",
            "Good preparation means asking better questions in class."
        ],
        "class_questions": [
            f"What is the simplest definition of {title}?",
            f"Where is {title} used in real life?",
            f"What is the most common mistake in {title}?",
            f"How can I explain {title} to someone who has never heard of it?",
            f"What should I ask the teacher about {title}?"
        ]
    }


def ensure_pack_schema(data, requested_title):
    pack = dict(data or {})
    pack.setdefault("title", requested_title)
    pack.setdefault(
        "hook",
        f"{requested_title} becomes easier when "
        f"the student sees the big picture first."
    )
    pack.setdefault("definition", f"{requested_title} is an academic topic.")
    pack.setdefault(
        "simple",
        f"Think of {requested_title} as a map: "
        f"first learn the main roads, then the details make sense."
    )
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
            "Understanding the core idea improves class participation."
        ]

    if not pack["misconceptions"]:
        lead = next(iter(pack["concepts"]), "the core idea")
        pack["misconceptions"] = [
            f"{pack['title']} is not only memorization.",
            f"{lead.title()} should be connected to real examples.",
            f"Students understand {pack['title']} better by asking questions."
        ]

    if not pack["class_questions"]:
        pack["class_questions"] = [
            f"What is the simplest definition of {pack['title']}?",
            f"Where is {pack['title']} used in practice?",
            "What is the most common mistake?",
            "How can I explain it simply?",
            "What should I ask in class?"
        ]

    return pack


def build_pack(topic):
    requested = clean_text(topic) or "Machine Learning"
    key = canonical_key(requested)

    if key in TOPICS:
        data = TOPICS[key]
        return ensure_pack_schema(data, data.get("title", requested.title()))

    wiki_data = fetch_from_wikipedia(requested)
    if wiki_data:
        pack = build_wikipedia_pack(requested, wiki_data)
        return ensure_pack_schema(pack, pack.get("title", requested.title()))

    fallback = make_generic_fallback(requested.title())
    return ensure_pack_schema(fallback, requested.title())


def _first_concept(pack):
    name = next(iter(pack["concepts"]))
    return name, pack["concepts"][name]


def best_concept_match(pack, question):
    q = clean_text(question).lower()
    q_words = set(re.sub(r"[^a-z\s]", "", q).split())

    best_name = None
    best_score = 0

    for name, c in pack["concepts"].items():
        name_words = set(name.lower().split())
        score = len(q_words & name_words)

        full_text = " ".join([
            c.get("definition", ""),
            c.get("kid", ""),
            c.get("example", "")
        ]).lower()
        for word in q_words:
            if len(word) > 3 and word in full_text:
                score += 0.5

        if score > best_score:
            best_score = score
            best_name = name

    if best_name:
        return best_name, pack["concepts"][best_name]

    return _first_concept(pack)


def answer_any_question(pack, question):
    q_lower = clean_text(question).lower()

    if any(w in q_lower for w in ["what is", "define", "definition", "mean", "meaning"]):
        mode = "definition"
    elif any(w in q_lower for w in ["example", "show", "illustrate", "demonstrate"]):
        mode = "example"
    elif any(w in q_lower for w in ["why", "reason", "purpose", "important"]):
        mode = "why"
    elif any(w in q_lower for w in ["how", "work", "process", "steps"]):
        mode = "how"
    elif any(w in q_lower for w in ["mistake", "wrong", "error", "common problem"]):
        mode = "mistake"
    elif any(w in q_lower for w in ["exam", "test", "remember", "tip"]):
        mode = "exam"
    elif any(w in q_lower for w in ["application", "use", "where", "real"]):
        mode = "application"
    else:
        mode = "general"

    cname, c = best_concept_match(pack, question)

    sections = {
        "concept": cname.title(),
        "tiny_answer": c["definition"],
        "explain_simply": c["kid"],
        "real_life_example": c["example"],
        "common_mistake": c["mistake"],
        "exam_angle": c["exam"],
        "memory_line": (
            f"Remember {cname.title()} through this: {c['example']}"
        )
    }

    if mode == "definition":
        sections["highlight"] = c["definition"]
    elif mode == "example":
        sections["highlight"] = c["example"]
    elif mode == "mistake":
        sections["highlight"] = c["mistake"]
    elif mode == "exam":
        sections["highlight"] = c["exam"]
    elif mode == "application":
        apps = pack.get("applications", {})
        if apps:
            app_text = ". ".join(
                f"{k.title()}: {v}" for k, v in list(apps.items())[:3]
            )
            sections["highlight"] = app_text
        else:
            sections["highlight"] = c["example"]
    else:
        sections["highlight"] = c["kid"]

    return sections


def make_questions(pack):
    cname, c = _first_concept(pack)
    app = next(iter(pack["applications"])) if pack["applications"] else "real life"
    mis = pack["misconceptions"][0]

    concept_names = list(pack["concepts"].keys())
    distractors_pool = [
        "A random activity with no clear rules",
        "Only memorizing a list of words",
        "A topic that cannot be explained",
        "Something unrelated to this subject",
        "An idea that applies to no real situation"
    ]

    return [
        {
            "skill": SKILL_DEFINITION,
            "q": f"What is the best simple definition of {pack['title']}?",
            "options": [
                pack["definition"],
                distractors_pool[0],
                distractors_pool[1],
                distractors_pool[2]
            ],
            "answer": pack["definition"],
            "why": "The definition explains the main meaning of the topic clearly."
        },
        {
            "skill": SKILL_CORE,
            "q": f"Which concept is an important part of {pack['title']}?",
            "options": [
                cname.title(),
                "Shoe Size",
                "Cooking Temperature",
                "Random Guess"
            ],
            "answer": cname.title(),
            "why": f"{cname.title()} is a core concept that belongs to this topic."
        },
        {
            "skill": SKILL_APPLICATION,
            "q": f"Where can {pack['title']} be applied in the real world?",
            "options": [
                app.title(),
                "Only in imaginary situations",
                "Nowhere useful at all",
                "Only as a decoration"
            ],
            "answer": app.title(),
            "why": f"{app.title()} is a genuine real-world application of this topic."
        },
        {
            "skill": SKILL_MISCONCEPTION,
            "q": "Which of the following is a common misunderstanding?",
            "options": [
                mis,
                "Examples help understanding",
                "Class questions improve learning",
                "Definitions are worth knowing"
            ],
            "answer": mis,
            "why": "This is a misconception that students should recognize and avoid."
        }
    ]


def grade(questions, answers):
    details = []
    score = 0
    weak = []

    for i, q in enumerate(questions):
        chosen = answers.get(i, "")
        correct = chosen == q["answer"]
        score += int(correct)
        if not correct:
            weak.append(q["skill"])
        details.append({
            "q": q["q"],
            "chosen": chosen,
            "answer": q["answer"],
            "correct": correct,
            "skill": q["skill"],
            "why": q["why"]
        })

    total = len(questions)
    pct = round(score / total * 100, 1) if total else 0

    return {
        "score": score,
        "total": total,
        "pct": pct,
        "weakest": weak[0] if weak else "None",
        "details": details
    }


def tutor_sections(pack, question, style="Normal Mode"):
    return answer_any_question(pack, question)


def build_brain_brief(pack):
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
        "class_questions": pack["class_questions"][:5]
    }
