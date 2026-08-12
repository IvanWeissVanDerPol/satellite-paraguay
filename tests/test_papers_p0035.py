"""Tests for src/papers/p0035_tatakua_air_quality/pipeline.py.

Coverage target: 70%+. The TatakuaPipeline class handles air quality
forecasting for Asunción.
"""


import numpy as np
import pytest


class TestTatakuaPipeline:
    """Tests for the TatakuaPipeline class."""

    @pytest.fixture
    def pipeline(self):
        from src.papers.p0035_tatakua_air_quality.pipeline import TatakuaPipeline

        return TatakuaPipeline()

    @pytest.fixture
    def s5p_npz(self, tmp_path):
        """Create a synthetic Sentinel-5P .npz file with NO2/SO2/CO arrays."""
        days = 365
        np.savez(
            tmp_path / "s5p_paraguay.npz",
            no2=np.linspace(1e15, 5e15, days),
            so2=np.linspace(1e15, 3e15, days),
            co=np.linspace(1e18, 5e18, days),
            o3=np.linspace(1e18, 4e18, days),
            ch4=np.linspace(1e3, 2e3, days),
            aer_ai=np.linspace(-1.0, 1.0, days),
            timestamps=np.arange(0, days, dtype="datetime64[D]"),
        )
        return tmp_path / "s5p_paraguay.npz"

    # --- __init__ ---

    def test_init_default_config(self, pipeline):
        assert pipeline.config is not None
        assert "asuncion_bbox" in pipeline.config
        assert "pollutants" in pipeline.config
        assert "forecast_horizon_days" in pipeline.config

    def test_init_asuncion_bbox(self, pipeline):
        bbox = pipeline.config["asuncion_bbox"]
        assert bbox["min_lon"] < bbox["max_lon"]
        assert bbox["min_lat"] < bbox["max_lat"]

    def test_init_pollutants_list(self, pipeline):
        pollutants = pipeline.config["pollutants"]
        assert isinstance(pollutants, list)
        assert "pm25" in pollutants
        assert "pm10" in pollutants
        assert "no2" in pollutants

    def test_init_forecast_horizon(self, pipeline):
        assert pipeline.config["forecast_horizon_days"] > 0

    def test_init_custom_config(self):
        from src.papers.p0035_tatakua_air_quality.pipeline import TatakuaPipeline

        cfg = {"forecast_horizon_days": 14}
        p = TatakuaPipeline(config=cfg)
        assert p.config["forecast_horizon_days"] == 14

    # --- fetch_openaq_data ---

    def test_fetch_openaq_data_returns_list(self, pipeline):
        """fetch_openaq_data should return a list (possibly empty on error)."""
        result = pipeline.fetch_openaq_data(city="Asunción", days=30)
        assert isinstance(result, list)

    def test_fetch_openaq_data_default_params(self, pipeline):
        """Default city is Asunción, days is 365."""
        result = pipeline.fetch_openaq_data()
        assert isinstance(result, list)

    # --- fetch_sentinel5p ---

    def test_fetch_sentinel5p_returns_dict(self, pipeline, s5p_npz):
        result = pipeline.fetch_sentinel5p(days=30, data_path=s5p_npz)
        assert isinstance(result, dict)

    def test_fetch_sentinel5p_default_days(self, pipeline, s5p_npz):
        result = pipeline.fetch_sentinel5p(data_path=s5p_npz)
        assert isinstance(result, dict)
        # Should have NO2, SO2, CO keys
        assert "no2" in result
        assert "so2" in result
        assert "co" in result

    def test_fetch_sentinel5p_array_shapes(self, pipeline, s5p_npz):
        """The returned arrays should match `days`."""
        result = pipeline.fetch_sentinel5p(days=50, data_path=s5p_npz)
        assert result["no2"].shape == (50,)
        assert result["so2"].shape == (50,)
        assert result["co"].shape == (50,)

    # --- forecast_pm25 ---

    def test_forecast_pm25_returns_array(self, pipeline):
        """forecast_pm25 returns numpy array."""
        historical = np.array([10.0, 12.0, 15.0, 14.0, 13.0])
        result = pipeline.forecast_pm25(historical)
        assert isinstance(result, np.ndarray)

    def test_forecast_pm25_correct_horizon(self, pipeline):
        """Forecast should be horizon_days long."""
        historical = np.array([10.0, 12.0, 15.0, 14.0, 13.0])
        result = pipeline.forecast_pm25(historical)
        assert len(result) == pipeline.config["forecast_horizon_days"]

    def test_forecast_pm25_empty_input(self, pipeline):
        """Empty input should return empty array."""
        result = pipeline.forecast_pm25(np.array([]))
        assert isinstance(result, np.ndarray)
        assert len(result) == 0

    def test_forecast_pm25_with_atmospheric(self, pipeline):
        """Atmospheric data should be accepted (not yet used in impl)."""
        historical = np.array([10.0, 12.0, 15.0, 14.0, 13.0])
        atmospheric = {"no2": np.array([1e-5] * 30)}
        result = pipeline.forecast_pm25(historical, atmospheric_data=atmospheric)
        assert isinstance(result, np.ndarray)
        assert len(result) == pipeline.config["forecast_horizon_days"]

    def test_forecast_pm25_close_to_last_value(self, pipeline):
        """Forecast should be close to the last historical value."""
        historical = np.full(10, 25.0)  # PM2.5 = 25
        result = pipeline.forecast_pm25(historical)
        # Mean should be in range (last ± 2 because of small noise)
        assert 23.0 < result.mean() < 27.0

    # --- validate ---

    def test_validate_returns_dict(self, pipeline):
        predictions = np.array([10.0, 12.0, 15.0])
        ground_truth = np.array([10.5, 11.5, 14.5])
        result = pipeline.validate(predictions, ground_truth)
        assert isinstance(result, dict)
