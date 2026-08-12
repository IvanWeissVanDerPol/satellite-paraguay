"""Tests for src/papers/p0011_yvytu_deforestation/pipeline.py.

Coverage target: 60%+. The YvytuPipeline class is the main entry point.
We test it with heavy mocking to avoid loading real models.
"""

from pathlib import Path
from unittest.mock import patch

import numpy as np
import pytest


class TestYvytuPipeline:
    """Tests for the YvytuPipeline class."""

    @pytest.fixture
    def pipeline(self):
        """Create a pipeline without auto-loading models."""
        from src.papers.p0011_yvytu_deforestation.pipeline import YvytuPipeline

        return YvytuPipeline()

    # --- __init__ ---

    def test_init_with_default_config(self, pipeline):
        assert pipeline.config is not None
        assert "tile_size_km" in pipeline.config
        assert "start_date" in pipeline.config
        assert "end_date" in pipeline.config
        assert "chaco_bbox" in pipeline.config

    def test_init_chaco_bbox(self, pipeline):
        bbox = pipeline.config["chaco_bbox"]
        assert "min_lon" in bbox
        assert "max_lon" in bbox
        assert "min_lat" in bbox
        assert "max_lat" in bbox

    def test_init_model_none(self, pipeline):
        assert pipeline.model is None

    def test_init_embeddings_empty(self, pipeline):
        assert pipeline.embeddings == {}

    def test_init_with_custom_config(self):
        from src.papers.p0011_yvytu_deforestation.pipeline import YvytuPipeline

        cfg = {"custom_key": "value"}
        p = YvytuPipeline(config=cfg)
        assert p.config["custom_key"] == "value"

    # --- select_tiles ---

    def test_select_tiles(self, pipeline):
        """select_tiles returns a list of tile IDs."""
        with patch(
            "src.paraguay_admin.list_tiles_in_region",
            return_value=["20S_055W", "20S_060W"],
        ):
            tiles = pipeline.select_tiles()
        assert isinstance(tiles, list)
        assert len(tiles) > 0

    def test_select_tiles_uses_chaco_bbox(self, pipeline):
        """select_tiles should use the chaco_bbox from config."""
        with patch(
            "src.paraguay_admin.list_tiles_in_region",
            return_value=["tile1"],
        ) as mock_fn:
            pipeline.select_tiles()
        # Check the bbox passed matches config
        call_args = mock_fn.call_args
        bbox_arg = call_args[0][0] if call_args[0] else call_args[1].get("bbox")
        assert bbox_arg == pipeline.config["chaco_bbox"]

    # --- download_data ---

    def test_download_data(self, pipeline):
        """download_data calls download_via_gee with correct params."""
        with patch(
            "src.papers.p0011_yvytu_deforestation.pipeline.download_via_gee",
            return_value=Path("/tmp/test.tif"),
        ) as mock_dl:
            with patch(
                "src.papers.p0011_yvytu_deforestation.pipeline.get_tile_bbox",
                return_value={"min_lon": -60, "max_lon": -55, "min_lat": -25, "max_lat": -20},
            ):
                result = pipeline.download_data("test_tile")
        assert result == Path("/tmp/test.tif")
        mock_dl.assert_called_once()

    # --- compute_tile_embeddings ---

    def test_compute_tile_embeddings(self, pipeline):
        """compute_tile_embeddings returns array."""
        fake_embeddings = np.zeros((10, 768))
        with patch(
            "src.papers.p0011_yvytu_deforestation.pipeline.compute_tile_embeddings",
            return_value=fake_embeddings,
        ):
            with patch(
                "src.papers.p0011_yvytu_deforestation.pipeline.get_tile_bbox",
                return_value={"min_lon": -60, "max_lon": -55, "min_lat": -25, "max_lat": -20},
            ):
                result = pipeline.compute_tile_embeddings("test_tile")
        assert result.shape == (10, 768)

    # --- detect_deforestation ---

    def test_detect_deforestation_basic(self, pipeline):
        """Test detect_deforestation returns a binary mask."""
        # Synthetic NDVI timeseries: 5 timesteps, 2x2 pixels
        ndvi = np.array(
            [
                [[0.9, 0.5], [0.5, 0.5]],
                [[0.7, 0.5], [0.5, 0.5]],
                [[0.5, 0.5], [0.5, 0.5]],
                [[0.3, 0.5], [0.5, 0.5]],
                [[0.1, 0.5], [0.5, 0.5]],
            ],
            dtype=np.float32,
        )
        dates = ["2020-01-01", "2020-06-01", "2020-12-01", "2021-06-01", "2021-12-01"]
        result = pipeline.detect_deforestation(
            tile_id="test_tile",
            ndvi_timeseries=ndvi,
            dates=dates,
        )
        assert result.shape == (2, 2)
        assert result.dtype == bool or result.dtype == np.uint8

    def test_detect_deforestation_detects_decline(self, pipeline):
        """Pixels with strong decline should be flagged as deforested."""
        ndvi = np.full((10, 4, 4), 0.8, dtype=np.float32)
        # Strong decline on pixel [0, 0]
        for t in range(10):
            ndvi[t, 0, 0] = 0.8 - t * 0.08
        dates = [f"2020-{m:02d}-01" for m in range(1, 11)]
        result = pipeline.detect_deforestation(
            tile_id="test",
            ndvi_timeseries=ndvi,
            dates=dates,
        )
        # Pixel [0, 0] should be detected as deforested
        assert result[0, 0] in (True, 1)

    def test_detect_deforestation_stable_pixels(self, pipeline):
        """Stable pixels should NOT be flagged."""
        ndvi = np.full((10, 4, 4), 0.7, dtype=np.float32)
        dates = [f"2020-{m:02d}-01" for m in range(1, 11)]
        result = pipeline.detect_deforestation(
            tile_id="test",
            ndvi_timeseries=ndvi,
            dates=dates,
        )
        # No change anywhere — should have very few/no detections
        assert result.sum() <= 2
