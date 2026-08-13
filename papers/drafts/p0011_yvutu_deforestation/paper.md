# Chapter 3: Yvutu — Multi-Temporal Satellite Computer Vision for Chaco Deforestation Detection

**Author:** Iván Weiss Van der Pol
**Status:** Chapter of the thesis (in journal-preparation)
**Target journal:** Remote Sensing of Environment (IF 13.5, CiteScore 22.1)

---

## Abstract

We present **Yvutu** ("wind" in Guaraní), a multi-temporal computer
vision framework for deforestation analysis and per-tile
deforestation detection in Paraguay's Gran Chaco using foundation
models. We establish a **real-data baseline** using Hansen Global
Forest Change (GFC) v1.11, MapBiomas Paraguay Collection 2, and
six Sentinel-2 L2A scenes (Microsoft Planetary Computer).

Our contributions are:

1. **Country-scale deforestation quantification using real
   Hansen GFC data**: 16,628 km² of forest loss quantified
   (2001-2023), 2,755 MtCO₂e emitted (Chave 2014 + IPCC Tier-1).
2. **Per-department analysis** showing 28.49% loss in Alto
   Paraguay, with the Chaco frontier accounting for 47.8% of
   national loss.
3. **Per-indigenous-territory analysis** showing indigenous
   territories are deforested at **2.90× the national rate**
   (95% bootstrap CI [1.72, 4.20]×, χ² = 460,597, df = 9,
   p < 0.001); the worst single case (Carmelo Peralta / Enlhet
   Norte) is **49.45% loss**.
4. **End-to-end ML pipeline + measured pilot baseline** for
   per-tile deforestation detection: reproducible pipeline
   ingesting Sentinel-2 + MapBiomas + Hansen validation; four
   baselines compared; **measured** F1 = 0.5592 (U-Net from
   scratch, high recall but low precision) and F1 = 0.4968
   (Yvutu with Prithvi-mock fallback that did not converge in
   5 CPU epochs).
5. **Honest negative results** from the pilot experiment,
   documenting what is needed for operational deployment: one
   week of human time + ~$5 of GPU spend on Vast.ai to replace
   the synthetic data + CPU training + Prithvi mock fallback
   with real Sentinel-2 + real MapBiomas labels + a 30-epoch
   Prithvi fine-tune.

We release all scripts, data manifests, and reproducibility
artifacts under CC-BY-NC-4.0.

> **Honest Reporting Note (added 2026-08-10):** The abstract above
> formerly cited "**F1 = 0.85 vs F1 = 0.017 from-scratch**". The
> 0.85 figure is a literature benchmark from the Prithvi paper
> on a different dataset, **not** a measured Yvutu result; the
> 0.017 figure is from a different earlier U-Net baseline run
> with a different (synthetic) training set. See
> `ACTUAL_RESULTS.md` for the measured pilot numbers (F1 = 0.559
> for U-Net from scratch, F1 = 0.497 for Yvutu-Prithvi-mock in
> the 2026-08-03 run) and `discussion.md` for the gap to the
> aspirational 0.85 target.

---

## Paper body

This paper is organized as a set of structured sections in
companion files. Read in order:

- **`introduction.md`** — research questions and contributions.
- **`methods.md`** — data sources (Hansen, MapBiomas, Sentinel-2,
  Paraguay admin, indigenous territories), per-department and
  per-territory analysis, the per-tile ML pipeline.
- **`results.md`** — country-scale findings (16,628 km² loss,
  3.0× disparity, per-department breakdown) and the measured
  pilot ML experiment (F1 = 0.559 / 0.497).
- **`discussion.md`** — the disparity finding as a substantive
  contribution, the gap to operational, the carbon estimate
  uncertainty, and the concrete roadmap to close the gap.
- **`conclusion.md`** — main contributions, honest limitations,
  deployment roadmap.
- **`related_work.md`** — Hansen / GFW, geospatial foundation
  models (Prithvi, SatMAE, EarthPT), indigenous-land literature,
  operational MRV systems.
- **`ACTUAL_RESULTS.md`** — the source of truth for every number
  in this paper (the measured pilot numbers + the publication
  targets).
- **`paper.tex`** — LaTeX submission template for Remote
  Sensing of Environment.
- **`cover_letter.md`** + **`submission_checklist.md`** — for
  RSE submission.

---

## Headline numbers (measured)

| Finding | Value | Source |
|---|---|---|
| Total loss 2001-2023 | 16,628 km² | Hansen GFC v1.11 |
| Carbon emitted (Chave 2014 + IPCC) | 2,755 MtCO₂e | Hansen + Chave + IPCC |
| Alto Paraguay loss | 28.49% | Hansen + department polygons |
| **Indigenous disparity (territory / national)** | **2.90×** (CI [1.72, 4.20]×) | Hansen + territories, χ² p<0.001 |
| Worst territory (Carmelo Peralta / Enlhet Norte) | 49.45% loss | Hansen + territory polygon |
| U-Net pilot F1 (synthetic 15 tiles, CPU) | 0.5592 (P=0.099, R=0.987) | 5 epochs, seed 42 |
| Yvutu pilot F1 (Prithvi-mock fallback) | 0.4968 | transformers/numpy compat issue |
| Published Prithvi-Lite F1 (literature benchmark, not Yvutu) | > 0.85 | [Jakubik et al. 2023] |

---

## Honest limitations

- The 2.90× indigenous disparity is a substantive finding that has
  **not** been validated under FPIC (Free, Prior, and Informed
  Consent) engagement with the 10 communities or with INDI;
  per-community map release requires community review per CARE
  Principles [Carroll et al. 2020].
- The pilot ML experiment is not publication-quality for the F1
  metric. Closing the gap requires the GPU re-run documented in
  `discussion.md` Section D.4.
- The carbon estimate (±~27% band) depends on the Chave 2014
  model form and the forest/non-forest pixel convention; the
  order-of-magnitude (~10³ MtCO₂e) is robust, the precise figure
  is a point estimate.
- The published 0.85 F1 figure is a literature benchmark on a
  different dataset; it is not a measured Yvutu result and
  should not be cited as one in any submission.
