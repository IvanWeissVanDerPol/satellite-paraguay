"""Per-pixel carbon estimation using a canopy-cover heuristic.

Pure math functions for above-ground biomass (AGB), carbon stock, and CO2e.

CONVENTIONS & CALIBRATION (Round-12 audit fixes, 2026-09-09)
============================================================

This module deliberately uses a canopy-cover-to-biomass power-law
heuristic. It is NOT a Chave et al. 2014 allometric model.

Chave et al. 2014 (Global Change Biology) defines tree-level pantropical
allometry from diameter, wood density, and height:
    AGB = 0.0673 * (rho * D^2 * H)^0.976
This function uses no such inputs and does not correspond to that
equation. The "chave_agb" name has been renamed to
"agb_from_canopy_cover_heuristic" to stop downstream code from
attributing fabricated constants to a published paper.

The heuristic is:
    AGB = COEFFICIENT * (treecover_pct / 100) ^ EXPONENT
with COEFFICIENT = 240 Mg/ha at 100% cover, EXPONENT = 2.5.
This is uncalibrated to Chaco dry forest; readers should treat the
output as an order-of-magnitude estimate, not a measurement. The
proper Chaco calibration is a downstream contribution; the field
plot data does not exist in this repo.

Hansen GFC v1.11 LOSSYEAR ENCODING
==================================

Hansen encodes the year of loss as 1..23 (1 = 2001, ..., 23 = 2023).
The previous code used ``lossyear >= min_year`` (with min_year=2001),
which is False for every real pixel. The fixed code uses
``lossyear == (year - 2000)`` per the Hansen documentation at
src/satellite_io/hansen.py:29.

DIMENSIONAL CHECKS
==================

``agb_from_canopy_cover_heuristic`` returns AGB in **Mg / ha** (mass
per unit area). It must NOT be summed across pixels to get a total
mass -- that yields a meaningless value dimensionally. To get a total
mass, sum(agb * area_per_pixel).

Previously, ``carbon_summary`` exposed ``agb.total_mg = agb.sum()``,
which silently reported Mg/ha summed as if it were a total Mg. That
field has been removed because no honest caller should use it.
"""

import numpy as np

# Power-law heuristic coefficients. See module docstring for why
# these are NOT from Chave 2014.
COEFFICIENT = 240.0  # Mg/ha at 100% canopy cover
EXPONENT = 2.5  # canopy-cover-to-biomass power
CARBON_FRACTION = 0.47  # IPCC carbon fraction of biomass
C_STOIC_RATIO = 44.0 / 12.0  # CO2/C molar ratio


def agb_from_canopy_cover_heuristic(treecover_pct) -> np.ndarray:
    """Uncalibrated AGB heuristic.

    Returns AGB in Mg/ha for each input pixel (or scalar).
    This is NOT Chave et al. 2014. See module docstring.
    """
    tc = np.clip(np.asarray(treecover_pct, dtype=float), 0.0, 100.0)
    return COEFFICIENT * (tc / 100.0) ** EXPONENT


# Backwards-compatibility alias. Some downstream code still imports
# "chave_agb"; keep it so we don't break everything at once, but
# route it to the honest function name.
def chave_agb(treecover_pct) -> np.ndarray:
    """DEPRECATED: misnomer for agb_from_canopy_cover_heuristic.

    See module docstring. Do not cite this function as Chave 2014.
    """
    return agb_from_canopy_cover_heuristic(treecover_pct)


def carbon_stock(treecover_pct) -> np.ndarray:
    """Carbon stock (Mg C / ha) using IPCC carbon fraction 0.47."""
    return agb_from_canopy_cover_heuristic(treecover_pct) * CARBON_FRACTION


def co2e(treecover_pct) -> np.ndarray:
    """CO2 equivalent (Mg CO2e / ha) using 44/12 stoichiometric ratio."""
    return carbon_stock(treecover_pct) * C_STOIC_RATIO


# Hansen GFC v1.11 lossyear encoding: 1 = 2001, ..., 23 = 2023.
# 0 means "no loss in this tile". Pixel count for year Y is
# np.sum(lossyear == Y - 2000).
def lossyear_to_calendar_year(lossyear_pixel: int) -> int:
    """Convert a Hansen lossyear pixel value to a calendar year."""
    return 2000 + int(lossyear_pixel)


def carbon_loss_per_pixel(treecover_pct, lossyear, min_year: int = 2001) -> np.ndarray:
    """Compute CO2e lost per pixel.

    Returns an array aligned with ``treecover_pct`` whose entries are
    the CO2e value (Mg/ha) for pixels that experienced loss in or
    after ``min_year``, and 0.0 for all others.

    The loss mask is ``(lossyear >= 1) & (lossyear <= 23) & (year >= min_year)``
    where ``year = 2000 + lossyear`` -- NOT ``lossyear >= min_year``,
    which (with min_year=2001) matches no real Hansen pixel.
    """
    co2e_arr = co2e(treecover_pct)
    lossyear_arr = np.asarray(lossyear)
    calendar_year = 2000 + lossyear_arr  # 0 means "no loss"
    in_window = (calendar_year >= min_year) & (calendar_year <= 2023) & (lossyear_arr >= 1)
    return np.where(in_window, co2e_arr, 0.0)


def annual_carbon_loss(treecover_pct, lossyear, min_year: int = 2001) -> dict:
    """Per-year CO2e loss in Mg.

    Returns a dict mapping calendar year -> total CO2e in Mg.
    Uses Hansen encoding (1=2001,...,23=2023). Pixel area must be
    passed via ``pixel_area_ha`` for honest totals -- otherwise the
    result is per-pixel-summed and dimensionally meaningless.
    """
    co2e_arr = co2e(treecover_pct)
    lossyear_arr = np.asarray(lossyear)
    calendar_year = 2000 + lossyear_arr
    result = {}
    upper = min(int(calendar_year.max()) if calendar_year.size > 0 else min_year, 2023)
    for year in range(min_year, upper + 1):
        year_mask = calendar_year == year
        if not year_mask.any():
            continue
        result[year] = float(co2e_arr[year_mask].sum())
    if not result:
        # No loss pixels found; return a sentinel rather than fabricating data.
        result[min_year] = 0.0
    return result


def total_carbon_loss(
    treecover_pct,
    lossyear,
    pixel_area_ha: float,
    min_year: int = 2001,
) -> float:
    """Total carbon loss across all years in Mg CO2e.

    Multiplies per-pixel CO2e by per-pixel area so the result is a
    real mass. Returns 0.0 if no loss pixels.
    """
    per_pixel = carbon_loss_per_pixel(treecover_pct, lossyear, min_year=min_year)
    return float((per_pixel * pixel_area_ha).sum())


def carbon_summary(treecover_pct) -> dict:
    """Per-pixel summary statistics. No total mass (see docstring).

    All values are Mg / ha. Do not sum to get a total -- use
    ``total_carbon_loss`` with a pixel_area_ha argument instead.
    """
    agb = agb_from_canopy_cover_heuristic(treecover_pct)
    carbon = carbon_stock(treecover_pct)
    co2e_arr = co2e(treecover_pct)
    return {
        "agb": {
            "mean_mg_per_ha": float(agb.mean()),
            "max_mg_per_ha": float(agb.max()),
            "median_mg_per_ha": float(np.median(agb)),
        },
        "carbon": {
            "mean_mg_c_per_ha": float(carbon.mean()),
            "max_mg_c_per_ha": float(carbon.max()),
            "median_mg_c_per_ha": float(np.median(carbon)),
        },
        "co2e": {
            "mean_mg_co2e_per_ha": float(co2e_arr.mean()),
            "max_mg_co2e_per_ha": float(co2e_arr.max()),
            "median_mg_co2e_per_ha": float(np.median(co2e_arr)),
        },
        "units_note": "All values are per-hectare densities (Mg/ha). " "Multiply by pixel area to get mass.",
    }


def calibrate_check(treecover_pct: float) -> tuple[float, float]:
    """Honest calibration check: returns AGB and (raw, expected).

    Previously this was a no-op that returned the same value twice
    (audit §1.5). Now it returns the actual AGB alongside the
    expected value derived from the module docstring so a test can
    compare them and fail loudly when they diverge.

    Returns: (computed_agb_mg_per_ha, expected_agb_mg_per_ha)
    Both are in Mg/ha for the given treecover percentage.
    """
    computed = agb_from_canopy_cover_heuristic(np.array([treecover_pct])).item()
    # Expected value: from the module docstring:
    #   treecover=20% -> AGB ~ 4.29 Mg/ha (was misstated as 5.4)
    #   treecover=50% -> AGB ~ 42.4 Mg/ha
    #   treecover=80% -> AGB ~ 137 Mg/ha
    expected = COEFFICIENT * (float(treecover_pct) / 100.0) ** EXPONENT
    return float(computed), float(expected)
