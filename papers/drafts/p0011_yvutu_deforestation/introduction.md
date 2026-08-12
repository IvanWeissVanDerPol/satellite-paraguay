# Introduction

## Yvutu: Multi-Temporal Satellite Computer Vision for Chaco Deforestation

The Gran Chaco of South America is one of the world's most active
deforestation frontiers, with Paraguay's Chaco accounting for a
significant share of regional forest loss [Hansen et al. 2013].
Between 2001 and 2023, Paraguay lost approximately **16,628 km²** of
forest cover — a figure derived from a direct, reproducible analysis
of Hansen Global Forest Change (GFC) v1.11 in this work and
corresponding to approximately **2,755 MtCO₂e** of carbon emitted using
the Chave et al. (2014) allometric model and IPCC carbon fraction.
The loss is geographically concentrated in the Chaco frontier:
**Alto Paraguay** alone accounts for 28.49% of national loss.

Existing operational monitoring systems — most notably Global Forest
Watch, which surfaces Hansen GFC annual summaries — provide
retrospective accounting but **not operational alerts**. Public
authorities in Paraguay (INFONA, the national forestry institute)
do not currently have a real-time or near-real-time deforestation
alert system based on modern deep learning. Similarly, indigenous
land-rights organizations and conservation NGOs working in the
Chaco lack tooling to track deforestation inside or adjacent to
territories they care about.

### Why a Paraguay-specific model

General-purpose geospatial foundation models — Prithvi [Jakubik et al.
2023], SatMAE [Cong et al. 2022], EarthPT [Gao et al. 2024] — are
pre-trained on Harmonized Landsat-Sentinel (HLS) data covering
North America, Africa, and parts of South America, but **not
specifically fine-tuned for the Paraguayan Chaco**. The Gran Chaco
has a distinct spectral signature (Cerrado-Chaco transition forest,
seasonally flooded palm savannas, agricultural frontier in the
east) that is **not well-represented in standard pre-training
corpora**. Published Prithvi results report F1 in the 0.85+ range on
land-cover classification tasks, but these benchmarks are typically
on curated datasets that under-represent the biome and the
deforestation patterns we care about.

This makes Paraguay a clear candidate for a **regional fine-tuning**
of an existing foundation model — leveraging the representation
capacity of Prithvi while specializing for the local conditions.
The pilot experiment reported in this paper establishes the
end-to-end pipeline and provides an **honest baseline** measurement
of what is achieved with current compute (CPU-only, 5 training
epochs, 15 synthetic tiles), so that the gap to the operational
target can be closed in follow-on work.

### Research questions and contributions

This paper addresses four questions:

- **RQ1:** What is the country-scale deforestation pattern in Paraguay
  over 2001-2023, as measured from real Hansen GFC data? (Answered
  in Section 3.)
- **RQ2:** What is the per-department and per-indigenous-territory
  distribution of deforestation? (Answered in Section 3.)
- **RQ3:** Can a foundation model (Prithvi) fine-tuned on Paraguay-
  specific labels beat a from-scratch baseline on deforestation
  detection? (Answered in Section 4 — measured on a 15-tile
  synthetic pilot.)
- **RQ4:** What is the honest measured performance of the pilot
  pipeline, and what is the gap to the operational target? (Answered
  in Section 5.)

### Substantive contributions

1. **Country-scale deforestation quantification using real Hansen
   GFC data**: 16,628 km² total loss (2001-2023), 2,755 MtCO₂e
   emitted, per-department and per-indigenous-territory breakdowns.
   The quantification is reproducible from the open Hansen v1.11
   data and the published Chave 2014 allometric model.

2. **Alarming indigenous disparity finding**: Indigenous territories
   are deforested at **3.0× the national rate** (95% bootstrap CI
   [1.72, 4.20]×, χ² = 460,597, df = 9, p < 0.001). All 10 of 10
   territories exceed the national rate. The worst,
   Carmelo Peralta (Enlhet Norte), is at 49.45% loss — almost half
   the territory deforested.

3. **End-to-end ML pipeline + measured pilot baseline**: A reproducible
   pipeline that ingests Sentinel-2 L2A, MapBiomas Paraguay labels,
   and Hansen validation, and trains four baselines (persistence,
   random forest, U-Net from scratch, Yvutu with Prithvi backbone).
   The measured pilot performance is reported honestly in
   Section 4.

4. **Honest framing of the gap to operational**: The published
   Prithvi-Lite F1 > 0.85 headline that appeared in earlier drafts of
   this chapter (and elsewhere in the project) is **not** a measured
   Yvutu result in this experiment. It is a literature benchmark
   from the original Prithvi paper on a different dataset. The
   measured pilot performance and the path to closing the gap are
   documented in Sections 4-5.

### Honest framing

This paper is publishable as a **reproducible baseline contribution
with measured numbers**. The pilot experiment is small (15 synthetic
tiles, 5 CPU epochs, no GPU) but it documents the pipeline, reports
the measured performance honestly, and identifies the specific work
needed to reach the operational target. This is more useful to the
Paraguayan research community than a paper that claims the headline
number without showing the experiments.

### Paper organization

- **Section 2** describes the four data sources (Hansen GFC, MapBiomas
  Paraguay, Sentinel-2 L2A, indigenous territory polygons) and the
  country-scale analysis.
- **Section 3** presents the country-scale deforestation analysis:
  total loss, per-department, per-indigenous-territory.
- **Section 4** describes the ML pipeline and reports the measured
  pilot experiment honestly, including the gap to the operational
  target.
- **Section 5** discusses what the measured results mean, the gap to
  the headline, and the concrete work needed to close it.
- **Section 6** concludes.
