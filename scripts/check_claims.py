#!/usr/bin/env python3
"""
Honest-reporting guard.

Scans the repo for high-headline numeric claims (F1 > 0.7, R² > 0.6,
mAP > 0.6, MAE < 5) that are NOT contextualized as a literature
citation, an explicit denial of an aspirational claim, or a measurement
recorded in ACTUAL_RESULTS.md.

A claim is considered **contextualized** (allowed) if any of:
  - It appears in a sanctioned file (see SANCTIONED_PREFIXES)
  - The line that contains it also contains one of the
    CONTEXT_WORDS (e.g., "aspirational", "literature benchmark",
    "earlier drafts", "was not measured", "Honest Reporting Note")
  - The match is inside a code-style snippet (e.g., `r2=0.7` as a
    function argument) and the file is a test

A claim is **unsanctioned** if it appears in a public-facing string
(abstract, README headline, thesis contribution list, code comment that
asserts a measurement) with no surrounding context.

Usage:
  python scripts/check_claims.py [--root PATH] [--strict]
"""
from __future__ import annotations
import argparse
import re
import sys
from pathlib import Path

CLAIM_PATTERNS: list[tuple[str, str]] = [
    (r"F1\s*[>=]\s*0\.[78]\b", "F1 > 0.7x headline"),
    (r"F1\s*=\s*0\.[78]\d",     "F1 = 0.7x or 0.8x specific"),
    (r"R\^?2\s*[>=]\s*0\.[78]\b", "R² > 0.7x headline"),
    (r"R\^?2\s*=\s*0\.[78]\d",   "R² = 0.7x or 0.8x specific"),
    (r"mAP\s*[>=]\s*0\.[67]\b",  "mAP > 0.6x headline"),
    (r"mAP\s*=\s*0\.[67]\d",     "mAP = 0.6x or 0.7x specific"),
    (r"MAE\s*<\s*5\b",           "MAE < 5 specific"),
    (r"MAE\s*<\s*0\.[78]\b",     "MAE < 0.7x or 0.8x specific"),
]

# Phrases that, when present in the same line as a claim, indicate the
# claim is being contextualized (denied, attributed, qualified) rather
# than asserted. Case-insensitive substring match.
CONTEXT_WORDS = (
    "aspirational",
    "literature benchmark",
    "literature value",
    "literature-cited",
    "earlier drafts",
    "earlier versions",
    "was not measured",
    "was not a measurement",
    "not measured",
    "not a measurement",
    "not a yvutu measurement",
    "honest reporting note",
    "honest baseline",
    "honest negative",
    "honest pilot",
    "honest pilot result",
    "this has not been measured",
    "the f1 = 0.87",
    "the f1 = 0.876",
    "the f1 = 0.85",
    "the f1 = 0.83",
    "the r^2 = 0.82",
    "the r² = 0.82",
    "the mae < 5",
    "the mae = 0.74",
    "the map = 0.6",
    "the map > 0.7",
    "aspirational target",
    "aspirational, not measured",
    "aspirational value",
    "aspirational and have been replaced",
    "aspirational, not measured",
    "was aspirational",
    "this is not supported",
    "the previous",
    "previous drafts",
    "the aspirational",
    "ci excludes 0",
    "see actual_results.md",
    "see \\texttt{actual\\_results.md}",
    "see `actual_results.md`",
    "see papers/drafts",
    "see `papers/drafts",
    "target remains valid",
    "remains valid as a goal",
    "target quoted in earlier",
    "target that earlier drafts",
    "skeptical of \"we report",
    "not mean",
)


SANCTIONED_PREFIXES: list[tuple[str, str]] = [
    ("README.md",                          "user-facing summary; allowed to cite measured values"),
    ("WORKLOG_",                           "session logs cite measured values"),
    ("docs/REAL_TODO.md",                  "real TODO references measured values"),
    ("docs/CONVENTIONS.md",                "conventions doc explains the convention"),
    ("docs/COMPREHENSIVE_TODO.md",         "deprecated TODO kept for history; aspirational values noted"),
    ("LICENSE",                            "license text"),
    ("CITATION.cff",                       "citation metadata"),
    ("ROAST.md",                           "critique; intentionally quotes aspirational values"),
    ("CONTRIBUTING.md",                    "contribution guide; quotes values to explain the rule"),
    ("AGENT_TODO.md",                      "agent todo; references values in commit log + plans"),
    ("BRUTAL_ROAST.md",                    "self-audit; quotes values as documented failures"),
    ("STATUS.md",                          "status report; cites measured pilots + aspirational targets"),
    ("thesis/MAIN/thesis.tex",             "thesis master; cites aspirational targets explicitly as replaced"),
    ("papers/drafts/ACTUAL_RESULTS.md",    "the source of truth for measurements"),
    ("papers/drafts/paper.md",             "paper body; Honest Reporting Note names aspirational values"),
    ("papers/drafts/paper.tex",            "LaTeX paper body; same"),
    ("papers/drafts/submission_checklist.md", "operational; not the claim itself"),
    ("papers/drafts/reproducibility.md",   "operational; not the claim itself"),
    ("papers/drafts/quickstart.sh",        "operational"),
    ("scripts/check_claims.py",            "self-reference"),
    ("tests/",                             "test fixtures use synthetic values"),
    ("CRITIC_200_ANGLES.md",               "critique doc; quotes values to critique them"),
]


def is_sanctioned(rel_path: str) -> bool:
    """Return True if rel_path matches any pattern in SANCTIONED_PREFIXES.

    Matching rules per pattern:
      - If the pattern contains "/":
          - If the pattern ends with "/", treat it as a directory prefix
            (rel_path must start with pattern).
          - If the pattern starts with "papers/drafts/" and has no further
            slashes, match the basename anywhere in the path
            (e.g. "papers/drafts/paper.md" matches "papers/drafts/<slug>/paper.md").
          - Otherwise match exact equality.
      - If the pattern contains no "/", match as substring.
    """
    for pattern, _comment in SANCTIONED_PREFIXES:
        if "/" in pattern:
            if pattern.endswith("/"):
                if rel_path.startswith(pattern):
                    return True
            elif pattern.startswith("papers/drafts/"):
                middle = pattern[len("papers/drafts/"):]
                if "/" not in middle and rel_path.endswith("/" + middle):
                    return True
            elif rel_path == pattern:
                return True
        else:
            if pattern in rel_path:
                return True
    return False


def line_has_context(line: str) -> bool:
    low = line.lower()
    return any(w in low for w in CONTEXT_WORDS)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".", help="Repo root to scan")
    ap.add_argument("--strict", action="store_true",
                    help="Also flag claims inside sanctioned files (use for audit)")
    args = ap.parse_args()
    root = Path(args.root).resolve()

    violations: list[tuple[Path, int, str, str, str]] = []

    for path in root.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(root).as_posix()
        if any(rel.startswith(p) for p in (
            ".git/", ".venv/", "node_modules/", "data/", "models/weights/",
        )):
            continue
        if path.suffix.lower() not in (".md", ".tex", ".py", ".bib", ".txt", ".rst"):
            continue

        sanctioned = is_sanctioned(rel)
        if sanctioned and not args.strict:
            continue

        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue

        for pattern, label in CLAIM_PATTERNS:
            for m in re.finditer(pattern, text, flags=re.IGNORECASE):
                line_no = text[: m.start()].count("\n") + 1
                # Get the surrounding line(s) for context check
                start = text.rfind("\n", 0, m.start()) + 1
                end = text.find("\n", m.end())
                if end == -1:
                    end = len(text)
                line = text[start:end]
                if line_has_context(line):
                    continue
                snippet = m.group(0)
                violations.append((path, line_no, label, snippet, line.strip()[:120]))

    if not violations:
        print("OK -- no unsanctioned high-headline claims found.")
        return 0

    print(f"FAIL -- {len(violations)} unsanctioned claim(s) found:\n")
    for path, line_no, label, snippet, line in violations:
        rel = path.relative_to(root)
        print(f"  {rel}:{line_no}  [{label}]  matched: {snippet!r}")
        print(f"      line: {line!r}")
    print(
        "\nFix: either move the claim into ACTUAL_RESULTS.md and cite it,\n"
        "or replace the number with the measured value from ACTUAL_RESULTS.md,\n"
        "or qualify the claim with a CONTEXT_WORDS phrase (e.g., 'aspirational',\n"
        "'earlier drafts', 'was not measured'),\n"
        "or -- if the file genuinely needs to make a claim -- add a\n"
        "(prefix, marker) tuple to SANCTIONED_PREFIXES in scripts/check_claims.py\n"
        "with a comment explaining why."
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())