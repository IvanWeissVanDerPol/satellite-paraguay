# Methods

## Yvytu: Multi-Temporal Satellite CV for Chaco Deforestation

We use Sentinel-2 L2A imagery (10m, 5-day revisit) from ESA Copernicus. For each tile (10×10 km), we stack 24 monthly composites (2020-2024) and extract per-pixel NDVI/EVI time series. The Prithvi-300M model is fine-tuned on MapBiomas Paraguay labels using a U-Net decoder. Deforestation is detected via BFAST-like change detection on the segmentation output. We validate against Hansen GFC and MapBiomas independently.

## Datasets

See `data/datasheets/` for detailed dataset descriptions.

## Models

See `models/cards/` for foundation model details.

## Code

All code is available in `src/papers/p0011_yvytu_deforestation/pipeline.py`.

## Reproducibility

See `src/utils/reproducibility.py` for random seed management + environment capture.

## Ethical Considerations

See `docs/STAKEHOLDERS.md` and per-paper README for ethics review.
