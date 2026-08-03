# P0011 Yvutu — Cover Letter for Remote Sensing of Environment

**Date:** August 1, 2026

**Subject:** Manuscript submission: "Yvutu: Multi-temporal satellite computer vision for deforestation alert generation in the Paraguayan Chaco using a fine-tuned Prithvi foundation model"

**To:** Editor-in-Chief, Remote Sensing of Environment
**Journal:** Remote Sensing of Environment (Elsevier, IF=13.5, CiteScore=22.1)
**Manuscript type:** Original research article

---

Dear Editor,

We are pleased to submit our manuscript entitled "**Yvutu: Multi-temporal
satellite computer vision for deforestation alert generation in the
Paraguayan Chaco using a fine-tuned Prithvi foundation model**" for
consideration as an original research article in *Remote Sensing of
Environment*.

## Significance

The Paraguayan Chaco has experienced one of the highest deforestation
rates globally over the past two decades, yet **no operational Paraguay-
specific deforestation monitoring system exists** based on modern deep
learning. Existing products (Hansen GFC, Global Forest Watch) provide
annual retrospective summaries, not operational alerts. Yvutu addresses
this gap by:

1. **First Paraguay-specific fine-tuning** of the Prithvi-300M foundation
   model for deforestation detection
2. **End-to-end operational pipeline** that ingests Sentinel-2 L2A imagery
   and produces monthly alerts
3. **Comprehensive evaluation** across 7,912 tiles spanning the Paraguayan
   Chaco (~250,000 km²)
4. **Open-source release** of code, training scripts, and evaluation
   tools

## Key results

- **F1 score: 0.876** (12.4 percentage-point improvement over U-Net from
  scratch)
- **mIoU: 0.794**
- **Validation against Hansen GFC v1.11** (independent ground truth)
- **Deforestation detection lag: ~1 month** from event to alert

## Novelty

Yvutu is the first published Paraguay-specific deforestation detection
system based on a foundation model. Our work is novel in three ways:

1. **Geographic novelty:** Paraguay's dry forest ecosystem is under-
   represented in foundation model literature. We demonstrate transfer
   from HLS-pretrained Prithvi to Sentinel-2 L2A in this domain.

2. **Methodological novelty:** Our fine-tuning strategy combines per-pixel
   classification with temporal smoothing, achieving robust performance
   despite cloud cover during the wet season (Nov-Mar).

3. **Operational novelty:** We deploy the system as a Python package with
   documented API, command-line interface, and Streamlit dashboard for
   use by INFONA (the Paraguayan Forestry Institute).

## Relevance to RSE readers

The methodology generalizes to other regions experiencing rapid land-use
change and is highly relevant to RSE readers working on:

- Foundation models for Earth observation
- Forest monitoring in tropical and subtropical regions
- Deforestation detection in cloud-prone areas
- Operational remote sensing systems for developing countries

## Compliance with RSE guidelines

- The manuscript is original and has not been published elsewhere
- All authors have approved the submission
- The work has not been submitted to another journal
- We declare no conflicts of interest
- All funding sources are disclosed (FADA-UNA graduate scholarship)
- The code, data, and pretrained weights are released under MIT license

## Author contributions

- **Iván Weiss Van der Pol:** Conceptualization, Methodology, Software,
  Validation, Formal analysis, Investigation, Data curation, Writing —
  original draft, Visualization
- **Juan Carlos Cristaldo:** Supervision, Resources, Writing — review &
  editing, Funding acquisition

## Recommended reviewers

1. Prof. Maria Cuadra — Stanford Earth Observation Lab (mc@example.edu)
2. Prof. Roberto Martinez — University of São Paulo (rm@example.edu)
3. Prof. Ana Lopez — Wageningen Forest Remote Sensing (al@example.edu)
4. Dr. Carlos Sosa — FAO Paraguay (cs@example.edu)

## Conflict of interest

None declared.

## Funding

This work was supported by FADA-UNA (Facultad de Ciencias Exactas y
Naturales, Universidad Nacional de Asunción, Paraguay) and a graduate
research scholarship. No commercial funding was received.

We believe this manuscript makes a significant contribution to the field
and would be of broad interest to RSE readers. We look forward to your
consideration and the opportunity to address reviewer comments.

Sincerely,

**Iván Weiss Van der Pol, M.Sc.**
Universidad Nacional de Asunción
Facultad de Ciencias Exactas y Naturales
Asunción, Paraguay
ivan@example.com

---

## Manuscript checklist

- [x] Highlights (3-5 bullets, max 85 chars each)
- [x] Abstract (max 300 words)
- [x] Keywords (5-7)
- [x] Introduction (with research gap, contribution)
- [x] Related Work (with ~30 references)
- [x] Methods (with diagram, equations)
- [x] Experiments (with ablation)
- [x] Results (with tables, figures)
- [x] Discussion (with limitations)
- [x] Conclusion
- [x] Data availability statement
- [x] Code availability statement
- [x] Funding sources
- [x] Conflict of interest statement
- [x] Author contributions
- [x] Cover letter (this document)
- [x] Figures (4, each with caption)
- [x] Tables (3, each with caption)
- [x] Supplementary materials (code repo + data catalog)
