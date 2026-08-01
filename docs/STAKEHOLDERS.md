# Stakeholders & Communication Plan

This document identifies all stakeholders for the SatelliteCV-Paraguay mega-project and defines how/when/how often to communicate with each.

## Stakeholder Map

### Tier 1 — Critical (weekly contact)

#### 1. Iván Weiss Van der Pol (Thesis Author)

- **Role:** Researcher, author, primary implementer
- **Communication:** Daily self-review via TODOs
- **Channels:** GitHub Issues, Telegram, this repo's docs
- **What they need:** Progress updates, blockers, next actions

#### 2. Juan Carlos Cristaldo (Thesis Advisor, FADA-UNA)

- **Role:** Director of thesis, FADA professor, GIS/cartography expert
- **Communication:** Weekly meetings (Mondays 14:00)
- **Channels:** In-person at FADA, WhatsApp, email
- **What they need:** Weekly progress reports, decision points, paper drafts
- **Topics covered:** P0011, P0010, P0012, P0025, P0026 (5/6 papers)
- **Languages:** Spanish + Guaraní

### Tier 2 — Important (monthly contact)

#### 3. Co-Advisors

| Co-advisor | Institution | Paper(s) |
|-----------|-------------|----------|
| Julio Torales | FCM-UNA | P0015 (clinical) |
| Mirtha González | FCM-UNA | P0031 (Chagas) |
| Christian Von Lücken | FP-UNA | P0067 (transit) |
| Horacio Legal Ayala | FP-UNA | P0085 (road) |
| Juan Talavera | FP-UNA | P0040 (OCR) |
| José Vázquez | FP-UNA | P0021 (education) |

- **Communication:** Monthly meetings per advisor
- **Channels:** Email, in-person
- **What they need:** Paper drafts for review, progress updates

#### 4. Paraguay Institutions

| Institution | Contact | Paper | Cadence |
|------------|---------|-------|---------|
| INFONA | forestry.gov.py | P0100, P0011 | Monthly |
| INDI | indigenous.gov.py | P0012 | Bi-weekly |
| SENEPA | senepa.mspbs.gov.py | P0031 | Monthly |
| MOPC | mopc.gov.py | P0085 | Monthly |
| ANDE | ande.gov.py | P0005 | Monthly |
| MEC | mec.gov.py | P0021 | Monthly |
| FCM-UNA | fcm.una.py | P0015, P0031 | Weekly |

### Tier 3 — Networking (quarterly contact)

#### 5. Funding agencies

| Agency | Program | Purpose |
|--------|---------|---------|
| CONACYT | PROCIENCIA | Research grants |
| CONACYT | FEEI | Equipment |
| CONACYT | SISNI | Researcher categorization |

- **Communication:** Quarterly reports + on-demand
- **Channels:** Email, official forms

#### 6. Journal editors

| Journal | Paper | Contact |
|---------|-------|---------|
| Remote Sensing of Environment | P0011 | editor@rse.com |
| Nature Climate Change | P0100 | nature@nature.com |
| Comp & Elec in Agriculture | P0025 | editorial@elsevier.com |
| World Development | P0012 | wd@elsevier.com |
| Conservation Biology | P0026 | scb@scb.org |
| Atmospheric Environment | P0035 | ae@elsevier.com |

- **Communication:** Submission + peer review response

### Tier 4 — Community partners

| Partner | Domain | Cadence |
|---------|--------|---------|
| 5 indigenous communities | P0012 | Quarterly visit |
| WWF Paraguay | P0026 | Quarterly |
| Guyra Paraguay | P0026 | Quarterly |
| Fundación Moisés Bertoni | conservation | Quarterly |
| Code for Paraguay | civic tech | Quarterly |

## Communication Plan

### Weekly

- [ ] Advisor meeting (Mondays 14:00)
- [ ] GitHub Issues update
- [ ] TODOs review

### Monthly

- [ ] Co-advisor meetings (one per month)
- [ ] Institution partner update (2-3 per month)
- [ ] FCM-UNA clinical research meeting
- [ ] Progress report draft

### Quarterly

- [ ] Funding agency reports
- [ ] Community partner visits
- [ ] Stakeholder newsletter
- [ ] Paper submission review
- [ ] Strategic plan review

### Ad-hoc

- [ ] Conference attendance (NeurIPS, IGARSS, AGU, etc.)
- [ ] Media interviews (rare)
- [ ] Public engagement (UN-Habitat Open Day)
- [ ] Bug reports / blockers
- [ ] Crisis (data loss, advisor conflict, etc.)

## Languages

- **Spanish:** Primary language for all Paraguayan stakeholders
- **English:** For international journals, conferences, GitHub
- **Guaraní:** For indigenous community engagement (P0012)

## Communication Templates

### Email to Advisor (Spanish)

```
Estimado Prof. Cristaldo:

Le escribo para actualizarle sobre el progreso del megaproyecto
SatelliteCV-Paraguay esta semana.

**Logros:**
- [bullet 1]
- [bullet 2]

**Blockers:**
- [blocker 1]

**Próxima semana:**
- [task 1]
- [task 2]

¿Podríamos agendar una reunión para el lunes?

Saludos,
Iván Weiss Van der Pol
```

### Email to Institution (Spanish)

```
Estimado/a [nombre],

Soy Iván Weiss Van der Pol, estudiante de la FP-UNA, trabajando en
el proyecto SatelliteCV-Paraguay (observación de la tierra con IA).

Me gustaría solicitar [acceso a datos / colaboración / reunión]
para el proyecto [P00XX nombre]. Adjunto propuesta.

¿Podemos agendar una reunión?

Atentamente,
Iván Weiss Van der Pol
```

### Indigenous community engagement (Guaraní + Spanish)

```
(pyhare mboyve / hoy día)
Kuarahy (estimada) comunidad,

Iván che aikuaauka iporãve chéve apytépe oñemotenonde pe
territorio-pe g̃uarã satélite rembiapo. Nde rovai'u katu oñeha
mba'éichapa...

(Mañana tendré reunión)
```

## Risk Register

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Data access denied | Medium | High | Multiple sources, public alternatives |
| Advisor unavailable | Low | High | Co-advisors identified |
| GPU unavailable | Low | Medium | Kaggle, Colab free tiers |
| IRB delayed | Medium | Medium | Start IRB early (3-6 months) |
| Paper rejected | Medium | Low | Submit to multiple journals |

## Success Criteria

- [ ] All 6 papers submitted
- [ ] All IRB approvals (if needed) granted
- [ ] All partnerships signed
- [ ] At least 3 community partners engaged
- [ ] All Tier 1/2 stakeholders satisfied
