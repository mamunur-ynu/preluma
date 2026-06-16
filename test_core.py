from engine import build_pack, make_questions, grade, tutor_sections


def test_pack():
    p = build_pack("Quantum Mechanics", use_wikipedia=False)
    assert p["title"] == "Quantum Mechanics"


def test_quiz():
    p = build_pack("Machine Learning", use_wikipedia=False)
    qs = make_questions(p)
    result = grade(qs, {i: q["answer"] for i, q in enumerate(qs)})
    assert result["score"] == len(qs)


def test_tutor():
    p = build_pack("Quantum Mechanics", use_wikipedia=False)
    sections = tutor_sections(p, "I do not understand superposition", "Kid-simple")
    combined = " ".join(str(v) for v in sections.values())
    assert len(combined) > 20
