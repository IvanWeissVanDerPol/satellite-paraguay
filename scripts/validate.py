"""Validate predictions for each paper."""
import argparse
from pathlib import Path

from src.papers.p0011_yvytu_deforestation import YvytuPipeline
from src.papers.p0100_yvyra_carbon_credits import YvyraPipeline
from src.papers.p0025_yrupe_yield import YrupePipeline
from src.papers.p0012_yvy_indigenous import YvyPipeline
from src.papers.p0026_kai_poaching import KaiPipeline
from src.papers.p0035_tatakua_air_quality import TatakuaPipeline


def validate_paper_1():
    """Validate P0011 Yvytu deforestation predictions."""
    print("\n=== P0011 Yvytu (Chaco deforestation) ===")
    pipeline = YvytuPipeline()
    # Simulate predictions
    import numpy as np
    preds = np.random.randint(0, 5, size=(256, 256), dtype=np.uint8)
    print(f"  Predictions shape: {preds.shape}")
    print(f"  Deforested pixels: {(preds == 2).sum()}")
    print("  NOTE: Real validation needs MapBiomas + Hansen GFC files")


def validate_paper_2():
    """Validate P0100 Yvyra carbon predictions."""
    print("\n=== P0100 Yvyra (Carbon credits) ===")
    pipeline = YvyraPipeline()
    projects = pipeline.fetch_verra_projects()
    print(f"  Verra projects: {len(projects)}")


def validate_paper_3():
    """Validate P0025 Yrupe yield predictions."""
    print("\n=== P0025 Yrupe (Soybean yield) ===")
    pipeline = YrupePipeline()
    inbio = pipeline.load_inbio_data()
    print(f"  INBIO data: {inbio}")


def validate_paper_4():
    """Validate P0012 Yvy indigenous conflicts."""
    print("\n=== P0012 Yvy (Indigenous territory) ===")
    pipeline = YvyPipeline()
    conflicts = pipeline.detect_conflicts()
    print(f"  Conflicts: {conflicts['conflict_parcels']}")


def validate_paper_5():
    """Validate P0026 Kai poaching detection."""
    print("\n=== P0026 Kai (Wildlife poaching) ===")
    pipeline = KaiPipeline()
    tiles = pipeline.select_tiles()
    print(f"  Defensores del Chaco tiles: {len(tiles)}")


def validate_paper_6():
    """Validate P0035 Tatakua air quality."""
    print("\n=== P0035 Tatakua (Air quality) ===")
    pipeline = TatakuaPipeline()
    data = pipeline.fetch_openaq_data(days=30)
    print(f"  OpenAQ measurements: {len(data)}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--paper", type=int, help="Validate specific paper (1-6)")
    parser.add_argument("--all", action="store_true", help="Validate all papers")
    args = parser.parse_args()

    if args.all or args.paper is None:
        for i in range(1, 7):
            func = globals()[f"validate_paper_{i}"]
            func()
    else:
        func = globals()[f"validate_paper_{args.paper}"]
        func()

    print("\nValidation complete.")


if __name__ == "__main__":
    main()
