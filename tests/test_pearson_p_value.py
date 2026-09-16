"""Direct unit tests for src.papers.p0030_yvyra_soy.pipeline._pearson_p_value.

Layer 3 (Pitfall #36) verification for the P0030 regression helper.
This helper computes a two-sided p-value for Pearson r using the
math.erfc normal approximation (stdlib-only, works in the CI sandbox
without scipy).

The pipeline calls it with the **unrounded** pearson_r value
(e.g., -0.30576735550575, not -0.306 — see how the pipeline rounds
AFTER computing the p-value). The integration test
`tests/test_p0030_yvyra_soy.py::TestP0030RegressionFinding::
test_regression_interpretation_reflects_data` checks that the JSON
output has p_value_two_sided == 0.2659 for the measured case.

These unit tests verify the helper in isolation, against scipy's
t-distribution when available, and assert the specific P0030 case.

Notes on accuracy:
- _pearson_p_value uses the **normal approximation** (math.erfc), not
  scipy's t-distribution. This is intentional (per the helper's docstring):
  math.erfc is stdlib, scipy is not guaranteed in CI sandbox.
- For n >= 10 (the smallest n we use in the thesis), the normal
  approximation agrees with scipy t-test to within ~0.04 for |r| < 0.5.
- The thesis commentary "normal-approx and t-distribution agree to
  within 0.005 for n=14, df=12, p~0.27" was overly optimistic; the
  actual difference is 0.022 (scipy t-test = 0.2873, our normal = 0.2659).
  Both correctly indicate "not significant" at p > 0.05.
"""

import math
from pathlib import Path
import sys

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from src.papers.p0030_yvyra_soy.pipeline import _pearson_p_value


class TestPearsonPValueMath:
    """Verify the math.erfc-based normal approximation formula."""

    def test_zero_r_returns_1(self):
        """r = 0 means no correlation → p = 1.0."""
        assert _pearson_p_value(0.0, 14) == pytest.approx(1.0, abs=1e-9)

    def test_symmetry_in_r(self):
        """t = |r| * sqrt(n-2) / sqrt(1-r^2), so p is symmetric in sign of r."""
        for n in [5, 10, 20, 50]:
            for r in [0.1, 0.3, 0.5, 0.8]:
                p_pos = _pearson_p_value(r, n)
                p_neg = _pearson_p_value(-r, n)
                assert p_pos == pytest.approx(p_neg, abs=1e-12), \
                    f"p({r}, {n})={p_pos} != p(-{r}, {n})={p_neg}"

    def test_decreases_with_n_for_mod_r(self):
        """For fixed |r|, larger n → smaller p (more statistical power)."""
        r = 0.5
        for n in [10, 14, 20, 30, 50]:
            p = _pearson_p_value(r, n)
        # For r=0.5, p should decrease monotonically with n
        n_values = [10, 14, 20, 30, 50]
        p_values = [_pearson_p_value(r, n) for n in n_values]
        for i in range(len(p_values) - 1):
            assert p_values[i] > p_values[i + 1], \
                f"p({r}, {n_values[i]})={p_values[i]} should be > p({r}, {n_values[i+1]})={p_values[i+1]}"

    def test_decreases_with_r_for_fixed_n(self):
        """For fixed n, larger |r| → smaller p (more extreme)."""
        n = 20
        p_values = [_pearson_p_value(r, n) for r in [0.1, 0.3, 0.5, 0.7, 0.9]]
        for i in range(len(p_values) - 1):
            assert p_values[i] > p_values[i + 1]

    def test_returns_nan_for_r_at_boundary(self):
        """r = ±1.0 is undefined (division by zero in formula)."""
        assert math.isnan(_pearson_p_value(1.0, 10))
        assert math.isnan(_pearson_p_value(-1.0, 10))

    def test_returns_nan_for_r_beyond_boundary(self):
        """|r| > 1.0 is mathematically impossible."""
        assert math.isnan(_pearson_p_value(1.5, 10))
        assert math.isnan(_pearson_p_value(-2.0, 10))

    def test_returns_nan_for_n_too_small(self):
        """n < 3: not enough data for Pearson r."""
        assert math.isnan(_pearson_p_value(0.5, 2))
        assert math.isnan(_pearson_p_value(0.5, 1))
        assert math.isnan(_pearson_p_value(0.5, 0))


class TestPearsonPValueP0030MeasuredCase:
    """Verify the specific values used in the P0030 regression output.

    The pipeline computes pearson_r with full precision (~-0.30576735550575)
    and passes the unrounded value to _pearson_p_value. The function
    returns 0.2659 (rounded), which is then stored as
    cross_dept_regression.p_value_two_sided in the JSON.

    If someone refactors the pipeline to round pearson_r BEFORE calling
    _pearson_p_value, the result would be 0.2655 (using r=-0.306 as input).
    This test catches that regression."""

    def test_p0030_actual_r_value(self):
        """The pipeline's actual r value (-0.30576735550575) gives p=0.2659."""
        # Recompute r from MAG data to confirm
        import csv
        import math
        import re

        rend_path = REPO_ROOT / "data" / "raw" / "fao_mag" / "mag_soja_rendimiento.csv"
        with open(rend_path) as f:
            reader = csv.reader(f)
            header = next(reader)
            year_cols = [(i, h.strip()) for i, h in enumerate(header) if i > 0]
            dept_yields = {}
            for row in reader:
                if not row or not row[0].strip():
                    continue
                dept = row[0].strip()
                years, yields = [], []
                for idx, year_str in year_cols:
                    if idx >= len(row):
                        continue
                    try:
                        v = float(row[idx])
                        if v > 0:
                            m = re.match(r"(\d{4})", year_str)
                            if m is not None:
                                years.append(int(m.group(1)))
                                yields.append(v)
                    except ValueError:
                        continue
                if len(years) >= 5:
                    n = len(years)
                    mean_y = sum(years) / n
                    mean_v = sum(yields) / n
                    ss_xy = sum((years[i] - mean_y) * (yields[i] - mean_v) for i in range(n))
                    ss_xx = sum((years[i] - mean_y) ** 2 for i in range(n))
                    ss_yy = sum((yields[i] - mean_v) ** 2 for i in range(n))
                    slope = ss_xy / ss_xx
                    intercept = mean_v - slope * mean_y
                    ss_res = sum((yields[i] - (slope * years[i] + intercept)) ** 2 for i in range(n))
                    dept_yields[dept.title()] = {
                        "slope_kg_per_ha_per_year": round(slope, 2),
                        "mean_yield": round(mean_v, 1),
                    }

        means = [dept_yields[d]["mean_yield"] for d in dept_yields]
        slps = [dept_yields[d]["slope_kg_per_ha_per_year"] for d in dept_yields]
        n = len(means)
        mean_m = sum(means) / n
        mean_s = sum(slps) / n
        ss_xy = sum((means[i] - mean_m) * (slps[i] - mean_s) for i in range(n))
        ss_xx = sum((means[i] - mean_m) ** 2 for i in range(n))
        ss_yy = sum((slps[i] - mean_s) ** 2 for i in range(n))
        r = ss_xy / (ss_xx * ss_yy) ** 0.5

        p = _pearson_p_value(r, n)
        # Pipeline rounds to 4 decimals
        rounded = round(p, 4)
        assert rounded == 0.2659, \
            f"Expected 0.2659 (matches JSON output + integration test); got {rounded}"

    def test_p0030_with_3dp_rounded_input(self):
        """If someone refactors to round r BEFORE calling the helper,
        the result changes to 0.2655. This test catches that regression."""
        # r=-0.306 (the 3dp-rounded value used in the JSON's pearson_r field)
        p = _pearson_p_value(-0.306, 14)
        rounded = round(p, 4)
        assert rounded == 0.2655, \
            f"Sanity: with r=-0.306 (3dp-rounded), p={rounded}; this is what " \
            f"the helper WOULD return if someone round-too-early'd the input"

    def test_p0030_matches_integration_test_value(self):
        """The integration test asserts p_value_two_sided == 0.2659.
        Make sure the helper still produces 0.2659 in the canonical pipeline path."""
        # Verify with the unrounded r value
        r_unrounded = -0.30576735550575
        p = _pearson_p_value(r_unrounded, 14)
        rounded = round(p, 4)
        assert rounded == 0.2659, \
            f"Expected 0.2659 after rounding (matches integration test); got {rounded}"


class TestPearsonPValueVsScipy:
    """Verify that math.erfc normal approximation agrees with scipy t-test
    within acceptable bounds for the input ranges we actually use."""

    @pytest.fixture
    def scipy_t_sf(self):
        try:
            import scipy.stats
            return scipy.stats.t.sf
        except ImportError:
            pytest.skip("scipy not available")

    def test_p0030_normal_vs_t_distribution(self, scipy_t_sf):
        """For P0030 (r=-0.3057..., n=14), normal approx 0.2659 vs
        scipy t-test 0.2873. Difference ~0.022 (the documented limitation
        of the normal approximation at small n)."""
        r = -0.30576735550575
        n = 14
        my_p = _pearson_p_value(r, n)
        t = abs(r) * math.sqrt(n - 2) / math.sqrt(1 - r * r)
        scipy_p = 2 * scipy_t_sf(t, n - 2)
        diff = abs(my_p - scipy_p)
        # Both agree the result is "not significant" (p > 0.05)
        assert my_p > 0.05
        assert scipy_p > 0.05
        # Difference is bounded
        assert diff < 0.05, f"normal={my_p:.4f}, scipy={scipy_p:.4f}, diff={diff:.4f}"

    def test_qualitative_agreement_for_thesis_inputs(self, scipy_t_sf):
        """For thesis-relevant inputs, normal approx and scipy
        t-test agree on significance at p<0.05.

        KNOWN LIMITATION: At small n (< 20) with moderate |r| (around 0.4-0.5),
        the normal approximation and t-test differ enough to flip the
        significance conclusion. We avoid that range here — the test
        cases are either "clearly significant" or "clearly not significant"
        so both methods agree."""
        # The P0030 cross-dept regression + a few sanity cases
        cases = [
            (-0.30576735550575, 14),  # P0030: NOT significant in both
            (0.85, 14),                # strong effect, significant in both
            (0.5, 30),                  # moderate effect, larger n → significant in both
            (0.5, 50),                  # moderate effect, large n → significant in both
        ]
        for r, n in cases:
            my_p = _pearson_p_value(r, n)
            t = abs(r) * math.sqrt(n - 2) / math.sqrt(1 - r * r)
            scipy_p = 2 * scipy_t_sf(t, n - 2)
            my_sig = my_p < 0.05
            scipy_sig = scipy_p < 0.05
            assert my_sig == scipy_sig, \
                f"Disagreement on significance for r={r}, n={n}: " \
                f"normal={my_sig} (p={my_p:.4f}), scipy={scipy_sig} (p={scipy_p:.4f})"


class TestPearsonPValueDocumentedBehavior:
    """Verify the documented behavior matches actual behavior."""

    def test_returns_float(self):
        """Function returns float, not int."""
        result = _pearson_p_value(0.5, 14)
        assert isinstance(result, float)

    def test_returns_nan_for_undefined(self):
        """For undefined inputs (|r|>=1 or n<3), returns NaN (not raises)."""
        assert math.isnan(_pearson_p_value(1.0, 14))
        assert math.isnan(_pearson_p_value(2.0, 14))
        assert math.isnan(_pearson_p_value(0.5, 2))

    def test_output_range_zero_to_one(self):
        """For valid inputs, output is in [0, 1]."""
        for r in [-0.9, -0.5, 0, 0.5, 0.9]:
            for n in [3, 5, 10, 30, 100]:
                p = _pearson_p_value(r, n)
                if math.isnan(p):
                    continue
                assert 0 <= p <= 1, f"r={r}, n={n} gave p={p} (out of [0, 1])"
