"""Command-line entry point for course-compliance demonstration.

Run: python main.py
This uses only Python standard-library based modules for CSV loading,
statistics, manual sorting, manual searching, timing, and result.txt output.
"""
from __future__ import annotations

from analyzer import analyze, binary_search_student, sort_by_student_name
from data_loader import load_records, write_result

DATASET_PATH = "dataset.csv"
RESULT_PATH = "result.txt"


def format_report() -> list[str]:
    records = load_records(DATASET_PATH)
    summary, ranked = analyze(records)
    sorted_by_name = sort_by_student_name(records)
    sample_target = records[0].student if records else ""
    found_index = binary_search_student(sorted_by_name, sample_target) if sample_target else -1

    lines = [
        "Preluma Pure-Python Course Compliance Result",
        "============================================",
        f"Dataset file: {DATASET_PATH}",
        f"Student count: {summary.student_count}",
        f"Average readiness: {summary.average_readiness}",
        f"Lowest readiness: {summary.lowest_readiness}",
        f"Highest readiness: {summary.highest_readiness}",
        f"Population variance: {summary.variance}",
        f"Most common weak skill: {summary.most_common_weak_skill}",
        f"Timed analysis operation: {summary.elapsed_ns} ns",
        "",
        "Manual Merge Sort ranking:",
    ]
    for number, record in enumerate(ranked, start=1):
        lines.append(f"{number}. {record.student} | {record.topic} | readiness={record.readiness}")
    lines.extend([
        "",
        "Manual Binary Search demonstration:",
        f"Target student: {sample_target}",
        f"Found index in name-sorted records: {found_index}",
    ])
    return lines


def main() -> None:
    try:
        lines = format_report()
        write_result(RESULT_PATH, lines)
        print("Analysis complete. See result.txt")
    except FileNotFoundError as error:
        print(f"Error: {error}")
    except Exception as error:
        print(f"Unexpected error: {error}")


if __name__ == "__main__":
    main()
