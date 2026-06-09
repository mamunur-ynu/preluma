import json
import re
from datetime import datetime
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

APP_VERSION = "15.5"
APP_NAME = "Preluma"
TAGLINE = "Light Up Before Class"

def _campus_bg_data_uri():
    """Load campus photo safely for Streamlit Cloud and local demo."""
    import base64
    candidates = [
        Path.cwd() / "assets" / "ynu_campus.jpg",
        Path.cwd() / "ynu_campus.jpg",
        Path(__file__).resolve().parent / "assets" / "ynu_campus.jpg",
        Path(__file__).resolve().parent / "ynu_campus.jpg",
    ]
    for img_path in candidates:
        try:
            if img_path.exists():
                encoded = base64.b64encode(img_path.read_bytes()).decode("utf-8")
                return f"data:image/jpeg;base64,{encoded}"
        except Exception:
            pass
    return ""

CAMPUS_BG = _campus_bg_data_uri()
HERO_BG_STYLE = (
    f"linear-gradient(90deg, rgba(2,6,23,.70) 0%, rgba(15,23,42,.42) 44%, rgba(88,28,135,.54) 100%), url('{CAMPUS_BG}')"
    if CAMPUS_BG
    else "linear-gradient(135deg, #020617 0%, #111827 48%, #4c1d95 100%)"
)

TEAM = [
    ("MAMUNUR RASHID", "Product • UI • Integration"),
    ("MD FAHIM", "Feature Logic • Testing"),
    ("MD JIARUL ISLAM", "Data • Research • Support"),
]

TOPIC_PACKS = {
    "Quantum Mechanics": {
        "tiny": "Quantum mechanics studies how very tiny things, like electrons and atoms, behave.",
        "simple": ["Tiny things do not always behave like balls or stones.", "An electron can act like a small particle and also like a wave.", "Before we measure it, we often describe possible results using probability.", "Measurement helps us get one clear result from many possible results.", "So quantum mechanics is the rulebook for the tiny world."],
        "analogy": "Think of a spinning coin. Before it lands, it has possibilities. After it lands, you see one result.",
        "keywords": ["particle", "wave", "probability", "measurement", "superposition", "uncertainty"],
        "mistake": "Superposition does not mean magic. It means we describe possible states before measurement.",
        "questions": ["Why do tiny particles need probability?", "What changes when we measure a quantum system?", "How can something behave like both a wave and a particle?", "Why is uncertainty important?", "How is this useful in quantum computers?"],
        "source": "Curated introductory physics concept pack for demo stability."
    },
    "Machine Learning": {
        "tiny": "Machine learning is when computers learn patterns from data and use them to make predictions.",
        "simple": ["A normal program follows rules written by humans.", "A machine learning system learns rules from examples.", "If we show it many house prices, it can learn what affects price.", "Then it can predict the price of a new house.", "The better the data, the better the learning."],
        "analogy": "It is like learning to recognize mangoes after seeing many mangoes, not by memorizing one mango only.",
        "keywords": ["data", "model", "training", "prediction", "features", "accuracy"],
        "mistake": "Machine learning does not truly understand like a human. It finds useful patterns in data.",
        "questions": ["What is the difference between training data and test data?", "Why can bad data make a model bad?", "How do features help prediction?", "What does accuracy mean?", "Can a machine learning model be biased?"],
        "source": "Curated AI/ML concept pack for demo stability."
    },
    "Python Programming": {
        "tiny": "Python is a programming language used to tell computers what to do.",
        "simple": ["Python lets us write instructions in a readable way.", "We store information using variables.", "We repeat work using loops.", "We organize code using functions.", "Python is popular because it is simple and useful for AI."],
        "analogy": "Python is like giving a recipe to a computer: first do this, then do that.",
        "keywords": ["variable", "function", "loop", "condition", "list", "program"],
        "mistake": "Python is easy to start, but professional Python still needs clean logic and good structure.",
        "questions": ["Why are functions useful?", "What is a variable?", "Why do loops save time?", "How does an if statement control flow?", "Why is Python used in AI?"],
        "source": "Curated programming concept pack for demo stability."
    },
    "Convolutional Neural Network": {
        "tiny": "A CNN is a neural network that learns visual patterns from images.",
        "simple": ["Images are made of pixels.", "A CNN uses filters to find small patterns like edges.", "Deeper layers combine small patterns into bigger ideas like eyes, wheels, or shapes.", "Pooling makes the image information smaller but keeps important parts.", "Finally, the network predicts what the image may contain."],
        "analogy": "It is like first noticing lines in a drawing, then shapes, then the full object.",
        "keywords": ["filter", "feature map", "convolution", "pooling", "layer", "classification"],
        "mistake": "A CNN does not see like humans. It learns mathematical patterns from pixels.",
        "questions": ["Why do CNNs use filters?", "What is a feature map?", "Why is pooling useful?", "How does a CNN learn from images?", "Where are CNNs used?"],
        "source": "Curated deep learning concept pack for demo stability."
    },
    "Natural Language Processing": {
        "tiny": "NLP helps computers understand and work with human language.",
        "simple": ["Human language is messy and full of meaning.", "NLP breaks text into useful pieces.", "It can find sentiment, translate sentences, summarize text, or answer questions.", "Modern NLP uses machine learning and large language models.", "The goal is to make computers handle language more naturally."],
        "analogy": "NLP is like teaching a computer to read, listen, and reply more like a helpful assistant.",
        "keywords": ["token", "embedding", "language model", "sentiment", "translation", "summary"],
        "mistake": "NLP does not always understand meaning perfectly. It can still misunderstand context.",
        "questions": ["What is tokenization?", "Why are embeddings useful?", "How does sentiment analysis work?", "Why is language hard for computers?", "What are NLP applications?"],
        "source": "Curated NLP concept pack for demo stability."
    },
    "Statistics": {
        "tiny": "Statistics helps us understand data and make decisions from it.",
        "simple": ["Data can be messy.", "Statistics helps us summarize data using mean and median.", "It helps us understand spread using variance and standard deviation.", "It helps us decide whether a result is meaningful.", "So statistics turns raw numbers into useful understanding."],
        "analogy": "It is like looking at many exam marks and finding the story behind the class performance.",
        "keywords": ["mean", "median", "variance", "standard deviation", "probability", "hypothesis"],
        "mistake": "Statistics is not just calculation. It is about interpreting what numbers mean.",
        "questions": ["Why do we need standard deviation?", "What is the difference between mean and median?", "How does probability support statistics?", "What is a hypothesis test?", "Why can data be misleading?"],
        "source": "Curated statistics concept pack for demo stability."
    },
    "SQL": {
        "tiny": "SQL is a language used to ask questions from databases.",
        "simple": ["A database stores data in tables.", "SQL lets us select, filter, update, and join data.", "A SELECT query asks the database to show information.", "A WHERE condition filters the result.", "A JOIN connects related tables."],
        "analogy": "SQL is like asking a librarian: show me only the books about AI written after 2020.",
        "keywords": ["table", "select", "where", "join", "primary key", "database"],
        "mistake": "SQL is not only for searching. It also manages and updates structured data.",
        "questions": ["What does SELECT do?", "Why do we use WHERE?", "What is a primary key?", "Why are JOINs important?", "How is SQL used in real apps?"],
        "source": "Curated database concept pack for demo stability."
    },
    "Urban Water Management": {
        "tiny": "Urban water management helps cities manage clean water, wastewater, drainage, and floods.",
        "simple": ["Cities need safe water for people.", "They also need systems to remove dirty water.", "Rainwater must be drained so streets do not flood.", "Sensors and AI can help predict problems early.", "Good water management makes cities safer and healthier."],
        "analogy": "A city is like a body. Water pipes are like veins, and drainage is like cleaning waste from the body.",
        "keywords": ["water supply", "drainage", "wastewater", "flood", "sensor", "prediction"],
        "mistake": "Urban water management is not only about water pipes. It includes planning, health, environment, and technology.",
        "questions": ["How can AI help predict urban flooding?", "Why is drainage important?", "What happens if wastewater is not treated?", "How can sensors improve water management?", "Why is water planning important?"],
        "source": "Curated smart-city concept pack connected to AI research direction."
    },
}

ALIASES = {"cnn": "Convolutional Neural Network", "nlp": "Natural Language Processing", "ml": "Machine Learning", "ai": "Artificial Intelligence", "quantum": "Quantum Mechanics", "python": "Python Programming", "urban water": "Urban Water Management"}

def norm(x):
    return re.sub(r"\s+", " ", x.strip().lower())

def fallback_pack(topic):
    return {
        "tiny": f"{topic} can be understood by breaking it into one main idea, one example, and one quick question.",
        "simple": ["First, find the main idea.", "Then explain that idea using simple words.", "Next, connect it to a real-life example.", "After that, check one common mistake.", "Finally, ask one question to test understanding."],
        "analogy": "Learning a new topic is like building with blocks: one small block at a time.",
        "keywords": ["main idea", "example", "concept", "mistake", "question", "memory"],
        "mistake": "A topic feels hard when the first idea is not explained simply enough.",
        "questions": ["What is the simplest definition?", "Where is it used?", "What is the common mistake?", "What should I remember first?", "How can I explain it to a friend?"],
        "source": "Generated fallback concept pack. Future version should ground this with retrieval and citations."
    }

def get_pack(topic):
    key = ALIASES.get(norm(topic), topic)
    return TOPIC_PACKS.get(key, fallback_pack(topic)), key

def quiz_for(pack):
    k = pack["keywords"]
    return [
        ("Which word is most connected to this topic?", [k[0].title(), "Random Noise", "Cooking Oil", "Shoe Size"], k[0].title(), f"{k[0].title()} is a core keyword for this topic."),
        ("What is the best strategy for a confusing topic?", ["Memorize blindly", "Break it into small ideas", "Skip it", "Only read the title"], "Break it into small ideas", "Small ideas reduce confusion and make memory stronger."),
        ("Why does Preluma use a quick check?", ["To test understanding quickly", "To make class longer", "To confuse students", "To replace teachers"], "To test understanding quickly", "A quick check shows whether the main idea is understood."),
        ("What should the student do after the brief?", ["Ask a better class question", "Forget it", "Avoid examples", "Stop learning"], "Ask a better class question", "The goal is class readiness, not only reading."),
    ]

def tutor_answer(topic, question):
    pack, _ = get_pack(topic)
    return [
        "Let's make it very simple.",
        pack["simple"][0],
        pack["simple"][1] if len(pack["simple"]) > 1 else pack["tiny"],
        f"Example: {pack['analogy']}",
        f"Common mistake: {pack['mistake']}",
        "Memory trick: remember the example first, then the definition."
    ]

# V15.4 verified hero image layer: CSS contains .hero-img, .hero-overlay, .hero-content
st.set_page_config(page_title="Preluma Product Prototype", layout="wide", page_icon="✨")

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');
html, body, [class*="css"] {font-family: 'Inter', sans-serif;}
.block-container {padding-top: 1rem; max-width: 1180px;}
[data-testid="stSidebar"] {background:#071021;}
[data-testid="stSidebar"] * {color:#e5e7eb;}
.hero {position:relative; padding:34px 36px; min-height:250px; border-radius:30px; overflow:hidden; border:1px solid rgba(125,211,252,.22); background:linear-gradient(135deg,#020617 0%,#111827 48%,#4c1d95 100%); box-shadow:0 28px 60px rgba(2,6,23,.4);}


.hero-content {position:relative; z-index:2;}
.brand-row {display:flex; align-items:center; gap:14px; margin-bottom:18px;}
.logo-mark {width:42px;height:42px;border-radius:15px;background:linear-gradient(135deg,#38bdf8,#8b5cf6);box-shadow:0 12px 28px rgba(56,189,248,.22);}
.brand-title {font-weight:900;color:#fff;font-size:18px}.brand-sub{color:#dbeafe;font-size:13px;margin-top:2px}
.badge,.uni-badge {display:inline-block;padding:8px 13px;border-radius:999px;font-weight:850;font-size:13px}.badge{background:rgba(14,165,233,.16);border:1px solid rgba(125,211,252,.35);color:#bae6fd}.uni-badge{background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.25);color:#fff;margin-left:8px}
.hero h1{font-size:40px;line-height:1.05;color:#fff;margin:30px 0 14px}.hero p{font-size:16px;max-width:850px;color:#e0f2fe;line-height:1.6}
.step{display:inline-block;padding:10px 14px;margin:4px 5px 8px 0;border-radius:999px;background:#eef2ff;color:#3730a3;font-weight:900;font-size:13px}
.clean-team{margin-top:18px;padding:16px;border-radius:22px;background:linear-gradient(135deg,rgba(15,23,42,.85),rgba(30,41,59,.75));border:1px solid rgba(148,163,184,.22)}.team-title{color:#93c5fd;font-size:12px;font-weight:900;letter-spacing:.09em;text-transform:uppercase;margin-bottom:10px}.team-list{display:flex;flex-direction:column;gap:8px}.team-item{padding:10px 12px;border-radius:14px;background:rgba(255,255,255,.045);border:1px solid rgba(255,255,255,.09)}.team-name{font-weight:900;color:#fff;font-size:12px}.team-role{font-size:11px;color:#94a3b8;margin-top:2px}
.metric-row{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:16px 0 8px}.metric-card{padding:16px 18px;border-radius:20px;background:linear-gradient(135deg,rgba(15,23,42,.92),rgba(30,41,59,.8));border:1px solid rgba(148,163,184,.22)}.metric-number{font-size:25px;color:#fff;font-weight:900}.metric-label{font-size:12px;color:#93c5fd;font-weight:900;letter-spacing:.08em;text-transform:uppercase;margin-top:5px}
.flow-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin:18px 0}.flow-card,.answer-card{padding:18px 20px;border-radius:22px;background:rgba(15,23,42,.72);border:1px solid rgba(148,163,184,.2)}.flow-card small,.answer-title{color:#93c5fd;font-size:13px;font-weight:900;text-transform:uppercase;letter-spacing:.08em}.flow-card h3{color:#fff;margin:8px 0}.flow-card p,.answer-card p,.answer-card li{color:#e5e7eb;line-height:1.6}.answer-card{margin:12px 0}.answer-title{margin-bottom:8px}.notice,.warning{padding:13px 15px;border-radius:17px;line-height:1.55;margin-bottom:12px}.notice{background:rgba(59,130,246,.12);border:1px solid rgba(96,165,250,.24);color:#dbeafe}.warning{background:rgba(245,158,11,.12);border:1px solid rgba(245,158,11,.25);color:#fef3c7}.footer-note{color:#94a3b8;font-size:13px}
@media(max-width:900px){.metric-row,.flow-grid{grid-template-columns:1fr}.hero{padding:24px 22px}.hero h1{font-size:30px}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

if "answer" not in st.session_state: st.session_state.answer = None
if "pack" not in st.session_state: st.session_state.pack = None
if "topic" not in st.session_state: st.session_state.topic = "Quantum Mechanics"
if "quiz" not in st.session_state: st.session_state.quiz = []
if "history" not in st.session_state: st.session_state.history = []

st.sidebar.markdown(f"## {APP_NAME}")
st.sidebar.caption(TAGLINE)
page = st.sidebar.radio("Workspace", ["Student Mission", "Teacher Studio", "Evidence Board", "Demo Guide", "Future Roadmap"])
st.sidebar.toggle("Presentation Mode", value=True)
st.sidebar.caption("Stable concept-level packs for smooth live demo.")

if CAMPUS_BG:
    st.sidebar.caption("Campus image loaded.")
else:
    st.sidebar.caption("Campus image not found. Upload assets/ynu_campus.jpg.")

st.sidebar.markdown("""
<div class='clean-team'><div class='team-title'>Project Team</div><div class='team-list'>
<div class='team-item'><div class='team-name'>MAMUNUR RASHID</div><div class='team-role'>Product • UI • Integration</div></div>
<div class='team-item'><div class='team-name'>MD FAHIM</div><div class='team-role'>Feature Logic • Testing</div></div>
<div class='team-item'><div class='team-name'>MD JIARUL ISLAM</div><div class='team-role'>Data • Research • Support</div></div>
</div></div>
""", unsafe_allow_html=True)
st.sidebar.markdown("---")
if st.sidebar.button("Reset session"):
    st.session_state.answer = None; st.session_state.pack = None; st.session_state.quiz = []
    st.rerun()
st.sidebar.markdown(f"<span class='footer-note'>Version {APP_VERSION}</span>", unsafe_allow_html=True)

def hero():
    if CAMPUS_BG:
        hero_bg = f"linear-gradient(90deg, rgba(2,6,23,.70) 0%, rgba(15,23,42,.44) 45%, rgba(88,28,135,.50) 100%), url('{CAMPUS_BG}')"
        campus_status = "Campus image loaded."
    else:
        hero_bg = "linear-gradient(135deg, #020617 0%, #111827 48%, #4c1d95 100%)"
        campus_status = "Campus image not found."
    st.markdown(f"""
    <div class='hero' style="background-image: {hero_bg};">
        <div class='hero-content'>
            <div class='brand-row'>
                <div class='logo-mark'></div>
                <div>
                    <div class='brand-title'>Preluma</div>
                    <div class='brand-sub'>Light Up Before Class</div>
                </div>
                <span class='uni-badge'>Yunnan University</span>
            </div>
            <span class='badge'>Pre-class brain priming</span>
            <h1>Understand any topic before class.</h1>
            <p>Preluma turns passive preparation into a short learning mission: simple explanation, quick quiz, mistake clinic, UltraTutor, and class-ready questions.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

def overview():
    st.markdown(" ".join([f"<span class='step'>{s}</span>" for s in ["Topic", "Tiny Answer", "Explain Simply", "Quiz", "Mistake Clinic", "UltraTutor", "Class Questions"]]), unsafe_allow_html=True)
    st.markdown("""<div class='metric-row'><div class='metric-card'><div class='metric-number'>1</div><div class='metric-label'>Tiny Answer</div></div><div class='metric-card'><div class='metric-number'>4</div><div class='metric-label'>Quiz Checks</div></div><div class='metric-card'><div class='metric-number'>5</div><div class='metric-label'>Class Questions</div></div><div class='metric-card'><div class='metric-number'>ELI5</div><div class='metric-label'>Simple English</div></div></div>""", unsafe_allow_html=True)
    st.markdown("""<div class='flow-grid'><div class='flow-card'><small>STEP 1</small><h3>Prime the brain</h3><p>Start with a tiny answer and a clear explanation before lecture.</p></div><div class='flow-card'><small>STEP 2</small><h3>Find weak spots</h3><p>Use a short quiz and mistake explanation to detect misunderstanding.</p></div><div class='flow-card'><small>STEP 3</small><h3>Ask better questions</h3><p>Leave with class-ready questions and a readiness score.</p></div></div>""", unsafe_allow_html=True)

def render_answer(topic, pack):
    st.markdown("### Brain Brief")
    st.markdown(f"<div class='answer-card'><div class='answer-title'>Tiny answer</div><p>{pack['tiny']}</p></div>", unsafe_allow_html=True)
    st.markdown("<div class='answer-card'><div class='answer-title'>Explain it simply</div><ol>" + "".join(f"<li>{x}</li>" for x in pack["simple"]) + "</ol></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='answer-card'><div class='answer-title'>Real-life example</div><p>{pack['analogy']}</p></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='answer-card'><div class='answer-title'>Common mistake</div><p>{pack['mistake']}</p></div>", unsafe_allow_html=True)
    st.markdown("<div class='answer-card'><div class='answer-title'>Hard words made easy</div><ul>" + "".join(f"<li><b>{k.title()}</b> — an important word for this topic.</li>" for k in pack["keywords"][:6]) + "</ul></div>", unsafe_allow_html=True)
    with st.expander("Sources and reliability note"):
        st.write(pack["source"])
        st.info("Future product version will use retrieval from course notes, Wikipedia/Wikimedia, and licensed open-access sources with citations.")

def student_mission():
    hero(); overview()
    st.markdown("### Mission Control")
    st.markdown("<div class='notice'>Ask any academic topic. Preluma will explain it in tiny steps, then check understanding with a short quiz.</div>", unsafe_allow_html=True)
    with st.container(border=True):
        c1,c2,c3 = st.columns([1.15,1,1])
        with c1:
            student = st.text_input("Student", "Mim")
            choice = st.selectbox("Lecture topic", list(TOPIC_PACKS.keys()) + ["Custom topic"])
            topic = st.text_input("Type any topic", "Entropy") if choice == "Custom topic" else choice
            lecture_time = st.text_input("Lecture time", "Tomorrow 9 AM")
        with c2:
            st.radio("Learning mode", ["Tiny steps", "Class-ready", "Deeper dive"], captions=["ELI5 simple", "Lecture focused", "More detail"])
        with c3:
            st.radio("Feedback style", ["Supportive", "Direct", "Challenge"], captions=["Encouraging", "Clear", "Push me"])
        if st.button("Start Explanation", use_container_width=True):
            pack, canon = get_pack(topic)
            st.session_state.pack = pack; st.session_state.topic = canon; st.session_state.quiz = quiz_for(pack); st.session_state.answer = True
            st.session_state.history.append({"student": student, "topic": canon, "time": datetime.now().isoformat()})
            st.rerun()
    if st.session_state.answer and st.session_state.pack:
        pack = st.session_state.pack; topic = st.session_state.topic
        render_answer(topic, pack)
        st.markdown("### Quick Quiz")
        answers = {}
        with st.form("quiz"):
            for i,(q, opts, ans, why) in enumerate(st.session_state.quiz):
                answers[i] = st.radio(q, opts, key=f"quiz_{i}")
            submit = st.form_submit_button("Check My Readiness", use_container_width=True)
        if submit:
            score = sum(answers[i] == item[2] for i,item in enumerate(st.session_state.quiz))
            total = len(st.session_state.quiz); readiness = int(score/total*100)
            st.success(f"Readiness Score: {readiness}% ({score}/{total})")
            st.markdown("### Mistake Clinic")
            for i,item in enumerate(st.session_state.quiz):
                q, opts, ans, why = item; correct = answers[i] == ans
                with st.expander(f"Question {i+1}: {'Correct' if correct else 'Review needed'}"):
                    st.write(f"Your answer: {answers[i]}")
                    st.write(f"Correct answer: {ans}")
                    st.write(f"Why: {why}")
                    if not correct:
                        st.info("Kid-simple fix: The correct answer connects directly to the main idea. Read the tiny answer again, then explain it in one sentence.")
        st.markdown("### UltraTutor")
        st.markdown("<div class='notice'>Confused about one idea? Ask UltraTutor. It explains like a friendly senior before class.</div>", unsafe_allow_html=True)
        tq = st.text_input("What did you not understand?", "I do not understand the main idea")
        if st.button("Explain Clearly"):
            for line in tutor_answer(topic, tq): st.write(f"- {line}")
        st.markdown("### Smart Class Questions")
        for i,q in enumerate(pack["questions"],1): st.write(f"{i}. {q}")
        brief = {"topic": topic, "tiny_answer": pack["tiny"], "simple_explanation": pack["simple"], "analogy": pack["analogy"], "class_questions": pack["questions"]}
        st.download_button("Download Study Brief", json.dumps(brief, indent=2), file_name=f"preluma_{norm(topic).replace(' ','_')}_brief.json", mime="application/json", use_container_width=True)

def teacher_studio():
    hero(); st.markdown("### Teacher Studio")
    st.markdown("<div class='notice'>This panel shows how a teacher could monitor class readiness in a future product version.</div>", unsafe_allow_html=True)
    data = pd.DataFrame({"Student":["Mim","Alex","Sara","Fahim","Jiarul","Mamunur"],"Readiness":[72,88,65,81,77,84],"Weak Skill":["Concept","None","Keyword","Example","Mistake","Question"],"Topic":["Quantum Mechanics","Machine Learning","Statistics","SQL","CNN","Urban Water Management"]})
    c1,c2 = st.columns([1.1,1])
    with c1: st.dataframe(data, use_container_width=True)
    with c2: st.plotly_chart(px.bar(data, x="Student", y="Readiness", color="Topic", title="Class Readiness Overview"), use_container_width=True)
    st.write("Teacher can identify weak topics, prepare warm-up questions, and export readiness reports.")

def evidence_board():
    hero(); st.markdown("### Evidence Board")
    st.markdown("<div class='warning'>Preluma is designed as a pre-class readiness system, not just a quiz app.</div>", unsafe_allow_html=True)
    c1,c2,c3 = st.columns(3)
    with c1:
        st.markdown("#### Problem"); st.write("- Students attend lectures unprepared.\n- Passive learning reduces retention.\n- Existing tools often feel like boring summaries.")
    with c2:
        st.markdown("#### Solution"); st.write("- Tiny answer\n- Simple explanation\n- Quick quiz\n- Mistake clinic\n- UltraTutor\n- Class questions")
    with c3:
        st.markdown("#### Innovation"); st.write("- Pre-class brain priming\n- ELI5 explanation mode\n- Readiness score\n- Teacher analytics\n- Future RAG architecture")
    st.markdown("### Technology Stack")
    st.dataframe(pd.DataFrame({"Layer":["Frontend","Logic","Data","Visualization","Future Backend","Future AI"],"Tool":["Streamlit","Python","Curated concept packs","Plotly","FastAPI + PostgreSQL","RAG + Embeddings"],"Purpose":["Interactive web demo","Quiz/tutor logic","Stable demo content","Teacher analytics","Scalable app architecture","Any-topic grounded answers"]}), use_container_width=True)
    st.markdown("### Quality Rubric")
    st.dataframe(pd.DataFrame({"Dimension":["Accuracy","Simplicity","Engagement","Mistake Help","Class Readiness"],"Target":["Source-grounded","5-year-old-level English","Short mission flow","Explain why wrong","Better questions before lecture"],"Status":["Demo-ready","Improved","Improved","Built","Built"]}), use_container_width=True)

def demo_guide():
    hero(); st.markdown("### 3-Minute Demo Script")
    steps = ["Open Student Mission and explain the problem.", "Choose Quantum Mechanics or Machine Learning.", "Click Start Explanation.", "Show Tiny Answer, Simple Explanation, and Real-life Example.", "Answer one quiz item wrong to show Mistake Clinic.", "Ask UltraTutor: I do not understand superposition.", "Show Teacher Studio and Evidence Board.", "End: Preluma prepares students to understand class better."]
    for i,s in enumerate(steps,1): st.write(f"{i}. {s}")
    st.success("Final line: Preluma turns passive students into lecture-ready learners through short, simple, and interactive preparation.")

def roadmap():
    hero(); st.markdown("### Future Product Roadmap")
    st.dataframe(pd.DataFrame({"Phase":["Phase 1","Phase 2","Phase 3","Phase 4"],"Goal":["University final demo","Real prototype","AI-powered product","Mobile app"],"Features":["Polished Streamlit, better data, demo script, report","Login, database, saved history, teacher dashboard","RAG, PDF upload, citations, Bangla support, safety checks","React Native/Flutter app, notifications, class codes"],"Priority":["Now","Next","After validation","Future"]}), use_container_width=True)
    st.markdown("### Product Architecture")
    st.code("""Student topic input → Query router → Course notes/Wikipedia/licensed sources → Hybrid retrieval → ELI5 answer generator → Quiz + Mistake Clinic → Teacher analytics""", language="text")
    st.markdown("### 5-Day Team Sprint")
    for s in ["Day 1: UI cleanup + topic/data expansion", "Day 2: Better tutor explanations + quiz logic", "Day 3: Teacher Studio + Evidence Board + export", "Day 4: Mobile view + testing + bug fixing", "Day 5: Report + slides + demo rehearsal"]: st.write(f"- {s}")

if page == "Student Mission": student_mission()
elif page == "Teacher Studio": teacher_studio()
elif page == "Evidence Board": evidence_board()
elif page == "Demo Guide": demo_guide()
else: roadmap()
