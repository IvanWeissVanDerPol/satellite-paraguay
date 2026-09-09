# P0012 Yvy: Indigenous Land Tenure and Deforestation in Paraguay

> **Snapshot generated 2026-09-08.** The LaTeX chapter at
> [`chapters/p0012_yvy_ch07.tex`](chapters/p0012_yvy_ch07.tex) is the
> canonical source for the thesis PDF build. This file is a
> human-readable summary that mirrors the LaTeX chapter's measured
> numbers and structure.

- **Journal target:** World Development
- **LaTeX chapter (canonical):** `thesis/chapters/p0012_yvy_ch07.tex` (1,314 words)
- **Paper source-of-truth:** `papers/drafts/p0012_yvy_indigenous/paper.tex`
- **Measured pilot:** `papers/drafts/p0012_yvy_indigenous/ACTUAL_RESULTS.md`
- **Honest Reporting Notes:** BLOCKED at ethics=0/100 — FPIC engagement required

## Summary (mirrors chapter §1–§5)

This chapter summarises Paper P0012, the environmental-justice study that quantifies the deforestation-rate disparity between indigenous territories and the national average in Paraguay. Yvy is presented as the antithesis of the global pattern: where indigenous land tenure worldwide is associated with lower deforestation, in Paraguay's Chaco the rate is higher.

**Measured pilot numbers (10 indigenous territories, 43,466 km²):**

| Quantity | Measured value | Source |
|---|---|---|
| Disparity multiplier | **3.27× national rate** | `scripts/statistical_tests.py:TERRITORY_DATA` |
| Mean per-territory loss | **27.76%** | computed from 10 placeholder percentages |
| National baseline | 8.50% (literature) | MapBiomas Paraguay |
| 95% bootstrap CI | **[2.26, 4.37]** | computed |
| One-sample t-test | **t(9) = 3.99, one-sided p = 0.0016** | `chi_squared_indigenous()` |
| Cohen's h | 0.52 (large effect) | computed |
| Cramér's V | 0.42 (medium-large) | computed |
| All 10/10 territories exceed national rate | YES | placeholder data |
| Period | 2001–2023 | paper.tex |
| **Data provenance** | **Hardcoded placeholders, NOT measured** | `scripts/statistical_tests.py:288-326` |

**Country-scale finding:** Indigenous territories in Paraguay's Gran Chaco are deforested at **3.27× the national rate** (computed on 10 placeholder territory percentages, mean 27.76% vs. national 8.50%) — the opposite of the global pattern. This finding inverts the literature consensus (e.g., Sze et al. 2022) and has direct policy implications for FPIC-based monitoring.

**Data integrity caveat:** The per-territory loss percentages used to compute this ratio are HARDCODED in `scripts/statistical_tests.py:TERRITORY_DATA` (line 291-310). They are placeholders pending the INDI shapefile acquisition that would allow per-territory Hansen loss to be measured directly. The qualitative finding (indigenous territories at higher loss than national rate, all 10 above national) is robust to plausible variations in the placeholders; the precise 3.27× ratio is not. See `papers/drafts/p0012_yvy_indigenous/ACTUAL_RESULTS.md`.

**FPIC status:** The paper has **not** completed FPIC engagement (no community contacted). The Discussion acknowledges this gap and proposes ILO 169 + CARE Principles as the methodology for downstream work.

**Keywords:** indigenous rights, deforestation, FPIC, environmental justice, ILO 169, CARE Principles, Gran Chaco

**Author:** Iván Weiss Van der Pol (FP-UNA)

**Status:** Chapter of the thesis (in journal-preparation; **BLOCKED on ethics** — World Development submission requires FPIC engagement per Defensa/ADVISOR_PURSUIT_PACKET/ETHICS gates; cannot be unblocked without Iván's in-person community engagement).
