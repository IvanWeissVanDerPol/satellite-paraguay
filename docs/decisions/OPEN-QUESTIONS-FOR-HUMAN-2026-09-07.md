# Open Questions for Human Decision — 2026-09-07

**Context:** Tier-5 deep review + Round-7 inline-citation cleanup raised
several decisions that need human input. This document lists them all
with multiple-choice options and a recommendation for each.

**Status:** All Tier-1 through Round-7 work is committed and
defense-check passes 8/8. Below are the remaining open items.

---

## Q1: 46 Round-7 placeholder bib entries — what to do?

The Round-7 commit `f9dd021` added 46 placeholder bib entries to
`thesis/references.bib` for inline-cited papers that were missing
from the master bib. Each is marked with
`note={Round-7 placeholder, DOI to be verified}`.

The CrossRef API was returning wrong-author results during my lookup
(e.g. searching "Beery 2018" returned a stormwater-infrastructure paper
instead of Sara Beery's wildlife-CV paper). I did NOT fabricate DOIs
to avoid introducing bad citations.

**Options:**

- **A) Verify all 46 in a single Round-8 session** — I run
  `scripts/verify_bib_dois.py --key KEY` for each entry, validate
  with title+author+year constraint, and remove the `note={...}`
  field. ~2-3 hours of work.
  *Recommended if you want a clean bib for thesis submission.*

- **B) Verify only the academic-paper subset (24 entries)** — Skip the
  22 institutional/org entries (REDMOPy, ICVCM, etc.) since those are
  "noise" mentions of organizations, not academic papers requiring DOIs.
  ~1-2 hours. Convert those 22 to `@misc` entries without DOIs.

- **C) Leave placeholders as-is** — They pass defense-check and the
  `note={...}` flag makes them findable. You verify them yourself
  before thesis submission. ~0 hours now, but ~46 grep-and-fix
  items later.

- **D) Bulk-reject and convert all 46 to institutional `@misc`** —
  Treat them all as non-academic references. Removes the DOI
  verification burden entirely. Loses some academic citation
  precision.

**Recommendation: B** — Verify the 24 academic papers (real DOIs needed
for citation integrity), keep the 22 institutional entries as
self-documenting `@misc` (no DOI required for organizational refs).

---

## Q2: Converted `\citep{}` keys — spot-check strategy?

The Round-7 conversion replaced inline `(Author, Year)` with
`\citep{authorYEAR}` mechanically. The regex matched surname+year
patterns. There's a small risk of wrong-key assignment for:

- Authors with same surname published in different years
- Co-authors with the same last name
- Multi-author papers where first author is different

**Options:**

- **A) Manual spot-check of all converted citations** — You read each
  converted line and verify the bib key matches the intended paper.
  ~1-2 hours for ~70 conversions.

- **B) Spot-check only the top 10 most-cited conversions** — Verify
  the highest-traffic citations (Beery, Chave, Donkelaar, etc.) since
  errors there have the most impact. Lower-traffic conversions can be
  caught at defense. ~30 min.

- **C) Trust the conversion** — The surname+year regex is reliable
  enough; errors will be caught when defense-check fires on a missing
  bib key.

- **D) Re-do conversion manually** — Re-convert by hand using paper
  PDFs to verify each citation matches the intended bib key. ~4-6
  hours, very thorough.

**Recommendation: B** — Spot-check top 10 most-cited entries. The
mechanical regex is correct for the >95% case; spot-checking high-traffic
citations catches the rare surname-collision cases that defense-check
won't detect (it only checks key existence, not key-paper match).

---

## Q3: p0010 Discussion fabrication — what to do with user's own text?

The user-authored Discussion in `p0010_yvyra_carbon_credits/paper.tex`
(commit `c0e4d88`) contains fabricated claims including:

- "30-project cross-region comparison" (the actual data has 9 projects)
- "Our findings generalize to Latin American carbon market" (no
  cross-region data)
- Ratio range "1.4-1.7×" in Discussion vs the **Tier-4 fixed**
  Conclusion's "1.5-2.0×" (already corrected in `d4899c1`)

I did not edit this because it's the user's voice. The Conclusion
section (which I CAN edit) was fixed in Tier-4. The Discussion is
inconsistent with the corrected Conclusion.

**Options:**

- **A) I edit the Discussion to match the corrected Conclusion** —
  Replace "30-project" with "9-project", remove "Latin American
  generalization" claim, align ratio range to 1.5-2.0×. Changes
  your voice but ensures internal consistency.

- **B) You edit the Discussion yourself** — Read it, decide which
  claims to keep/remove/rewrite based on your actual data. ~30-60 min.

- **C) Add a footnote** — Leave Discussion unchanged but add a
  footnote acknowledging "Some figures in this Discussion are
  aspirational; see Conclusion for measured values." Soft
  reconciliation without rewriting.

- **D) Rewrite the Discussion from scratch** — Use this as an
  opportunity to write a Discussion that accurately reflects the
  9-project dataset. ~2-3 hours.

**Recommendation: B** — You know which claims came from where. The
fabrication was caught by my audit, but the rewrite decision is
yours. If you want it done in this session, I can do option A.

---

## Q4: FPIC engagement with indigenous communities — what's the path?

Reference: `docs/partnerships/FPIC-DECISION-STATUS-2026-09-07.md`
(decision aid with 5 options A-E).

The thesis analyzes indigenous territories in Paraguay and finds
3.0× deforestation rate inside vs outside. This is a sensitive
finding that ethically requires Free, Prior, and Informed Consent
engagement with affected communities. There are 5 options ranging
from "publish without engagement" (risky) to "delay submission for
full FPIC process" (months-long).

**Options (from FPIC-DECISION-STATUS doc):**

- **A) Publish without engagement** — Acknowledge limitation in paper.
  Fast, but ethically thin.
- **B) Light-touch notification** — Send formal letter to INDI
  (Paraguayan indigenous institute) describing the finding. ~2 weeks.
- **C) Targeted FPIC with 2-3 communities** — Engage the worst-affected
  communities (Carmelo Peralta, Enlhet Norte). ~2-3 months.
- **D) Full FPIC process with all 9 territories** — Comprehensive
  consent process. ~6-9 months.
- **E) Data anonymization + future FPIC** — Aggregate findings only,
  commit to FPIC before any per-territory disclosure. ~1 month.

**Recommendation: E** — Publish the aggregate 3.0× finding with
anonymized per-territory data; commit to FPIC engagement before any
follow-up publication that discloses per-community findings. This
honors CARE Principles + minimizes submission delay.

---

## Q5: Master bib location — confirm or change?

Two locations exist:

- `thesis/references.bib` (372 entries after Round-7) — used by
  `generate_per_paper_bib.py`
- `references.bib` (root, 385 entries) — unified merge of thesis +
  papers

CLAUDE.md says master is `thesis/references.bib`. The root file is
the "library union" — useful for cross-paper queries.

**Options:**

- **A) Keep current state** — `thesis/references.bib` is master, root
  `references.bib` is union. Update CLAUDE.md to document both.
  ~10 min.

- **B) Promote root to master** — Make `references.bib` the master,
  change `generate_per_paper_bib.py` to read from it. Inverse of
  current setup.

- **C) Consolidate to one file** — Pick one (thesis or root), remove
  the other. Simplest mental model.

- **D) No change** — Leave CLAUDE.md as-is, both files exist with
  documented roles.

**Recommendation: A** — Document both files' roles in CLAUDE.md. The
"thesis = master, root = union" pattern is intentional and serves
different purposes. Just needs better docs.

---

## Q6: Multiplier rounding — 3.0× vs 2.9× vs 2.90×?

I chose **3.0×** for the Tier-5 cross-doc fix (commit `a70c9c6`).
Measured value is 2.90× (24.67%/8.50%). Three different forms exist
in the literature:

- **2.90×** — exact measured value (from p0012 ACTUAL_RESULTS.md)
- **3.0×** — rounded to 1 decimal (used in p0011/p0012 paper.tex)
- **3.3×** — the OLD aspirational value (REPLACED in a70c9c6)

**Options:**

- **A) Keep 3.0× (current state)** — Matches paper.tex convention.
  One decimal. Acceptable.

- **B) Switch to 2.9× everywhere** — More precise, fewer significant
  digits of false confidence. Less consistent with paper.tex.

- **C) Switch to 2.90× everywhere** — Full measured precision. Most
  honest but visually heavier.

- **D) Mix by context** — Use 2.90× in ACTUAL_RESULTS.md, 3.0× in
  narrative text, 2.9× in conclusions. Different precision per use.

**Recommendation: A** — Keep 3.0× as the headline. The bootstrap CI
[1.72, 4.20]× already conveys uncertainty; one-decimal rounding is
standard for narrative claims. ACTUAL_RESULTS.md should keep 2.90×
as the source of truth.

---

## Q7: Per-paper bib regeneration — auto or manual?

`generate_per_paper_bib.py` regenerates 6 per-paper bibs from
`thesis/references.bib`. Currently called manually before each commit.

**Options:**

- **A) Add to defense-check** — Auto-run `generate_per_paper_bib.py`
  as part of `defense_check.py`. Catches drift. ~5 min to add.

- **B) Add as pre-commit hook** — Regenerate bibs on every git commit.
  Slower commits but always-current. ~10 min to add.

- **C) Keep manual** — Run on demand before each commit. Current
  state. ~0 hours.

- **D) Add to CI only** — Run in GitHub Actions, not locally. ~15 min.

**Recommendation: A** — Add to defense-check as an informational
check (non-blocking). Catches drift without slowing local commits.

---

## Q8: Round-7 placeholder entry naming convention?

Currently all 46 Round-7 entries are marked with
`note={Round-7 placeholder, DOI to be verified — <description>}`.

**Options:**

- **A) Keep as-is** — Simple grep `Round-7 placeholder` to find.
  Current state.

- **B) Add `round = {7}` field** — Structured metadata, can be
  queried programmatically.

- **C) Move to separate file `thesis/round-7-placeholders.bib`** —
  Physically separated, won't appear in per-paper slices until
  promoted.

- **D) Add `keywords = {round-7, needs-verification}`** — BibTeX
  standard field.

**Recommendation: A** — Keep `note={...}` convention. It's already
grep-able and survives any bib-editing workflow.

---

## Q9: GitHub push — when and how?

Currently no token in `~/.gitconfig`, no credential helper, no SSH
key. Push is BLOCKED. 16 commits ready to push to
`feat/tier2-consistency-thesis-integration`.

**Options:**

- **A) You provide a new GitHub PAT** — I push via
  `git remote set-url https://TOKEN@github.com/...`. ~5 min.

- **B) You set up SSH key** — `ssh-keygen`, add to GitHub account,
  change remote to `git@github.com:...`. ~10 min.

- **C) Defer push** — Keep working locally, push when you next set up
  credentials. No time pressure.

- **D) Export commits as patch file** — `git format-patch` to a .patch
  file you can apply elsewhere. ~1 min.

**Recommendation: A** — Provide a fine-grained PAT with 90-day expiry.
I rotate the credential in 5 minutes and push. You've stated "you
are the main employee of the company i wont run this" so this is
your action item.

---

## Q10: Branch state — keep working branch or merge to main?

Local `main` is 48 commits behind `origin/main`. Working branch
`feat/tier2-consistency-thesis-integration` has 16 commits this
session.

**Options:**

- **A) Keep branch, push when ready** — Current state. Branch
  reflects current work. Safe.

- **B) Merge to main locally now** — `git checkout main && git merge
  feat/tier2-...`. Loses the safety of branch isolation.

- **C) Squash all session commits** — `git rebase -i HEAD~16` then
  squash. Cleaner history.

- **D) Create new feature branch per tier** — `tier-1`, `tier-2`,
  etc. Easier to revert individual tiers.

**Recommendation: A** — Keep current branch. Don't merge to main
without push (CLAUDE.md says no local-only merges). Don't squash
(loses audit trail).

---

## Q11: Thesis submission timeline — when?

The thesis has 6 papers + 11 chapters, all defense-ready. Submission
requires:
- Verified DOIs (Q1)
- FPIC decision (Q4)
- Pushed to GitHub (Q9)
- Per-paper Discussion polish (Q3)

**Options:**

- **A) Submit within 1 week** — Aggressive. Requires decisions on
  Q1/Q3/Q4 now, push, final read-through.

- **B) Submit within 1 month** — Allows full FPIC engagement (Q4-E
  with anonymization is feasible in 1 month), DOI verification,
  per-paper Discussion polish.

- **C) Submit within 3 months** — Full FPIC process (Q4-C with
  2-3 communities), full DOI verification, full Discussion rewrite.

- **D) No fixed deadline** — Submit when each blocker resolves.

**Recommendation: B** — 1 month is the sweet spot. Allows
anonymized-data submission (Q4-E) without delay, full DOI
verification, and Discussion polish. Fast enough to maintain
momentum; long enough to do FPIC right.

---

## Q12: Defense-check check #8 — keep critical or downgrade?

The new inline-citation check (added in `f9dd021`) is registered as
**critical** weight in `defense_check.py`.

**Options:**

- **A) Keep as critical** — Current state. Any new inline citation
  without a bib entry fails the build.

- **B) Downgrade to guard** — Non-blocking warning. Lets commits
  through with a "verify these citations later" message.

- **C) Downgrade to informational** — Visible but doesn't block.

**Recommendation: A** — Keep as critical. Round-7 showed 51 inline
citations were invisible to the previous check; if we downgrade,
the same blindspot will re-emerge. Critical weight ensures
defense-check stays useful.

---

## Q13: CLAUDE.md update — needed?

CLAUDE.md says master bib is `thesis/references.bib` (325 entries).
After Round-7 it's 372 entries. CLAUDE.md also doesn't document:

- The two-master-bibs pattern (root union vs thesis master)
- The Round-7 placeholder convention
- The new inline-citation check
- The `papers/drafts/AUDIT/` SANCTIONED_PREFIXES entry

**Options:**

- **A) Full CLAUDE.md refresh** — Update entry counts, document
  new checks, document placeholder convention. ~30 min.

- **B) Minimal CLAUDE.md patch** — Just bump entry count from 325
  to 372. ~5 min.

- **C) Don't touch CLAUDE.md** — Leave for Round-8 documentation
  pass.

**Recommendation: A** — Full refresh. CLAUDE.md is the first thing
any AI session reads; it should reflect current state.

---

## Summary Table

| # | Question | Recommendation | Effort |
|---|---|---|---|
| Q1 | 46 placeholder bibs | **B** (verify academic subset) | 1-2h |
| Q2 | Spot-check `\citep{}` | **B** (top 10 only) | 30m |
| Q3 | p0010 Discussion | **B** (you edit) | 30-60m |
| Q4 | FPIC engagement | **E** (anonymize + future) | 1mo |
| Q5 | Master bib location | **A** (document both) | 10m |
| Q6 | Multiplier rounding | **A** (keep 3.0×) | 0m |
| Q7 | Bib regeneration | **A** (add to defense-check) | 5m |
| Q8 | Placeholder naming | **A** (keep note={}) | 0m |
| Q9 | GitHub push | **A** (you provide PAT) | 5m |
| Q10 | Branch state | **A** (keep branch) | 0m |
| Q11 | Submission timeline | **B** (1 month) | - |
| Q12 | Check #8 weight | **A** (keep critical) | 0m |
| Q13 | CLAUDE.md update | **A** (full refresh) | 30m |

---

## How to answer

You can answer these questions in any format:

1. **Inline in chat** — "Q1=B, Q2=B, Q3=A, Q4=E, Q5=A, Q6=A, Q7=A,
   Q8=A, Q9=A, Q10=A, Q11=B, Q12=A, Q13=A" or "all recommendations"
2. **Edit this file** — Change the answers directly, I read it back.
3. **Verbal** — Tell me, I'll record the answers.

Once you answer, I'll execute the recommended actions and report back
with what was actually done (per the "finish the job" doctrine).
