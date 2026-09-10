> **⚠️ UNVERIFIED DOCUMENT — PENDING INSTITUTIONAL REVIEW**
>
> This file was added to the repo on or before 2026-09-08 by an unspecified author (the file's git history shows commits under "Iván Weiss Van der Pol" but the user has stated they did not write it themselves; the content appears to be AI-generated or template-based).
>
> **Status as of 2026-09-09:**
> - No IRB submission has been filed with FP-UNA or any other institution.
> - No FPIC engagement has been conducted with any indigenous community.
> - The contact information, adviser names, and FPIC community contacts in this document are placeholders and have NOT been verified.
>
> **This file is preserved as a working draft for future use**, NOT as evidence of an institutional submission. Before any of this content is acted upon, every name, address, contact, and institutional reference must be re-verified by the user.
>
> See `outputs/DEFENSE_PREP_15_HAT_AUDIT_2026-09-09.md` Hat 7 for the full audit context.

---

# IRB Protocol — Paraguay UNA (FADA)

**Title:** Satellite remote sensing of deforestation and indigenous territories in the Gran Chaco: A multi-method study of forest loss, biodiversity, and indigenous land tenure (2018-2024)

**Principal Investigator:** Iván Hocht-VonDerPol
**Co-Investigators:** [Thesis adviser name], FADA-UNA
**Institution:** Facultad de Ciencias Agrarias (FADA), Universidad Nacional de Asunción (UNA)
**Submission target:** Comité de Ética en Investigación, FADA-UNA
**Submission date:** [Pending Iván's review]
**Version:** 1.0 (2026-09-07)

---

## 1. Background and rationale

This PhD thesis investigates the drivers and consequences of deforestation in the Gran Chaco region of Paraguay. Six papers (P0010-P0035) use satellite remote sensing, machine learning, and field validation to analyze: forest carbon credit integrity (P0010), real-time deforestation detection (P0011), indigenous territory impact (P0012), crop yield prediction (P0025), wildlife detection (P0026), and air quality (P0035).

The thesis relies primarily on **publicly available satellite data** (Hansen GFC v1.11, Sentinel-2, MODIS, VIIRS) and **public statistics** (INE census, FAO data). Field data collection is minimal but requires IRB approval when it involves human subjects.

---

## 2. Study objectives

**Primary objective:** Quantify the rate, drivers, and consequences of deforestation in the Gran Chaco using satellite remote sensing and machine learning.

**Secondary objectives:**
1. Measure forest loss rates in 10 indigenous territories and compare to national baseline
2. Estimate under-claim in Verra REDD+ projects
3. Detect wildlife using YOLOv8 on camera trap imagery
4. Predict crop yield using satellite features
5. Monitor air quality using OpenAQ station data

---

## 3. Methods

### 3.1 Data sources

| Data type | Source | Sensitive? | IRB scope |
|---|---|---|---|
| Satellite imagery | Hansen GFC, Sentinel-2, MODIS, VIIRS, GEDI | No | Out of scope |
| Verra project boundaries | Verra registry | No | Out of scope |
| INE census statistics | INE public data | No | Out of scope |
| OpenAQ air quality | OpenAQ API | No | Out of scope |
| OpenstreetMap features | OSM | No | Out of scope |
| **Guyra Paraguay camera trap images** | Guyra (5,000 public images) | **YES — wildlife in private land** | **In scope — anonymized location** |
| **INBIO yield data** | INBIO (TBD) | **YES — farm-level commercial data** | **In scope — anonymized** |
| **Indigenous territory aggregate data** | Hansen GFC + INDI boundaries | **YES — group-level statistics** | **In scope — see CARE Principles section** |

### 3.2 Aggregate-only data analysis

Per the FPIC decision (`docs/partnerships/FPIC-DECISION-STATUS-2026-09-07.md`), all per-community analyses are **deferred** until Free, Prior, and Informed Consent is obtained from each community. The thesis contains only:
- National-level statistics (16,628 km² loss 2001-2023, 2,755 MtCO₂e)
- Aggregate statistics across all 10 territories (mean 24.7% loss vs national 8.5%, ratio 3.0×, 95% bootstrap CI [1.72, 4.20]×)
- Anonymized summaries (no community names in P0012 except in examples)

### 3.3 Human subjects

This thesis involves minimal direct human-subjects research. The only human-subjects interaction is:
- **Email outreach to partner institutions** (INFONA, INDI, SENEPA, Verra, etc.) — covered by UNA IRB expedited review (no in-person contact, no personal data collected)
- **FPIC engagement with indigenous communities** (deferred per #10) — requires separate IRB amendment after FPIC protocol finalized

---

## 4. Inclusion and exclusion criteria

**Inclusion:** All 10 indigenous territories in the Chaco with formal INDI registration; all 5 Paraguayan Verra REDD+ projects with public boundaries; all Chaco municipalities with OpenAQ stations.

**Exclusion:** Territories or projects where data license forbids analysis; territories where FPIC has been refused.

---

## 5. Risks

### 5.1 Risk to individuals

**Minimal.** No personal data collected. Satellite analysis does not identify individuals.

### 5.2 Risk to communities (group harm)

**Moderate — mitigated.** The aggregate finding (3.0× deforestation disparity) could attract unwanted attention to specific territories if per-community attribution is inferred. Mitigation:
- Aggregate-only publication in thesis (per FPIC decision)
- No community names appear in P0012 quantitative results
- Anonymized spatial analysis (random offsets of 5-10 km on any community-identified point)
- All FPIC engagement preceded by community-led disclosure of risks

### 5.3 Risk to ecosystems

**None.** Analysis is non-invasive (satellite imagery is passive, no field disturbance).

### 5.4 Risk of data misuse

**Moderate — mitigated.** Carbon credit integrity findings (P0010) could be used to attack or defend specific Verra projects. Mitigation:
- Findings framed as *methodology improvement*, not *project accusation*
- 95% bootstrap confidence intervals provided to acknowledge uncertainty
- Independent satellite validation recommended; not presented as definitive

---

## 6. Benefits

### 6.1 To participants

- **Indigenous communities:** Aggregate findings may inform advocacy for FPIC enforcement (no per-community attribution risk)
- **Partner institutions:** Methodological framework and open-source code
- **Academic community:** Peer-reviewed publications in 6 thematic areas

### 6.2 To society

- Evidence-based policy input for Paraguayan National Forestry Plan (2025-2030)
- Independent verification methodology for carbon market integrity
- Open data and code for replicability

---

## 7. Informed consent

### 7.1 Partner institutions

Written consent via email outreach (formal partnership letters per `docs/partnerships/ONE-PAGERS-2026-09-07.md`). No data shared without institutional consent.

### 7.2 Indigenous communities

**Deferred.** No per-community analysis in current thesis. FPIC protocol (`docs/partnerships/TEMPLATE-FPIC.md`) will be activated before any per-community analysis. Spanish and Guaraní consent templates prepared.

### 7.3 Individual participants

N/A — no individual human-subjects data collected.

---

## 8. Data management

### 8.1 CARE Principles for Indigenous Data Governance

Per the FPIC decision, the thesis applies:
- **Collective benefit:** Data use must benefit the communities, not just researchers
- **Authority to control:** Communities decide what data is shared and with whom
- **Responsibility:** Researchers responsible for protecting data integrity
- **Ethics:** Minimization of harm, transparency about risks

### 8.2 Storage

- All data on encrypted local storage (LUKS) and GitHub private repo (until FPIC obtained)
- Public release only after FPIC for any per-community data
- Aggregated public statistics published openly

### 8.3 Retention

- Raw data: retained for 10 years per UNA policy
- Anonymized analysis data: retained indefinitely for reproducibility
- Per-community data: **deleted if community withdraws consent** (right to be forgotten)

---

## 9. Confidentiality

- Personal identifiers: none collected
- Community identifiers: anonymized in all published outputs
- Institutional identifiers: partnership is public (INFONA, INDI, etc. — these are institutional not personal)

---

## 10. Compensation

No compensation to participants (no human-subjects data collection).

Partner institutions receive co-authorship on relevant papers and open-source code as compensation for data sharing.

---

## 11. Adverse event reporting

- **Process for reporting:** Iván will report any adverse events (data breach, community complaint, etc.) to UNA IRB within 48 hours via email + follow-up documentation within 7 days
- **Definition of adverse event:** any unintended harm to participant, community, or partner institution caused by the research
- **Mitigation plan:** halt affected analysis, consult community/institution, revise protocol as needed

---

## 12. Conflict of interest

None declared. Iván is a PhD candidate at FADA-UNA with no commercial interest in the outcomes. Verra project developers are not co-investigators and have no editorial control over P0010.

---

## 13. Funding

This thesis is self-funded (no commercial sponsor). GPU costs for T3-K (~$20) funded personally by Iván. No funder has editorial control over the analysis or conclusions.

---

## 14. Timeline

- 2026-Q3: IRB submission (this protocol)
- 2026-Q4: IRB approval + thesis defense preparation
- 2027-Q1: Per-community FPIC engagement begins
- 2027-Q2-Q3: Thesis defense + journal submissions

---

## 15. References

- Helsinki Declaration (current revision)
- Belmont Report
- CARE Principles for Indigenous Data Governance (Carroll et al. 2020)
- UNA FADA Ethics Committee guidelines

---

## Submission checklist

- [ ] Iván reviews all 15 sections
- [ ] Co-investigators sign off
- [ ] Translation to Spanish for UNA submission
- [ ] FADA UNA submission via formal channel
- [ ] IRB approval letter received before any data collection begins

---

## Contact

**Iván Hocht-VonDerPol**
PhD candidate, FADA-UNA
Email: [to be added]
Adviser: [to be added]
