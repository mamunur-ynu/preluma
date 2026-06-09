import json
import random
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from engine import build_pack, make_questions, grade, tutor, study_brief_markdown
from teacher import demo_teacher_data
from topics import TOPICS

APP_VERSION = "9.0"

st.set_page_config(page_title="Preluma", page_icon="●", layout="wide")

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
html, body, [class*="css"] {font-family: 'Inter', sans-serif;}
.block-container {padding-top: .8rem; max-width: 1160px;}
[data-testid="stSidebar"] {background: #080d1c;}
[data-testid="stSidebar"] * {color: #e5e7eb;}
.hero {
    padding: 24px 32px;
    border-radius: 28px;
    background:
        radial-gradient(circle at top left, rgba(14,165,233,.35), transparent 30%),
        radial-gradient(circle at bottom right, rgba(124,58,237,.34), transparent 34%),
        linear-gradient(135deg, #060914 0%, #111827 58%, #2e1065 100%);
    border: 1px solid rgba(255,255,255,.12);
    color: white;
    box-shadow: 0 22px 70px rgba(0,0,0,.30);
}
.hero h1 {font-size: 38px; line-height: 1.06; margin: 0 0 10px 0; letter-spacing: -1px;}
.hero p {font-size: 15px; max-width: 780px; color: #dbeafe; line-height: 1.55;}
.hero-tag {
    display: inline-block; padding: 6px 12px; border-radius: 999px;
    background: rgba(56,189,248,.16); border: 1px solid rgba(56,189,248,.34);
    color: #bae6fd; font-weight: 800; margin-bottom: 12px; font-size: 13px;
}
.step {
    display:inline-block; padding:7px 12px; margin:3px; border-radius:999px;
    background:#eef2ff; color:#3730a3; font-weight:800; font-size:13px;
}
.card {
    padding: 18px; border-radius: 20px; background: #ffffff;
    border: 1px solid #e5e7eb; box-shadow: 0 10px 28px rgba(15,23,42,.05);
}
.dark-card {
    padding: 18px; border-radius: 20px; background: #0f172a; color: #e5e7eb;
    border: 1px solid rgba(255,255,255,.10);
}
.mini-title {color:#64748b; font-size:13px; font-weight:900; text-transform:uppercase; letter-spacing:.08em;}
.badge-green {padding:12px 15px; border-radius:15px; background:#dcfce7; color:#166534; font-weight:900;}
.badge-yellow {padding:12px 15px; border-radius:15px; background:#fef3c7; color:#92400e; font-weight:900;}
.badge-red {padding:12px 15px; border-radius:15px; background:#fee2e2; color:#991b1b; font-weight:900;}
.footer-note {color:#94a3b8; font-size:13px;}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

if "pack" not in st.session_state:
    st.session_state.pack = None
if "questions" not in st.session_state:
    st.session_state.questions = None
if "result" not in st.session_state:
    st.session_state.result = None

def reset():
    st.session_state.pack = None
    st.session_state.questions = None
    st.session_state.result = None

def radar_fig(values):
    labels = list(values.keys())
    vals = list(values.values())
    labels.append(labels[0])
    vals.append(vals[0])
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=vals, theta=labels, fill="toself"))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=False,
        height=330,
        margin=dict(l=20, r=20, t=30, b=20),
    )
    return fig

st.sidebar.markdown("## Preluma")
st.sidebar.caption("Light Up Before Class")
page = st.sidebar.radio("Workspace", ["Student Mission", "Teacher Studio", "Evidence Board"])
presentation_mode = st.sidebar.toggle("Presentation Mode", True)
st.sidebar.caption("Uses stable curated lesson packs for smooth live demo.")
st.sidebar.markdown("---")
if st.sidebar.button("Reset session"):
    reset()
st.sidebar.markdown(f"<span class='footer-note'>Version {APP_VERSION}</span>", unsafe_allow_html=True)

if page == "Student Mission":
    st.markdown("""
    <div class="hero">
        <div class="hero-tag">Pre-class brain priming</div>
        <h1>Prepare before class. Understand more during class.</h1>
        <p>Preluma gives every student a Brain Brief, short quiz, Mistake Clinic, tutor help, and smart class questions before the lecture starts.</p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")
    st.markdown(" ".join([f"<span class='step'>{s}</span>" for s in ["Topic", "Brain Brief", "Quiz", "Mistake Clinic", "Tutor", "Class Questions", "Dashboard"]]), unsafe_allow_html=True)

    st.write("")
    with st.container(border=True):
        st.markdown("### Start a pre-class mission")
        left, mid, right = st.columns([1.1, 1, 1])
        with left:
            student = st.text_input("Student", "Mim")
            topic_options = ["Quantum Mechanics", "Machine Learning", "Artificial Intelligence", "Data Structures", "Python Programming", "Object Oriented Programming", "Neural Networks", "Linear Regression", "Database Systems", "Climate Change", "Custom topic"]
            chosen = st.selectbox("Lecture topic", topic_options)
            if chosen == "Custom topic":
                topic = st.text_input("Custom topic", "Natural Language Processing")
            else:
                topic = chosen
            lecture_time = st.text_input("Lecture time", "Tomorrow 9 AM")
        with mid:
            mood = st.radio("Study mood", ["Let's go", "Calm focus", "Last minute survival"], captions=["High energy", "Focused", "Quick survival"])
        with right:
            persona = st.radio("Feedback style", ["Normal Mode", "Coach Mode", "Roast Mode"], captions=["Direct", "Supportive", "Funny pressure"])

        if st.button("Start My Pre-Class Mission", use_container_width=True):
            st.session_state.pack = build_pack(topic)
            st.session_state.questions = make_questions(st.session_state.pack)
            st.session_state.result = None

    if st.session_state.pack:
        pack = st.session_state.pack

        st.markdown("---")
        st.markdown("### Brain Brief")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Topic", pack["title"])
        c2.metric("Confidence", f"{int(pack['confidence'] * 100)}%")
        c3.metric("Concepts", len(pack["concepts"]))
        c4.metric("Applications", len(pack["applications"]))
        st.caption(f"Source: {pack['source']}")

        a, b = st.columns([1.1, 0.9])
        with a:
            st.markdown(f"<div class='card'><div class='mini-title'>Definition</div><br>{pack['definition']}</div>", unsafe_allow_html=True)
            st.write("")
            st.info(pack["simple"])
        with b:
            st.markdown(f"<div class='dark-card'><div class='mini-title'>Why this matters</div><br>{pack['hook']}</div>", unsafe_allow_html=True)

        t1, t2, t3, t4 = st.tabs(["Core ideas", "Misconceptions", "Applications", "Facts"])
        t1.write(", ".join(pack["concepts"]))
        for m in pack["misconceptions"]:
            t2.warning(m)
        for app in pack["applications"]:
            t3.success(app)
        for fact in pack["facts"]:
            t4.info(fact)

        st.markdown("### Pre-class Quiz")
        selected = {}
        with st.form("quiz_form"):
            for i, q in enumerate(st.session_state.questions):
                st.markdown(f"**Q{i+1}. {q['q']}**")
                selected[i] = st.radio("Choose one", q["options"], index=None, key=f"q_{i}_{pack['title']}", label_visibility="collapsed")
            submitted = st.form_submit_button("Check My Readiness", use_container_width=True)

        if submitted:
            if any(v is None for v in selected.values()):
                st.warning("Answer all questions first.")
            else:
                st.session_state.result = grade(st.session_state.questions, selected)

    if st.session_state.result:
        pack = st.session_state.pack
        res = st.session_state.result
        pct = res["percentage"]

        if pct >= 85:
            label, cls = "Lecture Ready", "badge-green"
        elif pct >= 60:
            label, cls = "Almost Ready", "badge-yellow"
        else:
            label, cls = "Needs Review", "badge-red"

        st.markdown(f"<div class='{cls}'>{label}: {pct:.0f}%</div>", unsafe_allow_html=True)
        st.write("")

        st.markdown("### Mistake Clinic")
        if persona == "Roast Mode" and pct < 85:
            st.warning("Not bad, but your notebook is still asking for backup. Fix the weak parts before class.")
        elif pct >= 85:
            st.success("Strong work. You are ready to participate in class.")
        else:
            st.info("Good start. Review the weak skills and you will improve.")

        for i, row in enumerate(res["rows"], 1):
            q = row["q"]
            with st.expander(f"Question {i}: {'Correct' if row['ok'] else 'Review needed'}", expanded=not row["ok"]):
                st.write("Your answer:", row["answer"])
                st.write("Correct answer:", q["answer"])
                if not row["ok"]:
                    st.error(f"Why your answer was wrong: it does not match the tested skill, which is {q['skill']}.")
                st.success("Why the correct answer is right: " + q["why"])
                st.info("Explain like I am 5: " + q["kid"])
                st.caption("Evidence: " + q["evidence"])

        st.markdown("### Ask Me Tutor")
        style = st.selectbox("Explanation style", ["Kid-simple", "Exam-focused", "Real-world", "Normal"])
        suggested = st.radio(
            "Quick help prompts",
            ["I do not understand the main idea", "Give me an example", "What mistake do students make?", "How can this come in exam?", "Why should I care?", "Write my own question"],
            horizontal=True
        )
        if suggested == "Write my own question":
            ask = st.text_input("Your question", "I do not understand superposition")
        else:
            ask = suggested
        if st.button("Explain Clearly"):
            st.info(tutor(pack, ask, style))

        st.markdown("### Concept Map")
        graph = "digraph { rankdir=LR; node [shape=box, style=rounded]; "
        for concept in pack["concepts"][:6]:
            graph += f'"{pack["title"]}" -> "{concept}";'
        graph += f'"{pack["title"]}" -> "Quiz"; "Quiz" -> "Mistake Clinic"; "Mistake Clinic" -> "Lecture Readiness";'
        graph += "}"
        st.graphviz_chart(graph)

        st.markdown("### Five smart questions to ask in class")
        questions_to_ask = [
            f"What is the simplest explanation of {pack['title']}?",
            f"Which concept is most important in {pack['title']}?",
            f"What is one common misconception about {pack['title']}?",
            f"How is {pack['title']} used in real life?",
            f"What type of exam question can come from {pack['title']}?"
        ]
        for i, q in enumerate(questions_to_ask, 1):
            st.write(f"{i}. {q}")

        st.markdown("### Readiness Dashboard")
        d1, d2 = st.columns(2)
        mastery = {"Definition": 35, "Concept": 35, "Application": 35, "Misconception": 35, "Confidence": int(pct)}
        for row in res["rows"]:
            if row["ok"]:
                mastery[row["q"]["skill"]] = 90
        d1.plotly_chart(radar_fig(mastery), use_container_width=True)

        rival = random.randint(70, 96)
        fig = go.Figure()
        fig.add_bar(x=["You", "Rival"], y=[pct, rival])
        fig.update_layout(yaxis_range=[0, 100], height=330, margin=dict(l=20, r=20, t=30, b=20))
        d2.plotly_chart(fig, use_container_width=True)

        export = {
            "student": student,
            "topic": pack["title"],
            "lecture_time": lecture_time,
            "score": res["score"],
            "total": res["total"],
            "weak": res["weak"],
            "questions_to_ask": questions_to_ask
        }
        st.download_button("Download JSON Brief", json.dumps(export, indent=2), "preluma_study_brief.json", "application/json", use_container_width=True)
        st.download_button("Download Study Brief", study_brief_markdown(student, lecture_time, pack, res, questions_to_ask), "preluma_study_brief.md", "text/markdown", use_container_width=True)

elif page == "Teacher Studio":
    st.markdown("## Teacher Studio")
    st.caption("A teacher can see class readiness before entering the room.")
    df = demo_teacher_data()
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Students", len(df))
    k2.metric("Average readiness", f"{df['Readiness'].mean():.1f}%")
    k3.metric("Needs review", int((df["Readiness"] < 60).sum()))
    k4.metric("Topics", df["Topic"].nunique())
    st.dataframe(df, use_container_width=True)

    c1, c2 = st.columns(2)
    c1.plotly_chart(px.bar(df, x="Student", y="Readiness", color="Topic", title="Readiness by Student"), use_container_width=True)
    weak = df[df["Weak Skill"] != "None"]["Weak Skill"].value_counts().reset_index()
    weak.columns = ["Weak Skill", "Count"]
    c2.plotly_chart(px.bar(weak, x="Weak Skill", y="Count", title="Most common weak areas"), use_container_width=True)
    st.download_button("Download Teacher CSV", df.to_csv(index=False), "teacher_readiness.csv", "text/csv", use_container_width=True)

else:
    st.markdown("## Evidence Board")
    st.markdown("""
    ### Problem

    Students often enter lectures without preparation. This creates passive learning, weak retention, and low class participation.

    ### Objective

    Preluma prepares students before class with a guided learning mission.

    ### M1: Brain and Data

    - Curated lesson packs
    - Core concept extraction
    - Misconception awareness
    - Application-based learning

    ### M2: Learning Features

    - Brain Brief
    - Pre-class Quiz
    - Mistake Clinic
    - Explain-like-I-am-5 support
    - Ask Me Tutor
    - Smart class questions

    ### M3: UI and Analytics

    - Product-style web interface
    - Readiness dashboard
    - Teacher Studio
    - Exportable study brief

    ### Limitations

    - Current version uses curated and rule-based data.
    - Future versions can add LLM-based generation and syllabus upload.

    ### Future Work

    - Student login
    - Syllabus upload
    - More topics
    - Multilingual explanations
    - Teacher assignment dashboard
    """)
