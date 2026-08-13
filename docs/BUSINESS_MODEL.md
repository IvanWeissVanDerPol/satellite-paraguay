# Business Model & Monetization Strategy — SatelliteCV-Paraguay

**Status:** Draft v1 (2026-08-11)
**Scope:** Six-paper academic thesis + open-source Python toolkit → revenue-generating products
**Owner:** Iván Weiss Van Der Pol
**Review cycle:** Quarterly, after each paper acceptance

---

## 1. Value proposition (one-line)

Production-grade, audited, satellite-based environmental intelligence for Paraguay —
deforestation alerts, carbon-credit verification, indigenous-territory monitoring,
agricultural yield forecasting, wildlife poaching detection, and air-quality mapping —
delivered as APIs, dashboards, and audit reports.

The thesis is **the credibility asset** (peer review, university backing, IRB-grade
data ethics). The products are the **delivery mechanism** for that credibility.

---

## 2. Product / revenue lines (6 lines)

### 2.1 SaaS — `paragu-ai.com/forestwatch-py` (P0011 + P0010)

Tiered platform API for deforestation alerts and carbon-credit verification.

| Tier | Price | Target | Includes |
|------|-------|--------|----------|
| Basic | **USD 500/mo per seat** | NGOs, journalists, small cooperatives | Monthly NDVI/deforestation rasters over 6 biomes, email alerts, GeoJSON exports, 6-month history |
| Professional | **USD 2,000/mo per seat** | Mid-size NGOs, compliance officers, ESG consultants | All Basic + weekly updates, custom AOI, Verra/VCS claim overlay, REST API access, 2-year history |
| Enterprise | **USD 10,000/mo per org** | INFONA, Itaipu Binacional, large soy/cattle firms, ESG-rated banks | All Pro + on-premise deploy, dedicated support, custom models, SLAs, audit-trail log export |
| Carbon-Market API | **USD 50,000/yr per project** | Verra / Gold Standard auditors, carbon-project developers | Real-time under-claim detection, P0010-derived methodology, audit-grade report |

**Assumed customers Year 1 (realistic seed-stage):**

- 10 Basic seats → $60,000/yr
- 5 Professional seats → $120,000/yr
- 2 Enterprise orgs → $240,000/yr
- 3 Carbon-Market API → $150,000/yr

**SaaS subtotal: USD 570,000/yr (Year 1)**

---

### 2.2 Model + data licensing (P0011 + P0025)

| Asset | Price | Buyers |
|-------|-------|--------|
| Prithvi fine-tune weights (P0011) | **USD 100,000-500,000/license** | Remote-sensing startups, national space agencies (CONAE Argentina, AEB Brazil, ESA third-party programs) |
| Yrupe multi-task CNN (P0025) | **USD 80,000-200,000/license** | Soy/cattle cooperatives, agricultural ministries (MAG Paraguay, INBIO Argentina) |
| Hansen + MapBiomas curated tiles | **USD 50,000-200,000/license** | Researchers, ESG data providers (Planet, Maxar downstream), academic consortia |
| Curated dataset bundle (all 6) | **USD 300,000 single + USD 50,000/yr maintenance** | Conservation NGOs (WWF, CI, WCS), research institutions |

**Assumed deals Year 1:**

- 2 model licenses (P0011 + P0025) → $180,000-700,000
- 1 dataset bundle → $300,000 + $50,000/yr

**Licensing subtotal: USD 480,000-1,050,000 (Year 1), then $50k/yr recurring**

---

### 2.3 Consulting + custom analysis (all 6 papers)

| Service | Price | Deliverable |
|---------|-------|-------------|
| Hourly consulting | **USD 200-500/hour** | Ad-hoc analysis, model retraining, expert witness |
| Custom analysis project | **USD 10,000-100,000/project** | One-off report (e.g., "deforestation baseline for 3 soy cooperatives in Alto Paraná") |
| Litigation support | **USD 5,000-20,000/case** | Court-admissible expert report + testimony (P0010 carbon fraud cases) |
| ESG due diligence | **USD 25,000-75,000/engagement** | Pre-investment verification of land-use claims |

**Assumed engagements Year 1:**

- 100 consulting hours → $20,000-50,000
- 5 custom analysis projects → $50,000-500,000
- 2 litigation cases → $10,000-40,000
- 3 ESG due diligence → $75,000-225,000

**Consulting subtotal: USD 155,000-815,000/yr**

---

### 2.4 Grants + non-dilutive funding (research continuity)

| Funder | Program | Typical award |
|--------|---------|---------------|
| NASA ROSES | Carbon Monitoring System, NISAR Science Team | $300,000-1,500,000/2yr |
| NSF GEO | Geoinformatics, SBE Environmental | $200,000-800,000/2yr |
| EU Horizon Europe | Cluster 6 (Food, Bioeconomy), Cluster 5 (Climate) | €300,000-€1,200,000/3yr |
| World Bank / IDB | Forest Carbon Partnership Facility | $200,000-500,000/2yr |
| WWF / CI / WCS | Conservation grants | $50,000-200,000/yr |
| Google.org AI for Social Good | AI Impact Challenge | $500,000-2,000,000/yr |
| Paraguay CONACYT | Becas + proyectos de investigación | ₲ 500M-2,000M (~$70,000-280,000) per project |
| UNA internal | Proyectos de extensión universitaria | ₲ 100M-300M |

**Assumed grants Year 1:**

- 1 NASA/NSF/EU grant → $300,000-1,500,000
- 1 conservation NGO grant → $50,000-200,000
- 1 Paraguay local grant → $70,000-280,000

**Grants subtotal: USD 420,000-1,980,000 (Year 1, non-recurring)**

---

### 2.5 Education + training (capacity-building)

| Offering | Price | Platform |
|----------|-------|----------|
| Online course "Deforestation Monitoring with ML" | **USD 200-1,000/student** | Coursera / Udemy / Paragu-AI Academy |
| In-person 5-day workshop | **USD 500-2,000/participant** | Delivered in Asunción / Buenos Aires / São Paulo |
| University guest lectures | Honorarium | UNA, UCA, UP, UFPR, USP |
| Tech consultancy training | **USD 10,000-30,000/company** | 4-week bootcamp for new hires |

**Assumed Year 1:**

- 100 online course students → $20,000-100,000
- 50 workshop participants → $25,000-100,000
- 2 corporate bootcamps → $20,000-60,000

**Education subtotal: USD 65,000-260,000/yr**

---

### 2.6 Publications + books + media (credibility → indirect income)

| Asset | Direct income | Indirect income |
|-------|---------------|-----------------|
| 6 peer-reviewed papers (RSE, ERL, RSE-ISR, AE, JAG, FAC) | $0 | Multiplies grant credibility, consulting rates, partnership willingness |
| PhD thesis book (LAP Lambert / Springer) | $20-50/copy × 500 = $10,000-25,000 | Industry recognition, keynote invitations |
| Public dashboard (free, branded) | $0 | Inbound leads for SaaS + consulting |
| Policy brief trilingüe (ES/EN/GY) | $0 | Government sales channel |
| Documentary / podcast appearances | $0-5,000/appearance | Brand awareness |

**Publications subtotal (direct): USD 10,000-25,000/yr. Indirect leverage: ~10x multiplier on all other lines.**

---

## 3. Consolidated revenue forecast

### Year 1 (post-thesis-defense)

| Line | Conservative | Expected | Optimistic |
|------|--------------|----------|------------|
| SaaS | $300,000 | **$570,000** | $900,000 |
| Licensing | $300,000 | **$480,000** | $1,050,000 |
| Consulting | $155,000 | **$400,000** | $815,000 |
| Grants | $420,000 | **$800,000** | $1,980,000 |
| Education | $65,000 | **$150,000** | $260,000 |
| Publications | $10,000 | **$20,000** | $25,000 |
| **TOTAL** | **$1,250,000** | **$2,420,000** | **$5,030,000** |

### Year 2-3 (assuming 1 large grant + 4 SaaS customers)

| Line | Y2 expected | Y3 expected |
|------|-------------|-------------|
| SaaS | $1,100,000 | $2,200,000 |
| Licensing (recurring) | $600,000 | $900,000 |
| Consulting | $600,000 | $900,000 |
| Grants | $500,000 | $500,000 |
| Education | $300,000 | $500,000 |
| Publications | $25,000 | $30,000 |
| **TOTAL** | **$3,125,000** | **$5,030,000** |

### Year 5 (steady state)

**USD 4-8M ARR** — Paraguay-focused SaaS + global consulting + recurring license + education platform.

---

## 4. Cost structure (must be subtracted before net)

### Year 1 costs

| Category | Cost |
|----------|------|
| Cloud infra (AWS/GCP) | $30,000-80,000/yr |
| Data acquisition (Planet, Maxar, GEE egress) | $20,000-60,000/yr |
| GPU compute (Vast.ai + Lambda) | $5,000-30,000/yr |
| Personnel (1-2 part-time devs) | $80,000-200,000/yr |
| Legal + accounting | $15,000-30,000/yr |
| Marketing + travel | $20,000-50,000/yr |
| Paraguay entity formation (Sociedad Anónima) | $3,000-5,000 one-time |
| IRB + partnership fees (annual) | $2,000-5,000/yr |
| Insurance (D&O, E&O, cyber) | $5,000-15,000/yr |
| **TOTAL Year 1 costs** | **$180,000-475,000** |

### Net income

- Conservative Year 1: **$775,000 net**
- Expected Year 1: **$1,945,000 net**
- Optimistic Year 1: **$4,555,000 net**

---

## 5. Pricing rationale (why these numbers)

### 5.1 SaaS tiers

| Tier | Comparable | Source |
|------|-----------|--------|
| Basic $500/mo | Global Forest Watch Pro (~$400-800/mo), Planet Insights (~$1,000/mo) | public pricing 2024-25 |
| Professional $2,000/mo | Descartes Labs custom (~$2-5k/mo), Maxar SecureWatch (~$3k/mo) | industry interviews |
| Enterprise $10,000/mo | Kayrros (~$50k/yr base), RS Metrics (custom $50k+/yr) | competitive intel |
| Carbon-Market API $50k/yr | Sylvera API (~$30-100k/yr), Pachama platform fees | public |

### 5.2 License fees

Comparable to academic-to-industry model transfers:

- ESA Φ-sat-1 model license: €50,000-€200,000
- NASA Harvest model transfers: $100,000-500,000
- Prithvi EO Foundation weights (free for non-commercial, $50-200k for commercial)
- TensorFlow / PyTorch proprietary model licenses: $100,000-1,000,000

### 5.3 Consulting rates

Senior remote-sensing scientist in LATAM: $150-400/hr. With PhD + publications + IRB track record: $300-500/hr.

### 5.4 Grant ranges

NASA Carbon Monitoring System historical awards: $500,000-2,000,000 over 2-3 years. EU Horizon Cluster 6: €1-5M over 3 years (typical SME share: €300-800k).

---

## 6. Unit economics

### Customer Acquisition Cost (CAC)

- Enterprise SaaS: $5,000-15,000/customer (conferences, demos, RFPs)
- Professional SaaS: $500-1,500/customer
- Basic SaaS: $50-200/customer
- Consulting client: $2,000-5,000/engagement

### Lifetime Value (LTV)

- Enterprise: 3-5 years × $120,000/yr = $360,000-600,000
- Professional: 2-3 years × $24,000/yr = $48,000-72,000
- Basic: 1-2 years × $6,000/yr = $6,000-12,000
- Consulting client: 5-10 years × $50,000/yr = $250,000-500,000

### LTV/CAC ratios

| Customer | LTV | CAC | Ratio |
|----------|-----|-----|-------|
| Enterprise | $480,000 | $10,000 | **48:1** |
| Professional | $60,000 | $1,000 | **60:1** |
| Basic | $9,000 | $125 | **72:1** |
| Consulting | $375,000 | $3,500 | **107:1** |

All well above the 3:1 SaaS-health threshold.

---

## 7. Risk register

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Paraguay political instability affects public-sector sales | Medium | High ($200-500k/yr) | Diversify: LATAM + global customers |
| Open-source competitors (e.g., Global Forest Watch free tier) | High | Medium | Vertical: Paraguay-specific AOI + local partnerships is defensible |
| FPIC/ethics failure blocks P0012 | High | Medium | Decouple P0012 commercialization from rest; treat as research-only |
| Cloud costs spike | Medium | Low | Move compute to Paraguayan VPS (aiw-*) where possible |
| Hiring bottleneck (talent in Paraguay) | Medium | High | Hybrid remote team + Paraguay university partnerships |
| Currency risk (PYG/USD) | Medium | Low | Invoice in USD; Pygaify only expenses |
| Indigenous data misuse backlash | Low | Catastrophic | CARE Principles compliance + per-community opt-out + ethics board |
| OpenAI / Google releases competing product | Medium | High | Brand as "audited academic-grade" — credibility moat |

---

## 8. Go-to-market plan (first 90 days post-defense)

### Days 0-30: Foundation

- [ ] Form Paraguay entity (Sociedad Anónima or SAS)
- [ ] Register `paragu-ai.com` SaaS product on Cloudflare
- [ ] Publish P0011 paper (open-access on RSE)
- [ ] Launch public dashboard (`forestwatch.paragu-ai.com`)
- [ ] CFP (call for pilots) to 10 NGOs, 5 government agencies

### Days 30-60: Pilots

- [ ] Onboard 3 Basic + 1 Professional pilot (free 90 days)
- [ ] Submit 2 grants (NASA ROSES + WWF)
- [ ] Record 1 online course module (2 hours)
- [ ] Schedule 3 consulting pitches (soy co-op, ESG firm, audit firm)

### Days 60-90: Conversion + scale

- [ ] Convert pilots to paid (target 80% conversion)
- [ ] First press release (paper + dashboard)
- [ ] First speaking engagement (e.g., ESA Living Planet Symposium)
- [ ] File provisional patent on P0010 carbon-claim methodology (if novel enough)

---

## 9. Defensibility & moats

1. **Data moat** — Paraguay-specific curated tiles are 5+ years of curation work; not easily replicable.
2. **Compliance moat** — UNA IRB + INDI partnerships = barrier to new entrants.
3. **Academic moat** — 6 peer-reviewed papers + thesis = credibility competitors can't buy.
4. **Local moat** — Spanish + Guaraní + Portuguese trilingual; relationship with INFONA, INDI, UNA.
5. **Open-source reputation** — GitHub stars, contributor network, conference talks build trust.
6. **Ethics moat** — CARE-compliant per-community consent creates legitimacy for carbon markets.

---

## 10. KPIs to track

| KPI | Target Year 1 | Source |
|-----|---------------|--------|
| Paying SaaS customers | 17 | billing system |
| Active API calls/month | 100,000 | Cloudflare analytics |
| Papers accepted/published | 6 | publisher alerts |
| Grants awarded ($) | $800,000 | grant management |
| Consulting hours billed | 200 | invoicing |
| GitHub stars | 1,000 | GitHub API |
| MRR (monthly recurring revenue) | $50,000 MRR exit Y1 | billing |
| Net Promoter Score (B2B) | >50 | survey |
| FPIC communities covered | 10 (CARE-compliant) | ethics log |

---

## 11. Connection back to the thesis

Every section in `docs/CITATION.md`, `docs/STAKEHOLDERS.md`, and `paper.tex` files should
reinforce a commercialization thesis:

- **Introduction** → market size (ESG market = $30T+; carbon markets = $2B+ LATAM)
- **Methods** → reproducible IP (models, pipelines, data curation)
- **Results** → measurable accuracy claims (after honest reporting pass)
- **Discussion** → path-to-market (deforestation dashboards → SaaS; carbon under-claim → API)
- **Conclusion** → policy + commercial impact
- **Acknowledgments** → thank INFONA, INDI, UNA, and commercial partners

The thesis is **the marketing document**. Peer-review = third-party validation.
Defense = market entry event. Acceptance = media moment.

---

## 12. Decision: when to spin out?

| Trigger | Action |
|---------|--------|
| First $100k ARR | Hire first part-time dev + accountant |
| First $500k ARR | Hire CEO/CFO, move from SaaS-on-top-of-research to standalone company |
| First $2M ARR | Series A: $5-10M raise, 20-30 person team, 3-country expansion |
| First $5M ARR | Series B: $30-50M raise, M&A opportunities (acquire by Planet, Maxar, or ESG data firm) |

**Exit options (Y3-Y7):**

1. **Acqui-hire** by Planet Labs / Maxar / Google Earth Engine / ESRI — likely $20-100M
2. **Strategic acquisition** by carbon-credit registry (Verra, Gold Standard) — likely $50-200M
3. **ESG data rollup** (Watershed, Persefoni, Sylvera, Pachama consolidate) — likely $30-150M
4. **Independent IPO** (LATAM SaaS) — likely $300M-1B at scale
5. **Cooperative / non-profit** (mission-driven alternative — lower upside, more impact)

---

## 13. Open questions (to resolve in next 30 days)

- [ ] Confirm Paraguay entity type with local legal counsel (SA vs SAS vs Sucursal)
- [ ] Decide on SaaS provider (Cloudflare Workers + R2 vs AWS vs Supabase)
- [ ] Provisional patent for P0010 methodology (need IP lawyer opinion)
- [ ] Brand: ParaguAI (umbrella) vs satellite-paraguay (specific)
- [ ] First customer: who's the realistic anchor (INFONA? Itaipu? WWF?)
- [ ] Hire: where (Asunción? Buenos Aires? Remote-first?)
- [ ] Equity: 100% Iván vs co-founders vs SAFE-notes

---

## 14. Related documents

- `docs/CITATION.md` — how to cite (built credibility)
- `docs/STAKEHOLDERS.md` — partner map
- `docs/REAL_TODO.md` — operational priorities (drives deliverables)
- `docs/COMMERCIALIZATION_ROADMAP.md` — concrete next-90-days tasks
- `STATUS.md` — submission readiness per paper
- `BRUTAL_ROAST.md` — what NOT to over-claim when selling

---

**Last updated:** 2026-08-11
**Next review:** post-thesis-defense + after first paying customer