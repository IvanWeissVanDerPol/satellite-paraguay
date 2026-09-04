"""Fetch Sentinel-2 grid for P0011 Yvutu (default 30 tiles covering Paraguay).

Wraps `download_sentinel2_real.py` and orchestrates downloading a grid of
30 tiles at 5x6 covering the whole country with under 10 percent cloud cover.

Each tile is approximately 50MB RGB plus NIR. 30 tiles is approximately 1.5GB total.

This script generates the tile bounding box list, then loops through
calling download_sentinel2_real.py per tile with retry logic.

Usage:
    python3 scripts/fetch_yvutu_sentinel2_grid.py --n-tiles 30
    python3 scripts/fetch_yvutu_sentinel2_grid.py --n-tiles 30 --max-cloud 5 --months 2024-06 2024-08

Output:
    data/sentinel2/S2_{tile_id}_{date}_B02_B03_B04_B08.tif
    data/sentinel2/MANIFEST.json
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def generate_paraguay_grid(n_tiles=30):
    """Generate Paraguay bounding-box grid.

    Paraguay spans roughly:
    - Lat: -19.5 (south) to -27.5 (south) equals 8 degrees
    - Lon: -62.5 (west) to -54.5 (east) equals 8 degrees

    For 30 tiles (5 rows by 6 columns): each tile is roughly 1.6 deg lat by 1.3 deg lon.

    Returns list of (min_lon, min_lat, max_lon, max_lat, tile_id) tuples.
    """
    rows = 5
    cols = 6
    lat_min, lat_max = -27.5, -19.5
    lon_min, lon_max = -62.5, -54.5

    lat_step = (lat_max - lat_min) / rows
    lon_step = (lon_max - lon_min) / cols

    tiles = []
    for r in range(rows):
        for c in range(cols):
            t_lat_min = lat_min + r * lat_step
            t_lat_max = lat_min + (r + 1) * lat_step
            t_lon_min = lon_min + c * lon_step
            t_lon_max = lon_min + (c + 1) * lon_step
            tile_id = "PAR_{}_{}_S{}W{}".format(r, c, r, c)
            tiles.append((t_lon_min, t_lat_min, t_lon_max, t_lat_max, tile_id))

    return tiles[:n_tiles]


def download_one(tile, max_cloud, months, output_dir, retry=3):
    """Download one tile via the underlying script."""
    lon_min, lat_min, lon_max, lat_max, tile_id = tile

    cmd = [
        ".venv/bin/python",
        str(REPO_ROOT / "scripts" / "download_sentinel2_real.py"),
        "--bbox", str(lon_min), str(lat_min), str(lon_max), str(lat_max),
        "--max-cloud", str(max_cloud),
        "--n-scenes", "1",
        "--output-dir", str(output_dir / tile_id),
    ]
    if months:
        cmd.extend(["--months"] + months)

    print("  [{}] Downloading bbox=[{:.2f},{:.2f},{:.2f},{:.2f}]".format(
        tile_id, lon_min, lat_min, lon_max, lat_max))
    for attempt in range(retry):
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
            if r.returncode == 0:
                return {"tile_id": tile_id, "status": "success", "attempt": attempt + 1}
            else:
                print("    Attempt {} failed (rc={}): {}".format(
                    attempt + 1, r.returncode, r.stderr[:100]))
        except subprocess.TimeoutExpired:
            print("    Attempt {} timed out".format(attempt + 1))
    return {"tile_id": tile_id, "status": "failed", "attempt": retry}


def main():
    parser = argparse.ArgumentParser(
        description="Fetch Sentinel-2 grid for P0011 Yvutu (default 30 tiles covering Paraguay)"
    )
    parser.add_argument("--n-tiles", type=int, default=30,
                        help="Number of tiles (default 30)")
    parser.add_argument("--max-cloud", type=float, default=10,
                        help="Max cloud cover (default 10)")
    parser.add_argument("--months", type=str, nargs="+",
                        default=["2024-06", "2024-07", "2024-08"],
                        help="Months to search (default 2024 dry season)")
    parser.add_argument("--output-dir", type=Path,
                        default=REPO_ROOT / "data" / "sentinel2")
    args = parser.parse_args()

    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    tiles = generate_paraguay_grid(args.n_tiles)
    print("=" * 70)
    print("P0011 Yvutu — Sentinel-2 grid download")
    print("=" * 70)
    print("  Target: {} tiles covering Paraguay".format(len(tiles)))
    print("  Max cloud: {}".format(args.max_cloud))
    print("  Months: {}".format(args.months))
    print("  Output: {}".format(output_dir))
    print("  Estimated size: ~{} MB".format(len(tiles) * 50))
    print()

    results = []
    for tile in tiles:
        result = download_one(
            tile, args.max_cloud, args.months, output_dir
        )
        results.append(result)
        print("    Status: {} (attempt {})".format(result["status"], result["attempt"]))

    manifest = output_dir / "MANIFEST.json"
    with manifest.open("w") as f:
        json.dump({
            "downloaded_at": __import__("datetime").datetime.utcnow().isoformat() + "Z",
            "n_tiles_target": len(tiles),
            "results": results,
            "successful": sum(1 for r in results if r["status"] == "success"),
            "failed": sum(1 for r in results if r["status"] == "failed"),
        }, f, indent=2)
    print()
    print("Manifest: {}".format(manifest))
    print("Successful: {}/{}".format(
        sum(1 for r in results if r["status"] == "success"),
        len(results)))

    if any(r["status"] == "failed" for r in results):
        sys.exit(1)


if __name__ == "__main__":
    main()