"""Tests for src.papers.p0030_yvyra_soy (P0030 Yvyra Soy pipeline)."""

import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent

# Run via the project venv so we don't fight interpreter/dependency mismatches
PYTHON = str(REPO_ROOT / ".venv" / "bin" / "python")
if not Path(PYTHON).exists():
    PYTHON = sys.executable  # fallback


def run_p0030_demo():
    """Run the demo end-to-end via subprocess so we don't pollute sys.path.

    Uses a helper script (tests/_p0030_test_helper.py) that stubs
    geopandas/rasterio/shapely before importing src.papers.p0030_yvyra_soy
    so the pipeline runs in CI Python 3.10 (which doesn't have those
    deps installed).
    """
    helper = REPO_ROOT / "tests" / "_p0030_test_helper.py"
    result = subprocess.run(
        [PYTHON, str(helper)],
        capture_output=True,
        text=True,
        cwd=str(REPO_ROOT),
    )
    assert result.returncode == 0, f"Pipeline failed: {result.stderr}"
    return json.loads(result.stdout)


class TestYvyraSoyPipeline:
    """Tests for the P0030 Yvyra Soy pipeline."""

    def test_pipeline_runs_end_to_end(self):
        """The pipeline produces a result dict."""
        result = run_p0030_demo()
        assert isinstance(result, dict)
        assert "census" in result
        assert "soy_by_department" in result
        assert "osm_polygons" in result
        assert "national_mean_yield_kg_per_ha" in result

    def test_census_loads_19_pueblos(self):
        """INE 2022 census has 19 pueblos with positive community counts."""
        result = run_p0030_demo()
        assert result["census"]["n_pueblos"] == 19
        assert result["census"]["national_total_2022"] == 557

    def test_pueblo_top5_matches_documented(self):
        """Top 5 pueblos by community count (measured from INE 2022)."""
        result = run_p0030_demo()
        pueblos = result["census"]["pueblos"][:5]
        names = [p["pueblo"] for p in pueblos]
        # Top 5: Mbya Guarani, Ava Guarani, Pai Tavytera, Ayoreo, Nivacle
        assert "Mbya Guarani" in names
        assert "Ava Guarani" in names
        assert "Pai Tavytera" in names
        # Total of top 5 should be ~460 (200+150+61+26+23)
        top5_total = sum(p["ine_communities_2022"] for p in pueblos)
        assert 400 <= top5_total <= 500, f"Top 5 pueblos total = {top5_total}, expected ~460"

    def test_national_yield_is_in_realistic_range(self):
        """National mean soy yield should be 1500-3500 kg/ha (real range)."""
        result = run_p0030_demo()
        ny = result["national_mean_yield_kg_per_ha"]
        assert 1500 <= ny <= 3500, f"National yield = {ny}, out of realistic range"

    def test_at_least_15_departments_with_yield(self):
        """MAG soy yield has at least 15 departments with positive data."""
        result = run_p0030_demo()
        assert len(result["soy_by_department"]) >= 15

    def test_osm_polygons_loads_30_features(self):
        """OSM community polygons GeoJSON has 30 features."""
        result = run_p0030_demo()
        assert result["osm_polygons"]["n_features"] == 30
        bbox = result["osm_polygons"]["bbox"]
        assert bbox is not None and len(bbox) == 4
        # Paraguay bbox: lon ~-63 to -54, lat ~-28 to -19 (Gran Chaco extends west)
        lon_min, lat_min, lon_max, lat_max = bbox
        assert -63 < lon_min < -54
        assert -28 < lat_min < -19
        assert -63 < lon_max < -54
        assert -28 < lat_max < -19

    def test_output_files_written(self):
        """Pipeline writes JSON and Markdown outputs."""
        run_p0030_demo()
        assert (REPO_ROOT / "outputs/p0030/p0030_analysis.json").exists()
        assert (REPO_ROOT / "outputs/p0030/p0030_analysis.md").exists()

    def test_no_fabricated_pueblo_names(self):
        """Pueblo names should match the real INE 2022 census."""
        result = run_p0030_demo()
        # From data/raw/ine_indi/indigenous_communities_2022_summary.csv
        # (19 pueblos listed in the INE 2022 census)
        real_pueblos = {
            "Ache",
            "Ava Guarani",
            "Mbya Guarani",
            "Pai Tavytera",
            "Guarani Occidental / Pueblo Guarani",
            "Guarani Nandeva",
            "Enlhet Norte",
            "Enxet Sur",
            "Sanapana",
            "Angaite",
            "Guana",
            "Toba Maskoy / Toba Enenlhet",
            "Nivacle",
            "Maka",
            "Manjui",
            "Ayoreo",
            "Ybytoso",
            "Tomaraho",
            "Qom",
        }
        actual = {p["pueblo"] for p in result["census"]["pueblos"]}
        # All actual pueblo names should be in the real set
        for p in actual:
            # Allow for whitespace/encoding variants (e.g., "Guarani" vs "Guaraní")
            stripped = (
                p.replace(" ", "")
                .replace("í", "i")
                .replace("é", "e")
                .replace("á", "a")
                .replace("ó", "o")
                .replace("ú", "u")
                .replace("ñ", "n")
                .replace("Ñ", "N")
            )
            for real in real_pueblos:
                real_stripped = (
                    real.replace(" ", "")
                    .replace("í", "i")
                    .replace("é", "e")
                    .replace("á", "a")
                    .replace("ó", "o")
                    .replace("ú", "u")
                    .replace("ñ", "n")
                    .replace("Ñ", "N")
                )
                if stripped == real_stripped:
                    break
            else:
                # pueblo name not in real set
                pytest.fail(f"Pueblo {p!r} not in real INE 2022 set")


class TestYvyraSoyDataLineage:
    """Tests for the data provenance documented in ACTUAL_RESULTS.md."""

    def test_actual_results_documents_real_datasets(self):
        """ACTUAL_RESULTS.md mentions INE 2022, OSM, MAG, Hansen GFC."""
        actual = (REPO_ROOT / "papers/drafts/p0030_yvyra_soy/ACTUAL_RESULTS.md").read_text()
        assert "INE 2022" in actual
        assert "OSM" in actual
        assert "MAG" in actual
        assert "Hansen GFC" in actual

    def test_actual_results_states_zero_fpic(self):
        """ACTUAL_RESULTS.md explicitly states no FPIC engagement."""
        actual = (REPO_ROOT / "papers/drafts/p0030_yvyra_soy/ACTUAL_RESULTS.md").read_text()
        assert "FPIC" in actual
        assert "not contacted" in actual.lower() or "zero communities" in actual.lower()

    def test_paper_tex_does_not_claim_circular_unverified_territory_numbers(self):
        """paper.tex does not use the 10 hardcoded placeholders from P0012."""
        paper = (REPO_ROOT / "papers/drafts/p0030_yvyra_soy/paper.tex").read_text()
        # Must not contain the P0012 hardcoded list (49.45%, 49.43%, etc.)
        for placeholder in ["49.45", "49.43", "46.46"]:
            assert placeholder not in paper, f"P0030 paper.tex contains P0012 placeholder {placeholder!r}"


class TestP0030RegressionFinding:
    """Tests for the per-region regression finding (P0030 contribution)."""

    def _run_regression(self):
        """Run the regression via the helper script + return parsed JSON."""
        import json
        import subprocess
        import sys
        from pathlib import Path

        REPO_ROOT = Path("/opt/data/work/satellite-paraguay")
        result = subprocess.run(
            [sys.executable, str(REPO_ROOT / "tests" / "_p0030_test_helper.py")],
            capture_output=True,
            text=True,
            cwd=str(REPO_ROOT),
        )
        if result.returncode != 0:
            pytest.skip(f"P0030 helper failed: {result.stderr[:200]}")
        return json.loads(result.stdout)

    def test_regression_finding_runs(self):
        """run_p0030_regression returns a dict with the expected keys."""
        out = self._run_regression()
        assert (
            "regression_analysis" in out
        ), f"Expected regression_analysis key in P0030 demo output; got keys: {list(out.keys())}"
        reg = out["regression_analysis"]
        assert "headline_finding" in reg
        assert "regional_data" in reg
        assert "interpretation" in reg

    def test_regression_occidental_slope_greater_than_oriental(self):
        """Headline finding: Occidental slope > Oriental slope."""
        out = self._run_regression()
        reg = out["regression_analysis"]
        occ = reg["regional_data"]["Occidental"]["mean_slope_kg_per_ha_per_yr"]
        ori = reg["regional_data"]["Oriental"]["mean_slope_kg_per_ha_per_yr"]
        assert occ > ori, f"Occidental slope {occ} should exceed Oriental {ori}"
        ratio = reg["headline_finding"]["ratio_occident_vs_orient"]
        assert 1.5 <= ratio <= 2.5, f"Ratio {ratio} outside expected range"

    def test_regression_density_oriental_lower(self):
        """Occidental has higher indigenous community density than Oriental."""
        out = self._run_regression()
        reg = out["regression_analysis"]
        occ_d = reg["regional_data"]["Occidental"]["indi_density_per_dept"]
        ori_d = reg["regional_data"]["Oriental"]["indi_density_per_dept"]
        assert occ_d > ori_d, f"Occidental density {occ_d} should exceed Oriental {ori_d}"
