"""Tests for src/utils/carbon_math.py."""
import numpy as np
import pytest


class TestCarbonMath:
    """Tests for carbon_math module."""

    def test_chave_agb_at_known_values(self):
        """Verify Chave model returns expected range."""
        from src.utils.carbon_math import chave_agb
        # 20% treecover → ~4.3 Mg/ha
        assert chave_agb(np.array([20.0]))[0] == pytest.approx(4.3, rel=0.1)
        # 50% → ~42.4 Mg/ha
        assert chave_agb(np.array([50.0]))[0] == pytest.approx(42.4, rel=0.05)
        # 80% → ~137 Mg/ha
        assert chave_agb(np.array([80.0]))[0] == pytest.approx(137.0, rel=0.05)

    def test_chave_agb_zero(self):
        from src.utils.carbon_math import chave_agb
        assert chave_agb(np.array([0.0]))[0] == 0.0

    def test_chave_agb_clip_above_100(self):
        from src.utils.carbon_math import chave_agb
        # Values >100 should be clipped to 100
        assert chave_agb(np.array([150.0]))[0] == pytest.approx(chave_agb(np.array([100.0]))[0])

    def test_chave_agb_clip_negative(self):
        from src.utils.carbon_math import chave_agb
        # Negative values should be clipped to 0
        assert chave_agb(np.array([-10.0]))[0] == 0.0

    def test_carbon_stock_is_47_percent(self):
        from src.utils.carbon_math import carbon_stock, chave_agb
        tc = np.array([50.0])
        cs = carbon_stock(tc)
        agb = chave_agb(tc)
        assert cs[0] == pytest.approx(agb[0] * 0.47, rel=0.001)

    def test_co2e_uses_44_over_12(self):
        from src.utils.carbon_math import co2e, carbon_stock
        tc = np.array([50.0])
        ce = co2e(tc)
        cs = carbon_stock(tc)
        assert ce[0] == pytest.approx(cs[0] * 44.0 / 12.0, rel=0.001)

    def test_carbon_loss_per_pixel(self):
        from src.utils.carbon_math import carbon_loss_per_pixel
        tc = np.array([50.0, 80.0, 30.0])
        ly = np.array([2001, 2002, 0])  # 0 means no loss
        result = carbon_loss_per_pixel(tc, ly, min_year=2001)
        # All 3 with lossyear>0 are loss pixels
        assert result[0] > 0  # 2001 loss year
        assert result[1] > 0  # 2002 loss year
        assert result[2] == 0.0  # no loss year

    def test_carbon_loss_with_min_year(self):
        from src.utils.carbon_math import carbon_loss_per_pixel
        tc = np.array([50.0, 80.0])
        ly = np.array([2000, 2005])
        # min_year=2001 means 2000 not counted
        result = carbon_loss_per_pixel(tc, ly, min_year=2001)
        assert result[0] == 0.0  # 2000 < 2001
        assert result[1] > 0.0  # 2005 >= 2001

    def test_annual_carbon_loss(self):
        from src.utils.carbon_math import annual_carbon_loss
        tc = np.array([50.0, 50.0, 80.0, 80.0])
        ly = np.array([2001, 2002, 2002, 0])
        result = annual_carbon_loss(tc, ly, min_year=2001)
        assert 2001 in result
        assert 2002 in result
        # 2002 has 2 pixels
        assert result[2002] > 0
        assert result[2002] > result[2001]

    def test_carbon_summary(self):
        from src.utils.carbon_math import carbon_summary
        tc = np.array([10.0, 50.0, 80.0, 90.0])
        result = carbon_summary(tc)
        assert "agb" in result
        assert "carbon" in result
        assert "co2e" in result
        assert result["agb"]["max"] > result["agb"]["mean"]

    def test_calibrate_check(self):
        from src.utils.carbon_math import calibrate_check
        a, b = calibrate_check(50.0)
        assert a == b
        assert a > 0

    def test_chave_constants(self):
        from src.utils.carbon_math import CHAVE_COEFFICIENT, CARBON_FRACTION, C_STOIC_RATIO
        assert CHAVE_COEFFICIENT == 240.0
        assert CARBON_FRACTION == 0.47
        assert abs(C_STOIC_RATIO - 44.0 / 12.0) < 0.001