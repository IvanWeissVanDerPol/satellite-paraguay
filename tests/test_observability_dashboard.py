"""Tests for src/observability_dashboard.py — Observability dashboard.

Coverage target: 30%+. Test the load_json helper and module imports.
"""
import json
import pytest
from pathlib import Path


class TestLoadJson:
    """Tests for the load_json helper function."""

    def test_load_existing_file(self, tmp_path):
        """Load JSON from an existing file."""
        from src.observability_dashboard import load_json
        test_file = tmp_path / "test.json"
        test_data = {"key": "value", "list": [1, 2, 3]}
        test_file.write_text(json.dumps(test_data))

        result = load_json(test_file)
        assert result == test_data

    def test_load_missing_file_returns_empty_dict(self, tmp_path):
        """When file doesn't exist, return empty dict."""
        from src.observability_dashboard import load_json
        missing_file = tmp_path / "nonexistent.json"
        result = load_json(missing_file)
        assert result == {}

    def test_load_empty_object(self, tmp_path):
        """Empty JSON object loads correctly."""
        from src.observability_dashboard import load_json
        test_file = tmp_path / "empty.json"
        test_file.write_text("{}")
        result = load_json(test_file)
        assert result == {}

    def test_load_nested_dict(self, tmp_path):
        """Nested JSON loads correctly."""
        from src.observability_dashboard import load_json
        test_file = tmp_path / "nested.json"
        nested = {"a": {"b": {"c": 1}}}
        test_file.write_text(json.dumps(nested))
        result = load_json(test_file)
        assert result == nested


class TestModuleConstants:
    """Tests for module-level constants."""

    def test_repo_root_is_path(self):
        from src import observability_dashboard
        assert isinstance(observability_dashboard.REPO_ROOT, Path)

    def test_repo_root_exists(self):
        from src import observability_dashboard
        assert observability_dashboard.REPO_ROOT.exists()


class TestMainFunction:
    """Tests for the main() function (smoke test only)."""

    def test_main_exists(self):
        from src.observability_dashboard import main
        assert callable(main)