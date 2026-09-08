# Thesis Index — Markdown Snapshot

This is the human-readable Markdown snapshot of the thesis. Each chapter
also exists as LaTeX in `thesis/MAIN/thesis.tex` for journal-style typesetting.

## Front matter

- [`thesis/THESIS_ABSTRACT.md`](THESIS_ABSTRACT.md) — 1-page abstract
- [`thesis/CH1_introduction.md`](CH1_introduction.md) — Chapter 1: Introduction (5,000 words)
- [`thesis/CH2_methodology.md`](CH2_methodology.md) — Chapter 2: Methodology (8,000 words)

## Core chapters (one per paper)

| Ch | Paper ID | Title | LaTeX (canonical) | Submission target |
|----|----------|-------|-------------------|-------------------|
| 4 | P0011 | Yvutu — Deforestation Detection | [`chapters/04_p0011_yvutu.tex`](chapters/04_p0011_yvutu.tex) | Remote Sensing of Environment |
| 5 | P0010 | Yvyra — Carbon Credit Verification | [`chapters/05_p0010_yvyra.tex`](chapters/05_p0010_yvyra.tex) | Nature Climate Change (Letter) |
| 6 | P0025 | Yrupe — Cross-Domain Transfer | [`chapters/06_p0025_yrupe.tex`](chapters/06_p0025_yrupe.tex) | Agricultural Systems |
| 7 | P0012 | Yvy — Indigenous Land Tenure | [`chapters/07_p0012_yvy.tex`](chapters/07_p0012_yvy.tex) | World Development |
| 8 | P0026 | Kai — Wildlife Detection | [`chapters/08_p0026_kai.tex`](chapters/08_p0026_kai.tex) | Conservation Biology |
| 9 | P0035 | Tatakua — Air Quality Forecasting | [`chapters/09_p0035_tatakua.tex`](chapters/09_p0035_tatakua.tex) | Atmospheric Environment |

The LaTeX `.tex` files under `chapters/` are the canonical source for the
thesis PDF build (compiled via `make thesis-pdf` → `pdflatex thesis/main.tex`).
The Markdown `.md` files (`CH3_paper1_P0011_yvutu.md` etc.) are
human-readable snapshots that mirror the measured numbers from the
LaTeX chapters, ACTUAL_RESULTS.md, and paper.tex.

- [`CH3_paper1_P0011_yvutu.md`](CH3_paper1_P0011_yvutu.md) ←→ [`chapters/04_p0011_yvutu.tex`](chapters/04_p0011_yvutu.tex)
- [`CH4_paper2_P0010_yvyra.md`](CH4_paper2_P0010_yvyra.md) ←→ [`chapters/05_p0010_yvyra.tex`](chapters/05_p0010_yvyra.tex)
- [`CH5_paper3_P0012_yvy.md`](CH5_paper3_P0012_yvy.md) ←→ [`chapters/07_p0012_yvy.tex`](chapters/07_p0012_yvy.tex)
- [`CH6_paper4_P0025_yrupe.md`](CH6_paper4_P0025_yrupe.md) ←→ [`chapters/06_p0025_yrupe.tex`](chapters/06_p0025_yrupe.tex)
- [`CH7_paper5_P0026_kai.md`](CH7_paper5_P0026_kai.md) ←→ [`chapters/08_p0026_kai.tex`](chapters/08_p0026_kai.tex)
- [`CH8_paper6_P0035_tatakua.md`](CH8_paper6_P0035_tatakua.md) ←→ [`chapters/09_p0035_tatakua.tex`](chapters/09_p0035_tatakua.tex)

## Closing chapters

- [`thesis/CH9_cross-cutting.md`](CH9_cross-cutting.md) — Cross-cutting analysis (3,500 words)
- [`thesis/CH10_discussion.md`](CH10_discussion.md) — Discussion (5,000 words)
- [`thesis/CH11_conclusion.md`](CH11_conclusion.md) — Conclusion (2,500 words)

## Appendices

- [`thesis/references.bib`](references.bib) — 120-entry bibliography
- [`thesis/MAIN/thesis.tex`](MAIN/thesis.tex) — Unified LaTeX render of all 11 chapters
- [`thesis/main.tex`](main.tex) — Alternative lightweight LaTeX scaffold (350 lines)
- [`thesis/preamble.tex`](preamble.tex) — LaTeX preamble (shared with `MAIN/`)

## Submission papers (LaTeX)

- [`../papers/drafts/p0011_yvutu_deforestation/paper.tex`](../papers/drafts/p0011_yvutu_deforestation/paper.tex)
- [`../papers/drafts/p0010_yvyra_carbon_credits/paper.tex`](../papers/drafts/p0010_yvyra_carbon_credits/paper.tex)
- [`../papers/drafts/p0012_yvy_indigenous/paper.tex`](../papers/drafts/p0012_yvy_indigenous/paper.tex)
- [`../papers/drafts/p0025_yrupe_yield/paper.tex`](../papers/drafts/p0025_yrupe_yield/paper.tex)
- [`../papers/drafts/p0026_kai_poaching/paper.tex`](../papers/drafts/p0026_kai_poaching/paper.tex)
- [`../papers/drafts/p0035_tatakua_air_quality/paper.tex`](../papers/drafts/p0035_tatakua_air_quality/paper.tex)

## Honest reporting documents (per paper)

Each paper has `ACTUAL_RESULTS.md` documenting measured vs. claimed metrics:
- [`../papers/drafts/p0011_yvutu_deforestation/ACTUAL_RESULTS.md`](../papers/drafts/p0011_yvutu_deforestation/ACTUAL_RESULTS.md)
- [`../papers/drafts/p0010_yvyra_carbon_credits/ACTUAL_RESULTS.md`](../papers/drafts/p0010_yvyra_carbon_credits/ACTUAL_RESULTS.md)
- [`../papers/drafts/p0012_yvy_indigenous/ACTUAL_RESULTS.md`](../papers/drafts/p0012_yvy_indigenous/ACTUAL_RESULTS.md)
- [`../papers/drafts/p0025_yrupe_yield/ACTUAL_RESULTS.md`](../papers/drafts/p0025_yrupe_yield/ACTUAL_RESULTS.md)
- [`../papers/drafts/p0026_kai_poaching/ACTUAL_RESULTS.md`](../papers/drafts/p0026_kai_poaching/ACTUAL_RESULTS.md)
- [`../papers/drafts/p0035_tatakua_air_quality/ACTUAL_RESULTS.md`](../papers/drafts/p0035_tatakua_air_quality/ACTUAL_RESULTS.md)

## Compilation

To produce a PDF of the thesis, use either:
- **Unified version:** `cd thesis/MAIN && latexmk -pdf thesis.tex`
- **Markdown first:** Use the above links, then paste into your typist

The Markdown snapshot is the human-readable form; the LaTeX is for
camera-ready submission to UNA FADA.

## Related

- [`../SUBMISSION_PLAN.md`](../SUBMISSION_PLAN.md) — Six-paper submission schedule
- [`../PAPER_SUBMISSION_TRACKER.md`](../PAPER_SUBMISSION_TRACKER.md) — (when created) Per-paper submission state
- [`../GAP_AUDIT_2026-08-04.md`](../GAP_AUDIT_2026-08-04.md) — Gap analysis as of 2026-08-04
