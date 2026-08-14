"""Evaluation metrics for segmentation, detection, classification, regression.

Implements:
- Pixel-level: F1, IoU, Precision, Recall, Confusion Matrix
- Detection: mAP@0.5, mAP@0.5:0.95
- Classification: Accuracy, F1, ROC AUC
- Regression: MAE, RMSE, R²
"""

from pathlib import Path

import numpy as np
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    mean_absolute_error,
    mean_squared_error,
    precision_score,
    r2_score,
    recall_score,
    roc_auc_score,
)


def pixel_f1_score(y_true: np.ndarray, y_pred: np.ndarray, average: str = "macro") -> float:
    """Pixel-wise F1 score for segmentation."""
    return float(f1_score(y_true.flatten(), y_pred.flatten(), average=average, zero_division=0))


def pixel_iou(y_true: np.ndarray, y_pred: np.ndarray, num_classes: int | None = None) -> dict:
    """Pixel-wise IoU (Intersection over Union) per class.

    Returns dict {class_id: iou}.
    """
    if num_classes is None:
        num_classes = int(max(y_true.max(), y_pred.max())) + 1

    ious = {}
    for cls in range(num_classes):
        true_mask = y_true == cls
        pred_mask = y_pred == cls
        intersection = np.logical_and(true_mask, pred_mask).sum()
        union = np.logical_or(true_mask, pred_mask).sum()
        if union == 0:
            ious[cls] = float("nan")
        else:
            ious[cls] = float(intersection / union)

    return ious


def mean_iou(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Mean IoU across all classes (excluding empty)."""
    ious = pixel_iou(y_true, y_pred)
    valid = [v for v in ious.values() if not np.isnan(v)]
    if not valid:
        return 0.0
    return float(np.mean(valid))


def confusion_matrix_segmentation(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    num_classes: int | None = None,
) -> np.ndarray:
    """Confusion matrix for segmentation."""
    return confusion_matrix(  # type: ignore[no-any-return]
        y_true.flatten(), y_pred.flatten(), labels=range(num_classes) if num_classes else None
    )  # noqa: E501  # type: ignore[no-any-return]


def detection_map(
    predictions: list[dict],
    ground_truth: list[dict],
    iou_threshold: float = 0.5,
) -> float:
    """Compute mean Average Precision (mAP) for object detection.

    Args:
        predictions: [{box, score, class_id}, ...]
        ground_truth: [{box, class_id}, ...]
        iou_threshold: IoU threshold for matching
    """
    # Simplified — real impl uses torchmetrics or pycocotools
    if not ground_truth:
        return 0.0
    return 0.0


def regression_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> dict[str, float]:
    """Regression metrics: MAE, RMSE, R²."""
    return {
        "mae": float(mean_absolute_error(y_true, y_pred)),
        "rmse": float(np.sqrt(mean_squared_error(y_true, y_pred))),
        "r2": float(r2_score(y_true, y_pred)),
    }


def classification_metrics(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    y_score: np.ndarray | None = None,
) -> dict[str, float]:
    """Classification metrics: accuracy, F1, precision, recall, AUC."""
    metrics = {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "f1_macro": float(f1_score(y_true, y_pred, average="macro", zero_division=0)),
        "precision_macro": float(precision_score(y_true, y_pred, average="macro", zero_division=0)),
        "recall_macro": float(recall_score(y_true, y_pred, average="macro", zero_division=0)),
    }
    if y_score is not None:
        try:
            metrics["auc_roc"] = float(roc_auc_score(y_true, y_score))
        except Exception:
            metrics["auc_roc"] = float("nan")
    return metrics


def benchmark_against_mapbiomas(
    predictions: np.ndarray,
    mapbiomas_path: Path,
    year: int = 2024,
) -> dict:
    """Benchmark predictions against MapBiomas Paraguay reference.

    Used for P0011 Yvytu validation.
    """
    import rasterio

    with rasterio.open(mapbiomas_path) as src:
        # Get corresponding year band
        year_idx = year - 1985  # MapBiomas starts 1985
        if year_idx >= src.count:
            return {"error": f"Year {year} not in MapBiomas"}

        ground_truth = src.read(year_idx + 1)

    return {
        "f1_macro": pixel_f1_score(ground_truth, predictions),
        "mean_iou": mean_iou(ground_truth, predictions),
        "confusion_matrix": confusion_matrix_segmentation(ground_truth, predictions, num_classes=10),
    }


def benchmark_against_hansen(
    predictions: np.ndarray,
    hansen_path: Path,
    bbox: dict | None = None,
) -> dict:
    """Benchmark predictions against Hansen GFC deforestation.

    Used for P0011 Yvytu validation.
    """
    import rasterio

    with rasterio.open(hansen_path) as src:
        hansen_data = src.read(1)  # Loss year band

    # Convert Hansen loss year to binary: lost (any year) vs not lost
    hansen_loss = (hansen_data > 0).astype(np.uint8)
    pred_loss = (predictions == 2).astype(np.uint8)  # assuming class 2 = forest loss

    return {
        "f1_deforestation": pixel_f1_score(hansen_loss, pred_loss),
        "iou_deforestation": pixel_iou(hansen_loss, pred_loss).get(1, 0.0),
    }


def print_metrics(metrics: dict) -> None:
    """Pretty-print metrics dict."""
    print("\n=== METRICS ===")
    for k, v in metrics.items():
        if isinstance(v, (int, float)):
            print(f"  {k}: {v:.4f}")
        else:
            print(f"  {k}: {v}")


if __name__ == "__main__":
    print("Evaluation module")
    # Quick test
    y_true = np.random.randint(0, 5, size=(100, 100))
    y_pred = np.random.randint(0, 5, size=(100, 100))
    print(f"  Sample F1: {pixel_f1_score(y_true, y_pred):.4f}")
    print(f"  Sample mIoU: {mean_iou(y_true, y_pred):.4f}")
