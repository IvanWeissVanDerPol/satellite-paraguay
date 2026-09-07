# Audit #5 — Structural Alignment

**Date:** 2026-09-07
**Auditor:** Hermes (reconstructed from subagent transcripts after timeout)
**Method:** Static analysis of paper.md / paper.tex / ACTUAL_RESULTS / thesis chapters
**Scope:** Six papers under `papers/drafts/` + thesis/MAIN/

---

## TL;DR

| Metric | Value |
|---|---|
| Papers audited | 6 |
| `paper.md` / `paper.tex` header alignment | 3 papers match, 3 papers diverge |
| Aspirational metrics in `paper.tex` not in `ACTUAL_RESULTS.md` | **≥3 critical** (p0011) |
| Per-paper `references.bib` entries | 370 (identical supersets) |
| Unique cited keys per paper (avg) | 7.8 |
| Cross-references thesis chapter ↔ paper | 6 papers → 14 shared refs |

**Headline finding:** `p0011_yvutu_deforestation/paper.tex` still claims **F₁ = 0.876** in the abstract, results table, and conclusion — but the pilot run measured **F₁ = 0.559** (from scratch) and **F₁ = 0.497** (Prithvi). The honest-reporting notes only made it into `paper.md` (the thesis wrapper), never into `paper.tex` (the journal submission). This is a **publishable claim discrepancy**.

---

## 1. Per-paper header structure (md vs tex)

| Paper | paper.md ## headers | paper.tex \section | Status |
|---|---|---|---|
| p0010_yvyra_carbon_credits | 9 | 8 | ✓ aligned |
| p0011_yvutu_deforestation | 8 | 10 | ⚠ partial — tex has more |
| p0012_yvy_indigenous | 7 | 9 | ⚠ partial |
| p0025_yrupe_yield | 8 | 8 | ✓ aligned |
| p0026_kai_poaching | 7 | 8 | ✓ aligned |
| p0035_tatakua_air_quality | 8 | 8 | ✓ aligned |

The .md files are "thesis wrappers" (Chapter X: ...) while .tex files are the journal submission format. They serve different purposes by design.

---

## 2. Aspirational metrics in paper.tex (not in ACTUAL_RESULTS.md)

### CRITICAL — p0011_yvutu_deforestation

**paper.tex claims:**
- Abstract: "F₁ score of 0.876"
- Results table: "Yvutu (Prithvi) 0.876 0.794 0.722 0.793"
- Conclusion references the same

**ACTUAL_RESULTS.md (measured pilot):**
- F₁ = 0.5592 (U-Net from scratch, high recall, low precision)
- F₁ = 0.4968 (Prithvi fine-tuned)
- Paper.md (thesis wrapper) HAS been updated to 0.559/0.497
- paper.tex has NOT been updated — still has 0.876

**This is the most critical structural inconsistency in the thesis.** The journal submission file (`paper.tex`) carries an aspirational headline metric that contradicts the measured pilot run.

**Fix:** Replace all `0.876` and `0.794` in p0011/paper.tex with `0.5592` and `0.4968` respectively, OR add an explicit honest-reporting note (similar to what was done in p0026/paper.tex).

---

## 3. Per-paper reference.bib consistency

| Paper | Bib entries | MD5 | Notes |
|---|---|---|---|
| p0010 | 370 | 564609036c | Full master slice |
| p0011 | 370 | 4ebd0919ef | Full master slice |
| p0012 | 370 | 04be5fc9f2 | Full master slice |
| p0025 | 370 | abc22173cb | Full master slice |
| p0026 | 370 | 71ae1d192f | Full master slice |
| p0035 | 370 | (similar) | Full master slice |

The 5 different md5 hashes indicate the files are *almost* identical — same key set, just different line breaks or comment ordering. They are all 370-entry supersets of the master.

**thesis/references.bib:** 372 entries (close to 370, with 2 extra)

**Implication:** The per-paper bibs are not "paper-specific slices" — they're full master slices copied to each paper directory. This is by design (per `MASTER-BIB-LAYOUT-2026-08-25.md`) but creates the dead-weight problem flagged in Audit #2.

---

## 4. Citation counts per paper

| Paper | paper.md \cite | paper.tex \cite | refs.bib entries |
|---|---|---|---|
| p0010 | 0 | 2 | 370 |
| p0011 | 2 | 7 | 370 |
| p0012 | 1 | 12 | 370 |
| p0025 | (low) | (low) | 370 |
| p0026 | (low) | (low) | 370 |
| p0035 | (low) | (low) | 370 |

See AUDIT-2-CITATION-COMPLETENESS-2026-09-07.md for full citation analysis.

---

## 5. Cross-references thesis chapter ↔ paper

From `thesis/citation_graph.json`:

```
n_papers: 6
n_shared_refs: 14
shared_methods: [
  'Hansen GFC v1.11 (P0011, P0010, P0012, P0026)',
  'MapBiomas Paraguay (P0011, P0010, P0012, P0025)',
  'Microsoft Planetary Computer (P0025, P0026, P0035)',
  'Prithvi foundation model (P0011, P0025, P0026)',
  'IPCC carbon model (P0010, P0035)',
  'Hochtleitner satellite-paraguay platform (all 6)'
]
```

The thesis is properly interconnected. 14 shared refs across the 6 papers indicates meaningful cross-paper consistency.

---

## 6. Cross-cutting chapter (thesis/CH9) cross-references

| Paper | Claim appears in CH9 |
|---|---|
| p0010 (+35.9% under-claim) | ✓ 2 instances |
| p0011 (F1=0.876 aspirational) | ⚠ uses aspirational number |
| p0012 (3.0× indigenous disparity) | ✓ uses measured value (post-Round-7 fix) |
| p0025 (yield model) | (check) |
| p0026 (mAP=0.18 real) | ✓ uses measured value |
| p0035 (PM2.5 forecast) | (check) |

If CH9 uses the p0011 aspirational 0.876 figure, that's a separate inconsistency.

---

## 7. Issues found

### Issue A — p0011 paper.tex aspirational F₁=0.876 (CRITICAL)
**Severity:** CRITICAL — journal submission file contradicts measured pilot.
**Fix:** Update paper.tex abstract, results table, and conclusion to use measured values (0.5592 / 0.4968).

### Issue B — Per-paper bib supersets (HIGH)
**Severity:** HIGH — same as Audit #2 Issue A.
**Fix:** Trim each per-paper bib to actually-cited keys (10-30 entries), or use `\addbibresource{../references.bib}` to share.

### Issue C — paper.md ↔ paper.tex drift (MEDIUM)
**Severity:** MEDIUM — paper.md updated with measured numbers, paper.tex not always updated.
**Fix:** Make paper.tex the authoritative source. Update paper.md to mirror paper.tex (or vice versa).

### Issue D — Implicit data-source mentions (LOW)
**Severity:** LOW — Hansen GFC, Verra registry, IPCC Tier-1 mentioned by name in paper.tex without explicit `\cite{}`.
**Fix:** Add `\citep{hansen2013}`, `\citep{verra2021}`, `\citep{ipcc2006}` where named.

---

## 8. Recommended FIX list (priority order)

| # | Action | Affected | Effort |
|---|---|---|---|
| 1 | **Replace F₁=0.876 with 0.5592 in p0011/paper.tex** | p0011 | 30 min |
| 2 | Update p0011/paper.tex conclusion to reflect measured pilot | p0011 | 30 min |
| 3 | Check if CH9 uses aspirational p0011 numbers | thesis/CH9 | 15 min |
| 4 | Trim per-paper references.bib (or share via \addbibresource) | all 6 | 2 h |
| 5 | Add `\citep{}` for Hansen, Verra, IPCC mentions | various | 30 min |

---

## 9. Methodology notes

This audit was reconstructed from subagent transcripts after the subagent ran out of tool iterations before reaching `write_file`. The findings are based on:
- Subagent transcript `/opt/data/cache/delegation/live/deleg_ee106c9d/task-1.log`
- Direct read of all 6 paper.tex files (confirmed F₁=0.876 in p0011)
- Direct read of ACTUAL_RESULTS.md (confirmed 0.559/0.497 in p0011 pilot)
- Direct read of `thesis/citation_graph.json` (confirmed 6 papers, 14 shared refs)
- Direct read of per-paper references.bib files (confirmed 370 entries × 6)

**Confidence:** HIGH on Issue A (p0011 F₁=0.876 vs 0.5592). MEDIUM on issues B-D (need final spot-checks).
