# Third-Party Library Policy

The teacher confirmed that third-party libraries may be used. For safer grading, Preluma keeps the assessed algorithmic core in pure Python standard library.

## Standard-library core

- `main.py`
- `data_loader.py`
- `analyzer.py`
- `models.py`
- `algorithms_core.py`
- `analytics_core.py`
- `storage_core.py`

These modules handle CSV I/O, statistics, manual Merge Sort, manual Binary Search, timing, exception handling, and `result.txt` output without pandas, numpy, or sklearn.

## Presentation layer

- Streamlit: web application interface
- Plotly: charts inside the teacher dashboard
- Requests: optional Wikipedia data fetcher

These are not used for the required core calculations.
