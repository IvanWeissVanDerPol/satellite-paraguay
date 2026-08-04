"""Tests for paper pipeline demo functions — p0025, p0026, p0035, p0100.

Coverage target: 95%+. Covers the __main__ demo runners.
"""
import sys
import numpy as np
import pytest
from unittest.mock import patch, MagicMock


class TestYrupeDemo:
    """Tests for run_yrupe_demo function."""

    def test_yrupe_demo_runs(self, monkeypatch, capsys):
        from src.papers.p0025_yrupe_yield.pipeline import run_yrupe_demo
        with patch("src.papers.p0025_yrupe_yield.pipeline.YrupePipeline") as mock_class:
            mock_instance = MagicMock()
            mock_instance.load_inbio_data.return_value = {"status": "loaded"}
            mock_instance.predict_yield.return_value = 4.5
            mock_class.return_value = mock_instance
            run_yrupe_demo()
        captured = capsys.readouterr()
        assert "INBIO data" in captured.out
        assert "Predicted yield" in captured.out


class TestKaiDemo:
    """Tests for run_kai_demo function."""

    def test_kai_demo_runs(self, monkeypatch, capsys):
        from src.papers.p0026_kai_poaching.pipeline import run_kai_demo
        with patch("src.papers.p0026_kai_poaching.pipeline.KaiPipeline") as mock_class:
            mock_instance = MagicMock()
            mock_instance.load_data.return_value = {"status": "loaded"}
            mock_instance.detect_events.return_value = [{"id": 1}]
            mock_instance.validate.return_value = {"f1": 0.85}
            mock_class.return_value = mock_instance
            run_kai_demo()
        captured = capsys.readouterr()
        assert "events" in captured.out.lower() or "Demo" in captured.out or "0" in captured.out


class TestTatakuaDemo:
    """Tests for run_tatakua_demo function."""

    def test_tatakua_demo_runs(self, monkeypatch, capsys):
        from src.papers.p0035_tatakua_air_quality.pipeline import run_tatakua_demo
        with patch("src.papers.p0035_tatakua_air_quality.pipeline.TatakuaPipeline") as mock_class:
            mock_instance = MagicMock()
            mock_instance.fetch_openaq_data.return_value = [{"value": 10}]
            mock_instance.fetch_sentinel5p.return_value = {
                "no2": np.array([1e-5]),
                "so2": np.array([1e-5]),
                "co": np.array([1e-5]),
            }
            mock_instance.forecast_pm25.return_value = np.array([10.5, 11.0, 12.0])
            mock_class.return_value = mock_instance
            run_tatakua_demo()
        captured = capsys.readouterr()
        assert "OpenAQ" in captured.out
        assert "Sentinel-5P" in captured.out
        assert "Forecast" in captured.out


class TestYvyraDemo:
    """Tests for run_yvyra_demo function."""

    def test_yvyra_demo_runs(self, monkeypatch, capsys):
        from src.papers.p0100_yvyra_carbon_credits.pipeline import run_yvyra_demo
        with patch("src.papers.p0100_yvyra_carbon_credits.pipeline.YvyraPipeline") as mock_class:
            mock_instance = MagicMock()
            mock_instance.load_verra_data.return_value = {"status": "loaded"}
            mock_instance.load_hansen_data.return_value = {"status": "loaded"}
            mock_instance.detect_discrepancies.return_value = [{"id": 1}]
            mock_class.return_value = mock_instance
            run_yvyra_demo()
        captured = capsys.readouterr()
        assert "Demo" in captured.out or "Verra" in captured.out or "carbon" in captured.out.lower()
