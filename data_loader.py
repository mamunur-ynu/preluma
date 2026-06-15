"""CSV loading and result persistence for the Preluma project.

Only Python standard-library modules are used here: csv, pathlib, and typing.
"""
from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterable

from models import StudentRecord

FIELDNAMES = [
    "Record ID",
    "Student",
    "Topic",
    "Readiness",
    "Weak Skill",
    "Quiz Score",
    "Quiz Total",
    "Lecture Time",
    "Learning Mode",
    "Created At",
]


def _safe_int(value: str, default: int = 0) -> int:
    try:
        return int(str(value).strip())
    except (TypeError, ValueError):
        return default


def _safe_float(value: str, default: float = 0.0) -> float:
    try:
        return float(str(value).strip())
    except (TypeError, ValueError):
        return default


def load_records(path: str | Path) -> list[StudentRecord]:
    """Load student readiness records from a CSV file with exception handling."""
    csv_path = Path(path)
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    records: list[StudentRecord] = []
    with csv_path.open("r", newline="", encoding="utf-8") as file_obj:
        reader = csv.DictReader(file_obj)
        for row in reader:
            records.append(
                StudentRecord(
                    record_id=_safe_int(row.get("Record ID", "0")),
                    student=str(row.get("Student", "")).strip(),
                    topic=str(row.get("Topic", "")).strip(),
                    readiness=_safe_float(row.get("Readiness", "0")),
                    weak_skill=str(row.get("Weak Skill", "Unknown")).strip() or "Unknown",
                    quiz_score=_safe_int(row.get("Quiz Score", "0")),
                    quiz_total=_safe_int(row.get("Quiz Total", "0")),
                    lecture_time=str(row.get("Lecture Time", "")).strip(),
                    learning_mode=str(row.get("Learning Mode", "")).strip(),
                    created_at=str(row.get("Created At", "")).strip(),
                )
            )
    return records


def write_result(path: str | Path, lines: Iterable[str]) -> None:
    """Save analysis output to result.txt."""
    output_path = Path(path)
    with output_path.open("w", encoding="utf-8") as file_obj:
        for line in lines:
            file_obj.write(str(line).rstrip() + "\n")
