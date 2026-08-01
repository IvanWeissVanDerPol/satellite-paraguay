"""Paper 5: P0026 Kai — Wildlife poaching detection.

Target journal: Conservation Biology
Advisors: Multi (FCM + WWF Paraguay + Guyra Paraguay)
Timeline: 10 weeks

Hypothesis: YOLOv8 + COCO-zoo transfer learning + NASA FIRMS fire alerts
detects poaching camps in Defensores del Chaco with mAP@0.5 > 0.70.
"""
from pathlib import Path
from typing import Optional, Dict
import numpy as np

from ...paraguay_admin import get_tile_bbox, list_tiles_in_region
from ...evaluation import detection_map, print_metrics


class KaiPipeline:
    """Wildlife poaching detection pipeline."""

    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {
            "defensores_bbox": {
                "min_lon": -61.0,
                "max_lon": -58.0,
                "min_lat": -22.5,
                "max_lat": -20.0,
            },
            "yolo_model": "yolov8m.pt",
            "coco_transfer": True,
        }
        self.model = None

    def load_model(self):
        """Load YOLOv8 model."""
        try:
            from ultralytics import YOLO
        except ImportError:
            raise ImportError("ultralytics not installed. Run: pip install ultralytics")
        self.model = YOLO(self.config["yolo_model"])

    def select_tiles(self) -> list:
        """Select Defensores del Chaco tiles."""
        return list_tiles_in_region(self.config["defensores_bbox"])

    def detect_poaching(
        self,
        tile_id: str,
        image_path: Path,
    ) -> Dict:
        """Detect poaching camps in a tile.

        Returns detection results.
        """
        if self.model is None:
            self.load_model()

        # Real implementation: model.predict(image_path)
        results = self.model(image_path) if self.model else []

        return {
            "tile_id": tile_id,
            "detections": [],
            "num_detections": 0,
            "confidence_scores": [],
        }

    def fetch_firms_fires(self, days: int = 7) -> list:
        """Fetch recent fire detections from NASA FIRMS.

        Used to find suspicious fire patterns (poaching camps).
        """
        # Real implementation: NASA FIRMS API
        print(f"[firms] Fetching fires for last {days} days")
        return []


def run_kai_demo():
    """Demo: detect poaching in Defensores del Chaco."""
    pipeline = KaiPipeline()
    tiles = pipeline.select_tiles()
    print(f"  Defensores del Chaco tiles: {len(tiles)}")


if __name__ == "__main__":
    run_kai_demo()
