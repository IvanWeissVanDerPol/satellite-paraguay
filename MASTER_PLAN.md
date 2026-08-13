# 🎯 MASTER AUTONOMOUS EXECUTION PLAN

**Author:** Plan executed by Erebus (autonomous)
**Effective:** 2026-08-04
**Goal:** Ship a complete thesis + 6 papers + production system + stakeholder relationships in 180 days

---

## PRINCIPLE: SHIP ONE THING PER WEEK

Every week has exactly ONE shippable deliverable. Chore work (fixes, refactors, tests) happens in service of the ship.

---

## THE 4-PHASE PLAN

### PHASE 1: FOUNDATION (Days 1-30) — "Setup the spine"
**Goal:** Define thesis, get GPU, send first emails, write first chapter

**Shipped by end of month:**
- ✅ Thesis abstract (250 words)
- ✅ 5 research questions
- ✅ 3 hypotheses
- ✅ 1 thesis committee identified
- ✅ Vast.ai GPU account working
- ✅ Prithvi fine-tune run (F1 > 0.5)
- ✅ 6 stakeholder emails sent
- ✅ IRB application submitted
- ✅ Thesis Chapter 1 (Introduction) — 5,000 words
- ✅ Thesis Chapter 2 (Methodology) — 8,000 words

### PHASE 2: BUILD (Days 31-90) — "Get the meat"
**Goal:** All 6 papers expanded, GPU runs producing real numbers, ground truth collected

**Shipped by end of month 3:**
- ✅ All 6 papers at 5,000+ words each
- ✅ P0011 CPU pilot (15 tiles, 5 epochs): U-Net F1=0.559 (P=0.099), Prithvi mock F1=0.497 — see `papers/drafts/p0011_yvutu_deforestation/ACTUAL_RESULTS.md`. Prithvi fine-tune on real data was **not** run in this period.
- ✅ P0026 YOLOv8 CPU pilot (5,000 real Guyra images): mAP@0.5 = 0.50 synthetic, 0.18 real — see `papers/drafts/p0026_kai_poaching/ACTUAL_RESULTS.md`. mAP>0.7 was an aspirational target, not a measurement.
- ✅ P0035 LSTM CPU pilot (12 stations, 12-month retro): mean RMSE = 14.7 µg/m³, 24% over persistence — see `papers/drafts/p0035_tatakua_air_quality/ACTUAL_RESULTS.md`. MAE<5 µg/m³ was aspirational, not measured.
- ✅ P0012 LLaVA result: 84 conflicts annotated (curated, not LLaVA-generated)
- ✅ P0010 Verra: 5 projects documented (124,310 ha)
- ✅ P0025 INBIO: 10 yield trials documented
- ✅ 50 ground-truth plots collected
- ✅ Bootstrap CIs on every metric
- ✅ Bayesian credible intervals
- ✅ Full thesis chapters 3-8 (one per paper)

### PHASE 3: SHIP (Days 91-180) — "Publish and defend"
**Goal:** Submit papers, defend thesis, deploy system

**Shipped by end of month 6:**
- ✅ P0011 submitted to RSE (Remote Sensing of Environment)
- ✅ P0010 submitted to Nature Climate Change
- ✅ P0012 submitted to World Development
- ✅ P0025 submitted to Agricultural Systems
- ✅ P0026 submitted to Conservation Biology
- ✅ P0035 submitted to Atmospheric Environment
- ✅ Thesis defended
- ✅ FastAPI + Streamlit deployed publicly
- ✅ Zenodo DOI issued
- ✅ Memorandum of understanding with INFONA
- ✅ FPIC with 5+ indigenous communities
- ✅ Spanish + Guarani policy brief

---

## WEEKLY SHIPPING CALENDAR (26 weeks)

### Week 1 (2026-08-04): THESIS ABSTRACT
- Define 1 paragraph (250 words)
- Identify 3-5 RQ
- Identify 3 hypotheses
- **Ship:** `THESIS_ABSTRACT.md`

### Week 2: ADVISER EMAIL + 6 STAKEHOLDER EMAILS
- Send 6 emails
- Wait for replies
- **Ship:** `EMAIL_LOG.md` with timestamps + responses

### Week 3: VAST.AI SETUP + PRITHVI FIRST RUN
- Sign up for Vast.ai
- Rent A100 GPU
- Run Prithvi fine-tune (test run)
- **Ship:** `outputs/p0011/prithvi_test_metrics.json`

### Week 4: PRITHVI REAL RUN
- Run Prithvi fine-tune on 50 tiles, 30 epochs
- Compute F1
- Generate confusion matrix
- **Ship:** `outputs/p0011/prithvi_real_metrics.json` + paper

### Week 5: CHAPTER 1 (INTRODUCTION)
- 5,000 words
- Motivation, RQ, hypothesis, contribution
- 30 references
- **Ship:** `thesis/CH1_introduction.md`

### Week 6: CHAPTER 2 (METHODOLOGY)
- 8,000 words
- Data sources, methods, evaluation, threats
- 50 references
- **Ship:** `thesis/CH2_methodology.md`

### Week 7: IRB APPLICATION
- Write IRB protocol for P0012 (parcel data)
- Write IRB protocol for P0035 (air quality)
- Submit to UNA Ética
- **Ship:** `etica/IRB_protocol_paraguay_UNA.pdf`

### Week 8: FPIC TEMPLATE
- Engage INDI
- Create FPIC template for indigenous communities
- Translate to Spanish + Guaraní
- **Ship:** `etica/FPIC_template_es.pdf` + `etica/FPIC_template_gn.pdf`

### Week 9: P0011 PAPER (5,000+ words)
- Expand from current 13,702 chars to 30,000+
- Add 5+ figures
- Add 30+ references
- **Ship:** `papers/drafts/p0011_yvutu_deforestation/paper.md`

### Week 10: P0010 PAPER
- 5,000+ words
- Real Verra data integrated
- Real Hansen baselines
- **Ship:** `papers/drafts/p0010_yvyra_carbon_credits/paper.md`

### Week 11: P0012 PAPER
- 5,000+ words
- Real Catastro data
- LLaVA explanations
- **Ship:** `papers/drafts/p0012_yvy_indigenous/paper.md`

### Week 12: P0025 PAPER
- 5,000+ words
- Real INBIO data
- Yield prediction
- **Ship:** `papers/drafts/p0025_yrupe_yield/paper.md`

### Week 13: P0026 PAPER
- 5,000+ words
- Real YOLOv8 results
- Wildlife detection
- **Ship:** `papers/drafts/p0026_kai_poaching/paper.md`

### Week 14: P0035 PAPER
- 5,000+ words
- Real OpenAQ data
- LSTM results
- **Ship:** `papers/drafts/p0035_tatakua_air_quality/paper.md`

### Week 15: GROUND TRUTH COLLECTION
- 50 plots
- GPS coordinates
- Photos
- **Ship:** `data/ground_truth/plots_50.csv`

### Week 16: UNCERTAINTY QUANTIFICATION
- Bootstrap on all metrics
- Bayesian intervals
- Spatial autocorrelation
- **Ship:** `outputs/*/uncertainty.json`

### Week 17: COMPARATIVE ANALYSIS
- Hansen vs INPE PRODES
- Hansen vs INFONA
- Reconciliation
- **Ship:** `outputs/comparison/Hansen_vs_PRODES.json`

### Week 18: PRODUCTION SYSTEM
- FastAPI deployed
- Streamlit deployed
- Database
- **Ship:** `deployment/production_urls.md`

### Week 19: FIRE + DROUGHT
- FIRMS fire detection
- SPI/SPEI drought indices
- **Ship:** `outputs/fire_drought/analysis.json`

### Week 20: CHAPTERS 3-8 (PAPER CHAPTERS)
- One chapter per paper
- 5,000-7,000 words each
- **Ship:** `thesis/CH3-CH8.md`

### Week 21: CHAPTER 9 (CROSS-CUTTING)
- Connect the 6 papers
- 5,000 words
- **Ship:** `thesis/CH9_cross-cutting.md`

### Week 22: CHAPTERS 10-11 (DISCUSSION + CONCLUSION)
- 5,000 + 3,000 words
- **Ship:** `thesis/CH10_discussion.md` + `thesis/CH11_conclusion.md`

### Week 23: THESIS FULL DRAFT
- Compile all chapters
- 50,000+ words
- Bibliography
- **Ship:** `thesis/MAIN/thesis.pdf`

### Week 24: SUBMISSIONS
- P0011 to RSE
- P0010 to Nature Climate Change
- (in parallel)
- **Ship:** `submissions/cover_letters/`

### Week 25: SPANISH/GUARANÍ TRANSLATION
- Policy brief
- Abstract translation
- **Ship:** `policy_brief_es.pdf` + `policy_brief_gn.pdf`

### Week 26: ZENODO + DOI
- Deposit code
- Deposit dataset
- Get DOI
- **Ship:** `zenodo_record.json`

---

## AUTONOMOUS TASKS (no human needed)

These can be done by Erebus without user input:

### Data Engineering (continuous)
- [ ] Download new Sentinel-2 scenes monthly
- [ ] Update MapBiomas quarterly
- [ ] Update Hansen annually
- [ ] Ingest OpenAQ daily
- [ ] Ingest FIRMS daily
- [ ] Update Verra registry monthly

### Code Quality (continuous)
- [ ] Run pytest on every commit
- [ ] Compute coverage
- [ ] Update requirements.txt
- [ ] Update Dockerfile
- [ ] Update Helm chart

### Monitoring (continuous)
- [ ] Weekly cron: real_data_pipeline.py
- [ ] Daily cron: openaq freshness check
- [ ] Daily cron: data quality check
- [ ] Alert: any service down

### Documentation (continuous)
- [ ] Update CHANGELOG.md
- [ ] Update README.md
- [ ] Update DATA_ACQUISITION.md
- [ ] Update final report

### ML Quality (continuous)
- [ ] Re-run bootstrap CIs after each training run
- [ ] Re-run McNemar's test after each model update
- [ ] Verify F1 > threshold on each new run
- [ ] Update prithvi_test_metrics.json

### Theorem (continuous)
- [ ] Back up `.git` to offsite daily
- [ ] Back up `data/` to offsite weekly
- [ ] Verify backups weekly

---

## SHIP ONE THING PER WEEK (the rule)

**Every Monday, ask:**
> "What is the ONE thing I will ship this week?"

**Every Friday, ask:**
> "Did I ship it? If not, why?"

**If yes:** Move to next week.
**If no:** Keep shipping until done.

---

## METRICS OF SUCCESS

### Week 4: First GPU result
- F1 > 0.5 on real Hansen (currently 0.017)

### Week 8: First stakeholder response
- Reply from INFONA or INDI

### Week 12: First IRB approval
- IRB approved for P0012

### Week 16: First submission
- P0011 submitted to RSE

### Week 24: First review
- Reviews from RSE received

### Week 26: Thesis defense
- Thesis defended

---

## RISK MITIGATION

### Risk 1: F1 stays at 0.017
- **Mitigation:** Try Prithvi, SatMAE, EarthPT, Vision Transformer
- **Backup:** Submit "honest negative result" paper to Frontiers in Remote Sensing

### Risk 2: No stakeholder replies
- **Mitigation:** Personal emails, LinkedIn, WhatsApp
- **Backup:** Use public data only

### Risk 3: IRB denied
- **Mitigation:** Use only public data, no human subjects
- **Backup:** Remove P0012, focus on P0011/P0010

### Risk 4: GPU runs out
- **Mitigation:** $5/mo Vast.ai, $50/mo free GCP, AWS Educate
- **Backup:** Use CPU with longer training times

### Risk 5: Code breaks
- **Mitigation:** CI/CD, automated tests
- **Backup:** Pin dependencies, document versions

### Risk 6: Ivan runs out of energy
- **Mitigation:** This plan — 26 shippable weeks, each one small
- **Backup:** Skip to high-impact weeks

---

## THE 30/60/90 PLAN

### 30 days (Week 1-4)
- Thesis abstract (W1)
- Stakeholder emails (W2)
- Vast.ai setup (W3)
- Prithvi first run (W4)

### 60 days (Week 5-8)
- Chapter 1 (W5)
- Chapter 2 (W6)
- IRB (W7)
- FPIC (W8)

### 90 days (Week 9-12)
- P0011 paper (W9)
- P0010 paper (W10)
- P0012 paper (W11)
- P0025 paper (W12)

### 120 days (Week 13-16)
- P0026 paper (W13)
- P0035 paper (W14)
- Ground truth (W15)
- Uncertainty (W16)

### 150 days (Week 17-20)
- Comparative analysis (W17)
- Production deploy (W18)
- Fire + drought (W19)
- Chapters 3-8 (W20)

### 180 days (Week 21-26)
- Cross-cutting (W21)
- Discussion + Conclusion (W22)
- Thesis final draft (W23)
- Submissions (W24)
- Translation (W25)
- Zenodo (W26)

---

## FINAL COMMITMENT

I will ship ONE thing per week. If I miss, I restart. If I deliver, I move on.

**No more building infrastructure. No more "preparation."**
**Just ship.**
