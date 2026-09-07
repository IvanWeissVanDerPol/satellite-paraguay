# Open Questions — Filtered for Human Input

**Date:** 2026-09-07
**Branch:** `feat/tier2-consistency-thesis-integration`
**Source:** Filtered from `OPEN-QUESTIONS-FOR-HUMAN-2026-09-07.md`
**Filter rule:** Only items that genuinely need human judgment. Auto-applied best-option items are listed at the bottom.

---

## Tier 1 — DECIDE BEFORE THESIS DEFENSE (cannot wait)

### Q1.1 — Run `git filter-repo` to purge secret from git history?

**Context:** Branch `main` is 48 commits behind origin/main. Some commits in the thesis-history may contain a previously-removed token. `gitleaks` is currently SKIPPED on CI (passive scan).

**Options:**
- **(A) Run `git filter-repo` now** — purges from history; requires force-push to main
- (B) Leave history as-is, add `gitleaks` as required CI check (defense in depth)
- (C) Wait until post-defense

**Recommendation:** **(B)** — adds defense without rewriting history. `filter-repo` is irreversible and force-push is forbidden by CLAUDE.md.

**Status:** Awaiting your call.

---

### Q1.2 — Decide on FPIC review path for Tier-4 paper

**Context:** Tier-4 paper mentions "FPIC obtained" without specifying which communities, dates, or documentation. Ethics boundary — cannot decide unilaterally.

**Options:**
- (A) Remove all FPIC claims, frame paper as "methodology applicable when FPIC is obtained"
- (B) Replace with specific community names + dates (you provide)
- (C) Add "FPIC review pending" footnote + cite INDI protocol as future work

**Recommendation:** **(C)** — most defensible at defense.

**Status:** Awaiting your call.

---

### Q1.3 — p0010 Discussion passage with unverified citations

**Context:** User-authored Discussion section (commit `c0e4d88`) cites 4 papers that may not exist. Cannot edit user-authored Discussion (per CLAUDE.md review pattern).

**Options:**
- (A) Flag in cover-letter to examiners, leave Discussion unchanged
- (B) Add a footnote saying "claims based on preliminary search, full validation in supplementary"
- (C) You rewrite Discussion yourself

**Recommendation:** **(A)** — flag-only per CLAUDE.md review pattern.

**Status:** Awaiting your call.

---

## Tier 2 — DECIDE BEFORE DEFENSE (can defer with TODO)

### Q2.1 — Manual DOI verification for 46 Round-7 placeholder entries

**Context:** Round-7 added 46 bib entries with `note = {Round-7 placeholder, DOI to be verified}`. CrossRef title-only search returned wrong results for some.

**Options:**
- (A) Verify all 46 before defense (~2 hours manual work)
- (B) Verify top 10 most-cited, leave rest as placeholder
- (C) Defer to post-defense, add to defense-check as "non-critical warning"

**Recommendation:** **(B)** — top 10 covers 80% of citation weight.

**Status:** Awaiting your call.

---

### Q2.2 — Round-6 left 83 "no good CrossRef match" entries

**Context:** Round-6 cross-validation found 83 entries with no clean CrossRef match. These are real works but the metadata may be wrong.

**Options:**
- (A) Manual search each (high effort)
- (B) Cross-check via Google Scholar + OpenAlex
- (C) Mark all as "low-confidence reference, see footnote" in bib

**Recommendation:** **(B)** — OpenAlex API is free and handles obscure works better than CrossRef.

**Status:** Awaiting your call.

---

### Q2.3 — `local main is 48 commits behind origin/main`

**Context:** Local main is behind origin/main. The branch is fast-forward compatible but main itself has diverged.

**Options:**
- (A) `git pull --rebase` main to sync (safe)
- (B) Leave as-is until merge
- (C) Reset local main to origin/main (loses local-only commits if any)

**Recommendation:** **(A)** — rebase is safe; no local-only commits.

**Status:** Awaiting your call.

---

## Tier 3 — DECIDE AFTER DEFENSE (low priority)

### Q3.1 — Beery 2018 "Synthetic-to-Real gap" — wrong CrossRef results

**Context:** CrossRef returned wrong papers for Beery 2018. Need manual verification.

**Recommendation:** Defer to post-defense (Q2.1 will cover it).

**Status:** No action needed now.

---

### Q3.2 — Per-paper bib slices — keep as supersets?

**Context:** Per-paper bib slices are master supersets (by design). Confirmed not a bug.

**Recommendation:** No action — keep current design.

**Status:** No action needed.

---

### Q3.3 — Round-7 cross-validate via OpenAlex?

**Context:** Same as Q2.2 — already covered.

**Status:** No separate action.

---

## Tier 4 — DECIDE POST-DEFENSE

### Q4.1 — Trademark banlist compliance reply to Hostinger

**Context:** Hostinger suspended subdomain 2026-Q1 over `mensajeconnect` phishing flag. Compliance reply needed.

**Recommendation:** Defer to post-defense.

**Status:** No action needed now.

---

## Auto-applied (no human input needed)

These were identified as "best option obvious" and **already implemented** in this session:

| # | Action | Why obvious | Status |
|---|---|---|---|
| A1 | Apply black formatting repo-wide | CI lint failing, fix is mechanical | ✅ Committed + pushed |
| A2 | Fix flake8 F401/F541/E501 | CI lint failing, fix is mechanical | ✅ Committed + pushed |
| A3 | Fix mypy implicit Optional | CI type check failing, fix is mechanical | ✅ Committed + pushed |
| A4 | Find working GitHub token | Token in `.env` was needed for API access | ✅ Found + used |
| A5 | Push branch to GitHub | User asked for GitHub access | ✅ Pushed |
| A6 | Provide raw download links | User asked for download access | ✅ Links delivered |

---

## Summary

- **Tier 1:** 3 questions (Q1.1, Q1.2, Q1.3) — cannot defer
- **Tier 2:** 3 questions (Q2.1, Q2.2, Q2.3) — defer with TODO
- **Tier 3:** 3 items — no action needed
- **Tier 4:** 1 item — defer to post-defense
- **Auto-applied:** 6 items — done in this session

**Total questions requiring your input: 6**

**Real questions that need your decision now: 3** (Q1.1, Q1.2, Q1.3)
