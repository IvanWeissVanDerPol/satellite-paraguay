# Paper Submission Plan

**Goal:** Submit 6 papers, one per month, to target journals by end of 2027.

## Submission Schedule

### Month 1 (2026-09): P0011 Yvutu → Remote Sensing of Environment
- **Impact factor:** 13.5
- **Submission format:** Original research
- **Co-authors:** Need adviser, optional collaborators
- **Cover letter:** See template below
- **Required materials:**
  - Highlights (3-5 bullet points)
  - Abstract (250 words)
  - Main manuscript (5,000+ words)
  - Figures (5+ publication-quality)
  - Tables (3+ publication-quality)
  - Supplementary materials (data, code, reproducibility)
  - Conflict of interest disclosure
  - Author contributions (CRediT taxonomy)

### Month 2 (2026-10): P0010 Yvyra → Nature Climate Change
- **Impact factor:** 29.6
- **Submission format:** Letter (short, 4-page max)
- **Key innovation:** Verra under-claim discrepancy in Paraguay
- **Required materials:**
  - Letter format (4 pages, 30 references)
  - Display items (1 figure, 1 table)
  - Cover letter emphasizing novelty

### Month 3 (2026-11): P0012 Yvy → World Development
- **Impact factor:** 5.0
- **Submission format:** Original research
- **Key innovation:** 3.0× indigenous deforestation disparity
- **Required materials:**
  - Manuscript (8,000-10,000 words)
  - Strong policy implications
  - FPIC methodology
  - Indigenous co-authors (after FPIC engagement)

### Month 4 (2026-12): P0025 Yrupe → Agricultural Systems
- **Impact factor:** 5.1
- **Submission format:** Original research
- **Key innovation:** Cross-domain transfer from deforestation to yield
- **Required materials:**
  - 8,000 words
  - Real yield data from INBIO
  - Comparison with state-of-the-art

### Month 5 (2027-01): P0026 Kai → Conservation Biology
- **Impact factor:** 5.2
- **Submission format:** Original research
- **Key innovation:** Wildlife detection in Chaco
- **Required materials:**
  - 6,000 words
  - Paraguay-specific wildlife data
  - Comparison with COCO baseline

### Month 6 (2027-02): P0035 Tatakua → Atmospheric Environment
- **Impact factor:** 5.0
- **Submission format:** Original research
- **Key innovation:** LSTM air quality forecasting
- **Required materials:**
  - 8,000 words
  - Real OpenAQ data
  - Sentinel-5P integration

## Cover Letter Templates

### P0011 RSE cover letter

> Dear Editors,
>
> We submit our manuscript "Yvutu: Multi-Temporal Satellite Computer Vision for Chaco Deforestation Detection" for consideration in *Remote Sensing of Environment*.
>
> This paper makes three contributions:
> 1. **Country-scale analysis:** 16,628 km² forest loss 2001-2023 quantified using real Hansen GFC v1.11 data.
> 2. **Foundation model comparison:** Measured U-Net from-scratch achieves F1=0.5592 on 15 synthetic tiles (over-prediction, precision=0.0992); Prithvi-300M fine-tune did not converge within the 5-CPU-epoch budget, falling back to mock F1=0.4968. The earlier aspirational headline (F1>0.85 vs F1=0.017, 50× improvement) is **not measured** — see paper.tex §3 for the honest-reporting note. A real Prithvi run on 150 Chaco tiles is the next step (blocked on GPU budget).
> 3. **Indigenous territory analysis:** 3.0× deforestation disparity in 10 indigenous territories.
>
> The methodology is fully reproducible at github.com/IvanWeissVanDerPol/satellite-paraguay.
>
> We believe this work is well-suited for RSE given the journal's focus on methodological innovation in remote sensing. Our measured pilot numbers (U-Net F1=0.5592 on 15 synthetic tiles; Prithvi mock F1=0.4968 due to non-convergence) replace the aspirational F1>0.85 vs F1=0.017 framing typical of computer-vision papers, in line with RSE's standards for scientific rigor.
>
> All authors have approved the submission. This manuscript is not under consideration elsewhere.
>
> Sincerely,
> Iván Hocht-VonDerPol et al.

### P0012 World Development cover letter

> Dear Editors,
>
> We submit "Indigenous Land Tenure and Deforestation in Paraguay's Gran Chaco" for *World Development*.
>
> This paper documents a striking finding: **indigenous territories in Paraguay's Gran Chaco are deforested at 3.0× the national average**. This contradicts the global pattern (indigenous territories typically protect against deforestation) and warrants urgent policy attention.
>
> We propose a four-stage FPIC-based monitoring framework that integrates Free, Prior, Informed Consent (ILO 169) with satellite-based observation.
>
> The methodology is reproducible. We provide all code, data, and supplementary materials.
>
> Sincerely,
> Iván Hocht-VonDerPol et al.

## Co-Author Strategy

### Phase 1 (months 1-3): Solo author
- P0011, P0010, P0012 submitted with Hocht-VonDerPol as sole author
- After initial submission, invite co-authors for revisions

### Phase 2 (months 4-6): Collaborators
- Add INFONA researcher for P0010 (carbon credit verification)
- Add INDI researcher for P0012 (indigenous rights)
- Add INBIO researcher for P0025 (yield data)
- Add Guyra researcher for P0026 (wildlife)

### Phase 3 (post-defense): Full team
- Adviser as senior author
- All collaborators
- Industry partners (Verra, MapBiomas)

## Reviewer Suggestions

For each paper, suggest 3-5 potential reviewers who are NOT in your network:

### P0011 RSE
- Prof. David Skole (Michigan State, Hansen co-author)
- Prof. Matthew Hansen (UMD, Hansen PI)
- Prof. Mercedes Bustamante (UnB Brasilia, MapBiomas)
- Prof. Raoni Rajão (UFMG, deforestation policy)

### P0010 Nature Climate Change
- Prof. Myles Allen (Oxford, climate metrics)
- Prof. Robert Mendelsohn (Yale, environmental economics)
- Prof. Brendan Mackey (Griffith, REDD+ policy)

### P0012 World Development
- Prof. Arun Agrawal (Michigan, indigenous governance)
- Prof. Peter Carneiro (UCL, field experiments)
- Prof. Esther Duflo (MIT, development economics)

## Timeline

| Date | Milestone | Deliverable |
|---|---|---|
| 2026-08 | Prepare submission materials | Highlights, figures, tables |
| 2026-09 | Submit P0011 | Confirmation email |
| 2026-10 | Submit P0010 | Confirmation email |
| 2026-11 | Submit P0012 | Confirmation email |
| 2026-12 | Submit P0025 | Confirmation email |
| 2027-01 | Submit P0026 | Confirmation email |
| 2027-02 | Submit P0035 | Confirmation email |
| 2027-03 | First reviews received | P0011 review |
| 2027-04 | First revision submitted | P0011 revision |
| 2027-05 | First acceptance | P0011 accepted! |
| 2027-06 | Thesis defense | PhD |

---

## Round-9 status note (2026-09-08)

- `beery2018` now has a verified DOI: `10.1007/978-3-030-01270-0_28` (Round-8 CrossRef verification, score 9.0/11).
- 44 of 45 Round-7 placeholder bib entries remain **unverified** — see `outputs/ROUND_8_VERIFICATION_2026-09-08.md` for the full breakdown. They are NOT safe to cite in any journal submission until each is verified by Ivan against the actual source paper.
- The per-paper bib slices (one per paper in `papers/drafts/p00XX/references.bib`) are auto-generated from `thesis/references.bib` via `scripts/generate_per_paper_bib.py`. They will need re-generation once the Round-7 placeholders are resolved.
- `thesis/main.tex` has 15 active `\input{...}` lines (CH0 abstract, CH00 acknowledgments, CH1-CH11, appendix A, appendix B) and 0 commented-out inputs. The Tier-6 audit-flagged "Emergency stop" build issue is fully resolved.

**This document is updated by Erebus (autonomous agent) based on submission status.**