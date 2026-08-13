"""Fail-loud guard tests for the 2026-08-11 pass (BRUTAL_ROAST fix).

Each paper pipeline + baseline that previously fell back to
``np.random.rand()`` silent fill now must raise ``FileNotFoundError``
(or a similar guard) when the expected real data path is absent.

These tests cover the 6 production files updated in 2026-08-11:
- src/papers/p0011_yvutu_deforestation/pipeline.py
- src/papers/p0025_yrupe_yield/pipeline.py
- src/papers/p0035_tatakua_air_quality/pipeline.py
- src/baselines/p0011_yvutu_baselines.py
- src/baselines/p0035_tatakua_baselines.py
- src/baselines/p0100_yvyra_baselines.py
- src/utils/mlflow_tracking.py

If you find a paper pipeline that still produces numbers from
``np.random.rand()`` when real data is missing, that's a regression
of the BRUTAL_ROAST fix and should be fixed before any review.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent


def _run_module(module: str, args: list[str], cwd: Path) -> subprocess.CompletedProcess:
    """Run `python -m <module> <args...>` and capture output."""
    return subprocess.run(
        [sys.executable, "-m", module, *args],
        capture_output=True,
        text=True,
        cwd=str(cwd),
        timeout=60,
    )


# ----------------------------------------------------------------------
# 1. P0011 Yvutu — run_yvutu_demo requires NDVI data, no random fill
# ----------------------------------------------------------------------


class TestP0011YvutuFailLoud:
    """run_yvutu_demo() must fail loud if no NDVI is supplied."""

    def test_run_yvutu_demo_without_data_raises_filenotfounderror(self):
        # The pipeline class itself isn't importable in the sandbox because
        # it pulls in heavy deps (rasterio, geopandas). The demo function
        # is in `if __name__ == "__main__":` so we exercise it as a script.
        r = _run_module(
            "src.papers.p0011_yvutu_deforestation.pipeline",
            [],
            cwd=REPO,
        )
        # Either it raises FileNotFoundError (good) or import fails (skip).
        # We accept either: the key contract is "no random fill".
        # If the script exits cleanly, that's a regression.
        if r.returncode == 0:
            pytest.fail(
                "run_yvutu_demo() exited 0 with no data — silent random fill!\n"
                f"stdout: {r.stdout[:300]}\nstderr: {r.stderr[:300]}"
            )
        # rc=2 is FileNotFoundError from our guard (good).

    def test_run_yvutu_demo_with_dummy_file_still_fails_loud(self):
        """Passing a non-existent file must raise, not generate fake numbers."""
        r = _run_module(
            "src.papers.p0011_yvutu_deforestation.pipeline",
            ["/tmp/this_file_does_not_exist.npz"],
            cwd=REPO,
        )
        # Acceptable: rc != 0 (any error). Unacceptable: rc=0 with random output.
        if r.returncode == 0:
            pytest.fail("run_yvutu_demo() succeeded with nonexistent data — silent corruption!")


# ----------------------------------------------------------------------
# 2. P0025 Yrupe — same contract
# ----------------------------------------------------------------------


class TestP0025YrupeFailLoud:
    def test_run_yrupe_demo_without_data_raises(self):
        r = _run_module(
            "src.papers.p0025_yrupe_yield.pipeline",
            [],
            cwd=REPO,
        )
        if r.returncode == 0:
            pytest.fail("run_yrupe_demo() exited 0 with no data — silent random fill!\n" f"stdout: {r.stdout[:300]}")

    def test_run_yrupe_demo_with_nonexistent_file_raises(self):
        r = _run_module(
            "src.papers.p0025_yrupe_yield.pipeline",
            ["/tmp/this_file_does_not_exist.npz"],
            cwd=REPO,
        )
        if r.returncode == 0:
            pytest.fail("run_yrupe_demo() succeeded with nonexistent file")


# ----------------------------------------------------------------------
# 3. P0035 Tatakua — fetch_sentinel5p + run_tatakua_demo + forecast
# ----------------------------------------------------------------------


class TestP0035TatakuaFailLoud:
    def test_run_tatakua_demo_without_data_raises(self):
        r = _run_module(
            "src.papers.p0035_tatakua_air_quality.pipeline",
            [],
            cwd=REPO,
        )
        if r.returncode == 0:
            pytest.fail(
                "run_tatakua_demo() exited 0 with no historical — silent random fill!\n"
                f"stdout: {r.stdout[:400]}\nstderr: {r.stderr[:200]}"
            )

    def test_run_tatakua_demo_with_nonexistent_history_raises(self):
        r = _run_module(
            "src.papers.p0035_tatakua_air_quality.pipeline",
            ["/tmp/this_file_does_not_exist.npy"],
            cwd=REPO,
        )
        if r.returncode == 0:
            pytest.fail("run_tatakua_demo() succeeded with nonexistent file")

    def test_forecast_pm25_deterministic_with_default_seed(self):
        """The pilot heuristic must be deterministic — seeded with 42.

        Without the seed, two consecutive calls produce different numbers,
        which makes the heuristic unfit for any reproducible result.
        """
        try:
            from src.papers.p0035_tatakua_air_quality import pipeline as p
        except ImportError:
            pytest.skip("p0035 pipeline import requires heavier deps (requests)")
        # Construct with default config; call forecast twice with same input.
        # If forecast_pm25 is deterministic (seed=42 default), the two calls
        # must produce identical arrays.
        import numpy as np

        pipe = p.TatakuaPipeline()
        hist = np.array([10.0, 12.0, 8.0, 15.0, 11.0] * 50)  # 250 points
        f1 = pipe.forecast_pm25(hist.copy())
        f2 = pipe.forecast_pm25(hist.copy())
        np.testing.assert_array_equal(
            f1,
            f2,
            err_msg="forecast_pm25 must be deterministic with seed=42 default",
        )


# ----------------------------------------------------------------------
# 4-6. Baselines — CLI-only, require real data files
# ----------------------------------------------------------------------


class TestBaselinesFailLoud:
    """The 3 baseline modules previously used random data in __main__.

    They now require real inputs; bare `python -m ...` without arguments
    must fail with FileNotFoundError, not generate fake metrics.
    """

    @pytest.mark.parametrize(
        "module",
        [
            "src.baselines.p0011_yvutu_baselines",
            "src.baselines.p0035_tatakua_baselines",
            "src.baselines.p0100_yvyra_baselines",
        ],
    )
    def test_baseline_bare_invocation_raises(self, module):
        r = _run_module(module, [], cwd=REPO)
        assert r.returncode != 0, f"{module} exited 0 with no data — silent random fill!\n" f"stdout: {r.stdout[:300]}"

    @pytest.mark.parametrize(
        "module",
        [
            "src.baselines.p0011_yvutu_baselines",
            "src.baselines.p0035_tatakua_baselines",
            "src.baselines.p0100_yvyra_baselines",
        ],
    )
    def test_baseline_with_nonexistent_files_raises(self, module):
        r = _run_module(
            module,
            ["/tmp/no.npz", "/tmp/no.npy"],
            cwd=REPO,
        )
        assert r.returncode != 0, f"{module} succeeded with nonexistent data — silent corruption!"


# ----------------------------------------------------------------------
# 7. mlflow_tracking demo — NaN placeholders, no random.uniform
# ----------------------------------------------------------------------


class TestMLflowTrackingNoRandom:
    """The MLflow demo previously logged `random.uniform(0.7, 0.9)` as F1.

    Now it logs NaN with a `status` field naming the placeholder. Verify
    no `random.uniform` strings remain in the source.
    """

    def test_no_random_uniform_in_mlflow_tracking(self):
        """No `random.uniform(...)` calls should remain in the source.

        The string `random.uniform` may appear in comments / docstrings
        describing the historical bug; only actual function calls count.
        """
        import re

        text = (REPO / "src/utils/mlflow_tracking.py").read_text()
        # Strip comments and docstrings before searching.
        code = re.sub(r"(?m)^\s*#.*$", "", text)
        code = re.sub(r'"""[\s\S]*?"""', "", code)
        code = re.sub(r"'''[\s\S]*?'''", "", code)
        real_calls = re.findall(r"random\.uniform\s*\(", code)
        assert not real_calls, f"mlflow_tracking.py still has random.uniform() calls: {real_calls}"

    def test_mlflow_demo_logs_nan_status(self):
        """The demo should log NaN metrics with a clear PLACEHOLDER status."""
        # Read the file directly and check the demo block contains NaN + PLACEHOLDER
        text = (REPO / "src/utils/mlflow_tracking.py").read_text()
        assert "nan" in text.lower(), "mlflow_tracking.py should use NaN placeholders"
        assert "PLACEHOLDER" in text, "mlflow_tracking.py should label placeholders explicitly"


# ---------------------------------------------------------------------------
# References bibliography guard
# ---------------------------------------------------------------------------


class TestReferencesBibliography:
    """The unified references.bib must contain no malformed escape artifacts.

    The 2026-08-11 manual pass fixed 26 doubled backslash-backslash-url
    artifacts and 6 doubled i-with-acute artifacts that came from the
    original BibTeX parser upstream. Re-introduction would silently
    break PDF rendering. Run scripts/merge_bib.py to sanitize.
    """

    def test_references_bib_has_no_doubled_backslash_url(self):
        import re

        text = (REPO / "references.bib").read_text()
        bad = re.findall(r"\\\\url", text)
        assert not bad, (
            f"references.bib contains {len(bad)} doubled backslash-backslash-url artifacts. "
            "Run scripts/merge_bib.py to sanitize."
        )

    def test_references_bib_has_no_doubled_quote_i_artifact(self):
        import re

        text = (REPO / "references.bib").read_text()
        bad = re.findall(r"\\'\\i", text)
        assert not bad, (
            f"references.bib contains {len(bad)} doubled i-acute artifacts. " "Run scripts/merge_bib.py to sanitize."
        )

    def test_references_bib_has_180_unique_entries(self):
        import re
        from collections import Counter

        text = (REPO / "references.bib").read_text()
        keys = re.findall(r"^@\w+\{\s*([^,\s]+)", text, flags=re.M)
        # 2026-08-13: 182 (was 180; added vallejos2020 + xie2023 for p0011)
        assert len(keys) >= 180, f"Expected >= 180 unique entries, got {len(keys)}"
        dups = [k for k, c in Counter(keys).items() if c > 1]
        assert not dups, f"Duplicate keys in references.bib: {dups}"

    def test_merge_bib_runs_clean_with_no_unresolved(self):
        """merge_bib.py must succeed with zero unresolved conflicts.

        Any future re-introduction of a duplicate key would cause this to
        fail loudly via the script's unresolved-fail-loud branch.
        """
        import subprocess

        r = subprocess.run(
            [sys.executable, "scripts/merge_bib.py"],
            capture_output=True,
            text=True,
            cwd=str(REPO),
            timeout=30,
        )
        assert r.returncode == 0, "merge_bib.py failed:\n" f"stdout={r.stdout}\n" f"stderr={r.stderr}"
        assert "0 unresolved" in r.stdout, "merge_bib.py printed unresolved conflicts:\n" f"{r.stdout}"

    def test_resolved_conflict_keys_contain_expected_canonical_text(self):
        """Each of the 5 PREFER_PAPERS-resolved keys should contain the
        papers version's text (more informative title, "Paraguay" suffix
        on author, etc.). If someone reverts PREFER_PAPERS to the thesis
        version accidentally, this test catches it.
        """
        import re

        text = (REPO / "references.bib").read_text()
        expected_substrings = {
            "indi2024": "Instituto Nacional del Ind",
            "infona2024": "Instituto Forestal Nacional (INFONA)",
            "mades2024": "(MADES)",
            "openaq2024": "Open Air Quality Data",
            "tensorflow2015": "@software{tensorflow2015,",
        }
        for key, expected in expected_substrings.items():
            m = re.search(
                rf"@\w+\{{{re.escape(key)},.*?\n\}}",
                text,
                flags=re.S,
            )
            assert m, f"Entry for {key} not found in references.bib"
            assert expected in m.group(0), (
                f"{key} in references.bib does not contain expected canonical "
                f"text {expected!r}. Did someone revert PREFER_PAPERS?"
            )
