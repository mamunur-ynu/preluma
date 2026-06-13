# Preluma V22 — Guided Learning + Homework MVP

Preluma is now a connected pre-class learning and homework diagnostic prototype.

## Guided Student Mission

The input form disappears after the student starts a mission. The same main area becomes a five-step learning journey:

1. Understand the Big Idea
2. See It in Real Life
3. Practice the Idea
4. Mini Mock Test
5. Final Learning Overview

The final overview shows readiness, weak skill, review direction, and class-ready questions.

## Ask Preluma AI

The sidebar contains a dedicated AI tutor page with these modes:

- Explain like I am 5
- Friendly Tutor
- Step-by-Step
- Exam/Viva Answer
- Give More Examples

Mission and homework mistake context can be passed to this tutor.

## Homework MVP

Teacher:
- Creates and publishes homework
- Assigns to all students or named students
- Creates student notifications
- Views submissions, average, highest, lowest, and common weak concept

Student:
- Receives homework notification
- Completes homework in Preluma
- Receives automatic marking
- Reviews mistakes
- Captures weak concepts
- Sends mistake context to Preluma AI

## Physical data files

Created at runtime with Python csv:

- data/homework.csv
- data/homework_questions.csv
- data/homework_submissions.csv
- data/student_mistakes.csv
- data/notifications.csv
- data/students.csv
- result.txt

## Account scope

Real user accounts are intentionally not implemented in this MVP. The active student name simulates user identity. Authentication, class membership, permissions, and database migration are shown in the Future Roadmap.

## Safe secret management

Never upload a real `.streamlit/secrets.toml` to GitHub. Add API keys only through Streamlit Cloud Secrets.
