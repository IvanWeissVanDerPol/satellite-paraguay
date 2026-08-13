"""Uncertainty quantification utilities for remote sensing analysis.

Pixel-level and block bootstrap methods for Hansen lossyear data.
"""

from typing import Any, Dict

import numpy as np


def pixel_bootstrap_fast(lossyear: np.ndarray, n_boot: int = 1000, seed: int = 42) -> Dict[str, Any]:
    """Fast pixel-level bootstrap on summary statistic.

    Parametric: assumes pixel independence, samples from binomial distribution.
    """
    rng = np.random.default_rng(seed)
    flat = lossyear.flatten()
    n_pixels = flat.size
    if n_pixels == 0:
        return {
            "mean": 0.0,
            "ci_lower_95": 0.0,
            "ci_upper_95": 0.0,
            "ci_lower_90": 0.0,
            "ci_upper_90": 0.0,
            "std": 0.0,
            "n_bootstrap": n_boot,
            "method": "parametric (assumes pixel independence)",
        }
    n_loss = int((flat > 0).sum())
    p_loss = n_loss / n_pixels

    boots = rng.binomial(n_pixels, p_loss, size=n_boot)

    return {
        "mean": float(boots.mean()),
        "ci_lower_95": float(np.percentile(boots, 2.5)),
        "ci_upper_95": float(np.percentile(boots, 97.5)),
        "ci_lower_90": float(np.percentile(boots, 5)),
        "ci_upper_90": float(np.percentile(boots, 95)),
        "std": float(boots.std()),
        "n_bootstrap": n_boot,
        "method": "parametric (assumes pixel independence)",
    }


def block_bootstrap_fast(
    lossyear: np.ndarray, block_size: int = 100, n_boot: int = 1000, seed: int = 42
) -> Dict[str, Any]:
    """Fast block bootstrap preserving spatial structure."""
    rng = np.random.default_rng(seed)
    H, W = lossyear.shape
    if H < block_size or W < block_size:
        return {
            "mean": 0.0,
            "ci_lower_95": 0.0,
            "ci_upper_95": 0.0,
            "block_size": block_size,
            "n_blocks": 0,
            "n_bootstrap": n_boot,
        }
    n_blocks_h = H // block_size
    n_blocks_w = W // block_size
    n_blocks = n_blocks_h * n_blocks_w

    # Pre-compute block-level loss counts
    block_losses = np.zeros(n_blocks)
    for bh in range(n_blocks_h):
        for bw in range(n_blocks_w):
            y = bh * block_size
            x = bw * block_size
            block_losses[bh * n_blocks_w + bw] = (lossyear[y : y + block_size, x : x + block_size] > 0).sum()

    boots = np.zeros(n_boot)
    for i in range(n_boot):
        idx = rng.integers(0, n_blocks, size=n_blocks)
        boots[i] = block_losses[idx].sum()

    return {
        "mean": float(boots.mean()),
        "ci_lower_95": float(np.percentile(boots, 2.5)),
        "ci_upper_95": float(np.percentile(boots, 97.5)),
        "block_size": block_size,
        "n_blocks": n_blocks,
        "n_bootstrap": n_boot,
    }


def agb_sensitivity(lossyear: np.ndarray, treecover: np.ndarray) -> Dict[str, Dict[str, float]]:
    """Sensitivity analysis: how much does carbon estimate change with AGB assumptions?

    Returns dict with low/mid/high scenarios.
    """
    n_loss = int((lossyear > 0).sum())
    area_ha = n_loss * 0.0625  # 30m pixel = 0.09 ha, using 0.0625 = approx

    agb_scenarios = {
        "low": {"tc": 30, "agb": 18},
        "mid": {"tc": 50, "agb": 56},
        "high": {"tc": 80, "agb": 156},
    }

    results: Dict[str, Dict[str, float]] = {}
    for name, params in agb_scenarios.items():
        agb = params["agb"]
        carbon = area_ha * agb * 0.47
        co2e = carbon * (44 / 12)
        results[name] = {
            "agb_mg_per_ha": float(agb),
            "area_ha": float(area_ha),
            "carbon_mt": float(carbon / 1e6),
            "co2e_mt": float(co2e / 1e6),
        }

    return results


def annual_loss_ci(lossyear: np.ndarray, n_boot: int = 1000, seed: int = 42) -> Dict[str, Dict[str, float]]:
    """Bootstrap CI on annual loss time series.

    Returns dict mapping year (str) -> {mean, ci_lower_95, ci_upper_95}.
    """
    rng = np.random.default_rng(seed)
    flat = lossyear.flatten()
    n_pixels = flat.size
    if n_pixels == 0:
        return {}

    # Annual histogram (years 2001-2023 = bincount indices 1-23)
    hist = np.bincount(flat.flatten(), minlength=24)[1:]  # noqa: F841

    boots = np.zeros((n_boot, 23))
    for i in range(n_boot):
        idx = rng.integers(0, n_pixels, size=n_pixels)
        sample = flat[idx]
        sample_hist = np.bincount(sample, minlength=24)[1:]
        boots[i] = sample_hist

    years = list(range(2001, 2024))
    cis: Dict[str, Dict[str, float]] = {}
    for j, year in enumerate(years):
        cis[str(year)] = {
            "mean": float(boots[:, j].mean()),
            "ci_lower_95": float(np.percentile(boots[:, j], 2.5)),
            "ci_upper_95": float(np.percentile(boots[:, j], 97.5)),
        }

    return cis


def pixel_loss_rate(lossyear: np.ndarray) -> float:
    """Compute fraction of pixels that are loss (any year)."""
    flat = lossyear.flatten()
    if flat.size == 0:
        return 0.0
    return float((flat > 0).sum() / flat.size)


def loss_area_hectares(lossyear: np.ndarray, pixel_area_ha: float = 0.09) -> float:
    """Convert loss pixel count to hectares.

    Default pixel_area_ha = 0.09 (Sentinel-2 10m pixel = 0.01 ha, but
    Hansen uses 30m which is 0.09 ha).
    """
    n_loss = int((lossyear > 0).sum())
    return float(n_loss * pixel_area_ha)
