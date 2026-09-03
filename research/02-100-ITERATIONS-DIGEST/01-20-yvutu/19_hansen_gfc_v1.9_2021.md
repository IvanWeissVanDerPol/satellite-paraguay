![](https://storage.googleapis.com/earthenginepartners-hansen/GFC-2021-v1.9/downloadPage_files/banner.jpg)![University of Maryland](https://storage.googleapis.com/earthenginepartners-hansen/GFC-2021-v1.9/downloadPage_files/umd-logo.jpg)

# Global Forest Change 2000–2021  Data Download

Results from time-series analysis of Landsat images in characterizing global forest extent and change from 2000 through 2021. For additional information about these results, please see the [associated journal article](http://www.sciencemag.org/content/342/6160/850) (Hansen et al., _Science_ 2013).

Web-based visualizations of these results are also available at our main site:

> **[https://glad.earthengine.app/view/global-forest-change](https://glad.earthengine.app/view/global-forest-change)**

Please use that URL when linking to this dataset.

We anticipate releasing updated versions of this dataset. To keep up to date with the latest updates, and to help us better understand how these data are used, please **[register as a user](https://docs.google.com/a/google.com/forms/d/1AkAUb4kfF7pUTOADPGEW7Do2oRhdDUPYb2mzIr8OIx4/viewform)**. Thanks!

## Usage Notes

The [Global Land Analysis and Discovery (GLAD)](https://glad.umd.edu/) laboratory at the University of Maryland, in partnership with [Global Forest Watch (GFW)](https://www.globalforestwatch.org/), provides annually updated global-scale forest loss data, derived using Landsat time-series imagery. These data, available here, are a relative indicator of spatiotemporal trends in forest loss dynamics globally. However, inconsistencies exist due to the following factors:

1. Differences in Landsat sensor technology, whether Thematic Mapper, Enhanced Thematic Mapper Plus, or Operational Land Image data. For example, the Operational Land Imager (2013-onward) onboard the Landsat 8 spacecraft employs a pushbroom sensor technology that increases per observation dwell time compared to past whiskbroom systems. The result is a signal to noise ratio that is a magnitude greater than that of Landsat 7's Enhanced Thematic Mapper Plus sensor. The increased signal enables better detection capabilities in mapping land change.
2. Data richness, or the number of viable land observations available as inputs to analysis. The global acquisition strategy has improved over time, with acquisitions increasing from under 150k per year in the early 2000s to over 250k per year in recent years. Additionally, Landsat 7 was the only input for the 2001-2012 initial product, and is affected by the scan-line corrector malfunction of the Enhanced Thematic Mapper from 2002 onward, where nearly a quarter of the footprint of each scene is not collected. Also, the gap between the decommissioning of Landsat 5 in 2011 and the launch of Landsat 8 in 2013 resulted in a total 2012 global collection of less than 100k Landsat 7 images.
3. Algorithm adjustments, including modifications of training data and input image feature space. For example, the original 2001-2012 forest loss map was made using a single algorithm run, compared to subsequent years that have been added individually. Additionally, models have been iterated to improve performance in the 2012-forward period. Such changes in the mapping method can result in year to year inconsistencies.

While the resulting map data are a largely viable relative indicator of trends, care must be taken when comparing change across any interval. Applying a temporal filter, for example a 3-year moving average, is often useful in discerning trends. However, definitive area estimation should not be made using pixels counts from the forest loss layers.

The Intergovernmental Panel on Climate Change (IPCC) provides guidance on reporting areal extent and change of land cover and land use, requiring the use of estimators that neither over or underestimate dynamics to the degree possible, and that have known uncertainties. The maps provided by GLAD do not have these properties. However, the maps can be leveraged to facilitate appropriate probability-based statistical methods in deriving statistically valid areas of forest extent and change. Specifically, the maps may be used as a stratifier in targeting forest extent and/or change by a probability sample. The team at GLAD has demonstrated such approaches using the GLAD forest loss data in sample-based area estimation (Tyukavina et al., ERL, 2018, Turubanova et al., ERL, 2019, and Potapov et al., RSE, 2019, among others).

## User Notes for Version 1.9 Update

This update of gross forest cover loss includes new 2021 loss-year and multispectral imagery layers. Relative to the version 1.0 product our method has been modified in numerous ways, and the new update should be seen as part of a transition to a future version 2.0 that is more consistent over the entire 2000-onward period. Key changes include:

1. The use of Landsat 8 OLI data for 2013 onward,
2. The reprocessing of data from 2011 onward in measuring loss,
3. Improved training data for calibrating the loss model,
4. Improved per sensor quality assessment models to filter input data, and
5. Improved input spectral features for building and applying the loss model.

These changes lead to a different and improved detection of global forest loss. However, the years preceding 2011 have not yet been reprocessed in this manner, and users will notice inconsistencies as a result. It must also be noted that a full validation of the results incorporating Landsat 8 has not been undertaken. Such an analysis may reveal a more sensitive ability to detect and map forest disturbance with Landsat 8 data. If this is the case then there will be a more fundamental limitation to the consistency of the mapped interannual loss before and after the inclusion of Landsat 8 data, and a validation of Landsat 8-incorporated loss detection is planned. The integrated use of version 1.0 2000–2012 data and updated version 1.9 2011–2021 data should be performed with caution.

Some examples of improved change detection in the 2011–2021 update include the following:

1. Improved detection of boreal forest loss due to fire.
2. Improved detection of smallholder rotation agricultural clearing in dry and humid tropical forests.
3. Improved detection of selective logging.
4. Improved detection of the clearing of short cycle plantations in sub-tropical and tropical ecozones.

These are examples of dynamics that may be differentially mapped over the 2001-2021 period in Version 1.9. A version 2.0 reprocessing of the 2000-onward record is planned, but no delivery date is yet confirmed.

The original version 1.0 data is also still available for download [here](https://storage.googleapis.com/earthenginepartners-hansen/GFC-2021-v1.9/download_v1.0.html).

In addition, to reduce confusion, beginning with version 1.4 we are no longer releasing `loss` as a separate layer from `lossyear`. Loss as previously releaed corresponds to nonzero values of loss year.

## License and Attribution

[![Creative Commons License](https://storage.googleapis.com/earthenginepartners-hansen/GFC-2021-v1.9/downloadPage_files/88x31.png)](http://creativecommons.org/licenses/by/4.0/) This work is licensed under a [Creative Commons Attribution 4.0 International License](http://creativecommons.org/licenses/by/4.0/). You are free to copy and redistribute the material in any medium or format, and to transform and build upon the material for any purpose, even commercially. You must give appropriate credit, provide a link to the license, and indicate if changes were made.

Use the following credit when these data are displayed:

> **Source: Hansen/UMD/Google/USGS/NASA**

Use the following credit when these data are cited:

> Hansen, M. C., P. V. Potapov, R. Moore, M. Hancher, S. A. Turubanova, A.
> Tyukavina, D. Thau, S. V. Stehman, S. J. Goetz, T. R. Loveland, A. Kommareddy, A.
> Egorov, L. Chini, C. O. Justice, and J. R. G. Townshend. 2013. “High-Resolution
> Global Maps of 21st-Century Forest Cover Change.” Science 342 (15 November):
> 850–53. Data available on-line from:
> [https://glad.earthengine.app/view/global-forest-change](https://glad.earthengine.app/view/global-forest-change).

## Dataset Details

This global dataset is divided into 10x10 degree tiles, consisting of seven files per tile. All files contain unsigned 8-bit values and have a spatial resolution of 1 arc-second per pixel, or approximately 30 meters per pixel at the equator. Only `lossyear` and `last` are updated annualy.

Tree canopy cover for year 2000 (`treecover2000`)Tree cover in the year 2000, defined as canopy closure for all vegetation taller than 5m in height. Encoded as a percentage per output grid cell, in the range 0–100.Global forest cover gain 2000–2012 (`gain`)Forest gain during the period 2000–2012, defined as the inverse of loss, or a non-forest to forest change entirely within the study period. Encoded as either 1 (gain) or 0 (no gain).Year of gross forest cover loss event (`lossyear`)Forest loss during the period 2000–2021, defined as a stand-replacement disturbance, or a change from a forest to non-forest state. Encoded as either 0 (no loss) or else a value in the range 1–20, representing loss detected primarily in the year 2001–2021, respectively.Data mask (`datamask`)Three values representing areas of no data (0), mapped land surface (1), and persistent water bodies (2) based on 2000-2012.Circa year 2000 Landsat 7 cloud-free image composite (`first`)Reference multispectral imagery from the first available year, typically 2000. If no cloud-free observations were available for year 2000, imagery was taken from the closest year with cloud-free data, within the range 1999–2012.Circa year 2021 Landsat cloud-free image composite (`last`)Reference multispectral imagery from the last available year, typically 2021. If no cloud-free observations were available for year 2021, imagery was taken from the closest year with cloud-free data.

Reference composite imagery are median observations from a set of quality assessed growing season observations in four spectral bands, specifically Landsat bands 3, 4, 5, and 7. Normalized top-of-atmosphere (TOA) reflectance values ( _ρ_) have been scaled to an 8-bit data range using a scale factor ( _g_):

DN = ρ · _g_ \+ 1

The _g_ factor was chosen independently for each band to preserve the band-specific dynamic range, as shown in the following table:

| Landsat Band | _g_ |
| --- | --- |
| Red (0.66 micrometers) | 508 |
| NIR (0.86 micrometers) | 254 |
| SWIR1 (1.6 micrometers) | 363 |
| SWIR2 (2.2 micrometers) | 423 |

## Download Instructions

To download individual 10x10 degree granules, click on a region on the map below and then click on the URLs underneath it.

![](https://storage.googleapis.com/earthenginepartners-hansen/GFC-2021-v1.9/downloadPage_files/loss_tree_gain.jpg)

Granule with top-left corner at 40N, 80W:

[https://storage.googleapis.com/earthenginepartners-hansen/GFC-2021-v1.9/Hansen\_GFC-2021-v1.9\_treecover2000\_40N\_080W.tif](https://storage.googleapis.com/earthenginepartners-hansen/GFC-2021-v1.9/Hansen_GFC-2021-v1.9_treecover2000_40N_080W.tif)

[https://storage.googleapis.com/earthenginepartners-hansen/GFC-2021-v1.9/Hansen\_GFC-2021-v1.9\_gain\_40N\_080W.tif](https://storage.googleapis.com/earthenginepartners-hansen/GFC-2021-v1.9/Hansen_GFC-2021-v1.9_gain_40N_080W.tif)

[https://storage.googleapis.com/earthenginepartners-hansen/GFC-2021-v1.9/Hansen\_GFC-2021-v1.9\_lossyear\_40N\_080W.tif](https://storage.googleapis.com/earthenginepartners-hansen/GFC-2021-v1.9/Hansen_GFC-2021-v1.9_lossyear_40N_080W.tif)

[https://storage.googleapis.com/earthenginepartners-hansen/GFC-2021-v1.9/Hansen\_GFC-2021-v1.9\_datamask\_40N\_080W.tif](https://storage.googleapis.com/earthenginepartners-hansen/GFC-2021-v1.9/Hansen_GFC-2021-v1.9_datamask_40N_080W.tif)

[https://storage.googleapis.com/earthenginepartners-hansen/GFC-2021-v1.9/Hansen\_GFC-2021-v1.9\_first\_40N\_080W.tif](https://storage.googleapis.com/earthenginepartners-hansen/GFC-2021-v1.9/Hansen_GFC-2021-v1.9_first_40N_080W.tif)

[https://storage.googleapis.com/earthenginepartners-hansen/GFC-2021-v1.9/Hansen\_GFC-2021-v1.9\_last\_40N\_080W.tif](https://storage.googleapis.com/earthenginepartners-hansen/GFC-2021-v1.9/Hansen_GFC-2021-v1.9_last_40N_080W.tif)

We have provided a complete set of granules spanning the range 180W–180E and 80N–60S, but the granules over the ocean are provided for completeness only and do not contain any meaningful data. Should you wish to download a complete layer, you may download a text file containing the complete list of URLs for each layer:
[`treecover2000`](https://storage.googleapis.com/earthenginepartners-hansen/GFC-2021-v1.9/treecover2000.txt),
[`gain`](https://storage.googleapis.com/earthenginepartners-hansen/GFC-2021-v1.9/gain.txt),
[`lossyear`](https://storage.googleapis.com/earthenginepartners-hansen/GFC-2021-v1.9/lossyear.txt),
[`datamask`](https://storage.googleapis.com/earthenginepartners-hansen/GFC-2021-v1.9/datamask.txt),
[`first`](https://storage.googleapis.com/earthenginepartners-hansen/GFC-2021-v1.9/first.txt), or
[`last`](https://storage.googleapis.com/earthenginepartners-hansen/GFC-2021-v1.9/last.txt).

Note that the `loss`, `gain`, `lossyear`, and `datamask` layers compress extremely well (totalling less than 10GB each globally), and the `treecover2000` layer compresses fairly well (less than 50GB), but the `first` and `last` multispectral layers are much larger (totalling over 600GB each). You may wish to take this into account when selecting which layers to download in their entirety.

## Analyzing the Results in Earth Engine

You can also analyze these results directly in [Google Earth Engine](http://earthengine.google.com/) using the asset ID `UMD/hansen/global_forest_change_2021_v1_9`. If you are not yet an Earth Engine user, you may [sign up here](http://signup.earthengine.google.org/). To help you get started we have made an [introductory tutorial](https://developers.google.com/earth-engine/tutorials/tutorial_forest_01) showing examples of how to use this data to do a variety of things, including generating indices from annual Landsat composites and computing tree loss per year for regions of interest.