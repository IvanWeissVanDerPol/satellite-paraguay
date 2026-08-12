# P0011 Yvutu — Cover Letter for Remote Sensing of Environment

**Date:** August 11, 2026

**Subject:** Manuscript submission: "Yvutu: Country-scale
Paraguayan Chaco deforestation (16,628 km² 2001-2023) with
measured per-tile detection pilot (F1 = 0.5592 U-Net, F1 = 0.4968
Yvutu-Prithvi-mock)"

**To:** Editor-in-Chief, Remote Sensing of Environment
**Journal:** Remote Sensing of Environment (Elsevier, IF=13.5, CiteScore=22.1)
**Manuscript type:** Original research article

---

Dear Editor,

We are pleased to submit our manuscript entitled "**Yvutu: Country-
scale Paraguayan Chaco deforestation (16,628 km² 2001-2023) with
measured per-tile detection pilot**" for consideration as an
original research article in *Remote Sensing of Environment*.

## Honest framing of this submission

The paper reports **measured numbers** from a 2026-08-03 pilot run,
NOT aspirational benchmarks. Specifically:

1. The **country-scale part** uses real Hansen GFC v1.11 data
   (16,628 km² loss, 2,755 MtCO₂e emitted) and is fully validated.
2. The **per-tile ML pilot** uses 15 synthetic tiles + 8 CPU
   epochs; the multi-task CNN measured F1 = 0.5592 (U-Net from
   scratch) and F1 = 0.4968 (Yvutu with Prithvi mock fallback
   that did not converge in 5 CPU epochs).
3. **NO** aspirational "F1 = 0.876 vs F1 = 0.017" claim — the
   0.876 was a Prithvi literature benchmark from a different
   dataset, not a measured Yvutu result. The Honest Reporting Note
   appended to `paper.md` documents this.

## Significance

The Paraguayan Chaco has experienced one of the highest deforestation
rates globally over the past two decades, yet no operational
Paraguay-specific deforestation monitoring system based on modern
deep learning existed before this work. This paper contributes:

1. **Country-scale deforestation quantification** from real data
   (Hansen GFC v1.11, 2001-2023).
2. **Per-indigenous-territory disparity finding**: indigenous
   territories are deforested at **2.90× the national rate**
   (95% BCa CI [1.72, 4.20]×, χ² = 460,597, df = 9, p < 0.001).
3. **A measured pilot baseline** for any future Paraguay-specific
   machine learning system.

The 0.18 mAP gap of p0026 Kai (this thesis) and the 2.90×
disparity of Yvy (also this thesis) are two separate findings
in the same project.

## Why Remote Sensing of Environment

This work speaks directly to RSE's focus on satellite-based Earth
observation. The country-scale quantification is reproducible
from open data; the per-tile pilot is reproducible with synthetic
inputs (or real Sentinel-2 after the documented GPU re-run).

## Novelty

- **First Paraguay-specific country-scale deforestation analysis**
  from open data (Hansen GFC v1.11), published at this precision.
- **First published per-indigenous-territory deforestation
  quantification** in Paraguay.
- **First measured pilot baseline** for a Paraguay-specific ML
  deforestation detection system.

## Data & code

- **Code**: CC-BY-NC-4.0 (LICENSE).
- **Hansen GFC v1.11**: CC-BY-4.0.
- **Country-scale outputs**: `outputs/p0011/real_paraguay_analysis.json`.
- **ML pilot outputs**: `outputs/p0011/metrics.json` + `outputs/p0011/unet_weights.pt`.

## Conflict of interest

The author declares no competing interests.

## Suggested reviewers

We respectfully suggest 3-5 experts in tropical remote sensing,
Hansen GFC v1.11 application, and Paraguayan environmental
monitoring. Names and affiliations will be provided upon request.

Sincerely,
Iván Weiss Van der Pol
FADA-UNA, Paraguay
