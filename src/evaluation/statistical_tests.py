"""Statistical significance tests for thesis findings.

Pure statistical functions for:
1. McNemar's test on classification models
2. Paired t-test on per-year loss (drought vs non-drought years)
3. Chi-squared test on indigenous territory disparity
4. Bootstrap hypothesis test for disparity ratios
5. Numpy type cleaning for JSON serialization
"""

from typing import Any, Dict, List, Union

import numpy as np


def mcnemar_test(
    y_true: np.ndarray,
    y_pred_a: np.ndarray,
    y_pred_b: np.ndarray,
) -> Dict[str, Any]:
    """McNemar's test for comparing two classifiers.

    Returns dict with chi2, p_value, n12, n21, n_total, significant_at_005.
    Uses exact binomial test for small samples.
    """
    n12 = ((y_pred_a == y_true) & (y_pred_b != y_true)).sum()
    n21 = ((y_pred_a != y_true) & (y_pred_b == y_true)).sum()

    n = n12 + n21
    if n == 0:
        return {
            "chi2": 0.0,
            "p_value": 1.0,
            "n12": int(n12),
            "n21": int(n21),
            "n_total": 0,
            "significant_at_005": False,
        }

    from scipy.stats import binomtest

    result = binomtest(min(int(n12), int(n21)), n=int(n), p=0.5)
    p_value = 2 * result.pvalue
    chi2 = (abs(n12 - n21) - 1) ** 2 / n if n > 0 else 0

    return {
        "chi2": float(chi2),
        "p_value": float(p_value),
        "n12": int(n12),
        "n21": int(n21),
        "n_total": int(n),
        "significant_at_005": p_value < 0.05,
    }


def chi_squared_indigenous(
    observed_territories: Dict[str, int],
    expected_at_national_rate: Dict[str, int],
) -> Dict[str, Any]:
    """Chi-squared test for indigenous territory deforestation disparity.

    H0: territories have same deforestation rate as national.
    H1: territories have higher deforestation rate.
    """
    from scipy.stats import chi2_contingency

    obs_table = np.array(
        [
            [
                observed_territories["lost"],
                observed_territories["total"] - observed_territories["lost"],
            ],
            [
                expected_at_national_rate["lost"],
                expected_at_national_rate["total"] - expected_at_national_rate["lost"],
            ],
        ]
    )

    chi2, p_value, dof, expected = chi2_contingency(obs_table)
    n = obs_table.sum()
    cramers_v = float(np.sqrt(chi2 / n)) if n > 0 else 0.0

    return {
        "chi2": float(chi2),
        "p_value": float(p_value),
        "dof": int(dof),
        "cramers_v": cramers_v,
        "observed": observed_territories,
        "expected": expected_at_national_rate,
        "significant_at_001": p_value < 0.001,
    }


def paired_ttest_drought(
    annual_loss: Dict[int, float],
    drought_years: List[int],
    non_drought_years: List[int],
) -> Dict[str, Any]:
    """Welch's t-test for drought vs non-drought year loss.

    Args:
        annual_loss: dict mapping year -> loss value
        drought_years: list of drought years
        non_drought_years: list of non-drought years

    Returns dict with t_statistic, p_value, mean_drought, etc.
    Returns {"error": "insufficient data"} when not enough samples.
    """
    from scipy.stats import ttest_ind

    drought_loss = [annual_loss[y] for y in drought_years if y in annual_loss]
    non_drought_loss = [annual_loss[y] for y in non_drought_years if y in annual_loss]

    if len(drought_loss) < 2 or len(non_drought_loss) < 2:
        return {"error": "insufficient data"}

    t_stat, p_value = ttest_ind(drought_loss, non_drought_loss, equal_var=False)

    mean_d = float(np.mean(drought_loss))
    mean_n = float(np.mean(non_drought_loss))
    return {
        "t_statistic": float(t_stat),
        "p_value": float(p_value),
        "n_drought": len(drought_loss),
        "n_non_drought": len(non_drought_loss),
        "mean_drought": mean_d,
        "mean_non_drought": mean_n,
        "drought_higher": mean_d > mean_n,
        "significant_at_005": p_value < 0.05,
    }


def bootstrap_disparity(
    territory_loss_pcts: Union[List[float], np.ndarray],
    national_loss_pct: float,
    n_boot: int = 10000,
    threshold_ratio: float = 1.5,
    seed: int = 42,
) -> Dict[str, Any]:
    """Bootstrap test for disparity ratio.

    H0: territory mean = national rate.
    H1: territory mean > threshold_ratio * national rate.
    """
    rng = np.random.default_rng(seed)
    n = len(territory_loss_pcts)
    threshold = threshold_ratio * national_loss_pct

    ratios = []
    for _ in range(n_boot):
        boot_sample = rng.choice(territory_loss_pcts, size=n, replace=True)
        ratios.append(boot_sample.mean() / national_loss_pct)
    ratios = np.array(ratios)

    p_value = (ratios > threshold).mean()

    return {
        "bootstrap_mean_ratio": float(ratios.mean()),
        "bootstrap_ci_lower": float(np.percentile(ratios, 2.5)),
        "bootstrap_ci_upper": float(np.percentile(ratios, 97.5)),
        "p_value_h1_gt_1_5x": float(p_value),
        "n_bootstrap": n_boot,
        "threshold_1_5x": float(threshold),
        "significant_at_001": p_value < 0.001,
    }


def to_native(obj: Any) -> Any:
    """Convert numpy types to Python native for JSON serialization."""
    if isinstance(obj, np.integer):
        return int(obj)
    if isinstance(obj, np.floating):
        return float(obj)
    if isinstance(obj, np.bool_):
        return bool(obj)
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    return obj


def clean_for_json(obj: Any) -> Any:
    """Recursively clean numpy types for JSON serialization."""
    if isinstance(obj, dict):
        return {k: clean_for_json(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [clean_for_json(v) for v in obj]
    return to_native(obj)
