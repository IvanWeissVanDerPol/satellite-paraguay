"""Timeseries module."""

from .analysis import (
    aggregate_by_department,
    compute_anomaly,
    compute_ndvi_timeseries,
    compute_trend,
    detect_changes_bfast,
    stack_timeseries,
)

__all__ = [
    "stack_timeseries",
    "compute_ndvi_timeseries",
    "detect_changes_bfast",
    "compute_trend",
    "compute_anomaly",
    "aggregate_by_department",
]
