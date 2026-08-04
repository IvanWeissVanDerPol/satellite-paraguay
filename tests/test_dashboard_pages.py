"""Tests for src/dashboard/app.py page functions.

Coverage target: 70%+. We mock the streamlit module entirely and
call each page function to exercise the code paths.
"""
import json
import sys
import pytest
import pandas as pd
from pathlib import Path
from unittest.mock import MagicMock, patch


def _make_col():
    c = MagicMock()
    c.__enter__ = MagicMock(return_value=c)
    c.__exit__ = MagicMock(return_value=False)
    return c


def _make_mock_streamlit():
    mock_st = MagicMock()

    def _columns(n=1, **kwargs):
        return [_make_col() for _ in range(n if isinstance(n, int) else 1)]

    def _tabs(labels):
        n = len(labels) if hasattr(labels, "__len__") else 2
        return [_make_col() for _ in range(n)]

    mock_st.columns.side_effect = _columns
    mock_st.tabs.side_effect = _tabs
    for ctx_method in ["spinner", "echo", "expander", "container"]:
        setattr(mock_st, ctx_method, _make_col())
    mock_st.set_page_config = MagicMock()
    mock_st.title = MagicMock()
    mock_st.markdown = MagicMock()
    mock_st.metric = MagicMock()
    mock_st.dataframe = MagicMock()
    mock_st.bar_chart = MagicMock()
    mock_st.line_chart = MagicMock()
    mock_st.warning = MagicMock()
    mock_st.error = MagicMock()
    mock_st.info = MagicMock()
    mock_st.subheader = MagicMock()
    mock_st.code = MagicMock()
    mock_st.write = MagicMock()
    mock_st.json = MagicMock()
    mock_st.pyplot = MagicMock()
    mock_st.plotly_chart = MagicMock()
    mock_st.map = MagicMock()
    mock_st.divider = MagicMock()
    mock_st.sidebar = MagicMock()
    mock_st.radio = MagicMock(return_value="overview")
    return mock_st


@pytest.fixture
def mock_streamlit(monkeypatch):
    mock_st = _make_mock_streamlit()
    import src.dashboard.app as app_module
    saved_st = app_module.st
    app_module.st = mock_st
    saved_sys = sys.modules.get("streamlit")
    sys.modules["streamlit"] = mock_st
    yield mock_st
    app_module.st = saved_st
    if saved_sys is None:
        sys.modules.pop("streamlit", None)
    else:
        sys.modules["streamlit"] = saved_sys


class TestPageOverview:
    def test_page_overview_runs(self, mock_streamlit):
        from src.dashboard import app
        app.page_overview()
        mock_streamlit.title.assert_called()

    def test_page_overview_calls_metrics(self, mock_streamlit):
        from src.dashboard import app
        app.page_overview()
        assert mock_streamlit.metric.call_count >= 4

    def test_page_overview_calls_markdown(self, mock_streamlit):
        from src.dashboard import app
        app.page_overview()
        assert mock_streamlit.markdown.call_count >= 1


class TestPageDepartments:
    def test_page_departments_runs(self, mock_streamlit, tmp_path):
        """Use tmp_path to avoid real data files."""
        from src.dashboard import app
        app.REPO_ROOT = tmp_path
        app.page_departments()
        mock_streamlit.title.assert_called()

    def test_page_departments_warning_when_no_data(self, mock_streamlit, tmp_path):
        from src.dashboard import app
        app.REPO_ROOT = tmp_path
        app.page_departments()
        mock_streamlit.warning.assert_called()

    def test_page_departments_with_data(self, mock_streamlit, tmp_path):
        from src.dashboard import app
        dept_dir = tmp_path / "outputs/p0011/departments"
        dept_dir.mkdir(parents=True)
        (dept_dir / "department_stats.json").write_text(json.dumps({
            "departments": [
                {"name": "Alto Paraguay", "loss_pct": 28.49, "loss_km2": 11910},
                {"name": "Boquerón", "loss_pct": 24.05, "loss_km2": 1151},
            ]
        }))
        app.REPO_ROOT = tmp_path
        app.page_departments()
        mock_streamlit.dataframe.assert_called()


class TestPageIndigenous:
    def test_page_indigenous_runs(self, mock_streamlit):
        from src.dashboard import app
        app.page_indigenous()
        mock_streamlit.title.assert_called()

    def test_page_indigenous_warning_when_no_data(self, mock_streamlit, tmp_path):
        from src.dashboard import app
        app.REPO_ROOT = tmp_path
        app.page_indigenous()
        mock_streamlit.warning.assert_called()

    def test_page_indigenous_with_data(self, mock_streamlit, tmp_path):
        from src.dashboard import app
        ind_dir = tmp_path / "outputs/p0011/indigenous"
        ind_dir.mkdir(parents=True)
        (ind_dir / "indigenous_overlap.json").write_text(json.dumps({
            "territories": [
                {"name": "Carmelo Peralta", "loss_percentage": 49.45},
            ]
        }))
        app.REPO_ROOT = tmp_path
        app.page_indigenous()
        mock_streamlit.dataframe.assert_called()


class TestPageCarbon:
    def test_page_carbon_runs(self, mock_streamlit):
        from src.dashboard import app
        app.page_carbon()
        mock_streamlit.title.assert_called()

    def test_page_carbon_warning_when_no_data(self, mock_streamlit, tmp_path):
        from src.dashboard import app
        app.REPO_ROOT = tmp_path
        app.page_carbon()
        mock_streamlit.warning.assert_called()

    def test_page_carbon_with_data(self, mock_streamlit, tmp_path):
        from src.dashboard import app
        carbon_dir = tmp_path / "outputs/p0011/carbon"
        carbon_dir.mkdir(parents=True)
        (carbon_dir / "per_year_loss.json").write_text(json.dumps({
            "total_co2e_loss_mt": 277.5,
            "total_loss_pixels": 266_000_000,
            "per_year": {
                "2015": {"co2e_mt": 25.5, "pixels": 25000000},
            },
        }))
        app.REPO_ROOT = tmp_path
        app.page_carbon()
        assert mock_streamlit.metric.call_count >= 2


class TestPageModels:
    def test_page_models_runs(self, mock_streamlit):
        from src.dashboard import app
        app.page_models()
        mock_streamlit.title.assert_called()


class TestPageReferences:
    def test_page_references_runs(self, mock_streamlit):
        from src.dashboard import app
        app.page_references()
        mock_streamlit.title.assert_called()


class TestPageUncertainty:
    def test_page_uncertainty_runs(self, mock_streamlit):
        from src.dashboard import app
        app.page_uncertainty()
        mock_streamlit.title.assert_called()


class TestLoadJsonDashboard:
    def test_load_json(self, tmp_path):
        from src.dashboard.app import load_json
        f = tmp_path / "test.json"
        f.write_text(json.dumps({"key": "value"}))
        assert load_json(str(f)) == {"key": "value"}

    def test_load_json_missing(self, tmp_path):
        from src.dashboard.app import load_json
        result = load_json(str(tmp_path / "missing.json"))
        assert result is None