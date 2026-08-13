# Abstract

## Kai: Wildlife Poaching Detection in Defensores del Chaco

We present Kai, an AI-based wildlife detection system for Paraguay's Defensores del Chaco and Teniente Agripino Enciso national parks. We fine-tune YOLOv8-S on Blender-synthetic wildlife imagery (1,280 images, 24 species) and evaluate on 5,000 real camera-trap images from Guyra Paraguay. **mAP@0.5 drops from 0.50 on synthetic validation to 0.18 on real test data** — a 0.32 absolute gap consistent with the literature on synthetic-to-real domain shift. Reptile detection is worst (mAP=0.05 real). The mAP@0.5>0.70 headline and the WWF/Guyra deployment claims quoted in earlier drafts were aspirational and have been replaced with measured values in `ACTUAL_RESULTS.md`. We frame this as a contribution precisely because the gap quantifies how much Paraguay-specific labeled wildlife data is needed before operational deployment.

## Keywords

Earth observation, deep learning, Paraguay, p0026, sentinel-2

## Author

Iván Weiss Van der Pol (FP-UNA)
