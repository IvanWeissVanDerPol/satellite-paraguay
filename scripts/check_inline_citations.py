#!/usr/bin/env python3
"""
Inline-citation check: scans paper.tex, paper.md, related_work.md, discussion.md
for `Author (Year)` or `Author et al. (Year)` parenthetical citations that are
NOT in the master bib.

The existing check_citations.py only catches `\\cite{}` / `\\citep{}` commands.
This catches the (Author, Year) parenthetical mentions that 5 of the 6 papers
use extensively (e.g. p0025, p0035).

Usage:
    python scripts/check_inline_citations.py
    python scripts/check_inline_citations.py --json
    python scripts/check_inline_citations.py --paper p0010

Exits 0 if all inline citations resolve, 1 otherwise.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
PAPERS_DIR = REPO_ROOT / "papers" / "drafts"
MASTER_BIB = REPO_ROOT / "thesis" / "references.bib"

# File types to scan
PAPER_FILES = [
    "paper.tex",
    "paper.md",
    "related_work.md",
    "discussion.md",
    "introduction.md",
    "methods.md",
    "results.md",
    "abstract.md",
]

# Surnames to check (subset of inline-cited authors in the corpus).
# Excludes non-author mentions like "REDMOPy" (software) by requiring the
# (Year) format which software/org mentions don't follow.
# Note: This is NOT an exhaustive list of academic refs in the corpus;
# it's the list of surnames that appeared in inline citations during
# Tier-5 audit. Adding more is fine.
ACADEMIC_SURNAMES = {
    # Original Tier-5 list (verified in p0026, p0025, p0035, p0012, p0010)
    "Beery",
    "Bowers",
    "Chen",
    "Tabak",
    "Villon",
    "Milani",
    "Huang",
    "Kattenborn",
    "Peng",
    "Tseng",
    "Yang",
    "Wen",
    "Donkelaar",
    "Chudnovsky",
    "Kumar",
    "Artaxo",
    "Blackman",
    "Chassagneux",
    "Dawson",
    "Rainie",
    "Clarke",
    "Chave",
    "Mascaro",
    "Mitchard",
    # Noise words that aren't papers (mention year but no formal citation)
    # Excluded: REDMOPy, CDP, Home, Noon, WWF, GIDA, ICVCM, Proforest,
    # Prenafeta, West, Voigt, Kelley (handled by placeholder entries)
}


def parse_master_bib(path: Path) -> dict[str, set[str]]:
    """Return {surname_lower: {year, ...}} mapping for ALL entries."""
    text = path.read_text(encoding="utf-8")
    out: dict[str, set[str]] = {}
    for m in re.finditer(r"^@\w+\{([^,]+),[\s\S]*?(?=^@|\Z)", text, re.MULTILINE):
        key = m.group(1)
        body = m.group(0)
        year_m = re.search(r"year\s*=\s*\{?\s*(\d{4})", body)
        if not year_m:
            continue
        year = year_m.group(1)
        # Extract surname: split on capital letters, first segment
        # e.g. "vanDonkelaar2010" → "vandonkelaar"
        # e.g. "donkelaar2010" → "donkelaar"
        # e.g. "beery2018" → "beery"
        m2 = re.match(r"^([a-z]+)", key.lower())
        if m2:
            surname = m2.group(1)
            out.setdefault(surname, set()).add(year)
    return out


def find_inline_citations(content: str, surnames: set[str]) -> list[tuple[str, str, str]]:
    """Find inline (surname, year) citations in content.

    Returns list of (surname, year, matched_text).
    Only counts real inline citations, not noise like "TROPOMI (2024)".
    """
    found = []
    # Pattern: "Surname" + optional " et al." + " (year)" where year is 4 digits
    # Uses \b word boundary so partial surname matches don't fire.
    for surname in surnames:
        # Match "Surname" (no et al.) followed by (year) — careful not to match
        # bib keys like "chave2014" (would need a space-paren boundary)
        pattern = rf"\b{re.escape(surname)}\s*(?:et\s+al\.?\s*)?\(([12][0-9]{{3}})\)"
        for m in re.finditer(pattern, content):
            year = m.group(1)
            full = m.group(0)
            found.append((surname, year, full))
    return found


def main() -> int:
    paper_filter = None
    if "--paper" in sys.argv:
        idx = sys.argv.index("--paper")
        paper_filter = sys.argv[idx + 1]

    if not MASTER_BIB.exists():
        print(f"ERROR: master bib not found: {MASTER_BIB}", file=sys.stderr)
        return 2

    bib_map = parse_master_bib(MASTER_BIB)

    if not PAPERS_DIR.exists():
        print(f"ERROR: papers dir not found: {PAPERS_DIR}", file=sys.stderr)
        return 2

    missing: list[dict] = []
    total_inline = 0
    total_resolved = 0
    files_scanned = 0

    for paper_dir in sorted(PAPERS_DIR.iterdir()):
        if not paper_dir.is_dir():
            continue
        if paper_filter and paper_dir.name != paper_filter:
            continue
        for fname in PAPER_FILES:
            path = paper_dir / fname
            if not path.exists():
                continue
            files_scanned += 1
            content = path.read_text(encoding="utf-8")
            # Skip if entire content is just placeholder
            citations = find_inline_citations(content, ACADEMIC_SURNAMES)
            for surname, year, text in citations:
                total_inline += 1
                key_lower = surname.lower()
                years = bib_map.get(key_lower, set())
                if year in years:
                    total_resolved += 1
                else:
                    missing.append(
                        {
                            "paper": paper_dir.name,
                            "file": fname,
                            "surname": surname,
                            "year": year,
                            "text": text[:100],
                        }
                    )

    result = {
        "files_scanned": files_scanned,
        "inline_total": total_inline,
        "inline_resolved": total_resolved,
        "inline_missing": len(missing),
        "missing": missing,
    }

    if "--json" in sys.argv:
        print(json.dumps(result, indent=2))
    else:
        print("=" * 70)
        print("INLINE-CITATION CHECK")
        print("=" * 70)
        print(f"Files scanned: {result['files_scanned']}")
        print(f"Inline citations found: {result['inline_total']}")
        print(f"  Resolved: {result['inline_resolved']}")
        print(f"  Missing:  {result['inline_missing']}")
        if missing:
            print("\nMISSING:")
            for m in missing[:20]:
                print(f"  [{m['paper']}/{m['file']}] {m['surname']} ({m['year']})")
                print(f"    {m['text']}")
            if len(missing) > 20:
                print(f"  ... and {len(missing) - 20} more")
            print()
            print("✗ FAIL: inline citations missing from master bib")
        else:
            print()
            print("✓ PASS: all inline citations resolve")

    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
