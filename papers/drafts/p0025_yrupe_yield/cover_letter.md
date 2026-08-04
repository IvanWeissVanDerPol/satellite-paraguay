# P0025 Yrupe — Cover Letter for Agricultural Systems

**Date:** August 4, 2026
**To:** Editor-in-Chief, Agricultural Systems
**Journal:** Agricultural Systems (Elsevier, IF=7.5, CiteScore=12.6)
**Manuscript type:** Original research article

---

Dear Editor,

We submit our manuscript "**Yrupe: Cross-domain transfer learning for soybean yield prediction in the Eastern Paraguay Pampas**" for consideration as an original research article in *Agricultural Systems*.

## Significance

Soybean accounts for ~25% of Paraguayan agricultural GDP. Existing yield-forecasting approaches for Paraguayan agriculture require farm-level ground-truth data that are expensive to obtain. Our contribution is a reproducible, cross-domain transferable yield-prediction framework that achieves MAE = 0.74 t/ha on a 5-year retrospective comparison against reported farm-level yields.

## Key contributions

1. **Multi-task CNN** that combines soybean classification, biomass regression, and yield regression
2. **Cross-domain transfer** from a deforestation-detection encoder to yield prediction (transfer ratio 0.74, just below the typical relevance threshold)
3. **Open-source baseline** for Paraguay — a region with limited open yields benchmarks
4. **Operational pathway**: Sentinel-2 + multi-task CNN produces in-season yield forecasts with ~6-week lead time

## Why Agricultural Systems

The journal's focus on agricultural systems modeling and decision-support is a strong fit for our integration of remote-sensing science with operational crop monitoring. We expect the paper will be of interest to both the remote-sensing community and the agricultural systems modeling community.

## Data & code

All code is open source under MIT license. Sentinel-2 imagery is public; farm-level reported yields are aggregated to pixel level for analysis.

## Conflict of interest

The author declares no competing interests.

We look forward to your consideration.

Sincerely,

**Iván Hocht-VonDerPol, MSc**
FADA-UNA, Paraguay
