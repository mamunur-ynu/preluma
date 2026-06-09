import json
import random
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from engine import build_pack, make_questions, grade, tutor, study_brief_markdown, concept_names, application_names
from teacher import demo_teacher_data

APP_VERSION = "11.0"

st.set_page_config(page_title="Preluma", page_icon="●", layout="wide")

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');
html, body, [class*="css"] {font-family: 'Inter', sans-serif;}
.block-container {padding-top: .55rem; max-width: 1150px;}
[data-testid="stSidebar"] {background: #070b18;}
[data-testid="stSidebar"] * {color: #e5e7eb;}
[data-testid="stHeader"] {background: rgba(0,0,0,0);}
.hero {
    padding: 22px 30px;
    border-radius: 28px;
    background:
        radial-gradient(circle at 10% 0%, rgba(14,165,233,.34), transparent 31%),
        radial-gradient(circle at 96% 100%, rgba(124,58,237,.34), transparent 36%),
        linear-gradient(135deg, #050816 0%, #111827 58%, #2e1065 100%);
    border: 1px solid rgba(255,255,255,.12);
    color: white;
    box-shadow: 0 22px 70px rgba(0,0,0,.30);
}
.brand-row {display:flex; align-items:center; gap:12px; margin-bottom:12px;}
.logo-dot {width:34px; height:34px; border-radius:12px; background:linear-gradient(135deg,#38bdf8,#8b5cf6); box-shadow:0 0 28px rgba(56,189,248,.35);}
.brand-name {font-size:18px; font-weight:900; letter-spacing:-.3px;}
.hero h1 {font-size: 34px; line-height: 1.08; margin: 0 0 10px 0; letter-spacing: -1px;}
.hero p {font-size: 15px; max-width: 790px; color: #dbeafe; line-height: 1.55;}
.hero-tag {
    display: inline-block; padding: 6px 12px; border-radius: 999px;
    background: rgba(56,189,248,.16); border: 1px solid rgba(56,189,248,.34);
    color: #bae6fd; font-weight: 800; margin-bottom: 8px; font-size: 13px;
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
.mini-card {
    padding: 14px 16px; border-radius: 18px; background: rgba(248,250,252,.96);
    border: 1px solid #e5e7eb; min-height: 100px;
}
.mini-title {color:#64748b; font-size:12px; font-weight:900; text-transform:uppercase; letter-spacing:.08em;}
.big-label {font-size: 17px; font-weight: 900; color: #0f172a; margin-top: 6px;}
.badge-green {padding:12px 15px; border-radius:15px; background:#dcfce7; color:#166534; font-weight:900;}
.badge-yellow {padding:12px 15px; border-radius:15px; background:#fef3c7; color:#92400e; font-weight:900;}
.badge-red {padding:12px 15px; border-radius:15px; background:#fee2e2; color:#991b1b; font-weight:900;}
.footer-note {color:#94a3b8; font-size:13px;}
.caption-soft {color:#94a3b8; font-size:13px;}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

if "pack" not in st.session_state:
    st.session_state.pack = None
if "questions" not in st.session_state:
    st.session_state.questions = None
if "result" not in st.session_state:
    st.session_state.result = None
if "latest_session" not in st.session_state:
    st.session_state.latest_session = None

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
    fig.add_trace(go.Scatterpolar(r=vals, theta=labels, fill="toself", name="Readiness"))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=False, height=325, margin=dict(l=20, r=20, t=30, b=20))
    return fig

st.sidebar.markdown("## Preluma")
st.sidebar.caption("Light Up Before Class")
page = st.sidebar.radio("Workspace", ["Student Mission", "Teacher Studio", "Evidence Board", "Demo Guide"])
presentation_mode = st.sidebar.toggle("Presentation Mode", True)
st.sidebar.caption("Stable concept-level lesson packs for smooth live demo.")
st.sidebar.markdown("---")
if st.sidebar.button("Reset session"):
    reset()
st.sidebar.markdown(f"<span class='footer-note'>Version {APP_VERSION}</span>", unsafe_allow_html=True)

if page == "Student Mission":
    st.markdown("""
    <div class="hero">
        <div class="brand-row">
            <div class="logo-dot"></div>
            <div>
                <div class="brand-name">Preluma</div>
                <div class="caption-soft">Light Up Before Class</div>
            </div>
        </div>
        <div class="hero-tag">Pre-class brain priming</div>
        <h1>Prepare before class. Understand more during class.</h1>
        <p>A concept-level study mission that gives students a Brain Brief, short quiz, Mistake Clinic, tutor help, and smart class questions before the lecture starts.</p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")
    st.markdown(" ".join([f"<span class='step'>{s}</span>" for s in ["Topic", "Brain Brief", "Quiz", "Mistake Clinic", "Tutor", "Class Questions", "Dashboard"]]), unsafe_allow_html=True)

    st.write("")
    cA, cB, cC = st.columns(3)
    cA.markdown("<div class='mini-card'><div class='mini-title'>Step 1</div><div class='big-label'>Prime the brain</div><br>Start with a compact Brain Brief before the lecture.</div>", unsafe_allow_html=True)
    cB.markdown("<div class='mini-card'><div class='mini-title'>Step 2</div><div class='big-label'>Find weak spots</div><br>Use a short quiz to detect misunderstanding.</div>", unsafe_allow_html=True)
    cC.markdown("<div class='mini-card'><div class='mini-title'>Step 3</div><div class='big-label'>Ask better questions</div><br>Leave with class-ready questions and a score.</div>", unsafe_allow_html=True)

    st.write("")
    with st.container(border=True):
        st.markdown("### Mission Control")
        left, mid, right = st.columns([1.1, 1, 1])
        with left:
            student = st.text_input("Student", "Mim")
            topic_options = ["Quantum Mechanics", "Machine Learning", "Python Programming", "Data Structures", "Artificial Intelligence", "Object Oriented Programming", "Neural Networks", "Linear Regression", "Database Systems", "Climate Change", "Custom topic"]
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
        c3.metric("Concepts", len(concept_names(pack)))
        c4.metric("Applications", len(application_names(pack)))
        st.caption(f"Source: {pack['source']}")

        a, b = st.columns([1.1, 0.9])
        with a:
            st.markdown(f"<div class='card'><div class='mini-title'>Definition</div><br>{pack['definition']}</div>", unsafe_allow_html=True)
            st.write("")
            st.info(pack["simple"])
        with b:
            st.markdown(f"<div class='dark-card'><div class='mini-title'>Why this matters</div><br>{pack['hook']}</div>", unsafe_allow_html=True)

        t1, t2, t3, t4, t5 = st.tabs(["Concept Cards", "Misconceptions", "Applications", "Facts", "Keywords"])
        for name, details in pack["concepts"].items():
            with t1.expander(name.title()):
                st.write(details["definition"])
                st.info("Simple: " + details["kid"])
                st.success("Example: " + details["example"])
                st.warning("Common mistake: " + details["mistake"])
                st.caption("Exam angle: " + details["exam"])
        for m in pack["misconceptions"]:
            t2.warning(m)
        for name, text in pack["applications"].items():
            t3.success(f"{name}: {text}")
        for fact in pack["facts"]:
            t4.info(fact)
        t5.write(", ".join(pack["keywords"]))

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
                st.session_state.latest_session = {
                    "Student": student,
                    "Topic": pack["title"],
                    "Readiness": st.session_state.result["percentage"],
                    "Weak Skill": ", ".join(st.session_state.result["weak"]) if st.session_state.result["weak"] else "None",
                }

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
        prompt_options = [
            f"I do not understand {concept_names(pack)[0]}",
            "Give me an example",
            "What mistake do students make?",
            "How can this come in exam?",
            "Why should I care?",
            "Write my own question",
        ]
        suggested = st.radio("Quick help prompts", prompt_options, horizontal=True)
        if suggested == "Write my own question":
            ask = st.text_input("Your question", f"I do not understand {concept_names(pack)[0]}")
        else:
            ask = suggested
        if st.button("Explain Clearly"):
            st.info(tutor(pack, ask, style))

        st.markdown("### Concept Map")
        graph = "digraph { rankdir=LR; node [shape=box, style=rounded]; "
        for concept in concept_names(pack)[:6]:
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
    if st.session_state.latest_session:
        df = pd.concat([pd.DataFrame([st.session_state.latest_session]), df], ignore_index=True)

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

elif page == "Evidence Board":
    st.markdown("## Evidence Board")
    st.markdown("""
    ### Problem

    Students often enter lectures without preparation. This creates passive learning, weak retention, and low class participation.

    ### Objective

    Preluma prepares students before class with a guided learning mission.

    ### M1: Brain and Data

    - Curated concept-level lesson packs
    - Concept cards with definition, example, mistake, and exam angle
    - Application-based learning
    - Evidence-based quiz feedback

    ### M2: Learning Features

    - Brain Brief
    - Pre-class Quiz
    - Mistake Clinic
    - Explain-like-I-am-5 support
    - Topic-aware Ask Me Tutor
    - Smart class questions

    ### M3: UI and Analytics

    - Product-style web interface
    - Readiness dashboard
    - Teacher Studio
    - Exportable study brief

    ### Evaluation

    - Readiness score
    - Weak skill detection
    - Teacher analytics
    - Exported study brief

    ### Limitations

    - Current version uses curated and rule-based data.
    - Future versions can add LLM-based generation and syllabus upload.
    """)

else:
    st.markdown("## Demo Guide")
    st.markdown("""
    ### Two-minute presentation flow

    1. Open Preluma and explain the problem: students attend class unprepared.
    2. Select `Quantum Mechanics`.
    3. Choose `Roast Mode`.
    4. Start the mission and show the Brain Brief.
    5. Answer one quiz question incorrectly.
    6. Show Mistake Clinic and kid-simple explanation.
    7. Ask the tutor: `I do not understand superposition`.
    8. Show class questions.
    9. Open Teacher Studio and show readiness analytics.

    ### Best final sentence

    Preluma does not only quiz students. It shows what they know, what they misunderstood, and what they should ask in class.
    """)
