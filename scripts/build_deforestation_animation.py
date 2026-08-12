"""Build animated GIF showing forest loss progression 2001-2023 in Paraguay.

Uses Hansen lossyear to create 23 frames of deforestation, one per year.
Each frame shows pixels lost up to that year as red, stable forest as green,
non-forest as grey.

Output:
    outputs/p0011/figures/deforestation_timeline.gif
"""

from rasterio.windows import Window
import rasterio
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))


OUT_DIR = REPO_ROOT / "outputs/p0011/figures"
OUT_DIR.mkdir(parents=True, exist_ok=True)

HANSEN_DIR = REPO_ROOT / "data/hansen"


def main():
    print("=" * 70)
    print("DEFORESTATION TIMELINE ANIMATION (Hansen GFC v1.11)")
    print("=" * 70)

    # Load Hansen for a window showing clear deforestation
    tile = "20S_060W"
    lossyear_path = HANSEN_DIR / f"hansen_lossyear_{tile}.tif"
    treecover_path = HANSEN_DIR / f"hansen_treecover2000_{tile}.tif"

    # Window: 2000x2000, find one with clear deforestation
    # We know tile 20S_060W has lots of loss, use central Paraguay
    win_x, win_y = 8000, 13000
    win_size = 1500

    with rasterio.open(lossyear_path) as src:
        lossyear = src.read(1, window=Window(win_x, win_y, win_size, win_size))
    with rasterio.open(treecover_path) as src:
        treecover = src.read(1, window=Window(win_x, win_y, win_size, win_size))

    print(f"  Window: {win_x}-{win_x+win_size}, {win_y}-{win_y+win_size}")
    print(f"  Loss pixels: {(lossyear > 0).sum():,} " f"({100*(lossyear>0).mean():.2f}%)")

    # Create figure
    fig, ax = plt.subplots(figsize=(8, 8))

    # Initial frame (year 2000): all green (forest) where treecover > 30, else grey
    initial_state = np.where(
        treecover > 30,
        2,  # green
        0,  # grey
    ).astype(np.uint8)

    # RGB image
    rgb = np.zeros((win_size, win_size, 3), dtype=np.float32)
    rgb[initial_state == 2] = [0.18, 0.55, 0.34]  # forest green
    rgb[initial_state == 0] = [0.6, 0.6, 0.55]  # non-forest grey

    im = ax.imshow(rgb)
    ax.set_title(
        "Paraguay Deforestation 2001-2023\n"
        f"Window {win_x}-{win_x+win_size}, {win_y}-{win_y+win_size}\n"
        "Green = Forest, Red = Deforested, Grey = Non-forest"
    )
    ax.axis("off")
    txt = ax.text(
        0.02,
        0.98,
        "Year: 2000",
        transform=ax.transAxes,
        fontsize=14,
        fontweight="bold",
        va="top",
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.8),
    )

    def update(frame_idx):
        """Update to year 2001 + frame_idx."""
        year = 2001 + frame_idx
        # Current state
        current_state = np.where(
            treecover > 30,
            2,  # green
            0,  # grey
        ).astype(np.uint8)
        # Mark pixels with lossyear <= year as lost
        lost_mask = (lossyear > 0) & (lossyear <= (year - 2000))
        current_state[lost_mask] = 1  # red

        rgb = np.zeros((win_size, win_size, 3), dtype=np.float32)
        rgb[current_state == 2] = [0.18, 0.55, 0.34]  # forest green
        rgb[current_state == 1] = [0.85, 0.20, 0.10]  # deforestation red
        rgb[current_state == 0] = [0.6, 0.6, 0.55]  # non-forest grey

        im.set_array(rgb)
        txt.set_text(f"Year: {year}\n" f"Loss: {lost_mask.sum():,} pixels " f"({100*lost_mask.sum()/win_size**2:.2f}%)")
        return im, txt

    anim = animation.FuncAnimation(fig, update, frames=23, interval=300, blit=False)

    out_gif = OUT_DIR / "deforestation_timeline.gif"
    print(f"\nSaving animation to {out_gif}...")
    anim.save(str(out_gif), writer="pillow", fps=3, dpi=80)
    plt.close()

    print(f"\n✓ Saved: {out_gif}")
    print("  23 frames, one per year (2001-2023)")
    print("  Forest → red as pixels are lost")


if __name__ == "__main__":
    main()
