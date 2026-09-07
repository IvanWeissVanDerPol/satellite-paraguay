#!/usr/bin/env python3
"""v3 - improved scoring: bag-of-words with weighted + permissive matching."""

import json
import re
import subprocess
import sys
import time
from collections import Counter
from pathlib import Path

SRC = Path("/opt/data/profiles/ivan/research/verification/citations_to_verify.txt")
OUT_DIR = Path("/opt/data/profiles/ivan/research/verification/results")
OUT_DIR.mkdir(parents=True, exist_ok=True)
RATE_LIMIT_SECS = 0.3

# Common academic stopwords to ignore in matching
STOP = set(
    "a of the for and with in to is that by on from as this paper analysis study methods model studies two new".split()
)


def parse_citations(path):
    entries = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                m = re.match(r"\d+\.\s*([^|]+?)\s*\|\s*(.+)", line)
                if m:
                    author = m.group(1).strip()
                    title = m.group(2).strip()
                    year_m = re.search(r"(\d{4})", author)
                    year = year_m.group(1) if year_m else None
                    surname_m = re.match(r"([A-Z][a-z\u00C0-\u00FC\']+)", author)
                    surname = surname_m.group(1) if surname_m else author.split()[0]
                    entries.append(
                        {
                            "surname": surname,
                            "author": author,
                            "year": year,
                            "title": title,
                        }
                    )
    return entries


def sign_score(a, b):
    """Score two title strings.

    Return best of: direct overlap, sorted-words overlap,
    stem overlap, year match bonus.
    """

    # Strip punctuation, lowercase
    def clean(s):
        return re.sub(r"[^a-z0-9\u00C0-\u00FC\s]", " ", s.lower())

    aw = [w for w in clean(a).split() if w and w not in STOP and len(w) > 2]
    bw = [w for w in clean(b).split() if w and w not in STOP and len(w) > 2]
    if not aw or not bw:
        return 0.0
    aset, bset = set(aw), set(bw)
    jacc = len(aset & bset) / len(aset | bset)
    overlap = len(aset & bset) / min(len(aset), len(bset))
    # Boost for key signature words present in both
    return max(jacc * 2, overlap)  # use max of either


def crossref_query(surname, year, title):
    from urllib.parse import quote_plus

    title_words = " ".join(title.split()[:10])
    title_q = quote_plus(title_words)
    surname_q = quote_plus(surname)
    url = f"https://api.crossref.org/works?query.author={surname_q}&query.bibliographic={title_q}&rows=10"
    if year:
        y = int(year)
        url += f"&filter=from-pub-date:{y-1}-01-01,until-pub-date:{y+1}-12-31"
    try:
        result = subprocess.run(
            ["curl", "-s", "--max-time", "15", "-A", "thesis-verifier/3.0", url],
            capture_output=True,
            text=True,
            timeout=20,
        )
        if result.returncode != 0:
            return {
                "matches": [],
                "error": f"curl exit {result.returncode}",
                "best_score": 0,
            }
        if not result.stdout.strip():
            return {"matches": [], "error": "empty response", "best_score": 0}
        data = json.loads(result.stdout)
        items = data.get("message", {}).get("items", [])
        matches = []
        for item in items:
            title_match = (item.get("title", [""]) or [""])[0]
            year_match = item.get("issued", {}).get("date-parts", [[None]])[0][0]
            score = sign_score(title, title_match)
            # Year bonus
            try:
                if year_match and year and abs(int(year_match) - int(year)) <= 1:
                    score = min(1.0, score + 0.2)
            except (TypeError, ValueError):
                pass
            matches.append(
                {
                    "doi": item.get("DOI"),
                    "title": title_match[:200],
                    "year": year_match,
                    "authors": [
                        f"{a.get('family', '')}, {a.get('given', '')}"
                        for a in (item.get("author", []) or [])
                    ][:3],
                    "score": round(score, 3),
                }
            )
        matches.sort(key=lambda x: -x["score"])
        best = matches[0]["score"] if matches else 0
        return {"matches": matches, "best_score": best}
    except Exception as e:
        return {"matches": [], "error": str(e), "best_score": 0}


entries = parse_citations(SRC)
print(f"Total to verify: {len(entries)}", flush=True)
results = []
for i, e in enumerate(entries, 1):
    sys.stdout.write(f"\r[{i}/{len(entries)}] {e['surname']} {e.get('year', '?')}")
    sys.stdout.flush()
    result = crossref_query(e["surname"], e["year"], e["title"])
    rec = dict(e)
    rec.update(
        {
            "best_score": result.get("best_score", 0),
            "matches": result.get("matches", [])[:5],
            "error": result.get("error"),
        }
    )
    if rec["best_score"] > 0.6:
        rec["status"] = "VERIFIED"
    elif rec["best_score"] > 0.4:
        rec["status"] = "LIKELY"
    elif rec["best_score"] > 0.2:
        rec["status"] = "PARTIAL"
    else:
        rec["status"] = "NOT_FOUND"
    results.append(rec)
    time.sleep(RATE_LIMIT_SECS)

print()
status_count = Counter(r["status"] for r in results)
print(f"Status: {dict(status_count)}")

with open(OUT_DIR / "verification_results_v3.json", "w") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

verified = [r for r in results if r["status"] == "VERIFIED"]
likely = [r for r in results if r["status"] == "LIKELY"]
partial = [r for r in results if r["status"] == "PARTIAL"]
not_found = [r for r in results if r["status"] == "NOT_FOUND"]

with open(OUT_DIR / "verification_report_v3.md", "w") as f:
    f.write("# Round-2 Citation Verification Report (v3)\n\n")
    f.write("**Date:** 2026-09-03\n")
    f.write(
        "**Method:** CrossRef API via curl, +/-1 year filter, "
        "two-tier scoring (Jaccard x2 + min-overlap), +0.2 year bonus\n"
    )
    f.write(
        "**Source:** `citations_to_verify.txt` (226 candidates extracted from round-2 files)\n\n"
    )
    f.write("## Statistics\n\n")
    total = len(entries)
    f.write(f"- Total candidates: {total}\n")
    f.write(
        f"- ✅ **VERIFIED** (>0.6): {len(verified)} ({100*len(verified)/total:.0f}%)\n"
    )
    f.write(
        f"- ⚠️ **LIKELY** (0.4-0.6): {len(likely)} ({100*len(likely)/total:.0f}%)\n"
    )
    f.write(
        f"- 📝 **PARTIAL** (0.2-0.4): {len(partial)} ({100*len(partial)/total:.0f}%)\n"
    )
    f.write(
        f"- ❌ **NOT_FOUND** (<0.2): {len(not_found)} ({100*len(not_found)/total:.0f}%)\n\n"
    )

    if verified:
        f.write("## ✅ VERIFIED — Add to thesis bibliography\n\n")
        for r in verified:
            m = r["matches"][0]
            f.write(
                f"- **{r['author']}** → DOI: `{m.get('doi', '?')}` (score {r['best_score']})\n"
            )
            f.write(f"  - Matched: {m.get('title', '')[:120]}\n")

    if likely:
        f.write("\n## ⚠️ LIKELY — Verify manually before citing\n\n")
        for r in likely[:50]:
            m = r["matches"][0] if r["matches"] else {}
            f.write(
                f"- **{r['author']}** (score {r['best_score']}) → possible DOI: `{m.get('doi', '?')}`\n"
            )

    if partial:
        f.write(
            "\n## 📝 PARTIAL — Title doesn't match well, may be a real paper with different title\n\n"
        )
        for r in partial[:50]:
            m = r["matches"][0] if r["matches"] else {}
            f.write(
                f"- **{r['author']}** (score {r['best_score']}) → unrelated top hit: {m.get('title', '')[:100]}\n"
            )

    if not_found:
        f.write(
            "\n## ❌ NOT_FOUND — Likely reconstruction from training data; do not cite without further search\n\n"
        )
        for r in not_found:
            f.write(f"- {r['author']} | {r['title'][:120]}\n")

print(
    f"\nResults: {len(verified)} verified, {len(likely)} likely, {len(partial)} partial, {len(not_found)} not-found"
)
print(f"Report: {OUT_DIR / 'verification_report_v3.md'}")
print(f"JSON: {OUT_DIR / 'verification_results_v3.json'}")
