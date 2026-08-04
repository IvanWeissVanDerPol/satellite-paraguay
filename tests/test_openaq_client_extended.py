"""Extended tests for src/external/openaq_client.py.

Coverage target: 90%+. Tests all retry paths, parameter mapping,
aggregation, and synthetic data generation.
"""
import json
import pytest
from unittest.mock import patch, MagicMock


class TestRequestWithRetry:
    """Tests for _request_with_retry function."""

    def test_successful_request(self):
        from src.external.openaq_client import _request_with_retry
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"results": []}

        with patch("src.external.openaq_client.requests.get", return_value=mock_response):
            result = _request_with_retry("http://test.com")
        assert result == {"results": []}

    def test_404_returns_none(self):
        from src.external.openaq_client import _request_with_retry
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.text = "Not found"

        with patch("src.external.openaq_client.requests.get", return_value=mock_response):
            result = _request_with_retry("http://test.com")
        assert result is None

    def test_410_returns_none(self):
        from src.external.openaq_client import _request_with_retry
        mock_response = MagicMock()
        mock_response.status_code = 410
        mock_response.text = "Gone"

        with patch("src.external.openaq_client.requests.get", return_value=mock_response):
            result = _request_with_retry("http://test.com")
        assert result is None

    def test_500_returns_none(self):
        from src.external.openaq_client import _request_with_retry
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.text = "Server error"

        with patch("src.external.openaq_client.requests.get", return_value=mock_response):
            result = _request_with_retry("http://test.com")
        assert result is None

    def test_rate_limited_retries(self):
        """429 should trigger retry logic."""
        from src.external.openaq_client import _request_with_retry
        # First 429, then 200
        mock_429 = MagicMock()
        mock_429.status_code = 429
        mock_200 = MagicMock()
        mock_200.status_code = 200
        mock_200.json.return_value = {"ok": True}

        responses = [mock_429, mock_200]

        def side_effect(*args, **kwargs):
            return responses.pop(0)

        with patch("src.external.openaq_client.requests.get", side_effect=side_effect):
            with patch("src.external.openaq_client.time.sleep") as mock_sleep:
                result = _request_with_retry("http://test.com", max_retries=3)
        assert result == {"ok": True}

    def test_request_exception_retries(self):
        """Connection errors should trigger retries."""
        from src.external.openaq_client import _request_with_retry
        import requests

        mock_success = MagicMock()
        mock_success.status_code = 200
        mock_success.json.return_value = {"ok": True}

        with patch("src.external.openaq_client.requests.get") as mock_get:
            # First 2 calls raise, 3rd succeeds
            mock_get.side_effect = [
                requests.ConnectionError("net"),
                requests.ConnectionError("net"),
                mock_success,
            ]
            with patch("src.external.openaq_client.time.sleep"):
                result = _request_with_retry("http://test.com", max_retries=3)
        assert result == {"ok": True}

    def test_all_retries_fail_returns_none(self):
        """When all retries fail, returns None."""
        from src.external.openaq_client import _request_with_retry
        import requests
        with patch("src.external.openaq_client.requests.get") as mock_get:
            mock_get.side_effect = requests.ConnectionError("net")
            with patch("src.external.openaq_client.time.sleep"):
                result = _request_with_retry("http://test.com", max_retries=2)
        assert result is None


class TestParameterId:
    """Tests for _parameter_id function."""

    def test_known_parameters(self):
        from src.external.openaq_client import _parameter_id
        assert _parameter_id("pm25") > 0
        assert _parameter_id("pm10") > 0
        assert _parameter_id("o3") > 0

    def test_unknown_parameter_returns_default(self):
        from src.external.openaq_client import _parameter_id
        result = _parameter_id("unknown_xyz")
        # Should return a default value
        assert isinstance(result, int)


class TestAggregateByMonth:
    """Tests for aggregate_by_month function."""

    def test_aggregate_with_dates(self):
        import pandas as pd
        from src.external.openaq_client import aggregate_by_month
        df = pd.DataFrame({
            "date_utc": pd.to_datetime(["2024-01-15", "2024-01-20", "2024-02-10"]),
            "value": [10, 20, 30],
        })
        result = aggregate_by_month(df, "value")
        assert len(result) == 2  # 2 months
        assert "mean" in result.columns

    def test_aggregate_empty(self):
        import pandas as pd
        from src.external.openaq_client import aggregate_by_month
        df = pd.DataFrame()
        result = aggregate_by_month(df, "value")
        assert result.empty


class TestGenerateSyntheticOpenaq:
    """Tests for generate_synthetic_openaq function."""

    def test_generate_default(self):
        import pandas as pd
        from src.external.openaq_client import generate_synthetic_openaq
        df = generate_synthetic_openaq()
        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0

    def test_generate_for_station(self):
        import pandas as pd
        from src.external.openaq_client import generate_synthetic_openaq_for_station
        df = generate_synthetic_openaq_for_station(-25.3, -57.6, parameter="pm25")
        assert isinstance(df, pd.DataFrame)
        assert "pm25" in df.columns or "value" in df.columns

    def test_generate_for_station_no2(self):
        import pandas as pd
        from src.external.openaq_client import generate_synthetic_openaq_for_station
        df = generate_synthetic_openaq_for_station(-25.3, -57.6, parameter="no2")
        assert isinstance(df, pd.DataFrame)


class TestFetchOpenaqForLocation:
    """Tests for fetch_openaq_for_location function."""

    def test_fetch_returns_dataframe_or_none(self):
        from src.external.openaq_client import fetch_openaq_for_location
        # No network — should fall back to synthetic DataFrame
        import pandas as pd
        result = fetch_openaq_for_location(-25.3, -57.6, parameter="pm25")
        assert result is None or isinstance(result, pd.DataFrame)


class TestFetchOpenaqAsuncion:
    """Tests for fetch_openaq_asuncion function."""

    def test_fetch_asuncion(self):
        from src.external.openaq_client import fetch_openaq_asuncion
        # No network — should fall back to synthetic DataFrame
        import pandas as pd
        result = fetch_openaq_asuncion(parameter="pm25")
        assert result is None or isinstance(result, pd.DataFrame)


class TestModuleConstants:
    def test_user_agent_defined(self):
        from src.external import openaq_client
        assert openaq_client.USER_AGENT is not None


class TestFetchOpenaqWithApiKey:
    """Tests for fetch_openaq_for_location with API key (mocked)."""

    def test_fetch_with_api_key_success(self, tmp_path, monkeypatch):
        from src.external import openaq_client
        monkeypatch.setattr(openaq_client, "CACHE_DIR", tmp_path)

        # Mock _request_with_retry to return fake data
        def fake_request(url, params=None, headers=None, max_retries=3):
            if "locations" in url:
                return {
                    "results": [
                        {"id": "loc1", "name": "Asunción Centro"},
                        {"id": "loc2", "name": "Fernando de la Mora"},
                    ]
                }
            elif "measurements" in url:
                return {
                    "results": [
                        {
                            "value": 25.5,
                            "period": {"datetimeFrom": {"utc": "2024-01-15T10:00:00Z"}},
                        },
                        {
                            "value": 30.2,
                            "period": {"datetimeFrom": {"utc": "2024-02-20T12:00:00Z"}},
                        },
                    ]
                }
            return None

        monkeypatch.setattr(openaq_client, "_request_with_retry", fake_request)

        result = openaq_client.fetch_openaq_for_location(
            -25.3, -57.6, parameter="pm25", api_key="test_key"
        )
        assert result is not None
        assert len(result) > 0

    def test_fetch_with_api_key_no_locations(self, tmp_path, monkeypatch):
        from src.external import openaq_client
        monkeypatch.setattr(openaq_client, "CACHE_DIR", tmp_path)

        def fake_request(url, params=None, headers=None, max_retries=3):
            return {"results": []}

        monkeypatch.setattr(openaq_client, "_request_with_retry", fake_request)

        result = openaq_client.fetch_openaq_for_location(
            -25.3, -57.6, parameter="pm25", api_key="test_key"
        )
        # No locations -> falls back to synthetic
        assert result is not None

    def test_fetch_cache_hit(self, tmp_path, monkeypatch):
        from src.external import openaq_client
        monkeypatch.setattr(openaq_client, "CACHE_DIR", tmp_path)

        # Pre-populate cache
        import pandas as pd
        cache_data = pd.DataFrame({
            "date_utc": pd.to_datetime(["2024-01-15"]),
            "value": [25.5],
        })
        cache_file = tmp_path / "openaq_-25.3_-57.6_pm25_2024-01-01_2024-12-31.json"
        cache_data.to_json(cache_file)

        result = openaq_client.fetch_openaq_for_location(
            -25.3, -57.6, parameter="pm25",
            date_from="2024-01-01", date_to="2024-12-31",
        )
        assert result is not None


class TestFetchAsuncionExtended:
    """Extended tests for fetch_openaq_asuncion."""

    def test_fetch_asuncion_basic(self, tmp_path, monkeypatch):
        from src.external import openaq_client
        monkeypatch.setattr(openaq_client, "CACHE_DIR", tmp_path)

        def fake_request(url, params=None, headers=None, max_retries=3):
            return {"results": [{"id": "loc1", "name": "Test"}]}

        monkeypatch.setattr(openaq_client, "_request_with_retry", fake_request)

        result = openaq_client.fetch_openaq_asuncion(parameter="pm25", days=30)
        assert result is not None
