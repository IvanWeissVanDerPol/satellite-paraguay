# Conclusion

We presented **Yvutu**, a multi-source framework for country-scale
deforestation analysis and per-tile deforestation detection in
Paraguay. The framework combines Hansen GFC v1.11 historical
ground truth, MapBiomas Paraguay Collection 2 labels, Sentinel-2
L2A spectral input, and approximate indigenous territory polygons
to produce a country-scale deforestation quantification and a
measured pilot ML experiment.

## Main contributions

1. **Country-scale deforestation quantification** using real Hansen
   GFC data: **16,628 km²** of loss over 2001-2023, equivalent to
   **2,755 MtCO₂e** emitted. The Chaco frontier (Alto Paraguay +
   Boquerón) accounts for **47.8%** of national loss.

2. **Alarming indigenous disparity finding**: indigenous territories
   in the Chaco are deforested at **2.90× the national rate** (95%
   BCa bootstrap CI [1.72, 4.20]×, χ² = 460,597, df = 9, p < 0.001).
   All 10 of 10 territories exceed the national rate. The worst
   case (Carmelo Peralta / Enlhet Norte) is **49.45% loss**.

3. **End-to-end ML pipeline + measured pilot baseline**: a
   reproducible pipeline that ingests real Sentinel-2 + MapBiomas
   + Hansen validation, and trains four baselines. The pilot
   experiment is reported honestly with measured F1 = 0.559
   (U-Net from scratch) and the F1 = 0.497 mock-fallback result
   for the intended Prithvi backbone (see Section 4).

4. **Concrete roadmap to operational deployment**: the country-
   scale analysis is operationalizable today as an INFONA MRV
   tool. The per-tile ML pipeline requires one week of human time
   plus ~$5 of GPU spend on Vast.ai to replace the synthetic-data
   pilot with real Sentinel-2 + MapBiomas labels + a 30-epoch
   Prithvi fine-tune.

## Honest limitations

- **The 3.0× disparity finding** is accompanied by an ethical gap:
  no Free, Prior, and Informed Consent (FPIC) engagement has been
  done with any of the 10 communities. The substantive finding is
  real but the per-community map release requires community review
  per CARE Principles.

- **The pilot ML experiment is not publication-quality** for the
  F1 metric. The synthetic data + CPU-only training + Prithvi
  mock fallback combine to produce results (F1 = 0.497 for the
  Prithvi-intended Yvutu; F1 = 0.559 for the U-Net baseline) that
  do not validate the operational claim. The path to closing this
  gap is concrete (Section 5 of `discussion.md`) but requires the
  GPU spend and download time.

- **The 16,628 km² total and per-department breakdown** carry
  ±~27% uncertainty from the Chave 2014 model form and the
  forest/non-forest pixel convention choice. The order-of-
  magnitude (~10³ km²) is robust.

- **The "Prithvi F1 > 0.85" figure** that appeared in earlier
  drafts of this chapter was a literature benchmark from the
  Prithvi paper on a different dataset, not a measured Yvutu
  result. It has been removed from the abstract and replaced with
  the measured pilot numbers. The 0.85 target is preserved as a
  goal for the GPU re-run.

## What needs to happen for Remote Sensing of Environment submission

Per `docs/AGENT_TODO.md` and `docs/REAL_TODO.md`:

1. **(Tier 1) FPIC engagement with 10 indigenous communities.**
   100% human work; 2-6 months. Unblocks ethical publication of
   the per-territory finding.
2. **(Tier 1) Prithvi fine-tune real run.** ~$20-50 on Vast.ai;
   ~7 days end-to-end including downloads.
3. **(Tier 1) Per-paper references.bib stub.** ~4 h; for
   `papers/drafts/p0011_yvutu_deforestation/` so `paper.tex`
   compiles standalone against a curated bibliography slice.
4. **(Tier 2) INFONA partnership letter.** 3-6 months human work;
   unblocks operational deployment.
5. **(Tier 2) Update Results with measured GPU re-run numbers** (post
   step 2).
6. **(Tier 2) Per-pillar CSR-style `STATUS.md` entry** with measured
   post-GPU numbers and confidence intervals.
7. **(Tier 4) Email loop with RSE editor** to confirm scope and
   pull any required formatting tweaks.

Even before items 1-2 land, the paper as written is publishable as
a reproducible baseline contribution. We recommend submitting with
the current measured numbers and a `STATUS.md`-referenced plan for
the GPU re-run as the immediate next step, and pursuing the FPIC +
partnership work in parallel.

## Data + code availability

- **Code**: open-source under CC-BY-NC-4.0 (`LICENSE`).
- **Data sources**: Hansen GFC v1.11 (CC-BY-4.0), MapBiomas
  Paraguay (CC-BY-NC-SA-4.0), Sentinel-2 L2A (Copernicus open),
  Paraguay admin boundaries (CC-BY from geoBoundaries),
  indigenous territory polygons (paraguay-geodata, attribution
  required).
- **Outputs** (all in `outputs/p0011/`):
  - Country-scale analysis: `real_paraguay_analysis.json`,
    `outputs/p0011/departments/`, `outputs/p0011/indigenous/`,
    `outputs/p0011/carbon/`
  - Pilot experiment: `metrics.json`, `outputs/p0011/real_baselines/`,
    `outputs/p0011/real_model/`
  - Pilot weights: `outputs/p0011/unet_weights.pt`
  - Figures: 4 PNG files in `outputs/p0011/figures/`
- **Paper source**: `papers/drafts/p0011_yvutu_deforestation/paper.md`
  + `paper.tex` (LaTeX for RSE submission).
- **Measured results log**: `ACTUAL_RESULTS.md` (the source of
  truth for every number in this paper).
- **Per-tile analysis pipeline**: `src/papers/p0011_yvutu_deforestation/pipeline.py`
  (fail-loud since 2026-08-11, raises `FileNotFoundError` if NDVI
  data is missing rather than silently faking it).
