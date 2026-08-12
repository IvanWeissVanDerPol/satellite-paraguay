"""Evaluation module."""

from .metrics import (
    benchmark_against_hansen,
    benchmark_against_mapbiomas,
    classification_metrics,
    confusion_matrix_segmentation,
    detection_map,
    mean_iou,
    pixel_f1_score,
    pixel_iou,
    print_metrics,
    regression_metrics,
)

__all__ = [
    "pixel_f1_score",
    "pixel_iou",
    "mean_iou",
    "confusion_matrix_segmentation",
    "detection_map",
    "regression_metrics",
    "classification_metrics",
    "benchmark_against_mapbiomas",
    "benchmark_against_hansen",
    "print_metrics",
]
