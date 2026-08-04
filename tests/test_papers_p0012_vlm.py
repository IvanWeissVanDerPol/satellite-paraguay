"""Tests for src/papers/p0012_yvy_indigenous/pipeline.py VLM paths.

Coverage target: 90%+. Tests VLM validation with LLaVA fallback and GPT-4V.
"""
import sys
import pytest
import numpy as np
from pathlib import Path
from unittest.mock import patch, MagicMock


@pytest.fixture
def pipeline():
    from src.papers.p0012_yvy_indigenous.pipeline import YvyPipeline
    return YvyPipeline()


class TestValidateIndigenousVLM:
    """Tests for validate_with_vlm function."""

    def test_llava_default(self, pipeline):
        """When use_paid_api=False (default), uses LLaVA fallback."""
        from shapely.geometry import box
        path = Path("dummy.tif")
        geometry = box(0, 0, 1, 1)
        result = pipeline.validate_with_vlm(path, geometry, "P001")
        assert result["api"] == "llava-1.6"
        assert result["cost"] == "$0"
        assert result["parcel_id"] == "P001"

    def test_gpt4v_opt_in(self, pipeline):
        """When use_paid_api=True, attempts GPT-4V with mocked openai."""
        pipeline.config["use_paid_api"] = True
        mock_openai = MagicMock()
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "yes, this is indigenous territory"
        mock_openai.ChatCompletion.create.return_value = mock_response

        with patch.dict(sys.modules, {"openai": mock_openai}):
            from shapely.geometry import box
            path = Path("dummy.tif")
            result = pipeline.validate_with_vlm(path, box(0, 0, 1, 1), "P002")
        assert result["api"] == "gpt-4v"
        assert result["is_indigenous"] is True
        assert result["cost"] == "$0.03"

    def test_gpt4v_import_error_falls_to_llava(self, pipeline):
        """When openai not installed with paid API, falls back to LLaVA."""
        pipeline.config["use_paid_api"] = True
        # Block openai import
        saved = sys.modules.get("openai")
        sys.modules["openai"] = None
        try:
            from shapely.geometry import box
            result = pipeline.validate_with_vlm(Path("dummy.tif"), box(0, 0, 1, 1), "P003")
            assert result["api"] == "llava-1.6"
        finally:
            if saved is None:
                sys.modules.pop("openai", None)
            else:
                sys.modules["openai"] = saved


class TestRunDemo:
    """Tests for run_yvy_demo function."""

    def test_runs_demo_full(self, monkeypatch):
        """Demo runs end-to-end with mocked data."""
        from src.papers.p0012_yvy_indigenous.pipeline import run_yvy_demo

        mock_pipeline = MagicMock()
        mock_pipeline.load_data.return_value = None
        mock_pipeline.detect_conflicts.return_value = {
            "total_parcels": 7500,
            "indigenous_territories": 17,
            "conflict_parcels": 5,
        }

        with patch("src.papers.p0012_yvy_indigenous.pipeline.YvyPipeline", return_value=mock_pipeline):
            run_yvy_demo()
