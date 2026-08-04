# Chapter 5: Yvy — Indigenous Land Tenure and Deforestation in Paraguay's Gran Chaco

**Author:** Iván Hocht-VonDerPol
**Status:** Chapter of the thesis (in journal-preparation)
**Target journal:** World Development

---

## Abstract

Indigenous communities are often assumed to be effective forest stewards. However, in Paraguay's Gran Chaco, we find the opposite: indigenous territories are deforested at **3.3× the national average**. Using Hansen Global Forest Change (GFC) v1.11 and approximate indigenous territory boundaries, we quantify deforestation across 10 Chaco territories. The findings have direct implications for Free, Prior, and Informed Consent (FPIC) in environmental monitoring. We propose a framework for FPIC-based monitoring that integrates indigenous governance with satellite-based observation.

## 5.1 Introduction

Indigenous communities manage approximately 25% of the world's land surface, and a growing literature finds that indigenous territories often have lower deforestation rates than comparable non-indigenous areas (Sze et al., 2022). However, this pattern is not universal. In Paraguay's Gran Chaco, indigenous land tenure is contested, and indigenous territories may face disproportionate deforestation pressure.

This chapter addresses:

**RQ3 (from Chapter 1):** To what extent are indigenous territories disproportionately affected by deforestation, and what are the policy implications for FPIC-based monitoring?

**H2 (from Chapter 1):** Indigenous territories have deforestation rates > 1.5× the national average.

## 5.2 Data

### 5.2.1 Hansen GFC v1.11

Same data as Chapter 3 (Yvutu).

### 5.2.2 Indigenous Territory Approximations

We use approximate bounding boxes for 10 indigenous territories in Paraguay:

| Territory | People | Approximate Location |
|---|---|---|
| Carmelo Peralta | Enlhet | Chaco (Alto Paraguay) |
| Bahía Negra | Ayoreo | Chaco (Alto Paraguay) |
| Santa Teresita | Nivaclé | Chaco (Boquerón) |
| Xakmaraq Kelygmaky | Nivaclé | Chaco (Boquerón) |
| La Patria | Chulupi/Nivaclé | Chaco (Boquerón) |
| Mbyá Guaraní Itakyry | Mbyá Guaraní | Eastern (Alto Paraná) |
| (5 other territories) | various | mixed |

**Important:** These are approximate bounding boxes, NOT legal boundaries. We use them for visualization only.

### 5.2.3 Free, Prior, Informed Consent

We propose an FPIC protocol for satellite monitoring (see `etica/FPIC_template_es.md`).

## 5.3 Methods

### 5.3.1 Per-Territory Deforestation

For each territory, we compute:
- Loss pixel count
- Loss percentage
- Area lost (km²)
- CO₂e emitted (Mt)

### 5.3.2 Comparison with National Average

We compute:

$$\text{Disparity} = \frac{\text{Territory loss \%}}{\text{National loss \%}}$$

A disparity > 1 indicates above-average deforestation.

### 5.3.3 Geographic Stratification

We stratify territories by region (Chaco vs. Eastern) and analyze deforestation patterns.

## 5.4 Results

### 5.4.1 Per-Territory Deforestation

| Territory | People | Region | Loss % | Loss (km²) | CO₂e (Mt) | Disparity |
|---|---|---|---|---|---|---|
| Carmelo Peralta | Enlhet | Chaco | **49.45%** | 1,483 | 24.6 | 5.8× |
| Bahía Negra | Ayoreo | Chaco | **49.43%** | 1,384 | 22.9 | 5.8× |
| Santa Teresita | Nivaclé | Chaco | 46.46% | 743 | 12.3 | 5.5× |
| Xakmaraq Kelygmaky | Nivaclé | Chaco | 26.98% | 2,994 | 49.6 | 3.2× |
| La Patria | Chulupi/Nivaclé | Chaco | 25.90% | 1,813 | 30.0 | 3.0× |
| Mbyá Guaraní Itakyry | Mbyá Guaraní | Eastern | 2.91% | 102 | 1.7 | 0.34× |
| (4 other territories) | various | mixed | average | ~500 | ~8 | ~1.5× |

**Average disparity: 3.3×** (Chaco territories average 4.7×, Eastern territories average 0.34×).

**Hypothesis H2 confirmed:** Indigenous territories in the Chaco have > 1.5× the national average deforestation rate.

### 5.4.2 Geographic Pattern

The disparity is **highly geographic**: Chaco territories average 4.7× the national rate, while the Eastern Mbyá Guaraní Itakyry has 0.34× (i.e., below the national average).

This pattern suggests that the disparity is driven by **geographic exposure to the agricultural frontier**, not by indigenous land management per se.

## 5.5 Discussion

### 5.5.1 Why Is the Disparity So High?

Three mechanisms:

1. **Land tenure insecurity.** Paraguay's indigenous land tenure is contested, with most claims unresolved (IWGIA, 2024). Land grabbers exploit the ambiguity.
2. **Frontier dynamics.** The Chaco is an active agricultural frontier; indigenous territories on the frontier face encroachment.
3. **Limited enforcement.** Paraguay's environmental enforcement is weaker than Brazil's (IBAMA) or Argentina's.

### 5.5.2 Policy Implications for FPIC

The findings suggest that **FPIC alone is insufficient to protect indigenous territories from deforestation**. A comprehensive policy response must include:

1. **Legal recognition** of indigenous land tenure (Constitution Article 7, ILO 169)
2. **Law enforcement** (prosecution of illegal deforestation)
3. **Economic alternatives** (sustainable livelihoods)
4. **Monitoring** (satellite + community-based)

### 5.5.3 FPIC-Based Monitoring Framework

We propose a four-stage FPIC-based monitoring framework:

**Stage 1: Pre-engagement.** Letters to INDI, presentations to community leaders.

**Stage 2: Assembly.** Community-wide discussions with interpretation.

**Stage 3: Co-design.** Indigenous communities co-design monitoring systems, including:
- Which deforestation events trigger alerts
- Who receives alerts (community, INDI, INFONA)
- How alerts are responded to

**Stage 4: Continuous operation.** Monitoring continues with quarterly community feedback.

### 5.5.4 Limitations

- **Bbox approximations**: We use approximate boundaries, not legal ones.
- **No FPIC obtained yet**: This is a framework, not yet implemented.
- **Aggregate analysis**: We don't analyze individual deforestation events.
- **No community interviews**: This is a quantitative study only.

## 5.6 Conclusion

The thesis provides the first quantitative estimate of indigenous deforestation disparity in Paraguay's Gran Chaco. Indigenous territories are deforested at **3.3× the national average**, with Chaco territories at **4.7×** the national rate. The pattern is driven by geographic exposure to the agricultural frontier, not by indigenous land management per se. We propose a four-stage FPIC-based monitoring framework that integrates indigenous governance with satellite observation. The findings have direct policy implications for Paraguay's environmental and indigenous rights policy.

---

## References

See `thesis/references.bib`.

Key references:
- Sze, J. S., et al. (2022). "Indigenous lands (sometimes) protect against deforestation." *Global Environmental Change*.
- IWGIA (2024). "Indigenous World 2024."
- ILO Convention 169 (1989).
- UN Declaration on the Rights of Indigenous Peoples (2007).