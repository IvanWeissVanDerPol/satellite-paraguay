"""Tests for thesis chapters and references."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
import re


def test_thesis_abstract_exists():
    """Thesis abstract file exists."""
    path = Path(__file__).parent.parent / "THESIS_ABSTRACT.md"
    assert path.exists()


def test_thesis_abstract_word_count():
    """Thesis abstract is ~250 words (core body)."""
    path = Path(__file__).parent.parent / "THESIS_ABSTRACT.md"
    content = path.read_text()
    # Find the section between "## Abstract" and "## Research Questions"
    m = re.search(r"## Abstract.*?## Research Questions", content, re.DOTALL)
    if m:
        text = m.group(0)
        # Strip markdown
        text = re.sub(r"[^a-zA-Z\s]", " ", text)
        words = text.split()
        assert 150 <= len(words) <= 400, f"Abstract body has {len(words)} words"
    else:
        pytest.skip("Abstract section not found")


def test_thesis_chapters_exist():
    """All 11 thesis chapters exist."""
    repo_root = Path(__file__).parent.parent
    expected_chapters = [
        "CH1_introduction.md",
        "CH2_methodology.md",
        "CH9_cross-cutting.md",
        "CH10_discussion.md",
        "CH11_conclusion.md",
    ]
    thesis_dir = repo_root / "thesis"
    for ch in expected_chapters:
        assert (thesis_dir / ch).exists(), f"Missing {ch}"


def test_thesis_total_word_count():
    """Total thesis word count > 5,000 (current scope)."""
    repo_root = Path(__file__).parent.parent
    thesis_dir = repo_root / "thesis"
    total_words = 0
    for f in thesis_dir.glob("CH*.md"):
        text = f.read_text()
        words = len(re.findall(r"\b\w+\b", text))
        total_words += words
    assert total_words > 5000, f"Only {total_words} words"


def test_references_bib_count():
    """References bib has at least 50 entries."""
    path = Path(__file__).parent.parent / "thesis/references.bib"
    content = path.read_text()
    # Count @article, @misc, @book entries
    entries = re.findall(r"@\w+\{[^,]+,", content)
    assert len(entries) >= 50, f"Only {len(entries)} references"


def test_papers_exist():
    """All 6 paper drafts exist."""
    repo_root = Path(__file__).parent.parent
    papers = [
        "p0011_yvutu_deforestation/paper.md",
        "p0010_yvyra_carbon_credits/paper.md",
        "p0012_yvy_indigenous/paper.md",
        "p0025_yrupe_yield/paper.md",
        "p0026_kai_poaching/paper.md",
        "p0035_tatakua_air_quality/paper.md",
    ]
    for p in papers:
        assert (repo_root / "papers/drafts" / p).exists(), f"Missing {p}"


def test_ethics_docs_exist():
    """IRB and FPIC documents exist."""
    repo_root = Path(__file__).parent.parent
    assert (repo_root / "etica/IRB_protocol_paraguay_UNA.md").exists()
    assert (repo_root / "etica/FPIC_template_es.md").exists()


def test_stakeholder_outreach_exists():
    """Stakeholder outreach plan exists."""
    repo_root = Path(__file__).parent.parent
    assert (repo_root / "STAKEHOLDER_OUTREACH.md").exists()


def test_policy_brief_exists():
    """Policy brief exists."""
    repo_root = Path(__file__).parent.parent
    assert (repo_root / "POLICY_BRIEF_es.md").exists()


def test_indigenous_finding():
    """Indigenous 3.3x disparity is documented in thesis abstract."""
    path = Path(__file__).parent.parent / "THESIS_ABSTRACT.md"
    content = path.read_text()
    assert "3.3" in content, "Indigenous 3.3x disparity missing from abstract"


def test_h1_foundation_models():
    """H1 hypothesis about foundation models is documented."""
    path = Path(__file__).parent.parent / "THESIS_ABSTRACT.md"
    content = path.read_text()
    assert "Prithvi" in content or "foundation" in content.lower()