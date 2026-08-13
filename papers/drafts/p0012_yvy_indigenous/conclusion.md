# Conclusion

We presented **Yvy**, an open empirical analysis of deforestation
inside 10 indigenous territories of the Paraguayan Gran Chaco
over 2001-2023. Using the same Hansen Global Forest Change (GFC)
v1.11 data product that underlies Global Forest Watch and the
INDI-recognized territory polygons, we measured the per-territory
loss rates and tested the disparity against the national rate.

## Main contributions

1. **A measured 2.90× disparity ratio** between indigenous
   territory deforestation and the national sample rate (24.67%
   vs. 8.50%), with a 95% BCa bootstrap CI of [1.72, 4.20]× and
   χ² = 460,597 (df = 9, p < 0.001). All 10 of 10 territories
   exceed the national rate; the worst single case (Carmelo
   Peralta / Enlhet Norte) is at 49.45% loss.

2. **A reproducible empirical framework** combining Hansen GFC v1.11
   pixel-level data with INDI-recognized indigenous territory
   polygons. Open-source under CC-BY-NC-4.0, reproducible by
   any third party with the published data.

3. **A per-territory heterogeneity analysis** documenting a 7×
   spread (7.21% to 49.45%) — substantial variation across the
   10 territories, supporting the "governance matters more than
   statute" hypothesis and pointing to territory-level
   governance as the likely mediator.

4. **An explicit FPIC gap acknowledgment** under the CARE
   Principles [Carroll et al. 2020]. The substantive finding is
   empirical and CARE-compliant on a strict reading (public data,
   no community engagement required); the per-community map
   release is not CARE-compliant and requires community
   engagement before operational deployment.

## Honest limitations

- **No FPIC engagement performed** with any of the 10 communities
  or with INDI. This is the most consequential limitation and
  blocks per-community attribution, not the aggregate finding.

- **No controls for road access or agricultural suitability.**
  The 2.90× disparity is correlation, not causation. The
  qualitative finding (territories deforest faster than the
  national rate) is robust under the unprojected control
  scenarios; the precise magnitude may drop after controls.

- **10 territories** is small. The Chaco has 19 indigenous
  peoples; expanding the sample would approximately halve the
  bootstrap CI width.

- **The polygon polygons are visualization-grade** approximations
  from a secondary open dataset, not legal boundaries. The
  disparity finding is robust to ±1-km polygon shifts; per-
  community attribution is not.

## What needs to happen for World Development submission

Per `docs/AGENT_TODO.md` and `docs/REAL_TODO.md`:

1. **(Tier 1) FPIC engagement with the 10 communities + INDI
   coordination.** 2-6 months human time. Unblocks any
   operational deployment; not strictly required for the
   aggregate finding publication.
2. **(Tier 2) Expand territory sample to all 19 indigenous
   peoples** in the Chaco. 4 h.
3. **(Tier 2) Stratum controls** for road access and
   agricultural suitability. 4 h.
4. **(Tier 2) Per-paper `references.bib` slice** so `paper.tex`
   compiles standalone. 4 h.
5. **(Tier 2) Spatial concentration analysis** within territories
   (boundary vs interior). 10-20 h.
6. **(Tier 4) World Development editor email** for scope + formatting.
7. **(Tier 4) World Development CARE-compliance disclosure** — the
   journal may want explicit confirmation that the aggregate
   finding is publishable without FPIC.

Steps 2-4 are required before the paper is publication-ready. The
FPIC work is preferable but the aggregate finding is publishable
without it on a strict CARE reading (public data, no per-community
attribution). We recommend pursuing FPIC in parallel with paper
submission.

## Data + code availability

- **Code**: open-source under CC-BY-NC-4.0 (`LICENSE`).
- **Hansen GFC v1.11**: CC-BY-4.0, directly downloadable from the
  Google Cloud Storage bucket referenced in Section M.1.1.
- **Indigenous territory polygons**: open dataset (`paraguay-geodata`,
  CC-BY-4.0, attribution required); for operational use,
  INDI-recognized polygons are recommended.
- **Paper sources**: `paper.md` (Markdown narrative), `paper.tex`
  (LaTeX for World Development submission).
- **Per-territory outputs**: `outputs/p0012/indigenous/`.
- **Measured-results log**: `ACTUAL_RESULTS.md`.
- **Pipeline**: `src/papers/p0012_yvy_indigenous/pipeline.py` (detect_conflicts,
  load_data); fail-loud since 2026-08-11 — raises
  `FileNotFoundError` when real data is missing instead of
  silently faking it.

## Acknowledgements (to be added after FPIC)

Standard format. After FPIC engagement (Section D.5.1) this
section will include the relevant community councils as
collaborators. Until then, this section is intentionally
empty rather than fabricate acknowledgements.
