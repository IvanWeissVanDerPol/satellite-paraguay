"""Tests for src.papers pipelines."""

import pytest  # noqa: E402

pytest.importorskip("rasterio", reason="CI: requires optional system dep 'rasterio' (not installed)")  # noqa: E402

import os  # noqa: E402
import sys  # noqa: E402
from pathlib import Path  # noqa: E402

import pytest  # noqa: E402

sys.path.insert(0, str(Path(__file__).parent.parent))


# 2026-08-13: Skip tests that need paraguay-geodata when it isn't readable.
_DATA_DIR = Path(os.environ.get("PARAGUAY_GEODATA_DIR", "/root/paraguay-geodata/exports/web/data"))
try:
    _HAS_DATA = os.access(_DATA_DIR, os.R_OK) and _DATA_DIR.is_dir()
except (PermissionError, OSError):
    _HAS_DATA = False


def test_yvutu_pipeline_instantiates():
    """P0011 pipeline can be created.

    Note (2026-09-08, Round-12 audit): the live directory is
    p0011_yvytu_deforestation (y-v-u-t-y, double-y). The duplicate
    p0011_yvytu_deforestation directory (y-v-u-t-u) is being
    consolidated in Phase 9; for now the live import uses the
    actual class name `YvytuPipeline` (not the typo'd version).
    """
    from src.papers.p0011_yvytu_deforestation import YvytuPipeline

    pipeline = YvytuPipeline()
    assert pipeline is not None
    assert pipeline.config is not None


# NOTE: test_yvyra_pipeline_instantiates removed in Round-12 (P0010
# Yvyra was np.random.normal fabrication).


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


def test_yvutu_select_chaco_tiles():
    """P0011 selects Chaco tiles."""
    if not _HAS_DATA:
        pytest.skip("paraguay-geodata not readable (set PARAGUAY_GEODATA_DIR)")
    from src.papers.p0011_yvytu_deforestation import YvytuPipeline

    pipeline = YvytuPipeline()
    tiles = pipeline.select_tiles()
    # Should return a list (possibly empty if paraguay-geodata missing)
    assert isinstance(tiles, list)


# NOTE: test_yvyra_fetch_verra removed in Round-12 (P0010 deleted).


def test_kai_select_defensores():
    """P0026 selects Defensores del Chaco tiles."""
    if not _HAS_DATA:
        pytest.skip("paraguay-geodata not readable (set PARAGUAY_GEODATA_DIR)")
    from src.papers.p0026_kai_poaching import KaiPipeline

    pipeline = KaiPipeline()
    tiles = pipeline.select_tiles()
    assert isinstance(tiles, list)
