"""Integration tests exercising the public API surface.

These tests verify that the modules can be imported, instantiated,
and used end-to-end without crashes (smoke tests for the full pipeline).
"""

import pytest  # noqa: E402

pytest.importorskip("geopandas", reason="CI: requires optional system dep 'geopandas' (not installed)")  # noqa: E402

from pathlib import Path  # noqa: E402
from unittest.mock import MagicMock  # noqa: E402

import numpy as np  # noqa: E402
import pytest  # noqa: E402


class TestUtilsImports:
    """Verify utils module imports work."""

    def test_imports_reproducibility(self):
        from src.utils.reproducibility import (
            set_seed,
        )

        assert set_seed is not None
        assert callable(set_seed)

    def test_imports_mlflow(self):
        from src.utils.mlflow_tracking import setup_mlflow

        assert setup_mlflow is not None

    def test_imports_secrets(self):
        # Just check utils package imports
        import src.utils

        assert src.utils is not None


class TestEndToEndSmoke:
    """Smoke tests for the full pipeline."""

    def test_yvytu_pipeline_full_init(self):
        """YvytuPipeline initializes cleanly."""
        from src.papers.p0011_yvytu_deforestation.pipeline import YvytuPipeline

        p = YvytuPipeline()
        assert p.config is not None
        assert p.model is None

    def test_yrupe_pipeline_full_init(self):
        from src.papers.p0025_yrupe_yield.pipeline import YrupePipeline

        p = YrupePipeline()
        assert p.config is not None

    def test_kai_pipeline_full_init(self):
        from src.papers.p0026_kai_poaching.pipeline import KaiPipeline

        p = KaiPipeline()
        assert p.config is not None

    def test_yvy_pipeline_full_init(self):
        from src.papers.p0012_yvy_indigenous.pipeline import YvyPipeline

        p = YvyPipeline()
        assert p.config is not None

    def test_tatakua_pipeline_full_init(self):
        from src.papers.p0035_tatakua_air_quality.pipeline import TatakuaPipeline

        p = TatakuaPipeline()
        assert p.config is not None

    def test_yvyra_pipeline_full_init(self):
        from src.papers.p0100_yvyra_carbon_credits.pipeline import YvyraPipeline

        p = YvyraPipeline()
        assert p.config is not None


class TestDataFlow:
    """End-to-end data flow tests."""

    def test_ndvi_to_carbon(self):
        """NDVI → AGB conversion roundtrip."""
        from scripts.per_pixel_carbon import chave_agb

        ndvi = np.random.rand(20, 20).astype(np.float32) * 100  # tree cover %
        agb = chave_agb(ndvi)
        assert agb.shape == ndvi.shape
        assert np.all(agb >= 0)

    def test_yvytu_pipeline_to_mask(self):
        """NDVI time series → deforestation mask."""
        from src.papers.p0011_yvytu_deforestation.pipeline import YvytuPipeline

        p = YvytuPipeline()
        p.model = MagicMock()
        # Time series with a sharp drop
        ndvi = np.full((15, 30, 30), 0.7, dtype=np.float32)
        ndvi[7:, :, :] = 0.2
        dates = [f"2024-{m:02d}-01" for m in range(1, 16)]
        mask = p.detect_deforestation("TILE", ndvi, dates)
        assert mask.sum() > 0


class TestCarbonCalculations:
    """Test carbon calculation pipeline."""

    def test_agb_to_carbon(self):
        """AGB → biomass carbon → CO2 conversion."""
        from scripts.per_pixel_carbon import chave_agb

        # 100% tree cover
        agb = chave_agb(np.array([[100.0]]))
        # Should produce positive carbon
        assert agb[0, 0] > 0


class TestModuleConstants:
    """Test module-level constants."""

    def test_paraguay_admin_constants(self):
        from src.paraguay_admin import real_analysis

        assert isinstance(real_analysis.PG_DATA_DIR, Path)

    def test_foundation_models_constants(self):
        from src.foundation_models import models

        assert isinstance(models.DEFAULT_CACHE_DIR, Path)

    def test_external_init(self):
        import src.external

        assert src.external is not None

    def test_papers_init(self):
        import src.papers

        assert src.papers is not None


class TestPipelineImports:
    """Test that all paper pipeline modules can be imported."""

    @pytest.mark.parametrize(
        "paper_name",
        [
            "p0011_yvytu_deforestation",
            "p0012_yvy_indigenous",
            "p0025_yrupe_yield",
            "p0026_kai_poaching",
            "p0035_tatakua_air_quality",
            "p0100_yvyra_carbon_credits",
        ],
    )
    def test_import_paper_module(self, paper_name):
        """Each paper module should import without errors."""
        import importlib

        mod = importlib.import_module(f"src.papers.{paper_name}")
        assert mod is not None

    @pytest.mark.parametrize(
        "paper_name,class_name",
        [
            ("p0011_yvytu_deforestation", "YvytuPipeline"),
            ("p0012_yvy_indigenous", "YvyPipeline"),
            ("p0025_yrupe_yield", "YrupePipeline"),
            ("p0026_kai_poaching", "KaiPipeline"),
            ("p0035_tatakua_air_quality", "TatakuaPipeline"),
            ("p0100_yvyra_carbon_credits", "YvyraPipeline"),
        ],
    )
    def test_paper_class_instantiation(self, paper_name, class_name):
        """Each paper class should instantiate."""
        import importlib

        mod = importlib.import_module(f"src.papers.{paper_name}.pipeline")
        cls = getattr(mod, class_name)
        instance = cls()
        assert instance is not None
