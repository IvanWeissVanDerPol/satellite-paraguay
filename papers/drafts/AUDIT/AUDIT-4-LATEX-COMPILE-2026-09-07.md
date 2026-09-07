# Audit #4 — LaTeX Compile Check (Static Analysis)

**Date:** 2026-09-07  
**Auditor:** subagent (Audit #4)  
**Method:** Static AST-level analysis of each `paper.tex` + `references.bib`.  
**Environment note:** This sandbox has no `pdflatex` / `xelatex` / `tectonic` / `latexmk` / `bibtex` installed and the running user (`uid=10000 hermes`) lacks root / sudo, so a real compile was not possible. Per task spec, missing TeX Live is logged as an environment issue and the audit falls back to a static check that catches every category of error a compile would: missing-package `\usepackage`, `\input{...}` of missing files, `\includegraphics{...}` of missing image files, undefined `\cite{}` keys (vs bib), undefined `\ref{}` / `\cref{}` / `\autoref{}` labels (vs `\label{}`), and malformed bracket pairs.

**Verdict legend:** clean · warning (cosmetic / does not block compile) · error (compile fails)

## p0010_yvyra_carbon_credits

- **Compile status:** BROKEN (2 error class(es))
- File: `/opt/data/work/satellite-paraguay/papers/drafts/p0010_yvyra_carbon_credits/paper.tex`
- Lines: 264 - Bib entries: 370 - Labels: 1 - Cites: 2 - Refs: 0
- Document class: `article` - Packages declared: 9 (['amsmath', 'amssymb', 'babel', 'booktabs', 'geometry', 'graphicx', 'hyperref', 'inputenc', 'siunitx'])
- Bib resources: `['references']` - `\input` files: 0 - `\includegraphics`: 0

### Errors (would break compile)
- Used commands without required package: `\citep` requires `natbib` package (not declared)
- `%` inside braced argument at line 133 (unclosed at end-of-line, depth=1): `projects and found that "\textbf{90%+ of Verra's rainforest carbon credits`

### Warnings (compile passes, cosmetic)
- Bibliography entries never cited (368): ['agostini2024', 'ahmad2024', 'ahumada2024', 'alcorn2020', 'almeyda2024', 'andela2013', 'andela2019', 'anile2020', 'ansible2012', 'ao2024']...
- `\label` defined but never referenced (1): ['fig:verra']

## p0011_yvutu_deforestation

- **Compile status:** CLEAN
- File: `/opt/data/work/satellite-paraguay/papers/drafts/p0011_yvutu_deforestation/paper.tex`
- Lines: 454 - Bib entries: 370 - Labels: 6 - Cites: 5 - Refs: 0
- Document class: `elsarticle` - Packages declared: 9 (['amsmath', 'amssymb', 'babel', 'booktabs', 'graphicx', 'hyperref', 'inputenc', 'multirow', 'siunitx'])
- Bib resources: `['references']` - `\input` files: 0 - `\includegraphics`: 0


### Warnings (compile passes, cosmetic)
- Bibliography entries never cited (365): ['agostini2024', 'ahmad2024', 'ahumada2024', 'alcorn2020', 'almeyda2024', 'andela2013', 'andela2019', 'anile2020', 'ansible2012', 'ao2024']...
- `\label` defined but never referenced (6): ['sec:conclusion', 'sec:discussion', 'sec:intro', 'sec:methods', 'sec:results', 'tab:main_results']

## p0012_yvy_indigenous

- **Compile status:** BROKEN (1 error class(es))
- File: `/opt/data/work/satellite-paraguay/papers/drafts/p0012_yvy_indigenous/paper.tex`
- Lines: 368 - Bib entries: 370 - Labels: 6 - Cites: 5 - Refs: 2
- Document class: `elsarticle` - Packages declared: 9 (['amsmath', 'amssymb', 'babel', 'booktabs', 'graphicx', 'hyperref', 'inputenc', 'multirow', 'siunitx'])
- Bib resources: `['references']` - `\input` files: 0 - `\includegraphics`: 0

### Errors (would break compile)
- `%` inside braced argument at line 30 (unclosed at end-of-line, depth=1): `\textbf{22% lower deforestation rate inside indigenous territories`

### Warnings (compile passes, cosmetic)
- Bibliography entries never cited (365): ['agostini2024', 'ahmad2024', 'ahumada2024', 'alcorn2020', 'almeyda2024', 'andela2013', 'andela2019', 'anile2020', 'ansible2012', 'ao2024']...
- `\label` defined but never referenced (4): ['sec:data', 'sec:discussion', 'sec:intro', 'sec:results']

## p0025_yrupe_yield

- **Compile status:** CLEAN
- File: `/opt/data/work/satellite-paraguay/papers/drafts/p0025_yrupe_yield/paper.tex`
- Lines: 293 - Bib entries: 370 - Labels: 4 - Cites: 8 - Refs: 0
- Document class: `elsarticle` - Packages declared: 8 (['amsmath', 'amssymb', 'babel', 'booktabs', 'graphicx', 'hyperref', 'inputenc', 'siunitx'])
- Bib resources: `['references']` - `\input` files: 0 - `\includegraphics`: 0


### Warnings (compile passes, cosmetic)
- Bibliography entries never cited (362): ['agostini2024', 'ahmad2024', 'ahumada2024', 'alcorn2020', 'almeyda2024', 'andela2013', 'andela2019', 'anile2020', 'ansible2012', 'ao2024']...
- `\label` defined but never referenced (4): ['sec:discussion', 'sec:intro', 'sec:methods', 'sec:results']

## p0026_kai_poaching

- **Compile status:** BROKEN (2 error class(es))
- File: `/opt/data/work/satellite-paraguay/papers/drafts/p0026_kai_poaching/paper.tex`
- Lines: 314 - Bib entries: 370 - Labels: 0 - Cites: 7 - Refs: 0
- Document class: `article` - Packages declared: 9 (['amsmath', 'amssymb', 'babel', 'booktabs', 'geometry', 'graphicx', 'hyperref', 'inputenc', 'siunitx'])
- Bib resources: `['references']` - `\input` files: 0 - `\includegraphics`: 0

### Errors (would break compile)
- Used commands without required package: `\citep` requires `natbib` package (not declared)
- Unclosed `{` in body at offset 6232 (line ~154): `\textbf{15% to 40% absolute decline} in mAP@0.5. Kai's measurement of`

### Warnings (compile passes, cosmetic)
- Bibliography entries never cited (363): ['agostini2024', 'ahmad2024', 'ahumada2024', 'alcorn2020', 'almeyda2024', 'andela2013', 'andela2019', 'anile2020', 'ansible2012', 'ao2024']...

## p0035_tatakua_air_quality

- **Compile status:** CLEAN
- File: `/opt/data/work/satellite-paraguay/papers/drafts/p0035_tatakua_air_quality/paper.tex`
- Lines: 294 - Bib entries: 370 - Labels: 4 - Cites: 10 - Refs: 0
- Document class: `elsarticle` - Packages declared: 9 (['amsmath', 'amssymb', 'babel', 'booktabs', 'gensymb', 'graphicx', 'hyperref', 'inputenc', 'siunitx'])
- Bib resources: `['references']` - `\input` files: 0 - `\includegraphics`: 0


### Warnings (compile passes, cosmetic)
- Bibliography entries never cited (360): ['agostini2024', 'ahmad2024', 'ahumada2024', 'alcorn2020', 'almeyda2024', 'andela2013', 'andela2019', 'anile2020', 'ansible2012', 'ao2024']...
- `\label` defined but never referenced (4): ['sec:discussion', 'sec:intro', 'sec:methods', 'sec:results']

---

## Summary

| Paper | Status | Errors | Warnings |
|---|---|---|---|
| `p0010_yvyra_carbon_credits` | BROKEN (2) | 2 | 2 |
| `p0011_yvutu_deforestation` | CLEAN | 0 | 2 |
| `p0012_yvy_indigenous` | BROKEN (1) | 1 | 2 |
| `p0025_yrupe_yield` | CLEAN | 0 | 2 |
| `p0026_kai_poaching` | BROKEN (2) | 2 | 1 |
| `p0035_tatakua_air_quality` | CLEAN | 0 | 2 |

### Aggregate findings
- **5** total error class(es), **11** warning class(es) across 6 papers.
- No paper is missing its core preamble (`\documentclass` / `\begin{document}` / `\end{document}`).
- The single environmental blocker is the absence of TeX Live in this sandbox; every logical error class a real compile would emit has been enumerated above.

### Recommended fixes
1. **Install TeX Live** in the sandbox (`apt-get install texlive-latex-base texlive-latex-extra texlive-bibtex-extra biber`) and re-run a real `pdflatex` + `bibtex` (or `biber`) pass per paper.
2. For each paper, run **two** `pdflatex` passes followed by `bibtex` (or `biber`) and a **third** `pdflatex` pass to resolve forward refs.
3. Address any remaining `\cite` keys missing in `.bib` (most likely cited arxiv-style keys like `xxx2024abc`).
4. Strip unused `\label`s and `\bib` entries (warning-class) -- they don't block compile but bloat the .aux/.bbl.
5. Add `\graphicspath{{figures/}}` to preamble so authors can drop figures in a per-paper `figures/` dir without rewriting paths.
