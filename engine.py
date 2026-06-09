import re
from collections import Counter
from topics import TOPICS, ALIASES

STOPWORDS = set("the and for that with from this have has are was were been will would could should about into than then them they their there where when which what also more most some such only other many each these those because while used known called based topic class lecture".split())

def canonical_key(topic):
    key = topic.strip().lower()
    return ALIASES.get(key, key)

def concept_names(pack):
    return list(pack.get("concepts", {}).keys())

def application_names(pack):
    return list(pack.get("applications", {}).keys())

def build_pack(topic):
    key = canonical_key(topic)
    data = TOPICS.get(key)
    if not data:
        title = topic.strip().title() or "Machine Learning"
        concepts = ["definition", "keywords", "examples", "applications", "limitations", "questions"]
        data = {
            "title": title,
            "hook": f"{title} becomes easier when the student sees the big picture first.",
            "definition": f"{title} is an academic topic that can be understood through definition, core concepts, examples, applications, and questions.",
            "simple": f"Think of {title} like a new game. First learn the basic rules, then practice with examples.",
            "concepts": {c: {
                "definition": f"{c.title()} is an important part of {title}.",
                "kid": f"{c.title()} is one small piece of the {title} puzzle.",
                "example": f"In {title}, {c} helps students organize understanding.",
                "mistake": f"Students often memorize {c} without connecting it to examples.",
                "exam": f"Define {c} and explain its role in {title}."
            } for c in concepts},
            "misconceptions": [
                f"{title} is not only memorization.",
                f"{title} needs examples to become clear.",
                f"{title} becomes easier when students ask questions."
            ],
            "applications": {
                "exam preparation": f"{title} helps with exam preparation.",
                "project work": f"{title} can support project work.",
                "class discussion": f"{title} can improve class discussion.",
                "real-world problem solving": f"{title} supports real-world problem solving.",
                "critical thinking": f"{title} develops critical thinking."
            },
            "facts": [
                f"{title} is easier when connected to examples.",
                f"{title} has real-world uses.",
                f"Good questions help students understand {title} better."
            ]
        }

    text = " ".join([data["definition"], data["hook"], " ".join(concept_names(data)), " ".join(application_names(data))])
    words = re.findall(r"[a-zA-Z][a-zA-Z\-]{2,}", text.lower())
    keywords = [w for w, _ in Counter([w for w in words if w not in STOPWORDS and len(w) > 3]).most_common(10)]

    pack = dict(data)
    pack["keywords"] = keywords
    pack["confidence"] = 0.93 if key in TOPICS else 0.72
    pack["source"] = "Curated concept-level lesson pack" if key in TOPICS else "Generic fallback lesson pack"
    pack["topic_key"] = key
    return pack

def make_questions(pack):
    concepts = concept_names(pack)
    apps = application_names(pack)
    c1 = concepts[0]
    c2 = concepts[1] if len(concepts) > 1 else concepts[0]
    app1 = apps[0]
    misconception = pack["misconceptions"][0]

    return [
        {
            "q": f"What should you understand first about {pack['title']}?",
            "options": ["The core meaning of the topic", "Only random facts", "Only interface design", "Only copying notes"],
            "answer": "The core meaning of the topic",
            "skill": "Definition",
            "why": "Before going deep, the student needs the basic meaning of the topic.",
            "kid": f"Before playing a new game, you first learn what the game is. {pack['title']} works the same way.",
            "evidence": pack["definition"]
        },
        {
            "q": f"Which one is a core concept in {pack['title']}?",
            "options": [c1, c2, "decoration", "attendance only"],
            "answer": c1,
            "skill": "Core Concept",
            "why": f"{c1} is included in the Brain Brief as a core concept.",
            "kid": pack["concepts"][c1]["kid"],
            "evidence": pack["concepts"][c1]["definition"]
        },
        {
            "q": f"Where can {pack['title']} become useful?",
            "options": [app1, "Avoiding class questions", "Making learning useless", "Only memorizing without meaning"],
            "answer": app1,
            "skill": "Application",
            "why": pack["applications"][app1],
            "kid": "Application means where an idea helps in real life, not just inside the textbook.",
            "evidence": pack["applications"][app1]
        },
        {
            "q": f"Which one is a misconception about {pack['title']}?",
            "options": [misconception, pack["definition"][:90], f"{pack['title']} can be discussed in class", f"{pack['title']} has examples"],
            "answer": misconception,
            "skill": "Misconception",
            "why": "A misconception is a wrong or incomplete idea that students often believe.",
            "kid": "A misconception is like thinking a shadow is a monster. Explanation helps you see it clearly.",
            "evidence": " ".join(pack["misconceptions"])
        }
    ]

def grade(questions, selected):
    rows = []
    score = 0
    weak = []
    for i, q in enumerate(questions):
        ans = selected.get(i, "")
        ok = ans == q["answer"]
        if ok:
            score += 1
        else:
            weak.append(q["skill"])
        rows.append({"q": q, "answer": ans, "ok": ok})
    return {"score": score, "total": len(questions), "percentage": round(score / len(questions) * 100, 1), "rows": rows, "weak": weak}

def best_concept_match(pack, question):
    q = question.lower()
    for name in concept_names(pack):
        if name.lower() in q:
            return name
    # token overlap fallback
    q_tokens = set(re.findall(r"[a-zA-Z][a-zA-Z\-]{2,}", q))
    best_name = None
    best_score = 0
    for name, details in pack.get("concepts", {}).items():
        text = " ".join([name, details["definition"], details["example"], details["mistake"]]).lower()
        tokens = set(re.findall(r"[a-zA-Z][a-zA-Z\-]{2,}", text))
        score = len(q_tokens & tokens)
        if score > best_score:
            best_name = name
            best_score = score
    return best_name if best_score > 0 else None


def tutor(pack, question, style):
    q = question.lower().strip()
    concept = best_concept_match(pack, q)

    def format_answer(title, simple, definition, example, mistake, exam):
        if style == "Kid-simple":
            return (
                f"Let’s make it very simple. {simple} "
                f"Example: {example} "
                f"Memory hook: remember it as one small puzzle piece of {pack['title']}. "
                f"Common mistake: {mistake}"
            )
        if style == "Exam-focused":
            return (
                f"Exam-ready answer: {definition} "
                f"Example: {example} "
                f"Common mistake to avoid: {mistake} "
                f"How to write in exam: {exam}"
            )
        if style == "Real-world":
            return (
                f"Real-world view: {example} "
                f"This matters because it shows how {pack['title']} is useful beyond memorizing definitions. "
                f"Key idea: {definition}"
            )
        return (
            f"{title}: {definition} "
            f"Simple idea: {simple} "
            f"Example: {example} "
            f"Common mistake: {mistake}"
        )

    if concept:
        details = pack["concepts"][concept]
        return format_answer(
            concept.title(),
            details["kid"],
            details["definition"],
            details["example"],
            details["mistake"],
            details["exam"]
        )

    if "main" in q or "basic" in q or "idea" in q or "understand" in q:
        first = concept_names(pack)[0]
        details = pack["concepts"][first]
        return (
            f"Start with this simple idea: {pack['simple']} "
            f"The first concept to learn is {first}. {details['kid']} "
            f"Example: {details['example']}"
        )

    if "example" in q or "use" in q or "real" in q:
        items = [f"{name}: {text}" for name, text in list(pack["applications"].items())[:3]]
        return "Here are simple real uses from this Brain Brief: " + " ".join(items)

    if "mistake" in q or "wrong" in q or "confus" in q:
        return "Common student confusions: " + " ".join([f"{i+1}. {m}" for i, m in enumerate(pack["misconceptions"])])

    if "exam" in q:
        first = concept_names(pack)[0]
        details = pack["concepts"][first]
        return (
            f"Exam focus for {pack['title']}: first define the topic, then explain {first}. "
            f"Use this line: {details['exam']} "
            f"Then add one application such as {application_names(pack)[0]}."
        )

    if "why" in q or "care" in q:
        apps = ", ".join(application_names(pack)[:3])
        return (
            f"You should care about {pack['title']} because it connects classroom theory with real uses such as {apps}. "
            f"If you know the basic map before class, the lecture becomes much easier to follow."
        )

    return (
        f"I could not find that exact idea inside the current Brain Brief, but we can still learn from the closest concept for {pack['title']}. "
        f"Please ask about one of these concepts: {', '.join(concept_names(pack)[:6])}. "
        f"For example: 'I do not understand {concept_names(pack)[0]}'."
    )

def study_brief_markdown(student, lecture_time, pack, result, questions_to_ask):
    weak = ", ".join(result["weak"]) if result["weak"] else "No major weak area"
    lines = [
        "# Preluma Study Brief",
        "",
        f"Student: {student}",
        f"Lecture: {pack['title']}",
        f"Lecture time: {lecture_time}",
        f"Readiness: {result['percentage']}%",
        f"Score: {result['score']}/{result['total']}",
        f"Weak area: {weak}",
        "",
        "## Brain Brief",
        pack["definition"],
        "",
        "## Explain Like I Am 5",
        pack["simple"],
        "",
        "## Core Concepts",
    ]
    for concept, details in pack["concepts"].items():
        lines.append(f"- {concept}: {details['definition']}")
    lines.extend(["", "## Smart Questions to Ask in Class"])
    for i, question in enumerate(questions_to_ask, 1):
        lines.append(f"{i}. {question}")
    return "\n".join(lines)
