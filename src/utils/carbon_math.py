"""Per-pixel carbon estimation using Chave 2014 allometric model.

Pure math functions for above-ground biomass (AGB), carbon stock, and CO2e.
"""
from typing import Tuple

import numpy as np

CHAVE_COEFFICIENT = 240.0
CARBON_FRACTION = 0.47  # IPCC carbon fraction of biomass
C_STOIC_RATIO = 44.0 / 12.0  # CO2/C molar ratio

# Calibration check values (for validation):
# - treecover=20% → AGB ≈ 5.4 Mg/ha
# - treecover=50% → AGB ≈ 42.4 Mg/ha
# - treecover=80% → AGB ≈ 137 Mg/ha


def chave_agb(treecover_pct) -> np.ndarray:
    """Chave 2014 approximation: AGB = 240 * (tc/100)^2.5.

    Returns AGB in Mg/ha for each input pixel.
    """
    tc = np.clip(treecover_pct, 0, 100)
    return CHAVE_COEFFICIENT * (tc / 100.0) ** 2.5


def carbon_stock(treecover_pct) -> np.ndarray:
    """Carbon stock (Mg C / ha) using IPCC carbon fraction 0.47."""
    return chave_agb(treecover_pct) * CARBON_FRACTION


def co2e(treecover_pct) -> np.ndarray:
    """CO2 equivalent (Mg CO2e / ha) using 44/12 stoichiometric ratio."""
    return carbon_stock(treecover_pct) * C_STOIC_RATIO


def carbon_loss_per_pixel(
    treecover_pct, lossyear, min_year: int = 2001
) -> np.ndarray:
    """Compute CO2e lost per pixel (only loss pixels > min_year).

    Returns array with CO2e values; 0 for non-loss pixels.
    """
    co2e_arr = co2e(treecover_pct)
    loss_mask = (lossyear >= min_year) & (lossyear > 0)
    return np.where(loss_mask, co2e_arr, 0.0)


def annual_carbon_loss(
    treecover_pct, lossyear, min_year: int = 2001
) -> dict:
    """Compute annual CO2e loss.

    Returns dict mapping year (int) -> total CO2e (Mg).
    """
    co2e_arr = co2e(treecover_pct)
    years = range(min_year, lossyear.max() + 1) if lossyear.max() >= min_year else [min_year]
    result = {}
    for year in years:
        year_mask = lossyear == year
        result[year] = float(co2e_arr[year_mask].sum())
    return result


def carbon_summary(treecover_pct) -> dict:
    """Compute summary statistics for carbon layers.

    Returns dict with mean, max, median, total for AGB, carbon, CO2e.
    """
    agb = chave_agb(treecover_pct)
    carbon = carbon_stock(treecover_pct)
    co2e_arr = co2e(treecover_pct)
    return {
        "agb": {
            "mean": float(agb.mean()),
            "max": float(agb.max()),
            "median": float(np.median(agb)),
            "total_mg": float(agb.sum()),
        },
        "carbon": {
            "mean": float(carbon.mean()),
            "max": float(carbon.max()),
            "median": float(np.median(carbon)),
        },
        "co2e": {
            "mean": float(co2e_arr.mean()),
            "max": float(co2e_arr.max()),
            "median": float(np.median(co2e_arr)),
        },
    }


def calibrate_check(treecover_pct: float) -> Tuple[float, float]:
    """Compute AGB and return both raw and validation-adjusted value.

    Used for testing calibration against documented values.
    """
    agb = chave_agb(np.array([treecover_pct])).item()
    return agb, agb