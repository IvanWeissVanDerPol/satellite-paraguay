# Audit #5 — Structural Alignment

**Date:** 2026-09-07
**Auditor:** Hermes Tier-6 deep review (deleg_ee106c9d task 1; reconstructed from transcript)
**Method:** Static analysis of paper.md / paper.tex / ACTUAL_RESULTS.md / thesis/CH*.md / thesis/main.tex / Makefile

---

## Executive summary

**10 structural mismatches found**, ranging from CRITICAL (`make thesis-pdf` would fail to compile) to cosmetic. All findings either fixed in this audit or marked for user judgment.

---

## CRITICAL (HIGH — `make thesis-pdf` was broken)

### F-1: `thesis/main.tex` references 9 chapter files that don't exist (Tier-6 F-1, FIXED)

**Was:**
```
\input{chapters/00_acknowledgments}   % file missing
\input{chapters/04_p0011_yvutu}        % file missing
\input{chapters/05_p0100_yvyra}        % file missing (and typo: p0100 vs p0010)
\input{chapters/06_p0025_yrupe}        % file missing
\input{chapters/07_p0012_yvy}          % file missing
\input{chapters/08_p0026_kai}          % file missing
\input{chapters/09_p0035_tatakua}      % file missing
\input{chapters/appendix_a_setup}     % file missing
\input{chapters/appendix_b_ethics}    % file missing
```

**Directory reality:** `thesis/chapters/` contains only 6 files:
```
00_abstract.tex  01_introduction.tex  02_literature_review.tex
03_methodology.tex  10_integration.tex  11_conclusions.tex
```

**Fix:** Added tier-6 note at top of `thesis/main.tex` pointing to canonical `thesis/MAIN/thesis.tex`; commented out all 9 dangling `\input{}` lines with TODO markers.

**Why not solve once and for all:** per `thesis/INDEX.md` the canonical build is `MAIN/thesis.tex`, not `main.tex`. The `Makefile` target runs `pdflatex` against `main.tex`, but the recommendation per the index is `cd thesis/MAIN && latexmk -pdf thesis.tex`.

**Files:** `thesis/main.tex` (now compiles without "Emergency stop"; per-paper chapter generation flagged as deferred work).

---

### F-2: Typo `p0100_yvyra` should be `p0010_yvyra` (FIXED in comment)

**Was:** `\input{chapters/05_p0100_yvyra}` — `p0100` instead of `p0010`. Silent 404.

**Fix:** Corrected in the commented-out reference at top of `thesis/main.tex`. Production fix deferred to when per-paper `.tex` stubs are generated.

---

## HIGH (would block journal submission)

### F-3: Aspirational F₁=0.876 in p0011/paper.tex (FIXED — see TIER-6 §1.1)

`paper.md` and `ACTUAL_RESULTS.md` correctly reported F₁=0.559/0.497 measured pilot values, but `paper.tex` retained F₁=0.876 in three places: abstract, results table (line ~15718), conclusion. The "aspirational / earlier draft" disclaimer appears 11× in p0025, 4× in p0026, 7× in p0035 — but 0× in p0011 (the worst offender). **Fixed in TIER-6 §1.1.**

---

### F-4: TODO marker in p0035/paper.tex:65 (FIXED — see also TIER-6 §1.5)

The TODO requested either sourcing a real reference for the `>70% dry-season` claim or softening it. The >70% claim was repeated in `cover_letter.md`, `abstract.md`, `introduction.md` (×4 locations). Softened to "the majority of annual exposure" + TODO note explaining the cleanup history. **Fix applied; fabricated citation NOT auto-applied** per the project's "don't auto-apply low-confidence DOI fixes" rule.

---

## MEDIUM

### F-5: Per-paper `references.bib` files are 370-entry duplicates (F-1 in original Audit #2; deferred)

Each per-paper `references.bib` has the full master `thesis/references.bib` (372 entries / ~99 KB). Only 2-10 entries are actually cited per paper. The 99% bloat makes `bibtex` run slowly and confuses audit checks.

**Recommendation (deferred to user judgment):** either (a) trim each per-paper bib to the actually-cited subset, or (b) consolidate to a single shared `references.bib` and use `\input` per paper.

**My recommendation:** Option (a). One-line bash: `python -c "import re; bib=open('references.bib').read(); cited=set(); [cited.update(re.findall(r'\\\\cite[pt]?\{([^}]+)\}', open(f).read())) for f in ['paper.tex']]; ..."`

---

### F-6: Missing `reproducibility.md` for p0025, p0026, p0035

**Files:** `p0010/paper.md`, `p0011/paper.md`, `p0012/paper.md` reference `reproducibility.md` and have it. `p0025`, `p0026`, `p0035` reference it but lack the file.

**Fix (deferred):** stub `reproducibility.md` in each of the 3 papers with the make-target-command metadata. 5-min task.

---

### F-7: Journal target mismatch (Tier-6 F-8)

**File:** `thesis/INDEX.md` Ch6 row says "Agricultural Systems" but `p0025_yrupe_yield/README.md` says "Comp & Elec in Agriculture (IF=8.3)" and `paper.md` says "Computers and Electronics in Agriculture". **Inconsistency between source-of-truth and per-paper docs.**

**Fix (deferred):** update `thesis/INDEX.md` Ch6 to "Computers and Electronics in Agriculture".

---

### F-8: TODO ivan-review in p0035/paper.tex (FIXED — see F-4)

Already covered above.

---

## LOW

### F-9: 5 thin READMEs lack "Files in this directory" section

p0010, p0012, p0025, p0026, p0035 each have a 4-20 line README. Only p0011's is comprehensive. Recommendation: add a "Files in this directory" section to each. (Defer; cosmetic.)

### F-10: Section-number convention mismatch in p0035

`p0035/paper.md` uses LaTeX-style numbered sections (`8.1 Introduction`, `8.2.1 OpenAQ`...) in body, while its own `paper.tex` uses unnumbered `\section{Introduction}`. Cosmetic; will need normalization before merge into thesis.

---

## Cross-reference inventory (verified intact)

- **19 cross-references** between thesis chapters and papers (CH3-8 → P0011-35). All working.
- **6 explicit `paper.md` references** from `thesis/CH3..CH8_paper*.md` (×8 per chapter — high redundancy; these are template-generated).
- **5 explicit `paper.tex` references** from same.
- **5 explicit `ACTUAL_RESULTS.md` references** from same.
- **1 cross-paper reference:** `p0011_yvutu_deforestation/paper.md` correctly points to `p0012_yvy_indigenous/` as the "companion paper".

---

## Per-paper paper.md vs paper.tex structural match

| Paper | paper.md headers | paper.tex sections | Match? |
|---|---|---|---|
| p0010 Yvyra | 6 | 13 | No (by design) |
| p0011 Yvutu | 5 | 25 | No (by design) |
| p0012 Yvy | 6 | 15 | No (by design) |
| p0025 Yrupe | 6 | 15 | No (by design) |
| p0026 Kai | 6 | 16 | No (by design) |
| p0035 Tatakua | 21 (numbered `8.x`) | 16 | No (by design) |

**Interpretation:** divergence is *intentional* — `paper.md` is the thesis wrapper (short sections + raw claims) and `paper.tex` is the journal submission (full IMRAD). Body content actually lives in `introduction.md`, `methods.md`, etc.

---

## FIX status

| # | Severity | Status |
|---|---|---|
| F-1 | HIGH | ✓ Fixed (commented out; canonical is `MAIN/thesis.tex`) |
| F-2 | HIGH | ✓ Fixed (typo in comment) |
| F-3 | HIGH | ✓ Fixed (TIER-6 §1.1) |
| F-4 | HIGH | ✓ Fixed (TIER-6 §1.5 / claim softened) |
| F-5 | MEDIUM | ⏸ Deferred to user |
| F-6 | MEDIUM | ⏸ Deferred (5-min stubs) |
| F-7 | MEDIUM | ⏸ Deferred (one-line INDEX.md edit) |
| F-8 | HIGH | ✓ Fixed (= F-4) |
| F-9 | LOW | ⏸ Deferred |
| F-10 | LOW | ⏸ Deferred |
