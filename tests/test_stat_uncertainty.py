"""Tests for src/utils/stat_analysis.py and src/utils/uncertainty.py."""
import pytest
import numpy as np
from pathlib import Path
from unittest.mock import patch, MagicMock


class TestStatAnalysis:
    """Tests for stat_analysis module."""

    def test_bootstrap_ci_basic(self):
        from src.utils.stat_analysis import bootstrap_ci_from_confusion
        # 100 tp, 10 fp, 20 fn, 1000 tn (typical classifier results)
        result = bootstrap_ci_from_confusion(100, 10, 20, 1000, n_bootstrap=100)
        assert "precision" in result
        assert "recall" in result
        assert "f1" in result
        assert all("mean" in v and "ci_lower" in v and "ci_upper" in v for v in result.values())

    def test_bootstrap_ci_zero_total(self):
        from src.utils.stat_analysis import bootstrap_ci_from_confusion
        result = bootstrap_ci_from_confusion(0, 0, 0, 0, n_bootstrap=10)
        assert all(v["mean"] == 0.0 for v in result.values())

    def test_bootstrap_ci_high_ci(self):
        from src.utils.stat_analysis import bootstrap_ci_from_confusion
        result = bootstrap_ci_from_confusion(50, 5, 10, 500, ci=0.99, n_bootstrap=100)
        assert "ci_lower" in result["f1"]

    def test_metric_stats_with_ci_basic(self):
        from src.utils.stat_analysis import metric_stats_with_ci
        result = metric_stats_with_ci([1.0, 2.0, 3.0, 4.0, 5.0])
        assert result["n"] == 5
        assert result["mean"] == 3.0
        assert result["std"] > 0

    def test_metric_stats_with_ci_empty(self):
        from src.utils.stat_analysis import metric_stats_with_ci
        result = metric_stats_with_ci([])
        assert result["n"] == 0
        assert result["mean"] == 0.0

    def test_aggregate_metrics(self):
        from src.utils.stat_analysis import aggregate_metrics
        metrics = [
            {"f1": 0.8, "precision": 0.85, "recall": 0.75},
            {"f1": 0.82, "precision": 0.87, "recall": 0.77},
            {"f1": 0.78, "precision": 0.83, "recall": 0.73},
        ]
        result = aggregate_metrics(metrics)
        assert "f1" in result
        assert "precision" in result
        assert "recall" in result
        assert result["f1"]["n"] == 3

    def test_analyze_confusion_matrix_basic(self):
        from src.utils.stat_analysis import analyze_confusion_matrix
        result = analyze_confusion_matrix(100, 10, 20, 1000)
        assert result["precision"] == 100 / 110
        assert result["recall"] == 100 / 120
        assert result["f1"] > 0
        assert result["accuracy"] == 1100 / 1130

    def test_analyze_confusion_matrix_zero(self):
        from src.utils.stat_analysis import analyze_confusion_matrix
        result = analyze_confusion_matrix(0, 0, 0, 0)
        assert result["precision"] == 0.0
        assert result["n"] == 0

    def test_analyze_confusion_matrix_no_positives(self):
        from src.utils.stat_analysis import analyze_confusion_matrix
        result = analyze_confusion_matrix(0, 0, 0, 100)
        assert result["precision"] == 0.0
        assert result["recall"] == 0.0
        assert result["f1"] == 0.0


class TestUncertainty:
    """Tests for uncertainty module."""

    def test_pixel_bootstrap_fast_basic(self):
        from src.utils.uncertainty import pixel_bootstrap_fast
        lossyear = np.array([[0, 1, 2], [3, 4, 5], [6, 7, 8]])
        result = pixel_bootstrap_fast(lossyear, n_boot=100)
        assert "mean" in result
        assert "ci_lower_95" in result
        assert "ci_upper_95" in result
        assert result["n_bootstrap"] == 100

    def test_pixel_bootstrap_empty(self):
        from src.utils.uncertainty import pixel_bootstrap_fast
        lossyear = np.array([])
        result = pixel_bootstrap_fast(lossyear)
        assert result["mean"] == 0.0

    def test_pixel_bootstrap_all_zeros(self):
        from src.utils.uncertainty import pixel_bootstrap_fast
        lossyear = np.zeros((10, 10), dtype=int)
        result = pixel_bootstrap_fast(lossyear, n_boot=50)
        assert result["mean"] == 0.0

    def test_block_bootstrap_fast_basic(self):
        from src.utils.uncertainty import block_bootstrap_fast
        lossyear = np.random.randint(0, 5, size=(200, 200))
        result = block_bootstrap_fast(lossyear, block_size=50, n_boot=100)
        assert "mean" in result
        assert result["n_blocks"] == 16

    def test_block_bootstrap_too_small(self):
        from src.utils.uncertainty import block_bootstrap_fast
        lossyear = np.array([[0, 1], [2, 3]])
        result = block_bootstrap_fast(lossyear, block_size=100, n_boot=10)
        assert result["n_blocks"] == 0

    def test_agb_sensitivity_basic(self):
        from src.utils.uncertainty import agb_sensitivity
        lossyear = np.ones((10, 10), dtype=int)
        treecover = np.zeros((10, 10))
        result = agb_sensitivity(lossyear, treecover)
        assert "low" in result
        assert "mid" in result
        assert "high" in result
        assert all("co2e_mt" in r for r in result.values())

    def test_agb_sensitivity_high_above_low(self):
        from src.utils.uncertainty import agb_sensitivity
        lossyear = np.ones((10, 10), dtype=int)
        treecover = np.zeros((10, 10))
        result = agb_sensitivity(lossyear, treecover)
        # Higher AGB scenario should produce more CO2e
        assert result["high"]["co2e_mt"] > result["low"]["co2e_mt"]
        assert result["mid"]["co2e_mt"] > result["low"]["co2e_mt"]

    def test_annual_loss_ci(self):
        from src.utils.uncertainty import annual_loss_ci
        lossyear = np.random.randint(0, 24, size=(100, 100))
        result = annual_loss_ci(lossyear, n_boot=50)
        assert "2001" in result
        assert "2023" in result
        assert all("mean" in v for v in result.values())

    def test_annual_loss_ci_empty(self):
        from src.utils.uncertainty import annual_loss_ci
        lossyear = np.array([])
        result = annual_loss_ci(lossyear)
        assert result == {}

    def test_pixel_loss_rate(self):
        from src.utils.uncertainty import pixel_loss_rate
        lossyear = np.array([[0, 1], [0, 1]])
        assert pixel_loss_rate(lossyear) == 0.5

    def test_pixel_loss_rate_empty(self):
        from src.utils.uncertainty import pixel_loss_rate
        assert pixel_loss_rate(np.array([])) == 0.0

    def test_loss_area_hectares(self):
        from src.utils.uncertainty import loss_area_hectares
        lossyear = np.array([[0, 1], [1, 1]])
        area = loss_area_hectares(lossyear)
        # 3 loss pixels * 0.09 ha = 0.27 ha
        assert area == pytest.approx(0.27, rel=0.01)

    def test_loss_area_custom_pixel(self):
        from src.utils.uncertainty import loss_area_hectares
        lossyear = np.array([[1, 1]])
        area = loss_area_hectares(lossyear, pixel_area_ha=0.01)
        assert area == pytest.approx(0.02, rel=0.01)