# IRB Protocol — Universidad Nacional de Asunción (UNA)

**Title:** *Multi-Temporal Satellite Computer Vision for Paraguay: A Foundation-Model Approach to Land-Use, Climate, and Environmental Justice*

**PI:** Iván Hocht-VonDerPol
**Institution:** Universidad Nacional de Asunción, Facultad de Ciencias Agrarias (FADA)
**Investigator type:** PhD student
**Date:** 2026-08-04
**Protocol version:** 1.0

---

## 1. BACKGROUND AND RATIONALE

The thesis develops a multi-temporal satellite computer vision framework for Paraguay, integrating Sentinel-2, MapBiomas Paraguay, Hansen GFC, OpenAQ, and Verra data. The research addresses three challenges:

1. **Deforestation monitoring** in the Gran Chaco (one of Earth's most active forest frontiers)
2. **Land tenure security** for indigenous communities (3.3× deforestation disparity)
3. **Limited local capacity** for geospatial AI in Paraguay

The research uses **only public, non-personally-identifying data** for most analyses. Human subjects data is limited to parcel ownership information from Catastro Nacional, which is publicly available but contains property owner identifiers.

## 2. SPECIFIC AIMS

### Aim 1: Develop six reproducible pipelines
- Yvutu (deforestation), Yvyra (carbon), Yvy (indigenous), Yrupe (yield), Kai (poaching), Tatakua (air quality)

### Aim 2: Validate against ground truth
- Field plots with INFONA
- Photos with community monitors
- Cross-validation with Hansen, INPE PRODES

### Aim 3: Engage indigenous communities via FPIC
- Coordinate with INDI
- Translate outputs to Guaraní
- Co-design monitoring systems

## 3. STUDY DESIGN

### 3.1 Type of Study
- **Mixed methods:** quantitative (remote sensing) + qualitative (interviews, FPIC)
- **Duration:** 2026-08 to 2027-02 (6 months)
- **Research questions:** 5 (see THESIS_ABSTRACT.md)

### 3.2 Data Sources
| Data type | Source | Sensitivity | Subjects |
|---|---|---|---|
| Sentinel-2 L2A | ESA Copernicus | Public | None |
| MapBiomas | MapBiomas Paraguay | Public | None |
| Hansen GFC | Hansen/UMD | Public | None |
| OpenAQ | OpenAQ | Public | None |
| Verra | Verra Registry | Public | None |
| Catastro | Paraguay gov | Public with PII | Property owners |
| OpenAQ near schools | OpenAQ | Public | School children |
| Field plots | INFONA partners | Privacy-reducing | Landowners |
| Indigenous FPIC | INDI communities | Sensitive | Communities |

### 3.3 Human Subjects

**Catastro data** (Aim 1, P0012):
- Public parcel ownership information
- Anonymized before publication (no owner names)
- Stored encrypted, access-controlled

**Field plots for ground truth** (Aim 2):
- 50-100 plots with landowner consent
- Data: GPS coordinates, photos, vegetation measurements
- No personal identifying information published

**Indigenous community interviews** (Aim 3, P0012):
- 10-20 communities in the Gran Chaco
- FPIC protocol required
- Community-controlled data

## 4. RISK ASSESSMENT

### Risk 1: Privacy Risk (LOW)
- Catastro ownership data is already public
- All identifying information anonymized before publication
- ❌ **Risk:** Property owners could be wrongly associated with deforestation
- ✅ **Mitigation:** Anonymize at parcel level, not at individual level

### Risk 2: Stigmatization Risk (MEDIUM)
- Indigenous community members could be wrongly associated with deforestation
- ❌ **Risk:** Community reputations affected
- ✅ **Mitigation:** FPIC process, community-controlled data, opt-out at any time

### Risk 3: Misuse Risk (MEDIUM)
- Data could be used to justify land grabs
- ❌ **Risk:** Conservation-as-pretext-for-displacement
- ✅ **Mitigation:** Open data, but FPIC barriers for sensitive analyses

### Risk 4: Health Risk (LOW)
- OpenAQ monitoring near schools
- ❌ **Risk:** Misinterpretation of pollution data
- ✅ **Mitigation:** Coordination with Ministry of Health, child welfare

### Risk 5: Commercial Risk (LOW)
- Paraguay environmental data could be monetized
- ❌ **Risk:** Data colonialism
- ✅ **Mitigation:** Open license (CC-BY-SA), no commercial exploitation

## 5. DATA MANAGEMENT

### 5.1 Storage
- All raw data on encrypted SSD
- Anonymized outputs on public repository
- Catastro data NEVER published raw

### 5.2 Access
- Principal investigator only
- Co-investigators with signed confidentiality
- No third-party access

### 5.3 Retention
- 5 years post-publication
- Then deleted, except anonymized outputs

### 5.4 Sharing
- Anonymized data on Zenodo
- Sensitive data NOT shared
- Indigenous community data NOT shared without community consent

## 6. CONSENT PROCEDURES

### 6.1 Catastro Data
- Public data, no individual consent required
- Aggregate anonymized before publication

### 6.2 Field Plots
- Written consent from landowner
- Right to withdraw at any time
- Data shared with landowner first

### 6.3 Indigenous Communities
- **FPIC protocol** (separate document)
- Community-controlled data
- Right to withdraw at any time
- Co-author opportunities
- Compensation for community time

### 6.4 School Near OpenAQ
- Coordination with Ministry of Education
- Anonymous aggregate data only

## 7. BENEFITS

### 7.1 Scientific
- 6 papers published in open access
- Methods available to Paraguayan researchers
- Foundation for future research

### 7.2 Societal
- Better deforestation monitoring
- Indigenous land tenure protection
- Public health information
- Capacity building

### 7.3 Economic
- Open data for local entrepreneurs
- Cost savings for Paraguayan government
- New market opportunities

### 7.4 Environmental
- Quantified deforestation
- Quantified carbon loss
- Indigenous territory protection
- Policy recommendations

## 8. SUBJECT COMPENSATION

### 8.1 Field Work Participants
- Travel reimbursement
- Per diem
- Co-authorship on relevant papers

### 8.2 Indigenous Communities
- Free training for community members
- Equipment donations (GPS, computers)
- Compensation for community time
- Open publication of relevant findings

### 8.3 Anyone Else
- No direct compensation (public data only)

## 9. PROTOCOL REVIEW

### 9.1 Internal Review
- FADA adviser review
- UNA ethics committee review

### 9.2 External Review
- INDI FPIC review
- INFONA technical review
- MADES (Ministry of Environment) review

### 9.3 Continuous Review
- Amendments to protocol as needed
- Annual progress reports
- Adverse event reporting

## 10. PRINCIPAL INVESTIGATOR COMMITMENT

I commit to:
- Honoring all consent procedures
- Anonymizing all data
- Coordinating with INDI on FPIC
- Publishing all results openly
- Responding to community concerns within 14 days
- Training next-generation Paraguayan researchers

---

## Appendix A: Data Flow Diagram

```
Public Data:
    Sentinel-2 → Process → Anonymized → Open Repo
    MapBiomas   → Process → Anonymized → Open Repo
    Hansen      → Process → Anonymized → Open Repo
    OpenAQ      → Process → Anonymized → Open Repo
    Verra       → Process → Anonymized → Open Repo

Semi-Public (Catastro):
    Catastro    → Anonymize → Aggregate → Open Repo
                 (raw never published)

Private (Ground Truth):
    Field Plots → Anonymize → Restricted Access
                 (not publicly shared)

Sensitive (Indigenous):
    Communities → FPIC → Community-Controlled
                 (not shared without consent)
```

## Appendix B: Informed Consent Template (Field Plots)

[A separate document `etica/CONSENT_field_plots.md`]

## Appendix C: FPIC Template (Indigenous)

[A separate document `etica/FPIC_template_es.pdf`]

## Appendix D: Adverse Event Reporting

[Any adverse event: data breach, community complaint, etc.]
- Report to FADA within 24 hours
- Report to UNA ética within 48 hours
- Resolve within 30 days

---

**Signed:** _______________________ Date: ___________
**Iván Hocht-VonDerPol, Principal Investigator**

**Witness:** _______________________ Date: ___________
**UNA Comité de Ética**

---

**This protocol will be submitted to:**
- Universidad Nacional de Asunción, FADA-Comité de Ética
- Ministerio del Ambiente y Desarrollo Sostenible (MADES)
- Instituto Paraguayo del Indígena (INDI)
- Instituto Forestal Nacional (INFONA)
