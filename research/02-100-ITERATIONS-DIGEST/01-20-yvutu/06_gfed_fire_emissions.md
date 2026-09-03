- [Home](https://www.globalfiredata.org/)
- [Data](https://www.globalfiredata.org/data.html)
- [Related datasets](https://www.globalfiredata.org/related.html)
- [About](https://www.globalfiredata.org/about.html)
- [FAQ](https://www.globalfiredata.org/faq.html)

## Global Fire Emissions Database (GFED)

Fires are an important source of atmospheric trace gases and aerosols and they are the most important disturbance agent on a global scale. In addition, deforestation and tropical peatland fires and areas that see an increase in the frequency of fires add to the build-up of atmospheric CO2.

We have combined satellite information on fire activity and vegetation productivity to estimate gridded monthly burned area and fire emissions, as well as scalars that can be used to calculate higher temporal resolution emissions. The resulting datasets are downloadable from this website for use in large-scale atmospheric and biogeochemical studies. The core datasets are:

- **Burned area** for all vegetation types except croplands from [Chen et al. (2023)](https://essd.copernicus.org/articles/15/5227/2023/essd-15-5227-2023.html). This burned area dataset builds on the MODIS MCD64A1 Collection 6 burned area from [Giglio et al. (2018)](https://www.sciencedirect.com/science/article/pii/S0034425718303705) but accounts for errors of commission and omission. Cropland burned area is taken from the GloCAB dataset from [Hall et al. (2023)](https://essd.copernicus.org/articles/16/867/2024/essd-16-867-2024.html).
- **Fuel consumption** (emissions per square meter burned) based on [Van Wees et al. (2022)](https://gmd.copernicus.org/articles/15/8411/2022/).
- The resulting carbon losses are converted to trace gas and aerosol emissions using **emission factors**. For savannas (and only CO2, CO, CH4, N2O) these are based on [Vernooij et al. (2023)](https://esd.copernicus.org/articles/14/1039/2023/), for other biomes as well as for other species in savannas NEIVA (Next-generation Emissions InVentory Expansion of Akagi) is used, please see [Binte Shahid et al. (2024)](https://gmd.copernicus.org/articles/17/7679/2024/). For the Boreal region and for CO and CH4 this dataset has been expanded with the tower-based study by [Wiggins et al. (2021)](https://acp.copernicus.org/articles/21/8557/2021/)
- **Emissions** of carbon, trace gases, and aerosols are then the multiplication of these three layers and described in [Van der Werf et al. (2025)](https://www.nature.com/articles/s41597-025-06127-w)

The current version is 5 which has a spatial resolution of 0.25 degrees for the 2001 onwards period. Data for the 1997-2000 period has a spatial resolution of 1.00 degree reflecting larger uncertainties. Post 2022 emissions are based on VIIRS active fire data, using relations between VIIRS active fire data and burned area and emissions for the overlapping period. Data for this 2023 onwards period is still a Beta version and subject to change until the accompanying paper is accepted.

![](https://www.globalfiredata.org/_plots/UCI.png)![](https://www.globalfiredata.org/_plots/WUR.png)![](https://www.globalfiredata.org/_plots/UMD.png)![](https://www.globalfiredata.org/_plots/NASA.jpg)