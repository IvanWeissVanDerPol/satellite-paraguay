"""Paper 1: P0011 Yvytu — Multi-temporal satellite CV for Chaco deforestation.

Target journal: Remote Sensing of Environment
Advisors: Juan Carlos Cristaldo (FADA)
Timeline: 12 weeks

Hypothesis: Pre-trained Prithvi + MapBiomas labels + BFAST change detection
outperforms Hansen GFC on Chaco deforestation (F1 > 0.85).
"""

from pathlib import Path
from typing import Dict, List, Optional

import numpy as np

from ...evaluation import (
    benchmark_against_hansen,
    benchmark_against_mapbiomas,
)
from ...foundation_models import compute_tile_embeddings, load_prithvi
from ...paraguay_admin import get_tile_bbox
from ...satellite_io import download_via_gee
from ...timeseries import (
    detect_changes_bfast,
)


class YvytuPipeline:
    """End-to-end pipeline for Chaco deforestation detection."""

    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {
            "tile_size_km": 10,
            "start_date": "2018-01-01",
            "end_date": "2025-12-31",
            "max_cloud_cover": 20,
            "chaco_bbox": {
                "min_lon": -62.0,
                "max_lon": -57.0,
                "min_lat": -24.0,
                "max_lat": -19.0,
            },
        }
        self.model = None
        self.embeddings = {}

    def load_model(self):
        """Load Prithvi foundation model."""
        self.model = load_prithvi("300m")
        return self.model

    def select_tiles(self) -> List[str]:
        """Select Chaco tiles for analysis."""
        from ...paraguay_admin import list_tiles_in_region

        return list_tiles_in_region(self.config["chaco_bbox"])

    def download_data(self, tile_id: str) -> Path:
        """Download Sentinel-2 for a Chaco tile."""
        bbox = get_tile_bbox(tile_id)
        return download_via_gee(
            tile_id=tile_id,
            bbox=bbox,
            satellite="sentinel2",
            start_date=self.config["start_date"],
            end_date=self.config["end_date"],
        )

    def compute_tile_embeddings(self, tile_id: str) -> np.ndarray:
        """Compute Prithvi embeddings for tile."""
        bbox = get_tile_bbox(tile_id)
        return compute_tile_embeddings(tile_id, bbox, model_name="prithvi")

    def detect_deforestation(
        self,
        tile_id: str,
        ndvi_timeseries: np.ndarray,
        dates: List[str],
    ) -> np.ndarray:
        """Detect deforestation in a tile using BFAST-like change detection.

        Args:
            tile_id: tile identifier
            ndvi_timeseries: (T, H, W) NDVI values over time
            dates: ISO date strings

        Returns:
            (H, W) deforestation mask (1 = deforested)
        """
        # Use change detection
        change_result = detect_changes_bfast(
            ndvi_timeseries,
            dates,
            h=0.25,
        )

        # Threshold on magnitude
        # NDVI drop > 0.2 = likely deforestation
        threshold = 0.2
        mask = (
            (change_result["magnitudes"] > threshold) & (change_result["before_mean"] > change_result["after_mean"])
        ).astype(np.uint8)

        return mask

    def validate(
        self,
        predictions: np.ndarray,
        mapbiomas_path: Optional[Path] = None,
        hansen_path: Optional[Path] = None,
    ) -> Dict:
        """Validate predictions against MapBiomas + Hansen."""
        results = {}
        if mapbiomas_path:
            results["mapbiomas"] = benchmark_against_mapbiomas(predictions, mapbiomas_path)
        if hansen_path:
            results["hansen"] = benchmark_against_hansen(predictions, hansen_path)
        return results


def run_yvytu_demo():
    """Run a demo of the Yvytu pipeline on 1 Chaco tile."""
    pipeline = YvytuPipeline()
    pipeline.load_model()

    # Select Chaco tiles
    tiles = pipeline.select_tiles()
    print(f"Selected {len(tiles)} Chaco tiles")
    print(f"First 5: {tiles[:5]}")

    if not tiles:
        print("No Chaco tiles found")
        return

    # Process first tile
    tile = tiles[0]
    print(f"\nProcessing {tile}...")

    # Compute embeddings
    emb = pipeline.compute_tile_embeddings(tile)
    print(f"  Embeddings shape: {emb.shape}")

    # Simulate NDVI time series
    T = 24  # 2 years of monthly composites
    H = W = 224  # standard tile size
    ndvi = np.random.rand(T, H, W).astype(np.float32) * 0.5 + 0.3

    dates = [f"2024-{m:02d}-01" for m in range(1, 13)] * 2

    # Detect deforestation
    mask = pipeline.detect_deforestation(tile, ndvi, dates)
    print(f"  Deforestation pixels: {mask.sum()} / {mask.size}")

    return mask


if __name__ == "__main__":
    run_yvytu_demo()
