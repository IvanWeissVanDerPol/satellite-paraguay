"""MapBiomas temporal comparison — synthetic 2020 vs 2023 from Hansen.

Since we only have MapBiomas 2023, we use Hansen-derived proxies for
historical land cover. For each year y, we compute "what MapBiomas
would have shown" by aggregating Hansen treecover and lossyear.

This gives a "pseudo-MapBiomas" time series that's consistent with
the real 2023 MapBiomas.

Outputs:
    outputs/mapbiomas_temporal/yearly_land_cover.csv
    outputs/mapbiomas_temporal/land_cover_changes.json
"""
import sys
import json
import csv
from pathlib import Path

REPO_ROOT = Path("/root/satellite-paraguay")
sys.path.insert(0, str(REPO_ROOT))

import numpy as np
import rasterio
from rasterio.windows import Window

OUT_DIR = REPO_ROOT / "outputs/mapbiomas_temporal"
OUT_DIR.mkdir(parents=True, exist_ok=True)

HANSEN_DIR = REPO_ROOT / "data/hansen"


def mapbiomas_class_from_hansen(treecover, lossyear, year):
    """Compute MapBiomas-like classification from Hansen at year.

    Classes:
    - 3 (Forest): treecover > 60% AND not yet deforested
    - 4 (Savanna): treecover 30-60% AND not yet deforested (Chaco dry forest)
    - 15 (Pasture): was forest (treecover 2000 > 30%), now lost
    - 18 (Agriculture): was forest, lost multiple times (proxy)
    - 26 (Water): low treecover (proxy)

    Returns: array of class labels
    """
    # Forest cover at year
    was_forest_dense = treecover > 60
    was_forest_open = treecover > 30
    lost_before = lossyear > 0
    lost_before_y = (lossyear > 0) & (lossyear <= (year - 2000))

    forest = was_forest_dense & ~lost_before_y
    savanna = was_forest_open & ~was_forest_dense & ~lost_before_y
    pasture = was_forest_open & lost_before_y

    classification = np.full(treecover.shape, 0, dtype=np.uint8)  # 0 = unclassified
    classification[forest] = 3
    classification[savanna] = 4
    classification[~was_forest_open & (treecover > 10)] = 26  # proxy for water/bare
    classification[pasture] = 15

    return classification


def main():
    print("=" * 70)
    print("MAPBIOMAS TEMPORAL COMPARISON (synthetic from Hansen)")
    print("=" * 70)

    print("\n[1/4] Loading Hansen data...")
    with rasterio.open(HANSEN_DIR / "hansen_lossyear_20S_060W.tif") as src:
        lossyear = src.read(1, window=Window(0, 0, 2000, 2000))
    with rasterio.open(HANSEN_DIR / "hansen_treecover2000_20S_060W.tif") as src:
        treecover = src.read(1, window=Window(0, 0, 2000, 2000))

    print(f"  Treecover: {treecover.shape}, mean={treecover.mean():.1f}%")
    print(f"  Lossyear: {(lossyear > 0).sum():,} loss pixels 2001-2023")

    print("\n[2/4] Computing pseudo-MapBiomas for each year (2015-2023)...")
    years = list(range(2015, 2024))
    yearly_stats = {}
    for y in years:
        classification = mapbiomas_class_from_hansen(treecover, lossyear, y)
        n_forest = int((classification == 3).sum())
        n_savanna = int((classification == 4).sum())
        n_pasture = int((classification == 15).sum())
        n_water = int((classification == 26).sum())
        total = classification.size
        yearly_stats[y] = {
            "forest_pct": round(100 * n_forest / total, 2),
            "savanna_pct": round(100 * n_savanna / total, 2),
            "pasture_pct": round(100 * n_pasture / total, 2),
            "water_pct": round(100 * n_water / total, 2),
            "n_forest": n_forest,
            "n_savanna": n_savanna,
            "n_pasture": n_pasture,
            "n_water": n_water,
            "total_pixels": total,
        }

    print(f"\n  {'Year':<6} {'Forest':>10} {'Savanna':>10} {'Pasture':>10} {'Water':>10}")
    print(f"  {'-'*6:<6} {'-'*10:>10} {'-'*10:>10} {'-'*10:>10} {'-'*10:>10}")
    for y, stats in yearly_stats.items():
        print(f"  {y:<6} {stats['forest_pct']:>9.2f}% {stats['savanna_pct']:>9.2f}% {stats['pasture_pct']:>9.2f}% {stats['water_pct']:>9.2f}%")

    print("\n[3/4] Computing year-on-year changes...")
    changes = {}
    for i in range(1, len(years)):
        prev = yearly_stats[years[i-1]]
        curr = yearly_stats[years[i]]
        forest_change = curr["forest_pct"] - prev["forest_pct"]
        pasture_change = curr["pasture_pct"] - prev["pasture_pct"]
        changes[years[i]] = {
            "forest_change_pct": round(forest_change, 3),
            "pasture_change_pct": round(pasture_change, 3),
        }
        print(f"  {years[i-1]} -> {years[i]}: forest {forest_change:+.3f}%, pasture {pasture_change:+.3f}%")

    print("\n[4/4] Real 2023 MapBiomas comparison...")
    mb_path = REPO_ROOT / "data/mapbiomas/mapbiomas_paraguay_2023.tif"
    if mb_path.exists():
        with rasterio.open(mb_path) as src:
            mb_chunk = src.read(1, window=Window(8000, 8000, 1000, 1000))
        from scipy.ndimage import zoom
        mb_full = zoom(mb_chunk, (2.0, 2.0), order=0)
        mb_forest = float((mb_full == 3).mean() * 100)
        mb_pasture = float((mb_full == 15).mean() * 100)
        mb_agri = float((mb_full == 18).mean() * 100)

        our_2023 = yearly_stats[2023]

        comparison = {
            "metric": "2023 forest/pasture/agriculture %",
            "mapbiomas_real": {
                "forest_pct": round(mb_forest, 2),
                "pasture_pct": round(mb_pasture, 2),
                "agriculture_pct": round(mb_agri, 2),
            },
            "our_pseudo_mapbiomas": {
                "forest_pct": our_2023["forest_pct"],
                "pasture_pct": our_2023["pasture_pct"],
            },
            "differences": {
                "forest_diff": round(our_2023["forest_pct"] - mb_forest, 2),
                "pasture_diff": round(our_2023["pasture_pct"] - mb_pasture, 2),
            },
        }
        print(f"  Real MapBiomas 2023: forest {mb_forest:.2f}%, pasture {mb_pasture:.2f}%")
        print(f"  Our pseudo 2023:     forest {our_2023['forest_pct']:.2f}%, pasture {our_2023['pasture_pct']:.2f}%")
        print(f"  Difference: forest {comparison['differences']['forest_diff']:+.2f}%, pasture {comparison['differences']['pasture_diff']:+.2f}%")
    else:
        comparison = {"mapbiomas_2023": "not available"}
        print("  Real MapBiomas 2023 not available for comparison")

    # Save outputs
    (OUT_DIR / "yearly_land_cover.csv").write_text(
        "\n".join([
            ",".join(["year", "forest_pct", "savanna_pct", "pasture_pct", "water_pct", "n_forest", "n_pasture"]),
            *[
                ",".join([
                    str(y),
                    str(stats["forest_pct"]),
                    str(stats["savanna_pct"]),
                    str(stats["pasture_pct"]),
                    str(stats["water_pct"]),
                    str(stats["n_forest"]),
                    str(stats["n_pasture"]),
                ])
                for y, stats in yearly_stats.items()
            ],
        ])
    )

    (OUT_DIR / "land_cover_changes.json").write_text(json.dumps({
        "yearly_stats": yearly_stats,
        "yearly_changes": changes,
        "real_mapbiomas_comparison": comparison,
        "methodology": "Pseudo-MapBiomas derived from Hansen treecover + lossyear",
        "limitations": [
            "Pasture/agriculture classes are proxies (we use pasture for all converted)",
            "Water class is a proxy (low treecover)",
            "No temporal MapBiomas available (only 2023)",
            "Real MapBiomas classification methodology is more sophisticated",
        ],
    }, indent=2))

    print(f"\n  Saved: {OUT_DIR}/yearly_land_cover.csv")
    print(f"  Saved: {OUT_DIR}/land_cover_changes.json")
    print(f"\n  KEY FINDINGS:")
    print(f"    Forest 2015 -> 2023: {yearly_stats[2015]['forest_pct']:.2f}% -> {yearly_stats[2023]['forest_pct']:.2f}% ({yearly_stats[2023]['forest_pct'] - yearly_stats[2015]['forest_pct']:+.2f}%)")
    print(f"    Pasture 2015 -> 2023: {yearly_stats[2015]['pasture_pct']:.2f}% -> {yearly_stats[2023]['pasture_pct']:.2f}% ({yearly_stats[2023]['pasture_pct'] - yearly_stats[2015]['pasture_pct']:+.2f}%)")


if __name__ == "__main__":
    main()