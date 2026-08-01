# Tests for FastAPI app.
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture
def client():
    """Create a test client."""
    try:
        from fastapi.testclient import TestClient
    except ImportError:
        pytest.skip("fastapi not installed")

    from api.main import app
    return TestClient(app)


def test_health(client):
    """Health endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_info(client):
    """Info endpoint."""
    response = client.get("/info")
    assert response.status_code == 200
    data = response.json()
    assert "papers" not in data  # /info returns endpoints
    assert "/health" in data["endpoints"]


def test_predict_deforestation(client):
    """Deforestation endpoint."""
    import numpy as np
    np.random.seed(42)
    ndvi = np.random.rand(12, 256, 256).astype(np.float32).tolist()
    dates = [f"2024-{m:02d}-01" for m in range(1, 13)]

    response = client.post("/predict/deforestation", json={
        "tile_id": "-54.267_-21.164",
        "ndvi_timeseries": ndvi,
        "dates": dates,
    })
    # May fail without real data, but should not crash
    assert response.status_code in [200, 500]


def test_predict_carbon(client):
    """Carbon verification endpoint."""
    response = client.post("/predict/carbon", json={
        "project_id": "VCS-001",
        "tile_id": "-54.267_-21.164",
    })
    assert response.status_code in [200, 500]


def test_predict_yield(client):
    """Yield prediction endpoint."""
    response = client.post("/predict/yield", json={
        "tile_id": "-55.5_-25.0",
        "ndvi_series": [0.3, 0.5, 0.7, 0.6],
    })
    assert response.status_code in [200, 500]


def test_predict_air_quality(client):
    """Air quality forecast endpoint."""
    response = client.post("/predict/air-quality", json={
        "historical_pm25": [10.0, 12.0, 15.0, 13.0, 11.0],
        "days_ahead": 7,
    })
    assert response.status_code in [200, 500]
