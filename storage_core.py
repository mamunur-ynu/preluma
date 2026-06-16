from __future__ import annotations
import csv
from datetime import datetime
from pathlib import Path
from typing import Any

DATA_DIR     = Path("data")
STUDENTS_CSV = DATA_DIR / "students.csv"
RESULT_LOG   = Path("audit_log.txt")
FIELDNAMES   = ["Record ID","Student","Topic","Readiness","Weak Skill",
                "Quiz Score","Quiz Total","Lecture Time","Learning Mode","Created At"]

def timestamp() -> str:
    return datetime.now().isoformat(timespec="seconds")

def ensure_data_files() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not STUDENTS_CSV.exists():
        with STUDENTS_CSV.open("w", newline="", encoding="utf-8") as f:
            csv.DictWriter(f, fieldnames=FIELDNAMES).writeheader()
    if not RESULT_LOG.exists():
        RESULT_LOG.write_text("Preluma Audit Log\n", encoding="utf-8")

def load_student_rows() -> list[dict[str, Any]]:
    ensure_data_files()
    rows = []
    with STUDENTS_CSV.open("r", newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            for field in ["Record ID","Quiz Score","Quiz Total"]:
                try: row[field] = int(row.get(field, 0))
                except (TypeError, ValueError): row[field] = 0
            try: row["Readiness"] = float(row.get("Readiness", 0.0))
            except (TypeError, ValueError): row["Readiness"] = 0.0
            rows.append(row)
    return rows

def next_record_id() -> int:
    max_id = 0
    for row in load_student_rows():
        try: max_id = max(max_id, int(row.get("Record ID", 0)))
        except (TypeError, ValueError): pass
    return max_id + 1

def append_student_row(row: dict[str, Any]) -> None:
    ensure_data_files()
    clean = {field: row.get(field, "") for field in FIELDNAMES}
    with STUDENTS_CSV.open("a", newline="", encoding="utf-8") as f:
        csv.DictWriter(f, fieldnames=FIELDNAMES).writerow(clean)

def append_result_log(operation: str, details: dict[str, Any]) -> None:
    ensure_data_files()
    parts = [f"{timestamp()} | op={operation}"]
    for key, value in details.items():
        parts.append(f"{key}={value}")
    with RESULT_LOG.open("a", encoding="utf-8") as f:
        f.write(" | ".join(parts) + "\n")

def read_recent_logs(limit: int = 10) -> list[str]:
    ensure_data_files()
    lines = [l for l in RESULT_LOG.read_text(encoding="utf-8").splitlines() if l.strip()]
    return lines[-limit:]

def seed_demo_rows() -> None:
    ensure_data_files()
    if load_student_rows():
        return
    demo = [
        ("Amir",   "Quantum Mechanics",       85.0, "Core Concept", 3, 4, "Tomorrow 9 AM", "Deep Understanding"),
        ("Jia",    "Neural Network",           92.0, "None",         4, 4, "Tomorrow 9 AM", "Deep Understanding"),
        ("Fahim",  "Python Programming",       76.0, "Application",  3, 4, "Tomorrow 9 AM", "Exam/Viva Mode"),
        ("Nadia",  "Statistics",               68.0, "Definition",   2, 4, "Tomorrow 9 AM", "Fast Review"),
        ("Omar",   "Machine Learning",         88.0, "None",         4, 4, "Tomorrow 9 AM", "Deep Understanding"),
        ("Sara",   "Artificial Intelligence",  72.0, "Misconception",3, 4, "Tomorrow 9 AM", "Normal Mode"),
    ]
    rid = 1
    for student, topic, readiness, weak, score, total, lecture, mode in demo:
        append_student_row({
            "Record ID": rid, "Student": student, "Topic": topic,
            "Readiness": readiness, "Weak Skill": weak,
            "Quiz Score": score, "Quiz Total": total,
            "Lecture Time": lecture, "Learning Mode": mode,
            "Created At": timestamp()
        })
        rid += 1
    append_result_log("seed_demo_rows", {"n": len(demo)})
