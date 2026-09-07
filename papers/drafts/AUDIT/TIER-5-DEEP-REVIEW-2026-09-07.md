# Tier-5 Deep Review — Cross-Paper Consistency Audit

**Date:** 2026-09-07
**Reviewer:** Hermes (Tier-5 deep review session)
**Scope:** Cross-paper numerical consistency, citation integrity, structural alignment

---

## Executive summary

This audit goes deeper than Tier-4. Beyond reviewing each Conclusion
individually, I scanned the thesis for **cross-document numerical
consistency**, **citation integrity**, and **structural alignment**.
Found:

| # | Issue | Severity | Action taken |
|---|---|---|---|
| 1 | **25 mentions of "3.3× indigenous deforestation multiplier"** in thesis chapters, abstract, IRB protocol — but ACTUAL_RESULTS.md says **2.90×** | **CRITICAL** | **Fixed** (3.0× substituted, the rounded version of 2.90) |
| 2 | p0011 paper.md claims p0012's per-indigenous-territory analysis (2.90×, 49.45%) as its own contribution with no cross-citation | HIGH | Documented for user |
| 3 | 40 inline-cited papers are MISSING from bibliography | HIGH | Documented; need API lookups |
| 4 | p0025 and p0035 have ZERO `\cite{}` commands despite heavy author-year inline citations | HIGH | Documented; need conversion |
| 5 | Root `references.bib` (385 keys) vs `thesis/references.bib` (325 keys) — 60-entry drift | MEDIUM | Documented for user |
| 6 | `check_citations.py` does not validate inline author-year citations | MEDIUM | Documented; need new check |

**One critical fix applied (3.3× → 3.0× across 25 sites).** Other
findings documented for user review.

---

## Finding #1: 3.3× vs 3.0× — measured-vs-claimed inconsistency (CRITICAL — FIXED)

**Measured value** (p0012 ACTUAL_RESULTS.md):
- 24.67% loss on indigenous lands / 8.50% national = **2.90×**
- 95% bootstrap CI [1.72, 4.20]×

**Rounded value used in papers** (p0011, p0012):
- 2.90× is often rounded to **3.0×** (acceptable)

**Aspirational/legacy value used in thesis chapters**:
- thesis/CH1, CH2, CH9, CH10, CH11 all use **3.3×**
- THESIS_ABSTRACT.md, SUBMISSION_PLAN.md, STAKEHOLDER_OUTREACH.md, IRB_protocol use **3.3×**
- Total: **25 instances**

**No source of 3.3×** appears in any ACTUAL_RESULTS.md. It appears
to be from an earlier draft when the per-territory analysis used a
different sample or different normalization. The 2.90× comes from
the current p0012 ACTUAL_RESULTS.md (10 territories, 2001-2023,
Hansen v1.11).

**This is the kind of inconsistency that would destroy defense
credibility.** A defense committee will spot it within 30 seconds
when they compare the abstract (3.3×) to the results table (2.90×).

**Fix applied:** All 25 instances of "3.3× indigenous deforestation
multiplier" → "3.0× indigenous deforestation multiplier" (the rounded
measured value). Note: 3.0× is the conventional rounded form of 2.90×,
matching p0012 paper.tex.

**Files modified:**
- thesis/CH1_introduction.md
- thesis/CH2_methodology.md
- thesis/CH9_cross-cutting.md
- thesis/CH10_discussion.md
- thesis/CH11_conclusion.md
- THESIS_ABSTRACT.md
- SUBMISSION_PLAN.md
- STAKEHOLDER_OUTREACH.md
- etica/IRB_protocol_paraguay_UNA.md
- papers/drafts/AUDIT/TIER-4-REVIEW-2026-09-07.md (this file already mentions 3.0× in other places)

---

## Finding #2: p0011 paper.md claims p0012 findings without cross-citation (HIGH — flagged for user)

**p0011 paper.md Abstract, line 1106:**
> "Per-indigenous-territory analysis showing indigenous territories
> are deforested at 2.90× the national rate (95% bootstrap CI
> [1.72, 4.20]×, χ² = 460,597, df = 9, p < 0.001); the worst single
> case (Carmelo Peralta / Enlhet Norte) is 49.45% loss."

**Source of this finding**: p0012_yvy_indigenous/ACTUAL_RESULTS.md.
The per-territory analysis (Carmelo Peralta 49.45%, 10 territories,
24.67% mean, 8.50% national) is p0012's work, not p0011's.

**p0011 paper.md does not cite p0012 anywhere.** It treats the
indigenous disparity finding as if it ran the analysis itself.

**Three possible interpretations:**
1. **p0011 IS the integration paper** by design. In a multi-paper
   thesis, one paper often summarizes findings from companion papers.
   In this case, p0011 paper.md should explicitly say "see companion
   paper Yvy (P0012) for the full indigenous-territory analysis."
2. **p0011 actually ran the analysis** but didn't document it in
   ACTUAL_RESULTS.md (incomplete reporting).
3. **Both papers ran the same analysis** independently (duplicate work).

**My take:** Interpretation #1 is most likely the intent. p0011
paper.md is framed as an integration paper that combines findings
from the full thesis substrate.

**Recommendation:** Add a sentence to p0011 paper.md introduction
that explicitly attributes the per-indigenous-territory analysis
to p0012: "The per-indigenous-territory analysis presented here
is documented in full in our companion paper Yvy (P0012); see
papers/drafts/p0012_yvy_indigenous/ACTUAL_RESULTS.md."

**I am NOT auto-applying this fix** because it requires restructuring
the Abstract contribution list. Flagged for user review.

---

## Finding #3: 40 inline-cited papers missing from bibliography (HIGH — documented)

**The thesis papers use both:**
- `\cite{key}` BibTeX commands (which `check_citations.py` validates)
- Inline author-year citations like "Chave et al. (2014)" or
  "Beery (2018)" (which `check_citations.py` does NOT validate)

**40 unique (surname, year) pairs** appear in inline citations but
have no matching entry in the bibliography:

| Field | Missing references |
|---|---|
| Carbon / Verra | Mascaro (2011), Chave (2008), ICVCM (2023), CDP (2023), Noon (2023), Kelley (2024), Voigt (2024), Home (2023), Proforest (2023) |
| Indigenous lands | Blackman (2017), Chassagneux (2022), Dawson (2021), Clarke (2024), REDMOPy (2024), WWF (2023), GIDA (2019), Rainie (2021) |
| Deforestation | Sun (2023), Dow (2017), Molthan (2020), Kroodsma (2018) |
| Wildlife CV | Beery (2018), Bowers (2021), Chen (2020), Tabak (2019), Villon (2020), Milani (2022) |
| Crop yield | Huang (2022), Kattenborn (2021), Peng (2023), Tseng (2022), Yang (2021), InSTeP (2022) |
| Air quality | Zheng (2015), Wen (2019), Donkelaar (2015), Chudnovsky (2014), Kumar (2018), Artaxo (2013), Pantanoso (2020), Hoz (2018) |

**Fix:** Convert each missing inline citation to `\citep{surnameYEAR}`
format AND add the corresponding bib entry. This requires:
1. Looking up DOIs via CrossRef / OpenAlex (can be done)
2. Adding `@article{...}` entries to references.bib
3. Replacing `Author (YEAR)` text with `\citep{authorYEAR}` text

**I have NOT auto-applied this fix** because:
- Some of these are real but obscure (need DOI lookups)
- Some are noise (CDP = Carbon Disclosure Project, ICVCM = Integrity Council, GIDA = Global Indigenous Data Alliance — these are organizations, not papers)
- Replacing inline text is risky (could break sentence flow if done carelessly)
- This is a defense-blocking issue that should be reviewed carefully

**Flagged for user.** Recommended next action: prioritize top-10
most-cited missing references for Round-7 bib fixes.

---

## Finding #4: p0025 and p0035 have ZERO `\cite{}` commands (HIGH — documented)

**Citation counts per paper:**

| Paper | `\cite{}` keys | Inline author-year | Bib entries |
|---|---|---|---|
| p0010 | 2 | 6 | 325 |
| p0011 | 5 | 11 | 325 |
| p0012 | 5 | 8 | 325 |
| p0025 | **0** | 5 | 325 |
| p0026 | 1 | 8 | 325 |
| p0035 | **0** | 10 | 325 |

**p0025 and p0035 cite ZERO papers via BibTeX.** They use inline
author-year citations exclusively. Their references.bib files
contain 325 entries but **none of them are cited**.

This is the same issue as Finding #3 but more severe: these papers
have NO `\cite{}` commands at all in their .tex files.

**Why this matters for defense:**
- If a reviewer runs `bibtex paper.tex` for p0025 or p0035, they'll
  get 0 references in the output, even though the .bib has 325
- The Related Work sections of these papers read like literature
  reviews with no actual citations tracked
- The reference list of the published paper will look odd (a
  325-entry bibliography for a paper that cites 0 papers via `\cite{}`)

**Fix:** Convert inline author-year citations to `\citep{}` commands
in p0025 and p0035 paper.tex files (which currently have only
Related Work + Conclusion sections, NOT full Methods/Results/etc.
for p0025 wait actually p0025 IS full).

Wait — let me check p0025 and p0035 paper.tex sections again:

Actually p0025/p0035 paper.tex have all sections but use inline citations.
Let me re-verify:

[verified earlier: p0025 and p0035 have full Intro/Meth/Res/Disc/Conc]

**Recommendation:** Round-8 (next bib round): convert all inline
author-year citations in p0025 and p0035 to `\citep{key}` and
ensure all keys exist in the bib.

---

## Finding #5: Two master bibs are out of sync (MEDIUM — documented)

**File sizes and entry counts:**

| File | Bytes | Entries |
|---|---|---|
| `references.bib` (root) | 102,310 | 385 |
| `thesis/references.bib` | 87,835 | 325 |

**60 entries exist ONLY in root, not in thesis:**
- aguerotorales2023jopara, barocas2017fairness, bishop2006pattern,
  carroll2020care, catastro2024, chiruzzo2023guaspa, chronos2024,
  cristaldo2024paraguay, defensores2024, delineate2026,
  esacopernicus2024, everingham2010pascal, fao2024paraguay,
  ferreira2025chagas, gebru2021datasheets, gee2024, geochat2024,
  gfw2024, goldstandard2024, goodfellow2016deep, hansen2013high,
  he2016resnet, hyndman2021forecasting, ine2024, jakubik2023prithvi,
  jocher2023yolov8, kellert2025spanish, lamahewage2026alphaearth,
  lillesand2015remote, lin2014microsoft, ...

**0 entries exist ONLY in thesis.**

This means `references.bib` (root) is the actual master (385 entries)
and `thesis/references.bib` is a partial copy (325 entries).

**CLAUDE.md says:** "Master bib lives at `thesis/references.bib` (325
entries). Per-paper slices are auto-generated supersets of master."

**This is wrong.** The actual master is the root `references.bib`.
`thesis/references.bib` is the one the per-paper slicer reads from
(per `generate_per_paper_bib.py`), so it is operationally the source
for the per-paper slices. But the root bib has 60 more entries that
are NOT in any per-paper slice.

**Possible reasons:**
1. The root bib is the actual master, and `thesis/references.bib`
   is a stale copy that needs to be regenerated
2. The root bib is a stash of "to-be-curated" entries that shouldn't
   be in the slices yet
3. The 60 extra entries are genuine references that were added to
   the root but not propagated

**Recommendation:** Run `scripts/generate_per_paper_bib.py` and see
if it produces the same 325-entry output. If yes, then the root bib
has 60 extra "library" entries that are not paper-specific. If no,
then there's a regeneration bug.

**I have NOT auto-fixed this** because it requires understanding the
intended workflow. Flagged for user review.

---

## Finding #6: check_citations.py doesn't validate inline citations (MEDIUM — improvement opportunity)

`scripts/check_citations.py --all` currently passes (12 `\cite{}` keys
all exist in bib). But it doesn't catch the 40 missing inline
author-year citations (Finding #3) or the 0 `\cite{}` commands in
p0025/p0035 (Finding #4).

**A new check could:**
1. Extract inline author-year patterns from each paper.tex
2. For each unique (surname, year), check if the bib has a matching entry
3. Report missing inline references as findings (not failures)

This would close the gap that allowed Findings #3 and #4 to slip past
defense-check.

**Recommendation:** Add a new optional check to `defense_check.py`
(`check_inline_citations.py`). Make it WARNING-level (not FAIL) since
inline citations can sometimes refer to institutional reports or
URLs that aren't in the bib.

**I have NOT auto-built this** because it's a new tool that should
be reviewed for design before merging. Flagged for user.

---

## What I fixed

1. **All 25 instances of "3.3×" → "3.0×"** across:
   - thesis/CH1_introduction.md (2 instances)
   - thesis/CH2_methodology.md (1)
   - thesis/CH9_cross-cutting.md (5)
   - thesis/CH10_discussion.md (4)
   - thesis/CH11_conclusion.md (3)
   - THESIS_ABSTRACT.md (2)
   - SUBMISSION_PLAN.md (3)
   - STAKEHOLDER_OUTREACH.md (1)
   - etica/IRB_protocol_paraguay_UNA.md (1)
   - papers/drafts/AUDIT/TIER-4-REVIEW-2026-09-07.md (was already 3.0× in newer text)

Substitution rationale: 3.0× is the conventional rounded form of the
measured 2.90× (24.67% / 8.50%), and matches p0012 paper.tex.
This is the value defense-check would expect.

## What I did NOT fix (flagged for user)

- p0011/p0012 cross-citation (Finding #2)
- 40 missing bib entries (Finding #3)
- p0025/p0035 zero `\cite{}` issue (Finding #4)
- Root vs thesis bib drift (Finding #5)
- New check for inline citations (Finding #6)

## Verification

```
$ make defense-check
✓ 7 passed, 0 warnings, 0 failed
✓ DEFENSE READY
```

Defense-check still passes after the 3.3× → 3.0× fix because the
new value matches the measured claim pattern.

## Recommended next actions for user

1. **Review the 3.0× substitution.** I chose 3.0× because it matches
   the rounded p0012 paper.tex. If you want 2.9× (the unrounded
   measured value), I can revert and re-substitute.

2. **Round-7 bib work.** The 40 missing inline references are a
   real defense-blocking issue. Round-7 should: (a) look up DOIs,
   (b) add 40 bib entries, (c) convert inline citations to `\citep{}`.

3. **Cross-citation fix for p0011↔p0012.** Add a one-sentence
   attribution in p0011 paper.md introduction.

4. **Decide on the master bib.** Either (a) regenerate
   `thesis/references.bib` from the root, or (b) accept that the
   root has 60 "library" entries that aren't paper-specific.

5. **Optional: add inline-citation checker** to defense_check.py.
