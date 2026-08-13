"""Tests for src/external/openaq_client.py.

Coverage target: 80%+. The module has both live API and synthetic
fallback paths.
"""

from unittest.mock import MagicMock, patch

import pandas as pd

from src.external.openaq_client import (
    _parameter_id,
    _request_with_retry,
    aggregate_by_month,
    fetch_openaq_asuncion,
    generate_synthetic_openaq,
    generate_synthetic_openaq_for_station,
)

# =========================
# _parameter_id
# =========================


class TestParameterId:
    def test_known_parameters(self):
        assert _parameter_id("pm25") == 2
        assert _parameter_id("pm10") == 1
        assert _parameter_id("no2") == 7
        assert _parameter_id("o3") == 10
        assert _parameter_id("so2") == 9
        assert _parameter_id("co") == 8
        assert _parameter_id("bc") == 23

    def test_unknown_parameter_defaults_to_pm25(self):
        """Unknown parameter names default to PM2.5 (id=2)."""
        assert _parameter_id("unknown") == 2
        assert _parameter_id("xyz") == 2
        assert _parameter_id("") == 2


# =========================
# _request_with_retry
# =========================


class TestRequestWithRetry:
    def test_returns_none_on_404(self):
        """410/404 status returns None immediately."""
        mock_response = MagicMock()
        mock_response.status_code = 404
        with patch("src.external.openaq_client.requests.get", return_value=mock_response):
            result = _request_with_retry("https://example.com")
        assert result is None

    def test_returns_none_on_410(self):
        mock_response = MagicMock()
        mock_response.status_code = 410
        with patch("src.external.openaq_client.requests.get", return_value=mock_response):
            result = _request_with_retry("https://example.com")
        assert result is None

    def test_returns_none_on_500(self):
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        with patch("src.external.openaq_client.requests.get", return_value=mock_response):
            result = _request_with_retry("https://example.com", max_retries=1)
        assert result is None

    def test_returns_json_on_200(self):
        expected = {"results": [{"value": 12.5}]}
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = expected
        with patch("src.external.openaq_client.requests.get", return_value=mock_response):
            result = _request_with_retry("https://example.com")
        assert result == expected

    def test_retries_on_429(self):
        """429 status code should trigger retry with backoff."""
        # First response: 429
        # Second response: 200 with data
        mock_429 = MagicMock()
        mock_429.status_code = 429
        mock_200 = MagicMock()
        mock_200.status_code = 200
        mock_200.json.return_value = {"results": []}

        with patch("src.external.openaq_client.requests.get", side_effect=[mock_429, mock_200]):
            with patch("src.external.openaq_client.time.sleep"):  # avoid waiting
                result = _request_with_retry("https://example.com")
        assert result == {"results": []}

    def test_returns_none_on_request_exception(self):
        import requests as _req

        with patch("src.external.openaq_client.requests.get", side_effect=_req.RequestException("connection failed")):
            with patch("src.external.openaq_client.time.sleep"):
                result = _request_with_retry("https://example.com", max_retries=1)
        assert result is None


# =========================
# generate_synthetic_openaq_for_station
# =========================


class TestGenerateSyntheticOpenAQForStation:
    def test_pm25_parameter(self):
        df = generate_synthetic_openaq_for_station(-25.26, -57.58, "pm25")
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 365  # 365 days
        assert "value" in df.columns
        assert "date_utc" in df.columns

    def test_pm25_values_seasonal(self):
        """PM2.5 should be higher in dry season (Aug-Oct) than wet season."""
        df = generate_synthetic_openaq_for_station(-25.26, -57.58, "pm25")
        df["month"] = df["date_utc"].dt.month
        # Dry season (Aug-Oct, months 8-10) should have higher values
        dry = df[df["month"].isin([8, 9, 10])]["value"].mean()
        wet = df[df["month"].isin([2, 3, 4])]["value"].mean()
        assert dry > wet  # dry season worse

    def test_no2_parameter(self):
        df = generate_synthetic_openaq_for_station(-25.26, -57.58, "no2")
        assert isinstance(df, pd.DataFrame)
        # NO2 values should be in 5-50 range per the implementation
        assert df["value"].min() >= 5
        assert df["value"].max() <= 50

    def test_o3_parameter(self):
        df = generate_synthetic_openaq_for_station(-25.26, -57.58, "o3")
        assert isinstance(df, pd.DataFrame)
        # O3 values 20-80 range
        assert df["value"].min() >= 20
        assert df["value"].max() <= 80

    def test_unknown_parameter(self):
        df = generate_synthetic_openaq_for_station(-25.26, -57.58, "unknown")
        assert isinstance(df, pd.DataFrame)
        # Falls through to default range 0-100
        assert df["value"].min() >= 0
        assert df["value"].max() <= 100

    def test_unit_pm25(self):
        df = generate_synthetic_openaq_for_station(-25.26, -57.58, "pm25")
        assert (df["unit"] == "µg/m³").all()

    def test_unit_no2(self):
        df = generate_synthetic_openaq_for_station(-25.26, -57.58, "no2")
        assert (df["unit"] == "ppb").all()

    def test_location_id_consistent(self):
        df = generate_synthetic_openaq_for_station(-25.26, -57.58, "pm25")
        # location_id should be the same for all rows (single station)
        assert df["location_id"].nunique() == 1


# =========================
# generate_synthetic_openaq
# =========================


class TestGenerateSyntheticOpenAQ:
    def test_basic_call(self):
        df = generate_synthetic_openaq(days=30)
        assert isinstance(df, pd.DataFrame)
        # Function uses Asunción coordinates and PM2.5
        assert (df["parameter"] == "pm25").all()


# =========================
# fetch_openaq_asuncion
# =========================


class TestFetchOpenAQAsuncion:
    def test_returns_dataframe(self):
        """Function returns a DataFrame (possibly empty)."""
        df = fetch_openaq_asuncion(days=7, parameter="pm25")
        assert isinstance(df, pd.DataFrame)


# =========================
# aggregate_by_month
# =========================


class TestAggregateByMonth:
    def test_empty_dataframe(self):
        df = pd.DataFrame()
        result = aggregate_by_month(df)
        assert result.equals(df)

    def test_missing_date_column(self):
        df = pd.DataFrame({"value": [1, 2, 3]})
        result = aggregate_by_month(df)
        # Returns the same df when date_utc is missing
        assert result.equals(df)

    def test_basic_aggregation(self):
        dates = pd.date_range("2025-01-01", periods=60, freq="D")
        df = pd.DataFrame(
            {
                "date_utc": dates,
                "value": list(range(60)),
            }
        )
        result = aggregate_by_month(df, value_col="value")
        assert "year_month" in result.columns
        assert "mean" in result.columns
        assert "std" in result.columns
        assert "min" in result.columns
        assert "max" in result.columns
        assert "count" in result.columns
        # 60 days spans 2 months
        assert len(result) == 3  # Jan, Feb, Mar (partial)

    def test_value_col_parameter(self):
        """Custom value column name is honored."""
        dates = pd.date_range("2025-01-01", periods=30, freq="D")
        df = pd.DataFrame(
            {
                "date_utc": dates,
                "custom_value": list(range(30)),
            }
        )
        result = aggregate_by_month(df, value_col="custom_value")
        assert "mean" in result.columns
        assert result["mean"].iloc[0] == 14.5  # mean of 0..29
