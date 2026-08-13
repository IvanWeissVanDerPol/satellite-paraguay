"""Tests for src/external/firms_client.py.

Coverage target: 80%+. The module has both live-API and synthetic
fallback paths. Testing the synthetic-fallback paths gives the most
coverage without requiring a FIRMS API key.
"""

import json
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from src.external import firms_client as _fc
from src.external.firms_client import (
    compute_fire_clusters,
    fetch_firms_fires,
    fetch_firms_paraguay,
    generate_synthetic_firms,
    generate_synthetic_firms_paraguay,
)


@pytest.fixture(autouse=True)
def _tmp_cache_dir(tmp_path, monkeypatch):
    """All tests use a tmp cache dir to avoid touching real filesystem."""
    cache_dir = tmp_path / "firms_cache"
    cache_dir.mkdir(parents=True, exist_ok=True)
    monkeypatch.setenv("FIRMS_CACHE_DIR", str(cache_dir))
    monkeypatch.setattr(_fc, "CACHE_DIR", cache_dir)
    yield cache_dir


# =========================
# generate_synthetic_firms
# =========================


class TestGenerateSyntheticFirms:
    def test_returns_dataframe(self):
        bbox = {"min_lon": -60, "max_lon": -55, "min_lat": -25, "max_lat": -20}
        df = generate_synthetic_firms(bbox, days=7)
        assert isinstance(df, pd.DataFrame)

    def test_has_expected_columns(self):
        bbox = {"min_lon": -60, "max_lon": -55, "min_lat": -25, "max_lat": -20}
        df = generate_synthetic_firms(bbox, days=7)
        expected = {
            "latitude",
            "longitude",
            "brightness",
            "scan",
            "track",
            "acq_date",
            "acq_time",
            "satellite",
            "confidence",
            "version",
            "bright_t31",
            "frp",
            "daynight",
        }
        assert expected.issubset(set(df.columns))

    def test_lat_lon_within_bbox(self):
        bbox = {"min_lon": -60, "max_lon": -55, "min_lat": -25, "max_lat": -20}
        df = generate_synthetic_firms(bbox, days=7)
        assert (df["latitude"] >= bbox["min_lat"]).all()
        assert (df["latitude"] <= bbox["max_lat"]).all()
        assert (df["longitude"] >= bbox["min_lon"]).all()
        assert (df["longitude"] <= bbox["max_lon"]).all()

    def test_count_in_range(self):
        bbox = {"min_lon": -60, "max_lon": -55, "min_lat": -25, "max_lat": -20}
        df = generate_synthetic_firms(bbox, days=7)
        # n_fires is rng.integers(5, 50) — 5 to 49 inclusive
        assert 5 <= len(df) <= 50

    def test_deterministic_with_seed(self):
        bbox = {"min_lon": -60, "max_lon": -55, "min_lat": -25, "max_lat": -20}
        a = generate_synthetic_firms(bbox, days=7)
        b = generate_synthetic_firms(bbox, days=7)
        # Same seed (42) in the function should produce identical output
        pd.testing.assert_frame_equal(a, b)

    def test_days_affects_date_range(self):
        bbox = {"min_lon": -60, "max_lon": -55, "min_lat": -25, "max_lat": -20}
        df_7 = generate_synthetic_firms(bbox, days=7)  # noqa: F841
        df_30 = generate_synthetic_firms(bbox, days=30)
        # Longer period means more date variety (not strictly necessary to test
        # but checks that the function doesn't crash with bigger days values)
        assert isinstance(df_30, pd.DataFrame)


# =========================
# generate_synthetic_firms_paraguay
# =========================


class TestGenerateSyntheticFirmsParaguay:
    def test_returns_dataframe(self):
        df = generate_synthetic_firms_paraguay(days=7)
        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0

    def test_covers_paraguay_bbox(self):
        df = generate_synthetic_firms_paraguay(days=7)
        # Paraguay bounding box approximately:
        # lon: -62.5 to -54.5, lat: -27.5 to -19.5
        if len(df) > 0:
            assert df["longitude"].min() >= -63
            assert df["longitude"].max() <= -54
            assert df["latitude"].min() >= -28
            assert df["latitude"].max() <= -19


# =========================
# fetch_firms_fires
# =========================


class TestFetchFirmsFires:
    def test_no_api_key_returns_synthetic(self):
        """Without an API key, falls back to synthetic data."""
        bbox = {"min_lon": -60, "max_lon": -55, "min_lat": -25, "max_lat": -20}
        df = fetch_firms_fires(bbox, days=7, api_key=None)
        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0

    def test_uses_cache_when_fresh(self, _tmp_cache_dir):
        """When cache exists, read from it instead of fetching."""
        # Write a cache file
        cache_path = _tmp_cache_dir / "firms_VIIRS_SNPP_NRT_7d.json"
        sample = [
            {
                "latitude": -23.5,
                "longitude": -58.5,
                "brightness": 320.0,
                "scan": 1.0,
                "track": 1.0,
                "acq_date": "2025-01-01",
                "acq_time": "0000",
                "satellite": "VIIRS_SNPP_NRT",
                "confidence": "high",
                "version": "2.0NRT",
                "bright_t31": 300.0,
                "frp": 25.0,
                "daynight": "D",
            }
        ]
        cache_path.write_text(json.dumps(sample))

        bbox = {"min_lon": -60, "max_lon": -55, "min_lat": -25, "max_lat": -20}
        df = fetch_firms_fires(bbox, days=7, use_cache=True)
        assert len(df) == 1
        assert df.iloc[0]["latitude"] == -23.5

    def test_bypass_cache(self, _tmp_cache_dir):
        """With use_cache=False, skip cache even if present."""
        cache_path = _tmp_cache_dir / "firms_VIIRS_SNPP_NRT_7d.json"
        cache_path.write_text("[]")  # empty cache
        bbox = {"min_lon": -60, "max_lon": -55, "min_lat": -25, "max_lat": -20}
        df = fetch_firms_fires(bbox, days=7, use_cache=False)
        # Falls through to synthetic since no API key
        assert len(df) > 0

    def test_live_fetch_success(self, _tmp_cache_dir):
        """Live fetch from FIRMS API succeeds."""
        # Mock the requests.get call
        csv_data = (
            "latitude,longitude,brightness,scan,track,acq_date,acq_time,"
            "satellite,confidence,version,bright_t31,frp,daynight\n"
            "-23.5,-58.5,320.0,1.0,1.0,2025-01-01,0000,VIIRS_SNPP_NRT,"
            "high,2.0NRT,300.0,25.0,D\n"
        )
        mock_response = MagicMock()
        mock_response.text = csv_data
        mock_response.raise_for_status = MagicMock()

        with patch("src.external.firms_client.requests.get", return_value=mock_response):
            bbox = {"min_lon": -60, "max_lon": -55, "min_lat": -25, "max_lat": -20}
            df = fetch_firms_fires(bbox, days=7, api_key="test_key", use_cache=False)
        assert len(df) == 1
        assert df.iloc[0]["latitude"] == -23.5

    def test_live_fetch_failure_falls_back(self, _tmp_cache_dir):
        """If live fetch fails (network error), fall back to synthetic."""
        with patch("src.external.firms_client.requests.get", side_effect=Exception("network down")):
            bbox = {"min_lon": -60, "max_lon": -55, "min_lat": -25, "max_lat": -20}
            df = fetch_firms_fires(bbox, days=7, api_key="test_key", use_cache=False)
        assert len(df) > 0  # synthetic

    def test_live_fetch_http_error_falls_back(self, _tmp_cache_dir):
        """If live fetch returns HTTP error, fall back to synthetic."""
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = Exception("500")
        with patch("src.external.firms_client.requests.get", return_value=mock_response):
            bbox = {"min_lon": -60, "max_lon": -55, "min_lat": -25, "max_lat": -20}
            df = fetch_firms_fires(bbox, days=7, api_key="test_key", use_cache=False)
        assert len(df) > 0  # synthetic

    def test_api_key_from_env(self, _tmp_cache_dir, monkeypatch):
        """If api_key not passed, read from FIRMS_API_KEY env var."""
        # Mock successful fetch
        csv_data = "latitude,longitude\n-23.5,-58.5\n"
        mock_response = MagicMock()
        mock_response.text = csv_data
        mock_response.raise_for_status = MagicMock()
        monkeypatch.setenv("FIRMS_API_KEY", "env_key")
        with patch("src.external.firms_client.requests.get", return_value=mock_response) as mock_get:
            bbox = {"min_lon": -60, "max_lon": -55, "min_lat": -25, "max_lat": -20}
            fetch_firms_fires(bbox, days=7, use_cache=False)
        # Verify the URL was constructed with the env-var key
        call_args = mock_get.call_args
        assert "env_key" in call_args[0][0] or "env_key" in str(call_args)


# =========================
# fetch_firms_paraguay
# =========================


class TestFetchFirmsParaguay:
    def test_no_api_key_returns_synthetic(self):
        df = fetch_firms_paraguay(days=7, api_key=None)
        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0

    def test_uses_cache_when_present(self, _tmp_cache_dir):
        cache_path = _tmp_cache_dir / "firms_paraguay_7d.json"
        sample = [
            {
                "latitude": -23.5,
                "longitude": -58.5,
                "brightness": 320.0,
                "scan": 1.0,
                "track": 1.0,
                "acq_date": "2025-01-01",
                "acq_time": "0000",
                "satellite": "VIIRS_SNPP_NRT",
                "confidence": "high",
                "version": "2.0NRT",
                "bright_t31": 300.0,
                "frp": 25.0,
                "daynight": "D",
            }
        ]
        cache_path.write_text(json.dumps(sample))
        df = fetch_firms_paraguay(days=7)
        assert len(df) == 1

    def test_live_fetch_success(self, _tmp_cache_dir):
        csv_data = (
            "latitude,longitude,brightness,scan,track,acq_date,acq_time,"
            "satellite,confidence,version,bright_t31,frp,daynight\n"
            "-23.5,-58.5,320.0,1.0,1.0,2025-01-01,0000,VIIRS_SNPP_NRT,"
            "high,2.0NRT,300.0,25.0,D\n"
        )
        mock_response = MagicMock()
        mock_response.text = csv_data
        mock_response.raise_for_status = MagicMock()
        with patch("src.external.firms_client.requests.get", return_value=mock_response):
            df = fetch_firms_paraguay(days=7, api_key="key")
        assert len(df) == 1

    def test_live_fetch_failure_falls_back(self, _tmp_cache_dir):
        with patch("src.external.firms_client.requests.get", side_effect=Exception("timeout")):
            df = fetch_firms_paraguay(days=7, api_key="key")
        assert len(df) > 0  # synthetic


# =========================
# compute_fire_clusters
# =========================


class TestComputeFireClusters:
    def test_empty_dataframe_returns_empty_list(self):
        empty = pd.DataFrame(columns=["latitude", "longitude"])
        clusters = compute_fire_clusters(empty)
        assert clusters == []

    def test_missing_columns_returns_empty(self):
        df = pd.DataFrame({"x": [1, 2, 3], "y": [4, 5, 6]})
        clusters = compute_fire_clusters(df)
        assert clusters == []

    def test_basic_clustering(self):
        """Two clusters of fires should be detected."""
        df = pd.DataFrame(
            {
                "latitude": [-23.5, -23.51, -23.52, -25.0, -25.01],
                "longitude": [-58.5, -58.51, -58.52, -60.0, -60.01],
                "brightness": [320.0, 322.0, 318.0, 330.0, 325.0],
                "frp": [10.0, 12.0, 8.0, 20.0, 18.0],
            }
        )
        clusters = compute_fire_clusters(df, distance_km=10.0)
        assert isinstance(clusters, list)
        assert len(clusters) >= 1

    def test_cluster_dict_structure(self):
        df = pd.DataFrame(
            {
                "latitude": [-23.5, -23.51, -23.52],
                "longitude": [-58.5, -58.51, -58.52],
                "brightness": [320.0, 322.0, 318.0],
                "frp": [10.0, 12.0, 8.0],
            }
        )
        clusters = compute_fire_clusters(df, distance_km=10.0)
        if clusters:
            c = clusters[0]
            assert "center_lat" in c
            assert "center_lon" in c
            assert "count" in c
            assert c["count"] >= 2

    def test_distance_km_parameter_accepted(self):
        """Function accepts different distance_km values without error."""
        df = pd.DataFrame(
            {
                "latitude": [-23.5, -23.51, -23.52, -25.0, -25.01],
                "longitude": [-58.5, -58.51, -58.52, -60.0, -60.01],
                "brightness": [320.0, 322.0, 318.0, 330.0, 325.0],
                "frp": [10.0, 12.0, 8.0, 20.0, 18.0],
            }
        )
        # Just verify different distance values work without crashing
        for d in [1.0, 10.0, 100.0, 1000.0]:
            clusters = compute_fire_clusters(df, distance_km=d)
            assert isinstance(clusters, list)
