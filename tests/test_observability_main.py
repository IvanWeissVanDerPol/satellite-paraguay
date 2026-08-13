"""Tests for src/observability_dashboard.py main() function.

Coverage target: 70%+. We mock streamlit and run main() with
synthetic REPO_ROOT data.
"""

import pytest  # noqa: E402

pytest.importorskip("rasterio", reason="CI: requires optional system dep 'rasterio' (not installed)")  # noqa: E402

import json  # noqa: E402
import sys  # noqa: E402
from unittest.mock import MagicMock  # noqa: E402

import pytest  # noqa: E402


def _make_col():
    c = MagicMock()
    c.__enter__ = MagicMock(return_value=c)
    c.__exit__ = MagicMock(return_value=False)
    return c


def _make_mock_streamlit():
    mock_st = MagicMock()

    def _columns(spec=1, **kwargs):
        if isinstance(spec, int):
            n = spec
        elif isinstance(spec, (list, tuple)):
            n = len(spec)
        else:
            n = 1
        return [_make_col() for _ in range(n)]

    mock_st.columns.side_effect = _columns
    mock_st.set_page_config = MagicMock()
    mock_st.title = MagicMock()
    mock_st.markdown = MagicMock()
    mock_st.metric = MagicMock()
    mock_st.header = MagicMock()
    mock_st.subheader = MagicMock()
    mock_st.info = MagicMock()
    mock_st.success = MagicMock()
    mock_st.warning = MagicMock()
    mock_st.error = MagicMock()
    mock_st.dataframe = MagicMock()
    mock_st.bar_chart = MagicMock()
    mock_st.line_chart = MagicMock()
    mock_st.text = MagicMock()
    mock_st.expander = MagicMock(return_value=_make_col())
    mock_st.tabs = MagicMock(return_value=[_make_col(), _make_col()])
    return mock_st


@pytest.fixture
def mock_streamlit(monkeypatch):
    monkeypatch.setenv("MLFLOW_ALLOW_FILE_STORE", "true")
    monkeypatch.setenv("MLFLOW_TRACKING_URI", "file:/tmp/obs_mlruns")
    mock_st = _make_mock_streamlit()
    import src.observability_dashboard as obs_mod

    saved_st = obs_mod.st
    obs_mod.st = mock_st
    saved_sys = sys.modules.get("streamlit")
    sys.modules["streamlit"] = mock_st
    yield mock_st
    obs_mod.st = saved_st
    if saved_sys is None:
        sys.modules.pop("streamlit", None)
    else:
        sys.modules["streamlit"] = saved_sys


class TestMainEmpty:
    """Tests for main() with no data files."""

    def test_main_with_no_data(self, mock_streamlit, tmp_path):
        """Run main() with empty REPO_ROOT."""
        from src import observability_dashboard as obs_mod

        obs_mod.REPO_ROOT = tmp_path
        # Need to create the expected dirs (even if empty) so glob doesn't crash
        for sub in ["tests", "scripts", "src", "outputs"]:
            (tmp_path / sub).mkdir()
        obs_mod.main()
        # Should have called title, columns, metric
        mock_streamlit.title.assert_called()
        assert mock_streamlit.metric.call_count >= 1


class TestMainWithData:
    """Tests for main() with various data files present."""

    def test_main_with_test_report(self, mock_streamlit, tmp_path):
        """Run main() with test_report.json present."""
        from src import observability_dashboard as obs_mod

        # Set up dirs
        for sub in ["tests", "scripts", "src", "outputs"]:
            (tmp_path / sub).mkdir()
        # Test report
        (tmp_path / "outputs" / "test_report.json").write_text(json.dumps({"passed": 100, "failed": 5}))
        obs_mod.REPO_ROOT = tmp_path
        obs_mod.main()
        mock_streamlit.title.assert_called()

    def test_main_with_coverage_xml(self, mock_streamlit, tmp_path):
        """Run main() with coverage.xml present."""
        from src import observability_dashboard as obs_mod

        for sub in ["tests", "scripts", "src", "outputs"]:
            (tmp_path / sub).mkdir()
        (tmp_path / "coverage.xml").write_text(
            '<?xml version="1.0"?>\n'
            '<coverage line-rate="0.85" branch-rate="0.7">\n'
            '<packages><package name="src"><classes>'
            '<class name="foo" filename="src/foo.py" line-rate="0.9"/>\n'
            '<class name="bar" filename="src/bar.py" line-rate="0.8"/>\n'
            "</classes></package></packages>\n"
            "</coverage>\n"
        )
        obs_mod.REPO_ROOT = tmp_path
        obs_mod.main()
        mock_streamlit.title.assert_called()

    def test_main_with_dependency_audit(self, mock_streamlit, tmp_path):
        """Run main() with dependency_audit.json present."""
        from src import observability_dashboard as obs_mod

        for sub in ["tests", "scripts", "src", "outputs"]:
            (tmp_path / sub).mkdir()
        (tmp_path / "outputs" / "dependency_audit.json").write_text(
            json.dumps(
                {
                    "declared": ["numpy", "pandas", "scipy"],
                    "used_packages": ["numpy", "pandas"],
                    "missing": ["scipy"],
                    "unused": [],
                }
            )
        )
        obs_mod.REPO_ROOT = tmp_path
        obs_mod.main()
        mock_streamlit.title.assert_called()

    def test_main_with_alerts(self, mock_streamlit, tmp_path):
        """Run main() with alert_report.json present."""
        from src import observability_dashboard as obs_mod

        for sub in ["tests", "scripts", "src", "outputs"]:
            (tmp_path / sub).mkdir()
        (tmp_path / "outputs" / "alert_report.json").write_text(
            json.dumps(
                {
                    "alerts": [
                        {"severity": "high", "type": "test_fail", "message": "5 tests failed"},
                        {"severity": "medium", "type": "coverage_drop", "message": "Coverage dropped 2%"},
                        {"severity": "low", "type": "info", "message": "Dep update available"},
                    ]
                }
            )
        )
        obs_mod.REPO_ROOT = tmp_path
        obs_mod.main()
        mock_streamlit.title.assert_called()

    def test_main_with_no_alerts(self, mock_streamlit, tmp_path):
        """Run main() with empty alerts list."""
        from src import observability_dashboard as obs_mod

        for sub in ["tests", "scripts", "src", "outputs"]:
            (tmp_path / sub).mkdir()
        (tmp_path / "outputs" / "alert_report.json").write_text(json.dumps({"alerts": []}))
        obs_mod.REPO_ROOT = tmp_path
        obs_mod.main()
        # Should call success since no alerts
        mock_streamlit.success.assert_called()

    def test_main_full(self, mock_streamlit, tmp_path):
        """Run main() with everything."""
        from src import observability_dashboard as obs_mod

        for sub in ["tests", "scripts", "src", "outputs"]:
            (tmp_path / sub).mkdir()
        # Test files (one)
        (tmp_path / "tests" / "test_foo.py").write_text("# test")
        # Outputs
        (tmp_path / "outputs" / "test_report.json").write_text(json.dumps({"passed": 100, "failed": 0}))
        (tmp_path / "outputs" / "dependency_audit.json").write_text(
            json.dumps({"declared": ["a"], "used_packages": ["a"], "missing": [], "unused": []})
        )
        (tmp_path / "outputs" / "alert_report.json").write_text(json.dumps({"alerts": []}))
        (tmp_path / "coverage.xml").write_text('<coverage line-rate="0.95"></coverage>')
        obs_mod.REPO_ROOT = tmp_path
        obs_mod.main()
        mock_streamlit.title.assert_called()
        assert mock_streamlit.metric.call_count >= 4


class TestLoadJsonObs:
    def test_load_json(self, tmp_path):
        from src.observability_dashboard import load_json

        f = tmp_path / "test.json"
        f.write_text(json.dumps({"k": "v"}))
        assert load_json(f) == {"k": "v"}

    def test_load_json_missing(self, tmp_path):
        from src.observability_dashboard import load_json

        result = load_json(tmp_path / "missing.json")
        assert result == {}
