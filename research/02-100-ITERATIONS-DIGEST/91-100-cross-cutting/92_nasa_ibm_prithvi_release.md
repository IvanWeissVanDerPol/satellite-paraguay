[Skip to main content](https://www.earthdata.nasa.gov/news/nasa-ibm-openly-release-geospatial-ai-foundation-model-nasa-earth-observation-data#main-content)

Delivery of Suomi National Polar-orbiting Partnership (Suomi NPP) satellite data products will cease on November 1, 2026. Data users should transition now to alternative products from NOAA-21 and NOAA-20. [Suomi NPP data announcement](https://www.earthdata.nasa.gov/data/alerts-outages/suomi-npp-data-product-delivery-cease-november-1-2026)

# NASA and IBM Openly Release Geospatial AI Foundation Model for NASA Earth Observation Data

Based on NASA's Harmonized Landsat Sentinel-2 (HLS) data, the artificial intelligence (AI) foundation model is a milestone in the application of AI for Earth science.

6 MIN READ



Josh Blumenfeld

Aug. 3, 2023

News

[X](https://www.earthdata.nasa.gov/#x) [Facebook](https://www.earthdata.nasa.gov/#facebook) [LinkedIn](https://www.earthdata.nasa.gov/#linkedin)

Image

[![brown desert with greenish line indicating water through center of image; circular plantings in upper left next to water](https://earthdata.nasa.gov/s3fs-public/styles/hds_large/public/2023-07/nasa-ibm_fields-in-egypt_500x500_news.jpeg?VersionId=54EuWF_Qa4pj_Q0IeBj7nVScEft.ePbv&itok=WXu9HZp5)](https://earthdata.nasa.gov/s3fs-public/2023-07/nasa-ibm_fields-in-egypt_500x500_news.jpeg?VersionId=yd8e9Rl8QMleceKPXGe6ZVMjiEQXhzpI "")

Image Caption

Foundation models were applied to HLS imagery, such as this true color composite image of irrigated agricultural fields near Sadat City, about 80 km northwest of Cairo, Egypt. Credit: HLS/NASA IMPACT.

A public/private partnership involving NASA and IBM Research has led to the release of NASA's first open-source geospatial artificial intelligence (AI) foundation model for Earth observation data. Built using NASA's Harmonized Landsat and Sentinel-2 ( [HLS](https://www.earthdata.nasa.gov/esds/harmonized-landsat-sentinel-2)) dataset, the release of the HLS Geospatial Foundation Model (HLS Geospatial FM) is a milestone in the application of AI for Earth science. The model has a wide range of potential applications, including tracking changes in land use, monitoring natural disasters, and predicting crop yields. The HLS Geospatial FM is available at [Hugging Face](https://huggingface.co/ibm-nasa-geospatial "(opens in a new window)")(link is external), a public repository for open-source machine learning models.

NASA's Interagency Implementation and Advanced Concepts Team ( [IMPACT](https://www.earthdata.nasa.gov/esds/impact)) played a major role in this work. Located at NASA's Marshall Space Flight Center in Huntsville, Alabama, IMPACT is a component of NASA's Earth Science Data Systems ( [ESDS](https://www.earthdata.nasa.gov/esds)) Program and is charged with expanding the use of NASA Earth observation data through innovation, partnerships, and technology, including the application of AI to these data.

"AI foundation models for Earth observations present enormous potential to address intricate scientific problems and expedite the broader deployment of AI across diverse applications,” says Dr. Rahul Ramachandran, IMPACT manager and a senior research scientist at Marshall. “We call on the Earth science and applications communities to evaluate this initial HLS foundation model for a variety of uses and share feedback on its merits and drawbacks."

Along with NASA and IBM Research, this collaborative effort included Clark University's Center for Geospatial Analytics, ESA (European Space Agency), USGS, and the U.S. Department of Energy's Oak Ridge National Laboratory. This work is part of NASA's Open-Source Science Initiative ( [OSSI](https://science.nasa.gov/open-science-overview)), a commitment to building an inclusive, transparent, and collaborative open science community over the next decade. Development of the HLS Geospatial FM began in January 2023, and the FM was released in July 2023.

## The Significance of Foundation Models

[Foundation models](https://research.ibm.com/blog/what-are-foundation-models "(opens in a new window)")(link is external) (FMs) are types of AI models trained on a broad set of unlabeled data. They can be used for different tasks and can apply information about one situation to another. The goal of the NASA/IBM work is to provide an easier way for researchers to analyze and draw insights from large NASA datasets related to Earth processes.

"We believe that foundation models have the potential to change the way observational data are analyzed and help us to better understand our planet," says NASA Chief Science Data Officer Kevin Murphy. "And by open-sourcing such models and making them available to the world, we hope to multiply their impact."

AI FMs have the potential to play a pivotal role in understanding our planet's interconnected processes and the climate effects of ongoing natural and human-caused changes. FMs that are pretrained on Earth observation data can accelerate the analysis of tremendous amounts of data in two primary ways.

First, FMs do not need large training datasets, which can be laborious and resource-intensive to create. The ability to train FMs on much smaller datasets can save time and money. Second, FMs can reduce redundant efforts to build downstream applications, which use FM output to perform a specific task, such as tracking changes in land use or monitoring natural disasters.

## The Harmonized Landsat Sentinel-2 Data Collection

Image

[![True color mostly clear sky image of northwest Iceland with brown/green land surrounded by dark blue water](https://earthdata.nasa.gov/s3fs-public/styles/hds_large/public/2023-07/hls_western-iceland_07-11-2023_news.jpeg?VersionId=eknk1oTYbbNaW8u9W5.BrSq8TQE_s_Lt&itok=V4EF4fCa)](https://earthdata.nasa.gov/s3fs-public/2023-07/hls_western-iceland_07-11-2023_news.jpeg?VersionId=_TkTZedcIdTgii_LF1k04eG5BPP4m18Z "")

Image Caption

True-color HLS image of northwest Iceland acquired on July 11, 2023. NASA IMPACT developed the processing stream to expand HLS coverage from 28% of Earth to near-global. [Interactively explore this image in NASA Worldview](https://go.nasa.gov/3KkLOP2). Credit: HLS/NASA IMPACT; NASA Worldview.

HLS is a logical dataset on which to base the FM work. The HLS project provides consistent surface reflectance data from the Operational Land Imager ( [OLI](https://www.earthdata.nasa.gov/sensors/oli)) aboard the joint NASA/USGS Landsat 8 and 9 satellites and the Multi-Spectral Instrument ( [MSI](https://www.earthdata.nasa.gov/sensors/msi)) aboard the European Union's Copernicus Sentinel-2A and Sentinel-2B satellites. The combined sensor measurements enable global land observations every 2 to 3 days at 30-meter spatial resolution.

NASA IMPACT was instrumental in developing the HLS processing architecture to achieve near-global coverage. HLS imagery can be interactively explored using the [NASA Worldview](https://worldview.earthdata.nasa.gov/) Earth science data visualization tool and can be downloaded through [NASA Earthdata Search](https://search.earthdata.nasa.gov/search?q=HLS).

## The Road to the HLS Geospatial FM

The infrastructure needed for AI FMs is constantly evolving as the neural network architectures used to train these models become more complex. FMs are typically trained on massive datasets, which requires a significant amount of computing power.

As part of the NASA/IBM collaboration, IBM Research trained the HLS Geospatial FM on the IBM Cloud Vela supercomputer using the IBM watsonx FM stack, which is a cloud-based platform for training and deploying FMs. The IBM watsonx FM stack is currently running in NASA's Science Managed Cloud Environment ( [SMCE](https://smce.nasa.gov/)). Located at NASA's Goddard Space Flight Center in Greenbelt, Maryland, the SMCE is designed to accelerate NASA science research by enabling quick access to cloud resources for rapid prototyping and open collaboration.

## Evaluating the Model

NASA, IBM Research, and Clark University teams are in the process of assessing the HLS Geospatial FM for a wide range of downstream applications, including classification, object detection, time-series segmentation, and similarity search. The FM already has been applied to flood mapping, where it achieved state-of-the-art performance using smaller samples. Along with flood mapping, the FM also has been applied to burn scar identification, a critical component for active fire management and post-fire recovery. Additionally, using time-series data, the teams have shown the benefits of using the FM model for land cover and crop type mapping in diverse geographies across the contiguous United States.

## Fine-Tuning the Model

A recent workshop demonstrated the potential of AI FMs for Earth science applications. Organized by IMPACT in collaboration with the Institute of Electrical and Electronics Engineers Geoscience and Remote Sensing Society (IEEE GRSS) Earth Science Informatics Technical Committee (ESI TC), the workshop covered the development of FMs using HLS data and included a hands-on exercise in fine-tuning the FM using IBM's watsonx.ai. Participants also applied the model to new HLS data and successfully fine-tuned the FM for flood water detection and burn scar identification.

The workshop demonstrated that with the right tutorials, platform, and infrastructure, it is possible to quickly train geoscientists to effectively use FMs for downstream applications. This is a significant step forward in the development of AI for Earth science, as it opens up the possibility of using FMs to solve a wide range of problems.

## Next Steps

Along with the work on the HLS Geospatial FM, NASA and IBM are developing other applications to extract insights from Earth observations, including a large language model based on Earth science literature. In keeping with NASA's [open science guidelines and principles](https://www.earthdata.nasa.gov/esds/open-science), models and products resulting from this collaborative work will be open and available to the entire science community.

## Explore the Data

Hugging Face calls the HLS Geospatial FM family pipelines Prithvi. Prithvi is a first-of-its-kind temporal vision transformer pre-trained by the NASA and IBM team on contiguous U.S. HLS data.

Prithvi 100M:

- [Prithvi 100M model](https://huggingface.co/ibm-nasa-geospatial/Prithvi-100M "(opens in a new window)")(link is external)
- [Prithvi 100M demo](https://huggingface.co/spaces/ibm-nasa-geospatial/Prithvi-100M-demo "(opens in a new window)")(link is external)

Prithvi 100M Burn Scars:

- [Prithvi 100M Burn Scars model](https://huggingface.co/ibm-nasa-geospatial/Prithvi-100M-burn-scar "(opens in a new window)")(link is external)
- [Prithvi 100M Burn Scars demo](https://huggingface.co/spaces/ibm-nasa-geospatial/Prithvi-100M-Burn-scars-demo "(opens in a new window)")(link is external)

Prithvi 100M Flooding:

- [Prithvi 100M Flooding model](https://huggingface.co/ibm-nasa-geospatial/Prithvi-100M-sen1floods11 "(opens in a new window)")(link is external)
- [Prithvi 100M Flooding demo](https://huggingface.co/spaces/ibm-nasa-geospatial/Prithvi-100M-sen1floods11-demo "(opens in a new window)")(link is external)

Prithvi 100M Multitemporal Crop Detection:

- [Prithvi 100M Multitemporal Crop Detection model](https://huggingface.co/ibm-nasa-geospatial/Prithvi-100M-multi-temporal-crop-classification "(opens in a new window)")(link is external)
- [Prithvi 100M Multitemporal Crop Detection demo](https://huggingface.co/spaces/ibm-nasa-geospatial/Prithvi-100M-multi-temporal-crop-classification-demo "(opens in a new window)")(link is external)

## Details

## Last Updated

Aug. 7, 2025

## Published

Aug. 3, 2023

Copy link

✓

Thanks for sharing!

Find any service

[AddToAny](https://www.addtoany.com/ "Share Buttons")

[More…](https://www.earthdata.nasa.gov/news/nasa-ibm-openly-release-geospatial-ai-foundation-model-nasa-earth-observation-data#addtoany "Show all")

A2A