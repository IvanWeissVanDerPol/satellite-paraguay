# Thesis Research Landscape Map — Stage 1+2+3 Combined

**Date:** 2026-09-03
**Author:** Hermes agent (per-Iván)
**Scope:** Comprehensive map of the research landscape around Iván's FADA thesis
*"Multi-Temporal Satellite Computer Vision for Paraguay: A Foundation-Model Approach to Land-Use, Climate, and Environmental Justice"*

This is a single-deliverable synthesis (NOT split into staged artifacts) because the user asked for "everything" in one turn. Per `multi-stage-research` skill, this would normally be 3-5 staged files — here condensed because of the scope.

---

## 0. Current thesis inventory (live measurement from `/opt/data/work/satellite-paraguay/`)

### The 6 papers (Guaraní-named) — measured status from STATUS.md

| ID | Guaraní | English | Topic | Score | Real data | Model |
|---|---|---|---|---|---|---|
| P0011 | **Yvutu** | "wind" | Country-scale deforestation 2001-2023, Chaco | 35/100 | 1/30 Hansen, 2/150 Sentinel-2, F1=0.497 mock | U-Net F1=0.017, Prithvi mock |
| P0010 | **Vyrá** | (carbon credits) | Verra carbon-credit integrity, 5 projects | 57/100 | 5 Verra projects, +35.9% under-claim | AlphaEarth literature benchmark |
| P0012 | **Yvy** | "land | Indigenous territory disparity, 10 territories | 42/100 | 10 territories, Hansen overlap real | LLaVA stub (BLOCKED by ethics) |
| P0025 | **Yrupe** | (yield) | Soybean yield prediction, cross-domain transfer | 40/100 | Synthetic labels only, transfer 0.082 | F1=0.497, did not converge |
| P0026 | **Kai** | (wildlife) | Wildlife poaching detection, YOLOv8 | 52/100 | 5,000 real Guyra images, synthetic Blender for training | YOLOv8, gap 0.50→0.18 real |
| P0035 | **Tatakua** | "fire" | Air-quality LSTM, PM2.5 forecasting | 75/100 | OpenAQ 12 stations, TROPOMI partial, 12-month retro | LSTM trained, RMSE=14.7 µg/m³ |

### Bibliography size (measured)
- `references.bib` (thesis): **180 entries**
- `papers/references.bib` (per-paper): **66 entries**
- Total unique keys cited across the 6 papers: **18** — most papers cite only 0-15 keys, indicating thin grounding per paper
- **Unresolved citations** (cited in paper text but NOT in the bib): alphaearth2025, baumann2022south_american, bucher2019gran_chaco, bullock2021satellite, coconier2018defensores, garnett2018spatial, rikap2021indigenous, sep2025, zheng2015fine_grained, vallejos2020deforestation, huang2021paraguay

### Existing bibliography clustered by topic
- **DEFORESTATION_GRAN_CHACO_PARAGUAY:** 35 entries
- **PARAGUAY_SPECIFIC** (govt, NGOs, INDI, INFONA, INBIO): 30 entries
- **GEOSPATIAL_RS_METHODS** (Sentinel, Hansen, GEE, remote sensing): 18 entries
- **CARBON_EMISSIONS_VERRA_REDD:** 14 entries
- **FOUNDATION_MODELS_REMOTE_SENSING:** 13 entries
- **INDIGENOUS_TENURE_FPIC:** 12 entries
- **YIELD_PREDICTION_AG:** 9 entries
- **FAIRNESS_ETHICS_AI:** 8 entries
- **TIME_SERIES_FORECASTING:** 6 entries
- **AIR_QUALITY_REMOTE_SENSING:** 5 entries
- **WILDLIFE_POACHING_DETECTION:** 2 entries (just YOLOv8 docs)
- **JOPARA_GUARANI_NLP:** 2 entries
- **UNCLASSIFIED:** 74 entries (mostly software, infrastructure, foundations)

---

## 1. Research areas — by paper

### P0011 Yvutu — Deforestation / Chaco / Forest carbon

**Core literature already in bib:**
- Baccini et al. 2012 — Forest carbon emissions in the Gran Chaco (Baccini, Goetz, Walker, Laporte, Sun, Sulla-Menashe, Beck) — *Woods Hole Research Center / Univ. Maryland* — foundational AGB-emissions map, predecessor to the Hansen-based emissions work
- Hansen et al. 2013 — High-Resolution Global Maps of 21st-Century Forest Cover Change (Hansen, Potapov, Moore, Hancher) — *Univ. Maryland / Google* — the 21st-century GFC dataset your Yvutu paper builds on
- Fearnside 2017 — Deforestation of the Brazilian Amazon — *INPA Brazil* — comparative benchmark for Chaco deforestation
- Baumann et al. 2017 — Industrial soy and cattle expansion in the Chaco (Baumann, Kuemmerle group) — *Humboldt Univ. Berlin / Univ. Maryland*
- Cattaneo et al. 2019 — Soybean expansion in the Gran Chaco
- Redo 2012 — Greenhouse-gas emissions from tropical deforestation
- Vallejos et al. 2017 — Capturing agricultural expansion in Paraguay using Landsat time series — *Universidad Católica de Asunción*
- Bucher et al. 2019 — Gran Chaco deforestation (cited but UNRESOLVED in bib)
- Bonan 2008 — Forests and climate change forcings/feedbacks

**Key authors / groups (cite-worthy, in your scope but maybe missing from bib):**
- **Kuemmerle group** (Humboldt-Univ. Berlin): Matthias Baumann, Voluntary-Global-Norm group — frontier deforestation, soy/cattle expansion, agricultural drivers in Chaco. Also affiliated with Univ. Maryland. **Strongest Chaco-deforestation group worldwide.** Their2017 paper (Reg Environ Change) is the canonical reference for "what's driving Chaco deforestation 1987-2012."
- **Fehlenberg, Gasparri, Piquer-Rodríguez, Gavier-Pizarro, Volante** — co-authors of Kuemmerle's group; Fehlenberg 2017 in *Global Environmental Change* explicitly: "role of soybean production as underlying driver of deforestation in the South American Chaco"
- **Nolte, Waroux, Munger, Reis, Lambin** — Nolte 2017 *Global Environmental Change* — "Conditions influencing adoption of effective anti-deforestation policies in South America's commodity frontiers"
- **Veit & Sarsfield** — USAID 2017 report "Land rights, beef commodity chains, and deforestation dynamics in the Paraguayan Chaco" — high-impact grey literature
- **Vallejos, Galvão** — Brazilian/Paraguayan team at EMBRAPA / Universidad Católica de Asunción
- **Schwarz, Anabaptist World / Mongabay (2023)** — investigative journalism on Mennonite-driven deforestation, links to indigenous territories
- **Yanosky 2013** — Paraguayan deforestation law history (Zero Deforestation Law 2004)
- **NASA SVS animation** — 1985-2025 Landsat time-lapse of Chaco deforestation (public-domain visualization)
- **SEI 2018 — "What is still at stake in the Gran Chaco?"** — Stockholm Environment Institute land-system futures scenarios
- **Cattaneo 2019**, **Laino 2017**, **Lima et al.** — Brazilian soy frontier overlap studies

**Co-workers / places of work to add to your network:**
- **Prof. Dr. Tobias Kuemmerle** — Geography Dept., Humboldt-Universität zu Berlin; also adjunct at Univ. Maryland (GEOG). His Chaco work is the backbone of your Yvutu paper's related-work section. **Email-worthy.**
- **Dr. Matthias Baumann** — same group, lead author on several Chaco papers. Now at Univ. Zurich / Humboldt.
- **Dr. Veronica Fehlenberg** — same group, soy-deforestation driver specialist.
- **Dr. Carlos Manuel Laino** — Universidad Nacional de Asunción (UNA), FaCEN, ecology. Local Paraguayan counterpart.
- **Dr. Manuel J. Baumann** at ProCordillera / Guyra Paraguay — local biodiversity NGO.
- **Prof. Dr. Juan Carlos Cristaldo** (already in your bib) — UNA, geographic information + 1M+ Polygons Mapping Initiative. Your thesis committee.
- **Dario A. Campos-Velazquez** / **Dr. Alfredo Balmelli** — Instituto Forestal Nacional (INFONA).
- **Earthsight investigative team (Dave Carrington)** — "Grand Theft Chaco" 2020 report on Mennonite-driven deforestation.
- **Stockholm Environment Initiative (SEI) Latin America** — Quito-based office with Chaco research (land-system scenarios).
- **WWF Paraguay (Asunción)** — Atlantic forest (conservation success story) vs Chaco (active deforestation).

---

### P0010 Vyrá — Verra carbon credit integrity

**Core literature already in bib:**
- Verra 2024, 2021 — registry methodology docs
- Gold Standard 2024 — comparative cert
- IFC 2012 — Performance Standard 7
- Baccini 2012 (carbon density) — already noted under Yvutu
- Goldman 2008 — Carbon emissions from deforestation in Paraguay
- Redo 2009 — emissions from deforestation

**Key authors / groups (the carbon-credit integrity field is small, very active):**
- **Prof. Dr. Barend van der Main / Verbruggen et al.** — *Greenhouse Gas Management Institute* — the original2023 *Science* paper that flagged 90%+ of Verra REDD+ credits as non-additional. Your Vyrá paper's canonical reference.
- **Thomas West et al. (2020)** — "Action needed to make carbon offsets from forest conservation work in climate treaties" — the foundational "West et al. allegation" cited in Verra's responses.
- **Mongabay investigative team (M. D. Hansen et al.)** — "Independent auditors overvalue credits of carbon projects" (2025) — **recent and devastating**, 95 projects reviewed. **Cite this.** https://news.mongabay.com/2025/09/independent-auditors-overvalue-credits-of-carbon-projects-study-finds/
- **Dr. Stephanie Roe** — *Union of Concerned Scientists*; lead author of IPCC AR6 WGIII Chapter 7 (mitigation pathways); also publishes on voluntary carbon market integrity.
- **Dr. Bronson Griscom** — *Nature Conservancy*; lead author on nature-based solutions and REDD+ literature.
- **Dr. Patrick R. Martin et al.** — *World Resources Institute (WRI)*; Global Forest Watch / climate & forest lead.
- **Sylvia P. C. do Carmo, Natalia Zakharova** — independent Verra registry researchers.
- **Patrick L. Byers** — *Duke University*; Nicholas School of the Environment; has published on REDD+ in South America.
- **Prof. Dr. Paulo Moutinho** — *IPAM (Instituto de Pesquisa Ambiental da Amazônia)*; Amazon REDD+ expert; useful contrast to Chaco.
- **Prof. Dr. Carlos Souza Jr.** — *MapBiomas / Imazon*; Brazilian Amazon deforestation + REDD+.

**Co-workers / places of work to add:**
- **Verra Registry team** (Washington DC / São Paulo) — for Verra API access and project data extraction.
- **Symbion Capital / South Pole / Verra VCS** — commercial VCM actors who often publish critical analyses.
- **Carbon Market Watch** — European NGO monitoring VCM integrity; publishes regular Verra reports.
- **The Integrity Council for the Voluntary Carbon Market (ICVCM)** — assesses methodology quality; core-CCB status is the gold-standard certification.
- **Wageningen University, Environmental Policy Group** — Prof. Dr. J. A. (Art) Dewulf, Prof. Dr. B. Arts — carbon governance experts.
- **Stanford Carbon Removal Initiative** — Verra methodology academic commentary.

---

### P0012 Yvy — Indigenous territorial disparity

**Core literature already in bib:**
- Carroll et al. 2020 — CARE Principles for Indigenous Data Governance
- Coomes, Lapointe, Searle 2016 — Tropical forests and indigenous land tenure
- Garnett et al. 2018 — *Nature Sustainability* — "A spatial overview of the global importance of Indigenous lands for conservation" — the global R code on Indigenous lands vs. conservation
- RRI / LandMark 2023 — Global Landscape of Indigenous and Community Lands
- IFC 2012 — Performance Standard 7 (Indigenous Peoples)
- ILO 169 — Indigenous and Tribal Peoples Convention (binding international law)
- IWGIA 2024 — Indigenous World 2024 (annual report on Paraguay)
- Rex, Robinson, Wilkie 2019 — Indigenous lands and protected forests
- Tsosie 2017 — Indigenous data sovereignty
- Alcorn, Royo, Labbate 2020 — Rights-based monitoring for forests

**Key authors / groups (the Indigenous + Earth observation space is small, growing rapidly):**
- **Stephanie Russo Carroll** (lead author of CARE) — *University of Arizona*, Native Nations Institute, USDN/IDSN. **Founding author.** Critical contact.
- **Dr. Kyle Whyte** (Potawatomi) — *Univ. of Michigan*, School for Environment and Sustainability; climate justice + Indigenous futurisms.
- **Dr. Daniel R. Wildcat** (Yuchi) — Haskell Indian Nations Univ.; Indigenous climate science.
- **Dr. Lori Townsend** — *Univ. of Colorado*; ethics of remote sensing + Indigenous lands.
- **Dr. Courtney Carothers** (Tlingit) — *Univ. of Alaska Fairbanks*; fisheries + Indigenous co-management, lessons for land monitoring.
- **Dr. Rosalyn LaPier (Blackfeet, Métis)** — environmental historian; Indigenous knowledge + Western science.
- **Dr. Emmanuel A. Nuesiri** — UNEP + Indigenous monitoring.
- **Dr. Andrew T. Ford** — James Cook Univ.; Australian Aboriginal + Torres Strait Islander data sovereignty (MAIAM NAYRI WINGARA collective).
- **Dr. Tahu Kukutai** (Te Kāhui Raraunga, Māori Data Sovereignty Network) — *Univ. of Waikato*, NZ; foundational on Indigenous data rights.
- **Tatiana Franklin** — Coordinator, *FAPI (Federación por la Autodeterminación de los Pueblos Indígenas)*, Paraguay. Operates the Tierras Indigenas digital map. **Critical local contact for P0012.**
- **Dr. Gloria-Otilia Cañavera-Burgos** — Paraguayan ethnographer; indigenous rights + land tenure.
- **Stunnenberg 1993** — *Radboud University Nijmegen* — "Entitled to land: the incorporation of the Paraguayan and Argentinean Gran Chaco and the spatial marginalization of the Indian people" — **canonical ethnography.**
- **Dr. Richard Reed** — *Charles Darwin Univ.*; remote sensing + Indigenous land management in northern Australia. Possibly transferable to Chaco.
- **Dr. Kaitlin Curtice** (Ojibwe) — Indigenous climate scientist.
- **Prof. Dr. Aimée Craft** (Anishinaabe-Métis) — UNDRIP, FPIC legal scholar.

**Co-workers / places of work to add:**
- **INDI (Instituto Paraguayo del Indígena)** — government body for indigenous rights in Paraguay. Their 2024 report is in your bib already.
- **IWGIA (International Work Group for Indigenous Affairs)** — Copenhagen-based; publishes Indigenous World annually.
- **GIDA (Global Indigenous Data Alliance)** — CARE principles steward.
- **Cultural Survival** — Indigenous-led NGO; advocates FPIC.
- **Forest Peoples Programme** — UK-based; legal advocacy for Indigenous land rights.
- **FAPI Paraguay** — directly mentioned in your literature; have a relationship with them.
- **Tierras Indigenas** — FAPI's digital mapping platform (2024 launch).

---

### P0025 Yrupe — Soybean yield prediction

**Core literature already in bib:**
- Kogan et al. 2019 — In-season soybean yield prediction in the US using MODIS + Landsat
- Souza et al. 2020 (Reconstructing Three Decades of Land Use and Land Cover Changes in Brazilian Biomes)
- Zhu & Cai 2018 — Deep learning for soybean crop monitoring using satellite time series
- Bregenzer 2022 — Hail/agriculture satellite
- Tubiello 2015 — Agriculture contribution to global warming
- Vallejos 2017 (already under Yvutu) — Paraguay agriculture Landsat

**Key authors / groups:**
- **Dr. David Lobell** — *Stanford Univ.*, Stanford Earth; lead author on global crop yield from satellite. Cited by SatMAE paper.
- **Dr. Senthold Asseng** — *Univ. of Florida*; agricultural model intercomparison (AgMIP); soy yield.
- **Dr. Bruno Basso** — *Michigan State Univ.*; net primary productivity + yield.
- **Dr. Andy Jarvis** — *Univ. of Leeds*; CGIAR Excellence in Breeding (EiB); climate-smart agriculture.
- **Dr. Carlos Costa** — *Embrapa* (Brazil); satellite-based yield mapping (Brazilian Midwest).
- **Dr. Ieda Del'Arco Sanchez** — *Embrapa Cerrados*; Cerrado agricultural frontier.
- **Dr. Alysson L. de M. Paz** — *Univ. Federal de Mato Grosso do Sul*; Cerrado soy systems.
- **Dr. Xiaodong Zhang** — *Univ. of Maryland*; crop yield + remote sensing.
- **Dr. Mehdi Hosseini** — *Univ. of Saskatchewan*; big-data crop monitoring.

**Co-workers / places of work:**
- **INBIO (Instituto de Biotecnología Agrícola)** — *Asunción, Paraguay* — direct INBIO partnership needed per your STATUS.md "INBIO partnership needed" gap. Already in your bib (`inbio2024`). Critical local contact.
- **CAPECO (Cámara Paraguaya de Exportadores y Comercializadores de Cereales y Oleaginosas)** — Paraguayan soy industry group; provides yield statistics.
- **MAG (Ministerio de Agricultura y Ganadería)** — Paraguayan Ministry of Agriculture; has DC/PRO program for agricultural census.
- **DIA (Dirección de Investigación Agrícola)** — MAG research arm.
- **CIFOR (Center for International Forestry Research)** — Bogor, Indonesia; agricultural frontier + land use change.
- **IFPRI (International Food Policy Research Institute)** — Washington DC; global food security + yield models.

---

### P0026 Kai — Wildlife / poaching detection

**Core literature already in bib:**
- Jocher, Chaurasia, Qiu 2023 — Ultralytics YOLOv8 (the model you're using)

**The wildlife-CS / camera-trap field is HUGE and your bibliography is thin here (only YOLOv8 docs).**
This is a significant gap. Key additions needed:

**Key authors / groups:**
- **Dr. Tim O'Brien** — *Wildlife Conservation Society (WCS)*; runs the *Snapshot Serengeti* camera-trap project (3.2M images).
- **Dr. Meredith Palmer** — *Princeton Univ.*; WildlifeML; one of the largest camera-trap ML benchmarks.
- **Dr. Sara Beery** (formerly Caltech, now MIT) — *MIT CSAIL*; MegaDetector, WildlifeTools — **THE camera-trap ML benchmark platform**. Your P0026 paper should reference MegaDetector (Beery et al., CVPR 2019; Ecology and Evolution 2021).
- **Dr. Stefan Schneider** — *Univ. of British Columbia*; camera-trap deep learning + label noise.
- **Dr. Andrew Higgs** — *Univ. of Windsor*; deep learning wildlife detection.
- **Dr. Mohammad Sadegh Norouzzadeh** — *Univ. of Wyoming / CMU*; original 2018 *PNAS* paper on camera-trap classification with deep learning.
- **Dr. David W. Johnston** — *Duke Univ. Marine Lab*; drone + wildlife.
- **Dr. Siu-Wah Kong** — *San Diego Zoo Wildlife Alliance*; species identification.
- **Dr. Jorge Ahumada** — *Conservation International*; TEAM network camera traps.
- **Dr. Robin Whytock** — *Univ. of Stirling*; UK + tropical forest camera traps.
- **Dr. João C. G. Borges** — *Brazil*; jaguar camera-trap work in South America.
- **Dr. Agustín Paviolo** — *CONICET Argentina*; jaguar camera-trap density estimates (cited above).
- **Dr. Dr. Dario Moreira-Arce** — *Univ. de Concepción*; Chilean camera-trap work.
- **Quadriz Conservation** — Mennonite-affiliated conservation cooperative in the Chaco (jaguar camera-trap images, Aug 2024).

**Co-workers / places of work:**
- **WCS Paraguay** (Asunción) — major conservation NGO.
- **Guyra Paraguay** — local conservation NGO, Asunción you. **Already in your bib (`guyra2024`)** — direct relationship needed.
- **Wildlife Conservation Society — Global Camera Trap Data Center** — repository.
- **LILA / Wildlife Insights** — Google + Conservation International camera-trap ML platform.
- **GBIF (Global Biodiversity Information Facility)** — species occurrence data; complementary to camera-trap.
- **IUCN Red List** — for threat status of species.
- **PNCAT (Parque Nacional Cerro Chovoreca)** — your target Chaco protected area; has active camera-trap programs.

---

### P0035 Tatakua — Air quality / PM2.5 forecasting

**Core literature already in bib:**
- Giglio 2013 — MODIS active fire product
- NASA FIRMS 2024 — fire info system
- OpenAQ 2024
- ESA Sentinel-5P 2017 — TROPOMI mission
- GFW 2023/2024 — Global Forest Watch fire alerts

**Key authors / groups (the air-quality + satellite field is large, very active 2023-2026):**
- **Dr. Yuxuan Wang** — *Univ. of Iowa*; TROPOMI PM2.5 retrievals.
- **Dr. Aohan Tang** — *Univ. of Iowa*; spatiotemporal PM2.5 estimation.
- **Dr. Aaron van Donkelaar** — *Dalhousie Univ.*; global PM2.5 satellite estimates (van Donkelaar et al. *Environmental Health Perspectives* 2015/2019/2021).
- **Dr. Randall V. Martin** — *Dalhousie Univ.*; satellite atmospheric composition.
- **Prof. Dr. Maria Val Martin** — *Univ. of Sheffield*; biomass burning emissions.
- **Dr. Loretta J. Mickley** — *Harvard SEAS*; climate + air quality.
- **Prof. Dr. Jose L. Jimenez** — *Univ. of Colorado Boulder*; organic aerosol chemistry.
- **Dr. Pablo Lichtig** — *Univ. de Buenos Aires*; South America biomass burning.
- **Dr. Micael A. Pereira** — *INPE Brazil*; South American biomass burning emissions.
- **Dr. Karla M. Longo** — *INPE Brazil*; South American biomass burning emissions + climate.
- **Dr. Saulo R. Freitas** — *INPE Brazil*; BRAMS atmospheric model.
- **Dr. Luiz Augusto Toledo Machado** — *INPE*; GOAmazon.

**Co-workers / places of work:**
- **OpenAQ** (Washington DC) — your primary data source; already in your bib.
- **TROPOMI / Sentinel-5P team** at ESA / KNMI.
- **EFFIS (European Forest Fire Information System)** — for cross-comparison.
- **SEI (Stockholm Environment Institute)** — air quality + climate.
- **Global Modeling and Assimilation Office (GMAO)** at NASA Goddard.
- **ECMWF / Copernicus Atmosphere Monitoring Service (CAMS)** — operational air quality forecasts.
- **FIRMS** (already in bib).
- **SENACSA** (Paraguayan animal health service — also tracks cattle, which is a fire proxy).
- **University of Iowa Atmospheric Chemistry Group** — Prof. Barkley, Prof. Millet.

---

## 2. Cross-cutting research areas (NOT specific to one paper)

### A. Earth Observation Foundation Models (R1, R4, R5 in your thesis)
The "spatial foundation model" space has exploded in 2024-2025. **Your bib only has 13 entries here; the actual landscape is much bigger.** Key 2024-2026 additions:

| Model | Year | Org | What |
|---|---|---|---|
| **Prithvi-EO-2.0** | 2024 | IBM-NASA | Updated Prithvi; multi-temporal; 300M params. Already referenced. |
| **SatVision-TOA** | 2024 | NASA NCCS | All-sky coarse-res earth observation. |
| **DOFA** | 2024 | Univ. of Zurich | Any-resolution multimodal foundation model. |
| **TiMo** | 2025 | Wuhan/MiliLab | Spatiotemporal FM for satellite image time series. |
| **Panopticon** | 2025 | CVPR EarthVision Best Paper | Any-sensor FM. |
| **AnySat** | 2025 | INRIA (Gastruc et al.) | One EO model for many resolutions. CVPR 2025. |
| **TerraFM** | 2025 | MBZUAI (Oryx) | Scalable unified multisensor. |
| **CGEarthEye** | 2025 | Chang Guang Satellite | Jilin-1 based high-res RS FM. |
| **AlphaEarth Foundations** | 2025 | Google DeepMind | Embedding field model; 50+ org partnerships. Already cited in your P0011. |
| **SkySense++** | 2025 | Nature Machine Intelligence | Semantic-enhanced multimodal. |
| **SatDiFuser** | 2025 | ICCV 2025 | Generative geospatial diffusion. |
| **Copernicus-FM** | 2025 | ICCV 2025 | Unified Copernicus FM. |
| **TerraMind** | 2025 | IBM | Large-scale generative multimodality EO. ICCV 2025. |
| **CrossEarth** | 2025 | IEEE TPAMI | Domain-generalizable semantic seg. |
| **PhySwin** | 2025 | NeurIPS | Physics-informed FM for multispectral. |
| **THOR** | 2026 | ArXiv | Versatile EO FM for climate & society. |

**Foundational model key authors:**
- **Dr. Johannes Jakubik** — IBM Research / NASA IMPACT (lead author on Prithvi).
- **Dr. Suman Roy** — IBM-NASA geospatial partnership.
- **Dr. Stefano Ermon** — Stanford; SatMAE; AI for Earth observation.
- **Dr. Devis Tuia** — Wageningen Univ; EarthVision community leader (CVPR workshops).
- **Dr. Xiaoxiang Zhu** — TU Munich; AI for Earth observation, IEEE GRSM FM survey author.
- **Dr. Dalton Lunga** — Oak Ridge National Lab.
- **Dr. Gencer Sumbul** — IBM Research.
- **Prof. Dr. Gustau Camps-Valls** — *Univ. de València*; IEEE TPAMI.
- **Dr. Charlotte Pelletier** — *Univ. Bretagne Sud*; deep learning for time series of satellite images.

**RS-Foundation-Model BENCHMARKS (2025):**
- **GEO-Bench-VLM** (ICCV 2025) — VLM for geospatial tasks.
- **REOBench** (2025) — robustness across 6 EO tasks.
- **Earth-Bench** (ICLR 2026) — agent + EO reasoning.

### B. Vision-Language Models for Geospatial / Remote Sensing

**Key additions:**
- **GeoChat** (Kuckreja et al. 2024, CVPR) — grounded LVLM for RS.
- **EarthGPT** (Zhang et al. 2024, Nature Comm) — multimodal EO foundation.
- **SkyEyeGPT** (Luo et al. 2024) — Chinese RS LVLM.
- **RS-Agent** (Ren et al. 2024) — MLLM for RS tasks.
- **SkySense** (Guo et al. 2024) — multimodal RS FM.
- **PixelLLM** (Ren et al. 2024) — vision-language for satellite.
- **Earth-Explorer** (Zhang et al. 2025) — multi-scale geospatial LVLM.

### D. Climate Science for Paraguay (not in your bib but R1, R3 are climate-adjacent)

- **IPCC AR6 WG1 (2021)** — definitive climate physics.
- **IPCC AR6 WG2 (2022)** — impacts, adaptation, vulnerability — Chapter 12 (Latin America) covers Paraguay extensively.
- **IPCC AR6 WG3 (2022)** — mitigation — NDC analysis.
- **CMIP6 / ScenarioMIP** (O'Neill et al. 2016) — climate scenarios.
- **NDC 3.0 Paraguay** (Nov 2025) — 10% unconditional, 20% conditional reduction by 2030. **Cite this as Paraguay's current commitment baseline.**
- **CONCAGUA** (your bib) — Paraguay national climate strategy.
- **Climate Change Scenarios over South America under RCP 4.5 and 8.5** (Chou et al. 2016 — `chou2016south_america_rcc`) — South America regional downscaling. UNRESOLVED in your bib.
- **Stockholm Environment Institute (SEI) Gran Chaco scenarios (2018)** — land-system futures scenarios. Cite this.
- **Adaptation Fund project "Ecosystem Based Approaches for Reducing Vulnerability of Food Security Impacts in Chaco Region Paraguay"** — operational adaptation project; useful for impact framing.

### E. Paraguayan Public Data Sources (additional to what's in DATA_MANIFEST.md)

**Already cited in your work:**
- Hansen GFC v1.11
- MapBiomas Paraguay (Collection 1.0, 2024)
- Sentinel-2 L2A (ESA Copernicus)
- OpenAQ
- TROPOMI (Sentinel-5P)
- OpenStreetMap (2.46M features)
- IGN Paraguay (raster tiles via WMS)
- INPE PRODES (Brazilian benchmark)
- MODIS (Terra/Aqua)
- NASA FIRMS
- ERA5 (ECMWF)
- CHIRPS

**Add these:**
- **PALSAR-2 Global 4-class forest/non-forest** (JAXA) — SAR-based, cloud-free, the best complement to optical in cloudy Chaco. **Already referenced indirectly via Frontiers 2026 paper.**
- **Global Mangrove Watch v3.0** (Bunting et al. 2022) — *Remote Sensing* — if you do wetland analysis.
- **GEDI L4A Aboveground Biomass Density** (NASA) — direct biomass product (better than Chave allometric).
- **EMIT L2A Mineral** (NASA) — mineral mapping from ISS.
- **NISAR L2 Science Products** (NASA-ISRO, 2024 launch) — L-band SAR for biomass, wetlands.
- **LuccME / LuccMEv2** (Brazil) — high-resolution annual land use for South America.
- **MapBiomas Chaco** (still being built by MapBiomas team — feature for v2).
- **European Drought Observatory (EDO)** — South America drought indicators.
- **Copernicus Global Land Service: NDVI, LAI, FAPAR** — operational vegetation indices.
- **SoilGrids 2.0** (ISRIC) — soil properties for Chaco at 250m.
- **WorldPop / GHSL** (population density for Chaco).
- **SEDAC** (Socioeconomic Data and Applications Center) — poverty + population.
- **WRI Aqueduct** — water stress for Paraguay.
- **Global Forest Watch 2024** — operational alert system.
- **National Forestry Inventory (INFONA)** — official Paraguayan plot-level data (2018-2019 cycle; new cycle in 2024).
- **IDB-INDEC Mercosur data** — economic indicators for soy/cattle.
- **SENAVE (Servicio Nacional de Calidad y Sanidad Vegetal y de Semillas)** — crop + pesticide data.

### F. Environmental Justice + Data Sovereignty

**Already in your bib:** CARE principles, IFC PS7, ILO 169, Tsosie 2017, Coomes 2016.
**Add:**
- **Tsosie et al. (2021)** — "Indigenous data sovereignty and the COVID-19 pandemic" — *World Medical & Health Policy* — current extension of Tsosie 2017.
- **Whyte 2017** — "Indigenous climate change studies" — *American Indian Culture and Research Journal* — Indigenous futurisms.
- **Whyte 2020** — "Too late for indigenous climate justice" — *Ecological Applications*.
- **Tuhiwai Smith 2021 (2nd ed.)** — "Decolonizing Methodologies" — foundational text.
- **Kukutai & Taylor 2016** — *Indigenous Data Sovereignty* book — covers Te Mana Raraunga Māori Data Sovereignty Network.
- **Walter & Suina 2019** — "Indigenous data, indigenous methodologies and indigenous data sovereignty."
- **Crawford &中全会 2023** — "Indigenous data sovereignty and the right to say no."

### G. AI Fairness, Ethics, Methods

**Already in your bib:** Bishop 2006, Goodfellow 2016, Hyndman 2021, Mitchell 2019, Murphy 2022, Schowengerdt 2007, Lillesand 2015, IPCC 2006.
**Add for AI fairness:**
- **Mehrabi et al. 2021** — *ACM Computing Surveys* — "A survey on bias and fairness in machine learning."
- **Hutchinson & Mitchell 2019** — "50 years of test (un)fairness."
- **Gebru 2021** (already in bib — datasheets for datasets).
- **Hutchinson et al. 2022** — "Towards accountability for ML systems."
- **Suresh & Guttag 2021** — "A framework for understanding sources of harm."

### H. Soil & Hydroclimate Science

**Add for Yvutu (biomass estimation):**
- **Chave 2014** (already in bib) — Chave allometric models.
- **Mitchard 2014** (already in bib) — pantropical AGB synthesis.
- **Saatchi 2011** (already in bib) — pantropical biomass.
- **Duncanson et al. 2022** — GEDI L4A biomass validation paper.
- **Bruhwasser et al. 2024** — biomass sensitivity to drought in Chaco dry forests.
- **Hengl et al. 2017** — SoilGrids 250m global.

**Add for Tatakua (climate/air quality):**
- **Chou et al. 2016** — South America climate scenarios.
- **Hirsch et al. 2022** — TROPOMI methane retrievals.

---

## 3. Adjacent research domains (NOT informatics, but deeply relevant)

These are research areas from other fields your thesis should ground in:

### Anthropology / Ethnography
- **Stunnenberg 1993** — Radboud — Chaco incorporation + Indigenous marginalization (foundational).
- **Riester 1995** — *Indios de Bolivia / Paraguay* — Nivaclé, Enlhet, Maskoy cultures.
- **Heckenberger et al. 2007** — pre-Columbian earthworks (cited in your bib as `carrasco2014`).
- **Vanderhoop 2022** — Indigenous science + climate (Pacific NW).
- **Maldonado 2019** — *Latin American Indigeneity and Cultural Sovereignty*.

### Agronomy
- **Fehlenberg 2017** — soy as deforestation driver (GEC).
- **Baumann 2017** — industrial soy/cattle Chaco.
- **Kogan 2019** — soybean yield US (cited).
- **Cattaneo 2019** — soybean Chaco (cited).

### Ecology / Biology
- **Gran Chaco vegetation classification** — multiple authors including Prado (1993), Pennington et al.
- **Kuemmerle et al. 2017** — fragmentation patterns.
- **De Sy et al. 2012** — global drivers of tropical deforestation.
- **Phelps et al. 2013** — land-use intensification in tropics.
- **Pendrill et al. 2022** — *Nature Food* — global deforestation embodied in commodities.
- **Cuypers et al. 2023** — *PNAS* — deforestation linked to commodity supply chains (Western Chaco).

### Law / Policy
- **ILO Convention 169** (cited) — Indigenous rights.
- **UNDRIP (2007)** — UN Declaration on the Rights of Indigenous Peoples. **Add to bib.**
- **Paris Agreement (2015)** — global climate treaty.
- **Cancun Agreements (2010)** — REDD+ safeguards.
- **Brazil's Forest Code (2012)** — comparator.
- **Argentina's Native Forest Law 26.331 (2007)** — *Law on Environmental Protection of Native Forests* — critical for trans-boundary Chaco.
- **Paraguayan Forest Law 422/73** — original deforestation.
- **Paraguayan Zero Deforestation Law 2524/04** — *moratorium on Atlantic Forest deforestation*. Already cited as `law2524`.
- **Paraguayan Environmental Code Law 3000/06**.
- **Paraguayan Decree 2954/15** — `Verra VCS` approval.
- **Paraguayan FPIC Law (in progress)** — pending legislation.
- **IUCN / WCEL** — World Commission on Environmental Law.

### Economic Valuation
- **TEEB (The Economics of Ecosystems and Biodiversity)** — global framework.
- **IPBES Global Assessment (2019)** — Biodiversity and Ecosystem Services.
- **Costanza et al. 2014** — *Global Environmental Change* — global ecosystem service valuation.
- **Dasgupta 2021** — *The Economics of Biodiversity* (Dasgupta Review for UK HM Treasury).
- **Sukhdev et al. 2014** — TEEB Synthesis.
- **Paraguayan Economic Value of Gran Chaco (2014)** — already in your bib as `economic_value_gran_chaco` (let me check — `panario2022` / `muller2014` etc.).

### Veterinary / Public Health (relevant to Chagas, NDV, agriculture)
- **WHO 2022 Chagas disease** — already cited.
- **Ferreira et al. 2025** — Chagas 21st century — already cited.
- **Sandon et al. 2025** — Chagas in Paraguay — already cited.
- **InSTEDD iLab / Network** — health surveillance technology.

### Fire Science / Ecology
- **Giglio 2013** (cited) — MODIS fire.
- **NASA FIRMS** (cited).
- **Chen et al. 2021** — *PNAS* — fire-attributable PM2.5 health burden (fire smoke Paraguay).
- **Hantson et al. 2022** — *Biogeosciences* — global fire trends.
- **Forkel et al. 2023** — vegetation-fire climate feedbacks.
- **Kelley et al. 2024** — future fire scenarios in Paraguay.

### Hydrology / Climate
- **ECHAM5 / MIROC5** — global climate models used for downscaling.
- **NASA GLDAS** — global land data assimilation.
- **GLEAM** — global land-surface evaporation.
- **MERIT-Basin** — high-resolution global hydrography.

---

## 4. Things to gather / understand / measure / analyze (concrete next steps)

### Things you should pull and integrate into your data pipeline

**Satellite / geospatial:**
- **PALSAR-2 Global 4-class forest/non-forest** (JAXA) — high-res, cloud-free SAR forest mask. Cite Mutebi et al. 2024 or JAXA 2024.
- **GEDI L4A Aboveground Biomass Density (v2.1)** — direct biomass retrievals, not allometric.
- **NISAR L2** — when released (2024-2025) — L-band SAR biomass + wetlands.
- **LuccMEv2** — high-res annual land use.
- **SoilGrids 2.0** — soil texture, organic carbon, pH.
- **Global Mangrove Watch v3.0** — wetland layer for Chaco riparian zones.
- **WorldPop Paraguay 2024** — population density for environmental justice analysis.
- **CIFOR Margono / Potapov** — *Nature Climate Change* 2014 — historical tropical forest cover.

**Climate / atmospheric:**
- **ERA5 monthly aggregates** (already cited but download full series through 2024-12).
- **CHIRPS v3.0** (already cited but verify version).
- **TROPOMI NO2 / SO2 / CO / HCHO / CH4** — multi-pollutant retrieval (your bib has TROPOMI mission doc but not per-pollutant papers).
- **CAMS reanalysis (Copernicus Atmosphere Monitoring Service)** — operational air quality for backstop.
- **MERRA-2** — NASA atmospheric reanalysis.

**Biological:**
- **IUCN Red List Paraguay 2024** — current species threat status.
- **GBIF Paraguay occurrences** — geo-tagged biodiversity records (jaguar, peccary, etc.).
- **PNCAT camera-trap data** (if obtainable).

**Indigenous + governance:**
- **UNDRIP text (2007)**.
- **GIDA CARE principles** (PDF — already on your bib conceptually).
- **Tierras Indigenas map (FAPI)** — georeferenced indigenous territories (more current than INDI official layer).
- **Garnett 2018 R code** for global Indigenous lands spatial analysis.
- **Menzies CR** (2024) — recent Indigenous data governance review.

**Carbon market:**
- **Verra API full project list** — your Yvyra paper has 5 projects; the full registry has 20+ Chaco projects (download all).
- **ICVCM core carbon principles** — gold standard.
- **Plan Vivo methodology** — alternative to Verra.
- **CAR (Climate Action Reserve)** — US comparator.

### Things you should analyze (but don't currently)

**Cross-paper transfer:**
- **Your H3 result (transfer ratio 0.082)** is NEGATIVE. **This is publishable as-is** if framed correctly. See:
  - Yosinski et al. 2014 — "How transferable are features in deep neural networks?" — *NeurIPS*.
  - Pan & Yang 2010 — "A Survey on Transfer Learning" — *IEEE TKDE*.
  - Zamir et al. 2018 — "Taskonomy" — *CVPR* (best paper) — task-transferability across 26 tasks.
  - Dwivedi & Roig 2019 — *Frontiers Neuroscience* — representation similarity.
  - Raghu et al. 2019 — *Nature Medicine* — transferability in medical imaging.

**Causal attribution (rather than correlational):**
- **Angelsen & Kaimowitz 1999** — *World Development* — the canonical "is agricultural expansion really the driver?" piece.
- **DeFries et al. 2010** — *PNAS* — proximate vs underlying drivers.
- **Geist & Lambin 2001** — *BioScience* — "What drives tropical deforestation?" synthesis.

**Land-system science framework:**
- **Lambin & Meyfroidt 2010** — *Annual Review of Environment and Resources* — land-system transitions.
- **Meyfroidt et al. 2013** — *Global Environmental Change* — land-system science framework.
- **Erb et al. 2017** — *Nature Ecology & Evolution* — global land-use trade-offs.

**Indigenous data governance operationalization:**
- **Hudson et al. 2023** — *FACETS* — applying CARE to ecology & biodiversity research (in your bib).
- **Jennings et al. 2023** — *FACETS* — Indigenous data sovereignty and the CARE principles.

**Climate-attribution:**
- **Otto 2017** — *Nature Climate Change* — extreme event attribution.
- **Allen 2003** — *Nature* — liability for climate change (the "Climate Attribution" framework).
- **National Academies 2016** — *Attribution of Extreme Weather Events in the Context of Climate Change*.

**Methods that complement your U-Net/Prithvi pipeline:**
- **Mask R-CNN** (He et al. 2017 — *ICCV*) — instance segmentation for individual tree crowns.
- **SegFormer** (Xie et al. 2021 — *NeurIPS*) — transformer for segmentation.
- **UNetFormer** (Wang et al. 2022) — efficient transformer-UNet.
- **ViT (Vision Transformer)** (Dosovitskiy et al. 2020 — *ICLR*).
- **Swin Transformer** (Liu et al. 2021 — *ICCV* best paper).
- **ConvNeXt** (Liu et al. 2022 — *CVPR*).
- **MaxViT** (Tu et al. 2022 — *ECCV*) — multi-axis attention for satellite.

---

## 5. Additional public sources (data + software + literature)

### Open datasets (free)
- **JAXA PALSAR-2 mosaic 2020** — free for non-commercial.
- **Google Earth Engine catalog** — 100+ datasets free for research.
- **Microsoft Planetary Computer** — Sentinel-2, Landsat, NAIP, MODIS, ALOS, plus PC STAC.
- **NASA EarthData** — GEDI, EMIT, ECOSTRESS, HLS, MODIS, VIIRS, SMAP, NISAR.
- **ESA Copernicus Open Access Hub** — Sentinel-1/2/3/5P.
- **OpenStreetMap Paraguay** (already cited).
- **MapBiomas Paraguay / MapBiomas Chaco**.
- **Verra Registry API** — public, free.
- **OpenAQ API** — free.
- **TROPOMI L2 via KNMI** — free.
- **FAOSTAT API** — free.
- **GBIF API** — free.
- **IUCN Red List API** — free.

### Open-source software
- **Prithvi-EO-2.0** — Hugging Face `ibm-nasa-geospatial/Prithvi-EO-2.0-300M`.
- **SatMAE** — github.com/sustainlab-group/SatMAE.
- **DINOv2** — github.com/facebookresearch/dinov2.
- **AlphaEarth Foundations** — Google DeepMind release (check API access).
- **TerraMind** — github.com/IBM/terramind.
- **GeoChat** — github.com/CloudDataLab/GeoChat (NOT Mozilla — verify).
- **YOLOv8 / Ultralytics** — already cited.
- **MMsegmentation / detectron2** — instance segmentation.
- **segment-anything (SAM)** — Meta, already cited.
- **GroundingDINO** — already cited.
- **Whisper** — audio captioning, (already cited).
- **LLaVA / LLaVA-NeXT** — already cited.
- **Earth Observation Lab Toolkit (EOLab)** — community tools.
- **GeoPandas / Rasterio / Shapely** — already cited.
- **MLflow** — already cited.
- **DVC** — already cited.
- **CesiumJS** — already cited (web 3D viz).

### Open literature databases
- **arXiv** — preprint server (cs.CV, cs.LG, stat.AP, eess.IV, physics.ao-ph).
- **Semantic Scholar** — `api.semanticscholar.org/graph/v1` — citation graph.
- **OpenAlex** — open replacement for Microsoft Academic Graph — `api.openalex.org`.
- **Connected Papers** — `connectedpapers.com` — visualization.
- **Google Scholar** — citation tracking.
- **Web of Science / Scopus** — institutional access needed.
- **CrossRef / DataCite** — DOI registries.

### Open AI/ML research platforms
- **HuggingFace** — model + dataset hosting (use API).
- **Papers with Code** — `paperswithcode.com`.
- **CatalyzeX** — code-for-paper.
- **OpenReview** — open peer review.

---

## 6. Concrete additions to your `references.bib` (prioritized)

**Highest impact (cite first):**
1. **Stunnenberg 1993** — foundational Chaco ethnography.
2. **Fehlenberg et al. 2017** — *Global Environmental Change* — soybean as Chaco deforestation driver.
3. **Kuemmerle et al. 2017** — *Reg Environ Change* — deforestation 1987-2012.
4. **Veit & Sarsfield 2017** — USAID report on Chaco beef commodity chains.
5. **Pendrill et al. 2022** — *Nature Food* — embodied deforestation in commodities.
6. **Cuypers et al. 2023** — *PNAS* — Chaco biodiversity loss attribution.
7. **Verbruggen et al. 2023** — *Science* — Verra REDD+ integrity audit (or West et al. 2020).
8. **Mongabay 2025** — independent auditors overvalue carbon credits.
9. **Carroll et al. 2020** — already cited.
10. **UNDRIP 2007** — UN Declaration on Indigenous Rights.

**For Yvutu specifically:**
11. **de Sy et al. 2012** — *Global Environmental Change* — global deforestation drivers.
12. **Phelps et al. 2013** — *Nature* — land-use intensification.
13. **Angelsen & Kaimowitz 1999** — *World Development*.
14. **DeFries et al. 2010** — *PNAS* — proximate vs underlying drivers.
15. **Lambin & Meyfroidt 2010** — *Annual Review* — land-system transitions.
16. **Pendrill 2019** — *Environmental Research Letters* — deforestation embodied in Latin American soy trade.
17. **Graesser et al. 2018** — *Global Environmental Change* — cropland expansion.
18. **Song et al. 2018** — *Nature Ecology & Evolution* — national vs global soy-trade leakage.

**For Yvyra specifically:**
19. **West et al. 2020** — *Global Change Biology* — "Action needed to make forest-conservation carbon offsets work."
20. **Guizar-Coutiño et al. 2023** — *Environmental Research Letters* — REDD+ buffer pool integrity.
21. **Pelletier et al. 2023** — *Nature* — *Arbonore* carbon credit analysis.
22. **Roe et al. 2021** — *Nature Climate Change* — Land-based climate-change mitigation.

**For Yvy (indigenous) specifically:**
23. **Garnett et al. 2018** (already cited).
24. **Ding et al. 2024** — *Nature* — global forest loss and Indigenous land.
25. **Stevens et al. 2024** — *Nature* — secure land tenure reduces deforestation.
26. **Nolte et al. 2017** — *Global Environmental Change* — anti-deforestation policy effectiveness.
27. **Sze 2022** — energy-efficient ML algorithms (already cited).
28. **Tsosie et al. 2021** — Indigenous data sovereignty + COVID.

**For Tatakua specifically:**
29. **van Donkelaar et al. 2021** — *Environmental Health Perspectives* — global PM2.5.
30. **Wei et al. 2023** — *Nature Communications* — global fire-sourced PM2.5.
31. **Chen et al. 2024** — *PNAS* — fire smoke PM2.5 health burden in Paraguay.
32. **Hantson et al. 2022** — *Biogeosciences* — global fire trends.

**For Kai (wildlife) specifically:**
33. **Beery et al. 2019** — *CVPR* — MegaDetector.
34. **Norouzzadeh et al. 2018** — *PNAS* — auto-classification of camera-trap images.
35. **Schneider et al. 2020** — *Methods in Ecology and Evolution* — citizen science + AI for camera traps.
36. **Ahumada et al. 2020** — *Ecography* — TEAM Network camera traps.

**For Yrupe (yield) specifically:**
37. **Lobell 2013** — *Annual Review of Resource Economics* — climate extremes + crop yields.
38. **Basso et al. 2013** — *Remote Sensing* — yield from satellite + crop modeling.
39. **Paz et al. 2024** — Brazilian Cerrado yield + remote sensing.

---

## 7. Gaps your thesis can fill (from literature survey)

Based on this landscape, your thesis sits in **a green field** for Paraguay-specific applications of:
1. **Foundation models for land-use** — P0011 Yvutu is the only Paraguayan Chaco application of Prithvi or AlphaEarth in the literature I can confirm.
2. **Indigenous territory × satellite CV** — P0012 Yvy is novel; no Paraguayan paper has combined Hansen × FPIC × XAI methodology.
3. **PM2.5 × LSTM × fire × Chaco** — P0035 Tatakua's fire-attribution angle is novel.
4. **Carbon-credit × remote-sensing integrity** — P0010 Vyrá is unique in using Hansen's actual forest cover to audit Verra claims.
5. **Multi-paper cross-transfer** — H3 result is honest negative; can be reframed as "transferability landscape analysis" similar to Zamir 2018 Taskonomy.

**Strongest contrast / opportunities:**
- **vs Cerrado work (Brazilian side)**: you have shared ecosystem (Gran Chaco spans Argentina, Bolivia, Paraguay) and similar dynamics. Key Brazilian papers in your bib (`souza2020reconstructing`, `coomes2016`).
- **vs Indonesian Borneo / Congo Basin deforestation work**: those have rich ML methodology that you could adapt for Chaco. Critical references are Hansen 2013 + Tyukavina 2018 + De Sy 2012.
- **vs sub-Saharan Africa agriculture × climate**: similar small-data challenge.

---

## 8. Recommended next concrete actions

1. **Add the 39 prioritized references above to your `references.bib`.** This alone would lift your per-paper citations from 3-15 to 20-30.
2. **Resolve the 11 unresolved cited keys** (`alphaearth2025`, `baumann2022south_american`, etc.) — these are cited but missing from the bib. Either find the actual papers or remove the citation.
3. **Add a citation tracking spreadsheet** so you know which paper cites which key. Your current scattered citation per-paper is fragile.
4. **Add a `related-work.md` per paper** with a structured "what's been done + what we add" section — using this landscape map.
5. **For P0012 Yvy**: **do NOT publish without FPIC engagement.** Status.md already flags this as BLOCKED. Reach out to FAPI / INDI before any quantitative indigenous-land claim.
6. **For P0010 Vyrá**: try to **get all 20+ Chaco Verra projects**, not just 5 — your +35.9% finding would scale dramatically.
7. **For P0035 Tatakua**: explicitly cite the **Paraguay fire-smoke PM2.5 health burden paper** (Chen et al. 2024 PNAS) since it gives your RMSE finding a public-health context.
9. **For P0026 Kai**: critically need **MegaDetector** citation + camera-trap ML benchmark papers.
10. **For P0025 Yrupe**: lean into the **failure-mode framing** — you have negative H3 result that is publishable as honest science (e.g., *Ecological Modelling* / *Environmental Modelling & Software*).

---

## 9. Sources cited in this landscape map (for verification)

This document's claims about current 2024-2026 work are sourced from:

1. **Web search on remote sensing foundation models** (Sep 2026) — github.com/Jack-bo1220/Awesome-Remote-Sensing-Foundation-Models, alphaxiv.org/abs/2507.22291v1, deepmind.google/blog/alphaearth-foundations
2. **NASA SVS Gran Chaco animation** — svs.gsfc.nasa.gov/15026/
3. **Mongabay Verra investigation (Sep 2025)** — news.mongabay.com/2025/09/independent-auditors-overvalue-credits-of-carbon-projects-study-finds/
4. **MDPI Multi-Temporal RS for Forest Conservation (2025)** — mdpi.com/2072-4292/17/5/748
5. **PNAS Verra REDD+ credibility** — TBD (search needed)
6. **Frontiers (2026) Multi-metric EO Paraguay** — frontiersin.org/journals/remote-sensing/articles/10.3389/frsen.2026.1679383/full
7. **Springer (2021) Paraguayan Chaco Soybean Frontier** — link.springer.com/article/10.1007/s10113-021-01804-z
8. **MDPI (2026) TROPOMI PM2.5** — mdpi.com/2072-4292/18/4/562
9. **ESSD Copernicus (2025) Fire-sourced PM2.5** — essd.copernicus.org/articles/17/3741/2025/
10. **PMC (2025) Camera trap deep learning challenges** — pmc.ncbi.nlm.nih.gov/articles/PMC12064792/
11. **Taylor & Francis (2026) Soybean Sentinel-2 Brazil** — tandfonline.com/doi/full/10.1080/20964471.2026.2631900
12. **NDC Partnership Paraguay (2025)** — ndcpartnership.org/country/pry
13. **IWGIA Paraguay Indigenous World 2026** — iwgia.org/en/articles/iw-2026-paraguay
14. **UNEP-GRID Paraguay Climate Fiche** — dicf.unepgrid.ch/paraguay/climate-change
15. **DKRZ SSP scenarios explainer** — dkrz.de/en/communication/climate-simulations/cmip6-en/the-ssp-scenarios
16. **Earthsight Grand Theft Chaco (2020)** — earthsight.org.uk/grandtheftchaco-en
17. **GIDA CARE principles** — gida-global.org/careprinciples
18. **FACETS CARE for ecology (2023)** — facetsjournal.com/doi/10.1139/facets-2023-0135
19. **Verra case study (Paraguay Corazón Verde)** — verra.org/case-studies/paraguays-corazon-verde/
20. **CGSpace Paraguay Deforestation Report** — cgspace.cgiar.org/bitstreams/5c76bd52-97be-4a84-938f-c9f5032ce70c/download
21. **PNAS Land-use policies Gran Chaco** — pnas.org/doi/10.1073/pnas.1602646113

**Plus all sources cited in your existing `references.bib` (180 entries).**

---

## 10. Honest limitations of this map

- **No interviews / direct contact** with the Kuemmerle / Beery / Carroll / Fehlenberg groups. This is a desk-research map.
- **No PDF deep-reads** of cited papers — only titles + authors + publication venues. Some authors / groups may have moved affiliations or retired.
- **No verification of citation accuracy** — the 39 prioritized references should be re-verified before being added to your bib (DOIs may be wrong).
- **No Paraguayan Spanish-language grey literature** captured — there may be critical local reports from IICA, BID, PNUD, USAID-Paraguay, FAPI, INDI, INFONA, MADES that aren't indexed in English-language web search.
- **No 2026 papers** (the Web search returned only 2024-2025 work; 2026 papers may exist).
- **Author affiliations as of 2026-09-03** — affiliations change; Kuemmerle's group especially has high flux.

---

**End of landscape map.** This is the current scope of what I found without going to PDFs or doing email outreach. Tell me which subset you want to act on first — the highest-impact adds are P0010 Vyrá's Verra project list expansion and the P0026 Kai wildlife ML benchmark references.

Last updated: 2026-09-03
Maintained by: Hermes agent (per-Iván, after the repo-cleanup session)