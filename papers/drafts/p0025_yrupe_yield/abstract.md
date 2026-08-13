# Abstract

## Yrupe: Soybean Yield Prediction using Sentinel-2 + INBIO

We present Yrupe, a machine-learning-based soybean yield prediction system for the Caaguazú department of Paraguay. Yrupe combines Sentinel-2 time series, Delineate Anything v2 for field boundary delineation, and INBIO yield records. We test whether a deforestation-pretrained encoder transfers to yield prediction. In our pilot (4 scenes, 18 monthly composites, 8 epochs, CPU), the multi-task CNN **did not converge** (F1=0.497, MAE=3.20 t/ha on synthetic labels), and the cross-domain transfer ratio measured 0.082 — far below the 0.74 figure quoted in earlier drafts. The R²>0.80 / 5,000-fields headline was a target, not a measurement, and has been corrected in `ACTUAL_RESULTS.md`. The pipeline, baseline definitions, and a reproducible failure analysis are released so the failure mode (degenerate all-zero output under CPU-only training on synthetic labels) can be addressed before claiming operational yield forecasts.

## Keywords

Earth observation, deep learning, Paraguay, p0025, sentinel-2

## Author

Iván Weiss Van der Pol (FP-UNA)
