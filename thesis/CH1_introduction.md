---
title: "Chapter 1 — Introduction"
author: "Iván Hocht-VonDerPol"
date: "2026-08-04"
---

# Chapter 1: Introduction

## 1.1 The Gran Chaco Problem

The Gran Chaco is the second-largest forested biome in South America after the Amazon, covering approximately 1,000,000 km² across Paraguay, Argentina, Bolivia, and a small portion of Brazil. Within Paraguay, the Chaco region represents 61% of the national territory (24.7 million hectares) and contains the largest remaining tracts of dry forest in the country. However, the Gran Chaco is also one of the world's most active deforestation frontiers, with rates of forest loss exceeding 1% per year in the early 21st century (Hansen et al., 2013).

This deforestation has substantial consequences at three levels:

**At the global level**, the Paraguayan Chaco contributes to climate change through carbon emissions. Using the Hansen Global Forest Change (GFC) v1.11 dataset, we estimate that **16,628 km² of Paraguayan forest cover was lost between 2001 and 2023**, equivalent to **2,755 MtCO₂e** (assuming a mean treecover of 50% and IPCC carbon conversion factors). This represents a significant share of South American land-use emissions.

**At the national level**, deforestation is unevenly distributed across Paraguay's 18 departments. The Chaco frontier departments—Alto Paraguay, Boquerón, and Presidente Hayes—account for the majority of absolute forest loss, with **Alto Paraguay alone losing 28.49% of its forest cover during the study period**. This concentration of deforestation has implications for agricultural policy, food security, and rural livelihoods.

**At the local level**, the costs of deforestation are borne disproportionately by indigenous communities. We find that the ten indigenous territories in the Gran Chaco have an average deforestation rate of **28.4%**, which is **3.3 times the national average** of 8.5%. This finding raises serious environmental justice concerns and is the central empirical contribution of this thesis.

## 1.2 The Geospatial AI Gap

Despite these stakes, Paraguay faces a significant capacity gap in geospatial artificial intelligence (AI). Most monitoring systems for Paraguayan deforestation are operated by foreign institutions (Hansen/UMD, Global Forest Watch, MapBiomas Paraguay, INPE Brazil), and the country lacks the local research infrastructure to develop independent, contextually-aware monitoring systems.

Three specific challenges characterize this gap:

**Challenge 1: Data sovereignty.** Paraguay produces extensive environmental data (forest inventories, indigenous land registries, air quality measurements) but lacks the local computational capacity to convert this data into actionable insights. Foreign organizations that process this data often retain control over the resulting analytics.

**Challenge 2: Methodological transferability.** Algorithms developed for tropical rainforests (e.g., the Amazon) often perform poorly in dry forests (e.g., the Chaco). The smaller canopy, distinct phenology, and more subtle deforestation signals require adaptation.

**Challenge 3: Stakeholder integration.** Existing monitoring systems rarely integrate the perspectives of indigenous communities, smallholder farmers, and local government. This limits their effectiveness and legitimacy.

## 1.3 Research Questions

To address these challenges, this thesis poses five research questions:

**RQ1 (Foundational Modeling):** Can open-source foundation models (Prithvi, SatMAE) fine-tuned on multi-temporal Sentinel-2 imagery achieve state-of-the-art performance on Paraguayan land-use tasks, despite limited labeled training data?

**RQ2 (Country-Scale Deforestation):** What are the spatial, temporal, and departmental patterns of deforestation in Paraguay 2001-2023, and how do they relate to land tenure, agricultural expansion, and indigenous community boundaries?

**RQ3 (Environmental Justice):** To what extent are indigenous territories disproportionately affected by deforestation, and what are the policy implications for FPIC-based monitoring?

**RQ4 (Cross-Domain Generalization):** How well does a model trained on one Paraguayan land-use task (e.g., deforestation) generalize to other tasks (e.g., crop yield, air quality, poaching detection)?

**RQ5 (Sovereign AI):** What pipeline architecture and governance model enable Paraguay to deploy geospatial AI without relying on commercial foreign providers?

## 1.4 Hypotheses

We propose three hypotheses derived from these research questions:

**H1 (Foundation Models Superiority):** A Prithvi-fine-tuned model achieves F1 > 0.85 on Paraguayan deforestation detection, compared to F1 < 0.30 for a from-scratch U-Net baseline.

**H2 (Indigenous Deforestation Disparity):** Indigenous territories in Paraguay have deforestation rates greater than 1.5 times the national average.

**H3 (Cross-Domain Transfer):** A deforestation-pretrained model achieves at least 0.7× the accuracy of a yield-prediction-trained model on the yield prediction task (positive transfer).

These hypotheses are tested in the empirical chapters (Chapters 3-8) and synthesized in Chapter 9.

## 1.5 Contributions

This thesis makes three contributions:

**Contribution 1: A unified framework.** We develop six reproducible pipelines (Yvutu, Yvyra, Yvy, Yrupe, Kai, Tatakua) integrated into a single open-source repository (`satellite-paraguay`). These pipelines cover deforestation, carbon credits, indigenous conflict, crop yield, wildlife poaching, and air quality.

**Contribution 2: An empirical finding.** We provide the first quantitative estimate of the deforestation disparity affecting indigenous territories in Paraguay, finding a 3.3× multiplier compared to the national average. This finding has direct policy implications for FPIC-based monitoring.

**Contribution 3: A methodology.** We propose a rights-aware deployment methodology that integrates Free, Prior, and Informed Consent (FPIC) for indigenous communities, IRB approval for human-subjects data, and federated states for cross-border comparison. This methodology can be replicated in other contexts.

## 1.6 Thesis Outline

The thesis is organized as follows:

**Chapter 2 (Methodology):** Describes the data sources, computational pipelines, evaluation methodology, and ethical framework.

**Chapter 3 (Yvutu Deforestation):** Tests H1 using multi-temporal Sentinel-2 and Hansen GFC data on a real Paraguayan deforestation case study.

**Chapter 4 (Yvyra Carbon):** Integrates Verra registry data with Hansen deforestation to assess carbon credit integrity.

**Chapter 5 (Yvy Indigenous):** Cross-references Hansen deforestation with indigenous territory boundaries to quantify the 3.3× disparity.

**Chapter 6 (Yrupe Yield):** Tests H3 by transferring a deforestation-pretrained model to soybean yield prediction.

**Chapter 7 (Kai Poaching):** Tests wildlife detection using YOLOv8 on Paraguayan Chaco fauna.

**Chapter 8 (Tatakua Air Quality):** Tests LSTM-based air quality forecasting using OpenAQ data.

**Chapter 9 (Cross-Cutting Analysis):** Synthesizes findings across the six papers, addressing RQ4.

**Chapter 10 (Discussion):** Discusses implications for policy, science, and AI ethics.

**Chapter 11 (Conclusion):** Summarizes contributions, acknowledges limitations, and proposes future work.

## 1.7 Reading Guide

The thesis can be read in multiple ways:

**For Paraguay researchers:** Focus on Chapter 5 (Yvy indigenous) and Chapter 10 (Discussion) for policy implications.

**For ML researchers:** Focus on Chapter 3 (Yvutu) for the foundation model comparison, and Chapter 9 (Cross-Cutting) for transfer learning.

**For sustainability researchers:** Focus on Chapter 4 (Yvyra carbon) and Chapter 9 for cross-domain findings.

**For AI ethics researchers:** Focus on Chapter 2 (Methodology) for the FPIC framework and Chapter 10 (Discussion) for synthesis.

The repo `github.com/IvanWeissVanDerPol/satellite-paraguay` provides the code, data, and reproducibility artifacts referenced throughout.

---

## Chapter 1 References

A complete bibliography is provided in `thesis/references.bib`. Key citations:

- Hansen, M. C., et al. (2013). "High-Resolution Global Maps of 21st-Century Forest Cover Change." *Science* 342(6160): 850-853.
- MapBiomas Paraguay (2023). "MapBiomas Paraguay Collection 2 (2000-2022)."
- NASA-IBM Hugging Face Team (2023). "Prithvi-100M: A Geospatial Foundation Model for Earth Observation."
- IWGIA (2024). "Indigenous World 2024."
- INDI (2024). "Instituto Paraguayo del Indígena."
- Verra (2021). "Verified Carbon Standard (VCS) Program."
- Microsoft (2022). "Microsoft Planetary Computer."
- OpenAQ (2024). "OpenAQ Air Quality Data."
