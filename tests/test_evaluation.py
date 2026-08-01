"""Tests for src.evaluation module."""
import sys
from pathlib import Path

import pytest
import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.evaluation import (
    pixel_f1_score,
    pixel_iou,
    mean_iou,
    confusion_matrix_segmentation,
    regression_metrics,
    classification_metrics,
)


def test_pixel_f1_score():
    """Test F1 score."""
    y_true = np.array([0, 1, 2, 0, 1, 2])
    y_pred = np.array([0, 1, 2, 0, 2, 2])
    f1 = pixel_f1_score(y_true, y_pred, average="macro")
    assert 0 <= f1 <= 1


def test_pixel_iou():
    """Test IoU calculation."""
    y_true = np.array([0, 0, 1, 1])
    y_pred = np.array([0, 1, 1, 1])
    ious = pixel_iou(y_true, y_pred, num_classes=2)
    assert 0 in ious
    assert 1 in ious
    # Class 0: 1 true 0, 1 false 1 → 1 pred 0 + 1 false positive (pred=1 actual=0)
    # TP_0 = 1, FN_0 = 0, FP_0 = 1, union = 2 → IoU_0 = 0.5
    assert ious[0] == pytest.approx(0.5)
    # Class 1: TP = 2 (both true 1 correctly predicted as 1)
    # FN_1 = 0, FP_1 = 1 (pred 1 when actual 0), union = 3 → IoU = 2/3
    assert ious[1] == pytest.approx(2 / 3)


def test_mean_iou():
    """Test mIoU."""
    y_true = np.random.randint(0, 3, size=(50, 50))
    y_pred = np.random.randint(0, 3, size=(50, 50))
    miou = mean_iou(y_true, y_pred)
    assert 0 <= miou <= 1


def test_confusion_matrix_segmentation():
    """Test confusion matrix."""
    y_true = np.array([0, 0, 1, 1, 2, 2])
    y_pred = np.array([0, 1, 1, 1, 2, 2])
    cm = confusion_matrix_segmentation(y_true, y_pred, num_classes=3)
    assert cm.shape == (3, 3)


def test_regression_metrics():
    """Test regression metrics."""
    y_true = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    y_pred = np.array([1.1, 2.0, 2.9, 4.1, 4.8])
    metrics = regression_metrics(y_true, y_pred)
    assert "mae" in metrics
    assert "rmse" in metrics
    assert "r2" in metrics
    assert 0 <= metrics["mae"] <= 1.0


def test_classification_metrics():
    """Test classification metrics."""
    y_true = np.array([0, 0, 1, 1, 2, 2])
    y_pred = np.array([0, 0, 1, 1, 1, 2])
    metrics = classification_metrics(y_true, y_pred)
    assert "accuracy" in metrics
    assert "f1_macro" in metrics
    assert metrics["accuracy"] == pytest.approx(5 / 6)
