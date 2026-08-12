# Introduction

## Yvy: Indigenous Land Tenure and Deforestation in Paraguay's Gran Chaco

### 1.1 The global question

Worldwide, an estimated **~1 billion hectares** of land are held
by indigenous and local communities [Garnett et al. 2018]. A
growing empirical literature [Sze et al. 2022 in PNAS; Fa et al.
2020; Dawson et al. 2021] has established that this land is
typically *deforested at lower rates* than comparable non-indigenous
land, with observed protective ratios of 1.3× to 3× depending on the
region and the specific comparison.

The standard interpretation [Garnett et al. 2018; Dinerstein et
al. 2020] is that the "indigenous lands as forest stewards" pattern
holds across the majority of biomes and governance regimes, and is
attributed to a combination of cultural land-use norms,
community-scale enforcement, and political mobilization against
encroachment. The PNAS result by Sze et al. (2022) used a global
sample of ~15,000 indigenous territories and found a 22% lower
deforestation rate inside territories versus outside, controlling
for biome, slope, distance to roads, and other confounders.

### 1.2 The Paraguay reversal

Paraguay's Gran Chaco is one of the documented exceptions to this
pattern. Industry reports (Guyra Paraguay, WWF Paraguay, Tierranuestra),
the Paraguayan government's own Annual Forestry Report (INFONA
2024), and unpublished NGO monitoring (REDMOPy 2024) consistently
report that the indigenous territories of the Chaco are
disproportionately affected by the agricultural frontier's advance
even though they are nominally state-recognized as indigenous
lands.

We present **Yvy** ("land" or "earth" in Guaraní), a paper that
quantifies this pattern in reproducible numbers using the same
Hansen Global Forest Change (GFC) v1.11 data product that has become
the operational reference for global forest monitoring [Hansen
et al. 2013].

### 1.3 Research questions

This paper addresses three questions:

- **RQ1:** What is the aggregate per-pixel deforestation rate
  inside the 10 indigenous territories of the Chaco over
  2001-2023, as measured from real Hansen GFC data? (Answered
  in Section 3.)
- **RQ2:** What is the disparity ratio between the territories and
  the national rate? How robust is the disparity to bootstrapping?
  (Answered in Section 3 with χ² and 1,000-resample bootstrap.)
- **RQ3:** How do individual territories differ in magnitude, and
  what is the spatial pattern of under- and over-performance?
  (Answered in Section 4.)

### 1.4 Substantive contributions

1. **A measured 2.90× disparity ratio** between indigenous-territory
   deforestation and the national sample rate, with a 95% bias-
   corrected-and-accelerated (BCa) bootstrap CI of [1.72, 4.20]× and
   χ² = 460,597 (df = 9, p < 0.001). All **10 of 10** territories are
   above the national rate; the worst single territory (Carmelo
   Peralta / Enlhet Norte) is at **49.45% loss** — almost half
   deforested over 23 years.

2. **A reproducible empirical framework** combining Hansen GFC v1.11
   pixel-level data with the 10 INDI-recognized Chaco indigenous
   territory polygons. The framework is open-source, the code is
   under CC-BY-NC-4.0, and any third party can re-run the analysis
   from the published data.

3. **A per-territory heterogeneity analysis** documenting that
   the 7× spread (7.21% to 49.45%) is itself a contribution —
   it shows that the disparities are not uniform across territories
   and points to territory-level governance and enforcement as the
   likely mediators, rather than indigenous land tenure per se.

4. **An explicit FPIC (Free, Prior, and Informed Consent) gap
   acknowledgment** under the CARE Principles for Indigenous Data
   Governance [Carroll et al. 2020]. The substantive finding (2.90×
   disparity) is empirically defensible from the public data; the
   *per-community map release* is not, because no community has
   been engaged. Section 5 documents the prerequisite work for any
   operational deployment.

### 1.5 Paper positioning

This is the second paper in a 6-paper thesis substrate (P0011
documents the country-scale deforestation quantification;
P0012 this paper documents the indigenous-territory overlap
finding). The substantive scientific question (does the global
"indigenous lands as forest stewards" pattern hold in the
Paraguayan Chaco?) is answered **no, with statistical robustness**,
and the practical implication (urgent policy attention to the
forest governance gap in the Chaco) is the operational follow-on.

### 1.6 Paper organization

- **Section 2** describes the data sources (Hansen GFC v1.11,
  INDI-recognized indigenous territory polygons) and the analysis
  protocol.
- **Section 3** reports the per-territory findings and the
  disparity statistical tests (χ² and bootstrap CI).
- **Section 4** discusses the per-territory heterogeneity and what
  the magnitude of the disparity implies for policy.
- **Section 5** is the honest assessment: what the analysis shows,
  what it does not show, and the CARE / FPIC prerequisite work
  needed before any operational deployment.
- **Section 6** concludes.
- **Section 7** positions the work against the prior literature.
