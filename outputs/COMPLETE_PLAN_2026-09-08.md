# Complete Plan — 2026-09-08 session

> **Action plan generated after the user's "make a complete plan and do all the things you consider worth doing" prompt.** All items below are agent-actionable; user-blocked items are listed separately at the bottom.

## Tier 0 — Meta-fixes (so all subsequent verifications catch everything)

### M1. Add `scripts/run_tests_fast.sh` for the inner-loop subset
**Rationale:** `scripts/run_tests.sh` runs the **full** suite (759 tests, ~82s). My inner-loop was a 5-file subset (64 tests, ~2s). The 2 failures I just fixed would have been caught earlier if I'd been using a documented fast option. 5-minute fix.
- Add `scripts/run_tests_fast.sh` that runs the 5 inner-loop files (`test_input_references.py`, `test_numerical_consistency.py`, `test_citation_completeness.py`, `test_latex_check.py`, `test_latex_safety.py`, `test_bibliography.py`, `test_citation_patterns.py`)
- Plus the 3 "every-commit" guards: `check_claims.py`, `check_latex.py`, `scripts/verify_bib_dois.py --summary`

### M2. Add canonical-numbers lifecycle rule to `docs/CONVENTIONS.md`
**Rationale:** The second failure was a stale-list vs measured-value drift. Future measured-value updates should remove the old stale-list entry in the same commit. 5-minute fix.
- Add a §6 "Canonical numbers lifecycle" section: when a measured value replaces an aspirational one, the `CANONICAL_NUMBERS` entry must be removed in the same commit + the OPEN-QUESTIONS doc must be updated.

### M3. Update CLAUDE.md to reflect current state
**Rationale:** CLAUDE.md still says `325 entries` (it's `371`), doesn't mention the Round-7 placeholder convention, the 2-master-bibs pattern, the new `verify_bib_dois.py` CrossRef bug fix, or the new fast-test runner. 10-minute fix.
- Bump master bib count 325 → 371
- Document the two-master-bibs pattern (`thesis/references.bib` = master; root `references.bib` = union)
- Document the Round-7 placeholder convention + Round-8 verdict
- Document the `verify_bib_dois.py` empty-DOI bug fix (Round-8)
- Add `scripts/run_tests_fast.sh` to the "Common tasks" table
- Add the 4 EXT-blocked human actions to a new "External actions needed" section

## Tier 1 — File generations (Tier-6 audit cleanup)

### F1. Generate `thesis/chapters/appendix_a_setup.tex`
**Rationale:** `main.tex` has `\input{chapters/appendix_a_setup}` + `\input{chapters/appendix_b_ethics}` commented out (Tier-6 audit). The appendix A is about reproducibility setup (conda/uv/DVC commands). 15-minute fix.
- Generate ~500-word appendix from `pyproject.toml` + `Dockerfile` + `dvc.yaml` + `Makefile`
- Include the `make` targets, the env setup, the test commands

### F2. Generate `thesis/chapters/appendix_b_ethics.tex`
**Rationale:** Ethics framework is currently scattered across `etica/FPIC_template_es.md` + `docs/partnerships/IRB_PROTOCOL_PARAGUAY_UNA-2026-09-07.md` + `docs/partnerships/FPIC-DECISION-STATUS-2026-09-07.md`. 20-minute fix.
- Generate ~700-word ethics appendix consolidating CARE Principles + ILO 169 + IRB protocol
- Include the FPIC decision status (Q4-E: anonymized aggregate + future FPIC)
- Cite the relevant one-pagers

### F3. Generate `thesis/chapters/00_acknowledgments.tex`
**Rationale:** `main.tex` has `\input{chapters/00_acknowledgments}` commented out. The partnership one-pagers at `docs/partnerships/ONE-PAGERS-2026-09-07.md` have the partner names + roles. 10-minute fix.
- Generate ~400-word acknowledgment from the 10 partnership one-pagers
- Acknowledge FPIC-affected communities (anonymized per Q4-E)

### F4. Uncomment the 3 new `\input{}` lines in `main.tex`
- `\input{chapters/00_acknowledgments}`
- `\input{chapters/appendix_a_setup}`
- `\input{chapters/appendix_b_ethics}`

## Tier 2 — Defense-check improvements

### D1. Wire `generate_per_paper_bib.py` into `defense_check.py` (Q7)
**Rationale:** The OPEN-QUESTIONS doc recommended adding it as an informational check (non-blocking). 10-minute fix.
- Add a step that runs `python3 scripts/generate_per_paper_bib.py` and reports whether per-paper bibs are in sync with the master
- Non-blocking — informational only

### D2. Run the Q2 spot-check (top 10 most-cited converted `\citep{}` keys)
**Rationale:** Round-7 mechanically converted inline citations. 5-minute sanity check.
- Count `\citep{...}` occurrences in `papers/drafts/*/paper.tex` + `thesis/chapters/*.tex`
- Pick the top 10 most-cited keys
- For each, verify the bib entry exists + the title roughly matches the citation context (5-10 lines around each cite)

## Tier 3 — Docs sync

### S1. Update `SUBMISSION_PLAN.md` with Round-8 results
- Mention the beery2018 verified DOI + the 44 still-unverified placeholders
- Note that the per-paper bib slices will need re-verification once the 23 academic placeholders are resolved

### S2. Update `MASTER_PLAN.md` with current session progress
- Mark the 12 audit-driven tasks complete (this session)
- Add the Round-8 + Round-9 (this session) + the meta-fix items to the history

## Tier 4 — Verification

### V1. Full suite at HEAD after all changes
- `bash scripts/run_tests.sh` → must show 759+ passed, 0 failed
- `bash scripts/run_tests_fast.sh` → new file, must work
- `.venv/bin/python scripts/defense_check.py` → must show 0 FAIL

## Items NOT in this plan (user-blocked or out of scope)

### U-blocked
1. **Send EMAIL_01_cristaldo.md** — external email, only Iván
2. **Vast.ai training + ~$35 budget** — needs money + account
3. **FPIC engagement with 10 indigenous communities** — 40-100h in-person
4. **Push to public GitHub** — explicit permission needed
5. **Provider quota upgrade** — billing action
6. **Manual lookup of 23 Round-7 fabricated @article entries** — requires human judgment + PDF access

### U-deferred
- **Spanish translation CH1-CH11** — 4-6h, can run while email-reply clock ticks
- **Per-paper Discussion polish (P0010 etc.)** — Q3 already addressed via honest-reporting notes
- **Vast.ai training runs** — once budget approved

## Estimated effort

| Tier | Items | Effort |
|---|---|---|
| 0 (meta-fixes) | 3 | ~25 min |
| 1 (file gen) | 4 | ~50 min |
| 2 (defense-check) | 2 | ~15 min |
| 3 (docs sync) | 2 | ~10 min |
| 4 (verification) | 1 | ~5 min |
| **Total** | **12** | **~105 min (1.75 h)** |

## Execution order

1. M1 (fast test runner) → test it works
2. M2 (CONVENTIONS.md lifecycle)
3. F1 (appendix_a_setup.tex) + F2 (appendix_b_ethics.tex) + F3 (00_acknowledgments.tex)
4. F4 (uncomment the 3 inputs in main.tex)
5. D1 (wire generate_per_paper_bib.py into defense_check.py)
6. D2 (Q2 spot-check)
7. M3 (CLAUDE.md refresh)
8. S1 (SUBMISSION_PLAN update)
9. S2 (MASTER_PLAN update)
10. V1 (final HEAD verification)

## Cancellation triggers (if any check fails)

- If `scripts/defense_check.py` exits non-zero at any step → STOP, fix root cause, re-run from there
- If any of the 3 new `.tex` files break `check_latex.py` → STOP, fix before generating next
- If the new test file picks up a real regression → STOP and triage
