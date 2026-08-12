"""Real baselines for P0011 Yvytu (Chaco deforestation).

Baselines to compare against Prithvi foundation model:
1. Random Forest per-pixel
2. U-Net from scratch
3. Persistence (no change)
4. Linear trend
"""
from pathlib import Path
from typing import Optional, Tuple
import numpy as np

from src.evaluation import pixel_f1_score, mean_iou, print_metrics


def random_forest_baseline(
    ndvi_timeseries: np.ndarray,
    ground_truth: np.ndarray,
    n_estimators: int = 100,
    random_state: int = 42,
) -> np.ndarray:
    """Random Forest per-pixel baseline.

    Features per pixel: mean, std, min, max, slope over time.
    Train: per-pixel classification.

    Args:
        ndvi_timeseries: (T, H, W) NDVI values
        ground_truth: (H, W) land cover labels
        n_estimators: number of trees
        random_state: random seed

    Returns:
        (H, W) predictions
    """
    try:
        from sklearn.ensemble import RandomForestClassifier
    except ImportError:
        raise ImportError("scikit-learn not installed")

    T, H, W = ndvi_timeseries.shape

    # Compute features per pixel
    features = np.stack([
        ndvi_timeseries.mean(axis=0),
        ndvi_timeseries.std(axis=0),
        ndvi_timeseries.min(axis=0),
        ndvi_timeseries.max(axis=0),
        # Linear trend
        np.polyfit(np.arange(T), ndvi_timeseries.reshape(T, -1), 1)[0].reshape(H, W),
    ], axis=-1)  # (H, W, 5)

    X = features.reshape(-1, 5)
    y = ground_truth.reshape(-1)

    # Subsample for training (RF slow on full image)
    n_samples = min(10000, len(y))
    np.random.seed(random_state)
    sample_idx = np.random.choice(len(y), n_samples, replace=False)
    X_sample = X[sample_idx]
    y_sample = y[sample_idx]

    # Train
    clf = RandomForestClassifier(n_estimators=n_estimators, random_state=random_state, n_jobs=-1)
    clf.fit(X_sample, y_sample)

    # Predict
    preds = clf.predict(X).reshape(H, W)
    return preds


def unet_baseline(
    ndvi_timeseries: np.ndarray,
    ground_truth: np.ndarray,
    epochs: int = 30,
    batch_size: int = 16,
) -> np.ndarray:
    """U-Net from scratch baseline.

    Simple encoder-decoder for segmentation.
    """
    try:
        import torch
        import torch.nn as nn
        from torch.utils.data import DataLoader, TensorDataset
    except ImportError:
        raise ImportError("PyTorch not installed")

    T, H, W = ndvi_timeseries.shape

    # Add channel dim + pad to 256x256
    if H < 256 or W < 256:
        pad_h = max(0, 256 - H)
        pad_w = max(0, 256 - W)
        ndvi_padded = np.pad(ndvi_timeseries, ((0, 0), (0, pad_h), (0, pad_w)), mode="reflect")
        gt_padded = np.pad(ground_truth, ((0, pad_h), (0, pad_w)), mode="constant")
    else:
        ndvi_padded = ndvi_timeseries[:, :256, :256]
        gt_padded = ground_truth[:256, :256]

    # Simple U-Net
    class UNet(nn.Module):
        def __init__(self, in_channels=T, n_classes=10):
            super().__init__()
            self.enc = nn.Sequential(
                nn.Conv2d(in_channels, 32, 3, padding=1),
                nn.ReLU(),
                nn.MaxPool2d(2),
                nn.Conv2d(32, 64, 3, padding=1),
                nn.ReLU(),
                nn.MaxPool2d(2),
            )
            self.dec = nn.Sequential(
                nn.ConvTranspose2d(64, 32, 2, stride=2),
                nn.ReLU(),
                nn.ConvTranspose2d(32, 16, 2, stride=2),
                nn.ReLU(),
                nn.Conv2d(16, n_classes, 1),
            )

        def forward(self, x):
            x = self.enc(x)
            x = self.dec(x)
            return x

    # Simple training loop
    model = UNet()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    criterion = nn.CrossEntropyLoss(ignore_index=-1)

    X_tensor = torch.from_numpy(ndvi_padded.astype(np.float32)).unsqueeze(0)
    y_tensor = torch.from_numpy(gt_padded.astype(np.int64)).unsqueeze(0)

    model.train()
    for epoch in range(epochs):
        optimizer.zero_grad()
        out = model(X_tensor)
        loss = criterion(out, y_tensor)
        loss.backward()
        optimizer.step()

    # Predict
    model.eval()
    with torch.no_grad():
        out = model(X_tensor)
        preds = out.argmax(dim=1).squeeze(0).numpy()

    return preds[:H, :W]


def persistence_baseline(
    ndvi_timeseries: np.ndarray,
    n_classes: int = 10,
) -> np.ndarray:
    """Persistence baseline — predict most common class from first time step.

    For NDVI: high NDVI = forest, low NDVI = bare/deforested.
    """
    T, H, W = ndvi_timeseries.shape
    first_frame = ndvi_timeseries[0]

    # Map NDVI to classes (simple heuristic)
    preds = np.zeros((H, W), dtype=np.int64)
    preds[first_frame > 0.7] = 1  # forest
    preds[(first_frame > 0.5) & (first_frame <= 0.7)] = 2  # partial
    preds[(first_frame > 0.3) & (first_frame <= 0.5)] = 3  # grass
    preds[first_frame <= 0.3] = 4  # bare
    return preds


def linear_trend_baseline(
    ndvi_timeseries: np.ndarray,
    threshold: float = -0.1,
) -> np.ndarray:
    """Linear trend baseline — predict deforestation where NDVI trend is steeply negative.

    Args:
        ndvi_timeseries: (T, H, W)
        threshold: pixels with slope < threshold = deforested

    Returns:
        (H, W) binary deforestation mask
    """
    T, H, W = ndvi_timeseries.shape

    # Compute slope per pixel
    x = np.arange(T)
    x_mean = np.mean(x)
    y_mean = np.mean(ndvi_timeseries, axis=0)

    numerator = np.zeros((H, W))
    denominator = np.sum((x - x_mean) ** 2)
    for t in range(T):
        numerator += (x[t] - x_mean) * (ndvi_timeseries[t] - y_mean)
    slope = numerator / (denominator + 1e-8)

    # Predict deforestation
    preds = (slope < threshold).astype(np.int64)
    return preds


def run_all_baselines(
    ndvi_timeseries: np.ndarray,
    ground_truth: np.ndarray,
) -> dict:
    """Run all baselines and return metrics."""
    results = {}

    # 1. Persistence
    print("Running persistence baseline...")
    preds = persistence_baseline(ndvi_timeseries)
    results["persistence"] = {
        "f1_macro": pixel_f1_score(ground_truth, preds),
        "miou": mean_iou(ground_truth, preds),
    }

    # 2. Linear trend
    print("Running linear trend baseline...")
    preds = linear_trend_baseline(ndvi_timeseries)
    # Convert to multi-class (binary: 0 or 4)
    preds_multi = preds.copy()
    results["linear_trend"] = {
        "f1_macro": pixel_f1_score(ground_truth, preds_multi),
        "miou": mean_iou(ground_truth, preds_multi),
    }

    # 3. Random Forest (subsampled)
    print("Running Random Forest baseline...")
    try:
        preds = random_forest_baseline(ndvi_timeseries, ground_truth, n_estimators=50)
        results["random_forest"] = {
            "f1_macro": pixel_f1_score(ground_truth, preds),
            "miou": mean_iou(ground_truth, preds),
        }
    except Exception as e:
        print(f"  RF failed: {e}")
        results["random_forest"] = {"error": str(e)}

    return results


if __name__ == "__main__":
    # FAIL-LOUD (added 2026-08-11): no more np.random.rand() silent fallback.
    # Provide real NDVI/ground-truth arrays via the CLI args, or run via the
    # scripts/run_real_experiment_p0011.py wrapper which loads from
    # data/cache/sentinel2/.
    print("P0011 baselines demo (fail-loud mode)")
    print("Pass NDVI as .npz and ground-truth as .npy:")
    print("    python -m src.baselines.p0011_yvutu_baselines ndvi.npz gt.npy")
    import sys
    if len(sys.argv) >= 3:
        ndvi = np.load(sys.argv[1])["ndvi"]
        gt = np.load(sys.argv[2])
        if ndvi.ndim != 3:
            raise FileNotFoundError(
                f"NDVI must be (T, H, W); got shape {ndvi.shape}. "
                "See scripts/download_sentinel2_real.py."
            )
        if gt.shape != ndvi.shape[1:]:
            raise FileNotFoundError(
                f"ground_truth shape {gt.shape} != NDVI spatial {ndvi.shape[1:]}"
            )
        results = run_all_baselines(ndvi, gt)
        print_metrics(results)
    else:
        raise FileNotFoundError(
            "P0011 baselines demo requires real data. "
            "Use scripts/run_real_experiment_p0011.py to load from data/cache/sentinel2/. "
            "Silent random-fill was removed 2026-08-11 — see BRUTAL_ROAST.md."
        )
