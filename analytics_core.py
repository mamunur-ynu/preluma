from __future__ import annotations
from typing import Any

def extract_numeric_values(rows: list[dict[str, Any]], field: str) -> list[float]:
    values=[]
    for row in rows:
        try: values.append(float(row.get(field,0.0)))
        except (TypeError,ValueError): continue
    return values

def mean(values: list[float]) -> float:
    total=0.0; count=0
    for value in values:
        total += float(value); count += 1
    return 0.0 if count==0 else total/count

def population_variance(values: list[float]) -> float:
    count=0
    for _ in values: count += 1
    if count==0: return 0.0
    avg=mean(values); total=0.0
    for value in values:
        diff=float(value)-avg; total += diff*diff
    return total/count

def sample_variance(values: list[float]) -> float:
    count=0
    for _ in values: count += 1
    if count<2: return 0.0
    avg=mean(values); total=0.0
    for value in values:
        diff=float(value)-avg; total += diff*diff
    return total/(count-1)

def frequency_table(rows: list[dict[str, Any]], field: str) -> list[dict[str, Any]]:
    counts={}
    for row in rows:
        key=str(row.get(field,'Unknown') or 'Unknown')
        counts[key]=counts.get(key,0)+1
    output=[]
    for key,count in counts.items(): output.append({'Weak Skill':key,'Count':count})
    return output

def unique_count(rows: list[dict[str, Any]], field: str) -> int:
    seen=set()
    for row in rows: seen.add(str(row.get(field,'')))
    return len(seen)

def readiness_summary(rows: list[dict[str, Any]]) -> dict[str, float|int]:
    values=extract_numeric_values(rows,'Readiness')
    return {'students_tracked':len(rows),'class_average':round(mean(values),1),'population_variance':round(population_variance(values),2),'sample_variance':round(sample_variance(values),2),'unique_weak_skills':unique_count(rows,'Weak Skill')}
