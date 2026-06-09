import re
from collections import Counter
from topics import TOPICS

STOPWORDS = set("the and for that with from this have has are was were been will would could should about into than then them they their there where when which what also more most some such only other many each these those because while used known called based topic class lecture".split())

def build_pack(topic):
    key = topic.strip().lower()
    data = TOPICS.get(key)
    if not data:
        title = topic.strip().title() or "Machine Learning"
        data = {
            "title": title,
            "hook": f"{title} becomes easier when you see the big picture first.",
            "definition": f"{title} is an academic topic that can be understood through definition, concepts, examples, and applications.",
            "simple": f"Think of {title} like a new game. First you learn the rules, then you practice examples.",
            "concepts": ["definition", "keywords", "examples", "applications", "limitations", "questions"],
            "misconceptions": [f"{title} is not only memorization.", f"{title} needs examples.", f"{title} becomes clearer through questions."],
            "applications": ["exam preparation", "project work", "class discussion", "real-world problem solving", "critical thinking"],
            "facts": [f"{title} is easier when connected to examples.", f"{title} has real-world uses.", f"Questions help students understand {title} better."]
        }
    text = " ".join([data["definition"], data["hook"], " ".join(data["concepts"]), " ".join(data["applications"])])
    words = re.findall(r"[a-zA-Z][a-zA-Z\-]{2,}", text.lower())
    keywords = [w for w, _ in Counter([w for w in words if w not in STOPWORDS and len(w) > 3]).most_common(10)]
    pack = dict(data)
    pack["keywords"] = keywords
    pack["confidence"] = 0.9 if key in TOPICS else 0.73
    pack["source"] = "Curated lesson pack"
    return pack

def make_questions(pack):
    return [
        {"q": f"What should you understand first about {pack['title']}?", "options": ["The core meaning of the topic", "Only random facts", "Only UI design", "Only copying notes"], "answer": "The core meaning of the topic", "skill": "Definition", "why": "Before going deep, a student needs the basic meaning of the topic.", "kid": f"Before playing a new game, you first learn what the game is. {pack['title']} works the same way.", "evidence": pack["definition"]},
        {"q": f"Which one is a core concept in {pack['title']}?", "options": [pack["concepts"][0], pack["concepts"][1], "decoration", "attendance only"], "answer": pack["concepts"][0], "skill": "Core Concept", "why": f"{pack['concepts'][0]} is included in the Brain Brief as a core concept.", "kid": f"Think of {pack['title']} as a house. {pack['concepts'][0]} is one brick in the house.", "evidence": ", ".join(pack["concepts"])},
        {"q": f"Where can {pack['title']} become useful?", "options": [pack["applications"][0], "Avoiding class questions", "Making learning useless", "Only memorizing without meaning"], "answer": pack["applications"][0], "skill": "Application", "why": "This option shows where the topic becomes useful beyond a definition.", "kid": "Application means where an idea helps in real life.", "evidence": ", ".join(pack["applications"])},
        {"q": f"Which one is a misconception about {pack['title']}?", "options": [pack["misconceptions"][0], pack["definition"][:90], f"{pack['title']} can be discussed in class", f"{pack['title']} has examples"], "answer": pack["misconceptions"][0], "skill": "Misconception", "why": "A misconception is a wrong or incomplete idea that students often believe.", "kid": "A misconception is like thinking a shadow is a monster. Explanation helps you see it clearly.", "evidence": " ".join(pack["misconceptions"])}
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

def tutor(pack, question, style):
    q = question.lower()
    for concept in pack["concepts"]:
        if concept.lower() in q:
            if style == "Kid-simple":
                return f"{concept} is one piece of {pack['title']}. Imagine the topic is a puzzle. If you understand this piece, the full picture becomes easier."
            if style == "Exam-focused":
                return f"For exam: define {concept}, explain its role in {pack['title']}, then give one example."
            return f"{concept} helps explain how {pack['title']} works in real situations."
    if "example" in q or "use" in q or "real" in q:
        return f"Real uses of {pack['title']} include {', '.join(pack['applications'][:3])}."
    if "mistake" in q or "wrong" in q or "confus" in q:
        return "Common confusions: " + " ".join([f"{i+1}. {m}" for i, m in enumerate(pack["misconceptions"])])
    if style == "Exam-focused":
        return f"For exam, write definition, core concepts, one misconception, and one application of {pack['title']}."
    if style == "Real-world":
        return f"In real life, {pack['title']} connects to {', '.join(pack['applications'][:4])}."
    return pack["simple"]
