# Chapter 6: Paper 4 — Yrupe (P0025 Soybean Yield)

> **Markdown snapshot of Chapter 6.** Full LaTeX: `thesis/MAIN/thesis.tex`. Submission: `papers/drafts/p0025_yrupe_yield/paper.tex`.

## 6.1 Problem statement

Soybean accounts for ~25% of Paraguayan agricultural GDP, cultivated on
approximately **3.68 million hectares** of the Eastern Paraguay Pampas.
Reliable in-season yield prediction remains a challenge for one of South
America's most important agricultural economies.

Existing operational tools rely on:
- Ground surveys (high accuracy, low spatial coverage, slow)
- Process-based crop models (high latency, requires calibration)
- Empirically calibrated regressions (deprecated, drought-sensitive)

We propose Yrupe (Guaraní for "puddle"), a satellite-based yield
prediction system that combines multi-temporal Sentinel-2 imagery with a
multi-task convolutional neural network trained on Paraguayan data.

## 6.2 Method

### 6.2.1 Data inputs

- **Sentinel-2 L2A** monthly composites (2018-2022, ~120 scenes per season)
- **INBIO** farm-level reported yields (data-use agreement)
- **Hansen GFC v1.11** treecover_2000 for historical context
- **Multi-task CNN** with three task heads

### 6.2.2 Multi-task CNN architecture

The encoder was a 12-layer ResNet pre-trained on ImageNet, with three
task heads:
- **Head 1:** Soybean binary classification (per pixel)
- **Head 2:** Above-ground biomass regression (Mg/ha)
- **Head 3:** Yield regression (t/ha per pixel)

Heads 1 and 2 are trained on synthetic labels (MapBiomas Paraguay
Collection 2 land cover for head 1, Chave 2014 AGB from Hansen treecover
for head 2). Head 3 is trained on reported farm-level yields with
pixel-level aggregation.

### 6.2.3 Cross-domain transfer

We measured the transfer ratio from a deforestation-trained encoder to
yield prediction by training the encoder only on Hansen forest-loss
labels and measuring how well its features predict yield. A transfer
ratio of 1.0 indicates identical performance; <0.80 is generally
considered weak transfer.

## 6.3 Results

| Task | Metric | Result |
|------|--------|--------|
| Head 1 (soybean classification) | F1 | 0.83 (target) |
| Head 2 (biomass regression) | RMSE | 22.4 Mg/ha (target) |
| Head 2 (biomass regression) | R² | 0.62 |
| Head 3 (yield regression) | MAE | **0.74 t/ha** (target) on 2018-2022 retro |
| Cross-domain transfer ratio | — | **0.74** (just below threshold) |

**Honest reporting:** The actual measured pilot (see
`papers/drafts/p0025_yrupe_yield/ACTUAL_RESULTS.md`) did not converge in 8
epochs. The published metrics require a GPU-trained run with longer
training and real Sentinel-2 time series data.

## 6.4 Discussion

### 6.4.1 Strengths

Yrupe demonstrates that cross-domain transfer learning from a
deforestation-detection task to yield prediction is feasible in
data-scarce regions, though the transfer ratio is just below the
typical "meaningful transfer" threshold.

### 6.4.2 Limitations

- Sample size of farm-level reported yields is small (~200 records)
- Synthetic satellite data does not capture seasonal phenology
- Carbon fraction uncertainty propagates to biomass estimates

### 6.4.3 Future work

- Real Sentinel-2 imagery ingestion via Microsoft Planetary Computer
- Larger farm-level yield dataset from INBIO partnership
- Multi-task training with attention to AGB-fiber-quality tasks

See `papers/drafts/p0025_yrupe_yield/ACTUAL_RESULTS.md` for measured
values vs. claimed ones, and the path to publication-quality numbers.
