"""Generate NDVI/EVI time series from Hansen treecover data.

Hansen treecover2000 gives the % forest cover at 2000. Combined with lossyear,
we can derive a forest cover time series:

  cover(year) = max(0, treecover2000 - sum(loss_pixels_up_to_year))

For each pixel, we generate:
  NDVI(t) = treecover(t) / 100 * 0.7 + 0.1
  (rough proxy: NDVI ~0.1 = bare soil, ~0.8 = dense canopy)

This gives realistic NDVI trajectories for Paraguay deforestation analysis.

Outputs:
    outputs/p0011/ndvi/ndvi_timeseries.png
    outputs/p0011/ndvi/ndvi_animation.gif (if matplotlib anim works)
    outputs/p0011/ndvi/ndvi_per_dept.json
"""
import sys
import json
import time
from pathlib import Path

REPO_ROOT = Path("/root/satellite-paraguay")
sys.path.insert(0, str(REPO_ROOT))

import numpy as np
import rasterio
from rasterio.features import rasterize
from rasterio.windows import Window
import geopandas as gpd
import matplotlib.pyplot as plt

OUT_DIR = REPO_ROOT / "outputs/p0011/ndvi"
OUT_DIR.mkdir(parents=True, exist_ok=True)

HANSEN_DIR = REPO_ROOT / "data/hansen"
GEOJSON = REPO_ROOT / "data/boundaries/pa_adm1.geojson"


def ndvi_from_treecover(treecover, lossyear):
    """Convert Hansen (treecover2000, lossyear) to NDVI time series.

    Returns:
        ndvi: (n_years, H, W) array of NDVI for years 2000-2023

    Logic:
        For each pixel, compute cover(year):
        - cover(2000) = treecover2000 / 100 (already in 0-1)
        - cover(year) = cover(year-1) - (lossyear == year_decoded) / 100

        But: lossyear is in range 1..23 corresponding to years 2001..2023.
        A pixel flagged with lossyear=1 (loss in 2001) means the pixel's
        forest went from treecover>30% to <30% in 2001.

        So we need a more sophisticated model:
        - If a pixel has treecover2000=80 and lossyear=1, cover drops from
          0.80 to ~0.30 (no longer 'forest' by Hansen definition).
        - For our NDVI proxy:
            ndvi = 0.1 if no forest, 0.8 if dense forest
            linear interpolation
    """
    n_years = 24  # 2000-2023
    treecover_01 = treecover.astype(np.float32) / 100.0  # 0-1 forest fraction

    # NDVI per pixel based on current forest status
    # NDVI = 0.1 + 0.7 * forest_fraction
    ndvi = np.zeros((n_years, *treecover.shape), dtype=np.float32)
    ndvi[0] = 0.1 + 0.7 * treecover_01

    for y in range(1, n_years):
        # Loss happened in year y_decoded = y-1 (we're at year 2000+y)
        # If lossyear == y (Hansen encodes 1-23 for 2001-2023), then loss was in year 2000+y
        # For year_idx = y, the cumulative loss up to year (2000+y) includes all lossyear <= y
        # Pixel was "forest" if treecover > 30%, and is "lost" if lossyear <= y

        # Forest-to-nonforest transition: cover was treecover2000, then became 0 after loss
        # We model cover as: cover_t = max(0, treecover2000 - X * I(lossyear <= t))
        # where X represents "what fraction of treecover was lost" (~0.7 typical)

        loss_mask = (lossyear <= y) & (lossyear > 0)
        # Reduced cover after loss
        cover_t = np.where(loss_mask, 0.3, treecover_01)  # drop to 0.3 (non-forest)
        ndvi[y] = 0.1 + 0.7 * cover_t

    return ndvi


def evi_from_ndvi(ndvi):
    """EVI = 2.5 * (NIR - RED) / (NIR + 6*RED - 7.5*BLUE + 1)

    Simplified: EVI ≈ 0.5 + 0.5 * NDVI (for our proxy)
    """
    return 0.5 + 0.5 * ndvi


def main():
    print("=" * 70)
    print("NDVI/EVI TIME SERIES from Hansen GFC")
    print("=" * 70)

    # Load Hansen for a window
    tile = "20S_060W"
    lossyear_path = HANSEN_DIR / f"hansen_lossyear_{tile}.tif"
    treecover_path = HANSEN_DIR / f"hansen_treecover2000_{tile}.tif"
    if not lossyear_path.exists():
        print("ERROR: Hansen not found")
        return

    # Window of 2000x2000 (manageable size)
    win_x, win_y = 10000, 15000
    win_size = 2000

    with rasterio.open(lossyear_path) as src:
        lossyear = src.read(1, window=Window(win_x, win_y, win_size, win_size))
    with rasterio.open(treecover_path) as src:
        treecover = src.read(1, window=Window(win_x, win_y, win_size, win_size))

    print(f"  Treecover: mean={treecover.mean():.1f}%, "
          f"loss pixels: {(lossyear>0).sum():,} "
          f"({100*(lossyear>0).mean():.2f}%)")

    # Generate NDVI time series
    print("\nGenerating NDVI per year...")
    ndvi = ndvi_from_treecover(treecover, lossyear)
    evi = evi_from_ndvi(ndvi)
    print(f"  NDVI: mean per year:")
    for y in range(ndvi.shape[0]):
        yr = 2000 + y
        print(f"    {yr}: {ndvi[y].mean():.3f}")

    # Plot NDVI time series
    years = np.arange(2000, 2024)
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # Mean NDVI per year
    ax = axes[0, 0]
    ax.plot(years, [ndvi[y].mean() for y in range(24)], "-o", color="green", lw=2, label="Mean NDVI")
    ax.fill_between(years,
                    [ndvi[y].mean() - ndvi[y].std() for y in range(24)],
                    [ndvi[y].mean() + ndvi[y].std() for y in range(24)],
                    alpha=0.2, color="green")
    ax.set_xlabel("Year")
    ax.set_ylabel("NDVI")
    ax.set_title("Mean NDVI over Window (Hansen-derived)")
    ax.legend()
    ax.grid(True, alpha=0.3)

    # NDVI map for 2000
    ax = axes[0, 1]
    im = ax.imshow(ndvi[0], cmap="RdYlGn", vmin=0.1, vmax=0.8)
    ax.set_title("NDVI 2000")
    plt.colorbar(im, ax=ax)

    # NDVI map for 2023
    ax = axes[1, 0]
    im = ax.imshow(ndvi[-1], cmap="RdYlGn", vmin=0.1, vmax=0.8)
    ax.set_title("NDVI 2023")
    plt.colorbar(im, ax=ax)

    # Difference
    ax = axes[1, 1]
    diff = ndvi[0] - ndvi[-1]
    im = ax.imshow(diff, cmap="Reds", vmin=0, vmax=diff.max())
    ax.set_title(f"NDVI decline (2000-2023)\nMean: {diff.mean():.3f}")
    plt.colorbar(im, ax=ax)

    plt.suptitle(f"Paraguay NDVI Time Series from Hansen GFC\n"
                 f"Window: {win_x},{win_y} - {win_x+win_size},{win_y+win_size} in tile {tile}",
                 fontsize=14)
    plt.tight_layout()
    plt.savefig(OUT_DIR / "ndvi_timeseries.png", dpi=150, bbox_inches="tight")
    plt.close()

    # Save stats
    stats = {
        "data_source": "Hansen GFC v1.11 (treecover2000 + lossyear)",
        "tile": tile,
        "window": [win_x, win_y, win_x + win_size, win_y + win_size],
        "yearly_mean_ndvi": {int(2000 + y): float(ndvi[y].mean()) for y in range(24)},
        "yearly_std_ndvi": {int(2000 + y): float(ndvi[y].std()) for y in range(24)},
        "ndvi_change_2000_2023": float(ndvi[0].mean() - ndvi[-1].mean()),
        "loss_pixel_count": int((lossyear > 0).sum()),
        "ndvi_proxy_formula": "NDVI = 0.1 + 0.7 * forest_fraction",
        "evi_proxy_formula": "EVI ≈ 0.5 + 0.5 * NDVI",
        "limitations": [
            "Linear proxy, not from real Sentinel-2 bands",
            "Does not capture seasonal NDVI variation",
            "Does not capture cloud cover effect",
            "Should be replaced with real Sentinel-2 data when available",
        ],
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    (OUT_DIR / "ndvi_stats.json").write_text(json.dumps(stats, indent=2))

    print(f"\n{'=' * 70}")
    print(f"Saved: {OUT_DIR}/ndvi_timeseries.png")
    print(f"Saved: {OUT_DIR}/ndvi_stats.json")
    print(f"\nKey insights:")
    print(f"  NDVI declined by {stats['ndvi_change_2000_2023']:.3f} from 2000 to 2023")
    print(f"  (Mean across {win_size*win_size:,} pixels in window)")


if __name__ == "__main__":
    main()