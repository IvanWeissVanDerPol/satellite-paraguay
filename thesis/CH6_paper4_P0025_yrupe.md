# P0025 Yrupe: Cross-Domain Transfer Learning for Soybean Yield — Honest Failure-Mode

> **Thesis-voice chapter** — this is the unified-thesis summary of
> paper `papers/drafts/p0025_yrupe_yield/paper.md`. The full paper body (≥6,000
> words) is in the paper directory; this chapter is ~800-1000 words.

- **Journal target:** Agricultural Systems
- **Paper source-of-truth:** `papers/drafts/p0025_yrupe_yield/ACTUAL_RESULTS.md`
- **Honest Reporting Notes:** appended at end of paper.md

---

## Thesis-voice abstract

# Abstract

## Yrupe: Soybean Yield Prediction using Sentinel-2 + INBIO

We present Yrupe, a machine-learning-based soybean yield prediction system for the Caaguazú department of Paraguay. Yrupe combines Sentinel-2 time series, Delineate Anything v2 for field boundary delineation, and INBIO yield records. We test whether a deforestation-pretrained encoder transfers to yield prediction. In our pilot (4 scenes, 18 monthly composites, 8 epochs, CPU), the multi-task CNN **did not converge** (F1=0.497, MAE=3.20 t/ha on synthetic labels), and the cross-domain transfer ratio measured 0.082 — far below the 0.74 figure quoted in earlier drafts. The R²>0.80 / 5,000-fields headline was a target, not a measurement, and has been corrected in `ACTUAL_RESULTS.md`. The pipeline, baseline definitions, and a reproducible failure analysis are released so the failure mode (degenerate all-zero output under CPU-only training on synthetic labels) can be addressed before claiming operational yield forecasts.

## Keywords

Earth observation, deep learning, Paraguay, p0025, sentinel-2

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
**Status:** Chapter of the thesis (in journal-preparation as honest failure-mode analysis)
**Target journal:** Agricultural Systems (IF 8.3)

---

## Abstract

We present **Yrupe** (Guaraní for "puddle"), a multi-task
convolutional neural network for soybean yield prediction in
the Eastern Paraguay Pampas that combines multi-temporal
Sentinel-2 imagery with a Chave-2014-derived above-ground biomass
feature stack. The architecture tests the **cross-domain transfer
hypothesis**: that a satellite-based deforestation-detection
encoder (Yvutu, Chapter 3) can be fine-tuned for soybean yield
regression in a data-scarce agricultural application.

The pilot experiment was run on a **synthetic dataset** (4 scenes
× 18 monthly composites × 256×256 pixels) due to lack of real
INBIO yield labels at experiment time. The headline measured
results:

| Task | Target | Measured |
|------|-------:|----------:|
| Soybean-pixel classification F1 | 0.83 | **0.497** |
| AGB regression R² | 0.62 | **undefined** |

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
2. Read `papers/drafts/p0025_yrupe_yield/paper.md` for the full paper body.
3. Read `papers/drafts/p0025_yrupe_yield/ACTUAL_RESULTS.md` for the measured
   numbers (source of truth).
4. Read `papers/drafts/p0025_yrupe_yield/paper.tex` for the LaTeX submission
   to the journal.

---

*Total words in chapter: ~800-1000. Full paper body: ≥6,000 words.*
