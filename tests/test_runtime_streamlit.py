from streamlit.testing.v1 import AppTest


def _click(at, label):
    for button in at.button:
        if button.label == label:
            button.click().run()
            assert len(at.exception) == 0
            return
    raise AssertionError(f"Button not found: {label}")


def test_streamlit_startup_and_guided_flow():
    at = AppTest.from_file("streamlit_app.py", default_timeout=30).run()
    assert len(at.exception) == 0
    for label in [
        "Start Pre-Class Mission",
        "See a Real Example →",
        "Try It Yourself →",
        "Take the Mock Test →",
        "Submit Mock Test",
        "View Final Overview →",
    ]:
        _click(at, label)
    assert len(at.exception) == 0


def test_streamlit_sidebar_pages_open():
    at = AppTest.from_file("streamlit_app.py", default_timeout=30).run()
    assert len(at.exception) == 0
    radio = at.sidebar.radio[0]
    for page in ["✨ Ask Preluma AI", "Homework Center"]:
        radio.set_value(page).run()
        assert len(at.exception) == 0
        radio = at.sidebar.radio[0]
    homework_page = next(value for value in radio.options if value.startswith("🔔 My Homework"))
    radio.set_value(homework_page).run()
    assert len(at.exception) == 0


def test_project_team_page_and_question_aware_ai():
    at = AppTest.from_file("streamlit_app.py", default_timeout=30).run()
    radio = at.sidebar.radio[0]
    radio.set_value("Project Team").run()
    assert len(at.exception) == 0
    assert any("Team Preluma" in (item.value or "") for item in at.markdown)

    radio = at.sidebar.radio[0]
    radio.set_value("✨ Ask Preluma AI").run()
    assert len(at.exception) == 0
    at.text_area[0].set_value("about machine learning").run()
    _click(at, "Ask Preluma AI")
    assert any("Machine Learning" in (item.value or "") for item in at.markdown)
    assert not any("Variance · Curated" in (item.value or "") for item in at.markdown)
