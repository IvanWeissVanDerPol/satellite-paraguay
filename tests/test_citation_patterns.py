"""tests/test_citation_patterns.py — Regression guard for Round-1/2/3/4/5/6 citation bugs.

Catches two classes of regression:
1. Bare `\cite{}` patterns (we use `\citep{}` or `\citet{}`)
2. Empty bib keys like `\citep{}` with nothing inside

Why: Round 1-3 had 226 citations reconstructed from prose; Round 4-6 cleaned
up via `check_citations.py`. Without a guard, a future PR could re-introduce
the bug.
"""
import re
from pathlib import Path

import pytest

PAPERS_ROOT = Path(__file__).parent.parent / "papers" / "drafts"

# Skip these — they're auto-generated or non-citation files
SKIP_BASENAMES = {"references.bib", "paper.bbl", "related_work.md"}


def _iter_paper_tex():
    """Yield all paper.tex files in papers/drafts/."""
    for paper_dir in sorted(PAPERS_ROOT.iterdir()):
        if not paper_dir.is_dir():
            continue
        tex = paper_dir / "paper.tex"
        if tex.exists():
            yield paper_dir.name, tex


def test_no_bare_cite_in_paper_tex():
    """Round-4 lesson: bare \\cite{} broke BibTeX ordering.

    Every citation in paper.tex MUST use \\citep{} or \\citet{} (or \\citeauthor{}).
    Bare \\cite{} is forbidden.
    """
    bad = []
    for paper_name, tex_path in _iter_paper_tex():
        text = tex_path.read_text()
        # Find bare \cite{ (not \citep, \citet, \citeauthor, \citealp, \citetext)
        # Word boundary after `\cite` prevents matching `\citep`.
        for m in re.finditer(r"\\cite(?![a-z])\s*\{", text):
            line_no = text.count("\n", 0, m.start()) + 1
            line = text.split("\n")[line_no - 1].strip()
            bad.append((paper_name, line_no, line[:80]))

    assert not bad, (
        "Found bare \\cite{} patterns (must use \\citep{} or \\citet{}):\n"
        + "\n".join(f"  {p}:{ln}: {l}" for p, ln, l in bad[:20])
    )


def test_no_empty_citation_brackets():
    """Forbid \\citep{}, \\citet{}, \\cite{} with empty content."""
    bad = []
    for paper_name, tex_path in _iter_paper_tex():
        text = tex_path.read_text()
        # Match \cite<word>{<whitespace only>} or \cite<word>{}
        for m in re.finditer(r"\\cite[a-z]*\s*\{\s*\}", text):
            line_no = text.count("\n", 0, m.start()) + 1
            bad.append((paper_name, line_no))

    assert not bad, (
        "Found empty citation brackets:\n"
        + "\n".join(f"  {p}:{ln}" for p, ln in bad[:20])
    )


def test_every_paper_has_a_conclusion():
    """Defense-blocking: every paper must have a \\section{Conclusion} or \\section*{Conclusion}.

    Added 2026-09-07 after Round-6 audit found 5 of 6 papers were missing
    Conclusion sections. Without Conclusion, the paper cannot be submitted
    to FADA or any peer-reviewed venue.
    """
    missing = []
    for paper_name, tex_path in _iter_paper_tex():
        text = tex_path.read_text()
        # Accept either \section{...} or \section*{...}
        if not re.search(r"\\section\*?\{[^}]*[Cc]onclusion", text):
            missing.append(paper_name)

    assert not missing, (
        "Papers missing Conclusion section:\n"
        + "\n".join(f"  {p}" for p in missing)
    )


def test_no_double_brackets_in_citations():
    """Forbid \\citep{{key}} or \\citep{key,extra}} with stray braces."""
    bad = []
    for paper_name, tex_path in _iter_paper_tex():
        text = tex_path.read_text()
        # Match \cite<word>{<key with { inside>}
        for m in re.finditer(r"\\cite[a-z]*\s*\{[^}]*\{", text):
            line_no = text.count("\n", 0, m.start()) + 1
            line = text.split("\n")[line_no - 1].strip()
            bad.append((paper_name, line_no, line[:80]))

    assert not bad, (
        "Found citations with stray opening brace:\n"
        + "\n".join(f"  {p}:{ln}: {l}" for p, ln, l in bad[:20])
    )


@pytest.mark.parametrize("paper_name,tex_path", list(_iter_paper_tex()))
def test_paper_tex_compiles_latex_balance(paper_name, tex_path):
    """All { must match }. LaTeX won't compile otherwise."""
    text = tex_path.read_text()
    # Skip preamble (before \begin{document})
    begin = text.find(r"\begin{document}")
    if begin == -1:
        pytest.skip(f"{paper_name}: no \\begin{{document}}")
        return
    body = text[begin:]

    opens = body.count("{")
    closes = body.count("}")
    # LaTeX bracing should balance in the body
    assert opens == closes, (
        f"{paper_name}: brace imbalance: {opens} open vs {closes} close"
    )
