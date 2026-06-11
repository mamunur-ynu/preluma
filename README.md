# Preluma V20 Compliance Elite

Strict technical compliance version.

## Upgrades
- Removed pandas from core analytics and teacher backend.
- Added pure Python mean, population variance, sample variance, frequency count, unique count.
- Added manual Merge Sort for readiness ranking.
- Added manual Merge Sort by normalized name and Binary Search for student lookup.
- Added Linear Search baseline.
- Added timing with time.perf_counter_ns().
- Added physical persistence with data/students.csv using csv module.
- Added result.txt audit log for algorithm timings.

## Teacher defense line
The teacher dashboard no longer depends on pandas for analytics. It reads records from students.csv, computes all math using pure Python loops, ranks students using manual Merge Sort, searches students using Binary Search, measures execution time with perf_counter_ns(), and appends evidence to result.txt.

## Upload checklist
streamlit_app.py, engine.py, topics.py, teacher.py, wiki_fetcher.py, analytics_core.py, algorithms_core.py, storage_core.py, requirements.txt, README.md, DEPLOYMENT_GUIDE.md, tests/, assets/ynu_campus.jpg, assets/team_preluma.jpg
