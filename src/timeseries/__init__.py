"""Timeseries module."""
from .analysis import (
    stack_timeseries,
    compute_ndvi_timeseries,
    detect_changes_bfast,
    compute_trend,
    compute_anomaly,
    aggregate_by_department,
)

__all__ = [
    "stack_timeseries",
    "compute_ndvi_timeseries",
    "detect_changes_bfast",
    "compute_trend",
    "compute_anomaly",
    "aggregate_by_department",
]
