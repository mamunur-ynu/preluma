from pathlib import Path
import base64
import json

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from engine import build_brain_brief, build_pack, grade, make_questions, tutor_sections
from teacher import build_teacher_dataframe, class_average_readiness, readiness_label, teacher_analytics, search_student
from topics import TOPIC_OPTIONS, validate_topics
from wiki_fetcher import smart_answer_from_pack
from storage_core import append_student_row, next_record_id, read_recent_logs, timestamp
from llm import active_provider as _provider, available_providers, llm_available, llm_tutor, detect_topic_from_question
from homework_core import (
    create_homework,
    homework_for_student,
    homework_overview,
    load_homework,
    load_questions,
    load_student_mistakes,
    notifications_for_student,
    mark_homework_notifications_read,
    seed_homework_demo,
    submit_homework,
)

APP_VERSION = "28.2 Cinematic Full Home + Safe Team Overlay"
APP_NAME    = "Preluma"
TAGLINE     = "Light Up Before Class"

TEAM_MEMBERS = [
    ("MAMUNUR RASHID", "Core Development · UI/UX · Integration · Deployment"),
    ("MD FAHIM",       "Feature Logic · Quiz Testing · Interaction Feedback"),
    ("MD JIARUL ISLAM","Topic Data · Documentation · Presentation Support"),
]

CAMPUS_IMAGE = Path("assets/ynu_campus.jpg")
TEAM_IMAGE = Path("assets/team_preluma.jpg")
SIDEBAR_IMAGE = Path("assets/sidebar_clocktower.jpg")

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

CAMPUS_URI = image_data_uri(str(CAMPUS_IMAGE))
TEAM_URI = image_data_uri(str(TEAM_IMAGE))
SIDEBAR_URI = image_data_uri(str(SIDEBAR_IMAGE))


CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
*, *::before, *::after { box-sizing: border-box; }
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.block-container { max-width: 1200px; padding-top: 1.45rem !important; padding-left: 1.8rem; padding-right: 1.8rem; }
[data-testid="stSidebar"] {
    background:
        linear-gradient(180deg, rgba(2,6,23,.12) 0%, rgba(2,6,23,.18) 24%, rgba(2,6,23,.30) 52%, rgba(2,6,23,.46) 100%),
        radial-gradient(circle at 50% 61%, rgba(251,191,36,.22) 0%, rgba(251,191,36,.08) 20%, transparent 42%),
        url('__SIDEBAR_BG__');
    background-size: auto, auto, 250% auto;
    background-position: center center, center center, 50% 62%;
    background-repeat: no-repeat;
    border-right: 1px solid rgba(255,255,255,.10);
    box-shadow: inset -1px 0 0 rgba(255,255,255,.05);
}
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
}
.progress-step { flex: 1; text-align: center; padding: 10px 8px; border-radius: 12px;
    font-size: 12px; font-weight: 600; color: #64748b; }
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
.member-card.main { border-color: rgba(96,165,250,.45); background: linear-gradient(135deg, rgba(14,165,233,.17), rgba(124,58,237,.14)); }
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

/* compact sidebar */
[data-testid="stSidebar"] {
    border-right: 1px solid rgba(148,163,184,.10);
}
[data-testid="stSidebar"] > div:first-child {
    padding-top: 1.15rem;
    background: linear-gradient(180deg, rgba(2,6,23,.02), rgba(2,6,23,.05));
    backdrop-filter: blur(1px);
}
[data-testid="stSidebar"] .stButton > button {
    min-height: 46px !important;
    border-radius: 16px !important;
    justify-content: flex-start !important;
    padding: .7rem .9rem !important;
    background: rgba(2,6,23,.26) !important;
    border: 1px solid rgba(255,255,255,.06) !important;
    box-shadow: 0 10px 24px rgba(0,0,0,.12) !important;
    color: #f1f5f9 !important;
    font-weight: 650 !important;
    font-size: 14px !important;
    backdrop-filter: blur(10px);
    transition: background .28s ease, border-color .28s ease, transform .28s ease, box-shadow .28s ease, color .28s ease;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(59,130,246,.18) !important;
    border-color: rgba(125,211,252,.32) !important;
    color: #fff !important;
    transform: translateX(4px);
    box-shadow: 0 14px 30px rgba(37,99,235,.18) !important;
}
[data-testid="stSidebar"] .stButton > button[kind="primary"] {
    background: linear-gradient(135deg, rgba(37,99,235,.34), rgba(124,58,237,.28)) !important;
    border-color: rgba(125,211,252,.38) !important;
    color: #ffffff !important;
    box-shadow: 0 14px 34px rgba(59,130,246,.18) !important;
}
.nav-label {
    margin: 1.12rem 0 .48rem;
    color: #dbeafe !important;
    font-size: 10px !important;
    letter-spacing: .19em;
    font-weight: 900;
    text-transform: uppercase;
    text-shadow: 0 1px 12px rgba(0,0,0,.22);
}
.sidebar-profile {
    border-radius: 18px;
    padding: 15px 16px;
    margin: .85rem 0 1rem;
    border: 1px solid rgba(125,211,252,.22);
    background: linear-gradient(145deg, rgba(15,23,42,.70), rgba(8,15,27,.80));
    box-shadow: 0 16px 34px rgba(0,0,0,.18);
    backdrop-filter: blur(10px);
    transition: transform .25s ease, border-color .25s ease, box-shadow .25s ease;
}
.sidebar-profile:hover { transform: translateY(-1px); border-color: rgba(125,211,252,.28); box-shadow: 0 18px 34px rgba(0,0,0,.22); }
.sidebar-profile b { font-size: 14px; color: #f8fafc; }
.sidebar-profile span { display:block; margin-top:5px; color:#cbd5e1; font-size:12px; }

.sidebar-status {
    margin-top: 1rem;
    border: 1px solid rgba(45,212,191,.20);
    background: linear-gradient(145deg, rgba(13,148,136,.12), rgba(2,6,23,.34));
    padding: 12px 13px;
    border-radius: 16px;
    box-shadow: 0 14px 30px rgba(0,0,0,.16);
    backdrop-filter: blur(10px);
    transition: transform .25s ease, border-color .25s ease;
}
.sidebar-status:hover { transform: translateY(-1px); border-color: rgba(110,231,183,.28); }
.sidebar-status .status-title { color:#ccfbf1; font-size:12px; font-weight:700; }
.sidebar-status .status-copy { color:#cbd5e1; font-size:11px; line-height:1.5; margin-top:4px; }

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


@keyframes fadeSlideIn {
    from { opacity: 0; transform: translateY(-4px); }
    to { opacity: 1; transform: translateY(0); }
}

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


/* ─────────────────────────────────────────────────────────────────────
   V26 IMAGE FIT POLISH
   Fixes the first-page campus hero and Project Team photo so the image
   fills the visual frame edge-to-edge without side gaps or letterboxing.
   Source photos are 16:9, so the cards now respect 16:9 on desktop.
   ───────────────────────────────────────────────────────────────────── */
.block-container {
    max-width: 1240px !important;
    padding-left: clamp(.85rem, 1.6vw, 1.35rem) !important;
    padding-right: clamp(.85rem, 1.6vw, 1.35rem) !important;
}
.hero {
    width: 100% !important;
    aspect-ratio: 16 / 9 !important;
    min-height: 420px !important;
    max-height: 560px !important;
    background-size: cover !important;
    background-position: center center !important;
    background-repeat: no-repeat !important;
}
.hero-content {
    min-height: 420px !important;
    height: 100% !important;
}
.team-photo-hero {
    width: 100% !important;
    aspect-ratio: 16 / 9 !important;
    min-height: unset !important;
    height: auto !important;
    background-size: cover !important;
    background-position: center center !important;
    background-repeat: no-repeat !important;
    background-color: transparent !important;
}
.team-photo-hero::before {
    content: "";
    position: absolute;
    inset: 0;
    z-index: 1;
    pointer-events: none;
    background:
        linear-gradient(90deg, rgba(2,6,23,.90) 0%, rgba(2,6,23,.58) 43%, rgba(2,6,23,.16) 72%, rgba(2,6,23,.18) 100%),
        linear-gradient(0deg, rgba(2,6,23,.64), rgba(2,6,23,.05) 55%) !important;
}
.team-photo-hero::after {
    z-index: 1;
    pointer-events: none;
}
.team-photo-content {
    z-index: 2 !important;
}
@media (max-width: 900px) {
    .hero {
        aspect-ratio: auto !important;
        min-height: 430px !important;
        max-height: none !important;
        background-position: center center !important;
    }
    .hero-content { min-height: 430px !important; }
    .team-photo-hero {
        aspect-ratio: 4 / 3 !important;
        background-size: cover !important;
        background-position: center center !important;
    }
}

/* grouped sidebar navigation */
.sidebar-group-hint {
    color:#64748b; font-size:11px; line-height:1.45; margin:8px 0 12px;
}
.nav-submenu {
    margin: 4px 0 14px 10px;
    padding-left: 10px;
    border-left: 1px solid rgba(96,165,250,.18);
}
.nav-submenu .stButton > button {
    min-height: 38px !important;
    font-size: 13px !important;
    padding-left: .85rem !important;
}



/* ─────────────────────────────────────────────────────────────────────
   V27 NAVIGATION + STUDENT MISSION POLISH
   Makes Learn / Teach / Project real section buttons and gives the
   Student Mission page a premium dashboard-style landing area.
   ───────────────────────────────────────────────────────────────────── */
.block-container {
    max-width: 1280px !important;
    padding-left: clamp(.9rem, 1.6vw, 1.4rem) !important;
    padding-right: clamp(.9rem, 1.6vw, 1.4rem) !important;
}
[data-testid="stSidebar"] .stButton > button[key^="nav_group_"] {
    min-height: 46px !important;
    margin-top: 8px !important;
    background: linear-gradient(135deg, rgba(15,23,42,.94), rgba(30,41,59,.72)) !important;
    border: 1px solid rgba(96,165,250,.20) !important;
    box-shadow: inset 0 1px 0 rgba(255,255,255,.04) !important;
    color: #eaf2ff !important;
    letter-spacing: .10em !important;
    text-transform: uppercase !important;
    font-size: 12px !important;
    font-weight: 850 !important;
}
[data-testid="stSidebar"] .stButton > button[key^="nav_group_"]:hover {
    background: linear-gradient(135deg, rgba(37,99,235,.28), rgba(14,165,233,.11)) !important;
    border-color: rgba(125,211,252,.36) !important;
}
.nav-submenu {
    margin: 8px 0 16px 10px !important;
    padding: 4px 0 4px 12px !important;
    border-left: 1px solid rgba(96,165,250,.28) !important;
}
.nav-submenu-note {
    color:#64748b;
    font-size:10px;
    text-transform:uppercase;
    letter-spacing:.12em;
    font-weight:800;
    margin: 12px 0 6px;
}
.sidebar-group-hint { display:none !important; }

.mission-landing {
    position: relative;
    overflow: hidden;
    border-radius: 30px;
    padding: 28px;
    margin: 10px 0 20px;
    border: 1px solid rgba(125,211,252,.18);
    background:
        radial-gradient(circle at 12% 0%, rgba(56,189,248,.18), transparent 31%),
        radial-gradient(circle at 85% 10%, rgba(124,58,237,.22), transparent 34%),
        linear-gradient(145deg, rgba(8,13,28,.97), rgba(15,23,42,.92));
    box-shadow: 0 26px 80px rgba(0,0,0,.34);
}
.mission-landing::after {
    content:"";
    position:absolute;
    inset:0;
    pointer-events:none;
    background: linear-gradient(90deg, rgba(255,255,255,.05) 0 1px, transparent 1px 70px),
                linear-gradient(0deg, rgba(255,255,255,.035) 0 1px, transparent 1px 70px);
    mask-image: linear-gradient(135deg, black, transparent 70%);
    opacity:.35;
}
.mission-landing-inner {
    position:relative;
    z-index:1;
    display:grid;
    grid-template-columns: 1.15fr .85fr;
    gap:22px;
    align-items:stretch;
}
.mission-kicker {
    display:inline-flex;
    align-items:center;
    gap:8px;
    padding:7px 12px;
    border-radius:999px;
    background:rgba(56,189,248,.10);
    border:1px solid rgba(56,189,248,.26);
    color:#7dd3fc;
    font-size:11px;
    font-weight:850;
    letter-spacing:.13em;
    text-transform:uppercase;
}
.mission-title {
    color:#f8fafc;
    font-size:38px;
    line-height:1.08;
    font-weight:900;
    margin:18px 0 12px;
    max-width:760px;
    letter-spacing:-.04em;
}
.mission-copy {
    color:#a8b4c7;
    font-size:15px;
    line-height:1.75;
    max-width:760px;
}
.mission-chip-row { display:flex; flex-wrap:wrap; gap:8px; margin-top:20px; }
.mission-chip {
    padding:8px 12px;
    border-radius:999px;
    background:rgba(15,23,42,.72);
    border:1px solid rgba(148,163,184,.14);
    color:#cbd5e1;
    font-size:12px;
    font-weight:700;
}
.mission-side-card {
    border-radius:24px;
    padding:20px;
    background:linear-gradient(145deg, rgba(15,23,42,.88), rgba(30,41,59,.62));
    border:1px solid rgba(148,163,184,.14);
    box-shadow: inset 0 1px 0 rgba(255,255,255,.04);
}
.side-title { color:#e2e8f0; font-size:15px; font-weight:850; margin-bottom:14px; }
.side-row { display:flex; align-items:center; justify-content:space-between; gap:12px; padding:11px 0; border-bottom:1px solid rgba(148,163,184,.08); }
.side-row:last-child { border-bottom:0; }
.side-label { color:#94a3b8; font-size:12px; }
.side-value { color:#f8fafc; font-size:13px; font-weight:800; }
.mission-form-title {
    margin: 26px 0 12px;
    display:flex;
    align-items:center;
    justify-content:space-between;
    gap:16px;
}
.mission-form-title h3 { color:#f8fafc; font-size:24px; margin:0; }
.mission-form-title span { color:#7c8da5; font-size:13px; }
.mission-form-box {
    border:1px solid rgba(96,165,250,.18);
    border-radius:24px;
    padding:18px 20px 8px;
    background:linear-gradient(145deg, rgba(15,23,42,.82), rgba(8,13,28,.94));
    box-shadow:0 20px 50px rgba(0,0,0,.20);
    margin-bottom: 18px;
}
.mission-output-card {
    border:1px solid rgba(52,211,153,.16);
    border-radius:18px;
    padding:16px;
    background:rgba(6,78,59,.08);
    margin-top:2px;
}
.mission-output-card b { color:#d1fae5; }
.mission-output-card div { color:#93a4b8; font-size:13px; padding:3px 0; }
.mission-metric-grid {
    display:grid;
    grid-template-columns: repeat(4, minmax(0,1fr));
    gap:14px;
    margin:22px 0;
}
.mission-metric-card {
    position:relative;
    overflow:hidden;
    border-radius:22px;
    padding:22px 20px;
    border:1px solid rgba(125,211,252,.14);
    background:linear-gradient(145deg, rgba(15,23,42,.92), rgba(30,41,59,.56));
    min-height:126px;
}
.mission-metric-card::after {
    content:"";
    position:absolute;
    width:120px; height:120px; right:-50px; top:-55px;
    border-radius:50%; background:rgba(56,189,248,.12);
}
.metric-big { color:#f8fafc; font-size:34px; font-weight:950; letter-spacing:-.04em; }
.metric-label { color:#71829a; font-size:11px; font-weight:850; text-transform:uppercase; letter-spacing:.11em; margin-top:14px; }
.metric-desc { color:#94a3b8; font-size:12px; line-height:1.45; margin-top:7px; }
.journey-grid {
    display:grid;
    grid-template-columns: repeat(3, minmax(0,1fr));
    gap:16px;
    margin:18px 0 6px;
}
.journey-card {
    position:relative;
    overflow:hidden;
    min-height:210px;
    padding:24px 22px;
    border-radius:26px;
    border:1px solid rgba(148,163,184,.14);
    background:linear-gradient(145deg, rgba(8,13,28,.96), rgba(15,23,42,.86));
    box-shadow:0 20px 45px rgba(0,0,0,.18);
}
.journey-card::before {
    content:attr(data-step);
    position:absolute;
    right:16px;
    top:10px;
    font-size:58px;
    line-height:1;
    font-weight:950;
    color:rgba(125,211,252,.07);
}
.journey-step { color:#38bdf8; font-size:11px; font-weight:900; letter-spacing:.14em; text-transform:uppercase; }
.journey-title { color:#f8fafc; font-size:22px; line-height:1.18; font-weight:900; margin:22px 0 10px; }
.journey-desc { color:#95a3b7; font-size:14px; line-height:1.65; }
@media(max-width:900px) {
    .mission-landing { padding:22px; border-radius:24px; }
    .mission-landing-inner { grid-template-columns:1fr; }
    .mission-title { font-size:30px; }
    .mission-metric-grid, .journey-grid { grid-template-columns:1fr; }
}


/* ─────────────────────────────────────────────────────────────────────
   V27.1 STABILITY FIX
   Separate Learn / Teach / Project blocks and lock the campus hero to
   the original 16:9 image ratio so the background does not jump/crop.
   ───────────────────────────────────────────────────────────────────── */
.hero {
    aspect-ratio: 16 / 9 !important;
    min-height: 0 !important;
    max-height: 640px !important;
    width: 100% !important;
    background-size: 100% 100% !important;
    background-position: center center !important;
    background-repeat: no-repeat !important;
}
.hero-content {
    height: 100% !important;
    min-height: 0 !important;
    max-width: 780px !important;
}
.hero-overlay {
    background:
        linear-gradient(105deg, rgba(2,6,23,.90) 0%, rgba(7,14,35,.76) 38%,
        rgba(15,23,62,.50) 66%, rgba(55,10,120,.34) 100%),
        radial-gradient(ellipse at 15% 50%, rgba(56,189,248,.16) 0%, transparent 50%) !important;
}
[data-testid="stSidebar"] .nav-label {
    margin-top: 1.35rem !important;
    padding-top: .9rem !important;
    border-top: 1px solid rgba(148,163,184,.08) !important;
}
[data-testid="stSidebar"] .nav-label:first-of-type {
    border-top: 0 !important;
}
.nav-submenu {
    margin: 7px 0 8px 12px !important;
    padding: 8px 0 8px 13px !important;
    border-left: 1px solid rgba(125,211,252,.28) !important;
    animation: fadeSlideIn .24s ease;
}
@media(max-width:900px) {
    .hero {
        aspect-ratio: auto !important;
        min-height: 430px !important;
        background-size: cover !important;
    }
    .hero-content {
        min-height: 430px !important;
        height: auto !important;
        max-width: 100% !important;
    }
}

/* V27.8 cleanup: remove inactive student notification panel */
.sidebar-profile { display: none !important; }
[data-testid="stSidebar"] .nav-label { color:#f8fafc !important; text-shadow:0 2px 16px rgba(0,0,0,.85) !important; }
[data-testid="stSidebar"] .stButton > button { background: rgba(2,6,23,.34) !important; backdrop-filter: blur(8px); }
[data-testid="stSidebar"] .stButton > button:hover { background: rgba(59,130,246,.20) !important; }



/* V27.7 final sidebar + page polish */
[data-testid="stSidebar"] {
    background:
        linear-gradient(180deg, rgba(2,6,23,.24) 0%, rgba(2,6,23,.32) 28%, rgba(2,6,23,.46) 58%, rgba(2,6,23,.62) 100%),
        radial-gradient(circle at 50% 73%, rgba(251,191,36,.32) 0%, rgba(251,191,36,.14) 18%, transparent 38%),
        url('__SIDEBAR_BG__') !important;
    background-size: auto, auto, auto 106% !important;
    background-position: center, center, 50% 100% !important;
    background-repeat: no-repeat !important;
}
[data-testid="stSidebar"] > div:first-child {
    background: linear-gradient(180deg, rgba(2,6,23,.02), rgba(2,6,23,.08)) !important;
    backdrop-filter: none !important;
}
.sidebar-profile { display:none !important; }
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] .stMarkdown h2 {
    font-size: 22px !important;
    letter-spacing: -.025em !important;
    margin-top: 10px !important;
    text-shadow: 0 3px 18px rgba(0,0,0,.75) !important;
}
[data-testid="stSidebar"] .stCaptionContainer,
[data-testid="stSidebar"] p {
    text-shadow: 0 2px 14px rgba(0,0,0,.75) !important;
}
[data-testid="stSidebar"] .stButton > button {
    min-height: 45px !important;
    border-radius: 15px !important;
    background: rgba(3,7,18,.38) !important;
    border: 1px solid rgba(255,255,255,.08) !important;
    box-shadow: 0 12px 30px rgba(0,0,0,.18) !important;
    backdrop-filter: blur(5px) !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(37,99,235,.26) !important;
    border-color: rgba(125,211,252,.38) !important;
    transform: translateX(4px) scale(1.01) !important;
}
[data-testid="stSidebar"] .stButton > button[kind="primary"] {
    background: linear-gradient(135deg, rgba(37,99,235,.52), rgba(124,58,237,.44)) !important;
    border: 1px solid rgba(147,197,253,.52) !important;
    box-shadow: 0 16px 38px rgba(37,99,235,.24) !important;
}
[data-testid="stSidebar"] .nav-label {
    margin-top: 1.45rem !important;
    color: #e0f2fe !important;
    text-shadow: 0 3px 18px rgba(0,0,0,.95) !important;
}
.nav-submenu {
    border-left: 1px solid rgba(147,197,253,.36) !important;
    animation: fadeSlideIn .22s ease !important;
}
.sidebar-status {
    background: rgba(3,7,18,.28) !important;
    border-color: rgba(110,231,183,.16) !important;
    backdrop-filter: blur(5px) !important;
}

/* clean page polish for weaker screens */
.ai-chat-shell {
    border: 1px solid rgba(125,211,252,.14) !important;
    background: linear-gradient(145deg, rgba(8,13,28,.96), rgba(15,23,42,.82)) !important;
    border-radius: 26px !important;
    padding: 22px !important;
}
.chat-user {
    box-shadow: 0 14px 34px rgba(79,70,229,.26) !important;
}
.ai-main-answer {
    max-width: 86% !important;
    border-color: rgba(125,211,252,.16) !important;
    background: linear-gradient(145deg, rgba(15,23,42,.95), rgba(30,41,59,.70)) !important;
}
.assignment-card {
    border-color: rgba(125,211,252,.16) !important;
    background: linear-gradient(145deg, rgba(15,23,42,.88), rgba(8,13,28,.96)) !important;
    box-shadow: 0 20px 46px rgba(0,0,0,.16) !important;
}
[data-testid="stExpander"] {
    border: 1px solid rgba(125,211,252,.14) !important;
    border-radius: 16px !important;
    background: rgba(15,23,42,.52) !important;
}


/* V27.9 hard clean: remove unused sidebar notification/profile block completely from view */
.sidebar-profile, div.sidebar-profile { display: none !important; height:0 !important; min-height:0 !important; margin:0 !important; padding:0 !important; border:0 !important; overflow:hidden !important; }
[data-testid="stSidebar"] {
    background-size: auto, auto, auto 112% !important;
    background-position: center, center, 50% 102% !important;
}



/* V28.1 final cinematic landing and safe image fitting */
.hero {
    aspect-ratio: 16 / 9 !important;
    min-height: 470px !important;
    max-height: 690px !important;
    background-size: cover !important;
    background-position: center center !important;
    background-repeat: no-repeat !important;
    margin-top: .15rem !important;
}
.hero-home {
    min-height: 570px !important;
    box-shadow: 0 34px 90px rgba(0,0,0,.55), inset 0 0 0 1px rgba(125,211,252,.08) !important;
}
.hero-home .hero-content {
    min-height: 570px !important;
    padding: 54px 58px !important;
}
.hero-home .hero-overlay {
    background:
        linear-gradient(105deg, rgba(2,6,23,.94) 0%, rgba(7,14,35,.80) 36%, rgba(15,23,62,.44) 66%, rgba(55,10,120,.26) 100%),
        radial-gradient(ellipse at 20% 24%, rgba(56,189,248,.20) 0%, transparent 42%),
        radial-gradient(ellipse at 88% 12%, rgba(167,139,250,.16) 0%, transparent 36%) !important;
}
.hero-signature {
    position: absolute;
    right: 34px;
    bottom: 28px;
    z-index: 3;
    padding: 12px 16px;
    border-radius: 18px;
    border: 1px solid rgba(255,255,255,.14);
    background: rgba(2,6,23,.38);
    backdrop-filter: blur(12px);
    color: #dbeafe;
    font-size: 12px;
    line-height: 1.45;
    text-align: right;
    box-shadow: 0 16px 36px rgba(0,0,0,.24);
}
.hero-signature b { display:block; color:#f8fafc; font-size:13px; }
.home-clean-note {
    margin: 18px 2px 0;
    color: #64748b;
    font-size: 12px;
    letter-spacing: .08em;
    text-transform: uppercase;
    font-weight: 800;
}
.page-intro { margin-top: .15rem !important; }
.sec-head { margin-top: 1.2rem !important; }
.team-photo-hero {
    aspect-ratio: 16 / 9 !important;
    min-height: 520px !important;
    background-size: cover !important;
    background-position: center center !important;
    margin-top: .3rem !important;
}
.team-photo-hero::before {
    content:"";
    position:absolute;
    inset:0;
    z-index:1;
    pointer-events:none;
    background:
      linear-gradient(90deg, rgba(2,6,23,.62) 0%, rgba(2,6,23,.30) 28%, rgba(2,6,23,.06) 58%, rgba(2,6,23,.12) 100%),
      linear-gradient(0deg, rgba(2,6,23,.30), transparent 52%) !important;
}
.team-photo-content {
    top: 34px !important;
    left: 34px !important;
    bottom: auto !important;
    right: auto !important;
    max-width: 470px !important;
    padding: 22px 24px !important;
    border-radius: 22px !important;
    border: 1px solid rgba(255,255,255,.16) !important;
    background: rgba(2,6,23,.38) !important;
    backdrop-filter: blur(12px) !important;
    box-shadow: 0 18px 42px rgba(0,0,0,.26) !important;
}
.team-photo-content h1 {
    font-size: 34px !important;
    line-height: 1.08 !important;
    margin: 10px 0 8px !important;
}
.team-photo-content p { font-size: 13px !important; line-height:1.58 !important; max-width:420px !important; }
.team-school-line { color:#93c5fd; font-size:12px; font-weight:800; letter-spacing:.08em; text-transform:uppercase; }
@media(max-width:900px){
    .hero, .hero-home { aspect-ratio:auto !important; min-height: 510px !important; }
    .hero-home .hero-content { min-height: 510px !important; padding: 34px 26px !important; }
    .hero-signature { left: 24px; right:24px; text-align:left; bottom:22px; }
    .team-photo-hero { aspect-ratio: 4/3 !important; min-height: 430px !important; }
    .team-photo-content { top:22px !important; left:22px !important; right:22px !important; max-width:none !important; }
}


/* V28.2 cinematic home: one strong visual, no boxed/text-dump feeling */
.hero-home {
    min-height: calc(100vh - 92px) !important;
    border-radius: 34px !important;
    border: 1px solid rgba(125,211,252,.16) !important;
    box-shadow: 0 38px 100px rgba(0,0,0,.62), inset 0 0 80px rgba(2,6,23,.28) !important;
    margin: 0 auto 0 !important;
    background-position: center center !important;
}
.hero-home .hero-content {
    min-height: calc(100vh - 92px) !important;
    padding: 56px 58px !important;
    max-width: 820px !important;
}
.hero-home .hero-overlay {
    background:
        linear-gradient(100deg, rgba(2,6,23,.96) 0%, rgba(2,6,23,.82) 30%, rgba(15,23,42,.48) 58%, rgba(15,23,42,.12) 100%),
        radial-gradient(ellipse at 18% 22%, rgba(56,189,248,.22) 0%, transparent 42%),
        radial-gradient(ellipse at 88% 16%, rgba(167,139,250,.18) 0%, transparent 38%) !important;
}
.hero-home .hero-badge { margin-top: 6px !important; }
.hero-home h1 {
    font-size: clamp(42px, 5vw, 76px) !important;
    max-width: 880px !important;
    line-height: .98 !important;
    margin-top: 28px !important;
}
.hero-home .hero-sub {
    max-width: 720px !important;
    font-size: 18px !important;
    line-height: 1.72 !important;
    color: #e2e8f0 !important;
    margin-top: 22px !important;
}
.hero-home .hero-stats {
    margin-top: 42px !important;
    gap: 18px !important;
    padding: 12px !important;
    width: fit-content !important;
    border-radius: 22px !important;
    background: rgba(2,6,23,.28) !important;
    border: 1px solid rgba(255,255,255,.08) !important;
    backdrop-filter: blur(10px) !important;
}
.hero-home .hero-stats > div {
    min-width: 108px !important;
    padding: 8px 12px !important;
    border-radius: 16px !important;
    background: rgba(15,23,42,.30) !important;
}
.hero-signature {
    right: 34px !important;
    bottom: 30px !important;
    background: linear-gradient(145deg, rgba(15,23,42,.48), rgba(2,6,23,.34)) !important;
    border-color: rgba(255,255,255,.16) !important;
}
.home-clean-note { display: none !important; }

/* V28.2 team page: keep all faces visible, make text small and low */
.team-photo-hero {
    min-height: 560px !important;
    aspect-ratio: 16 / 9 !important;
    background-size: cover !important;
    background-position: center 38% !important;
    border-radius: 32px !important;
    overflow: hidden !important;
}
.team-photo-hero::before {
    background:
        linear-gradient(0deg, rgba(2,6,23,.68) 0%, rgba(2,6,23,.18) 38%, rgba(2,6,23,.02) 70%),
        linear-gradient(90deg, rgba(2,6,23,.18) 0%, rgba(2,6,23,.04) 35%, rgba(2,6,23,.02) 100%) !important;
}
.team-photo-hero::after {
    background: linear-gradient(0deg, rgba(2,6,23,.62), transparent 48%) !important;
}
.team-photo-content {
    top: auto !important;
    left: 32px !important;
    bottom: 28px !important;
    right: auto !important;
    max-width: 500px !important;
    padding: 18px 20px !important;
    border-radius: 20px !important;
    background: rgba(2,6,23,.36) !important;
    border: 1px solid rgba(255,255,255,.13) !important;
    backdrop-filter: blur(12px) !important;
}
.team-photo-content h1 {
    font-size: 28px !important;
    line-height: 1.1 !important;
    margin: 8px 0 8px !important;
    max-width: 460px !important;
}
.team-photo-content p {
    font-size: 12px !important;
    line-height: 1.55 !important;
    max-width: 440px !important;
    color: #e2e8f0 !important;
}
.team-school-line { font-size: 10.5px !important; margin-top: 7px !important; }

/* keep page starts clean; no header cuts */
.page-intro { margin-top: .65rem !important; padding-top: 34px !important; }
.sec-head { margin-top: 1.6rem !important; }

@media(max-width:900px){
    .hero-home, .hero-home .hero-content { min-height: 560px !important; }
    .hero-home .hero-content { padding: 36px 26px !important; }
    .hero-home .hero-stats { width: 100% !important; flex-wrap: wrap !important; }
    .hero-signature { left: 24px !important; right: 24px !important; text-align:left !important; }
    .team-photo-hero { min-height: 470px !important; background-position: center 35% !important; }
    .team-photo-content { left: 18px !important; right:18px !important; bottom:18px !important; max-width:none !important; }
}

</style>
"""
CSS = CSS.replace("__SIDEBAR_BG__", SIDEBAR_URI or CAMPUS_URI)
st.markdown(CSS, unsafe_allow_html=True)


# ── helpers ─────────────────────────────────────────────────────────────────

def init_state():
    st.session_state.setdefault("student", "Student")
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
        "selected_homework_id", "ai_context_note", "nav_group",
    ]
    for key in keys:
        st.session_state.pop(key, None)



def _nav_button(label: str, page_name: str) -> None:
    is_active = st.session_state.get("active_page") == page_name
    if st.sidebar.button(label, key=f"nav_{page_name}", use_container_width=True, type="primary" if is_active else "secondary"):
        st.session_state.active_page = page_name
        st.session_state.nav_group = _page_to_group(page_name)
        st.rerun()


def _page_to_group(page_name: str) -> str:
    if page_name == "Home":
        return ""
    groups = {
        "Learn": {"Student Mission", "My Homework", "Ask Preluma AI"},
        "Teach": {"Teacher Studio", "Homework Center"},
        "Project": {"Evidence Board", "Professor Defense", "Project Team", "Demo Guide", "Future Roadmap"},
    }
    for group_name, pages in groups.items():
        if page_name in pages:
            return group_name
    return ""


def _nav_group_button(group_name: str) -> None:
    current_group = st.session_state.get("nav_group", "")
    label = f"Open {group_name} {'▾' if current_group == group_name else '▸'}"
    is_open = current_group == group_name
    if st.sidebar.button(label, key=f"nav_group_{group_name}", use_container_width=True, type="primary" if is_open else "secondary"):
        st.session_state.nav_group = "" if current_group == group_name else group_name
        st.rerun()


def _nav_submenu(items: list[tuple[str, str]]) -> None:
    st.sidebar.markdown("<div class='nav-submenu'>", unsafe_allow_html=True)
    for label, page_name in items:
        _nav_button(label, page_name)
    st.sidebar.markdown("</div>", unsafe_allow_html=True)


def sidebar():
    st.sidebar.markdown("## Preluma")
    st.sidebar.caption("Light Up Before Class")
    st.session_state.setdefault("active_page", "Home")
    st.session_state.setdefault("nav_group", "")
    # Three separated navigation groups.
    # Only the clicked group opens; sub-pages are hidden until the group is opened.
    if not st.session_state.get("nav_group"):
        st.session_state.nav_group = _page_to_group(st.session_state.get("active_page", "Home"))

    nav_groups = {
        "Learn": [
            ("Student Mission", "Student Mission"),
            ("My Homework", "My Homework"),
            ("Ask Preluma AI", "Ask Preluma AI"),
        ],
        "Teach": [
            ("Teacher Studio", "Teacher Studio"),
            ("Homework Center", "Homework Center"),
        ],
        "Project": [
            ("Evidence Board", "Evidence Board"),
            ("Professor Defense", "Professor Defense"),
            ("Project Team", "Project Team"),
            ("Demo Guide", "Demo Guide"),
            ("Future Roadmap", "Future Roadmap"),
        ],
    }

    if st.sidebar.button("Home", key="nav_home", use_container_width=True, type="primary" if st.session_state.get("active_page") == "Home" else "secondary"):
        st.session_state.active_page = "Home"
        st.session_state.nav_group = ""
        st.rerun()

    st.sidebar.markdown("<div class='nav-label'>Learn</div>", unsafe_allow_html=True)
    _nav_group_button("Learn")
    if st.session_state.get("nav_group") == "Learn":
        _nav_submenu(nav_groups["Learn"])

    st.sidebar.markdown("<div class='nav-label'>Teach</div>", unsafe_allow_html=True)
    _nav_group_button("Teach")
    if st.session_state.get("nav_group") == "Teach":
        _nav_submenu(nav_groups["Teach"])

    st.sidebar.markdown("<div class='nav-label'>Project</div>", unsafe_allow_html=True)
    _nav_group_button("Project")
    if st.session_state.get("nav_group") == "Project":
        _nav_submenu(nav_groups["Project"])

    presentation = st.sidebar.toggle("Presentation Mode", value=True)

    st.sidebar.markdown(
        """
        <div class='sidebar-status'>
            <div class='status-title'>Preluma AI ready</div>
            <div class='status-copy'>Ready for lessons, homework help, and exam preparation.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.sidebar.button("Reset session", use_container_width=True):
        reset_session()
        st.session_state.active_page = "Home"
        st.session_state.nav_group = ""
        st.rerun()

    st.sidebar.caption(f"v{APP_VERSION}")
    return st.session_state.active_page, presentation

# ── Hero ─────────────────────────────────────────────────────────────────────

def hero(show_signature: bool = False, home: bool = False):
    bg = f"url('{CAMPUS_URI}')" if CAMPUS_URI else "linear-gradient(135deg,#020617,#0f172a,#1e1b4b)"
    provider = _provider()
    ai_pill = f"<span class='ai-pill'>AI: {provider}</span>" if provider != "none" else ""

    signature = """<div class='hero-signature'><b>School of Software and Artificial Intelligence</b>Yunnan University</div>""" if show_signature else ""
    hero_class = "hero hero-home" if home else "hero"

    st.markdown(f"""
    <div class='{hero_class}' style="background-image:{bg};">
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
      {signature}
    </div>""", unsafe_allow_html=True)


# ── Progress ──────────────────────────────────────────────────────────────────

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
        prefix = "✓ " if done else ""
        html += f"<div class='progress-step {c}'>{prefix}{label}</div>"
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)

def chip_row():
    labels = ["Topic","Brain Brief","All Concepts","Quiz","Mistake Clinic","UltraTutor","Class Questions","Readiness Score"]
    st.markdown("<div class='chip-row'>" + "".join(f"<span class='chip'>{l}</span>" for l in labels) + "</div>", unsafe_allow_html=True)


# ── Mission Control ───────────────────────────────────────────────────────────

def mission_control():
    provider = _provider()
    provider_label = provider if provider != "none" else "Offline fallback"

    st.markdown(
        f"""
        <section class='mission-landing'>
            <div class='mission-landing-inner'>
                <div>
                    <div class='mission-kicker'>Pre-class mission control</div>
                    <div class='mission-title'>Turn a lecture topic into a guided learning mission.</div>
                    <div class='mission-copy'>Choose a topic, select the tutor style, and Preluma prepares a Brain Brief, concept practice, mini mock test, readiness score, and class questions before the lecture starts.</div>
                    <div class='mission-chip-row'>
                        <span class='mission-chip'>Brain Brief</span>
                        <span class='mission-chip'>Skill Check</span>
                        <span class='mission-chip'>UltraTutor</span>
                        <span class='mission-chip'>CSV Evidence</span>
                    </div>
                </div>
                <div class='mission-side-card'>
                    <div class='side-title'>Live system status</div>
                    <div class='side-row'><span class='side-label'>AI provider</span><span class='side-value'>{provider_label}</span></div>
                    <div class='side-row'><span class='side-label'>Data mode</span><span class='side-value'>CSV persistence</span></div>
                    <div class='side-row'><span class='side-label'>Backend rule</span><span class='side-value'>Pure Python core</span></div>
                    <div class='side-row'><span class='side-label'>Mission steps</span><span class='side-value'>5 stages</span></div>
                </div>
            </div>
        </section>
        <div class='mission-form-title'>
            <h3>Build your mission</h3>
            <span>Fast setup for student demo or manual topic input</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    preset = st.selectbox(
        "Demo preset",
        ["Manual Input", "AI Class Demo", "Python Exam Demo", "Statistics Viva Demo"],
        index=0,
    )

    preset_data = {
        "AI Class Demo": (
            "Amir",
            "Neural Network",
            "Tomorrow 9 AM",
            "Coach Mode",
            "Deep Understanding",
        ),
        "Python Exam Demo": (
            "Jia",
            "Python Programming",
            "Tomorrow 9 AM",
            "Normal Mode",
            "Exam/Viva Mode",
        ),
        "Statistics Viva Demo": (
            "Nadia",
            "Statistics",
            "Tomorrow 9 AM",
            "Coach Mode",
            "Exam/Viva Mode",
        ),
    }

    ds, dt, dtime, dp, dm = preset_data.get(
        preset,
        (
            "",
            st.session_state.topic,
            "Tomorrow 9 AM",
            st.session_state.persona,
            "Fast Review",
        ),
    )

    st.markdown("<div class='mission-form-box'>", unsafe_allow_html=True)
    with st.form("mission_form", border=False):
        c1, c2, c3 = st.columns([1.25, 1.05, 0.95], gap="large")

        with c1:
            st.markdown("**Student setup**")
            student = st.text_input("Your name", value="" if ds == "Student" else ds, placeholder="Please write your name")

            topic_choice = st.selectbox(
                "Lecture topic",
                TOPIC_OPTIONS,
                index=TOPIC_OPTIONS.index(dt) if dt in TOPIC_OPTIONS else 0,
            )

            if topic_choice == "Custom Topic":
                topic = st.text_input(
                    "Custom topic",
                    placeholder="e.g. Reinforcement Learning",
                )
            else:
                topic = topic_choice

            lecture_time = st.text_input("Lecture time", value=dtime)

        with c2:
            st.markdown("**Tutor behavior**")
            persona = st.radio(
                "Tutor personality",
                ["Normal Mode", "Coach Mode", "Roast Mode"],
                captions=[
                    "Clear and direct",
                    "Warm and motivating",
                    "Light humour",
                ],
                index=["Normal Mode", "Coach Mode", "Roast Mode"].index(dp)
                if dp in ["Normal Mode", "Coach Mode", "Roast Mode"]
                else 0,
            )

            learning_mode = st.selectbox(
                "Learning mode",
                ["Fast Review", "Deep Understanding", "Exam/Viva Mode"],
                index=["Fast Review", "Deep Understanding", "Exam/Viva Mode"].index(dm)
                if dm in ["Fast Review", "Deep Understanding", "Exam/Viva Mode"]
                else 0,
            )

        with c3:
            st.markdown("**Mission output**")
            use_wiki = st.checkbox("Wikipedia real data", value=True)
            st.markdown(
                """
                <div class='mission-output-card'>
                    <b>Output package</b>
                    <div>01 Brain Brief</div>
                    <div>02 Concept explanation</div>
                    <div>03 Practice step</div>
                    <div>04 Mini mock test</div>
                    <div>05 Final overview</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        start = st.form_submit_button(
            "Start Pre-Class Mission",
            use_container_width=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)

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

        st.session_state.update(
            {
                "student": student.strip() or "Learner",
                "topic": topic,
                "persona": persona,
                "learning_mode": learning_mode,
                "use_wiki": use_wiki,
                "pack": pack,
                "brief": brief,
                "questions": questions,
                "class_questions": class_qs,
                "quiz_result": None,
                "latest_session": None,
                "tutor_history": [],
                "mission_started": True,
                "mission_step": 1,
                "practice_reflection": "",
            }
        )

        st.rerun()


# ── Brain Brief ───────────────────────────────────────────────────────────────

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
          <div class='sec-icon' style='background:rgba(251,191,36,.10);'>📖</div>
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


# ── Quiz ──────────────────────────────────────────────────────────────────────

def quiz():
    if "questions" not in st.session_state: return
    st.markdown("""<div class='sec-head'>
      <div class='sec-icon' style='background:rgba(34,211,238,.10);'>⚡</div>
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
            "Quiz Total": result["total"],
            "Lecture Time": st.session_state.get("lecture_time", "Tomorrow 9 AM"),
            "Learning Mode": st.session_state.get("learning_mode","Fast Review"), "Created At": timestamp(),
        })
        st.rerun()


# ── Result ────────────────────────────────────────────────────────────────────

def result_section():
    result = st.session_state.get("quiz_result")
    if not result: return

    pct       = result["pct"]
    pill_cls, color = _rc(pct)
    label     = _rl(pct)

    st.markdown("""<div class='sec-head'>
      <div class='sec-icon' style='background:rgba(52,211,153,.10);'>📊</div>
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
      <div class='sec-icon' style='background:rgba(248,113,113,.10);'>🔬</div>
      <div><div class='sec-title'>Mistake Clinic</div><div class='sec-sub'>Every wrong answer explained clearly</div></div>
    </div>""", unsafe_allow_html=True)

    for i, d in enumerate(result["details"], 1):
        ok = d["correct"]
        with st.expander(f"{'✓' if ok else '✗'} Q{i}: {d['skill']} — {'Correct' if ok else 'Review needed'}"):
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


# ── Smart QnA + UltraTutor ────────────────────────────────────────────────────

def smart_qna():
    if "pack" not in st.session_state: return

    st.markdown("""<div class='sec-head'>
      <div class='sec-icon' style='background:rgba(99,102,241,.12);'>🤖</div>
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


# ── Class Questions ───────────────────────────────────────────────────────────

def class_questions_and_download():
    if "pack" not in st.session_state: return
    st.markdown("""<div class='sec-head'>
      <div class='sec-icon' style='background:rgba(34,211,238,.10);'>💬</div>
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


# ── How it works ──────────────────────────────────────────────────────────────

def how_it_works():
    st.markdown(
        """
        <div class='mission-metric-grid'>
            <div class='mission-metric-card'>
                <div class='metric-big'>18</div>
                <div class='metric-label'>Curated topics</div>
                <div class='metric-desc'>Ready-made academic topics for quick classroom demos.</div>
            </div>
            <div class='mission-metric-card'>
                <div class='metric-big'>4</div>
                <div class='metric-label'>Skill checks</div>
                <div class='metric-desc'>Focused quiz items to detect weak concepts fast.</div>
            </div>
            <div class='mission-metric-card'>
                <div class='metric-big'>AI</div>
                <div class='metric-label'>Smart tutor</div>
                <div class='metric-desc'>Adaptive explanation with local fallback support.</div>
            </div>
            <div class='mission-metric-card'>
                <div class='metric-big'>CSV</div>
                <div class='metric-label'>Evidence data</div>
                <div class='metric-desc'>Student readiness records saved for teacher review.</div>
            </div>
        </div>
        <div class='journey-grid'>
            <div class='journey-card' data-step='01'>
                <div class='journey-step'>Step 1</div>
                <div class='journey-title'>Prime the brain</div>
                <div class='journey-desc'>Preluma creates a short Brain Brief so the student enters class with the core idea already prepared.</div>
            </div>
            <div class='journey-card' data-step='02'>
                <div class='journey-step'>Step 2</div>
                <div class='journey-title'>Find weak spots</div>
                <div class='journey-desc'>A mini quiz detects the exact concept that needs review instead of giving a random score only.</div>
            </div>
            <div class='journey-card' data-step='03'>
                <div class='journey-step'>Step 3</div>
                <div class='journey-title'>Ask better questions</div>
                <div class='journey-desc'>The final overview gives readiness, weak skill, and class questions that prove preparation.</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ── Student Mission ───────────────────────────────────────────────────────────

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
    st.markdown("""<div class='sec-head'>
      <div class='sec-icon' style='background:rgba(239,68,68,.15);'>04</div>
      <div><div class='sec-title'>Step 4 · Mini Mock Test</div>
      <div class='sec-sub'>Check understanding before entering the lecture</div></div>
    </div>""", unsafe_allow_html=True)

    questions = st.session_state.questions
    if st.session_state.get("quiz_result"):
        result = st.session_state.quiz_result
        st.success(f"Submitted: {result['score']}/{result['total']} correct · {result['pct']}% readiness")
        for index, detail in enumerate(result["details"], 1):
            status = "Correct" if detail["correct"] else "Review"
            with st.expander(f"Question {index} · {status} · {detail['skill']}"):
                st.write(f"Your answer: {detail['chosen'] or 'No answer'}")
                st.write(f"Correct answer: {detail['answer']}")
                st.info(detail["why"])
        _mission_navigation(3, 5, "View Final Overview")
        return

    with st.form("guided_mock_test", border=False):
        answers = {}
        for index, question in enumerate(questions):
            st.markdown(
                f"<div class='card-glass'><div class='albl lbl-red'>"
                f"{question['skill']}</div><div class='atxt'>{question['q']}</div></div>",
                unsafe_allow_html=True,
            )
            answers[index] = st.radio(
                "Choose one",
                question["options"],
                key=f"guided_quiz_{index}",
                label_visibility="collapsed",
            )
        submitted = st.form_submit_button("Submit Mock Test", use_container_width=True)

    if submitted:
        result = grade(questions, answers)
        _save_mission_quiz_result(result)
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



def home_page(presentation=True):
    """Landing page only: one cinematic brand impression."""
    hero(show_signature=True, home=True)


def student_mission(presentation):
    if not st.session_state.get("mission_started") or "pack" not in st.session_state:
        page_intro(
            "teacher",
            "Learning workspace",
            "Student Mission",
            "Build a focused study route before class. Enter your name, choose a lecture topic, and start a guided mission."
        )
        mission_control()
        if presentation:
            how_it_works()
        return

    step = st.session_state.get("mission_step", 1)

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

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


# ── Teacher Studio

# ── Teacher Studio ────────────────────────────────────────────────────────────

def teacher_studio():
    hero()
    st.markdown("""<div class='sec-head'>
      <div class='sec-icon' style='background:rgba(56,189,248,.12);'>👩‍🏫</div>
      <div><div class='sec-title'>Teacher Studio</div><div class='sec-sub'>Manual Python algorithms: Merge Sort, Binary Search, CSV persistence, audit log</div></div>
    </div>""", unsafe_allow_html=True)

    rows      = build_teacher_dataframe(st.session_state.get("latest_session"))
    analytics = teacher_analytics(rows)
    summary   = analytics["summary"]

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



def _question_needs_clarification(question: str) -> bool:
    text = " ".join(str(question).strip().split())
    if not text:
        return True
    cleaned = text.casefold().strip(" ?.,!")
    ambiguous_only = {
        "help", "explain", "tell me", "more", "details",
        "why", "how", "this", "it", "i do not understand",
    }
    return cleaned in ambiguous_only

def _is_casual_query(question: str) -> bool:
    """Return True for greetings or social chat that should not be routed as a lesson topic."""
    cleaned = " ".join(str(question).strip().casefold().replace("?", "").replace("!", "").split())
    casual_phrases = {
        "hi", "hello", "hey", "hi there", "hello there",
        "how are you", "hi how are you", "hello how are you",
        "good morning", "good afternoon", "good evening", "thanks", "thank you",
    }
    return cleaned in casual_phrases


def _casual_ai_answer(question: str) -> str:
    cleaned = " ".join(str(question).strip().casefold().split())
    if "how are you" in cleaned:
        return (
            "I’m doing well and ready to help. "
            "You can ask me about today’s lecture, a homework question, or an exam topic. "
            "For example: ‘Explain quantum mechanics simply’ or ‘Quiz me on neural networks.’"
        )
    return (
        "Hi! I’m Preluma AI. I can help you prepare before class, understand a difficult concept, "
        "review homework mistakes, or practice exam-style questions. What topic are you studying today?"
    )


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

    current_pack = st.session_state.get("pack")
    mission_topic = current_pack.get("title") if current_pack else st.session_state.get("topic", "General learning")
    providers = available_providers()
    provider_label = _provider()

    top1, top2, top3 = st.columns([1.2, 1, 1])
    with top1:
        use_context = st.toggle("Use current study context", value=True)
    with top2:
        mode = st.selectbox("Tutor style", ["Auto-detect", "Explain like I am 5", "Friendly Tutor", "Step-by-Step", "Exam/Viva Answer", "Give More Examples"])
    with top3:
        depth = st.selectbox("Answer depth", ["Balanced", "Short", "Deep"])

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
        if _is_casual_query(question):
            st.session_state.tutor_history.append({
                "question": question.strip(),
                "topic": "Preluma AI",
                "casual": True,
                "answer_text": _casual_ai_answer(question),
                "source": "Natural greeting",
            })
            st.rerun()
        detected_topic = detect_topic_from_question(question, mission_topic if use_context else "General learning")
        if _question_needs_clarification(question):
            st.session_state.tutor_history.append({
                "question": question.strip(),
                "topic": detected_topic,
                "clarification": True,
                "answer_text": "I can help, but I need one detail first: do you want a simple overview, a deep explanation of how it works, a real-life example, or an exam-ready answer?",
                "source": "Preluma intent check",
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
                source = f"AI provider: {_provider()}" if response else "Curated + Wikipedia fallback"
                if response is None:
                    fallback_pack = build_pack(detected_topic, use_wikipedia=True)
                    response = tutor_sections(fallback_pack, routed_question, st.session_state.get("persona", "Normal Mode"))
            response["concept"] = detected_topic
            answer_text = _natural_answer_text(response, depth)
            st.session_state.tutor_history.append({"question":question.strip(),"topic":detected_topic,"response":response,"answer_text":answer_text,"source":source,"depth":depth})

    st.markdown("<div class='ai-chat-shell'>", unsafe_allow_html=True)
    for index, item in enumerate(st.session_state.get("tutor_history", [])[-8:]):
        st.markdown(f"<div class='chat-user'>{item['question']}</div>", unsafe_allow_html=True)
        if not item.get("casual"):
            st.markdown(f"<div class='ai-meta'>Tutor response · {item['topic']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='ai-main-answer'>{item.get('answer_text','')}</div>", unsafe_allow_html=True)
        if not item.get("clarification") and not item.get("casual"):
            response = item.get("response", {})
            with st.expander("Study support: mistake, exam line, and extra details"):
                if response.get("common_mistake"):
                    st.markdown(f"**Common mistake:** {response['common_mistake']}")
                if response.get("exam_angle"):
                    st.markdown(f"**Exam/Viva memory line:** {response['exam_angle']}")
                if response.get("real_life_example"):
                    st.markdown(f"**Example:** {response['real_life_example']}")
    st.markdown("</div>", unsafe_allow_html=True)


def _reset_homework_flow(homework_id: str) -> None:
    st.session_state.hw_active_id = str(homework_id)
    st.session_state.hw_step = 0
    st.session_state.hw_answers = {}
    st.session_state.homework_result = None


def _homework_progress(current: int, total: int) -> None:
    value = (current + 1) / total if total else 0
    st.progress(value, text=f"Question {current + 1} of {total}")


def my_homework_page():
    student = st.session_state.get("student", "Student")

    page_intro(
        "homework",
        "Student assignment desk",
        "My Homework",
        "Complete homework one question at a time, review your answers, submit, and learn from captured mistakes.",
    )

    homework_rows = homework_for_student(student)

    # Opening the homework desk counts as viewing homework notifications.
    mark_homework_notifications_read(student)

    if not homework_rows:
        st.info("No homework has been assigned to this student yet.")
        return

    labels = {
        f"#{row['Homework ID']} · {row['Title']} · Due {row['Due Date']}": row
        for row in homework_rows
    }

    selected_label = st.selectbox("Choose homework", list(labels))
    selected = labels[selected_label]
    homework_id = str(selected["Homework ID"])

    if st.session_state.get("hw_active_id") != homework_id:
        _reset_homework_flow(homework_id)

    questions = load_questions(homework_id)

    if not questions:
        st.warning("This homework has no questions.")
        return

    st.markdown(
        f"""
        <div class='assignment-card'>
          <div class='albl lbl-purple'>{selected.get('Topic')}</div>
          <div class='atxt'>
            <b>{selected.get('Title')}</b><br>
            {selected.get('Instructions')}
          </div>
          <div style='margin-top:12px;color:#94a3b8;font-size:13px;'>
            Due: {selected.get('Due Date')} · Difficulty: {selected.get('Difficulty')}
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    result = st.session_state.get("homework_result")

    if result:
        st.markdown(
            f"""
            <div class='mission-metric-grid'>
                <div class='mission-metric-card'><div class='metric-big'>{result['percentage']}%</div><div class='metric-label'>Accuracy</div></div>
                <div class='mission-metric-card'><div class='metric-big'>{result['score']}/{result['total']}</div><div class='metric-label'>Score</div></div>
                <div class='mission-metric-card'><div class='metric-big'>{result['attempt']}</div><div class='metric-label'>Attempt</div></div>
                <div class='mission-metric-card'><div class='metric-big'>{'Ready' if not result['mistakes'] else 'Review'}</div><div class='metric-label'>Status</div></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if result["mistakes"]:
            st.markdown("### Mistake Review")

            for detail in result["details"]:
                if detail["correct"]:
                    continue

                with st.expander(f"Review: {detail['concept']}", expanded=True):
                    st.write(f"Your answer: {detail['chosen']}")
                    st.write(f"Correct answer: {detail['correct_answer']}")
                    st.info(detail["explanation"])

                    if st.button(
                        f"Ask Preluma AI about {detail['concept']}",
                        key=f"ask_mistake_{detail['question_id']}",
                    ):
                        st.session_state.ai_context_note = (
                            f"Homework mistake. Topic: {selected.get('Topic')}. "
                            f"Question: {detail['question']} "
                            f"Student answer: {detail['chosen']}. "
                            f"Correct answer: {detail['correct_answer']}."
                        )
                        st.session_state.active_page = "Ask Preluma AI"
                        st.rerun()
        else:
            st.info("No mistakes were captured. This homework is complete, so the notification is cleared.")

        if st.button("Try this homework again"):
            _reset_homework_flow(homework_id)
            st.rerun()

        return

    step = int(st.session_state.get("hw_step", 0))
    total = len(questions)

    if step >= total:
        st.markdown("### Review Answers Before Submit")

        missing = []

        for question in questions:
            question_id = int(question["Question ID"])
            chosen = st.session_state.hw_answers.get(question_id, "")

            if not chosen:
                missing.append(question_id)

            st.markdown(
                f"""
                <div class='assignment-card'>
                  <div class='albl lbl-yellow'>
                    Question {question_id} · {question.get('Concept')}
                  </div>
                  <div class='atxt'>{question.get('Question')}</div>
                  <div style='margin-top:10px;color:#cbd5e1;font-size:14px;'>
                    Your answer: <b>{chosen or 'Not answered yet'}</b>
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        c1, c2, c3 = st.columns([1, 2, 1])

        with c1:
            if st.button("Back", use_container_width=True):
                st.session_state.hw_step = max(0, total - 1)
                st.rerun()

        with c2:
            if missing:
                st.warning(
                    f"Please answer question(s): {', '.join(map(str, missing))}"
                )
            else:
                if st.button("Submit Homework", use_container_width=True):
                    st.session_state.homework_result = submit_homework(
                        homework_id,
                        student,
                        st.session_state.hw_answers,
                    )
                    mark_homework_notifications_read(student, homework_id)
                    st.rerun()

        with c3:
            if st.button("Reset", use_container_width=True):
                _reset_homework_flow(homework_id)
                st.rerun()

        return

    question = questions[step]
    question_id = int(question["Question ID"])

    _homework_progress(step, total)

    st.markdown(
        f"""
        <div class='assignment-card' style='border-color:rgba(245,158,11,.34);'>
          <div class='albl lbl-yellow'>
            Question {question_id} · {question.get('Concept')}
          </div>
          <div class='atxt' style='font-size:18px;font-weight:700;'>
            {question.get('Question')}
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    current_answer = st.session_state.hw_answers.get(question_id, "")
    options = question["Options"]

    try:
        selected_index = options.index(current_answer)
    except ValueError:
        selected_index = 0

    selected_answer = st.radio(
        "Choose one answer",
        options,
        index=selected_index,
        key=f"homework_step_{homework_id}_{question_id}",
    )

    if selected_answer:
        st.session_state.hw_answers[question_id] = selected_answer

    c1, c2, c3 = st.columns([1, 2, 1])

    with c1:
        if st.button("Back", disabled=step == 0, use_container_width=True):
            st.session_state.hw_step = max(0, step - 1)
            st.rerun()

    with c2:
        st.caption(
            "Answer the current question, then continue. Only one question is shown at a time."
        )

    with c3:
        button_label = "Review" if step == total - 1 else "Next"

        if st.button(button_label, use_container_width=True):
            if not st.session_state.hw_answers.get(question_id):
                st.warning("Please choose an answer first.")
            else:
                st.session_state.hw_step = step + 1
                st.rerun()

    mistakes = load_student_mistakes(student)

    if mistakes:
        with st.expander("My captured weak areas", expanded=False):
            for mistake in mistakes[-8:]:
                st.write(
                    f"{mistake.get('Weak Concept')} — "
                    f"{mistake.get('Question')}"
                )

def _default_homework_questions(topic: str) -> list[dict]:
    return [
        {
            "question": f"What is the best simple definition of {topic}?",
            "options": [
                f"The main idea and meaning of {topic}",
                "A random unrelated fact",
                "Only a difficult formula",
                "Something that cannot be learned",
            ],
            "answer": f"The main idea and meaning of {topic}",
            "concept": "Definition",
            "explanation": "Start with the core meaning before learning details.",
            "marks": 1,
        },
        {
            "question": f"What is the best way to understand {topic}?",
            "options": [
                "Connect the definition with an example",
                "Memorize one sentence without meaning",
                "Skip practice",
                "Avoid asking questions",
            ],
            "answer": "Connect the definition with an example",
            "concept": "Application",
            "explanation": "Examples connect theory to something the learner can picture.",
            "marks": 1,
        },
        {
            "question": f"What should a student do after making a mistake in {topic}?",
            "options": [
                "Review the weak concept and try again",
                "Hide the mistake",
                "Stop studying",
                "Choose random answers",
            ],
            "answer": "Review the weak concept and try again",
            "concept": "Reflection",
            "explanation": "Mistakes are useful when they guide the next study action.",
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


# ── Evidence Board ────────────────────────────────────────────────────────────

def evidence_board():
    hero()
    st.markdown("""<div class='sec-head'>
      <div class='sec-icon' style='background:rgba(167,139,250,.12);'>📋</div>
      <div><div class='sec-title'>Evidence Board</div><div class='sec-sub'>What this project demonstrates and why it matters</div></div>
    </div>""", unsafe_allow_html=True)

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


# ── Professor Defense ─────────────────────────────────────────────────────────

def professor_defense():
    hero()
    st.markdown("""<div class='sec-head'>
      <div class='sec-icon' style='background:rgba(52,211,153,.10);'>🎓</div>
      <div><div class='sec-title'>Professor Defense</div><div class='sec-sub'>Built for final presentation — clear problem, Python proof, innovation, and contribution</div></div>
    </div>""", unsafe_allow_html=True)

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
    st.success("Course permission allows third-party libraries for the product interface. Preluma uses Streamlit and Plotly only in the presentation layer; the assessed core work — CSV loading/saving, statistics, Merge Sort, Binary Search, timing, exception handling, and result.txt logging — is implemented manually with the Python standard library.")


# ── Project Team ──────────────────────────────────────────────────────────────

def project_team():
    if TEAM_URI:
        st.markdown(f"""
        <div class='team-photo-hero' style="background-image:url('{TEAM_URI}');">
          <div class='team-photo-content'>
            <span class='badge'>Project Team · Team Preluma</span>
            <h1>Building a smarter pre-class learning experience together.</h1>
            <p>Three students combined core development, testing, topic data, and presentation support to shape Preluma into a working Python Streamlit prototype.</p>
            <div class='team-school-line'>School of Software and Artificial Intelligence · Yunnan University</div>
          </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("Team photo is missing: assets/team_preluma.jpg")

    st.markdown("""
    <div class='member-grid'>
      <div class='member-card'>
        <div class='member-role'>Feature Logic · Quiz Testing</div>
        <h3>MD FAHIM</h3>
        <p>Supported quiz checking, feature testing, and interaction feedback.</p>
      </div>
      <div class='member-card main'>
        <div class='member-role'>Core App · UI/UX · Integration</div>
        <h3>MAMUNUR RASHID</h3>
        <p>Worked on the main Python Streamlit app, interface design, module integration, and deployment flow.</p>
      </div>
      <div class='member-card'>
        <div class='member-role'>Topic Data · Documentation</div>
        <h3>MD JIARUL ISLAM</h3>
        <p>Supported topic data organization, documentation, and presentation preparation.</p>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Work Division")
    st.dataframe([
        {"Member":"MAMUNUR RASHID", "Main Responsibility":"Core app, UI/UX, integration", "Contribution":"Connected the main modules into one deployed Streamlit product"},
        {"Member":"MD FAHIM", "Main Responsibility":"Quiz testing and feature feedback", "Contribution":"Improved interaction quality and checked quiz behaviour"},
        {"Member":"MD JIARUL ISLAM", "Main Responsibility":"Topic data and documentation", "Contribution":"Supported content organization and presentation material"},
    ], use_container_width=True, hide_index=True)


# ── Demo Guide ────────────────────────────────────────────────────────────────

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


# ── Roadmap ───────────────────────────────────────────────────────────────────

def roadmap():
    hero()
    st.markdown("""<div class='sec-head'>
      <div class='sec-icon' style='background:rgba(52,211,153,.10);'>🚀</div>
      <div><div class='sec-title'>Future Roadmap</div><div class='sec-sub'>Where Preluma goes next</div></div>
    </div>""", unsafe_allow_html=True)

    st.dataframe(pd.DataFrame({
        "Phase":      ["Current","Prototype","AI Upgrade","Real Product"],
        "Goal":       ["Final project submission","Student accounts + history","RAG tutor with citations","Mobile app + class codes"],
        "Technology": ["Python + Streamlit + Gemini","Python + SQLite","Embeddings + retrieval + LLM","API backend + React Native"],
        "Status":     ["Live now","Next semester","Future","Long-term"],
    }), use_container_width=True)
    st.code("Now:    Python + Streamlit + Wikipedia + Claude/Groq/Gemini + CSV + Merge Sort\nNext:   Login + SQLite + saved student history per account\nLater:  Upload course PDF + retrieval + cited AI answers\nFuture: Mobile app + teacher dashboard + real-time class codes", language="text")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    init_state()
    page, presentation = sidebar()

    if page in {"My Homework", "🔔 My Homework"} or page.startswith("🔔 My Homework"):
        my_homework_page()
        return

    pages = {
        "Home": lambda: home_page(presentation),
        "Student Mission": lambda: student_mission(presentation),
        "Ask Preluma AI": ask_preluma_ai_page,
        "Teacher Studio": teacher_studio,
        "Homework Center": homework_center_page,
        "Evidence Board": evidence_board,
        "Professor Defense": professor_defense,
        "Project Team": project_team,
        "Demo Guide": demo_guide,
        "Future Roadmap": roadmap,
    }
    pages.get(page, lambda: home_page(presentation))()



if __name__ == "__main__":
    main()
