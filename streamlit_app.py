from pathlib import Path
import json

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from engine import build_brain_brief, build_pack, grade, make_questions, tutor_sections
from teacher import build_teacher_dataframe, class_average_readiness, readiness_label
from topics import TOPIC_OPTIONS, validate_topics
from wiki_fetcher import smart_answer_from_pack


APP_VERSION = "17.1 Strict Python Import Fix"
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


def init_state():
    st.session_state.setdefault("student", "Mim")
    st.session_state.setdefault("topic", "Quantum Mechanics")
    st.session_state.setdefault("persona", "Normal Mode")


def reset_session():
    for key in [
        "student",
        "topic",
        "persona",
        "use_wiki",
        "pack",
        "brief",
        "questions",
        "quiz_result",
        "latest_session",
    ]:
        st.session_state.pop(key, None)


def sidebar():
    st.sidebar.title(APP_NAME)
    st.sidebar.caption(TAGLINE)

    page = st.sidebar.radio(
        "Workspace",
        [
            "Student Mission",
            "Teacher Studio",
            "Evidence Board",
            "Project Team",
            "Demo Guide",
            "Future Roadmap",
        ],
    )

    presentation = st.sidebar.toggle("Presentation Mode", value=True)
    st.sidebar.info("Strict Python-only codebase: Streamlit native UI, Pandas, Plotly, Requests.")

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
    left, right = st.columns([1, 1])
    with left:
        st.title("Prepare before class. Understand more during class.")
        st.write(
            "Preluma is a Python-based pre-class learning assistant built with Streamlit. "
            "It creates a Brain Brief, quiz, Mistake Clinic, Smart QnA, and teacher dashboard."
        )
        st.caption("Yunnan University learning context • Python project • Streamlit native UI")
    with right:
        if CAMPUS_IMAGE.exists():
            st.image(str(CAMPUS_IMAGE), caption="Yunnan University campus context", use_container_width=True)
        else:
            st.info("Campus image not found. Add assets/ynu_campus.jpg")


def flow_chips():
    st.write("**Learning Flow:** Topic → Brain Brief → Quiz → Mistake Clinic → Smart QnA → Class Questions → Dashboard")


def metrics():
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Quiz Checks", "4")
    c2.metric("Class Questions", "5")
    c3.metric("Mistake Clinic", "1")
    c4.metric("Readiness Score", "0–100")


def mission_control():
    st.subheader("Mission Control")
    st.info(
        "Choose a topic. Preluma will generate a pre-class learning mission using Python, "
        "curated topic data, and optional Wikipedia real-data fallback."
    )

    with st.form("mission_form", border=True):
        c1, c2, c3 = st.columns([1, 1.2, 1])
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
            st.caption("Native Streamlit form")

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

    st.subheader("Brain Brief")
    c1, c2 = st.columns(2)
    with c1:
        st.info(b["tiny_answer"])
        st.write("**Simple explanation**")
        st.write(b["simple"])
        st.write("**Key concept**")
        st.write(f"{b['key_concept']}: {b['concept_simple']}")
    with c2:
        st.write("**Real-life example**")
        st.write(b["example"])
        st.write("**Common mistake**")
        st.warning(b["misconception"])

    with st.expander("Important facts"):
        for fact in b["facts"]:
            st.write(f"- {fact}")

    if pack.get("source_url"):
        st.success("Real data source used.")
        st.write(pack.get("source_url"))


def quiz():
    if "questions" not in st.session_state:
        return

    st.subheader("Quick Quiz")
    st.caption("The quiz checks definition, concept, application, and misconception.")

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

    st.subheader("Readiness Result")
    st.metric("Your Readiness", f"{result['pct']}%", f"{result['score']}/{result['total']} correct")
    st.write(f"Status: **{readiness_label(result['pct'])}**")

    st.subheader("Mistake Clinic")
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
    fig.update_layout(title="Readiness Comparison", yaxis_range=[0, 100], height=320)
    st.plotly_chart(fig, use_container_width=True)


def smart_qna():
    if "pack" not in st.session_state:
        return

    st.subheader("Smart QnA + UltraTutor")
    question = st.text_input("Ask any question about this topic", value="Explain this topic with a simple example")

    c1, c2 = st.columns(2)
    with c1:
        ask = st.button("Get Smart Answer", use_container_width=True)
    with c2:
        tutor = st.button("Explain Like a Tutor", use_container_width=True)

    if ask:
        ans = smart_answer_from_pack(st.session_state.pack, question)
        st.write("**Smart answer**")
        st.write(ans["answer"])
        st.write("**Simple version**")
        st.write(ans["simple"])
        st.write("**Example**")
        st.write(ans["example"])
        st.caption(ans["note"])
        if ans.get("source_url"):
            st.write(ans["source_url"])

    if tutor:
        sections = tutor_sections(st.session_state.pack, question, st.session_state.persona)
        st.write(f"**Concept:** {sections['concept']}")
        st.write("**Tiny answer**")
        st.write(sections["tiny_answer"])
        st.write("**Explain simply**")
        st.write(sections["explain_simply"])
        st.write("**Real-life example**")
        st.write(sections["real_life_example"])
        st.write("**Common mistake**")
        st.warning(sections["common_mistake"])
        st.write("**Exam angle**")
        st.info(sections["exam_angle"])


def class_questions_and_download():
    if "pack" not in st.session_state:
        return

    st.subheader("Smart Class Questions")
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
    flow_chips()
    mission_control()
    brain_brief()
    quiz()
    result_and_mistake_clinic()
    smart_qna()
    class_questions_and_download()
    if presentation:
        metrics()


def teacher_studio():
    hero()
    st.subheader("Teacher Studio")
    st.write("Teacher Studio demonstrates how a teacher can monitor readiness, topic preparation, and weak skills.")
    df = build_teacher_dataframe(st.session_state.get("latest_session"))
    st.dataframe(df, use_container_width=True)

    fig = px.bar(df, x="Student", y="Readiness", color="Weak Skill", title="Class Readiness")
    fig.update_layout(yaxis_range=[0, 100], height=360)
    st.plotly_chart(fig, use_container_width=True)
    st.metric("Class Average Readiness", f"{class_average_readiness(df)}%")


def evidence_board():
    hero()
    st.subheader("Evidence Board")
    st.write("This page explains why the project is valuable as a Python final project.")

    c1, c2, c3 = st.columns(3)
    c1.info("Problem: students often attend lectures unprepared.")
    c2.info("Solution: short Python-powered preparation mission.")
    c3.info("Value: Brain Brief, quiz, Mistake Clinic, QnA, and teacher dashboard.")

    st.subheader("Python Concepts Used")
    concepts = pd.DataFrame(
        {
            "Concept": [
                "Functions",
                "Dictionaries",
                "Session State",
                "Forms",
                "DataFrame",
                "Plotly Charts",
                "Requests API",
                "File Export",
                "Testing",
            ],
            "Use in Project": [
                "Separate app logic into reusable units",
                "Store topic packs and concepts",
                "Remember selected topic and quiz result",
                "Submit mission and quiz safely",
                "Build teacher analytics",
                "Visualize readiness",
                "Fetch Wikipedia data using Python",
                "Download study brief as JSON",
                "Check app stability before demo",
            ],
        }
    )
    st.dataframe(concepts, use_container_width=True)

    st.subheader("Topic Data Validation")
    errors = validate_topics()
    if errors:
        st.warning("Some topic validation issues were found.")
        for issue in errors:
            st.write(f"- {issue}")
    else:
        st.success("Topic data validation passed.")


def project_team():
    st.title("Project Team")
    st.write("Team Preluma — Yunnan University")

    if TEAM_IMAGE.exists():
        st.image(str(TEAM_IMAGE), caption="Team Preluma", use_container_width=True)
    else:
        st.warning("Team photo missing. Add assets/team_preluma.jpg")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.subheader("MD FAHIM")
        st.write("Feature Logic • Quiz Testing")
        st.write("Supported quiz behavior checking, interaction feedback, and feature testing.")
    with c2:
        st.subheader("MAMUNUR RASHID")
        st.write("Core Development • UI/UX • Integration • Deployment")
        st.write(
            "Handled the hardest core part of Preluma: product design, Python Streamlit UI, "
            "system integration, deployment, real-data upgrade, and final demo flow."
        )
    with c3:
        st.subheader("MD JIARUL ISLAM")
        st.write("Topic Data • Documentation")
        st.write("Supported topic data organization, documentation, and presentation preparation.")

    st.subheader("Work Division")
    st.dataframe(
        pd.DataFrame(
            {
                "Member": ["MAMUNUR RASHID", "MD FAHIM", "MD JIARUL ISLAM"],
                "Main Responsibility": [
                    "Core development, UI/UX, system integration, deployment, real-data upgrade, final demo flow",
                    "Feature logic, quiz testing, interaction feedback",
                    "Topic data, documentation, presentation support",
                ],
                "Project Value": [
                    "Builds the hardest core system and connects all parts into one deployed Python Streamlit product",
                    "Improves interaction quality and checks app behavior",
                    "Strengthens content base and presentation material",
                ],
            }
        ),
        use_container_width=True,
    )


def demo_guide():
    hero()
    st.subheader("3-Minute Demo Guide")
    st.write("1. Say: Preluma is a Python-only Streamlit project.")
    st.write("2. Explain the problem: students enter lectures unprepared.")
    st.write("3. Choose a topic and start the mission.")
    st.write("4. Show Brain Brief, quiz, Mistake Clinic, and Smart QnA.")
    st.write("5. Show Teacher Studio and Evidence Board.")
    st.write("6. Show Project Team and workload distribution.")
    st.success("Final line: Preluma does not replace teachers. It prepares students to understand teachers better.")


def roadmap():
    hero()
    st.subheader("Future Roadmap")
    df = pd.DataFrame(
        {
            "Phase": ["Current Python Demo", "Prototype", "AI Upgrade", "Real Product"],
            "Goal": ["Final project submission", "Student/teacher accounts", "RAG tutor with citations", "Mobile/web app"],
            "Technology": ["Python + Streamlit", "Python + database", "Python + retrieval", "Python backend + app frontend"],
            "Status": ["Now", "Next", "Later", "Future"],
        }
    )
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
