"""Indigenous territory overlap with deforestation — using Hansen data.

Strategy: process each Hansen tile independently because territories span
the full country. Compute loss per territory, taking into account which
tiles each territory touches.

Outputs:
    outputs/p0011/indigenous/indigenous_overlap.json
    outputs/p0011/indigenous/indigenous_overlap.png
"""

import json
import sys
import time
from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import rasterio
from rasterio.features import rasterize

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))


OUT_DIR = REPO_ROOT / "outputs/p0011/indigenous"
OUT_DIR.mkdir(parents=True, exist_ok=True)

HANSEN_DIR = REPO_ROOT / "data/hansen"
GEOJSON = REPO_ROOT / "data/boundaries/indigenous_territories.geojson"


def process_tile(tile, gdf):
    """Process one Hansen tile and compute per-territory loss."""
    lossyear_path = HANSEN_DIR / f"hansen_lossyear_{tile}.tif"
    if not lossyear_path.exists():
        return None

    with rasterio.open(lossyear_path) as src:
        lossyear = src.read(1)
        transform = src.transform
        crs = src.crs
        shape = src.shape

    # Filter territories that intersect this tile's bounds
    tile_bounds = src.bounds  # left, bottom, right, top
    gdf_tile = gdf.cx[tile_bounds.left : tile_bounds.right, tile_bounds.bottom : tile_bounds.top].copy()
    if len(gdf_tile) == 0:
        return {}

    if gdf_tile.crs != crs:
        gdf_tile = gdf_tile.to_crs(crs)

    # Rasterize
    shapes = [(geom, i + 1) for i, geom in enumerate(gdf_tile.geometry)]
    territory_array = rasterize(
        shapes=shapes,
        out_shape=shape,
        transform=transform,
        fill=0,
        dtype=np.uint16,
    )

    # Per-territory stats
    results = {}
    for i, (_, row) in enumerate(gdf_tile.iterrows()):
        territory_id = i + 1
        mask = territory_array == territory_id
        if not mask.any():
            continue
        loss_pixels = int((lossyear[mask] > 0).sum())
        total_pixels = int(mask.sum())
        loss_pct = 100 * loss_pixels / total_pixels if total_pixels > 0 else 0
        results[row["name"]] = {
            "pixels": total_pixels,
            "loss_pixels": loss_pixels,
            "loss_pct": loss_pct,
        }
    return results


def main():
    print("=" * 70)
    print("INDIGENOUS TERRITORY OVERLAP WITH DEFORESTATION (Hansen GFC)")
    print("=" * 70)
    print("\n*** NOTE: Territory bounding boxes are approximate, NOT legal")
    print("    boundaries. Results are illustrative only.\n")

    # Load territories
    print("[1/2] Loading indigenous territories...")
    gdf = gpd.read_file(str(GEOJSON))
    print(f"  {len(gdf)} territories loaded")

    # Process each tile
    print("\n[2/2] Processing Hansen tiles...")
    combined_results = {}  # name -> {pixels, loss_pixels, loss_pct}

    for tile in ["20S_060W", "20S_070W"]:
        tile_results = process_tile(tile, gdf)
        if tile_results is None:
            print(f"  {tile}: NOT FOUND, skipping")
            continue
        print(f"  {tile}: processed {len(tile_results)} territories in tile bounds")
        # Accumulate
        for name, stats in tile_results.items():
            if name not in combined_results:
                combined_results[name] = {"pixels": 0, "loss_pixels": 0}
            combined_results[name]["pixels"] += stats["pixels"]
            combined_results[name]["loss_pixels"] += stats["loss_pixels"]

    # Build full results with metadata
    pixel_area_ha = 0.0625
    mean_tc = 50.0
    agb = 100 * mean_tc**2 / (100 + mean_tc**2)
    carbon_per_ha = agb * 0.47

    results = []
    for _, row in gdf.iterrows():
        name = row["name"]
        if name not in combined_results:
            continue
        stats = combined_results[name]
        total_pixels = stats["pixels"]
        loss_pixels = stats["loss_pixels"]
        loss_pct = 100 * loss_pixels / total_pixels if total_pixels > 0 else 0
        loss_ha = loss_pixels * pixel_area_ha
        co2e_mt = carbon_per_ha * loss_ha * 44 / 12 / 1000

        results.append(
            {
                "name": name,
                "people": row["people"],
                "status": row.get("status", "Unknown"),
                "claimed_area_km2": float(row.get("area_km2", 0)),
                "polygon_area_km2": float(row.get("area_km2_computed", 0)),
                "pixels_in_window": total_pixels,
                "loss_pixels": loss_pixels,
                "loss_pct": float(loss_pct),
                "loss_ha": float(loss_ha),
                "co2e_mt": float(co2e_mt),
            }
        )

    # Sort by loss %
    results.sort(key=lambda x: x["loss_pct"], reverse=True)

    print(f"\n{'=' * 70}")
    print(f"{'Territory':<35}  {'People':<18}  {'Loss %':>8}  {'Loss km²':>10}")
    print("-" * 80)
    for r in results:
        print(f"{r['name'][:33]:<35}  {r['people'][:16]:<18}  " f"{r['loss_pct']:>7.2f}%  {r['loss_ha']/100:>10,.0f}")

    # Save
    out_json = OUT_DIR / "indigenous_overlap.json"
    out_json.write_text(
        json.dumps(
            {
                "data_source": "Hansen GFC v1.11 + IWGIA/AVINA/INDI public references",
                "n_territories": len(results),
                "disclaimer": "Territories are approximate bboxes, not legal boundaries",
                "territories": results,
                "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            },
            indent=2,
        )
    )

    # Plot
    plot_results(results, OUT_DIR / "indigenous_overlap.png")

    print(f"\n{'=' * 70}")
    print(f"Results: {out_json}")
    print(f"Figure: {OUT_DIR}/indigenous_overlap.png")
    if results:
        worst = results[0]
        print(
            f"\n  Most affected: {worst['name']} — {worst['loss_pct']:.1f}% loss, " f"~{worst['loss_ha']/100:.0f} km²"
        )
        avg_loss = np.mean([r["loss_pct"] for r in results])
        print(f"  Average loss % across all territories: {avg_loss:.1f}%")


def plot_results(results, out_path):
    """Bar chart of loss % per indigenous territory."""
    names = [r["name"][:25] for r in results]
    pcts = [r["loss_pct"] for r in results]
    co2es = [r["co2e_mt"] for r in results]

    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    ax = axes[0]
    colors = plt.cm.Reds(np.linspace(0.3, 0.9, len(names)))
    ax.barh(names[::-1], pcts[::-1], color=colors[::-1])
    ax.set_xlabel("Forest loss 2001-2023 (%)")
    ax.set_title("Deforestation in Indigenous Territories")
    ax.grid(True, alpha=0.3, axis="x")

    ax = axes[1]
    colors2 = plt.cm.Oranges(np.linspace(0.3, 0.9, len(names)))
    ax.barh(names[::-1], co2es[::-1], color=colors2[::-1])
    ax.set_xlabel("CO2e (Mt)")
    ax.set_title("Carbon loss in Indigenous Territories")
    ax.grid(True, alpha=0.3, axis="x")

    plt.suptitle(
        "Indigenous Territory Overlap with Hansen GFC Loss\n" "*** Approximate bboxes — illustrative only ***",
        fontsize=12,
    )
    plt.tight_layout()
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close()


if __name__ == "__main__":
    main()
