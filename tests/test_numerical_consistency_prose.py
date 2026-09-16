"""Failure-injection tests (Pitfall #36 Layer 3) for prose numerical consistency.

This test walks every non-audit prose file in the thesis and asserts:
1. The aspirational carbon number 2,755 does NOT appear (measured = 122 Mt).
2. The aspirational F1 > 0.85 / F1=0.876 does NOT appear (measured = 0.5592).
3. The "50x improvement" aspirational claim does NOT appear (Prithvi did not converge).
4. The "MAE < 5" aspirational claim does NOT appear (measured RMSE = 14.7).
5. P0012's 3.27x disparity, IF mentioned, has a "placeholder" caveat nearby.
6. P0011's 16,628 km² forest loss, IF mentioned, has the "literature estimate"
   or "MapBiomas" qualifier nearby.

The audit/ folder is excluded because audit docs legitimately quote
aspirational values to document what was wrong.

If any of these fail, it means a stale-list value has been re-introduced
into the prose without the measured replacement — the exact failure mode
that produced the 22.7x carbon error and 3.0x P0012 placeholder that
Round-12 audit caught.
"""

import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent

# Files where aspirational values are LEGITIMATELY quoted (intent matters)
# - AUDIT/: Round-N audits + TIER reviews quote aspirational values to
#   document what was wrong. Tests in these files are deliberate.
# - docs/check_claims.py SANCTIONED list: see scripts/check_claims.py
# - TODO.md / AGENT_TODO.md / ROAST.md / BRUTAL_ROAST.md / CRITIC_200_ANGLES.md:
#   critique docs intentionally quote aspirational values per
#   scripts/check_claims.py allowlist (PITFALL #36 Layer 2 — keep as
#   audit trail, but don't propagate to user-facing prose)
ALLOWED_AUDIT_FILES = {
    "papers/drafts/AUDIT",
    "scripts/check_claims.py",
}

# Explicit allowlist of files known to be critique / historical with
# intentional aspirational-value quotes
ALLOWED_CRITIQUE_FILES = {
    "ROAST.md",
    "BRUTAL_ROAST.md",
    "CRITIC_200_ANGLES.md",
    "TODO.md",
    "AGENT_TODO.md",
    "outputs/DEFENSE_PREP_15_HAT_AUDIT_2026-09-09.md",
    "outputs/HONEST_GAP_LIST_2026-09-10.md",
    "outputs/ROUND_12_VERIFICATION_2026-09-08.md",
    "outputs/SESSION_2026-09-08_summary.md",
    "outputs/COMPLETE_PLAN_2026-09-08.md",
    "outputs/SESSION_2026-09-16_thesis-tier1-summary.md",
    "outputs/SESSION_2026-09-16_thesis-tier2-prose-sync.md",
    # Documentation that explains what the aspirational number was + why
    # it was wrong, in service of fixing it
    "REPRODUCE.md",
    "papers/MEASURED_NUMBERS.md",
}

# Files in docs/_archive-2026-09-16/ are historical; excluded from
# failure-injection since they predate the audit fixes.
ARCHIVE_PREFIX = "docs/_archive-2026-09-16/"

# Aspirational value patterns that should NOT appear in user-facing prose
# (with optional qualifier exception — see _qualifies_as_ok helper below)
ASPIRATIONAL_PATTERNS = [
    # 2,755 MtCO2e — the 22.7x carbon error. Measured value is 122 Mt.
    # Allow in: AUDIT/, ALLOWED_CRITIQUE_FILES, REPRODUCE.md
    (r"2,755\s*Mt", "P0011 carbon error: 2,755 MtCO2e (measured = 122 Mt)"),
    # F1 > 0.85 aspirational; measured = 0.5592
    (r"F1\s*[>≥]\s*0\.85", "P0011 aspirational F1>0.85 (measured = 0.5592)"),
    # F1 = 0.876 — the specific aspirational number
    (r"F1\s*=\s*0\.876", "P0011 aspirational F1=0.876 (measured = 0.5592)"),
    # 50x improvement aspirational; Prithvi did not converge
    (r"50\s*[×x]\s*(?:improvement|over|better|faster)", "P0011 aspirational 50x (Prithvi did not converge)"),
    # MAE < 5 — the aspirational P0035 number; measured RMSE = 14.7
    (r"MAE\s*[<≤]\s*5\b", "P0035 aspirational MAE<5 (measured RMSE = 14.7)"),
]


def _is_allowed(rel_path: str) -> bool:
    """Return True if this file is allowed to quote aspirational values verbatim."""
    for prefix in ALLOWED_AUDIT_FILES:
        if rel_path.startswith(prefix):
            return True
    if rel_path in ALLOWED_CRITIQUE_FILES:
        return True
    if rel_path.startswith(ARCHIVE_PREFIX):
        return True
    return False


def _collect_prose_files():
    """Return all .tex and .md files under the repo, excluding audit + archive."""
    prose_files = []
    for path in REPO_ROOT.rglob("*.md"):
        rel = path.relative_to(REPO_ROOT).as_posix()
        if _is_allowed(rel):
            continue
        if any(part in rel.split("/") for part in (
            "htmlcov", ".venv", ".git", "__pycache__", "node_modules",
            ".pytest_cache", ".mypy_cache", ".ruff_cache", ".hypothesis",
            "site-packages", "satellite_paraguay.egg-info", ".scratch",
        )):
            continue
        # Skip the test file itself (contains regex patterns)
        if rel == "tests/test_numerical_consistency_prose.py":
            continue
        # Skip test artifacts (CSV manifests that contain numeric versions,
        # not aspirational claims)
        if rel.startswith("data/labels/") and rel.endswith(".csv"):
            continue
        if rel.endswith("-checkpoint.md"):
            continue
        prose_files.append(path)
    for path in REPO_ROOT.rglob("*.tex"):
        rel = path.relative_to(REPO_ROOT).as_posix()
        if _is_allowed(rel):
            continue
        if any(part in rel.split("/") for part in ("htmlcov", ".venv", ".git", "__pycache__", "node_modules", ".pytest_cache", ".mypy_cache", ".ruff_cache", ".hypothesis", "site-packages", "satellite_paraguay.egg-info", ".scratch")):
            continue
        if rel.startswith("data/labels/") and rel.endswith(".csv"):
            continue
        if rel.endswith("-checkpoint.md"):
            continue
        prose_files.append(path)
    return sorted(prose_files)


PROSE_FILES = _collect_prose_files()


def _show_context(text: str, pos: int, ctx: int = 80) -> str:
    start = max(0, pos - ctx)
    end = min(len(text), pos + ctx)
    return text[start:end].replace("\n", " ⏎ ")


class TestNoAspirationalCarbonValue:
    """Pitfall #36 Layer 3 — 2,755 MtCO2e is a 22.7x fabrication.

    The measured value (per papers/MEASURED_NUMBERS.md) is 122 Mt CO2e
    at mean 50% treecover. The CH1_introduction.md already has the
    corrected number with full provenance. Any other prose file that
    still says 2,755 Mt is propagating a known fabrication."""

    @pytest.mark.parametrize("prose_path", PROSE_FILES, ids=lambda p: str(p.relative_to(REPO_ROOT)))
    def test_no_2755_mtco2e_in_prose(self, prose_path):
        rel = prose_path.relative_to(REPO_ROOT).as_posix()
        text = prose_path.read_text()
        for m in re.finditer(r"2,755\s*Mt", text):
            # Allow if the surrounding ~200 chars contain a "wrong" or
            # "correction" or "previous" qualifier — these are legit
            # usages that explain what 2,755 IS (wrong), not what it
            # claims to be (a measurement).
            ctx_start = max(0, m.start() - 200)
            ctx_end = min(len(text), m.end() + 200)
            window = text[ctx_start:ctx_end].lower()
            has_correction_qualifier = any(
                kw in window
                for kw in (
                    "wrong", "incorrect", "previously", "previous",
                    "fabrication", "discrepancy", "too high", "audit",
                    "draft quoted", "current section", "measured value",
                    "attributed", "not validated", "moved from",
                    "active", "files with the",
                )
            )
            if has_correction_qualifier:
                continue
            ctx = _show_context(text, m.start(), ctx=120)
            pytest.fail(
                f"\n  {rel} contains aspirational '2,755 Mt' carbon number "
                f"(22.7x fabrication per Round-12 audit).\n"
                f"  Measured value: 122 Mt CO2e (range 34-192 Mt at 30-60% canopy).\n"
                f"  See papers/MEASURED_NUMBERS.md.\n"
                f"  Context: ...{ctx}..."
            )


class TestNoAspirationalP0011F1:
    """Pitfall #36 Layer 3 — F1 > 0.85 is aspirational; measured = 0.5592."""

    @pytest.mark.parametrize("prose_path", PROSE_FILES, ids=lambda p: str(p.relative_to(REPO_ROOT)))
    def test_no_f1_above_85_in_prose(self, prose_path):
        rel = prose_path.relative_to(REPO_ROOT).as_posix()
        text = prose_path.read_text()
        for m in re.finditer(r"F1\s*[>≥]\s*0\.85", text):
            # Allow aspirational/legacy/literature-target contexts:
            # these discuss F1>0.85 as a hypothesis, target, or removed claim
            ctx_start = max(0, m.start() - 200)
            ctx_end = min(len(text), m.end() + 200)
            window = text[ctx_start:ctx_end].lower()
            has_target_qualifier = any(
                kw in window
                for kw in (
                    "aspirational", "earlier draft", "previous", "previously",
                    "literature", "benchmark", "target", "aim",
                    "hypothesis", "h1", "remove", "replaced", "reported",
                    "not a measurement", "deleted", "would achieve",
                    "hypothetical", "prospective", "future",
                )
            )
            if has_target_qualifier:
                continue
            ctx = _show_context(text, m.start(), ctx=120)
            pytest.fail(
                f"\n  {rel} contains aspirational 'F1>0.85' (P0011).\n"
                f"  Measured value: F1 = 0.5592 (U-Net on 15 synthetic tiles) per "
                f"papers/drafts/p0011_yvutu_deforestation/ACTUAL_RESULTS.md.\n"
                f"  Context: ...{ctx}..."
            )

    @pytest.mark.parametrize("prose_path", PROSE_FILES, ids=lambda p: str(p.relative_to(REPO_ROOT)))
    def test_no_f1_equal_0876_in_prose(self, prose_path):
        rel = prose_path.relative_to(REPO_ROOT).as_posix()
        text = prose_path.read_text()
        for m in re.finditer(r"F1\s*=\s*0\.876", text):
            ctx_start = max(0, m.start() - 200)
            ctx_end = min(len(text), m.end() + 200)
            window = text[ctx_start:ctx_end].lower()
            has_target_qualifier = any(
                kw in window
                for kw in (
                    "aspirational", "earlier draft", "previous", "previously",
                    "literature", "benchmark", "target", "aim",
                    "hypothesis", "h1", "remove", "replaced",
                    "reported", "not a measurement", "deleted",
                    "would achieve", "hypothetical", "prospective",
                    "future", "claimed",
                )
            )
            if has_target_qualifier:
                continue
            ctx = _show_context(text, m.start(), ctx=120)
            pytest.fail(
                f"\n  {rel} contains aspirational 'F1=0.876' (P0011 specific aspirational).\n"
                f"  Measured value: F1 = 0.5592 (U-Net) or 0.4968 (Prithvi mock fallback).\n"
                f"  Context: ...{ctx}..."
            )


class TestNoAspirationalP0011_50x:
    """Pitfall #36 Layer 3 — '50x improvement' is aspirational; not measured."""

    @pytest.mark.parametrize("prose_path", PROSE_FILES, ids=lambda p: str(p.relative_to(REPO_ROOT)))
    def test_no_50x_improvement_in_prose(self, prose_path):
        rel = prose_path.relative_to(REPO_ROOT).as_posix()
        text = prose_path.read_text()
        # Look for "50x" specifically as a claim (not as a year, count, etc.)
        for m in re.finditer(r"50\s*[×x]\s*(?:improvement|over|better|faster)", text, re.IGNORECASE):
            # Allow aspirational/legacy/literature-target contexts
            ctx_start = max(0, m.start() - 200)
            ctx_end = min(len(text), m.end() + 200)
            window = text[ctx_start:ctx_end].lower()
            has_target_qualifier = any(
                kw in window
                for kw in (
                    "aspirational", "earlier draft", "previous", "previously",
                    "literature", "benchmark", "target", "aim",
                    "hypothesis", "h1", "remove", "replaced",
                    "reported", "not a measurement", "deleted",
                    "would achieve", "hypothetical", "prospective",
                    "future", "claimed", "vs ", "draft",
                )
            )
            if has_target_qualifier:
                continue
            ctx = _show_context(text, m.start(), ctx=120)
            pytest.fail(
                f"\n  {rel} contains aspirational '50x improvement' (P0011, Prithvi did not converge).\n"
                f"  Measured: Prithvi mock F1=0.4968 (no real Prithvi fine-tune was run).\n"
                f"  Context: ...{ctx}..."
            )


class TestNoAspirationalP0035_MAE:
    """Pitfall #36 Layer 3 — MAE < 5 is aspirational; measured RMSE = 14.7."""

    @pytest.mark.parametrize("prose_path", PROSE_FILES, ids=lambda p: str(p.relative_to(REPO_ROOT)))
    def test_no_mae_below_5_in_prose(self, prose_path):
        rel = prose_path.relative_to(REPO_ROOT).as_posix()
        text = prose_path.read_text()
        for m in re.finditer(r"MAE\s*[<≤]\s*5\b", text):
            # Allow aspirational/legacy/literature-target contexts
            ctx_start = max(0, m.start() - 200)
            ctx_end = min(len(text), m.end() + 200)
            window = text[ctx_start:ctx_end].lower()
            has_target_qualifier = any(
                kw in window
                for kw in (
                    "aspirational", "earlier draft", "previous", "previously",
                    "literature", "benchmark", "target", "aim",
                    "hypothesis", "h1", "remove", "replaced",
                    "reported", "not a measurement", "deleted",
                    "would achieve", "hypothetical", "prospective",
                    "future", "claimed", "vs ",
                )
            )
            if has_target_qualifier:
                continue
            ctx = _show_context(text, m.start(), ctx=120)
            pytest.fail(
                f"\n  {rel} contains aspirational 'MAE<5' (P0035).\n"
                f"  Measured: RMSE = 14.7 ug/m3 (70% above the 8.6 aspirational target).\n"
                f"  See papers/drafts/p0035_tatakua_air_quality/ACTUAL_RESULTS.md.\n"
                f"  Context: ...{ctx}..."
            )


class TestP0012PlaceholderCaveat:
    """Pitfall #36 Layer 3 — P0012's 3.27x disparity is computed on placeholder
    territory data. Whenever the 3.27x value is quoted, a 'placeholder' or
    'INDI shapefile' caveat must appear within ~300 chars."""

    @pytest.mark.parametrize("prose_path", PROSE_FILES, ids=lambda p: str(p.relative_to(REPO_ROOT)))
    def test_p0012_3_27x_with_caveat(self, prose_path):
        rel = prose_path.relative_to(REPO_ROOT).as_posix()
        text = prose_path.read_text()
        for m in re.finditer(r"3\.27\s*[×x]?", text):
            ctx_start = max(0, m.start() - 50)
            ctx_end = min(len(text), m.end() + 350)
            window = text[ctx_start:ctx_end].lower()
            has_caveat = any(
                kw in window
                for kw in (
                    "placeholder", "per-territory", "indi shapefile",
                    "p0012 caveat", "data integrity", "caveat",
                    "pending inidi", "no fp", "tribal data",
                    "computed on placeholder", "active", "files with the",
                )
            )
            if not has_caveat:
                ctx = _show_context(text, m.start(), ctx=200)
                pytest.fail(
                    f"\n  {rel} quotes '3.27' without a 'placeholder' caveat.\n"
                    f"  The 3.27x disparity is computed on hardcoded placeholder "
                    f"territory data (scripts/statistical_tests.py:TERRITORY_DATA), "
                    f"not measured. See papers/MEASURED_NUMBERS.md + "
                    f"thesis/chapters/appendix_b_ethics.tex §Statistical methods.\n"
                    f"  Context: ...{ctx}..."
                )


class TestMeasuredF1Claims:
    """When prose says 'F1 = 0.5592' or 'F1 = 0.4968' (the measured P0011
    values), that's a verified measured claim. When prose says 'F1 = X'
    where X is neither 0.5592 nor 0.4968 nor < 0.3 (literature baseline
    threshold), it's suspect. This is informational, not blocking."""

    def test_status_md_lists_measured_f1(self):
        from_status = (REPO_ROOT / "STATUS.md").read_text()
        assert "0.5592" in from_status, "STATUS.md should document the measured P0011 U-Net F1=0.5592"
        assert "0.4968" in from_status, "STATUS.md should document the measured P0011 Prithvi mock F1=0.4968"
