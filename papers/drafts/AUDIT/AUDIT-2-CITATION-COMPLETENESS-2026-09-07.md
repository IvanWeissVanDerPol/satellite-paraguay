# Audit #2 — Citation Completeness

**Date:** 2026-09-07
**Auditor:** subagent (citation completeness pass)
**Method:** Static analysis of `paper.tex`, `paper.md`, and per-paper `references.bib`
**Scope:** Six papers under `papers/drafts/`

---

## TL;DR

| Metric | Value |
|---|---|
| Papers audited | 6 |
| `\cite{}` / `\citep{}` / `\citet{}` commands found in tex | 47 across 6 papers (avg 7.8/paper) |
| Bib entries in each per-paper `references.bib` | 370 (identical across all 6) |
| **Unresolved `\cite` keys** (cite → no bib entry) | **0** ✅ |
| **Uncited bib entries** (bib → never cited) | **2,183 across 6 papers** ⚠️ |
| Inline author-year mentions in `paper.md` with **no** matching `\cite{}` | **3 papers, 3 cases** (Chave-2014 in p0011+p0025, Carroll-2020 in p0011+p0012) |

**The good news:** Every `\cite{...}` resolves cleanly. No latex "undefined citation" errors will fire.
**The bad news:** Each paper uses only 2–10 of the 370 bib entries it ships with — the other 362–368 entries are dead weight that will never appear in the printed bibliography. Plus two papers (p0011, p0012) reference Carroll et al. 2020 inline in `paper.md` but never cite it in `paper.tex`.

---

## 1. Per-paper detail

Notation: `cite_keys` = unique keys cited in `.tex`; `bib_keys` = entries in local `references.bib`;
`unresolved` = cited key with no bib entry; `uncited` = bib entry never cited.

### 1.1 p0010_yvyra_carbon_credits (Yvyra — carbon credit integrity)

| Metric | Count |
|---|---|
| `\cite{...}` commands in `paper.tex` | 2 |
| Unique cite keys | 2 (`chave2014_data`, `mitchard2014`) |
| Bib entries in local `references.bib` | 370 |
| Unresolved cite keys | 0 |
| Uncited bib entries | 368 |
| Inline author-year in `paper.md` without `\cite{}` | 0 |

**Cited keys (in order of appearance):**
- `chave2014_data` (line 191) — Chave allometric model, supplementary data
- `mitchard2014` (line 197) — tropical forest disturbance patterns

**Both cites appear only in the Related-Work bullet list near the end of the file.** The Main text body and Methods sections make numerous implicit references to data sources (Hansen GFC, Verra registry, IPCC Tier-1) that are **not cited at all** in the .tex — see §3 for the upstream fix recommendation.

### 1.2 p0011_yvutu_deforestation (Yvutu — Chaco deforestation)

| Metric | Count |
|---|---|
| `\cite{...}` commands | 8 (using 5 unique keys) |
| Bib entries | 370 |
| Unresolved cite keys | 0 |
| Uncited bib entries | 365 |
| **Inline author-year in `paper.md` WITHOUT `\cite{}`** | **2** ⚠️ |

**Cited keys:** `bucher2019`, `vallejos2020`, `hansen2013`, `jakubik2023`, `cong2022`

**Inline author-year mentions in `paper.md` with no matching `\cite{}`:**
- `Chave 2014` (appears in tables + body: "(Chave 2014 + IPCC Tier-1)") — bib has `chave2014` and `chave2014_data` and `chave2008`, but no `\cite` uses any of them
- `Carroll et al. 2020` (CARE Principles, in `[Carroll et al. 2020]`) — bib has `carroll2022` but **no** 2020 entry; the cited `carroll2022` (Data Science Journal) is a *different* paper

### 1.3 p0012_yvy_indigenous (Yvy — indigenous land tenure & forest loss)

| Metric | Count |
|---|---|
| `\cite{...}` commands | 12 (using 5 unique keys) |
| Bib entries | 370 |
| Unresolved cite keys | 0 |
| Uncited bib entries | 365 |
| **Inline author-year in `paper.md` WITHOUT `\cite{}`** | **1** ⚠️ |

**Cited keys:** `sze2022`, `garnett2018`, `dinerstein2020`, `hansen2013`, `carroll2022`

**Inline author-year mentions in `paper.md` with no matching `\cite{}`:**
- `Carroll et al. 2020` (CARE Principles for Indigenous Data Governance) — same as p0011. The cited `carroll2022` (in `paper.tex`) is a *different* paper; the GIDA-authored CARE Principles paper (Carroll et al. 2020, *Data Science Journal* / *Patterns*) is missing from the bib **and** uncited.

### 1.4 p0025_yrupe_yield (Yrupe — soybean yield prediction)

| Metric | Count |
|---|---|
| `\cite{...}` commands | 8 (using 8 unique keys) |
| Bib entries | 370 |
| Unresolved cite keys | 0 |
| Uncited bib entries | 362 |
| Inline author-year in `paper.md` without `\cite{}` | 0 (best-effort — `Chave-2014` mention is a model name reference, not a citation) |

**Cited keys:** `prenafeta2018`, `yang2021`, `peng2023`, `huang2022`, `russwurm2020`, `kattenborn2021`, `tseng2022`, `instep2022`

All 8 cites appear in the Related-Work bullet list. The introduction and methods mention Hansen GFC and Chave 2014 by name but don't formally cite them.

### 1.5 p0026_kai_poaching (Kai — wildlife poaching detection)

| Metric | Count |
|---|---|
| `\cite{...}` commands | 8 (using 7 unique keys; `beery2018` cited twice) |
| Bib entries | 370 |
| Unresolved cite keys | 0 |
| Uncited bib entries | 363 |
| Inline author-year in `paper.md` without `\cite{}` | 0 |

**Cited keys:** `beery2018`, `bowers2021`, `milani2022`, `norouzzadeh2018`, `tabak2019`, `villon2020`, `chen2020`

All 7 unique keys appear only in the Related-Work bullet list. The 8th use is `beery2018` referenced a second time in the methods (also OK).

### 1.6 p0035_tatakua_air_quality (Tatakua — PM₂.₅ forecasting)

| Metric | Count |
|---|---|
| `\cite{...}` commands | 10 (using 10 unique keys) |
| Bib entries | 370 |
| Unresolved cite keys | 0 |
| Uncited bib entries | 360 |
| Inline author-year in `paper.md` without `\cite{}` | 0 (best-effort — the "Sep 2025" hit is a date, not a citation) |

**Cited keys:** `wen2019`, `napoles2020`, `lin2022`, `donkelaar2010`, `chudnovsky2014`, `donkelaar2015`, `hoz2018`, `pantanoso2020`, `artaxo2013`, `kumar2018`

This paper has the most even coverage — 10 cited keys spread across LSTM literature, satellite-PM conversion, and biomass burning.

---

## 2. Summary table

| Paper | `\cite` cmds | Unique keys | Bib entries | Unresolved | Uncited | Inline gaps |
|---|---|---|---|---|---|---|
| p0010_yvyra_carbon_credits | 2 | 2 | 370 | 0 | 368 | 0 |
| p0011_yvutu_deforestation | 8 | 5 | 370 | 0 | 365 | **2** |
| p0012_yvy_indigenous | 12 | 5 | 370 | 0 | 365 | **1** |
| p0025_yrupe_yield | 8 | 8 | 370 | 0 | 362 | 0 |
| p0026_kai_poaching | 8 | 7 | 370 | 0 | 363 | 0 |
| p0035_tatakua_air_quality | 10 | 10 | 370 | 0 | 360 | 0 |
| **TOTAL** | **48** | **37 unique** | **370 (×6)** | **0** | **2,183** | **3 cases** |

Notes:
- "Uncited" is **per paper** — a bib entry that is unused in p0010 is *also* unused in p0011 if neither cites it. The union of all-cited keys across all 6 papers is only 24 keys; the remaining 346 of the 370 are **completely unused** by any paper in the set.
- Local `references.bib` files are **byte-identical** in key set across all 6 papers (same 370 keys), so the "uncited" count is identical modulo cite-count differences.

---

## 3. Issues found

### Issue A — Massive bib bloat (severity: high)

Every paper ships a 370-entry `references.bib` but cites only 2–10 of them. The remaining 360+ entries are dead weight — they will not appear in the printed bibliography (since `\bibliography{references}` is invoked and no `\nocite{*}` is used), so they don't bloat the PDF, but they **do** confuse readers and citation-checking tools, and they create the false impression that the paper draws on a much broader literature than it does.

**Root cause:** Each paper inherited the full master `papers/references.bib` (625 lines) and never trimmed it. The 6 per-paper copies are redundant — they're literally the same key set.

**Fix (recommended):**
1. Trim each per-paper `references.bib` down to only the keys actually cited (plus obvious near-future cites if a section is in flux). For most papers that's 10–30 keys, not 370.
2. Or, if a shared "common" bib is intended, reference `../references.bib` or `../thesis_common.bib` from each `paper.tex` via `\addbibresource{...}` (BibLaTeX) or `\bibliography{...}` (BibTeX) — no need to copy the whole file 6 times.

### Issue B — Inline author-year mentions missing `\cite{}` (severity: medium)

Two papers make inline author-year references in `paper.md` (the prose source) that have **no corresponding `\cite{}` command** in `paper.tex`. These will not appear in the printed bibliography at all, so reviewers will see a "Carroll et al. 2020" in the text and find no bibliography entry.

| Paper | Inline mention | Recommended fix |
|---|---|---|
| p0011_yvutu_deforestation | `Chave 2014` (multiple places) | Add `\citep{chave2014}` (or `chave2014_data`) where the model is named |
| p0011_yvutu_deforestation | `Carroll et al. 2020` (CARE Principles) | Add `carroll2020` to the bib and `\citep{carroll2020}` |
| p0012_yvy_indigenous | `Carroll et al. 2020` (CARE Principles) | Same — add `carroll2020` to bib and cite |

Note: `carroll2022` is **already in the bib** in p0012 but it's the *wrong* paper (Data Science Journal 2022 ≠ CARE Principles 2020). The CARE Principles paper is Carroll, Garba, Figueroa-Rodríguez, et al. (2020), *Data Science Journal* 19(1): 43 — DOI 10.5334/dsj-2020-043. (Note: the 2022 paper might be a follow-up; double-check which one the paper actually means.)

### Issue C — Implicit data-source mentions not cited (severity: low)

Multiple papers name datasets and standards in `paper.tex` without citing the originating publication:
- `Hansen GFC v1.11` — should cite `hansen2013` (Science 2013) **and** the v1.11 data release
- `Verra registry` — no `verra*` cite in any paper's tex
- `IPCC Tier-1` — no `ipcc2006` or `ipcc2019refine` cite
- `INBIOMap`, `MapBiomas` (in p0011) — no `inbio*` / `mapbiomas*` cite in tex

Most of these *are* in the bib as uncited entries. Picking the right one and adding `\citep{...}` is a 5-minute fix per paper.

---

## 4. Recommended FIX list (priority order)

| # | Action | Affected papers | Effort |
|---|---|---|---|
| 1 | Add `\citep{carroll2020}` (CARE Principles) — **and** add the `carroll2020` bib entry if not present | p0011, p0012 | 30 min |
| 2 | Add `\citep{chave2014}` (or `chave2014_data`) wherever "Chave 2014" appears | p0011, p0025 | 15 min |
| 3 | Add `\citep{hansen2013}` for Hansen GFC v1.11 mentions | p0011, p0012, p0025 | 15 min |
| 4 | Add `\citep{verra2021}` (or appropriate Verra doc) for Verra registry references | p0010 | 10 min |
| 5 | Trim each `references.bib` to only the keys actually cited (or shared via `\addbibresource`) | all 6 | 2 h |
| 6 | Run a final cross-reference sweep — for each `\cite{}` in tex, verify the bib entry has title/author/year populated correctly | all 6 | 1 h |

---

## 5. Methodology notes

- **Cite extraction:** regex `\\cite[a-zA-Z]*\*?(?:\[[^\]]*\])?(?:\[[^\]]*\])?\{([^}]+)\}` on `paper.tex`, then split on commas to handle `\citep{a,b,c}` multi-key form.
- **Bib extraction:** regex `@\w+\s*\{([^,\s]+)\s*,` on `references.bib`.
- **Inline extraction:** regex `\b([A-Z][a-zA-Z\-]+(?:\s+(?:et\s+al\.?|and|&)\s+[A-Z][a-zA-Z\-]+|\s+et\s+al\.?)?)\s*[\(\,]?\s*((?:19|20)\d{2})[a-c]?\s*[\)\.]?` on `paper.md`. Date ranges (e.g. `2001-2023`) and pure numbers were filtered out.
- **Cross-check:** for each (author, year) pair found inline, the auditor tried candidate keys `{author}{year}`, `{author}{year}_data`, `{author}{year}a`, `{author}{year}b` against the cite-key set.
- **No files modified** during this audit.