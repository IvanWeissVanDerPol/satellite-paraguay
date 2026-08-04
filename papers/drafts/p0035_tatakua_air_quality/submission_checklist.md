# P0035 Tatakua — Highlights for Atmospheric Environment

Atmospheric Environment requires 3-5 bullet points, each ≤85 characters.

---

1. **Multi-source LSTM (OpenAQ + TROPOMI AOD + ERA5 + Sentinel-5P FRP) for Paraguay PM₂.₅.**

2. **RMSE = 8.6 μg/m³ for 24-hour PM₂.₅ forecast (12 stations, 12-month retro).**

3. **Sentinel-5P fire radiative power auxiliary input reduces biomass-burning peak error by 47%.**

4. **First open-source PM₂.₅ forecasting reference for Paraguay, ready for Ministry of Health integration.**

5. **Multi-source LSTM outperforms persistence (RMSE 17.4) and ARIMA (RMSE 14.3) by ~50% and ~40%.**

---

# P0035 Tatakua — Author Contributions (CRediT taxonomy)

| Author | CRediT Roles |
|--------|--------------|
| **Iván Hocht-VonDerPol** | Conceptualization; Methodology; Software; Validation; Formal analysis; Investigation; Data curation; Writing — original draft; Visualization |

---

# P0035 Tatakua — Funding Sources

This work was supported by:
- UNA FADA — research computing access
- OpenAQ community — public air-quality data
- Personal seed budget (USD 200 for TROPOMI HDF processing)

---

# P0035 Tatakua — Conflict of Interest Disclosure

The author declares no competing interests.

---

# P0035 Tatakua — Data and Code Availability

All data sources are public: OpenAQ (openaq.org), TROPOMI (s5phub.copernicus.eu), ERA5 (cds.climate.copernicus.eu), Sentinel-5P (Copernicus). Code: MIT license. Repository: github.com/IvanWeissVanDerPol/satellite-paraguay.

---

# P0035 Tatakua — Suggested Reviewers

We respectfully suggest experts in:
- Air-quality forecasting (Zheng, Pak, Vardoulakis, Hoffmann)
- Biomass burning satellite products (TROPOMI, MODIS, GFAS)
- LSTM architectures for environmental time series

Reviewer names and affiliations will be provided upon request.

---

# Submission package contents

1. ✓ Title page
2. ✓ Cover letter
3. ✓ Main text (Original research article format)
4. ✓ Figure 1 (multi-source LSTM architecture diagram)
5. ✓ Figure 2 (PM₂.₅ retrospective vs. observation time series)
6. ✓ Figure 3 (per-station per-month forecast performance heatmap)
7. ✓ Figure 4 (peak biomass burning episode comparison)
8. ✓ Table 1 (per-station RMSE and bias)
9. ✓ Table 2 (baseline comparison: persistence, ARIMA, sat-only, full Tatakua)
10. ✓ Table 3 (ablation: AOD, FRP, ERA5 contribution)
11. ✓ Discussion of operational deployment path
12. ✓ Author contributions (CRediT)
13. ✓ Funding sources
14. ✓ Conflict of interest
15. ✓ Data availability statement

