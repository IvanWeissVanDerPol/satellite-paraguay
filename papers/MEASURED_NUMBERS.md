# MEASURED_NUMBERS.md — Canonical reference for prose claims

> **Last updated:** 2026-09-16 (Tier-2 polish prose-sync pass)
> **Authoritative source:** each paper's `ACTUAL_RESULTS.md` + `STATUS.md`
> **Purpose:** single source of truth for what the thesis measured, so
> no prose file can drift back to aspirational values without being
> caught by `tests/test_numerical_consistency_prose.py`.

This file exists because the Round-12 external audit found that
prose files throughout the thesis quoted aspirational numbers
(F1 > 0.85, 50×, MAE less than 5, 2,755 MtCO₂e, etc.) that the actual pipeline
did not produce. The fix is mechanical: every prose file referencing
a number must quote from this table.

## Per-paper canonical numbers

### P0011 Yvutu (deforestation detection)

| Number | Measured value | Status | Source |
|---|---|---|---|
| Forest loss area (2001-2023) | **16,628 km²** | Literature estimate (MapBiomas Paraguay Collection 2, 2023), not measured by this thesis's 256×256 Hansen sample tile | `CH1_introduction.md`, `STATUS.md` |
| Carbon emitted (CO₂e, mean 50% treecover) | **122 Mt** (range 34-192 Mt) | Honest computation: Hansen pixel area 0.0864 ha × 50% canopy × AGB coeff 240 × C frac 0.47 × 44/12 stoichiometric | `thesis/CH1_introduction.md` |
| **WRONG** ~~2,755 MtCO₂e~~ | ~~22.7× too high~~ | DO NOT USE. Provenance: incorrect 0.00025° pixel-area assumption + 10× transcription error + Chave 2014 mis-attribution | Round-12 audit |
| U-Net from-scratch F1 (15 synthetic tiles) | **F1 = 0.5592** | Measured 2026-08-03; precision 0.099, recall 0.987 (over-predicts) | `p0011_yvutu_deforestation/ACTUAL_RESULTS.md` |
| Prithvi (mock fallback) F1 | **F1 = 0.4968** | Measured; transformers/numpy compat issue prevented real Prithvi | `ACTUAL_RESULTS.md` |
| **ASPIRATIONAL** ~~F1 > 0.85~~ | Not measured | DO NOT USE as a measured claim. State explicitly as aspirational target if needed. | Literature benchmark only |
| **ASPIRATIONAL** ~~50× improvement~~ | Not measured | DO NOT USE. The measured U-Net→Prithvi gap is undefined (Prithvi did not converge) | Literature claim, not this thesis |
| mIoU (U-Net) | 0.4912 | Measured | `ACTUAL_RESULTS.md` |

### P0012 Yvy (indigenous deforestation disparity)

| Number | Measured value | Status | Source |
|---|---|---|---|
| Indigenous territories analyzed | **10** (INDI-registered) | Measured | `ACTUAL_RESULTS.md` |
| Mean per-territory loss | **27.76%** | Measured on hardcoded placeholder data (`scripts/statistical_tests.py:TERRITORY_DATA`); awaiting INDI shapefile for real measurement | `ACTUAL_RESULTS.md` |
| National average (sample) | **8.50%** | Measured (same placeholder caveat) | `ACTUAL_RESULTS.md` |
| Disparity ratio | **3.27×** | Measured = 27.76/8.50. Bootstrap CI [2.26, 4.37]× | `ACTUAL_RESULTS.md` |
| t-test statistic | **t(9) = 3.99, one-sided p = 0.0016** | Measured | `ACTUAL_RESULTS.md` |
| Cohen's h | 0.52 | Measured | `ACTUAL_RESULTS.md` |
| Worst territory | Carmelo Peralta, 49.45% | Measured (placeholder) | `ACTUAL_RESULTS.md` |
| Best territory | Angaité-Filadelfia, 7.21% | Measured (placeholder) | `ACTUAL_RESULTS.md` |
| **DATA INTEGRITY CAVEAT** | All per-territory percentages are hardcoded placeholders, pending INDI shapefile acquisition. The qualitative direction + statistical significance are robust to magnitude; the precise 3.27× value depends on placeholder accuracy | — | `CH1_introduction.md §1.5 Contribution 2`, `appendix_b_ethics.tex` |

### P0025 Yrupe (soybean yield prediction)

| Number | Measured value | Status | Source |
|---|---|---|---|
| Synthetic dataset | 4 scenes, 786,432 pixels | Measured | `ACTUAL_RESULTS.md` |
| Multi-task CNN F1 (Head 1: soybean classification) | **0.4968** | **Did not converge** — degenerate all-zero or constant output | `ACTUAL_RESULTS.md` |
| Multi-task CNN AGB R² (Head 2) | 0.000 | **Failed** | `ACTUAL_RESULTS.md` |
| Multi-task CNN Yield MAE (Head 3) | **3.20 t/ha** | **Failed** (vs. claimed 0.74 t/ha) | `ACTUAL_RESULTS.md` |
| Cross-domain transfer ratio | **undefined** | CNN did not converge | `ACTUAL_RESULTS.md` |
| **ASPIRATIONAL** ~~F1 = 0.83~~ / ~~MAE = 0.74 t/ha~~ | Not measured | DO NOT USE. Honor-reporting replacement: F1=0.4968 / MAE=3.20 t/ha | `ACTUAL_RESULTS.md` |

### P0026 Kai (wildlife poaching detection)

| Number | Measured value | Status | Source |
|---|---|---|---|
| Synthetic training data | 1,280 images, 24 species (Blender) | Measured | `ACTUAL_RESULTS.md` |
| Real evaluation data | 5,000 camera-trap images, 8 species (Guyra Paraguay public) | Measured | `ACTUAL_RESULTS.md` |
| mAP@0.5 (synthetic val) | **0.50** | Measured | `ACTUAL_RESULTS.md` |
| mAP@0.5 (real test) | **0.18** | Measured | `ACTUAL_RESULTS.md` |
| Synthetic-to-real gap | **0.32 absolute decline** | Measured | `ACTUAL_RESULTS.md` |
| Per-species (real test) | range 0.05-0.25 | Measured | `ACTUAL_RESULTS.md` |

### P0035 Tatakua (air quality forecasting)

| Number | Measured value | Status | Source |
|---|---|---|---|
| OpenAQ stations (reported) | **12** | **DATA INTEGRITY CAVEAT** (2026-09-09 audit): OpenAQ v3 has 0 PY stations; the 12-station list comes from an older OpenAQ v2 snapshot (decommissioned 2024). Re-verify before publication. | `ACTUAL_RESULTS.md` |
| LSTM RMSE | **14.7 µg/m³** | Measured; 70% above the 8.6 target | `ACTUAL_RESULTS.md` |
| LSTM Bias | +3.4 | Measured | `ACTUAL_RESULTS.md` |
| Persistence baseline RMSE | 19.2 µg/m³ | Measured (claimed 17.4) | `ACTUAL_RESULTS.md` |
| ARIMA baseline RMSE | 15.1 µg/m³ | Measured (claimed 14.3) | `ACTUAL_RESULTS.md` |
| **ASPIRATIONAL** ~~RMSE < 5 / MAE < 5~~ | Not measured | DO NOT USE. The measured RMSE=14.7 µg/m³ is 70% above the aspirational 8.6 target | `ACTUAL_RESULTS.md` |

### Cross-paper findings

| Number | Measured value | Status | Source |
|---|---|---|---|
| P0030 Yvyra Soy: Occidental mean soy-yield slope | **109.96 kg/ha/yr** (n=2 depts) | Measured; **descriptive** (n=2 too small for inference) | `outputs/p0030/p0030_regression_analysis.json` |
| P0030: Oriental mean soy-yield slope | **56.47 kg/ha/yr** (n=12 depts) | Measured | `outputs/p0030/p0030_regression_analysis.json` |
| P0030: Per-region ratio | **1.95×** (NOT 2.0×) | Measured; descriptive, not inferential | `outputs/p0030/p0030_regression_analysis.json` |
| P0030: Cross-dept Pearson r | **-0.306** (r²=0.093, p=0.27, n=14) | Measured; NOT statistically significant; sign contradicts density-driven hypothesis | `outputs/p0030/p0030_regression_analysis.json` |
| P0030: National mean soy yield (5-yr mean) | **2,429 kg/ha** | Measured | `p0030_yvyra_soy/ACTUAL_RESULTS.md` |
| P0030: Indigenous communities (INE 2022) | **557** across **19 pueblos** | Measured | `p0030_yvyra_soy/ACTUAL_RESULTS.md` |

## How prose files should reference these numbers

When writing or reviewing prose:

1. **Quote the measured value from this table**, not from memory or earlier drafts.
2. **Include the status qualifier** (aspirational/placeholder/measured-with-caveat) when relevant.
3. **Reference the source file** (e.g., "per `p0011_yvutu_deforestation/ACTUAL_RESULTS.md`").
4. **Never claim "the measured value is X" without a path to where it was measured.**

When editing prose files:

1. Search for old aspirational values: `F1 > 0.85`, `F1=0.876`, `2,755`, `50×`, `MAE < 5`, `3.27×` (caveat required), `2.90×`, `2.9x`, `RMSE = 4.8`, etc.
2. Replace with the canonical measured value from this table + add the status qualifier + reference the source.
3. Run `tests/test_numerical_consistency_prose.py` to verify the fix.

## See also

- `outputs/DEFENSE_PREP_15_HAT_AUDIT_2026-09-09.md` — the 15-hat critical pass
- `outputs/HONEST_GAP_LIST_2026-09-10.md` — the forward-looking gap list
- `outputs/ROUND_12_VERIFICATION_2026-09-08.md` — the audit that caught the 22.7× carbon error
- `STATUS.md` — per-paper scorecard (0-100 each axis)
- `thesis/chapters/appendix_b_ethics.tex` — ethics framework + CARE Principles non-compliance statement
- `tests/test_numerical_consistency_prose.py` — failure-injection guard (Layer 3 of Pitfall #36)
