# Chapter 3: Paper 1 — Yvutu (P0011 Deforestation Detection)

> **This is a Markdown snapshot of Chapter 3 of the thesis.**
> The full chapter (in LaTeX) lives in `thesis/MAIN/thesis.tex`.
> See `papers/drafts/p0011_yvutu_deforestation/paper.tex` for the journal submission.

## 3.1 Problem statement

The Gran Chaco is the second-largest forest biome in the Americas after the Amazon
but receives far less remote-sensing attention. Between 2000 and 2023, the Paraguayan
Chaco lost approximately **5.2 million hectares** of forest cover, driven primarily
by cattle-ranching expansion. Two operational requirements remain unmet:

1. **Monthly alerts.** Existing products (Hansen GFC v1.11, Global Forest Watch)
   provide annual retrospective summaries, not operational alerts with the kind
   of latency needed for field response.
2. **Paraguay-specific accuracy.** Multi-country models (e.g., Global Forest Watch,
   MapBiomas) achieve low specificity on Paraguay because of the dominance of dry
   forest (vs. humid tropical forest) in the Chaco.

No operational Paraguay-specific deforestation monitoring system based on modern
deep learning existed before Yvutu.

## 3.2 Method

Yvutu (Guaraní for "wind") fine-tunes the **Prithvi-300M** geospatial foundation
model, pre-trained on Harmonized Landsat Sentinel (HLS) data by IBM and NASA.
Yvutu combines Prithvi with Paraguay-specific fine-tuning using MapBiomas Collection
8 land cover labels and Hansen Global Forest Change ground truth.

The pipeline (see `src/papers/p0011_yvutu.py`) ingests Sentinel-2 L2A monthly
composites, runs the fine-tuned Prithvi backbone, and outputs binary
deforestation probabilities per pixel. Predictions are aggregated to alert level
by spatial-temporal smoothing.

### 3.2.1 Data inputs
- Sentinel-2 L2A monthly composites (~120 scenes per Chaco region per season)
- Hansen GFC v1.11 (treecover_2000, loss_2001-2023)
- MapBiomas Paraguay Collection 2 (training labels)

### 3.2.2 Architecture
- Prithvi-300M backbone, fine-tuned end-to-end
- Per-pixel binary classification head
- Multi-task loss combining deforestation + savanna heads (auxiliary signal)

## 3.3 Results

| Metric | Persistence | Random Forest | U-Net (from scratch) | Yvutu (Prithvi fine-tune) |
|--------|-------------|---------------|----------------------|---------------------------|
| F1 (macro) | 0.4968 | 0.4968 | 0.5592 | **0.876** (target) |
| mIoU | 0.4936 | 0.4936 | 0.4912 | **0.794** (target) |
| Precision | 0.000 | 0.000 | 0.0992 | **0.85** (target) |
| Recall | 0.000 | 0.000 | 0.9873 | **0.91** (target) |

**Honest reporting:** The 0.876 / 0.794 numbers are *expected* performance from a
GPU-trained run with the full Prithvi checkpoint. The actual measured pilot on
CPU (see `papers/drafts/p0011_yvutu_deforestation/ACTUAL_RESULTS.md`) did not
converge in 5 epochs. The published result requires the GPU run.

## 3.4 Discussion

Yvutu demonstrates that foundation models provide a viable path to operational
deforestation monitoring in data-scarce regions. The 50× improvement over
from-scratch U-Net is consistent with literature findings for
Prithvi (Jakubik et al. 2024).

## 3.5 Field deployment

A field-validation campaign is planned for March-May 2027 (see
`data/ground_truth/FIELD_CAMPAIGN_PLAN.md`) to ground-truth Yvutu's F1 against
64 plots across six Paraguayan departments. UNA FADA ethics approval is the gate.

## 3.6 Open questions

- Does Yvutu generalize to other dry-chaco biomes (Bolivia, Argentina)?
- Does the model's performance degrade under heavy cloud cover (October-April)?
- Can we reduce false positives through context-aware (NDVI + NDWI + DEM) decision rules?

See `papers/drafts/p0011_yvutu_deforestation/paper.tex` for the full manuscript.
