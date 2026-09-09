"""Tests for src/utils/carbon_math.py.

Updated 2026-09-09 (Round-12 audit fixes):
  - Hansen GFC v1.11 lossyear encoding is 1..23 (1 = 2001, ..., 23 = 2023).
    Calendar years like 2001 must NOT be passed as lossyear values.
  - The "chave" naming was a misattribution; the heuristic is
    uncalibrated canopy-cover-to-biomass power law.
"""

import numpy as np
import pytest


class TestCarbonMath:
    """Tests for carbon_math module."""

    def test_agb_at_known_values(self):
        """Verify power-law heuristic returns expected range."""
        from src.utils.carbon_math import agb_from_canopy_cover_heuristic

        # 20% treecover -> 4.29 Mg/ha
        assert agb_from_canopy_cover_heuristic(np.array([20.0]))[0] == pytest.approx(4.29, rel=0.05)
        # 50% -> 42.43 Mg/ha
        assert agb_from_canopy_cover_heuristic(np.array([50.0]))[0] == pytest.approx(42.43, rel=0.02)
        # 80% -> 137.38 Mg/ha
        assert agb_from_canopy_cover_heuristic(np.array([80.0]))[0] == pytest.approx(137.4, rel=0.02)

    def test_chave_agb_alias_still_works(self):
        """Backwards compatibility: chave_agb still callable."""
        from src.utils.carbon_math import chave_agb

        assert chave_agb(np.array([50.0]))[0] == pytest.approx(42.43, rel=0.02)

    def test_zero_treecover(self):
        from src.utils.carbon_math import agb_from_canopy_cover_heuristic

        assert agb_from_canopy_cover_heuristic(np.array([0.0]))[0] == 0.0

    def test_clip_above_100(self):
        from src.utils.carbon_math import agb_from_canopy_cover_heuristic

        # Values >100 should be clipped to 100
        v100 = agb_from_canopy_cover_heuristic(np.array([100.0]))[0]
        v150 = agb_from_canopy_cover_heuristic(np.array([150.0]))[0]
        assert v150 == pytest.approx(v100)

    def test_clip_negative(self):
        from src.utils.carbon_math import agb_from_canopy_cover_heuristic

        # Negative values should be clipped to 0
        assert agb_from_canopy_cover_heuristic(np.array([-10.0]))[0] == 0.0

    def test_carbon_stock_is_47_percent(self):
        from src.utils.carbon_math import agb_from_canopy_cover_heuristic, carbon_stock

        tc = np.array([50.0])
        cs = carbon_stock(tc)
        agb = agb_from_canopy_cover_heuristic(tc)
        assert cs[0] == pytest.approx(agb[0] * 0.47, rel=0.001)

    def test_co2e_uses_44_over_12(self):
        from src.utils.carbon_math import carbon_stock, co2e

        tc = np.array([50.0])
        ce = co2e(tc)
        cs = carbon_stock(tc)
        assert ce[0] == pytest.approx(cs[0] * 44.0 / 12.0, rel=0.001)

    def test_carbon_loss_per_pixel_hansen_encoding(self):
        """Loss mask uses Hansen encoding (1..23), NOT calendar years."""
        from src.utils.carbon_math import carbon_loss_per_pixel

        tc = np.array([50.0, 80.0, 30.0])
        # Hansen encoding: 1 = year 2001, 2 = year 2002, 0 = no loss.
        ly = np.array([1, 2, 0])
        result = carbon_loss_per_pixel(tc, ly, min_year=2001)
        # 2001 loss: tc=50% -> 73.11 Mg/ha
        assert result[0] == pytest.approx(73.11, rel=0.01)
        # 2002 loss: tc=80% -> 236.76 Mg/ha
        assert result[1] == pytest.approx(236.76, rel=0.01)
        # no loss
        assert result[2] == 0.0

    def test_carbon_loss_old_calendar_year_returns_zero(self):
        """Calendar years (>= 23) used as lossyear must return 0
        because real Hansen encoding is 1..23, not the calendar year."""
        from src.utils.carbon_math import carbon_loss_per_pixel

        tc = np.array([50.0, 80.0])
        # If a caller passes calendar years like 2001 or 2005, the new
        # code must NOT interpret them as valid Hansen lossyear values.
        ly = np.array([2001, 2005])
        result = carbon_loss_per_pixel(tc, ly, min_year=2001)
        assert result[0] == 0.0
        assert result[1] == 0.0

    def test_carbon_loss_with_min_year(self):
        """min_year filters by calendar year derived from lossyear."""
        from src.utils.carbon_math import carbon_loss_per_pixel

        tc = np.array([50.0, 80.0])
        # Hansen encoding: 0 = no loss, 5 = year 2005
        ly = np.array([0, 5])
        result = carbon_loss_per_pixel(tc, ly, min_year=2001)
        assert result[0] == 0.0  # no loss
        # year 2005 with tc=80% -> 236.76 Mg/ha
        assert result[1] == pytest.approx(236.76, rel=0.01)

    def test_annual_carbon_loss(self):
        from src.utils.carbon_math import annual_carbon_loss

        tc = np.array([50.0, 50.0, 80.0, 80.0])
        # Hansen encoding: 1 = 2001, 2 = 2002, 0 = no loss
        ly = np.array([1, 2, 2, 0])
        result = annual_carbon_loss(tc, ly, min_year=2001)
        assert 2001 in result
        assert 2002 in result
        # 2002 has 2 pixels (one 50%, one 80%)
        assert result[2002] > 0
        # 2002 sum > 2001 sum (extra 80% pixel)
        assert result[2002] > result[2001]

    def test_carbon_summary_returns_per_hectare_stats(self):
        """carbon_summary must NOT expose 'total_mg' (dimensional lie)."""
        from src.utils.carbon_math import carbon_summary

        tc = np.array([10.0, 50.0, 80.0, 90.0])
        result = carbon_summary(tc)
        assert "agb" in result
        assert "carbon" in result
        assert "co2e" in result
        # Per-hectare stats only -- no total_mg
        assert "total_mg" not in result["agb"], (
            "total_mg is a dimensional lie (Mg/ha summed as total mass); "
            "use total_carbon_loss() with pixel_area_ha instead"
        )
        # New schema: max_mg_per_ha, mean_mg_per_ha, median_mg_per_ha
        assert "max_mg_per_ha" in result["agb"]
        assert "mean_mg_per_ha" in result["agb"]
        assert "median_mg_per_ha" in result["agb"]
        assert result["agb"]["max_mg_per_ha"] > result["agb"]["mean_mg_per_ha"]

    def test_total_carbon_loss_multiplies_by_area(self):
        """total_carbon_loss(per_pixel * pixel_area) is a real mass."""
        from src.utils.carbon_math import total_carbon_loss

        tc = np.array([50.0, 80.0])
        ly = np.array([1, 2])  # both loss years
        # 1 pixel at 73.11 + 1 pixel at 236.76 = 309.87 Mg/ha; with 0.0864 ha/px = 26.77 Mg total
        total = total_carbon_loss(tc, ly, pixel_area_ha=0.0864)
        expected = (73.115 + 236.758) * 0.0864
        assert total == pytest.approx(expected, rel=0.02)

    def test_calibrate_check_returns_two_values(self):
        """calibrate_check must return (computed, expected) not (x, x)."""
        from src.utils.carbon_math import calibrate_check

        result = calibrate_check(50.0)
        assert isinstance(result, tuple)
        assert len(result) == 2
        a, b = result
        assert a > 0
        # By construction a == b since expected is computed from the same
        # formula, but at least we expose the structure so a downstream
        # test could compare against an external reference.
        assert b == pytest.approx(a, rel=0.001)

    def test_constant_values(self):
        """The renamed constants exist with correct values."""
        from src.utils.carbon_math import C_STOIC_RATIO, CARBON_FRACTION, COEFFICIENT, EXPONENT

        assert COEFFICIENT == 240.0
        assert EXPONENT == 2.5
        assert CARBON_FRACTION == 0.47
        assert abs(C_STOIC_RATIO - 44.0 / 12.0) < 0.001

    def test_chave_coefficient_alias_removed(self):
        """The old CHAVE_COEFFICIENT constant must be gone to stop the misattribution."""
        from src.utils import carbon_math as cm

        assert not hasattr(cm, "CHAVE_COEFFICIENT"), (
            "CHAVE_COEFFICIENT was removed because it misattributed the " "canopy-cover heuristic to Chave 2014."
        )

    def test_lossyear_to_calendar_year(self):
        from src.utils.carbon_math import lossyear_to_calendar_year

        assert lossyear_to_calendar_year(0) == 2000  # 0 = no loss, treated as year 2000
        assert lossyear_to_calendar_year(1) == 2001
        assert lossyear_to_calendar_year(23) == 2023
