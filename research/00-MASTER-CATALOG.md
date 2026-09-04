# Thesis Research Landscape — Master Catalog (Session 2 Update)
**Date:** 2026-09-03
**Author:** Hermes agent (per-Iván)
**Session:** Continuation — gathered actual papers, datasets, software, and organizations
**Storage:** `/opt/data/profiles/ivan/research/thesis-landscape-2026-09-03/`

---

## What's new since the Stage 1+2+3 combined artifact

The previous landscape map identified the research areas, authors, and citations needed. This session **actually pulled the materials** into a structured archive organized by paper topic:

- **14 papers** with full text/summaries (3-150KB each)
- **6 datasets** with metadata and download paths
- **3 software** repos and HuggingFace model cards
- **3 Paraguay-specific** government/policy documents
- **3 organization** profiles (FAO, IWGIA, Tierras Indigenas)

Total: **29 files**, **~1.2 MB** of source material ready to be cited in your thesis.

---

## 🟢 New papers fetched (with full reference info)

### For P0011 Yvutu (deforestation)

| Paper | Authors / Year | Where saved | Key finding |
|---|---|---|---|
| **Kuemmerle 2017** (Deforestation & cattle expansion in Chaco 1987-2012) | Kuemmerle T., Baumann M., et al. — *Reg Environ Change* | (referenced in Mongabay / Sci-Direct / ResearchGate) | 44,000 km² Chaco loss 1987-2012; 86.16% classification accuracy |
| **Henderson 2021** (Paraguayan Chaco soybean frontier) | Henderson, J., Godar, J., Frey G.P. et al. — *Reg Environ Change* 21:72 | `papers/henderson2021_chao_soybean_frontier.md` | 742,000 ha suitable + 940,000 ha moderately suitable for soy expansion; Corredor-Bioceánico drivers |
| **Carpenter 2025** (Biodiversity decline in Gran Chaco) | Carpenter I., **Kuemmerle T., Romero-Muñoz A., Aguiar S., Gasparri I., Lathuillière M., Nanni S., Ribero V., Baumann M.** — *Global Environmental Change* 92, 103011 | `papers/carpenter2025_chaco_biodiversity_supply_chains.md` | Pasture has higher biodiversity impact than cropland; EU imports 25% of South American soy; Paraguay top beef importers: Chile, Russia, Israel |
| **Gapare & Sperlich 2026** (Forest dataset comparison Paraguay) | Gapare N., Suresh G., Sperlich D. — *Frontiers in Remote Sensing* | `papers/gapare_sperlich2026_paraguay_forest_datasets.md` | GFW has 3-35% deviation from Dynamic World/PALSAR-2 in Paraguay; Dynamic World performed best |
| **Bullock 2023** (GEDI biomass + Paraguay NFI) | Bullock E.L., Healey S.P., Yang Z., **Acosta R., Villalba H., Insfrán K.P. (INFONA), Melo J., Wilson S., Duncanson L., Næsset E.** — *Environ. Res. Lett.* 18 085001 | `papers/bullock2023_gedi_paraguay_nfi.md` | **Mean AGBD Paraguay = 65.55 Mg/ha** (range 52.34-103.88); standard errors 47% lower with hybrid inference; direct INFONA contacts (Acosta, Villalba, Insfrán) |
| **Earthsight 2020** (Grand Theft Chaco) | Earthsight (Carrington D., Schwarz B.) investigative report | `papers/earthsight2020_grand_theft_chaco.md` | Ayoreo-Totobiegosode forced cattle ranching links to BMW, Range Rover, Italian tanneries; 20% of Chaco deforestation illegal |

### For P0010 Vyrá (Verra carbon credit integrity)

| Paper / Source | Authors / Year | Where saved | Key finding |
|---|---|---|---|
| **Berkeley 2023** (Quality Assessment of REDD+ Carbon Credit Projects) | Berkeley Carbon Trading Project (Goldman School) — 196 pp. report | `papers/berkeley2023_redd_quality_assessment.md` | "REDD+ is ill-suited to generation of carbon credits for use as offsets" |
| **Chase et al. 2025** (REDD+ over-claiming) | Chase J. et al. (iDiv, MLU Halle-Wittenberg) — *Science* | `papers/redd2025_science_synthetic_control.md` | Only ~1 in 8 tradable REDD+ credits = real reductions; 19% met emissions targets; synthetic control method |
| **Mongabay 2025** (Verra auditors overvalue credits) | Ruas C., Giles C. (Univ. Pennsylvania Law) — *SSRN* | `papers/mongabay2025_verra_audit.md` | 2/3 of auditors failed to flag flaws in 95 flawed Verra projects; structural conflict of interest |
| **Verra Digital Gateway API** | Verra registry | `datasets/verra_registry_scraper_apify.md` | 9,000+ Verra + Gold Standard projects scrapable via Apify (no account needed) |

### For P0012 Yvy (Indigenous land tenure + remote sensing)

| Paper | Authors / Year | Where saved | Key finding |
|---|---|---|---|
| **Garnett 2018** (Indigenous lands global) | Garnett S.T., Burgess N.D., Fa J.E., Fernández-Llamazares Á., Robinson R., Zander K.K. — *Nature Sustainability* 1:369-374 | `papers/garnett2018_indigenous_lands_global.md` | **38M km² Indigenous lands globally** in 87 countries; intersects 40% of all terrestrial protected areas |
| **Tierras Indigenas** (FAPI digital map) | FAPI Paraguay (coordinated with UCINY, CLIBCH, Tierraviva, GAT, Sombra de Árbol, WWF Paraguay) | `organizations/tierras_indigenas_fapi.md` + official launch | Digital map of Paraguay's indigenous territories, integrated with GFW + LandMark, launched Nov 2017; **13 of 19 Indigenous Peoples contributed** |
| **IWGIA Paraguay** (current country profile) | International Work Group for Indigenous Affairs | `organizations/iwgia_paraguay.html.md` | **19 Indigenous Peoples in Paraguay**; **5 linguistic families** (Guaraní, Maskoy, Mataco-Mataguayo, Zamuco, Guaicurú); ILO 169 ratified; UNDRIP voted for but not enforced |

### For P0026 Kai (wildlife / camera trap ML)

| Paper / Source | Authors / Year | Where saved | Key finding |
|---|---|---|---|
| **Beery 2019** (MegaDetector original paper) | Beery S., Morris D., Yang S. — KDD19 Data Mining for Conservation Workshop, arXiv:1907.06772 | `papers/beery2019_megadetector_arxiv.md` | Original MegaDetector pipeline; trained on transfer learning from animal detector + regional classifier |
| **Microsoft MegaDetector V6** | Microsoft AI for Good Lab | `software/microsoft_megadetector.md` | Current V6 with PyTorchWildlife; 80+ conservation orgs use it; SPARROW edge-AI device |
| **Mulero-Pázmány 2025** (Camera-trap DL challenges) | Mulero-Pázmány M., Hurtado S., Barba-González C., Antequera-Gómez M.L., Díaz-Ruiz F., Real R., Navas-Delgado I., Aldana-Montes J.F. (Univ. Málaga) — *Sci Rep* 15:16191 | `papers/mulero_pazmany2025_camera_trap_dl.md` | Real-world challenges: animal/empty imbalance, similar species confusion, background impact |

### For P0035 Tatakua (air quality / fire-smoke)

| Paper | Authors / Year | Where saved | Key finding |
|---|---|---|---|
| **Chen et al. 2024** (Fire-smoke PM2.5 health burden in Paraguay) | (Chen et al.) — *Science of the Total Environment* 2024 | `papers/pubmed_paraguay_fire_smoke_pm25.md` | Annual fire smoke PM2.5 from fires expected to **increase by 7.7 µg/m³ by 2100**; Paraguay suffers disproportionate health burden |
| (Other wildfire-PM2.5 papers: *Yale YSPH 2025*, *iScience 2025* — covered in landscape map, not yet fetched) |

### Foundation models (R1, R4, R5)

| Paper / Source | Authors / Year | Where saved | Key finding |
|---|---|---|---|
| **AlphaEarth Foundations** | Google DeepMind team (Brown C., Kazmierski M., Pasquarella V., Rucklidge W., Samsikova M., Wiles O., Zhang C., Lahera E., Shelhamer E., Ilyushchenko S., Gorelick N., Zhang L.L., Alj S., Schechter E., Askay S., Guinan O., Moore R., Boukouvalas A., Kohli P.) — arXiv:2507.22291 | `papers/deepmind2025_alphaearth_foundations.md` | Embedding field model; 64-dim vectors, 10m resolution; **released as Satellite Embedding V1 dataset on GEE** for 2017-2024 |
| **Prithvi-EO-1.0 / 2.0** | Jakubik J., Roy S., Phillips C.E., Fraccaro P. et al. (IBM-NASA) | `software/prithvi_eo1_earthdata_release.md` + `software/prithvi_ibm_nasa_huggingface.md` | Prithvi-EO-2.0 is **600M params, 6× bigger than 1.0**, trained on 4.2M HLS points; **topped GEO-Bench leaderboard**; use cases: Amazon canopy height, Valencia floods, Baltimore heat islands |
| **Berkeley Carbon Trading Project** | Berkeley Goldman School | (under P0010) | Foundational REDD+ critique |

---

## 🟢 New datasets cataloged

| Dataset | Provider | Where saved | Resolution / Coverage | Use for paper |
|---|---|---|---|---|
| **Satellite Embedding V1** (AlphaEarth) | Google DeepMind / GEE | `datasets/satellite_embedding_v1_gee.md` | 10m, 64-dim, 2017-2024 | **Yvutu** (replaces need for custom Prithvi fine-tune?) |
| **GEDI L4A v2.1 Raster** | NASA / USFS LARSE / GEE | `datasets/gedi_l4a_v2.1_gee.md` | ~25m, Mg/ha, 2019-2023 | **Yvutu** AGB |
| **GEDI L4A v3 Footprint** | NASA / ORNL DAAC | `datasets/gedi_l4a_v3_nasa.md` | ~25m, Mg/ha, 2019-2024+, ISS | **Yvutu** AGB |
| **PALSAR-2 Global FNF4** (4-class) | JAXA / GEE | `datasets/palsar2_fnf4_gee.md` | 25m, 2017-2021, dense/non-dense/non-forest/water | **Yvutu** + **Vyrá** (cloud-free forest mask) |
| **PALSAR-2 Dataset History (JAXA direct)** | JAXA EORC | `datasets/palsar2_jaxa_dataset_history.md` | 25m, 2007-2025 (Ver.2.6.0) | **Yvutu** + **Vyrá** |
| **Verra Registry Scraper** (Apify) | jungle_synthesizer | `datasets/verra_registry_scraper_apify.md` | 9,000+ projects, JSON | **Vyrá** (need to scale from 5 → 20+ Chaco projects) |
| **Tierras Indigenas** (FAPI map) | FAPI Paraguay | (under organizations/) | Live, integrated with GFW + LandMark | **Yvy** (canonical indigenous territories) |

---

## 🟢 New software cataloged

| Tool | Provider | Where saved | Key use |
|---|---|---|---|
| **Microsoft MegaDetector V6** | Microsoft AI for Good Lab | `software/microsoft_megadetector.md` | Pre-trained animal/person/vehicle detector for camera traps — **must adopt for Kai P0026** |
| **Prithvi-EO-1.0/2.0** | IBM-NASA HuggingFace | `software/prithvi_eo1_earthdata_release.md` + `software/prithvi_ibm_nasa_huggingface.md` | HLS-based foundation model for EO tasks — **paper cites this but consider Prithvi-EO-2.0 as v2 in Yvutu** |
| **PyTorchWildlife** | Microsoft | (referenced in MegaDetector) | New unified API: `MegaDetectorV6()` |

---

## 🟢 New Paraguay-specific material

| Source | Where saved | What's new |
|---|---|---|
| **NDC 3.0 Paraguay** (Nov 2025) | `paraguay-specific/ndc_partnership_3.0.md` + `ndc_lac_profile.md` | **10% unconditional + 20% conditional** GHG reduction by 2030/2035; submitted Nov 6, 2025; covers entire economy; 7 adaptation sectors |
| **INFONA National Forest Inventory 2026** | `paraguay-specific/infona_ifn_2026_release.md` | **Freshest authoritative forest data for Paraguay** — 10-year milestone inventory; explicit Nivaclé collaboration; April 2026 release |
| **Tierras Indigenas (FAPI)** | `organizations/tierras_indigenas_fapi.md` + official | FAPI digital map for Paraguay indigenous territories; **launched with WRI/USAID/GFW integration** |
| **IWGIA Paraguay profile** | `organizations/iwgia_paraguay.html.md` | **5 linguistic families, 19 Indigenous Peoples**; UN Special Rapportur 2016 critical country visit |
| **FAO FRA 2020** | `organizations/fao_fra2020.html.md` | 60+ forest variables across 236 countries; Paraguay-specific data extractable |

---

## 🎯 Recommended next actions by paper (concrete, actionable)

### P0011 Yvutu (deforestation) — TOP priority
1. **Add to bib:** Bullock 2023 (GEDI + Paraguay NFI) — **directly applicable** to AGB validation
2. **Add to bib:** Gapare & Sperlich 2026 (Frontiers in Remote Sensing) — justifies dataset choice (Dynamic World > GFW for Paraguay)
3. **Add to bib:** Carpenter 2025 (Gran Chaco biodiversity + supply chains) — connects Yvutu to economic attribution
4. **Adopt:** Satellite Embedding V1 dataset (AlphaEarth on GEE) — directly testable in your Yvutu pipeline, no custom training needed
5. **Adopt:** PALSAR-2 FNF4 (2017-2021) as cloud-free complement to Hansen
6. **Contact:** Regino Acosta / Hermelinda Villalba / Katherin Patricia Insfrán at INFONA (collaborators on Bullock 2023)

### P0010 Vyrá (Verra integrity) — TOP priority
1. **Add to bib:** Chase 2025 *Science* + Mongabay 2025 + Berkeley 2023 — three foundational critiques
2. **Pipeline:** Use Verra Apify scraper to get **all 20+ Chaco Verra projects** (currently only 5)
3. **Add to bib:** West 2020 *Global Change Biology* (foundational critique)
4. **Investigate:** Paraguayan Corazón Verde project specifically (Verra case study)

### P0012 Yvy (Indigenous) — TOP priority
1. **⚠️ CRITICAL:** Do NOT publish P0012 without FPIC engagement (BLOCKED per STATUS.md)
2. **Add to bib:** Garnett 2018 *Nature Sustainability* (the global anchor paper)
3. **Pipeline:** Pull Tierras Indigenas map from FAPI / LandMark
4. **Reference:** IWGIA Paraguay profile for the 19 Indigenous Peoples + 5 linguistic families list
5. **Add to bib:** CARE principles (Carroll 2020) — already cited but expand with newer extensions
6. **Add:** UNDRIP 2007 text (international law)
7. **Contact:** Tatiana Franklin (FAPI), GIDA network, INDI directly

### P0026 Kai (wildlife) — TOP priority
1. **Adopt:** Microsoft MegaDetector V6 + MegaDetector-Classifier (Beery et al. 2019) — **critical missing references**
2. **Add to bib:** Mulero-Pázmány 2025 *Sci Rep*
3. **Adopt:** PyTorchWildlife API (modern unified toolkit)
4. **Contact:** Sara Beery (MIT CSAIL) — direct expert
5. **Contact:** Agustín Paviolo (CONICET Argentina) for jaguar density estimates

### P0035 Tatakua (air quality)
1. **Add to bib:** Chen 2024 *STOTEN* (Paraguay fire-smoke PM2.5) — gives public-health context for RMSE 14.7 finding
2. **Add to bib:** Yale YSPH 2025 long-term mortality paper
3. **Add to bib:** ESSD 2025 global high-resolution fire-sourced PM2.5 (2000-2023)

### All papers — overarching
1. **NDC 3.0 (Nov 2025)** should appear in your thesis introduction as Paraguay's current commitment baseline
2. **INFONA IFN 2026** is the freshest authoritative Paraguayan forest data — use this for any AGB, forest cover, deforestation NFI validation
3. **Kuemmerle's group (Carpenter 2025, Henderson 2021, Kuemmerle 2017)** is THE Chaco research cluster — strong evidence your thesis sits in a major research lineage

---

## 📂 Where everything is stored

```
/opt/data/profiles/ivan/research/thesis-landscape-2026-09-03/
├── papers/                                       (14 files, ~750KB)
│   ├── bullock2023_gedi_paraguay_nfi.md          ★ direct INFONA contacts
│   ├── carpenter2025_chaco_biodiversity_supply_chains.md  ★ Kuemmerle group
│   ├── henderson2021_chao_soybean_frontier.md    ★ Kuemmerle group
│   ├── gapare_sperlich2026_paraguay_forest_datasets.md    ★ Paraguay datasets comparison
│   ├── garnett2018_indigenous_lands_global.md    ★ Nature Sustainability anchor
│   ├── earthsight2020_grand_theft_chaco.md       ★ Investigative report
│   ├── deepmind2025_alphaearth_foundations.md    ★ Embedding model
│   ├── mulero_pazmany2025_camera_trap_dl.md       ★ Wildlife ML
│   ├── pubmed_paraguay_fire_smoke_pm25.md         ★ PNAS-class public health
│   ├── mongabay2025_verra_audit.md               ★ Vyrá paper critique
│   ├── mongabay2025_chaco_biodiv_summary.md      ★ Biodiversity
│   ├── berkeley2023_redd_quality_assessment.md   ★ Vyrá paper critique
│   ├── redd2025_science_synthetic_control.md     ★ Vyrá paper critique
│   └── beery2019_megadetector_arxiv.md           ★ Kai paper ML
│
├── datasets/                                     (6 files, ~140KB)
│   ├── satellite_embedding_v1_gee.md             ★ AlphaEarth on GEE
│   ├── gedi_l4a_v2.1_gee.md                      ★ Yvutu biomass
│   ├── gedi_l4a_v3_nasa.md                       ★ Yvutu biomass
│   ├── palsar2_fnf4_gee.md                       ★ Cloud-free forest mask
│   ├── palsar2_jaxa_dataset_history.md           ★ PALSAR-2 2007-2025
│   └── verra_registry_scraper_apify.md           ★ Vyrá paper scaling
│
├── software/                                     (3 files, ~70KB)
│   ├── microsoft_megadetector.md                 ★ Kai paper must use
│   ├── prithvi_eo1_earthdata_release.md          ★ Foundation model
│   └── prithvi_ibm_nasa_huggingface.md           ★ Model hub
│
├── paraguay-specific/                            (3 files, ~45KB)
│   ├── ndc_partnership_3.0.md                    ★ NDC 3.0 official
│   ├── ndc_lac_profile.md                        ★ LAC NDC tracker
│   └── infona_ifn_2026_release.md                ★ INFONA IFN 2026
│
└── organizations/                                (3 files, ~40KB)
    ├── fao_fra2020.html.md                       ★ Global forest stats
    ├── iwgia_paraguay.html.md                    ★ Indigenous rights tracker
    └── tierras_indigenas_fapi.md                 ★ FAPI map
```

---

## ⚠️ Honest limitations

- **Not PDF deep-reads** — these are web extracts (HTML rendering of pages); some metadata is lost
- **IWGIA 2025/2026 articles are 404** — could not retrieve; the country profile is 2024 data
- **No Google Scholar citation graphs** — citation counts not pulled
- **No PDF of Stunnenberg 1993** — Radboud library access needed
- **No direct author contact** — these are digital artifacts only; relationship-building is separate work
- **No NDV (Network of Development Volunteers)** or Madidi/Chiquitano cross-border datasets pulled yet (Gran Chaco spans 4 countries)
- **Status of each saved file** is "saved verbatim" but some are truncated by web_extract — re-verify citations before adding to `references.bib`

---

## 🎓 What this means for your thesis

You now have **a working corpus of 29 sources** ready to be cited in your `references.bib`. The most important additions are:

1. **Bullock 2023** — your **#1 missing reference** for P0011 Yvutu (AGB validation + INFONA contacts)
2. **AlphaEarth Satellite Embedding V1** — your **#1 dataset opportunity** for Yvutu (no fine-tuning needed, just query embeddings)
3. **MegaDetector + PyTorchWildlife** — your **#1 missing methodology** for P0026 Kai
4. **Chase 2025 *Science*** — your **#1 critical citation** for P0010 Vyrá (most recent REDD+ over-crediting finding)
5. **Garnett 2018 + IWGIA + Tierras Indigenas** — your **#1 missing infrastructure** for P0012 Yvy
6. **Verra Apify scraper** — your **#1 missing tool** to scale Vyrá from 5 to 20+ projects
7. **NDC 3.0 + INFONA IFN 2026** — your **#1 freshest 2026 sources** for the thesis intro and framing

**Of the 11 unresolved cited keys I flagged in the previous artifact,** I've now captured or pointed to real sources for several — but the unresolved citation work (resolving `alphaearth2025`, `baumann2022south_american`, `bucher2019gran_chaco`, `bullock2021satellite`, etc.) is still a separate cleanup task.

---

**Next concrete steps:**

1. **Add to `references.bib`** — 14 specific BibTeX entries (you'd need to extract citation keys from the markdown files; I'll do I if you say go)
2. **Resolve remaining 11 unresolved cited keys** — search by year + author + topic
3. **Initiate 2-3 author contacts** — FAPI (Tatiana Franklin), INFONA (Acosta/Villalba), MegaDetector team (Sara Beery)
4. **Build per-paper `related-work.md` files** in your `papers/drafts/P0011/`, `P0012/`, etc.

Tell me which to do next.

Last updated: 2026-09-03 02:18 UTC
Maintained by: Hermes agent (per-Iván, session 2 of landscape research)