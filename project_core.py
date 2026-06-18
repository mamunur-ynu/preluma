"""
project_core.py — Preluma Project Management Module

Stores:
  • Project metadata  → data/projects.csv  (local, re-creatable)
  • Project files     → Supabase preluma_project_files table (permanent base64 blobs)
                        Falls back to data/project_files/ directory when Supabase unavailable

Supabase table required (run once in Supabase SQL editor):
    create table if not exists preluma_project_files (
      file_id       text primary key,
      project_id    text not null,
      uploader      text not null,
      uploader_role text not null,
      file_name     text not null,
      file_type     text,
      file_data     text not null,
      notes         text,
      created_at    text not null
    );
    alter table preluma_project_files enable row level security;
    create policy "anon full access" on preluma_project_files
      for all using (true) with check (true);
"""
from __future__ import annotations

import base64
import csv
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any

import requests as _requests

DATA_DIR         = Path("data")
PROJECTS_CSV     = DATA_DIR / "projects.csv"
LOCAL_FILES_DIR  = DATA_DIR / "project_files"

PROJECT_FIELDS = [
    "Project ID", "Title", "Description", "Due Date",
    "Created By", "Created At", "Published",
]


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def _now() -> str:
    return datetime.now().isoformat(timespec="seconds")


def _new_id() -> str:
    return str(uuid.uuid4())[:10]


def _get_secret(name: str) -> str:
    try:
        import streamlit as st
        val = st.secrets.get(name, "")
        return str(val).strip() if val else ""
    except Exception:
        return ""


def _supabase_available() -> bool:
    return bool(_get_secret("SUPABASE_URL") and _get_secret("SUPABASE_KEY"))


def _sb_headers() -> dict:
    key = _get_secret("SUPABASE_KEY")
    return {
        "apikey": key,
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
    }


def _sb_files_url() -> str:
    base = _get_secret("SUPABASE_URL").rstrip("/")
    return f"{base}/rest/v1/preluma_project_files"


# ─────────────────────────────────────────────────────────────────────────────
# CSV helpers — project metadata
# ─────────────────────────────────────────────────────────────────────────────

def _ensure_projects_csv() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not PROJECTS_CSV.exists():
        with PROJECTS_CSV.open("w", newline="", encoding="utf-8") as f:
            csv.DictWriter(f, fieldnames=PROJECT_FIELDS).writeheader()


def _read_projects() -> list[dict]:
    _ensure_projects_csv()
    if not PROJECTS_CSV.exists():
        return []
    with PROJECTS_CSV.open("r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _append_project(row: dict) -> None:
    _ensure_projects_csv()
    clean = {field: row.get(field, "") for field in PROJECT_FIELDS}
    with PROJECTS_CSV.open("a", newline="", encoding="utf-8") as f:
        csv.DictWriter(f, fieldnames=PROJECT_FIELDS).writerow(clean)


# ─────────────────────────────────────────────────────────────────────────────
# Supabase file helpers
# ─────────────────────────────────────────────────────────────────────────────

def _sb_upload_file(row: dict) -> bool:
    """Insert a file record into preluma_project_files."""
    try:
        resp = _requests.post(
            _sb_files_url(),
            headers={**_sb_headers(), "Prefer": "return=minimal"},
            json=row,
            timeout=30,
        )
        return resp.status_code in (200, 201, 204)
    except Exception:
        return False


def _sb_get_files(project_id: str | None = None,
                  uploader: str | None = None,
                  uploader_role: str | None = None) -> list[dict]:
    """Fetch file records, optionally filtered."""
    params: dict = {"select": "file_id,project_id,uploader,uploader_role,file_name,file_type,notes,created_at"}
    filters = []
    if project_id:
        filters.append(f"project_id=eq.{project_id}")
    if uploader:
        filters.append(f"uploader=eq.{uploader}")
    if uploader_role:
        filters.append(f"uploader_role=eq.{uploader_role}")
    if filters:
        params["and"] = "(" + ",".join(filters) + ")"
    try:
        resp = _requests.get(
            _sb_files_url(), headers=_sb_headers(), params=params, timeout=10
        )
        if resp.status_code == 200:
            return resp.json()
    except Exception:
        pass
    return []


def _sb_get_file_data(file_id: str) -> dict | None:
    """Fetch a single file record including its base64 data."""
    try:
        resp = _requests.get(
            _sb_files_url(),
            headers=_sb_headers(),
            params={"file_id": f"eq.{file_id}", "select": "*", "limit": "1"},
            timeout=20,
        )
        if resp.status_code == 200:
            rows = resp.json()
            return rows[0] if rows else None
    except Exception:
        pass
    return None


def _sb_delete_file(file_id: str) -> bool:
    try:
        resp = _requests.delete(
            _sb_files_url(),
            headers=_sb_headers(),
            params={"file_id": f"eq.{file_id}"},
            timeout=10,
        )
        return resp.status_code in (200, 204)
    except Exception:
        return False


# ─────────────────────────────────────────────────────────────────────────────
# Local file fallback
# ─────────────────────────────────────────────────────────────────────────────

_LOCAL_META_CSV = DATA_DIR / "project_file_meta.csv"
_LOCAL_META_FIELDS = [
    "file_id", "project_id", "uploader", "uploader_role",
    "file_name", "file_type", "notes", "created_at", "local_path",
]


def _ensure_local_meta() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    LOCAL_FILES_DIR.mkdir(parents=True, exist_ok=True)
    if not _LOCAL_META_CSV.exists():
        with _LOCAL_META_CSV.open("w", newline="", encoding="utf-8") as f:
            csv.DictWriter(f, fieldnames=_LOCAL_META_FIELDS).writeheader()


def _local_save_file(row: dict, file_bytes: bytes) -> bool:
    _ensure_local_meta()
    safe_name = "".join(c if c.isalnum() or c in "._-" else "_" for c in row["file_name"])
    local_path = LOCAL_FILES_DIR / f"{row['file_id']}_{safe_name}"
    try:
        local_path.write_bytes(file_bytes)
        row["local_path"] = str(local_path)
        clean = {f: row.get(f, "") for f in _LOCAL_META_FIELDS}
        with _LOCAL_META_CSV.open("a", newline="", encoding="utf-8") as f:
            csv.DictWriter(f, fieldnames=_LOCAL_META_FIELDS).writerow(clean)
        return True
    except Exception:
        return False


def _local_get_files(project_id: str | None = None,
                     uploader: str | None = None,
                     uploader_role: str | None = None) -> list[dict]:
    _ensure_local_meta()
    rows = []
    if not _LOCAL_META_CSV.exists():
        return rows
    with _LOCAL_META_CSV.open("r", newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if project_id and row.get("project_id") != project_id:
                continue
            if uploader and row.get("uploader") != uploader:
                continue
            if uploader_role and row.get("uploader_role") != uploader_role:
                continue
            rows.append(row)
    return rows


def _local_get_file_bytes(file_id: str) -> tuple[bytes | None, str]:
    """Returns (bytes, filename) or (None, '')."""
    _ensure_local_meta()
    if not _LOCAL_META_CSV.exists():
        return None, ""
    with _LOCAL_META_CSV.open("r", newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row.get("file_id") == file_id:
                path = Path(row.get("local_path", ""))
                if path.exists():
                    return path.read_bytes(), row.get("file_name", "file")
    return None, ""


# ─────────────────────────────────────────────────────────────────────────────
# Public API
# ─────────────────────────────────────────────────────────────────────────────

def create_project(
    title: str,
    description: str,
    due_date: str,
    created_by: str,
) -> str:
    """Create a project record. Returns the new project_id."""
    project_id = _new_id()
    _append_project({
        "Project ID": project_id,
        "Title": title.strip(),
        "Description": description.strip(),
        "Due Date": due_date.strip(),
        "Created By": created_by.strip(),
        "Created At": _now(),
        "Published": "Yes",
    })
    return project_id


def load_projects(published_only: bool = True) -> list[dict]:
    rows = _read_projects()
    if published_only:
        return [r for r in rows if r.get("Published", "Yes") == "Yes"]
    return rows


def upload_file(
    project_id: str,
    uploader: str,
    uploader_role: str,
    file_name: str,
    file_bytes: bytes,
    file_type: str = "",
    notes: str = "",
) -> tuple[bool, str]:
    """
    Upload a file for a project.
    Returns (success, file_id or error_message).
    """
    file_id = _new_id()
    b64_data = base64.b64encode(file_bytes).decode()
    row = {
        "file_id":       file_id,
        "project_id":    project_id,
        "uploader":      uploader,
        "uploader_role": uploader_role,
        "file_name":     file_name,
        "file_type":     file_type,
        "file_data":     b64_data,
        "notes":         notes,
        "created_at":    _now(),
    }
    if _supabase_available():
        ok = _sb_upload_file(row)
        if ok:
            return True, file_id
        # Fallback to local if Supabase upload fails
    ok = _local_save_file(dict(row), file_bytes)
    return ok, file_id if ok else "Upload failed"


def get_project_files(
    project_id: str | None = None,
    uploader: str | None = None,
    uploader_role: str | None = None,
) -> list[dict]:
    """Get file metadata (no binary data) — fast list for display."""
    if _supabase_available():
        rows = _sb_get_files(project_id, uploader, uploader_role)
        if rows is not None:
            return rows
    return _local_get_files(project_id, uploader, uploader_role)


def download_file(file_id: str) -> tuple[bytes | None, str, str]:
    """
    Download file bytes.
    Returns (bytes, file_name, file_type).
    """
    if _supabase_available():
        rec = _sb_get_file_data(file_id)
        if rec:
            try:
                raw = base64.b64decode(rec["file_data"])
                return raw, rec.get("file_name", "file"), rec.get("file_type", "")
            except Exception:
                pass
    raw, fname = _local_get_file_bytes(file_id)
    return raw, fname, ""


def delete_file(file_id: str) -> bool:
    if _supabase_available():
        return _sb_delete_file(file_id)
    # Local delete — mark as deleted (simple: just remove from meta CSV)
    return False  # simplified for now


def student_has_uploaded(project_id: str, student: str) -> bool:
    files = get_project_files(project_id=project_id, uploader=student, uploader_role="student")
    return len(files) > 0
