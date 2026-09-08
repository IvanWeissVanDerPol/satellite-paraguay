"""tests/test_numerical_consistency.py — Regression guard for Tier-6 numerical drift.

WHAT IT CATCHES
===============
The Tier-6 deep review (commit cb6363d, 27592fb, e8bd893) found 30+ instances
of paper.tex/paper.md/thesis-chapter files reporting numbers that contradicted
the canonical ACTUAL_RESULTS.md. Specific drift classes that recurred:

  1. Stale ratios: "3.0× / 3.3 times / 28.4%" when measured was 2.90× / 24.67%
  2. Stale RMSE: "RMSE 4.8" when measured was 14.7
  3. Stale ranges: "27–41%" when measured was 33.3–50.0%
  4. Stale areas: "43 kha" when measured was 43,466 km²
  5. Stale per-territory values: Mbyá Guaraní 2.91% when measured was 19.50%

WHY THIS TEST
=============
Without an explicit numerical-consistency test, future PRs can re-introduce
the same drift pattern. check_claims.py catches aspirational-claim regressions
but NOT measured-value drift (those values are "real", just outdated).

This test:
  - Loads each paper's ACTUAL_RESULTS.md as the source of truth
  - Defines the canonical measured numbers explicitly
  - Sweeps ALL .md / .tex files in papers/drafts/ + thesis/
  - Flags any occurrence of a stale number appearing in non-sanctioned contexts

The canonical-number table is curated manually; it MUST be updated whenever a
new measurement replaces an old one. See the "Updating canonical numbers"
section at the bottom of this file.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable

import pytest

REPO_ROOT = Path(__file__).parent.parent

# Canonical measured numbers, paper by paper. Updated 2026-09-07 (Tier-6).
# Each entry: (file_path_glob, list_of_stale_patterns_to_forbid).
#
# Why encode manually rather than auto-parse ACTUAL_RESULTS.md?
#   - Numbers appear in many forms in prose (RMSE 14.7, RMSE=14.7, 14.7 µg/m³)
#     so a regex-from-source parse produces false positives
#   - Manual curation forces a human to think about what to forbid
#   - The audit docs (AUDIT/TIER-6-DEEP-REVIEW-2026-09-07.md) document why
#     each canonical number is canonical

# Each entry: (label, regex_pattern, context_words_for_sanction)
# A match is only counted if the line does NOT contain any context_words.
CANONICAL_NUMBERS: list = [  # type: ignore[valid-type]  # 4th element is optional sentinel (bool)
    # ----- P0010 Yvyra: Verra carbon credits -----
    # Measured: 35.9% mean under-claim, range 33.3-50.0% (95% bootstrap CI excludes 0%)
    (
        "P0010 stale range 27-41%",
        r"\b27\s*[-–]\s*41\s*%",
        ("aspirational", "earlier", "replaced", "previous", "this report", "stale", "audit"),
        False,
    ),
    ("P0010 stale mean 4.44 Mt", r"\b4\.44\s*Mt", ("aspirational", "earlier", "replaced", "previous"), False),
    ("P0010 stale +1.14 Mt over-credit", r"\b1\.14\s*Mt", ("aspirational", "earlier", "replaced", "previous"), False),
    (
        "P0010 fabricated 30-Verra-project replication",
        r"30[\s-]+Verra\s+projects?\s+(across|in|throughout)",
        ("aspirational", "earlier", "replaced", "previous", "was not", "not yet", "honest"),
        False,
    ),
    # ----- P0011 Yvutu: Chaco deforestation -----
    # Measured F1 = 0.5592 / 0.4970; aspirational F1 = 0.876 in earlier drafts
    (
        "P0011 stale F1 = 0.876",
        r"F1\s*=\s*0\.876\b",
        ("aspirational", "earlier", "replaced", "previous", "honest", "stale"),
        False,
    ),
    (
        "P0011 stale mIoU = 0.794",
        r"mIoU\s*=\s*0\.794\b",
        ("aspirational", "earlier", "replaced", "previous", "honest", "stale"),
        False,
    ),
    # ----- P0012 Yvy: Indigenous territories -----
    # Measured: Mbyá Guaraní Itakyry = 19.50%; aspirational was 2.91%
    (
        "P0012 stale Mbyá Guaraní 2.91%",
        r"\bMbyá[^\n]*\b2\.91\s*%",
        ("aspirational", "earlier", "replaced", "previous", "honest", "stale", "audit"),
        False,
    ),
    (
        "P0012 stale 43 kha",
        r"\b43\s*kha\b",
        ("aspirational", "earlier", "replaced", "previous", "honest", "stale", "audit", "km²", "hectare"),
        False,
    ),
    # Measured: 2.90× with 95% CI [1.72, 4.20]; one-decimal rounded headline
    # is 3.0× (chosen per docs/decisions/OPEN-QUESTIONS-FOR-HUMAN-2026-09-07
    # Q6 recommendation A). The aspirational was 3.3×. The 3.0× form is
    # canonical (see THESIS_ABSTRACT.md L62-63 and STATUS.md P0012 scorecard),
    # so it is intentionally NOT in this stale-list.
    # Tier-6 escape class: LaTeX math mode renders × as `$\times$`, so we
    # must catch both the unicode × AND the LaTeX math-mode form.
    (
        "P0012 stale 28.4% indigenous average",
        r"\b28\.4\s*%\s+(?:which|average|of)",
        ("aspirational", "earlier", "replaced", "previous", "honest", "stale", "audit"),
        False,
    ),
    # Tier-6 escape class: prose mentions "2.9%" without "Mbyá" context and
    # without an honest-reporting disclaimer. The measured value is 19.50%.
    # The Mbyá context can be 1-2 lines away from the 2.9% value (multi-line
    # prose paragraph), so we use [\s\S] to span newlines within a window.
    # Use raw string with single [character class containing both \s and \S]
    # by using the dotall flag DOTALL — simpler: use re.DOTALL at compile time.
    # We mark these entries with a sentinel; the test loop compiles with DOTALL.
    (
        "P0012 stale Mbyá 2.9% prose (should be 19.50%)",
        r"\b(?:Mbyá|Mby\\'a).{0,80}?\b2\.9\s*\\?%",
        ("aspirational", "earlier", "replaced", "previous", "honest", "stale", "audit"),
        True,
    ),  # _use_dotall
    (
        "P0012 stale 'lowest loss (2.9%)' prose",
        r"\bloss\s*\(\s*2\.9\s*\\?%\s*\)",
        ("aspirational", "earlier", "replaced", "previous", "honest", "stale", "audit"),
        False,
    ),
    # ----- P0025 Yrupe: Soybean yield -----
    # Measured: MAE = 3.20 t/ha; aspirational was 0.74 / 0.78 / 0.81
    (
        "P0025 stale MAE = 0.74 t/ha",
        r"MAE\s*=\s*0\.74\s*t/ha",
        ("aspirational", "earlier", "replaced", "previous", "honest", "stale"),
        False,
    ),
    (
        "P0025 stale MAE < 1.0 t/ha in title/abstract",
        r"MAE\s*<\s*1\.0\s*t/ha",
        ("aspirational", "earlier", "replaced", "previous", "honest", "stale"),
        False,
    ),
    # ----- P0035 Tatakua: Air quality -----
    # Measured: RMSE 14.7 (3-layer × 64-hidden); aspirational was 4.8 / 6.1 / 8.6 / 11.72
    (
        "P0035 stale LSTM-1layer RMSE 4.8",
        r"LSTM-?1\s*layer[^.\n]*\b4\.8\b",
        ("aspirational", "earlier", "replaced", "previous", "honest", "stale", "audit", "measured"),
        False,
    ),
    (
        "P0035 stale LSTM-2layer RMSE 6.1",
        r"LSTM-?2\s*layer[^.\n]*\b6\.1\b",
        ("aspirational", "earlier", "replaced", "previous", "honest", "stale", "audit", "measured"),
        False,
    ),
    # 4.8 µg/m³ as headline RMSE (not in an honest-reporting disclaimer)
    (
        "P0035 stale RMSE 4.8 µg/m³",
        r"(?<![\d.])4\.8\s*(?:\\micro\s*g|µg|ug)[^\n]{0,8}m[^\n]{0,5}3",
        (
            "aspirational",
            "earlier",
            "replaced",
            "previous",
            "honest",
            "stale",
            "audit",
            "measured",
            "above",
            "is well above",
        ),
        False,
    ),
    # MAE = 11.72 µg/m³ as a measurement (NOT as a historical disclaimer)
    (
        "P0035 stale MAE = 11.72 (as measurement)",
        r"MAE\s*=\s*11\.72\b[^.\n]{0,40}\b(measured|pilot|achieved)",
        ("aspirational", "earlier", "replaced", "previous", "honest", "stale", "audit"),
        False,
    ),
]

# Files exempt from this check — they explain the bug history, document audits,
# or are themselves the source of truth.
SANCTIONED_PATH_PATTERNS = (
    re.compile(r"AUDIT/"),
    re.compile(r"ACTUAL_RESULTS\.md$"),
    re.compile(r"check_claims\.py$"),
    re.compile(r"check_numerical_consistency\.py$"),
    re.compile(r"test_numerical_consistency\.py$"),
    re.compile(r"defense_check\.py$"),
    re.compile(r"docs/CONVENTIONS\.md$"),
    re.compile(r"docs/REAL_TODO\.md$"),
    re.compile(r"docs/COMPREHENSIVE_TODO\.md$"),
    re.compile(r"docs/AGENT_TODO\.md$"),
    re.compile(r"docs/AUDIT_.*\.md$"),
    re.compile(r"docs/ROAST\.md$"),
    re.compile(r"docs/BRUTAL_ROAST\.md$"),
    re.compile(r"docs/CRITIC_.*\.md$"),
    re.compile(r"STATUS\.md$"),
    re.compile(r"WORKLOG_.*"),
    re.compile(r"TODO\.md$"),
    re.compile(r"README\.md$"),  # readme headlines often cite aspirational targets
    re.compile(r"ROAST\.md$"),
    re.compile(r"AGENT_TODO\.md$"),
    re.compile(r"BRUTAL_ROAST\.md$"),
    re.compile(r"COVER_LETTER.*"),
    re.compile(r"cover_letter.*"),
    re.compile(r"submission_checklist\.md$"),
    re.compile(r"reproducibility\.md$"),
    re.compile(r"quickstart\.sh$"),
)


def _is_sanctioned(path: Path) -> bool:
    """Return True if path is exempt from numerical-consistency check."""
    rel = str(path.relative_to(REPO_ROOT))
    return any(pat.search(rel) for pat in SANCTIONED_PATH_PATTERNS)


def _iter_text_files() -> Iterable[Path]:
    """Yield all .md / .tex files under papers/drafts/ and thesis/."""
    for sub in ("papers/drafts", "thesis"):
        base = REPO_ROOT / sub
        if not base.exists():
            continue
        for p in base.rglob("*"):
            if p.is_file() and p.suffix in (".md", ".tex"):
                yield p


def _line_contains_any(line: str, words: tuple[str, ...]) -> bool:
    """Case-insensitive substring check."""
    lower = line.lower()
    return any(w.lower() in lower for w in words)


def _context_qualifies(line: str, label: str) -> bool:
    """Return True if a stale number match is genuinely in an honest-reporting context.

    Beyond the per-pattern context_words, allow these universal
    historical-disclaimer phrases. These MUST be present somewhere on the same line.
    """
    UNIVERSAL_CONTEXT_WORDS = (
        "aspirational",
        "earlier drafts",
        "earlier versions",
        "previous drafts",
        "honest reporting",
        "this report",
        "honest-reporting",
        "honest pilot",
        "the stale",
        "the audit",
        "replaced by",
        "replaced with",
        "have been replaced",
        "was not a measurement",
        "not a measurement",
        "we replace",
        "tier-6",
        "earlier version",
    )
    return _line_contains_any(line, UNIVERSAL_CONTEXT_WORDS)


# ----- Parametric regression tests -----


@pytest.mark.parametrize(
    "label,pattern,context_words,_use_dotall", CANONICAL_NUMBERS, ids=[c[0] for c in CANONICAL_NUMBERS]
)
def test_no_stale_canonical_numbers(label, pattern, context_words, _use_dotall):
    """Tier-6 lesson: a paper can report measured-but-superseded numbers.

    Each test case scans every text file and fails if a stale number appears
    outside of an honest-reporting / historical-context sentence.
    """
    # _use_dotall is True for patterns that span multiple lines (e.g. Mbyá
    # context is on a different line from the 2.9% value). The sentinel
    # selects re.DOTALL.
    use_dotall = bool(_use_dotall)
    flags = re.IGNORECASE | (re.DOTALL if use_dotall else 0)
    rx = re.compile(pattern, flags)
    findings = []

    for f in _iter_text_files():
        if _is_sanctioned(f):
            continue
        try:
            text = f.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for m in rx.finditer(text):
            line_start = text.rfind("\n", 0, m.start()) + 1
            line_end = text.find("\n", m.end())
            if line_end == -1:
                line_end = len(text)
            # Context window: previous line + current line + next line.
            # This catches honest-reporting disclaimers split across LaTeX line breaks
            # where "aspirational and have been replaced" is on the next line.
            prev_start = text.rfind("\n", 0, line_start - 2) + 1
            prev_end = line_start - 1  # strip the \n
            next_end = text.find("\n", line_end + 1)
            if next_end == -1:
                next_end = len(text)
            context = (
                text[prev_start:line_start] + " " + text[line_start:line_end] + " " + text[line_end + 1 : next_end]
            )
            line = text[line_start:line_end].strip()
            if not line:
                continue
            if _line_contains_any(line, context_words):
                continue
            if _context_qualifies(context, label):
                continue
            line_no = text.count("\n", 0, m.start()) + 1
            rel = str(f.relative_to(REPO_ROOT))
            findings.append(f"  {rel}:{line_no}: {line[:120]}")

    assert not findings, (
        f"{label}: stale number found in {len(findings)} location(s). "
        f"If this number is now canonical (e.g. after a new measurement), update CANONICAL_NUMBERS "
        f"in tests/test_numerical_consistency.py. If it's in an honest-reporting context, "
        f"add the appropriate phrase to that line. Otherwise replace the stale number.\n" + "\n".join(findings[:30])
    )


def test_canonical_numbers_table_is_nonempty():
    """Sanity: there must be at least one entry to enforce.

    If someone clears the table by mistake, this test fires.
    """
    assert len(CANONICAL_NUMBERS) >= 10, (
        f"CANONICAL_NUMBERS has only {len(CANONICAL_NUMBERS)} entries. "
        "Tier-6 found 30+ stale-number regressions; a table smaller than 10 entries "
        "likely means the table was cleared. Restore from git history."
    )


# ----- Updating canonical numbers -----
#
# When a new measurement replaces an old one:
#   1. Add the OLD number to CANONICAL_NUMBERS above with a comment citing the
#      commit that introduced the replacement (e.g. # e8bd893, 2026-09-07)
#   2. Bump the comment date in this file's header
#   3. Run: .venv/bin/python -m pytest tests/test_numerical_consistency.py -v
#   4. If the test passes, commit. If it fails, find the unmarked stale location.
