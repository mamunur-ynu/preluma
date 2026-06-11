from __future__ import annotations
from time import perf_counter_ns
from typing import Any, Callable

def normalize_name(name: str) -> str:
    return ' '.join(str(name).strip().casefold().split())

def timed_call(function: Callable, *args, **kwargs) -> tuple[Any, int]:
    start=perf_counter_ns(); result=function(*args, **kwargs); return result, perf_counter_ns()-start

def _key_value(row: dict[str, Any], key: str) -> Any:
    value=row.get(key,'')
    if key == 'Readiness':
        try: return float(value)
        except (TypeError,ValueError): return 0.0
    return str(value)

def merge_sort_records(rows: list[dict[str, Any]], key: str, reverse: bool=False) -> list[dict[str, Any]]:
    if len(rows)<=1: return rows[:]
    mid=len(rows)//2
    left=merge_sort_records(rows[:mid], key, reverse)
    right=merge_sort_records(rows[mid:], key, reverse)
    return _merge(left, right, key, reverse)

def _merge(left, right, key, reverse):
    merged=[]; i=0; j=0
    while i<len(left) and j<len(right):
        a=_key_value(left[i], key); b=_key_value(right[j], key)
        take_left = a>=b if reverse else a<=b
        if take_left:
            merged.append(left[i]); i+=1
        else:
            merged.append(right[j]); j+=1
    while i<len(left): merged.append(left[i]); i+=1
    while j<len(right): merged.append(right[j]); j+=1
    return merged

def add_normalized_name(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    copied=[]
    for row in rows:
        new=dict(row); new['student_name_norm']=normalize_name(str(row.get('Student', row.get('student_name','')))); copied.append(new)
    return copied

def linear_search_by_name(rows: list[dict[str, Any]], target_name: str) -> list[dict[str, Any]]:
    target=normalize_name(target_name); results=[]
    for row in rows:
        name=row.get('student_name_norm') or normalize_name(str(row.get('Student', row.get('student_name',''))))
        if name==target: results.append(row)
    return results

def binary_search_leftmost(rows: list[dict[str, Any]], target_name: str, key: str='student_name_norm') -> int:
    target=normalize_name(target_name); low=0; high=len(rows)-1; answer=-1
    while low<=high:
        mid=low+(high-low)//2; value=str(rows[mid].get(key,''))
        if value==target:
            answer=mid; high=mid-1
        elif value<target: low=mid+1
        else: high=mid-1
    return answer

def collect_binary_search_matches(rows: list[dict[str, Any]], target_name: str, key: str='student_name_norm') -> list[dict[str, Any]]:
    index=binary_search_leftmost(rows, target_name, key)
    if index==-1: return []
    target=normalize_name(target_name); matches=[]; cur=index
    while cur<len(rows) and str(rows[cur].get(key,''))==target:
        matches.append(rows[cur]); cur+=1
    return matches
