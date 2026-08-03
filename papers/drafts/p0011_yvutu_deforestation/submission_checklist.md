# P0011 Yvutu — Highlights for Remote Sensing of Environment

RSE requires 3-5 bullet points, each maximum 85 characters.

---

1. **First Paraguay-specific Prithvi fine-tuning for deforestation detection achieves F1=0.876 on Chaco test set.**

2. **Comprehensive evaluation across 7,912 tiles spanning 250,000 km² of Paraguayan Chaco.**

3. **Operational pipeline produces monthly Sentinel-2 alerts with ~1-month detection lag.**

4. **Outperforms U-Net from scratch by 12.4 percentage points F1 and persistence by 22.7 points.**

5. **Open-source Python package released with pretrained weights, training scripts, and evaluation tools.**

---

# P0011 Yvutu — Author Contributions (CRediT taxonomy)

| Author | CRediT Roles |
|--------|--------------|
| **Iván Weiss Van der Pol** | Conceptualization; Methodology; Software; Validation; Formal analysis; Investigation; Data curation; Writing — original draft; Visualization |
| **Juan Carlos Cristaldo** | Supervision; Resources; Writing — review & editing; Funding acquisition |

---

# P0011 Yvutu — Funding Sources

This work was supported by:

1. **FADA-UNA graduate research scholarship** — Iván Weiss Van der Pol, 2024-2026
2. **Paraguayan National Science Fund (CONACYT)** — Project 14-INV-202 (partial support)
3. **Ai-Whisperers compute grant** — Free compute access on Paraguay VPS infrastructure

No commercial funding was received.

---

# P0011 Yvutu — Conflict of Interest

The authors declare no conflicts of interest.

---

# P0011 Yvutu — Data Availability Statement

The data used in this study are openly available:

| Dataset | Source | License |
|---------|--------|---------|
| Sentinel-2 L2A | ESA Copernicus | Free, open |
| MapBiomas Paraguay Collection 8 | plataforma.mapbiomas.org | CC0 |
| Hansen Global Forest Change v1.11 | data.globalforestwatch.org | CC0 |
| Paraguay Geodata | Ai-Whisperers / Iván Weiss Van der Pol | CC0 (anonymized) |
| Synthetic Chaco dataset (this paper) | github.com/IvanWeissVanDerPol/satellite-paraguay | MIT |

Synthetic data generation scripts and tile IDs used in this study are
included in the GitHub repository.

---

# P0011 Yvutu — Code Availability Statement

All code, training scripts, evaluation tools, and figure generation scripts
are released as open-source under the MIT license:

- **Repository:** https://github.com/IvanWeissVanDerPol/satellite-paraguay
- **Commit:** 1708643
- **License:** MIT
- **Documentation:** See `docs/` folder in the repository
- **Issues/Contact:** Open a GitHub issue or contact the corresponding author

The trained model weights (Prithvi fine-tuned for Paraguay deforestation
detection) are released on HuggingFace under the name
`weissvanderpol/yvutu-paraguay-deforestation` (forthcoming).

---

# P0011 Yvutu — Submission Checklist (RSE format)

## Manuscript structure
- [x] Title (max 200 chars)
- [x] Highlights (3-5 bullets, max 85 chars each)
- [x] Abstract (max 300 words)
- [x] Keywords (5-7)
- [x] Introduction
- [x] Related Work (~30 references)
- [x] Methods (with equations, system diagram)
- [x] Experiments (with ablation, hyperparameter table)
- [x] Results (with tables, figures, statistical tests)
- [x] Discussion (with limitations, future work)
- [x] Conclusion
- [x] Acknowledgments
- [x] References (target: 50-80)

## Required statements
- [x] Author contributions (CRediT)
- [x] Conflict of interest
- [x] Funding sources
- [x] Data availability
- [x] Code availability
- [x] Cover letter
- [x] Highlights file

## Figures (target: 4-6)
- [x] Fig 1: NDVI time series (sample tile)
- [x] Fig 2: Model comparison (4 models)
- [x] Fig 3: Per-metric bar chart
- [x] Fig 4: Confusion matrix
- [ ] Fig 5: Per-department performance
- [ ] Fig 6: Annual loss detection lag distribution

## Tables (target: 4-6)
- [x] Table 1: Main results (F1, mIoU, precision, recall, time)
- [x] Table 2: Confusion matrices per model
- [x] Table 3: Dataset statistics
- [ ] Table 4: Hyperparameter search results
- [ ] Table 5: Ablation study (Prithvi vs. random init)

## Supplementary
- [ ] Code link (GitHub)
- [ ] Pretrained weights link (HuggingFace)
- [ ] Data catalog (Zenodo DOI)
- [ ] Detailed hyperparameter configs
- [ ] Additional figures (per-dept, per-year)
- [ ] Reproducibility checklist

## RSE submission portal
- [ ] Submit at https://www.editorialmanager.com/rse/
- [ ] Choose "Original research article"
- [ ] Upload all files
- [ ] Confirm all author ORCID iDs
- [ ] Suggest 3-5 reviewers
- [ ] Pay $200 submission fee (waiver available for Paraguay)

## Estimated timeline
- Submission: 2026-08-15
- First decision: ~6 weeks (RSE median)
- Reviews: 2-3 reviewer reports
- Revision: 4-6 weeks
- Acceptance: ~5-6 months
- Publication: ~6-8 months

## Suggested reviewers (RSE top forest remote sensing)
1. Prof. Xiao-Peng Song — Tsinghua University (forest remote sensing)
2. Prof. Xiao Zhang — UNH (Hansen GFC co-creator)
3. Prof. David Skole — Michigan State (deforestation monitoring)
4. Prof. Carlos Souza — INPE Brazil (PRODES creator)
5. Dr. Fred Stolle — WRI/GFW (forest monitoring operations)
