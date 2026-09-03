[Skip to main content](https://www.nature.com/articles/s41597-024-04139-6#content)

Thank you for visiting nature.com. You are using a browser version with limited support for CSS. To obtain
the best experience, we recommend you use a more up to date browser (or turn off compatibility mode in
Internet Explorer). In the meantime, to ensure continued support, we are displaying the site without styles
and JavaScript.

Annual 30-m maps of global grassland class and extent (2000–2022) based on spatiotemporal Machine Learning


[Download PDF](https://www.nature.com/articles/s41597-024-04139-6.pdf)

[Download PDF](https://www.nature.com/articles/s41597-024-04139-6.pdf)

## Abstract

The paper describes the production and evaluation of global grassland extent mapped annually for 2000–2022 at 30 m spatial resolution. The dataset showing the spatiotemporal distribution of cultivated and natural/semi-natural grassland classes was produced by using GLAD Landsat ARD-2 image archive, accompanied by climatic, landform and proximity covariates, spatiotemporal machine learning (per-class Random Forest) and over 2.3 M reference samples (visually interpreted in Very High Resolution imagery). Custom probability thresholds (based on five-fold spatial cross-validation) were used to derive dominant class maps with balanced user’s and producer’s accuracy, resulting in f1 score of 0.64 and 0.75 for cultivated and natural/semi-natural grassland, respectively. The produced maps (about 4 TB in size) are available under an open data license as Cloud-Optimized GeoTIFFs and as Google Earth Engine assets. The suggested uses of data include (1) integration with other compatible land cover products and (2) tracking the intensity and drivers of conversion of land to cultivated grasslands and from natural / semi-natural grasslands into other land use systems.

### Similar content being viewed by others

![](https://media.springernature.com/w215h120/springer-static/image/art%3A10.1038%2Fs41597-024-03990-x/MediaObjects/41597_2024_3990_Fig1_HTML.png)

### [A 30-m annual grassland dataset from 1991 to 2020 for Inner Mongolia, China](https://www.nature.com/articles/s41597-024-03990-x?fromPaywallRec=false)

ArticleOpen access17 October 2024

![](https://media.springernature.com/w215h120/springer-static/image/art%3A10.1038%2Fs41597-023-02798-5/MediaObjects/41597_2023_2798_Fig1_HTML.png)

### [A global land cover training dataset from 1984 to 2020](https://www.nature.com/articles/s41597-023-02798-5?fromPaywallRec=false)

ArticleOpen access07 December 2023

![](https://media.springernature.com/w215h120/springer-static/image/art%3A10.1038%2Fs41597-024-03017-5/MediaObjects/41597_2024_3017_Fig1_HTML.png)

### [A 10-m annual grazing intensity dataset in 2015–2021 for the largest temperate meadow steppe in China](https://www.nature.com/articles/s41597-024-03017-5?fromPaywallRec=false)

ArticleOpen access10 February 2024

### Explore related subjects

Discover the latest articles and news in related subjects.

- [Environmental impact](https://www.nature.com/subjects/environmental-impact)
- [Research data](https://www.nature.com/subjects/research-data)

## Background & Summary

Grasslands are among the most vital global ecosystems, and, comprising open grasslands, grassy shrublands, and savannas, they cover approximately 40% of the Earth’s surface[1](https://www.nature.com/articles/s41597-024-04139-6#ref-CR1 "Bardgett, R. D. et al. Combatting global grassland degradation. Nature Reviews Earth & Environment 2, 720–735,                    https://doi.org/10.1038/s43017-021-00207-2                                     (2021)."), [2](https://www.nature.com/articles/s41597-024-04139-6#ref-CR2 "O’Mara, F. P. The role of grasslands in food security and climate change. Annals of Botany 110, 1263–1270,                    https://doi.org/10.1093/aob/mcs209                                     (2012)."). These ecosystems are critical for carbon sequestration, food production, biodiversity maintenance, and cultural heritage for people all over the world[1](https://www.nature.com/articles/s41597-024-04139-6#ref-CR1 "Bardgett, R. D. et al. Combatting global grassland degradation. Nature Reviews Earth & Environment 2, 720–735,                    https://doi.org/10.1038/s43017-021-00207-2                                     (2021)."). Klein _et al_.[3](https://www.nature.com/articles/s41597-024-04139-6#ref-CR3 "Klein Goldewijk, K., Beusen, A., Doelman, J. & Stehfest, E. Anthropogenic land use estimates for the Holocene–HYDE 3.2. Earth System Science Data 9, 927–953,                    https://doi.org/10.5194/essd-9-927-2017                                     (2017).") estimate that in 2000, there were 3,322 Mha of pastures in the world, both pastures and croplands experiencing rapid expansion. However, despite their ecological, cultural and socioeconomic importance, no comprehensive time series of high-resolution global maps specifically focused on grasslands yet exists. In addition, more detailed information on grassland management and use is also lacking, particularly at high resolutions and over extended periods of time. Geospatial monitoring for these areas is urgently needed to support conservation efforts, to underpin meaningful corporate supply chain no-conversion commitments, to reduce greenhouse gas emissions from the land sector[4](https://www.nature.com/articles/s41597-024-04139-6#ref-CR4 "Chang, J. et al. Climate warming from managed grasslands cancels the cooling effect of carbon sinks in sparsely grazed and natural grasslands. Nature Communications 12, 118,                    https://doi.org/10.1038/s41467-020-20406-7                                     (2021)."), [5](https://www.nature.com/articles/s41597-024-04139-6#ref-CR5 "Herrero, M. et al. Biomass use, production, feed efficiencies, and greenhouse gas emissions from global livestock systems. Proceedings of the National Academy of Sciences 110, 20888–20893,                    https://doi.org/10.1073/pnas.1308149110                                     (2013)."), to aid contribution to positive land use planning, allow finance for nature-based solutions and to contribute to restoring degraded landscapes[1](https://www.nature.com/articles/s41597-024-04139-6#ref-CR1 "Bardgett, R. D. et al. Combatting global grassland degradation. Nature Reviews Earth & Environment 2, 720–735,                    https://doi.org/10.1038/s43017-021-00207-2                                     (2021)."), [2](https://www.nature.com/articles/s41597-024-04139-6#ref-CR2 "O’Mara, F. P. The role of grasslands in food security and climate change. Annals of Botany 110, 1263–1270,                    https://doi.org/10.1093/aob/mcs209                                     (2012).").

Grasslands are one of the most challenging classes in land cover monitoring, driven by various natural, anthropogenic, and social aspects that vary between regions and cultures[6](https://www.nature.com/articles/s41597-024-04139-6#ref-CR6 "Phelps, L. N. & Kaplan, J. O. Land use for animal production in global change studies: Defining and characterizing a framework. Global change biology 23, 4457–4471,                    https://doi.org/10.1038/nature20584                                     (2017)."). General-purpose global land cover maps have traditionally mapped classes such as grasslands and shrublands with coarse spatial resolution, such as 500 m for NASA’s Global Land Cover Type[7](https://www.nature.com/articles/s41597-024-04139-6#ref-CR7 "Sulla-Menashe, D., Gray, J. M., Abercrombie, S. P. & Friedl, M. A. Hierarchical mapping of annual global land cover 2001 to present: The MODIS Collection 6 Land Cover product. Remote Sensing of Environment 222, 183–194,                    https://doi.org/10.1016/j.rse.2018.12.013                                     (2019).") and 300 m for ESA’s Climate Change Initiative Land Cover[8](https://www.nature.com/articles/s41597-024-04139-6#ref-CR8 "Plummer, S., Lecomte, P. & Doherty, M. The ESA Climate Change Initiative (CCI): A European contribution to the generation of the Global Climate Observing System. Remote Sensing of Environment 203, 2–8,                    https://doi.org/10.1016/j.rse.2017.07.014                                     (2017)."). Other products such as HYDE (10 km)[3](https://www.nature.com/articles/s41597-024-04139-6#ref-CR3 "Klein Goldewijk, K., Beusen, A., Doelman, J. & Stehfest, E. Anthropogenic land use estimates for the Holocene–HYDE 3.2. Earth System Science Data 9, 927–953,                    https://doi.org/10.5194/essd-9-927-2017                                     (2017)."), Earthstat (10 km)[9](https://www.nature.com/articles/s41597-024-04139-6#ref-CR9 "Ramankutty, N., Evan, A. T., Monfreda, C. & Foley, J. A. Farming the planet: 1. geographic distribution of global agricultural lands in the year 2000. Global biogeochemical cycles 22,                    https://doi.org/10.1029/2007GB002952                                     (2008)."), and HILDA+ (1 km)[10](https://www.nature.com/articles/s41597-024-04139-6#ref-CR10 "Winkler, K., Fuchs, R., Rounsevell, M. & Herold, M. Global land use changes are four times greater than previously estimated. Nature communications 12, 2501,                    https://doi.org/10.1038/s41467-021-22702-2                                     (2021).") further differentiate grassland management systems such as pastures/rangelands and unmanaged lands. However, their spatial resolution remains relatively coarse. In addition, the loose class definitions of existing grassland maps significantly hinder interoperability between classification systems. Recently, higher-resolution general-purpose land cover maps have become available by classifying Landsat (30 m) and Sentinel-2 (10 m) Earth Observation (EO) archives[11](https://www.nature.com/articles/s41597-024-04139-6#ref-CR11 "Brown, C. F. et al. Dynamic World, Near real-time global 10 m land use land cover mapping. Scientific Data 9, 251,                    https://doi.org/10.1038/s41597-022-01307-4                                     (2022)."), [12](https://www.nature.com/articles/s41597-024-04139-6#ref-CR12 "Friedl, M. A. et al. Medium Spatial Resolution Mapping of Global Land Cover and Land Cover Change Across Multiple Decades From Landsat. Frontiers in Remote Sensing 3, 894571,                    https://doi.org/10.3389/frsen.2022.894571                                     (2022)."), [13](https://www.nature.com/articles/s41597-024-04139-6#ref-CR13 "Potapov, P. et al. The global 2000-2020 land cover and land use change dataset derived from the landsat archive: first results. Frontiers in Remote Sensing 3, 856903,                    https://doi.org/10.3389/frsen.2022.856903                                     (2022)."), [14](https://www.nature.com/articles/s41597-024-04139-6#ref-CR14 "Zanaga, D. et al. ESA WorldCover 10 m 2020 v100                    https://doi.org/10.5281/zenodo.5571936                                     (2021)."), [15](https://www.nature.com/articles/s41597-024-04139-6#ref-CR15 "Zhang, X. et al. GLC_fcs30d: the first global 30 m land-cover dynamics monitoring product with a fine classification system for the period from 1985 to 2022 generated using dense-time-series Landsat imagery and the continuous change-detection method. Earth System Science Data 16, 1353–1381,                    https://doi.org/10.5194/essd-16-1353-2024                                     (2024)."), improving spatial resolution of grasslands, however have maintained the broad definition for grasslands without incorporating information on how they are actually intended to be used; thus limiting their usability for farmers, national agencies monitoring livestock, and agricultural extension experts. National medium- to high-resolution products[16](https://www.nature.com/articles/s41597-024-04139-6#ref-CR16 "Jones, M. O. et al. Innovation in rangeland monitoring: annual, 30 m, plant functional type percent cover maps for U.S. rangelands, 1984–2017. Ecosphere 9, e02430,                    https://doi.org/10.1002/ecs2.2430                                     (2018)."), [17](https://www.nature.com/articles/s41597-024-04139-6#ref-CR17 "Souza, C. M. et al. Reconstructing Three Decades of Land Use and Land Cover Changes in Brazilian Biomes with Landsat Archive and Earth Engine. Remote Sensing 12, 2735,                    https://doi.org/10.3390/rs12172735                                     (2020).") successfully add further differentiation to grasslands, but unfortunately cannot be used globally due to their limited spatial coverage.

In response to the need for detailed global-scale monitoring products targeting grasslands, the Land & Carbon Lab initiated the Global Pasture Watch (GPW) research consortium, gathering experts from the World Resources Institute (WRI), OpenGeoHub Foundation, the Image Processing and GIS Laboratory at the Federal University of Goiás (LAPIG/UFG), the International Institute for Applied Systems Analysis (IIASA), the German Center for Integrative Biodiversity Research (iDiv), Cornell University; and the Global Land Analysis and Discovery laboratory of the University of Maryland (GLAD). GPW aims to advance grassland monitoring by creating recurrent collections of global mapping products from the year 2000 onward at a suitable spatial resolution ( _i.e_. 30 m) to create fit-for-purpose monitoring solutions which are uniquely designed to be open to incorporating the significantly regional cultural knowledge surrounding grasslands.

In this paper, we present a novel data set with annual time series of global cultivated and natural/semi-natural grasslands mapped at 30 m spatial resolution covering the period from 2000 to 2022. We first explain all sampling and modeling steps and then report results of spatial cross-validation and comparison with existing datasets ( _e.g_. GLanCE[18](https://www.nature.com/articles/s41597-024-04139-6#ref-CR18 "Stanimirova, R. et al. A global land cover training dataset from 1984 to 2020. Scientific Data 10, 879 (2023)."), UMD GLAD GLCLUC[13](https://www.nature.com/articles/s41597-024-04139-6#ref-CR13 "Potapov, P. et al. The global 2000-2020 land cover and land use change dataset derived from the landsat archive: first results. Frontiers in Remote Sensing 3, 856903,                    https://doi.org/10.3389/frsen.2022.856903                                     (2022)."), GLC\_FCS30D[15](https://www.nature.com/articles/s41597-024-04139-6#ref-CR15 "Zhang, X. et al. GLC_fcs30d: the first global 30 m land-cover dynamics monitoring product with a fine classification system for the period from 1985 to 2022 generated using dense-time-series Landsat imagery and the continuous change-detection method. Earth System Science Data 16, 1353–1381,                    https://doi.org/10.5194/essd-16-1353-2024                                     (2024).")). We also visualize the annual values of the dominant class and the probability of grasslands, discuss potential applications, and openly report the limitations and future needs of the data we have produced. The data are available under open license (CC-BY) and will be regularly updated and improved with additional regional contexts, as well as new years added as the EO images become available.

## Methods

Our mapping framework, shown in Fig. [1](https://www.nature.com/articles/s41597-024-04139-6#Fig1), was based on multiple Earth Observation (EO) data such as GLAD Landsat ARD-2[19](https://www.nature.com/articles/s41597-024-04139-6#ref-CR19 "Potapov, P. et al. Landsat analysis ready data for global land cover and land cover change mapping. Remote Sensing 12, 426,                    https://doi.org/10.3390/rs12030426                                     (2020)."), MOD11A2[20](https://www.nature.com/articles/s41597-024-04139-6#ref-CR20 "Wan, Z., Hook, S. & Hulley, G. MODIS/Terra Land Surface Temperature/Emissivity 8-Day L3 Global 1 km SIN Grid V061,                    https://doi.org/10.5067/MODIS/MOD11A2.061                                     (2021)."), MCD19A2[21](https://www.nature.com/articles/s41597-024-04139-6#ref-CR21 "Lyapustin, A. & Wang, Y. MODIS/Terra + Aqua Land Aerosol Optical Depth Daily L2G Global 1 km SIN Grid V006,                    https://doi.org/10.5067/MODIS/MCD19A2.006                                     (2018)."), digital terrain model derivatives and distance maps of accessibility, roads, and water. To train the models, we used more than 2.3 M reference samples visually interpreted in Very High Resolution (VHR) images ( _i.e_. Google Maps and Bing Maps). Two independent spatiotemporal machine learning (ML) models[22](https://www.nature.com/articles/s41597-024-04139-6#ref-CR22 "Witjes, M. et al. A spatiotemporal ensemble machine learning framework for generating land use/land cover time-series maps for Europe (2000–2019) based on LUCAS, CORINE and GLAD Landsat. PeerJ 10, e13573,                    https://doi.org/10.7717/peerj.13573                                     (2022).") were used to predict each grassland class ( _i.e. cultivated grassland_ and _natural/semi-natural grassland_) over multiple years on a global scale. We produced predictions for all years from 2000 to 2022, resulting in a time series of global probability maps for cultivated and natural/semi-natural grassland at 30 m spatial resolution. Both probabilities were used to derive an integrated dominant class of grasslands, considering a custom global threshold per class. The exact methodological steps are described in the following sections.

**Fig. 1**

![Fig. 1](https://media.springernature.com/lw685/springer-static/image/art%3A10.1038%2Fs41597-024-04139-6/MediaObjects/41597_2024_4139_Fig1_HTML.png)

[Full size image](https://www.nature.com/articles/s41597-024-04139-6/figures/1)

The Global Pasture Watch grassland mapping framework encompasses general processing workflows, key inputs and outputs, and a feedback loop to improve future versions of the global maps.

### Reference sampling design

We use a Feature Space Coverage Sampling (FSCS[23](https://www.nature.com/articles/s41597-024-04139-6#ref-CR23 "Ma, T., Brus, D. J., Zhu, A.-X., Zhang, L. & Scholten, T. Comparison of conditioned Latin hypercube and feature space coverage sampling for predicting soil classes using simulation from soil maps. Geoderma 370, 114366,                    https://doi.org/10.1016/j.geoderma.2020.114366                                     (2020).")) to generate reference samples. This sampling design helps improve the representativeness of reference samples and is especially suitable for fitting multivariate predictive mapping models[23](https://www.nature.com/articles/s41597-024-04139-6#ref-CR23 "Ma, T., Brus, D. J., Zhu, A.-X., Zhang, L. & Scholten, T. Comparison of conditioned Latin hypercube and feature space coverage sampling for predicting soil classes using simulation from soil maps. Geoderma 370, 114366,                    https://doi.org/10.1016/j.geoderma.2020.114366                                     (2020)."). We used FSCS to generate 10,000 sample tiles ( _i.e_. 1 × 1 km) distributed across the World. We used 87 input layers for FSCS, shown in Table [1](https://www.nature.com/articles/s41597-024-04139-6#Tab1), restricted by a short vegetation mask that includes all pixels mapped as mosaic, shrubland, grassland, and sparse vegetation in at least one year from 1993 to 2021 ( _i.e_. 13 land cover classes described in Table [S1](https://www.nature.com/articles/s41597-024-04139-6#MOESM1)), according to the ESA/CCI global land cover time-series[24](https://www.nature.com/articles/s41597-024-04139-6#ref-CR24 "ESA Climante Change initiative. Global Land Cover time-series v2.1.1 (1992–2015).                    http://maps.elie.ucl.ac.be/CCI/viewer/download.php                                     (2021).").

**Table 1 Input layers for the Feature Space Coverage Sampling (FSCS).**

[Full size table](https://www.nature.com/articles/s41597-024-04139-6/tables/1)

In practice, the FSCS steps[25](https://www.nature.com/articles/s41597-024-04139-6#ref-CR25 "Parente, L., Hengl, T., Bonannello, C., Sloat, L. & Wheeler, I. Global Pasture Watch - Grassland sampling design derived by Feature Space Coverage Sampling (FSCV) at 1-km spatial resolution,                    https://doi.org/10.5281/zenodo.11275539                                     (2024).") include:

1. 1.
Principal Components Analysis (PCA) using all input layers,

2. 2.
Selection of the 10 first components (explaining 75% of variance),

3. 3.
K-Means with 10,000 clusters (targeted number of samples),

4. 4.
Calculation of Euclidean distance (in the principal component space) of all 1 km pixels to the centre of each cluster,

5. 5.
Selection of the pixel with the shortest distance for each cluster,

6. 6.
Conversion of the selected pixels to sample tiles (1 × 1 km).


### Reference labeling protocol

The selected FSCS tiles were visually interpreted by 16 visual interpretation (VI) analysts who classified the entire tile surface into three classes ( _i.e. cultivated grassland_, _natural/semi-natural grassland_ and _other land cover_) using Google Maps and Bing Maps imagery as reference. The analysts used a QGIS plugin ( [https://plugins.qgis.org/plugins/qgis-fgi-plugin](https://plugins.qgis.org/plugins/qgis-fgi-plugin)) specifically designed to optimize the classification process and evaluated 10,000 tile samples ( _i.e_. 1 × 1 km). For each tile, the plugin automatically created a finer grid ( _i.e_. 10 m grid cells), where each analyst manually assigned a single class and a reference date for a group of grid cells according to base imagery, as shown in Fig. [2](https://www.nature.com/articles/s41597-024-04139-6#Fig2). For Google Maps images, the analysts got the reference date from Google Earth software, and for Bing Maps, the plugin retrieved it through the Bing API. A total of 2,995 tiles were discarded due to a lack of suitable VHR images, predominately occurring in regions with latitudes higher than 60.5 degrees north.

**Fig. 2**

![Fig. 2](https://media.springernature.com/lw685/springer-static/image/art%3A10.1038%2Fs41597-024-04139-6/MediaObjects/41597_2024_4139_Fig2_HTML.png)

[Full size image](https://www.nature.com/articles/s41597-024-04139-6/figures/2)

Spatial distribution of tiles with available information (Single, 2 or more years) and examples of raw interpreted and converted to points for training the prediction models.

### Reference labeling criteria

In order to initially capture the inherent complexity of grasslands ecosystems, we developed a hierarchical ontology based on[26](https://www.nature.com/articles/s41597-024-04139-6#ref-CR26 "Allen, V. G. et al. An international terminology for grazing lands and grazing animals. Grass and forage science 66, 2,                    https://doi.org/10.1111/j.1365-2494.2010.00780.x                                     (2011).") (see Table [S2](https://www.nature.com/articles/s41597-024-04139-6#MOESM1)) and in line with attempting to separate natural/semi-natural grasslands without significant human directed management, from those under heavy management and/or entirely cultivated grasslands. We defined grassland as any land cover type which contains at least 30% of dry or wet low vegetation, dominated by grasses and forbs (less than 3 meters) and a:

- maximum of 50% tree canopy cover (greater than 5 meters),

- maximum of 70% of other woody vegetation (scrubs and open shrubland), and

- maximum of 50% active cropland cover in mosaic landscapes of cropland and other vegetation.

The reference labelling criteria were by necessity focused only on two end-member states ( _i.e. cultivated_ and _natural/semi-natural_) taking into consideration features that can be objectively identified in VHR imagery (see Fig. [S1](https://www.nature.com/articles/s41597-024-04139-6#MOESM1)). The reference labelling criteria, shown in Table [2](https://www.nature.com/articles/s41597-024-04139-6#Tab2), was used to train all analysts to visually distinguish our mapping classes according to the follow descriptions:

**Table 2 Visual interpretation criteria used in the reference labeling protocol.**

[Full size table](https://www.nature.com/articles/s41597-024-04139-6/tables/2)

- **Cultivated grassland** includes areas where grasses and other forage plants have been intentionally planted and managed, as well as areas of native grassland-type vegetation where they clearly exhibit active and ‘heavy’ management for specific human-directed uses, such as directed grazing of livestock. Many natural/semi-natural landscapes exist on a human intervention gradient, which is assumed by our criteria to initially be indicated by the presence of livestock-related infrastructure such as fencing and watering points. As interventions become more intensive through time, practices such as regular seeding, ploughing, mowing, fertilization, controlled grazing, and sometimes irrigation, aimed at enhancing productivity and maintaining the desired vegetation cover, start to become visible and/or implied by the visual character of the landscape. In general, the nonexclusive criteria applied to this class can be approximated from Table [2](https://www.nature.com/articles/s41597-024-04139-6#Tab2),

- **Natural/semi-natural grassland** includes relatively undisturbed native grasslands/short-height vegetation, such as steppes and tundra, as well as areas that have experienced varying degrees of human activity in the past. These grasslands may contain a mix of native and introduced species due to historical land use and natural processes. In general, they exhibit natural-looking patterns of varied vegetation and clearly ordered hydrological relationships throughout the landscape. This class also includes land that may have become degraded due to overuse or mismanagement but is not currently under intensive restoration or active management. Semi-natural areas may still have minimal active management and low-intensity practices such as periodic burning or episodic grazing under human direction to maintain the current grassy state or as part of arid or semi-arid transhumance practices. In general, the nonexclusive criteria applied to this class can be approximated from Table [2](https://www.nature.com/articles/s41597-024-04139-6#Tab2),

- **Other land cover** includes all other classes of land cover and land use, including, but not limited to, water bodies, rivers, snow, permanent ice, built-up areas, forest, annual crops ( _e.g_. soybean, maize), perennial crops ( _e.g_. coffee), bare ground, rocky outcrops, and wetlands. The definitions of the criteria may vary according to the types of LULC classes. Generally, we considered everything that does not fit into the other two classes as _Other land cover_.


Our reference labelling criteria were re-evaluated and refined through iterative discussions involving the GPW team, and may be actively fed by external analysts/users bringing additional cultural and regional expert knowledge, systematically contributing for improvements in our grassland reference samples.

### Reference sample pre-processing and filtering

All classified tiles with an assigned reference date were converted to point samples considering a 60 m of spatial support ( _i.e_. two Landsat pixels). For each point sample, we derive a class proportion based on the number of grid cells ( _i.e_. 10 m) for each class. For example, a point sample with 30 grid cells classified as _cultivated grassland_ had a class proportion equal to 0.83 ( _i.e_. 30 divided by 36). Since we implemented an independent binary classification model per grassland class, we kept only point samples with the 100% class proportion in our reference set, aiming for predictions based on distinct classes.

For point samples visually interpreted in two years ( _i.e_. different reference dates for Bing Maps and Google Maps), we implemented a data augmentation approach to increase the number of samples in consecutive years in our model. Every point sample with the same class according to Bing Maps and Google Maps, and less than 5 years of time difference, was replicated in all intermediate years. For example, a point sample of _cultivated grassland_ in 2010, according to Google Maps, and in 2014, according to Bing Maps, was replicated in 2011, 2012 and 2013. Assuming a minimum rotation period of 5 years for crops and grasslands[27](https://www.nature.com/articles/s41597-024-04139-6#ref-CR27 "Upcott, E. V., Henrys, P. A., Redhead, J. W., Jarvis, S. G. & Pywell, R. F. A new approach to characterising and predicting crop rotations using national-scale annual crop maps. Science of the Total Environment 860, 160471,                    https://doi.org/10.1016/j.scitotenv.2022.160471                                     (2023)."), this approach resulted in approximately 300,000 additional samples, mostly located in Europe, the U.S., India and South America.

The point samples were filtered considering the disagreement between our reference classes and three global land cover products ( _i.e_. UMD GLAD GLCLUC[13](https://www.nature.com/articles/s41597-024-04139-6#ref-CR13 "Potapov, P. et al. The global 2000-2020 land cover and land use change dataset derived from the landsat archive: first results. Frontiers in Remote Sensing 3, 856903,                    https://doi.org/10.3389/frsen.2022.856903                                     (2022)."), GLC\_FCS30D[15](https://www.nature.com/articles/s41597-024-04139-6#ref-CR15 "Zhang, X. et al. GLC_fcs30d: the first global 30 m land-cover dynamics monitoring product with a fine classification system for the period from 1985 to 2022 generated using dense-time-series Landsat imagery and the continuous change-detection method. Earth System Science Data 16, 1353–1381,                    https://doi.org/10.5194/essd-16-1353-2024                                     (2024).") and ESA WorldCover 2020[14](https://www.nature.com/articles/s41597-024-04139-6#ref-CR14 "Zanaga, D. et al. ESA WorldCover 10 m 2020 v100                    https://doi.org/10.5281/zenodo.5571936                                     (2021).")), from which we obtained the mapped classes for multiple years ( _i.e_. 2000, 2005, 2010, 2015 and 2020). All samples of _cultivated grassland_ and _natural/semi-natural grassland_ mapped as urban areas, forest, cropland, water, snow, or wetlands were removed by at least two global products in two years. Likewise, all samples of _other land cover_ predicted as grassland, short vegetation or herbaceous by at least two global products across two years were removed (for the filtering rules details, see Table [S3](https://www.nature.com/articles/s41597-024-04139-6#MOESM1)). This process removed 75,129 points ( _i.e_. about 3% of the total), improving the overall quality of our training data (specifically for augmented samples with crop-grassland rotation period less than 5 years) and resulting in 2,353,785 point samples distributed across the time series 2000–2022 (see Figs. [S2](https://www.nature.com/articles/s41597-024-04139-6#MOESM1) and [S3](https://www.nature.com/articles/s41597-024-04139-6#MOESM1)).

### GLAD Landsat ARD-2

The primary EO data input for our spatiotemporal modeling was the global Landsat Analysis Ready Data developed by the Global Land Analysis and Discovery Lab at the University of Maryland (GLAD ARD)0[19](https://www.nature.com/articles/s41597-024-04139-6#ref-CR19 "Potapov, P. et al. Landsat analysis ready data for global land cover and land cover change mapping. Remote Sensing 12, 426,                    https://doi.org/10.3390/rs12030426                                     (2020)."). GLAD ARD provides a 16-day time series of tiled Landsat normalized surface reflectance from 1997 onward. The entire Landsat 5, 7, 8, and 9 Collection 2 USGS data archive was used to produce the data set[28](https://www.nature.com/articles/s41597-024-04139-6#ref-CR28 "Crawford, C. J. et al. The 50-year landsat collection 2 archive. Science of Remote Sensing 8, 100103,                    https://doi.org/10.1016/j.srs.2023.100103                                     (2023)."). The Landsat data processing algorithm included per-pixel observation quality assessment, reflectance normalization, and anisotropy correction. The Moderate Resolution Imaging Spectroradiometer (MODIS) MOD44C surface reflectance product was used as a normalization target for a single-step reflectance bias and anisotropy correction. Each 16-day composite includes the best quality observation and contains eight spectral bands ( _i.e_. blue, green, red, Near-infrared–NIR, Short-wave infrared 1–SWIR1, Short-wave infrared 2–SWIR2, and thermal) and a quality assessment band that flags clouds, cloud shadows, snow/ice, haze, water, and clear-sky land. Since our reference samples are sparsely distributed over time, we decided to use GLAD ARD instead of the USGS Landsat collection to take advantage of the consistent pixel values across different Landsat systems over the years, improving the temporal generalization of our models and reducing the need of sampling all mapped periods.

### Landsat temporal aggregation and imputation

To reduce the impact of cloud cover and enable the incorporation of intra-annual seasonality in our features, we aggregated the Landsat ARD-2 time series (1997–2022) in bi-monthly temporal composites. For every GLAD tile ( _i.e_. 1 × 1 geographic degree), we executed the following steps[29](https://www.nature.com/articles/s41597-024-04139-6#ref-CR29 "Consoli, D. et al. A computational framework for processing time-series of earth observation data based on discrete convolution: global-scale historical landsat cloud-free aggregates at 30 m spatial resolution. PeerJ,                    https://doi.org/10.7717/peerj.18585                                     (In Press)."):

1. 1.
Removal of all pixels classified as cloud, cloud shadow, haze, cloud buffer, shadow buffer and shadow high likelihood according to quality assessment band (mask values: 3,4,7,8,9,10);

2. 2.
Conversion of pixel values to 8-bit by linear normalization, resulting in values ranging from 0 to 250;

3. 3.
Temporal aggregation of all clear-sky pixels for a 2-month period using a weighted average by cloud\_cover (estimated for each date and tile);

4. 4.
The remaining data gaps were imputed using time-series reconstruction, relying solely on clear-sky pixels acquired on previous dates ( _e.g_. gaps in Jan–Feb, 2002 composite considered clear-sky pixels of 1997, 1998, 1999, 2000 and 2001). The imputed values were derived using Seasonally Weighted Average Generalization (SWAG), which applied a vector of weights that prioritized pixel values from the same bi-month period and previous years over those from neighboring regions or different bi-month periods[29](https://www.nature.com/articles/s41597-024-04139-6#ref-CR29 "Consoli, D. et al. A computational framework for processing time-series of earth observation data based on discrete convolution: global-scale historical landsat cloud-free aggregates at 30 m spatial resolution. PeerJ,                    https://doi.org/10.7717/peerj.18585                                     (In Press).").


### Landsat-derived indices

In addition to the bi-monthly aggregates for the reflectance bands, we also incorporated several key vegetation and water indices as predictor variables for modeling purposes. These indices include the Bare Soil Index (BSI)[30](https://www.nature.com/articles/s41597-024-04139-6#ref-CR30 "Roy, P., Sharma, K. & Jain, A. Stratification of density in dry deciduous forest using satellite remote sensing digital data–an approach based on spectral indices. Journal of biosciences 21, 723–734 (1996)."), Enhanced Vegetation Index (EVI)[31](https://www.nature.com/articles/s41597-024-04139-6#ref-CR31 "Huete, A. et al. Overview of the radiometric and biophysical performance of the modis vegetation indices. Remote Sensing of Environment 83, 195–213 (2002)."), the Modified Normalized Burn Ratio (NBR2), also called Normalized Difference Tillage Index (NDTI)[32](https://www.nature.com/articles/s41597-024-04139-6#ref-CR32 "Van Deventer, A., Ward, A., Gowda, P. & Lyon, J. Using thematic mapper data to identify contrasting soil plains and tillage practices. Photogrammetric engineering and remote sensing 63, 87–93 (1997)."), the Normalized Difference Vegetation Index (NDVI)[33](https://www.nature.com/articles/s41597-024-04139-6#ref-CR33 "Tucker, C. J. Red and photographic infrared linear combinations for monitoring vegetation. Remote sensing of Environment 8, 127–150 (1979)."), the Normalized Difference Water Index (NDWI)[34](https://www.nature.com/articles/s41597-024-04139-6#ref-CR34 "Gao, B.-C. NDWI–A normalized difference water index for remote sensing of vegetation liquid water from space. Remote Sensing of Environment 58, 257–266 (1996).") and the near-infrared reflectance of vegetation (NIRv)[35](https://www.nature.com/articles/s41597-024-04139-6#ref-CR35 "Badgley, G., Field, C. B. & Berry, J. A. Canopy near-infrared reflectance and terrestrial photosynthesis. Science advances 3, e1602244 (2017)."). Each of these indices was derived from different linear combinations of the reflectance bands and provides unique information on vegetation health, moisture content, severity of burns, and overall ecological conditions. We also included a temporal aggregated index, Bare Soil Fraction (BSF)[36](https://www.nature.com/articles/s41597-024-04139-6#ref-CR36 "Castaldi, F., Chabrillat, S., Don, A. & van Wesemael, B. Soil organic carbon mapping using lucas topsoil database and sentinel-2 data: An approach to reduce soil moisture and crop residue effects. Remote Sensing 11, 2121 (2019)."), which is used to capture processes that require a longer temporal frame for sensible quantification: it is determined by the proportion of time the NDVI is <0.35 over the six bi-monthly aggregates[29](https://www.nature.com/articles/s41597-024-04139-6#ref-CR29 "Consoli, D. et al. A computational framework for processing time-series of earth observation data based on discrete convolution: global-scale historical landsat cloud-free aggregates at 30 m spatial resolution. PeerJ,                    https://doi.org/10.7717/peerj.18585                                     (In Press)."). In addition to spectral indices, we derived per-pixel Fraction of Absorbed Photosynthetically Active Radiation (FAPAR) using its correlation with NDVI[37](https://www.nature.com/articles/s41597-024-04139-6#ref-CR37 "Robinson, N. P. et al. Terrestrial primary production for the conterminous United States derived from Landsat 30 m and MODIS 250 m. Remote Sensing in Ecology and Conservation 4, 264–280 (2018)."). Table [S4](https://www.nature.com/articles/s41597-024-04139-6#MOESM1) summarizes the formulas for each Landsat-derived index utilized in our modeling.

### Atmospheric and land surface data

Land surface data was obtained from the MODIS Land Surface Temperature and Emissivity (LST&E) product, specifically MOD11A2[20](https://www.nature.com/articles/s41597-024-04139-6#ref-CR20 "Wan, Z., Hook, S. & Hulley, G. MODIS/Terra Land Surface Temperature/Emissivity 8-Day L3 Global 1 km SIN Grid V061,                    https://doi.org/10.5067/MODIS/MOD11A2.061                                     (2021)."). This product is available at a spatial resolution of 1 km and provides 8-day composite data that include both daytime and nighttime surface temperatures. To adapt these data for our analysis, we aggregated the 8-day composites into monthly averages, facilitating the calculation of long-term temperature trends for the period from 2000 to 2022. Specifically, we computed the median (50th quantile) and the standard deviation for both daytime and nighttime temperatures on a monthly basis. This processing yielded a total of 48 input features for our modelling. We also used MODIS water vapor data, specifically the atmospheric product MCD19A2, which captures column water vapour above the ground using near-IR bands. We aggregated the daily product into monthly composites, calculating the mean and standard deviation of positive, non-cloudy observations. The remaining no-data values were imputed using a gap-filling algorithm; for more detailed information on the methodology and data processing steps, refer to the Zenodo entry Parente _et al_.[38](https://www.nature.com/articles/s41597-024-04139-6#ref-CR38 "Parente, L., Simoes, R. & Hengl, T. Monthly aggregated Water Vapor MODIS MCD19A2 (1 km): Long-term data (2000–2022),                    https://doi.org/10.5281/zenodo.8192544                                     (2023)."), and Consoli _et al_.[29](https://www.nature.com/articles/s41597-024-04139-6#ref-CR29 "Consoli, D. et al. A computational framework for processing time-series of earth observation data based on discrete convolution: global-scale historical landsat cloud-free aggregates at 30 m spatial resolution. PeerJ,                    https://doi.org/10.7717/peerj.18585                                     (In Press).").

### Static raster datasets

The elevation data utilized in the modeling was obtained from the Ensemble Digital Terrain Model (EDTM) of the world at 30 m spatial resolution[39](https://www.nature.com/articles/s41597-024-04139-6#ref-CR39 "Ho, Y. F., Hengl, T. & Parente, L. Ensemble Digital Terrain Model (EDTM) of the world (1.1) (OpenGeoHub foundation, Doorwerth, NL, 2023)."). This DTM results from integrating multiple sources, including ALOS AW3D[40](https://www.nature.com/articles/s41597-024-04139-6#ref-CR40 "Tadono, T. et al. Generation of the 30 m-mesh global digital surface model by alos prism. The international archives of the photogrammetry, remote sensing and spatial information sciences 41, 157–162 (2016)."), GLO-30[41](https://www.nature.com/articles/s41597-024-04139-6#ref-CR41 "Strobl, P. The new copernicus digital elevation model. GSICS Quarterly 14, 17–18 (2020)."), MERIT DEM[42](https://www.nature.com/articles/s41597-024-04139-6#ref-CR42 "Yamazaki, D. et al. Merit dem: A new high-accuracy global digital elevation model and its merit to global hydrodynamic modeling. In AGU fall meeting abstracts, vol. 2017 (2017)."), and various national DTMs. To quantify the isolation from urban areas and correlate it with the livestock management practices, we used a suite of 10 global accessibility indicators calculated at 1 km resolution[43](https://www.nature.com/articles/s41597-024-04139-6#ref-CR43 "Nelson, A. et al. A suite of global accessibility indicators. Scientific data 6, 266 (2019)."); class 1 represents areas with travel times of less than 30 minutes to the nearest city of 50,000 or more inhabitants, indicating high accessibility, while class 9 refers to areas where travel time exceeds 10 hours to reach the nearest city of 50,000 or more inhabitants, indicating very low accessibility.

We also independently developed distance maps from permanent or seasonal inland water at 100 m resolution using a Landsat-derived product specifically developed for inland waters[44](https://www.nature.com/articles/s41597-024-04139-6#ref-CR44 "Pickens, A. H. et al. Mapping and sampling to characterize global inland water dynamics from 1999 to 2018 with full landsat time-series. Remote Sensing of Environment 243, 111792 (2020)."). Similarly, we produced maps of distances to areas classified by road density, ranging from low to high, utilizing OpenStreetMap (OSM) data. We also calculated the geometric minimum and maximum temperature as geometric transformations based on latitude, day of the year, and elevation[45](https://www.nature.com/articles/s41597-024-04139-6#ref-CR45 "Kilibarda, M. et al. Spatio-temporal interpolation of daily temperatures for global land areas at 1 km resolution. Journal of Geophysical Research: Atmospheres 119, 2294–2313 (2014)."). This calculation considered both the minimum and maximum temperature per month, resulting in 24 input features. These variables not only capture Earth’s geometry and temporal dynamics within a year but also enable the model to differentiate between locations that, despite having similar long-term or monthly temperature profiles, are distinct in their latitudinal positions or seasonal timing. This approach improves the model’s ability to discern and predict on the basis of subtle climatic variations influenced by geographical and temporal factors.

### Spatiotemporal model training

We modeled the grassland classes separately, training one model specialized in cultivated ( _i.e_. binary classifier of _cultivated grassland_ vs _other land cover_) and another model specialized in natural/semi-natural grassland ( _i.e_. binary classifier of _natural/semi-natural grassland_ vs _other land cover_). For each model, we ran a feature selection ( _i.e_. Recursive Feature Elimination–RFE[46](https://www.nature.com/articles/s41597-024-04139-6#ref-CR46 "Demarchi, L. et al. Recursive feature elimination and random forest classification of natura 2000 grasslands in lowland river valleys of poland based on airborne hyperspectral and lidar data fusion. Remote Sensing 12, 1842,                    https://doi.org/10.3390/rs12111842                                     (2020).")), a hyperparameter tuning ( _i.e_. Successive Halving[47](https://www.nature.com/articles/s41597-024-04139-6#ref-CR47 "Jamieson, K. & Talwalkar, A. Non-stochastic best arm identification and hyperparameter optimization. In Artificial intelligence and statistics, 240–248,                    https://doi.org/10.1109/SDS.2019.00-11                                     (PMLR, 2016).")) and a comparison between three ML algorithms ( _i.e_. Random Forest - RF[48](https://www.nature.com/articles/s41597-024-04139-6#ref-CR48 "Breiman, L. Random forests. Machine learning 45, 5–32,                    https://doi.org/10.1023/A:1010933404324                                     (2001)."), Gradient-boosted trees–GBT[49](https://www.nature.com/articles/s41597-024-04139-6#ref-CR49 "Friedman, J. H. Greedy function approximation: a gradient boosting machine. Annals of statistics 1189–1232,                    https://doi.org/10.1214/aos/1013203451                                     (2001).") and Artificial Neural Network–ANN[50](https://www.nature.com/articles/s41597-024-04139-6#ref-CR50 "Zou, J., Han, Y. & So, S.-S. Overview of artificial neural networks. Artificial neural networks: methods and applications 14–22,                    https://doi.org/10.1007/978-1-60327-101-1_2                                     (2009).")). The modeling strategy used all samples, with different reference years (see Fig. [S2](https://www.nature.com/articles/s41597-024-04139-6#MOESM1)), to train a single model able to generalize in time and produce predictions for all years (effective relying in the harmonized Landsat ARD-2 composites).

Before modeling, we overlaid our point samples with the temporal and static EO data. The Landsat pixel values were associated with each sample by spacetime overlay, matching the location ( _i.e_. geographical coordinates) and the time period ( _i.e_. year of reference) of each sample with 84 Landsat composites in a specific year ( _i.e_. seven reflectance bands and seven spectral indices for six bi-monthly aggregates). All samples were treated individually and were associated with the temporal features considering only the year of reference, established by our labeling process. For static layers ( _i.e_. long-term MOD11A2 land surface temperature, long-term MCD19A2 water vapor, geometric temperature, static DTM, and static distance maps of cities, roads, and water), the overlay considered only the sample locations, resulting in a total of 197 input features for feature selection. The overlaid samples were then split into training and calibration, where 10% of samples from each visually interpreted tile ( _i.e_. 11 km) were randomly selected to compose the calibration set, resulting in 2,122,357 and 231,428 samples for training and calibration, respectively. The calibration set was used to run the Recursive Feature Elimination and then Successive Halving, thus establishing the best features and hyperparameters to compare the ML algorithms.

Our Recursive Feature Elimination[46](https://www.nature.com/articles/s41597-024-04139-6#ref-CR46 "Demarchi, L. et al. Recursive feature elimination and random forest classification of natura 2000 grasslands in lowland river valleys of poland based on airborne hyperspectral and lidar data fusion. Remote Sensing 12, 1842,                    https://doi.org/10.3390/rs12111842                                     (2020).") considered a standard Random Forest model with 60 trees and default hyper-parameters (fitted using scikit-learn[51](https://www.nature.com/articles/s41597-024-04139-6#ref-CR51 "Shaharum, N. et al. Image classification for mapping oil palm distribution via support vector machine using scikit-learn module. The International Archives of the Photogrammetry, Remote Sensing and Spatial Information Sciences 42, 133–137,                    https://doi.org/10.5194/isprs-archives-XLII-4-W9-133-2018                                     (2018).")), targeting 75 features as final selection ( _i.e_. about 38% of the total number of features) and removing the four least important features per iteration (according to gini importance). The best 75 features of each model, shown in Table [S5](https://www.nature.com/articles/s41597-024-04139-6#MOESM1), were then used to run Successive Halving, which considered the log\_loss metric[22](https://www.nature.com/articles/s41597-024-04139-6#ref-CR22 "Witjes, M. et al. A spatiotemporal ensemble machine learning framework for generating land use/land cover time-series maps for Europe (2000–2019) based on LUCAS, CORINE and GLAD Landsat. PeerJ 10, e13573,                    https://doi.org/10.7717/peerj.13573                                     (2022).") and five-fold spatial blocking cross-validation (based on visually interpreted tiles– _i.e_. 11 km) for assessing iteratively different combinations of hyper-parameters candidates bounded by a customized search space. Our Successive Halving started with 500 samples, selecting the best candidates ( _i.e_. dropping half of the less accurate candidates) and doubling the number of samples per iteration until reaching the full set of calibration samples. After the last iteration, the hyper-parameters with best log\_loss ( _i.e_. lowest value), shown in Table [S6](https://www.nature.com/articles/s41597-024-04139-6#MOESM1), were selected for each ML algorithm.

The comparison used the training set and the five-fold spatial blocking cross-validation to estimate accuracy metrics adequate for probability output ( _i.e_. R2logloss[52](https://www.nature.com/articles/s41597-024-04139-6#ref-CR52 "Bonannella, C. et al. Forest tree species distribution for europe 2000–2020: mapping potential and realized distributions using spatiotemporal machine learning. PeerJ 10, e13728,                    https://doi.org/10.7717/peerj.13728                                     (2022).") and precision-recall curves[53](https://www.nature.com/articles/s41597-024-04139-6#ref-CR53 "Ebrahimy, H., Mirbagheri, B., Matkan, A. A. & Azadbakht, M. Effectiveness of the integration of data balancing techniques and tree-based ensemble machine learning algorithms for spatially-explicit land cover accuracy prediction. Remote Sensing Applications: Society and Environment 27, 100785,                    https://doi.org/10.1016/j.rsase.2022.100785                                     (2022).")) for Random Forest, Gradient-boosted trees and Artificial Neural Network. For each algorithm, five ML models were trained using 80% of samples ( _i.e_. one fold) and 20% for validation in each iteration, resulting in an out-of-the-fold prediction for all samples. The blocking strategy kept all samples from the same tile ( _i.e_. 11 km) either in training or validation set, reducing the spatial correlation between boFth sets and allowing for a more strict evaluation of the error estimate[54](https://www.nature.com/articles/s41597-024-04139-6#ref-CR54 "Roberts, D. R. et al. Cross-validation strategies for data with temporal, spatial, hierarchical, or phylogenetic structure. Ecography 40, 913–929,                    https://doi.org/10.1111/ecog.0288                                     (2017)."). This analysis excluded the interpolated point samples. The best model according to R2logloss ( _i.e_. highest value) was used to train two global models considering all points samples ( _i.e_. 2,353,785 samples) and 102 features ( _i.e_. union of the best-selected features–see Table [S5](https://www.nature.com/articles/s41597-024-04139-6#MOESM1)). The global models were then used to predict (worldwide) _cultivated_ and _natural/semi-natural grassland_ for all years of the time series.

### Spatiotemporal prediction

Global predictions were produced per GLAD tile ( _i.e_. 11 geographic degree) and on a yearly basis from 2000 to 2022, resulting in annual per-pixel probabilities for each class of grassland at 30 m spatial resolution. In an effort to speed up this process, we did not predict pixels mapped as deserts, stable tree cover, salt pan wetlands, stable snow and ocean water in all years between 2000–2020, according to the UMD GLAD GLCLUC product (for a complete list of land cover classes see Table [S7](https://www.nature.com/articles/s41597-024-04139-6#MOESM1)). Furthermore, we also excluded areas mapped as buildings by the World Settlement Footprint in 2019, and by the evolution product, which covers every 5 years between 1990 and 2015[55](https://www.nature.com/articles/s41597-024-04139-6#ref-CR55 "Marconcini, M. et al. Outlining where humans live, the world settlement footprint 2015. Scientific Data 7, 242,                    https://doi.org/10.1038/s41597-020-00580-5                                     (2020).").

Our Random Forest models were compiled to a native C binary using TL2cgen[56](https://www.nature.com/articles/s41597-024-04139-6#ref-CR56 "TL2cgen: model compiler for decision trees.                    https://tl2cgen.readthedocs.io/en/latest/                                    . Accessed: 2024-03-11."), reducing the prediction time by factor 3. After running the predictions, the time-series of probabilities were smoothed out by a spatio-temporal filter, which considered a three-dimensional Savitzky-golay–SG (polynomial order three and squared window with five pixels) to reduce the inter-annual variability in the prediction outputs. Savitzky-golay is a robust filter capable of significantly reducing local noise/spikes without changing the main trend of the time-series[57](https://www.nature.com/articles/s41597-024-04139-6#ref-CR57 "Shekhar, C. On simplified application of multidimensional savitzky-golay filters and differentiators. In AIP Conference Proceedings, vol. 1705,                    https://doi.org/10.1063/1.4940262                                     (AIP Publishing, 2016)."). Additionally, we produced a Mean Absolute Difference (MADi) layer for each class of grassland, where we estimated the absolute difference between the predicted and the smothered probabilities and aggregated all years by average.

All these processing steps ran on a High-Performance Computing (HPC) infrastructure and were distributed among the processing nodes using SLURM[58](https://www.nature.com/articles/s41597-024-04139-6#ref-CR58 "Yoo, A. B., Jette, M. A. & Grondona, M. Slurm: Simple linux utility for resource management. In Workshop on job scheduling strategies for parallel processing, 44–60 (Springer, 2003).") and Docker containers[59](https://www.nature.com/articles/s41597-024-04139-6#ref-CR59 "Boettiger, C. An introduction to docker for reproducible research. ACM SIGOPS Operating Systems Review 49, 71–79,                    https://doi.org/10.1145/2723872.2723882                                     (2015)."). Approximately 120,960 CPU hours and 7.2 terabytes of RAM were used to produce the final predictions. All predicted tiles were then used to create Cloud-Optimized GeoTIFF (COG) mosaics and made publicly available in Google Earth Engine and the SpatioTemporal Asset Catalog (STAC).

### Dominant grassland production

The cultivated and natural/semi-natural grassland probabilities (smoothed with Savitzky-golay) were used to derive annual dominant grassland maps based in a customized probability threshold. For each class, we calculate the precision-recall curves[53](https://www.nature.com/articles/s41597-024-04139-6#ref-CR53 "Ebrahimy, H., Mirbagheri, B., Matkan, A. A. & Azadbakht, M. Effectiveness of the integration of data balancing techniques and tree-based ensemble machine learning algorithms for spatially-explicit land cover accuracy prediction. Remote Sensing Applications: Society and Environment 27, 100785,                    https://doi.org/10.1016/j.rsase.2022.100785                                     (2022).") through five-fold spatial blocking cross-validation and using 2,1 million points samples. The curves were then used to find which probability threshold provides balanced/equal recall ( _i.e_. producer’s accuracy) and precision ( _i.e_. user’s accuracy). All probabilities greater or equal to the selected thresholds were converted to dominant grassland classes. For pixels classified simultaneously as dominant in our two grassland classes, we kept only the class with the higher f1-score according to our cross-validation strategy ( _i.e_. natural/semi-natural grassland).

## Data Records

The global grassland maps described in this paper are available from 2000–2022 in COG (Cloud Optimized GeoTIFF) format under the Creative Commons license CC-BY, archived in Zenodo ( [https://doi.org/10.5281/zenodo.13890401](https://doi.org/10.5281/zenodo.13890401) [60](https://www.nature.com/articles/s41597-024-04139-6#ref-CR60 "Parente, L. et al. Global Pasture Watch - Annual grassland class and extent maps at 30-m spatial resolution (2000–2022),                    https://doi.org/10.5281/zenodo.13890401                                     (2024).") \- Fig. [3](https://www.nature.com/articles/s41597-024-04139-6#Fig3)), and publicly accessible in OpenLandMap SpatioTemporal Asset Catalog (STAC - [https://stac.openlandmap.org/gpw\_ggc-30m/collection.json](https://stac.openlandmap.org/gpw_ggc-30m/collection.json)). The COG format supports HTTP range requests, enabling seamless lazy loading access by GIS solutions ( _e.g_. Quantum GIS, MapServer, GeoServer, etc) and programming environments ( _e.g_. JupyterLab, RStudio, etc).

**Fig. 3**

![Fig. 3](https://media.springernature.com/lw685/springer-static/image/art%3A10.1038%2Fs41597-024-04139-6/MediaObjects/41597_2024_4139_Fig3_HTML.png)

[Full size image](https://www.nature.com/articles/s41597-024-04139-6/figures/3)

Global grassland maps for 2000 and 2022 including dominant class and probabilities for cultivated and natural/semi-natural grassland.

A total of 69 global mosaics ( _i.e_. 23 years for each time series) is available in the WGS84 Coordinate Systems ( _i.e_. EPSG:4326) and pixel size equal to 0.00025 degrees. The grassland probability values range from 0–100, and the class values used by the dominant maps are zero (0) for _other land cover_, one (1) for to _cultivated grassland_ and two (2) for _natural/semi-natural grassland_. All raster files are in unsigned 8-bit integer format and use 255 as no-data value (pixels which were ignored in by predictions according to the UMD GLAD GLCLUC product; see Table [S7](https://www.nature.com/articles/s41597-024-04139-6#MOESM1)), following a naming convention that organizes the most important data properties in nine fields:

01. 1.
    Project name: Global Pasture Watch (gpw)

02. 2.
    Class name: _cultivated grassland_ (cultiv.grassland), _natural/semi-natural grassland_ (nat.semi.grassland) and dominant grassland (grassland)

03. 3.
    Procedure combination: Random Forest (rf), Savitzky-golay (savgol), balanced threshold (bthr) and mean absolute difference (madi).

04. 4.
    Variable type: probability (p) and class (c)

05. 5.
    Spatial resolution: 30 m

06. 6.
    Begin of time reference: date of first Landsat composite used by the modeling (20220101)

07. 7.
    End of time reference: date of last Landsat composite used by the modeling (20221231)

08. 8.
    Spatial extent: global (go)

09. 9.
    Coordinate system: World Geodetic System 1984, used in GPS (epsg.4326)

10. 10.
    Version: v1


## Technical Validation

### Spatial cross-validation and feature importance

Our comparison results, shown in Table [3](https://www.nature.com/articles/s41597-024-04139-6#Tab3), revealed very similar R2logloss values for tree-based algorithms ( _i.e_. Random Forest and Gradient-boosted trees), while Artificial Neural Network presented the lowest values for both classes of grasslands. We used the precision-recall curves to define probability thresholds that can balance precision and recall ( _i.e_. similar values) and maximize the F1 score[53](https://www.nature.com/articles/s41597-024-04139-6#ref-CR53 "Ebrahimy, H., Mirbagheri, B., Matkan, A. A. & Azadbakht, M. Effectiveness of the integration of data balancing techniques and tree-based ensemble machine learning algorithms for spatially-explicit land cover accuracy prediction. Remote Sensing Applications: Society and Environment 27, 100785,                    https://doi.org/10.1016/j.rsase.2022.100785                                     (2022)."). Artificial Neural Network had the highest probability threshold, while Gradient-boosted trees had the lowest one. These thresholds were used to convert probabilities in dominant classes ( _e.g_. all samples with predicted probabilities greater than or equal to 0.32 were converted to _“Cultivated grassland”_ class), which were then used to estimate the F1 score. Gradient-boosted trees presented F1 scores slightly higher than Random Forest, and Artificial Neural Network presented the lowest scores for both grass classes. As there were no significant differences in accuracy between Random Forest and Gradient-boosted trees, we decided to use Random Forest to train the final global models due to the speed-up possibility offered by TL2cgen[56](https://www.nature.com/articles/s41597-024-04139-6#ref-CR56 "TL2cgen: model compiler for decision trees.                    https://tl2cgen.readthedocs.io/en/latest/                                    . Accessed: 2024-03-11.").

**Table 3 Comparison of ML algorithms derived by five-fold spatial blocking cross-validation using 2,122,357 points samples.**

[Full size table](https://www.nature.com/articles/s41597-024-04139-6/tables/3)

The accuracy matrix, derived using the probability thresholds shown in Table [3](https://www.nature.com/articles/s41597-024-04139-6#Tab3), presented higher accuracies for _natural/semi-natural grassland_ than _cultivated grassland_ (see Table [4](https://www.nature.com/articles/s41597-024-04139-6#Tab4)). The class _other land cover_ had values greater than 0.90 in all accuracy metrics. In addition to the massive number of points samples and robustness of the spatial blocking cross-validation[54](https://www.nature.com/articles/s41597-024-04139-6#ref-CR54 "Roberts, D. R. et al. Cross-validation strategies for data with temporal, spatial, hierarchical, or phylogenetic structure. Ecography 40, 913–929,                    https://doi.org/10.1111/ecog.0288                                     (2017)."), [61](https://www.nature.com/articles/s41597-024-04139-6#ref-CR61 "King, R. D., Orhobor, O. I. & Taylor, C. C. Cross-validation is safe to use. Nature Machine Intelligence 3, 276–276,                    https://doi.org/10.1038/s42256-021-00332-z                                     (2021).") and sampling design ( _i.e_. FSCS), the current accuracy was based on 7,005 tiles where we had VHR imagery available for the labeling process. Tiles without reference labels might have very specific grassland dynamics that have not been captured by our models and accuracy assessment. Furthermore, our reference data are quite sparse in time, with 40% of tiles having a single year available for visual interpretation, and most of the samples obtained in 2009–2014 and 2019–2022 for Bing and Google Maps, respectively (see Fig. [S3](https://www.nature.com/articles/s41597-024-04139-6#MOESM1)). This temporal sparsity makes inferences based on sample-based annual areas currently not possible for our grassland classes, even that considering all years, the proportion of _cultivated grassland_ and _natural/semi-natural grassland_ together reaches 32% (see Fig. [S2](https://www.nature.com/articles/s41597-024-04139-6#MOESM1)).

**Table 4 Accuracy matrix for the final Random Forest models estimated by five-fold spatial blocking cross-validation using 2,122,357 points samples.**

[Full size table](https://www.nature.com/articles/s41597-024-04139-6/tables/4)

To overcome these issues, work is ongoing to independently validate output layers (led by IIASA) based on a new set of reference samples and a different group of analysts, following the good practices of evaluation for LULC products[62](https://www.nature.com/articles/s41597-024-04139-6#ref-CR62 "Stehman, S. V. & Foody, G. M. Key issues in rigorous accuracy assessment of land cover products. Remote Sensing of Environment 231, 111199,                    https://doi.org/10.1016/j.rse.2019.05.018                                     (2019).") and able to support a proper assessment of grassland land cover changes/dynamics. Visual interpretation has been conducted on the Geo-Wiki platform considering the current class definitions/criteria and multiple satellite imagery to address the temporal sparsity ( _e.g_. Google Maps, Bing Maps, Landsat and Sentinel)[63](https://www.nature.com/articles/s41597-024-04139-6#ref-CR63 "Fritz, S. et al. Geo-wiki: An online platform for improving global land cover. Environmental Modelling & Software 31, 110–123,                    https://doi.org/10.1016/j.envsoft.2011.11.015                                     (2012)."). This validation helps assess and measure concrete improvements in the next versions of grassland maps since we can reinterpret our current training samples based on feedback and local knowledge without changing the independent validation samples. Additionally, we will evaluate the quality of our cross-validation assessment, measuring how well our ML models will perform on a new set of reference samples.

Feature importance of our Random Forest models shows that SWIR1 is the most important Landsat band for identifying _cultivated grassland_, with the highest importance for all bi-monthly periods (see Fig. [4a](https://www.nature.com/articles/s41597-024-04139-6#Fig4)). The green and red bands, together with NDTI (Normalized Difference tillage Index), are also important Landsat features and probably contribute to the distinction of _cultivated grassland_ and croplands. The long-term MODIS water vapor (December and February) and the MODIS daytime temperature (October and September) are the only coarser resolution layers ( _i.e_. 1 km) among the top-15 most important features. For _natural/semi-natural grassland_, eight of the 15 features are coarser resolution layers, including several city accessibility maps[43](https://www.nature.com/articles/s41597-024-04139-6#ref-CR43 "Nelson, A. et al. A suite of global accessibility indicators. Scientific data 6, 266 (2019)."), which are probably contributing to the identification of remote grassland areas ( _e.g_. nature reserves, semi-arid grasslands, tundra ecosystems). Nevertheless, red is the most important Landsat band for distinguishing this class of grasslands, specifically the May to December ( _i.e_. four bi-monthly periods–see Fig. [4b](https://www.nature.com/articles/s41597-024-04139-6#Fig4)) seem to help the predictive mapping especially.

**Fig. 4**

![Fig. 4](https://media.springernature.com/lw685/springer-static/image/art%3A10.1038%2Fs41597-024-04139-6/MediaObjects/41597_2024_4139_Fig4_HTML.png)

[Full size image](https://www.nature.com/articles/s41597-024-04139-6/figures/4)

Top-15 most important features according to our global Random Forest (RF) models for: ( **a**) cultivated grassland, and ( **b**) natural/semi-natural grassland.

### Independent validation with existing samples

To comprehensively compare our global grassland maps with existing LULC mapping initiatives, we harmonized reference samples from 7 datasets, shown in Table [5](https://www.nature.com/articles/s41597-024-04139-6#Tab5). This process involved translating the original LULC classifications of these datasets into our three classes ( _i.e. grassland_, _natural/semi-natural grassland_ and _other land cover_), leveraging the original class definitions and expert knowledge to map LULC across different datasets accurately. This involved meticulously comparing the definitions of LULC classes within each dataset with the classification scheme described above. The crosswalk/class harmonization tables were implemented using Python computational notebooks and are available in Zenodo[64](https://www.nature.com/articles/s41597-024-04139-6#ref-CR64 "de Oliveira, B. S., Teles, N. M., Mesquita, V. V., Parente, L. L. & Ferreira, L. G. Integrated Approach to Global Land Use and Land Cover Reference Data Harmonization,                    https://doi.org/10.5281/zenodo.11246630                                     (2024)."). As a result, we obtained 66,991,467 harmonized individual samples (unique points in geographical space and time - [https://doi.org/10.5281/zenodo.13951976](https://doi.org/10.5281/zenodo.13951976) [64](https://www.nature.com/articles/s41597-024-04139-6#ref-CR64 "de Oliveira, B. S., Teles, N. M., Mesquita, V. V., Parente, L. L. & Ferreira, L. G. Integrated Approach to Global Land Use and Land Cover Reference Data Harmonization,                    https://doi.org/10.5281/zenodo.11246630                                     (2024).")).

**Table 5 Datasets of pre-existing reference samples harmonized to our classification taxonomy.**

[Full size table](https://www.nature.com/articles/s41597-024-04139-6/tables/5)

The harmonized samples were used in to conduct an independent validation of the dominant grassland-class maps (cultivated and natural/semi-natural combined - Fig. [3](https://www.nature.com/articles/s41597-024-04139-6#Fig3)). This analyses revealed higher precision ( _i.e_. user’s accuracy) than recall (producer’s accuracy) in all datasets (see Fig. [5](https://www.nature.com/articles/s41597-024-04139-6#Fig5)), indicating, in general, that our grassland predictions are more conservative and might not include regions defined as grassland/shrubs by multiple LULC mapping initiatives. Globally, our dominant class maps have precision values higher than 0.7 and F1 scores of 0.79, 0.65 and 0.63 according to GLanCE, CGLS-LC and WorldCereal, respectively.

**Fig. 5**

![Fig. 5](https://media.springernature.com/lw685/springer-static/image/art%3A10.1038%2Fs41597-024-04139-6/MediaObjects/41597_2024_4139_Fig5_HTML.png)

[Full size image](https://www.nature.com/articles/s41597-024-04139-6/figures/5)

Independent validation of grassland class ( _i.e_. cultivated and natural/semi-natural grassland combined) based on harmonized existing reference datasets and and sorted ascending by F1 score.

Specifically for GLanCE, the accuracy metrics were derived per continent, enabling cross-checking with continental and national datasets. F1 score values greater than 0.8 were found for South America (GLanCE) and Brazil (MapBiomas), a key agricultural frontier with the historical expansion of cultivated grassland[65](https://www.nature.com/articles/s41597-024-04139-6#ref-CR65 "Zalles, V. et al. Rapid expansion of human impact on natural land in south america since 1985. Science Advances 7, eabg1620,                    https://doi.org/10.1126/sciadv.abg1620                                     (2021)."). Higher accuracy values were found for the U.S. (LCMAP CONUS) compared to North America, indicating more accurate predictions for the country in relation to the rest of the continent. Oceania had similar accuracy values compared to North America, which may be explained by similar patterns in their land cover footprint[66](https://www.nature.com/articles/s41597-024-04139-6#ref-CR66 "Creutzig, F. et al. Assessing human and environmental pressures of global land-use change 2000–2010. Global Sustainability 2, e1 (2019)."). Asia presented the most balanced precision and recall among all continents, remarkably similar to our cross-validation values (3). In Europe, the F1 score was 0.64, 0.63 and 0.50 according to GLanCE, EuroCrops and LUCAS, respectively, indicating less accurate predictions compared to other continents, with systematic omission error (recall between 0.35 and 0.53). The low accuracy values obtained with LUCAS might indicate significant mismatches between grassland classification taxonomies[67](https://www.nature.com/articles/s41597-024-04139-6#ref-CR67 "d’Andrimont, R. et al. Harmonised lucas in-situ land cover and use database for field surveys from 2006 to 2018 in the european union. Scientific data 7, 352,                    https://doi.org/10.1038/s41597-019-0340-y                                     (2020)."). The lowest accuracy values were obtained in Africa, and it is probably related to the widespread disagreement among existing LULC datasets in the continent[68](https://www.nature.com/articles/s41597-024-04139-6#ref-CR68 "Pérez-Hoyos, A., Udas, A. & Rembold, F. Integrating multiple land cover maps through a multi-criteria analysis to improve agricultural monitoring in africa. International Journal of Applied Earth Observation and Geoinformation 88, 102064,                    https://doi.org/10.1016/j.jag.2020.102064                                     (2020).").

Considering the wide temporal coverage of GLanCE, we used it to conduct an annual independent validation of our dominant class maps. Since its temporal distribution is not regular across the time series (with several samples having class labels for one to three years), this analyze considered only samples with 10 or more years labeled between 2000–2018. We notice a minor increase in precision ( _i.e_. 0.9394 and 0.931 on average for smoothed and non-smoothed probabilities, respectively) followed by a minor decrease in recall ( _i.e_. 0.7410 and 0.7449 in average for smoothed and non-smoothed probabilities, respectively) due to SG (Fig. [6](https://www.nature.com/articles/s41597-024-04139-6#Fig6)). Combined with a visual assessment of probabilities, this confirms that SG increases the spatiotemporal consistency of our predictions without significantly changing their accuracy. The accuracy metrics remain stable throughout the years and show higher precision ( _i.e_. user’s accuracy) than recall (producer’s accuracy) across all years, revealing a systematic omission error ( _i.e_. false negatives), rather than a commission error ( _i.e_. false positives). This can be partially attributed to the establishment of balanced probability thresholds independently for each class, which does not ensure comparable precision and recall values for the combined classes. Compared to the naive threshold, on the other hand, ( _i.e_. 0.5) the balanced thresholds increased the F1 score by 0.1241 and recall by 0.1892, on average, while decreased the precision by 0.0369, on average (see Fig. [S4](https://www.nature.com/articles/s41597-024-04139-6#MOESM1)).

**Fig. 6**

![Fig. 6](https://media.springernature.com/lw685/springer-static/image/art%3A10.1038%2Fs41597-024-04139-6/MediaObjects/41597_2024_4139_Fig6_HTML.png)

[Full size image](https://www.nature.com/articles/s41597-024-04139-6/figures/6)

Independent validation of grassland class ( _i.e_. cultivated and natural/semi-natural grassland combined) based on GLANCE training dataset. The GLANCE classes grassland (12), shrub (10) and moss/lichen (13) were reclassified to grassland for matching with our legend. All metrics were derived for smoothed probabilities ( _i.e_. Savitzky-golay - SG) and non-smoothed ( _i.e_. No-SG) considering balanced thresholds of 0.32 and 0.42 for cultivated and natural/semi-natural grassland, respectively.

Aiming to evaluate the temporal consistency of our grassland maps, we estimated the stability index for precision and recall[69](https://www.nature.com/articles/s41597-024-04139-6#ref-CR69 "Tsendbazar, N. et al. Towards operational validation of annual global land cover maps. Remote Sensing of Environment 266, 112686,                    https://doi.org/10.1016/j.rse.2021.112686                                     (2021).") from 2000 to 2018 using GLanCE, MapBiomas and LCMAP CONUS (see Fig. [7](https://www.nature.com/articles/s41597-024-04139-6#Fig7)). Stability index is basically the absolute percentage difference of a specific accuracy metric between two neighborhood years, where values close to zero indicate more stable predictions. At global scale (GLANCE), the averaged stability index is 0.15 and 0.21 for precision and recall, respectively. In U.S. (LCMAP CONUS) and Brazil (MapBiomas) the stability index is higher, with averaged values of 0.41 and 0.53 for precision, and 0.77 and 1.35 for recall, respectively for each country. Considering that the grasslands are quite dynamic in the two countries, our predictions are probably not matching in time with the reference samples, and some of the grassland conversions are captured a few years later or completely missed in the time-series.

**Fig. 7**

![Fig. 7](https://media.springernature.com/lw685/springer-static/image/art%3A10.1038%2Fs41597-024-04139-6/MediaObjects/41597_2024_4139_Fig7_HTML.png)

[Full size image](https://www.nature.com/articles/s41597-024-04139-6/figures/7)

Stability index[69](https://www.nature.com/articles/s41597-024-04139-6#ref-CR69 "Tsendbazar, N. et al. Towards operational validation of annual global land cover maps. Remote Sensing of Environment 266, 112686,                    https://doi.org/10.1016/j.rse.2021.112686                                     (2021).") estimated for grassland ( _i.e_. cultivated and natural/semi-natural grassland combined) based on GLANCE ( **a**), LCMAP CONUS ( **b**) and MapBiomas ( **c**), presenting the absolute percentage difference in precision and recall metrics for two consecutive years.

### Comparison with other LULC maps

To complement our independent validation, we performed a spatial comparison between the grassland maps and 30 m global land cover products, UMD GLAD GLCLUC[13](https://www.nature.com/articles/s41597-024-04139-6#ref-CR13 "Potapov, P. et al. The global 2000-2020 land cover and land use change dataset derived from the landsat archive: first results. Frontiers in Remote Sensing 3, 856903,                    https://doi.org/10.3389/frsen.2022.856903                                     (2022).") and the GLC\_FC30[15](https://www.nature.com/articles/s41597-024-04139-6#ref-CR15 "Zhang, X. et al. GLC_fcs30d: the first global 30 m land-cover dynamics monitoring product with a fine classification system for the period from 1985 to 2022 generated using dense-time-series Landsat imagery and the continuous change-detection method. Earth System Science Data 16, 1353–1381,                    https://doi.org/10.5194/essd-16-1353-2024                                     (2024)."), respectively. For each grassland class ( _i.e_. cultivated and natural/semi-natural), we calculated the overlap with LULC classes from the products for 3 years (2000, 2010 and 2020). To allow for easier comparison, we combined some of the classes (deciduous and broadleaf forest into a _Forest_ class, for example) in each of the LULC products and additionally combined any classes with less than 3% overlap with the grassland classes into the _other_ class. With this comparison, we want to identify potential confusion between our grassland predictions and unexpected LULC classes. For example, we expect our _grassland_ classes to overlap with the _grassland_ class from GLC\_FC30 rather than the _forest_ class. The comparisons revealed that the grassland proportions do not change over time, so we show only three years out of 20.

Comparison between UMD GLAD GLCLUC and our grassland classes revealed that most of the overlap occurs with the _short vegetation_ class (71% for cultivated and 78% for natural/semi-natural), with _croplands_ (16% for cultivated) and with _wet short vegetation_ (16% for natural/semi-natural). Confusion between cultivated grassland and croplands is expected, as these classes may have very similar spectral-temporal responses in EO imagery[70](https://www.nature.com/articles/s41597-024-04139-6#ref-CR70 "Van Tricht, K. et al. Worldcereal: a dynamic open-source system for global-scale, seasonal, and reproducible crop and irrigation mapping. Earth System Science Data 15, 5491–5515,                    https://doi.org/10.5194/essd-15-5491-2023                                     (2023)."), [71](https://www.nature.com/articles/s41597-024-04139-6#ref-CR71 "Blickensdörfer, L. et al. Mapping of crop types and crop sequences with combined time series of sentinel-1, sentinel-2 and landsat 8 data for germany. Remote sensing of environment 269, 112831,                    https://doi.org/10.1016/j.rse.2021.112831                                     (2022).")) and overlapping taxonomies ( _e.g_. hay is a type of grass that is planted but falls outside our definition of cultivated grasslands). The comparison between GLC\_FC30 and our grassland classes revealed that most of the overlap occurs with _grasslands_ (24% for cultivated and 27% for natural/semi-natural), _rainfed cropland_ (21% for cultivated), _herbaceous cover cropland_ (27% for cultivated), _shrubland_ (11% for cultivated and 22% for natural/semi-natural), and _sparse vegetation_ (21% for natural/semi-natural). There was unexpected overlap between grassland and _forest_ (14% for cultivated and 12% for natural/semi-natural).

However, comparison between our predictions and 30 m products time-series of land cover is limited because our grassland classes are defined based on the use and overlap of 3 + classes ( _e.g. grassland, shrubland, short vegetation_) in either of the two LULC legends. The only global grassland products we can compare with our predictions are coarse resolution, such the 10 km pasture map of the world for the year 2000[9](https://www.nature.com/articles/s41597-024-04139-6#ref-CR9 "Ramankutty, N., Evan, A. T., Monfreda, C. & Foley, J. A. Farming the planet: 1. geographic distribution of global agricultural lands in the year 2000. Global biogeochemical cycles 22,                    https://doi.org/10.1029/2007GB002952                                     (2008).") and the HILDA+ distribution of _pasture/rangeland_ and _unmanaged grass/shrubland_ at 1 km resolution[10](https://www.nature.com/articles/s41597-024-04139-6#ref-CR10 "Winkler, K., Fuchs, R., Rounsevell, M. & Herold, M. Global land use changes are four times greater than previously estimated. Nature communications 12, 2501,                    https://doi.org/10.1038/s41467-021-22702-2                                     (2021).") (see Fig. [8](https://www.nature.com/articles/s41597-024-04139-6#Fig8)). Comparing our predictions of _cultivated grassland_, in general, shows a good match, especially with the global pastureland map by Ramankutty _et al_.[9](https://www.nature.com/articles/s41597-024-04139-6#ref-CR9 "Ramankutty, N., Evan, A. T., Monfreda, C. & Foley, J. A. Farming the planet: 1. geographic distribution of global agricultural lands in the year 2000. Global biogeochemical cycles 22,                    https://doi.org/10.1029/2007GB002952                                     (2008)."); when looking more closely, it seems that the previous products miss some smaller patches where we are certain they can be classified as pastures, but were probably difficult to distinguish from other cropland similar to them or were just too small for resolution of 1 km.

**Fig. 8**

![Fig. 8](https://media.springernature.com/lw685/springer-static/image/art%3A10.1038%2Fs41597-024-04139-6/MediaObjects/41597_2024_4139_Fig8_HTML.png)

[Full size image](https://www.nature.com/articles/s41597-024-04139-6/figures/8)

Comparision of pastureland distribution map produced by Ramankutty _et al_.[9](https://www.nature.com/articles/s41597-024-04139-6#ref-CR9 "Ramankutty, N., Evan, A. T., Monfreda, C. & Foley, J. A. Farming the planet: 1. geographic distribution of global agricultural lands in the year 2000. Global biogeochemical cycles 22,                    https://doi.org/10.1029/2007GB002952                                     (2008)."), land cover classes at 1 km resolution based on HILDA+ data set[10](https://www.nature.com/articles/s41597-024-04139-6#ref-CR10 "Winkler, K., Fuchs, R., Rounsevell, M. & Herold, M. Global land use changes are four times greater than previously estimated. Nature communications 12, 2501,                    https://doi.org/10.1038/s41467-021-22702-2                                     (2021)."), and our predictions for cultivated and natural / semi-natural grassland at 30 m resolution focused in: ( **A**) Kazakhstan, ( **B**) Australia, ( **C**) Uruguay, ( **D**) Ireland / UK and ( **E**) South West Africa.

A comparison between HILDA+ and our grassland predictions reveals similar patterns of overlap as described above; however, in this case, we also wanted to assess whether there are grassland areas that we are missing (as demonstrated by the accuracy assessment based on the GLANCE training dataset) and found that 11% and 12% of our _other land cover_ class fall within areas classified in HILDA+ as _pasture/rangeland_ and _unmanaged grass/shrubland_, respectively. Moreover, 6% of our _other land cover_ class falls within the pasture class for the year 2000 of Ramankutty _et al_.[9](https://www.nature.com/articles/s41597-024-04139-6#ref-CR9 "Ramankutty, N., Evan, A. T., Monfreda, C. & Foley, J. A. Farming the planet: 1. geographic distribution of global agricultural lands in the year 2000. Global biogeochemical cycles 22,                    https://doi.org/10.1029/2007GB002952                                     (2008).") map. While some of this overlap can be explained by the difference in spatial resolution between the two products (30 m vs 10 km), some of it is due to the under-prediction of the extent of grasslands in our product. On the other hand, because our analysis is not limited to pasturelands, the extent of our natural grasslands far exceeds the extent of pasturelands as reported by Ramankutty _et al_.[9](https://www.nature.com/articles/s41597-024-04139-6#ref-CR9 "Ramankutty, N., Evan, A. T., Monfreda, C. & Foley, J. A. Farming the planet: 1. geographic distribution of global agricultural lands in the year 2000. Global biogeochemical cycles 22,                    https://doi.org/10.1029/2007GB002952                                     (2008).").

## Usage Notes

Users can provide feedback and report classification errors for dominant class maps in Geo-Wiki and all the maps (4 terabytes in total) are also publicly accessible in the follow platforms:

- Geo-Wiki (Feedback tool): [https://geo-wiki.org](https://geo-wiki.org/)

- Google Earth Engine Apps:
  - Map customization: [https://global-pasture-watch.projects.earthengine.app/view/ggc-30m](https://global-pasture-watch.projects.earthengine.app/view/ggc-30m)

  - Comparison tool: [https://ee-vieiramesquita.projects.earthengine.app/view/ggc-30m-comparison](https://ee-vieiramesquita.projects.earthengine.app/view/ggc-30m-comparison)
- Earth Engine Image Collections:
  - projects/global-pasture-watch/assets/ggc-30m/v1/cultiv-grassland\_p

  - projects/global-pasture-watch/assets/ggc-30m/v1/grassland\_c

  - projects/global-pasture-watch/assets/ggc-30m/v1/nat-semi-grassland\_p

### Grassland probability maps

The main data output described in this paper is the time series of probabilities for two classes of grasslands ( _i.e_. cultivated and natural/semi-natural representing the end members of a spectrum of grassland definitions, selected primarily based on the capacity of identifying them in VHR imagery), estimated independently by global Random Forest models. In general, our predictions are able to capture the expansion of cultivated grassland over different types of native vegetation in tropics (see Figs. [9a](https://www.nature.com/articles/s41597-024-04139-6#Fig9), [c](https://www.nature.com/articles/s41597-024-04139-6#Fig9) and [10](https://www.nature.com/articles/s41597-024-04139-6#Fig10)), and distinguish between grassland and cropland in, for example; Europe (Fig. [9b](https://www.nature.com/articles/s41597-024-04139-6#Fig9)), Asia (Fig. [9d](https://www.nature.com/articles/s41597-024-04139-6#Fig9)) and Australia (Fig. [9e](https://www.nature.com/articles/s41597-024-04139-6#Fig9)) over multiple years.

**Fig. 9**

![Fig. 9](https://media.springernature.com/lw685/springer-static/image/art%3A10.1038%2Fs41597-024-04139-6/MediaObjects/41597_2024_4139_Fig9_HTML.png)

[Full size image](https://www.nature.com/articles/s41597-024-04139-6/figures/9)

Examples of predicted probabilities for cultivated and natural/semi-natural grassland in ( **A)** Paraguay, ( **B)** Scotland - UK, ( **C)** Democratic Republic of the Congo–DRC, ( **D)** Kazakhstan and ( **E)** Australia. Landsat ARD-2 images are shown as true colour composite (red, green and blue) for the year of grassland probabilities. The composites are from Mar. & Apr. (all years) in Paraguay and Scotland; Mar. & Apr. 2002 and Nov. & Dec. 2012 in DRC; Aug. & Sep. 2015 and May. & Jun. 2020 in Kazakhstan; and May & Jun. 2007 and Mar. & Apr 2017 in Australia.

**Fig. 10**

![Fig. 10](https://media.springernature.com/lw685/springer-static/image/art%3A10.1038%2Fs41597-024-04139-6/MediaObjects/41597_2024_4139_Fig10_HTML.png)

[Full size image](https://www.nature.com/articles/s41597-024-04139-6/figures/10)

Cultivated grassland probabilities for 2000, 2019 and 2022 at 30 m spatial resolution (below) for a deforested area in in Brazil (Rio Maria, Pará state) as compared to the very high resolution images of ESRI Wayback (above).

Global modeling enables custom thresholds for converting probability values into dominant classes seamlessly and consistently, once all pixels are predicted using the same model for all years across the world. To demonstrate this application, we derived global maps for dominant classes considering balanced probability thresholds, where precision and recall have similar values according to our five-fold spatial blocking cross-validation ( _i.e_. 0.38 for _Cultivated grassland_ and 0.42 for _Natural/Semi-natural grassland_), resulting in more area mapped as grassland (both classes combined) compared to a naive threshold ( _i.e_. 0.5–see Fig. [S4](https://www.nature.com/articles/s41597-024-04139-6#MOESM1)). However, the assessment with existing independent reference sample datasets consistently showed greater precision than recall ( _i.e_. more omission than commission error for dominant classes), which can be partly explained by the inherent limitations in harmonizing multiple grassland definitions with our classification taxonomy. The independent accuracy assessment paired with the visual comparison with existing land cover products have shown that, most likely, the maps for dominant classes are providing a conservative estimate for global grassland areas. Users of dominant class maps should additionally note that our global thresholds were derived from ∼70% of total tiles ( _i.e_. 1 × 1 km) determined by our sampling design and may not cover specific grassland regions where VHR imagery was not available. Additionally, our predictions were based on independent ML models, which treated each class separately and resulted in several grassland areas mapped simultaneously as cultivated and natural/semi-natural after applying the balanced probability threshold (See Fig. [9](https://www.nature.com/articles/s41597-024-04139-6#Fig9)). As _natural/semi-natural grasslands_ reached a higher accuracy than _cultivated grassland_, pixels that reached the required threshold in both classes were assigned the natural/semi-natural class over the cultivated one, which additionally assumes a position in line with the precautionary principle for monitoring global natural/semi-natural grasslands[72](https://www.nature.com/articles/s41597-024-04139-6#ref-CR72 "Kriebel, D. et al. The precautionary principle in environmental science. Environmental health perspectives 109, 871–876,                    https://doi.org/10.1289/ehp.0110987                                     (2001).").

Our mapping strategy has the main aim of providing probabilities that allow the production of customized maps of dominant grassland classes (as demonstrated in the current study) and empower users to define their own decision and integration rules ( _e.g_. probability threshold, class priority, other land cover masks). For example, a user interested in South African grasslands can select a specific probability threshold based on national reference samples, prioritize cultivated over natural/semi-natural grasslands and mask areas mapped as cropland by existing land cover maps. In this way, the global maps provided here constitute an integral component of a broader framework led by GPW focusing on grassland, pastures, and livestock monitoring (see Fig. [11a](https://www.nature.com/articles/s41597-024-04139-6#Fig11)). Some of the potential uses identified in project conception which are aimed to serve a wide range of organizations and user communities at global, national, and local scale, include the following:

- **Precision-recall calibration**: Reference grassland samples, including _in-situ_ data, can be used to estimate precision-recall curves for target areas ( _e.g_. watersheds, biomes, administrative areas), enabling the development and use of locally calibrated thresholds. Such local probability thresholds would necessarily differ from those found in our global analysis ( _i.e_. 0.32 for _Cultivated grassland_ and 0.42 for _Natural/Semi-natural grassland_), and are likely to result in grassland maps which more accurately reflect the target local area. In addition to balancing precision and recall, other criteria could be used to define the threshold, minimizing the error of omission, for example, based on the Murashkin _et al_.[73](https://www.nature.com/articles/s41597-024-04139-6#ref-CR73 "Murashkin, D., Spreen, G., Huntemann, M. & Dierking, W. Method for detection of leads from sentinel-1 sar images. Annals of Glaciology 59, 124–136,                    https://doi.org/10.1017/aog.2018.6                                     (2018).") method.

- **Area estimation calibration**: Known or estimated quantities of _cultivated grassland_ and _natural/semi-natural grassland_ in an administrative area, for example, through reports or census results, can be used to derive thresholds that explicitly enforce correct and spatial class proportions. Recent findings suggest that this can be done in a way that actually modestly improves overall map accuracy, especially in parts of the map where classes are mixed or atypical in the feature space[74](https://www.nature.com/articles/s41597-024-04139-6#ref-CR74 "Witjes, M., Herold, M. & de Bruin, S. Iterative Mapping of Probabilities (IMP): A data fusion framework for generating accurate land cover maps that match area statistics. Journal of Applied Earth Observation and Geoinformation                    https://doi.org/10.21203/rs.3.rs-3481177/v1                                     (2024)."), which might be particularly useful to match grazing areas with livestock census records in the context of the Gridded Livestock of the World product[75](https://www.nature.com/articles/s41597-024-04139-6#ref-CR75 "Gilbert, M. et al. Global distribution data for cattle, buffaloes, horses, sheep, goats, pigs, chickens and ducks in 2010. Scientific data 5, 1–11,                    https://doi.org/10.1038/sdata.2018.227                                     (2018).").

- **Land cover primitives**: Combined with other land cover products, probability maps can be used as _“primitives”_/ which are considered as building blocks for the construction of ensemble land cover products (see Fig. [11b](https://www.nature.com/articles/s41597-024-04139-6#Fig11)). _“Primitives”_ represent raw information needed to make decisions within a dichotomous key applied to land cover typologies, and recent findings have shown consistent and promising results through an implementation that assumes Random Forest probabilities as land cover primitives[76](https://www.nature.com/articles/s41597-024-04139-6#ref-CR76 "Saah, D. et al. Primitives as building blocks for constructing land cover maps. International Journal of Applied Earth Observation and Geoinformation 85, 101979,                    https://doi.org/10.1016/j.jag.2019.101979                                     (2020)."). In addition to probabilities, dominant land cover classes from existing products ( _e.g_. GLanCE30[77](https://www.nature.com/articles/s41597-024-04139-6#ref-CR77 "Arevalo, P. et al. Global land cover mapping and estimation yearly 30 m V001 (Distributed by NASA EOSDIS Land Processes DAAC, 2022)."), GLC FCS30[78](https://www.nature.com/articles/s41597-024-04139-6#ref-CR78 "Zhang, X. et al. Glc_fcs30: global land-cover product with fine classification system at 30 m using time-series landsat imagery. Earth System Science Data 13, 2753–2776,                    https://doi.org/10.5194/essd-13-2753-2021                                     (2021)."), MapBiomas[17](https://www.nature.com/articles/s41597-024-04139-6#ref-CR17 "Souza, C. M. et al. Reconstructing Three Decades of Land Use and Land Cover Changes in Brazilian Biomes with Landsat Archive and Earth Engine. Remote Sensing 12, 2735,                    https://doi.org/10.3390/rs12172735                                     (2020).")) can be used as _“primitives”_ if converted to indicators ( _i.e_. binary rasters); weighted by expert-based rules and averaged by standardization fractions that sum up 100% amongst all inputs. Although this possibility can take advantage of several land cover products in a holistic and multi-scale way; the process of legend harmonization amongst the classes might constitute an undefined source of uncertainty and requires further investigation.


**Fig. 11**

![Fig. 11](https://media.springernature.com/lw685/springer-static/image/art%3A10.1038%2Fs41597-024-04139-6/MediaObjects/41597_2024_4139_Fig11_HTML.png)

[Full size image](https://www.nature.com/articles/s41597-024-04139-6/figures/11)

Future Global Pasture Watch applications for the produced grassland probability maps: ( **a**) to delineate for example active grazing areas matching with census estimates and help produce more reasonable livestock density maps[75](https://www.nature.com/articles/s41597-024-04139-6#ref-CR75 "Gilbert, M. et al. Global distribution data for cattle, buffaloes, horses, sheep, goats, pigs, chickens and ducks in 2010. Scientific data 5, 1–11,                    https://doi.org/10.1038/sdata.2018.227                                     (2018)."), ( **b**) to help produce global time-series of ensemble land cover products harmonizing and combining multiple existing products (Esa WorldCover[14](https://www.nature.com/articles/s41597-024-04139-6#ref-CR14 "Zanaga, D. et al. ESA WorldCover 10 m 2020 v100                    https://doi.org/10.5281/zenodo.5571936                                     (2021).") UMD GLAD GLCLUC[13](https://www.nature.com/articles/s41597-024-04139-6#ref-CR13 "Potapov, P. et al. The global 2000-2020 land cover and land use change dataset derived from the landsat archive: first results. Frontiers in Remote Sensing 3, 856903,                    https://doi.org/10.3389/frsen.2022.856903                                     (2022)."), GLC FCS30[78](https://www.nature.com/articles/s41597-024-04139-6#ref-CR78 "Zhang, X. et al. Glc_fcs30: global land-cover product with fine classification system at 30 m using time-series landsat imagery. Earth System Science Data 13, 2753–2776,                    https://doi.org/10.5194/essd-13-2753-2021                                     (2021).") and GLanCE30[77](https://www.nature.com/articles/s41597-024-04139-6#ref-CR77 "Arevalo, P. et al. Global land cover mapping and estimation yearly 30 m V001 (Distributed by NASA EOSDIS Land Processes DAAC, 2022).")).

### Current limitations and mapping feedback

Despite the flexibility provided by the probability maps, we note several classification issues and limitation in our grassland predictions (see Table [6](https://www.nature.com/articles/s41597-024-04139-6#Tab6)). Most of these issues ( _e.g_. specially the miss-classification errors) are not trivial to resolve in the face of Random Forest as a complex and non-linear prediction system, as we are not sure these outcomes happen because of (1) extrapolation problems, (2) noise/limited detectability in the Landsat images, (3) fuzzy definition of grassland classes, (4) need of more specialized and regional/local ML models, or (5) simply a lack of training points in these areas. Our best approach moving forward is to simply increase the representation of regional cultural knowledge in these areas and assess the accuracy of future versions of the maps with global and local reference validation samples/datasets.

**Table 6 Issues and limitation currently identified in the global grassland maps.**

[Full size table](https://www.nature.com/articles/s41597-024-04139-6/tables/6)

Nevertheless, we can reasonably assume that some of these issues are related to very similar values of two or more classes in the feature space (limited detectability in Landsat images), where our ML models did not allow separation among areas with distinct LULC dynamics as embodied in our visually interpreted training dataset. It appears that intensively managed grasslands, with high homogeneity under many conditions, have a high chance of being confused with other classes that have very similar spectral properties, such as urban mosaics ( _i.e_. buildings, sparse trees and grass fields with different densities) or (greenish) croplands with similar vegetation height and spatial configuration (such as cereal crops[70](https://www.nature.com/articles/s41597-024-04139-6#ref-CR70 "Van Tricht, K. et al. Worldcereal: a dynamic open-source system for global-scale, seasonal, and reproducible crop and irrigation mapping. Earth System Science Data 15, 5491–5515,                    https://doi.org/10.5194/essd-15-5491-2023                                     (2023)."), [71](https://www.nature.com/articles/s41597-024-04139-6#ref-CR71 "Blickensdörfer, L. et al. Mapping of crop types and crop sequences with combined time series of sentinel-1, sentinel-2 and landsat 8 data for germany. Remote sensing of environment 269, 112831,                    https://doi.org/10.1016/j.rse.2021.112831                                     (2022).")). Less intensively cultivated grasslands, where more diverse plant species can be found and where the landscape may not be very regular, are easily confused with grasslands that are not cultivated or (semi) natural herbaceous vegetation, in general[68](https://www.nature.com/articles/s41597-024-04139-6#ref-CR68 "Pérez-Hoyos, A., Udas, A. & Rembold, F. Integrating multiple land cover maps through a multi-criteria analysis to improve agricultural monitoring in africa. International Journal of Applied Earth Observation and Geoinformation 88, 102064,                    https://doi.org/10.1016/j.jag.2020.102064                                     (2020)."). In addition, the spectral signal of cultivated grasslands can not be as clearly distinguished from natural/semi-natural grassland as it could be from croplands, where there are clear breaks in vegetation growth in cases where multi-temporal clear-sky images are available[79](https://www.nature.com/articles/s41597-024-04139-6#ref-CR79 "Potapov, P. et al. Global maps of cropland extent and change show accelerated cropland expansion in the twenty-first century. Nature Food 3, 19–28,                    https://doi.org/10.1038/s43016-021-00429-z                                     (2022).").

The distinction between cultivated and natural/semi-natural grasslands has been notoriously difficult to map in the past[16](https://www.nature.com/articles/s41597-024-04139-6#ref-CR16 "Jones, M. O. et al. Innovation in rangeland monitoring: annual, 30 m, plant functional type percent cover maps for U.S. rangelands, 1984–2017. Ecosphere 9, e02430,                    https://doi.org/10.1002/ecs2.2430                                     (2018)."), [17](https://www.nature.com/articles/s41597-024-04139-6#ref-CR17 "Souza, C. M. et al. Reconstructing Three Decades of Land Use and Land Cover Changes in Brazilian Biomes with Landsat Archive and Earth Engine. Remote Sensing 12, 2735,                    https://doi.org/10.3390/rs12172735                                     (2020)."), [80](https://www.nature.com/articles/s41597-024-04139-6#ref-CR80 "Mancino, G., Falciano, A., Console, R. & Trivigno, M. L. Comparison between parametric and non-parametric supervised land cover classifications of sentinel-2 msi and landsat-8 oli data. Geographies 3, 82–109,                    https://doi.org/10.3390/geographies3010005                                     (2023)."), which has also affected our reference data collection and harmonization process. Hence, our reference labeling protocol relied on more indirect indicators of management, such as fences and other typical infrastructure, hay bales, machine presence, and even animal presence in the field or geometric shapes of the landscape. This may lead to an underestimation of signs of cultivation that may be less intensive or where VHR imagery was not available at the time of management practices. Regarding our harmonization process, the description or labeling among different datasets is a limiting factor. Since we analyzed samples from a wide range of sources, all with their own ontological definitions and classification taxonomy, harmonization was possible only based on rough estimations. Even when acknowledging language and conceptual differences; some fundamental differences between scientific domains/schools of thought/cultural views may also result in ambiguous terms or descriptions. For example, while it may be called _“rangeland”_ in the U.S., the same concept would be called _“pasture”_ in Europe, while a _“pastagem”_ (the literal translation of ‘pasture’) would be regarded as a cultivated grassland in Brazil. Often, the finer distinctions of how dataset creators perceive and interpret mental concepts whilst creating the training dataset, is missing from their fundamental description, making it harder for downstream applications to form a proper semantic match across many datasets. Due to these challenges, we have attempted to be as clear and as transparent as possible in our reference labeling criteria and to plan for active inclusion of regional cultural knowledge in further versions of Global Pasture Watch products.

One possible way to resolve such semantic/ontological issues is through international registers where land cover and land use classes/systems are unequivocally specified and illustrated with decision trees and photographs accompanied by multi-lingual descriptions. However, for this, the international community would have not just to provide such context, but to also have to agree on some thresholds and recommendations, such as the minimum livestock densities in relation to productivity, the minimum number of years under some land use system, and the duration of fallow periods. Disregarding such forward looking assertions, our predicted grassland distribution for 2000–2022 aims to become an integral component of a broader framework of monitoring products to be produced by Global Pasture Watch and will also include aspects of grassland productivity, fraction of scrubs and woody vegetation, and densities of multiple livestock animals ( _i.e_. cattle, goat, sheep, buffalo and horses). The data set presented here is the first essential step toward these future products, serving as both a pioneering demonstration and a foundation for ongoing refinements (follow the project at [https://landcarbonlab.org/data/global-grassland-and-livestock-monitoring/](https://landcarbonlab.org/data/global-grassland-and-livestock-monitoring/)).

Users need to be aware of the limitations and the known issues discussed in this section; whilst considering them carefully to ensure appropriate use of maps at this initial prediction stage ( _e.g_. we do not recommend the usage of our global maps as replacement for fieldwork campaigns and/or source of ground-truth data for grassland ecosystems). Alongside noting shortcomings in current maps, we are working actively to address most of the these issues through mapping feedback campaigns on the Geo-Wiki platform, where experts and/or users with local knowledge of LULC classes can visualize and interact with the most recent versions of our products. Additionally, all global products used in our comparison analyzes (UMD GLAD, GLC FCS30D, HILDA+, Ramankutty _et al_.[9](https://www.nature.com/articles/s41597-024-04139-6#ref-CR9 "Ramankutty, N., Evan, A. T., Monfreda, C. & Foley, J. A. Farming the planet: 1. geographic distribution of global agricultural lands in the year 2000. Global biogeochemical cycles 22,                    https://doi.org/10.1029/2007GB002952                                     (2008).")) have been uploaded on the platform, supporting users in the provision of feedback regarding overall agreement, spatio-temporal consistency, and over- and under-estimated grassland extent. Solicited feedback via Geo-Wiki may consist of drawing polygons in designated or non-designated areas, concentrating on the differentiation of (1) grassland or non-grass cover and (2) cultivated or natural/semi-natural grassland. In order to improve the consistency of the mapping feedback and avoid ambiguities in visual interpretation and classification, users are provided with sufficient materials to follow the predefined labeling criteria and protocols. The consortium considers that systematically collected feedback, together with multiple partnerships and wide stakeholder participation, will lead to the most efficient path for improving future versions of the Global Pasture Watch products, supporting the development of fit-for-purpose applications able to advance the protection, restoration and sustainable use of global grasslands. We encourage and welcome all readers of this publication to contribute knowledge to this effort.

## Code availability

All workflow presented in this paper were implemented in Python, and the source code is publicly available (MIT License) at: [https://github.com/wri/global-pasture-watch](https://github.com/wri/global-pasture-watch). For reproducibility purposes, we have archived a snapshot of the source code (release ggc30m\_v1) ( [https://doi.org/10.5281/zenodo.13952867](https://doi.org/10.5281/zenodo.13952867) [81](https://www.nature.com/articles/s41597-024-04139-6#ref-CR81 "Parente, L. & Consoli, D. Global Pasture Watch - Source code of the global grassland class and extent maps at 30 m,                    https://doi.org/10.5281/zenodo.13952867                                     (2024).")), all reference samples ( [https://doi.org/10.5281/zenodo.14035457](https://doi.org/10.5281/zenodo.14035457) [82](https://www.nature.com/articles/s41597-024-04139-6#ref-CR82 "Parente, L. et al. Global Pasture Watch - Grassland reference samples based on visual interpretation of VHR imagery (2000–2022),                    https://doi.org/10.5281/zenodo.14035457                                     (2024).")) and trained models ( [https://doi.org/10.5281/zenodo.13952806](https://doi.org/10.5281/zenodo.13952806) [83](https://www.nature.com/articles/s41597-024-04139-6#ref-CR83 "Parente, L. et al. Global Pasture Watch - Global machine learning model for prediction of cultivated and natural/semi-natural grassland,                    https://doi.org/10.5281/zenodo.13952806                                     (2024).")) in Zenodo.

## References

01. Bardgett, R. D. _et al_. Combatting global grassland degradation. _Nature Reviews Earth & Environment_ **2**, 720–735, [https://doi.org/10.1038/s43017-021-00207-2](https://doi.org/10.1038/s43017-021-00207-2) (2021).

    [Article](https://doi.org/10.1038%2Fs43017-021-00207-2) [ADS](http://adsabs.harvard.edu/cgi-bin/nph-data_query?link_type=ABSTRACT&bibcode=2021NRvEE...2..720B) [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Combatting%20global%20grassland%20degradation&journal=Nature%20Reviews%20Earth%20%26%20Environment&doi=10.1038%2Fs43017-021-00207-2&volume=2&pages=720-735&publication_year=2021&author=Bardgett%2CRD)

02. O’Mara, F. P. The role of grasslands in food security and climate change. _Annals of Botany_ **110**, 1263–1270, [https://doi.org/10.1093/aob/mcs209](https://doi.org/10.1093/aob/mcs209) (2012).

    [Article](https://doi.org/10.1093%2Faob%2Fmcs209) [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=23002270) [PubMed Central](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC3478061) [Google Scholar](http://scholar.google.com/scholar_lookup?&title=The%20role%20of%20grasslands%20in%20food%20security%20and%20climate%20change&journal=Annals%20of%20Botany&doi=10.1093%2Faob%2Fmcs209&volume=110&pages=1263-1270&publication_year=2012&author=O%E2%80%99Mara%2CFP)

03. Klein Goldewijk, K., Beusen, A., Doelman, J. & Stehfest, E. Anthropogenic land use estimates for the Holocene–HYDE 3.2. _Earth System Science Data_ **9**, 927–953, [https://doi.org/10.5194/essd-9-927-2017](https://doi.org/10.5194/essd-9-927-2017) (2017).

    [Article](https://doi.org/10.5194%2Fessd-9-927-2017) [ADS](http://adsabs.harvard.edu/cgi-bin/nph-data_query?link_type=ABSTRACT&bibcode=2017ESSD....9..927K) [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Anthropogenic%20land%20use%20estimates%20for%20the%20Holocene%E2%80%93HYDE%203.2&journal=Earth%20System%20Science%20Data&doi=10.5194%2Fessd-9-927-2017&volume=9&pages=927-953&publication_year=2017&author=Klein%20Goldewijk%2CK&author=Beusen%2CA&author=Doelman%2CJ&author=Stehfest%2CE)

04. Chang, J. _et al_. Climate warming from managed grasslands cancels the cooling effect of carbon sinks in sparsely grazed and natural grasslands. _Nature Communications_ **12**, 118, [https://doi.org/10.1038/s41467-020-20406-7](https://doi.org/10.1038/s41467-020-20406-7) (2021).

    [Article](https://doi.org/10.1038%2Fs41467-020-20406-7) [ADS](http://adsabs.harvard.edu/cgi-bin/nph-data_query?link_type=ABSTRACT&bibcode=2021NatCo..12..118C) [CAS](https://www.nature.com/articles/cas-redirect/1:CAS:528:DC%2BB3MXnsV2gsw%3D%3D) [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=33402687) [PubMed Central](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC7785734) [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Climate%20warming%20from%20managed%20grasslands%20cancels%20the%20cooling%20effect%20of%20carbon%20sinks%20in%20sparsely%20grazed%20and%20natural%20grasslands&journal=Nature%20Communications&doi=10.1038%2Fs41467-020-20406-7&volume=12&publication_year=2021&author=Chang%2CJ)

05. Herrero, M. _et al_. Biomass use, production, feed efficiencies, and greenhouse gas emissions from global livestock systems. _Proceedings of the National Academy of Sciences_ **110**, 20888–20893, [https://doi.org/10.1073/pnas.1308149110](https://doi.org/10.1073/pnas.1308149110) (2013).

    [Article](https://doi.org/10.1073%2Fpnas.1308149110) [ADS](http://adsabs.harvard.edu/cgi-bin/nph-data_query?link_type=ABSTRACT&bibcode=2013PNAS..11020888H) [CAS](https://www.nature.com/articles/cas-redirect/1:CAS:528:DC%2BC2cXnsFyrsA%3D%3D) [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Biomass%20use%2C%20production%2C%20feed%20efficiencies%2C%20and%20greenhouse%20gas%20emissions%20from%20global%20livestock%20systems&journal=Proceedings%20of%20the%20National%20Academy%20of%20Sciences&doi=10.1073%2Fpnas.1308149110&volume=110&pages=20888-20893&publication_year=2013&author=Herrero%2CM)

06. Phelps, L. N. & Kaplan, J. O. Land use for animal production in global change studies: Defining and characterizing a framework. _Global change biology_ **23**, 4457–4471, [https://doi.org/10.1038/nature20584](https://doi.org/10.1038/nature20584) (2017).

    [Article](https://doi.org/10.1038%2Fnature20584) [ADS](http://adsabs.harvard.edu/cgi-bin/nph-data_query?link_type=ABSTRACT&bibcode=2017GCBio..23.4457P) [CAS](https://www.nature.com/articles/cas-redirect/1:CAS:528:DC%2BC28XitVWmurbJ) [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=28434200) [PubMed Central](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC5655935) [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Land%20use%20for%20animal%20production%20in%20global%20change%20studies%3A%20Defining%20and%20characterizing%20a%20framework&journal=Global%20change%20biology&doi=10.1038%2Fnature20584&volume=23&pages=4457-4471&publication_year=2017&author=Phelps%2CLN&author=Kaplan%2CJO)

07. Sulla-Menashe, D., Gray, J. M., Abercrombie, S. P. & Friedl, M. A. Hierarchical mapping of annual global land cover 2001 to present: The MODIS Collection 6 Land Cover product. _Remote Sensing of Environment_ **222**, 183–194, [https://doi.org/10.1016/j.rse.2018.12.013](https://doi.org/10.1016/j.rse.2018.12.013) (2019).

    [Article](https://doi.org/10.1016%2Fj.rse.2018.12.013) [ADS](http://adsabs.harvard.edu/cgi-bin/nph-data_query?link_type=ABSTRACT&bibcode=2019RSEnv.222..183S) [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Hierarchical%20mapping%20of%20annual%20global%20land%20cover%202001%20to%20present%3A%20The%20MODIS%20Collection%206%20Land%20Cover%20product&journal=Remote%20Sensing%20of%20Environment&doi=10.1016%2Fj.rse.2018.12.013&volume=222&pages=183-194&publication_year=2019&author=Sulla-Menashe%2CD&author=Gray%2CJM&author=Abercrombie%2CSP&author=Friedl%2CMA)

08. Plummer, S., Lecomte, P. & Doherty, M. The ESA Climate Change Initiative (CCI): A European contribution to the generation of the Global Climate Observing System. _Remote Sensing of Environment_ **203**, 2–8, [https://doi.org/10.1016/j.rse.2017.07.014](https://doi.org/10.1016/j.rse.2017.07.014) (2017).

    [Article](https://doi.org/10.1016%2Fj.rse.2017.07.014) [ADS](http://adsabs.harvard.edu/cgi-bin/nph-data_query?link_type=ABSTRACT&bibcode=2017RSEnv.203....2P) [Google Scholar](http://scholar.google.com/scholar_lookup?&title=The%20ESA%20Climate%20Change%20Initiative%20%28CCI%29%3A%20A%20European%20contribution%20to%20the%20generation%20of%20the%20Global%20Climate%20Observing%20System&journal=Remote%20Sensing%20of%20Environment&doi=10.1016%2Fj.rse.2017.07.014&volume=203&pages=2-8&publication_year=2017&author=Plummer%2CS&author=Lecomte%2CP&author=Doherty%2CM)

09. Ramankutty, N., Evan, A. T., Monfreda, C. & Foley, J. A. Farming the planet: 1. geographic distribution of global agricultural lands in the year 2000. _Global biogeochemical cycles_ **22**, [https://doi.org/10.1029/2007GB002952](https://doi.org/10.1029/2007GB002952) (2008).

10. Winkler, K., Fuchs, R., Rounsevell, M. & Herold, M. Global land use changes are four times greater than previously estimated. _Nature communications_ **12**, 2501, [https://doi.org/10.1038/s41467-021-22702-2](https://doi.org/10.1038/s41467-021-22702-2) (2021).

    [Article](https://doi.org/10.1038%2Fs41467-021-22702-2) [ADS](http://adsabs.harvard.edu/cgi-bin/nph-data_query?link_type=ABSTRACT&bibcode=2021NatCo..12.2501W) [CAS](https://www.nature.com/articles/cas-redirect/1:CAS:528:DC%2BB3MXhtFWgt7vE) [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=33976120) [PubMed Central](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC8113269) [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Global%20land%20use%20changes%20are%20four%20times%20greater%20than%20previously%20estimated&journal=Nature%20communications&doi=10.1038%2Fs41467-021-22702-2&volume=12&publication_year=2021&author=Winkler%2CK&author=Fuchs%2CR&author=Rounsevell%2CM&author=Herold%2CM)

11. Brown, C. F. _et al_. Dynamic World, Near real-time global 10 m land use land cover mapping. _Scientific Data_ **9**, 251, [https://doi.org/10.1038/s41597-022-01307-4](https://doi.org/10.1038/s41597-022-01307-4) (2022).

    [Article](https://doi.org/10.1038%2Fs41597-022-01307-4) [PubMed Central](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC9184477) [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Dynamic%20World%2C%20Near%20real-time%20global%2010%E2%80%89m%20land%20use%20land%20cover%20mapping&journal=Scientific%20Data&doi=10.1038%2Fs41597-022-01307-4&volume=9&publication_year=2022&author=Brown%2CCF)

12. Friedl, M. A. _et al_. Medium Spatial Resolution Mapping of Global Land Cover and Land Cover Change Across Multiple Decades From Landsat. _Frontiers in Remote Sensing_ **3**, 894571, [https://doi.org/10.3389/frsen.2022.894571](https://doi.org/10.3389/frsen.2022.894571) (2022).

    [Article](https://doi.org/10.3389%2Ffrsen.2022.894571) [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Medium%20Spatial%20Resolution%20Mapping%20of%20Global%20Land%20Cover%20and%20Land%20Cover%20Change%20Across%20Multiple%20Decades%20From%20Landsat&journal=Frontiers%20in%20Remote%20Sensing&doi=10.3389%2Ffrsen.2022.894571&volume=3&publication_year=2022&author=Friedl%2CMA)

13. Potapov, P. _et al_. The global 2000-2020 land cover and land use change dataset derived from the landsat archive: first results. _Frontiers in Remote Sensing_ **3**, 856903, [https://doi.org/10.3389/frsen.2022.856903](https://doi.org/10.3389/frsen.2022.856903) (2022).

    [Article](https://doi.org/10.3389%2Ffrsen.2022.856903) [Google Scholar](http://scholar.google.com/scholar_lookup?&title=The%20global%202000-2020%20land%20cover%20and%20land%20use%20change%20dataset%20derived%20from%20the%20landsat%20archive%3A%20first%20results&journal=Frontiers%20in%20Remote%20Sensing&doi=10.3389%2Ffrsen.2022.856903&volume=3&publication_year=2022&author=Potapov%2CP)

14. Zanaga, D. _et al_. _ESA WorldCover 10 m 2020 v100_ [https://doi.org/10.5281/zenodo.5571936](https://doi.org/10.5281/zenodo.5571936) (2021).

    [Article](https://doi.org/10.5281%2Fzenodo.5571936) [Google Scholar](http://scholar.google.com/scholar_lookup?&title=&journal=ESA%20WorldCover%2010%E2%80%89m%202020%20v100&doi=10.5281%2Fzenodo.5571936&publication_year=2021&author=Zanaga%2CD)

15. Zhang, X. _et al_. GLC\_fcs30d: the first global 30 m land-cover dynamics monitoring product with a fine classification system for the period from 1985 to 2022 generated using dense-time-series Landsat imagery and the continuous change-detection method. _Earth System Science Data_ **16**, 1353–1381, [https://doi.org/10.5194/essd-16-1353-2024](https://doi.org/10.5194/essd-16-1353-2024) (2024).

    [Article](https://doi.org/10.5194%2Fessd-16-1353-2024) [ADS](http://adsabs.harvard.edu/cgi-bin/nph-data_query?link_type=ABSTRACT&bibcode=2024ESSD...16.1353Z) [Google Scholar](http://scholar.google.com/scholar_lookup?&title=GLC_fcs30d%3A%20the%20first%20global%2030%E2%80%89m%20land-cover%20dynamics%20monitoring%20product%20with%20a%20fine%20classification%20system%20for%20the%20period%20from%201985%20to%202022%20generated%20using%20dense-time-series%20Landsat%20imagery%20and%20the%20continuous%20change-detection%20method&journal=Earth%20System%20Science%20Data&doi=10.5194%2Fessd-16-1353-2024&volume=16&pages=1353-1381&publication_year=2024&author=Zhang%2CX)

16. Jones, M. O. _et al_. Innovation in rangeland monitoring: annual, 30 m, plant functional type percent cover maps for U.S. rangelands, 1984–2017. _Ecosphere_ **9**, e02430, [https://doi.org/10.1002/ecs2.2430](https://doi.org/10.1002/ecs2.2430) (2018).

    [Article](https://doi.org/10.1002%2Fecs2.2430) [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Innovation%20in%20rangeland%20monitoring%3A%20annual%2C%2030%E2%80%89m%2C%20plant%20functional%20type%20percent%20cover%20maps%20for%20U.S.%20rangelands%2C%201984%E2%80%932017&journal=Ecosphere&doi=10.1002%2Fecs2.2430&volume=9&publication_year=2018&author=Jones%2CMO)

17. Souza, C. M. _et al_. Reconstructing Three Decades of Land Use and Land Cover Changes in Brazilian Biomes with Landsat Archive and Earth Engine. _Remote Sensing_ **12**, 2735, [https://doi.org/10.3390/rs12172735](https://doi.org/10.3390/rs12172735) (2020).

    [Article](https://doi.org/10.3390%2Frs12172735) [ADS](http://adsabs.harvard.edu/cgi-bin/nph-data_query?link_type=ABSTRACT&bibcode=2020RemS...12.2735S) [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Reconstructing%20Three%20Decades%20of%20Land%20Use%20and%20Land%20Cover%20Changes%20in%20Brazilian%20Biomes%20with%20Landsat%20Archive%20and%20Earth%20Engine&journal=Remote%20Sensing&doi=10.3390%2Frs12172735&volume=12&publication_year=2020&author=Souza%2CCM)

18. Stanimirova, R. _et al_. A global land cover training dataset from 1984 to 2020. _Scientific Data_ **10**, 879 (2023).

    [Article](https://doi.org/10.1038%2Fs41597-023-02798-5) [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=38062043) [PubMed Central](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC10703991) [Google Scholar](http://scholar.google.com/scholar_lookup?&title=A%20global%20land%20cover%20training%20dataset%20from%201984%20to%202020&journal=Scientific%20Data&doi=10.1038%2Fs41597-023-02798-5&volume=10&publication_year=2023&author=Stanimirova%2CR)

19. Potapov, P. _et al_. Landsat analysis ready data for global land cover and land cover change mapping. _Remote Sensing_ **12**, 426, [https://doi.org/10.3390/rs12030426](https://doi.org/10.3390/rs12030426) (2020).

    [Article](https://doi.org/10.3390%2Frs12030426) [ADS](http://adsabs.harvard.edu/cgi-bin/nph-data_query?link_type=ABSTRACT&bibcode=2020RemS...12..426P) [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Landsat%20analysis%20ready%20data%20for%20global%20land%20cover%20and%20land%20cover%20change%20mapping&journal=Remote%20Sensing&doi=10.3390%2Frs12030426&volume=12&publication_year=2020&author=Potapov%2CP)

20. Wan, Z., Hook, S. & Hulley, G. MODIS/Terra Land Surface Temperature/Emissivity 8-Day L3 Global 1 km SIN Grid V061, [https://doi.org/10.5067/MODIS/MOD11A2.061](https://doi.org/10.5067/MODIS/MOD11A2.061) (2021).

21. Lyapustin, A. & Wang, Y. MODIS/Terra + Aqua Land Aerosol Optical Depth Daily L2G Global 1 km SIN Grid V006, [https://doi.org/10.5067/MODIS/MCD19A2.006](https://doi.org/10.5067/MODIS/MCD19A2.006) (2018).

22. Witjes, M. _et al_. A spatiotemporal ensemble machine learning framework for generating land use/land cover time-series maps for Europe (2000–2019) based on LUCAS, CORINE and GLAD Landsat. _PeerJ_ **10**, e13573, [https://doi.org/10.7717/peerj.13573](https://doi.org/10.7717/peerj.13573) (2022).

    [Article](https://doi.org/10.7717%2Fpeerj.13573) [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=35891647) [PubMed Central](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC9308969) [Google Scholar](http://scholar.google.com/scholar_lookup?&title=A%20spatiotemporal%20ensemble%20machine%20learning%20framework%20for%20generating%20land%20use%2Fland%20cover%20time-series%20maps%20for%20Europe%20%282000%E2%80%932019%29%20based%20on%20LUCAS%2C%20CORINE%20and%20GLAD%20Landsat&journal=PeerJ&doi=10.7717%2Fpeerj.13573&volume=10&publication_year=2022&author=Witjes%2CM)

23. Ma, T., Brus, D. J., Zhu, A.-X., Zhang, L. & Scholten, T. Comparison of conditioned Latin hypercube and feature space coverage sampling for predicting soil classes using simulation from soil maps. _Geoderma_ **370**, 114366, [https://doi.org/10.1016/j.geoderma.2020.114366](https://doi.org/10.1016/j.geoderma.2020.114366) (2020).

    [Article](https://doi.org/10.1016%2Fj.geoderma.2020.114366) [ADS](http://adsabs.harvard.edu/cgi-bin/nph-data_query?link_type=ABSTRACT&bibcode=2020Geode.370k4366M) [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Comparison%20of%20conditioned%20Latin%20hypercube%20and%20feature%20space%20coverage%20sampling%20for%20predicting%20soil%20classes%20using%20simulation%20from%20soil%20maps&journal=Geoderma&doi=10.1016%2Fj.geoderma.2020.114366&volume=370&publication_year=2020&author=Ma%2CT&author=Brus%2CDJ&author=Zhu%2CA-X&author=Zhang%2CL&author=Scholten%2CT)

24. ESA Climante Change initiative. Global Land Cover time-series v2.1.1 (1992–2015). [http://maps.elie.ucl.ac.be/CCI/viewer/download.php](http://maps.elie.ucl.ac.be/CCI/viewer/download.php) (2021).

25. Parente, L., Hengl, T., Bonannello, C., Sloat, L. & Wheeler, I. Global Pasture Watch - Grassland sampling design derived by Feature Space Coverage Sampling (FSCV) at 1-km spatial resolution, [https://doi.org/10.5281/zenodo.11275539](https://doi.org/10.5281/zenodo.11275539) (2024).

26. Allen, V. G. _et al_. An international terminology for grazing lands and grazing animals. _Grass and forage science_ **66**, 2, [https://doi.org/10.1111/j.1365-2494.2010.00780.x](https://doi.org/10.1111/j.1365-2494.2010.00780.x) (2011).

    [Article](https://doi.org/10.1111%2Fj.1365-2494.2010.00780.x) [Google Scholar](http://scholar.google.com/scholar_lookup?&title=An%20international%20terminology%20for%20grazing%20lands%20and%20grazing%20animals&journal=Grass%20and%20forage%20science&doi=10.1111%2Fj.1365-2494.2010.00780.x&volume=66&publication_year=2011&author=Allen%2CVG)

27. Upcott, E. V., Henrys, P. A., Redhead, J. W., Jarvis, S. G. & Pywell, R. F. A new approach to characterising and predicting crop rotations using national-scale annual crop maps. _Science of the Total Environment_ **860**, 160471, [https://doi.org/10.1016/j.scitotenv.2022.160471](https://doi.org/10.1016/j.scitotenv.2022.160471) (2023).

    [Article](https://doi.org/10.1016%2Fj.scitotenv.2022.160471) [CAS](https://www.nature.com/articles/cas-redirect/1:CAS:528:DC%2BB38XjtVaju7nP) [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=36435258) [Google Scholar](http://scholar.google.com/scholar_lookup?&title=A%20new%20approach%20to%20characterising%20and%20predicting%20crop%20rotations%20using%20national-scale%20annual%20crop%20maps&journal=Science%20of%20the%20Total%20Environment&doi=10.1016%2Fj.scitotenv.2022.160471&volume=860&publication_year=2023&author=Upcott%2CEV&author=Henrys%2CPA&author=Redhead%2CJW&author=Jarvis%2CSG&author=Pywell%2CRF)

28. Crawford, C. J. _et al_. The 50-year landsat collection 2 archive. _Science of Remote Sensing_ **8**, 100103, [https://doi.org/10.1016/j.srs.2023.100103](https://doi.org/10.1016/j.srs.2023.100103) (2023).

    [Article](https://doi.org/10.1016%2Fj.srs.2023.100103) [Google Scholar](http://scholar.google.com/scholar_lookup?&title=The%2050-year%20landsat%20collection%202%20archive&journal=Science%20of%20Remote%20Sensing&doi=10.1016%2Fj.srs.2023.100103&volume=8&publication_year=2023&author=Crawford%2CCJ)

29. Consoli, D. _et al_. A computational framework for processing time-series of earth observation data based on discrete convolution: global-scale historical landsat cloud-free aggregates at 30 m spatial resolution. _PeerJ_, [https://doi.org/10.7717/peerj.18585](https://doi.org/10.7717/peerj.18585) (In Press).

30. Roy, P., Sharma, K. & Jain, A. Stratification of density in dry deciduous forest using satellite remote sensing digital data–an approach based on spectral indices. _Journal of biosciences_ **21**, 723–734 (1996).

    [Article](https://link.springer.com/doi/10.1007/BF02703148) [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Stratification%20of%20density%20in%20dry%20deciduous%20forest%20using%20satellite%20remote%20sensing%20digital%20data%E2%80%93an%20approach%20based%20on%20spectral%20indices&journal=Journal%20of%20biosciences&doi=10.1007%2FBF02703148&volume=21&pages=723-734&publication_year=1996&author=Roy%2CP&author=Sharma%2CK&author=Jain%2CA)

31. Huete, A. _et al_. Overview of the radiometric and biophysical performance of the modis vegetation indices. _Remote Sensing of Environment_ **83**, 195–213 (2002).

    [Article](https://doi.org/10.1016%2FS0034-4257%2802%2900096-2) [ADS](http://adsabs.harvard.edu/cgi-bin/nph-data_query?link_type=ABSTRACT&bibcode=2002RSEnv..83..195H) [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Overview%20of%20the%20radiometric%20and%20biophysical%20performance%20of%20the%20modis%20vegetation%20indices&journal=Remote%20Sensing%20of%20Environment&doi=10.1016%2FS0034-4257%2802%2900096-2&volume=83&pages=195-213&publication_year=2002&author=Huete%2CA)

32. Van Deventer, A., Ward, A., Gowda, P. & Lyon, J. Using thematic mapper data to identify contrasting soil plains and tillage practices. _Photogrammetric engineering and remote sensing_ **63**, 87–93 (1997).

    [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Using%20thematic%20mapper%20data%20to%20identify%20contrasting%20soil%20plains%20and%20tillage%20practices&journal=Photogrammetric%20engineering%20and%20remote%20sensing&volume=63&pages=87-93&publication_year=1997&author=Deventer%2CA&author=Ward%2CA&author=Gowda%2CP&author=Lyon%2CJ)

33. Tucker, C. J. Red and photographic infrared linear combinations for monitoring vegetation. _Remote sensing of Environment_ **8**, 127–150 (1979).

    [Article](https://doi.org/10.1016%2F0034-4257%2879%2990013-0) [ADS](http://adsabs.harvard.edu/cgi-bin/nph-data_query?link_type=ABSTRACT&bibcode=1979RSEnv...8..127T) [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Red%20and%20photographic%20infrared%20linear%20combinations%20for%20monitoring%20vegetation&journal=Remote%20sensing%20of%20Environment&doi=10.1016%2F0034-4257%2879%2990013-0&volume=8&pages=127-150&publication_year=1979&author=Tucker%2CCJ)

34. Gao, B.-C. NDWI–A normalized difference water index for remote sensing of vegetation liquid water from space. _Remote Sensing of Environment_ **58**, 257–266 (1996).

    [Article](https://doi.org/10.1016%2FS0034-4257%2896%2900067-3) [ADS](http://adsabs.harvard.edu/cgi-bin/nph-data_query?link_type=ABSTRACT&bibcode=1996RSEnv..58..257G) [Google Scholar](http://scholar.google.com/scholar_lookup?&title=NDWI%E2%80%93A%20normalized%20difference%20water%20index%20for%20remote%20sensing%20of%20vegetation%20liquid%20water%20from%20space&journal=Remote%20Sensing%20of%20Environment&doi=10.1016%2FS0034-4257%2896%2900067-3&volume=58&pages=257-266&publication_year=1996&author=Gao%2CB-C)

35. Badgley, G., Field, C. B. & Berry, J. A. Canopy near-infrared reflectance and terrestrial photosynthesis. _Science advances_ **3**, e1602244 (2017).

    [Article](https://doi.org/10.1126%2Fsciadv.1602244) [ADS](http://adsabs.harvard.edu/cgi-bin/nph-data_query?link_type=ABSTRACT&bibcode=2017SciA....3E2244B) [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=28345046) [PubMed Central](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC5362170) [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Canopy%20near-infrared%20reflectance%20and%20terrestrial%20photosynthesis&journal=Science%20advances&doi=10.1126%2Fsciadv.1602244&volume=3&publication_year=2017&author=Badgley%2CG&author=Field%2CCB&author=Berry%2CJA)

36. Castaldi, F., Chabrillat, S., Don, A. & van Wesemael, B. Soil organic carbon mapping using lucas topsoil database and sentinel-2 data: An approach to reduce soil moisture and crop residue effects. _Remote Sensing_ **11**, 2121 (2019).

    [Article](https://doi.org/10.3390%2Frs11182121) [ADS](http://adsabs.harvard.edu/cgi-bin/nph-data_query?link_type=ABSTRACT&bibcode=2019RemS...11.2121C) [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Soil%20organic%20carbon%20mapping%20using%20lucas%20topsoil%20database%20and%20sentinel-2%20data%3A%20An%20approach%20to%20reduce%20soil%20moisture%20and%20crop%20residue%20effects&journal=Remote%20Sensing&doi=10.3390%2Frs11182121&volume=11&publication_year=2019&author=Castaldi%2CF&author=Chabrillat%2CS&author=Don%2CA&author=Wesemael%2CB)

37. Robinson, N. P. _et al_. Terrestrial primary production for the conterminous United States derived from Landsat 30 m and MODIS 250 m. _Remote Sensing in Ecology and Conservation_ **4**, 264–280 (2018).

    [Article](https://doi.org/10.1002%2Frse2.74) [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Terrestrial%20primary%20production%20for%20the%20conterminous%20United%20States%20derived%20from%20Landsat%2030%E2%80%89m%20and%20MODIS%20250%E2%80%89m&journal=Remote%20Sensing%20in%20Ecology%20and%20Conservation&doi=10.1002%2Frse2.74&volume=4&pages=264-280&publication_year=2018&author=Robinson%2CNP)

38. Parente, L., Simoes, R. & Hengl, T. Monthly aggregated Water Vapor MODIS MCD19A2 (1 km): Long-term data (2000–2022), [https://doi.org/10.5281/zenodo.8192544](https://doi.org/10.5281/zenodo.8192544) (2023).

39. Ho, Y. F., Hengl, T. & Parente, L. _Ensemble Digital Terrain Model (EDTM) of the world (1.1)_ (OpenGeoHub foundation, Doorwerth, NL, 2023).

40. Tadono, T. _et al_. Generation of the 30 m-mesh global digital surface model by alos prism. _The international archives of the photogrammetry, remote sensing and spatial information sciences_ **41**, 157–162 (2016).

    [Article](https://doi.org/10.5194%2Fisprs-archives-XLI-B4-157-2016) [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Generation%20of%20the%2030%20m-mesh%20global%20digital%20surface%20model%20by%20alos%20prism&journal=The%20international%20archives%20of%20the%20photogrammetry%2C%20remote%20sensing%20and%20spatial%20information%20sciences&doi=10.5194%2Fisprs-archives-XLI-B4-157-2016&volume=41&pages=157-162&publication_year=2016&author=Tadono%2CT)

41. Strobl, P. The new copernicus digital elevation model. _GSICS Quarterly_ **14**, 17–18 (2020).

    [Google Scholar](http://scholar.google.com/scholar_lookup?&title=The%20new%20copernicus%20digital%20elevation%20model&journal=GSICS%20Quarterly&volume=14&pages=17-18&publication_year=2020&author=Strobl%2CP)

42. Yamazaki, D. _et al_. Merit dem: A new high-accuracy global digital elevation model and its merit to global hydrodynamic modeling. In _AGU fall meeting abstracts_, vol. 2017 (2017).

43. Nelson, A. _et al_. A suite of global accessibility indicators. _Scientific data_ **6**, 266 (2019).

    [Article](https://doi.org/10.1038%2Fs41597-019-0265-5) [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=31700070) [PubMed Central](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC6838165) [Google Scholar](http://scholar.google.com/scholar_lookup?&title=A%20suite%20of%20global%20accessibility%20indicators&journal=Scientific%20data&doi=10.1038%2Fs41597-019-0265-5&volume=6&publication_year=2019&author=Nelson%2CA)

44. Pickens, A. H. _et al_. Mapping and sampling to characterize global inland water dynamics from 1999 to 2018 with full landsat time-series. _Remote Sensing of Environment_ **243**, 111792 (2020).

    [Article](https://doi.org/10.1016%2Fj.rse.2020.111792) [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Mapping%20and%20sampling%20to%20characterize%20global%20inland%20water%20dynamics%20from%201999%20to%202018%20with%20full%20landsat%20time-series&journal=Remote%20Sensing%20of%20Environment&doi=10.1016%2Fj.rse.2020.111792&volume=243&publication_year=2020&author=Pickens%2CAH)

45. Kilibarda, M. _et al_. Spatio-temporal interpolation of daily temperatures for global land areas at 1 km resolution. _Journal of Geophysical Research: Atmospheres_ **119**, 2294–2313 (2014).

    [Article](https://doi.org/10.1002%2F2013JD020803) [ADS](http://adsabs.harvard.edu/cgi-bin/nph-data_query?link_type=ABSTRACT&bibcode=2014JGRD..119.2294K) [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Spatio-temporal%20interpolation%20of%20daily%20temperatures%20for%20global%20land%20areas%20at%201%E2%80%89km%20resolution&journal=Journal%20of%20Geophysical%20Research%3A%20Atmospheres&doi=10.1002%2F2013JD020803&volume=119&pages=2294-2313&publication_year=2014&author=Kilibarda%2CM)

46. Demarchi, L. _et al_. Recursive feature elimination and random forest classification of natura 2000 grasslands in lowland river valleys of poland based on airborne hyperspectral and lidar data fusion. _Remote Sensing_ **12**, 1842, [https://doi.org/10.3390/rs12111842](https://doi.org/10.3390/rs12111842) (2020).

    [Article](https://doi.org/10.3390%2Frs12111842) [ADS](http://adsabs.harvard.edu/cgi-bin/nph-data_query?link_type=ABSTRACT&bibcode=2020RemS...12.1842D) [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Recursive%20feature%20elimination%20and%20random%20forest%20classification%20of%20natura%202000%20grasslands%20in%20lowland%20river%20valleys%20of%20poland%20based%20on%20airborne%20hyperspectral%20and%20lidar%20data%20fusion&journal=Remote%20Sensing&doi=10.3390%2Frs12111842&volume=12&publication_year=2020&author=Demarchi%2CL)

47. Jamieson, K. & Talwalkar, A. Non-stochastic best arm identification and hyperparameter optimization. In _Artificial intelligence and statistics_, 240–248, [https://doi.org/10.1109/SDS.2019.00-11](https://doi.org/10.1109/SDS.2019.00-11) (PMLR, 2016).

48. Breiman, L. Random forests. _Machine learning_ **45**, 5–32, [https://doi.org/10.1023/A:1010933404324](https://doi.org/10.1023/A:1010933404324) (2001).

    [Article](https://doi.org/10.1023%2FA%3A1010933404324) [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Random%20forests&journal=Machine%20learning&doi=10.1023%2FA%3A1010933404324&volume=45&pages=5-32&publication_year=2001&author=Breiman%2CL)

49. Friedman, J. H. Greedy function approximation: a gradient boosting machine. _Annals of statistics_ 1189–1232, [https://doi.org/10.1214/aos/1013203451](https://doi.org/10.1214/aos/1013203451) (2001).

50. Zou, J., Han, Y. & So, S.-S. Overview of artificial neural networks. _Artificial neural networks: methods and applications_ 14–22, [https://doi.org/10.1007/978-1-60327-101-1\_2](https://doi.org/10.1007/978-1-60327-101-1_2) (2009).

51. Shaharum, N. _et al_. Image classification for mapping oil palm distribution via support vector machine using scikit-learn module. _The International Archives of the Photogrammetry, Remote Sensing and Spatial Information Sciences_ **42**, 133–137, [https://doi.org/10.5194/isprs-archives-XLII-4-W9-133-2018](https://doi.org/10.5194/isprs-archives-XLII-4-W9-133-2018) (2018).

    [Article](https://doi.org/10.5194%2Fisprs-archives-XLII-4-W9-133-2018) [ADS](http://adsabs.harvard.edu/cgi-bin/nph-data_query?link_type=ABSTRACT&bibcode=2018ISPAr4249..133S) [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Image%20classification%20for%20mapping%20oil%20palm%20distribution%20via%20support%20vector%20machine%20using%20scikit-learn%20module&journal=The%20International%20Archives%20of%20the%20Photogrammetry%2C%20Remote%20Sensing%20and%20Spatial%20Information%20Sciences&doi=10.5194%2Fisprs-archives-XLII-4-W9-133-2018&volume=42&pages=133-137&publication_year=2018&author=Shaharum%2CN)

52. Bonannella, C. _et al_. Forest tree species distribution for europe 2000–2020: mapping potential and realized distributions using spatiotemporal machine learning. _PeerJ_ **10**, e13728, [https://doi.org/10.7717/peerj.13728](https://doi.org/10.7717/peerj.13728) (2022).

    [Article](https://doi.org/10.7717%2Fpeerj.13728) [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=35910765) [PubMed Central](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC9332400) [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Forest%20tree%20species%20distribution%20for%20europe%202000%E2%80%932020%3A%20mapping%20potential%20and%20realized%20distributions%20using%20spatiotemporal%20machine%20learning&journal=PeerJ&doi=10.7717%2Fpeerj.13728&volume=10&publication_year=2022&author=Bonannella%2CC)

53. Ebrahimy, H., Mirbagheri, B., Matkan, A. A. & Azadbakht, M. Effectiveness of the integration of data balancing techniques and tree-based ensemble machine learning algorithms for spatially-explicit land cover accuracy prediction. _Remote Sensing Applications: Society and Environment_ **27**, 100785, [https://doi.org/10.1016/j.rsase.2022.100785](https://doi.org/10.1016/j.rsase.2022.100785) (2022).

    [Article](https://doi.org/10.1016%2Fj.rsase.2022.100785) [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Effectiveness%20of%20the%20integration%20of%20data%20balancing%20techniques%20and%20tree-based%20ensemble%20machine%20learning%20algorithms%20for%20spatially-explicit%20land%20cover%20accuracy%20prediction&journal=Remote%20Sensing%20Applications%3A%20Society%20and%20Environment&doi=10.1016%2Fj.rsase.2022.100785&volume=27&publication_year=2022&author=Ebrahimy%2CH&author=Mirbagheri%2CB&author=Matkan%2CAA&author=Azadbakht%2CM)

54. Roberts, D. R. _et al_. Cross-validation strategies for data with temporal, spatial, hierarchical, or phylogenetic structure. _Ecography_ **40**, 913–929, [https://doi.org/10.1111/ecog.0288](https://doi.org/10.1111/ecog.0288) (2017).

    [Article](https://doi.org/10.1111%2Fecog.0288) [ADS](http://adsabs.harvard.edu/cgi-bin/nph-data_query?link_type=ABSTRACT&bibcode=2017Ecogr..40..913R) [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Cross-validation%20strategies%20for%20data%20with%20temporal%2C%20spatial%2C%20hierarchical%2C%20or%20phylogenetic%20structure&journal=Ecography&doi=10.1111%2Fecog.0288&volume=40&pages=913-929&publication_year=2017&author=Roberts%2CDR)

55. Marconcini, M. _et al_. Outlining where humans live, the world settlement footprint 2015. _Scientific Data_ **7**, 242, [https://doi.org/10.1038/s41597-020-00580-5](https://doi.org/10.1038/s41597-020-00580-5) (2020).

    [Article](https://doi.org/10.1038%2Fs41597-020-00580-5) [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=32686674) [PubMed Central](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC7371630) [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Outlining%20where%20humans%20live%2C%20the%20world%20settlement%20footprint%202015&journal=Scientific%20Data&doi=10.1038%2Fs41597-020-00580-5&volume=7&publication_year=2020&author=Marconcini%2CM)

56. TL2cgen: model compiler for decision trees. [https://tl2cgen.readthedocs.io/en/latest/](https://tl2cgen.readthedocs.io/en/latest/). Accessed: 2024-03-11.

57. Shekhar, C. On simplified application of multidimensional savitzky-golay filters and differentiators. In _AIP Conference Proceedings_, vol. 1705, [https://doi.org/10.1063/1.4940262](https://doi.org/10.1063/1.4940262) (AIP Publishing, 2016).

58. Yoo, A. B., Jette, M. A. & Grondona, M. Slurm: Simple linux utility for resource management. In _Workshop on job scheduling strategies for parallel processing_, 44–60 (Springer, 2003).

59. Boettiger, C. An introduction to docker for reproducible research. _ACM SIGOPS Operating Systems Review_ **49**, 71–79, [https://doi.org/10.1145/2723872.2723882](https://doi.org/10.1145/2723872.2723882) (2015).

    [Article](https://doi.org/10.1145%2F2723872.2723882) [Google Scholar](http://scholar.google.com/scholar_lookup?&title=An%20introduction%20to%20docker%20for%20reproducible%20research&journal=ACM%20SIGOPS%20Operating%20Systems%20Review&doi=10.1145%2F2723872.2723882&volume=49&pages=71-79&publication_year=2015&author=Boettiger%2CC)

60. Parente, L. _et al_. Global Pasture Watch - Annual grassland class and extent maps at 30-m spatial resolution (2000–2022), [https://doi.org/10.5281/zenodo.13890401](https://doi.org/10.5281/zenodo.13890401) (2024).

61. King, R. D., Orhobor, O. I. & Taylor, C. C. Cross-validation is safe to use. _Nature Machine Intelligence_ **3**, 276–276, [https://doi.org/10.1038/s42256-021-00332-z](https://doi.org/10.1038/s42256-021-00332-z) (2021).

    [Article](https://doi.org/10.1038%2Fs42256-021-00332-z) [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Cross-validation%20is%20safe%20to%20use&journal=Nature%20Machine%20Intelligence&doi=10.1038%2Fs42256-021-00332-z&volume=3&pages=276-276&publication_year=2021&author=King%2CRD&author=Orhobor%2COI&author=Taylor%2CCC)

62. Stehman, S. V. & Foody, G. M. Key issues in rigorous accuracy assessment of land cover products. _Remote Sensing of Environment_ **231**, 111199, [https://doi.org/10.1016/j.rse.2019.05.018](https://doi.org/10.1016/j.rse.2019.05.018) (2019).

    [Article](https://doi.org/10.1016%2Fj.rse.2019.05.018) [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Key%20issues%20in%20rigorous%20accuracy%20assessment%20of%20land%20cover%20products&journal=Remote%20Sensing%20of%20Environment&doi=10.1016%2Fj.rse.2019.05.018&volume=231&publication_year=2019&author=Stehman%2CSV&author=Foody%2CGM)

63. Fritz, S. _et al_. Geo-wiki: An online platform for improving global land cover. _Environmental Modelling & Software_ **31**, 110–123, [https://doi.org/10.1016/j.envsoft.2011.11.015](https://doi.org/10.1016/j.envsoft.2011.11.015) (2012).

    [Article](https://doi.org/10.1016%2Fj.envsoft.2011.11.015) [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Geo-wiki%3A%20An%20online%20platform%20for%20improving%20global%20land%20cover&journal=Environmental%20Modelling%20%26%20Software&doi=10.1016%2Fj.envsoft.2011.11.015&volume=31&pages=110-123&publication_year=2012&author=Fritz%2CS)

64. de Oliveira, B. S., Teles, N. M., Mesquita, V. V., Parente, L. L. & Ferreira, L. G. Integrated Approach to Global Land Use and Land Cover Reference Data Harmonization, [https://doi.org/10.5281/zenodo.11246630](https://doi.org/10.5281/zenodo.11246630) (2024).

65. Zalles, V. _et al_. Rapid expansion of human impact on natural land in south america since 1985. _Science Advances_ **7**, eabg1620, [https://doi.org/10.1126/sciadv.abg1620](https://doi.org/10.1126/sciadv.abg1620) (2021).

    [Article](https://doi.org/10.1126%2Fsciadv.abg1620) [ADS](http://adsabs.harvard.edu/cgi-bin/nph-data_query?link_type=ABSTRACT&bibcode=2021SciA....7.1620Z) [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=33811082) [PubMed Central](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC11057777) [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Rapid%20expansion%20of%20human%20impact%20on%20natural%20land%20in%20south%20america%20since%201985&journal=Science%20Advances&doi=10.1126%2Fsciadv.abg1620&volume=7&publication_year=2021&author=Zalles%2CV)

66. Creutzig, F. _et al_. Assessing human and environmental pressures of global land-use change 2000–2010. _Global Sustainability_ **2**, e1 (2019).

    [Article](https://doi.org/10.1017%2Fsus.2018.15) [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Assessing%20human%20and%20environmental%20pressures%20of%20global%20land-use%20change%202000%E2%80%932010&journal=Global%20Sustainability&doi=10.1017%2Fsus.2018.15&volume=2&publication_year=2019&author=Creutzig%2CF)

67. d’Andrimont, R. _et al_. Harmonised lucas _in-situ_ land cover and use database for field surveys from 2006 to 2018 in the european union. _Scientific data_ **7**, 352, [https://doi.org/10.1038/s41597-019-0340-y](https://doi.org/10.1038/s41597-019-0340-y) (2020).

    [Article](https://doi.org/10.1038%2Fs41597-019-0340-y) [CAS](https://www.nature.com/articles/cas-redirect/1:CAS:528:DC%2BB3cXltlKltA%3D%3D) [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=33067440) [PubMed Central](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC7567823) [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Harmonised%20lucas%20in-situ%20land%20cover%20and%20use%20database%20for%20field%20surveys%20from%202006%20to%202018%20in%20the%20european%20union&journal=Scientific%20data&doi=10.1038%2Fs41597-019-0340-y&volume=7&publication_year=2020&author=d%E2%80%99Andrimont%2CR)

68. Pérez-Hoyos, A., Udas, A. & Rembold, F. Integrating multiple land cover maps through a multi-criteria analysis to improve agricultural monitoring in africa. _International Journal of Applied Earth Observation and Geoinformation_ **88**, 102064, [https://doi.org/10.1016/j.jag.2020.102064](https://doi.org/10.1016/j.jag.2020.102064) (2020).

    [Article](https://doi.org/10.1016%2Fj.jag.2020.102064) [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=32999637) [PubMed Central](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC7497230) [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Integrating%20multiple%20land%20cover%20maps%20through%20a%20multi-criteria%20analysis%20to%20improve%20agricultural%20monitoring%20in%20africa&journal=International%20Journal%20of%20Applied%20Earth%20Observation%20and%20Geoinformation&doi=10.1016%2Fj.jag.2020.102064&volume=88&publication_year=2020&author=P%C3%A9rez-Hoyos%2CA&author=Udas%2CA&author=Rembold%2CF)

69. Tsendbazar, N. _et al_. Towards operational validation of annual global land cover maps. _Remote Sensing of Environment_ **266**, 112686, [https://doi.org/10.1016/j.rse.2021.112686](https://doi.org/10.1016/j.rse.2021.112686) (2021).

    [Article](https://doi.org/10.1016%2Fj.rse.2021.112686) [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Towards%20operational%20validation%20of%20annual%20global%20land%20cover%20maps&journal=Remote%20Sensing%20of%20Environment&doi=10.1016%2Fj.rse.2021.112686&volume=266&publication_year=2021&author=Tsendbazar%2CN)

70. Van Tricht, K. _et al_. Worldcereal: a dynamic open-source system for global-scale, seasonal, and reproducible crop and irrigation mapping. _Earth System Science Data_ **15**, 5491–5515, [https://doi.org/10.5194/essd-15-5491-2023](https://doi.org/10.5194/essd-15-5491-2023) (2023).

    [Article](https://doi.org/10.5194%2Fessd-15-5491-2023) [ADS](http://adsabs.harvard.edu/cgi-bin/nph-data_query?link_type=ABSTRACT&bibcode=2023ESSD...15.5491V) [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Worldcereal%3A%20a%20dynamic%20open-source%20system%20for%20global-scale%2C%20seasonal%2C%20and%20reproducible%20crop%20and%20irrigation%20mapping&journal=Earth%20System%20Science%20Data&doi=10.5194%2Fessd-15-5491-2023&volume=15&pages=5491-5515&publication_year=2023&author=Tricht%2CK)

71. Blickensdörfer, L. _et al_. Mapping of crop types and crop sequences with combined time series of sentinel-1, sentinel-2 and landsat 8 data for germany. _Remote sensing of environment_ **269**, 112831, [https://doi.org/10.1016/j.rse.2021.112831](https://doi.org/10.1016/j.rse.2021.112831) (2022).

    [Article](https://doi.org/10.1016%2Fj.rse.2021.112831) [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Mapping%20of%20crop%20types%20and%20crop%20sequences%20with%20combined%20time%20series%20of%20sentinel-1%2C%20sentinel-2%20and%20landsat%208%20data%20for%20germany&journal=Remote%20sensing%20of%20environment&doi=10.1016%2Fj.rse.2021.112831&volume=269&publication_year=2022&author=Blickensd%C3%B6rfer%2CL)

72. Kriebel, D. _et al_. The precautionary principle in environmental science. _Environmental health perspectives_ **109**, 871–876, [https://doi.org/10.1289/ehp.0110987](https://doi.org/10.1289/ehp.0110987) (2001).

    [Article](https://doi.org/10.1289%2Fehp.0110987) [CAS](https://www.nature.com/articles/cas-redirect/1:STN:280:DC%2BD3MrmsF2hsg%3D%3D) [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=11673114) [PubMed Central](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC1240435) [Google Scholar](http://scholar.google.com/scholar_lookup?&title=The%20precautionary%20principle%20in%20environmental%20science&journal=Environmental%20health%20perspectives&doi=10.1289%2Fehp.0110987&volume=109&pages=871-876&publication_year=2001&author=Kriebel%2CD)

73. Murashkin, D., Spreen, G., Huntemann, M. & Dierking, W. Method for detection of leads from sentinel-1 sar images. _Annals of Glaciology_ **59**, 124–136, [https://doi.org/10.1017/aog.2018.6](https://doi.org/10.1017/aog.2018.6) (2018).

    [Article](https://doi.org/10.1017%2Faog.2018.6) [ADS](http://adsabs.harvard.edu/cgi-bin/nph-data_query?link_type=ABSTRACT&bibcode=2018AnGla..59..124M) [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Method%20for%20detection%20of%20leads%20from%20sentinel-1%20sar%20images&journal=Annals%20of%20Glaciology&doi=10.1017%2Faog.2018.6&volume=59&pages=124-136&publication_year=2018&author=Murashkin%2CD&author=Spreen%2CG&author=Huntemann%2CM&author=Dierking%2CW)

74. Witjes, M., Herold, M. & de Bruin, S. Iterative Mapping of Probabilities (IMP): A data fusion framework for generating accurate land cover maps that match area statistics. _Journal of Applied Earth Observation and Geoinformation_ [https://doi.org/10.21203/rs.3.rs-3481177/v1](https://doi.org/10.21203/rs.3.rs-3481177/v1) (2024).

75. Gilbert, M. _et al_. Global distribution data for cattle, buffaloes, horses, sheep, goats, pigs, chickens and ducks in 2010. _Scientific data_ **5**, 1–11, [https://doi.org/10.1038/sdata.2018.227](https://doi.org/10.1038/sdata.2018.227) (2018).

    [Article](https://doi.org/10.1038%2Fsdata.2018.227) [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Global%20distribution%20data%20for%20cattle%2C%20buffaloes%2C%20horses%2C%20sheep%2C%20goats%2C%20pigs%2C%20chickens%20and%20ducks%20in%202010&journal=Scientific%20data&doi=10.1038%2Fsdata.2018.227&volume=5&pages=1-11&publication_year=2018&author=Gilbert%2CM)

76. Saah, D. _et al_. Primitives as building blocks for constructing land cover maps. _International Journal of Applied Earth Observation and Geoinformation_ **85**, 101979, [https://doi.org/10.1016/j.jag.2019.101979](https://doi.org/10.1016/j.jag.2019.101979) (2020).

    [Article](https://doi.org/10.1016%2Fj.jag.2019.101979) [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Primitives%20as%20building%20blocks%20for%20constructing%20land%20cover%20maps&journal=International%20Journal%20of%20Applied%20Earth%20Observation%20and%20Geoinformation&doi=10.1016%2Fj.jag.2019.101979&volume=85&publication_year=2020&author=Saah%2CD)

77. Arevalo, P. _et al_. _Global land cover mapping and estimation yearly 30 m V001_ (Distributed by NASA EOSDIS Land Processes DAAC, 2022).

78. Zhang, X. _et al_. Glc\_fcs30: global land-cover product with fine classification system at 30 m using time-series landsat imagery. _Earth System Science Data_ **13**, 2753–2776, [https://doi.org/10.5194/essd-13-2753-2021](https://doi.org/10.5194/essd-13-2753-2021) (2021).

    [Article](https://doi.org/10.5194%2Fessd-13-2753-2021) [ADS](http://adsabs.harvard.edu/cgi-bin/nph-data_query?link_type=ABSTRACT&bibcode=2021ESSD...13.2753Z) [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Glc_fcs30%3A%20global%20land-cover%20product%20with%20fine%20classification%20system%20at%2030%E2%80%89m%20using%20time-series%20landsat%20imagery&journal=Earth%20System%20Science%20Data&doi=10.5194%2Fessd-13-2753-2021&volume=13&pages=2753-2776&publication_year=2021&author=Zhang%2CX)

79. Potapov, P. _et al_. Global maps of cropland extent and change show accelerated cropland expansion in the twenty-first century. _Nature Food_ **3**, 19–28, [https://doi.org/10.1038/s43016-021-00429-z](https://doi.org/10.1038/s43016-021-00429-z) (2022).

    [Article](https://doi.org/10.1038%2Fs43016-021-00429-z) [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=37118483) [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Global%20maps%20of%20cropland%20extent%20and%20change%20show%20accelerated%20cropland%20expansion%20in%20the%20twenty-first%20century&journal=Nature%20Food&doi=10.1038%2Fs43016-021-00429-z&volume=3&pages=19-28&publication_year=2022&author=Potapov%2CP)

80. Mancino, G., Falciano, A., Console, R. & Trivigno, M. L. Comparison between parametric and non-parametric supervised land cover classifications of sentinel-2 msi and landsat-8 oli data. _Geographies_ **3**, 82–109, [https://doi.org/10.3390/geographies3010005](https://doi.org/10.3390/geographies3010005) (2023).

    [Article](https://doi.org/10.3390%2Fgeographies3010005) [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Comparison%20between%20parametric%20and%20non-parametric%20supervised%20land%20cover%20classifications%20of%20sentinel-2%20msi%20and%20landsat-8%20oli%20data&journal=Geographies&doi=10.3390%2Fgeographies3010005&volume=3&pages=82-109&publication_year=2023&author=Mancino%2CG&author=Falciano%2CA&author=Console%2CR&author=Trivigno%2CML)

81. Parente, L. & Consoli, D. Global Pasture Watch - Source code of the global grassland class and extent maps at 30 m, [https://doi.org/10.5281/zenodo.13952867](https://doi.org/10.5281/zenodo.13952867) (2024).

82. Parente, L. _et al_. Global Pasture Watch - Grassland reference samples based on visual interpretation of VHR imagery (2000–2022), [https://doi.org/10.5281/zenodo.14035457](https://doi.org/10.5281/zenodo.14035457) (2024).

83. Parente, L. _et al_. Global Pasture Watch - Global machine learning model for prediction of cultivated and natural/semi-natural grassland, [https://doi.org/10.5281/zenodo.13952806](https://doi.org/10.5281/zenodo.13952806) (2024).

84. European Space Agency. Copernicus GLO-90 Digital Elevation Model, 10.5069/G9028PQB (2021).

85. Amatulli, G., McInerney, D., Sethi, T., Strobl, P. & Domisch, S. Geomorpho90m, empirical evaluation and accuracy assessment of global high-resolution geomorphometric layers. _Scientific Data_ **7**, 162, [https://doi.org/10.1038/s41597-020-0479-6](https://doi.org/10.1038/s41597-020-0479-6) (2020).

    [Article](https://doi.org/10.1038%2Fs41597-020-0479-6) [CAS](https://www.nature.com/articles/cas-redirect/1:CAS:528:DC%2BB3cXhtVyisbbM) [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=32467582) [PubMed Central](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC7256046) [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Geomorpho90m%2C%20empirical%20evaluation%20and%20accuracy%20assessment%20of%20global%20high-resolution%20geomorphometric%20layers&journal=Scientific%20Data&doi=10.1038%2Fs41597-020-0479-6&volume=7&publication_year=2020&author=Amatulli%2CG&author=McInerney%2CD&author=Sethi%2CT&author=Strobl%2CP&author=Domisch%2CS)

86. Didan, K. MODIS/Terra Vegetation Indices 16-Day L3 Global 250 m SIN Grid V061, [https://doi.org/10.5067/MODIS/MOD13Q1.061](https://doi.org/10.5067/MODIS/MOD13Q1.061) (2021).

87. Karger, D. N. _et al_. Climatologies at high resolution for the earth’s land surface areas. _Scientific data_ **4**, 1–20, [https://doi.org/10.1038/sdata.2017.122](https://doi.org/10.1038/sdata.2017.122) (2017).

    [Article](https://doi.org/10.1038%2Fsdata.2017.122) [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Climatologies%20at%20high%20resolution%20for%20the%20earth%E2%80%99s%20land%20surface%20areas&journal=Scientific%20data&doi=10.1038%2Fsdata.2017.122&volume=4&pages=1-20&publication_year=2017&author=Karger%2CDN)

88. Pekel, J.-F., Cottam, A., Gorelick, N. & Belward, A. S. High-resolution mapping of global surface water and its long-term changes. _Nature_ **540**, 418–422, [https://doi.org/10.1038/nature20584](https://doi.org/10.1038/nature20584) (2016).

    [Article](https://doi.org/10.1038%2Fnature20584) [ADS](http://adsabs.harvard.edu/cgi-bin/nph-data_query?link_type=ABSTRACT&bibcode=2016Natur.540..418P) [CAS](https://www.nature.com/articles/cas-redirect/1:CAS:528:DC%2BC28XitVWmurbJ) [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=27926733) [Google Scholar](http://scholar.google.com/scholar_lookup?&title=High-resolution%20mapping%20of%20global%20surface%20water%20and%20its%20long-term%20changes&journal=Nature&doi=10.1038%2Fnature20584&volume=540&pages=418-422&publication_year=2016&author=Pekel%2CJ-F&author=Cottam%2CA&author=Gorelick%2CN&author=Belward%2CAS)

89. Schneider, M., Schelte, T., Schmitz, F. & Körner, M. Eurocrops: The largest harmonized open crop dataset across the european union. _Scientific Data_ **10**, 612, [https://doi.org/10.1038/s41597-023-02517-0](https://doi.org/10.1038/s41597-023-02517-0) (2023).

    [Article](https://doi.org/10.1038%2Fs41597-023-02517-0) [PubMed](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&dopt=Abstract&list_uids=37696807) [PubMed Central](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC10495462) [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Eurocrops%3A%20The%20largest%20harmonized%20open%20crop%20dataset%20across%20the%20european%20union&journal=Scientific%20Data&doi=10.1038%2Fs41597-023-02517-0&volume=10&publication_year=2023&author=Schneider%2CM&author=Schelte%2CT&author=Schmitz%2CF&author=K%C3%B6rner%2CM)

90. Stehman, S. V., Pengra, B. W., Horton, J. A. & Wellington, D. F. Validation of the us geological survey’s land change monitoring, assessment and projection (lcmap) collection 1.0 annual land cover products 1985–2017. _Remote sensing of environment_ **265**, 112646, [https://doi.org/10.1016/j.rse.2021.112646](https://doi.org/10.1016/j.rse.2021.112646) (2021).

    [Article](https://doi.org/10.1016%2Fj.rse.2021.112646) [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Validation%20of%20the%20us%20geological%20survey%E2%80%99s%20land%20change%20monitoring%2C%20assessment%20and%20projection%20%28lcmap%29%20collection%201.0%20annual%20land%20cover%20products%201985%E2%80%932017&journal=Remote%20sensing%20of%20environment&doi=10.1016%2Fj.rse.2021.112646&volume=265&publication_year=2021&author=Stehman%2CSV&author=Pengra%2CBW&author=Horton%2CJA&author=Wellington%2CDF)

91. Buchhorn, M. _et al_. Copernicus global land cover layers–collection 2. _Remote Sensing_ **12**, 1044 (2020).

    [Article](https://doi.org/10.3390%2Frs12061044) [ADS](http://adsabs.harvard.edu/cgi-bin/nph-data_query?link_type=ABSTRACT&bibcode=2020RemS...12.1044B) [Google Scholar](http://scholar.google.com/scholar_lookup?&title=Copernicus%20global%20land%20cover%20layers%E2%80%93collection%202&journal=Remote%20Sensing&doi=10.3390%2Frs12061044&volume=12&publication_year=2020&author=Buchhorn%2CM)


[Download references](https://citation-needed.springer.com/v2/references/10.1038/s41597-024-04139-6?format=refman&flavour=references)

## Acknowledgements

This research was supported by a grant to the Land & Carbon Lab from the Bezos Earth Fund and by the Open-Earth-Monitor Cyberinfrastructure project, which received funding from the European Union’s Horizon Europe research and innovation program under grant agreement No. 101059548. CM acknowledges support through the Senior Scientist program of iDiv, funded by the German Research Foundation (DFG–FZT 118, 202548816). The authors are grateful to Dr. Peter Potapov from the Global Land Analysis and Discovery (GLAD) laboratory at the University of Maryland, and the whole GLAD team for providing assistance with the Landsat ARD-2 product.

## Author information

### Authors and Affiliations

1. OpenGeoHub Foundation, Doorwerth, The Netherlands

Leandro Parente, Davide Consoli, Tomislav Hengl, Carmelo Bonannella, Ichsani Wheeler, Murat Şahin & Martijn Witjes

2. Land & Carbon Lab, World Resources Institute, Washington, DC, USA

Lindsey Sloat, Radost Stanimirova & Fred Stolle

3. Remote Sensing and GIS Laboratory (LAPIG/UFG), Goiânia, Brazil

Vinicius Mesquita, Nathália Teles, Maria Hunter, Laerte Ferreira, Ana Paula Mattos & Bernard Oliveira

4. Laboratory of Geo-Information Science and Remote Sensing, Wageningen University & Research, Wageningen, The Netherlands

Carmelo Bonannella & Martijn Witjes

5. International Institute for Applied Systems Analysis (IIASA), Laxenburg, Austria

Steffen Ehrmann, Steffen Fritz & Ziga Malek

6. German Centre for Integrative Biodiversity Research (iDiv) Halle-Jena-Leipzig, Leipzig, Germany

Steffen Ehrmann & Carsten Meyer

7. Institute of Biology, Leipzig University, Leipzig, Germany

Steffen Ehrmann & Carsten Meyer

8. Institute of Geosciences and Geography, Martin Luther University Halle-Wittenberg, Halle, Saale, Germany

Carsten Meyer


Authors

01. Leandro Parente


    [View author publications](https://www.nature.com/search?author=Leandro%20Parente)





    Search author on:[PubMed](https://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=search&term=Leandro%20Parente) [Google Scholar](https://scholar.google.co.uk/scholar?as_q=&num=10&btnG=Search+Scholar&as_epq=&as_oq=&as_eq=&as_occt=any&as_sauthors=%22Leandro%20Parente%22&as_publication=&as_ylo=&as_yhi=&as_allsubj=all&hl=en)

02. Lindsey Sloat


    [View author publications](https://www.nature.com/search?author=Lindsey%20Sloat)





    Search author on:[PubMed](https://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=search&term=Lindsey%20Sloat) [Google Scholar](https://scholar.google.co.uk/scholar?as_q=&num=10&btnG=Search+Scholar&as_epq=&as_oq=&as_eq=&as_occt=any&as_sauthors=%22Lindsey%20Sloat%22&as_publication=&as_ylo=&as_yhi=&as_allsubj=all&hl=en)

03. Vinicius Mesquita


    [View author publications](https://www.nature.com/search?author=Vinicius%20Mesquita)





    Search author on:[PubMed](https://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=search&term=Vinicius%20Mesquita) [Google Scholar](https://scholar.google.co.uk/scholar?as_q=&num=10&btnG=Search+Scholar&as_epq=&as_oq=&as_eq=&as_occt=any&as_sauthors=%22Vinicius%20Mesquita%22&as_publication=&as_ylo=&as_yhi=&as_allsubj=all&hl=en)

04. Davide Consoli


    [View author publications](https://www.nature.com/search?author=Davide%20Consoli)





    Search author on:[PubMed](https://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=search&term=Davide%20Consoli) [Google Scholar](https://scholar.google.co.uk/scholar?as_q=&num=10&btnG=Search+Scholar&as_epq=&as_oq=&as_eq=&as_occt=any&as_sauthors=%22Davide%20Consoli%22&as_publication=&as_ylo=&as_yhi=&as_allsubj=all&hl=en)

05. Radost Stanimirova


    [View author publications](https://www.nature.com/search?author=Radost%20Stanimirova)





    Search author on:[PubMed](https://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=search&term=Radost%20Stanimirova) [Google Scholar](https://scholar.google.co.uk/scholar?as_q=&num=10&btnG=Search+Scholar&as_epq=&as_oq=&as_eq=&as_occt=any&as_sauthors=%22Radost%20Stanimirova%22&as_publication=&as_ylo=&as_yhi=&as_allsubj=all&hl=en)

06. Tomislav Hengl


    [View author publications](https://www.nature.com/search?author=Tomislav%20Hengl)





    Search author on:[PubMed](https://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=search&term=Tomislav%20Hengl) [Google Scholar](https://scholar.google.co.uk/scholar?as_q=&num=10&btnG=Search+Scholar&as_epq=&as_oq=&as_eq=&as_occt=any&as_sauthors=%22Tomislav%20Hengl%22&as_publication=&as_ylo=&as_yhi=&as_allsubj=all&hl=en)

07. Carmelo Bonannella


    [View author publications](https://www.nature.com/search?author=Carmelo%20Bonannella)





    Search author on:[PubMed](https://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=search&term=Carmelo%20Bonannella) [Google Scholar](https://scholar.google.co.uk/scholar?as_q=&num=10&btnG=Search+Scholar&as_epq=&as_oq=&as_eq=&as_occt=any&as_sauthors=%22Carmelo%20Bonannella%22&as_publication=&as_ylo=&as_yhi=&as_allsubj=all&hl=en)

08. Nathália Teles


    [View author publications](https://www.nature.com/search?author=Nath%C3%A1lia%20Teles)





    Search author on:[PubMed](https://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=search&term=Nath%C3%A1lia%20Teles) [Google Scholar](https://scholar.google.co.uk/scholar?as_q=&num=10&btnG=Search+Scholar&as_epq=&as_oq=&as_eq=&as_occt=any&as_sauthors=%22Nath%C3%A1lia%20Teles%22&as_publication=&as_ylo=&as_yhi=&as_allsubj=all&hl=en)

09. Ichsani Wheeler


    [View author publications](https://www.nature.com/search?author=Ichsani%20Wheeler)





    Search author on:[PubMed](https://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=search&term=Ichsani%20Wheeler) [Google Scholar](https://scholar.google.co.uk/scholar?as_q=&num=10&btnG=Search+Scholar&as_epq=&as_oq=&as_eq=&as_occt=any&as_sauthors=%22Ichsani%20Wheeler%22&as_publication=&as_ylo=&as_yhi=&as_allsubj=all&hl=en)

10. Maria Hunter


    [View author publications](https://www.nature.com/search?author=Maria%20Hunter)





    Search author on:[PubMed](https://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=search&term=Maria%20Hunter) [Google Scholar](https://scholar.google.co.uk/scholar?as_q=&num=10&btnG=Search+Scholar&as_epq=&as_oq=&as_eq=&as_occt=any&as_sauthors=%22Maria%20Hunter%22&as_publication=&as_ylo=&as_yhi=&as_allsubj=all&hl=en)

11. Steffen Ehrmann


    [View author publications](https://www.nature.com/search?author=Steffen%20Ehrmann)





    Search author on:[PubMed](https://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=search&term=Steffen%20Ehrmann) [Google Scholar](https://scholar.google.co.uk/scholar?as_q=&num=10&btnG=Search+Scholar&as_epq=&as_oq=&as_eq=&as_occt=any&as_sauthors=%22Steffen%20Ehrmann%22&as_publication=&as_ylo=&as_yhi=&as_allsubj=all&hl=en)

12. Laerte Ferreira


    [View author publications](https://www.nature.com/search?author=Laerte%20Ferreira)





    Search author on:[PubMed](https://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=search&term=Laerte%20Ferreira) [Google Scholar](https://scholar.google.co.uk/scholar?as_q=&num=10&btnG=Search+Scholar&as_epq=&as_oq=&as_eq=&as_occt=any&as_sauthors=%22Laerte%20Ferreira%22&as_publication=&as_ylo=&as_yhi=&as_allsubj=all&hl=en)

13. Ana Paula Mattos


    [View author publications](https://www.nature.com/search?author=Ana%20Paula%20Mattos)





    Search author on:[PubMed](https://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=search&term=Ana%20Paula%20Mattos) [Google Scholar](https://scholar.google.co.uk/scholar?as_q=&num=10&btnG=Search+Scholar&as_epq=&as_oq=&as_eq=&as_occt=any&as_sauthors=%22Ana%20Paula%20Mattos%22&as_publication=&as_ylo=&as_yhi=&as_allsubj=all&hl=en)

14. Bernard Oliveira


    [View author publications](https://www.nature.com/search?author=Bernard%20Oliveira)





    Search author on:[PubMed](https://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=search&term=Bernard%20Oliveira) [Google Scholar](https://scholar.google.co.uk/scholar?as_q=&num=10&btnG=Search+Scholar&as_epq=&as_oq=&as_eq=&as_occt=any&as_sauthors=%22Bernard%20Oliveira%22&as_publication=&as_ylo=&as_yhi=&as_allsubj=all&hl=en)

15. Carsten Meyer


    [View author publications](https://www.nature.com/search?author=Carsten%20Meyer)





    Search author on:[PubMed](https://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=search&term=Carsten%20Meyer) [Google Scholar](https://scholar.google.co.uk/scholar?as_q=&num=10&btnG=Search+Scholar&as_epq=&as_oq=&as_eq=&as_occt=any&as_sauthors=%22Carsten%20Meyer%22&as_publication=&as_ylo=&as_yhi=&as_allsubj=all&hl=en)

16. Murat Şahin


    [View author publications](https://www.nature.com/search?author=Murat%20%C5%9Eahin)





    Search author on:[PubMed](https://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=search&term=Murat%20%C5%9Eahin) [Google Scholar](https://scholar.google.co.uk/scholar?as_q=&num=10&btnG=Search+Scholar&as_epq=&as_oq=&as_eq=&as_occt=any&as_sauthors=%22Murat%20%C5%9Eahin%22&as_publication=&as_ylo=&as_yhi=&as_allsubj=all&hl=en)

17. Martijn Witjes


    [View author publications](https://www.nature.com/search?author=Martijn%20Witjes)





    Search author on:[PubMed](https://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=search&term=Martijn%20Witjes) [Google Scholar](https://scholar.google.co.uk/scholar?as_q=&num=10&btnG=Search+Scholar&as_epq=&as_oq=&as_eq=&as_occt=any&as_sauthors=%22Martijn%20Witjes%22&as_publication=&as_ylo=&as_yhi=&as_allsubj=all&hl=en)

18. Steffen Fritz


    [View author publications](https://www.nature.com/search?author=Steffen%20Fritz)





    Search author on:[PubMed](https://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=search&term=Steffen%20Fritz) [Google Scholar](https://scholar.google.co.uk/scholar?as_q=&num=10&btnG=Search+Scholar&as_epq=&as_oq=&as_eq=&as_occt=any&as_sauthors=%22Steffen%20Fritz%22&as_publication=&as_ylo=&as_yhi=&as_allsubj=all&hl=en)

19. Ziga Malek


    [View author publications](https://www.nature.com/search?author=Ziga%20Malek)





    Search author on:[PubMed](https://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=search&term=Ziga%20Malek) [Google Scholar](https://scholar.google.co.uk/scholar?as_q=&num=10&btnG=Search+Scholar&as_epq=&as_oq=&as_eq=&as_occt=any&as_sauthors=%22Ziga%20Malek%22&as_publication=&as_ylo=&as_yhi=&as_allsubj=all&hl=en)

20. Fred Stolle


    [View author publications](https://www.nature.com/search?author=Fred%20Stolle)





    Search author on:[PubMed](https://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=search&term=Fred%20Stolle) [Google Scholar](https://scholar.google.co.uk/scholar?as_q=&num=10&btnG=Search+Scholar&as_epq=&as_oq=&as_eq=&as_occt=any&as_sauthors=%22Fred%20Stolle%22&as_publication=&as_ylo=&as_yhi=&as_allsubj=all&hl=en)


### Contributions

L.P. was the primary author and together with L.S., T.H., I.W., L.F., S.F., F.S. conceived, designed and coordinated the implementation of the mapping framework. L.P., D.C. implemented the EO data pre-processing, model training, predictive modeling and data publication. V.M., N.T., M.H., L.F., A.P.M., B.O. performed the reference data collection and the harmonization of existing reference samples. L.P., L.S., R.S., M.S., S.E., C.M. performed visual assessment and technical validation of the results. L.P., T.H., M.S. prepared data visualization. L.P., L.S., R.S., T.H., C.B., N.T., I.W., M.H., S.F., C.M., M.W., S.E., Z.M. contributed with writing. All authors reviewed the manuscript.

### Corresponding author

Correspondence to
[Leandro Parente](mailto:leandro.parente@opengeohub.org).

## Ethics declarations

### Competing interests

The authors declare no competing interests.

## Additional information

**Publisher’s note** Springer Nature remains neutral with regard to jurisdictional claims in published maps and institutional affiliations.

## Supplementary information

### [Supplementary information (download PDF )](https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41597-024-04139-6/MediaObjects/41597_2024_4139_MOESM1_ESM.pdf)

## Rights and permissions

**Open Access** This article is licensed under a Creative Commons Attribution 4.0 International License, which permits use, sharing, adaptation, distribution and reproduction in any medium or format, as long as you give appropriate credit to the original author(s) and the source, provide a link to the Creative Commons licence, and indicate if changes were made. The images or other third party material in this article are included in the article’s Creative Commons licence, unless indicated otherwise in a credit line to the material. If material is not included in the article’s Creative Commons licence and your intended use is not permitted by statutory regulation or exceeds the permitted use, you will need to obtain permission directly from the copyright holder. To view a copy of this licence, visit [http://creativecommons.org/licenses/by/4.0/](http://creativecommons.org/licenses/by/4.0/).

[Reprints and permissions](https://s100.copyright.com/AppDispatchServlet?title=Annual%2030-m%20maps%20of%20global%20grassland%20class%20and%20extent%20%282000%E2%80%932022%29%20based%20on%20spatiotemporal%20Machine%20Learning&author=Leandro%20Parente%20et%20al&contentID=10.1038%2Fs41597-024-04139-6&copyright=The%20Author%28s%29&publication=2052-4463&publicationDate=2024-12-11&publisherName=SpringerNature&orderBeanReset=true&oa=CC%20BY)

## About this article

[![Check for updates. Verify currency and authenticity via CrossMark](<Base64-Image-Removed>)](https://crossmark.crossref.org/dialog/?doi=10.1038/s41597-024-04139-6)

### Cite this article

Parente, L., Sloat, L., Mesquita, V. _et al._ Annual 30-m maps of global grassland class and extent (2000–2022) based on spatiotemporal Machine Learning.
_Sci Data_ **11**, 1303 (2024). https://doi.org/10.1038/s41597-024-04139-6

[Download citation](https://citation-needed.springer.com/v2/references/10.1038/s41597-024-04139-6?format=refman&flavour=citation)

- Received: 31 May 2024

- Accepted: 14 November 2024

- Published: 11 December 2024

- Version of record: 11 December 2024

- DOI: https://doi.org/10.1038/s41597-024-04139-6


### Share this article

Anyone you share the following link with will be able to read this content:

Get shareable link

Sorry, a shareable link is not currently available for this article.

Copy shareable link to clipboard

Provided by the Springer Nature SharedIt content-sharing initiative


Close bannerClose

![Nature Briefing Anthropocene](https://www.nature.com/static/images/logos/nature-briefing-anthropocene-logo-55353f564d.svg)

Sign up for the _Nature Briefing: Anthropocene_ newsletter — what matters in anthropocene research, free to your inbox weekly.

Email address

Sign up

I agree my information will be processed in accordance with the _Nature_ and Springer Nature Limited [Privacy Policy](https://www.nature.com/info/privacy).

Close bannerClose

Get the most important science stories of the day, free in your inbox. [Sign up for Nature Briefing: Anthropocene](https://www.nature.com/briefing/anthropocene/?brieferEntryPoint=AnthropoceneBriefingBanner)