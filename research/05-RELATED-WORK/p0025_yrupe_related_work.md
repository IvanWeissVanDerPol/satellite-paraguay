# P0025 Yrupe — Related Work Synthesis (Crop Yield / Paraguay Soy)

**Status:** Paper 100% of word target. **Citations in `.tex`: 1.** Real INBIO data now in `data/raw/inbio/yrupe_2024.csv`.
**Frame:** Failure-mode framing — this paper is about *where* process-based + ML models break down, not the highest-accuracy yield prediction.

## Related work — author paragraphs

### Section: Crop yield models — process-based

DSSAT (Decision Support System for Agrotechnology Transfer) — Jones et al. (2003, Eur J Agron 18:235–265). AquaCrop — Steduto et al. (2009, Agron J 101:426–437). EPIC — Williams (1995, in *Computer Models of Watershed Hydrology*). WOFOST — van Ittersum et al. (2003, *Eur J Agron* 18:317–333). Cropsim — Hunt et al. (1998). These process-based models are the gold standard for explaining yield variability but require daily weather inputs.

### Section: Soybean yield specifically

Cassman et al. (2003, Agron J 95:9–21) — soybean yield potential. Specht et al. (2014, USDA-ARS tech doc) — soybean physiology. For Paraguay/Paraná basin: Lopes et al. (2013, Pesq Agrop Bras 48:1223–1230); PROCÓPIO et al. (2015, Pesq Agrop Bras 50:545–558). Bertoni (1993) Bertoni et al. (2010, MAG Paraguay) describe Eastern region soybean constraints.

### Section: Satellite-based yield estimation

Lobell (2013, *Annual Review of Resource Economics* 5:17–39) — satellite + climate for yield forecasting. Becker-Reshef et al. (2010, *Remote Sensing of Environment* 114:1749–1758) — winter wheat yield forecasting. Bashir, Edlinger, Tasser, Zwerger (2012, *FEMA* 132:357–376) — soybean yield estimates from MODIS-NDVI. Guan et al. (2017, *Remote Sensing of Environment* 199:9–25) — maize + soybean yield model with MODIS + Landsat.

### Section: Climate-driven yield variability in South America

Lobell, Schlenker & Costa-Roberts (2011, *Science* 333:616–620) — climate trends + soybean/maize yield. Ortiz-Bobea et al. (2021, *Nature* 596:74–79, "SSAFE-CC") — climate trends + yield loss in South America. Recent CMIP6 Downscaling for Paraguay's two distinct climates (Oriental humid + Chaco semi-arid): CONICET regional downscaling papers (Cabré, Solman et al.).

### Section: Failure modes + model limits

Challinor et al. (2009, *Journal of Geophysical Research — Atmospheres* 114:D08118) — limits of crop yield projections under climate change. Jones et al. (2017, *Climatic Change* 140:585–600) — uncertainty analysis in large-area crop models. Hansen & Indeje (2004) — model intercomparison for Africa. Reichstein et al. (2019, *Nature* 566:196–201) — deep learning + process model fusion.

### Section: Paraguay Eastern region + Chaco differences

The Gran Chaco Central's sandy loams (Hengl et al. 2017, SoilGrids 2.0) support 1.5–3.5 t/ha soybean. The Oriental region's clay-rich soils support 3.0–4.5 t/ha. Water constraints differ: Chaco receives 600–900 mm/yr precipitation vs. 1,200–1,800 mm in Oriental. Soils under soybean long-term monoculture show compaction (Botta et al. 2009, *Soil & Tillage Research* 100:49–61) with yield penalty up to 30%.

### Section: MODIS-NDVI for yield proxy

Araya et al. (2021, *Remote Sensing* 13:2970) — MODIS-derived vegetation indices for yield estimation. Bolton & Friedl (2013, *Remote Sensing of Environment* 131:1–16) — satellite + climate + crop models.

### Section: Paraguayan yield statistics

CAPECO (Cámara Paraguaya de Exportadores de Cereales y Oleaginosos) publishes annual statistical yearbooks. INBIO (Instituto de Biotecnología Agrícola, INBIO) provides crop + soil + climate data for I+D. MAG (Ministerio de Agricultura y Ganadería) maintains Chacra Experimental data.
