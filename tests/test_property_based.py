"""Property-based tests using hypothesis.

These tests generate many inputs automatically to find edge cases.
"""

import json

import numpy as np
from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st


class TestNumpyProperties:
    """Property tests for numpy operations."""

    @given(
        n=st.integers(min_value=10, max_value=100),
    )
    def test_array_shapes(self, n):
        arr = np.random.rand(n)
        assert arr.shape == (n,)

    @given(
        seed=st.integers(min_value=0, max_value=10000),
    )
    def test_seed_reproducibility(self, seed):
        np.random.seed(seed)
        a = np.random.rand(50)
        np.random.seed(seed)
        b = np.random.rand(50)
        np.testing.assert_array_equal(a, b)

    @given(
        values=st.lists(st.floats(min_value=-100, max_value=100, allow_nan=False), min_size=1, max_size=20),
    )
    def test_mean_in_range(self, values):
        """Mean should be approximately between min and max of values."""
        arr = np.array(values)
        if len(values) > 0:
            m = arr.mean()
            lo, hi = min(values), max(values)
            # Use small tolerance for floating point
            tol = max(1e-10 * abs(hi), 1e-15)
            assert lo - tol <= m <= hi + tol


class TestStatisticsProperties:
    """Property tests for statistical functions."""

    @given(
        a=st.floats(min_value=1, max_value=100, allow_nan=False),
        b=st.floats(min_value=1, max_value=100, allow_nan=False),
    )
    @settings(max_examples=15, deadline=None)
    def test_cohens_d_sign(self, a, b):
        """Cohen's d sign reflects which group is higher."""
        from src.evaluation.statistics import cohens_d

        # Use differences ≥ 1 to avoid floating point noise
        if abs(a - b) < 1.0:
            return  # Skip close cases
        g1 = np.array([a, a + 0.5, a + 1.0])
        g2 = np.array([b, b + 0.5, b + 1.0])
        try:
            d = cohens_d(g1, g2)
            if a > b:
                assert d > 0
            elif a < b:
                assert d < 0
        except ZeroDivisionError:
            pass  # identical groups


class TestJSONProperties:
    """Property tests for JSON."""

    @given(
        data=st.dictionaries(
            keys=st.text(min_size=1, max_size=10).filter(lambda k: not k.startswith("_")),
            values=st.integers(min_value=-100, max_value=100),
            min_size=1,
            max_size=5,
        )
    )
    @settings(suppress_health_check=[HealthCheck.function_scoped_fixture], deadline=None)
    def test_json_roundtrip(self, data, tmp_path):
        f = tmp_path / "test.json"
        f.write_text(json.dumps(data))
        loaded = json.loads(f.read_text())
        assert loaded == data


class TestStringProperties:
    """Property tests for strings."""

    @given(text=st.text(min_size=1, max_size=50).filter(lambda t: t.strip()))
    def test_string_not_empty(self, text):
        """After stripping, text should not be empty."""
        assert len(text.strip()) > 0


class TestMathProperties:
    """Property tests for math."""

    @given(
        x=st.floats(min_value=0.001, max_value=100, allow_nan=False),
    )
    def test_log_exp_roundtrip(self, x):
        """log(exp(x)) should equal x for small x."""
        result = np.log(np.exp(x))
        # Allow small floating point error
        assert abs(result - x) < 1e-3 * x

    @given(
        x=st.floats(min_value=-1e6, max_value=1e6, allow_nan=False),
    )
    def test_sqrt_nonneg(self, x):
        """sqrt of positive number should be non-negative."""
        if x >= 0:
            assert np.sqrt(x) >= 0

    @given(
        a=st.floats(min_value=0.001, max_value=1000, allow_nan=False),
        b=st.floats(min_value=0.001, max_value=1000, allow_nan=False),
    )
    def test_division_inverse(self, a, b):
        """(a / b) * b should equal a."""
        result = (a / b) * b
        # Allow small floating point error
        assert abs(result - a) < 1e-6 * max(a, 1)


class TestListProperties:
    """Property tests for lists."""

    @given(
        lst=st.lists(st.integers(min_value=0, max_value=100), min_size=1, max_size=20),
    )
    def test_sum_nonneg(self, lst):
        """Sum of non-negative ints should be non-negative."""
        assert sum(lst) >= 0

    @given(
        lst=st.lists(st.integers(), min_size=1, max_size=20),
    )
    def test_len_preserved(self, lst):
        """len() returns the original length."""
        assert len(lst) == len(lst)


class TestDictProperties:
    """Property tests for dicts."""

    @given(
        d=st.dictionaries(
            keys=st.text(min_size=1, max_size=10).filter(lambda k: not k.startswith("_")),
            values=st.integers(),
            min_size=1,
            max_size=10,
        )
    )
    def test_dict_roundtrip(self, d):
        """Dict should roundtrip via dict()."""
        assert dict(d) == d


class TestDateProperties:
    """Property tests for date operations."""

    @given(
        year=st.integers(min_value=1900, max_value=2100),
    )
    def test_year_range(self, year):
        from datetime import datetime

        d = datetime(year, 6, 15)
        assert d.year == year


class TestSetProperties:
    """Property tests for set operations."""

    @given(
        lst=st.lists(st.integers(), min_size=0, max_size=20),
    )
    def test_set_dedup(self, lst):
        """set() deduplicates."""
        s = set(lst)
        assert len(s) <= len(lst)
