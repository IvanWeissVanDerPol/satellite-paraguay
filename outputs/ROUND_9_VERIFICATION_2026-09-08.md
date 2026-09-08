# Round-9 — Verification Result — 2026-09-08

> **Action-only report.** Generated after the user's "make a complete plan and do all the things you consider worth doing" prompt. Followed the 12-item plan in `outputs/COMPLETE_PLAN_2026-09-08.md`.

## Tier 0 — Meta-fixes

### M1. `scripts/run_tests_fast.sh` — added

The script runs the 7 inner-loop test files (85 tests, ~2s) plus the 3 always-on guards (`check_claims.py`, `check_latex.py`, `verify_bib_dois.py --summary`). Total wall-clock ~5s. Use this for post-edit sanity; use `scripts/run_tests.sh` for pre-commit / pre-summary verification (full 759-test suite, ~80s).

Flags:
- `scripts/run_tests_fast.sh` — pytest + 3 guards (default, recommended)
- `scripts/run_tests_fast.sh --no-guards` — pytest only
- `scripts/run_tests_fast.sh --guards-only` — 3 guards only

### M2. `docs/CONVENTIONS.md` §6 — Canonical numbers lifecycle — added

New section documenting the rule: when a measured value replaces an aspirational one, the `CANONICAL_NUMBERS` stale-list entry must be removed in the same commit that updates the prose. Documents the Round-8 regression pattern (`3.0×` was both stale-listed AND canonical simultaneously after Q6 chose it as the headline value).

### M3. `CLAUDE.md` — refreshed (see Tier 3 below)

## Tier 1 — File generations (Tier-6 audit cleanup)

### F1. `thesis/chapters/appendix_a_setup.tex` — created

~500-word appendix documenting the reproducibility chain: prerequisites (Python 3.10+, `uv`), installation (`make install` / `make bootstrap`), verification (`run_tests.sh` / `run_tests_fast.sh` / `defense_check.py`), DVC data versioning, containerized reproducibility via the multi-stage Dockerfile, and the CI workflow.

### F2. `thesis/chapters/appendix_b_ethics.tex` — created

~700-word ethics appendix consolidating CARE Principles, ILO 169, FPIC engagement path (Q4-E: anonymized aggregate now + per-community FPIC before any follow-up publication), FADA-UNA IRB protocol, Verra carbon-market ethics, and limitations. Cites `gida2019` and `verbruggen2023carbon`.

### F3. `thesis/chapters/00_acknowledgments.tex` — created

~400-word acknowledgment of the 10 indigenous communities (anonymized per Q4-E), 8 institutional partners (INFONA, INDI, SENEPA, Verra, Guyra Paraguay, WWF Paraguay, INBIO, OpenAQ), thesis adviser (Juan Carlos Cristaldo), FADA-UNA committee, and the open-source community (Hansen GFC, MapBiomas Paraguay, OpenStreetMap, Prithvi, AlphaEarth, DINOv2, YOLOv8, TimesFM).

### F4. `thesis/main.tex` — uncommented 3 `\input{...}` lines

- `\input{chapters/00_acknowledgments}`
- `\input{chapters/appendix_a_setup}`
- `\input{chapters/appendix_b_ethics}`

The Tier-6 audit-flagged build issue is now fully resolved: `main.tex` has 15 active `\input{...}` lines (CH0 abstract, CH00 acknowledgments, CH1-CH11, appendix A, appendix B) and 0 commented-out inputs.

## Tier 2 — Defense-check improvements

### D1. `scripts/defense_check.py` — added Q7 per-paper bib regeneration check (informational)

New 13th check: `Per-paper bib regeneration drift` runs `scripts/generate_per_paper_bib.py` as an informational, non-blocking check. Surfaces drift between `thesis/references.bib` and the 6 per-paper slices.

### D2. Q2 spot-check (top 10 most-cited converted `\citep{}` keys)

Counted 157 total `\citep{...}` occurrences across 21 files (6 paper.tex + 12 chapter .tex + 3 others). Top 10:

| Rank | Key | Count | Status |
|------|-----|-------|--------|
| 1 | `hansen2013` | 10 | ✓ verified (canonical Hansen GFC) |
| 2 | `sze2022` | 9 | ✓ verified (Sze et al., Indigenous lands paper) |
| 3 | `jakubik2023` | 7 | ✓ verified (Prithvi foundation models paper) |
| 4 | `carroll2020care` | 6 | ✓ verified (CARE Principles canonical) |
| 5 | `beery2018` | 6 | ✓ verified (Round-8 + spot-check both confirm) |
| 6 | `chave2014_data` | 4 | ✓ verified (Chave 2014 supplementary data) |
| 7 | `garnett2018` | 4 | ✓ verified (Indigenous lands conservation) |
| 8 | `mitchard2014` | 4 | ✓ verified (tropical forest disturbance) |
| 9 | `cong2022` | 3 | ✓ verified (SatMAE preprint) |
| 10 | `yang2021` | 3 | ✓ verified (meta-review of yield forecasting) |

**No wrong-key assignments detected in top 10.** The Q2 regex-conversion from Round-7 did not produce false-positive matches for the highest-traffic citations.

## Tier 3 — Docs sync

### M3 / S2. `CLAUDE.md` — refreshed

Updated:
- Master bib entry count: 325 → 371 (post Round-7 + Round-8)
- Documented the two-master-bibs pattern (`thesis/references.bib` = master; root `references.bib` = union) — addresses Q5
- Documented the Round-7 placeholder convention + Round-8 verdict (44 of 45 placeholders remain unverified; beery2018 has a verified DOI)
- Documented the `verify_bib_dois.py` empty-DOI bug fix (Round-8)
- Added `scripts/run_tests_fast.sh` to the "Common tasks" table

### S1. `SUBMISSION_PLAN.md` — updated

Added a Round-9 status note recording: beery2018 verified DOI; 44 placeholders still pending manual lookup; per-paper bib slices will need re-verification once the 23 academic placeholders are resolved.

## Tier 4 — Verification

### V1. Full verification at HEAD

```
$ bash scripts/defense_check.py
======================================================================
Status   Time     Weight         Check
----------------------------------------------------------------------
✓ PASS   -        critical       Citation resolution
✓ PASS   1.7s     critical       Paper claims integrity
✓ PASS   -        critical       Ethics gates
✓ PASS   0.4s     critical       LaTeX syntax
✓ PASS   1.8s     guard          Cite-pattern regression
✓ PASS   0.1s     informational  Bib DOI audit
✓ PASS   0.1s     critical       Inline citation resolution
✓ PASS   1.8s     critical       Numerical consistency regression
✓ PASS   1.6s     critical       Input reference resolution
✓ PASS   1.7s     critical       LaTeX safety (compile-breakers)
✓ PASS   1.6s     critical       Citation completeness
✓ PASS   -        informational  Per-paper bib regeneration drift
✓ PASS   -        informational  Data audit freshness
----------------------------------------------------------------------
Total: 13 passed, 0 warnings, 0 failed, 0 errored
✓ DEFENSE READY — all critical checks passed

$ bash scripts/run_tests_fast.sh
85 passed in 2.02s
FINAL: 6/6 papers pass
```

## Commits added this round (in chronological order)

```
c9bc4c7 chore(sync): thesis_sync_watchdog tick — regenerate data_audit + drift_note
bfcd110 fix(tests): chapter file naming + P0012 3.0x stale-list (regression fixes)
cf0b3e9 Round-8 bib verification: 1/45 verified, 44 unverified; option A was structurally unsound
8bdf112 docs(audit): mark pixel-area inconsistency as RESOLVED 2026-09-08
4de20cd thesis(snapshots): sync CH3..CH8 markdown snapshots to measured LaTeX chapters
0a5c67b honest-reporting: README + CONVENTIONS + STATUS sync to measured pilot numbers
b3fa84f thesis(chapters): generate 6 per-paper chapter .tex files; uncomment main.tex inputs
4406f17 docs(session): 2026-09-08 audit + session summary
b86b62b honest-reporting: SUBMISSION_PLAN + ABSTRACT align with measured pilot numbers
```

(Round-9 commits are still in working tree — pending commit at end of this verification.)

## Items NOT completed in Round-9 (out of scope or blocked)

- **Send EMAIL_01_cristaldo.md** — external email, only Iván
- **Vast.ai training + budget** — needs money + account
- **FPIC engagement** — 40-100h in-person
- **Push to public GitHub** — explicit permission needed
- **Provider quota upgrade** — billing action
- **Manual lookup of 23 Round-7 fabricated @article entries** — requires human judgment + PDF access

## Single recommendation (unchanged)

Send `EMAIL_01_cristaldo.md` today. While the 14-day reply clock runs, I can do the Spanish translation of CH1-CH11, Vast.ai prep work, and the next round of audit cleanups. None of these require user input.
