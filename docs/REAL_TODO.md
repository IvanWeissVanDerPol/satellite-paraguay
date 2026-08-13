# SatelliteCV-Paraguay — Real TODO (2026-08-10 trim)

**Previous version:** `docs/COMPREHENSIVE_TODO.md` (587 lines, ~345 items,
generated 2026-07-31). Largely out of date per `GAP_AUDIT_2026-08-04.md`.
This file replaces it. Keep this ≤30 items.

**Status legend:** `[ ]` todo · `[x]` done · `[~]` in progress · `[!]` blocked

---

## Tier 1 — Must finish before thesis defense (8 items)

- [x] All 6 papers have `paper.tex`, `cover_letter.md`, `ACTUAL_RESULTS.md`,
      `submission_checklist.md`. Abstract + paper.md updated to cite measured
      values (not literature-benchmarks) on 2026-08-10.
- [ ] **P0011 Yvutu — train Prithvi on real Paraguay tiles on a GPU** (≥150
      tiles, ≥30 epochs, held-out real test split). Currently blocked on
      GEE auth + Vast.ai credits.
- [ ] **P0011 Yvutu — re-run on real Prithvi backbone**, report measured F1,
      delete the F1>0.85 / 50× claim if not supported.
- [ ] **P0012 Yvy — FPIC engagement with the 10 territories analyzed** before
      any submission to World Development. CARE Principles compliant.
- [ ] **P0010 Yvyra — re-verify Verra under-claim finding** on a 2025 refresh
      of Hansen GFC (v1.12 if available) before Nature Climate Change
      submission.
- [ ] **P0025 Yrupe — train on real INBIO yield labels** (currently synthetic).
      Re-test H3 cross-domain transfer.
- [ ] **P0026 Kai — acquire a Paraguay-specific real labeled wildlife set**
      beyond the 5,000-image evaluation set. Synthetic-to-real gap = 0.32 mAP.
- [ ] **P0035 Tatakua — close the rural-station gap** (Filadelfia/Chaco at
      18.6 µg/m³ RMSE). Add ground stations or change loss function.

## Tier 2 — Required for any single submission (8 items)

- [x] All 6 abstracts cite `ACTUAL_RESULTS.md` instead of literature benchmarks.
- [x] LICENSE (CC-BY-NC-4.0) added at repo root.
- [x] CITATION.cff added for GitHub "Cite this repository" button.
- [x] Unified `references.bib` (180 entries, 5 conflicts flagged for review).
- [ ] P0011 cover letter + submission checklist re-checked against RSE
      formatting requirements (page limits, ORCID, conflict-of-interest form).
- [ ] P0010 cover letter + checklist for Nature Climate Change.
- [ ] P0012 cover letter + checklist for World Development (CARE statement).
- [ ] P0025 / P0026 / P0035 cover letters + checklists finalized.

## Tier 3 — Repo health (8 items)

- [x] Trimmed COMPREHENSIVE_TODO from 345 → 30 items (this file).
- [ ] README "Headline findings" table — replace F1=0.85 row with measured
      pilot numbers + citation to ACTUAL_RESULTS.md.
- [ ] Replace `docs/COMPREHENSIVE_TODO.md` with a stub pointing to this file.
- [ ] Add a CONTRIBUTING.md (CARE-compliant, INDI contact line, no-data
      redistribution clause).
- [ ] CI: pin Python version, add pre-commit hook that fails on unverified
      claims (e.g., grep for "F1 > 0.8" outside ACTUAL_RESULTS.md).
- [ ] Reduce `coverage.xml` size — current 350 KB file should be in
      `.gitignore` or generated only in CI artifacts.
- [ ] Verify `models/cards/` are not stale (model cards should reference
      measured, not expected, performance).
- [ ] Add Zenodo integration per `OPEN_SCIENCE.md` — release v0.1 with the
      six ACTUAL_RESULTS.md snapshots.

## Tier 4 — Decline (low leverage) (6 items)

- [!] Test coverage 6.71% → 30%+ — blocked; would need ~30 new unit tests on
      research scripts that are not production code. Decision: keep current
      coverage and document the rationale.
- [ ] Reduce duplication in 5 lowercase notebook stubs — already merged to
      canonical set per GAP_AUDIT (2026-08-04).
- [ ] Glossary trilingual (ES/EN/GY) — needs Guaraní translator.
- [ ] Figure captions auto-linter for thesis PDF.
- [ ] Helm chart — empty, no deployment target uses it. Delete.
- [ ] Sunstein / misc / IP-REMINDER files — already absent from working
      tree (audit 2026-08-10 confirmed).

---

## See also

- `WORKLOG_2026-08-10.md` — what changed today and why.
- `GAP_AUDIT_2026-08-04.md` — original audit that motivated the trim.
- `ROAST.md` — kept as honest counterweight; read first before submitting.