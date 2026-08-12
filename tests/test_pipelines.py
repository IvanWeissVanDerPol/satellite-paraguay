"""Tests for src.papers pipelines."""

import os
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))


# 2026-08-13: Skip tests that need paraguay-geodata when it isn't readable.
_DATA_DIR = Path(os.environ.get("PARAGUAY_GEODATA_DIR", "/root/paraguay-geodata/exports/web/data"))
try:
    _HAS_DATA = os.access(_DATA_DIR, os.R_OK) and _DATA_DIR.is_dir()
except (PermissionError, OSError):
    _HAS_DATA = False


def test_yvytu_pipeline_instantiates():
    """P0011 pipeline can be created."""
    from src.papers.p0011_yvytu_deforestation import YvytuPipeline

    pipeline = YvytuPipeline()
    assert pipeline is not None
    assert pipeline.config is not None


def test_yvyra_pipeline_instantiates():
    """P0100 pipeline can be created."""
    from src.papers.p0100_yvyra_carbon_credits import YvyraPipeline

    pipeline = YvyraPipeline()
    assert pipeline is not None


def test_yrupe_pipeline_instantiates():
    """P0025 pipeline can be created."""
    from src.papers.p0025_yrupe_yield import YrupePipeline

    pipeline = YrupePipeline()
    assert pipeline is not None


def test_yvy_pipeline_instantiates():
    """P0012 pipeline can be created."""
    from src.papers.p0012_yvy_indigenous import YvyPipeline

    pipeline = YvyPipeline()
    assert pipeline is not None
    assert pipeline.config["care_principles"] is True


def test_kai_pipeline_instantiates():
    """P0026 pipeline can be created."""
    from src.papers.p0026_kai_poaching import KaiPipeline

    pipeline = KaiPipeline()
    assert pipeline is not None


def test_tatakua_pipeline_instantiates():
    """P0035 pipeline can be created."""
    from src.papers.p0035_tatakua_air_quality import TatakuaPipeline

    pipeline = TatakuaPipeline()
    assert pipeline is not None
    assert "pm25" in pipeline.config["pollutants"]


def test_yvytu_select_chaco_tiles():
    """P0011 selects Chaco tiles."""
    if not _HAS_DATA:
        pytest.skip("paraguay-geodata not readable (set PARAGUAY_GEODATA_DIR)")
    from src.papers.p0011_yvytu_deforestation import YvytuPipeline

    pipeline = YvytuPipeline()
    tiles = pipeline.select_tiles()
    # Should return a list (possibly empty if paraguay-geodata missing)
    assert isinstance(tiles, list)


def test_yvyra_fetch_verra():
    """P0100 fetches Verra projects."""
    from src.papers.p0100_yvyra_carbon_credits import YvyraPipeline

    pipeline = YvyraPipeline()
    projects = pipeline.fetch_verra_projects()
    assert "id" in projects.columns


def test_kai_select_defensores():
    """P0026 selects Defensores del Chaco tiles."""
    if not _HAS_DATA:
        pytest.skip("paraguay-geodata not readable (set PARAGUAY_GEODATA_DIR)")
    from src.papers.p0026_kai_poaching import KaiPipeline

    pipeline = KaiPipeline()
    tiles = pipeline.select_tiles()
    assert isinstance(tiles, list)
