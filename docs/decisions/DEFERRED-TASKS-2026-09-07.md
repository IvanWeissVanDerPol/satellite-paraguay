# Deferred Tasks — Post-Defense Follow-Up

**Created:** 2026-09-07
**Decision source:** `docs/decisions/OPEN-QUESTIONS-FILTERED-2026-09-07.md`

This file tracks Tier-2 questions that were deferred with TODO markers.
None block the thesis defense; all are post-defense cleanup work.

---

## TODO: Manual DOI verification for 46 Round-7 placeholder entries

**File locations:**
- `thesis/references.bib` — 48 entries
- `papers/drafts/p0010_yvyra_carbon_credits/references.bib` — 45 entries
- `papers/drafts/p0011_yvutu_deforestation/references.bib` — 45 entries
- `papers/drafts/p0012_yvy_indigenous/references.bib` — 45 entries
- `papers/drafts/p0025_yrupe_yield/references.bib` — 45 entries
- `papers/drafts/p0026_kai_poaching/references.bib` — 45 entries
- `papers/drafts/p0035_tatakua_air_quality/references.bib` — 45 entries

**Marker pattern in bib:**
```
note = {Round-7 placeholder, DOI to be verified}
```

**Why deferred:**
- 46 placeholder entries added during Round-7 work
- CrossRef title-only search returned wrong results for some
- Manual verification takes ~2 hours
- Defense-check tolerates these as "non-critical warnings"

**Plan (post-defense):**
1. Extract all entries with `note = {Round-7 placeholder, ...}`
2. Sort by `\cite{}` count in papers (top 10 cover ~80%)
3. Verify top 10 via DOI lookup
4. Replace `note = {Round-7 placeholder, DOI to be verified}` with actual DOI
5. Re-run `defense_check.py` — expect zero placeholder warnings

**Acceptance criteria:**
- Zero entries with `note = {Round-7 placeholder, ...}`
- All 46 DOIs verified via CrossRef or DOI.org

---

## TODO: Round-6 left 83 "no good CrossRef match" entries

**File locations:** Same bib files as above

**Marker pattern in bib:**
```
note = {Round-6 no good CrossRef match}
```

**Why deferred:**
- 83 entries with real works but possibly wrong metadata
- CrossRef failed; needs Google Scholar + OpenAlex cross-check
- High-effort manual research

**Plan (post-defense):**
1. Extract all entries with `note = {Round-6 no good CrossRef match}`
2. Cross-check each via OpenAlex API (`https://api.openalex.org/works?search=<title>`)
3. If OpenAlex returns a match with high confidence, update DOI/year/author
4. If no match, downgrade to `note = {Round-6 unverifiable, see OpenAlex}`

**Acceptance criteria:**
- All 83 entries either have a verified DOI or a clear "unverifiable" marker
- Bib integrity restored

---

## TODO: Sync local main with origin/main

**Why:** Local main was 48 commits behind origin/main before merge.
**Plan:** `git pull --rebase` after merge to ensure clean local state.

---

## How to track these TODOs

Use `grep -rn 'Round-7 placeholder\|Round-6 no good' thesis/ papers/drafts/` to find current state.
