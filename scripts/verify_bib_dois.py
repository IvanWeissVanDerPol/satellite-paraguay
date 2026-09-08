#!/usr/bin/env python3
"""verify_bib_dois.py — CrossRef title+author+year re-verification of master bib DOIs.

Reads ``thesis/references.bib``, queries CrossRef for each entry's
``<author> <title> <year>`` triple, and classifies the result:

- HIGH_CONF_UPDATE   — score ≥ 7; safe to auto-update DOI
- MED_CONF_REVIEW    — score 4-6; needs human review before update
- NO_MATCH_DROP      — score < 4; may be fabricated, keep as-is
- CR_OK              — current DOI matches best CrossRef hit (current is correct)

Usage:
    scripts/verify_bib_dois.py --start 0 --end 50        # Range of bib entries
    scripts/verify_bib_dois.py --key sze2022 fearnside2017  # Specific keys
    scripts/verify_bib_dois.py --resume                  # Continue from last run
    scripts/verify_bib_dois.py --summary                 # Summarize results
    scripts/verify_bib_dois.py --dry-run                 # Search but don't write

Notes:
    - Saves progress to /opt/data/scratchpad/verify_bib_progress.json
    - Rate-limited to 1.5s per query (CrossRef free tier)
    - 167 entries takes ~5 minutes wall-clock
"""

import argparse
import json
import os
import re
import time
import urllib.parse
import urllib.request
from collections import Counter

PROGRESS_PATH = "/opt/data/scratchpad/verify_bib_progress.json"
BIB_PATH = "/opt/data/work/satellite-paraguay/thesis/references.bib"

CROSSREF_UA = "thesis-verify/6.0 (mailto:ivan@weiss.ai)"


# ---------------------------------------------------------------------------
# Bib parsing
# ---------------------------------------------------------------------------


def parse_bib_entries(path):
    """Yield dicts: {key, type, author, title, year, doi} for each @entry{...}."""
    with open(path) as f:
        content = f.read()

    # Match @article{key, ... } (greedy until balanced close)
    entries = []
    pat = re.compile(r"@(\w+)\{([^,\s]+)\s*,", re.MULTILINE)
    for m in pat.finditer(content):
        etype = m.group(1)
        key = m.group(2)
        start = m.end()
        # Walk forward, counting braces
        depth = 1
        i = start
        while i < len(content) and depth > 0:
            c = content[i]
            if c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
            i += 1
        body = content[start : i - 1]

        # Extract fields
        def get_field(name):
            fp = re.search(rf"{name}\s*=\s*\{{([^}}]*)\}}", body, re.IGNORECASE)
            return fp.group(1).strip() if fp else ""

        entries.append(
            {
                "type": etype,
                "key": key,
                "author": get_field("author"),
                "title": get_field("title"),
                "year": get_field("year"),
                "doi": get_field("doi"),
            }
        )
    return entries


# ---------------------------------------------------------------------------
# CrossRef interaction
# ---------------------------------------------------------------------------


def crossref_search(query, limit=5, retries=2):
    """Search CrossRef. Returns list of dicts, or [{'error': ...}] on failure."""
    for attempt in range(retries):
        try:
            params = {"query.bibliographic": query, "rows": str(limit)}
            url = "https://api.crossref.org/works?" + urllib.parse.urlencode(params)
            req = urllib.request.Request(url, headers={"User-Agent": CROSSREF_UA})
            data = json.loads(urllib.request.urlopen(req, timeout=15).read())
            items = data.get("message", {}).get("items", [])
            return [
                {
                    "title": " ".join(it.get("title", [])),
                    "year": (it.get("issued", {}).get("date-parts", [[None]])[0] or [None])[0],
                    "doi": it.get("DOI"),
                    "authors": [a.get("family", "") for a in it.get("author", [])][:5],
                }
                for it in items
            ]
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(2**attempt)
            else:
                return [{"error": str(e)}]


# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------


def normalize_title(t):
    return re.sub(r"[^a-z0-9 ]", "", t.lower()).strip()


def title_overlap(bib_title, result_title):
    bib_words = [w for w in normalize_title(bib_title).split() if len(w) > 3][:3]
    res_norm = normalize_title(result_title)
    if not bib_words:
        return 0
    matches = sum(1 for w in bib_words if w in res_norm)
    return matches / len(bib_words)


def score_candidate(entry, r):
    if "error" in r or not r.get("doi"):
        return 0
    score = 0
    first_surname = entry["author"].split(",")[0].strip().lower()
    authors = [a.lower() for a in r.get("authors", [])]
    if first_surname and first_surname == (authors[0] if authors else ""):
        score += 4
    elif first_surname in authors:
        score += 2

    try:
        y_int = int(r.get("year"))
    except (TypeError, ValueError):
        y_int = 0
    try:
        e_y = int(entry["year"])
    except (TypeError, ValueError):
        e_y = 0

    if y_int and y_int == e_y:
        score += 3
    elif y_int and abs(y_int - e_y) <= 1:
        score += 1

    score += title_overlap(entry["title"], r.get("title", "")) * 2
    return score


def classify(score, current_doi, best_doi):
    """Return (action, severity)."""
    if not best_doi:
        return ("NO_MATCH_DROP", "info")
    if current_doi == best_doi:
        return ("CR_OK", "success")
    if score >= 7:
        return ("HIGH_CONF_UPDATE", "danger")
    if score >= 4:
        return ("MED_CONF_REVIEW", "warning")
    return ("NO_MATCH_DROP", "info")


# ---------------------------------------------------------------------------
# Progress management
# ---------------------------------------------------------------------------


def load_progress():
    if os.path.exists(PROGRESS_PATH):
        with open(PROGRESS_PATH) as f:
            return json.load(f)
    return []


def save_progress(progress):
    os.makedirs(os.path.dirname(PROGRESS_PATH), exist_ok=True)
    with open(PROGRESS_PATH, "w") as f:
        json.dump(progress, f, indent=2)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def verify_one(entry, dry_run=False):
    """Verify a single bib entry, return result dict.

    Always queries CrossRef (even if entry has no current DOI).
    Empty-DOI entries are the common case for Round-7 placeholders —
    without this query, the script would never find a DOI to verify.
    """
    first_surname = entry["author"].split(",")[0].strip() if entry["author"] else ""
    query = f"{first_surname} {entry['title']} {entry['year']}".strip()

    time.sleep(1.5)  # rate limit
    cr = crossref_search(query, limit=5)

    candidates = []
    if cr and not (len(cr) == 1 and "error" in cr[0]):
        for r in cr:
            if "error" not in r:
                candidates.append({"r": r, "score": score_candidate(entry, r)})
        candidates.sort(key=lambda c: c["score"], reverse=True)

    best = candidates[0]["r"] if candidates else None
    best_score = candidates[0]["score"] if candidates else 0

    # When entry has no DOI, a CrossRef match is a CANDIDATE_NEW_DOI
    # (the Round-7 placeholders need this branch — the previous version
    # short-circuited to NO_DOI and never queried).
    if not entry.get("doi"):
        if best and best_score >= 7:
            action = "CANDIDATE_NEW_DOI_HIGH_CONF"
        elif best and best_score >= 4:
            action = "CANDIDATE_NEW_DOI_MED_REVIEW"
        else:
            action = "NO_MATCH"
    else:
        action, _ = classify(best_score, entry.get("doi"), best["doi"] if best else None)

    return {
        **entry,
        "best_doi": best["doi"] if best else None,
        "best_year": best["year"] if best else None,
        "best_first_author": best["authors"][0] if best and best.get("authors") else None,
        "best_title": best["title"] if best else None,
        "best_score": best_score,
        "all_candidates": [
            {
                "doi": c["r"]["doi"],
                "year": c["r"]["year"],
                "authors": c["r"]["authors"],
                "score": c["score"],
            }
            for c in candidates[:3]
        ],
        "action": action,
    }


def cmd_verify(args):
    """Verify a range of bib entries."""
    entries = parse_bib_entries(BIB_PATH)
    print(f"Parsed {len(entries)} bib entries from {BIB_PATH}")

    if args.key:
        target = [e for e in entries if e["key"] in args.key]
    else:
        target = entries[args.start : args.end]

    print(f"Verifying {len(target)} entries...")

    progress = load_progress() if args.resume else []
    seen = {p["key"] for p in progress}

    for i, entry in enumerate(target):
        if entry["key"] in seen:
            continue

        result = verify_one(entry, dry_run=args.dry_run)
        progress.append(result)

        if (i + 1) % 10 == 0 or i == len(target) - 1:
            save_progress(progress)
            print(f"  [{i+1}/{len(target)}] saved {len(progress)} results")

    save_progress(progress)
    print_summary(progress)


def cmd_summary(args):
    """Summarize progress."""
    progress = load_progress()
    if not progress:
        print("No progress file found. Run verification first.")
        return
    print_summary(progress)


def print_summary(progress):
    counts = Counter(p.get("action", "UNKNOWN") for p in progress)
    print(f"\n=== CLASSIFICATION ({len(progress)} entries) ===")
    for action, count in counts.most_common():
        print(f"  {action}: {count}")

    high = [p for p in progress if p.get("action") == "HIGH_CONF_UPDATE"]
    if high:
        print(f"\n=== HIGH-CONFIDENCE FIXES ({len(high)}) ===")
        for p in high:
            print(f"  {p['key']}  (score={p['best_score']:.1f})")
            print(f"    {p.get('doi', '')} -> {p.get('best_doi', '')}")

    med = [p for p in progress if p.get("action") == "MED_CONF_REVIEW"]
    if med:
        print(f"\n=== MEDIUM-CONFIDENCE — NEEDS REVIEW ({len(med)}) ===")
        for p in med[:10]:
            print(f"  {p['key']}  (score={p['best_score']:.1f})")
        if len(med) > 10:
            print(f"  ... and {len(med) - 10} more")


def main():
    p = argparse.ArgumentParser(
        description="CrossRef title+author+year re-verification of master bib DOIs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("--start", type=int, default=0, help="First bib entry index")
    p.add_argument("--end", type=int, default=None, help="Last bib entry index (exclusive)")
    p.add_argument("--key", nargs="+", help="Specific bib keys to verify")
    p.add_argument("--resume", action="store_true", help="Skip entries already in progress file")
    p.add_argument("--summary", action="store_true", help="Just summarize existing progress")
    p.add_argument("--dry-run", action="store_true", help="Search but don't write")

    args = p.parse_args()

    if args.summary:
        cmd_summary(args)
    else:
        if args.end is None:
            args.end = len(parse_bib_entries(BIB_PATH))
        cmd_verify(args)


if __name__ == "__main__":
    main()
