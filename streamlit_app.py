from pathlib import Path
import base64
import json

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from engine import build_brain_brief, build_pack, grade, make_questions, tutor_sections
from teacher import build_teacher_dataframe, class_average_readiness, readiness_label
from topics import TOPIC_OPTIONS, validate_topics
from wiki_fetcher import smart_answer_from_pack

APP_VERSION = "18.0 Premium Stable Final"
APP_NAME = "Preluma"
TAGLINE = "Light Up Before Class"

TEAM_MEMBERS = [
    ("MAMUNUR RASHID", "Core Development • UI/UX • Integration • Deployment"),
    ("MD FAHIM", "Feature Logic • Quiz Testing • Interaction Feedback"),
    ("MD JIARUL ISLAM", "Topic Data • Documentation • Presentation Support"),
]

CAMPUS_IMAGE = Path("assets/ynu_campus.jpg")
TEAM_IMAGE = Path("assets/team_preluma.jpg")

st.set_page_config(page_title=APP_NAME, page_icon="✨", layout="wide")


@st.cache_data(show_spinner=False)
def image_data_uri(path_str):
    path = Path(path_str)
    if path.exists():
        suffix = path.suffix.lower().replace(".", "")
        mime = "jpeg" if suffix in ["jpg", "jpeg"] else "png"
        data = base64.b64encode(path.read_bytes()).decode("ascii")
        return f"data:image/{mime};base64,{data}"
    return ""


CAMPUS_URI = image_data_uri(str(CAMPUS_IMAGE))
TEAM_URI = image_data_uri(str(TEAM_IMAGE))


CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');
html, body, [class*="css"] {font-family: 'Inter', sans-serif;}
.block-container {max-width: 1180px; padding-top: 1.3rem;}
[data-testid="stSidebar"] {background: #071021;}
[data-testid="stSidebar"] * {color: #e5e7eb;}
h1, h2, h3 {letter-spacing: -0.02em;}
.hero {
    position: relative;
    padding: 34px 38px;
    min-height: 285px;
    border-radius: 30px;
    overflow: hidden;
    border: 1px solid rgba(125,211,252,.22);
    background-size: cover;
    background-position: center;
    box-shadow: 0 28px 60px rgba(2,6,23,.46);
    margin-bottom: 16px;
}
.hero::after {
    content: "";
    position: absolute;
    inset: 0;
    background:
      linear-gradient(90deg, rgba(2,6,23,.83) 0%, rgba(15,23,42,.55) 48%, rgba(88,28,135,.47) 100%),
      radial-gradient(circle at 20% 10%, rgba(14,165,233,.25), transparent 32%);
    z-index: 1;
}
.hero-content {position: relative; z-index: 2;}
.brand-row {display:flex; align-items:center; gap:14px; margin-bottom:18px;}
.logo-mark {
    width:42px; height:42px; border-radius:15px;
    background: linear-gradient(135deg,#38bdf8,#8b5cf6);
    box-shadow: 0 12px 28px rgba(56,189,248,.22);
}
.brand-title {font-weight:900; color:#fff; font-size:18px;}
.brand-sub {color:#dbeafe; font-size:13px; margin-top:2px;}
.badge {
    display:inline-block; padding:8px 13px; border-radius:999px;
    background:rgba(14,165,233,.17); border:1px solid rgba(125,211,252,.36);
    color:#bae6fd; font-weight:850; font-size:13px;
}
.uni-badge {
    display:inline-block; padding:8px 13px; border-radius:999px;
    background:rgba(255,255,255,.12); border:1px solid rgba(255,255,255,.24);
    color:#fff; font-weight:850; font-size:12px; margin-left:8px;
}
.hero h1 {font-size:40px; line-height:1.08; color:white; margin:28px 0 14px; max-width: 950px; text-shadow:0 4px 22px rgba(0,0,0,.52);}
.hero p {font-size:16px; max-width: 860px; color:#e0f2fe; line-height:1.6; text-shadow:0 3px 16px rgba(0,0,0,.42);}
.chip {
    display:inline-block; padding:10px 14px; margin: 4px 6px 8px 0;
    border-radius:999px; background:#eef2ff; color:#3730a3;
    font-weight:900; font-size:13px;
}
.card {
    padding: 18px 20px; border-radius:22px;
    background: linear-gradient(135deg, rgba(15,23,42,.94), rgba(30,41,59,.82));
    border:1px solid rgba(125,211,252,.18);
}
.metric-grid {display:grid; grid-template-columns: repeat(4, 1fr); gap:12px; margin: 14px 0 18px;}
.metric-number {font-size:26px; color:#fff; font-weight:900;}
.metric-label {font-size:12px; color:#93c5fd; font-weight:900; letter-spacing:.08em; text-transform:uppercase; margin-top:5px;}
.flow-grid {display:grid; grid-template-columns: repeat(3, 1fr); gap:16px; margin:16px 0;}
.flow-card small {color:#93c5fd; font-weight:900; letter-spacing:.08em;}
.flow-card h3 {color:#fff; margin:8px 0 8px; font-size:21px;}
.flow-card p {color:#cbd5e1; line-height:1.55;}
.answer-card {
    padding: 18px 20px;
    border-radius: 22px;
    background: rgba(15,23,42,.72);
    border: 1px solid rgba(148,163,184,.20);
    margin: 12px 0;
}
.answer-title {
    color:#93c5fd; font-size:13px; font-weight:900;
    text-transform:uppercase; letter-spacing:.08em; margin-bottom:8px;
}
.answer-card p, .answer-card li {color:#e5e7eb; font-size:15px; line-height:1.6;}
.notice {
    padding: 13px 15px; border-radius: 17px;
    background: rgba(59,130,246,.12);
    border: 1px solid rgba(96,165,250,.24);
    color:#dbeafe; line-height:1.55; margin-bottom:12px;
}
.prof-grid {display:grid; grid-template-columns: repeat(3, 1fr); gap:14px; margin:16px 0;}
.prof-card {
    padding:17px; border-radius:21px;
    background:linear-gradient(135deg, rgba(14,165,233,.13), rgba(124,58,237,.11));
    border:1px solid rgba(125,211,252,.22);
}
.prof-card h4 {margin:0 0 8px; color:#fff; font-size:17px;}
.prof-card p {color:#cbd5e1; font-size:14px; line-height:1.55;}
.team-hero {
    position: relative;
    min-height: 430px;
    border-radius: 32px;
    overflow: hidden;
    border: 1px solid rgba(125,211,252,.24);
    box-shadow: 0 28px 70px rgba(2,6,23,.50);
    background-size: cover;
    background-position: center 42%;
    margin-bottom: 22px;
}
.team-hero::after {
    content:"";
    position:absolute;
    inset:0;
    background:
      linear-gradient(90deg, rgba(2,6,23,.78) 0%, rgba(15,23,42,.34) 48%, rgba(88,28,135,.43) 100%),
      linear-gradient(0deg, rgba(2,6,23,.88) 0%, rgba(2,6,23,.12) 48%, rgba(2,6,23,.30) 100%);
    z-index:1;
}
.team-hero-content {position:absolute; left:34px; bottom:30px; right:34px; z-index:2;}
.team-hero h1 {color:white; margin:0 0 10px; font-size:40px; line-height:1.08; text-shadow:0 5px 24px rgba(0,0,0,.55);}
.team-hero p {color:#e0f2fe; max-width:850px; font-size:16px; line-height:1.6; margin:0; text-shadow:0 3px 18px rgba(0,0,0,.45);}
.member-grid {display:grid; grid-template-columns: repeat(3, 1fr); gap:16px; margin:18px 0;}
.member-card {
    padding:20px; border-radius:24px;
    background:linear-gradient(135deg, rgba(15,23,42,.94), rgba(30,41,59,.82));
    border:1px solid rgba(125,211,252,.18);
    box-shadow:0 18px 45px rgba(2,6,23,.28);
}
.member-card.main {border-color:rgba(96,165,250,.45); background:linear-gradient(135deg, rgba(14,165,233,.17), rgba(124,58,237,.14));}
.member-role {color:#93c5fd; font-weight:900; font-size:12px; letter-spacing:.08em; text-transform:uppercase; margin-bottom:8px;}
.member-card h3 {color:#fff; margin:0 0 8px; font-size:21px;}
.member-card p {color:#cbd5e1; line-height:1.55; margin:0;}
.contribution-list {margin-top:12px; padding-left:18px; color:#e5e7eb;}
.contribution-list li {margin-bottom:6px;}
.stButton > button {
    border-radius: 14px !important;
    font-weight: 900 !important;
    min-height: 48px !important;
    border: 1px solid rgba(125,211,252,.35) !important;
    background: linear-gradient(135deg, rgba(37,99,235,.95), rgba(124,58,237,.92)) !important;
    color: white !important;
}
@media (max-width: 900px) {
    .metric-grid, .flow-grid, .prof-grid, .member-grid {grid-template-columns: 1fr;}
    .hero {padding: 24px 22px;}
    .hero h1, .team-hero h1 {font-size: 30px;}
    .team-hero {min-height:340px;}
}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)


def init_state():
    st.session_state.setdefault("student", "Mim")
    st.session_state.setdefault("topic", "Quantum Mechanics")
    st.session_state.setdefault("persona", "Normal Mode")


def reset_session():
    for key in ["student", "topic", "persona", "use_wiki", "pack", "brief", "questions", "quiz_result", "latest_session"]:
        st.session_state.pop(key, None)


def sidebar():
    st.sidebar.title(APP_NAME)
    st.sidebar.caption(TAGLINE)
    page = st.sidebar.radio(
        "Workspace",
        ["Student Mission", "Teacher Studio", "Evidence Board", "Project Team", "Demo Guide", "Future Roadmap"],
    )
    presentation = st.sidebar.toggle("Presentation Mode", value=True)
    st.sidebar.info("Python + Streamlit project. Styling is inside Streamlit for presentation; core logic is Python.")
    st.sidebar.subheader("Project Team")
    for name, role in TEAM_MEMBERS:
        st.sidebar.write(f"**{name}**")
        st.sidebar.caption(role)
    st.sidebar.divider()
    if st.sidebar.button("Reset session"):
        reset_session()
        st.rerun()
    st.sidebar.caption(f"Version {APP_VERSION}")
    return page, presentation


def hero():
    bg = f"linear-gradient(90deg, rgba(2,6,23,.80) 0%, rgba(15,23,42,.54) 48%, rgba(88,28,135,.50) 100%), url('{CAMPUS_URI}')" if CAMPUS_URI else "linear-gradient(135deg, #020617 0%, #111827 48%, #4c1d95 100%)"
    st.markdown(f"""
    <div class='hero' style="background-image: {bg};">
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
            <h1>Prepare before class. Understand more during class.</h1>
            <p>Preluma turns passive preparation into a Python-powered learning mission: Brain Brief, quiz, Mistake Clinic, Smart QnA, Teacher Studio, and class-ready questions.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)


def chips():
    items = ["Topic", "Brain Brief", "Quiz", "Mistake Clinic", "Smart QnA", "Class Questions", "Dashboard"]
    st.markdown(" ".join([f"<span class='chip'>{item}</span>" for item in items]), unsafe_allow_html=True)


def metrics_and_steps():
    st.markdown("""
    <div class='metric-grid'>
        <div class='card'><div class='metric-number'>4</div><div class='metric-label'>Quiz Checks</div></div>
        <div class='card'><div class='metric-number'>5</div><div class='metric-label'>Class Questions</div></div>
        <div class='card'><div class='metric-number'>1</div><div class='metric-label'>Mistake Clinic</div></div>
        <div class='card'><div class='metric-number'>0–100</div><div class='metric-label'>Readiness Score</div></div>
    </div>
    <div class='flow-grid'>
        <div class='card flow-card'><small>STEP 1</small><h3>Prime the brain</h3><p>Start with a compact Brain Brief before the lecture.</p></div>
        <div class='card flow-card'><small>STEP 2</small><h3>Find weak spots</h3><p>Use a quiz and Mistake Clinic to detect misunderstanding.</p></div>
        <div class='card flow-card'><small>STEP 3</small><h3>Ask better questions</h3><p>Leave with class-ready questions and a readiness score.</p></div>
    </div>
    """, unsafe_allow_html=True)


def mission_control():
    st.markdown("### Mission Control")
    st.markdown("<div class='notice'>Choose a topic. Preluma will generate a pre-class learning mission using Python, curated topic data, and optional Wikipedia real-data fallback.</div>", unsafe_allow_html=True)

    with st.form("mission_form", border=True):
        c1, c2, c3 = st.columns([1, 1.25, 1])
        with c1:
            student = st.text_input("Student", value=st.session_state.student)
            lecture_time = st.text_input("Lecture time", value="Tomorrow 9 AM")
        with c2:
            current_topic = st.session_state.topic if st.session_state.topic in TOPIC_OPTIONS else "Quantum Mechanics"
            topic_choice = st.selectbox("Lecture topic", TOPIC_OPTIONS, index=TOPIC_OPTIONS.index(current_topic))
            if topic_choice == "Custom Topic":
                topic = st.text_input("Custom topic", value="Photosynthesis")
            else:
                topic = topic_choice
        with c3:
            persona = st.selectbox("Feedback style", ["Normal Mode", "Coach Mode", "Roast Mode"], index=0)
            use_wiki = st.checkbox("Use Wikipedia real data", value=True)
            st.caption("Brain Brief • Quiz • Smart QnA")
        start = st.form_submit_button("Start Pre-Class Mission", use_container_width=True)

    if start:
        with st.spinner("Building your pre-class mission..."):
            pack = build_pack(topic, use_wikipedia=use_wiki)
            st.session_state.student = student
            st.session_state.topic = topic
            st.session_state.persona = persona
            st.session_state.use_wiki = use_wiki
            st.session_state.pack = pack
            st.session_state.brief = build_brain_brief(pack)
            st.session_state.questions = make_questions(pack)
            st.session_state.quiz_result = None
            st.session_state.latest_session = None
        st.rerun()


def brain_brief():
    if "brief" not in st.session_state:
        return
    b = st.session_state.brief
    pack = st.session_state.pack
    st.markdown("### Brain Brief")
    st.markdown(f"""
    <div class='answer-card'><div class='answer-title'>Tiny answer</div><p>{b['tiny_answer']}</p></div>
    <div class='answer-card'><div class='answer-title'>Explain simply</div><p>{b['simple']}</p></div>
    <div class='answer-card'><div class='answer-title'>Key concept</div><p><b>{b['key_concept']}</b>: {b['concept_simple']}</p></div>
    <div class='answer-card'><div class='answer-title'>Real-life example</div><p>{b['example']}</p></div>
    <div class='answer-card'><div class='answer-title'>Common mistake</div><p>{b['misconception']}</p></div>
    """, unsafe_allow_html=True)
    with st.expander("Important facts and source"):
        for fact in b["facts"]:
            st.write(f"- {fact}")
        if pack.get("source_url"):
            st.success("Real data source used.")
            st.write(pack.get("source_url"))


def quiz():
    if "questions" not in st.session_state:
        return
    st.markdown("### Quick Quiz")
    with st.form("quiz_form", border=True):
        answers = {}
        for i, q in enumerate(st.session_state.questions):
            answers[i] = st.radio(q["q"], q["options"], key=f"quiz_{i}")
        submit = st.form_submit_button("Check Readiness", use_container_width=True)
    if submit:
        result = grade(st.session_state.questions, answers)
        st.session_state.quiz_result = result
        st.session_state.latest_session = {
            "Student": st.session_state.student,
            "Topic": st.session_state.pack["title"],
            "Readiness": result["pct"],
            "Weak Skill": result["weakest"],
        }
        st.rerun()


def result_and_mistake_clinic():
    result = st.session_state.get("quiz_result")
    if not result:
        return
    st.markdown("### Readiness Result")
    c1, c2 = st.columns(2)
    c1.metric("Your Readiness", f"{result['pct']}%", f"{result['score']}/{result['total']} correct")
    c2.metric("Status", readiness_label(result["pct"]))
    st.markdown("### Mistake Clinic")
    for i, item in enumerate(result["details"], 1):
        status = "Correct" if item["correct"] else "Review needed"
        with st.expander(f"Question {i}: {status} — {item['skill']}"):
            st.write(f"Your answer: {item['chosen']}")
            st.write(f"Correct answer: {item['answer']}")
            st.write(f"Why: {item['why']}")
            if not item["correct"]:
                st.info("Tiny fix: read the definition, connect it to one example, then explain it in your own words.")
    df = build_teacher_dataframe(st.session_state.latest_session)
    avg = class_average_readiness(df)
    fig = go.Figure()
    fig.add_bar(x=["You", "Class Average"], y=[result["pct"], avg])
    fig.update_layout(title="Readiness Comparison", yaxis_range=[0, 100], height=320, margin=dict(l=20, r=20, t=45, b=20))
    st.plotly_chart(fig, use_container_width=True)


def smart_qna():
    if "pack" not in st.session_state:
        return
    st.markdown("### Smart QnA + UltraTutor")
    question = st.text_input("Ask any question about this topic", value="Explain this topic with a simple example")
    c1, c2 = st.columns(2)
    ask = c1.button("Get Smart Answer", use_container_width=True)
    tutor = c2.button("Explain Like a Tutor", use_container_width=True)
    if ask:
        ans = smart_answer_from_pack(st.session_state.pack, question)
        st.markdown(f"""
        <div class='answer-card'><div class='answer-title'>Smart answer</div><p>{ans['answer']}</p></div>
        <div class='answer-card'><div class='answer-title'>Simple version</div><p>{ans['simple']}</p></div>
        <div class='answer-card'><div class='answer-title'>Example</div><p>{ans['example']}</p></div>
        <div class='answer-card'><div class='answer-title'>Reliability note</div><p>{ans['note']}</p></div>
        """, unsafe_allow_html=True)
        if ans.get("source_url"):
            st.caption(f"Source: {ans['source_url']}")
    if tutor:
        sections = tutor_sections(st.session_state.pack, question, st.session_state.persona)
        st.markdown(f"#### {sections['concept']}")
        st.markdown(f"""
        <div class='answer-card'><div class='answer-title'>Tiny answer</div><p>{sections['tiny_answer']}</p></div>
        <div class='answer-card'><div class='answer-title'>Explain simply</div><p>{sections['explain_simply']}</p></div>
        <div class='answer-card'><div class='answer-title'>Real-life example</div><p>{sections['real_life_example']}</p></div>
        <div class='answer-card'><div class='answer-title'>Common mistake</div><p>{sections['common_mistake']}</p></div>
        <div class='answer-card'><div class='answer-title'>Exam angle</div><p>{sections['exam_angle']}</p></div>
        """, unsafe_allow_html=True)


def class_questions_and_download():
    if "pack" not in st.session_state:
        return
    st.markdown("### Smart Class Questions")
    for i, question in enumerate(st.session_state.pack["class_questions"], 1):
        st.write(f"{i}. {question}")
    payload = {
        "student": st.session_state.student,
        "topic": st.session_state.pack["title"],
        "brief": st.session_state.brief,
        "class_questions": st.session_state.pack["class_questions"],
        "quiz_result": st.session_state.get("quiz_result"),
    }
    st.download_button(
        "Download Study Brief JSON",
        data=json.dumps(payload, indent=2),
        file_name=f"preluma_{st.session_state.pack['title'].lower().replace(' ', '_')}_brief.json",
        mime="application/json",
        use_container_width=True,
    )


def student_mission(presentation):
    hero()
    chips()
    mission_control()
    brain_brief()
    quiz()
    result_and_mistake_clinic()
    smart_qna()
    class_questions_and_download()
    if presentation:
        metrics_and_steps()


def teacher_studio():
    hero()
    st.markdown("### Teacher Studio")
    df = build_teacher_dataframe(st.session_state.get("latest_session"))
    st.dataframe(df, use_container_width=True)
    fig = px.bar(df, x="Student", y="Readiness", color="Weak Skill", title="Class Readiness")
    fig.update_layout(yaxis_range=[0, 100], height=360)
    st.plotly_chart(fig, use_container_width=True)
    st.metric("Class Average Readiness", f"{class_average_readiness(df)}%")


def evidence_board():
    hero()
    st.markdown("### Evidence Board")
    st.markdown("""
    <div class='prof-grid'>
        <div class='prof-card'><h4>Clear Problem</h4><p>Students often enter lectures unprepared, which leads to passive learning and poor retention.</p></div>
        <div class='prof-card'><h4>Python Implementation</h4><p>The project is built with Python, Streamlit, Pandas, Plotly, dictionaries, functions, forms, session state, and Requests.</p></div>
        <div class='prof-card'><h4>Learning Workflow</h4><p>Preluma combines Brain Brief, quiz, Mistake Clinic, Smart QnA, class questions, and readiness score.</p></div>
        <div class='prof-card'><h4>Real Data Upgrade</h4><p>Unknown topics can use Wikipedia API through Python Requests as a real-data fallback.</p></div>
        <div class='prof-card'><h4>Teacher Value</h4><p>Teacher Studio demonstrates readiness analytics and weak-skill detection.</p></div>
        <div class='prof-card'><h4>Testing</h4><p>Regression tests check topic data, core flow, Wikipedia argument support, and quiz logic.</p></div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("### Python Concepts Used")
    concepts = pd.DataFrame({
        "Concept": ["Functions", "Dictionaries", "Session State", "Forms", "DataFrame", "Plotly Charts", "Requests API", "File Export", "Testing"],
        "Use in Project": ["Reusable units", "Topic packs", "Remember user flow", "Safe submissions", "Analytics", "Readiness chart", "Wikipedia fetch", "Download JSON", "Stability tests"],
    })
    st.dataframe(concepts, use_container_width=True)
    errors = validate_topics()
    if errors:
        st.warning("Some topic validation issues were found.")
        for issue in errors:
            st.write(f"- {issue}")
    else:
        st.success("Topic data validation passed.")


def project_team():
    st.markdown("### Project Team")
    bg = f"url('{TEAM_URI}')" if TEAM_URI else "linear-gradient(135deg,#020617,#4c1d95)"
    st.markdown(f"""
    <div class='team-hero' style="background-image: {bg};">
        <div class='team-hero-content'>
            <span class='badge'>Team Preluma • Yunnan University</span>
            <h1>Built by students, for better pre-class learning.</h1>
            <p>This page shows the real project team and the workload distribution behind Preluma.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div class='member-grid'>
        <div class='member-card'>
            <div class='member-role'>Feature Logic • Quiz Testing</div>
            <h3>MD FAHIM</h3>
            <p>Supported quiz behavior checking, interaction feedback, and feature testing.</p>
            <ul class='contribution-list'><li>Quiz behavior checking</li><li>Interaction feedback</li><li>Feature testing support</li></ul>
        </div>
        <div class='member-card main'>
            <div class='member-role'>Core Development • UI/UX • Integration • Deployment</div>
            <h3>MAMUNUR RASHID</h3>
            <p>Handled the hardest core part of Preluma: product design, Python Streamlit UI, system integration, deployment, real-data upgrade, and final demo flow.</p>
            <ul class='contribution-list'><li>Main Python Streamlit app development</li><li>UI/UX design and premium interface polish</li><li>Core module integration and deployment</li><li>Wikipedia real-data and Smart QnA upgrade</li><li>Final demo flow and presentation preparation</li></ul>
        </div>
        <div class='member-card'>
            <div class='member-role'>Topic Data • Documentation</div>
            <h3>MD JIARUL ISLAM</h3>
            <p>Supported topic data organization, documentation, and presentation preparation.</p>
            <ul class='contribution-list'><li>Topic data support</li><li>Documentation support</li><li>Presentation support</li></ul>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("### Work Division")
    st.dataframe(pd.DataFrame({
        "Member": ["MAMUNUR RASHID", "MD FAHIM", "MD JIARUL ISLAM"],
        "Main Responsibility": ["Core development, UI/UX, system integration, deployment, real-data upgrade, final demo flow", "Feature logic, quiz testing, interaction feedback", "Topic data, documentation, presentation support"],
        "Project Value": ["Builds the hardest core system and connects all parts into one deployed Python Streamlit product", "Improves interaction quality and checks app behavior", "Strengthens content base and presentation material"],
    }), use_container_width=True)


def demo_guide():
    hero()
    st.markdown("### 3-Minute Demo Guide")
    steps = [
        "Say: Preluma is a Python Streamlit project for pre-class preparation.",
        "Explain the problem: students enter lectures unprepared.",
        "Choose a topic and start the mission.",
        "Show Brain Brief, quiz, Mistake Clinic, and Smart QnA.",
        "Show Teacher Studio and Evidence Board.",
        "Show Project Team and workload distribution.",
    ]
    for step in steps:
        st.write(step)
    st.success("Final line: Preluma does not replace teachers. It prepares students to understand teachers better.")


def roadmap():
    hero()
    st.markdown("### Future Roadmap")
    df = pd.DataFrame({
        "Phase": ["Current Python Demo", "Prototype", "AI Upgrade", "Real Product"],
        "Goal": ["Final project submission", "Student/teacher accounts", "RAG tutor with citations", "Mobile/web app"],
        "Technology": ["Python + Streamlit", "Python + database", "Python + retrieval", "Python backend + app frontend"],
        "Status": ["Now", "Next", "Later", "Future"],
    })
    st.dataframe(df, use_container_width=True)


def main():
    init_state()
    page, presentation = sidebar()
    if page == "Student Mission":
        student_mission(presentation)
    elif page == "Teacher Studio":
        teacher_studio()
    elif page == "Evidence Board":
        evidence_board()
    elif page == "Project Team":
        project_team()
    elif page == "Demo Guide":
        demo_guide()
    else:
        roadmap()


if __name__ == "__main__":
    main()
