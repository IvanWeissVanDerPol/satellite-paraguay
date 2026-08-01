# Model Card — AlphaEarth Foundations

**Model:** AlphaEarth Foundations (Google DeepMind)
**License:** Free for research use (Google DeepMind)
**URL:** https://deepmind.google/discover/blog/alphaearth-foundations/
**Used in:** P0100 Yvyra (carbon credit biomass)

## Model details

- **Architecture:** Embedding field model
- **Input:** Multi-source Earth observation data (optical + radar + DEM + climate + etc.)
- **Output:** 64-dimensional embedding per 10m×10m pixel
- **Spatial coverage:** Global land surface
- **Temporal coverage:** 2017-2024+

## Intended use

- Earth observation embeddings for downstream tasks
- Forest biomass estimation
- Land cover classification
- Biodiversity mapping

## Training data

- Multi-source Earth observation
- Global, multi-year
- Self-supervised pretraining

## Evaluation

- **Forest biomass (Lamahewage 2026):** R²=0.82 on regional-scale biomass estimation
- **Land cover:** Strong performance on multi-class segmentation
- **Biodiversity:** Useful features for species distribution

## Limitations

- 10m spatial resolution
- Cloud cover affects optical inputs
- May have geographic biases
- Trained globally — fine-tune for Paraguay

## Ethical considerations

- Used for: climate, biodiversity, agriculture
- Should not be used for: surveillance without consent, military
- Carbon credit applications need ground truth verification
- Indigenous lands require CARE Principles compliance

## Citation

```bibtex
@misc{alphaearth2025,
  title={AlphaEarth Foundations: An Embedding Field Model for Earth Observation},
  author={{Google DeepMind}},
  year={2025},
  howpublished={\\url{https://deepmind.google/discover/blog/alphaearth-foundations/}}
}
```
