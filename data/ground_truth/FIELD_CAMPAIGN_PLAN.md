# Field Campaign Operational Plan — Hansen Ground-Truth Validation

**Project:** Yvutu / P0011 Validation
**PI:** Iván Hocht-VonDerPol (Universidad Nacional de Asunción, FADA)
**Field Season:** 2027-03 to 2027-06 (dry season, post-rainy-transition)
**Status:** Plan ready, awaiting UNA IRB approval + UNA FADA partner confirmation
**Version:** 1.0 (2026-08-04)

---

## 1. WHY FIELD CAMPAIGN

The thesis' headline finding — 16,628 km² forest loss, 2,755 Mt CO₂e emitted, 3.0× indigenous disparity (CI [1.7, 4.2]×) — is computed from public satellite data (Hansen GFC v1.11). All numbers are reproducible but **not validated against on-the-ground measurement**.

This plan delivers the anchor: ground-truthed Hansen detection rates. Specifically:
- **Precision** (sensitivity to declared loss events being real)
- **Recall** (sensitivity to real loss being detected by Hansen)
- **F1** (the U-Net baseline reported F1=0.017 — without ground truth that's a number; with ground truth it's a finding)
- **Verra under-claim magnitude validation** (independent biomass measurement)

Without this campaign the thesis is "computational research" in the eyes of remote-sensing reviewers. With it, it's "validation paper."

---

## 2. PLOT DESIGN (FROM `field_plot_design.json`)

| Parameter | Value |
|---|---|
| Total plots | 64 (16 in each stratum per department) |
| Strata | forest_with_loss, forest_no_loss, nonforest_with_loss, nonforest_no_loss |
| Departments | 6 (Alto Paraguay, Boquerón, Presidente Hayes, Concepción, San Pedro, Caaguazú) |
| Plot size | 50 × 50 m (0.25 ha) |
| Plot shape | Square, GPS center ± 5 m |
| Photos per plot | 5 (center + 4 corners) |
| Tree measurements | All trees > 5 cm DBH |
| Biomass variables | DBH (all), height (5 tallest), species list |
| Soil sample | 1 kg from top 30 cm (lab-tested later) |
| Time per plot | 2-3 hours |
| Field season | 12 weeks (Mar–May 2027) |

**Randomization:** 64 plots allocated via stratified random sampling (department × stratum). Target: 4 plots per department-stratum cell × 16 cells = 64. (Some cells under-sampled due to access constraints — final n ≈ 50.)

---

## 3. SCHEDULE

### Phase 1 — Pre-field preparation (Sep–Dec 2026)
| Week | Activity | Owner | Deliverable |
|---|---|---|---|
| W1-2 | Submit IRB to UNA FADA ethics committee | Iván | etica/IRB_submission_packet.md |
| W3-4 | Hire field coordinator (consultant) | Iván | Signed contract |
| W5-6 | Recruit 4 fieldworkers | Coordinator | 4 contracts |
| W7-8 | Equipment procurement (GPS, dendrometer, scale, camera) | Iván | Equipment list (Annex A) |
| W9-10 | Training week (4 days) | Coordinator + Iván | Certificate of training |
| W11 | Pilot week — 4 plots near Asunción | Team | Pilot report |
| W12 | Plan refinement | Iván | Final operational protocol |

### Phase 2 — Field execution (Mar–May 2027)
| Week | Plots | Department |
|---|---|---|
| 13 | 8 | Alto Paraguay (Filadelfia base) |
| 14 | 8 | Alto Paraguay |
| 15 | 8 | Boquerón (Loma Plata base) |
| 16 | 8 | Boquerón |
| 17 | 8 | Presidente Hayes |
| 18 | 8 | Presidente Hayes |
| 19 | 8 | Concepción |
| 20 | 8 | Concepción |
| 21 | 8 | San Pedro |
| 22 | 8 | San Pedro |
| 23 | 8 | Caaguazú |
| 24 | 8 | Caaguazú + return trip |

### Phase 3 — Analysis (Jun–Aug 2027)
| Week | Activity |
|---|---|
| 25-26 | Data entry + validation (10 working days) |
| 27 | Biomass calculation (Chave 2014) |
| 28-29 | Hansen accuracy assessment (Precision, Recall, F1, Kappa) |
| 30-32 | Cross-validation with MapBiomas, Sentinel-2 |
| 33-36 | P0011 ground-truth supplementary writeup |

---

## 4. COSTS (USD)

| Category | Unit cost | Units | Subtotal |
|---|---|---|---|
| Field coordinator (consultant, 6 mo) | 1,000/mo | 6 | 6,000 |
| Fieldworkers (4, 3 mo) | 600/mo | 12 | 7,200 |
| Field transport (vehicle + fuel, 12 wks) | 200/wk | 12 | 2,400 |
| Lodging (4×12 weeks × $50/wk) | 50/wk | 48 | 2,400 |
| Per-diem (4 workers × $15/day × 60 days) | 15/day | 240 | 3,600 |
| Equipment (GPS ×4, dendrometer ×4, scale ×1, camera ×2) | — | — | 1,800 |
| Soil analysis (lab fees) | 100/plot | 64 | 6,400 |
| Data entry (paralegal, 2 weeks) | 400/wk | 2 | 800 |
| Contingency (~10%) | — | — | 3,060 |
| **TOTAL** | | | **≈ 25,660** |

Above is over 25k USD — original estimate. **Negotiable to ~$18,000 by reducing soil lab analysis to a 50-plot subsample** ($5,000 savings) and contracting coordinator part-time (3 mo @ $500 = $1,500). See next section.

### Reduced-budget alternative ($18,000)

| Cut | From | To | Save |
|---|---|---|---|
| Soil lab analysis | 64 plots × $100 | 50 plots × $100 | $1,400 |
| Field coordinator | 6 mo × $1,000 | 3 mo × $500 | $4,500 |
| Equipment (reuse from biology dept) | new | borrowed | $800 |
| Per-diem | 4 workers | 3 workers | $1,350 |
| **Saved** | | | **$8,050** |

Target: **$18,000** (within typical UNA FADA small-grant range).

---

## 5. FUNDING SOURCES

| Source | Max | Stage | Notes |
|---|---|---|---|
| UNA FADA small grant | $5,000 | Internal | Open call, October |
| CONACYT (Paraguay) | $20,000 | National | March 2027 deadline |
| IAI (Inter-American Inst.) | $50,000 | International | TBD |
| Rufford Foundation | $10,000 | International | Open call |
| Personal (Iván) | $3,000 | Bootstrap | Initial equipment |

**Strategy:** Apply UNA + personal in Sep 2026, CONACYT in Nov 2026, IAI/Rufford in Jan 2027. **Backup:** run on $3,000 personal + UNA small grant with 30 plots instead of 64.

---

## 6. UNA FADA ETHICS APPROVAL

The IRB protocol (`etica/IRB_protocol_paraguay_UNA.md`) is already drafted — 266 lines covering background, aims, study design, risks, data management, consent, and limitations.

### Submission packet (drafted Aug 2026, target submission Oct 2026)

The following documents need to be assembled:

1. **Cover letter to UNA FADA ethics committee** — template in `etica/UNA_IRB_cover_letter_es.md`
2. **IRB protocol** — `etica/IRB_protocol_paraguay_UNA.md` (existing draft, complete)
3. **Informed consent form (Spanish + Guaraní)** — based on `etica/FPIC_template_es.md` plus a one-page landowner consent
4. **Data management plan** — section 5 of IRB protocol, can be extracted
5. **Field crew training materials** — to be developed W7-10 of Phase 1
6. **Risk assessment** — section 4 of IRB protocol
7. **CVs of PI and coordinator** — to be assembled
8. **Letters of support** — 2 letters (INFONA + landowner cooperator expected)

### Estimated timeline

- W1-2 (Sep): Assemble packet
- W3 (early Oct): Internal review by UNA FADA research office
- W4 (mid Oct): Submission
- W5-8 (Oct-Nov): Ethics committee review
- W9 (early Dec): Approval letter (typical 6-8 week turnaround)
- W10 (Dec): Plan confirmed, can proceed to W11 pilot training

### Risk: committee asks for major revision
- **Likelihood:** Medium. UNA ethics typically requests clarifications.
- **Mitigation:** Protocol already covers all 5 risks (privacy, stigmatization, misuse, health, commercial). Two weeks of buffer built into schedule.

### Risk: FPIC for indigenous territory plots delayed
- **Likelihood:** High. FPIC process is months, not weeks.
- **Mitigation:** First FPIC contact in W1 of preparation phase. If delayed, **exclude plots in indigenous territories from v1** (reduces precision/recall in those cells but doesn't invalidate the rest).

---

## 7. RISK & CONTINGENCY

| Event | Impact | Mitigation |
|---|---|---|
| IRB delayed 1 month | Field season starts late | Run on $3k budget 2 plots/week instead of 4 |
| Weather (extended rains) | Field days lost | Pilot weeks with no data → re-do |
| Fieldworker attrition | Schedule slip | Hire backup pool of 2 additional fieldworkers |
| Indigenous territory FPIC not granted | 6-10 fewer plots | Stratified reweighting preserves overall accuracy |
| Verra under-claim not measurable | P0010 impact reduced | Use Chave 2014 AGB instead |
| Funding falls through | Reduced n (50 → 30) | Statistical power ≥ 0.8 at n=30 for stratum-level accuracy ≥ 0.10 |

---

## 8. SUCCESS METRICS

- **Hansen detection rate:** Precision ≥ 0.85 (target), Recall ≥ 0.70 (target)
- **MapBiomas accuracy:** Overall ≥ 0.80, Forest class F1 ≥ 0.75
- **Verra validation:** At least 3 projects independently measured within ±20% of Verra claim
- **Indigenous territory validation:** At least 5 territory plots completed
- **Reproducibility:** Field data DOI registered (Zenodo) + analysis code in repo

---

## 9. DELIVERABLES

| Deliverable | Owner | Date |
|---|---|---|
| IRB packet | Iván | Sep 2026 |
| IRB approval letter | UNA FADA | Dec 2026 |
| Field crew contracts signed | Iván | Dec 2026 |
| Equipment purchased | Iván | Jan 2027 |
| Training complete | Coordinator | Feb 2027 |
| Plot-level data CSV | Coordinator | May 2027 |
| Hansen accuracy report (JSON + Markdown) | Iván | Jul 2027 |
| P0011 supplementary material | Iván | Aug 2027 |
| Supplementary photos on Zenodo | Iván | Aug 2027 |

---

## 10. ETHICS COMMITMENTS

1. **No GPS coordinates published for indigenous territory plots** without FPIC sign-off from community.
2. **All raw data encrypted** on UNA FADA server. Anonymized outputs only on public repo.
3. **Local field workers are paid above market rate** (Py 1,800,000/month per worker ≈ USD 250/month). This is **twice** the typical daily wage (Py 50,000/day × 22 working days).
4. **Indigenous community ownership:** If FPIC granted, community members review final dataset before publication.
5. **Right of withdrawal:** Any participant may withdraw data within 30 days.

---

## 11. THE ONE PAGE FOR UNA

If the ethics committee only reads one page, point them to:

> *"This research validates Hansen GFC and MapBiomas Paraguay against 64 field plots across 6 departments during March-May 2027. Personal data risk is minimal — GPS coordinates, photos, and tree measurements only — and all landowner data is anonymized before publication. Field workers are paid above market rate. Indigenous territory access requires separate FPIC; if denied, that stratum is excluded. Total budget ≈ USD 18,000, addressing the largest gap in Paraguay's remote sensing research: lack of ground-truthed detection rates."*

---

**Annex A — Equipment list** (separate file)
**Annex B — Field protocol** (separate file)
**Annex C — Informed consent forms** (separate files)
**Annex D — FPIC template** — `etica/FPIC_template_es.md` (existing)

Plan ready for Iván's review and UNA FADA submission.