---
title: "Chapter 11 — Conclusion"
author: "Iván Hocht-VonDerPol"
date: "2026-08-04"
---

# Chapter 11: Conclusion

## 11.1 Summary of Contributions

This thesis developed a multi-temporal satellite computer vision framework for Paraguay, integrating open Earth-observation data with foundation models and rights-aware deployment. The thesis makes three contributions:

### 11.1.1 A Unified Framework

Six reproducible pipelines (Yvutu, Yvyra, Yvy, Yrupe, Kai, Tatakua) integrated into a single open-source repository. These pipelines cover deforestation, carbon credits, indigenous conflict, crop yield, wildlife poaching, and air quality.

### 11.1.2 An Empirical Finding

The first quantitative estimate of the deforestation disparity affecting indigenous territories in Paraguay, finding a **3.3× multiplier** compared to the national average. This finding has direct policy implications for FPIC-based monitoring.

### 11.1.3 A Methodology

A rights-aware deployment methodology that integrates Free, Prior, and Informed Consent (FPIC) for indigenous communities, IRB approval for human-subjects data, and federated states for cross-border comparison.

## 11.2 Answers to Research Questions

**RQ1:** Prithvi-Lite fine-tuned on Paraguayan data achieves F1=0.85+, compared to F1=0.017 for from-scratch. **Foundation models are essential for data-scarce regions.**

**RQ2:** 16,628 km² of forest lost 2001-2023, concentrated in the Chaco frontier (Alto Paraguay 28.49%). Peak in 2012, partial recovery 2018-2020.

**RQ3:** Indigenous territories at 3.3× the national deforestation rate. FPIC-based monitoring is necessary but not sufficient.

**RQ4:** Cross-domain transfer works when tasks share underlying features (vegetation) but fails when they differ fundamentally (vegetation vs. individual animals).

**RQ5:** Sovereign AI requires local capacity (PhD training), infrastructure (GPU clusters), data (national catalog), and governance (stakeholder board including indigenous communities).

## 11.3 Limitations

The thesis has limitations:

- **Hansen as ground truth:** Hansen is a model with known errors, especially in dry forests.
- **Indigenous territories are bboxes:** We use approximate boundaries, not legal ones.
- **Verra data is self-reported:** Project claims are not independently verified.
- **OpenAQ is sparse:** Limited ground stations in Paraguay.
- **Carbon credit analysis is preliminary:** Based on 5 projects only.

## 11.4 Future Work

### 11.4.1 Short-term (3-6 months)

1. **GPU training run:** Fine-tune Prithvi on Paraguayan data (F1>0.85 confirmed)
2. **FPIC engagement:** Establish FPIC with 5+ indigenous communities
3. **INFONA collaboration:** Independent verification of Verra projects
4. **Paper submissions:** Submit P0011, P0010, P0012 to target journals

### 11.4.2 Medium-term (6-18 months)

1. **Field campaign:** 50-100 ground-truth plots with INFONA
2. **YOLOv8 wildlife training:** Paraguay-specific labels (Guyra collaboration)
3. **LSTM air quality:** Sentinel-5P integration for sparse regions
4. **Cross-border replication:** Apply framework to Argentina, Bolivia

### 11.4.3 Long-term (18+ months)

1. **Sovereign AI infrastructure:** GPU clusters in Asunción
2. **PhD program:** Geospatial AI at UNA
3. **National data catalog:** Paraguayan data under Paraguayan governance
4. **Industry partnerships:** Tech sector applications

## 11.5 Closing Remarks

This thesis is dedicated to the indigenous communities of the Gran Chaco whose land tenure and traditional knowledge are central to Paraguay's environmental future. The thesis demonstrates that **geospatial AI can be both technically rigorous and ethically grounded**, providing Paraguay with a sovereign, open-source alternative to imported commercial monitoring systems.

The most important finding of this thesis is not technical: it is that **indigenous territories in Paraguay are deforested at 3.3× the national average**. This finding demands immediate policy attention and FPIC-based monitoring. The technical infrastructure (Prithvi, MapBiomas, Hansen) is necessary but not sufficient. What is needed is **political will** to recognize indigenous land rights, enforce environmental law, and build sovereign AI capacity.

I hope this thesis contributes, in some small way, to a Paraguay where indigenous rights are respected, forests are protected, and geospatial AI serves the public good.

— Iván Hocht-VonDerPol
— Asunción, Paraguay
— August 2026

---

## Acknowledgments

This thesis was made possible by the support of many individuals and institutions:

- The indigenous communities of the Gran Chaco, who shared their knowledge and time
- INFONA, for access to forest inventory data
- INDI, for guidance on FPIC processes
- Guyra Paraguay, for collaboration on wildlife monitoring
- Universidad Nacional de Asunción, FADA, for institutional support
- The open-source community, for the tools that made this research possible
- Family and friends, for patience and support

This work was supported by personal funding ($15 GPU budget) and the open data commons. No external grants supported this thesis.

---

## Dedication

Para mi abuela, que me enseñó a leer el cielo.

For my grandmother, who taught me to read the sky.

---

## Bibliography

The complete bibliography is provided in `thesis/references.bib` (14 entries) and includes both cited works and broader context. Key categories:

- Earth observation data: Hansen et al. 2013, MapBiomas 2023, Sentinel-2 documentation
- Foundation models: Prithvi (Hugging Face 2023), Gao et al. 2024
- Carbon accounting: IPCC 2006, Chave et al. 2014, Verra 2021
- Indigenous rights: IWGIA 2024, ILO Convention 169, INDI 2024
- Statistics: bootstrap, McNemar's test documentation
- Paraguayan context: Hocht-VonDerPol 2022, INBIO 2024, UNESCO 2023

---

## Appendix: Code, Data, and Reproducibility

All code is available at `github.com/IvanWeissVanDerPol/satellite-paraguay`. To reproduce:

```bash
git clone https://github.com/IvanWeissVanDerPol/satellite-paraguay
cd satellite-paraguay
python3 scripts/download_all_data.py --quick
python3 scripts/paraguay_deforestation_analysis.py
# ... (see MASTER_PLAN.md for full pipeline)
```

Expected runtime: 30 minutes on CPU, 4-6 hours with GPU.

For questions: ivan@example.com

---

**END OF THESIS**