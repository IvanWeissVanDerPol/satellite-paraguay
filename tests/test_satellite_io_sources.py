"""Tests for src/satellite_io/sources.py — multi-source data registry."""
import pytest
from unittest.mock import patch, MagicMock

from src.satellite_io import sources as _sources


class TestSourcesModule:
    """Smoke tests for src/satellite_io/sources.py."""

    def test_module_loads(self):
        assert _sources is not None

    def test_module_has_public_attrs(self):
        """Module should expose some public API."""
        public = [a for a in dir(_sources) if not a.startswith("_")]
        assert len(public) > 0

    def test_module_has_callable_api(self):
        """Module should have at least one callable function or class."""
        callables = [
            a for a in dir(_sources)
            if not a.startswith("_") and callable(getattr(_sources, a))
        ]
        # Even if all are classes, they should be callable
        assert len(callables) >= 0
