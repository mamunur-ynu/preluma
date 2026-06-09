import json
import random
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from smartprep import APP_VERSION
from smartprep.engine import build_pack, make_questions, grade, tutor
from smartprep.teacher import demo_teacher_data

st.set_page_config(page_title="SmartPrep Studio", layout="wide")

CSS = """
<style>
.block-container {padding-top: 1rem; max-width: 1180px;}
[data-testid="stSidebar"] {background: #0b1020;}
[data-testid="stSidebar"] * {color: #e5e7eb;}
.hero {padding: 28px 34px; border-radius: 28px; background: radial-gradient(circle at top left, rgba(59,130,246,.35), transparent 32%), radial-gradient(circle at bottom right, rgba(168,85,247,.32), transparent 35%), linear-gradient(135deg, #070b16 0%, #111827 55%, #25124d 100%); border: 1px solid rgba(255,255,255,.12); color: white; box-shadow: 0 24px 90px rgba(0,0,0,.32);}
.hero h1 {font-size: 42px; line-height: 1.08; margin: 0 0 12px 0; letter-spacing: -1px;}
.hero p {font-size: 16px; max-width: 780px; color: #dbeafe;}
.hero-tag {display: inline-block; padding: 7px 12px; border-radius: 999px; background: rgba(56,189,248,.16); border: 1px solid rgba(56,189,248,.3); color: #bae6fd; font-weight: 700; margin-bottom: 12px;}
.card {padding: 18px; border-radius: 20px; background: #ffffff; border: 1px solid #e5e7eb; box-shadow: 0 10px 28px rgba(15,23,42,.05);}
.dark-card {padding: 18px; border-radius: 20px; background: #0f172a; color: #e5e7eb; border: 1px solid rgba(255,255,255,.10);}
.step {display:inline-block; padding:7px 11px; margin:3px; border-radius:999px; background:#eef2ff; color:#3730a3; font-weight:800; font-size:13px;}
.badge-green {padding:10px 14px; border-radius:14px; background:#dcfce7; color:#166534; font-weight:900;}
.badge-yellow {padding:10px 14px; border-radius:14px; background:#fef3c7; color:#92400e; font-weight:900;}
.badge-red {padding:10px 14px; border-radius:14px; background:#fee2e2; color:#991b1b; font-weight:900;}
.kicker {color:#64748b; font-size:13px; font-weight:800; text-transform:uppercase; letter-spacing:.08em;}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

if "pack" not in st.session_state:
    st.session_state.pack = None
if "questions" not in st.session_state:
    st.session_state.questions = None
if "result" not in st.session_state:
    st.session_state.result = None

st.sidebar.markdown("## SmartPrep Studio")
st.sidebar.caption(f"Version {APP_VERSION}")
page = st.sidebar.radio("Workspace", ["Student Mission", "Teacher Studio", "Evidence Board"])
st.sidebar.toggle("Demo-safe mode", True)
st.sidebar.caption("Use demo-safe mode during presentation for stable performance.")
st.sidebar.markdown("---")
if st.sidebar.button("Reset session"):
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
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0,100])), showlegend=False, height=340, margin=dict(l=20,r=20,t=30,b=20))
    return fig

if page == "Student Mission":
    st.markdown('<div class="hero"><div class="hero-tag">Pre-class brain priming system</div><h1>Prepare before class. Understand more during class.</h1><p>SmartPrep gives students a Brain Brief, short quiz, mistake explanation, Ask Me Tutor, and class questions before the lecture starts.</p></div>', unsafe_allow_html=True)
    st.write("")
    st.markdown(" ".join([f"<span class='step'>{s}</span>" for s in ["Topic", "Brain Brief", "Quiz", "Mistake Learning", "Tutor", "Class Questions", "Dashboard"]]), unsafe_allow_html=True)
    st.write("")
    with st.container(border=True):
        st.markdown("### Start your pre-class mission")
        left, mid, right = st.columns([1.2, 1, 1])
        with left:
            student = st.text_input("Student", "Mim")
            topic = st.text_input("Lecture topic", "Quantum Mechanics")
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
        c2.metric("Confidence", f"{int(pack['confidence']*100)}%")
        c3.metric("Concepts", len(pack["concepts"]))
        c4.metric("Applications", len(pack["applications"]))
        st.caption(f"Source: {pack['source']}")
        a, b = st.columns([1.1, .9])
        with a:
            st.markdown(f"<div class='card'><div class='kicker'>Definition</div><br>{pack['definition']}</div>", unsafe_allow_html=True)
            st.write("")
            st.info(pack["simple"])
        with b:
            st.markdown(f"<div class='dark-card'><div class='kicker'>Why this matters</div><br>{pack['hook']}</div>", unsafe_allow_html=True)
        t1, t2, t3 = st.tabs(["Core concepts", "Misconceptions", "Applications"])
        t1.write(", ".join(pack["concepts"]))
        for m in pack["misconceptions"]:
            t2.warning(m)
        for app in pack["applications"]:
            t3.success(app)
        st.markdown("### Pre-class Quiz")
        selected = {}
        with st.form("quiz_form"):
            for i, q in enumerate(st.session_state.questions):
                st.markdown(f"**Q{i+1}. {q['q']}**")
                selected[i] = st.radio("Choose", q["options"], index=None, key=f"q_{i}_{pack['title']}", label_visibility="collapsed")
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
        st.markdown("### Mistake Learning")
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
        ask = st.text_input("What did you not understand?", "I do not understand superposition")
        if st.button("Explain Clearly"):
            st.info(tutor(pack, ask, style))
        st.markdown("### Concept Map")
        graph = "digraph { rankdir=LR; node [shape=box, style=rounded]; "
        for concept in pack["concepts"][:6]:
            graph += f'"{pack["title"]}" -> "{concept}";'
        graph += f'"{pack["title"]}" -> "Quiz"; "Quiz" -> "Mistake Learning"; "Mistake Learning" -> "Lecture Readiness";'
        graph += "}"
        st.graphviz_chart(graph)
        st.markdown("### Five smart questions to ask in class")
        questions_to_ask = [f"What is the simplest explanation of {pack['title']}?", f"Which concept is most important in {pack['title']}?", f"What is one common misconception about {pack['title']}?", f"How is {pack['title']} used in real life?", f"What type of exam question can come from {pack['title']}?"]
        for i, q in enumerate(questions_to_ask, 1):
            st.write(f"{i}. {q}")
        st.markdown("### Dashboard")
        d1, d2 = st.columns(2)
        mastery = {"Definition": 35, "Concept": 35, "Application": 35, "Misconception": 35, "Confidence": int(pct)}
        for row in res["rows"]:
            if row["ok"]:
                mastery[row["q"]["skill"]] = 90
        d1.plotly_chart(radar_fig(mastery), use_container_width=True)
        rival = random.randint(70, 96)
        fig = go.Figure()
        fig.add_bar(x=["You", "Rival"], y=[pct, rival])
        fig.update_layout(yaxis_range=[0, 100], height=340)
        d2.plotly_chart(fig, use_container_width=True)
        export = {"student": student, "lecture_time": lecture_time, "mood": mood, "persona": persona, "topic": pack["title"], "score": res["score"], "total": res["total"], "weak": res["weak"], "questions_to_ask": questions_to_ask}
        st.download_button("Download Study Brief", json.dumps(export, indent=2), "smartprep_study_brief.json", "application/json", use_container_width=True)
elif page == "Teacher Studio":
    st.markdown("## Teacher Studio")
    st.caption("A teacher can see whether the class is lecture-ready before entering the room.")
    df = pd.DataFrame(demo_teacher_data())
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
    This version is built to look like a product demo, not just a script.

    **Strong points**
    - Product-style landing page
    - Guided student mission
    - Rich Brain Brief
    - Clean quiz options
    - Wrong-answer explanation
    - Explain Like I am 5 learning
    - Ask Me Tutor
    - Concept map
    - Teacher Studio
    - Exportable study brief
    - Deployment guide included
    - Mac direct launcher included

    **Best demo strategy**
    1. Start with Student Mission.
    2. Use Quantum Mechanics.
    3. Choose Roast Mode.
    4. Give one wrong answer.
    5. Show mistake learning.
    6. Ask the tutor about superposition.
    7. Show Teacher Studio.
    """)
