from pathlib import Path
import base64
import json

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from engine import build_brain_brief, build_pack, grade, make_questions, tutor_sections
from teacher import build_teacher_dataframe, class_average_readiness, readiness_label, teacher_analytics, search_student
from result_generator import generate_result_file
from topics import TOPIC_OPTIONS, validate_topics
from wiki_fetcher import smart_answer_from_pack
from storage_core import append_student_row, next_record_id, read_recent_logs, timestamp
from llm import active_provider as _provider, available_providers, llm_available, llm_tutor, detect_topic_from_question, llm_free_chat
from auth import authenticate, register, get_all_students, username_exists
from homework_core import (
    create_homework,
    homework_for_student,
    homework_overview,
    load_homework,
    load_questions,
    load_student_mistakes,
    mark_notifications_read,
    notifications_for_student,
    seed_homework_demo,
    submit_homework,
)

APP_VERSION = "35.0 Login System"
APP_NAME    = "Preluma"
TAGLINE     = "Light Up Before Class"

TEAM_MEMBERS = [
    ("MAMUNUR RASHID", "Core Development · UI/UX · Integration · Deployment"),
    ("MD FAHIM",       "Feature Logic · Quiz Testing · Interaction Feedback"),
    ("MD JIARUL ISLAM","Topic Data · Documentation · Presentation Support"),
]

CAMPUS_IMAGE  = Path("assets/ynu_campus.jpg")
TEAM_IMAGE    = Path("assets/team_preluma.jpg")
SIDEBAR_IMAGE = Path("assets/sidebar_bg.jpg")   # YNU tower night photo

st.set_page_config(page_title="Preluma — Light Up Before Class", page_icon=None, layout="wide")


@st.cache_data(show_spinner=False)
def image_data_uri(path_str):
    path = Path(path_str)
    if path.exists():
        suffix = path.suffix.lower().replace(".", "")
        mime = "jpeg" if suffix in ["jpg","jpeg"] else "png"
        data = base64.b64encode(path.read_bytes()).decode("ascii")
        return f"data:image/{mime};base64,{data}"
    return ""

CAMPUS_URI  = image_data_uri(str(CAMPUS_IMAGE))
TEAM_URI    = image_data_uri(str(TEAM_IMAGE))
SIDEBAR_URI = image_data_uri(str(SIDEBAR_IMAGE))


CSS = """
<style>
/* System font stack — no external CDN required, works offline */
*, *::before, *::after { box-sizing: border-box; }
html, body, [class*="css"] { font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }
.block-container { max-width: 100% !important; padding-top: 1.5rem !important; padding-left: 2.5rem !important; padding-right: 2.5rem !important; }
[data-testid="stSidebar"] { background: #03080f; border-right: 1px solid rgba(255,255,255,.06); }
[data-testid="stSidebar"] * { color: #e2e8f0; }
h1, h2, h3 { letter-spacing: -0.02em; }

/* ── Hero ── */
.hero {
    position: relative; min-height: 340px; border-radius: 28px;
    overflow: hidden; border: 1px solid rgba(255,255,255,.10);
    box-shadow: 0 32px 80px rgba(0,0,0,.55); margin-bottom: 2rem;
    background-size: cover; background-position: center 35%;
}
.hero-overlay {
    position: absolute; inset: 0;
    background:
        linear-gradient(105deg, rgba(2,6,23,.92) 0%, rgba(7,14,35,.78) 38%,
        rgba(15,23,62,.55) 65%, rgba(55,10,120,.40) 100%),
        radial-gradient(ellipse at 15% 50%, rgba(56,189,248,.18) 0%, transparent 50%);
}
.hero-content {
    position: relative; z-index: 2; padding: 44px 52px;
    display: flex; flex-direction: column; justify-content: center; min-height: 340px;
}
.hero-top { display: flex; align-items: center; gap: 12px; margin-bottom: 24px; }
.logo-mark {
    width: 44px; height: 44px; border-radius: 14px; flex-shrink: 0;
    background: linear-gradient(135deg, #38bdf8 0%, #818cf8 50%, #a78bfa 100%);
    box-shadow: 0 8px 24px rgba(56,189,248,.30);
    display: flex; align-items: center; justify-content: center;
}
.logo-mark svg { width: 22px; height: 22px; }
.brand-name { font-size: 17px; font-weight: 800; color: #fff; }
.brand-tag  { font-size: 12px; color: #93c5fd; margin-top: 1px; }
.uni-pill {
    margin-left: auto; padding: 6px 14px; border-radius: 999px;
    background: rgba(255,255,255,.10); border: 1px solid rgba(255,255,255,.20);
    color: #e2e8f0; font-size: 12px; font-weight: 600;
}
.ai-pill {
    padding: 6px 12px; border-radius: 999px; margin-left: 8px;
    background: rgba(52,211,153,.12); border: 1px solid rgba(52,211,153,.25);
    color: #6ee7b7; font-size: 11px; font-weight: 700;
}
.hero-badge {
    display: inline-flex; align-items: center; gap: 6px;
    padding: 7px 14px; border-radius: 999px; margin-bottom: 18px;
    background: rgba(56,189,248,.15); border: 1px solid rgba(56,189,248,.35);
    color: #7dd3fc; font-size: 11px; font-weight: 700; letter-spacing: .05em; text-transform: uppercase;
}
.hero-badge::before { content: ""; width: 6px; height: 6px; border-radius: 50%; background: #38bdf8; }
.hero h1 {
    font-size: 42px; line-height: 1.06; font-weight: 900; color: #fff;
    margin: 0 0 16px; letter-spacing: -.025em; max-width: 780px;
    text-shadow: 0 2px 30px rgba(0,0,0,.50);
}
.hero h1 span { color: #7dd3fc; }
.hero-sub { font-size: 16px; color: #cbd5e1; line-height: 1.65; max-width: 640px; }
.hero-stats { display: flex; gap: 32px; margin-top: 28px; }
.hero-stat-num { font-size: 22px; font-weight: 800; color: #fff; }
.hero-stat-lbl { font-size: 11px; color: #94a3b8; margin-top: 2px; font-weight: 500; }

/* ── Progress ── */
.progress-wrap {
    display: flex; gap: 0; margin: 0 0 2rem;
    background: rgba(15,23,42,.60); border-radius: 16px;
    padding: 6px; border: 1px solid rgba(255,255,255,.07);
    overflow-x: auto;
}
.progress-step {
    flex: 1; min-width: 90px; text-align: center; padding: 10px 6px; border-radius: 12px;
    font-size: 11px; font-weight: 600; color: #64748b; white-space: nowrap;
}
.progress-step.done   { color: #34d399; background: rgba(52,211,153,.10); }
.progress-step.active { color: #38bdf8; background: rgba(56,189,248,.12); font-weight: 800; }

/* ── Section header ── */
.sec-head { display: flex; align-items: center; gap: 12px; margin: 2rem 0 1rem; }
.sec-icon {
    width: 36px; height: 36px; border-radius: 10px; flex-shrink: 0;
    display: flex; align-items: center; justify-content: center; font-size: 16px;
}
.sec-title { font-size: 20px; font-weight: 800; color: #f1f5f9; }
.sec-sub   { font-size: 13px; color: #64748b; margin-top: 2px; }

/* ── Cards ── */
.card-glass {
    background: rgba(15,23,42,.70); border: 1px solid rgba(255,255,255,.08);
    border-radius: 20px; padding: 20px 22px; margin: 10px 0;
}
.card-glass:hover { border-color: rgba(56,189,248,.22); }
.albl { font-size: 11px; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; margin-bottom: 8px; }
.atxt { font-size: 15px; color: #e2e8f0; line-height: 1.7; }
.lbl-blue   { color: #60a5fa; }
.lbl-purple { color: #a78bfa; }
.lbl-green  { color: #34d399; }
.lbl-orange { color: #fb923c; }
.lbl-red    { color: #f87171; }
.lbl-yellow { color: #fbbf24; }
.lbl-cyan   { color: #22d3ee; }

/* ── AI bar ── */
.ai-bar {
    display: flex; align-items: center; gap: 10px; padding: 12px 16px;
    border-radius: 14px; margin-bottom: 16px;
    background: rgba(52,211,153,.08); border: 1px solid rgba(52,211,153,.25);
}
.ai-dot { width: 8px; height: 8px; border-radius: 50%; background: #34d399; box-shadow: 0 0 8px #34d399; }
.ai-txt { font-size: 13px; color: #6ee7b7; font-weight: 600; }

/* ── Notice ── */
.notice {
    padding: 13px 16px; border-radius: 14px; margin-bottom: 14px;
    background: rgba(56,189,248,.08); border: 1px solid rgba(56,189,248,.20);
    color: #bae6fd; font-size: 14px; line-height: 1.6;
}

/* ── Score ── */
.score-big { font-size: 56px; font-weight: 900; line-height: 1; }
.score-lbl { font-size: 14px; color: #94a3b8; margin-top: 6px; }
.r-pill { display: inline-block; padding: 6px 18px; border-radius: 999px; font-size: 14px; font-weight: 700; margin-top: 8px; }
.pill-g { background: rgba(52,211,153,.15); color: #34d399; border: 1px solid rgba(52,211,153,.30); }
.pill-y { background: rgba(251,191,36,.15);  color: #fbbf24; border: 1px solid rgba(251,191,36,.30); }
.pill-r { background: rgba(248,113,113,.15); color: #f87171; border: 1px solid rgba(248,113,113,.30); }

/* ── KPI ── */
.kpi-grid { display: grid; grid-template-columns: repeat(4,1fr); gap: 14px; margin: 1.5rem 0; }
.kpi-card {
    background: rgba(15,23,42,.70); border: 1px solid rgba(255,255,255,.07);
    border-radius: 18px; padding: 20px 18px;
}
.kpi-num { font-size: 30px; font-weight: 900; color: #fff; }
.kpi-lbl { font-size: 11px; font-weight: 700; color: #64748b; text-transform: uppercase; letter-spacing: .07em; margin-top: 6px; }

/* ── Flow ── */
.flow-grid { display: grid; grid-template-columns: repeat(3,1fr); gap: 16px; margin: 1.5rem 0; }
.flow-card {
    background: rgba(15,23,42,.60); border: 1px solid rgba(255,255,255,.07);
    border-radius: 18px; padding: 22px 20px;
}
.flow-step  { font-size: 11px; font-weight: 700; color: #38bdf8; letter-spacing: .08em; text-transform: uppercase; margin-bottom: 10px; }
.flow-title { font-size: 18px; font-weight: 800; color: #f1f5f9; margin-bottom: 8px; }
.flow-desc  { font-size: 14px; color: #94a3b8; line-height: 1.6; }

/* ── Evidence ── */
.ev-grid { display: grid; grid-template-columns: repeat(3,1fr); gap: 14px; margin: 1.5rem 0; }
.ev-card {
    background: linear-gradient(135deg, rgba(14,165,233,.10), rgba(124,58,237,.08));
    border: 1px solid rgba(125,211,252,.15); border-radius: 18px; padding: 18px 16px;
}
.ev-card h4 { font-size: 15px; font-weight: 700; color: #e2e8f0; margin: 0 0 8px; }
.ev-card p  { font-size: 13px; color: #94a3b8; line-height: 1.6; margin: 0; }

/* ── Rubric ── */
.rubric-grid { display: grid; grid-template-columns: repeat(2,1fr); gap: 14px; margin: 1.5rem 0; }
.rubric-card {
    padding: 18px; border-radius: 22px;
    background: linear-gradient(135deg, rgba(34,197,94,.12), rgba(14,165,233,.10));
    border: 1px solid rgba(125,211,252,.22);
}
.rubric-card h4 { color: #fff; margin: 0 0 8px; font-size: 16px; }
.rubric-card p  { color: #cbd5e1; margin: 0; line-height: 1.55; font-size: 14px; }

/* ── Team ── */
.member-grid { display: grid; grid-template-columns: repeat(3,1fr); gap: 16px; margin: 1.5rem 0; }
.member-card {
    padding: 20px; border-radius: 24px;
    background: linear-gradient(135deg, rgba(15,23,42,.94), rgba(30,41,59,.82));
    border: 1px solid rgba(125,211,252,.18);
}
/* Equal styling for all team members — no visual hierarchy */
.member-role { color: #93c5fd; font-weight: 900; font-size: 11px; letter-spacing: .08em; text-transform: uppercase; margin-bottom: 8px; }
.member-card h3 { color: #fff; margin: 0 0 8px; font-size: 19px; }
.member-card p  { color: #cbd5e1; line-height: 1.55; margin: 0; font-size: 14px; }
.contrib-list { margin-top: 10px; padding-left: 16px; color: #94a3b8; font-size: 13px; }
.contrib-list li { margin-bottom: 5px; }

/* ── Chip ── */
.chip-row { display: flex; flex-wrap: wrap; gap: 8px; margin: 1rem 0 1.5rem; }
.chip { padding: 7px 14px; border-radius: 999px; background: rgba(99,102,241,.12); border: 1px solid rgba(99,102,241,.25); color: #a5b4fc; font-size: 12px; font-weight: 600; }

/* ── Concept ── */
.concept-block {
    background: rgba(15,23,42,.55); border: 1px solid rgba(255,255,255,.07);
    border-radius: 16px; padding: 16px 18px; margin: 8px 0;
}
.concept-block-title { font-size: 11px; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; margin-bottom: 8px; color: #818cf8; }
.concept-block p { font-size: 14px; color: #cbd5e1; line-height: 1.65; margin: 3px 0; }

/* ── Sidebar team ── */
.team-box { background: rgba(15,23,42,.80); border: 1px solid rgba(255,255,255,.07); border-radius: 16px; padding: 14px 16px; margin-top: 16px; }
.team-ttl { font-size: 10px; font-weight: 800; color: #475569; letter-spacing: .10em; text-transform: uppercase; margin-bottom: 12px; }
.team-row { padding: 9px 0; border-bottom: 1px solid rgba(255,255,255,.05); }
.team-row:last-child { border-bottom: none; }
.team-name { font-size: 12px; font-weight: 700; color: #e2e8f0; }
.team-role { font-size: 11px; color: #475569; margin-top: 2px; }

/* ── Buttons ── */
.stButton > button {
    border-radius: 14px !important; font-weight: 700 !important; font-size: 14px !important;
    min-height: 50px !important; border: none !important;
    background: linear-gradient(135deg, #2563eb, #7c3aed) !important;
    color: #fff !important; box-shadow: 0 4px 20px rgba(37,99,235,.35) !important;
}
.stButton > button:hover { opacity: .88 !important; }

@media(max-width:900px) {
    .kpi-grid,.flow-grid,.ev-grid,.rubric-grid,.member-grid { grid-template-columns: 1fr; }
    .hero-content { padding: 28px 24px; }
    .hero h1 { font-size: 28px; }
    .hero-stats { gap: 20px; }
}

/* ── Team photo: full image, no face cropping ── */
.team-photo-hero { position:relative; width:100%; aspect-ratio:16/9; border-radius:30px; overflow:hidden; background-size:100% auto; background-position:center; background-repeat:no-repeat; background-color:#020617; border:1px solid rgba(125,211,252,.25); box-shadow:0 28px 70px rgba(0,0,0,.42); margin:1rem 0 1.75rem; }
.team-photo-hero::after { content:''; position:absolute; inset:0; background:linear-gradient(0deg,rgba(2,6,23,.90) 0%,rgba(2,6,23,.18) 48%,rgba(2,6,23,.12) 100%),linear-gradient(90deg,rgba(14,165,233,.12),rgba(124,58,237,.14)); }
.team-photo-content { position:absolute; z-index:2; left:34px; right:34px; bottom:30px; }
.team-photo-content h1 { color:#fff; font-size:38px; line-height:1.12; margin:12px 0 8px; text-shadow:0 4px 24px rgba(0,0,0,.65); }
.team-photo-content p { color:#e2e8f0; max-width:760px; line-height:1.55; margin:0; text-shadow:0 3px 18px rgba(0,0,0,.65); }
.sidebar-profile { padding:12px 14px; border-radius:16px; background:rgba(15,23,42,.72); border:1px solid rgba(148,163,184,.12); margin:.35rem 0 1rem; }
.sidebar-profile b { color:#f8fafc; font-size:13px; }
.sidebar-profile span { color:#94a3b8; font-size:12px; }
.nav-label { color:#64748b; font-size:10px; font-weight:900; letter-spacing:.14em; text-transform:uppercase; margin:16px 0 7px; }
.ai-main-answer { padding:22px 24px; border-radius:22px; background:linear-gradient(135deg,rgba(15,23,42,.97),rgba(30,41,59,.88)); border:1px solid rgba(99,102,241,.30); box-shadow:0 18px 45px rgba(2,6,23,.26); color:#e5e7eb; font-size:16px; line-height:1.75; white-space:pre-wrap; }
.ai-meta { color:#94a3b8; font-size:12px; margin:7px 0 12px; }
.follow-grid { display:flex; flex-wrap:wrap; gap:8px; margin:12px 0; }
@media (max-width:900px){ .team-photo-content h1{font-size:28px}.team-photo-content{left:22px;right:22px;bottom:22px}.team-photo-hero{aspect-ratio:4/3;background-size:cover;} }
.provider-grid { display:grid; grid-template-columns: repeat(3,1fr); gap:10px; margin: 10px 0 18px; }
.provider-card { background:rgba(15,23,42,.72); border:1px solid rgba(255,255,255,.08); border-radius:14px; padding:12px 14px; }
.provider-name { color:#e2e8f0; font-size:13px; font-weight:700; }
.provider-status { color:#34d399; font-size:11px; margin-top:4px; }
.chat-user { margin:14px 0 10px auto; max-width:80%; background:linear-gradient(135deg,#2563eb,#7c3aed); color:white; padding:14px 16px; border-radius:18px 18px 4px 18px; line-height:1.55; }
.chat-ai { margin:10px auto 16px 0; max-width:92%; background:rgba(15,23,42,.78); border:1px solid rgba(125,211,252,.18); padding:16px 18px; border-radius:18px 18px 18px 4px; }
.context-chip { display:inline-block; padding:7px 12px; border-radius:999px; background:rgba(56,189,248,.10); border:1px solid rgba(56,189,248,.25); color:#7dd3fc; font-size:12px; font-weight:700; margin:0 8px 8px 0; }
@media (max-width: 900px) { .provider-grid { grid-template-columns: 1fr; } }


/* ─────────────────────────────────────────────────────────────────────
   V25 DESIGN SYSTEM
   No emoji, compact sidebar, page-specific interface identities.
   ───────────────────────────────────────────────────────────────────── */
html, body, [class*="css"] {
    font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont,
                 "Segoe UI", sans-serif;
}
h1, h2, h3, .page-title, .sec-title {
    font-family: Manrope, Inter, ui-sans-serif, system-ui, sans-serif;
}
code, pre, [data-testid="stCodeBlock"] {
    font-family: "SFMono-Regular", Consolas, "Liberation Mono", monospace;
}

/* ── SIDEBAR — Tower night photo background, ultra-clean ── */
[data-testid="stSidebar"] {
    background-color: #020810;
    border-right: 1px solid rgba(148,163,184,.08);
    position: relative;
    overflow: hidden;
}
/* Tower photo injected via JS below */
[data-testid="stSidebar"] > div:first-child {
    padding-top: 0 !important;
    position: relative;
    z-index: 2;
}
/* Nav buttons — ghost style, left-aligned */
[data-testid="stSidebar"] .stButton > button {
    min-height: 40px !important;
    border-radius: 10px !important;
    justify-content: flex-start !important;
    padding: .52rem .82rem !important;
    background: rgba(8,14,26,.55) !important;
    border: 1px solid rgba(255,255,255,.06) !important;
    box-shadow: none !important;
    color: rgba(203,213,225,.85) !important;
    font-weight: 500 !important;
    font-size: 13.5px !important;
    letter-spacing: .01em;
    backdrop-filter: blur(6px);
    transition: background .15s ease, border-color .15s ease, color .15s ease, transform .12s ease;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(56,189,248,.12) !important;
    border-color: rgba(56,189,248,.28) !important;
    color: #e0f2fe !important;
    transform: translateX(3px);
}
[data-testid="stSidebar"] .stButton > button:active {
    background: rgba(56,189,248,.22) !important;
}
/* Hide default Streamlit widget labels inside sidebar */
[data-testid="stSidebar"] label { display: none !important; }
[data-testid="stSidebar"] .stTextInput input {
    background: rgba(8,14,26,.7) !important;
    border: 1px solid rgba(255,255,255,.10) !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
    font-size: 13px !important;
    padding: .45rem .72rem !important;
    backdrop-filter: blur(8px);
}
[data-testid="stSidebar"] .stTextInput input::placeholder { color: #4a5568 !important; }
[data-testid="stSidebar"] .stTextInput input:focus {
    border-color: rgba(56,189,248,.40) !important;
    box-shadow: 0 0 0 2px rgba(56,189,248,.12) !important;
}
/* Hide Streamlit's toggle label clutter */
[data-testid="stSidebar"] .stToggle { display: none !important; }
/* Version caption */
[data-testid="stSidebar"] .stCaptionContainer { opacity: .35; }

/* Nav section labels */
.nav-label {
    margin: 1.1rem 0 .3rem .04rem;
    color: rgba(100,116,139,.75) !important;
    font-size: 9.5px !important;
    letter-spacing: .2em;
    font-weight: 800;
    text-transform: uppercase;
}

/* Sidebar top branding panel — sits above the photo */
.sb-brand {
    padding: 22px 16px 14px;
    background: linear-gradient(180deg, rgba(2,8,16,.96) 0%, rgba(2,8,16,.70) 100%);
    border-bottom: 1px solid rgba(255,255,255,.06);
    margin-bottom: 4px;
}
.sb-brand-name {
    font-size: 22px;
    font-weight: 800;
    color: #fff;
    letter-spacing: -.02em;
    line-height: 1.1;
}
.sb-brand-tag {
    font-size: 11px;
    color: rgba(56,189,248,.70);
    letter-spacing: .05em;
    margin-top: 2px;
    font-weight: 500;
}

/* Student identity chip */
.sb-student-chip {
    display: flex;
    align-items: center;
    gap: 9px;
    background: rgba(8,14,26,.72);
    border: 1px solid rgba(56,189,248,.15);
    border-radius: 12px;
    padding: 9px 12px;
    margin: 6px 0 4px;
    backdrop-filter: blur(10px);
}
.sb-student-name { color: #f8fafc; font-weight: 700; font-size: 13.5px; }
.sb-student-sub  { color: #64748b; font-size: 11px; margin-top: 2px; }
.sb-dot { width: 8px; height: 8px; border-radius: 50%; background: #22d3ee; flex-shrink: 0; box-shadow: 0 0 6px rgba(34,211,238,.5); }

/* Unread badge */
.sb-badge {
    display: inline-block;
    background: rgba(239,68,68,.85);
    color: #fff;
    font-size: 10px;
    font-weight: 800;
    border-radius: 20px;
    padding: 1px 7px;
    margin-left: 6px;
    vertical-align: middle;
}

/* Sidebar bottom status pill */
.sb-status {
    margin: 12px 0 8px;
    padding: 10px 12px;
    border-radius: 12px;
    background: rgba(6,182,212,.06);
    border: 1px solid rgba(6,182,212,.14);
    backdrop-filter: blur(8px);
}
.sb-status-dot { display:inline-block; width:7px; height:7px; border-radius:50%; background:#10b981; margin-right:7px; box-shadow: 0 0 5px rgba(16,185,129,.6); }
.sb-status-text { color: rgba(167,243,208,.7); font-size: 11.5px; font-weight: 600; }

/* Sidebar nav area padding */
.sb-nav-wrap { padding: 0 10px 12px; }

/* reusable unique page header */
.page-intro {
    position: relative;
    overflow: hidden;
    border-radius: 26px;
    padding: 30px 34px;
    margin: 4px 0 24px;
    border: 1px solid var(--page-border);
    background:
        linear-gradient(120deg, var(--page-bg-a), var(--page-bg-b)),
        #0b1220;
    box-shadow: 0 22px 60px rgba(0,0,0,.26);
}
.page-intro::after {
    content: "";
    position: absolute; width: 260px; height: 260px; right:-90px; top:-125px;
    border-radius: 50%; background: var(--page-glow); filter: blur(4px);
}
.page-kicker {
    color: var(--page-accent); font-size: 11px; font-weight: 800;
    text-transform: uppercase; letter-spacing: .15em; margin-bottom: 10px;
}
.page-title {
    position: relative; z-index: 1; color:#f8fafc; font-size: 34px;
    line-height:1.12; letter-spacing:-.035em; font-weight:800; margin:0;
}
.page-subtitle {
    position:relative; z-index:1; max-width:760px; color:#9fb0c6;
    font-size:14px; line-height:1.7; margin-top:10px;
}
.theme-ai       { --page-accent:#c4b5fd; --page-border:rgba(139,92,246,.28); --page-bg-a:rgba(76,29,149,.32); --page-bg-b:rgba(15,23,42,.88); --page-glow:rgba(139,92,246,.18); }
.theme-homework { --page-accent:#fbbf24; --page-border:rgba(245,158,11,.25); --page-bg-a:rgba(120,53,15,.26); --page-bg-b:rgba(15,23,42,.9); --page-glow:rgba(245,158,11,.13); }
.theme-teacher  { --page-accent:#67e8f9; --page-border:rgba(6,182,212,.24); --page-bg-a:rgba(8,47,73,.52); --page-bg-b:rgba(15,23,42,.9); --page-glow:rgba(6,182,212,.14); }
.theme-evidence { --page-accent:#86efac; --page-border:rgba(34,197,94,.25); --page-bg-a:rgba(5,46,22,.48); --page-bg-b:rgba(8,15,27,.95); --page-glow:rgba(34,197,94,.13); }
.theme-defense  { --page-accent:#bfdbfe; --page-border:rgba(96,165,250,.25); --page-bg-a:rgba(30,58,138,.30); --page-bg-b:rgba(15,23,42,.93); --page-glow:rgba(59,130,246,.15); }
.theme-demo     { --page-accent:#fdba74; --page-border:rgba(249,115,22,.24); --page-bg-a:rgba(124,45,18,.28); --page-bg-b:rgba(15,23,42,.92); --page-glow:rgba(249,115,22,.12); }
.theme-roadmap  { --page-accent:#e9d5ff; --page-border:rgba(168,85,247,.24); --page-bg-a:rgba(88,28,135,.30); --page-bg-b:rgba(15,23,42,.92); --page-glow:rgba(168,85,247,.14); }

/* distinct workspace panels */
.assignment-card {
    border:1px solid rgba(245,158,11,.21);
    background:linear-gradient(145deg,rgba(41,30,14,.72),rgba(12,18,29,.92));
    border-radius:20px;padding:20px 22px;margin:12px 0;
}
.analytics-panel {
    border:1px solid rgba(6,182,212,.18);
    background:linear-gradient(145deg,rgba(8,47,73,.34),rgba(11,18,32,.94));
    border-radius:20px;padding:18px;
}
.lab-panel {
    border:1px solid rgba(34,197,94,.18);
    background:#07110d;border-radius:18px;padding:18px;
    box-shadow:inset 0 0 35px rgba(34,197,94,.025);
}
.defense-panel {
    border:1px solid rgba(96,165,250,.20);
    background:linear-gradient(155deg,rgba(30,58,138,.20),rgba(15,23,42,.92));
    border-radius:20px;padding:20px;
}

/* AI chat: real conversation layout */
.ai-chat-shell {
    max-width: 940px; margin: 0 auto; border:1px solid rgba(139,92,246,.18);
    background:linear-gradient(160deg,rgba(24,18,46,.78),rgba(8,14,25,.95));
    border-radius:24px;padding:18px 20px 22px;
}
.chat-user {
    width:fit-content; max-width:78%; margin:18px 0 10px auto !important;
    background:linear-gradient(135deg,#4f46e5,#7c3aed) !important;
    border:0 !important; border-radius:20px 20px 5px 20px !important;
    padding:13px 16px !important; color:white !important;
}
.ai-meta { color:#7d8ca5 !important; font-size:11px !important; margin:0 0 6px 5px !important; }
.ai-main-answer {
    max-width:92%; border:1px solid rgba(167,139,250,.18) !important;
    border-radius:5px 20px 20px 20px !important;
    background:rgba(17,24,39,.88) !important; padding:18px 20px !important;
    color:#dbe4f0 !important; font-size:15px !important; line-height:1.82 !important;
    white-space:pre-wrap;
}
.context-chip { background:rgba(139,92,246,.08) !important; border-color:rgba(167,139,250,.20) !important; }

/* premium team background hero; keeps full 16:9 composition */
.team-photo-hero {
    min-height: 500px !important;
    background-size: cover !important;
    background-position: center center !important;
    border-radius: 28px !important;
    border: 1px solid rgba(148,163,184,.18) !important;
    box-shadow: 0 30px 80px rgba(0,0,0,.42) !important;
}
.team-photo-hero::before {
    background:
        linear-gradient(90deg, rgba(2,6,23,.88) 0%, rgba(2,6,23,.52) 42%, rgba(2,6,23,.12) 72%, rgba(2,6,23,.18) 100%),
        linear-gradient(0deg, rgba(2,6,23,.62), transparent 52%) !important;
}
.team-photo-content { max-width: 575px !important; padding: 44px !important; }
.team-photo-content h1 { font-size: 38px !important; line-height:1.12 !important; }

/* reduce repeated oversized visual language */
.stButton > button {
    border-radius: 12px;
    font-weight: 650;
}
@media (max-width: 850px) {
    .page-intro { padding:24px 22px; border-radius:20px; }
    .page-title { font-size:28px; }
    .team-photo-hero { min-height:420px !important; background-position:center center !important; }
    .team-photo-content { padding:26px !important; }
}

/* Sidebar expander (collapsible sections) */
[data-testid="stSidebar"] [data-testid="stExpander"] {
    border: none !important;
    background: transparent !important;
}
[data-testid="stSidebar"] [data-testid="stExpander"] summary {
    padding: 8px 4px !important;
    font-size: 9.5px !important;
    font-weight: 800 !important;
    color: rgba(100,116,139,.75) !important;
    letter-spacing: .18em !important;
    text-transform: uppercase !important;
    border-radius: 8px !important;
    border: none !important;
    background: transparent !important;
}
[data-testid="stSidebar"] [data-testid="stExpander"] summary:hover {
    color: rgba(148,163,184,.95) !important;
    background: rgba(255,255,255,.03) !important;
}
[data-testid="stSidebar"] [data-testid="stExpander"] summary svg {
    color: rgba(100,116,139,.55) !important;
}
[data-testid="stSidebar"] [data-testid="stExpander"] > div:last-child {
    padding: 0 !important;
    border: none !important;
}

</style>
"""
st.markdown(CSS, unsafe_allow_html=True)


# Session state helpers and shared utilities used across all pages

def init_state():
    st.session_state.setdefault("logged_in", False)
    st.session_state.setdefault("user_role", "")
    st.session_state.setdefault("username", "")
    st.session_state.setdefault("student", "")
    st.session_state.setdefault("topic", "Quantum Mechanics")
    st.session_state.setdefault("persona", "Normal Mode")
    st.session_state.setdefault("tutor_history", [])
    st.session_state.setdefault("score_history", [])
    st.session_state.setdefault("mission_started", False)
    st.session_state.setdefault("mission_step", 0)
    st.session_state.setdefault("practice_reflection", "")
    st.session_state.setdefault("homework_result", None)
    st.session_state.setdefault("selected_homework_id", None)
    st.session_state.setdefault("ai_context_note", "")
    seed_homework_demo()


def reset_session():
    keys = [
        "student", "topic", "persona", "use_wiki", "pack", "brief",
        "questions", "quiz_result", "latest_session", "tutor_history",
        "score_history", "class_questions", "mission_started",
        "mission_step", "practice_reflection", "homework_result",
        "selected_homework_id", "ai_context_note",
    ]
    for key in keys:
        st.session_state.pop(key, None)


def logout():
    """Clear all session state including login."""
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()


def _nav_button(label: str, page_name: str, badge: str = "",
                _in_expander: bool = False) -> None:
    # Render a nav button. Inside a sidebar expander use st.button so the item
    # stays inside the collapsed section. Outside use st.sidebar.button.
    display = f"{label}  {badge}".rstrip() if badge else label
    active = st.session_state.get("active_page") == page_name
    btn_type = "primary" if active else "secondary"
    btn_fn = st.button if _in_expander else st.sidebar.button
    if btn_fn(display, key=f"nav_{page_name}",
              use_container_width=True, type=btn_type):
        st.session_state.active_page = page_name
        st.rerun()


def sidebar():
    st.session_state.setdefault("active_page", "Home")

    # Tower photo — more visible gradient so photo shows through
    if SIDEBAR_URI:
        st.sidebar.markdown(
            f"<style>"
            f"[data-testid='stSidebar'] > div:first-child {{"
            f"  background: linear-gradient(180deg,"
            f"    rgba(2,8,16,.90) 0%,"
            f"    rgba(2,8,16,.52) 38%,"
            f"    rgba(2,8,16,.72) 68%,"
            f"    rgba(2,8,16,.92) 100%),"
            f"    url('{SIDEBAR_URI}') center 20% / cover no-repeat !important;"
            f"}}"
            f"</style>",
            unsafe_allow_html=True,
        )

    # Branding
    st.sidebar.markdown(
        "<div class='sb-brand'>"
        "<div class='sb-brand-name'>Preluma</div>"
        "<div class='sb-brand-tag'>Light Up Before Class</div>"
        "</div>",
        unsafe_allow_html=True,
    )

    # Logged-in user chip
    st.sidebar.markdown("<div class='sb-nav-wrap'>", unsafe_allow_html=True)

    current_student = st.session_state.get("student", "")
    display_name    = current_student if current_student else "Guest"
    user_role       = st.session_state.get("user_role", "student")
    unread_count    = len(notifications_for_student(display_name, unread_only=True))

    role_color  = "#67e8f9" if user_role == "teacher" else "#86efac"
    role_label  = "TEACHER" if user_role == "teacher" else "STUDENT"
    badge_html  = f"<span class='sb-badge'>{unread_count}</span>" if unread_count else ""

    st.sidebar.markdown(
        f"<div style='padding:10px 4px 8px;'>"
        f"  <div style='display:flex;align-items:center;gap:8px;'>"
        f"    <span class='sb-dot'></span>"
        f"    <span style='font-size:13px;color:#e2e8f0;font-weight:700;flex:1;'>{current_student}</span>"
        f"    {badge_html}"
        f"  </div>"
        f"  <div style='font-size:10px;color:{role_color};font-weight:800;letter-spacing:.1em;"
        f"              margin-top:3px;padding-left:15px;'>{role_label}</div>"
        f"</div>",
        unsafe_allow_html=True,
    )

    # Collapsible nav sections — role-based
    current_page = st.session_state.get("active_page", "Home")
    learn_pages   = {"Student Mission", "My Homework", "Ask Preluma AI"}
    teach_pages   = {"Teacher Profile", "Teacher Studio", "Homework Center"}
    project_pages = {"Evidence Board", "Professor Defense", "Project Team", "Demo Guide", "Future Roadmap"}

    hw_badge = f" [{unread_count}]" if unread_count else ""
    _role    = st.session_state.get("user_role", "student")

    # Home always visible
    _nav_button("Home", "Home")

    if _role == "student":
        with st.sidebar.expander("LEARN", expanded=(current_page in learn_pages)):
            _nav_button("Student Mission", "Student Mission", _in_expander=True)
            _nav_button(f"My Homework{hw_badge}", "My Homework", _in_expander=True)
            _nav_button("Ask Preluma AI", "Ask Preluma AI", _in_expander=True)

    if _role == "teacher":
        with st.sidebar.expander("TEACH", expanded=(current_page in teach_pages)):
            _nav_button("Teacher Profile", "Teacher Profile", _in_expander=True)
            _nav_button("Teacher Studio", "Teacher Studio", _in_expander=True)
            _nav_button("Homework Center", "Homework Center", _in_expander=True)

    with st.sidebar.expander("PROJECT", expanded=(current_page in project_pages)):
        _nav_button("Evidence Board", "Evidence Board", _in_expander=True)
        _nav_button("Professor Defense", "Professor Defense", _in_expander=True)
        _nav_button("Project Team", "Project Team", _in_expander=True)
        if _role == "student":
            _nav_button("Demo Guide", "Demo Guide", _in_expander=True)
            _nav_button("Future Roadmap", "Future Roadmap", _in_expander=True)

    # Logout button at bottom
    st.sidebar.markdown("<div style='margin-top:8px;'>", unsafe_allow_html=True)
    if st.sidebar.button("Log Out", key="logout_btn", use_container_width=True, type="secondary"):
        logout()
    st.sidebar.markdown("</div>", unsafe_allow_html=True)

    # AI status pill
    _prov = _provider()
    _has_key = llm_available()
    _ai_label  = f"AI: {_prov}" if _has_key else "Add API Key"
    _dot_color = "#10b981" if _has_key else "#f59e0b"
    _txt_color = "rgba(167,243,208,.8)" if _has_key else "rgba(253,230,138,.8)"
    _border    = "rgba(16,185,129,.18)" if _has_key else "rgba(245,158,11,.18)"
    _bg        = "rgba(6,182,212,.06)" if _has_key else "rgba(120,53,15,.12)"
    st.sidebar.markdown(
        f"<div style='margin:14px 0 8px;padding:10px 12px;border-radius:12px;"
        f"background:{_bg};border:1px solid {_border};backdrop-filter:blur(8px);'>"
        f"<span style='display:inline-block;width:7px;height:7px;border-radius:50%;"
        f"background:{_dot_color};margin-right:7px;box-shadow:0 0 5px {_dot_color};'></span>"
        f"<span style='color:{_txt_color};font-size:11.5px;font-weight:600;'>{_ai_label}</span>"
        f"</div>",
        unsafe_allow_html=True,
    )

    st.sidebar.markdown("</div>", unsafe_allow_html=True)  # close sb-nav-wrap

    st.sidebar.caption(f"v{APP_VERSION}")
    return st.session_state.active_page, True  # presentation always True


# Home page shown to all users on first load

def home_page():
    """Gorgeous Home page — the first thing teacher and students see."""
    provider = _provider()
    ai_label = provider.upper() if provider and provider != "none" else "AI"
    student  = st.session_state.get("student", "") or "Guest"
    bg_hero  = (
        f"url('{CAMPUS_URI}')"
        if CAMPUS_URI
        else "linear-gradient(135deg,#020617 0%,#0f172a 50%,#1e1b4b 100%)"
    )

    # Full-width hero
    st.markdown(f"""
    <style>
    @keyframes glow-pulse {{
      0%,100% {{ opacity:.55; transform:scale(1); }}
      50%      {{ opacity:.80; transform:scale(1.06); }}
    }}
    @keyframes float-up {{
      from {{ opacity:0; transform:translateY(18px); }}
      to   {{ opacity:1; transform:translateY(0); }}
    }}
    .hp-hero {{
      position:relative; overflow:hidden;
      min-height:560px;
      background:{bg_hero};
      background-size:cover; background-position:center 15%;
      box-shadow:0 40px 100px rgba(0,0,0,.60);
      margin-left:-2.5rem; margin-right:-2.5rem; margin-top:-1.5rem;
      margin-bottom:0; border-radius:0;
    }}
    .hp-overlay {{
      position:absolute; inset:0;
      background:
        linear-gradient(110deg, rgba(2,6,23,.94) 0%, rgba(4,10,28,.88) 28%,
                        rgba(8,16,40,.48) 50%, rgba(8,14,32,.12) 70%, transparent 88%),
        radial-gradient(ellipse at 12% 60%, rgba(56,189,248,.14) 0%, transparent 46%),
        linear-gradient(to top, rgba(2,6,23,1) 0%, rgba(2,6,23,.72) 10%, transparent 24%);
    }}
    .hp-glow {{
      position:absolute; right:-120px; top:-80px;
      width:480px; height:480px; border-radius:50%;
      background:radial-gradient(circle, rgba(99,102,241,.28) 0%, transparent 68%);
      animation:glow-pulse 5s ease-in-out infinite;
    }}
    .hp-glow2 {{
      position:absolute; left:-60px; bottom:-100px;
      width:340px; height:340px; border-radius:50%;
      background:radial-gradient(circle, rgba(14,165,233,.18) 0%, transparent 65%);
      animation:glow-pulse 7s ease-in-out infinite reverse;
    }}
    .hp-content {{
      position:relative; z-index:2; padding:52px 52px 48px;
      animation:float-up .6s ease both;
    }}
    .hp-badge {{
      display:inline-flex; align-items:center; gap:7px;
      background:rgba(56,189,248,.10); border:1px solid rgba(56,189,248,.28);
      border-radius:30px; padding:6px 16px; margin-bottom:22px;
    }}
    .hp-badge-dot {{
      width:7px; height:7px; border-radius:50%; background:#38bdf8;
      box-shadow:0 0 8px rgba(56,189,248,.8);
    }}
    .hp-badge-txt {{
      color:#7dd3fc; font-size:12px; font-weight:700; letter-spacing:.07em;
      text-transform:uppercase;
    }}
    .hp-h1 {{
      font-size:clamp(30px,3.8vw,54px); font-weight:900; color:#f8fafc;
      margin:0 0 18px; line-height:1.10; letter-spacing:-.03em;
      text-shadow:0 4px 30px rgba(0,0,0,.50);
    }}
    .hp-h1 span {{ color:#38bdf8; }}
    .hp-sub {{
      font-size:17px; color:#94a3b8; line-height:1.65;
      max-width:580px; margin-bottom:36px;
    }}
    .hp-cta-row {{ display:flex; gap:14px; flex-wrap:wrap; }}
    .hp-cta-primary {{
      background:linear-gradient(135deg,#0ea5e9 0%,#6366f1 100%);
      border-radius:14px; padding:14px 32px;
      font-weight:800; font-size:15px; color:#fff;
      box-shadow:0 8px 28px rgba(99,102,241,.38);
      letter-spacing:.01em;
    }}
    .hp-cta-ghost {{
      background:rgba(255,255,255,.06); border:1px solid rgba(255,255,255,.14);
      border-radius:14px; padding:14px 26px;
      font-weight:600; font-size:15px; color:#cbd5e1;
    }}
    </style>
    <div class='hp-hero'>
      <div class='hp-overlay'></div>
      <div class='hp-glow'></div>
      <div class='hp-glow2'></div>
      <div class='hp-content'>
        <div class='hp-badge'>
          <span class='hp-badge-dot'></span>
          <span class='hp-badge-txt'>{ai_label} Powered &nbsp;&bull;&nbsp; Yunnan University</span>
        </div>
        <h1 class='hp-h1'>
          Prepare before class.<br>
          <span>Understand more during class.</span>
        </h1>
        <p class='hp-sub'>
          Preluma is an AI-powered pre-class learning system for university students.
          Brain Brief, adaptive quiz, multi-provider AI tutor, and teacher analytics —
          all in one Python app.
        </p>
        <div class='hp-cta-row'>
          <div class='hp-cta-primary'>Start Learning Mission</div>
          <div class='hp-cta-ghost'>Ask Preluma AI</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Full page background wrapper — keeps the entire page cohesive
    st.markdown("""
    <style>
    .stApp { background: #020817 !important; }
    .stMainBlockContainer { background: transparent !important; }
    </style>
    <div style="
        position:fixed; inset:0; z-index:-1;
        background:
            radial-gradient(ellipse at 20% 50%, rgba(56,189,248,.055) 0%, transparent 55%),
            radial-gradient(ellipse at 80% 80%, rgba(99,102,241,.055) 0%, transparent 50%),
            #020817;
    "></div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
    # Stats row
    stats = [("28", "AI Topics", "#38bdf8"), ("5", "Mission Steps", "#818cf8"),
             ("3+", "Algorithms", "#34d399"), ("6+", "AI Providers", "#fb923c")]
    sc = st.columns(4)
    for col, (num, lbl, color) in zip(sc, stats):
        col.markdown(f"""
        <div style="
          background:linear-gradient(145deg,rgba(15,23,42,.88),rgba(8,14,28,.96));
          border:1px solid rgba(255,255,255,.07); border-radius:20px;
          padding:24px 16px; text-align:center;
          box-shadow:0 8px 32px rgba(0,0,0,.40);
          transition: border-color .2s;
        ">
          <div style="font-size:38px;font-weight:900;color:{color};
            text-shadow:0 0 22px {color}55;letter-spacing:-.02em;">{num}</div>
          <div style="font-size:10px;color:#334155;margin-top:7px;font-weight:800;
            letter-spacing:.10em;text-transform:uppercase;">{lbl}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:36px'></div>", unsafe_allow_html=True)

    # Feature cards
    st.markdown("""
    <div style="display:flex;align-items:center;gap:12px;margin-bottom:18px;">
      <div style="width:4px;height:28px;border-radius:4px;
        background:linear-gradient(180deg,#38bdf8,#818cf8);"></div>
      <h2 style="margin:0;color:#f8fafc;font-size:22px;font-weight:800;
        letter-spacing:-.02em;">Everything in one platform</h2>
    </div>
    """, unsafe_allow_html=True)

    feature_data = [
        ("linear-gradient(135deg,#0ea5e9,#0369a1)", "01", "Student Mission",
         "5-step AI-guided preparation: Brain Brief, real examples, practice, mock test, and class-ready overview."),
        ("linear-gradient(135deg,#6366f1,#4338ca)", "02", "Ask Preluma AI",
         "Multi-provider AI tutor with adaptive teaching style — child mode, exam mode, deep explanation, and more."),
        ("linear-gradient(135deg,#10b981,#047857)", "03", "My Homework",
         "View and complete teacher-assigned homework. Instant AI grading, mistake capture, and focused review."),
        ("linear-gradient(135deg,#f59e0b,#b45309)", "04", "Teacher Studio",
         "Manual Merge Sort, Binary Search, and Linear Search — live nanosecond timing, CSV proof, audit log."),
        ("linear-gradient(135deg,#ec4899,#9d174d)", "05", "Homework Center",
         "Publish assignments to the class, monitor submissions, and review class-wide weak concepts."),
        ("linear-gradient(135deg,#8b5cf6,#5b21b6)", "06", "Evidence Board",
         "Algorithm proof file, CSV persistence proof, Python module log, and 13-concept evidence table."),
    ]

    c1, c2, c3 = st.columns(3)
    cols = [c1, c2, c3]
    for i, (grad, num, title, desc) in enumerate(feature_data):
        cols[i % 3].markdown(f"""
        <div style="
          background: linear-gradient(145deg, rgba(10,17,36,.95), rgba(8,13,26,.98));
          border: 1px solid rgba(255,255,255,.07);
          border-top: 1px solid rgba(255,255,255,.14);
          border-radius: 20px; padding: 24px 22px; margin-bottom: 14px;
          box-shadow: 0 4px 24px rgba(0,0,0,.35), inset 0 1px 0 rgba(255,255,255,.04);
          position: relative; overflow: hidden;
        ">
          <div style="
            position:absolute; top:-20px; right:-20px; width:80px; height:80px;
            border-radius:50%; background:{grad}; opacity:.07; filter:blur(20px);
          "></div>
          <div style="
            display:inline-flex; align-items:center; justify-content:center;
            width:40px; height:40px; border-radius:12px;
            background:{grad};
            font-size:12px; font-weight:900; color:#fff; margin-bottom:16px;
            box-shadow: 0 4px 16px rgba(0,0,0,.28);
          ">{num}</div>
          <div style="font-size:15px;font-weight:800;color:#e2e8f0;
            margin-bottom:8px;letter-spacing:-.015em;">{title}</div>
          <div style="font-size:13px;color:#475569;line-height:1.65;">{desc}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)

    # "How it works" strip
    st.markdown("""
    <div style="
      background:linear-gradient(135deg,rgba(14,165,233,.08),rgba(99,102,241,.06));
      border:1px solid rgba(56,189,248,.12); border-radius:20px;
      padding:28px 28px 24px; margin-bottom:28px;
    ">
      <div style="font-size:13px;font-weight:800;color:#38bdf8;letter-spacing:.12em;
        text-transform:uppercase;margin-bottom:16px;">How Preluma Works</div>
      <div style="display:flex;gap:0;overflow:hidden;">
        <div style="flex:1;padding:0 16px 0 0;border-right:1px solid rgba(255,255,255,.06);">
          <div style="font-size:11px;font-weight:800;color:#6366f1;letter-spacing:.08em;
            text-transform:uppercase;margin-bottom:6px;">Step 1</div>
          <div style="font-size:14px;font-weight:700;color:#e2e8f0;margin-bottom:4px;">
            Choose Topic</div>
          <div style="font-size:12px;color:#64748b;line-height:1.55;">
            Pick your next lecture topic from 18 curated options or type your own.</div>
        </div>
        <div style="flex:1;padding:0 16px;border-right:1px solid rgba(255,255,255,.06);">
          <div style="font-size:11px;font-weight:800;color:#0ea5e9;letter-spacing:.08em;
            text-transform:uppercase;margin-bottom:6px;">Step 2</div>
          <div style="font-size:14px;font-weight:700;color:#e2e8f0;margin-bottom:4px;">
            Brain Brief</div>
          <div style="font-size:12px;color:#64748b;line-height:1.55;">
            AI builds a 2-minute primer with Wikipedia data and concept breakdown.</div>
        </div>
        <div style="flex:1;padding:0 16px;border-right:1px solid rgba(255,255,255,.06);">
          <div style="font-size:11px;font-weight:800;color:#10b981;letter-spacing:.08em;
            text-transform:uppercase;margin-bottom:6px;">Step 3</div>
          <div style="font-size:14px;font-weight:700;color:#e2e8f0;margin-bottom:4px;">
            Quiz + Practice</div>
          <div style="font-size:12px;color:#64748b;line-height:1.55;">
            Adaptive questions test each skill. Wrong answers trigger focused review.</div>
        </div>
        <div style="flex:1;padding:0 0 0 16px;">
          <div style="font-size:11px;font-weight:800;color:#f59e0b;letter-spacing:.08em;
            text-transform:uppercase;margin-bottom:6px;">Step 4</div>
          <div style="font-size:14px;font-weight:700;color:#e2e8f0;margin-bottom:4px;">
            AI Tutor + Class Ready</div>
          <div style="font-size:12px;color:#64748b;line-height:1.55;">
            Ask anything. Get smart class questions you are actually ready to ask.</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Quick-start buttons (real Streamlit buttons)
    st.markdown(
        "<div style='font-size:13px;font-weight:700;color:#475569;letter-spacing:.10em;"
        "text-transform:uppercase;margin-bottom:12px;'>Jump to</div>",
        unsafe_allow_html=True,
    )
    qs1, qs2, qs3, qs4 = st.columns(4)
    if qs1.button("Student Mission", use_container_width=True, type="primary"):
        st.session_state.active_page = "Student Mission"; st.rerun()
    if qs2.button("Ask Preluma AI", use_container_width=True):
        st.session_state.active_page = "Ask Preluma AI"; st.rerun()
    if qs3.button("My Homework", use_container_width=True):
        st.session_state.active_page = "My Homework"; st.rerun()
    if qs4.button("Teacher Studio", use_container_width=True):
        st.session_state.active_page = "Teacher Studio"; st.rerun()

    # Footer tag
    st.markdown(f"""
    <div style="margin-top:36px;padding:18px 24px;border-radius:14px;
      background:rgba(8,14,26,.60);border:1px solid rgba(255,255,255,.05);
      display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px;">
      <div style="font-size:14px;font-weight:700;color:#334155;">
        Preluma &nbsp;&bull;&nbsp; Yunnan University &nbsp;&bull;&nbsp; Python + Streamlit
      </div>
      <div style="font-size:12px;color:#1e293b;">
        Active student: <span style="color:#38bdf8;font-weight:600;">{student}</span>
        &nbsp;·&nbsp; v{APP_VERSION}
      </div>
    </div>
    """, unsafe_allow_html=True)


# Campus hero banner used on Evidence Board and Professor Defense pages

def hero():
    bg = f"url('{CAMPUS_URI}')" if CAMPUS_URI else "linear-gradient(135deg,#020617,#0f172a,#1e1b4b)"
    provider = _provider()
    ai_pill = f"<span class='ai-pill'>AI: {provider}</span>" if provider != "none" else ""

    st.markdown(f"""
    <div class='hero' style="background-image:{bg};">
      <div class='hero-overlay'></div>
      <div class='hero-content'>
        <div class='hero-top'>
          <div class='logo-mark'>
            <svg viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round">
              <path d="M12 2L2 7l10 5 10-5-10-5z"/><path d="M2 17l10 5 10-5"/><path d="M2 12l10 5 10-5"/>
            </svg>
          </div>
          <div><div class='brand-name'>Preluma</div><div class='brand-tag'>Light Up Before Class</div></div>
          <div class='uni-pill'>Yunnan University</div>
          {ai_pill}
        </div>
        <div class='hero-badge'>Pre-class brain priming system</div>
        <h1>Prepare before class.<br><span>Understand more during class.</span></h1>
        <div class='hero-sub'>Built for Yunnan University students. Preluma turns passive pre-class preparation into a guided, AI-powered learning mission with Brain Brief, Quiz, UltraTutor, and Smart Class Questions.</div>
        <div class='hero-stats'>
          <div><div class='hero-stat-num'>18</div><div class='hero-stat-lbl'>Curated Topics</div></div>
          <div><div class='hero-stat-num'>4</div><div class='hero-stat-lbl'>Skill Checks</div></div>
          <div><div class='hero-stat-num'>AI</div><div class='hero-stat-lbl'>Smart Tutor</div></div>
          <div><div class='hero-stat-num'>CSV</div><div class='hero-stat-lbl'>Data Persistence</div></div>
        </div>
      </div>
    </div>""", unsafe_allow_html=True)


# Progress bar and page header components shared across pages

def page_intro(theme: str, kicker: str, title: str, subtitle: str) -> None:
    """Render a consistent brand header with a page-specific visual identity."""
    st.markdown(
        f"""
        <section class="page-intro theme-{theme}">
            <div class="page-kicker">{kicker}</div>
            <h1 class="page-title">{title}</h1>
            <div class="page-subtitle">{subtitle}</div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def progress_bar():
    has_brief = "brief" in st.session_state
    has_quiz  = "quiz_result" in st.session_state
    has_tutor = bool(st.session_state.get("tutor_history"))
    steps = [
        ("Choose Topic", True,      False),
        ("Brain Brief",  has_brief, not has_brief),
        ("Quiz",         has_quiz,  has_brief and not has_quiz),
        ("UltraTutor",   has_tutor, has_quiz  and not has_tutor),
        ("Class Ready",  has_tutor, False),
    ]
    html = "<div class='progress-wrap'>"
    for label, done, active in steps:
        c = "done" if done else ("active" if active else "")
        prefix = "[v] " if done else ""
        html += f"<div class='progress-step {c}'>{prefix}{label}</div>"
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)

def chip_row():
    labels = ["Topic","Brain Brief","All Concepts","Quiz","Mistake Clinic","UltraTutor","Class Questions","Readiness Score"]
    st.markdown("<div class='chip-row'>" + "".join(f"<span class='chip'>{l}</span>" for l in labels) + "</div>", unsafe_allow_html=True)


# Mission setup form where the student picks a topic and starts preparation

def mission_control():
    st.markdown("""
    <style>
    .mc-banner {
        background: linear-gradient(135deg, rgba(14,165,233,.10) 0%, rgba(99,102,241,.08) 100%);
        border: 1px solid rgba(56,189,248,.16);
        border-radius: 24px; padding: 28px 32px; margin-bottom: 28px;
        position: relative; overflow: hidden;
    }
    .mc-banner-glow {
        position: absolute; right: -60px; top: -60px;
        width: 200px; height: 200px; border-radius: 50%;
        background: radial-gradient(circle, rgba(99,102,241,.22) 0%, transparent 70%);
    }
    .mc-banner-title {
        font-size: 26px; font-weight: 900; color: #f1f5f9;
        margin-bottom: 8px; letter-spacing: -.03em;
    }
    .mc-banner-title span { color: #38bdf8; }
    .mc-banner-sub {
        font-size: 14px; color: #64748b; line-height: 1.60;
    }
    .mc-checklist {
        display: flex; flex-wrap: wrap; gap: 8px; margin-top: 14px;
    }
    .mc-check {
        background: rgba(52,211,153,.08); border: 1px solid rgba(52,211,153,.20);
        border-radius: 20px; padding: 4px 12px;
        font-size: 12px; color: #34d399; font-weight: 600;
    }
    </style>
    <div class="mc-banner">
        <div class="mc-banner-glow"></div>
        <div class="mc-banner-title">Mission Control &nbsp;<span>GO</span></div>
        <div class="mc-banner-sub">
            Set your topic, choose how deep you want to go, and let Preluma AI build
            your complete pre-class learning mission in seconds.
        </div>
        <div class="mc-checklist">
            <span class="mc-check">AI Brain Brief</span>
            <span class="mc-check">All Concepts in Tabs</span>
            <span class="mc-check">Quiz + Skill Check</span>
            <span class="mc-check">Mistake Clinic</span>
            <span class="mc-check">UltraTutor Answers</span>
            <span class="mc-check">Smart Class Questions</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    preset = st.selectbox("Demo preset", ["Manual Input","AI Class Demo","Python Exam Demo","Statistics Viva Demo"], index=0)
    preset_data = {
        "AI Class Demo":        ("Amir",  "Neural Network",      "Tomorrow 9 AM", "Coach Mode",  "Deep Understanding"),
        "Python Exam Demo":     ("Jia",   "Python Programming",  "Tomorrow 9 AM", "Normal Mode", "Exam/Viva Mode"),
        "Statistics Viva Demo": ("Nadia", "Statistics",          "Tomorrow 9 AM", "Coach Mode",  "Exam/Viva Mode"),
    }
    ds, dt, dtime, dp, dm = preset_data.get(preset, (
        st.session_state.student, st.session_state.topic, "Tomorrow 9 AM", st.session_state.persona, "Fast Review"))

    st.markdown("""
    <style>
    /* Mission form — study environment feel */
    div[data-testid="stForm"] {
        background: linear-gradient(145deg, rgba(10,18,38,.96), rgba(6,12,26,.98));
        border: 1px solid rgba(56,189,248,.14);
        border-radius: 24px; padding: 28px 28px 20px; margin-top: 4px;
        box-shadow: 0 8px 40px rgba(0,0,0,.40), inset 0 1px 0 rgba(255,255,255,.04);
    }
    div[data-testid="stTextInput"] input,
    div[data-testid="stSelectbox"] > div {
        background: rgba(15,23,42,.80) !important;
        border: 1px solid rgba(56,189,248,.18) !important;
        border-radius: 12px !important; color: #e2e8f0 !important;
    }
    div[data-testid="stFormSubmitButton"] button {
        background: linear-gradient(135deg, #0ea5e9 0%, #6366f1 100%) !important;
        border: none !important; border-radius: 14px !important;
        font-weight: 800 !important; font-size: 16px !important;
        padding: 14px !important; letter-spacing: .02em !important;
        box-shadow: 0 8px 28px rgba(99,102,241,.38) !important;
        transition: transform .15s !important;
    }
    .mc-section-label {
        font-size: 10px; font-weight: 800; color: #38bdf8;
        letter-spacing: .10em; text-transform: uppercase;
        margin-bottom: 10px; margin-top: 4px;
    }
    </style>
    """, unsafe_allow_html=True)

    with st.form("mission_form", border=False):
        c1, c2, c3 = st.columns([1.4, 1, 0.9])
        with c1:
            st.markdown("<div class='mc-section-label'>Your details</div>", unsafe_allow_html=True)
            student      = st.text_input("Your name", value=ds, placeholder="Enter your name")
            topic_choice = st.selectbox("Lecture topic", TOPIC_OPTIONS,
                index=TOPIC_OPTIONS.index(dt) if dt in TOPIC_OPTIONS else 0)
            topic = st.text_input("Custom topic", placeholder="e.g. Reinforcement Learning") \
                    if topic_choice == "Custom Topic" else topic_choice
            lecture_time = st.text_input("Lecture time", value=dtime)
        with c2:
            st.markdown("<div class='mc-section-label'>Learning style</div>", unsafe_allow_html=True)
            persona       = st.radio("Tutor personality", ["Normal Mode","Coach Mode","Roast Mode"],
                captions=["Clear & direct","Warm & motivating","Funny pressure"],
                index=["Normal Mode","Coach Mode","Roast Mode"].index(dp) if dp in ["Normal Mode","Coach Mode","Roast Mode"] else 0)
            learning_mode = st.selectbox("Learning mode",["Fast Review","Deep Understanding","Exam/Viva Mode"],
                index=["Fast Review","Deep Understanding","Exam/Viva Mode"].index(dm) if dm in ["Fast Review","Deep Understanding","Exam/Viva Mode"] else 0)
        with c3:
            st.markdown("<div class='mc-section-label'>What you will get</div>", unsafe_allow_html=True)
            use_wiki = st.checkbox("Wikipedia real data", value=True)
            for item in [
                ("AI Brain Brief", "#38bdf8"),
                ("All concepts in tabs", "#818cf8"),
                ("Quiz + skill check", "#34d399"),
                ("Mistake clinic", "#f87171"),
                ("UltraTutor answers", "#fb923c"),
                ("Smart class questions", "#a78bfa"),
            ]:
                st.markdown(
                    f"<div style='display:flex;align-items:center;gap:8px;"
                    f"padding:4px 0;border-bottom:1px solid rgba(255,255,255,.04);'>"
                    f"<div style='width:6px;height:6px;border-radius:50%;"
                    f"background:{item[1]};flex-shrink:0;'></div>"
                    f"<span style='font-size:12px;color:#94a3b8;'>{item[0]}</span></div>",
                    unsafe_allow_html=True,
                )
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        start = st.form_submit_button("Start Pre-Class Mission", use_container_width=True)

    if start:
        if not topic or not topic.strip():
            st.warning("Please enter a topic first.")
            return
        with st.spinner("Building your AI-powered learning mission..."):
            pack = build_pack(topic, use_wikipedia=use_wiki)
            brief = build_brain_brief(pack)
            questions = make_questions(pack)
            try:
                from engine import build_enriched_class_questions
                class_qs = build_enriched_class_questions(pack)
            except Exception:
                class_qs = pack.get("class_questions", [])
        st.session_state.update({
            "student": student, "topic": topic, "persona": persona,
            "learning_mode": learning_mode, "use_wiki": use_wiki,
            "pack": pack, "brief": brief, "questions": questions,
            "class_questions": class_qs, "quiz_result": None,
            "latest_session": None, "tutor_history": [],
            "mission_started": True, "mission_step": 1,
            "practice_reflection": "",
        })
        st.rerun()


# Brain Brief
def brain_brief():
    if "brief" not in st.session_state: return
    b    = st.session_state.brief
    pack = st.session_state.pack

    st.markdown("""<div class='sec-head'>
      <div class='sec-icon' style='background:rgba(167,139,250,.12);'>01</div>
      <div><div class='sec-title'>Brain Brief</div><div class='sec-sub'>Your 2-minute primer before class</div></div>
    </div>""", unsafe_allow_html=True)

    mode = st.session_state.get("learning_mode","Fast Review")
    st.caption(f"Learning mode: {mode}")

    if b.get("study_tip"):
        st.markdown(f"<div class='ai-bar'><div class='ai-dot'></div><div class='ai-txt'>Before class: {b['study_tip']}</div></div>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""<div class='card-glass'><div class='albl lbl-blue'>What is it?</div><div class='atxt'>{b['tiny_answer']}</div></div>
        <div class='card-glass'><div class='albl lbl-purple'>Simply put</div><div class='atxt'>{b['simple']}</div></div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class='card-glass'><div class='albl lbl-green'>Real-life example</div><div class='atxt'>{b['example']}</div></div>
        <div class='card-glass'><div class='albl lbl-red'>Common mistake</div><div class='atxt'>{b['misconception']}</div></div>""", unsafe_allow_html=True)

    all_concepts = b.get("all_concepts", {})
    if all_concepts:
        st.markdown("""<div class='sec-head' style='margin-top:1.5rem;'>
          <div class='sec-icon' style='background:rgba(251,191,36,.10);'>BB</div>
          <div><div class='sec-title'>All Key Concepts</div><div class='sec-sub'>Click each tab to explore in depth</div></div>
        </div>""", unsafe_allow_html=True)
        tabs = st.tabs([f"  {n.title()}  " for n in all_concepts])
        for tab, (cname, c) in zip(tabs, all_concepts.items()):
            with tab:
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"""<div class='concept-block'><div class='concept-block-title'>Definition</div><p>{c['definition']}</p></div>
                    <div class='concept-block'><div class='concept-block-title'>In simple words</div><p>{c['kid']}</p></div>""", unsafe_allow_html=True)
                with col2:
                    st.markdown(f"""<div class='concept-block'><div class='concept-block-title'>Real example</div><p>{c['example']}</p></div>
                    <div class='concept-block'><div class='concept-block-title'>Mistake · Exam tip</div><p><b>Mistake:</b> {c['mistake']}</p><p><b>Exam:</b> {c['exam']}</p></div>""", unsafe_allow_html=True)

    with st.expander("Key facts & source"):
        for fact in b.get("facts", []):
            st.markdown(f"<div style='padding:6px 0;color:#cbd5e1;font-size:14px;border-bottom:1px solid rgba(255,255,255,.05);'>→ {fact}</div>", unsafe_allow_html=True)
        if pack.get("source_url"):
            st.success("Real Wikipedia data used.")
            st.write(pack.get("source_url"))


# Quiz
def quiz():
    if "questions" not in st.session_state: return
    st.markdown("""<div class='sec-head'>
      <div class='sec-icon' style='background:rgba(34,211,238,.10);'>EX</div>
      <div><div class='sec-title'>Readiness Quiz</div><div class='sec-sub'>4 questions across 4 skill types — find your weak spots</div></div>
    </div>""", unsafe_allow_html=True)

    skill_colors = {"Definition":"lbl-blue","Core Concept":"lbl-purple","Application":"lbl-green","Misconception":"lbl-orange"}
    with st.form("quiz_form", border=False):
        for i, q in enumerate(st.session_state.questions):
            sc = skill_colors.get(q["skill"],"lbl-blue")
            st.markdown(f"""<div class='card-glass' style='margin-bottom:4px;'>
              <div class='albl {sc}'>{q["skill"]}</div>
              <div style='font-size:15px;color:#f1f5f9;font-weight:600;margin-bottom:12px;'>{q["q"]}</div>
            </div>""", unsafe_allow_html=True)
            st.radio("", q["options"], key=f"quiz_{i}", label_visibility="collapsed")
            st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
        submit = st.form_submit_button("Check My Readiness", use_container_width=True)

    if submit:
        answers = {i: st.session_state.get(f"quiz_{i}","") for i in range(len(st.session_state.questions))}
        result  = grade(st.session_state.questions, answers)
        st.session_state.quiz_result = result
        st.session_state.latest_session = {
            "Student": st.session_state.student, "Topic": st.session_state.pack["title"],
            "Readiness": result["pct"], "Weak Skill": result["weakest"],
        }
        st.session_state.score_history = st.session_state.get("score_history",[])
        st.session_state.score_history.append({"Attempt": len(st.session_state.score_history)+1,
            "Topic": st.session_state.pack["title"], "Score": result["pct"]})
        # Persist to CSV
        append_student_row({
            "Record ID": next_record_id(), "Student": st.session_state.student,
            "Topic": st.session_state.pack["title"], "Readiness": result["pct"],
            "Weak Skill": result["weakest"], "Quiz Score": result["score"],
            "Quiz Total": result["total"], "Lecture Time": st.session_state.get("learning_mode","Fast Review"),
            "Learning Mode": st.session_state.get("learning_mode","Fast Review"), "Created At": timestamp(),
        })
        st.rerun()


# Result
def result_section():
    result = st.session_state.get("quiz_result")
    if not result: return

    pct       = result["pct"]
    pill_cls, color = _rc(pct)
    label     = _rl(pct)

    st.markdown("""<div class='sec-head'>
      <div class='sec-icon' style='background:rgba(52,211,153,.10);'>QZ</div>
      <div><div class='sec-title'>Your Result</div><div class='sec-sub'>Score breakdown and skill analysis</div></div>
    </div>""", unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1,1.6,1])
    with c1:
        st.markdown(f"""<div class='card-glass' style='text-align:center;padding:28px 16px;'>
          <div class='score-big' style='color:{color};'>{pct}%</div>
          <div class='score-lbl'>{result['score']}/{result['total']} correct</div>
          <div class='r-pill {pill_cls}'>{label}</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        rows = build_teacher_dataframe(st.session_state.latest_session)
        avg  = class_average_readiness(rows)
        fig  = go.Figure()
        fig.add_bar(x=["You","Class Avg"], y=[pct, avg], marker_color=[color,"#818cf8"],
                    text=[f"{pct}%",f"{avg}%"], textposition="outside")
        fig.update_layout(height=240, margin=dict(l=10,r=10,t=10,b=10),
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font_color="#94a3b8",
            yaxis=dict(range=[0,110], gridcolor="rgba(255,255,255,.05)"),
            xaxis=dict(gridcolor="rgba(0,0,0,0)"))
        st.plotly_chart(fig, use_container_width=True)
    with c3:
        st.markdown(f"""<div class='card-glass' style='text-align:center;padding:28px 16px;'>
          <div style='font-size:12px;color:#64748b;font-weight:700;margin-bottom:8px;'>WEAKEST SKILL</div>
          <div style='font-size:18px;font-weight:800;color:#f87171;'>{result['weakest']}</div>
          <div style='font-size:12px;color:#475569;margin-top:8px;'>Focus area</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("""<div class='sec-head' style='margin-top:1.5rem;'>
      <div class='sec-icon' style='background:rgba(248,113,113,.10);'>AN</div>
      <div><div class='sec-title'>Mistake Clinic</div><div class='sec-sub'>Every wrong answer explained clearly</div></div>
    </div>""", unsafe_allow_html=True)

    for i, d in enumerate(result["details"], 1):
        ok = d["correct"]
        with st.expander(f"{'[OK]' if ok else '[NO]'} Q{i}: {d['skill']} — {'Correct' if ok else 'Review needed'}"):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"<div style='font-size:13px;color:#64748b;'>Your answer</div><div style='font-size:14px;color:{'#34d399' if ok else '#f87171'};font-weight:600;'>{d['chosen'] or 'No answer'}</div>", unsafe_allow_html=True)
            with col2:
                st.markdown(f"<div style='font-size:13px;color:#64748b;'>Correct answer</div><div style='font-size:14px;color:#34d399;font-weight:600;'>{d['answer']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='margin-top:10px;font-size:14px;color:#cbd5e1;'>{d['why']}</div>", unsafe_allow_html=True)
            if not ok:
                st.info("Fix: read the definition → find one real example → say it in your own words.")

    history = st.session_state.get("score_history",[])
    if len(history) >= 2:
        df_h = pd.DataFrame(history)
        fig2 = px.line(df_h, x="Attempt", y="Score", markers=True, title="Your Readiness Trend", range_y=[0,100])
        fig2.update_traces(line_color="#38bdf8", marker_color="#7c3aed")
        fig2.update_layout(height=260, margin=dict(l=10,r=10,t=40,b=10),
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font_color="#94a3b8")
        st.plotly_chart(fig2, use_container_width=True)


# Smart QnA + UltraTutor
def smart_qna():
    if "pack" not in st.session_state: return

    st.markdown("""<div class='sec-head'>
      <div class='sec-icon' style='background:rgba(99,102,241,.12);'>AI</div>
      <div><div class='sec-title'>UltraTutor</div><div class='sec-sub'>Ask anything — get an answer matched exactly to how you asked</div></div>
    </div>""", unsafe_allow_html=True)

    provider = _provider()
    if provider != "none":
        st.markdown(f"<div class='ai-bar'><div class='ai-dot'></div><div class='ai-txt'>AI active: {provider} — ask simply for simple answers, ask deeply for deep answers</div></div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='notice'>Running on local data. Set GEMINI_API_KEY in Streamlit secrets for AI answers.</div>", unsafe_allow_html=True)

    persona = st.session_state.get("persona","Normal Mode")
    hints = {"Normal Mode":"e.g. What is overfitting?","Coach Mode":"e.g. I'm confused, help me understand","Roast Mode":"e.g. Why does everyone talk about neural networks?"}
    question = st.text_input("", placeholder=hints.get(persona,"Ask any question about this topic..."), key="tutor_q", label_visibility="collapsed")

    col1, col2, col3 = st.columns([2,2,1])
    with col1:
        ask_smart = st.button("Smart Answer (local)", use_container_width=True)
    with col2:
        ask_tutor = st.button("UltraTutor (AI)", use_container_width=True)
    with col3:
        if st.button("Clear", use_container_width=True):
            st.session_state.tutor_history = []; st.rerun()

    if ask_smart and question.strip():
        ans = smart_answer_from_pack(st.session_state.pack, question)
        st.session_state.tutor_history.append({"question": question, "type": "smart", "response": ans})
        st.rerun()

    if ask_tutor and question.strip():
        with st.spinner("Thinking..."):
            s = tutor_sections(st.session_state.pack, question, persona)
        st.session_state.tutor_history.append({"question": question, "type": "tutor", "response": s})
        st.rerun()

    for entry in reversed(st.session_state.get("tutor_history",[])):
        q = entry["question"]
        r = entry["response"]
        t = entry.get("type","tutor")

        if t == "smart":
            st.markdown(f"<div style='margin:16px 0 4px;font-size:16px;font-weight:800;color:#f1f5f9;'>Smart Answer <span style='font-size:12px;color:#475569;margin-left:10px;'>\"{q}\"</span></div>", unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            c1.markdown(f"<div class='card-glass'><div class='albl lbl-blue'>Answer</div><div class='atxt'>{r.get('answer','')}</div></div>", unsafe_allow_html=True)
            c2.markdown(f"<div class='card-glass'><div class='albl lbl-green'>Simple version</div><div class='atxt'>{r.get('simple','')}</div></div>", unsafe_allow_html=True)
            st.markdown(f"<div class='card-glass'><div class='albl lbl-purple'>Example</div><div class='atxt'>{r.get('example','')}</div></div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='margin:16px 0 4px;font-size:16px;font-weight:800;color:#f1f5f9;'>{r.get('concept','')} <span style='font-size:12px;color:#475569;margin-left:10px;'>\"{q}\"</span></div>", unsafe_allow_html=True)
            parts = [("Tiny Answer","lbl-blue",r.get("tiny_answer","")),
                     ("Explain Simply","lbl-purple",r.get("explain_simply","")),
                     ("Real-Life Example","lbl-green",r.get("real_life_example","")),
                     ("Common Mistake","lbl-red",r.get("common_mistake","")),
                     ("Exam Angle","lbl-yellow",r.get("exam_angle",""))]
            c1, c2 = st.columns(2)
            for idx,(title,lbl,text) in enumerate(parts):
                if not text: continue
                (c1 if idx%2==0 else c2).markdown(f"<div class='card-glass'><div class='albl {lbl}'>{title}</div><div class='atxt'>{text}</div></div>", unsafe_allow_html=True)
        st.markdown("<hr style='border-color:rgba(255,255,255,.05);margin:10px 0;'>", unsafe_allow_html=True)


# Class Questions
def class_questions_and_download():
    if "pack" not in st.session_state: return
    st.markdown("""<div class='sec-head'>
      <div class='sec-icon' style='background:rgba(34,211,238,.10);'>QA</div>
      <div><div class='sec-title'>Smart Class Questions</div><div class='sec-sub'>Walk into class with questions that show you prepared</div></div>
    </div>""", unsafe_allow_html=True)

    class_qs = st.session_state.get("class_questions", st.session_state.pack.get("class_questions",[]))
    for i, q in enumerate(class_qs, 1):
        st.markdown(f"<div class='card-glass' style='margin:6px 0;'><span style='color:#38bdf8;font-weight:700;font-size:13px;'>Q{i}</span><span style='color:#e2e8f0;font-size:14px;margin-left:10px;'>{q}</span></div>", unsafe_allow_html=True)

    payload = {"student": st.session_state.student, "topic": st.session_state.pack["title"],
               "brief": st.session_state.brief, "class_questions": class_qs,
               "quiz_result": st.session_state.get("quiz_result"),
               "learning_mode": st.session_state.get("learning_mode","Fast Review")}
    st.download_button("Download Study Brief", data=json.dumps(payload, indent=2),
        file_name=f"preluma_{st.session_state.pack['title'].lower().replace(' ','_')}.json",
        mime="application/json", use_container_width=True)


# How it works
def how_it_works():
    st.markdown("""<div class='kpi-grid'>
      <div class='kpi-card'><div class='kpi-num'>18</div><div class='kpi-lbl'>Curated Topics</div></div>
      <div class='kpi-card'><div class='kpi-num'>4</div><div class='kpi-lbl'>Skill Checks</div></div>
      <div class='kpi-card'><div class='kpi-num'>AI</div><div class='kpi-lbl'>Smart Tutor</div></div>
      <div class='kpi-card'><div class='kpi-num'>CSV</div><div class='kpi-lbl'>Persistent Data</div></div>
    </div>
    <div class='flow-grid'>
      <div class='flow-card'><div class='flow-step'>Step 1</div><div class='flow-title'>Prime the brain</div><div class='flow-desc'>AI Brain Brief with all concepts in tabs before the lecture.</div></div>
      <div class='flow-card'><div class='flow-step'>Step 2</div><div class='flow-title'>Find weak spots</div><div class='flow-desc'>4-question quiz detects exactly which skill needs work.</div></div>
      <div class='flow-card'><div class='flow-step'>Step 3</div><div class='flow-title'>Ask better questions</div><div class='flow-desc'>Leave with AI-generated class questions and a readiness score.</div></div>
    </div>""", unsafe_allow_html=True)


# Student Mission
def _set_mission_step(step: int) -> None:
    st.session_state.mission_step = max(1, min(5, int(step)))
    st.rerun()


def _mission_navigation(previous_step: int | None, next_step: int | None, next_label: str = "Next") -> None:
    left, center, right = st.columns([1, 2, 1])
    with left:
        if previous_step is not None and st.button("← Previous", use_container_width=True):
            _set_mission_step(previous_step)
    with center:
        step = st.session_state.get("mission_step", 1)
        st.progress(step / 5, text=f"Learning mission: Step {step} of 5")
    with right:
        if next_step is not None and st.button(f"{next_label} →", use_container_width=True):
            _set_mission_step(next_step)


def mission_brain_brief_screen() -> None:
    brief = st.session_state.brief
    pack = st.session_state.pack

    st.markdown("""<div class='sec-head'>
      <div class='sec-icon' style='background:rgba(99,102,241,.15);'>01</div>
      <div><div class='sec-title'>Step 1 · Understand the Big Idea</div>
      <div class='sec-sub'>A friendly foundation before examples and practice</div></div>
    </div>""", unsafe_allow_html=True)

    st.markdown(f"""
    <div class='card-glass' style='border-color:rgba(99,102,241,.35);'>
      <div class='albl lbl-blue'>The tiny answer</div>
      <div class='atxt'>{brief.get("tiny_answer", "")}</div>
    </div>
    <div class='card-glass'>
      <div class='albl lbl-purple'>Think of it like this</div>
      <div class='atxt'>{brief.get("simple", "")}</div>
    </div>
    """, unsafe_allow_html=True)

    key_points = brief.get("facts", [])[:3]
    if key_points:
        st.markdown("#### Three things to remember")
        columns = st.columns(len(key_points))
        for column, fact in zip(columns, key_points):
            column.markdown(
                f"<div class='concept-block'><div class='concept-block-title'>Remember</div>"
                f"<p>{fact}</p></div>",
                unsafe_allow_html=True,
            )

    all_concepts = brief.get("all_concepts", {})
    if all_concepts:
        with st.expander("Explore the key concepts"):
            tabs = st.tabs([name.title() for name in all_concepts])
            for tab, (name, concept) in zip(tabs, all_concepts.items()):
                with tab:
                    st.write(concept.get("kid", concept.get("definition", "")))
                    st.caption(f"Exam reminder: {concept.get('exam', '')}")

    if pack.get("source_url"):
        st.caption("Source-supported topic pack is active.")

    _mission_navigation(None, 2, "See a Real Example")


def mission_example_screen() -> None:
    brief = st.session_state.brief
    pack = st.session_state.pack

    st.markdown("""<div class='sec-head'>
      <div class='sec-icon' style='background:rgba(168,85,247,.15);'>02</div>
      <div><div class='sec-title'>Step 2 · See It in Real Life</div>
      <div class='sec-sub'>Turn theory into a picture you can remember</div></div>
    </div>""", unsafe_allow_html=True)

    example = brief.get("example", "")
    misconception = brief.get("misconception", "")
    applications = pack.get("applications", {})

    st.markdown(f"""
    <div class='card-glass' style='border-color:rgba(168,85,247,.35);'>
      <div class='albl lbl-purple'>Imagine this</div>
      <div class='atxt'>{example}</div>
    </div>
    <div class='card-glass'>
      <div class='albl lbl-red'>Do not confuse it with this</div>
      <div class='atxt'>{misconception}</div>
    </div>
    """, unsafe_allow_html=True)

    if applications:
        st.markdown("#### Where this idea is useful")
        cols = st.columns(min(3, len(applications)))
        for index, (name, value) in enumerate(applications.items()):
            cols[index % len(cols)].markdown(
                f"<div class='concept-block'><div class='concept-block-title'>"
                f"{name.title()}</div><p>{value}</p></div>",
                unsafe_allow_html=True,
            )

    st.info("Memory trick: connect the definition to one vivid example before trying to memorize it.")
    _mission_navigation(1, 3, "Try It Yourself")


def mission_practice_screen() -> None:
    brief = st.session_state.brief
    pack = st.session_state.pack
    concept_name = brief.get("key_concept", pack.get("title", "the topic"))

    st.markdown("""<div class='sec-head'>
      <div class='sec-icon' style='background:rgba(245,158,11,.15);'>03</div>
      <div><div class='sec-title'>Step 3 · Practice the Idea</div>
      <div class='sec-sub'>Active thinking makes the idea stay in memory</div></div>
    </div>""", unsafe_allow_html=True)

    st.markdown(f"""
    <div class='card-glass' style='border-color:rgba(245,158,11,.35);'>
      <div class='albl lbl-yellow'>Your challenge</div>
      <div class='atxt'>Explain <b>{concept_name}</b> in your own words, then give one example.</div>
    </div>
    """, unsafe_allow_html=True)

    reflection = st.text_area(
        "Write your explanation",
        value=st.session_state.get("practice_reflection", ""),
        placeholder="Start with: In simple words, this means...",
        height=150,
    )
    st.session_state.practice_reflection = reflection

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Show a gentle hint", use_container_width=True):
            st.info(f"Use this pattern: meaning → why it matters → example. Simple idea: {brief.get('simple', '')}")
    with col2:
        if st.button("Check my thinking", use_container_width=True):
            word_count = len(reflection.split())
            if word_count < 8:
                st.warning("Add a little more: include both the meaning and an example.")
            elif "example" not in reflection.casefold() and "like" not in reflection.casefold():
                st.info("Good start. Add a phrase such as “For example…” to make your explanation stronger.")
            else:
                st.success("Strong practice answer. You explained the idea and connected it to an example.")

    _mission_navigation(2, 4, "Take the Mock Test")


def _save_mission_quiz_result(result: dict) -> None:
    st.session_state.quiz_result = result
    st.session_state.latest_session = {
        "Student": st.session_state.student,
        "Topic": st.session_state.pack["title"],
        "Readiness": result["pct"],
        "Weak Skill": result["weakest"],
    }
    st.session_state.score_history = st.session_state.get("score_history", [])
    st.session_state.score_history.append({
        "Attempt": len(st.session_state.score_history) + 1,
        "Topic": st.session_state.pack["title"],
        "Score": result["pct"],
    })
    append_student_row({
        "Record ID": next_record_id(),
        "Student": st.session_state.student,
        "Topic": st.session_state.pack["title"],
        "Readiness": result["pct"],
        "Weak Skill": result["weakest"],
        "Quiz Score": result["score"],
        "Quiz Total": result["total"],
        "Lecture Time": "Pre-class mission",
        "Learning Mode": st.session_state.get("learning_mode", "Fast Review"),
        "Created At": timestamp(),
    })


def mission_mock_test_screen() -> None:
    st.markdown("""
    <style>
    @keyframes slide-in {
        from { opacity: 0; transform: translateX(28px); }
        to   { opacity: 1; transform: translateX(0); }
    }
    .mock-card {
        animation: slide-in .35s cubic-bezier(.22,.61,.36,1) both;
        background: linear-gradient(145deg, rgba(15,23,42,.90), rgba(8,14,28,.95));
        border: 1px solid rgba(255,255,255,.09); border-radius: 24px;
        padding: 32px 28px; margin-bottom: 20px;
    }
    .mock-skill-tag {
        display: inline-block; padding: 5px 14px; border-radius: 30px;
        font-size: 11px; font-weight: 800; letter-spacing: .09em;
        text-transform: uppercase; margin-bottom: 18px;
        background: rgba(239,68,68,.14); color: #f87171;
        border: 1px solid rgba(239,68,68,.28);
    }
    .mock-question-text {
        font-size: 19px; font-weight: 700; color: #f1f5f9;
        line-height: 1.50; margin-bottom: 28px;
    }
    .mock-progress-dots {
        display: flex; gap: 8px; margin-bottom: 24px;
    }
    .mock-dot {
        width: 34px; height: 6px; border-radius: 4px;
        background: rgba(255,255,255,.10);
    }
    .mock-dot.done   { background: #34d399; }
    .mock-dot.active { background: #38bdf8; }
    .mock-counter {
        font-size: 12px; font-weight: 700; color: #475569;
        letter-spacing: .06em; text-transform: uppercase;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""<div class='sec-head'>
      <div class='sec-icon' style='background:rgba(239,68,68,.15);'>04</div>
      <div><div class='sec-title'>Step 4 · Mini Mock Test</div>
      <div class='sec-sub'>One question at a time — think before you pick</div></div>
    </div>""", unsafe_allow_html=True)

    questions = st.session_state.questions
    total = len(questions)

    # Results screen
    if st.session_state.get("quiz_result"):
        result = st.session_state.quiz_result
        pct = result["pct"]
        color = "#34d399" if pct >= 75 else ("#f59e0b" if pct >= 50 else "#f87171")
        st.markdown(f"""
        <div style="
            background: linear-gradient(145deg,rgba(15,23,42,.90),rgba(8,14,28,.95));
            border: 1px solid {color}44; border-radius: 24px; padding: 32px 28px;
            text-align: center; margin-bottom: 24px;
        ">
            <div style="font-size:48px;font-weight:900;color:{color};margin-bottom:8px;">
                {pct}%
            </div>
            <div style="font-size:16px;color:#94a3b8;margin-bottom:4px;">
                {result["score"]} out of {result["total"]} correct
            </div>
            <div style="font-size:13px;color:#475569;margin-top:12px;">
                Weakest skill: <span style="color:#f87171;font-weight:700;">
                {result["weakest"]}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        for index, detail in enumerate(result["details"], 1):
            ok = detail["correct"]
            with st.expander(
                f"{'✓' if ok else '✗'} Q{index} · {detail['skill']} · "
                f"{'Correct' if ok else 'Review needed'}"
            ):
                c1, c2 = st.columns(2)
                c1.markdown(f"**Your answer:** {detail['chosen'] or 'No answer'}")
                c2.markdown(f"**Correct:** {detail['answer']}")
                st.info(detail["why"])
        _mission_navigation(3, 5, "View Final Overview")
        return

    # One-question-at-a-time flow
    idx = st.session_state.get("_mock_q_index", 0)
    if idx >= total:
        idx = total - 1
    st.session_state._mock_q_index = idx

    q = questions[idx]
    skill_colors = {
        "Definition":    ("rgba(56,189,248,.14)",  "#38bdf8",  "rgba(56,189,248,.28)"),
        "Core Concept":  ("rgba(167,139,250,.14)", "#a78bfa",  "rgba(167,139,250,.28)"),
        "Application":   ("rgba(52,211,153,.14)",  "#34d399",  "rgba(52,211,153,.28)"),
        "Misconception": ("rgba(251,191,36,.14)",  "#fbbf24",  "rgba(251,191,36,.28)"),
    }
    bg, fg, border = skill_colors.get(q["skill"], ("rgba(239,68,68,.14)", "#f87171", "rgba(239,68,68,.28)"))

    # Progress dots
    dots_html = "<div class='mock-progress-dots'>"
    for i in range(total):
        cls = "done" if i < idx else ("active" if i == idx else "")
        dots_html += f"<div class='mock-dot {cls}'></div>"
    dots_html += "</div>"

    st.markdown(f"""
    <div class="mock-card">
        <div class="mock-counter">Question {idx + 1} of {total}</div>
        {dots_html}
        <div style="
            display:inline-block; padding:5px 14px; border-radius:30px;
            font-size:11px; font-weight:800; letter-spacing:.09em;
            text-transform:uppercase; margin-bottom:18px;
            background:{bg}; color:{fg}; border:1px solid {border};
        ">{q["skill"]}</div>
        <div class="mock-question-text">{q["q"]}</div>
    </div>
    """, unsafe_allow_html=True)

    answer_key = f"mock_ans_{idx}"
    chosen = st.radio(
        "Choose your answer",
        q["options"],
        key=answer_key,
        label_visibility="collapsed",
    )

    is_last = idx == total - 1
    col_prev, col_next = st.columns([1, 3])

    with col_prev:
        if idx > 0 and st.button("← Back", use_container_width=True):
            st.session_state._mock_q_index = idx - 1
            st.rerun()

    with col_next:
        label = "Submit Mock Test" if is_last else f"Next Question →"
        if st.button(label, use_container_width=True, type="primary"):
            if not is_last:
                st.session_state._mock_q_index = idx + 1
                st.rerun()
            else:
                # Collect all answers and grade
                answers = {}
                for i in range(total):
                    answers[i] = st.session_state.get(f"mock_ans_{i}", "")
                result = grade(questions, answers)
                _save_mission_quiz_result(result)
                st.session_state._mock_q_index = 0
                st.rerun()

    _mission_navigation(3, None)


def mission_overview_screen() -> None:
    brief = st.session_state.brief
    result = st.session_state.get("quiz_result")
    class_questions = st.session_state.get("class_questions", [])
    score = result.get("pct", 0) if result else 0
    weak = result.get("weakest", "Not tested") if result else "Not tested"

    st.markdown("""<div class='sec-head'>
      <div class='sec-icon' style='background:rgba(16,185,129,.15);'>05</div>
      <div><div class='sec-title'>Step 5 · Your Learning Overview</div>
      <div class='sec-sub'>What you know, what to review, and what to ask in class</div></div>
    </div>""", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    c1.metric("Readiness", f"{score}%")
    c2.metric("Weakest skill", weak)
    c3.metric("Mission status", "Completed")

    st.markdown(f"""
    <div class='card-glass' style='border-color:rgba(16,185,129,.35);'>
      <div class='albl lbl-green'>One-sentence summary</div>
      <div class='atxt'>{brief.get("tiny_answer", "")}</div>
    </div>
    <div class='card-glass'>
      <div class='albl lbl-yellow'>Your next study action</div>
      <div class='atxt'>Review <b>{weak}</b>, explain the topic once in your own words, and ask one question during class.</div>
    </div>
    """, unsafe_allow_html=True)

    if class_questions:
        st.markdown("#### Questions you are ready to ask in class")
        for number, question in enumerate(class_questions[:5], 1):
            st.write(f"{number}. {question}")

    class_questions = st.session_state.get("class_questions", [])
    if class_questions:
        st.markdown(
            "<div style='font-size:10px;font-weight:800;color:#38bdf8;letter-spacing:.10em;"
            "text-transform:uppercase;margin:20px 0 12px;'>"
            "3 questions to ask in your next class</div>",
            unsafe_allow_html=True,
        )
        for number, question in enumerate(class_questions[:3], 1):
            st.markdown(
                f"<div style='background:linear-gradient(135deg,rgba(56,189,248,.07),rgba(99,102,241,.05));"
                f"border:1px solid rgba(56,189,248,.18);border-radius:16px;"
                f"padding:16px 20px;margin-bottom:10px;display:flex;gap:14px;align-items:flex-start;'>"
                f"<div style='min-width:28px;height:28px;border-radius:50%;"
                f"background:rgba(56,189,248,.15);border:1px solid rgba(56,189,248,.30);"
                f"display:flex;align-items:center;justify-content:center;"
                f"font-size:12px;font-weight:900;color:#38bdf8;flex-shrink:0;'>{number}</div>"
                f"<div style='font-size:14px;color:#cbd5e1;line-height:1.60;'>{question}</div>"
                f"</div>",
                unsafe_allow_html=True,
            )

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("← Review Practice", use_container_width=True):
            _set_mission_step(3)
    with col2:
        if st.button("Ask Preluma AI", use_container_width=True):
            st.session_state.ai_context_note = (
                f"Current topic: {st.session_state.pack['title']}. "
                f"Student readiness: {score}%. Weak skill: {weak}."
            )
            st.session_state.force_page_ai = True
            st.info("Open “Ask Preluma AI” from the sidebar. Your topic context is ready.")
    with col3:
        if st.button("Start a New Mission", use_container_width=True):
            for key in ["pack", "brief", "questions", "quiz_result", "class_questions"]:
                st.session_state.pop(key, None)
            st.session_state.mission_started = False
            st.session_state.mission_step = 0
            st.rerun()


def student_mission(presentation):
    if not st.session_state.get("mission_started") or "pack" not in st.session_state:
        page_intro(
            "ai",
            "Pre-class learning mission",
            "Student Mission",
            "Choose your topic, set your goal, and let Preluma guide you through a 5-step AI-powered preparation.",
        )
        mission_control()
        if presentation:
            how_it_works()
        return

    # Active mission — show progress
    progress_bar()
    step = st.session_state.get("mission_step", 1)
    if step == 1:
        mission_brain_brief_screen()
    elif step == 2:
        mission_example_screen()
    elif step == 3:
        mission_practice_screen()
    elif step == 4:
        mission_mock_test_screen()
    else:
        mission_overview_screen()



def teacher_profile_page():
    """Teacher profile page — course teacher info for Zhou Yujue."""
    page_intro(
        "teacher",
        "Course Teacher · Yunnan University",
        "Teacher Profile",
        "Course teacher information — department, school, and contact details.",
    )
    st.markdown("""
    <style>
    .tp-avatar {
        width:88px; height:88px; border-radius:50%;
        background:linear-gradient(135deg,#0ea5e9,#6366f1);
        display:flex; align-items:center; justify-content:center;
        font-size:32px; font-weight:900; color:#fff; flex-shrink:0;
        border:3px solid rgba(56,189,248,.35);
        box-shadow:0 8px 28px rgba(99,102,241,.40);
    }
    .tp-banner {
        background:linear-gradient(135deg,rgba(14,165,233,.09),rgba(99,102,241,.07));
        border:1px solid rgba(56,189,248,.15); border-radius:24px;
        padding:28px 32px; margin-bottom:28px;
        display:flex; align-items:center; gap:28px;
    }
    .tp-name { font-size:26px; font-weight:900; color:#f1f5f9; margin-bottom:4px; }
    .tp-cn   { font-size:18px; font-weight:700; color:#38bdf8; margin-bottom:6px; }
    .tp-role { font-size:13px; color:#64748b; }
    .tp-card {
        background:linear-gradient(145deg,rgba(10,18,36,.96),rgba(6,12,26,.98));
        border:1px solid rgba(255,255,255,.07); border-radius:20px;
        padding:22px 24px; margin-bottom:14px;
    }
    .tp-card-lbl {
        font-size:10px; font-weight:800; color:#38bdf8;
        letter-spacing:.10em; text-transform:uppercase; margin-bottom:10px;
    }
    .tp-row {
        display:flex; gap:12px; align-items:flex-start; padding:8px 0;
        border-bottom:1px solid rgba(255,255,255,.04);
    }
    .tp-row:last-child { border-bottom:none; }
    .tp-key { min-width:130px; font-size:12px; color:#475569; font-weight:600; }
    .tp-val { font-size:13px; color:#cbd5e1; }
    </style>
    <div class="tp-banner">
        <div class="tp-avatar">ZY</div>
        <div>
            <div class="tp-name">Zhou Yujue</div>
            <div class="tp-cn">周玉珏</div>
            <div class="tp-role">
                Lecturer &nbsp;&bull;&nbsp; School of Software &nbsp;&bull;&nbsp; Yunnan University
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("""
        <div class="tp-card">
            <div class="tp-card-lbl">Course and Teaching</div>
            <div class="tp-row"><div class="tp-key">Course</div>
            <div class="tp-val">AI and Software Development</div></div>
            <div class="tp-row"><div class="tp-key">Department</div>
            <div class="tp-val">School of Software, Yunnan University</div></div>
            <div class="tp-row"><div class="tp-key">Level</div>
            <div class="tp-val">2nd-year undergraduate</div></div>
            <div class="tp-row"><div class="tp-key">Teaching style</div>
            <div class="tp-val">Project-based, practical Python focus</div></div>
        </div>
        """, unsafe_allow_html=True)
    with col_b:
        st.markdown("""
        <div class="tp-card">
            <div class="tp-card-lbl">School and Location</div>
            <div class="tp-row"><div class="tp-key">University</div>
            <div class="tp-val">Yunnan University (云南大学)</div></div>
            <div class="tp-row"><div class="tp-key">School</div>
            <div class="tp-val">School of Software (软件学院)</div></div>
            <div class="tp-row"><div class="tp-key">Campus</div>
            <div class="tp-val">Chenggong Campus, Kunming, Yunnan</div></div>
            <div class="tp-row"><div class="tp-key">Profile photo</div>
            <div class="tp-val">To be added with teacher consent</div></div>
        </div>
        """, unsafe_allow_html=True)

    # Quick homework assign — teacher can assign directly from profile page
    st.markdown("""
    <div style="font-size:10px;font-weight:800;color:#f59e0b;letter-spacing:.10em;
        text-transform:uppercase;margin:28px 0 14px;">
        Quick Assign Homework
    </div>
    """, unsafe_allow_html=True)
    with st.form("tp_quick_assign", border=False):
        qa1, qa2 = st.columns(2)
        hw_title  = qa1.text_input("Homework title", placeholder="e.g. Neural Networks Practice")
        hw_topic  = qa2.text_input("Topic", placeholder="e.g. Machine Learning")
        qa3, qa4, qa5 = st.columns(3)
        hw_due    = qa3.text_input("Due date", placeholder="e.g. Friday 8 PM")
        hw_diff   = qa4.selectbox("Difficulty", ["Beginner", "Intermediate", "Advanced"])
        hw_assign = qa5.text_input("Assign to", value="All Students")
        submit_hw = st.form_submit_button("Publish Homework", use_container_width=True)
    if submit_hw:
        if hw_title.strip() and hw_topic.strip():
            hw_id = create_homework(
                title=hw_title.strip(),
                topic=hw_topic.strip(),
                instructions=f"Read the topic summary and answer all questions about {hw_topic.strip()}.",
                due_date=hw_due.strip() or "TBD",
                difficulty=hw_diff,
                assigned_to=hw_assign.strip() or "All Students",
                created_by="Teacher Zhou Yujue",
                questions=_default_homework_questions(hw_topic.strip()),
            )
            st.success(f"Homework #{hw_id} published to students.")
        else:
            st.warning("Please enter both a title and a topic.")

    # ── Student team members ──────────────────────────────────────────────────
    st.markdown("""
    <div style="font-size:10px;font-weight:800;color:#38bdf8;letter-spacing:.10em;
        text-transform:uppercase;margin:32px 0 16px;">
        Student Development Team
    </div>
    """, unsafe_allow_html=True)

    team_data = [
        ("MR", "Mamunur Rashid",  "mamun",  "#0ea5e9",
         "Core Development · UI/UX · Integration · Deployment",
         ["streamlit_app.py", "llm.py", "engine.py", "homework_core.py", "storage_core.py"]),
        ("FA", "Md Fahim Ahmed",   "fahim",  "#8b5cf6",
         "Feature Logic · Quiz Testing · Interaction Feedback",
         ["algorithms_core.py", "analytics_core.py", "teacher.py", "tests/"]),
        ("JI", "Md Jiarul Islam",  "jiarul", "#10b981",
         "Topic Data · Documentation · Presentation Support",
         ["topics.py", "wiki_fetcher.py", "models.py", "result_generator.py"]),
    ]

    tcols = st.columns(3)
    for i, (initials, name, uname, color, role, files) in enumerate(team_data):
        with tcols[i]:
            st.markdown(f"""
            <div style="background:linear-gradient(145deg,rgba(10,18,36,.96),rgba(6,12,26,.98));
                        border:1px solid {color}28;border-radius:18px;padding:20px 18px;">
                <div style="display:flex;align-items:center;gap:14px;margin-bottom:14px;">
                    <div style="width:52px;height:52px;border-radius:50%;
                                background:linear-gradient(135deg,{color},{color}99);
                                display:flex;align-items:center;justify-content:center;
                                font-size:18px;font-weight:900;color:#fff;flex-shrink:0;">
                        {initials}
                    </div>
                    <div>
                        <div style="font-size:14px;font-weight:800;color:#f1f5f9;">{name}</div>
                        <div style="font-size:10px;color:{color};font-weight:700;
                                    letter-spacing:.06em;text-transform:uppercase;">@{uname}</div>
                    </div>
                </div>
                <div style="font-size:12px;color:#94a3b8;margin-bottom:12px;line-height:1.5;">{role}</div>
                <div style="font-size:10px;color:#475569;">
                    {"  ·  ".join(f'<code style="background:rgba(255,255,255,.06);padding:2px 6px;border-radius:4px;color:#94a3b8;">{f}</code>' for f in files)}
                </div>
            </div>""", unsafe_allow_html=True)


# Teacher Studio: algorithm demos and class analytics

def teacher_studio():
    page_intro(
        "teacher",
        "Algorithm-powered class analytics",
        "Teacher Studio",
        "Manual Python algorithms — Merge Sort, Binary Search, Linear Search — with live timing and CSV persistence.",
    )

    rows      = build_teacher_dataframe(st.session_state.get("latest_session"))
    analytics = teacher_analytics(rows)
    summary   = analytics["summary"]

    # Auto-generate result.txt with live algorithm timing whenever Teacher Studio loads
    try:
        generate_result_file()
    except Exception:
        pass  # Never crash the UI — result.txt is a proof artifact, not critical path

    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Class Average",  f"{summary['class_average']}%")
    c2.metric("Variance",       summary["population_variance"])
    c3.metric("Students",       summary["students_tracked"])
    c4.metric("Unique Weak Skills", summary["unique_weak_skills"])

    tab1,tab2,tab3,tab4,tab5 = st.tabs(["CSV Records","Merge Sort Ranking","Search Student","Skill Analytics","Audit Log"])

    with tab1:
        st.caption("Physical file: data/students.csv — Python csv module, no pandas for I/O.")
        st.dataframe(rows, use_container_width=True)

    with tab2:
        st.caption(f"Manual Merge Sort by Readiness — O(n log n) — elapsed: {analytics['sort_readiness_ns']} ns")
        st.dataframe(analytics["sorted_by_readiness"], use_container_width=True)
        fig = go.Figure()
        fig.add_bar(
            x=[str(r.get("Student","")) for r in analytics["sorted_by_readiness"]],
            y=[float(r.get("Readiness",0)) for r in analytics["sorted_by_readiness"]],
            marker_color="#38bdf8")
        fig.update_layout(title="Readiness Ranking — Manual Merge Sort", yaxis_range=[0,100], height=360,
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font_color="#94a3b8")
        st.plotly_chart(fig, use_container_width=True)

    with tab3:
        target = st.text_input("Search student name", value="Amir")
        if st.button("Run Search Comparison", use_container_width=True):
            res = search_student(rows, target)
            col1, col2 = st.columns(2)
            col1.metric("Linear Search O(n)",       f"{res['linear_ns']} ns")
            col2.metric("Binary Search O(log n)",   f"{res['binary_ns']} ns")
            st.caption(f"Merge Sort before Binary Search: {res['sort_ns']} ns — Total Binary Pipeline: {res['total_binary_pipeline_ns']} ns")
            if res["binary_result"]:
                st.dataframe(res["binary_result"], use_container_width=True)
            else:
                st.info(f"No student found with name '{target}'.")

    with tab4:
        st.caption("Weak skill frequency — pure Python loop, no libraries.")
        st.dataframe(analytics["weak_skill_frequency"], use_container_width=True)
        if analytics["weak_skill_frequency"]:
            df_skill = pd.DataFrame(analytics["weak_skill_frequency"])
            if "Weak Skill" in df_skill.columns and "Count" in df_skill.columns:
                fig2 = px.pie(df_skill, values="Count", names="Weak Skill", title="Skill Gap Distribution", hole=0.45)
                fig2.update_layout(height=300, paper_bgcolor="rgba(0,0,0,0)", font_color="#94a3b8")
                st.plotly_chart(fig2, use_container_width=True)

    with tab5:
        st.caption("result.txt — algorithm timing audit log.")
        for line in read_recent_logs(15):
            st.code(line, language="text")


# Words that are not real questions and need a follow-up prompt instead of a topic answer
_GREETINGS = {"hi", "hello", "hey", "yo", "hiya", "sup", "ok", "okay", "sure",
               "test", "testing", "good", "nice", "great", "thanks", "thank you",
               "bye", "goodbye", "lol", "haha", "hmm", "yes", "no", "yeah"}

_VAGUE_WORDS = {"help", "explain", "tell me", "more", "details",
                "why", "how", "this", "it", "i do not understand"}

# Short phrases that are essentially greetings + requests for help with no topic
_HELP_PHRASES = {
    "i need help", "need help", "please help", "help me", "help please",
    "can you help", "can u help", "i need help please", "please help me",
    "hi i need help", "hello i need help", "hey i need help",
    "hi help me", "hello help me", "hey help me",
    "hi can you help", "hello can you help",
}


def _question_needs_clarification(question: str) -> bool:
    # Return True when the input is too vague to answer meaningfully.
    text = " ".join(str(question).strip().split())
    if not text:
        return True
    cleaned = text.casefold().strip(" ?.,!")
    # Exact greeting word
    if cleaned in _GREETINGS:
        return True
    # Exact vague phrase
    if cleaned in _VAGUE_WORDS:
        return True
    # Known help-only phrases with no real topic
    if cleaned in _HELP_PHRASES:
        return True
    # Starts with a greeting then has only vague words (e.g. "hi i need help please")
    words = cleaned.split()
    if words and words[0] in _GREETINGS:
        rest_words = set(words[1:])
        all_vague = rest_words <= (_GREETINGS | _VAGUE_WORDS | {"i", "a", "me", "please", "u", "need", "some"})
        if all_vague:
            return True
    # Very short input with no academic content (3 words or fewer, none academic)
    if len(words) <= 3 and not any(len(w) > 6 for w in words):
        return True
    return False


def _natural_answer_text(response: dict, depth: str) -> str:
    direct = str(response.get("tiny_answer", "")).strip()
    simple = str(response.get("explain_simply", "")).strip()
    example = str(response.get("real_life_example", "")).strip()
    mistake = str(response.get("common_mistake", "")).strip()
    exam = str(response.get("exam_angle", "")).strip()

    if depth == "Short":
        pieces = [direct, simple]
    elif depth == "Deep":
        pieces = [
            direct,
            simple,
            f"To make this concrete, consider this example: {example}" if example else "",
            f"One important misunderstanding to avoid is the following: {mistake}" if mistake else "",
            f"For an exam or viva, the strongest way to remember the idea is: {exam}" if exam else "",
        ]
    else:
        pieces = [
            direct,
            simple,
            f"For example, {example}" if example else "",
        ]

    paragraphs = []
    for piece in pieces:
        piece = " ".join(str(piece).split())
        if piece:
            paragraphs.append(piece)
    return "\n\n".join(paragraphs)


def _clear_ai_chat() -> None:
    st.session_state.tutor_history = []
    st.session_state.ai_context_note = ""
    st.session_state.pop("ai_question_input", None)


def ask_preluma_ai_page():
    page_intro(
        "ai",
        "Adaptive academic tutor",
        "Ask Preluma AI",
        "Ask naturally. Preluma detects the topic, understands the learning goal, and adjusts the depth and teaching style.",
    )

    # No key notice
    if not llm_available():
        st.markdown(
            "<div style='background:rgba(245,158,11,.08);border:1px solid rgba(245,158,11,.28);"
            "border-radius:16px;padding:14px 18px;margin-bottom:18px;'>"
            "<div style='font-size:11px;font-weight:800;color:#f59e0b;letter-spacing:.08em;"
            "text-transform:uppercase;margin-bottom:7px;'>Real AI — One-time Setup Needed</div>"
            "<div style='font-size:13px;color:#94a3b8;line-height:1.7;'>"
            "To enable <b style='color:#e2e8f0;'>Gemini / ChatGPT / Claude</b> real answers:<br>"
            "1. Go to <b style='color:#38bdf8;'>Streamlit Cloud → Manage App → Settings → Secrets</b><br>"
            "2. Add: <code style='color:#34d399;background:rgba(52,211,153,.08);"
            "padding:2px 6px;border-radius:4px;'>GEMINI_API_KEY = &quot;your-key-here&quot;</code><br>"
            "3. Or use <code style='color:#34d399;background:rgba(52,211,153,.08);"
            "padding:2px 6px;border-radius:4px;'>OPENAI_API_KEY</code> for ChatGPT<br>"
            "<span style='color:#64748b;font-size:12px;'>Until then, Preluma uses curated Wikipedia-based answers — still accurate, just not live AI.</span>"
            "</div></div>",
            unsafe_allow_html=True,
        )

    current_pack = st.session_state.get("pack")
    mission_topic = current_pack.get("title") if current_pack else st.session_state.get("topic", "General learning")
    providers = available_providers()
    provider_label = _provider()

    top1, top2, top3 = st.columns([1.2, 1, 1])
    with top1:
        use_context = st.toggle("Lock to mission topic", value=False)
    with top2:
        mode = st.selectbox("Teaching style", ["Auto-detect", "Explain like I am 5", "Friendly Tutor", "Step-by-Step", "Exam/Viva Answer", "Give More Examples"])
    with top3:
        depth = st.selectbox("Answer depth", ["Balanced", "Short", "Deep"])

    st.markdown(
        f"<span class='context-chip'>{'Topic locked: ' + mission_topic if use_context else 'Ask anything — any topic'}</span>"
        f"<span class='context-chip'>Provider: {provider_label}</span>"
        f"<span class='context-chip'>Fallbacks ready: {len(providers)}</span>",
        unsafe_allow_html=True,
    )

    st.session_state.setdefault("ai_question_input", "")
    question = st.text_area(
        "Your question",
        key="ai_question_input",
        placeholder="Ask naturally, for example: I do not understand machine learning. First explain the basic idea, then tell me how it learns from data.",
        height=130,
    )

    quick = st.columns(4)
    quick_prompts = ["Explain simply", "Give a real example", "Go deeper", "Quiz me"]
    for col, prompt in zip(quick, quick_prompts):
        if col.button(prompt, use_container_width=True):
            base = question.strip() or mission_topic
            st.session_state.ai_question_input = f"{prompt}: {base}"
            st.rerun()

    ask_col, clear_col = st.columns([5, 1])
    ask = ask_col.button("Ask Preluma AI", use_container_width=True)
    clear_col.button("Clear", use_container_width=True, on_click=_clear_ai_chat)

    if ask and question.strip():
        detected_topic = detect_topic_from_question(question, mission_topic if use_context else "General learning")
        if _question_needs_clarification(question):
            raw = question.strip().casefold().strip(" ?.,!")
            provider_name = _provider() or "AI"
            # Pure greeting — respond warmly like any real AI assistant
            if raw in _GREETINGS or (raw.split()[0] in _GREETINGS if raw.split() else False):
                reply = (
                    f"Hello! I am Preluma AI, powered by {provider_name}. "
                    f"How can I help you today? "
                    f"You can ask me anything — any topic, any concept, any question. "
                    f"Just type what you want to understand."
                )
            else:
                # Vague input with no specific topic — ask for one more detail
                reply = (
                    f"I am ready to help. Just tell me what topic or concept you want to understand "
                    f"and I will give you a clear, direct answer powered by {provider_name}."
                )
            st.session_state.tutor_history.append({
                "question": question.strip(),
                "topic": "General",
                "clarification": True,
                "answer_text": reply,
                "source": f"Preluma ({provider_name})",
            })
        else:
            style_prefix = {
                "Auto-detect": "Follow the user's wording and automatically match the requested teaching style. ",
                "Explain like I am 5": "Explain like I am 5 years old using a safe and memorable analogy. ",
                "Friendly Tutor": "Explain as a patient, natural, friendly tutor. ",
                "Step-by-Step": "Explain step by step and connect cause and effect. ",
                "Exam/Viva Answer": "Give an exam-ready and viva-ready answer. ",
                "Give More Examples": "Teach through multiple clear real-life examples. ",
            }[mode]
            depth_prefix = {
                "Short": "Answer briefly and directly. ",
                "Balanced": "Give a natural balanced explanation in connected paragraphs. ",
                "Deep": "Give a deep, accurate, mechanism-focused explanation in coherent paragraphs. Explain why and how, not only what. ",
            }[depth]
            routed_question = style_prefix + depth_prefix + question.strip()
            with st.spinner(f"Preluma AI is understanding your question about {detected_topic}..."):
                response = llm_tutor(detected_topic, routed_question, st.session_state.get("persona", "Normal Mode")) if llm_available() else None
                # Label the answer source so the student knows which AI answered
                if response:
                    source = f"{_provider()} AI"
                elif llm_available():
                    source = "Preluma Smart Answer"
                    err = st.session_state.pop("_llm_last_error", "")
                    if err:
                        st.warning(f"AI connection issue: {err}. Showing smart offline answer.", icon=None)
                else:
                    source = "Preluma Smart Answer"
                if response is None:
                    fallback_pack = build_pack(detected_topic, use_wikipedia=True)
                    response = tutor_sections(fallback_pack, routed_question, st.session_state.get("persona", "Normal Mode"))
            response["concept"] = detected_topic
            answer_text = _natural_answer_text(response, depth)
            st.session_state.tutor_history.append({"question":question.strip(),"topic":detected_topic,"response":response,"answer_text":answer_text,"source":source,"depth":depth})

    st.markdown("""
    <style>
    /* Premium chat shell */
    .ai-chat-shell {
        margin-top:24px;
        display:flex; flex-direction:column; gap:0;
    }
    /* User bubble — right side */
    .chat-user {
        background:linear-gradient(135deg,rgba(56,189,248,.16),rgba(99,102,241,.12));
        border:1px solid rgba(56,189,248,.28); border-radius:20px 20px 4px 20px;
        padding:12px 18px; margin:0 0 4px auto;
        font-size:14px; color:#e2e8f0; line-height:1.55;
        max-width:72%; text-align:left;
        box-shadow:0 2px 12px rgba(56,189,248,.10);
    }
    /* AI meta label */
    .ai-meta {
        font-size:10px; color:#334155; margin:0 0 4px 4px;
        font-weight:700; letter-spacing:.06em; text-transform:uppercase;
    }
    /* AI bubble — left side */
    .ai-main-answer {
        background:linear-gradient(145deg,rgba(15,23,42,.96),rgba(8,14,30,.98));
        border:1px solid rgba(255,255,255,.08); border-radius:4px 20px 20px 20px;
        padding:16px 20px; margin:0 auto 20px 0;
        font-size:14px; color:#cbd5e1; line-height:1.78;
        max-width:85%;
        box-shadow:0 4px 20px rgba(0,0,0,.30);
    }
    /* Quick prompt pills */
    .quick-pills { display:flex; gap:8px; flex-wrap:wrap; margin:10px 0 14px; }
    </style>
    """, unsafe_allow_html=True)
    history = st.session_state.get("tutor_history", [])[-8:]
    if history:
        st.markdown("<div class='ai-chat-shell'>", unsafe_allow_html=True)
        for index, item in enumerate(history):
            # User bubble — right aligned
            st.markdown(
                f"<div class='chat-user'>{item['question']}</div>",
                unsafe_allow_html=True,
            )
            # AI label + bubble
            topic_lbl = item.get("topic", "AI")
            src_lbl   = item.get("source", "Preluma AI")
            st.markdown(
                f"<div class='ai-meta'>{topic_lbl} &nbsp;·&nbsp; {src_lbl}</div>",
                unsafe_allow_html=True,
            )
            st.markdown(
                f"<div class='ai-main-answer'>{item.get('answer_text','')}</div>",
                unsafe_allow_html=True,
            )
            # Study support expander (only for real AI answers)
            if not item.get("clarification"):
                response = item.get("response", {})
                has_extra = any([
                    response.get("common_mistake"),
                    response.get("exam_angle"),
                    response.get("real_life_example"),
                ])
                if has_extra:
                    with st.expander("Study support — mistake, exam line, example"):
                        if response.get("common_mistake"):
                            st.markdown(f"**Common mistake:** {response['common_mistake']}")
                        if response.get("exam_angle"):
                            st.markdown(f"**Exam line:** {response['exam_angle']}")
                        if response.get("real_life_example"):
                            st.markdown(f"**Example:** {response['real_life_example']}")
        st.markdown("</div>", unsafe_allow_html=True)


def my_homework_page():
    student = st.session_state.get("student", "Student")

    page_intro(
        "homework",
        "Student assignment desk",
        "My Homework",
        "Complete your assigned work, question by question. Each answer is reviewed instantly.",
    )

    # Notifications
    notifications = notifications_for_student(student)
    if notifications:
        unread = [n for n in notifications if n.get("Is Read") == "No"]
        label = f"Notifications ({len(notifications)})"
        if unread:
            label += f" — {len(unread)} new"
        with st.expander(label, expanded=bool(unread)):
            for note in reversed(notifications[-6:]):
                is_new = note.get("Is Read") == "No"
                dot = (
                    "<span style='width:7px;height:7px;border-radius:50%;"
                    "background:#f87171;display:inline-block;margin-right:7px;'></span>"
                    if is_new else ""
                )
                st.markdown(
                    f"<div class='assignment-card'>"
                    f"<div class='albl lbl-blue' style='display:flex;align-items:center;'>"
                    f"{dot}{note.get('Title', '')}</div>"
                    f"<div class='atxt' style='margin-top:6px;'>{note.get('Message', '')}"
                    f"</div></div>",
                    unsafe_allow_html=True,
                )
            if unread:
                if st.button("Mark all as read", key="mark_read_btn"):
                    mark_notifications_read(student)
                    st.rerun()

    homework_rows = homework_for_student(student)
    if not homework_rows:
        st.info("No homework assigned yet. Check back after your teacher publishes an assignment.")
        return

    # Homework selector
    labels = {
        f"#{row['Homework ID']} · {row['Title']} · Due {row['Due Date']}": row
        for row in homework_rows
    }
    selected_label = st.selectbox("Choose assignment", list(labels))
    selected = labels[selected_label]
    homework_id = selected["Homework ID"]

    # Reset step when homework changes
    if st.session_state.get("_hw_active_id") != homework_id:
        st.session_state["_hw_q_step"] = 0
        st.session_state["_hw_answers"] = {}
        st.session_state["homework_result"] = None
        st.session_state["_hw_active_id"] = homework_id

    # Assignment info card
    st.markdown(
        f"<div style='background:linear-gradient(145deg,rgba(120,53,15,.22),rgba(12,18,29,.92));"
        f"border:1px solid rgba(245,158,11,.20);border-radius:20px;padding:20px 24px;margin:10px 0 20px;'>"
        f"<div style='font-size:10px;font-weight:800;color:#f59e0b;letter-spacing:.12em;"
        f"text-transform:uppercase;margin-bottom:8px;'>{selected.get('Topic', '')}</div>"
        f"<div style='font-size:17px;font-weight:800;color:#f8fafc;margin-bottom:6px;'>"
        f"{selected.get('Title', '')}</div>"
        f"<div style='font-size:13px;color:#94a3b8;margin-bottom:10px;'>{selected.get('Instructions', '')}</div>"
        f"<div style='display:flex;gap:16px;'>"
        f"<span style='font-size:12px;color:#64748b;'>Due: <b style='color:#fbbf24;'>"
        f"{selected.get('Due Date', '')}</b></span>"
        f"<span style='font-size:12px;color:#64748b;'>Difficulty: <b style='color:#fbbf24;'>"
        f"{selected.get('Difficulty', '')}</b></span></div></div>",
        unsafe_allow_html=True,
    )

    questions = load_questions(homework_id)
    total_q = len(questions)
    result = st.session_state.get("homework_result")

    # RESULTS view
    if result:
        pct   = result.get("percentage", 0)
        score = result.get("score", 0)
        total = result.get("total", total_q)
        grade_color = "#34d399" if pct >= 70 else "#fbbf24" if pct >= 40 else "#f87171"
        verdict = "Excellent!" if pct >= 80 else "Good effort!" if pct >= 50 else "Review and try again"

        st.markdown(
            f"<div style='background:linear-gradient(135deg,rgba(15,23,42,.95),rgba(8,14,26,.98));"
            f"border:2px solid {grade_color}44;border-radius:24px;padding:32px 28px;"
            f"text-align:center;margin-bottom:24px;'>"
            f"<div style='font-size:64px;font-weight:900;color:{grade_color};line-height:1;"
            f"text-shadow:0 0 30px {grade_color}66;'>{pct}%</div>"
            f"<div style='font-size:16px;color:#94a3b8;margin-top:8px;'>"
            f"{score} / {total} correct &nbsp;&bull;&nbsp; Attempt {result.get('attempt', 1)}</div>"
            f"<div style='margin-top:12px;display:inline-block;background:{grade_color}20;"
            f"border:1px solid {grade_color}50;border-radius:30px;padding:6px 20px;"
            f"color:{grade_color};font-size:13px;font-weight:700;'>{verdict}</div></div>",
            unsafe_allow_html=True,
        )

        for detail in result.get("details", []):
            ok = detail["correct"]
            bg = "rgba(52,211,153,.08)" if ok else "rgba(248,113,113,.08)"
            br = "rgba(52,211,153,.25)" if ok else "rgba(248,113,113,.25)"
            wrong_extra = (
                f"<div style='font-size:13px;color:#94a3b8;margin-top:4px;'>Correct: "
                f"<b style='color:#34d399;'>{detail.get('correct_answer', '')}</b></div>"
                f"<div style='font-size:12px;color:#64748b;margin-top:8px;'>"
                f"{detail.get('explanation', '')}</div>"
            ) if not ok else ""
            chosen_color = "#34d399" if ok else "#f87171"
            st.markdown(
                f"<div style='background:{bg};border:1px solid {br};border-radius:16px;"
                f"padding:16px 18px;margin:8px 0;'>"
                f"<div style='font-size:11px;font-weight:800;color:#94a3b8;letter-spacing:.08em;"
                f"text-transform:uppercase;margin-bottom:6px;'>{detail['concept']}</div>"
                f"<div style='font-size:14px;color:#e2e8f0;margin-bottom:10px;'>"
                f"{detail.get('question', '')}</div>"
                f"<div style='font-size:13px;color:#94a3b8;'>Your answer: "
                f"<b style='color:{chosen_color};'>{detail.get('chosen', '')}</b></div>"
                f"{wrong_extra}</div>",
                unsafe_allow_html=True,
            )

        col_a, col_b = st.columns(2)
        if col_a.button("Try Again", use_container_width=True):
            st.session_state["_hw_q_step"] = 0
            st.session_state["_hw_answers"] = {}
            st.session_state["homework_result"] = None
            st.rerun()
        if col_b.button("Ask AI about mistakes", use_container_width=True):
            weak = [d["concept"] for d in result.get("details", []) if not d["correct"]]
            st.session_state.ai_context_note = (
                f"Homework topic: {selected.get('Topic')}. "
                f"Weak concepts from wrong answers: {', '.join(weak) if weak else 'none'}."
            )
            st.session_state.active_page = "Ask Preluma AI"
            st.rerun()
        return

    # Sequential Q&A
    if not questions:
        st.info("No questions found for this assignment.")
        return

    q_step   = min(st.session_state.get("_hw_q_step", 0), total_q - 1)
    hw_answers = st.session_state.get("_hw_answers", {})
    question = questions[q_step]
    q_id     = int(question["Question ID"])
    is_last  = (q_step == total_q - 1)

    # Progress bar
    pct_done = int((q_step / total_q) * 100)
    st.markdown(
        f"<div style='margin-bottom:18px;'>"
        f"<div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;'>"
        f"<span style='font-size:12px;font-weight:700;color:#64748b;letter-spacing:.06em;"
        f"text-transform:uppercase;'>Question {q_step + 1} of {total_q}</span>"
        f"<span style='font-size:12px;color:#38bdf8;font-weight:700;'>{pct_done}% done</span></div>"
        f"<div style='background:rgba(30,41,59,.6);border-radius:8px;height:6px;overflow:hidden;'>"
        f"<div style='width:{pct_done}%;height:100%;"
        f"background:linear-gradient(90deg,#0ea5e9,#6366f1);border-radius:8px;'>"
        f"</div></div></div>",
        unsafe_allow_html=True,
    )

    # Question card
    st.markdown(
        f"<div style='background:linear-gradient(145deg,rgba(15,23,42,.94),rgba(8,14,26,.98));"
        f"border:1px solid rgba(99,102,241,.25);border-radius:24px;"
        f"padding:28px 28px 22px;margin-bottom:18px;"
        f"box-shadow:0 16px 50px rgba(0,0,0,.30);'>"
        f"<div style='display:flex;align-items:center;gap:10px;margin-bottom:18px;'>"
        f"<div style='width:36px;height:36px;border-radius:10px;"
        f"background:linear-gradient(135deg,#6366f1,#8b5cf6);"
        f"display:flex;align-items:center;justify-content:center;"
        f"font-size:14px;font-weight:900;color:#fff;flex-shrink:0;'>Q{q_step + 1}</div>"
        f"<div style='font-size:11px;font-weight:800;color:#a78bfa;letter-spacing:.09em;"
        f"text-transform:uppercase;'>{question.get('Concept', '')}</div></div>"
        f"<div style='font-size:17px;font-weight:700;color:#f1f5f9;line-height:1.55;'>"
        f"{question.get('Question', '')}</div></div>",
        unsafe_allow_html=True,
    )

    options = question.get("Options", [])
    prev_answer = hw_answers.get(q_id)
    default_idx = options.index(prev_answer) if prev_answer in options else 0

    chosen = st.radio(
        "Select your answer",
        options,
        index=default_idx,
        key=f"hw_radio_{homework_id}_{q_step}",
        label_visibility="collapsed",
    )

    col1, col2 = st.columns([1, 2])
    if q_step > 0:
        if col1.button("Previous", use_container_width=True):
            hw_answers[q_id] = chosen
            st.session_state["_hw_answers"] = hw_answers
            st.session_state["_hw_q_step"] = q_step - 1
            st.rerun()

    if not is_last:
        if col2.button("Next Question", use_container_width=True, type="primary"):
            hw_answers[q_id] = chosen
            st.session_state["_hw_answers"] = hw_answers
            st.session_state["_hw_q_step"] = q_step + 1
            st.rerun()
    else:
        if col2.button("Submit Homework", use_container_width=True, type="primary"):
            hw_answers[q_id] = chosen
            st.session_state["_hw_answers"] = hw_answers
            final_answers = {int(k): v for k, v in hw_answers.items()}
            result = submit_homework(homework_id, student, final_answers)
            st.session_state["homework_result"] = result
            st.rerun()

    # Weak areas history
    mistakes = load_student_mistakes(student)
    if mistakes:
        with st.expander("My previous weak areas"):
            for mistake in mistakes[-6:]:
                st.markdown(
                    f"<div style='font-size:13px;color:#64748b;padding:4px 0;"
                    f"border-bottom:1px solid rgba(255,255,255,.04);'>"
                    f"<b style='color:#f87171;'>{mistake.get('Weak Concept', '')}</b> — "
                    f"{mistake.get('Question', '')}</div>",
                    unsafe_allow_html=True,
                )


def _default_homework_questions(topic: str) -> list[dict]:
    """7 default questions covering definition, application, example, analysis,
    comparison, reflection, and exam readiness."""
    return [
        {
            "question": f"What is the most accurate definition of {topic}?",
            "options": [
                f"The core meaning and purpose of {topic}",
                "A random process unrelated to the subject",
                "Only a complex formula with no meaning",
                "Something that cannot be explained simply",
            ],
            "answer": f"The core meaning and purpose of {topic}",
            "concept": "Definition",
            "explanation": "Always start with the clear definition before exploring deeper details.",
            "marks": 1,
        },
        {
            "question": f"Which approach best helps a student understand {topic}?",
            "options": [
                "Connect the definition with a real-world example",
                "Memorize keywords without understanding",
                "Skip the basics and jump to advanced parts",
                "Avoid asking questions during class",
            ],
            "answer": "Connect the definition with a real-world example",
            "concept": "Learning Strategy",
            "explanation": "Real examples bridge theory and practice — they make abstract ideas concrete.",
            "marks": 1,
        },
        {
            "question": f"Which is a real-world application of {topic}?",
            "options": [
                f"Using {topic} principles to solve a practical problem",
                "Memorizing a single sentence about it",
                "Ignoring it until the exam",
                "Replacing it with an unrelated concept",
            ],
            "answer": f"Using {topic} principles to solve a practical problem",
            "concept": "Application",
            "explanation": "Application shows you understand not just what it is, but how and why it is used.",
            "marks": 1,
        },
        {
            "question": f"What is a common misconception students have about {topic}?",
            "options": [
                "That it is more complex than it needs to be",
                "That it requires no prior knowledge",
                "That it has no real-world use",
                "That it can be fully learned in one minute",
            ],
            "answer": "That it is more complex than it needs to be",
            "concept": "Misconception",
            "explanation": "Breaking false beliefs is a key step in deep understanding.",
            "marks": 1,
        },
        {
            "question": f"How does {topic} relate to other subjects or topics you have studied?",
            "options": [
                "It builds on prior knowledge and connects to related ideas",
                "It is completely isolated from everything else",
                "It only matters in one very specific exam",
                "It contradicts everything learned before",
            ],
            "answer": "It builds on prior knowledge and connects to related ideas",
            "concept": "Connection",
            "explanation": "Strong learners see connections between topics — this creates a knowledge network.",
            "marks": 1,
        },
        {
            "question": f"What should a student do after making a mistake in a {topic} question?",
            "options": [
                "Review the weak concept and attempt a similar question",
                "Ignore the mistake and move on",
                "Stop studying the topic entirely",
                "Choose random answers next time",
            ],
            "answer": "Review the weak concept and attempt a similar question",
            "concept": "Reflection",
            "explanation": "Mistakes guide the next learning action — they are most useful when reviewed.",
            "marks": 1,
        },
        {
            "question": f"If asked to explain {topic} in a university exam, which answer is best?",
            "options": [
                "Define it clearly, give one example, and state why it matters",
                "Write only the name of the topic",
                "Copy a formula without explaining what it means",
                "Say it is too difficult to explain",
            ],
            "answer": "Define it clearly, give one example, and state why it matters",
            "concept": "Exam Readiness",
            "explanation": "Exam answers must show understanding: definition + example + significance.",
            "marks": 1,
        },
    ]


def homework_center_page():
    page_intro(
        "homework",
        "Teacher assignment workspace",
        "Homework Center",
        "Create assignments, publish them to students, and review class submission patterns and weak concepts.",
    )

    create_tab, overview_tab = st.tabs(["Create Homework", "Class Overview"])

    with create_tab:
        with st.form("teacher_homework_creator", border=False):
            c1, c2 = st.columns(2)
            title = c1.text_input("Homework title", value="Introduction Practice")
            topic = c2.text_input("Topic", value="Machine Learning")
            instructions = st.text_area(
                "Instructions",
                value="Read the topic summary and answer all questions.",
            )
            c3, c4, c5 = st.columns(3)
            due_date = c3.text_input("Due date", value="Friday 8:00 PM")
            difficulty = c4.selectbox("Difficulty", ["Beginner", "Intermediate", "Advanced"])
            assigned_to = c5.text_input(
                "Assign to",
                value="All Students",
                help="Use All Students or comma-separated student names.",
            )
            publish = st.form_submit_button("Publish Homework", use_container_width=True)

        if publish:
            homework_id = create_homework(
                title=title,
                topic=topic,
                instructions=instructions,
                due_date=due_date,
                difficulty=difficulty,
                assigned_to=assigned_to,
                created_by="Teacher Demo",
                questions=_default_homework_questions(topic),
            )
            st.success(f"Homework #{homework_id} published. Student notifications were created.")

    with overview_tab:
        rows = load_homework()
        if not rows:
            st.info("No homework is available.")
        else:
            labels = {
                f"#{row['Homework ID']} · {row['Title']}": row
                for row in rows
            }
            selected_label = st.selectbox(
                "Homework report",
                list(labels),
                key="teacher_homework_report",
            )
            selected = labels[selected_label]
            report = homework_overview(selected["Homework ID"])

            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Submissions", report["submissions"])
            c2.metric("Average", f"{report['average']}%")
            c3.metric("Highest", f"{report['highest']}%")
            c4.metric("Lowest", f"{report['lowest']}%")

            st.markdown(
                f"<div class='card-glass'><div class='albl lbl-red'>"
                f"Most common weak concept</div><div class='atxt'>"
                f"{report['common_weak_concept']} "
                f"({report['common_weak_count']} captured mistakes)</div></div>",
                unsafe_allow_html=True,
            )
            st.dataframe(report["submission_rows"], use_container_width=True)


# Evidence Board: shows every Python concept and algorithm used in the project

def evidence_board():
    page_intro(
        "evidence",
        "Project proof and technical validation",
        "Evidence Board",
        "Every Python concept, algorithm, and AI integration used in Preluma — proven and documented.",
    )

    st.markdown("""<div class='ev-grid'>
      <div class='ev-card'><h4>Clear Problem</h4><p>Students enter lectures unprepared, leading to passive learning and poor retention.</p></div>
      <div class='ev-card'><h4>Python Architecture</h4><p>Streamlit, Pandas, Plotly, dicts, session state, forms, CSV, and modular functions.</p></div>
      <div class='ev-card'><h4>Manual Algorithms</h4><p>Merge Sort O(n log n) and Binary Search O(log n) implemented from scratch — no library sorting.</p></div>
      <div class='ev-card'><h4>Multi-LLM AI</h4><p>Claude, Groq, and Gemini with automatic fallback — whichever key is available is used.</p></div>
      <div class='ev-card'><h4>CSV Persistence</h4><p>Student quiz results stored in data/students.csv using Python csv module. Survives page refresh.</p></div>
      <div class='ev-card'><h4>Wikipedia Fallback</h4><p>Unknown topics fetch real content from Wikipedia API — no empty answers ever.</p></div>
      <div class='ev-card'><h4>Audit Log</h4><p>Every algorithm call is timed and written to result.txt with nanosecond precision.</p></div>
      <div class='ev-card'><h4>Smart Tutor Style</h4><p>UltraTutor detects if you want child-simple, exam-ready, example-first, or deep explanation.</p></div>
      <div class='ev-card'><h4>Live Deployment</h4><p>Running live at preluma-edtech.streamlit.app — accessible from any device, anywhere.</p></div>
    </div>""", unsafe_allow_html=True)

    errors = validate_topics()
    if errors:
        st.warning("Topic issues: " + ", ".join(errors[:3]))
    else:
        st.success(f"All topic packs validated — no data errors found.")

    st.markdown("### Python Concepts Demonstrated")
    st.dataframe(pd.DataFrame({
        "Concept": ["Functions","Nested Dicts","Session State","Forms","DataFrame","Plotly Charts",
                    "CSV File I/O","Wikipedia API","Multi-LLM","Merge Sort","Binary Search","Audit Log","Tabs"],
        "Used For": ["Modular app logic","Topic pack storage","Quiz and tutor state",
                     "Safe form submission","Teacher analytics","Readiness visualisation",
                     "Persistent student records","Unknown topic fallback","Claude/Groq/Gemini auto-select",
                     "Manual O(n log n) ranking","Manual O(log n) student search",
                     "Algorithm timing in result.txt","All-concept display"],
    }), use_container_width=True)


# Professor Defense: 8-point rubric for the final presentation

def professor_defense():
    page_intro(
        "defense",
        "Final defense preparation",
        "Professor Defense",
        "Built for final presentation — clear problem, Python proof, innovation, and contribution.",
    )

    st.markdown("""<div class='rubric-grid'>
      <div class='rubric-card'><h4>1. Real Problem</h4><p>Students enter lectures unprepared, reducing understanding, memory, and class participation.</p></div>
      <div class='rubric-card'><h4>2. Python Solution</h4><p>Preluma uses Python + Streamlit: Brain Brief, quiz, Mistake Clinic, UltraTutor, and dashboard.</p></div>
      <div class='rubric-card'><h4>3. Algorithm Proof</h4><p>Merge Sort (O n log n) and Binary Search (O log n) implemented manually. Timing stored in result.txt.</p></div>
      <div class='rubric-card'><h4>4. Real Data</h4><p>Wikipedia API fallback for unknown topics. CSV persistence for student records. No empty answers.</p></div>
      <div class='rubric-card'><h4>5. AI Integration</h4><p>Claude, Groq, and Gemini — multi-provider with automatic fallback. Smart question style detection.</p></div>
      <div class='rubric-card'><h4>6. Teacher Value</h4><p>Teacher Studio: readiness analytics, skill gap chart, merge sort ranking, and binary search demo.</p></div>
      <div class='rubric-card'><h4>7. Testing Proof</h4><p>Regression tests verify topic schema, build_pack, quiz flow, tutor output, and QnA.</p></div>
      <div class='rubric-card'><h4>8. Future Product</h4><p>Student accounts, teacher class codes, PDF notes, RAG retrieval, and mobile app roadmap.</p></div>
    </div>""", unsafe_allow_html=True)

    st.markdown("### System Architecture")
    st.code("Student Input → Topic Router → Curated Pack / Wikipedia Fallback → Brain Brief\n→ Quiz (4 skills) → Mistake Clinic → UltraTutor (AI) → Class Questions\n→ CSV Persistence → Merge Sort + Binary Search → Teacher Analytics → Export", language="text")

    st.markdown("### Defense Line")
    st.success("Third-party libraries are allowed. Preluma uses Streamlit and Plotly for the interface, but all core algorithms — Merge Sort, Binary Search, statistics, CSV I/O — are implemented manually in Python. This proves both presentation skill and algorithmic understanding.")


# Project Team: member cards, team photo, and contribution breakdown

def project_team():
    page_intro(
        "defense",
        "Student product team · Yunnan University",
        "Project Team",
        "Three students built Preluma together — combining core Python development, algorithm testing, and topic data engineering.",
    )

    # Team photo — full-width, proper fit
    if TEAM_URI:
        st.markdown(
            f"<div style='"
            f"width:100%;border-radius:26px;overflow:hidden;position:relative;"
            f"background:linear-gradient(135deg,#020617,#0f172a);"
            f"border:1px solid rgba(148,163,184,.18);"
            f"box-shadow:0 30px 80px rgba(0,0,0,.45);margin-bottom:28px;'>"
            f"<img src='{TEAM_URI}' style='"
            f"width:100%;display:block;object-fit:contain;background:#020617;min-height:260px;'>"
            f"<div style='position:absolute;inset:0;"
            f"background:linear-gradient(0deg,rgba(2,6,23,.80) 0%,transparent 55%);'></div>"
            f"<div style='position:absolute;bottom:28px;left:32px;right:32px;z-index:2;'>"
            f"<div style='font-size:11px;font-weight:800;color:#38bdf8;letter-spacing:.12em;"
            f"text-transform:uppercase;margin-bottom:8px;'>Team Preluma &nbsp;&bull;&nbsp; Yunnan University</div>"
            f"<div style='font-size:26px;font-weight:900;color:#fff;line-height:1.2;"
            f"text-shadow:0 4px 20px rgba(0,0,0,.60);'>"
            f"Building a smarter pre-class learning experience together.</div>"
            f"</div></div>",
            unsafe_allow_html=True,
        )
    else:
        st.warning("Team photo missing: assets/team_preluma.jpg")

    # Member cards
    m1, m2, m3 = st.columns(3)
    members = [
        (m1, "#0ea5e9", "MAMUNUR RASHID",
         "Lead Developer · Architecture · Deployment",
         "Built the complete Preluma architecture — streamlit_app.py (2 600+ lines), engine.py, llm.py, algorithms_core.py, homework_core.py, and analytics_core.py. Designed every page, connected the AI pipeline, and deployed to Streamlit Cloud.",
         "streamlit_app.py · engine.py · llm.py · algorithms_core.py"),
        (m2, "#10b981", "MD FAHIM",
         "Quiz Logic · Algorithm Validation · Python Testing",
         "Wrote and validated the quiz grading function in homework_core.py, tested all manual algorithm outputs in algorithms_core.py, and contributed session state handling for the interaction flow across teacher.py.",
         "homework_core.py · algorithms_core.py · teacher.py"),
        (m3, "#8b5cf6", "MD JIARUL ISLAM",
         "Topic Data · Wiki Pipeline · Storage",
         "Built and maintained the full topic data structure across all 18 topics in topics.py, contributed to the Wikipedia data pipeline in wiki_fetcher.py, and validated CSV record handling in storage_core.py.",
         "topics.py · wiki_fetcher.py · storage_core.py"),
    ]
    for col, color, name, role, desc, files in members:
        col.markdown(
            f"<div style='background:linear-gradient(145deg,rgba(15,23,42,.94),rgba(8,14,26,.98));"
            f"border:1px solid rgba(148,163,184,.09);border-top:3px solid {color};"
            f"border-radius:20px;padding:22px 18px;height:100%;'>"
            f"<div style='font-size:10px;font-weight:800;color:{color};letter-spacing:.10em;"
            f"text-transform:uppercase;margin-bottom:10px;'>{role}</div>"
            f"<div style='font-size:17px;font-weight:900;color:#f8fafc;margin-bottom:10px;'>{name}</div>"
            f"<div style='font-size:13px;color:#64748b;line-height:1.65;margin-bottom:12px;'>{desc}</div>"
            f"<div style='background:rgba(0,0,0,.30);border-radius:8px;padding:8px 12px;"
            f"border-left:3px solid {color}40;'>"
            f"<div style='font-size:9px;font-weight:800;color:{color};letter-spacing:.10em;"
            f"text-transform:uppercase;margin-bottom:4px;'>Python files</div>"
            f"<div style='font-size:11px;color:#64748b;font-family:monospace;'>{files}</div>"
            f"</div></div>",
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

    # Work division table
    st.markdown(
        "<div style='font-size:13px;font-weight:700;color:#475569;letter-spacing:.10em;"
        "text-transform:uppercase;margin-bottom:12px;'>Contribution Breakdown</div>",
        unsafe_allow_html=True,
    )
    st.dataframe([
        {
            "Member": "MAMUNUR RASHID",
            "Python Ownership": "streamlit_app.py, engine.py, llm.py, algorithms_core.py, analytics_core.py, homework_core.py",
            "Role": "Lead developer — full architecture, AI, UI, deployment",
        },
        {
            "Member": "MD FAHIM",
            "Python Ownership": "homework_core.py (quiz grading), algorithms_core.py (testing), teacher.py",
            "Role": "Quiz & algorithm validation, session state, Python testing",
        },
        {
            "Member": "MD JIARUL ISLAM",
            "Python Ownership": "topics.py (all 18 topics), wiki_fetcher.py, storage_core.py",
            "Role": "Topic data engineering, Wikipedia pipeline, CSV storage",
        },
    ], use_container_width=True, hide_index=True)


# Demo Guide: step-by-step script for the live class presentation

def demo_guide():
    page_intro(
        "demo",
        "Presentation walkthrough",
        "Demo Guide",
        "A focused presentation sequence for showing the problem, student flow, algorithms, AI support, and teacher value.",
    )

    steps = [
        ("Open Preluma", "Show preluma-edtech.streamlit.app. Say: Python-based pre-class learning assistant with Wikipedia fallback, manual algorithms, and multi-LLM AI."),
        ("Show the problem", "Students sit in lectures without preparation — passive learning, low retention, bad questions."),
        ("Start a mission", "Select Machine Learning, enter name, click Start Pre-Class Mission."),
        ("Brain Brief", "Show 2-column layout and concept tabs — all concepts explained, not just one."),
        ("Quiz", "Take the quiz — each question tests a different skill type."),
        ("Mistake Clinic", "Every wrong answer gets a clear correction with reasoning."),
        ("UltraTutor", "Ask 'explain it like I am 5 years old' — show how style changes completely with AI."),
        ("Teacher Studio", "Show Merge Sort ranking, Binary Search, CSV persistence, and audit log."),
        ("Evidence Board", "Show Python concepts table — 13 concepts demonstrated."),
        ("Professor Defense", "Show the 8-point rubric and defense line."),
    ]
    for i, (title, desc) in enumerate(steps, 1):
        st.markdown(f"""<div class='card-glass' style='margin:6px 0;display:flex;gap:16px;align-items:flex-start;'>
          <div style='min-width:28px;height:28px;border-radius:50%;background:rgba(56,189,248,.15);border:1px solid rgba(56,189,248,.25);display:flex;align-items:center;justify-content:center;color:#38bdf8;font-size:12px;font-weight:800;flex-shrink:0;'>{i}</div>
          <div><div style='font-size:14px;font-weight:700;color:#f1f5f9;'>{title}</div><div style='font-size:13px;color:#94a3b8;margin-top:4px;'>{desc}</div></div>
        </div>""", unsafe_allow_html=True)

    st.success("Final line: Preluma does not replace teachers. It prepares students to understand teachers better.")


# Future Roadmap: planned features and product vision beyond the prototype

def roadmap():
    page_intro(
        "roadmap",
        "Product vision",
        "Future Roadmap",
        "Where Preluma goes next — from prototype to real product.",
    )

    st.dataframe(pd.DataFrame({
        "Phase":      ["Current","Prototype","AI Upgrade","Real Product"],
        "Goal":       ["Final project submission","Student accounts + history","RAG tutor with citations","Mobile app + class codes"],
        "Technology": ["Python + Streamlit + Gemini","Python + SQLite","Embeddings + retrieval + LLM","API backend + React Native"],
        "Status":     ["Live now","Next semester","Future","Long-term"],
    }), use_container_width=True)
    st.code("Now:    Python + Streamlit + Wikipedia + Claude/Groq/Gemini + CSV + Merge Sort\nNext:   Login + SQLite + saved student history per account\nLater:  Upload course PDF + retrieval + cited AI answers\nFuture: Mobile app + teacher dashboard + real-time class codes", language="text")


# App entry point — called by Streamlit on every page load or user interaction

def login_page():
    """Beautiful full-screen login & register page with role toggle + invite code."""
    import streamlit as st

    st.markdown("""
<style>
.login-wrap { max-width:440px; margin:0 auto; padding:30px 0 20px; }
.login-logo { text-align:center; margin-bottom:28px; }
.login-logo-name { font-size:44px; font-weight:900; color:#06b6d4; letter-spacing:-1px; line-height:1; }
.login-logo-tag  { font-size:13px; color:#475569; font-weight:500; letter-spacing:.04em; margin-top:4px; }
.role-btn-active {
    flex:1; text-align:center; padding:12px 8px; border-radius:14px; cursor:pointer;
    font-size:12px; font-weight:800; letter-spacing:.07em; border:2px solid;
    transition:all .2s;
}
.cred-box {
    background:rgba(6,182,212,.06); border:1px solid rgba(6,182,212,.14);
    border-radius:12px; padding:12px 16px; margin-top:18px;
}
.cred-title { font-size:10px; font-weight:800; color:#06b6d4; letter-spacing:.1em; margin-bottom:8px; }
.cred-row   { font-size:11.5px; color:#94a3b8; line-height:1.9; font-family:monospace; }
.invite-box {
    background:rgba(103,232,249,.05); border:1px solid rgba(103,232,249,.18);
    border-radius:12px; padding:14px 16px; margin-bottom:14px;
    font-size:12px; color:#94a3b8; line-height:1.6;
}
</style>
""", unsafe_allow_html=True)

    st.markdown("<div class='login-wrap'>", unsafe_allow_html=True)
    st.markdown("""
<div class='login-logo'>
    <div class='login-logo-name'>Preluma</div>
    <div class='login-logo-tag'>Light Up Before Class</div>
</div>""", unsafe_allow_html=True)

    # ── Role toggle ──────────────────────────────────────────────
    st.session_state.setdefault("login_role", "Student")
    col_t, col_s = st.columns(2)

    t_active = st.session_state.login_role == "Teacher"
    s_active = st.session_state.login_role == "Student"

    t_bg  = "rgba(103,232,249,.14)" if t_active else "rgba(103,232,249,.04)"
    t_bc  = "#67e8f9"               if t_active else "rgba(103,232,249,.2)"
    t_col = "#e2e8f0"               if t_active else "#67e8f9"
    s_bg  = "rgba(134,239,172,.14)" if s_active else "rgba(134,239,172,.04)"
    s_bc  = "#86efac"               if s_active else "rgba(134,239,172,.2)"
    s_col = "#e2e8f0"               if s_active else "#86efac"

    with col_t:
        if st.button("TEACHER", key="role_teacher", use_container_width=True,
                     type="primary" if t_active else "secondary"):
            st.session_state.login_role = "Teacher"
            st.rerun()
    with col_s:
        if st.button("STUDENT", key="role_student", use_container_width=True,
                     type="primary" if s_active else "secondary"):
            st.session_state.login_role = "Student"
            st.rerun()

    st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)

    # ── TEACHER mode ─────────────────────────────────────────────
    if st.session_state.login_role == "Teacher":
        st.markdown("""
<div class='invite-box'>
    <b style='color:#67e8f9;'>Teacher Access</b><br>
    If you already have a teacher account, log in below.<br>
    To create a new teacher account, enter the <b>Teacher Invite Code</b>
    provided by the course admin.
</div>""", unsafe_allow_html=True)

        tab_tlogin, tab_treg = st.tabs(["Teacher Log In", "New Teacher? Use Invite Code"])

        with tab_tlogin:
            with st.form("teacher_login_form"):
                t_user = st.text_input("Username", placeholder="Teacher username")
                t_pass = st.text_input("Password", type="password", placeholder="Password")
                t_sub  = st.form_submit_button("Log In as Teacher", use_container_width=True, type="primary")

            if t_sub:
                if not t_user or not t_pass:
                    st.error("Please fill in all fields.")
                else:
                    user = authenticate(t_user, t_pass)
                    if user and user["Role"] == "teacher":
                        st.session_state.logged_in   = True
                        st.session_state.user_role   = "teacher"
                        st.session_state.username    = user["Username"]
                        st.session_state.student     = user["Full Name"]
                        st.session_state.active_page = "Home"
                        st.rerun()
                    elif user and user["Role"] == "student":
                        st.error("This is a student account. Please switch to Student mode.")
                    else:
                        st.error("Incorrect username or password.")

        with tab_treg:
            st.markdown(
                "<p style='font-size:12px;color:#64748b;margin-bottom:10px;'>"
                "Enter the invite code given to you by the course admin to create a teacher account.</p>",
                unsafe_allow_html=True,
            )
            with st.form("teacher_reg_form"):
                tr_name   = st.text_input("Full Name", placeholder="Your full name")
                tr_user   = st.text_input("Username",  placeholder="Choose a username (min 3 chars)")
                tr_pass   = st.text_input("Password",  type="password", placeholder="Min 6 characters")
                tr_pass2  = st.text_input("Confirm Password", type="password", placeholder="Repeat password")
                tr_code   = st.text_input("Teacher Invite Code", type="password",
                                          placeholder="Enter the secret invite code")
                tr_submit = st.form_submit_button("Create Teacher Account", use_container_width=True, type="primary")

            if tr_submit:
                import streamlit as _st
                # Get invite code from secrets, fallback to default
                try:
                    valid_code = st.secrets.get("TEACHER_INVITE_CODE", "PRELUMA-TEACH-2024")
                except Exception:
                    valid_code = "PRELUMA-TEACH-2024"

                if tr_pass != tr_pass2:
                    st.error("Passwords do not match.")
                elif tr_code.strip() != valid_code:
                    st.error("Invalid invite code. Contact your course admin for access.")
                else:
                    ok, msg = register(tr_user, tr_pass, tr_name, role="teacher")
                    if ok:
                        st.success(f"Teacher account created! You can now log in.")
                    else:
                        st.error(msg)

    # ── STUDENT mode ─────────────────────────────────────────────
    else:
        tab_login, tab_reg = st.tabs(["Log In", "New Student? Register Here"])

        with tab_login:
            with st.form("student_login_form"):
                username  = st.text_input("Username", placeholder="Enter your username")
                password  = st.text_input("Password", type="password", placeholder="Enter your password")
                submitted = st.form_submit_button("Log In", use_container_width=True, type="primary")

            if submitted:
                if not username or not password:
                    st.error("Please enter both username and password.")
                else:
                    user = authenticate(username, password)
                    if user and user["Role"] == "teacher":
                        st.error("This is a teacher account. Please switch to Teacher mode.")
                    elif user:
                        st.session_state.logged_in   = True
                        st.session_state.user_role   = user["Role"]
                        st.session_state.username    = user["Username"]
                        st.session_state.student     = user["Full Name"]
                        st.session_state.active_page = "Home"
                        st.rerun()
                    else:
                        st.error("Incorrect username or password.")



        with tab_reg:
            st.markdown(
                "<p style='font-size:12px;color:#64748b;margin-bottom:10px;'>"
                "Create your student account to track progress and access homework.</p>",
                unsafe_allow_html=True,
            )
            with st.form("student_reg_form"):
                reg_name  = st.text_input("Full Name", placeholder="e.g. Alice Wang")
                reg_user  = st.text_input("Username",  placeholder="Choose a username (min 3 chars)")
                reg_pass  = st.text_input("Password",  type="password", placeholder="Min 6 characters")
                reg_pass2 = st.text_input("Confirm Password", type="password", placeholder="Repeat password")
                reg_sub   = st.form_submit_button("Create Student Account", use_container_width=True, type="primary")

            if reg_sub:
                if reg_pass != reg_pass2:
                    st.error("Passwords do not match.")
                else:
                    ok, msg = register(reg_user, reg_pass, reg_name, role="student")
                    if ok:
                        st.success(f"{msg} Go to Log In tab.")
                    else:
                        st.error(msg)

    st.markdown("</div>", unsafe_allow_html=True)


def main():
    init_state()

    # Login gate — show login page if not authenticated
    if not st.session_state.get("logged_in", False):
        login_page()
        return

    page, presentation = sidebar()

    if page in {"My Homework", " My Homework"} or page.startswith(" My Homework"):
        my_homework_page()
        return

    # Role guard — redirect teacher to Home if they land on student-only pages
    _role = st.session_state.get("user_role", "student")
    student_only = {"Student Mission", "My Homework", "Ask Preluma AI"}
    teacher_only = {"Teacher Profile", "Teacher Studio", "Homework Center"}

    if _role == "teacher" and page in student_only:
        st.session_state.active_page = "Home"
        page = "Home"
    if _role == "student" and page in teacher_only:
        st.session_state.active_page = "Home"
        page = "Home"

    pages = {
        "Home": home_page,
        "Student Mission": lambda: student_mission(presentation),
        "Ask Preluma AI": ask_preluma_ai_page,
        "Teacher Profile": teacher_profile_page,
        "Teacher Studio": teacher_studio,
        "Homework Center": homework_center_page,
        "Evidence Board": evidence_board,
        "Professor Defense": professor_defense,
        "Project Team": project_team,
        "Demo Guide": demo_guide,
        "Future Roadmap": roadmap,
    }
    pages.get(page, home_page)()


if __name__ == "__main__":
    main()
