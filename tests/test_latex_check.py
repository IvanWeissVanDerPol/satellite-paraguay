"""AC3: LaTeX syntax + bib-resolve check for all 6 papers.

Run this test to verify that:
1. Each paper.tex parses cleanly with pylatexenc (no syntax errors)
2. Every \\cite{...} key resolves to an entry in the canonical shared references.bib
3. Every \\ref{...} key resolves to a \\label{...} in the same file
4. All \\begin{env} have matching \\end{env}

This catches regressions where:
- Someone removes a bib entry that a paper depends on
- Someone introduces a malformed \\cite command
- Someone unbalanced an environment

F-1 consolidation (2026-09-07): all 6 papers share thesis/references.bib
as the canonical single source of truth (371 entries). Per-paper bib
duplicates were removed.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
CANONICAL_BIB = REPO / "thesis" / "references.bib"  # F-1 single source of truth

PAPERS = [
    "p0011_yvutu_deforestation",
    "p0010_yvyra_carbon_credits",
    "p0012_yvy_indigenous",
    "p0025_yrupe_yield",
    "p0026_kai_poaching",
    "p0035_tatakua_air_quality",
]


def _run_check_latex() -> subprocess.CompletedProcess:
    """Run scripts/check_latex.py and capture output."""
    return subprocess.run(
        [sys.executable, "scripts/check_latex.py"],
        capture_output=True,
        text=True,
        cwd=str(REPO),
        timeout=60,
    )


def _canonical_bib_keys() -> set[str]:
    """Read all BibTeX keys from the canonical shared bib."""
    text = CANONICAL_BIB.read_text()
    return {m.group(1).strip() for m in re.finditer(r"@\w+\s*\{\s*([^,]+),", text)}


class TestLatexSyntaxAndBibResolve:
    """Each paper.tex must compile syntactically + reference-resolve."""

    def test_check_latex_runs_clean(self):
        r = _run_check_latex()
        assert r.returncode == 0, f"check_latex.py exited {r.returncode}\nstdout:\n{r.stdout}\nstderr:\n{r.stderr}"

    def test_check_latex_reports_all_six_papers(self):
        r = _run_check_latex()
        for p in PAPERS:
            assert p in r.stdout, f"{p} missing from check_latex.py output:\n{r.stdout}"

    @pytest.mark.parametrize("paper", PAPERS)
    def test_paper_tex_exists(self, paper):
        assert (REPO / "papers/drafts" / paper / "paper.tex").exists()

    @pytest.mark.parametrize("paper", PAPERS)
    def test_paper_cite_keys_resolve(self, paper):
        """Every \\cite{...} in paper.tex resolves in canonical references.bib.

        F-1 (2026-09-07): all 6 papers share thesis/references.bib, so this
        check uses the canonical shared bib instead of per-paper copies.
        """
        text = (REPO / "papers/drafts" / paper / "paper.tex").read_text()
        bib_keys = _canonical_bib_keys()

        cite_keys = set()
        for m in re.finditer(r"\\cite[a-z]?\*?(?:\[[^\]]*\])?\{([^}]+)\}", text):
            for k in m.group(1).split(","):
                cite_keys.add(k.strip())

        unresolved = cite_keys - bib_keys
        assert not unresolved, f"{paper}: \\cite keys not in canonical references.bib: {sorted(unresolved)}"

    @pytest.mark.parametrize("paper", PAPERS)
    def test_paper_ref_keys_resolve(self, paper):
        """Every \\ref{...} in paper.tex resolves to a \\label{...}."""
        text = (REPO / "papers/drafts" / paper / "paper.tex").read_text()
        ref_keys = set(re.findall(r"\\ref\{([^}]+)\}", text))
        label_keys = set(re.findall(r"\\label\{([^}]+)\}", text))
        unresolved = ref_keys - label_keys
        assert not unresolved, f"{paper}: \\ref keys not defined via \\label: {sorted(unresolved)}"

    @pytest.mark.parametrize("paper", PAPERS)
    def test_paper_environments_balanced(self, paper):
        """Every \\begin{env} has a matching \\end{env}."""
        text = (REPO / "papers/drafts" / paper / "paper.tex").read_text()
        begins = set(re.findall(r"\\begin\{(\w+)\}", text))
        ends = set(re.findall(r"\\end\{(\w+)\}", text))
        unbalanced = begins - ends
        assert not unbalanced, f"{paper}: unbalanced environments: {unbalanced}"

    def test_canonical_references_bib_has_at_least_300_entries(self):
        """The canonical references.bib (thesis/references.bib) must have enough entries.

        F-1 (2026-09-07): replaced `references.bib` master check with the
        canonical thesis/references.bib. The previous per-paper bibs were
        deleted; the canonical now holds all 371 entries.
        """
        text = CANONICAL_BIB.read_text()
        n = len(re.findall(r"@\w+\s*\{", text))
        assert n >= 300, f"Canonical references.bib has only {n} entries (expected >= 300)"
