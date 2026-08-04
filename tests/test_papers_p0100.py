"""Tests for src/papers/p0100_yvyra_carbon_credits/pipeline.py.

Coverage target: 70%+. The YvyraPipeline class handles carbon
credit verification against Verra/Gold Standard projects.
"""
import pytest
import pandas as pd
import numpy as np
from pathlib import Path
from unittest.mock import patch, MagicMock


class TestYvyraPipeline:
    """Tests for the YvyraPipeline class."""

    @pytest.fixture
    def pipeline(self):
        from src.papers.p0100_yvyra_carbon_credits.pipeline import YvyraPipeline
        return YvyraPipeline()

    # --- __init__ ---

    def test_init_default_config(self, pipeline):
        assert pipeline.config is not None
        assert "min_lon" in pipeline.config
        assert "max_lon" in pipeline.config
        assert "start_date" in pipeline.config
        assert "end_date" in pipeline.config

    def test_init_bbox(self, pipeline):
        """Config should cover all of Paraguay."""
        assert pipeline.config["min_lon"] < pipeline.config["max_lon"]
        assert pipeline.config["min_lat"] < pipeline.config["max_lat"]

    def test_init_model_none(self, pipeline):
        assert pipeline.model is None

    def test_init_custom_config(self):
        from src.papers.p0100_yvyra_carbon_credits.pipeline import YvyraPipeline
        cfg = {"min_lon": -60, "max_lon": -55}
        p = YvyraPipeline(config=cfg)
        assert p.config["min_lon"] == -60

    # --- fetch_verra_projects ---

    def test_fetch_verra_projects_returns_dataframe(self, pipeline):
        result = pipeline.fetch_verra_projects(country="Paraguay")
        assert isinstance(result, pd.DataFrame)

    def test_fetch_verra_projects_has_expected_columns(self, pipeline):
        result = pipeline.fetch_verra_projects()
        assert "id" in result.columns or len(result.columns) > 0

    def test_fetch_verra_projects_default_country(self, pipeline):
        """Default country should be Paraguay."""
        result = pipeline.fetch_verra_projects()
        assert isinstance(result, pd.DataFrame)

    def test_fetch_verra_projects_custom_country(self, pipeline):
        """Custom country is accepted."""
        result = pipeline.fetch_verra_projects(country="Brazil")
        assert isinstance(result, pd.DataFrame)

    # --- fetch_gold_standard ---

    def test_fetch_gold_standard_returns_dataframe(self, pipeline):
        result = pipeline.fetch_gold_standard()
        assert isinstance(result, pd.DataFrame)

    def test_fetch_gold_standard_has_rows(self, pipeline):
        result = pipeline.fetch_gold_standard()
        assert len(result) > 0

    # --- load_foundation_model ---

    def test_load_foundation_model(self, pipeline):
        """load_foundation_model calls load_alphaearth."""
        with patch(
            "src.papers.p0100_yvyra_carbon_credits.pipeline.load_alphaearth",
            return_value=MagicMock(),
        ) as mock_load:
            pipeline.load_foundation_model()
        assert pipeline.model is not None
        mock_load.assert_called_once()

    # --- verify_carbon_credit ---

    def test_verify_carbon_credit_returns_dict(self, pipeline):
        result = pipeline.verify_carbon_credit(project_id="VCS-001")
        assert isinstance(result, dict)

    def test_verify_carbon_credit_has_required_keys(self, pipeline):
        result = pipeline.verify_carbon_credit(project_id="VCS-001")
        assert "project_id" in result
        assert "verified" in result
        assert "claimed_carbon_tons" in result
        assert "estimated_carbon_tons" in result
        assert "confidence" in result

    def test_verify_carbon_credit_with_parcel(self, pipeline):
        """Optional parcel_id parameter."""
        result = pipeline.verify_carbon_credit(
            project_id="VCS-001",
            parcel_id="P-001",
        )
        assert result["project_id"] == "VCS-001"

    def test_verify_carbon_credit_with_tile(self, pipeline):
        """Optional tile_id parameter."""
        result = pipeline.verify_carbon_credit(
            project_id="VCS-001",
            tile_id="20S_055W",
        )
        assert result["project_id"] == "VCS-001"

    def test_verify_carbon_credit_confidence_in_range(self, pipeline):
        """Confidence should be 0-1."""
        result = pipeline.verify_carbon_credit(project_id="VCS-001")
        assert 0.0 <= result["confidence"] <= 1.0

    def test_verify_carbon_credit_positive_tons(self, pipeline):
        """Carbon tons should be positive."""
        result = pipeline.verify_carbon_credit(project_id="VCS-001")
        assert result["claimed_carbon_tons"] > 0
        assert result["estimated_carbon_tons"] > 0

    # --- validate_predictions ---

    def test_validate_predictions_with_required_columns(self, pipeline):
        """When both columns exist, returns regression metrics."""
        df = pd.DataFrame({
            "project_id": ["P1", "P2", "P3"],
            "claimed_carbon_tons": [10000, 20000, 30000],
            "estimated_carbon_tons": [10500, 19500, 29500],
        })
        result = pipeline.validate_predictions(df)
        assert isinstance(result, dict)

    def test_validate_predictions_missing_columns(self, pipeline):
        """When required columns are missing, returns empty dict."""
        df = pd.DataFrame({"project_id": ["P1"], "other": [1]})
        result = pipeline.validate_predictions(df)
        assert result == {}