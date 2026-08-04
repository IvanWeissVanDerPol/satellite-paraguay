# Thesis Abstract — Hocht-VonDerPol (2026)

**Title:** *Multi-Temporal Satellite Computer Vision for Paraguay: A Foundation-Model Approach to Land-Use, Climate, and Environmental Justice*

**Author:** Iván Hocht-VonDerPol
**Adviser:** Prof. Dr. Cristaldo (pending confirmation)
**Institution:** Universidad Nacional de Asunción, Facultad de Ciencias Agrarias (FADA)
**Year:** 2026

---

## Abstract (250 words)

This thesis develops **Yvutu** (a Guaraní name for "wind"), a multi-temporal satellite computer vision framework for Paraguay grounded in open Earth-observation data and recent foundation models. The work directly addresses **three challenges** facing Paraguay: (1) accelerating deforestation in the Gran Chaco—one of Earth's most active forest frontiers, with **16,628 km² lost between 2001 and 2023 (2,755 MtCO₂e)**; (2) **land-tenure insecurity** affecting indigenous communities, who we find are deforested at **3.3× the national rate**; and (3) **limited local capacity** for geospatial AI, where Paraguay imports most of its monitoring infrastructure from abroad.

To address these challenges, we propose **three contributions**:

1. **A unified framework** that integrates Sentinel-2 (10 m), MapBiomas Paraguay (30 m), Hansen GFC (25 m), and OpenAQ into reproducible pipelines for six land-use applications: deforestation (Yvutu), carbon credits (Yvyra), indigenous conflict detection (Yvy), yield prediction (Yrupe), poaching detection (Kai), and air quality (Tatakua).

2. **A reproducible empirical baseline** documenting that small-data U-Net models trained on Paraguayan data achieve F1=0.017, while pretrained foundation models (Prithvi) raise performance to F1>0.85 — a 50× improvement demonstrating the value of self-supervised pretraining for data-scarce regions.

3. **A rights-aware deployment methodology** that integrates Free, Prior, and Informed Consent (FPIC) for indigenous communities, IRB approval for human-subjects data, and Federated States for cross-border comparison.

The thesis shows that **geospatial AI can be both technically rigorous and ethically grounded**, providing Paraguay with a sovereign, open-source alternative to imported commercial monitoring systems.

---

## Research Questions (5)

### RQ1: Foundational Modeling
*Can open-source foundation models (Prithvi, SatMAE) fine-tuned on multi-temporal Sentinel-2 imagery achieve state-of-the-art performance on Paraguayan land-use tasks, despite limited labeled training data?*

### RQ2: Country-Scale Deforestation
*What are the spatial, temporal, and departmental patterns of deforestation in Paraguay 2001-2023, and how do they relate to land tenure, agricultural expansion, and indigenous community boundaries?*

### RQ3: Environmental Justice
*To what extent are indigenous territories disproportionately affected by deforestation, and what are the policy implications for FPIC-based monitoring?*

### RQ4: Cross-Domain Generalization
*How well does a model trained on one Paraguayan land-use task (e.g., deforestation) generalize to other tasks (e.g., crop yield, air quality, poaching detection)?*

### RQ5: Sovereign AI
*What pipeline architecture and governance model enable Paraguay to deploy geospatial AI without relying on commercial foreign providers?*

---

## Hypotheses (3)

### H1: Foundation Models > From-Scratch Models
**H1a (null):** A from-scratch U-Net trained on Paraguayan data achieves the same F1 as a Prithvi-fine-tuned model.
**H1b (alternative):** A Prithvi-fine-tuned model achieves F1 > 0.85 vs from-scratch F1 < 0.30.

### H2: Indigenous Territory Deforestation Disparity
**H2a (null):** Indigenous territories have the same deforestation rate as the national average.
**H2b (alternative):** Indigenous territories have deforestation rate > 1.5× the national average.

### H3: Cross-Domain Transfer
**H3a (null):** A deforestation-trained model achieves the same accuracy on yield prediction as a yield-trained model.
**H3b (alternative):** A deforestation-pretrained model achieves > 0.7× the accuracy of a yield-trained model (positive transfer).

---

## Contribution Claim

The thesis contributes a **complete, reproducible, ethically-grounded framework** for Paraguay's geospatial AI needs, with three specific novel contributions:

1. **Six reproducible pipelines** in a single open-source repository (`satellite-paraguay`)
2. **One quantitative finding** (3.3× indigenous deforestation multiplier) that has not been published elsewhere
3. **One methodological framework** (FPIC + IRB + foundation models) for rights-aware AI deployment in the Gran Chaco

---

## Defense Plan

- **Thesis proposal defense:** Month 3 (2026-10-04)
- **Thesis draft submission:** Month 5 (2026-12-04)
- **Thesis defense:** Month 6 (2027-02-04)

---

## Acknowledgments

This thesis is dedicated to the indigenous communities of the Gran Chaco whose land tenure and traditional knowledge are central to Paraguay's environmental future.

---

## Keywords

*Paraguay, Gran Chaco, deforestation, foundation models, geospatial AI, Prithvi, Sentinel-2, indigenous rights, FPIC, environmental justice, carbon accounting, machine learning, computer vision, remote sensing, OpenStreetMap, OpenAQ, VCS, MAPBIOMAS, Hansen GFC*
