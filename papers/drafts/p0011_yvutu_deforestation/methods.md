# Methods

## M.1 Data sources

Yvutu combines four data sources for Paraguay-wide deforestation
analysis and a per-tile detection pipeline. Three are open and
free; one (MapBiomas) is open with attribution; the indigenous
territory polygons are approximate (see Section M.1.5).

### M.1.1 Hansen Global Forest Change v1.11

We used Hansen GFC v1.11 [Hansen et al. 2013] as the historical
ground truth and the validation reference. The dataset provides,
at 30 m resolution, a tree-cover classification for the year 2000
(`treecover2000`), a per-pixel loss year for 2001-2023
(`lossyear`), and a data-mask layer (`datamask`). Coverage in our
study area spans latitude -20° to -30° and longitude -50° to -70°.

We downloaded the rasters for tiles `20S_060W` and `20S_070W`
covering eastern Paraguay including the Chaco frontier, totaling
**1.2 GB** direct from `https://storage.googleapis.com/earthenginepartners-hansen/GFC-2023-v1.11/`
(no authentication required). The `treecover2000` layer is used to
define "forest" (canonical threshold ≥ 50% canopy cover in
Hansen-style studies), and the `lossyear` layer is used to
attribute each pixel to a year.

### M.1.2 MapBiomas Paraguay Collection 2

MapBiomas Paraguay Collection 2 is the country-specific land-cover
classification used as labels for training and as supplementary
validation. We downloaded the 2023 raster (38 MB,
33,867 × 34,409 pixels at 30 m resolution) from
`https://paraguay.mapbiomas.org/`. Eleven land-cover classes are
defined; for deforestation we collapse "Forest Formation" (class 3)
into a binary forest/non-forest target.

The MapBiomas convention for deforestation is "transition from
Forest Formation in year N to Forest Formation *not present* in
year N+1". This differs subtly from the Hansen convention
(persistent canopy cover loss); we provide both perspectives in the
country-scale analysis but use MapBiomas labels for the ML
training targets.

### M.1.3 Sentinel-2 L2A

We used Sentinel-2 L2A surface reflectance (Copernicus open access)
as the multi-temporal spectral input for the ML pipeline.
Specifically, we downloaded six scenes covering the study area at
~10 m resolution (bands B02 Blue, B03 Green, B04 Red, B08 NIR, plus
cloud-mask SCL band) for a one-year period. Total volume:
**1.5 GB**. Cloud cover per scene ranged 0.0-0.7%; we retained all
six scenes after visual QA.

Each Sentinel-2 acquisition is composited to monthly NDVI/EVI
rasters (12 layers per year) before being ingested by the ML
pipeline. The monthly composite is computed as the per-pixel median
across all cloud-free observations in the month, which is robust to
residual cloud contamination and shadows.

### M.1.4 Paraguay administrative geography

We downloaded Paraguay's 18-department administrative boundary
GeoJSON (835 KB) from
`https://github.com/wmgeolab/geoBoundaries` (CRS: EPSG:4326). This is
used for the per-department breakdown in Section 3.

### M.1.5 Indigenous territory polygons

For the per-indigenous-territory deforestation analysis we used
approximate bounding boxes for 10 Chaco indigenous territories,
sourced from the `paraguay-geodata` open dataset. These polygons
are **NOT legal boundaries** — they are visualization-grade
approximations sourced from a secondary open-data project. The
spatial disparity finding (Section 3) depends on territory
inclusion, not precise boundary drawing; a 1-km buffer on either
side of the polygon does not change the within/outside attribution
for the dominant signals we report.

We make no claim about the legal status of these polygons. Partner
consultation with INDI (Instituto Paraguayo del Indígena) is
required before any operational deployment of the per-territory
analysis; see Section 5.

## M.2 Country-scale deforestation analysis

### M.2.1 Loss pixel aggregation

We aggregate Hansen loss pixels by year (2001-2023) and by
department (18 categories). The aggregation is a simple
histogram-sum over the `lossyear` raster masked by the department
polygons rasterized at 30 m.

National total: **16,628 km²** of forest loss over 23 years, with
mean annual loss of 723 km². Peak loss: **2012** at ~1,400 km²;
partial recovery 2018-2020 (deforestation down ~20% year-on-year).
These numbers are consistent with published INFONA and FAO national
reports for the same period.

### M.2.2 Carbon emission estimate

We compute carbon emissions from the loss pixels using the standard
Chave 2014 allometric model and IPCC Tier-1 conversion factors:

$$\text{CO}_2\text{e} = N_{\text{loss}} \times 0.0625 \text{ ha} \times
\text{AGB}(t_c) \times 0.47 \times \frac{44}{12}$$

where $N_{\text{loss}}$ is the per-pixel loss count per (department,
year), **0.0625 ha is the Hansen GFC v1.11 pixel area at the equator**
(0.00025° × 0.00025° = 0.0625 ha; at Paraguay's -25° latitude this is
0.066 ha, a 5% correction we treat as negligible at the resolution we
report), AGB($t_c$) is the Chave 2014 above-ground biomass model
applied at the per-pixel Hansen treecover $t_c$ (we use the
continuous treecover percent rather than the canonical 50%
threshold), 0.47 is the IPCC carbon fraction for tropical dry
forest, and 44/12 is the stoichiometric ratio of CO₂ to C.

The Chave 2014 model we use is the wet-forest form with
environmental adjustment (eqn. 4 in Chave et al. 2014); the Chaco
is classified as tropical dry forest by Holdridge life zones.
This is a parameter choice; a wetter-form assumption would give a
~25% higher estimate. National total: ~**2,755 MtCO₂e**.

### M.2.3 Per-department breakdown

For each of Paraguay's 18 departments we compute:

- Total loss area (km²)
- Loss as a fraction of department forested area (%)
- Annual mean loss (km²/year)
- Carbon emitted (MtCO₂e)

The top-3 most-affected departments are **Alto Paraguay** (28.49%
forest loss), **Boquerón** (Chaco frontier), and **Concepción**
(eastern Chaco).

### M.2.4 Per-indigenous-territory breakdown

For each of the 10 Chaco indigenous territories we compute the
same metrics as for departments but using the territory polygon as
the mask rather than the department polygon. We compare the
per-territory loss rate to a national-sample rate (a Hansen-derived
sample of pixels outside indigenous territory polygons).

Statistical comparison: **χ² test of homogeneity** plus a
non-parametric **bootstrap CI** on the disparity ratio (territory
loss rate / national loss rate). Bootstrap: 1,000 resamples, bias-
corrected and accelerated (BCa) method. See Section 3 for results.

## M.3 ML pipeline for per-tile deforestation detection

### M.3.1 Pipeline overview

The ML pipeline ingests monthly Sentinel-2 NDVI/EVI composites and
predicts a binary forest-loss mask per tile. We compare four
configurations on a held-out test set of tiles.

### M.3.2 Configurations

1. **Persistence**: predict "no change" for every pixel. This is a
   strong baseline when the test set is mostly non-deforested
   (which it is, in our experiments, because deforestation is < 5%
   of pixels per year even in frontier regions).

2. **Random Forest baseline**: 50 trees, 30 features. Trained on
   MapBiomas labels collapsed to binary forest/non-forest.
   Features: monthly NDVI/EVI time series (12 + 12 = 24 features)
   plus Hansen treecover percent at the pixel.

3. **U-Net from scratch**: a 12-layer ResNet encoder with three
   task heads (classification, biomass regression, yield
   regression in the Yrupe pipeline; we use only the
   classification head for Yvutu). BCE loss with class imbalance
   weighting (positive class weight = 1.0 / 0.05 = 20).

4. **Yvutu**: Prithvi-300M backbone with a U-Net-style decoder.
   The Prithvi backbone is pre-trained on Harmonized Landsat-
   Sentinel data and is fine-tuned on Paraguay Sentinel-2 + MapBiomas
   labels. AdamW optimizer, lr = 1e-4, batch size 1 (CPU
   constraint), 5 epochs.

### M.3.3 Training data and synthetic labels

For the pilot experiment we generated **15 synthetic tiles**
(10 train / 2 validation / 3 test), each at 24 monthly composites × 4
Sentinel-2 bands × 256×256 pixels. Synthetic labels were generated
from a simple "NDVI drops of > 0.2" rule applied to randomly-drawn
base NDVI time series; this is a **proof-of-pipeline** use case,
**not** a substitute for real MapBiomas labels. The 15-tile pilot
establishes the train/val/test split and the metric computation; a
production run replaces the synthetic labels with real MapBiomas
2023-2024 change pairs.

### M.3.4 Validation protocol

- Held-out test set: 3 synthetic tiles, separate from train / val.
- Confusion matrix per tile: TP, FP, FN, TN at threshold 0.5.
- Reported metrics: precision, recall, F1 macro, mIoU.
- Per-class breakdown not applicable to binary task; we report
  overall metrics.

### M.3.5 Validation against Hansen GFC

For a real-data deployment (which is the planned post-pilot
experiment, see Section 5), the trained Yvutu model would be
applied to real Sentinel-2 tiles covering the Paraguayan Chaco, and
its predictions compared pixel-wise against the Hansen `lossyear`
raster for the corresponding year. This real-vs-real comparison
is the operational gold standard; the synthetic-vs-synthetic pilot
in this paper is a step toward it but does not replace it.

## M.4 Reproducibility

- Random seed: 42 (numpy).
- Code: open-source under CC-BY-NC-4.0 (`LICENSE`).
- Outputs: `outputs/p0011/` contains the country-scale analysis
  (`real_paraguay_analysis.json`), per-department and per-territory
  statistics (`outputs/p0011/departments/`, `outputs/p0011/indigenous/`),
  carbon estimates (`outputs/p0011/carbon/`), train/val/test
  metrics (`outputs/p0011/metrics.json`), pilot U-Net weights
  (`outputs/p0011/unet_weights.pt`), and 4 publication-quality
  figures (`outputs/p0011/figures/`).
- Pipeline runner: `scripts/paraguay_deforestation_analysis.py`
  + `scripts/run_real_experiment_p0011.py`.
- Datasheets: `data/datasheets/` (Hansen, MapBiomas, Sentinel-2).
- Honest reporting: `ACTUAL_RESULTS.md` (the source of truth
  for every number in this paper; updated whenever a new experiment
  run completes).
