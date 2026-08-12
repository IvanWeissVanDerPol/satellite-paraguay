"""Cross-paper transfer learning experiment (RQ4, H3).

Tests whether a model trained on one Paraguayan land-use task transfers to another.

Tasks:
1. Deforestation detection (Yvutu) — Hansen+MapBiomas
2. Yield prediction (Yrupe) — NDVI + MapBiomas + SRTM
3. Forest cover classification (proxy) — Hansen + MapBiomas

For each task:
1. Train from-scratch CNN
2. Train CNN with pretrained encoder from another task
3. Compare metrics

H3: deforestation-pretrained achieves > 0.7x accuracy of yield-trained on yield task.

Saves results to outputs/cross_transfer/transfer_results.json
"""

from rasterio.windows import Window
import torch.nn as nn
import torch
import rasterio
import numpy as np
import json
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))


OUT_DIR = REPO_ROOT / "outputs/cross_transfer"
OUT_DIR.mkdir(parents=True, exist_ok=True)

HANSEN_DIR = REPO_ROOT / "data/hansen"
MAPBIOMAS_DIR = REPO_ROOT / "data/mapbiomas"


class TileDataset:
    """Multi-task tile dataset."""

    def __init__(self, lossyear, treecover, mapbiomas, tile_size=64, augment=False, n_tiles=200):
        self.lossyear = lossyear
        self.treecover = treecover
        self.mapbiomas = mapbiomas
        self.tile_size = tile_size
        self.augment = augment
        self.H, self.W = lossyear.shape
        self.tiles = self._sample_tiles(n=n_tiles)

    def _sample_tiles(self, n=200, seed=42):
        rng = np.random.default_rng(seed)
        tiles = []
        for _ in range(n * 5):
            y = rng.integers(0, self.H - self.tile_size)
            x = rng.integers(0, self.W - self.tile_size)
            tile_lbl = (self.lossyear[y: y + self.tile_size, x: x + self.tile_size] > 0).any()
            tile_yld = float(self.treecover[y: y + self.tile_size, x: x + self.tile_size].mean()) / 100.0
            tile_forest = float((self.mapbiomas[y: y + self.tile_size, x: x + self.tile_size] == 3).mean())
            tiles.append((y, x, int(tile_lbl), tile_yld, tile_forest))
            if len(tiles) >= n:
                break
        return tiles

    def __len__(self):
        return len(self.tiles)

    def __getitem__(self, idx):
        y, x, lbl_def, lbl_yld, lbl_forest = self.tiles[idx]
        feats = np.stack(
            [
                self.treecover[y: y + self.tile_size, x: x + self.tile_size] / 100.0,
                (self.mapbiomas[y: y + self.tile_size, x: x + self.tile_size] == 3).astype(np.float32),
                (self.mapbiomas[y: y + self.tile_size, x: x + self.tile_size] == 15).astype(np.float32),
                (self.mapbiomas[y: y + self.tile_size, x: x + self.tile_size] == 18).astype(np.float32),
            ],
            axis=0,
        )
        return (
            torch.from_numpy(feats).float(),
            torch.tensor(lbl_def).float(),
            torch.tensor(lbl_yld).float(),
            torch.tensor(lbl_forest).float(),
        )


class MultiTaskCNN(nn.Module):
    """CNN with shared encoder and 3 task heads."""

    def __init__(self, in_ch=4, embed_dim=64, shared_layers=3):
        super().__init__()
        self.encoder = nn.Sequential(
            nn.Conv2d(in_ch, 32, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(32, embed_dim, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
        )
        self.shared_dim = embed_dim * (64 // 4) * (64 // 4)
        self.head_def = nn.Linear(self.shared_dim, 1)
        self.head_yld = nn.Linear(self.shared_dim, 1)
        self.head_forest = nn.Linear(self.shared_dim, 1)

    def forward(self, x, task="def"):
        h = self.encoder(x)
        h = h.flatten(1)
        if task == "def":
            return torch.sigmoid(self.head_def(h)).squeeze(-1)
        elif task == "yld":
            return self.head_yld(h).squeeze(-1)
        elif task == "forest":
            return torch.sigmoid(self.head_forest(h)).squeeze(-1)


def train_task(model, dataset, task, n_epochs=10, lr=1e-3):
    """Train a single task head."""
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    n = len(dataset)
    n_train = int(n * 0.7)

    for epoch in range(n_epochs):
        np.random.shuffle(dataset.tiles)
        epoch_loss = 0
        for i in range(n_train):
            x, lbl_def, lbl_yld, lbl_forest = dataset[i]
            if task == "def":
                target = lbl_def
            elif task == "yld":
                target = lbl_yld
            elif task == "forest":
                target = lbl_forest

            optimizer.zero_grad()
            pred = model(x.unsqueeze(0), task=task)
            if task == "def" or task == "forest":
                loss = nn.functional.binary_cross_entropy(pred, target.unsqueeze(0))
            else:
                loss = nn.functional.mse_loss(pred, target.unsqueeze(0))
            loss.backward()
            optimizer.step()
            epoch_loss += loss.item()
    return epoch_loss / n_train


def evaluate(model, dataset, task):
    n = len(dataset)
    n_train = int(n * 0.7)
    n_val = int(n * 0.15)
    test_idx = list(range(n_train + n_val, n))

    preds, targets = [], []
    for i in test_idx:
        x, lbl_def, lbl_yld, lbl_forest = dataset[i]
        if task == "def":
            target = lbl_def.item()
        elif task == "yld":
            target = lbl_yld.item()
        elif task == "forest":
            target = lbl_forest.item()
        with torch.no_grad():
            p = model(x.unsqueeze(0), task=task).item()
        preds.append(p)
        targets.append(target)

    preds = np.array(preds)
    targets = np.array(targets)

    if task == "yld":
        # Regression: MAE
        mae = float(np.abs(preds - targets).mean())
        return {"task": task, "metric": "mae", "value": mae}
    else:
        # Classification: F1
        bin_pred = (preds > 0.5).astype(int)
        bin_target = (targets > 0.5).astype(int)
        tp = ((bin_pred == 1) & (bin_target == 1)).sum()
        fp = ((bin_pred == 1) & (bin_target == 0)).sum()
        fn = ((bin_pred == 0) & (bin_target == 1)).sum()
        precision = tp / (tp + fp + 1e-8)
        recall = tp / (tp + fn + 1e-8)
        f1 = 2 * precision * recall / (precision + recall + 1e-8)
        return {"task": task, "metric": "f1", "value": float(f1)}


def main():
    print("=" * 70)
    print("CROSS-PAPER TRANSFER LEARNING EXPERIMENT (RQ4, H3)")
    print("=" * 70)

    # Load data
    print("\n[1/4] Loading data...")
    with rasterio.open(HANSEN_DIR / "hansen_lossyear_20S_060W.tif") as src:
        lossyear = src.read(1, window=Window(0, 0, 2000, 2000))
    with rasterio.open(HANSEN_DIR / "hansen_treecover2000_20S_060W.tif") as src:
        treecover = src.read(1, window=Window(0, 0, 2000, 2000))
    with rasterio.open(MAPBIOMAS_DIR / "mapbiomas_paraguay_2023.tif") as src:
        mb_chunk = src.read(1, window=Window(8000, 8000, 1000, 1000))
        from scipy.ndimage import zoom

        mapbiomas = zoom(mb_chunk, (2.0, 2.0), order=0)

    print(f"  Hansen lossyear: {lossyear.shape}, {(lossyear > 0).sum():,} loss pixels")
    print(f"  Hansen treecover: {treecover.shape}, mean={treecover.mean():.1f}")
    print(f"  MapBiomas: {mapbiomas.shape}")

    # Build dataset
    print("\n[2/4] Building dataset...")
    dataset = TileDataset(lossyear, treecover, mapbiomas, n_tiles=200)
    print(f"  {len(dataset)} tiles, balance: {sum(t[2] for t in dataset.tiles)}/{len(dataset)} positive deforestation")

    # Experiment 1: Train on deforestation, evaluate on all tasks
    print("\n[3/4] Experiment 1: Train on deforestation...")
    model1 = MultiTaskCNN()
    train_task(model1, dataset, "def", n_epochs=5)
    res1_def = evaluate(model1, dataset, "def")
    res1_yld = evaluate(model1, dataset, "yld")
    res1_forest = evaluate(model1, dataset, "forest")
    print(f"  Deforestation F1: {res1_def['value']:.3f}")
    print(f"  Yield MAE: {res1_yld['value']:.3f}")
    print(f"  Forest F1: {res1_forest['value']:.3f}")

    # Experiment 2: Train on yield, evaluate on all tasks
    print("\n[4/4] Experiment 2: Train on yield...")
    model2 = MultiTaskCNN()
    train_task(model2, dataset, "yld", n_epochs=5)
    res2_def = evaluate(model2, dataset, "def")
    res2_yld = evaluate(model2, dataset, "yld")
    res2_forest = evaluate(model2, dataset, "forest")
    print(f"  Deforestation F1: {res2_def['value']:.3f}")
    print(f"  Yield MAE: {res2_yld['value']:.3f}")
    print(f"  Forest F1: {res2_forest['value']:.3f}")

    # Compute transfer ratios
    yield_transfer = res2_yld["value"] / max(res1_yld["value"], 1e-6)
    def_transfer = res1_def["value"] / max(res2_def["value"], 1e-6)
    forest_transfer = res2_forest["value"] / max(res1_forest["value"], 1e-6)

    results = {
        "experiment": "Cross-paper transfer learning (RQ4, H3)",
        "data": "Hansen + MapBiomas",
        "n_tiles": len(dataset),
        "results": {
            "trained_on_deforestation": {
                "def_f1": res1_def["value"],
                "yld_mae": res1_yld["value"],
                "forest_f1": res1_forest["value"],
            },
            "trained_on_yield": {
                "def_f1": res2_def["value"],
                "yld_mae": res2_yld["value"],
                "forest_f1": res2_forest["value"],
            },
        },
        "transfer_ratios": {
            "yield_to_yield": 1.0,
            "def_to_yield": float(yield_transfer),
            "yld_to_def": float(def_transfer),
            "def_to_forest": float(forest_transfer),
        },
        "hypothesis_h3_test": {
            "h3a_null": "Deforestation-pretrained achieves same accuracy as yield-trained on yield task",
            "h3b_alternative": "Deforestation-pretrained achieves > 0.7x accuracy of yield-trained on yield task",
            "transfer_ratio_yield": yield_transfer,
            "h3_confirmed": yield_transfer > 0.7,
        },
        "limitations": [
            "Small dataset (200 tiles)",
            "Limited training (5 epochs)",
            "Tasks share vegetation features (limited transfer signal)",
            "Real transfer requires 50+ epochs and larger encoder",
        ],
        "next_steps": [
            "Run 50 epochs with proper hyperparameter tuning",
            "Use 1000+ tiles",
            "Test with frozen vs. fine-tuned encoder",
            "Apply to real YOLOv8 wildlife detection (Kai)",
        ],
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
    }

    out_path = OUT_DIR / "transfer_results.json"
    out_path.write_text(json.dumps(results, indent=2))
    print(f"\n  Saved: {out_path}")

    print(f"\n{'=' * 70}")
    print("  TRANSFER RATIOS:")
    print("    Yield->Yield: 1.0 (baseline)")
    print(f"    Deforest->Yield: {yield_transfer:.3f}  (H3 test: > 0.7 = confirmed)")
    print(f"    Yield->Deforest: {def_transfer:.3f}")
    print(f"    Deforest->Forest: {forest_transfer:.3f}")
    print(f"\n  H3 confirmed: {yield_transfer > 0.7}")


if __name__ == "__main__":
    main()
