from smartprep.engine import build_pack, make_questions, grade, tutor

def test_pack():
    p = build_pack("Quantum Mechanics")
    assert p["title"] == "Quantum Mechanics"

def test_quiz():
    p = build_pack("Machine Learning")
    qs = make_questions(p)
    result = grade(qs, {i: q["answer"] for i, q in enumerate(qs)})
    assert result["score"] == len(qs)

def test_tutor():
    p = build_pack("Quantum Mechanics")
    assert len(tutor(p, "I do not understand superposition", "Kid-simple")) > 20
