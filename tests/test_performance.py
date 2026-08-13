"""Performance benchmark suite for satellite-paraguay.

Run with:
    pytest tests/test_performance.py -m performance --no-cov -v

Uses pytest-benchmark for accurate measurements.
"""

import pytest  # noqa: E402

pytest.importorskip("rasterio", reason="CI: requires optional system dep 'rasterio' (not installed)")  # noqa: E402

import sys  # noqa: E402
import time  # noqa: E402
from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402
import pytest  # noqa: E402

sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.mark.performance
@pytest.mark.slow
class TestCarbonModelBenchmarks:
    """Benchmarks for Chave 2014 AGB model."""

    def test_chave_scalar_benchmark(self, benchmark):
        """Single scalar computation."""
        from scripts.per_pixel_carbon import chave_agb

        result = benchmark(chave_agb, 50.0)
        assert 35 < result < 50

    def test_chave_vector_benchmark(self, benchmark):
        """Vectorized computation over 4M pixels."""
        from scripts.per_pixel_carbon import chave_agb

        tc = np.random.default_rng(42).uniform(0, 100, size=(2000, 2000)).astype(np.float32)
        result = benchmark(chave_agb, tc)
        assert result.shape == (2000, 2000)

    def test_chave_huge_array(self, benchmark):
        """Large array (16M pixels)."""
        from scripts.per_pixel_carbon import chave_agb

        tc = np.random.default_rng(42).uniform(0, 100, size=(4000, 4000)).astype(np.float32)
        result = benchmark(chave_agb, tc)
        assert result.shape == (4000, 4000)


@pytest.mark.performance
@pytest.mark.slow
class TestBootstrapBenchmarks:
    """Benchmarks for bootstrap functions."""

    def test_pixel_bootstrap_100(self, benchmark):
        """100 iterations."""
        from scripts.uncertainty_quantification import pixel_bootstrap_fast

        lossyear = (np.random.default_rng(42).uniform(0, 1, (1000, 1000)) > 0.8).astype(np.uint8)
        result = benchmark(pixel_bootstrap_fast, lossyear, 100)
        assert "mean" in result

    def test_pixel_bootstrap_1000(self, benchmark):
        """1000 iterations."""
        from scripts.uncertainty_quantification import pixel_bootstrap_fast

        lossyear = (np.random.default_rng(42).uniform(0, 1, (1000, 1000)) > 0.8).astype(np.uint8)
        result = benchmark(pixel_bootstrap_fast, lossyear, 1000)
        assert "ci_lower_95" in result


@pytest.mark.performance
@pytest.mark.filterwarnings("ignore::DeprecationWarning")
class TestRasterIOLoad:
    """Benchmarks for raster loading."""

    def test_hansen_load_window(self, hansen_dir):
        """Load 2000x2000 window from Hansen tile."""
        import rasterio
        from rasterio.windows import Window

        with rasterio.open(hansen_dir / "hansen_lossyear_20S_060W.tif") as src:
            data = src.read(1, window=Window(0, 0, 2000, 2000))
        assert data.shape == (2000, 2000)


@pytest.mark.performance
class TestStatisticalTests:
    """Benchmarks for statistical tests."""

    def test_chi_squared_small(self, benchmark):
        """Small contingency table (2x2)."""
        from scipy.stats import chi2_contingency

        def run():
            obs = np.array([[100, 50], [200, 150]])
            return chi2_contingency(obs)

        benchmark(run)


@pytest.mark.performance
class TestEndToEndBenchmarks:
    """End-to-end pipeline benchmarks."""

    def test_full_chave_carbon_pipeline(self, tmp_hansen_dir):
        """Full per-pixel carbon pipeline."""
        import rasterio

        from scripts.per_pixel_carbon import chave_agb

        with rasterio.open(tmp_hansen_dir / "hansen_lossyear_20S_060W.tif") as src:
            lossyear = src.read(1)
        with rasterio.open(tmp_hansen_dir / "hansen_treecover2000_20S_060W.tif") as src:
            treecover = src.read(1)
        agb = chave_agb(treecover)
        co2e = agb * 0.47 * (44 / 12) * 0.0625
        loss_co2e = co2e * (lossyear > 0)
        result = loss_co2e.sum() / 1e6
        assert result > 0


# ========== Performance assertions ==========


@pytest.mark.performance
class TestPerformanceRegression:
    """Regression tests for performance budgets."""

    def test_chave_computation_fast(self):
        """Chave on 4M pixels should complete in < 1 second."""
        from scripts.per_pixel_carbon import chave_agb

        tc = np.random.default_rng(42).uniform(0, 100, (2000, 2000)).astype(np.float32)
        start = time.time()
        chave_agb(tc)
        elapsed = time.time() - start
        assert elapsed < 1.0, f"Chave took {elapsed:.2f}s (limit 1.0s)"

    def test_bootstrap_1000_fast(self):
        """Bootstrap 1000 iterations on 1M pixels should complete in < 2 seconds."""
        from scripts.uncertainty_quantification import pixel_bootstrap_fast

        lossyear = (np.random.default_rng(42).uniform(0, 1, (1000, 1000)) > 0.8).astype(np.uint8)
        start = time.time()
        pixel_bootstrap_fast(lossyear, n_boot=1000)
        elapsed = time.time() - start
        assert elapsed < 2.0, f"Bootstrap took {elapsed:.2f}s (limit 2.0s)"
