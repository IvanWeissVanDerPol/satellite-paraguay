"""Sample download script for Sentinel-2.

This is a placeholder — real implementation uses Google Earth Engine API.
"""
import argparse
from pathlib import Path

from src.satellite_io import download_via_gee
from src.paraguay_admin import get_tile_bbox, load_tile_index


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--tile", default="-54.267_-21.164", help="Tile ID (lon_lat)")
    parser.add_argument("--satellite", default="sentinel2", choices=["sentinel2", "landsat9"])
    parser.add_argument("--start", default="2024-01-01")
    parser.add_argument("--end", default="2025-12-31")
    parser.add_argument("--max-tiles", type=int, default=5)
    args = parser.parse_args()

    print(f"Downloading {args.satellite} for tile {args.tile}")

    bbox = get_tile_bbox(args.tile)
    if bbox is None:
        print(f"ERROR: Invalid tile {args.tile}")
        return

    out_path = download_via_gee(
        tile_id=args.tile,
        bbox=bbox,
        satellite=args.satellite,
        start_date=args.start,
        end_date=args.end,
    )
    print(f"Output: {out_path}")


if __name__ == "__main__":
    main()
