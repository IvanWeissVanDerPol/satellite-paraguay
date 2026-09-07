"""tests/test_citation_completeness.py — Regression guard for broken \\cite{} keys.

WHAT IT CATCHES
===============
A \\citep{key} whose key is NOT in references.bib will:
  - Print "[?]" in the rendered PDF
  - Trigger "Citation 'key' undefined" warnings from bibtex
  - Silently break in journal review

The Tier-6 audit caught a missing `carroll2020care` bib entry that
caused "Carroll et al. 2020" to render as "[?]" in p0011 + p0012.

WHY THIS TEST
=============
A future PR could:
  - Add a new \\citep{newkey2025} without adding the bib entry
  - Rename a bib key without updating the cite calls
  - Use a typo in a cite key

This test fails CI if ANY \\cite{} key is not defined in references.bib.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).parent.parent
PAPERS_ROOT = REPO_ROOT / "papers" / "drafts"


# Match \cite, \citep, \citet, \citealp, \citeauthor, \citeyear, \citeyearpar
# with one or more comma-separated keys inside the braces.
CITE_PATTERN = re.compile(r"\\cite[a-z]*\{([^}]+)\}")

# Match @article{key, @book{key, @misc{key, etc.
BIB_ENTRY_PATTERN = re.compile(r"@\w+\{([^,\s]+)\s*,")


def _iter_paper_pairs():
    """Yield (paper_dir, paper.tex, references.bib) for each paper."""
    for paper_dir in sorted(PAPERS_ROOT.iterdir()):
        if not paper_dir.is_dir():
            continue
        tex = paper_dir / "paper.tex"
        bib = paper_dir / "references.bib"
        if tex.exists() and bib.exists():
            yield paper_dir, tex, bib


def _extract_cite_keys(tex_text: str) -> set[str]:
    """Return the set of all citation keys used in the tex file."""
    keys: set[str] = set()
    for m in CITE_PATTERN.finditer(tex_text):
        body = m.group(1)
        for k in body.split(","):
            k = k.strip()
            # Strip optional prefix/suffix like "[see p. 12]" in some keys
            k = re.sub(r"\[.*?\]", "", k).strip()
            if k:
                keys.add(k)
    return keys


def _extract_bib_keys(bib_text: str) -> set[str]:
    """Return the set of all bib entry keys defined in the bib file."""
    return {m.group(1).strip() for m in BIB_ENTRY_PATTERN.finditer(bib_text)}


# Parametrize one test per paper so failures point at the specific paper.
@pytest.mark.parametrize(
    "paper_name,tex_path,bib_path",
    [(d.name, d / "paper.tex", d / "references.bib") for d, _, _ in _iter_paper_pairs()],
    ids=[d.name for d, _, _ in _iter_paper_pairs()],
)
def test_all_cite_keys_resolve_to_bib(paper_name, tex_path, bib_path):
    """Every \\cite{key} in paper.tex must have a corresponding @entry in references.bib.

    Tier-6 lesson: missing `carroll2020care` entry caused p0011/p0012 to
    render Carroll et al. as "[?]" in the PDF.
    """
    tex_text = tex_path.read_text(encoding="utf-8")
    bib_text = bib_path.read_text(encoding="utf-8")
    cited = _extract_cite_keys(tex_text)
    defined = _extract_bib_keys(bib_text)
    unresolved = cited - defined

    assert not unresolved, (
        f"{paper_name}: {len(unresolved)} cited key(s) have no matching bib entry:\n"
        + "\n".join(f"  - {k}" for k in sorted(unresolved))
        + "\nAdd @entry{key, ...} to references.bib or fix the typo in paper.tex."
    )


def test_no_phantom_bib_entries_smoke():
    """Smoke test: every paper has at least 1 cite and at least 1 bib entry.

    Catches the empty-bib-file regression (a paper with no \\cite calls
    might be silently broken if the bib is empty too).
    """
    for paper_dir, tex, bib in _iter_paper_pairs():
        tex_text = tex.read_text(encoding="utf-8")
        bib_text = bib.read_text(encoding="utf-8")
        cited = _extract_cite_keys(tex_text)
        defined = _extract_bib_keys(bib_text)
        assert cited, f"{paper_dir.name}: no \\cite calls found in paper.tex"
        assert defined, f"{paper_dir.name}: no @entry keys found in references.bib"
        # Sanity: cited should be a subset of defined (we have other tests
        # for that, but ensure no obviously broken state here).
        unresolved = cited - defined
        assert not unresolved, (
            f"{paper_dir.name}: {len(unresolved)} unresolved cite key(s)"
        )
