# Model Card — Prithvi

**Model:** Prithvi (IBM + NASA)
**License:** Apache 2.0
**HuggingFace:** https://huggingface.co/ibm-nasa-geospatial/Prithvi-300M
**Paper:** https://arxiv.org/abs/2310.18660
**Used in:** P0011 Yvytu, P0100 Yvyra, P0012 Yvy

## Model details

- **Architecture:** Vision Transformer (ViT)
- **Size:** 100M / 300M parameters
- **Input:** 224x224 multi-spectral satellite tiles (6 bands)
- **Output:** 768-dim embeddings + per-pixel classification
- **Pre-training:** HLS (Harmonized Landsat Sentinel) dataset
- **Pre-training data size:** ~120M image-tile pairs

## Intended use

- Transfer learning for downstream satellite CV tasks
- Land cover classification
- Change detection
- Building footprint extraction

## Training data

- **HLS-2 (Harmonized Landsat Sentinel-2):** Global, multi-sensor
- **Source:** NASA HLS project
- **Coverage:** Global land surface, 2013-present

## Evaluation

- **Pre-training:** Masked autoencoder loss
- **Downstream tasks (per IBM paper):**
  - EuroSAT: 84.2% accuracy
  - BigEarthNet: 71.5% mAP
  - Sen1Floods11: 87.5% IoU
  - CropType classification: high accuracy on agricultural regions

## Limitations

- Trained on global data — may need fine-tuning for Paraguay
- 224x224 input size — limited spatial context
- 6 input bands (subset of Sentinel-2 13 bands)
- Trained on HLS — different from raw Sentinel-2 (atmospheric correction differences)

## Ethical considerations

- Trained on global data — biases in geographic coverage
- Should be evaluated for Paraguay-specific performance
- Used for: conservation, agriculture, urban planning
- Should not be used for: military targeting, surveillance without consent

## Citation

```bibtex
@inproceedings{jakubik2023foundation,
  title={Foundation Models for Generalist Geospatial Artificial Intelligence},
  author={Jakubik, Johannes and Roy, Suman and Phillips, Christopher E. and Fraccaro, Paolo and Godwin, Denys and Zadrozny, Bianca and Szwarcman, Daniela and Gomes, Carlos and Nyirjesy, Gabby and Edwards, Blair and others},
  booktitle={Proceedings of the IEEE/CVF International Conference on Computer Vision},
  pages={17682--17701},
  year={2023}
}
```
