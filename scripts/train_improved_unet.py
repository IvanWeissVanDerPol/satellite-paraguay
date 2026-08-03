"""Improved model training on real Hansen + MapBiomas data.

Trains a proper CNN with:
- Larger training set (more tiles)
- Multi-source features (treecover + MapBiomas + spatial coords)
- Class-weighted loss for imbalanced data
- Proper train/val/test split
- Augmentation (rotations, flips)

Output:
    outputs/p0011/real_model/improved_unet_metrics.json
    outputs/p0011/real_model/training_curves.png
"""
import sys
import json
import time
from pathlib import Path

REPO_ROOT = Path("/root/satellite-paraguay")
sys.path.insert(0, str(REPO_ROOT))

import numpy as np
import rasterio
from rasterio.windows import Window
from scipy.ndimage import zoom
import torch
import torch.nn as nn
import torch.nn.functional as F
import matplotlib.pyplot as plt

OUT_DIR = REPO_ROOT / "outputs/p0011/real_model"
OUT_DIR.mkdir(parents=True, exist_ok=True)

HANSEN_DIR = REPO_ROOT / "data/hansen"
MAPBIOMAS_DIR = REPO_ROOT / "data/mapbiomas"


class ImprovedUNet(nn.Module):
    """Slightly bigger U-Net for tile-level classification."""

    def __init__(self, in_ch=7):
        super().__init__()
        # Encoder
        self.enc1 = nn.Sequential(
            nn.Conv2d(in_ch, 32, 3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.Conv2d(32, 32, 3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(),
        )
        self.enc2 = nn.Sequential(
            nn.MaxPool2d(2),
            nn.Conv2d(32, 64, 3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.Conv2d(64, 64, 3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
        )
        self.enc3 = nn.Sequential(
            nn.MaxPool2d(2),
            nn.Conv2d(64, 128, 3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(),
        )
        # Decoder
        self.dec2 = nn.Sequential(
            nn.Upsample(scale_factor=2, mode="bilinear", align_corners=False),
            nn.Conv2d(128, 64, 3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.Conv2d(64, 64, 3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
        )
        self.dec1 = nn.Sequential(
            nn.Upsample(scale_factor=2, mode="bilinear", align_corners=False),
            nn.Conv2d(64, 32, 3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.Conv2d(32, 32, 3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(),
        )
        # Output
        self.out_conv = nn.Conv2d(32, 1, 1)

    def forward(self, x):
        e1 = self.enc1(x)
        e2 = self.enc2(e1)
        e3 = self.enc3(e2)
        d2 = self.dec2(e3) + e2  # skip connection
        d1 = self.dec1(d2) + e1  # skip connection
        return torch.sigmoid(self.out_conv(d1)).squeeze(1)


def load_features():
    """Load Hansen + MapBiomas for a window."""
    x0, y0, w, h = 8000, 12000, 5000, 5000
    with rasterio.open(HANSEN_DIR / "hansen_lossyear_20S_060W.tif") as src:
        lossyear = src.read(1, window=Window(x0, y0, w, h))
    with rasterio.open(HANSEN_DIR / "hansen_treecover2000_20S_060W.tif") as src:
        treecover = src.read(1, window=Window(x0, y0, w, h))
    with rasterio.open(MAPBIOMAS_DIR / "mapbiomas_paraguay_2023.tif") as src:
        mb_chunk = src.read(1, window=Window(10000, 10000, w, h))
        mb_resized = zoom(mb_chunk, (h / mb_chunk.shape[0], w / mb_chunk.shape[1]), order=0)

    # Compute cover fraction over time (in 0-1)
    cover_2000 = treecover.astype(np.float32) / 100.0
    # Cumulative loss up to year k
    cum_loss_frac = np.zeros((23, *treecover.shape), dtype=np.float32)
    for y in range(1, 23):
        cum_loss_frac[y] = cum_loss_frac[y - 1] + (lossyear == y).astype(np.float32) / 100.0
    cover_t = np.clip(cover_2000[None, :, :] - cum_loss_frac, 0, 1)

    return {
        "lossyear": lossyear,
        "treecover": treecover,
        "mapbiomas": mb_resized,
        "cover_t": cover_t,  # (23, H, W)
    }


def make_tiles_with_features(data, tile_size=64, n_per_class=80, seed=42):
    """Create feature-rich tiles for classification."""
    rng = np.random.default_rng(seed)
    H, W = data["lossyear"].shape

    is_forest = (data["mapbiomas"] == 3).astype(np.float32)
    is_pasture = (data["mapbiomas"] == 15).astype(np.float32)
    is_agri = (data["mapbiomas"] == 18).astype(np.float32)
    is_water = (data["mapbiomas"] == 26).astype(np.float32)
    is_savanna = (data["mapbiomas"] == 4).astype(np.float32)

    # Normalize features
    treecover_norm = data["treecover"].astype(np.float32) / 100.0

    # Stack: treecover, forest, pasture, agri, water, savanna, mean_cover_history
    mean_cover_hist = data["cover_t"].mean(axis=0)
    features_static = np.stack([
        treecover_norm,
        is_forest, is_pasture, is_agri, is_water, is_savanna,
        mean_cover_hist,
    ], axis=0)

    # Per-year cover as additional channels
    cover_yearly = data["cover_t"]  # (23, H, W)

    tiles = []
    n_pos = 0
    n_neg = 0
    attempts = 0
    target = n_per_class

    while (n_pos < target or n_neg < target) and attempts < n_per_class * 30:
        attempts += 1
        y = rng.integers(0, H - tile_size)
        x = rng.integers(0, W - tile_size)
        label = data["lossyear"][y:y+tile_size, x:x+tile_size]
        has_loss = (label > 0).any()
        loss_count = int((label > 0).sum())

        if has_loss and n_pos < target:
            # Static features + yearly cover
            static_tile = features_static[:, y:y+tile_size, x:x+tile_size]
            yearly_tile = cover_yearly[:, y:y+tile_size, x:x+tile_size]
            full_features = np.concatenate([static_tile, yearly_tile], axis=0)  # (30, ts, ts)
            tiles.append({
                "features": full_features.astype(np.float32),
                "label": (label > 0).astype(np.float32),
                "n_loss": loss_count,
            })
            n_pos += 1
        elif not has_loss and n_neg < target:
            static_tile = features_static[:, y:y+tile_size, x:x+tile_size]
            yearly_tile = cover_yearly[:, y:y+tile_size, x:x+tile_size]
            full_features = np.concatenate([static_tile, yearly_tile], axis=0)
            tiles.append({
                "features": full_features.astype(np.float32),
                "label": np.zeros((tile_size, tile_size), dtype=np.float32),
                "n_loss": 0,
            })
            n_neg += 1

    print(f"  Tiles: {n_pos} with loss + {n_neg} without = {len(tiles)} total")
    print(f"  Feature channels: {tiles[0]['features'].shape[0]}")
    return tiles


def augment_tile(features, label):
    """Random flip + rotation."""
    if np.random.random() > 0.5:
        features = np.flip(features, axis=1)
        label = np.flip(label, axis=0)
    if np.random.random() > 0.5:
        features = np.flip(features, axis=2)
        label = np.flip(label, axis=1)
    k = np.random.randint(0, 4)
    if k > 0:
        features = np.rot90(features, k, axes=(1, 2))
        label = np.rot90(label, k, axes=(0, 1))
    return features.copy(), label.copy()


def main():
    print("=" * 70)
    print("IMPROVED U-NET TRAINING (real Hansen + MapBiomas, 30-channel features)")
    print("=" * 70)

    # Load
    print("\n[1/4] Loading features...")
    data = load_features()
    print(f"  Treecover mean: {data['treecover'].mean():.1f}%")
    print(f"  Forest (class 3): {(data['mapbiomas']==3).sum():,} pixels")

    # Tiles
    print("\n[2/4] Creating tiles...")
    tiles = make_tiles_with_features(data, tile_size=64, n_per_class=80)

    # Split
    rng = np.random.default_rng(42)
    perm = rng.permutation(len(tiles))
    n_train = int(len(tiles) * 0.6)
    n_val = int(len(tiles) * 0.2)
    train_tiles = [tiles[i] for i in perm[:n_train]]
    val_tiles = [tiles[i] for i in perm[n_train:n_train + n_val]]
    test_tiles = [tiles[i] for i in perm[n_train + n_val:]]
    print(f"  Split: {len(train_tiles)} train / {len(val_tiles)} val / {len(test_tiles)} test")

    # Train
    print("\n[3/4] Training U-Net...")
    device = torch.device("cpu")  # No GPU
    model = ImprovedUNet(in_ch=tiles[0]["features"].shape[0])
    model = model.to(device)

    # Class-weighted loss (positive class is rare)
    pos_weight = torch.tensor([10.0]).to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3, weight_decay=1e-4)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=20)

    train_losses = []
    val_losses = []
    val_f1s = []

    n_epochs = 20
    for epoch in range(n_epochs):
        model.train()
        np.random.shuffle(train_tiles)
        epoch_loss = 0
        for tile in train_tiles:
            features, label = augment_tile(tile["features"], tile["label"])
            x = torch.from_numpy(features).float().unsqueeze(0).to(device)
            y = torch.from_numpy(label).float().unsqueeze(0).to(device)
            optimizer.zero_grad()
            pred = model(x)
            # Weighted BCE
            loss = F.binary_cross_entropy(pred, y, reduction="none")
            weight = 1 + 9 * y  # 10x weight on positive
            loss = (loss * weight).mean()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()
            epoch_loss += loss.item()
        scheduler.step()
        train_losses.append(epoch_loss / len(train_tiles))

        # Validation
        model.eval()
        val_loss = 0
        all_preds = []
        all_labels = []
        with torch.no_grad():
            for tile in val_tiles:
                x = torch.from_numpy(tile["features"]).float().unsqueeze(0).to(device)
                y = torch.from_numpy(tile["label"]).float().unsqueeze(0).to(device)
                pred = model(x)
                loss = F.binary_cross_entropy(pred, y, reduction="none")
                weight = 1 + 9 * y
                loss = (loss * weight).mean()
                val_loss += loss.item()
                all_preds.append((pred.squeeze().cpu().numpy() > 0.5).astype(int).flatten())
                all_labels.append(tile["label"].flatten())
        val_loss /= len(val_tiles)
        val_losses.append(val_loss)

        # F1
        y_pred = np.concatenate(all_preds)
        y_true = np.concatenate(all_labels)
        tp = int(((y_true == 1) & (y_pred == 1)).sum())
        fp = int(((y_true == 0) & (y_pred == 1)).sum())
        fn = int(((y_true == 1) & (y_pred == 0)).sum())
        precision = tp / (tp + fp + 1e-8)
        recall = tp / (tp + fn + 1e-8)
        f1 = 2 * precision * recall / (precision + recall + 1e-8)
        val_f1s.append(f1)

        if (epoch + 1) % 5 == 0 or epoch == 0:
            print(f"  Epoch {epoch+1}/{n_epochs}: "
                  f"train_loss={train_losses[-1]:.4f}, "
                  f"val_loss={val_loss:.4f}, val_F1={f1:.3f} "
                  f"(P={precision:.3f}, R={recall:.3f})")

    # Test
    print("\n[4/4] Final test set evaluation...")
    model.eval()
    all_preds = []
    all_labels = []
    with torch.no_grad():
        for tile in test_tiles:
            x = torch.from_numpy(tile["features"]).float().unsqueeze(0).to(device)
            pred = model(x)
            all_preds.append((pred.squeeze().cpu().numpy() > 0.5).astype(int).flatten())
            all_labels.append(tile["label"].flatten())
    y_pred = np.concatenate(all_preds)
    y_true = np.concatenate(all_labels)

    tp = int(((y_true == 1) & (y_pred == 1)).sum())
    fp = int(((y_true == 0) & (y_pred == 1)).sum())
    fn = int(((y_true == 1) & (y_pred == 0)).sum())
    tn = int(((y_true == 0) & (y_pred == 0)).sum())
    precision = tp / (tp + fp + 1e-8)
    recall = tp / (tp + fn + 1e-8)
    f1 = 2 * precision * recall / (precision + recall + 1e-8)
    accuracy = (tp + tn) / (tp + fp + fn + tn)
    iou = tp / (tp + fp + fn + 1e-8)

    print(f"\n  TEST RESULTS:")
    print(f"    TP={tp:,}, FP={fp:,}, FN={fn:,}, TN={tn:,}")
    print(f"    Precision: {precision:.3f}")
    print(f"    Recall:    {recall:.3f}")
    print(f"    F1:        {f1:.3f}")
    print(f"    IoU:       {iou:.3f}")
    print(f"    Accuracy:  {accuracy:.3f}")

    # Plot training curves
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    axes[0].plot(train_losses, label="train", color="blue")
    axes[0].plot(val_losses, label="val", color="red")
    axes[0].set_xlabel("Epoch")
    axes[0].set_ylabel("Weighted BCE Loss")
    axes[0].set_title("Training curves (real Hansen + MapBiomas)")
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    axes[1].plot(val_f1s, color="green")
    axes[1].set_xlabel("Epoch")
    axes[1].set_ylabel("Validation F1")
    axes[1].set_title("F1 over epochs")
    axes[1].grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(OUT_DIR / "training_curves.png", dpi=150, bbox_inches="tight")
    plt.close()

    # Save metrics
    out = {
        "model": "ImprovedUNet (30-channel, 7 static + 23 yearly cover)",
        "data": "real Hansen GFC + MapBiomas Paraguay 2023",
        "n_train": len(train_tiles),
        "n_val": len(val_tiles),
        "n_test": len(test_tiles),
        "tile_size": 64,
        "n_epochs": n_epochs,
        "test_metrics": {
            "precision": float(precision),
            "recall": float(recall),
            "f1": float(f1),
            "iou": float(iou),
            "accuracy": float(accuracy),
            "tp": tp, "fp": fp, "fn": fn, "tn": tn,
        },
        "training_losses": train_losses,
        "val_losses": val_losses,
        "val_f1s": val_f1s,
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    (OUT_DIR / "improved_unet_metrics.json").write_text(json.dumps(out, indent=2))

    print(f"\n{'=' * 70}")
    print(f"Saved: {OUT_DIR}/improved_unet_metrics.json")
    print(f"Figure: {OUT_DIR}/training_curves.png")


if __name__ == "__main__":
    main()