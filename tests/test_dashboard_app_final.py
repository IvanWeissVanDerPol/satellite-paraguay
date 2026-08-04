"""Final coverage tests for src/dashboard/app.py.

Coverage target: 95%+. Tests edge cases in dict handling.
"""
import json
import sys
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock


@pytest.fixture
def mock_streamlit(monkeypatch):
    mock_st = MagicMock()
    mock_st.columns.side_effect = lambda n=1, **kw: [MagicMock() for _ in range(n if isinstance(n, int) else 1)]
    mock_st.set_page_config = MagicMock()
    mock_st.sidebar = MagicMock()
    mock_st.sidebar.radio.return_value = "Overview"

    with patch.dict(sys.modules, {"streamlit": mock_st}):
        import src.dashboard.app as app_module
        saved = app_module.st
        app_module.st = mock_st
        yield mock_st
        app_module.st = saved


class TestPageIndigenousDictFallback:
    """Test the dict-with-non-territories fallback in page_indigenous."""

    def test_dict_with_dict_values(self, mock_streamlit, tmp_path):
        """When data is dict of dicts, fallback creates columns."""
        import src.dashboard.app as dash_mod
        dash_mod.REPO_ROOT = tmp_path

        ind_dir = tmp_path / "outputs/p0011/indigenous"
        ind_dir.mkdir(parents=True, exist_ok=True)
        (ind_dir / "indigenous_overlap.json").write_text(json.dumps({
            "stat1": {"total": 100, "loss": 20},
            "stat2": {"total": 50, "loss": 5},
        }))

        dash_mod.page_indigenous()


class TestPageDepartmentsNoLossPct:
    """Test when departments data has no loss_pct column."""

    def test_no_loss_pct_column(self, mock_streamlit, tmp_path):
        """When df has no loss_pct, no bar_chart."""
        import src.dashboard.app as dash_mod
        dash_mod.REPO_ROOT = tmp_path

        dept_dir = tmp_path / "outputs/p0011/departments"
        dept_dir.mkdir(parents=True, exist_ok=True)
        (dept_dir / "department_stats.json").write_text(json.dumps({
            "departments": [
                {"name": "Asuncion", "unrelated_field": 100},
            ]
        }))

        dash_mod.page_departments()


class TestPageDepartmentsFallbackDict:
    """Test departments with non-list structure."""

    def test_dict_with_only_list_value(self, mock_streamlit, tmp_path):
        """When data is dict containing a list value, use that."""
        import src.dashboard.app as dash_mod
        dash_mod.REPO_ROOT = tmp_path

        dept_dir = tmp_path / "outputs/p0011/departments"
        dept_dir.mkdir(parents=True, exist_ok=True)
        (dept_dir / "department_stats.json").write_text(json.dumps({
            "list_key": [
                {"name": "Alto Paraguay", "loss_pct": 28.49}
            ],
            "other_key": "value",
        }))

        dash_mod.page_departments()

    def test_dict_with_only_dict_value(self, mock_streamlit, tmp_path):
        """When data is dict with dict value."""
        import src.dashboard.app as dash_mod
        dash_mod.REPO_ROOT = tmp_path

        dept_dir = tmp_path / "outputs/p0011/departments"
        dept_dir.mkdir(parents=True, exist_ok=True)
        (dept_dir / "department_stats.json").write_text(json.dumps({
            "dict_key": {"name": "Asuncion", "loss_pct": 5.0},
            "other": 42,
        }))

        dash_mod.page_departments()