# P0035 Tatakua: Air-Quality Forecasting over Paraguay with Satellite-Informed LSTM

> **Snapshot generated 2026-09-08.** The LaTeX chapter at
> [`chapters/p0035_tatakua_ch09.tex`](chapters/p0035_tatakua_ch09.tex) is
> the canonical source for the thesis PDF build. This file is a
> human-readable summary that mirrors the LaTeX chapter's measured
> numbers and structure.

- **Journal target:** Atmospheric Environment
- **LaTeX chapter (canonical):** `thesis/chapters/p0035_tatakua_ch09.tex` (1,112 words)
- **Paper source-of-truth:** `papers/drafts/p0035_tatakua_air_quality/paper.tex`
- **Measured pilot:** `papers/drafts/p0035_tatakua_air_quality/ACTUAL_RESULTS.md`

## Summary (mirrors chapter §1–§5)

This chapter summarises Paper P0035, the air-quality forecasting study that combines OpenAQ ground measurements, TROPOMI satellite-derived aerosol optical depth (AOD), and meteorological covariates in an LSTM for PM₂.₅ forecasting over Paraguay. Tatakua is presented as the most complete measured pilot in the thesis — the only paper with a real trained model (`models/lstm_tatakua/best.pt`) that beats the persistence baseline.

**Measured pilot numbers (OpenAQ 12 stations, 12-month retro, 24-h horizon):**

| Quantity | Measured value | Source |
|---|---|---|
| Mean RMSE | **14.7 µg/m³** | ACTUAL_RESULTS.md / STATUS.md |
| Improvement over persistence | **24%** | ACTUAL_RESULTS.md |
| Architecture | 3-layer LSTM, 64 hidden units | paper.tex |
| Window | 168 hours (7 days) | paper.tex |
| Horizon | 24 hours | paper.tex |
| Trained weights | `models/lstm_tatakua/best.pt` | (only real .pt in repo) |

**Country-scale finding:** Tatakua outperforms persistence by 24% on PM₂.₅ forecasting over 12 OpenAQ stations in Paraguay. The LSTM is correctly implemented and trains stably; the OpenAQ + TROPOMI + ERA5 + Sentinel-5P data fusion is sound.

**Aspirational-vs-measured gap:** Earlier-draft headline values (8.6 µg/m³ RMSE; +2.1 µg/m³ bias; 47% peak-episode improvement) were placeholders, not measurements, and have been removed. The measured 14.7 µg/m³ is the only RMSE claim in the manuscript. A 5-year retrospective (2019–2024) + held-out station validation are the proposed next experiments.

**Keywords:** air quality, PM₂.₅, LSTM, OpenAQ, TROPOMI, AOD, satellite-informed forecasting, Paraguay

**Author:** Iván Weiss Van der Pol (FP-UNA)

**Status:** Chapter of the thesis (in journal-preparation; Atmospheric Environment submission pending multi-year CV + external station validation — Tatakua is the closest paper to submission-ready among the six).
