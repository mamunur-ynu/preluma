"""Pure-Python analysis, manual sorting, manual searching, and timing.

No pandas, numpy, sklearn, matplotlib, Streamlit, or Plotly is used in this file.
"""
from __future__ import annotations

from time import perf_counter_ns

from models import AnalysisResult, StudentRecord


def mean(values: list[float]) -> float:
    total = 0.0
    count = 0
    for value in values:
        total += value
        count += 1
    return total / count if count else 0.0


def population_variance(values: list[float]) -> float:
    if not values:
        return 0.0
    average = mean(values)
    total = 0.0
    for value in values:
        difference = value - average
        total += difference * difference
    return total / len(values)


def merge_sort_by_readiness(records: list[StudentRecord], reverse: bool = True) -> list[StudentRecord]:
    """Manual Merge Sort implementation for readiness ranking."""
    if len(records) <= 1:
        return records[:]
    middle = len(records) // 2
    left = merge_sort_by_readiness(records[:middle], reverse)
    right = merge_sort_by_readiness(records[middle:], reverse)
    return _merge(left, right, reverse)


def _merge(left: list[StudentRecord], right: list[StudentRecord], reverse: bool) -> list[StudentRecord]:
    merged: list[StudentRecord] = []
    i = 0
    j = 0
    while i < len(left) and j < len(right):
        take_left = left[i].readiness >= right[j].readiness if reverse else left[i].readiness <= right[j].readiness
        if take_left:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    while i < len(left):
        merged.append(left[i])
        i += 1
    while j < len(right):
        merged.append(right[j])
        j += 1
    return merged


def sort_by_student_name(records: list[StudentRecord]) -> list[StudentRecord]:
    """Manual Merge Sort by normalized student name for Binary Search preparation."""
    if len(records) <= 1:
        return records[:]
    middle = len(records) // 2
    left = sort_by_student_name(records[:middle])
    right = sort_by_student_name(records[middle:])
    merged: list[StudentRecord] = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i].student.casefold() <= right[j].student.casefold():
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    return merged + left[i:] + right[j:]


def binary_search_student(records: list[StudentRecord], target: str) -> int:
    """Manual Binary Search over records already sorted by student name."""
    wanted = target.casefold().strip()
    low = 0
    high = len(records) - 1
    while low <= high:
        mid = low + (high - low) // 2
        current = records[mid].student.casefold().strip()
        if current == wanted:
            return mid
        if current < wanted:
            low = mid + 1
        else:
            high = mid - 1
    return -1


def most_common_weak_skill(records: list[StudentRecord]) -> str:
    counts: dict[str, int] = {}
    for record in records:
        key = record.weak_skill or "Unknown"
        counts[key] = counts.get(key, 0) + 1
    best_key = "None"
    best_count = -1
    for key, count in counts.items():
        if count > best_count:
            best_key = key
            best_count = count
    return best_key


def analyze(records: list[StudentRecord]) -> tuple[AnalysisResult, list[StudentRecord]]:
    """Run statistics and sort ranking while measuring execution time."""
    start = perf_counter_ns()
    readiness_values = [record.readiness for record in records]
    ranked = merge_sort_by_readiness(records, reverse=True)
    result = AnalysisResult(
        student_count=len(records),
        average_readiness=round(mean(readiness_values), 2),
        lowest_readiness=round(min(readiness_values), 2) if readiness_values else 0.0,
        highest_readiness=round(max(readiness_values), 2) if readiness_values else 0.0,
        variance=round(population_variance(readiness_values), 2),
        most_common_weak_skill=most_common_weak_skill(records),
        elapsed_ns=perf_counter_ns() - start,
    )
    return result, ranked
