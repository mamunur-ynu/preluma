"""
auth.py — Preluma Authentication Module
Handles user registration, login, and session management.
All passwords stored as SHA-256 hashes. No external libraries needed.
"""
from __future__ import annotations

import csv
import hashlib
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional

DATA_DIR   = Path("data")
USERS_CSV  = DATA_DIR / "users.csv"

USER_FIELDS = [
    "User ID", "Username", "Password Hash", "Role", "Full Name", "Created At"
]

# Demo accounts pre-seeded on first run
DEMO_USERS = [
    # username,      password,     role,      full_name
    ("teacher",      "teach123",   "teacher", "Prof. Amir Hossain"),
    ("mamun",        "preluma1",   "student", "Mamunur Rashid"),
    ("fahim",        "preluma1",   "student", "Fahim Ahmed"),
    ("jiarul",       "preluma1",   "student", "Jiarul Islam"),
    ("student1",     "pass123",    "student", "Alice Wang"),
    ("student2",     "pass123",    "student", "Bob Chen"),
]


def _hash(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def _ensure_users_csv() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not USERS_CSV.exists():
        with USERS_CSV.open("w", newline="", encoding="utf-8") as f:
            csv.DictWriter(f, fieldnames=USER_FIELDS).writeheader()
        # Seed demo accounts
        for username, password, role, full_name in DEMO_USERS:
            _append_user(username, password, role, full_name)


def _read_users() -> list[dict]:
    _ensure_users_csv()
    with USERS_CSV.open("r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _append_user(username: str, password: str, role: str, full_name: str) -> None:
    _ensure_users_csv()
    row = {
        "User ID":       str(uuid.uuid4())[:8],
        "Username":      username.strip().lower(),
        "Password Hash": _hash(password),
        "Role":          role,
        "Full Name":     full_name.strip(),
        "Created At":    datetime.now().isoformat(timespec="seconds"),
    }
    with USERS_CSV.open("a", newline="", encoding="utf-8") as f:
        csv.DictWriter(f, fieldnames=USER_FIELDS).writerow(row)


def username_exists(username: str) -> bool:
    username = username.strip().lower()
    return any(u["Username"] == username for u in _read_users())


def authenticate(username: str, password: str) -> Optional[dict]:
    """Returns user dict on success, None on failure."""
    username = username.strip().lower()
    pw_hash  = _hash(password)
    for user in _read_users():
        if user["Username"] == username and user["Password Hash"] == pw_hash:
            return user
    return None


def register(username: str, password: str, full_name: str, role: str = "student") -> tuple[bool, str]:
    """
    Register a new user.
    Returns (success: bool, message: str).
    """
    username = username.strip().lower()
    if not username or not password or not full_name:
        return False, "All fields are required."
    if len(username) < 3:
        return False, "Username must be at least 3 characters."
    if len(password) < 6:
        return False, "Password must be at least 6 characters."
    if username_exists(username):
        return False, "Username already taken. Please choose another."
    _append_user(username, password, role, full_name)
    return True, "Account created successfully!"


def get_all_students() -> list[dict]:
    """Return all users with role=student."""
    return [u for u in _read_users() if u["Role"] == "student"]


def get_all_users() -> list[dict]:
    return _read_users()
