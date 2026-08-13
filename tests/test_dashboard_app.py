"""Tests for src/dashboard/app.py — Streamlit dashboard.

Coverage target: 30%+. We test the pure-Python helper functions
(load_json) since streamlit page functions are not directly testable
without AppTest. The page functions are exercised via import.
"""

import json
from pathlib import Path


class TestLoadJson:
    """Tests for the load_json helper function."""

    def test_load_existing_file(self, tmp_path):
        """Load JSON from an existing file."""
        from src.dashboard.app import load_json

        test_file = tmp_path / "test.json"
        test_data = {"key": "value", "number": 42}
        test_file.write_text(json.dumps(test_data))

        result = load_json(str(test_file))
        assert result == test_data

    def test_load_missing_file_returns_none(self, tmp_path):
        """When file doesn't exist, return None."""
        from src.dashboard.app import load_json

        missing_file = tmp_path / "nonexistent.json"
        result = load_json(str(missing_file))
        assert result is None

    def test_load_empty_object(self, tmp_path):
        """Empty JSON object loads correctly."""
        from src.dashboard.app import load_json

        test_file = tmp_path / "empty.json"
        test_file.write_text("{}")
        result = load_json(str(test_file))
        assert result == {}

    def test_load_array(self, tmp_path):
        """Top-level JSON array loads correctly."""
        from src.dashboard.app import load_json

        test_file = tmp_path / "array.json"
        test_file.write_text(json.dumps([1, 2, 3, 4]))
        result = load_json(str(test_file))
        assert result == [1, 2, 3, 4]


class TestDashboardPages:
    """Test that the page functions exist and can be imported."""

    def test_page_overview_exists(self):
        """page_overview function exists."""
        from src.dashboard import app

        assert hasattr(app, "page_overview")
        assert callable(app.page_overview)

    def test_page_departments_exists(self):
        from src.dashboard import app

        assert hasattr(app, "page_departments")

    def test_page_indigenous_exists(self):
        from src.dashboard import app

        assert hasattr(app, "page_indigenous")

    def test_page_carbon_exists(self):
        from src.dashboard import app

        assert hasattr(app, "page_carbon")

    def test_page_models_exists(self):
        from src.dashboard import app

        assert hasattr(app, "page_models")

    def test_page_references_exists(self):
        from src.dashboard import app

        assert hasattr(app, "page_references")

    def test_page_uncertainty_exists(self):
        from src.dashboard import app

        assert hasattr(app, "page_uncertainty")


class TestPageExecution:
    """Test pages can be imported (execution requires Streamlit runtime)."""

    def test_pages_are_callable(self):
        """All page functions should be callable."""
        from src.dashboard import app

        for fn in [
            app.page_overview,
            app.page_departments,
            app.page_indigenous,
            app.page_carbon,
            app.page_models,
            app.page_references,
            app.page_uncertainty,
        ]:
            assert callable(fn)


class TestModuleConstants:
    """Test module-level constants."""

    def test_repo_root_is_path(self):
        from src.dashboard import app

        assert isinstance(app.REPO_ROOT, Path)

    def test_repo_root_exists(self):
        from src.dashboard import app

        assert app.REPO_ROOT.exists()
