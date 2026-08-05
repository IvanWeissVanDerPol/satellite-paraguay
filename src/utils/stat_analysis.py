"""Statistical analysis utilities for model performance.

Bootstrap CIs and metric aggregation from confusion matrices.
"""
from typing import Any, Dict, Optional

import numpy as np


def bootstrap_ci_from_confusion(
    tp: int,
    fp: int,
    fn: int,
    tn: int,
    n_bootstrap: int = 10000,
    ci: float = 0.95,
    seed: int = 42,
) -> Dict[str, Dict[str, float]]:
    """Bootstrap CI for precision, recall, F1 from confusion matrix counts.

    Returns dict with precision, recall, f1 each containing mean,
    ci_lower, ci_upper.
    """
    rng = np.random.default_rng(seed)
    n = tp + fp + fn + tn

    if n == 0:
        return {
            "precision": {"mean": 0.0, "ci_lower": 0.0, "ci_upper": 0.0},
            "recall": {"mean": 0.0, "ci_lower": 0.0, "ci_upper": 0.0},
            "f1": {"mean": 0.0, "ci_lower": 0.0, "ci_upper": 0.0},
        }

    boot_p = []
    boot_r = []
    boot_f1 = []

    p_n = tp / n
    fp_n = fp / n
    fn_n = fn / n
    tn_n = tn / n

    for _ in range(n_bootstrap):
        # Sample with replacement from the implied multinomial
        counts = rng.multinomial(n, [p_n, fp_n, fn_n, tn_n])
        tp_b, fp_b, fn_b, tn_b = counts
        if tp_b + fp_b == 0:
            p = 0.0
        else:
            p = tp_b / (tp_b + fp_b)
        if tp_b + fn_b == 0:
            r = 0.0
        else:
            r = tp_b / (tp_b + fn_b)
        if p + r == 0:
            f1 = 0.0
        else:
            f1 = 2 * p * r / (p + r)
        boot_p.append(p)
        boot_r.append(r)
        boot_f1.append(f1)

    alpha = (1 - ci) / 2
    lower = int(alpha * 100)
    upper = int((1 - alpha) * 100)

    def stats(arr):
        return {
            "mean": float(np.mean(arr)),
            "ci_lower": float(np.percentile(arr, lower)),
            "ci_upper": float(np.percentile(arr, upper)),
        }

    return {
        "precision": stats(boot_p),
        "recall": stats(boot_r),
        "f1": stats(boot_f1),
    }


def metric_stats_with_ci(
    metric_values: list, ci: float = 0.95
) -> Dict[str, float]:
    """Compute mean and CI for a list of metric values."""
    arr = np.array(metric_values)
    if len(arr) == 0:
        return {"mean": 0.0, "std": 0.0, "ci_lower": 0.0, "ci_upper": 0.0, "n": 0}
    alpha = (1 - ci) / 2
    return {
        "mean": float(arr.mean()),
        "std": float(arr.std()),
        "ci_lower": float(np.percentile(arr, alpha * 100)),
        "ci_upper": float(np.percentile(arr, (1 - alpha) * 100)),
        "n": len(arr),
    }


def aggregate_metrics(
    metrics_list: list, ci: float = 0.95
) -> Dict[str, Dict[str, float]]:
    """Aggregate metrics across multiple runs.

    metrics_list: list of dicts with 'f1', 'precision', 'recall' keys.
    """
    keys = ["f1", "precision", "recall"]
    return {
        k: metric_stats_with_ci([m.get(k, 0) for m in metrics_list], ci)
        for k in keys
    }


def analyze_confusion_matrix(
    tp: int, fp: int, fn: int, tn: int
) -> Dict[str, float]:
    """Compute summary metrics from confusion matrix."""
    total = tp + fp + fn + tn
    if total == 0:
        return {"precision": 0.0, "recall": 0.0, "f1": 0.0, "accuracy": 0.0, "n": 0}
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = (
        2 * precision * recall / (precision + recall)
        if (precision + recall) > 0
        else 0.0
    )
    accuracy = (tp + tn) / total
    return {
        "precision": float(precision),
        "recall": float(recall),
        "f1": float(f1),
        "accuracy": float(accuracy),
        "n": total,
    }