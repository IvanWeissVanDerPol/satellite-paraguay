# P0026 Kai — Cover Letter for Conservation Biology

**Date:** August 4, 2026
**To:** Editor-in-Chief, Conservation Biology
**Journal:** Conservation Biology (Wiley, IF=5.2, CiteScore=8.9)
**Manuscript type:** Original research article (short report)

---

Dear Editor,

We submit our short report "**Kai: Automated wildlife detection in the Paraguayan Chaco — A pilot transfer-learning study of YOLOv8**" for consideration in *Conservation Biology*.

## Significance

Camera-trap networks in the Paraguayan Chaco generate data faster than human reviewers can analyze. Automated detection can relieve this constraint, but the validation is rare for South American biomes. We present a pilot evaluation using:

- YOLOv8-S pretrained on COCO, fine-tuned on a synthetic camera-trap dataset (1280 images)
- 24 species including jaguar, puma, marsh deer, pampas deer
- Cross-validation on real camera-trap images (5000 images, 8 species, Guyra Paraguay public dataset)

## Honest findings

Our contribution is honest about its limitations. Real-world detection mAP=0.18 is below operational threshold; we report it as such and propose a cascading system (binary classifier → species-level fine-tune) to close the gap. We hope this transparent reporting serves as a counter-example to the over-claiming that has eroded trust in published wildlife-detection studies.

## Why Conservation Biology

The journal's focus on practical conservation, including the Methods in Biodiversity section, is a strong fit for our methodology paper.

## Authors & contributions

Iván Hocht-VonDerPol (FADA-UNA) is sole author. Guyra Paraguay provided the real camera-trap data under a data-use agreement.

## Data & code

Synthetic data: CC-BY 4.0. Real data: subject to Guyra Paraguay data-use agreement. Code: MIT license.

## Conflict of interest

The author declares no competing interests.

We look forward to your consideration.

Sincerely,

**Iván Hocht-VonDerPol, MSc**
FADA-UNA, Paraguay
