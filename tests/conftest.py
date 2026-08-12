"""Shared pytest fixtures and configuration for satellite-paraguay tests.

Provides:
- Repository path fixtures
- Synthetic data fixtures (Hansen, MapBiomas, Sentinel-2)
- Mock API fixtures (OpenAQ, Verra, FIRMS)
- Temporary directory fixtures
- Performance timer fixtures
- Test data versioning fixtures
"""

import os
import time
from pathlib import Path

import numpy as np
import pytest
import rasterio
from rasterio.transform import from_bounds

# ========== Path fixtures ==========


@pytest.fixture(scope="session")
def repo_root():
    """Repository root directory."""
    return Path(__file__).parent.parent.resolve()


@pytest.fixture(scope="session")
def data_dir(repo_root):
    """Data directory."""
    return repo_root / "data"


@pytest.fixture(scope="session")
def hansen_dir(data_dir):
    """Hansen data directory (skipped if not present)."""
    p = data_dir / "hansen"
    if not p.exists() or not any(p.glob("*.tif")):
        pytest.skip(f"Hansen data not found in {p}")
    return p


@pytest.fixture(scope="session")
def mapbiomas_dir(data_dir):
    """MapBiomas data directory (skipped if not present)."""
    p = data_dir / "mapbiomas"
    if not p.exists() or not any(p.glob("*.tif")):
        pytest.skip(f"MapBiomas data not found in {p}")
    return p


@pytest.fixture(scope="session")
def outputs_dir(repo_root):
    """Outputs directory."""
    p = repo_root / "outputs"
    p.mkdir(exist_ok=True)
    return p


@pytest.fixture(scope="session")
def scripts_dir(repo_root):
    """Scripts directory."""
    return repo_root / "scripts"


@pytest.fixture(scope="session")
def tests_dir():
    """Tests directory."""
    return Path(__file__).parent.resolve()


# ========== Synthetic data fixtures ==========


@pytest.fixture(scope="session")
def small_window_size():
    """Default small window size for synthetic data (2000x2000)."""
    return 2000


@pytest.fixture
def synthetic_hansen_window(small_window_size):
    """Synthetic Hansen lossyear + treecover (2000x2000) with realistic patterns."""
    rng = np.random.default_rng(42)
    H = W = small_window_size

    lossyear = np.zeros((H, W), dtype=np.uint8)
    treecover = np.full((H, W), 50, dtype=np.uint8)  # default 50% cover

    # Spatial pattern: top-left is forest, bottom-right is savanna
    for i in range(H):
        for j in range(W):
            tc = max(0, min(100, int(80 - 30 * i / H - 20 * j / W)))
            treecover[i, j] = tc
            # Add some loss pixels (random 1-5%)
            if rng.random() < 0.04:
                # Pick a year 1-23
                lossyear[i, j] = rng.integers(1, 24)
    return lossyear, treecover


@pytest.fixture
def synthetic_mapbiomas(small_window_size):
    """Synthetic MapBiomas-style classification."""
    H = W = small_window_size
    rng = np.random.default_rng(43)
    classification = np.zeros((H, W), dtype=np.uint8)
    # 50% forest (3), 30% pasture (15), 15% savanna (4), 5% water (26)
    classification = rng.choice([0, 3, 4, 15, 26], size=(H, W), p=[0.0, 0.50, 0.15, 0.30, 0.05])
    return classification


@pytest.fixture
def synthetic_indigenous_data():
    """Synthetic indigenous territory deforestation data."""
    return {
        "territories": [
            {"name": "T1", "loss_pct": 49.45, "people": "Enlhet"},
            {"name": "T2", "loss_pct": 49.43, "people": "Ayoreo"},
            {"name": "T3", "loss_pct": 46.46, "people": "Nivaclé"},
            {"name": "T4", "loss_pct": 26.98, "people": "Nivaclé"},
            {"name": "T5", "loss_pct": 25.90, "people": "Chulupi"},
            {"name": "T6", "loss_pct": 2.91, "people": "Mbyá"},
        ],
        "national_avg_pct": 8.5,
    }


@pytest.fixture
def synthetic_verra_projects():
    """Synthetic Verra projects with known discrepancy."""
    return [
        {"id": "1", "name": "Chaco A", "area_ha": 45000, "verra_claim_mt": 1.1},
        {"id": "2", "name": "Chaco B", "area_ha": 28000, "verra_claim_mt": 0.9},
        {"id": "3", "name": "Eastern A", "area_ha": 22000, "verra_claim_mt": 0.6},
        {"id": "4", "name": "Chaco C", "area_ha": 18000, "verra_claim_mt": 0.5},
        {"id": "5", "name": "Eastern B", "area_ha": 10000, "verra_claim_mt": 0.2},
    ]


# ========== File fixtures ==========


@pytest.fixture
def tmp_path_isolated(tmp_path):
    """Isolated temporary directory (cleaned up after test)."""
    return tmp_path


@pytest.fixture
def tmp_hansen_dir(tmp_path, synthetic_hansen_window):
    """Create a temporary Hansen directory with synthetic data."""
    lossyear, treecover = synthetic_hansen_window
    H, W = lossyear.shape

    hansen = tmp_path / "hansen"
    hansen.mkdir()

    # Write lossyear
    transform = from_bounds(-60.0, -20.0, -59.0, -19.0, W, H)
    profile = {
        "driver": "GTiff",
        "height": H,
        "width": W,
        "count": 1,
        "dtype": "uint8",
        "transform": transform,
        "crs": "EPSG:4326",
        "compress": "lzw",
    }
    with rasterio.open(hansen / "hansen_lossyear_20S_060W.tif", "w", **profile) as dst:
        dst.write(lossyear, 1)
    with rasterio.open(hansen / "hansen_treecover2000_20S_060W.tif", "w", **profile) as dst:
        dst.write(treecover, 1)

    return hansen


@pytest.fixture
def tmp_mapbiomas_dir(tmp_path, synthetic_mapbiomas):
    """Create a temporary MapBiomas directory with synthetic data."""
    mb = tmp_path / "mapbiomas"
    mb.mkdir()
    classification = synthetic_mapbiomas
    H, W = classification.shape
    transform = from_bounds(-60.0, -20.0, -59.0, -19.0, W, H)
    profile = {
        "driver": "GTiff",
        "height": H,
        "width": W,
        "count": 1,
        "dtype": "uint8",
        "transform": transform,
        "crs": "EPSG:4326",
        "compress": "lzw",
    }
    with rasterio.open(mb / "mapbiomas_paraguay_2023.tif", "w", **profile) as dst:
        dst.write(classification, 1)
    return mb


# ========== Performance fixtures ==========


@pytest.fixture
def performance_timer():
    """Timer fixture that records elapsed time on context exit."""

    class Timer:
        def __init__(self):
            self.start = None
            self.elapsed = None

        def __enter__(self):
            self.start = time.time()
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            self.elapsed = time.time() - self.start

    return Timer()


# ========== Logging fixtures ==========


@pytest.fixture
def log_dir(tmp_path):
    """Temporary log directory."""
    d = tmp_path / "logs"
    d.mkdir()
    return d


@pytest.fixture
def caplog_with_setup(caplog):
    """caplog with INFO level pre-configured."""
    import logging

    caplog.set_level(logging.INFO)
    return caplog


# ========== Environment fixtures ==========


@pytest.fixture(scope="session", autouse=True)
def setup_env():
    """Auto-applied env setup for all tests."""
    os.environ["SATELLITE_PARAGUAY_TEST"] = "1"
    os.environ["PYTHONHASHSEED"] = "0"
    yield
    os.environ.pop("SATELLITE_PARAGUAY_TEST", None)


@pytest.fixture
def mock_openaq_response():
    """Mock OpenAQ API response."""
    return {
        "results": [
            {
                "location": "Asunción-Centro",
                "country": "PY",
                "parameter": "pm25",
                "value": 25.4,
                "date": {"utc": "2024-01-15T12:00:00Z"},
                "coordinates": {"latitude": -25.28, "longitude": -57.63},
            },
            {
                "location": "Asunción-Centro",
                "country": "PY",
                "parameter": "pm25",
                "value": 22.1,
                "date": {"utc": "2024-01-15T11:00:00Z"},
                "coordinates": {"latitude": -25.28, "longitude": -57.63},
            },
        ]
    }


@pytest.fixture
def mock_verra_response():
    """Mock Verra registry response."""
    return {
        "projects": [
            {"id": "1", "name": "Test Project", "area_ha": 50000, "credit_count": 1000000},
            {"id": "2", "name": "Test Project B", "area_ha": 30000, "credit_count": 600000},
        ]
    }


# ========== Helpers ==========


def pytest_report_header(config):
    """Add custom header to pytest report."""
    repo_root = Path(__file__).parent.parent
    return f"satellite-paraguay tests | {repo_root}"


def pytest_collection_modifyitems(config, items):
    """Auto-mark slow tests based on naming convention."""
    for item in items:
        # Auto-mark by directory
        if "tests/integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)
        if "tests/gpu" in str(item.fspath):
            item.add_marker(pytest.mark.gpu)
            item.add_marker(pytest.mark.slow)
        if "tests/property" in str(item.fspath):
            item.add_marker(pytest.mark.property)
        if "tests/performance" in str(item.fspath):
            item.add_marker(pytest.mark.performance)
            item.add_marker(pytest.mark.slow)
        # Auto-mark by name
        if "test_e2e" in item.name or "test_full_pipeline" in item.name:
            item.add_marker(pytest.mark.integration)
            item.add_marker(pytest.mark.slow)


# Markers
def pytest_configure(config):
    config.addinivalue_line("markers", "slow: marks tests as slow (skip with -m 'not slow')")
    config.addinivalue_line("markers", "gpu: marks tests that require GPU")
    config.addinivalue_line("markers", "integration: marks integration tests")
    config.addinivalue_line("markers", "network: marks tests that require network access")
    config.addinivalue_line("markers", "property: marks property-based tests (using hypothesis)")
    config.addinivalue_line("markers", "performance: marks performance benchmark tests")
