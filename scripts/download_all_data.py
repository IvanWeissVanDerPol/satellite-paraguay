"""Master data download — gets all real datasets needed for the thesis.

Downloads (all FREE, no auth required):
1. Hansen GFC v1.11 (2 tiles, ~700 MB) - forest loss for 2000-2023
2. MapBiomas Paraguay Collection 2 (38 MB) - land cover 2023
3. Sentinel-2 L2A (configurable) - 10m optical imagery

Outputs:
    data/hansen/hansen_*.tif
    data/mapbiomas/mapbiomas_paraguay_2023.tif
    data/sentinel2/S2*_*.tif
    data/DOWNLOAD_MANIFEST.json

Usage:
    python3 scripts/download_all_data.py --quick         # Hansen + MapBiomas only (~5 min)
    python3 scripts/download_all_data.py --with-s2 5      # also 5 Sentinel-2 scenes (~30 min)
    python3 scripts/download_all_data.py --full          # everything (~2 hours)
"""

import json
import sys
import time
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))


def download_hansen():
    """Download Hansen GFC v1.11 for Paraguay (2 tiles, ~700MB)."""
    print("\n[1/3] Downloading Hansen GFC v1.11...")
    output_dir = REPO_ROOT / "data" / "hansen"
    output_dir.mkdir(parents=True, exist_ok=True)

    base = "https://storage.googleapis.com/earthenginepartners-hansen/GFC-2023-v1.11/Hansen_GFC-2023-v1.11"

    # 2 tiles cover Paraguay: 20S_060W (east) + 20S_070W (west/Chaco)
    tiles = ["20S_060W", "20S_070W"]
    layers = ["treecover2000", "lossyear", "datamask"]

    results = []
    for tile in tiles:
        for layer in layers:
            out_path = output_dir / f"hansen_{layer}_{tile}.tif"
            url = f"{base}_{layer}_{tile}.tif"
            if out_path.exists():
                print(f"  {tile} {layer}: exists ({out_path.stat().st_size//1024//1024} MB)")
                continue
            print(f"  Downloading {tile} {layer}...", end=" ", flush=True)
            start = time.time()
            try:
                urllib.request.urlretrieve(url, str(out_path))
                size = out_path.stat().st_size // 1024 // 1024
                print(f"{size} MB in {time.time()-start:.0f}s")
                results.append({"tile": tile, "layer": layer, "size_mb": size})
            except Exception as e:
                print(f"FAIL {e}")

    return results


def download_mapbiomas():
    """Download MapBiomas Paraguay Collection 2 (latest year)."""
    print("\n[2/3] Downloading MapBiomas Paraguay 2023...")
    output_dir = REPO_ROOT / "data" / "mapbiomas"
    output_dir.mkdir(parents=True, exist_ok=True)

    url = "https://storage.googleapis.com/mapbiomas-public/initiatives/paraguay/collection_2/mapbiomas_paraguay_collection2_integration_v1-classification_2023.tif"  # noqa: E501
    out_path = output_dir / "mapbiomas_paraguay_2023.tif"

    if out_path.exists():
        print(f"  MapBiomas 2023: exists ({out_path.stat().st_size//1024//1024} MB)")
        return [{"size_mb": out_path.stat().st_size // 1024 // 1024}]

    print("  Downloading...", end=" ", flush=True)
    start = time.time()
    urllib.request.urlretrieve(url, str(out_path))
    size = out_path.stat().st_size // 1024 // 1024
    print(f"{size} MB in {time.time()-start:.0f}s")
    return [{"size_mb": size}]


def download_sentinel2(n_scenes=5, max_cloud=20):
    """Download Sentinel-2 L2A from Planetary Computer."""
    print(f"\n[3/3] Downloading {n_scenes} Sentinel-2 scenes (max cloud {max_cloud}%)...")

    try:
        import planetary_computer
        import pystac_client
    except ImportError:
        import subprocess

        subprocess.run(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                "planetary-computer",
                "pystac-client",
                "--break-system-packages",
                "-q",
            ],
            check=True,
        )
        import planetary_computer
        import pystac_client

    output_dir = REPO_ROOT / "data" / "sentinel2"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Paraguay Chaco bbox (covers Pilcomayo to Concepcion)
    bbox = [-60.5, -24.5, -58.5, -22.5]

    catalog = pystac_client.Client.open("https://planetarycomputer.microsoft.com/api/stac/v1/")
    search = catalog.search(
        collections=["sentinel-2-l2a"],
        bbox=bbox,
        datetime="2024-06-01/2024-09-30",
        query={"eo:cloud_cover": {"lt": max_cloud}},
        limit=n_scenes * 3,
    )
    items = list(search.items())[:n_scenes]

    print(f"  Found {len(items)} scenes")

    bands = ["B02", "B03", "B04", "B08"]  # RGB + NIR
    results = []

    for i, item in enumerate(items):
        print(f"\n  Scene {i+1}/{len(items)}: {item.id}")
        print(f"    Date: {item.datetime}, cloud={item.properties['eo:cloud_cover']:.1f}%")
        signed = planetary_computer.sign(item)
        for band in bands:
            out_path = output_dir / f"{item.id}_{band}.tif"
            if out_path.exists():
                continue
            try:
                start = time.time()
                urllib.request.urlretrieve(signed.assets[band].href, str(out_path))
                size_mb = out_path.stat().st_size // 1024 // 1024
                print(f"    {band}: {size_mb} MB in {time.time()-start:.1f}s")
                results.append({"scene": item.id, "band": band, "size_mb": size_mb})
            except Exception as e:
                print(f"    {band}: FAIL {e}")

    return results


def main():
    import argparse

    argparser = argparse.ArgumentParser()
    argparser.add_argument("--quick", action="store_true", help="Hansen + MapBiomas only (~5 min)")
    argparser.add_argument("--with-s2", type=int, default=0, help="Also download N Sentinel-2 scenes")
    argparser.add_argument("--full", action="store_true", help="Download everything (slow)")
    args = argparser.parse_args()

    print("=" * 70)
    print("SatelliteCV-Paraguay — Master Data Download")
    print("=" * 70)
    print("Sources (all FREE):")
    print("  - Hansen GFC: https://storage.googleapis.com/earthenginepartners-hansen/")
    print("  - MapBiomas Paraguay: https://plataforma.mapbiomas.org/")
    print("  - Sentinel-2: https://planetarycomputer.microsoft.com/")

    manifest = {
        "started_at": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "hansen": [],
        "mapbiomas": [],
        "sentinel2": [],
    }

    manifest["hansen"] = download_hansen()
    manifest["mapbiomas"] = download_mapbiomas()

    if args.with_s2 > 0:
        manifest["sentinel2"] = download_sentinel2(n_scenes=args.with_s2)
    elif args.full:
        manifest["sentinel2"] = download_sentinel2(n_scenes=20)

    manifest["finished_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ")

    out = REPO_ROOT / "data" / "DOWNLOAD_MANIFEST.json"
    out.write_text(json.dumps(manifest, indent=2, default=str))

    print(f"\n{'=' * 70}")
    print(f"Done. Manifest at {out}")
    print(f"Hansen: {len(manifest['hansen'])} files")
    print(f"MapBiomas: {len(manifest['mapbiomas'])} files")
    print(f"Sentinel-2: {len(manifest['sentinel2'])} files")


if __name__ == "__main__":
    main()
