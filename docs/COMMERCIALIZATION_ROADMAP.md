# Commercialization Roadmap — Next 90 Days

**Created:** 2026-08-11
**Owner:** Iván Weiss Van Der Pol
**Trigger:** Thesis-defense → market entry

This is the **operational checklist** that turns `BUSINESS_MODEL.md` projections
into actual revenue. Each item has a deliverable, an owner, and a deadline.

---

## Phase 1 — Days 0-30: Foundation (defense → legal entity → public assets)

### Legal entity (Day 1-7)

- [ ] **Day 1-2**: Consult abogado in Asunción on entity type:
  - `Sociedad Anónima (SA)` — traditional, ₲ 5-15M setup
  - `Sociedad por Acciones Simplificada (SAS)` — newer, ₲ 3-8M setup
  - `Sucursal de sociedad extranjera` — if parent company outside PY
- [ ] **Day 3-5**: Register company name (RPC). Reserved candidates:
  - `ParaguAI S.A.`
  - `ForestWatch Paraguay S.A.`
  - `SatellitCV S.A.`
- [ ] **Day 5-7**: Open bank account (Banco Itaú / Continental / Familiar)
- [ ] **Day 7**: Get RUC, set up basic accounting (Contador必备)

### Public assets (Day 7-21)

- [ ] **Day 7-10**: Deploy `paragu-ai.com` static site on Cloudflare
  - Brand: ParaguAI umbrella (forest, agriculture, air, wildlife products)
  - Logo + domain + minimal landing page
- [ ] **Day 10-14**: Deploy public dashboard at `forestwatch.paragu-ai.com`
  - Show P0011 deforestation map (open data only)
  - Show P0010 Verra under-claim chart (open methodology)
  - 6-month refresh cycle
- [ ] **Day 14-21**: Publish P0011 on arXiv pre-print (open access)
- [ ] **Day 14-21**: Write `POLICY_BRIEF_es.md` + `POLICY_BRIEF_en.md` + `POLICY_BRIEF_gn.md` (Guaraní)
  - 4 pages each, infographics
  - Send to INFONA, INDI, MAG, Itaipu, WWF

### CFP for pilots (Day 21-30)

- [ ] Draft email template for 3 customer segments:
  - **NGOs**: WWF Paraguay, Guyra Paraguay, Conservation International
  - **Government**: INFONA, MAG, INBIO
  - **Cooperatives**: 5 soy coops in Alto Paraná + Caaguazú
- [ ] Send to 15 prospects → target 3-5 responses → 3 signed pilot letters
- [ ] Offer: 90-day free pilot → 50% off Year 1 if converted

---

## Phase 2 — Days 30-60: Pilots (product validation + first $)

### Pilot onboarding (Day 30-45)

- [ ] **Day 30**: Set up Stripe billing + Cloudflare R2 data lake
- [ ] **Day 30-35**: Onboard 3 Basic pilots:
  - Jorge (Conservation International) — deforestation alerts, Volendam region
  - María (WWF Paraguay) — monthly reports, Chaco
  - NGO Tier3 NGO — cooperative member verification
- [ ] **Day 35-40**: Onboard 1 Professional pilot:
  - ESG consulting firm (TBD) — monthly reports + REST API
- [ ] **Day 40-45**: Weekly sync with each pilot; collect feedback

### Grant submissions (Day 30-60)

- [ ] **Day 30**: Identify top 3 grant calls:
  - NASA ROSES-2027 Carbon Monitoring System (LOI due ~Feb 2027)
  - NSF GEO Geoinformatics (rolling)
  - WWF Forests Forward (rolling)
- [ ] **Day 35**: Draft LOI for NASA CMS (5 pages)
- [ ] **Day 45**: Submit first grant application
- [ ] **Day 50-60**: Submit second + third grant

### Education content (Day 30-60)

- [ ] **Day 35**: Record Module 1 of "Deforestation Monitoring with ML" course (90 min)
  - Hosted on Udemy / Coursera / ParaguAI Academy
- [ ] **Day 50**: Launch course at $300 (intro price)
- [ ] **Day 60**: First 20 enrollments target

### Consulting pipeline (Day 30-60)

- [ ] **Day 30-45**: Identify 3 warm leads (existing UNA network)
- [ ] **Day 45-60**: Schedule 3 consulting pitches:
  - Soy co-op (Alto Paraná) — yield + deforestation baseline
  - ESG audit firm — due diligence support
  - Law firm — expert witness for litigation

---

## Phase 3 — Days 60-90: Conversion + scale (pilots → paid, first press)

### Pilot conversion (Day 60-75)

- [ ] **Day 60**: Send renewal offers to pilots (target 80% conversion)
- [ ] **Day 65**: First paid invoices:
  - 3 Basic × $500/mo × 3 months = $4,500
  - 1 Professional × $2,000/mo × 3 months = $6,000
  - **First revenue: $10,500**
- [ ] **Day 70**: Deploy customer-success playbook
- [ ] **Day 75**: Collect testimonials + case studies

### Press + visibility (Day 60-90)

- [ ] **Day 60**: Press release: "First Paraguayan satellite deforestation SaaS launches"
- [ ] **Day 65**: Submit to:
  - ESA Living Planet Symposium 2027 (abstract due Oct 2026)
  - AGU Fall Meeting 2026
  - IISc DRONES / EARSeL / GEO conferences
- [ ] **Day 75**: Podcast appearances (target 2):
  - Data Skeptic (machine learning + climate)
  - PyData / GeoPython podcast
- [ ] **Day 90**: First keynote at Universidad Nacional de Asunción

### IP + legal (Day 60-90)

- [ ] **Day 60-75**: Provisional patent for P0010 carbon-under-claim methodology
  - Hire IP lawyer (~$3,000-5,000)
  - File with INPI Paraguay + PCT international
- [ ] **Day 75-90**: Trademark "ParaguAI" + "ForestWatch Paraguay" in PY class 9, 42

### Hire (Day 75-90)

- [ ] **Day 75**: First hire — part-time senior Python dev (15 hrs/week)
  - $50-80/hr × 60 hrs/month = $3,000-4,800/month
- [ ] **Day 90**: First hire — part-time accountant ($500-1,000/month)

---

## Phase 4 — Days 90-180: First $100k ARR (recurring revenue lock-in)

- [ ] Reach $100k ARR by Day 180 (≈ $8,300 MRR)
  - 20 Basic × $500 = $10,000 MRR
  - 8 Professional × $2,000 = $16,000 MRR
  - 2 Enterprise × $10,000 = $20,000 MRR
  - 4 Carbon-Market API × $50k/yr ÷ 12 = $16,700 MRR
  - = $62,700 MRR target
- [ ] Hire first FTE (devops + ML engineer)
- [ ] Apply to Y Combinator or Latitud (LATAM accelerator)
- [ ] First speaking engagement at international conference
- [ ] Press coverage: at least 3 articles (TechCrunch, Rest of World, Climate Wire)

---

## Phase 5 — Days 180-365: First $500k ARR → Series A prep

- [ ] Reach $500k ARR (≈ $42,000 MRR)
- [ ] Add 1-2 enterprise customers (INFONA, Itaipu, large bank)
- [ ] File 1 model license (Prithvi weights) — first $100k+ check
- [ ] Sign 1 large consulting contract ($100k+)
- [ ] Hire CEO + CFO (if not co-founder)
- [ ] Legal entity upgrade: SA → SAS or international holding (US C-corp + PY branch)
- [ ] Series A fundraise: $5-10M at $20-40M valuation

---

## Decision points (stop / continue / pivot)

### Decision 1 — End of Day 30

**Continue if:** ≥3 pilots signed OR ≥1 grant application submitted
**Pivot if:** 0 pilots AND 0 grants → consider pure open-source / research route
**Stop if:** thesis defense delayed >6 months OR personal health/funding crisis

### Decision 2 — End of Day 60

**Continue if:** ≥1 paid invoice AND ≥1 grant in progress
**Pivot if:** only education/consulting revenue → focus on courses + books
**Stop if:** legal entity blocked (Paraguay bureaucracy) → consider Argentina or Uruguay

### Decision 3 — End of Day 90

**Scale if:** MRR ≥ $5,000 AND grant pipeline ≥ $300k pending
**Maintain if:** MRR $1,000-$5,000 → operate lean, single-person consulting + SaaS
**Sunset if:** MRR < $1,000 → close SaaS, pivot to consulting + open-source

---

## Tooling stack for the 90-day plan

| Function | Tool | Cost |
|----------|------|------|
| Legal entity | Abogado PY + RPC online | $2,000-5,000 setup |
| Bank | Itaú PY / Continental PY | $0 setup |
| Domain + DNS | Cloudflare Registrar | $10/yr per domain |
| Hosting | Cloudflare Pages + Workers | $0-50/month |
| Data lake | Cloudflare R2 | $1-50/month |
| Billing | Stripe Atlas | $0 + 2.9% per transaction |
| Email | Google Workspace | $6/user/month |
| CRM | HubSpot free tier | $0 |
| Project management | Linear (free for <10 users) | $0 |
| Documentation | GitHub Wiki + Notion | $0 |
| Accounting | Conta Azul PY or Wave | $30-100/month |
| Newsletter | Buttondown or Substack | $0-30/month |
| Podcast booking | Featured / ListenNotes | $500-2,000/booking |

**Total Year 1 tooling: $5,000-15,000**

---

## The single most important deliverable

If only ONE thing gets done in 90 days, it is:

> **Get 1 paying customer.**

Everything else (brand, press, courses, grants) is multiplier on revenue. Without
the first paying customer, none of the others compound. Customer-1 → customer-2 →
customer-3 → series-A → exit.

Customer-1 may be paying only $500/month for the Basic tier. **That first invoice
is the seed of the entire thesis-as-product pipeline.**

---

## Related documents

- `docs/BUSINESS_MODEL.md` — full pricing + revenue forecast
- `docs/REAL_TODO.md` — operational thesis tasks (parallel track)
- `docs/STAKEHOLDERS.md` — partner map
- `STATUS.md` — submission readiness per paper

**Last updated:** 2026-08-11
**Review cadence:** weekly for first 30 days, monthly thereafter