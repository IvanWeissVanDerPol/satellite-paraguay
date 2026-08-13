#!/usr/bin/env python3
"""Statistical analysis for paper figures.

Implements:
- Bootstrap confidence intervals (95%) for F1, mIoU, precision, recall
- McNemar's test for pairwise model comparison
- Paired t-test for metric differences across folds
- Effect size (Cohen's d) for practical significance
"""

import numpy as np
from scipy import stats


def bootstrap_ci(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    metric_func: callable,  # type: ignore[valid-type]
    n_bootstrap: int = 1000,
    ci: float = 0.95,
    seed: int = 42,
) -> tuple[float, float, float]:
    """Compute bootstrap confidence interval for a metric.

    Args:
        y_true: ground truth labels
        y_pred: predicted labels
        metric_func: function (y_true, y_pred) -> scalar
        n_bootstrap: number of bootstrap samples
        ci: confidence level (0-1)
        seed: random seed

    Returns:
        (point_estimate, lower_bound, upper_bound)
    """
    rng = np.random.default_rng(seed)
    n = len(y_true)
    point_est = metric_func(y_true, y_pred)  # type: ignore[misc]

    boot_scores = []
    for _ in range(n_bootstrap):
        idx = rng.integers(0, n, size=n)
        boot_scores.append(metric_func(y_true[idx], y_pred[idx]))  # type: ignore[misc]

    boot_scores = np.array(boot_scores)  # type: ignore[assignment]
    alpha = (1 - ci) / 2
    lower = np.percentile(boot_scores, alpha * 100)
    upper = np.percentile(boot_scores, (1 - alpha) * 100)

    return float(point_est), float(lower), float(upper)


def mcnemar_test(y_true: np.ndarray, pred_a: np.ndarray, pred_b: np.ndarray) -> dict:
    """McNemar's test for comparing two classifiers.

    Args:
        y_true: ground truth labels
        pred_a: predictions from model A
        pred_b: predictions from model B

    Returns:
        dict with chi2, p-value, contingency table
    """
    # Both correct
    a_correct = pred_a == y_true
    b_correct = pred_b == y_true

    # b01: A wrong, B right
    b01 = int((~a_correct & b_correct).sum())
    # b10: A right, B wrong
    b10 = int((a_correct & ~b_correct).sum())

    # McNemar's chi-squared (with continuity correction)
    if b01 + b10 == 0:
        chi2, p_value = 0.0, 1.0
    else:
        from scipy.stats import binomtest

        # Use exact binomial test for McNemar's test (more compatible)
        n_disagree = b01 + b10
        result = binomtest(b01, n_disagree, p=0.5)
        chi2 = (abs(b01 - b10) - 1) ** 2 / n_disagree if n_disagree > 0 else 0
        p_value = result.pvalue if n_disagree > 0 else 1.0

    return {
        "chi2": float(chi2),
        "p_value": float(p_value),
        "b01_a_wrong_b_right": b01,
        "b10_a_right_b_wrong": b10,
        "n_disagree": b01 + b10,
        "significant_at_0.05": p_value < 0.05,
    }


def cohens_d(group1: np.ndarray, group2: np.ndarray) -> float:
    """Compute Cohen's d effect size."""
    n1, n2 = len(group1), len(group2)
    var1, var2 = group1.var(ddof=1), group2.var(ddof=1)
    pooled_std = np.sqrt(((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2))
    if pooled_std == 0:
        return 0.0  # identical groups -> no effect
    return (group1.mean() - group2.mean()) / pooled_std  # type: ignore[no-any-return]


def paired_ttest(scores1: np.ndarray, scores2: np.ndarray) -> dict:
    """Paired t-test for two sets of scores (e.g., cross-validation folds)."""
    t_stat, p_value = stats.ttest_rel(scores1, scores2)
    return {
        "t_stat": float(t_stat),
        "p_value": float(p_value),
        "mean_diff": float(scores1.mean() - scores2.mean()),
        "cohens_d": float(cohens_d(scores1, scores2)),
        "significant_at_0.05": p_value < 0.05,
    }


def generate_confidence_intervals_table(results: dict, output_path: str) -> dict:  # type: ignore[empty-body]
    """Generate CI table for all models on all metrics."""

    # This is a placeholder - actual implementation requires
    # raw predictions per tile to bootstrap over


if __name__ == "__main__":
    print("Statistical analysis utilities loaded.")
    print("Available functions:")
    print("  - bootstrap_ci(y_true, y_pred, metric_func)")
    print("  - mcnemar_test(y_true, pred_a, pred_b)")
    print("  - cohens_d(group1, group2)")
    print("  - paired_ttest(scores1, scores2)")
