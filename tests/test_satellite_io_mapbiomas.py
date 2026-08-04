"""Tests for src/satellite_io/mapbiomas.py — MapBiomas data loader."""
import pytest


class TestMapBiomasModule:
    """Smoke tests for src/satellite_io/mapbiomas.py."""

    def test_module_loads(self):
        from src.satellite_io import mapbiomas
        assert mapbiomas is not None

    def test_module_has_public_api(self):
        from src.satellite_io import mapbiomas
        public = [a for a in dir(mapbiomas) if not a.startswith("_")]
        assert len(public) > 0
