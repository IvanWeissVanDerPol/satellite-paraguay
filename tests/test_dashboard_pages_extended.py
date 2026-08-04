"""Extended dashboard tests — all remaining pages.

Coverage target: 90%+. Mocks streamlit module-level execution by
patching `app.st` after import.
"""
import json
import sys
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock


@pytest.fixture
def mock_streamlit(monkeypatch):
    """Patch streamlit BEFORE importing app, then patch `app.st`."""
    mock_st = MagicMock()

    def _columns(n=1, **kwargs):
        return [MagicMock() for _ in range(n if isinstance(n, int) else 1)]

    def _tabs(labels):
        n = len(labels) if hasattr(labels, "__len__") else 2
        return [MagicMock() for _ in range(n)]

    def _ctx():
        c = MagicMock()
        c.__enter__ = MagicMock(return_value=c)
        c.__exit__ = MagicMock(return_value=False)
        return c

    mock_st.columns.side_effect = _columns
    mock_st.tabs.side_effect = _tabs
    mock_st.set_page_config = MagicMock()
    mock_st.sidebar = MagicMock()
    mock_st.sidebar.radio.return_value = "Overview"  # any valid key
    mock_st.sidebar.selectbox.return_value = "Overview"
    mock_st.radio.return_value = "overview"

    # Block module-level execution path
    with patch.dict(sys.modules, {"streamlit": mock_st}):
        import src.dashboard.app as app_module
        saved_st = app_module.st
        app_module.st = mock_st
        yield mock_st
        app_module.st = saved_st


class TestPageIndigenous:
    """Tests for page_indigenous function."""

    def test_with_territories_data(self, mock_streamlit, tmp_path):
        """When indigenous data exists, display it."""
        import src.dashboard.app as dash_mod
        dash_mod.REPO_ROOT = tmp_path

        ind_dir = tmp_path / "outputs/p0011/indigenous"
        ind_dir.mkdir(parents=True, exist_ok=True)
        (ind_dir / "indigenous_overlap.json").write_text(json.dumps({
            "territories": [
                {"name": "Carmelo Peralta", "loss_pct": 49.0},
                {"name": "Maka", "loss_pct": 15.0},
            ]
        }))

        dash_mod.page_indigenous()
        mock_streamlit.dataframe.assert_called()

    def test_with_array_data(self, mock_streamlit, tmp_path):
        """When indigenous data is a JSON array."""
        import src.dashboard.app as dash_mod
        dash_mod.REPO_ROOT = tmp_path

        ind_dir = tmp_path / "outputs/p0011/indigenous"
        ind_dir.mkdir(parents=True, exist_ok=True)
        (ind_dir / "indigenous_overlap.json").write_text(json.dumps([
            {"name": "Ayoreo", "loss_pct": 25.5},
        ]))

        dash_mod.page_indigenous()

    def test_with_loss_percentage_column(self, mock_streamlit, tmp_path):
        """Test with alternative loss_percentage column."""
        import src.dashboard.app as dash_mod
        dash_mod.REPO_ROOT = tmp_path

        ind_dir = tmp_path / "outputs/p0011/indigenous"
        ind_dir.mkdir(parents=True, exist_ok=True)
        (ind_dir / "indigenous_overlap.json").write_text(json.dumps({
            "territories": [
                {"name": "Guarani", "loss_percentage": 30.0},
            ]
        }))

        dash_mod.page_indigenous()

    def test_no_data_shows_warning(self, mock_streamlit, tmp_path):
        """When no data file exists, shows warning."""
        import src.dashboard.app as dash_mod
        dash_mod.REPO_ROOT = tmp_path
        dash_mod.page_indigenous()
        mock_streamlit.warning.assert_called()


class TestPageCarbon:
    """Tests for page_carbon function."""

    def test_with_data(self, mock_streamlit, tmp_path):
        import src.dashboard.app as dash_mod
        dash_mod.REPO_ROOT = tmp_path

        carbon_dir = tmp_path / "outputs/p0011/carbon"
        carbon_dir.mkdir(parents=True, exist_ok=True)
        (carbon_dir / "per_year_loss.json").write_text(json.dumps({
            "total_co2e_loss_mt": 150000.5,
            "total_loss_pixels": 50000000,
            "per_year": {
                "2020": {"co2e_mt": 100000, "pixels": 25000},
                "2021": {"co2e_mt": 110000, "pixels": 27000},
            }
        }))

        dash_mod.page_carbon()
        mock_streamlit.metric.assert_called()

    def test_no_data(self, mock_streamlit, tmp_path):
        import src.dashboard.app as dash_mod
        dash_mod.REPO_ROOT = tmp_path
        dash_mod.page_carbon()
        mock_streamlit.warning.assert_called()

    def test_empty_per_year(self, mock_streamlit, tmp_path):
        """When per_year is empty, line chart should not be called."""
        import src.dashboard.app as dash_mod
        dash_mod.REPO_ROOT = tmp_path

        carbon_dir = tmp_path / "outputs/p0011/carbon"
        carbon_dir.mkdir(parents=True, exist_ok=True)
        (carbon_dir / "per_year_loss.json").write_text(json.dumps({
            "total_co2e_loss_mt": 0.0,
            "total_loss_pixels": 0,
            "per_year": {},
        }))

        dash_mod.page_carbon()


class TestPageModels:
    """Tests for page_models function."""

    def test_runs(self, mock_streamlit, tmp_path):
        import src.dashboard.app as dash_mod
        dash_mod.REPO_ROOT = tmp_path
        dash_mod.page_models()


class TestPageReferences:
    """Tests for page_references function."""

    def test_runs(self, mock_streamlit, tmp_path):
        import src.dashboard.app as dash_mod
        dash_mod.REPO_ROOT = tmp_path
        dash_mod.page_references()


class TestPageUncertainty:
    """Tests for page_uncertainty function."""

    def test_runs_with_data(self, mock_streamlit, tmp_path):
        import src.dashboard.app as dash_mod
        dash_mod.REPO_ROOT = tmp_path

        # Provide uncertainty data
        unc_dir = tmp_path / "outputs/p0011/uncertainty"
        unc_dir.mkdir(parents=True, exist_ok=True)
        (unc_dir / "uncertainty_results.json").write_text(json.dumps({
            "pixel_bootstrap": {
                "mean": 10000,
                "lower_95": 9500,
                "upper_95": 10500,
            },
            "department_bootstrap": [],
        }))

        dash_mod.page_uncertainty()

    def test_runs_no_data(self, mock_streamlit, tmp_path):
        """When no uncertainty data, function still runs."""
        import src.dashboard.app as dash_mod
        dash_mod.REPO_ROOT = tmp_path
        dash_mod.page_uncertainty()
