# Methods

## Kai: Wildlife Poaching Detection in Defensores del Chaco

We fine-tune YOLOv8m on (1) COCO-zoo transfer learning; (2) iNaturalist wildlife dataset; (3) WWF poaching-camp images (synthetic + real). We apply the model to satellite imagery over Defensores del Chaco. We cross-reference with NASA FIRMS fire alerts (poaching camps often leave fire traces). We validate mAP@0.5 against held-out WWF test set.

## Datasets

See `data/datasheets/` for detailed dataset descriptions.

## Models

See `models/cards/` for foundation model details.

## Code

All code is available in `src/papers/p0026_kai_poaching/pipeline.py`.

## Reproducibility

See `src/utils/reproducibility.py` for random seed management + environment capture.

## Ethical Considerations

See `docs/STAKEHOLDERS.md` and per-paper README for ethics review.
