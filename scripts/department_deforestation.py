"""Per-department deforestation analysis using real Hansen GFC + Paraguay department GeoJSON.

Steps:
1. Load Hansen lossyear for both tiles
2. Load department GeoJSON (17 departments + Asunción)
3. Rasterize departments to match Hansen grid
4. For each department, count loss pixels 2001-2023
5. Compute % loss, km² loss, carbon loss per department
6. Generate bar chart of top-10 most-deforested departments
7. Compute Chaco vs Eastern breakdown

Outputs:
    outputs/p0011/departments/department_deforestation.json
    outputs/p0011/departments/department_deforestation.png
    outputs/p0011/departments/department_map.png
"""

import rasterio
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
import json
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))


OUT_DIR = REPO_ROOT / "outputs/p0011/departments"
OUT_DIR.mkdir(parents=True, exist_ok=True)

HANSEN_DIR = REPO_ROOT / "data/hansen"
BOUNDARIES_DIR = REPO_ROOT / "data/boundaries"
GEOJSON = BOUNDARIES_DIR / "pa_adm1.geojson"


def rasterize_departments(hansen_path, geojson_path):
    """Rasterize Paraguay departments to match Hansen grid."""
    import rasterio.features

    # Hansen metadata
    with rasterio.open(hansen_path) as src:
        h_crs = src.crs
        h_transform = src.transform
        h_shape = src.shape

    print(f"  Hansen: {h_shape}, CRS: {h_crs}")

    # Load departments
    gdf = gpd.read_file(str(geojson_path))
    print(f"  Loaded {len(gdf)} departments")
    if gdf.crs != h_crs:
        print(f"  Reprojecting departments to {h_crs}")
        gdf = gdf.to_crs(h_crs)

    # Get department IDs (use row index)
    dept_ids = gdf["shapeName"].tolist() if "shapeName" in gdf.columns else gdf["name"].tolist()
    print(f"  Departments: {dept_ids}")

    # Rasterize
    shapes = [(geom, i + 1) for i, geom in enumerate(gdf.geometry)]
    print("  Rasterizing (this takes a while for 40000x40000)...")
    t0 = time.time()
    dept_array = rasterio.features.rasterize(
        shapes=shapes,
        out_shape=h_shape,
        transform=h_transform,
        fill=0,
        dtype=np.uint16,
        all_touched=False,
    )
    print(f"  Done in {time.time()-t0:.1f}s")
    return dept_array, dept_ids


def compute_dept_stats(dept_array, lossyear, dept_ids):
    """For each department: total pixels, loss pixels (2001-2023), %, area, CO2e."""
    results = []
    pixel_area_ha = 0.0625  # Hansen 25m pixel
    mean_tc = 50.0  # Assume 50% treecover

    for i, dept in enumerate(dept_ids):
        dept_id = i + 1
        mask = dept_array == dept_id
        if not mask.any():
            continue
        total_pixels = int(mask.sum())
        loss_pixels = int((lossyear[mask] > 0).sum())
        loss_pct = 100 * loss_pixels / total_pixels if total_pixels > 0 else 0
        loss_ha = loss_pixels * pixel_area_ha
        loss_km2 = loss_ha / 100
        # Carbon: AGB = 100*tc^2/(100+tc^2), carbon = AGB * 0.47 * ha
        agb = 100 * mean_tc**2 / (100 + mean_tc**2)
        carbon_t = agb * 0.47 * loss_ha * 1000  # agb in Mg/ha, * loss_ha
        co2e_t = carbon_t * 44 / 12

        results.append(
            {
                "rank": 0,  # filled after sorting
                "department": dept,
                "total_pixels": total_pixels,
                "loss_pixels": loss_pixels,
                "loss_pct": float(loss_pct),
                "loss_ha": float(loss_ha),
                "loss_km2": float(loss_km2),
                "carbon_mt": float(carbon_t / 1e6),
                "co2e_mt": float(co2e_t / 1e6),
            }
        )

    # Sort by loss %
    results.sort(key=lambda x: x["loss_pct"], reverse=True)
    for i, r in enumerate(results):
        r["rank"] = i + 1
    return results


def plot_results(results, out_path):
    """Bar chart of loss % per department."""
    dept_names = [r["department"][:15] for r in results]
    loss_pcts = [r["loss_pct"] for r in results]
    co2es = [r["co2e_mt"] for r in results]

    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    ax = axes[0]
    colors = plt.cm.Reds(np.linspace(0.3, 0.9, len(dept_names)))
    ax.barh(dept_names[::-1], loss_pcts[::-1], color=colors[::-1])
    ax.set_xlabel("Forest loss 2001-2023 (%)")
    ax.set_title("Deforestation by Department (Hansen GFC)")
    ax.grid(True, alpha=0.3, axis="x")

    ax = axes[1]
    colors2 = plt.cm.Oranges(np.linspace(0.3, 0.9, len(dept_names)))
    ax.barh(dept_names[::-1], co2es[::-1], color=colors2[::-1])
    ax.set_xlabel("CO2e emissions (Mt)")
    ax.set_title("Carbon loss by Department (50% treecover assumption)")
    ax.grid(True, alpha=0.3, axis="x")

    plt.tight_layout()
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close()


def plot_map(dept_array, lossyear, dept_ids, results, out_path):
    """Visualize department-level loss on map."""
    fig, axes = plt.subplots(1, 2, figsize=(18, 7))

    # Sample 1/16 of the array for display speed
    step = 16
    dept_sample = dept_array[::step, ::step]
    loss_sample = (lossyear[::step, ::step] > 0).astype(np.uint8)

    # Map 1: departments
    ax = axes[0]
    cmap = plt.cm.tab20
    im = ax.imshow(dept_sample, cmap=cmap, vmin=0, vmax=len(dept_ids) + 1)
    ax.set_title("Paraguay Departments (rasterized)\n17 departments + Asunción")
    plt.colorbar(im, ax=ax, label="Department ID", shrink=0.5)

    # Map 2: deforestation intensity by department
    ax = axes[1]
    # Create per-pixel loss % map
    loss_pct_map = np.zeros_like(dept_array, dtype=np.float32)  # noqa: F841
    # Note: this is approximate (windowed histograms would be more accurate)
    ax.imshow(loss_sample, cmap="Reds", vmin=0, vmax=1, alpha=0.5)
    ax.imshow(dept_sample, cmap="Greys", vmin=0, vmax=len(dept_ids) + 1, alpha=0.3)
    ax.set_title("Deforestation distribution (red = loss)")

    plt.tight_layout()
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close()


def main():
    print("=" * 70)
    print("PARAGUAY DEFORESTATION BY DEPARTMENT (real Hansen + dept GeoJSON)")
    print("=" * 70)

    # Use tile 20S_060W (eastern Paraguay, all departments intersect)
    hansen_path = HANSEN_DIR / "hansen_lossyear_20S_060W.tif"
    if not hansen_path.exists():
        print(f"ERROR: {hansen_path} not found")
        return
    if not GEOJSON.exists():
        print(f"ERROR: {GEOJSON} not found")
        return

    # Load Hansen lossyear (small)
    print("\n[1/3] Loading Hansen lossyear...")
    with rasterio.open(hansen_path) as src:
        lossyear = src.read(1)
        print(f"  Shape: {lossyear.shape}, " f"loss pixels (2001-2023): {int((lossyear > 0).sum()):,}")

    # Rasterize departments
    print("\n[2/3] Rasterizing departments...")
    dept_array, dept_ids = rasterize_departments(hansen_path, GEOJSON)

    # Compute stats
    print("\n[3/3] Computing per-department statistics...")
    results = compute_dept_stats(dept_array, lossyear, dept_ids)

    # Print summary
    print(f"\n{'=' * 70}")
    print(f"{'Rank':>4}  {'Department':<20}  {'Loss %':>8}  {'Loss km²':>10}  {'CO2e Mt':>10}")
    print("-" * 70)
    for r in results:
        print(
            f"{r['rank']:>4}  {r['department']:<20}  "
            f"{r['loss_pct']:>7.2f}%  {r['loss_km2']:>10,.0f}  {r['co2e_mt']:>10.2f}"
        )

    # Top 3 most-deforested
    if len(results) >= 3:
        print("\nTop 3 most-deforested departments:")
        for r in results[:3]:
            print(
                f"  {r['rank']}. {r['department']}: "
                f"{r['loss_pct']:.1f}% loss, "
                f"{r['loss_km2']:.0f} km², "
                f"{r['co2e_mt']:.1f} MtCO2e"
            )

    # Save
    out_json = OUT_DIR / "department_deforestation.json"
    out_json.write_text(
        json.dumps(
            {
                "data_source": "Hansen GFC v1.11 + geoBoundaries Paraguay ADM1 simplified",
                "tiles_analyzed": ["20S_060W"],
                "n_departments": len(dept_ids),
                "departments": results,
                "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            },
            indent=2,
        )
    )

    # Plots
    plot_results(results, OUT_DIR / "department_deforestation.png")
    plot_map(dept_array, lossyear, dept_ids, results, OUT_DIR / "department_map.png")

    print(f"\n{'=' * 70}")
    print(f"  Results: {out_json}")
    print(f"  Figure: {OUT_DIR}/department_deforestation.png")
    print(f"  Map: {OUT_DIR}/department_map.png")


if __name__ == "__main__":
    main()
