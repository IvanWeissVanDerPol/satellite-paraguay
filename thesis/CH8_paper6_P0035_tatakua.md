# P0035 Tatakua: PM₂.₅ Forecasting in Paraguay via Multi-Source LSTM

> **Thesis-voice chapter** — this is the unified-thesis summary of
> paper `papers/drafts/p0035_tatakua_air_quality/paper.md`. The full paper body (≥6,000
> words) is in the paper directory; this chapter is ~800-1000 words.

- **Journal target:** Atmospheric Environment
- **Paper source-of-truth:** `papers/drafts/p0035_tatakua_air_quality/ACTUAL_RESULTS.md`
- **Honest Reporting Notes:** appended at end of paper.md

---

## Thesis-voice abstract

# Abstract

## Tatakua: Air Quality Forecasting for Asunción

We present Tatakua, a deep-learning-based air-quality forecasting system for Paraguay. Tatakua uses OpenAQ PM₂.₅ hourly measurements (12 stations, 2019-2025), TROPOMI AOD, and an LSTM (3 layers × 64 hidden units) with a 168-hour window to forecast PM₂.₅ 24 hours ahead. **Mean RMSE across stations is 14.7 µg/m³ with bias +3.4**, a 24% improvement over persistence (19.2 µg/m³) — meaningful but 70% above the 8.6 µg/m³ target quoted in earlier drafts. Performance varies sharply by station: Asunción 8.2 µg/m³, Filadelfia (Chaco) 18.6 µg/m³. The Ministry-of-Health deployment claim quoted in earlier drafts was aspirational; deployment depends on resolving the rural-station gap. The peak-biomass-burning episode (Sep 2025) showed a 32% RMSE reduction vs satellite-only baseline — substantially below the 47% claim — see `ACTUAL_RESULTS.md` for measured values.

## Keywords

Earth observation, deep learning, Paraguay, p0035, sentinel-2

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

**Author:** Iván Hocht-VonDerPol
**Status:** Chapter of the thesis (in journal-preparation)
**Target journal:** Atmospheric Environment

---

## Abstract

Air quality monitoring in Paraguay is limited by sparse ground stations. We present LSTM-based air quality forecasting using OpenAQ PM2.5 data and Sentinel-5P aerosol optical depth (AOD) as a complement. We compare LSTM-2layer, LSTM-4layer, and persistence baselines. The measured pilot performance is **mean RMSE = 14.7 µg/m³ across 12 OpenAQ stations** (24% above persistence), with bias +3.4 µg/m³. The LSTM DOES beat persistence by 24% in our pilot. The published target "MAE<5 µg/m³ (R²>0.80)" was aspirational, NOT measured; the Honest Reporting Note appended to this paper documents this.

## 8.1 Introduction

Air quality is a public health concern, especially in urban areas (Asunción, Ciudad del Este). OpenAQ aggregates measurements from government and research stations, but the station network in Paraguay is sparse (< 10 active stations).

LSTM (Long Short-Term Memory) networks are state-of-the-art for time-series forecasting. We test whether LSTM can forecast PM2.5 in Paraguay using OpenAQ + Sentinel-5P data.

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
2. Read `papers/drafts/p0035_tatakua_air_quality/paper.md` for the full paper body.
3. Read `papers/drafts/p0035_tatakua_air_quality/ACTUAL_RESULTS.md` for the measured
   numbers (source of truth).
4. Read `papers/drafts/p0035_tatakua_air_quality/paper.tex` for the LaTeX submission
   to the journal.

---

*Total words in chapter: ~800-1000. Full paper body: ≥6,000 words.*
