"""Tests for src/papers/p0012_yvy_indigenous/pipeline.py.

Coverage target: 60%+. The YvyPipeline class handles indigenous
territory mapping and conflict detection.
"""

import pytest  # noqa: E402

pytest.importorskip("rasterio", reason="CI: requires optional system dep 'rasterio' (not installed)")  # noqa: E402

from unittest.mock import MagicMock, patch  # noqa: E402

import pytest  # noqa: E402


class TestYvyPipeline:
    """Tests for the YvyPipeline class."""

    @pytest.fixture
    def pipeline(self):
        from src.papers.p0012_yvy_indigenous.pipeline import YvyPipeline

        return YvyPipeline()

    # --- __init__ ---

    def test_init_default_config(self, pipeline):
        assert pipeline.config is not None
        assert "vlm_model" in pipeline.config
        assert "use_paid_api" in pipeline.config
        assert "care_principles" in pipeline.config

    def test_init_care_principles_default_true(self, pipeline):
        assert pipeline.config["care_principles"] is True

    def test_init_custom_config(self):
        from src.papers.p0012_yvy_indigenous.pipeline import YvyPipeline

        cfg = {"vlm_model": "custom-model", "care_principles": False}
        p = YvyPipeline(config=cfg)
        assert p.config["vlm_model"] == "custom-model"
        assert p.config["care_principles"] is False

    # --- load_data ---

    def test_load_data(self, pipeline):
        """load_data returns indigenous territories and catastro."""
        mock_indigenous = MagicMock()
        mock_catastro = MagicMock()
        with patch(
            "src.papers.p0012_yvy_indigenous.pipeline.load_indigenous_territories",
            return_value=mock_indigenous,
        ):
            with patch(
                "src.papers.p0012_yvy_indigenous.pipeline.load_catastro_parcels",
                return_value=mock_catastro,
            ):
                indigenous, catastro = pipeline.load_data()
        assert indigenous == mock_indigenous
        assert catastro == mock_catastro

    # --- detect_conflicts ---

    def test_detect_conflicts_calls_load_if_needed(self, pipeline):
        """detect_conflicts should auto-load data if not present."""
        mock_indigenous = MagicMock()
        mock_catastro = MagicMock()
        mock_conflicts = MagicMock()
        mock_conflicts.geometry.tolist.return_value = []

        # Set up mock for intersects
        mock_catastro.intersects.return_value = [True, False, True]
        mock_catastro.__len__ = lambda self: 3

        # After filtering conflicts
        mock_catastro_filtered = MagicMock()
        mock_catastro_filtered.geometry.tolist.return_value = []
        # Patch __getitem__ to return filtered
        mock_catastro.__getitem__ = MagicMock(return_value=mock_conflicts)
        mock_conflicts.__len__ = lambda self: 2

        with patch(
            "src.papers.p0012_yvy_indigenous.pipeline.load_indigenous_territories",
            return_value=mock_indigenous,
        ):
            with patch(
                "src.papers.p0012_yvy_indigenous.pipeline.load_catastro_parcels",
                return_value=mock_catastro,
            ):
                result = pipeline.detect_conflicts()

        assert "total_parcels" in result
        assert "indigenous_territories" in result
        assert "conflict_parcels" in result
        assert "conflict_geometries" in result
