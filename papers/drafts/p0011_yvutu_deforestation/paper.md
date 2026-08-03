# P0011 Yvutu: Multi-Temporal Satellite Computer Vision for Chaco Deforestation

**Status:** Pilot experiment complete. Real-data run pending GEE auth + GPU.

---

## Abstract

We present **Yvutu** (\"wind\" in Guaraní), a multi-temporal satellite
computer vision pipeline for deforestation alert generation in the
Paraguayan Chaco. The pipeline is designed to fine-tune the Prithvi-300M
geospatial foundation model on Paraguay-specific data. **A pilot experiment
on 15 synthetic tiles is reported here.** The pilot validates the pipeline
end-to-end (data → training → evaluation → figures) but does not validate
the model itself. Real-data results are pending. The pilot is publicly
released so that reviewers can verify pipeline correctness and so that
the academic community can reproduce the implementation.

**Pilot results (15 synthetic tiles, 5 epochs):**
- Persistence: precision = 0.000 [0.000, 0.000], recall = 0.000 [0.000, 0.000], F1 = 0.000
- Random Forest (per-pixel): same as persistence
- U-Net from scratch: precision = 0.099 [0.095, 0.103], recall = 0.987 [0.983, 0.991], F1 = 0.180 [0.174, 0.186]
- Yvutu (lightweight fallback): same as persistence

All CIs are 95% bootstrap intervals over 10,000 resamples.

**Keywords:** deforestation, satellite computer vision, foundation models,
Paraguay, Chaco, Sentinel-2, MapBiomas, Prithvi

---

## 1. Introduction

Recent advances in self-supervised learning have produced foundation
models for satellite imagery. **The question is whether they can be
transferred to Paraguay-specific environmental monitoring with limited
local labeled data.** This paper describes a pipeline (Yvutu) designed
to test this question, and reports a pilot experiment that validates
the pipeline but does not yet answer the question.

The Paraguayan Chaco has lost approximately 5.2 million hectares of
forest cover between 2000 and 2023, driven primarily by agricultural
expansion. Operational monitoring of Chaco deforestation remains
expensive because the area is vast (~250,000 km²) and field surveys
are infrequent.

This paper makes three contributions:

1. **An open-source pipeline** for fine-tuning Prithvi on Paraguay tiles
   (the satellite-paraguay package).
2. **A pilot experiment** on synthetic data that validates the pipeline
   end-to-end.
3. **A clear roadmap** for real-data validation, including data
   acquisition scripts and expected results based on the Prithvi paper.

## 2. Related Work

### 2.1 Foundation Models for Earth Observation
Prithvi [Jakubik 2023] is a Vision Transformer pretrained on 600M HLS
patches. SatMAE [Cong 2022] extends the Masked Autoencoder framework.
AlphaEarth Foundations [Google DeepMind 2025] provides 64-dim embeddings
per 10 m pixel.

### 2.2 Deforestation Detection
Hansen GFC [Hansen 2013] provides annual 30 m forest loss globally.
MapBiomas Paraguay [MapBiomas 2024] provides 38-class land cover at 30 m.

### 2.3 Paraguay-Specific Studies
[Yvutu is the first Paraguay-specific AI system for deforestation detection
in the published literature.]

## 3. Methods

### 3.1 Study Area
Paraguayan Chaco (Western Paraguay), defined as the area west of the
Paraguay River (longitudes -62.5° to -57.0°, latitudes -25.0° to -19.0°).
~250,000 km², ~2,500 of Paraguay's 7,912 tiles (10×10 km grid).

### 3.2 Data Sources
- **Sentinel-2 L2A** (ESA Copernicus, free)
- **MapBiomas Paraguay** (CC0)
- **Hansen GFC v1.11** (CC0)
- **Paraguay Geodata** (CC0, Ai-Whisperers)

### 3.3 Synthetic Data (pilot only)
For the pilot experiment, we generated 15 synthetic tiles with
controllable deforestation events. Synthetic data allows verifiable
ground truth but does not capture real-world complexity (clouds, sensor
noise, mixed pixels). See `scripts/train_p0011_full.py` for generation
code.

### 3.4 Pipeline Architecture
Yvutu is built on `satellite-paraguay`:
- `src/satellite_io/` — Earth observation data ingestion
- `src/foundation_models/` — Prithvi, AlphaEarth, DINOv2 loaders
- `src/papers/p0011_yvutu_deforestation/pipeline.py` — Paper-specific pipeline

### 3.5 Training
For the pilot, 5 epochs of AdamW (lr=1e-3) with BCE loss. The lightweight
fallback backbone is used because Prithvi loading fails in this
environment (numpy 2.5 lacks version metadata).

## 4. Pilot Experiment

### 4.1 Setup
- 15 synthetic tiles (10 train, 2 val, 3 test)
- 24 monthly composites × 4 Sentinel-2 bands × 256×256 pixels
- 12,820 total deforestation pixels (1.0% of all pixels)
- 5 epochs, batch size 1, CPU
- Random seed 42

### 4.2 Results

| Model | Precision (95% CI) | Recall (95% CI) | F1 (95% CI) | TP | FP | FN | TN |
|-------|-------------------|----------------|-------------|----|----|----|----|
| Persistence | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 | 0 | 0 | 2,522 | 194,086 |
| Random Forest | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 | 0 | 0 | 2,522 | 194,086 |
| U-Net from scratch | 0.099 [0.095, 0.103] | 0.987 [0.983, 0.991] | 0.180 [0.174, 0.186] | 2,490 | 22,605 | 32 | 171,481 |
| Yvutu (lightweight) | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 | 0 | 0 | 2,522 | 194,086 |

### 4.3 Honest Interpretation

The pilot experiment exposes several limitations:

1. **Yvutu's lightweight fallback performed identically to persistence.**
   This is because the Prithvi model is incompatible with the current
   environment (numpy 2.5 lacks version metadata). The fallback is a
   3-layer CNN that did not converge in 5 epochs.

2. **U-Net overpredicts deforestation.** Precision = 0.099 means 99% of
   its positive predictions are false positives. It predicts 24,632
   pixels as deforested when only 2,522 are.

3. **Random Forest trained on pseudo-labels (NDVI < 0.4) rather than
   MapBiomas ground truth.** This produced a model that predicts all
   zero.

4. **The pilot validates pipeline correctness, not model quality.**
   Yvutu can ingest data, train, evaluate, and produce figures. It does
   not yet detect deforestation reliably.

### 4.4 Threats to Validity

- **Synthetic data:** The synthetic tiles do not capture real-world
  complexity. Real-data results are expected to differ.
- **Limited training:** 5 epochs is insufficient for the lightweight
  fallback. Prithvi typically requires 30+ epochs.
- **Class imbalance:** 1% positive class creates strong baseline
  incentive to predict zero.
- **No hyperparameter search:** All hyperparameters were set heuristically.

### 4.5 Reproduction

```bash
git clone https://github.com/IvanWeissVanDerPol/satellite-paraguay
cd satellite-paraguay
pip install -r requirements.txt
python3 scripts/train_p0011_full.py --epochs 5 --n-tiles 15 --output-dir outputs/p0011
python3 scripts/analyze_pilot.py  # produces bootstrap CIs
```

Expected output: same metrics in `outputs/p0011/metrics.json`.

## 5. Roadmap for Real Validation

To validate the pipeline on real data, the following steps are required:

1. **Set up GEE authentication:** `earthengine authenticate` (10 min)
2. **Download 50 real Sentinel-2 tiles** for the Paraguayan Chaco
3. **Acquire MapBiomas Paraguay 2022 labels** for those tiles
4. **Run Prithvi fine-tune on cloud GPU** (Vast.ai, ~$5, 4 hours)
5. **Re-run all 4 models** with 30 epochs
6. **Compare to baselines** (Random Forest, U-Net, Persistence)
7. **Validate against Hansen GFC** (independent ground truth)

**Expected real-data results based on Prithvi paper:**
- Prithvi achieves F1 = 0.85 on land cover classification tasks
- For binary deforestation detection, F1 = 0.80-0.85 is plausible
- Yvutu's improvement over U-Net should be 5-10 percentage points

**Cost:** ~$5 (Vast.ai GPU rental) + ~1 week of work
**Estimated timeline:** 1-2 weeks for real-data run + paper revision

## 6. Conclusion

This paper presents Yvutu, a multi-temporal satellite CV pipeline for
Paraguayan deforestation detection, and reports a pilot experiment on
15 synthetic tiles. The pilot validates the pipeline but does not
demonstrate model quality. Real-data validation is pending and is the
subject of ongoing work.

The pipeline is open-source (MIT license) and ready to reproduce.
Reviewers can verify its correctness today. The thesis-grade paper
will be submitted after real-data validation.

## 7. Author Contributions

- **Iván Weiss Van der Pol:** Conceptualization, Methodology, Software,
  Validation, Formal analysis, Investigation, Data curation, Writing
- **Juan Carlos Cristaldo (adviser):** Supervision, Resources, Review

## 8. Data and Code Availability

- Code: https://github.com/IvanWeissVanDerPol/satellite-paraguay
- Sentinel-2: https://browser.dataspace.copernicus.eu/
- MapBiomas Paraguay: https://plataforma.mapbiomas.org/
- Hansen GFC: https://www.globalforestwatch.org/

## 9. References

[1] Jakubik, J., et al. (2023). Foundation models for generalist
    geospatial AI. *arXiv:2310.18660*.

[2] Cong, Y., et al. (2022). SatMAE: Pre-training transformers for
    temporal and multi-spectral satellite imagery. *NeurIPS*.

[3] Google DeepMind (2025). AlphaEarth Foundations.

[4] Hansen, M. C., et al. (2013). High-resolution global maps of
    21st-century forest cover change. *Science*.

[5] MapBiomas Paraguay (2024). Collection 8.

[6] Cristaldo, J. C., et al. (2024). Paraguayan cartographic atlas.
    FADA-UNA Technical Report.

## A. Detailed Pilot Logs

See `outputs/p0011/`:
- `metrics.json` — Raw metrics
- `statistical_analysis.json` — Bootstrap CIs
- `STATISTICAL_ANALYSIS.md` — Human-readable
- `figures/` — 4 PNG figures
- `tables/` — 4 JSON tables + 1 LaTeX
- `unet_weights.pt`, `yvutu_weights.pt` — Trained checkpoints
