import base64
import json
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from engine import (
    build_brain_brief,
    build_enriched_class_questions,
    build_pack,
    grade,
    make_questions,
    tutor_sections,
)
from teacher import build_teacher_dataframe, class_average_readiness, readiness_label
from topics import TOPICS, validate_topics

APP_VERSION = "17.0"
APP_NAME    = "Preluma"
TAGLINE     = "Light Up Before Class"

TEAM_MEMBERS = [
    ("MAMUNUR RASHID", "Lead · UI · Integration"),
    ("MD FAHIM",       "Engine · Quiz · Testing"),
    ("MD JIARUL ISLAM","Topics · Data · Docs"),
]

TOPIC_OPTIONS = [
    "Quantum Mechanics",
    "Machine Learning",
    "Python Programming",
    "Data Structures",
    "Artificial Intelligence",
    "Natural Language Processing",
    "Convolutional Neural Network",
    "Statistics",
    "Database Management System",
    "Software Engineering",
    "Cybersecurity",
    "Operating System",
    "Computer Network",
    "Linear Regression",
    "Logistic Regression",
    "Decision Tree",
    "Neural Network",
    "Cloud Computing",
    "Custom Topic",
]


@st.cache_data(show_spinner=False)
def asset_to_data_uri() -> str:
    for path in [Path("assets/ynu_campus.jpg"), Path("ynu_campus.jpg")]:
        if path.exists():
            return "data:image/jpeg;base64," + base64.b64encode(path.read_bytes()).decode("ascii")
    return ""


CAMPUS_BG = asset_to_data_uri()

st.set_page_config(page_title="Preluma", page_icon=None, layout="wide")

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.block-container { padding-top: 1rem; max-width: 1180px; }
[data-testid="stSidebar"] { background: #071021; }
[data-testid="stSidebar"] * { color: #e5e7eb; }

.hero {
    position: relative; padding: 32px 36px; min-height: 260px;
    border-radius: 30px; overflow: hidden;
    border: 1px solid rgba(125,211,252,.22);
    background-size: cover; background-position: center;
    box-shadow: 0 28px 60px rgba(2,6,23,.40);
}
.hero::after {
    content: ""; position: absolute; inset: 0;
    background: linear-gradient(90deg, rgba(2,6,23,.80) 0%, rgba(15,23,42,.54) 48%, rgba(88,28,135,.50) 100%),
                radial-gradient(circle at 20% 10%, rgba(14,165,233,.23), transparent 32%);
    z-index: 1;
}
.hero-content { position: relative; z-index: 2; }
.brand-row { display: flex; align-items: center; gap: 14px; margin-bottom: 16px; }
.logo-mark {
    width: 42px; height: 42px; border-radius: 15px;
    background: linear-gradient(135deg, #38bdf8, #8b5cf6);
    box-shadow: 0 12px 28px rgba(56,189,248,.22);
}
.brand-title { font-weight: 900; color: #fff; font-size: 18px; }
.brand-sub { color: #dbeafe; font-size: 13px; margin-top: 2px; }
.badge {
    display: inline-block; padding: 8px 13px; border-radius: 999px;
    background: rgba(14,165,233,.16); border: 1px solid rgba(125,211,252,.35);
    color: #bae6fd; font-weight: 850; font-size: 13px;
}
.uni-badge {
    display: inline-block; padding: 8px 13px; border-radius: 999px;
    background: rgba(255,255,255,.12); border: 1px solid rgba(255,255,255,.24);
    color: #fff; font-weight: 850; font-size: 12px; margin-left: 8px;
}
.hero h1 {
    font-size: 38px; line-height: 1.08; color: white;
    margin: 28px 0 14px; max-width: 920px;
    text-shadow: 0 4px 22px rgba(0,0,0,.48);
}
.hero p {
    font-size: 16px; max-width: 850px; color: #e0f2fe;
    line-height: 1.6; text-shadow: 0 3px 16px rgba(0,0,0,.40);
}
.chip {
    display: inline-block; padding: 10px 14px; margin: 4px 6px 8px 0;
    border-radius: 999px; background: #eef2ff; color: #3730a3;
    font-weight: 900; font-size: 13px;
}
.team-box {
    padding: 14px 15px; border-radius: 22px;
    background: linear-gradient(135deg, rgba(15,23,42,.88), rgba(30,41,59,.78));
    border: 1px solid rgba(148,163,184,.23); margin-top: 16px;
}
.team-title {
    color: #93c5fd; font-size: 12px; font-weight: 900;
    letter-spacing: .09em; text-transform: uppercase; margin-bottom: 10px;
}
.team-line { padding: 9px 0; border-bottom: 1px solid rgba(148,163,184,.12); }
.team-line:last-child { border-bottom: 0; }
.team-name { font-weight: 900; color: #fff; font-size: 13px; }
.team-role { font-size: 11px; color: #94a3b8; margin-top: 2px; }
.card {
    padding: 18px 20px; border-radius: 22px;
    background: linear-gradient(135deg, rgba(15,23,42,.94), rgba(30,41,59,.82));
    border: 1px solid rgba(125,211,252,.18);
}
.metric-grid { display: grid; grid-template-columns: repeat(4,1fr); gap: 12px; margin: 16px 0; }
.metric-number { font-size: 26px; color: #fff; font-weight: 900; }
.metric-label {
    font-size: 12px; color: #93c5fd; font-weight: 900;
    letter-spacing: .08em; text-transform: uppercase; margin-top: 5px;
}
.flow-grid { display: grid; grid-template-columns: repeat(3,1fr); gap: 16px; margin: 16px 0; }
.flow-card small { color: #93c5fd; font-weight: 900; letter-spacing: .08em; }
.flow-card h3 { color: #fff; margin: 8px 0; font-size: 21px; }
.flow-card p { color: #cbd5e1; line-height: 1.55; }
.answer-card {
    padding: 18px 20px; border-radius: 22px;
    background: rgba(15,23,42,.72);
    border: 1px solid rgba(148,163,184,.20); margin: 12px 0;
}
.answer-title {
    color: #93c5fd; font-size: 13px; font-weight: 900;
    text-transform: uppercase; letter-spacing: .08em; margin-bottom: 8px;
}
.answer-card p, .answer-card li { color: #e5e7eb; font-size: 15px; line-height: 1.6; }
.notice {
    padding: 13px 15px; border-radius: 17px;
    background: rgba(59,130,246,.12); border: 1px solid rgba(96,165,250,.24);
    color: #dbeafe; line-height: 1.55; margin-bottom: 12px;
}
.notice-success {
    padding: 13px 15px; border-radius: 17px;
    background: rgba(16,185,129,.12); border: 1px solid rgba(52,211,153,.24);
    color: #d1fae5; line-height: 1.55; margin-bottom: 12px;
}
.concept-tab {
    padding: 14px 16px; border-radius: 18px; margin: 8px 0;
    background: rgba(15,23,42,.60); border: 1px solid rgba(125,211,252,.15);
}
.concept-tab h5 { color: #93c5fd; margin: 0 0 6px; font-size: 13px; text-transform: uppercase; letter-spacing: .07em; }
.concept-tab p { color: #e5e7eb; font-size: 14px; line-height: 1.55; margin: 4px 0; }
.prof-grid { display: grid; grid-template-columns: repeat(3,1fr); gap: 14px; margin: 16px 0; }
.prof-card {
    padding: 17px; border-radius: 21px;
    background: linear-gradient(135deg, rgba(14,165,233,.13), rgba(124,58,237,.11));
    border: 1px solid rgba(125,211,252,.22);
}
.prof-card h4 { margin: 0 0 8px; color: #fff; font-size: 17px; }
.prof-card p { color: #cbd5e1; font-size: 14px; line-height: 1.55; }
.provider-badge {
    display: inline-block; padding: 4px 10px; border-radius: 999px;
    background: rgba(16,185,129,.15); border: 1px solid rgba(52,211,153,.30);
    color: #6ee7b7; font-size: 12px; font-weight: 700; margin-left: 8px;
}

.stButton > button {
    border-radius: 14px !important; font-weight: 900 !important;
    min-height: 48px !important;
    border: 1px solid rgba(125,211,252,.35) !important;
    background: linear-gradient(135deg, rgba(37,99,235,.95), rgba(124,58,237,.92)) !important;
    color: white !important;
}
@media(max-width: 900px) {
    .metric-grid, .flow-grid, .prof-grid { grid-template-columns: 1fr; }
    .hero { padding: 24px 22px; }
    .hero h1 { font-size: 30px; }
}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)


# ── Session helpers ───────────────────────────────────────────────────────────

def reset():
    for key in ["pack", "brief", "questions", "quiz_result", "latest_session",
                "student", "topic", "persona", "tutor_history", "score_history",
                "class_questions"]:
        st.session_state.pop(key, None)


def init_state():
    st.session_state.setdefault("student",       "Student")
    st.session_state.setdefault("topic",         "Quantum Mechanics")
    st.session_state.setdefault("persona",       "Normal Mode")
    st.session_state.setdefault("tutor_history", [])
    st.session_state.setdefault("score_history", [])


def _provider_badge() -> str:
    try:
        from llm import active_provider
        p = active_provider()
        return f"<span class='provider-badge'>{p}</span>" if p != "none" else ""
    except ImportError:
        return ""


# ── Sidebar ───────────────────────────────────────────────────────────────────

def sidebar():
    st.sidebar.markdown(f"## {APP_NAME}")
    st.sidebar.caption(TAGLINE)
    page = st.sidebar.radio(
        "Workspace",
        ["Student Mission", "Teacher Studio", "Evidence Board", "Demo Guide", "Future Roadmap"],
    )
    presentation = st.sidebar.toggle("Presentation Mode", value=True)
    st.sidebar.caption("Python + Streamlit + Wikipedia + LLM real data upgrade.")

    st.sidebar.markdown("<div class='team-box'><div class='team-title'>Project Team</div>", unsafe_allow_html=True)
    for name, role in TEAM_MEMBERS:
        st.sidebar.markdown(
            f"<div class='team-line'><div class='team-name'>{name}</div>"
            f"<div class='team-role'>{role}</div></div>",
            unsafe_allow_html=True,
        )
    st.sidebar.markdown("</div><hr>", unsafe_allow_html=True)

    if st.sidebar.button("Reset session"):
        reset()
        st.rerun()
    st.sidebar.caption(f"Version {APP_VERSION}")
    return page, presentation


# ── Hero ──────────────────────────────────────────────────────────────────────

def hero():
    bg = (
        f"linear-gradient(90deg,rgba(2,6,23,.80) 0%,rgba(15,23,42,.54) 48%,rgba(88,28,135,.50) 100%),"
        f"url('{CAMPUS_BG}')"
        if CAMPUS_BG
        else "linear-gradient(135deg,#020617 0%,#111827 48%,#4c1d95 100%)"
    )
    st.markdown(
        f"""<div class='hero' style="background-image:{bg};">
          <div class='hero-content'>
            <div class='brand-row'>
              <div class='logo-mark'></div>
              <div><div class='brand-title'>Preluma</div><div class='brand-sub'>Light Up Before Class</div></div>
              <span class='uni-badge'>Yunnan University</span>
            </div>
            <span class='badge'>Pre-class brain priming</span>
            <h1>Prepare before class. Understand more during class.</h1>
            <p>Built with a Yunnan University learning context. Preluma turns passive pre-class
            preparation into a short, guided, and interactive learning mission.</p>
          </div>
        </div>""",
        unsafe_allow_html=True,
    )
    if not CAMPUS_BG:
        st.info("Campus image missing. Add assets/ynu_campus.jpg for the branded hero background.")


def chips():
    labels = ["Topic", "Brain Brief", "Quiz", "Mistake Clinic", "Tutor", "Class Questions", "Dashboard"]
    st.markdown(" ".join(f"<span class='chip'>{c}</span>" for c in labels), unsafe_allow_html=True)


def metrics_steps():
    st.markdown(
        """<div class='metric-grid'>
          <div class='card'><div class='metric-number'>4</div><div class='metric-label'>Quiz Checks</div></div>
          <div class='card'><div class='metric-number'>5</div><div class='metric-label'>Class Questions</div></div>
          <div class='card'><div class='metric-number'>1</div><div class='metric-label'>Mistake Clinic</div></div>
          <div class='card'><div class='metric-number'>0–100</div><div class='metric-label'>Readiness Score</div></div>
        </div>
        <div class='flow-grid'>
          <div class='card flow-card'><small>STEP 1</small><h3>Prime the brain</h3>
            <p>Start with a compact Brain Brief before the lecture.</p></div>
          <div class='card flow-card'><small>STEP 2</small><h3>Find weak spots</h3>
            <p>Use a short quiz to detect misunderstanding.</p></div>
          <div class='card flow-card'><small>STEP 3</small><h3>Ask better questions</h3>
            <p>Leave with class-ready questions and a readiness score.</p></div>
        </div>""",
        unsafe_allow_html=True,
    )


# ── Mission Control ───────────────────────────────────────────────────────────

def mission_control():
    st.markdown("### Mission Control")
    st.markdown(
        "<div class='notice'>Choose a topic. Preluma generates a pre-class learning mission "
        "from curated topic data, Wikipedia, and LLM-powered explanations.</div>",
        unsafe_allow_html=True,
    )
    with st.form("mission_form", border=True):
        c1, c2, c3 = st.columns([1.25, 1, 1])
        with c1:
            student = st.text_input("Student name", value=st.session_state.student)
            topic_choice = st.selectbox(
                "Lecture topic", TOPIC_OPTIONS,
                index=TOPIC_OPTIONS.index(st.session_state.topic)
                if st.session_state.topic in TOPIC_OPTIONS else 0,
            )
            topic = (
                st.text_input("Enter your topic", placeholder="e.g. Reinforcement Learning")
                if topic_choice == "Custom Topic"
                else topic_choice
            )
            st.text_input("Lecture time", value="Tomorrow 9 AM")
        with c2:
            persona = st.radio(
                "Feedback style",
                ["Normal Mode", "Coach Mode", "Roast Mode"],
                captions=["Direct", "Supportive", "Funny pressure"],
            )
        with c3:
            st.markdown("**Output includes**")
            for item in ["Tiny answer", "All concepts explained",
                         "Real example", "Mistake correction",
                         "LLM-generated class questions"]:
                st.caption(item)
        start = st.form_submit_button("Start Pre-Class Mission", use_container_width=True)

    if start:
        if not topic or not topic.strip():
            st.warning("Please enter a topic before starting.")
            return
        with st.spinner("Building your learning mission..."):
            pack = build_pack(topic)
            brief = build_brain_brief(pack)
            questions = make_questions(pack)
            class_qs = build_enriched_class_questions(pack)
        st.session_state.student        = student
        st.session_state.topic          = topic
        st.session_state.persona        = persona
        st.session_state.pack           = pack
        st.session_state.brief          = brief
        st.session_state.questions      = questions
        st.session_state.class_questions = class_qs
        st.session_state.quiz_result    = None
        st.session_state.latest_session = None
        st.session_state.tutor_history  = []
        st.rerun()


# ── Brain Brief ───────────────────────────────────────────────────────────────

def brain_brief():
    if "brief" not in st.session_state:
        return
    b = st.session_state.brief
    st.markdown("### Brain Brief")

    # Study tip if available (LLM-generated)
    if b.get("study_tip"):
        st.markdown(
            f"<div class='notice-success'>Before class: {b['study_tip']}</div>",
            unsafe_allow_html=True,
        )

    st.markdown(
        f"""<div class='answer-card'><div class='answer-title'>Tiny answer</div><p>{b['tiny_answer']}</p></div>
        <div class='answer-card'><div class='answer-title'>Explain simply</div><p>{b['simple']}</p></div>
        <div class='answer-card'><div class='answer-title'>Real-life example</div><p>{b['example']}</p></div>
        <div class='answer-card'><div class='answer-title'>Common mistake</div><p>{b['misconception']}</p></div>""",
        unsafe_allow_html=True,
    )

    # Show ALL concepts, not just the first
    all_concepts = b.get("all_concepts", {})
    if all_concepts:
        st.markdown("#### All Key Concepts")
        tabs = st.tabs([name.title() for name in all_concepts])
        for tab, (cname, c) in zip(tabs, all_concepts.items()):
            with tab:
                st.markdown(
                    f"<div class='concept-tab'>"
                    f"<h5>Definition</h5><p>{c['definition']}</p>"
                    f"<h5>In simple words</h5><p>{c['kid']}</p>"
                    f"<h5>Example</h5><p>{c['example']}</p>"
                    f"<h5>Common mistake</h5><p>{c['mistake']}</p>"
                    f"<h5>For exam or viva</h5><p>{c['exam']}</p>"
                    f"</div>",
                    unsafe_allow_html=True,
                )

    with st.expander("Important facts"):
        for fact in b["facts"]:
            st.write(f"- {fact}")


# ── Quiz ──────────────────────────────────────────────────────────────────────

def quiz():
    if "questions" not in st.session_state:
        return
    st.markdown("### Quick Quiz")
    st.caption("Answer once. Preluma will detect weak skills and explain every mistake.")

    with st.form("quiz_form", border=True):
        answers = {}
        for i, q in enumerate(st.session_state.questions):
            answers[i] = st.radio(q["q"], q["options"], key=f"quiz_{i}")
        submit = st.form_submit_button("Check Readiness", use_container_width=True)

    if submit:
        result = grade(st.session_state.questions, answers)
        st.session_state.quiz_result = result
        session = {
            "Student":    st.session_state.student,
            "Topic":      st.session_state.pack["title"],
            "Readiness":  result["pct"],
            "Weak Skill": result["weakest"],
        }
        st.session_state.latest_session = session
        # Track score history for trend chart
        st.session_state.score_history.append({
            "Attempt": len(st.session_state.score_history) + 1,
            "Topic":   st.session_state.pack["title"],
            "Score":   result["pct"],
        })
        st.rerun()


# ── Result + Mistake Clinic ───────────────────────────────────────────────────

def result_section():
    result = st.session_state.get("quiz_result")
    if not result:
        return

    st.markdown("### Readiness Result")
    st.success(f"{readiness_label(result['pct'])}: {result['score']}/{result['total']} ({result['pct']}%)")

    st.markdown("### Mistake Clinic")
    for i, d in enumerate(result["details"], 1):
        status = "Correct" if d["correct"] else "Review needed"
        with st.expander(f"Question {i}: {status} — {d['skill']}"):
            st.write(f"Your answer: {d['chosen']}")
            st.write(f"Correct answer: {d['answer']}")
            st.write(f"Why: {d['why']}")
            if not d["correct"]:
                st.info("Quick fix: read the definition, find one real example, then say it in your own words.")

    # Readiness comparison chart
    df  = build_teacher_dataframe(st.session_state.latest_session)
    avg = class_average_readiness(df)
    fig = go.Figure()
    fig.add_bar(x=["You", "Class Average"], y=[result["pct"], avg],
                marker_color=["#38bdf8", "#8b5cf6"])
    fig.update_layout(title="Readiness Comparison", yaxis_range=[0, 100],
                      height=320, margin=dict(l=20, r=20, t=45, b=20))
    st.plotly_chart(fig, use_container_width=True)

    # Score trend chart (shown after 2+ attempts)
    history = st.session_state.get("score_history", [])
    if len(history) >= 2:
        df_hist = pd.DataFrame(history)
        fig2 = px.line(df_hist, x="Attempt", y="Score", markers=True,
                       title="Your Readiness Trend", range_y=[0, 100])
        fig2.update_layout(height=280, margin=dict(l=20, r=20, t=45, b=20))
        st.plotly_chart(fig2, use_container_width=True)


# ── UltraTutor ────────────────────────────────────────────────────────────────

def tutor():
    if "pack" not in st.session_state:
        return
    st.markdown("### UltraTutor")

    try:
        from llm import active_provider
        provider = active_provider()
        if provider != "none":
            st.markdown(
                f"<div class='notice-success'>AI active: <strong>{provider}</strong> — "
                "ask any question and get a real intelligent answer.</div>",
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                "<div class='notice'>Running on local concept data. "
                "Set ANTHROPIC_API_KEY, GROQ_API_KEY, or GEMINI_API_KEY to enable AI answers.</div>",
                unsafe_allow_html=True,
            )
    except ImportError:
        pass

    q = st.text_input(
        "What did you not understand?",
        placeholder="e.g. What is superposition? How does overfitting happen?",
        key="tutor_input",
    )

    if st.button("Explain Clearly", use_container_width=True):
        if not q.strip():
            st.warning("Please type a question first.")
            return
        with st.spinner("Thinking..."):
            s = tutor_sections(st.session_state.pack, q, st.session_state.persona)
        # Save to history
        st.session_state.tutor_history.append({"question": q, "response": s})

    # Show tutor history (most recent first)
    history = st.session_state.get("tutor_history", [])
    for entry in reversed(history):
        s = entry["response"]
        st.markdown(f"#### {s.get('concept', st.session_state.pack['title'])}")
        st.caption(f"Question: {entry['question']}")
        parts = [
            ("Tiny answer",        s.get("tiny_answer",       "")),
            ("Explain simply",     s.get("explain_simply",    "")),
            ("Real-life example",  s.get("real_life_example", "")),
            ("Common mistake",     s.get("common_mistake",    "")),
            ("Exam angle",         s.get("exam_angle",        "")),
        ]
        html = "".join(
            f"<div class='answer-card'><div class='answer-title'>{title}</div><p>{text}</p></div>"
            for title, text in parts if text
        )
        st.markdown(html, unsafe_allow_html=True)
        st.markdown("---")


# ── Class Questions + Download ────────────────────────────────────────────────

def questions_download():
    if "pack" not in st.session_state:
        return
    st.markdown("### Smart Class Questions")
    class_qs = st.session_state.get("class_questions", st.session_state.pack["class_questions"])
    for i, q in enumerate(class_qs, 1):
        st.write(f"{i}. {q}")

    payload = {
        "student":         st.session_state.student,
        "topic":           st.session_state.pack["title"],
        "brief":           st.session_state.brief,
        "class_questions": class_qs,
        "quiz_result":     st.session_state.get("quiz_result"),
        "tutor_history":   [
            {"question": e["question"], "concept": e["response"].get("concept", "")}
            for e in st.session_state.get("tutor_history", [])
        ],
    }
    st.download_button(
        "Download Study Brief (JSON)",
        data=json.dumps(payload, indent=2),
        file_name=f"preluma_{st.session_state.pack['title'].lower().replace(' ','_')}_brief.json",
        mime="application/json",
        use_container_width=True,
    )


# ── Student Mission page ──────────────────────────────────────────────────────

def student_mission(presentation: bool):
    hero()
    chips()
    mission_control()
    if not presentation:
        metrics_steps()
    brain_brief()
    quiz()
    result_section()
    tutor()
    questions_download()
    if presentation:
        metrics_steps()


# ── Teacher Studio ────────────────────────────────────────────────────────────

def teacher_studio():
    hero()
    st.markdown("### Teacher Studio")
    st.markdown(
        "<div class='notice'>Teacher Studio shows how teachers can monitor readiness, "
        "weak skills, and topic preparation before class.</div>",
        unsafe_allow_html=True,
    )
    df = build_teacher_dataframe(st.session_state.get("latest_session"))

    # Filter by topic if a topic is selected
    current_topic = st.session_state.get("topic", "")
    topics_in_df  = ["All topics"] + sorted(df["Topic"].unique().tolist())
    selected_topic = st.selectbox("Filter by topic", topics_in_df,
                                  index=topics_in_df.index(current_topic)
                                  if current_topic in topics_in_df else 0)
    df_view = df if selected_topic == "All topics" else df[df["Topic"] == selected_topic]

    c1, c2 = st.columns([1.1, 1])
    with c1:
        st.dataframe(df_view, use_container_width=True)
    with c2:
        fig = px.bar(df_view, x="Student", y="Readiness", color="Weak Skill",
                     title=f"Class Readiness — {selected_topic}")
        fig.update_layout(yaxis_range=[0, 100], height=360)
        st.plotly_chart(fig, use_container_width=True)

    col1, col2, col3 = st.columns(3)
    col1.metric("Class Average", f"{class_average_readiness(df_view)}%")
    col2.metric("Students", len(df_view))
    ready = len(df_view[df_view["Readiness"] >= 65])
    col3.metric("Ready for lecture", f"{ready}/{len(df_view)}")

    # Skill gap summary
    if "Weak Skill" in df_view.columns:
        skill_counts = df_view[df_view["Weak Skill"] != "None"]["Weak Skill"].value_counts()
        if not skill_counts.empty:
            st.markdown("#### Skill Gap Summary")
            fig2 = px.pie(values=skill_counts.values, names=skill_counts.index,
                          title="Where students struggle most")
            fig2.update_layout(height=300)
            st.plotly_chart(fig2, use_container_width=True)


# ── Evidence Board ────────────────────────────────────────────────────────────

def evidence_board():
    hero()
    st.markdown("### Evidence Board")
    st.markdown(
        """<div class='prof-grid'>
          <div class='prof-card'><h4>Clear Problem</h4>
            <p>Students often enter lectures unprepared, leading to passive learning and poor retention.</p></div>
          <div class='prof-card'><h4>Python Implementation</h4>
            <p>Built with Python, Streamlit, Pandas, Plotly, dictionaries, functions, forms, and session state.</p></div>
          <div class='prof-card'><h4>Learning Workflow</h4>
            <p>Brain Brief, quiz, Mistake Clinic, UltraTutor, class questions, and readiness score.</p></div>
          <div class='prof-card'><h4>Multi-LLM Integration</h4>
            <p>UltraTutor connects to Claude, Groq, or Gemini automatically based on available API keys.</p></div>
          <div class='prof-card'><h4>Teacher Value</h4>
            <p>Teacher Studio shows readiness analytics, skill gaps, and per-topic filtering.</p></div>
          <div class='prof-card'><h4>Wikipedia Real Data</h4>
            <p>Unknown topics are fetched from the Wikipedia API — the app never returns an empty answer.</p></div>
          <div class='prof-card'><h4>All Concepts Shown</h4>
            <p>Brain Brief displays every concept in the topic pack through interactive tabs, not just one.</p></div>
          <div class='prof-card'><h4>Readiness Trend</h4>
            <p>Students who retake the quiz see a personal score trend chart over multiple attempts.</p></div>
          <div class='prof-card'><h4>Tutor History</h4>
            <p>Every UltraTutor question is saved in session so students can review all explanations together.</p></div>
        </div>""",
        unsafe_allow_html=True,
    )

    st.markdown("### Python Concepts Used")
    st.dataframe(pd.DataFrame({
        "Concept": [
            "Functions", "Dictionaries", "Session State", "Forms",
            "DataFrame", "Charts", "File Export", "Testing",
            "Requests API", "Real Data Fallback", "LRU Cache",
            "Multi-provider LLM", "Tab components",
        ],
        "Use in Project": [
            "Separate app logic into reusable units",
            "Store topic packs, concept data, and API responses",
            "Remember topic, quiz state, tutor history, and score trend",
            "Submit mission and quiz safely without page reload",
            "Build teacher analytics with filtering",
            "Visualize readiness, trends, and skill gaps",
            "Download study brief as structured JSON",
            "Check app stability before demo with pytest",
            "Fetch Wikipedia data and call LLM APIs",
            "Use curated data first, then Wikipedia for unknown topics",
            "Cache Wikipedia results to avoid repeated API calls",
            "Support Claude, Groq, and Gemini with automatic fallback",
            "Show all topic concepts in interactive tabs",
        ],
    }), use_container_width=True)

    errors = validate_topics()
    if errors:
        st.warning("Topic validation issues found:")
        for issue in errors:
            st.write(f"- {issue}")
    else:
        st.success(f"Topic data validation passed — {len(TOPICS)} curated topics ready.")


# ── Demo Guide ────────────────────────────────────────────────────────────────

def demo_guide():
    hero()
    st.markdown("### 3-Minute Demo Script")
    steps = [
        "Open Preluma and say: this is a Python-based pre-class learning assistant with curated topics, Wikipedia fallback, and multi-LLM AI integration.",
        "Show the problem: students sit in lectures without any preparation — passive learning, low retention.",
        "Select Machine Learning and click Start Pre-Class Mission.",
        "Show Brain Brief — tiny answer, simple explanation, real example, and the concept tabs.",
        "Take the quiz — show how each question tests a different skill.",
        "Show Mistake Clinic — each wrong answer gets a clear correction and why.",
        "Ask UltraTutor: 'What is overfitting?' — show the structured AI answer.",
        "Show the LLM provider badge — Claude, Groq, or Gemini, whichever is active.",
        "Switch to Teacher Studio — show class readiness, skill gap chart, and topic filter.",
        "Show Evidence Board — Python concepts used, all features explained.",
    ]
    for step in steps:
        st.write(f"- {step}")
    st.success("Final line: Preluma does not replace teachers. It prepares students to understand teachers better.")


# ── Roadmap ───────────────────────────────────────────────────────────────────

def roadmap():
    hero()
    st.markdown("### Future Roadmap")
    st.dataframe(pd.DataFrame({
        "Phase":      ["Current Python Demo",   "Prototype",                "AI Upgrade",                          "Real Product"],
        "Goal":       ["Final project submission","Student/teacher accounts","RAG tutor with citations",           "Mobile/web app"],
        "Technology": ["Python + Streamlit",     "Python + database",       "Python + embeddings + retrieval",    "API backend + app frontend"],
        "Status":     ["Now",                    "Next",                    "Later",                               "Future"],
    }), use_container_width=True)
    st.code(
        "Current:    Python + Streamlit + curated packs + Wikipedia + Claude/Groq/Gemini\n"
        "Next:       Login + database + saved history per student\n"
        "AI Upgrade: Course notes + retrieval + cited tutor answers\n"
        "Future:     Mobile app + teacher dashboard + class codes + notifications",
        language="text",
    )


# ── Entry point ───────────────────────────────────────────────────────────────

def main():
    init_state()
    page, presentation = sidebar()
    if page == "Student Mission":
        student_mission(presentation)
    elif page == "Teacher Studio":
        teacher_studio()
    elif page == "Evidence Board":
        evidence_board()
    elif page == "Demo Guide":
        demo_guide()
    else:
        roadmap()


if __name__ == "__main__":
    main()
