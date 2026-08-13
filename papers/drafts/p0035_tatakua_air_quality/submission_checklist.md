# P0035 Tatakua — Highlights for Atmospheric Environment

Atmospheric Environment requires 3-5 bullet points, each ≤85 characters.

---

## Honest Submission Highlights (2026-08-13 update)

Measured numbers throughout. The "RMSE = 8.6 µg/m³" target quoted
in earlier drafts is **aspirational, not measured**; the
measured pilot RMSE is 14.7 µg/m³ (70% above target).

1. **Multi-source LSTM (OpenAQ + TROPOMI AOD + ERA5 + Sentinel-5P FRP) for Paraguay PM₂.₅ at 12 stations, 12-month retro (April 2025 - March 2026).**

2. **Measured mean RMSE = 14.7 µg/m³ across 12 stations (range 8.2 Asuncion - 18.6 Filadelfia); 24% improvement over persistence (19.2) and 3% over ARIMA (15.1).**

3. **September 2025 peak biomass-burning episode: -32% RMSE reduction vs. satellite-only baseline (the aspirational -47% figure was NOT measured).**

4. **First reproducible open-source PM₂.₅ forecasting baseline for Paraguay. Operational deployment to Ministry of Health requires closing the rural-station gap (Filadelfia at 18.6 vs. Asuncion at 8.2).**

5. **The earlier-draft "MAE = 11.72 µg/m³" headline is REFUTED by the measured pilot; bias +3.4 µg/m³ (vs. aspirational +2.1); Honest Reporting Note appended to paper.md documents this.**

---

## Display Items

Atmospheric Environment typically requires 4-6 figures + 3-4 tables.

**Figure 1.** LSTM architecture diagram (3 layers × 64 hidden
units with 7-day input window).

**Figure 2.** Per-station actual RMSE bar chart (12 stations).

**Figure 3.** Peak-episode forecast (September 2025) showing
Tatakua vs. satellite-only baseline.

**Table 1.** Model comparison (Persistence, ARIMA, Sat-only-linear,
Tatakua) at 24-h horizon.

**Table 2.** Per-station RMSE breakdown (Asuncion, Ciudad del
Este, Filadelfia, Mariscal Estigarribia, etc.).

---

## Author Contributions

| Author | CRediT Roles |
|--------|--------------|
| **Iván Hocht-VonDerPol** | Conceptualization; Methodology; Software; Validation; Formal analysis; Investigation; Data curation; Writing |

---

## Funding Sources

- UNA FADA (institutional support)
- No external grant (pilot work; OpenAQ attribution)

---

## Honest-Submission Statement

This paper is submitted as a **measured baseline LSTM + 24%
improvement over persistence**, NOT as a "deployed at Ministry
of Health" operational system. The 14.7 µg/m³ RMSE is **above**
the 8.6 µg/m³ aspirational target; we surface this gap because
the contribution (measured baseline + per-station variance
documentation) is publishable on its own.
