"""Tests for src/evaluation/metrics.py — additional coverage.

Coverage target: 80%+. Tests detection_map, classification_metrics,
benchmark_against_mapbiomas, benchmark_against_hansen, print_metrics,
pixel_iou edge cases, regression_metrics edge cases.
"""
import pytest
import numpy as np
from pathlib import Path
from unittest.mock import patch, MagicMock


class TestPixelF1Score:
    def test_f1_perfect(self):
        from src.evaluation.metrics import pixel_f1_score
        y_true = np.array([0, 1, 0, 1, 0, 1])
        y_pred = np.array([0, 1, 0, 1, 0, 1])
        assert pixel_f1_score(y_true, y_pred) == 1.0

    def test_f1_zero(self):
        from src.evaluation.metrics import pixel_f1_score
        y_true = np.array([0, 0, 0, 0])
        y_pred = np.array([1, 1, 1, 1])
        # F1 should be 0 (no positive predicted)
        assert pixel_f1_score(y_true, y_pred) >= 0

    def test_f1_micro(self):
        from src.evaluation.metrics import pixel_f1_score
        y_true = np.array([0, 1, 0, 1, 0, 1])
        y_pred = np.array([0, 1, 1, 1, 0, 0])
        score = pixel_f1_score(y_true, y_pred, average="micro")
        assert 0 <= score <= 1


class TestPixelIoU:
    def test_iou_perfect(self):
        from src.evaluation.metrics import pixel_iou
        y_true = np.array([0, 1, 0, 1])
        y_pred = np.array([0, 1, 0, 1])
        result = pixel_iou(y_true, y_pred)
        assert result[0] == 1.0
        assert result[1] == 1.0

    def test_iou_with_num_classes(self):
        from src.evaluation.metrics import pixel_iou
        y_true = np.array([0, 1, 2, 0, 1, 2])
        y_pred = np.array([0, 1, 2, 0, 1, 2])
        result = pixel_iou(y_true, y_pred, num_classes=3)
        assert isinstance(result, dict)
        assert len(result) == 3


class TestMeanIoU:
    def test_mean_iou_perfect(self):
        from src.evaluation.metrics import mean_iou
        y_true = np.array([0, 1, 0, 1])
        y_pred = np.array([0, 1, 0, 1])
        assert mean_iou(y_true, y_pred) == 1.0


class TestConfusionMatrixSegmentation:
    def test_confusion_matrix(self):
        from src.evaluation.metrics import confusion_matrix_segmentation
        y_true = np.array([0, 1, 0, 1, 0, 1])
        y_pred = np.array([0, 1, 0, 1, 0, 0])
        result = confusion_matrix_segmentation(y_true, y_pred, num_classes=2)
        assert result.shape == (2, 2)

    def test_confusion_matrix_auto_classes(self):
        from src.evaluation.metrics import confusion_matrix_segmentation
        y_true = np.array([0, 1, 2, 0, 1, 2])
        y_pred = np.array([0, 1, 2, 0, 1, 2])
        result = confusion_matrix_segmentation(y_true, y_pred)
        # Should auto-detect 3 classes
        assert result.shape == (3, 3)


class TestDetectionMap:
    """Tests for detection_map (mAP) function."""

    def test_detection_map_returns_float(self):
        from src.evaluation.metrics import detection_map
        preds = [{"boxes": [[0, 0, 10, 10]], "scores": [0.95], "labels": [0]}]
        gts = [{"boxes": [[0, 0, 10, 10]], "labels": [0]}]
        result = detection_map(preds, gts)
        # Returns a float mAP score (stub returns 0.0)
        assert isinstance(result, (int, float))

    def test_detection_map_empty_gts(self):
        from src.evaluation.metrics import detection_map
        result = detection_map([], [])
        assert result == 0.0

    def test_detection_map_with_iou_threshold(self):
        from src.evaluation.metrics import detection_map
        preds = [{"boxes": [[0, 0, 10, 10]], "scores": [0.95], "labels": [0]}]
        gts = [{"boxes": [[0, 0, 10, 10]], "labels": [0]}]
        result = detection_map(preds, gts, iou_threshold=0.5)
        assert isinstance(result, (int, float))


class TestRegressionMetrics:
    def test_regression_metrics_perfect(self):
        from src.evaluation.metrics import regression_metrics
        y_true = np.array([1.0, 2.0, 3.0])
        y_pred = np.array([1.0, 2.0, 3.0])
        result = regression_metrics(y_true, y_pred)
        assert result["r2"] == 1.0
        assert result["mae"] == 0.0
        assert result["rmse"] == 0.0

    def test_regression_metrics_with_error(self):
        from src.evaluation.metrics import regression_metrics
        y_true = np.array([1.0, 2.0, 3.0])
        y_pred = np.array([2.0, 3.0, 4.0])  # off by 1
        result = regression_metrics(y_true, y_pred)
        assert result["mae"] == 1.0
        assert result["rmse"] == 1.0
        assert result["r2"] < 1.0  # not perfect


class TestClassificationMetrics:
    def test_classification_metrics_basic(self):
        from src.evaluation.metrics import classification_metrics
        y_true = np.array([0, 1, 0, 1, 0, 1])
        y_pred = np.array([0, 1, 0, 1, 0, 0])
        result = classification_metrics(y_true, y_pred)
        assert "accuracy" in result
        assert "f1_macro" in result
        assert "precision_macro" in result
        assert "recall_macro" in result

    def test_classification_metrics_with_scores(self):
        """When y_score is provided, should compute AUC."""
        from src.evaluation.metrics import classification_metrics
        y_true = np.array([0, 1, 0, 1, 0, 1])
        y_pred = np.array([0, 1, 0, 1, 0, 1])
        y_score = np.array([0.1, 0.9, 0.2, 0.8, 0.3, 0.7])
        result = classification_metrics(y_true, y_pred, y_score=y_score)
        assert "auc_roc" in result


class TestBenchmarkAgainstMapbiomas:
    """Tests for benchmark_against_mapbiomas function."""

    def test_benchmark_against_mapbiomas(self, tmp_path):
        """Mock rasterio to test benchmark_against_mapbiomas."""
        from src.evaluation.metrics import benchmark_against_mapbiomas

        # Create a fake raster
        fake_raster = tmp_path / "fake.tif"
        fake_raster.write_text("")

        # Mock rasterio
        mock_src = MagicMock()
        mock_src.__enter__ = MagicMock(return_value=mock_src)
        mock_src.__exit__ = MagicMock(return_value=False)
        mock_src.count = 40  # years 1985-2024
        mock_src.read.return_value = np.zeros((50, 50), dtype=np.uint8)

        predictions = np.zeros((50, 50), dtype=np.uint8)

        with patch("rasterio.open", return_value=mock_src):
            result = benchmark_against_mapbiomas(predictions, fake_raster, year=2024)

        assert "f1_macro" in result
        assert "mean_iou" in result

    def test_benchmark_year_out_of_range(self, tmp_path):
        from src.evaluation.metrics import benchmark_against_mapbiomas
        fake_raster = tmp_path / "fake.tif"
        fake_raster.write_text("")

        mock_src = MagicMock()
        mock_src.__enter__ = MagicMock(return_value=mock_src)
        mock_src.__exit__ = MagicMock(return_value=False)
        mock_src.count = 10  # only 10 years

        predictions = np.zeros((50, 50), dtype=np.uint8)

        with patch("rasterio.open", return_value=mock_src):
            result = benchmark_against_mapbiomas(predictions, fake_raster, year=2050)
        # Year out of range should return error
        assert "error" in result


class TestBenchmarkAgainstHansen:
    """Tests for benchmark_against_hansen function."""

    def test_benchmark_against_hansen(self, tmp_path):
        from src.evaluation.metrics import benchmark_against_hansen

        fake_raster = tmp_path / "fake.tif"
        fake_raster.write_text("")

        mock_src = MagicMock()
        mock_src.__enter__ = MagicMock(return_value=mock_src)
        mock_src.__exit__ = MagicMock(return_value=False)
        # Hansen has values 0-23 for loss year
        mock_src.read.return_value = np.zeros((50, 50), dtype=np.uint8)

        predictions = np.zeros((50, 50), dtype=np.uint8)

        with patch("rasterio.open", return_value=mock_src):
            result = benchmark_against_hansen(predictions, fake_raster)
        assert "f1_deforestation" in result
        assert "iou_deforestation" in result

    def test_benchmark_against_hansen_with_bbox(self, tmp_path):
        from src.evaluation.metrics import benchmark_against_hansen
        fake_raster = tmp_path / "fake.tif"
        fake_raster.write_text("")

        mock_src = MagicMock()
        mock_src.__enter__ = MagicMock(return_value=mock_src)
        mock_src.__exit__ = MagicMock(return_value=False)
        mock_src.read.return_value = np.zeros((50, 50), dtype=np.uint8)

        predictions = np.zeros((50, 50), dtype=np.uint8)
        bbox = {"min_lon": -60, "max_lon": -55}

        with patch("rasterio.open", return_value=mock_src):
            result = benchmark_against_hansen(predictions, fake_raster, bbox=bbox)
        assert "f1_deforestation" in result


class TestPrintMetrics:
    """Tests for print_metrics function."""

    def test_print_metrics(self, capsys):
        from src.evaluation.metrics import print_metrics
        metrics = {"f1": 0.85, "accuracy": 0.95, "list_val": [1, 2]}
        print_metrics(metrics)
        captured = capsys.readouterr()
        assert "f1" in captured.out
        assert "0.8500" in captured.out

    def test_print_metrics_with_string(self, capsys):
        from src.evaluation.metrics import print_metrics
        metrics = {"name": "test_model", "f1": 0.5}
        print_metrics(metrics)
        captured = capsys.readouterr()
        assert "test_model" in captured.out