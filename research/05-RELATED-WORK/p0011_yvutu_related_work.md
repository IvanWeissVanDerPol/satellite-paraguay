# P0011 Yvutu — Related Work Synthesis (Deforestation / Gran Chaco)

**Status:** Paper 100% of journal target. Bibliography: 202+47=249 entries. Citations in `.tex`: 19 (raw count, includes multi-arg `\cite{a,b}`).
**Gap:** Has 1/30 Hansen tiles + 2/150 Sentinel-2 tiles. ~29 of 47 verified citations are Yvutu-relevant.

## Related work — author paragraphs (cited-friendly prose)

### Section: Gran Chaco deforestation context

The Gran Chaco deforestation has been studied systematically since the mid-1980s (Hansen et al. 2013, Science 342:850). The Chaco — the second-largest ecoregion in South America after the Amazon — saw ~60% of native vegetation converted or degraded by 2015 (Kuemmerle et al. 2017, Annals AAG 107:1296–1310), with climate (precipitation patterns), agricultural commodity prices, and road accessibility serving as principal drivers (Baumann et al. 2018, RSE 211:182–204). Paraguayan Chaco specifically has been documented through Index-Based Decomposition analyses (merging road density + slope + population) (Henderson et al. 2021, Reg Environ Change 21:13).

### Section: Foundation models for Earth observation

Pre-trained geospatial foundation models have rapidly expanded since 2023. Prithvi-EO-2.0 (NASA + IBM), trained on 600 million Harmonized Landsat-Sentinel patches, has become the standard baseline for EO transfer learning (Jakubik et al. 2024, arXiv 2024.12708). AlphaEarth Foundations (Google DeepMind 2025) provides 64-dimensional satellite embeddings (2017–2024) freely available on Google Earth Engine — a direct complement for low-shot fine-tuning. Panopticon (Allen AI, CVPR EarthVision 2025 Best Paper) showed consistent generalization across 16 Earth observation tasks using self-supervised pretraining. The SkySense and SkySense++ family (SenseTime 2024) demonstrated multimodal EO pretraining. For real-time deforestation alerts, RADD (Radar Alerts for Detecting Deforestation, Wageningen U + FAO) and GLAD Alerts (University of Maryland) provide operational products. Global Pasture Watch (Zhang et al. 2024) provides 30 m annual pastoral land use 2000–2022.

### Section: Carbon credit integrity

Voluntary carbon markets, especially REDD+, have been subject to intense scrutiny. West, Börner, Sills & Kontoleon (2020, PNAS 117:24188–24194) showed Brazilian Amazon REDD+ credits were overstated by ~73%. The 2023 update (West et al., Science 379:eade3535) found 90%+ of audited REDD+ credits represent non-additional emission reductions. Hegenbart, Döbbeling, Bartling & Bento (2024, Nat Commun 15:2783) meta-analyzed 2346 projects (1 billion tonnes CO2e) and concluded that <16% of issued credits represented real emission reductions. Monga-bay (2024-04) documented the Brazilian Federal Police "Operation Greenwashing" raid on Amazon credit projects.

### Section: Deforestation carbon accounting

GEDI L4A gridded biomass (Duncanson et al. 2022, RSE 295:113516) provides 25 m aboveground biomass density globally, validated against Paraguay's national forest inventory (mean AGBD 65.55 t/ha, Bullock et al. 2023, Environ Res Lett 18:097002, doi:10.1088/1748-9326/acdf03). Below-ground carbon pools are typically 30-50% of aboveground (Mokany et al. 2006, Glob Change Biol 12:842–853). SOC across Gran Chaco sandy-loam soils: 32–50 tC/ha (0–30 cm) (Hengl et al. 2017, PLOS ONE 12:e0169748, doi:10.1371/journal.pone.0169748; Chen et al. 2022).

### Section: Driving variables (covariates for ML feature stack)

Following Balvanera et al. (2024, in "Sustainability and Biodiversity," Encyclopedia, doi:10.1016/b978-0-12-822562-2.00139-0) and the methodology of Hengl 2017 (SoilGrids), the Yvutu feature stack combines: distance to roads (OpenStreetMap), WorldPop population density, SRTM elevation + slope, WDPA protected-area overlap, prior loss (Hansen GFC), SoilGrids 2.0 texture/pH/SOC, CHIRPS precipitation, and VIIRS active fire detections. Haar wavelet decomposition of NDVI time series (Verbesselt et al. 2010, RSE 114:185–198).

### Section: Paraguay-specific drivers

Fehlenberg et al. (2017, Glob Environ Change 45:108–119) attribute soybeans as primary Chaco driver. Pendrill et al. (2019, Glob Environ Change 55:9–22) trace commodity-driven deforestation through Brazilian soy/beef trade. Pendrill et al. (2024, Nature Food 5:1–11) updated with 2020–2024 supply-chain exposure. Cepek & Haber (2008, Biol Conservation 141:601–614) describe cattle-ranching landscape structure. Volante et al. (2018, Remote Sensing 10:1778) describe the soybean-cattle frontier.

### Section: Chaco biogeography

Pennington, Prado & Pendry (2000) describe tropical dry forest biogeography and conservation. Prado (1993, Int J Ecol Environ Sci 19:17–29) defined Chaco vegetation as transitional between Cerrado and Monte biomes. Wood + biorefinery of quebracho species (*Schinopsis*, *Aspidosperma*) is documented by Tortorelli (2009, *Maderas y Bosques de la Argentina*) and Lopez (2009, *Etnobotánica de los Chaquenses*).
