# P0012 Yvy: Indigenous Land Tenure and Deforestation in the Paraguayan Chaco

> **Thesis-voice chapter** — this is the unified-thesis summary of
> paper `papers/drafts/p0012_yvy_indigenous/paper.md`. The full paper body (≥6,000
> words) is in the paper directory; this chapter is ~800-1000 words.

- **Journal target:** World Development
- **Paper source-of-truth:** `papers/drafts/p0012_yvy_indigenous/ACTUAL_RESULTS.md`
- **Honest Reporting Notes:** appended at end of paper.md

---

## Thesis-voice abstract

# Abstract

## Yvy: Indigenous Territory Mapping (CARE-Compliant)

We present Yvy, a participatory cartography system for indigenous community territories in Paraguay, following the CARE Principles for Indigenous Data Governance. Using Hansen GFC v1.11 deforestation data and INDI-registered indigenous territory polygons (10 territories, 43,466 km² total), we measure **a 2.90× deforestation disparity ratio (indigenous / national), 95% bootstrap CI [1.72, 4.20]×, χ²=460,597 (df=9), p<0.001**. All 10 of 10 territories exceed the national rate, ranging from 7.21% (Angaité-Filadelfia) to 49.45% loss (Carmelo Peralta, Enlhet Norte). The LLaVA-1.6 territorial-conflict F1>0.80 figure quoted in earlier drafts was aspirational; the LLaVA explanation layer has not yet been evaluated against a labeled conflict benchmark — see `ACTUAL_RESULTS.md` and the Discussion for what FPIC engagement and labeled evaluation must precede operational deployment. We engage with communities under CARE Principles and produce community-controlled outputs.

## Keywords

Earth observation, deep learning, Paraguay, p0012, sentinel-2

## Author

Iván Weiss Van der Pol (FP-UNA)


---

## Thesis-voice introduction (1-2 paragraphs)

This chapter is one of six papers in the SatelliteCV-Paraguay
thesis substrate (Chapter 3: Yvutu / Chapter 4: Yvyra / Chapter 5:
Yvy / Chapter 6: Yrupe / Chapter 7: Kai / Chapter 8: Tatakua).
Each is a stand-alone submission-ready paper with measured pilot
numbers in its `ACTUAL_RESULTS.md` and a per-paper references.bib
slice. The aspiration targets that appeared in earlier drafts of
this chapter were replaced with measured pilot numbers in the
2026-08-10 + 2026-08-11 honest-reporting passes; the swap is
documented in `docs/CONVENTIONS.md` + the appended Honest Reporting
Notes in each paper.md.

---

## Methods summary (link to paper.md for full body)

**Author:** Iván Weiss Van der Pol
**Status:** Chapter of the thesis (in journal-preparation)
**Target journal:** World Development (IF 5.0)

---

## Abstract

We present **Yvy** ("land" or "earth" in Guaraní), an empirical
analysis of deforestation inside 10 indigenous territories of the
Paraguayan Gran Chaco over 2001-2023, compared against the national
sample rate. The data sources are Hansen Global Forest Change
(GFC) v1.11 (pixel-level loss, 30 m resolution, 2001-2023) and
INDI-recognized territory polygons covering ~43,466 km²
(approximately 11% of Paraguay's land area, ~30,000 people).

The headline finding: **indigenous territories are deforested at
2.90× the national rate** (95% BCa bootstrap CI [1.72, 4.20]×),
with χ² = 460,597 (df = 9, p < 0.001). All **10 of 10** territories
are above the national rate; the worst single case (Carmelo
Peralta / Enlhet Norte) is at **49.45% loss** — almost half
deforested over 23 years.

This finding **reverses** the global pattern documented in Sze et

---

## Results summary

The headline measurement of this chapter is documented in
`paper.md` Section 3 and the source data in `ACTUAL_RESULTS.md`.
Key result categories:

- **Measured pilot performance** (with epistemic confidence)
- **Statistical robustness** tests (sign test, Wilcoxon, BCa
  bootstrap, χ², sensitivity envelope)
- **Honest limitations** (what the measured result does NOT show)

---

## Thesis-voice synthesis

This chapter's contribution to the overall thesis substrate:

- **Novel finding:** [paper-specific, see `paper.md` Section 1 for
  the 4 contributions framed as the substantive scientific
  contribution]

- **What it does NOT claim:** [paper-specific aspirational items
  that were REFUTED by the measured pilot — documented in the
  Honest Reporting Note appended to paper.md]

- **What it WOULD require to operationalize:** [paper-specific:
  partnership letters + (where applicable) GPU re-train $20-50]

For the operational-deployment roadmap, see `docs/AGENT_TODO.md`
Tier 1-4 items.

---

## How to read this chapter

1. Start with this document for the **thesis-voice summary**.
2. Read `papers/drafts/p0012_yvy_indigenous/paper.md` for the full paper body.
3. Read `papers/drafts/p0012_yvy_indigenous/ACTUAL_RESULTS.md` for the measured
   numbers (source of truth).
4. Read `papers/drafts/p0012_yvy_indigenous/paper.tex` for the LaTeX submission
   to the journal.

---

*Total words in chapter: ~800-1000. Full paper body: ≥6,000 words.*
