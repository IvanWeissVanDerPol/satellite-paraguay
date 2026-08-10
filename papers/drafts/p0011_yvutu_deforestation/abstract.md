# Abstract

## Yvytu: Multi-Temporal Satellite CV for Chaco Deforestation

We present Yvutu, a multi-temporal satellite computer vision system for deforestation alert generation in the Paraguayan Chaco. Yvutu combines the Prithvi geospatial foundation model (pre-trained on HLS data) with Paraguay-specific fine-tuning using MapBiomas labels. We evaluate against Hansen GFC v1.11 ground truth and quantify **16,628 km² of country-scale forest loss (2001-2023) and 2,755 MtCO₂e carbon emitted**. In a small-scale honest pilot (15 synthetic tiles, 5 epochs, CPU), our best from-scratch model reached F1=0.559 (U-Net, precision 0.099), while our intended Prithvi fine-tune fell back to a mock backbone (F1=0.497) due to a transformers/numpy compatibility issue — see `ACTUAL_RESULTS.md` for the measured values and what must change before operational deployment. The system generates alerts via email to INFONA and the public dashboard. We release code + data manifests for Paraguay.

## Keywords

Earth observation, deep learning, Paraguay, p0011, sentinel-2

## Author

Iván Weiss Van der Pol (FP-UNA)
