"""Tests for src/baselines/p0035_tatakua_baselines.py — air quality
forecasting baselines.
"""

import numpy as np
import pytest


class TestP0035Baselines:
    """Tests for src/baselines/p0035_tatakua_baselines.py."""

    @pytest.fixture
    def module(self):
        from src.baselines import p0035_tatakua_baselines

        return p0035_tatakua_baselines

    @pytest.fixture
    def historical(self):
        """30 days of PM2.5 data."""
        rng = np.random.default_rng(42)
        return rng.uniform(5, 30, 30).astype(np.float32)

    # --- mean_forecast_baseline ---

    def test_mean_forecast_returns_correct_shape(self, module, historical):
        forecast = module.mean_forecast_baseline(historical, horizon=7)
        assert forecast.shape == (7,)

    def test_mean_forecast_constant(self, module, historical):
        """All forecast values should be the mean of historical."""
        forecast = module.mean_forecast_baseline(historical, horizon=7)
        expected = np.mean(historical)
        np.testing.assert_allclose(forecast, expected)

    def test_mean_forecast_value_correct(self, module):
        """Test forecast equals mean of input."""
        data = np.array([10.0, 20.0, 30.0])
        forecast = module.mean_forecast_baseline(data, horizon=5)
        assert forecast[0] == 20.0  # mean of 10,20,30

    # --- persistence_forecast_baseline ---

    def test_persistence_forecast_returns_correct_shape(self, module, historical):
        forecast = module.persistence_forecast_baseline(historical, horizon=7)
        assert forecast.shape == (7,)

    def test_persistence_forecast_uses_last_value(self, module, historical):
        forecast = module.persistence_forecast_baseline(historical, horizon=7)
        assert forecast[0] == historical[-1]
        assert forecast[-1] == historical[-1]

    def test_persistence_forecast_constant(self, module, historical):
        forecast = module.persistence_forecast_baseline(historical, horizon=10)
        assert np.all(forecast == historical[-1])

    # --- linear_forecast_baseline ---

    def test_linear_forecast_returns_correct_shape(self, module, historical):
        forecast = module.linear_forecast_baseline(historical, horizon=7)
        assert forecast.shape == (7,)

    def test_linear_forecast_handles_constant_input(self, module):
        """Constant input should give constant forecast."""
        data = np.array([15.0] * 10)
        forecast = module.linear_forecast_baseline(data, horizon=5)
        np.testing.assert_allclose(forecast, 15.0, atol=1e-6)

    def test_linear_forecast_handles_strictly_increasing(self, module):
        """Strictly increasing input should extrapolate increasing."""
        data = np.arange(10, dtype=float)
        forecast = module.linear_forecast_baseline(data, horizon=3)
        # future_x = [10, 11, 12], slope ~1, intercept ~0
        assert forecast[1] > forecast[0]
        assert forecast[2] > forecast[1]
        assert 10.5 < forecast[1] < 11.5

    # --- run_all_baselines ---

    def test_run_all_baselines_returns_dict(self, module, historical):
        results = module.run_all_baselines(historical, horizon=7)
        assert isinstance(results, dict)
        assert "mean" in results
        assert "persistence" in results
        assert "linear_trend" in results

    def test_run_all_baselines_has_forecast_and_mean(self, module, historical):
        results = module.run_all_baselines(historical, horizon=7)
        for name, data in results.items():
            assert "forecast" in data
            assert "mean" in data
            assert len(data["forecast"]) == 7

    def test_run_all_baselines_default_horizon(self, module, historical):
        """Default horizon should be 7 days."""
        results = module.run_all_baselines(historical)
        for name, data in results.items():
            assert len(data["forecast"]) == 7
