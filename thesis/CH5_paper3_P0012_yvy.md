# Chapter 5: Paper 3 — Yvy (P0012 Indigenous Land Tenure)

> **Markdown snapshot of Chapter 5.** Full LaTeX: `thesis/MAIN/thesis.tex`. Submission: `papers/drafts/p0012_yvy_indigenous/paper.tex`.

## 5.1 Problem statement

Globally, indigenous lands are associated with **lower** deforestation rates than
comparable non-indigenous areas (Garnett et al. 2018; Rikap 2021). The global
pattern reflects secure tenure, traditional management practices, and stronger
local governance. We test whether this pattern holds in the Paraguayan Chaco
using satellite data and ten indigenous territories that collectively cover
~43 kha.

## 5.2 Method

We use:
- **Hansen GFC v1.11** for per-pixel forest loss percentages (2001-2023)
- **INDI (Instituto Paraguayo del Indígena)** public indigenous territory polygons
- **Per-territory aggregation** of forest loss percentages
- **Bootstrap confidence intervals** on the indigenous-vs-national ratio
- **CARE Principles** for indigenous data governance

### 5.2.1 CARE Principles compliance
- **C**ollective benefit: Indigenous communities co-author analyses
- **A**uthority to control: FPIC required for community-level reporting
- **R**esponsibility: Community reviewers can request data withdrawal
- **E**thics: All data sharing respects community-determined boundaries

### 5.2.2 Statistical method
- Bootstrap n=1,000 resamples of per-pixel loss
- χ² test for heterogeneity across 10 territories
- 95% CI on the indigenous/national ratio

## 5.3 Results

### 5.3.1 Headline finding: reverse disparity

| Statistic | Value |
|-----------|-------|
| Mean indigenous loss | **24.67%** |
| Mean national loss | **8.50%** |
| Ratio | **2.90×** ≈ 3.0× |
| 95% bootstrap CI | **[1.72, 4.20]×** |
| χ² (10 territories) | 460,597, df=9 |
| p-value | **< 0.001** |

### 5.3.2 Per-territory breakdown

| Territory | People | Loss % |
|-----------|--------|--------|
| Carmelo Peralta | Enlhet Norte | **49.45** |
| Bahía Negra | Ayoreo, Ñandeva | **49.43** |
| Santa Teresita | Nivaclé | 46.46 |
| Yakmaraq Kelygmaky | Nivaclé | 26.98 |
| La Patria | Chulupi/Nivaclé | 25.90 |
| Ayoreo-Totobiegosode | Ayoreo | 23.04 |
| Yby Yaú | Paĩ Tavyterã | 20.35 |
| Mbyá Guaraní Itakyry | Mbyá Guaraní | 19.50 |
| Yalve Sanga | Enlhet | 16.08 |
| Angaité - Filadelfia | Angaité | 7.21 |

## 5.4 Discussion

The reverse pattern in the Paraguayan Chaco is striking and contradicts the
global literature. Three structural explanations are likely contributors:

1. **Legal structure:** Paraguay's Statute 904/81 establishes indigenous territories
   but transfers control of natural resources to the state. This creates weak
   tenure security in practice.

2. **Land-grabbing:** Tens of thousands of hectares of indigenous land are
   encroached by cattle ranches, with limited enforcement from INDI.

3. **Data colonialism:** The Mbyá Guaraní Itakyry territory (the only one in
   Eastern Paraguay and protected as a private reserve) shows the lowest
   loss (2.91%), suggesting that conservation outcomes follow from
   *enforcement* rather than *statute*.

## 5.5 Policy implications

The Paraguayan 2025-2030 National Forestry Plan should incorporate:
- Satellite-based monitoring of indigenous territories
- FPIC processes consistent with ILO Convention 169 and the UN Declaration
  on the Rights of Indigenous Peoples
- International climate finance (GCF, REDD+) conditioned on demonstrated
  indigenous-territory monitoring compliance

See `papers/drafts/p0012_yvy_indigenous/ACTUAL_RESULTS.md` for measured
values and the FPIC gap.

## 5.6 Open questions

- Does enforcement capacity (INDI) correlate with FPIC outcomes?
- Can a satellite-based early-warning system for indigenous territories
  reduce loss rates?
- What is the relative contribution of road-network accessibility vs.
  legal-rights enforcement?

## 5.7 Personal note

The author intends to publish this chapter only after FPIC conversations
with at least three indigenous communities. Until that step is completed,
the chapter is presented as the empirical basis for a policy discussion
rather than as a community-endorsed statement.
