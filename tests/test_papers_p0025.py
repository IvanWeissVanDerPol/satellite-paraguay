"""Tests for src/papers/p0025_yrupe_yield/pipeline.py.

Coverage target: 70%+. The YrupePipeline class handles soybean
yield prediction.
"""
import json
import pytest
import numpy as np
from pathlib import Path
from unittest.mock import patch, MagicMock


class TestYrupePipeline:
    """Tests for the YrupePipeline class."""

    @pytest.fixture
    def pipeline(self):
        from src.papers.p0025_yrupe_yield.pipeline import YrupePipeline
        return YrupePipeline()

    # --- __init__ ---

    def test_init_default_config(self, pipeline):
        assert pipeline.config is not None
        assert "caaguazu_bbox" in pipeline.config
        assert "inbio_data_path" in pipeline.config

    def test_init_caaguazu_bbox(self, pipeline):
        bbox = pipeline.config["caaguazu_bbox"]
        assert "min_lon" in bbox
        assert bbox["min_lon"] < bbox["max_lon"]

    def test_init_custom_config(self):
        from src.papers.p0025_yrupe_yield.pipeline import YrupePipeline
        cfg = {"caaguazu_bbox": {"custom": True}}
        p = YrupePipeline(config=cfg)
        assert "custom" in p.config["caaguazu_bbox"]

    # --- load_inbio_data ---

    def test_load_inbio_data_missing_file(self, pipeline, tmp_path):
        """When INBIO file doesn't exist, return default zero dict."""
        # Use a non-existent path
        pipeline.config["inbio_data_path"] = str(tmp_path / "nonexistent.json")
        result = pipeline.load_inbio_data()
        assert result == {"soy_hectares": 0}

    def test_load_inbio_data_existing_file(self, pipeline, tmp_path):
        """When INBIO file exists, load and return JSON content."""
        test_data = {"soy_hectares": 3500000, "year": 2025}
        f = tmp_path / "inbio.json"
        with open(f, "w") as fp:
            json.dump(test_data, fp)
        pipeline.config["inbio_data_path"] = str(f)

        result = pipeline.load_inbio_data()
        assert result["soy_hectares"] == 3500000
        assert result["year"] == 2025

    # --- delineate_fields ---

    def test_delineate_fields(self, pipeline):
        """delineate_fields should return a dict with fields key."""
        result = pipeline.delineate_fields(Path("/tmp/test.tif"))
        assert isinstance(result, dict)
        assert "fields" in result

    # --- predict_yield ---

    def test_predict_yield_returns_float(self, pipeline):
        ndvi = np.random.rand(10, 256, 256).astype(np.float32) * 0.5 + 0.3
        result = pipeline.predict_yield("test_tile", ndvi)
        assert isinstance(result, float)

    def test_predict_yield_empty_array(self, pipeline):
        """Empty NDVI should return 0.0."""
        result = pipeline.predict_yield("test_tile", np.array([]))
        assert result == 0.0

    def test_predict_yield_positive_for_realistic_ndvi(self, pipeline):
        """NDVI ~0.5 should yield positive tons/hectare."""
        ndvi = np.full((10, 256, 256), 0.5, dtype=np.float32)
        result = pipeline.predict_yield("test_tile", ndvi)
        # Heuristic: 1.5 + 0.5 * 2.0 = 2.5
        assert 1.0 < result < 4.0

    def test_predict_yield_higher_for_higher_ndvi(self, pipeline):
        """Higher NDVI should yield higher prediction."""
        low = np.full((10, 256, 256), 0.2, dtype=np.float32)
        high = np.full((10, 256, 256), 0.8, dtype=np.float32)
        low_result = pipeline.predict_yield("t1", low)
        high_result = pipeline.predict_yield("t2", high)
        assert high_result > low_result

    def test_predict_yield_with_weather(self, pipeline):
        """Weather data should not break the prediction."""
        ndvi = np.full((10, 256, 256), 0.5, dtype=np.float32)
        weather = {"temperature": 25.0, "rainfall_mm": 100.0}
        result = pipeline.predict_yield("test_tile", ndvi, weather_data=weather)
        assert isinstance(result, float)

    # --- validate ---

    def test_validate_returns_dict(self, pipeline):
        predictions = np.array([2.5, 3.0, 2.8])
        ground_truth = np.array([2.6, 2.9, 3.0])
        result = pipeline.validate(predictions, ground_truth)
        assert isinstance(result, dict)