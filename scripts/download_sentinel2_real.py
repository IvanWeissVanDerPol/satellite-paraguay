"""Real Sentinel-2 download via Microsoft Planetary Computer.

NO AUTH REQUIRED. Free access to Sentinel-2 L2A via STAC API.
https://planetarycomputer.microsoft.com/

Usage:
    python3 scripts/download_sentinel2_real.py --bbox -60.5 -24.5 -58.5 -22.5 --max-cloud 10 --n-scenes 5
    python3 scripts/download_sentinel2_real.py --bbox -60.5 -24.5 -58.5 -22.5 --max-cloud 5 --months 2024-08 2024-09
"""
import sys
import time
import urllib.request
import json
from pathlib import Path

REPO_ROOT = Path("/root/satellite-paraguay")
sys.path.insert(0, str(REPO_ROOT))

# Auto-install if missing
try:
    import planetary_computer
    import pystac_client
except ImportError:
    import subprocess
    subprocess.run([
        sys.executable, "-m", "pip", "install",
        "planetary-computer", "pystac-client", "rasterio",
        "--break-system-packages", "-q"
    ], check=True)
    import planetary_computer
    import pystac_client

import argparse

argparser = argparse.ArgumentParser()
argparser.add_argument("--bbox", type=float, nargs=4, required=True,
                       help="Bounding box: min_lon min_lat max_lon max_lat")
argparser.add_argument("--max-cloud", type=float, default=20,
                       help="Max cloud cover percentage (default 20)")
argparser.add_argument("--n-scenes", type=int, default=5,
                       help="Number of scenes to download (default 5)")
argparser.add_argument("--months", type=str, nargs="+", default=None,
                       help="YYYY-MM months to filter (default: all)")
argparser.add_argument("--bands", type=str, nargs="+",
                       default=["B02", "B03", "B04", "B08"],
                       help="Bands to download (default RGB+NIR)")
argparser.add_argument("--output-dir", type=str, default="data/sentinel2")
args = argparser.parse_args()

output_dir = Path(args.output_dir)
output_dir.mkdir(parents=True, exist_ok=True)

print("=" * 70)
print("Sentinel-2 Real Download via Planetary Computer (FREE, NO AUTH)")
print("=" * 70)
print(f"BBox: {args.bbox}")
print(f"Max cloud: {args.max_cloud}%")
print(f"Bands: {args.bands}")

# Search
catalog = pystac_client.Client.open("https://planetarycomputer.microsoft.com/api/stac/v1/")

search_kwargs = {
    "collections": ["sentinel-2-l2a"],
    "bbox": args.bbox,
    "query": {"eo:cloud_cover": {"lt": args.max_cloud}},
    "limit": args.n_scenes * 3,  # over-fetch to filter by month
}

if args.months:
    search_kwargs["datetime"] = f"{args.months[0]}-01/{args.months[-1]}-28"

items = list(catalog.search(**search_kwargs).items())
print(f"\nFound {len(items)} scenes")

# Filter by months if specified
if args.months:
    items = [i for i in items if any(i.datetime.strftime("%Y-%m") == m for m in args.months)]

# Take first n
items = items[:args.n_scenes]
print(f"Downloading {len(items)} scenes")

# Download each
results = []
for i, item in enumerate(items):
    print(f"\n--- Scene {i+1}/{len(items)}: {item.id} ---")
    print(f"  Date: {item.datetime}")
    print(f"  Cloud: {item.properties['eo:cloud_cover']:.1f}%")
    print(f"  Tile: {item.properties['s2:mgrs_tile']}")

    signed = planetary_computer.sign(item)

    scene_results = {
        "id": item.id,
        "datetime": str(item.datetime),
        "tile": item.properties["s2:mgrs_tile"],
        "cloud_cover": item.properties["eo:cloud_cover"],
        "bands_downloaded": [],
    }

    for band in args.bands:
        out_path = output_dir / f"{item.id}_{band}.tif"
        if out_path.exists():
            print(f"  {band}: exists ({out_path.stat().st_size//1024//1024} MB)")
            scene_results["bands_downloaded"].append(band)
            continue

        url = signed.assets[band].href
        try:
            start = time.time()
            urllib.request.urlretrieve(url, str(out_path))
            elapsed = time.time() - start
            size_mb = out_path.stat().st_size // 1024 // 1024
            print(f"  {band}: {size_mb} MB in {elapsed:.1f}s")
            scene_results["bands_downloaded"].append(band)
        except Exception as e:
            print(f"  {band}: FAIL {e}")

    results.append(scene_results)

# Save manifest
manifest_path = output_dir / "manifest.json"
manifest_path.write_text(json.dumps(results, indent=2, default=str))

print(f"\n{'=' * 70}")
print(f"Done. Manifest at {manifest_path}")
print(f"Total scenes: {len(results)}")
total_bands = sum(len(r["bands_downloaded"]) for r in results)
print(f"Total bands: {total_bands}")