# Conventions — SatelliteCV-Paraguay

This document is the single source of truth for **how we report numbers,
cite claims, and disagree with prior drafts** in this repository. New
contributors should read it before opening a PR.

## 1. Measured vs. aspirational

Every numeric claim in `paper.md`, `paper.tex`, `abstract.md`, `README.md`,
or any public-facing string is one of:

1. **Measured** — the value was actually produced by an experiment run in
   this repo (see the matching `ACTUAL_RESULTS.md`) or by a published
   third-party study that is cited by name (`\citep{key}` / DOI).
2. **Aspirational** — a target for future work, a hypothesis, a benchmark
   from a different paper. **MUST NOT appear in an abstract headline.**

The default in this repo (after the 2026-08-10 honest-reporting pass) is:
**measured value in the abstract, aspiration in a Discussion paragraph
that names what must be true for the aspiration to be replaced by a
measurement.**

## 2. Citation pointers

Every `abstract.md` and `paper.tex` `\begin{abstract}` block MUST
reference the matching `ACTUAL_RESULTS.md` if measured values appear.
The convention is:

```markdown
**Measured pilot result (see `ACTUAL_RESULTS.md`):** F1 = 0.497, MAE = 3.20 t/ha.
```

For `paper.tex`, the equivalent is:

```latex
\textbf{Measured pilot result (see \texttt{ACTUAL\_RESULTS.md}):} F1 = 0.497, MAE = 3.20\,t/ha.
```

If the abstract quotes a value that is NOT measured (literature
benchmark, e.g., `R^2 = 0.82` for AlphaEarth on its own benchmark), the
abstract MUST state that the value is a literature benchmark and that
the thesis has not independently reproduced it.

## 3. The fabrication audit pattern

The repo carries a CI guard (`scripts/check_claims.py`) that scans for
high-headline claims (F1 > 0.7, R² > 0.7, mAP > 0.6, MAE < 5) outside the
sanctioned locations (`ACTUAL_RESULTS.md`, `README.md`, `WORKLOG_*.md`,
`docs/REAL_TODO.md`, `LICENSE`, `CITATION.cff`, `ROAST.md`,
`CONTRIBUTING.md`, `CONVENTIONS.md`). Run it before any PR:

```bash
python3 scripts/check_claims.py
```

Exit 0 = clean. Exit 1 = the PR introduces an unsanctioned claim.

To whitelist a file (use sparingly), add the file name to
`SANCTIONED_FILENAMES` in `scripts/check_claims.py` with a comment
explaining why.

## 4. Disagreement with earlier drafts

It is **fine and expected** to disagree with a prior version of a paper.
The convention for documenting disagreement:

```markdown
The F1 = 0.5592 figure (U-Net from-scratch on 15 synthetic Chaco tiles, 5 CPU epochs) is the current **measured** pilot value (over-prediction: precision 0.0992, recall 0.9873); see `papers/drafts/p0011_yvutu_deforestation/ACTUAL_RESULTS.md` and paper.tex §3. The earlier-draft F1 = 0.83 figure was an aspirational target and has been removed from all public-facing surfaces in the 2026-08-10 honest-reporting pass. The aspirational-vs-measured distinction is enforced by `scripts/check_claims.py` (run in CI).
```

This sentence belongs in the abstract or a clearly-labeled "Honest
Reporting Note" appended to the paper body, NOT in a git commit message
or PR description (which can become detached from the paper text).

## 6. Canonical numbers lifecycle (added 2026-09-08)

The `CANONICAL_NUMBERS` table in `tests/test_numerical_consistency.py`
is a **stale-list guard**, not a source of truth. It exists to catch
regressions where an aspirational number leaks back into the prose.

When a measured value replaces an aspirational one, the corresponding
stale-list entry MUST be removed in the **same commit** that updates
the prose. The convention:

1. **Identify the decision** — the value must be locked in either
   `docs/decisions/OPEN-QUESTIONS-FOR-HUMAN-2026-09-07.md` (or a newer
   decisions doc), in `STATUS.md` per-paper scorecard, or in
   `THESIS_ABSTRACT.md`. Without a documented decision, the stale-list
   entry stays.

2. **Single commit, two changes** — the prose change AND the
   `CANONICAL_NUMBERS` entry removal belong in one commit. Splitting
   them creates a window where the prose is canonical but the guard
   still forbids it (Round-8 regression class).

3. **Comment the lifecycle** — when removing a stale-list entry,
   replace the comment with a one-liner citing the decision
   (e.g., "Q6 recommendation A: 3.0× is canonical, see
   THESIS_ABSTRACT.md L62-63"). Future maintainers reading
   `CANONICAL_NUMBERS` must be able to understand why a number
   was demoted from stale-list.

4. **Watch for stale-list vs measured-value drift** — the regression
   pattern caught in Round-8 (2026-09-08): `CANONICAL_NUMBERS` still
   had `3.0× indigenous ratio` flagged as stale after `OPEN-QUESTIONS
   Q6` made 3.0× the canonical headline value. The test caught it
   (`test_no_stale_canonical_numbers`); the fix removed 3 stale-list
   entries + added a comment pointer to the decision. This is the
   pattern to watch for.

## 7. References

The unified `references.bib` at the repo root is the single BibTeX
source for both the thesis and the six paper drafts. Conflicts are
resolved in `scripts/merge_bib.py` via the `PREFER_PAPERS` set. New
conflicts fail the merge with `SystemExit` so they cannot be silently
ignored.

## 6. Versioning

This repo releases v0.1 via Zenodo on the first PR that lands the
honest-reporting pass + a working P0011 GPU re-run. Until then, treat
all metrics in the repo as **pilot** numbers, **not** production
benchmarks.

## 7. When in doubt

If you are unsure whether a number is a measurement, an aspiration, or a
literature citation, ask in the PR review. **Do not** remove the number
without checking `ACTUAL_RESULTS.md` first.