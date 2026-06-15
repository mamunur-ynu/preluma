from pathlib import Path

from engine import build_pack, make_questions
from topics import TOPIC_OPTIONS


def test_quiz_options_are_unique_for_all_curated_topics():
    for topic in TOPIC_OPTIONS:
        if topic == "Custom Topic":
            continue
        questions = make_questions(build_pack(topic, use_wikipedia=False))
        for question in questions:
            options = question["options"]
            assert len(options) == 4
            assert len(options) == len(set(options))


def test_course_required_files_exist():
    required = [
        "main.py",
        "data_loader.py",
        "analyzer.py",
        "models.py",
        "dataset.csv",
        "result.txt",
        "README.md",
    ]
    for filename in required:
        assert Path(filename).exists(), filename
