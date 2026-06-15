"""Data models for Preluma course-compliance analysis.

This module uses only the Python standard library.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class StudentRecord:
    """One CSV row representing a student's pre-class readiness result."""

    record_id: int
    student: str
    topic: str
    readiness: float
    weak_skill: str
    quiz_score: int
    quiz_total: int
    lecture_time: str
    learning_mode: str
    created_at: str


@dataclass(frozen=True)
class AnalysisResult:
    """Summary produced by the pure-Python analyzer."""

    student_count: int
    average_readiness: float
    lowest_readiness: float
    highest_readiness: float
    variance: float
    most_common_weak_skill: str
    elapsed_ns: int
