import re
from topics import TOPICS, canonical_key

SKILL_DEFINITION="Definition"; SKILL_CORE="Core Concept"; SKILL_APPLICATION="Application"; SKILL_MISCONCEPTION="Misconception"
DEFAULT_CONCEPT={"definition":"This is the main idea of the topic.","kid":"Start with the simplest meaning first, then add examples.","example":"Connect the idea to a real-life situation.","mistake":"Do not memorize words without understanding meaning.","exam":"Explain definition, example, and common mistake."}

def clean_text(text): return re.sub(r"\s+"," ",str(text).strip())

def make_generic_fallback(title):
    return {"title":title,"hook":f"{title} becomes easier when we break it into small ideas.","definition":f"{title} is an academic topic that can be understood through definition, examples, applications, and common mistakes.","simple":f"Think of {title} like building blocks: first one block, then another.","facts":[f"{title} has a main definition.",f"{title} becomes clearer through examples.",f"{title} can be discussed in class using smart questions."],"concepts":{"main idea":{"definition":f"The main idea of {title} is the first meaning a student should understand.","kid":f"{title} is easier when we explain it in tiny steps.","example":"A new topic is like a map: first see the big roads, then learn the details.","mistake":"Do not memorize without examples.","exam":"Give definition, simple example, and one common mistake."}},"applications":{"class learning":"Helps students prepare before lectures."},"misconceptions":[f"{title} is not only memorization.","A hard topic becomes easier with examples.","Good preparation means asking better questions in class."],"class_questions":[f"What is the simplest definition of {title}?",f"Where is {title} used in real life?",f"What is the most common mistake in {title}?",f"How can I explain {title} to a beginner?",f"What should I ask the teacher about {title}?"]}

def ensure_pack_schema(data, requested_title):
    pack=dict(data or {}); pack.setdefault("title", requested_title); pack.setdefault("hook", f"{requested_title} becomes easier when the student sees the big picture first."); pack.setdefault("definition", f"{requested_title} is an academic topic."); pack.setdefault("simple", f"Think of {requested_title} as a map: first learn the main roads, then the details make sense."); pack.setdefault("facts", []); pack.setdefault("concepts", {}); pack.setdefault("applications", {}); pack.setdefault("misconceptions", []); pack.setdefault("class_questions", [])
    if not pack["concepts"]: pack["concepts"]={"main idea":dict(DEFAULT_CONCEPT)}
    fixed={}
    for name, c in pack["concepts"].items():
        d=dict(DEFAULT_CONCEPT); d.update(c or {}); fixed[name]=d
    pack["concepts"]=fixed
    if not pack["facts"]: pack["facts"]=[f"{pack['title']} becomes easier when connected to examples.", f"{pack['title']} has academic value.", "Understanding the core idea improves class participation."]
    if not pack["misconceptions"]:
        lead=next(iter(pack["concepts"]), "the core idea")
        pack["misconceptions"]=[f"{pack['title']} is not only memorization.", f"{lead.title()} should be connected to examples.", f"Students understand {pack['title']} better when they ask questions."]
    if not pack["class_questions"]: pack["class_questions"]=[f"What is the simplest definition of {pack['title']}?", f"Where is {pack['title']} used?", "What is the most common mistake?", "How can I explain it simply?", "What should I ask in class?"]
    return pack

def build_pack(topic):
    requested=clean_text(topic) or "Machine Learning"; key=canonical_key(requested); data=TOPICS.get(key) or make_generic_fallback(requested.title()); return ensure_pack_schema(data, data.get("title", requested.title()))

def _first_concept(pack):
    name=next(iter(pack["concepts"])); return name, pack["concepts"][name]

def best_concept_match(pack, question):
    q=clean_text(question).lower()
    for name,c in pack["concepts"].items():
        if name.lower() in q: return name,c
    for name,c in pack["concepts"].items():
        if any(len(w)>3 and w in q for w in name.lower().split()): return name,c
    return _first_concept(pack)

def make_questions(pack):
    cname, c=_first_concept(pack); app=next(iter(pack["applications"])) if pack["applications"] else "real life"; mis=pack["misconceptions"][0]
    return [
        {"skill":SKILL_DEFINITION,"q":f"What is the best simple definition of {pack['title']}?","options":[pack["definition"],"A random activity with no rules","Only memorizing a word","A topic that cannot be explained"],"answer":pack["definition"],"why":"The definition explains the main meaning clearly."},
        {"skill":SKILL_CORE,"q":f"Which concept is important in {pack['title']}?","options":[cname.title(),"Shoe Size","Cooking Oil","Random Guess"],"answer":cname.title(),"why":f"{cname.title()} is a core concept from this topic."},
        {"skill":SKILL_APPLICATION,"q":f"Where can {pack['title']} be applied?","options":[app.title(),"Only in dreams","Nowhere useful","Only for decoration"],"answer":app.title(),"why":f"{app.title()} is a real application connected to the topic."},
        {"skill":SKILL_MISCONCEPTION,"q":"Which statement is a common misunderstanding?","options":[mis,"Examples help learning","Class questions are useful","Definitions are important"],"answer":mis,"why":"This option describes a misconception students should avoid."},
    ]

def grade(questions, answers):
    details=[]; score=0; weak=[]
    for i,q in enumerate(questions):
        chosen=answers.get(i,""); correct=chosen==q["answer"]; score+=int(correct)
        if not correct: weak.append(q["skill"])
        details.append({"q":q["q"],"chosen":chosen,"answer":q["answer"],"correct":correct,"skill":q["skill"],"why":q["why"]})
    total=len(questions); pct=round(score/total*100,1) if total else 0
    return {"score":score,"total":total,"pct":pct,"weakest":weak[0] if weak else "None","details":details}

def tutor_sections(pack, question, style="Normal Mode"):
    cname,c=best_concept_match(pack, question)
    return {"topic":pack["title"],"concept":cname.title(),"tiny_answer":c["definition"],"explain_simply":c["kid"],"real_life_example":c["example"],"common_mistake":c["mistake"],"hard_words_made_easy":f"{cname.title()} means: {c['kid']}","exam_angle":c["exam"],"memory_line":f"Remember {cname.title()} through this example: {c['example']}"}

def build_brain_brief(pack):
    cname,c=_first_concept(pack)
    return {"title":pack["title"],"tiny_answer":pack["definition"],"simple":pack["simple"],"hook":pack["hook"],"key_concept":cname.title(),"concept_simple":c["kid"],"example":c["example"],"misconception":pack["misconceptions"][0],"facts":pack["facts"][:3],"class_questions":pack["class_questions"][:5]}
