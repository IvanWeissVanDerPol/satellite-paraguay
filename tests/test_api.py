"""Tests for FastAPI endpoints."""

from src.api.main import app
from fastapi.testclient import TestClient
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))


client = TestClient(app)


def test_health():
    """Health endpoint returns healthy."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "endpoints" in data


def test_summary():
    """Summary endpoint returns expected fields."""
    response = client.get("/summary")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Multi-Temporal Satellite Computer Vision for Paraguay"
    assert "findings" in data
    assert data["findings"]["indigenous_disparity"] == 3.3
    assert data["findings"]["verra_discrepancy_pct"] == 35


def test_departments():
    """Departments endpoint returns list."""
    response = client.get("/departments")
    assert response.status_code == 200
    depts = response.json()
    assert isinstance(depts, list)
    assert len(depts) >= 5
    assert any(d["name"] == "Alto Paraguay" for d in depts)


def test_territories():
    """Territories endpoint returns list."""
    response = client.get("/territories")
    assert response.status_code == 200
    territories = response.json()
    assert isinstance(territories, list)
    assert len(territories) >= 6
    # Verify headline finding
    carmelo = next(t for t in territories if t["name"] == "Carmelo Peralta")
    assert carmelo["loss_pct"] > 49  # ~49.45%


def test_verra():
    """Verra endpoint returns 5 projects."""
    response = client.get("/verra")
    assert response.status_code == 200
    projects = response.json()
    assert len(projects) == 5
    # Verify discrepancy is positive
    for p in projects:
        assert p["hansen_co2e_mt"] > p["verra_co2e_mt"]
        assert p["discrepancy_pct"] > 0


def test_models():
    """Models endpoint returns expected metrics."""
    response = client.get("/models")
    assert response.status_code == 200
    models = response.json()
    assert any(m["name"] == "persistence" for m in models)
    assert any(m["name"] == "prithvi_lite" for m in models)


def test_carbon():
    """Carbon endpoint returns annual data."""
    response = client.get("/carbon")
    assert response.status_code == 200
    data = response.json()
    # May be empty if not yet run, but should be a list
    assert isinstance(data, list)


def test_uncertainty():
    """Uncertainty endpoint returns bootstrap CIs."""
    response = client.get("/uncertainty")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_docs_available():
    """OpenAPI docs are available."""
    response = client.get("/docs")
    assert response.status_code == 200


def test_openapi_schema():
    """OpenAPI schema is valid."""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    schema = response.json()
    assert "paths" in schema
    assert "/health" in schema["paths"]
    assert "/departments" in schema["paths"]
    assert "/territories" in schema["paths"]
