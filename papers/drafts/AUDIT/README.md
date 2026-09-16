# Citation & Integrity Audits

> **This folder holds HISTORICAL audit artifacts.** The Round-N audit
> workflow moved to `outputs/ROUND_N_VERIFICATION_<date>.md` starting
> with Round-8 (2026-09-08). The Round-5 and Round-6 docs here are
> preserved as defense-committee audit-trail evidence of the work
> done; do not add new audits to this folder.

## Current state-of-audits

The most recent and most-relevant audits live in `outputs/`:

- `outputs/DEFENSE_PREP_15_HAT_AUDIT_2026-09-09.md` — 15-hat critical
  defense-prep pass (most recent comprehensive review)
- `outputs/HONEST_GAP_LIST_2026-09-10.md` — forward-looking gap list
  (the "what's missing" doc)
- `outputs/ROUND_10_VERIFICATION_2026-09-08.md` — Round-10 (data-fetcher fixes)
- `outputs/ROUND_9_VERIFICATION_2026-09-08.md` — Round-9 (meta-fixes)
- `outputs/ROUND_8_VERIFICATION_2026-09-08.md` — Round-8 (bib DOI verification)

## Historical files in this folder (kept for audit trail)

- `AUDIT-1-NUMERICAL-CONSISTENCY-2026-09-07.md` — Round-7 numerical consistency
- `AUDIT-2-CITATION-COMPLETENESS-2026-09-07.md` — Round-7 citation completeness
- `AUDIT-3-ASPIRATIONAL-CLAIMS-2026-09-07.md` — Round-7 aspirational-claims audit
- `AUDIT-4-LATEX-COMPILE-2026-09-07.md` — Round-7 LaTeX compile check
- `AUDIT-5-STRUCTURAL-ALIGNMENT-2026-09-07.md` — Round-7 structural alignment
- `ROUND_5_S2_AUDIT.md` + `ROUND_5_S2_AUDIT.json` — Round-5 Semantic Scholar
  initial validation (107 mismatches + 60 errors + 16 valid; **superseded** by
  Round-6 CrossRef re-verification)
- `ROUND_6_AUDIT.md` — Round-6 CrossRef re-verification (76 S2-flags were
  false positives; 7 real fixes applied)
- `TIER-4-REVIEW-2026-09-07.md`, `TIER-5-DEEP-REVIEW-2026-09-07.md`,
  `TIER-6-DEEP-REVIEW-2026-09-07.md` — Round-7 tiered reviews

## Why these stay in git

Per the orientation skill Pitfall #36 (anti-stamp rule) and the broader
project principle: the defense committee may ask "what audits did you
run, and what did they find?" — the audit trail is evidence of the
work, not noise. The fact that Round-5's initial S2 sweep was wrong
and Round-6 had to correct it IS the work. Removing these files
would remove the evidence of due diligence.

## How to re-verify

```bash
# Re-verify the full bib (slow, ~5 min)
python3 scripts/verify_bib_dois.py --batch 0 200

# Quick check: just the 7 Round-6 fixes
python3 scripts/verify_bib_dois.py --verify-only sze2022 fearnside2017 ...

# Fast-test subset (~5s) + every-commit guards
bash scripts/run_tests_fast.sh

# Full test suite (~100s, all 1081 tests)
bash scripts/run_tests.sh

# Structural defense gate (13/13 checks)
.venv/bin/python scripts/defense_check.py
```

## Conventions for new audits

Add new audits to `outputs/` as `ROUND_N_VERIFICATION_<date>.md` (or
`SESSION_<date>_summary.md` for end-of-session reports). Do not add
to this folder unless it is part of the Round-5/6/7 historical
sequence.
