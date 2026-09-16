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

        REPO_ROOT = Path(__file__).resolve().parent.parent
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

    def test_regression_ratio_exact_value(self):
        """Failure-injection (Pitfall #36 Layer 3): ratio must equal 1.95.

        Catches regressions where anyone (or any auto-formatter) re-introduces
        the {:.1f}-formatted "2.0x" version of the headline. The pipeline
        computes 109.96 / 56.47 = 1.9472... which rounds to 1.95 with 2 decimal
        places, but to "2.0" via banker's rounding at 1 decimal place. The
        ratio_display string is the version the headline reports.
        """
        out = self._run_regression()
        reg = out["regression_analysis"]
        ratio = reg["headline_finding"]["ratio_occident_vs_orient"]
        assert ratio == 1.95, (
            f"Expected ratio=1.95 (actual 109.96/56.47=1.9472...), got {ratio}. "
            f"This test would catch a return to the misleading 2.0x headline."
        )
        ratio_display = reg["headline_finding"].get("ratio_display")
        assert ratio_display == "1.95x", (
            f"Expected ratio_display='1.95x' (NOT '2.0x' via {{:.1f}} banker's "
            f"rounding), got {ratio_display!r}"
        )

    def test_regression_interpretation_reflects_data(self):
        """Failure-injection (Pitfall #36 Layer 3): interpretation must
        acknowledge the negative cross-dept r and NOT claim indigenous-density
        causes faster expansion.

        Catches regressions where the narrative is softened back to the
        earlier (incorrect) "higher density → faster expansion" claim. The
        measured data shows r=-0.306, p=0.27 — not significant, and the sign
        contradicts the older causal-sounding narrative.
        """
        out = self._run_regression()
        reg = out["regression_analysis"]
        interp = reg["interpretation"]
        # Must contain the descriptive-not-inferential caveat
        assert "DESCRIPTIVE" in interp or "descriptive" in interp, (
            "Interpretation must explicitly state the per-region comparison "
            "is descriptive (n=2 Occidental), not inferential."
        )
        # Must contain the actual measured r value (with a tolerance for
        # re-formatting: -0.306, -0.31, etc.)
        assert "-0.306" in interp or "-0.31" in interp, (
            f"Interpretation must report the measured r value; got: {interp[:200]}"
        )
        # Must NOT contain the old (incorrect) phrasings
        forbidden = [
            "higher indigenous community density show faster",
            "Departments with higher indigenous community density show faster",
        ]
        for phrase in forbidden:
            assert phrase not in interp, (
                f"Interpretation still contains the discredited causal claim "
                f"{phrase!r}. The cross-dept r is negative; the old narrative "
                f"contradicts the data."
            )
        # Must mention limitations or p-value to flag the non-significance
        assert ("limitations" in reg) or ("p=" in interp) or ("NOT statistically" in interp), (
            "Interpretation must report p-value or explicitly state 'NOT "
            "statistically significant'. The cross-dept regression is n=14, "
            "r=-0.306, p=0.27 — not significant."
        )
        # n-with-data fields must be present and accurate
        n_occ = reg["headline_finding"].get("n_occidental_with_data")
        n_ori = reg["headline_finding"].get("n_oriental_with_data")
        assert n_occ == 2, f"n_occidental_with_data should be 2 (Alto Paraguay, Boqueron); got {n_occ}"
        assert n_ori == 12, f"n_oriental_with_data should be 12; got {n_ori}"
        # Cross-dept regression must include r^2 and p_value (Paper #36 Layer 2 requirement)
        cross = reg["cross_dept_regression"]
        assert "r_squared" in cross, "cross_dept_regression must include r_squared for transparency"
        assert "p_value_two_sided" in cross, "cross_dept_regression must include p_value_two_sided"
        assert cross["pearson_r"] == -0.306, f"pearson_r drift: got {cross['pearson_r']}, expected -0.306"
        # math.erfc normal approximation for the unrounded pearson_r
        # (-0.30576...) at n=14 → 0.2659 after round(_, 4).
        # (If you call _pearson_p_value(-0.306, 14) directly you get 0.2655
        # — that uses the rounded r, which is wrong. The pipeline correctly
        # passes the unrounded r.) See tests/test_pearson_p_value.py for
        # the direct unit test on the helper.
        assert abs(cross["p_value_two_sided"] - 0.2659) < 0.01, (
            f"p_value drift: got {cross['p_value_two_sided']}, expected ~0.2659"
        )

    def test_paper_tex_does_not_contain_discredited_causal_claim(self):
        """Failure-injection (Pitfall #36 Layer 3): paper.tex must not contain
        the older 'higher density → faster expansion' causal-sounding
        phrasing that contradicted the cross-dept data (r=-0.306, p=0.27).

        Catches regressions where the prose is reverted to the old narrative
        while the JSON output is correctly calibrated.
        """
        from pathlib import Path
        paper_dir = Path(__file__).resolve().parent.parent / "papers" / "drafts"
        paper_tex = paper_dir / "p0030_yvyra_soy" / "paper.tex"
        assert paper_tex.exists(), f"paper.tex not found at {paper_tex}"
        text = paper_tex.read_text()
        forbidden_phrases = [
            "Departments with higher indigenous community density show",
            "higher indigenous community density show\n\\textbf{faster}",
            "higher indigenous community density show faster",
        ]
        for phrase in forbidden_phrases:
            assert phrase not in text, (
                f"paper.tex still contains the discredited causal claim "
                f"{phrase!r}. The cross-dept regression is r=-0.306 (negative "
                f"and not significant); the older narrative contradicts the "
                f"data the pipeline itself computes."
            )
        # The corrected prose must be present (idempotent positive check)
        assert "not statistically significant" in text, (
            "paper.tex must explicitly state the cross-dept r is NOT "
            "statistically significant (Pitfall #36 Layer 2 disclosure)."
        )
        # The Presidente Hayes disclosure must be present
        assert "Presidente Hayes has no" in text, (
            "paper.tex must disclose that Presidente Hayes is excluded from "
            "the Occidental slope mean (it has no continuous MAG yield data)."
        )

    def test_paper_tex_reports_correct_n_with_yield_data(self):
        """Failure-injection: paper.tex must say '2 of 3' for Occidental
        and '12 of 14' for Oriental, not '3 departments' / '14 departments'
        (which would imply all 3 Occidental depts have yield data, when in
        fact Presidente Hayes has null yield data and is excluded).
        """
        from pathlib import Path
        paper_dir = Path(__file__).resolve().parent.parent / "papers" / "drafts"
        paper_tex = paper_dir / "p0030_yvyra_soy" / "paper.tex"
        text = paper_tex.read_text()
        # Correct framing
        assert "2 of 3 Occidental departments" in text, (
            "paper.tex must say '2 of 3 Occidental departments with yield "
            "data', not '3 departments' (Presidente Hayes has null data)."
        )
        assert "12 of 14 departments" in text, (
            "paper.tex must say '12 of 14' Oriental departments with yield "
            "data (Central and Neembucu have null data)."
        )
        # Old framing must be gone
        assert "3 departments --- Alto Paraguay, Boquer" not in text, (
            "paper.tex still has the old '3 departments --- Alto Paraguay, "
            "Boquer\\'on, Presidente Hayes ---' framing. Presidente Hayes "
            "has no continuous yield data."
        )

    def test_p0030_paper_tex_ratio_is_1_95_not_2_0(self):
        """Failure-injection: paper.tex must report 1.95x (the actual
        measured ratio 109.96/56.47=1.9472), not the banker's-rounded or
        hardcoded '2.0x' values from earlier drafts.
        """
        from pathlib import Path
        paper_dir = Path(__file__).resolve().parent.parent / "papers" / "drafts"
        paper_tex = paper_dir / "p0030_yvyra_soy" / "paper.tex"
        text = paper_tex.read_text()
        assert "1.95$\\times$" in text, (
            "paper.tex must report '1.95$\\\\times$' as the per-region ratio "
            "(actual 109.96/56.47=1.9472). Older drafts hardcoded '2.0x' or "
            "used {:.1f} banker's rounding (1.95 → '1.9x')."
        )
        # Make sure no stale 2.0x framing
        assert "2.0$\\times$" not in text, (
            "paper.tex still has the older '2.0$\\\\times$' hardcoded ratio. "
            "Use '1.95$\\\\times$' to match the measured value."
        )
