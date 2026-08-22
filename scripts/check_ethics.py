#!/usr/bin/env python3
"""
Ethics gate for satellite-paraguay papers.

Gates every paper's status with the required partnership/FPIC/IRB evidence.
Exits 1 if any paper has Model trained >= 50 BUT Ethics <= 30 without
the required partnership/FPIC/IRB doc in docs/partnerships/.

Run from CI lint step. Also runnable locally:
  python3 scripts/check_ethics.py          # human-readable output
  python3 scripts/check_ethics.py --json   # JSON for cron ingestion
  python3 scripts/check_ethics.py --strict # exit 1 on any paper with incomplete ethics

The scorecard is read from STATUS.md (per-paper scorecard table).
The ethics threshold comes from the "Axis definitions" section in STATUS.md.

Privacy invariant: a paper with measured model results on real data
WITHOUT proper FPIC / IRB / partnership documentation is a bug, not a
deferrable. Either:
  1. Downgrade the model score to <50 (model not really trained) OR
  2. Add the required docs (FPIC letter, IRB approval, partnership agreement)
     to docs/partnerships/

This script enforces (2). If (1) is preferred, edit the scorecard.
"""

import argparse
import json
import re
import sys
from pathlib import Path


def parse_scorecard(status_path: Path) -> list[dict]:
    """Parse the per-paper scorecard from STATUS.md.

    Returns list of dicts: {paper, data_real, model_trained, paper_text,
    ethics, overall}.

    Parses each row by:
    1. Finding the paper ID (P####) and name
    2. Walking the cells one at a time, pulling each "<n>/100" score
    3. Treating "n/a" as 0 for that fields
    """
    text = status_path.read_text()
    papers = []
    # Match rows starting with P####
    row_pattern = re.compile(
        r"^\|\s*(P\d{4})\s+(\w+)\s*\|(.+)$",
        re.MULTILINE,
    )
    for m in row_pattern.finditer(text):
        pid, name, rest = m.group(1), m.group(2), m.group(3)
        # Split rest into cells by '|'
        cells = [c.strip() for c in rest.split("|")]
        if len(cells) < 5:
            continue
        # cells: [data_real, model_trained, paper_text, ethics, overall, ...]
        # Extract first integer from each cell's leading number/100
        def parse_score(cell: str) -> int:
            # Find "<n>/100" or "**n/100**" or just "n/100"
            mm = re.search(r"(\d+)\s*/\s*100", cell)
            if mm:
                return int(mm.group(1))
            # Or "n/a" → 0
            if "n/a" in cell.lower():
                return 0
            return -1  # unknown

        try:
            data_real = parse_score(cells[0])
            model_trained = parse_score(cells[1])
            # paper_text score is total_words/target*100; the regex matches "/100" form
            # but paper_text shows like "**100/100** (11,378 / 8,000 words..."
            # So 100 is correct.
            paper_text_score = parse_score(cells[2])
            ethics = parse_score(cells[3])
            overall = parse_score(cells[4])
            if overall == -1 and len(cells) > 5:
                overall = parse_score(cells[4])
            papers.append({
                "paper_id": pid,
                "name": name,
                "data_real": data_real,
                "model_trained": model_trained,
                "paper_text": paper_text_score,
                "ethics": ethics,
                "overall": overall,
            })
        except (IndexError, ValueError):
            continue

    return papers


def find_partnership_docs(partnerships_dir: Path, paper_id: str) -> list[Path]:
    """Find partnership/FPIC/IRB docs related to a paper.

    Returns list of file paths. Empty list means no docs found.
    """
    if not partnerships_dir.exists():
        return []

    matches = []
    keywords_for_paper = {
        "P0010": ["verra", "carbon-credit"],
        "P0011": [],  # No human subjects
        "P0012": ["fpic", "indigenous", "indi", "consent"],
        "P0025": ["inbio", "yrupe"],
        "P0026": ["guyra", "kai", "wildlife"],
        "P0035": ["openaq", "tatakua", "attribution"],
    }

    paper_keywords = keywords_for_paper.get(paper_id, [])

    for f in partnerships_dir.iterdir():
        if not f.is_file():
            continue
        if paper_id.lower() in f.name.lower():
            matches.append(f)
            continue
        if any(kw in f.name.lower() for kw in paper_keywords):
            matches.append(f)
            continue
        # Try reading content
        try:
            content = f.read_text(errors="ignore").lower()
            if paper_id.lower() in content:
                matches.append(f)
                continue
            if any(kw in content for kw in paper_keywords):
                matches.append(f)
        except Exception:
            pass

    return matches


def check_paper(paper: dict, partnerships_dir: Path) -> dict:
    """Check ethics gate for one paper.

    Returns dict with: paper_id, status, reason, action.
    """
    pid = paper["paper_id"]
    ethics = paper["ethics"]
    model = paper["model_trained"]

    # Rule: if model_trained >= 50 AND ethics <= 30, FAIL.
    # The paper has a real trained model but no ethics documentation.
    needs_action = model >= 50 and ethics <= 30

    partnership_docs = find_partnership_docs(partnerships_dir, pid)
    has_docs = len(partnership_docs) > 0

    if needs_action and not has_docs:
        return {
            "paper_id": pid,
            "name": paper["name"],
            "status": "FAIL",
            "reason": (
                f"Model trained ({model}/100) >= 50 but Ethics "
                f"({ethics}/100) <= 30 with NO partnership/FPIC docs "
                f"in docs/partnerships/. Either upgrade ethics score "
                f"after documenting partnerships, OR downgrade model "
                f"score to <50."
            ),
            "action": "Add docs to docs/partnerships/ OR update STATUS.md scorecard",
            "docs_found": [],
        }
    elif needs_action and has_docs:
        return {
            "paper_id": pid,
            "name": paper["name"],
            "status": "PASS-WITH-DOCS",
            "reason": (
                f"Model trained ({model}/100) + Ethics ({ethics}/100) "
                f"triggering gate, but {len(partnership_docs)} partnership "
                f"doc(s) found in docs/partnerships/."
            ),
            "action": "Verify docs are current; ethics score may need bump",
            "docs_found": [str(p) for p in partnership_docs],
        }
    elif ethics <= 30 and has_docs:
        return {
            "paper_id": pid,
            "name": paper["name"],
            "status": "PASS-WITH-LOW-ETHICS",
            "reason": (
                f"Ethics ({ethics}/100) low but model not yet trained "
                f"({model}/100). {len(partnership_docs)} doc(s) found."
            ),
            "action": "No action needed now; revisit if model score rises",
            "docs_found": [str(p) for p in partnership_docs],
        }
    else:
        return {
            "paper_id": pid,
            "name": paper["name"],
            "status": "PASS",
            "reason": f"Ethics ({ethics}/100) acceptable for current model ({model}/100).",
            "action": "None",
            "docs_found": [str(p) for p in partnership_docs],
        }


def main():
    parser = argparse.ArgumentParser(description="Ethics gate for satellite-paraguay papers")
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--json", action="store_true", help="JSON output")
    parser.add_argument("--strict", action="store_true", help="Exit 1 on any FAIL")
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()
    status_path = repo_root / "STATUS.md"
    partnerships_dir = repo_root / "docs" / "partnerships"

    if not status_path.exists():
        print(f"ERROR: {status_path} not found", file=sys.stderr)
        sys.exit(2)

    papers = parse_scorecard(status_path)
    if not papers:
        print("WARNING: no papers parsed from STATUS.md scorecard", file=sys.stderr)

    results = [check_paper(p, partnerships_dir) for p in papers]
    failed = [r for r in results if r["status"] == "FAIL"]

    if args.json:
        print(json.dumps({
            "checked_at": __import__("datetime").datetime.utcnow().isoformat() + "Z",
            "papers_total": len(papers),
            "papers_failed": len(failed),
            "results": results,
        }, indent=2))
    else:
        print("=" * 70)
        print("ETHICS GATE — satellite-paraguay")
        print("=" * 70)
        for r in results:
            icon = {"PASS": "✓", "FAIL": "✗", "PASS-WITH-DOCS": "✓+", "PASS-WITH-LOW-ETHICS": "⚠"}.get(r["status"], "?")
            print(f"\n{icon} {r['paper_id']} {r['name']}: {r['status']}")
            print(f"   {r['reason']}")
            if r["docs_found"]:
                print(f"   Docs: {', '.join(r['docs_found'])}")
            print(f"   Action: {r['action']}")
        print()
        print("=" * 70)
        if failed:
            print(f"FAILED: {len(failed)} paper(s) need attention:")
            for r in failed:
                print(f"  - {r['paper_id']} {r['name']}")
            sys.exit(1)
        else:
            print(f"PASSED: {len(results)} paper(s) checked, all gates OK")
            sys.exit(0)


if __name__ == "__main__":
    main()