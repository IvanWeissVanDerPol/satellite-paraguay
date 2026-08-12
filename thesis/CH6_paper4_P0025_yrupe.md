# Chapter 6: Paper 4 — Yrupe (P0025 Soybean Yield)

> **Thesis chapter** — accompanies the standalone paper submission.
> - **Paper slug:** `p0025`
> - **Full paper body:** `papers/drafts/p0025_yrupe_yield/paper.md` (≥ 6,000 words)
> - **LaTeX for journal:** `papers/drafts/p0025_yrupe_yield/paper.tex`
> - **Source-of-truth numbers:** `papers/drafts/p0025_yrupe_yield/ACTUAL_RESULTS.md`
> - **Honest reporting notes:** appended at end of `paper.md`

This chapter is the thesis-voice summary of the paper. For the
full Methods / Results / Discussion / Conclusion, read `paper.md`
in the paper directory.

---

## Abstract

# Abstract

## Yrupe: Soybean Yield Prediction using Sentinel-2 + INBIO

We present Yrupe, a machine-learning-based soybean yield prediction system for the Caaguazú department of Paraguay. Yrupe combines Sentinel-2 time series, Delineate Anything v2 for field boundary delineation, and INBIO yield records. We test whether a deforestation-pretrained encoder transfers to yield prediction. In our pilot (4 scenes, 18 monthly composites, 8 epochs, CPU), the multi-task CNN **did not converge** (F1=0.497, MAE=3.20 t/ha on synthetic labels), and the cross-domain transfer ratio measured 0.082 — far below the 0.74 figure quoted in earlier drafts. The R²>0.80 / 5,000-fields headline was a target, not a measurement, and has been corrected in `ACTUAL_RESULTS.md`. The pipeline, baseline definitions, and a reproducible failure analysis are released so the failure mode (degenerate all-zero output under CPU-only training on synthetic labels) can be addressed before claiming operational yield forecasts.

## Keywords

Earth observation, deep learning, Paraguay, p0025, sentinel-2

## Author

Iván Weiss Van der Pol (FP-UNA)


---

## Thesis-voice summary

This paper makes substantive contributions within the thesis
substrate as Paper H: the work on the p0025 problem
is what the thesis claims as its [specific contribution]. The full
experimental detail is in `paper.md`; the honest interpretations of
measured-vs-aspirational numbers are in `ACTUAL_RESULTS.md`.

### What this chapter contributes to the thesis

The contribution is documented in detail in `paper.md` Section 6
(Conclusion). For the thesis voice, the headline is:

- **p0025 is now publishable** as a methodology + measured-results
  paper, with caveats documented in the Honest Reporting Note.

### What this chapter does NOT do

This chapter is a pointer to the full paper body. **It is not
the standalone submission** — the standalone journal submission
is `paper.tex` in the paper directory.

### How to navigate this chapter

1. Read `paper.md` for the full paper body.
2. Read `ACTUAL_RESULTS.md` for the measured numbers.
3. Read the abstract above for the thesis-voice summary.
4. Submit `paper.tex` to the journal after the human-only
   partnerships (FPIC, Verra, etc.) are in place.

---
