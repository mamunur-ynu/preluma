import base64, json
from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from engine import build_brain_brief, build_pack, grade, make_questions, tutor_sections
from wiki_fetcher import smart_answer_from_pack
from teacher import build_teacher_dataframe, class_average_readiness, readiness_label
from topics import validate_topics

APP_VERSION = "16.0 Real Data"; APP_NAME="Preluma"; TAGLINE="Light Up Before Class"
TEAM_MEMBERS=[("MAMUNUR RASHID","Lead • UI • Integration"),("MD FAHIM","Engine • Quiz • Testing"),("MD JIARUL ISLAM","Topics • Data • Docs")]
TOPIC_OPTIONS = [
    "Quantum Mechanics",
    "Machine Learning",
    "Python Programming",
    "Data Structures",
    "Artificial Intelligence",
    "Convolutional Neural Network",
    "Natural Language Processing",
    "Statistics",
    "Urban Water Management",
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
def asset_to_data_uri():
    for path in [Path("assets/ynu_campus.jpg"), Path("ynu_campus.jpg")]:
        if path.exists(): return "data:image/jpeg;base64," + base64.b64encode(path.read_bytes()).decode("ascii")
    return ""
CAMPUS_BG=asset_to_data_uri()
st.set_page_config(page_title="Preluma", page_icon="✨", layout="wide")
CSS="""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');
html, body, [class*="css"] {font-family: 'Inter', sans-serif;}
.block-container {padding-top: 1rem; max-width: 1180px;}
[data-testid="stSidebar"] {background: #071021;} [data-testid="stSidebar"] * {color: #e5e7eb;}
.hero{position:relative;padding:32px 36px;min-height:260px;border-radius:30px;overflow:hidden;border:1px solid rgba(125,211,252,.22);background-size:cover;background-position:center;box-shadow:0 28px 60px rgba(2,6,23,.40)}
.hero::after{content:"";position:absolute;inset:0;background:linear-gradient(90deg,rgba(2,6,23,.80) 0%,rgba(15,23,42,.54) 48%,rgba(88,28,135,.50) 100%),radial-gradient(circle at 20% 10%,rgba(14,165,233,.23),transparent 32%);z-index:1}.hero-content{position:relative;z-index:2}.brand-row{display:flex;align-items:center;gap:14px;margin-bottom:16px}.logo-mark{width:42px;height:42px;border-radius:15px;background:linear-gradient(135deg,#38bdf8,#8b5cf6);box-shadow:0 12px 28px rgba(56,189,248,.22)}.brand-title{font-weight:900;color:#fff;font-size:18px}.brand-sub{color:#dbeafe;font-size:13px;margin-top:2px}.badge{display:inline-block;padding:8px 13px;border-radius:999px;background:rgba(14,165,233,.16);border:1px solid rgba(125,211,252,.35);color:#bae6fd;font-weight:850;font-size:13px}.uni-badge{display:inline-block;padding:8px 13px;border-radius:999px;background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.24);color:#fff;font-weight:850;font-size:12px;margin-left:8px}.hero h1{font-size:38px;line-height:1.08;color:white;margin:28px 0 14px;max-width:920px;text-shadow:0 4px 22px rgba(0,0,0,.48)}.hero p{font-size:16px;max-width:850px;color:#e0f2fe;line-height:1.6;text-shadow:0 3px 16px rgba(0,0,0,.40)}
.chip{display:inline-block;padding:10px 14px;margin:4px 6px 8px 0;border-radius:999px;background:#eef2ff;color:#3730a3;font-weight:900;font-size:13px}.team-box{padding:14px 15px;border-radius:22px;background:linear-gradient(135deg,rgba(15,23,42,.88),rgba(30,41,59,.78));border:1px solid rgba(148,163,184,.23);margin-top:16px}.team-title{color:#93c5fd;font-size:12px;font-weight:900;letter-spacing:.09em;text-transform:uppercase;margin-bottom:10px}.team-line{padding:9px 0;border-bottom:1px solid rgba(148,163,184,.12)}.team-line:last-child{border-bottom:0}.team-name{font-weight:900;color:#fff;font-size:13px}.team-role{font-size:11px;color:#94a3b8;margin-top:2px}.card{padding:18px 20px;border-radius:22px;background:linear-gradient(135deg,rgba(15,23,42,.94),rgba(30,41,59,.82));border:1px solid rgba(125,211,252,.18)}.metric-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:16px 0}.metric-number{font-size:26px;color:#fff;font-weight:900}.metric-label{font-size:12px;color:#93c5fd;font-weight:900;letter-spacing:.08em;text-transform:uppercase;margin-top:5px}.flow-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin:16px 0}.flow-card small{color:#93c5fd;font-weight:900;letter-spacing:.08em}.flow-card h3{color:#fff;margin:8px 0 8px;font-size:21px}.flow-card p{color:#cbd5e1;line-height:1.55}.answer-card{padding:18px 20px;border-radius:22px;background:rgba(15,23,42,.72);border:1px solid rgba(148,163,184,.20);margin:12px 0}.answer-title{color:#93c5fd;font-size:13px;font-weight:900;text-transform:uppercase;letter-spacing:.08em;margin-bottom:8px}.answer-card p,.answer-card li{color:#e5e7eb;font-size:15px;line-height:1.6}.notice{padding:13px 15px;border-radius:17px;background:rgba(59,130,246,.12);border:1px solid rgba(96,165,250,.24);color:#dbeafe;line-height:1.55;margin-bottom:12px}.prof-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin:16px 0}.prof-card{padding:17px;border-radius:21px;background:linear-gradient(135deg,rgba(14,165,233,.13),rgba(124,58,237,.11));border:1px solid rgba(125,211,252,.22)}.prof-card h4{margin:0 0 8px;color:#fff;font-size:17px}.prof-card p{color:#cbd5e1;font-size:14px;line-height:1.55}@media(max-width:900px){.metric-grid,.flow-grid,.prof-grid{grid-template-columns:1fr}.hero{padding:24px 22px}.hero h1{font-size:30px}}

.stButton > button {
    border-radius: 14px !important;
    font-weight: 900 !important;
    min-height: 48px !important;
    border: 1px solid rgba(125,211,252,.35) !important;
    background: linear-gradient(135deg, rgba(37,99,235,.95), rgba(124,58,237,.92)) !important;
    color: white !important;
}

</style>"""
st.markdown(CSS, unsafe_allow_html=True)

def reset():
    for key in ["pack","brief","questions","quiz_result","latest_session","student","topic","persona"]: st.session_state.pop(key, None)

def init_state(): st.session_state.setdefault("student","Mim"); st.session_state.setdefault("topic","Quantum Mechanics"); st.session_state.setdefault("persona","Normal Mode")

def sidebar():
    st.sidebar.markdown(f"## {APP_NAME}"); st.sidebar.caption(TAGLINE)
    page=st.sidebar.radio("Workspace",["Student Mission","Teacher Studio","Evidence Board","Demo Guide","Future Roadmap"])
    presentation=st.sidebar.toggle("Presentation Mode", value=True); st.sidebar.caption("Python + Streamlit + Wikipedia real data upgrade.")
    st.sidebar.markdown("<div class='team-box'><div class='team-title'>Project Team</div>", unsafe_allow_html=True)
    for name,role in TEAM_MEMBERS: st.sidebar.markdown(f"<div class='team-line'><div class='team-name'>{name}</div><div class='team-role'>{role}</div></div>", unsafe_allow_html=True)
    st.sidebar.markdown("</div><hr>", unsafe_allow_html=True)
    if st.sidebar.button("Reset session"): reset(); st.rerun()
    st.sidebar.caption(f"Version {APP_VERSION}"); return page,presentation

def hero():
    bg=f"linear-gradient(90deg,rgba(2,6,23,.80) 0%,rgba(15,23,42,.54) 48%,rgba(88,28,135,.50) 100%), url('{CAMPUS_BG}')" if CAMPUS_BG else "linear-gradient(135deg,#020617 0%,#111827 48%,#4c1d95 100%)"
    st.markdown(f"""<div class='hero' style="background-image:{bg};"><div class='hero-content'><div class='brand-row'><div class='logo-mark'></div><div><div class='brand-title'>Preluma</div><div class='brand-sub'>Light Up Before Class</div></div><span class='uni-badge'>Yunnan University</span></div><span class='badge'>Pre-class brain priming</span><h1>Prepare before class. Understand more during class.</h1><p>Built with a Yunnan University learning context. Preluma turns passive pre-class preparation into a short, guided, and interactive learning mission.</p></div></div>""", unsafe_allow_html=True)
    if not CAMPUS_BG: st.info("Campus image missing. Add assets/ynu_campus.jpg for the branded hero background.")

def chips(): st.markdown(" ".join([f"<span class='chip'>{c}</span>" for c in ["Topic","Brain Brief","Quiz","Mistake Clinic","Tutor","Class Questions","Dashboard"]]), unsafe_allow_html=True)

def metrics_steps():
    st.markdown("""<div class='metric-grid'><div class='card'><div class='metric-number'>4</div><div class='metric-label'>Quiz Checks</div></div><div class='card'><div class='metric-number'>5</div><div class='metric-label'>Class Questions</div></div><div class='card'><div class='metric-number'>1</div><div class='metric-label'>Mistake Clinic</div></div><div class='card'><div class='metric-number'>0–100</div><div class='metric-label'>Readiness Score</div></div></div><div class='flow-grid'><div class='card flow-card'><small>STEP 1</small><h3>Prime the brain</h3><p>Start with a compact Brain Brief before the lecture.</p></div><div class='card flow-card'><small>STEP 2</small><h3>Find weak spots</h3><p>Use a short quiz to detect misunderstanding.</p></div><div class='card flow-card'><small>STEP 3</small><h3>Ask better questions</h3><p>Leave with class-ready questions and a readiness score.</p></div></div>""", unsafe_allow_html=True)

def mission_control():
    st.markdown("### Mission Control"); st.markdown("<div class='notice'>Choose a topic. Preluma will generate a simple pre-class learning mission in Python-powered Streamlit.</div>", unsafe_allow_html=True)
    with st.form("mission_form", border=True):
        c1,c2,c3=st.columns([1.25,1,1])
        with c1:
            student=st.text_input("Student", value=st.session_state.student)
            topic_choice=st.selectbox("Lecture topic", TOPIC_OPTIONS, index=TOPIC_OPTIONS.index(st.session_state.topic) if st.session_state.topic in TOPIC_OPTIONS else 0)
            topic=st.text_input("Custom topic", value="Entropy") if topic_choice=="Custom Topic" else topic_choice
            lecture_time=st.text_input("Lecture time", value="Tomorrow 9 AM")
        with c2: persona=st.radio("Feedback style", ["Normal Mode","Coach Mode","Roast Mode"], captions=["Direct","Supportive","Funny pressure"])
        with c3:
            st.markdown("**Output quality**"); st.caption("Tiny answer"); st.caption("Simple explanation"); st.caption("Real example"); st.caption("Mistake correction"); st.caption("Class questions")
        start=st.form_submit_button("Start Pre-Class Mission", use_container_width=True)
    if start:
        pack=build_pack(topic); st.session_state.student=student; st.session_state.topic=topic; st.session_state.persona=persona; st.session_state.pack=pack; st.session_state.brief=build_brain_brief(pack); st.session_state.questions=make_questions(pack); st.session_state.quiz_result=None; st.session_state.latest_session=None; st.rerun()

def brain_brief():
    if "brief" not in st.session_state: return
    b=st.session_state.brief; st.markdown("### Brain Brief")
    st.markdown(f"""<div class='answer-card'><div class='answer-title'>Tiny answer</div><p>{b['tiny_answer']}</p></div><div class='answer-card'><div class='answer-title'>Explain simply</div><p>{b['simple']}</p></div><div class='answer-card'><div class='answer-title'>Key concept</div><p><b>{b['key_concept']}</b>: {b['concept_simple']}</p></div><div class='answer-card'><div class='answer-title'>Real-life example</div><p>{b['example']}</p></div><div class='answer-card'><div class='answer-title'>Common mistake</div><p>{b['misconception']}</p></div>""", unsafe_allow_html=True)
    with st.expander("Important facts"):
        for fact in b["facts"]: st.write(f"- {fact}")

def quiz():
    if "questions" not in st.session_state: return
    st.markdown("### Quick Quiz"); st.caption("Answer once. Preluma will detect weak skills and explain mistakes.")
    with st.form("quiz_form", border=True):
        answers={}
        for i,q in enumerate(st.session_state.questions): answers[i]=st.radio(q["q"], q["options"], key=f"quiz_{i}")
        submit=st.form_submit_button("Check Readiness", use_container_width=True)
    if submit:
        result=grade(st.session_state.questions, answers); st.session_state.quiz_result=result; st.session_state.latest_session={"Student":st.session_state.student,"Topic":st.session_state.pack["title"],"Readiness":result["pct"],"Weak Skill":result["weakest"]}; st.rerun()

def result_section():
    result=st.session_state.get("quiz_result")
    if not result: return
    st.markdown("### Readiness Result"); st.success(f"{readiness_label(result['pct'])}: {result['score']}/{result['total']} ({result['pct']}%)")
    st.markdown("### Mistake Clinic")
    for i,d in enumerate(result["details"],1):
        with st.expander(f"Question {i}: {'Correct' if d['correct'] else 'Review needed'} — {d['skill']}"):
            st.write(f"Your answer: {d['chosen']}"); st.write(f"Correct answer: {d['answer']}"); st.write(f"Why: {d['why']}")
            if not d["correct"]: st.info("Tiny fix: read the definition, connect it to one example, then say it in your own words.")
    df=build_teacher_dataframe(st.session_state.latest_session); avg=class_average_readiness(df); fig=go.Figure(); fig.add_bar(x=["You","Class Average"], y=[result["pct"], avg]); fig.update_layout(title="Readiness Comparison", yaxis_range=[0,100], height=320, margin=dict(l=20,r=20,t=45,b=20)); st.plotly_chart(fig, use_container_width=True)

def tutor():
    if "pack" not in st.session_state: return
    st.markdown("### UltraTutor"); st.markdown("<div class='notice'>If one idea is confusing, ask here. Tutor will answer with tiny answer, example, mistake, and exam angle.</div>", unsafe_allow_html=True)
    q=st.text_input("What did you not understand?", value="I do not understand the main concept")
    if st.button("Explain Clearly", use_container_width=True):
        s=tutor_sections(st.session_state.pack, q, st.session_state.persona); st.markdown(f"#### {s['concept']}")
        st.markdown(f"""<div class='answer-card'><div class='answer-title'>Tiny answer</div><p>{s['tiny_answer']}</p></div><div class='answer-card'><div class='answer-title'>Explain simply</div><p>{s['explain_simply']}</p></div><div class='answer-card'><div class='answer-title'>Real-life example</div><p>{s['real_life_example']}</p></div><div class='answer-card'><div class='answer-title'>Common mistake</div><p>{s['common_mistake']}</p></div><div class='answer-card'><div class='answer-title'>Exam angle</div><p>{s['exam_angle']}</p></div>""", unsafe_allow_html=True)

def questions_download():
    if "pack" not in st.session_state: return
    st.markdown("### Smart Class Questions")
    for i,q in enumerate(st.session_state.pack["class_questions"],1): st.write(f"{i}. {q}")
    payload={"student":st.session_state.student,"topic":st.session_state.pack["title"],"brief":st.session_state.brief,"class_questions":st.session_state.pack["class_questions"],"quiz_result":st.session_state.get("quiz_result")}
    st.download_button("Download Study Brief", data=json.dumps(payload, indent=2), file_name=f"preluma_{st.session_state.pack['title'].lower().replace(' ','_')}_brief.json", mime="application/json", use_container_width=True)

def student_mission(presentation):
    hero(); chips(); mission_control()
    if not presentation: metrics_steps()
    brain_brief(); quiz(); result_section(); tutor(); questions_download()
    if presentation: metrics_steps()

def teacher_studio():
    hero(); st.markdown("### Teacher Studio"); st.markdown("<div class='notice'>Teacher Studio shows how teachers can monitor readiness, weak skills, and topic preparation before class.</div>", unsafe_allow_html=True); df=build_teacher_dataframe(st.session_state.get("latest_session")); c1,c2=st.columns([1.1,1])
    with c1: st.dataframe(df, use_container_width=True)
    with c2:
        fig=px.bar(df,x="Student",y="Readiness",color="Weak Skill",title="Class Readiness"); fig.update_layout(yaxis_range=[0,100], height=360); st.plotly_chart(fig, use_container_width=True)
    st.metric("Class Average Readiness", f"{class_average_readiness(df)}%"); st.write("Teacher value: the teacher can see who is ready, who is confused, and what topic needs a quick warm-up.")

def evidence_board():
    render_hero()
    st.markdown("### Evidence Board")
    st.markdown("""
    <div class='prof-grid'>
        <div class='prof-card'><h4>Clear Problem</h4><p>Students often enter lectures unprepared, which leads to passive learning and poor retention.</p></div>
        <div class='prof-card'><h4>Python Implementation</h4><p>The project is built with Python, Streamlit, Pandas, Plotly, dictionaries, functions, forms, and session state.</p></div>
        <div class='prof-card'><h4>Learning Workflow</h4><p>Preluma combines Brain Brief, quiz, Mistake Clinic, UltraTutor, class questions, and readiness score.</p></div>
        <div class='prof-card'><h4>Data Structure Thinking</h4><p>Topic packs use nested dictionaries, aliases, schema validation, and normalized data flow.</p></div>
        <div class='prof-card'><h4>Teacher Value</h4><p>Teacher Studio demonstrates analytics for readiness and weak skill detection.</p></div>
        <div class='prof-card'><h4>Wikipedia Real Data</h4><p>Unknown topics can be fetched through the Wikipedia API using Python requests.</p></div>
        <div class='prof-card'><h4>Smart QnA</h4><p>Questions are answered from curated topic data and fetched summary text, with examples and reliability notes.</p></div>
        <div class='prof-card'><h4>Massive Topic Base</h4><p>Curated topics were expanded while unknown topics use a real-data fallback.</p></div>
        <div class='prof-card'><h4>Future Potential</h4><p>The roadmap can grow into login, database, PDF notes, retrieval, and real AI tutor support.</p></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Python Concepts Used")
    concepts_df = pd.DataFrame({
        "Concept": ["Functions", "Dictionaries", "Session State", "Forms", "DataFrame", "Charts", "File Export", "Testing", "Requests API", "Real Data Fallback"],
        "Use in Project": [
            "Separate app logic into reusable units",
            "Store topic packs and concepts",
            "Remember selected topic and quiz result",
            "Submit mission and quiz safely",
            "Build teacher analytics",
            "Visualize readiness",
            "Download study brief as JSON",
            "Check app stability before demo",
            "Fetch Wikipedia data using Python",
            "Use curated data first, then real online data for unknown topics",
        ],
    })
    st.dataframe(concepts_df, use_container_width=True)

    errors = validate_topics()
    if len(errors) > 0:
        st.warning("Topic validation issues found:")
        for issue in errors:
            st.write(f"- {issue}")
    else:
        st.success("Topic data validation passed for curated demo packs.")

def demo_guide():
    hero(); st.markdown("### 3-Minute Demo Script")
    for x in ["Say: Preluma is a Python-based pre-class learning assistant with curated topics and Wikipedia real-data fallback.","Show the problem: students attend lectures unprepared.","Select Quantum Mechanics or Machine Learning.","Click Start Pre-Class Mission.","Show Brain Brief with Wikipedia source link for unknown topics.","Take the quiz and show Mistake Clinic.","Ask Smart QnA any question and show answer + example.","Show Teacher Studio and Evidence Board."]: st.write("- "+x)
    st.success("Final line: Preluma does not replace teachers. It prepares students to understand teachers better.")

def roadmap():
    hero(); st.markdown("### Future Roadmap"); st.dataframe(pd.DataFrame({"Phase":["Current Python Demo","Prototype","AI Upgrade","Real Product"],"Goal":["Final project submission","Student/teacher accounts","RAG tutor with citations","Mobile/web app"],"Technology":["Python + Streamlit","Python + database","Python + embeddings + retrieval","API backend + app frontend"],"Status":["Now","Next","Later","Future"]}), use_container_width=True)
    st.code("""Current: Python + Streamlit + curated topic packs
Next: Login + database + saved history
AI Upgrade: Course notes + retrieval + generated tutor answer + citations
Future Product: Mobile app + teacher dashboard + class codes + notifications""", language="text")

def main():
    init_state(); page,presentation=sidebar()
    if page=="Student Mission": student_mission(presentation)
    elif page=="Teacher Studio": teacher_studio()
    elif page=="Evidence Board": evidence_board()
    elif page=="Demo Guide": demo_guide()
    else: roadmap()
if __name__=="__main__": main()
