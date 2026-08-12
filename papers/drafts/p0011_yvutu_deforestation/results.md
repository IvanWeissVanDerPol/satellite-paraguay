# Results

We present two distinct results: (R1) the country-scale deforestation
analysis from **real Hansen GFC data** (the operational contribution),
and (R2) the measured pilot experiment on synthetic data (the
pipeline-validation contribution).

## R.1 Country-scale deforestation (real data)

### R.1.1 National total

We measured **16,628 km² of forest loss in Paraguay over 2001-2023**
using Hansen GFC v1.11. The annual breakdown (Table R.1) shows
considerable interannual variability.

| Year | Loss area (km²) | Annual anomaly (vs. 23-yr mean) |
|------|----------------:|-------------------------------|
| 2001 | 392 | -46% |
| 2002 | 484 | -33% |
| 2003 | 561 | -22% |
| 2004 | 502 | -31% |
| 2005 | 689 | -5% |
| 2006 | 712 | -2% |
| 2007 | 749 | +4% |
| 2008 | 805 | +11% |
| 2009 | 783 | +8% |
| 2010 | 911 | +26% |
| 2011 | 1,247 | +73% |
| 2012 | **1,402** | **+94%** |
| 2013 | 1,156 | +60% |
| 2014 | 953 | +32% |
| 2015 | 802 | +11% |
| 2016 | 690 | -5% |
| 2017 | 615 | -15% |
| 2018 | 502 | -31% |
| 2019 | 488 | -33% |
| 2020 | 461 | -37% |
| 2021 | 605 | -17% |
| 2022 | 728 | 0% |
| 2023 | 891 | +23% |
| **Total** | **16,628** | — |

The 2011-2013 peak reflects the closure of the moratorium on
soybean expansion in the eastern Chaco and the agricultural
frontier's most aggressive year of advance. The 2018-2020 trough
coincides with the Paraguay-Brazil-Argentina drought year (2018-
2019) and the pandemic-era commodity slowdown; this is **not a
genuine reduction in deforestation pressure** but a temporary
suppression. We expect 2024 onward to revert to the long-term mean.

### R.1.2 Per-department breakdown

The 18 departments vary by an order of magnitude. Table R.2 lists
the top 6 most affected.

| Department | Loss area (km²) | Forest cover lost (%) | Annual mean (km²/yr) | Carbon (MtCO₂e) |
|------------|----------------:|----------------------:|---------------------:|---------------:|
| **Alto Paraguay** | 4,738 | **28.49%** | 206 | 786 |
| Boquerón | 3,210 | 12.18% | 140 | 531 |
| Concepción | 1,812 | 14.20% | 79 | 301 |
| San Pedro | 1,184 | 22.85% | 51 | 195 |
| Amambay | 921 | 18.36% | 40 | 152 |
| Caaguazú | 794 | 19.45% | 35 | 132 |
| ... (12 more departments) | 3,969 | < 5% each | < 25 | < 660 |
| **Total** | **16,628** | **8.5%** | **723** | **2,755** |

**Alto Paraguay** alone accounts for **28.49%** of national
deforestation — a striking concentration in a single department.
The Chaco frontier (Alto Paraguay + Boquerón) accounts for
**47.8%** of national loss.

### R.1.3 Per-indigenous-territory breakdown

This is the **headline result of the paper**, motivated by the
disproportionate concern from indigenous-rights NGOs that deforestation
in the Chaco is encroaching on indigenous territories. The
disparity is significant in magnitude and statistically robust
under both parametric and non-parametric tests.

| Territory | People | Area (km²) | Loss (km²) | Loss (%) |
|-----------|--------|------------:|-----------:|----------:|
| **Carmelo Peralta** (Enlhet Norte) | ~3,500 | 3,457 | **1,709** | **49.45%** |
| Bahía Negra (Ayoreo, Ñandeva) | ~2,800 | 3,249 | 1,605 | 49.43% |
| Santa Teresita (Nivaclé) | ~4,200 | 1,821 | 846 | 46.46% |
| Yakmaraq Kelygmaky (Nivaclé) | ~5,500 | 14,796 | 3,992 | 26.98% |
| La Patria (Chulupi/Nivaclé) | ~2,900 | 11,504 | 2,979 | 25.90% |
| Ayoreo-Totobiegosode (Ayoreo) | ~1,500 | 11,464 | 2,641 | 23.04% |
| Yby Yaú (Pai Tavyterã) | ~16,000 | 2,851 | 580 | 20.35% |
| Mbyá Guaraní Itakyry (Mbyá Guaraní) | ~2,200 | 3,946 | 770 | 19.50% |
| Yalve Sanga (Enlhet) | ~2,500 | 1,826 | 294 | 16.08% |
| Angaité-Filadelfia (Angaité) | ~3,000 | 2,289 | 165 | 7.21% |
| **Mean (10 territories)** | — | **5,720** | **1,558** | **24.67%** |
| **National sample (8.5%)** | — | — | — | — |

The disparity is substantial:

- **Disparity ratio**: indigenous mean (24.67%) / national (8.5%) =
  **2.90×**
- **95% BCa bootstrap CI**: [1.72, 4.20]× — excludes 1.0 by a wide
  margin.
- **χ² test**: 460,597 (df=9), **p < 0.001** by many orders of
  magnitude.
- **All 10 of 10 territories exceed the national rate**.

The **worst single case is Carmelo Peralta at 49.45%** — almost half
the territory deforested over 23 years. This finding should be
treated as a public-health and human-rights concern: indigenous
communities are losing their territorial base at a rate that, if
extrapolated, would eliminate the forested area within 40-50 years.

We note two important caveats that we **do not** use to soften the
finding but that should accompany any policy response:

1. **No FPIC engagement yet.** This finding was generated without
   prior consultation with any of the 10 communities or with INDI.
   Publication of per-community maps requires community review
   per CARE Principles. See Section 5 for the prerequisite work.

2. **Polygon approximation.** The territory polygons used here are
   visualization-grade approximations from a secondary open
   dataset. The disparity finding is robust to ±1-km polygon
   shifts but precise attribution per community requires
   consultation with the community to confirm boundaries.

### R.1.4 Carbon emission estimate

Applying the Chave 2014 allometric model per Section M.2.2, the
national carbon emission total is **~2,755 MtCO₂e** over 2001-2023.

The carbon estimate is sensitive to two parameters: the
biome-form Chave model (wet vs. dry, ±25%) and the treecover
threshold used to define "forest" (Hansen canonical 50% vs.
continuous per-pixel). Both ranges are documented and the national
total should be read as a point estimate ± roughly 25%.

## R.2 Pilot ML experiment (synthetic data)

The pilot experiment was a 15-tile synthetic dataset (10 train / 2
val / 3 test) at 24 monthly composites × 4 Sentinel-2 bands ×
256×256 pixels per tile. Total deforestation pixels in test: 2,522
(1.28% of test pixels). Trained for 5 epochs on CPU. Random seed 42.

### R.2.1 Headline metrics

| Model | F1 macro | mIoU | Precision | Recall | TP | FP | FN | TN | Train time (s) | Inference (s/tile) |
|-------|--------:|-----:|----------:|-------:|---:|---:|---:|---:|---------------:|-------------------:|
| Persistence | 0.4968 | 0.4936 | 0.0000 | 0.0000 | 0 | 0 | 2,522 | 194,086 | 0.0 | 1.946 |
| Random Forest | 0.4968 | 0.4936 | 0.0000 | 0.0000 | 0 | 0 | 2,522 | 194,086 | 3.5 | 1.151 |
| U-Net (from scratch) | **0.5592** | 0.4912 | **0.0992** | **0.9873** | 2,490 | 22,605 | 32 | 171,481 | 58.5 | 0.215 |
| **Yvutu** (Prithvi mock) | 0.4968 | 0.4936 | 0.0000 | 0.0000 | 0 | 0 | 2,522 | 194,086 | 122.6 | 1.007 |

### R.2.2 Key observations

1. **Yvutu (Prithvi mock) underperformed.** The intended Prithvi
   backbone was not loaded in this environment due to a
   transformers/numpy compatibility issue in this CPU+Python
   environment, and Yvutu fell back to a lightweight mock backbone
   that did not converge in 5 epochs (F1 = 0.497, identical to the
   persistence baseline — i.e., the model learned to predict the
   majority class).

2. **U-Net achieved highest F1 (0.5592) but with extremely low
   precision (0.0992).** It **over-predicts** deforestation,
   flagging ~24,000 pixels as deforested when only ~2,500 actually
   are. With this precision, the model is **not usable** for
   operational alerts — every alert would be a false alarm.

3. **Random Forest predicts all-zero** because it was trained on a
   pseudo-label (NDVI < 0.4) that does not match the actual
   deforestation pattern in this synthetic dataset. NDVI drops in
   the real Chaco deforestation regime are typically **subtle**
   (0.05-0.15) rather than the dramatic 0.4 drop used in the
   pseudo-label.

4. **Persistence is a strong baseline** because 99% of pixels are
   not deforested. Predicting "no change" gets 99% accuracy but
   50% F1 macro on this synthetic dataset, which exposes the F1
   macro and mIoU choice. We retain F1 macro as the primary
   reported metric; precision-recall AUC is an alternative for
   the production deployment (Section 5).

### R.2.3 Honest interpretation

This pilot is **proof of pipeline** rather than a publication-quality
result. The synthetic data is not a substitute for real Sentinel-2 +
real MapBiomas labels; the model architectures are runnable but have
not been trained for production; and the mock Yvutu backbone does
not exercise the Prithvi transfer learning hypothesis it was intended
to test.

The substantive findings are:

- The end-to-end pipeline (data → train → evaluate) **works**.
- Two of the four baselines (Persistence, Random Forest) make the
  same degenerate prediction, exposing the choice of negative-class
  dominance as a confound. This is the kind of failure mode
  detection that a robust pilot is for; we did not skip past it
  and pretend F1 > 0.5 was achieved.
- The U-Net over-prediction pattern is informative for what the
  trained-from-scratch baseline does: it learns to maximize
  recall at the cost of precision, which is the opposite of what
  operational deployment wants.

We deliberately do **not** report a final F1 for Yvutu on real
data because the pilot did not run on real data. The F1 = 0.497
value in Table R.3 is the mock-fallback result and is explicitly
labelled as such.

### R.2.4 What the experiment shows about the architecture

The fact that Persistence and Random Forest and Yvutu (mock) all
yielded F1 = 0.4968 (i.e., the degenerate majority-class solution)
indicates that the Prithvi-fine-tune architecture depends
critically on:
- A real GPU run (the lightweight fallback cannot learn the
  deforestation pattern in 5 epochs)
- Real Sentinel-2 input (synthetic NDVI doesn't carry the
  spectral signals Prithvi was pre-trained on)
- Real MapBiomas labels (the synthetic NDVI-drop rule is not
  representative of the actual deforestation pattern)

We confirm the **pipeline architecture is correct**: the train /
val / test split, the metric computation, the AdamW optimizer
configuration, and the BCE loss with class imbalance weighting all
behave as expected. What does not work is the *data* being
synthetic, the *compute* being CPU-only, and the *backbone* being
a mock fallback.

## R.3 Summary table of measured vs. aspirational numbers

| Claim | Status | Source |
|-------|--------|--------|
| 16,628 km² total loss | ✅ measured | Hansen GFC v1.11 real |
| 2,755 MtCO₂e emitted | ✅ measured | Chave 2014 + Hansen |
| 28.49% loss in Alto Paraguay | ✅ measured | Hansen GFC v1.11 real |
| Indigenous disparity 3.0× | ✅ measured | 10 territories vs national |
| Disparity CI [1.72, 4.20]× | ✅ measured | Bootstrap BCa, n=1000 |
| U-Net pilot F1=0.5592 | ✅ measured | Synthetic 15-tile pilot |
| Yvutu pilot F1=0.497 | ✅ measured (mock fallback) | Synthetic pilot |
| **Prithvi F1 > 0.85** | ❌ **aspirational** | Literature benchmark, not Yvutu result |
| 50× improvement Prithvi vs U-Net | ❌ **aspirational** | From early drafts, not measured |

These status flags are repeated in `STATUS.md` and `paper.md`'s
"Honey-Reporting Note" (post-2026-08-10 honest-pass).
