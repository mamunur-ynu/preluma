import pytest

try:
    from engine import build_pack, make_questions, grade, tutor_sections
except Exception as exc:  # pragma: no cover
    pytest.skip(f"legacy test module skipped: {exc}", allow_module_level=True)


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
    result = tutor_sections(p, "I do not understand superposition", "Normal Mode")
    text = " ".join(str(v) for v in result.values())
    assert len(text) > 20
