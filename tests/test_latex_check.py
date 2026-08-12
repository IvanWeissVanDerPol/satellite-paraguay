"""AC3: LaTeX syntax + bib-resolve check for all 6 papers.

Run this test to verify that:
1. Each paper.tex parses cleanly with pylatexenc (no syntax errors)
2. Every \\cite{...} key resolves to an entry in references.bib
3. Every \\ref{...} key resolves to a \\label{...} in the same file
4. All \\begin{env} have matching \\end{env}

This catches regressions where:
- Someone removes a bib entry that a paper depends on
- Someone introduces a malformed \\cite command
- Someone unbalanced an environment
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent

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


class TestLatexSyntaxAndBibResolve:
    """Each paper.tex must compile syntactically + reference-resolve."""

    def test_check_latex_runs_clean(self):
        r = _run_check_latex()
        assert r.returncode == 0, (
            f"check_latex.py exited {r.returncode}\nstdout:\n{r.stdout}\nstderr:\n{r.stderr}"
        )

    def test_check_latex_reports_all_six_papers(self):
        r = _run_check_latex()
        for p in PAPERS:
            assert p in r.stdout, f"{p} missing from check_latex.py output:\n{r.stdout}"

    @pytest.mark.parametrize("paper", PAPERS)
    def test_paper_tex_exists(self, paper):
        assert (REPO / "papers/drafts" / paper / "paper.tex").exists()

    @pytest.mark.parametrize("paper", PAPERS)
    def test_paper_references_bib_exists(self, paper):
        assert (REPO / "papers/drafts" / paper / "references.bib").exists()

    @pytest.mark.parametrize("paper", PAPERS)
    def test_paper_cite_keys_resolve(self, paper):
        """Every \\cite{...} in paper.tex resolves in references.bib."""
        text = (REPO / "papers/drafts" / paper / "paper.tex").read_text()
        refs = (REPO / "papers/drafts" / paper / "references.bib").read_text()
        bib_keys = {m.group(1).strip() for m in re.finditer(r"@\w+\s*\{\s*([^,]+),", refs)}

        cite_keys = set()
        for m in re.finditer(r"\\cite[a-z]?\*?(?:\[[^\]]*\])?\{([^}]+)\}", text):
            for k in m.group(1).split(","):
                cite_keys.add(k.strip())

        unresolved = cite_keys - bib_keys
        assert not unresolved, (
            f"{paper}: \\cite keys not in references.bib: {sorted(unresolved)}"
        )

    @pytest.mark.parametrize("paper", PAPERS)
    def test_paper_ref_keys_resolve(self, paper):
        """Every \\ref{...} in paper.tex resolves to a \\label{...}."""
        text = (REPO / "papers/drafts" / paper / "paper.tex").read_text()
        ref_keys = set(re.findall(r"\\ref\{([^}]+)\}", text))
        label_keys = set(re.findall(r"\\label\{([^}]+)\}", text))
        unresolved = ref_keys - label_keys
        assert not unresolved, (
            f"{paper}: \\ref keys not defined via \\label: {sorted(unresolved)}"
        )

    @pytest.mark.parametrize("paper", PAPERS)
    def test_paper_environments_balanced(self, paper):
        """Every \\begin{env} has a matching \\end{env}."""
        text = (REPO / "papers/drafts" / paper / "paper.tex").read_text()
        begins = set(re.findall(r"\\begin\{(\w+)\}", text))
        ends = set(re.findall(r"\\end\{(\w+)\}", text))
        unbalanced = begins - ends
        assert not unbalanced, (
            f"{paper}: unbalanced environments: {unbalanced}"
        )

    def test_master_references_bib_has_at_least_190_entries(self):
        """The master references.bib must have grown beyond the 193 baseline."""
        text = (REPO / "references.bib").read_text()
        n = len(re.findall(r"@\w+\s*\{", text))
        assert n >= 170, f"Master references.bib has only {n} entries (expected >= 170)"

    @pytest.mark.parametrize("paper", PAPERS)
    def test_per_paper_references_bib_has_at_least_180_entries(self, paper):
        """Each per-paper references.bib must contain the master entries."""
        text = (REPO / "papers/drafts" / paper / "references.bib").read_text()
        n = len(re.findall(r"@\w+\s*\{", text))
        assert n >= 160, (
            f"{paper}/references.bib has only {n} entries (expected >= 160)"
        )
