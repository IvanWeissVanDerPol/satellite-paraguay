#!/usr/bin/env python3
"""v4 - improved verification using title-first search + OpenAlex + CrossRef fallback.

Strategy (in order):
  1. OpenAlex title-only search (best for novel titles)
  2. CrossRef title-first (title in query.bibliographic, no surname)
  3. CrossRef surname+title (existing v3 strategy)
  4. Score = max of all three

Scoring:
  - Same as v3 (Jaccard x2 + min-overlap, year bonus)
  - But now title-only matches can win (no surname requirement)
"""

import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path
from collections import defaultdict

# Load v3 results as the starting pool (only retry LIKELY + PARTIAL + NOT_FOUND)
V3 = Path("/opt/data/profiles/ivan/research/verification/results/verification_results_v3.json")
OUT = Path("/opt/data/profiles/ivan/research/verification/results/verification_results_v4.json")
OUT_REPORT = Path("/opt/data/profiles/ivan/research/verification/results/verification_report_v4.md")

STOP = set("a of the for and with in to is that by on from as this paper analysis study methods model studies two new".split())


def clean(s):
    return re.sub(r"[^a-z0-9À-Ü\s]", " ", s.lower())


def score(a, b):
    aw = [w for w in clean(a).split() if w and w not in STOP and len(w) > 2]
    bw = [w for w in clean(b).split() if w and w not in STOP and len(w) > 2]
    if not aw or not bw:
        return 0.0
    aset, bset = set(aw), set(bw)
    jacc = len(aset & bset) / len(aset | bset)
    overlap = len(aset & bset) / min(len(aset), len(bset))
    return max(jacc * 2, overlap)


def http_get(url, timeout=15):
    req = urllib.request.Request(url, headers={"User-Agent": "thesis-verify/4.0 (mailto:ivan@weiss.ai)"})
    return urllib.request.urlopen(req, timeout=timeout).read()


def openalex_search(title, year=None, limit=5):
    """OpenAlex /works?search=<title> — better title-only matching."""
    try:
        # OpenAlex uses polite pool with mailto
        params = {
            "search": title[:200],
            "per_page": str(limit),
            "mailto": "ivan@weiss.ai",
        }
        if year:
            params["filter"] = f"publication_year:{year - 1}-{year + 1}"
        url = "https://api.openalex.org/works?" + urllib.parse.urlencode(params)
        data = json.loads(http_get(url))
        results = []
        for w in data.get("results", []):
            t = w.get("title") or ""
            y = w.get("publication_year")
            doi = (w.get("doi") or "").replace("https://doi.org/", "")
            results.append({"title": t, "year": y, "DOI": doi, "source": "openalex"})
        return results
    except Exception as e:
        return [{"error": str(e), "source": "openalex"}]


def crossref_title_only(title, year=None, limit=5):
    """CrossRef with ONLY the title (no surname bias)."""
    try:
        params = {"query.bibliographic": title[:200], "rows": str(limit)}
        if year:
            params["filter"] = f"from-pub-date:{year - 1}-01-01,until-pub-date:{year + 1}-12-31"
        url = "https://api.crossref.org/works?" + urllib.parse.urlencode(params)
        data = json.loads(http_get(url))
        results = []
        for item in data.get("message", {}).get("items", []):
            t = " ".join(item.get("title", []))
            y = (item.get("issued", {}).get("date-parts", [[None]])[0][0])
            doi = item.get("DOI")
            results.append({"title": t, "year": y, "DOI": doi, "source": "crossref-title"})
        return results
    except Exception as e:
        return [{"error": str(e), "source": "crossref-title"}]


def crossref_surname_title(surname, year, title, limit=5):
    """v3 strategy: surname + title in bibliographic."""
    try:
        title_words = " ".join(title.split()[:10])
        params = {
            "query.author": surname,
            "query.bibliographic": title_words,
            "rows": str(limit),
        }
        if year:
            y = int(year)
            params["filter"] = f"from-pub-date:{y-1}-01-01,until-pub-date:{y+1}-12-31"
        url = "https://api.crossref.org/works?" + urllib.parse.urlencode(params)
        data = json.loads(http_get(url))
        results = []
        for item in data.get("message", {}).get("items", []):
            t = " ".join(item.get("title", []))
            y = (item.get("issued", {}).get("date-parts", [[None]])[0][0])
            doi = item.get("DOI")
            results.append({"title": t, "year": y, "DOI": doi, "source": "crossref-v3"})
        return results
    except Exception as e:
        return [{"error": str(e), "source": "crossref-v3"}]


def verify_entry(entry):
    """Run all 3 strategies, return best match + score."""
    title = entry["title"]
    surname = entry["surname"]
    year = entry.get("year")
    year_int = int(year) if year and year.isdigit() else None

    candidates = []
    # Strategy 1: OpenAlex title-only
    candidates.extend(openalex_search(title, year_int))
    time.sleep(0.4)
    # Strategy 2: CrossRef title-only
    candidates.extend(crossref_title_only(title, year_int))
    time.sleep(0.4)
    # Strategy 3: CrossRef surname+title
    candidates.extend(crossref_surname_title(surname, year_int, title))
    time.sleep(0.4)

    # Dedupe by DOI (or title+year)
    seen = set()
    deduped = []
    for c in candidates:
        if "error" in c:
            continue
        key = c.get("DOI") or (c.get("title", "")[:50], c.get("year"))
        if key in seen:
            continue
        seen.add(key)
        s = score(title, c.get("title", ""))
        # Year match bonus
        if year_int and c.get("year") and abs(int(c["year"]) - year_int) <= 1:
            s = min(1.0, s + 0.15)
        c2 = dict(c)
        c2["score"] = s
        deduped.append(c2)

    deduped.sort(key=lambda c: -c.get("score", 0))
    best = deduped[0] if deduped else None
    return best, deduped[:5]


def classify(score):
    if score >= 0.6:
        return "VERIFIED"
    if score >= 0.4:
        return "LIKELY"
    if score >= 0.2:
        return "PARTIAL"
    return "NOT_FOUND"


def main(target_statuses=("LIKELY", "PARTIAL", "NOT_FOUND")):
    v3 = json.load(open(V3))
    print(f"Loaded v3: {len(v3)} entries")

    # Only retry the unrecovered entries
    targets = [e for e in v3 if e.get("status") in target_statuses]
    print(f"Retrying {len(targets)} entries (statuses={target_statuses})")

    v4_results = []
    for i, entry in enumerate(targets):
        surname = entry["surname"]
        title = entry["title"]
        year = entry.get("year")
        try:
            best, top5 = verify_entry(entry)
            if best:
                score = best.get("score", 0)
                status = classify(score)
                v4_results.append({
                    "surname": surname,
                    "author": entry["author"],
                    "year": year,
                    "title": title,
                    "best_score": round(score, 3),
                    "status": status,
                    "best_match": {
                        "title": best.get("title", "")[:200],
                        "year": best.get("year"),
                        "DOI": best.get("DOI"),
                        "source": best.get("source"),
                    },
                    "top5": [{"title": c.get("title", "")[:200],
                              "year": c.get("year"),
                              "DOI": c.get("DOI"),
                              "score": round(c.get("score", 0), 3),
                              "source": c.get("source")} for c in top5],
                    "error": None,
                })
            else:
                v4_results.append({
                    "surname": surname, "author": entry["author"], "year": year,
                    "title": title, "best_score": 0, "status": "NOT_FOUND",
                    "best_match": None, "top5": [], "error": "no candidates",
                })
        except Exception as e:
            v4_results.append({
                "surname": surname, "author": entry["author"], "year": year,
                "title": title, "best_score": 0, "status": "ERROR",
                "best_match": None, "top5": [], "error": str(e),
            })

        if (i + 1) % 10 == 0:
            print(f"  [{i+1}/{len(targets)}] {surname} ({year}): {v4_results[-1]['status']} ({v4_results[-1]['best_score']})")

    # Merge with v3 — keep VERIFIED from v3 unchanged
    final = []
    seen_keys = set()
    for r in v4_results:
        key = (r["surname"], r["year"], r["title"])
        final.append(r)
        seen_keys.add(key)
    for r in v3:
        if r.get("status") == "VERIFIED":
            key = (r["surname"], r.get("year"), r["title"])
            if key not in seen_keys:
                final.append(r)
                seen_keys.add(key)

    # Sort by surname
    final.sort(key=lambda r: (r["surname"] or "", r.get("year") or ""))

    # Stats
    from collections import Counter
    by_status = Counter(r["status"] for r in final)
    print(f"\nFinal v4 distribution: {dict(by_status)}")
    print(f"Total: {len(final)}")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    json.dump(final, open(OUT, "w"), indent=2)
    print(f"Wrote: {OUT}")

    # Markdown report
    lines = [
        "# Round-3 Citation Verification Report (v4)",
        "",
        f"**Date:** {time.strftime('%Y-%m-%d')}",
        f"**Method:** OpenAlex title-only + CrossRef title-only + CrossRef surname+title, best-of-3 scoring",
        f"**Source:** `citations_to_verify.txt` (226 candidates from round-2)",
        "",
        "## Statistics",
        "",
        f"- Total candidates: {len(final)}",
        f"- ✅ **VERIFIED** (>0.6): {by_status.get('VERIFIED', 0)} ({100 * by_status.get('VERIFIED', 0) / len(final):.0f}%)",
        f"- ⚠️ **LIKELY** (0.4-0.6): {by_status.get('LIKELY', 0)} ({100 * by_status.get('LIKELY', 0) / len(final):.0f}%)",
        f"- 📝 **PARTIAL** (0.2-0.4): {by_status.get('PARTIAL', 0)} ({100 * by_status.get('PARTIAL', 0) / len(final):.0f}%)",
        f"- ❌ **NOT_FOUND** (<0.2): {by_status.get('NOT_FOUND', 0)} ({100 * by_status.get('NOT_FOUND', 0) / len(final):.0f}%)",
        "",
        "## ✅ NEW VERIFIED (promoted in v4 — not in v3)",
        "",
    ]
    v3_verified_keys = {(e["surname"], e.get("year")) for e in v3 if e.get("status") == "VERIFIED"}
    new_verified = [r for r in final if r["status"] == "VERIFIED" and (r["surname"], r.get("year")) not in v3_verified_keys]
    for r in new_verified:
        bm = r.get("best_match") or {}
        doi = bm.get("DOI", "?")
        lines.append(f"- **{r['surname']}, et al. ({r.get('year')})** → DOI: `{doi}` (score {r['best_score']})")
        lines.append(f"  - Matched: {bm.get('title', '')[:100]}")
        lines.append(f"  - Source: {bm.get('source', '?')}")
        lines.append(f"  - Input:  {r['title'][:100]}")
        lines.append("")
    lines.append(f"\n**Total promoted to VERIFIED in v4:** {len(new_verified)}")
    lines.append("")
    lines.append("## ⚠️ Still LIKELY (need manual review or DOI lookup)")
    lines.append("")
    for r in final:
        if r["status"] == "LIKELY":
            bm = r.get("best_match") or {}
            lines.append(f"- **{r['surname']} ({r.get('year')})** score {r['best_score']}")
            lines.append(f"  - Input:  {r['title'][:80]}")
            lines.append(f"  - Match:  {bm.get('title', '')[:80]} (DOI: {bm.get('DOI', '?')})")
    lines.append("")
    lines.append("## ❌ NOT_FOUND — likely fabricated (round-2 reconstruction artifacts)")
    lines.append("")
    lines.append("These need human verification or removal from the thesis:")
    lines.append("")
    for r in final:
        if r["status"] == "NOT_FOUND":
            lines.append(f"- **{r['surname']} ({r.get('year')})** — {r['title'][:90]}")

    OUT_REPORT.write_text("\n".join(lines))
    print(f"Wrote report: {OUT_REPORT}")
    return final


if __name__ == "__main__":
    main()
