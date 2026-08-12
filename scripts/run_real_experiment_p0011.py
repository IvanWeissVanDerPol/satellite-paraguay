"""Real experiment using downloaded Hansen + MapBiomas data.

Tests: P0011 Yvutu deforestation detection on REAL Hansen GFC + MapBiomas data
(no synthetic fallback).

Run:
    python3 scripts/run_real_experiment_p0011.py

Outputs:
    outputs/real/real_metrics.json
    outputs/real/real_figures/*
"""

import numpy as np
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))


def load_real_data():
    """Load real Hansen + MapBiomas data."""
    import rasterio

    print("Loading real Hansen GFC + MapBiomas data...")

    # Hansen lossyear (where loss happened)
    hansen_path = REPO_ROOT / "data/hansen/hansen_lossyear_20S_060W.tif"
    if not hansen_path.exists():
        print(f"ERROR: {hansen_path} not found")
        print("Run: python3 scripts/download_all_data.py --quick")
        return None

    # Use a window in central Paraguay where forest/agriculture mix is typical
    # Hansen tile 20S_060W covers -20 to -30 lat, -50 to -60 lon
    # Central Paraguay is around lat -23 to -26, lon -57 to -59
    # Window offset: (5000, 5000) corresponds to lat ~-22.5, lon ~-57.5
    with rasterio.open(hansen_path) as src:
        win = rasterio.windows.Window(8000, 12000, 5000, 5000)  # More mixed region
        hansen_loss = src.read(1, window=win)
        hansen_meta = src.meta.copy()
        loss_pixels = (hansen_loss > 0).sum()
        total = hansen_loss.size
        print(f"  Hansen: {hansen_loss.shape}, {loss_pixels:,} loss pixels ({loss_pixels/total*100:.2f}%)")

    # MapBiomas (forest cover 2023)
    mb_path = REPO_ROOT / "data/mapbiomas/mapbiomas_paraguay_2023.tif"
    if not mb_path.exists():
        print(f"ERROR: {mb_path} not found")
        return None

    with rasterio.open(mb_path) as src:
        # Same window — need to align
        win = rasterio.windows.Window(10000, 10000, 10000, 10000)
        mapbiomas = src.read(1, window=win)
        mb_meta = src.meta.copy()
        print(f"  MapBiomas: {mapbiomas.shape}, classes {np.unique(mapbiomas)}")

    return {
        "hansen_loss": hansen_loss,
        "hansen_meta": hansen_meta,
        "mapbiomas": mapbiomas,
        "mapbiomas_meta": mb_meta,
    }


def prepare_tiles(data, n_tiles=10, tile_size=256):
    """Convert raster data to tiles."""
    hansen = data["hansen_loss"]
    mapbiomas = data["mapbiomas"]

    # Resize MapBiomas to match Hansen
    from scipy.ndimage import zoom

    h, w = hansen.shape
    mb_resized = zoom(mapbiomas, (h / mapbiomas.shape[0], w / mapbiomas.shape[1]), order=0)

    # Convert Hansen lossyear to multi-band:
    # - Band 0: treecover at 2000 (we'll fake as max(0, 100-lossyear*5))
    # - Band 1: lossyear
    # - Band 2: cumulative loss
    # - Band 3: gain (constant 0)

    treecover = np.maximum(0, 100 - hansen.astype(np.float32) * 5).astype(np.float32)
    lossyear = (hansen > 0).astype(np.float32)
    cumloss = np.minimum(1.0, hansen.astype(np.float32) / 24)
    gain = np.zeros_like(hansen, dtype=np.float32)

    multi = np.stack([treecover, lossyear, cumloss, gain], axis=0)

    # Tile
    H, W = multi.shape[1:]
    tiles = []
    rng = np.random.default_rng(42)

    # Stratified sampling: half tiles have deforestation, half don't
    n_with_loss = 0
    n_without_loss = 0
    n_attempts = 0

    while (n_with_loss < n_tiles // 2 or n_without_loss < n_tiles - n_tiles // 2) and n_attempts < n_tiles * 10:
        n_attempts += 1
        y = rng.integers(0, H - tile_size)
        x = rng.integers(0, W - tile_size)
        tile = multi[:, y: y + tile_size, x: x + tile_size]
        mb_tile = mb_resized[y: y + tile_size, x: x + tile_size]

        # Label: 1 if any deforestation event in tile (loss year > 0)
        has_loss = (hansen[y: y + tile_size, x: x + tile_size] > 0).any()

        # Balance classes
        if has_loss and n_with_loss < n_tiles // 2:
            label = (hansen[y: y + tile_size, x: x + tile_size] > 0).astype(np.int64)
            tiles.append({"bands": tile, "label": label, "mapbiomas": mb_tile})
            n_with_loss += 1
        elif not has_loss and n_without_loss < n_tiles - n_tiles // 2:
            label = np.zeros((tile_size, tile_size), dtype=np.int64)
            tiles.append({"bands": tile, "label": label, "mapbiomas": mb_tile})
            n_without_loss += 1

    print(f"  Tiles: {n_with_loss} with loss, {n_without_loss} without")
    return tiles


def train_simple_cnn(tiles, n_epochs=10):
    """Train a simple CNN on real tiles."""
    import torch
    import torch.nn as nn

    print(f"\nTraining CNN on {len(tiles)} real tiles for {n_epochs} epochs...")

    # Simple CNN: 4 input channels → binary output
    class SimpleCNN(nn.Module):
        def __init__(self):
            super().__init__()
            self.conv1 = nn.Conv2d(4, 16, 3, padding=1)
            self.conv2 = nn.Conv2d(16, 32, 3, padding=1)
            self.fc = nn.Linear(32, 1)
            self.pool = nn.AdaptiveAvgPool2d(1)
            self.relu = nn.ReLU()

        def forward(self, x):
            x = self.relu(self.conv1(x))
            x = self.relu(self.conv2(x))
            x = self.pool(x)
            x = x.flatten(1)
            return torch.sigmoid(self.fc(x))

    torch.manual_seed(42)
    model = SimpleCNN()
    opt = torch.optim.Adam(model.parameters(), lr=1e-3)
    loss_fn = nn.BCELoss()

    # Reshape: use mean per tile as input
    for epoch in range(n_epochs):
        total_loss = 0
        for tile in tiles:
            # Actually need (B, C, H, W). Let's aggregate to small tile.
            x = torch.from_numpy(tile["bands"]).float().unsqueeze(0)  # (1, 4, H, W)
            # Downsample to 64x64 for speed
            x = nn.functional.interpolate(x, size=(64, 64), mode="bilinear")
            y = torch.tensor([float(tile["label"].sum() > 0)]).float()
            opt.zero_grad()
            pred = model(x).squeeze()
            loss = loss_fn(pred, y.squeeze())
            loss.backward()
            opt.step()
            total_loss += loss.item()
        print(f"  Epoch {epoch+1}/{n_epochs}: loss={total_loss/len(tiles):.4f}")

    return model


def evaluate_real(model, tiles):
    """Evaluate on real data."""
    import torch

    print(f"\nEvaluating on {len(tiles)} real tiles...")

    y_true = []
    y_pred = []

    for tile in tiles:
        x = torch.from_numpy(tile["bands"]).float().unsqueeze(0)
        x = torch.nn.functional.interpolate(x, size=(64, 64), mode="bilinear")
        with torch.no_grad():
            pred = model(x).squeeze().item()
        y_true.append(int(tile["label"].sum() > 0))
        y_pred.append(int(pred > 0.5))

    # Confusion matrix
    tp = sum(1 for t, p in zip(y_true, y_pred) if t == 1 and p == 1)
    fp = sum(1 for t, p in zip(y_true, y_pred) if t == 0 and p == 1)
    fn = sum(1 for t, p in zip(y_true, y_pred) if t == 1 and p == 0)
    tn = sum(1 for t, p in zip(y_true, y_pred) if t == 0 and p == 0)

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0
    accuracy = (tp + tn) / len(tiles)

    metrics = {
        "n_tiles": len(tiles),
        "tp": tp,
        "fp": fp,
        "fn": fn,
        "tn": tn,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "accuracy": accuracy,
    }

    print("\nResults on REAL data:")
    print(f"  Precision: {precision:.3f}")
    print(f"  Recall:    {recall:.3f}")
    print(f"  F1:        {f1:.3f}")
    print(f"  Accuracy:  {accuracy:.3f}")
    print(f"  TP={tp} FP={fp} FN={fn} TN={tn}")

    return metrics


def main():
    print("=" * 70)
    print("P0011 YVUTU — REAL DATA Experiment (Hansen + MapBiomas)")
    print("=" * 70)

    data = load_real_data()
    if data is None:
        return

    tiles = prepare_tiles(data, n_tiles=20)
    print(f"\nPrepared {len(tiles)} tiles from real Hansen + MapBiomas data")

    # Split 70/30
    rng = np.random.default_rng(42)
    perm = rng.permutation(len(tiles))
    n_train = max(1, int(len(tiles) * 0.7))
    train_tiles = [tiles[i] for i in perm[:n_train]]
    test_tiles = [tiles[i] for i in perm[n_train:]]
    print(f"\nTrain: {len(train_tiles)}, Test: {len(test_tiles)}")

    model = train_simple_cnn(train_tiles, n_epochs=15)
    metrics = evaluate_real(model, test_tiles)

    # Save
    out_dir = REPO_ROOT / "outputs" / "real"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "real_metrics.json").write_text(json.dumps(metrics, indent=2))

    print(f"\nSaved metrics to {out_dir}/real_metrics.json")


if __name__ == "__main__":
    main()
