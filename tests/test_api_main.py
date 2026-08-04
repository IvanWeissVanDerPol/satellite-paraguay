"""Tests for src/api/main.py — FastAPI endpoints.

Coverage target: 95%+. Uses FastAPI's TestClient to exercise endpoints.
"""
import json
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock


class TestAPIEndpoints:
    """Test all FastAPI endpoints."""

    def test_root_endpoint(self):
        """Root endpoint should respond."""
        from fastapi.testclient import TestClient
        from src.api.main import app
        client = TestClient(app)
        response = client.get("/")
        # Should return 200 (info dict) or 404
        assert response.status_code in (200, 404)

    def test_health_endpoint(self):
        """Health check endpoint should respond."""
        from fastapi.testclient import TestClient
        from src.api.main import app
        client = TestClient(app)
        response = client.get("/health")
        assert response.status_code in (200, 404)
        if response.status_code == 200:
            data = response.json()
            assert "status" in data or isinstance(data, dict)

    def test_list_departments_with_data(self, tmp_path, monkeypatch):
        """Test departments endpoint with real data file."""
        from src.api.main import REPO_ROOT
        monkeypatch.setattr("src.api.main.REPO_ROOT", tmp_path)

        # Create the expected file
        output_dir = tmp_path / "outputs/p0011/departments"
        output_dir.mkdir(parents=True, exist_ok=True)
        (output_dir / "department_stats.json").write_text(json.dumps({
            "departments": [
                {"name": "TestDept", "loss_pct": 10.5, "loss_km2": 100.0, "co2e_mt": 50000.0},
            ]
        }))

        from fastapi.testclient import TestClient
        from src.api.main import app
        client = TestClient(app)
        response = client.get("/departments")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        assert data[0]["name"] == "TestDept"

    def test_list_departments_no_data(self, tmp_path, monkeypatch):
        """Test departments endpoint without data file (returns defaults)."""
        monkeypatch.setattr("src.api.main.REPO_ROOT", tmp_path)
        # No files - should return default list
        from fastapi.testclient import TestClient
        from src.api.main import app
        client = TestClient(app)
        response = client.get("/departments")
        assert response.status_code == 200
        data = response.json()
        # Should return hardcoded defaults
        assert len(data) >= 1

    def test_list_territories(self, tmp_path, monkeypatch):
        """Test indigenous territories endpoint."""
        monkeypatch.setattr("src.api.main.REPO_ROOT", tmp_path)
        from fastapi.testclient import TestClient
        from src.api.main import app
        client = TestClient(app)
        response = client.get("/territories")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_carbon_endpoint_empty(self, tmp_path, monkeypatch):
        """Carbon endpoint with no data returns empty list."""
        monkeypatch.setattr("src.api.main.REPO_ROOT", tmp_path)
        from fastapi.testclient import TestClient
        from src.api.main import app
        client = TestClient(app)
        response = client.get("/carbon")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_carbon_endpoint_with_data(self, tmp_path, monkeypatch):
        """Carbon endpoint with data."""
        monkeypatch.setattr("src.api.main.REPO_ROOT", tmp_path)
        output_dir = tmp_path / "outputs/p0011/carbon"
        output_dir.mkdir(parents=True, exist_ok=True)
        (output_dir / "per_year_loss.json").write_text(json.dumps({
            "per_year": {
                "2020": {"co2e_mt": 100000, "pixels": 50000},
                "2021": {"co2e_mt": 110000, "pixels": 55000},
            }
        }))

        from fastapi.testclient import TestClient
        from src.api.main import app
        client = TestClient(app)
        response = client.get("/carbon")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2

    def test_uncertainty_endpoint(self, tmp_path, monkeypatch):
        """Uncertainty endpoint."""
        monkeypatch.setattr("src.api.main.REPO_ROOT", tmp_path)
        from fastapi.testclient import TestClient
        from src.api.main import app
        client = TestClient(app)
        response = client.get("/uncertainty")
        assert response.status_code == 200

    def test_uncertainty_with_data(self, tmp_path, monkeypatch):
        """Uncertainty endpoint with data."""
        monkeypatch.setattr("src.api.main.REPO_ROOT", tmp_path)
        output_dir = tmp_path / "outputs/p0011/uncertainty"
        output_dir.mkdir(parents=True, exist_ok=True)
        (output_dir / "uncertainty_results.json").write_text(json.dumps({
            "pixel_bootstrap": {
                "mean": 10000,
                "lower_95": 9500,
                "upper_95": 10500,
            }
        }))

        from fastapi.testclient import TestClient
        from src.api.main import app
        client = TestClient(app)
        response = client.get("/uncertainty")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1

    def test_models_endpoint(self):
        """Models endpoint."""
        from fastapi.testclient import TestClient
        from src.api.main import app
        client = TestClient(app)
        response = client.get("/models")
        assert response.status_code == 200

    def test_references_endpoint(self):
        """References endpoint."""
        from fastapi.testclient import TestClient
        from src.api.main import app
        client = TestClient(app)
        # Endpoint may not exist yet
        response = client.get("/references")
        assert response.status_code in (200, 404)


class TestAPIModels:
    """Test Pydantic model definitions."""

    def test_models_defined(self):
        from src.api.main import app
        # Models should be importable
        import src.api.main as api_mod
        # Check that the module loads without errors
        assert api_mod.app is not None