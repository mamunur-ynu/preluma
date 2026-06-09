import pandas as pd

def demo_teacher_data():
    return pd.DataFrame([
        {"Student": "Mim", "Topic": "Quantum Mechanics", "Readiness": 75, "Weak Skill": "Misconception"},
        {"Student": "Jia", "Topic": "Quantum Mechanics", "Readiness": 92, "Weak Skill": "None"},
        {"Student": "Fahim", "Topic": "Machine Learning", "Readiness": 55, "Weak Skill": "Application"},
        {"Student": "Rafi", "Topic": "Data Structures", "Readiness": 68, "Weak Skill": "Core Concept"},
        {"Student": "Nadia", "Topic": "Machine Learning", "Readiness": 84, "Weak Skill": "Definition"},
        {"Student": "Chen", "Topic": "Artificial Intelligence", "Readiness": 88, "Weak Skill": "None"},
    ])
