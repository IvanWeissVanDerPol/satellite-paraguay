# Round-8 Verification Result — 2026-09-08

> **Action-only report.** Generated after the user chose **Option A** ("verify all 46 in a single Round-8 session — title+author+year constraint") from `docs/decisions/OPEN-QUESTIONS-FOR-HUMAN-2026-09-07.md` Q1.

## TL;DR

**1 of 45 placeholder entries is verifiable. 44 are not.** The Round-7 inline-citation scan synthesized plausible-looking (author, title, year) triples that do not match real CrossRef records. The open-questions doc had warned of this trap ("searching 'Beery 2018' returned a stormwater-infrastructure paper instead of Sara Beery's wildlife-CV paper"). The data confirms: the trap applies to **44 of 45** entries.

## What was done

1. **Fixed `scripts/verify_bib_dois.py`** — previous version short-circuited to `NO_DOI` for any entry without a current DOI (line 201), which meant the Round-7 placeholders never even reached the CrossRef API. New version queries CrossRef unconditionally and emits `CANDIDATE_NEW_DOI_HIGH_CONF` / `CANDIDATE_NEW_DOI_MED_REVIEW` / `NO_MATCH` for empty-DOI entries.

2. **Ran CrossRef verification on all 45 keys** (`--dry-run`, no file writes): 3 HIGH_CONF, 22 MED_REVIEW, 20 NO_MATCH.

3. **Inspected all 22 MED_REVIEW candidates** for false-positive traps: every single one matched a CrossRef paper with the right year + first-author surname but a **completely different topic**. Examples:
   - `chen2020` (MegaDetector, wildlife detection) → CrossRef hit: "Research on Detection and Tracking Technology of quad-rotor Aircraft Based on Open Source" (Cao/Chen 2020). Surname collision, not the same paper.
   - `tseng2022` (ImageNet → agricultural RS) → CrossRef hit: "DO WE STILL NEED IMAGENET PRE-TRAINING IN REMOTE SENSING SCENE CLASSIFICATION?" (Risojević 2022). Year matches, but Risojević is a different person.
   - `prenafeta2018` (voluntary carbon market verification) → CrossRef hit: "An investigation into the early stages of New Zealand's voluntary carbon market" (Birchall 2018). Same year + topic keywords, different paper.

4. **Inspected the 3 HIGH_CONF candidates**: only 1 is truly safe.
   - ✅ `beery2018` (score 9.0/11): exact title match + first-author match + year match. Canonical paper.
   - ❌ `chudnovsky2014` (score 7.0): title is "High resolution aerosol data from MODIS satellite for urban air quality studies" — different from "MODIS-to-PM2.5 scaling in the United States". Same first author (Chudnovsky), same year, different paper.
   - ❌ `dawson2021` (score 7.0): title is "SDG 10: Reduced Inequalities" — different from "Indigenous lands in active agricultural frontiers show reduced or reversed protective effects". Surname collision.

5. **Applied the one safe update** in `thesis/references.bib`:
   - `beery2018`: added `doi={10.1007/978-3-030-01270-0_28}`, replaced Round-7 placeholder note with a "Round-8 verified" note documenting the score + date.

6. **Did NOT modify the other 44 placeholder notes.** The original `note={Round-7 placeholder, DOI to be verified}` field remains accurate — the DOIs are still unverified. Re-tagging them as "Round-8 NO MATCH" would suggest a definitive conclusion the CrossRef data does not support (many of these papers may exist under slightly different titles/authors that CrossRef's title-search did not surface).

7. **Updated the banner comment** in `thesis/references.bib` above the placeholder section to document the Round-8 result + the rationale for not over-claiming.

## Verdict on Q1's Option A

**Option A was structurally unsound.** The premise was "verify all 46 in a single Round-8 session". The data shows **45 of 46 entries were fabricated at the title/author level** — they cannot be verified because they don't correspond to real papers (at least not under the round-7-supplied metadata). Verifying them would require:

- For each entry, manually searching arXiv, Google Scholar, ORCID, and the author's other publications to find the actual paper that the original prose cited.
- ~30–60 minutes per entry × 44 = **24–44 hours** of manual work, not 2–3 hours.
- Cannot be parallelized by me — requires human judgment (and often PDF access that I don't have).

The honest recommendation now is **a combination of Option B + manual lookup**:

- **B**: convert the 21 institutional `@misc` entries (REDMOPy, ICVCM, CDP, WWF, etc.) to `@misc` with `note={institutional reference, no DOI}` — they're not academic papers, DOIs don't apply.
- **Manual**: for the 23 academic `@article` entries, the actual cited papers must be located by Ivan or by a manual lookup session. The Round-7 (author, title, year) triples are placeholders, not real citations.

## Verified state at end of this task

```
check_claims.py:       OK -- no unsanctioned high-headline claims found.
check_latex.py:        FINAL: 6/6 papers pass
pytest fast (5 files): 64 passed in 2.74s
thesis/references.bib: 371 entries, braces balanced (2344 = 2344)
beery2018 DOI:         10.1007/978-3-030-01270-0_28 (Round-8 verified)
unverified entries:    44 (with Round-7 placeholder notes preserved)
```

## Files changed

| File | Change |
|---|---|
| `scripts/verify_bib_dois.py` | Removed the `if not entry.get("doi"): return NO_DOI` short-circuit. Now queries CrossRef unconditionally for all entries. |
| `thesis/references.bib` | Added verified DOI to `beery2018`; replaced Round-7 banner comment with Round-8 status banner documenting the result + rationale. Other 44 placeholder notes preserved. |

## Single recommendation

**Send the Round-8 result to the user + propose the B + Manual hybrid.** The full Option A as originally specified was based on the assumption that CrossRef could verify DOIs for entries that lacked them. The data shows that assumption was wrong — most of the entries are fabricated at the title/author level, and CrossRef cannot recover them via title-search. The right next step is:

1. Convert 21 institutional `@misc` entries to self-documenting format (5 min, my work).
2. Open a new Q for the 23 academic `@article` entries: each needs Ivan's manual lookup of the actual cited paper (1–4 hours per paper, depending on citation clarity in the prose).

Until then, **these 44 placeholder entries are NOT safe to cite**. The `note={Round-7 placeholder, DOI to be verified}` field is the runtime signal — anyone reviewing the bib should treat those entries as unverified.
