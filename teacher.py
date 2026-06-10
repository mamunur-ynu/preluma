"""
teacher.py  –  Preluma V17
Builds the teacher analytics dataframe with realistic demo data.
"""

import pandas as pd


def demo_teacher_data() -> pd.DataFrame:
    return pd.DataFrame([
        {"Student": "Amir",   "Topic": "Quantum Mechanics",       "Readiness": 75, "Weak Skill": "Misconception"},
        {"Student": "Jia",    "Topic": "Quantum Mechanics",       "Readiness": 92, "Weak Skill": "None"},
        {"Student": "Fahim",  "Topic": "Machine Learning",        "Readiness": 55, "Weak Skill": "Application"},
        {"Student": "Rafi",   "Topic": "Data Structures",         "Readiness": 68, "Weak Skill": "Core Concept"},
        {"Student": "Nadia",  "Topic": "Machine Learning",        "Readiness": 84, "Weak Skill": "Definition"},
        {"Student": "Chen",   "Topic": "Artificial Intelligence", "Readiness": 88, "Weak Skill": "None"},
        {"Student": "Sara",   "Topic": "Statistics",              "Readiness": 62, "Weak Skill": "Core Concept"},
        {"Student": "Omar",   "Topic": "Neural Network",          "Readiness": 79, "Weak Skill": "Application"},
    ])


def build_teacher_dataframe(latest_session=None) -> pd.DataFrame:
    df = demo_teacher_data()
    if latest_session:
        df = pd.concat([pd.DataFrame([latest_session]), df], ignore_index=True)
    return df


def class_average_readiness(df: pd.DataFrame) -> float:
    return round(float(df["Readiness"].mean()), 1)


def readiness_label(score: float) -> str:
    if score >= 85:
        return "Lecture-ready"
    if score >= 65:
        return "Almost ready"
    return "Needs review"
