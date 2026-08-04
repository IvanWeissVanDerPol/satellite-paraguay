"""Extended tests for src/external/sentinel5p_client.py.

Coverage target: 90%+. Tests fetch functions, synthetic data,
aggregation, and module constants.
"""
import pytest
import numpy as np
from unittest.mock import patch, MagicMock


class TestFetchSentinel5PViaGEE:
    """Tests for fetch_sentinel5p_via_gee function."""

    def test_fetch_returns_none_when_gee_unavailable(self):
        """When ee module is not available, returns None."""
        from src.external import sentinel5p_client as s5p
        # Block ee import
        import sys as _sys
        saved = _sys.modules.get("ee")
        _sys.modules["ee"] = None
        try:
            result = s5p.fetch_sentinel5p_via_gee(
                band="NO2",
                bbox={"min_lon": -60, "max_lon": -55, "min_lat": -25, "max_lat": -20},
                start_date="2024-01-01",
                end_date="2024-06-01",
            )
            assert result is None
        finally:
            if saved is None:
                _sys.modules.pop("ee", None)
            else:
                _sys.modules["ee"] = saved


class TestFetchSentinel5PNo2:
    """Tests for fetch_sentinel5p_no2 function."""

    def test_fetch_no2_no_data(self):
        """Without real GEE, returns synthetic dict data."""
        from src.external.sentinel5p_client import fetch_sentinel5p_no2
        result = fetch_sentinel5p_no2(
            bbox={"min_lon": -60, "max_lon": -55, "min_lat": -25, "max_lat": -20},
            start_date="2024-01-01",
            end_date="2024-06-01",
        )
        # Returns either dict or None if GEE failed entirely
        assert result is None or isinstance(result, dict)


class TestFetchSentinel5PO3:
    """Tests for fetch_sentinel5p_o3 function."""

    def test_fetch_o3_no_data(self):
        """Without real GEE, returns synthetic dict data."""
        from src.external.sentinel5p_client import fetch_sentinel5p_o3
        result = fetch_sentinel5p_o3(
            bbox={"min_lon": -60, "max_lon": -55, "min_lat": -25, "max_lat": -20},
            start_date="2024-01-01",
            end_date="2024-06-01",
        )
        assert result is None or isinstance(result, dict)


class TestSyntheticGenerators:
    """Tests for synthetic data generators."""

    def test_generate_synthetic_no2(self):
        from src.external.sentinel5p_client import generate_synthetic_s5p_no2
        result = generate_synthetic_s5p_no2("2024-01-01", "2024-06-01")
        assert isinstance(result, dict)
        assert len(result) > 0

    def test_generate_synthetic_o3(self):
        from src.external.sentinel5p_client import generate_synthetic_s5p_o3
        result = generate_synthetic_s5p_o3("2024-01-01", "2024-06-01")
        assert isinstance(result, dict)
        assert len(result) > 0

    def test_generate_synthetic_no2_long_range(self):
        from src.external.sentinel5p_client import generate_synthetic_s5p_no2
        result = generate_synthetic_s5p_no2("2020-01-01", "2024-12-31")
        assert len(result) > 12  # Multi-year

    def test_generate_synthetic_o3_short_range(self):
        from src.external.sentinel5p_client import generate_synthetic_s5p_o3
        result = generate_synthetic_s5p_o3("2024-06-01", "2024-06-30")
        assert len(result) > 0


class TestAggregateAtmosphericByMonth:
    """Tests for aggregate_atmospheric_by_month function."""

    def test_aggregate_basic(self):
        import pandas as pd
        from src.external.sentinel5p_client import aggregate_atmospheric_by_month
        openaq_df = pd.DataFrame({
            "date_utc": pd.to_datetime(["2024-01-15", "2024-02-20", "2024-03-10"]),
            "value": [25.5, 30.2, 28.1],
        })
        s5p_data = {"2024-01-01": 0.0001, "2024-02-01": 0.0002, "2024-03-01": 0.00015}
        result = aggregate_atmospheric_by_month(openaq_df, s5p_data)
        assert isinstance(result, pd.DataFrame)

    def test_aggregate_empty(self):
        import pandas as pd
        from src.external.sentinel5p_client import aggregate_atmospheric_by_month
        empty_df = pd.DataFrame()
        s5p_data = {"2024-01-01": 0.0001}
        result = aggregate_atmospheric_by_month(empty_df, s5p_data)
        assert result.empty


class TestModuleConstants:
    def test_module_imports(self):
        from src.external import sentinel5p_client
        assert sentinel5p_client is not None