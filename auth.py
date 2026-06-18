"""
auth.py — Preluma Authentication Module

Storage strategy (in priority order):
  1. Supabase  — if SUPABASE_URL + SUPABASE_KEY are in Streamlit secrets.
                 Data survives every deploy forever.
  2. CSV file  — fallback when Supabase is not configured.
                 Ephemeral on Streamlit Cloud (resets on each deploy).
                 Reliable for local dev.

Permanent accounts live in DEMO_USERS below and are re-seeded on every
startup so they ALWAYS exist regardless of which backend is in use.

Passwords stored as SHA-256 hashes — no external libraries needed.
"""
from __future__ import annotations

import csv
import hashlib
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional

import requests as _requests

DATA_DIR  = Path("data")
USERS_CSV = DATA_DIR / "users.csv"
USER_FIELDS = ["User ID", "Username", "Password Hash", "Role", "Full Name", "Created At"]

# ─────────────────────────────────────────────────────────────────────────────
# PERMANENT ACCOUNTS — add anyone here who must always exist after a deploy.
# Format: (username, password, role, full_name)
# ─────────────────────────────────────────────────────────────────────────────
DEMO_USERS = [
    # ── Admin / Team ──────────────────────────────────────────────────────
    ("teacher",     "teach123",    "teacher", "Prof. Amir Hossain"),
    ("mim.ynu",     "MimYnu24",    "teacher", "Mamunur Rashid (Admin)"),
    # ── Course Teachers ───────────────────────────────────────────────────
    ("zhouyujue",   "Zhou2024",    "teacher", "Zhou Yujue"),
    ("gaosong",     "Gao2024",     "teacher", "Gao Song"),
    ("tangli",      "Tang2024",    "teacher", "Tang Li"),
    ("weiping",     "Wei2024",     "teacher", "Wei Ping"),
    # ── Dev Team (student access) ─────────────────────────────────────────
    ("mamun",       "preluma1",    "student", "Mamunur Rashid"),
    ("fahim",       "preluma1",    "student", "Fahim Ahmed"),
    ("jiarul",      "preluma1",    "student", "Jiarul Islam"),
    # ── Demo Students ─────────────────────────────────────────────────────
    ("student1",    "pass123",     "student", "Alice Wang"),
    ("student2",    "pass123",     "student", "Bob Chen"),
]


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def _hash(pw: str) -> str:
    return hashlib.sha256(pw.encode()).hexdigest()


def _now() -> str:
    return datetime.now().isoformat(timespec="seconds")


def _new_id() -> str:
    return str(uuid.uuid4())[:8]


def _get_secret(name: str) -> str:
    """Read from Streamlit secrets, fall back to empty string."""
    try:
        import streamlit as st
        val = st.secrets.get(name, "")
        return str(val).strip() if val else ""
    except Exception:
        return ""


# ─────────────────────────────────────────────────────────────────────────────
# Supabase backend  (used when SUPABASE_URL + SUPABASE_KEY are configured)
# Uses only the `requests` library — no extra dependencies.
#
# Required Streamlit secrets:
#   SUPABASE_URL = "https://xxxxxxxxxxxx.supabase.co"
#   SUPABASE_KEY = "your-anon-public-key"
#
# Required Supabase table  (run once in the Supabase SQL editor):
#   create table if not exists preluma_users (
#     user_id      text not null,
#     username     text primary key,
#     password_hash text not null,
#     role         text not null default 'student',
#     full_name    text not null,
#     created_at   text not null
#   );
#   alter table preluma_users enable row level security;
#   create policy "anon full access" on preluma_users
#     for all using (true) with check (true);
# ─────────────────────────────────────────────────────────────────────────────

def _sb_headers() -> dict:
    key = _get_secret("SUPABASE_KEY")
    return {
        "apikey": key,
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
    }


def _sb_url() -> str:
    base = _get_secret("SUPABASE_URL").rstrip("/")
    return f"{base}/rest/v1/preluma_users"


def _supabase_available() -> bool:
    return bool(_get_secret("SUPABASE_URL") and _get_secret("SUPABASE_KEY"))


def _sb_read_all() -> list[dict]:
    try:
        resp = _requests.get(
            _sb_url(),
            headers={**_sb_headers(), "Prefer": "return=representation"},
            params={"select": "user_id,username,password_hash,role,full_name,created_at"},
            timeout=8,
        )
        resp.raise_for_status()
        rows = resp.json()
        # Normalise keys to match CSV field names
        return [{
            "User ID":       r.get("user_id", ""),
            "Username":      r.get("username", ""),
            "Password Hash": r.get("password_hash", ""),
            "Role":          r.get("role", "student"),
            "Full Name":     r.get("full_name", ""),
            "Created At":    r.get("created_at", ""),
        } for r in rows]
    except Exception:
        return []


def _sb_upsert(row: dict) -> bool:
    """Insert or update a user row (upsert on username PK)."""
    payload = {
        "user_id":       row["User ID"],
        "username":      row["Username"],
        "password_hash": row["Password Hash"],
        "role":          row["Role"],
        "full_name":     row["Full Name"],
        "created_at":    row["Created At"],
    }
    try:
        resp = _requests.post(
            _sb_url(),
            headers={**_sb_headers(), "Prefer": "resolution=merge-duplicates,return=minimal"},
            json=payload,
            timeout=8,
        )
        return resp.status_code in (200, 201, 204)
    except Exception:
        return False


# ─────────────────────────────────────────────────────────────────────────────
# CSV backend  (fallback)
# ─────────────────────────────────────────────────────────────────────────────

def _csv_read_all() -> list[dict]:
    if not USERS_CSV.exists():
        return []
    with USERS_CSV.open("r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _csv_append(row: dict) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    needs_header = not USERS_CSV.exists()
    with USERS_CSV.open("a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=USER_FIELDS)
        if needs_header:
            w.writeheader()
        w.writerow(row)


# ─────────────────────────────────────────────────────────────────────────────
# Unified read / write — picks the right backend automatically
# ─────────────────────────────────────────────────────────────────────────────

def _read_all() -> list[dict]:
    if _supabase_available():
        rows = _sb_read_all()
        if rows:          # Supabase reachable and has data
            return rows
        # Supabase reachable but empty (first run) — fall through to seed
        return rows
    return _csv_read_all()


def _write_row(row: dict) -> None:
    if _supabase_available():
        _sb_upsert(row)
    else:
        _csv_append(row)


# ─────────────────────────────────────────────────────────────────────────────
# Public API
# ─────────────────────────────────────────────────────────────────────────────

_SETUP_DONE: bool = False  # module-level flag — runs only ONCE per Python process

def ensure_setup() -> None:
    """
    Idempotent — call once at app startup.
    Seeds all DEMO_USERS into whatever backend is active.
    Works whether using Supabase or CSV, and survives every deploy.
    """
    global _SETUP_DONE
    if _SETUP_DONE:
        return
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    existing = {u["Username"] for u in _read_all()}
    for username, password, role, full_name in DEMO_USERS:
        uname = username.strip().lower()
        if uname not in existing:
            _write_row({
                "User ID":       _new_id(),
                "Username":      uname,
                "Password Hash": _hash(password),
                "Role":          role,
                "Full Name":     full_name.strip(),
                "Created At":    _now(),
            })
            existing.add(uname)
    _SETUP_DONE = True


def authenticate(username: str, password: str) -> Optional[dict]:
    uname, pw_hash = username.strip().lower(), _hash(password)

    # ── Always check DEMO_USERS directly first (guaranteed to work) ──────────
    for demo_uname, demo_pw, demo_role, demo_name in DEMO_USERS:
        if demo_uname.strip().lower() == uname and _hash(demo_pw) == pw_hash:
            return {
                "User ID":       "demo",
                "Username":      uname,
                "Password Hash": pw_hash,
                "Role":          demo_role,
                "Full Name":     demo_name,
                "Created At":    "",
            }

    # ── Then check database (registered users) ───────────────────────────────
    ensure_setup()
    for u in _read_all():
        if u["Username"] == uname and u["Password Hash"] == pw_hash:
            return u
    return None


def username_exists(username: str) -> bool:
    return username.strip().lower() in {u["Username"] for u in _read_all()}


def register(username: str, password: str, full_name: str,
             role: str = "student") -> tuple[bool, str]:
    uname = username.strip().lower()
    if not uname or not password or not full_name.strip():
        return False, "All fields are required."
    if len(uname) < 3:
        return False, "Username must be at least 3 characters."
    if len(password) < 6:
        return False, "Password must be at least 6 characters."
    ensure_setup()
    if username_exists(uname):
        return False, "Username already taken. Please choose another."
    _write_row({
        "User ID":       _new_id(),
        "Username":      uname,
        "Password Hash": _hash(password),
        "Role":          role,
        "Full Name":     full_name.strip(),
        "Created At":    _now(),
    })
    return True, "Account created successfully!"


def get_all_students() -> list[dict]:
    ensure_setup()
    return [u for u in _read_all() if u["Role"] == "student"]


def get_all_users() -> list[dict]:
    ensure_setup()
    return _read_all()


def storage_backend() -> str:
    """Returns 'supabase' or 'csv' — used for status display."""
    return "supabase" if _supabase_available() else "csv"
