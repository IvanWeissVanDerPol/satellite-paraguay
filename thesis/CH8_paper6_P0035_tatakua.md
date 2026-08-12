# Chapter 8: Paper 6 — Tatakua (P0035 Air Quality)

> **Thesis chapter** — accompanies the standalone paper submission.
> - **Paper slug:** `p0035`
> - **Full paper body:** `papers/drafts/p0035_tatakua_air_quality/paper.md` (≥ 6,000 words)
> - **LaTeX for journal:** `papers/drafts/p0035_tatakua_air_quality/paper.tex`
> - **Source-of-truth numbers:** `papers/drafts/p0035_tatakua_air_quality/ACTUAL_RESULTS.md`
> - **Honest reporting notes:** appended at end of `paper.md`

This chapter is the thesis-voice summary of the paper. For the
full Methods / Results / Discussion / Conclusion, read `paper.md`
in the paper directory.

---

## Abstract

# Abstract

## Tatakua: Air Quality Forecasting for Asunción

We present Tatakua, a deep-learning-based air-quality forecasting system for Paraguay. Tatakua uses OpenAQ PM₂.₅ hourly measurements (12 stations, 2019-2025), TROPOMI AOD, and an LSTM (3 layers × 64 hidden units) with a 168-hour window to forecast PM₂.₅ 24 hours ahead. **Mean RMSE across stations is 14.7 µg/m³ with bias +3.4**, a 24% improvement over persistence (19.2 µg/m³) — meaningful but 70% above the 8.6 µg/m³ target quoted in earlier drafts. Performance varies sharply by station: Asunción 8.2 µg/m³, Filadelfia (Chaco) 18.6 µg/m³. The Ministry-of-Health deployment claim quoted in earlier drafts was aspirational; deployment depends on resolving the rural-station gap. The peak-biomass-burning episode (Sep 2025) showed a 32% RMSE reduction vs satellite-only baseline — substantially below the 47% claim — see `ACTUAL_RESULTS.md` for measured values.

## Keywords

Earth observation, deep learning, Paraguay, p0035, sentinel-2

## Author

Iván Weiss Van der Pol (FP-UNA)


---

## Thesis-voice summary

This paper makes substantive contributions within the thesis
substrate as Paper H: the work on the p0035 problem
is what the thesis claims as its [specific contribution]. The full
experimental detail is in `paper.md`; the honest interpretations of
measured-vs-aspirational numbers are in `ACTUAL_RESULTS.md`.

### What this chapter contributes to the thesis

The contribution is documented in detail in `paper.md` Section 6
(Conclusion). For the thesis voice, the headline is:

- **p0035 is now publishable** as a methodology + measured-results
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
