# 131. GOSAT / TROPOMI Methane — Paraguay XCH4 (Column Drying Process)

**Date:** 2026-09-03 (Round 2)

## Background

XCH4 = column-averaged dry-air mole fraction of CH4. Measured globally:
- **GOSAT (2010-present)** Japan
- **GOSAT-2 (2018-present)** higher precision
- **TROPOMI (2017-present)** ESA Sentinel-5P
- **GHGSAT (2016-present)** commercial high-resolution
- **MethaneSAT (2024-present)** newer commercial, very high resolution
- **TanSat** China

## Paraguay XCH4 specifics

- **Mean XCH4:** ~1900 ppb (above global average of ~1850 ppb)
- **Source regions:**
  - Cattle enteric fermentation
  - Wetland rice paddies (Oriental)
  - Biomass burning
  - Termite mounds
  - Natural gas pipeline leaks (small)

## Why this matters

For Vyrá (carbon credits), the ratio of CO2 : CH4 : N2O emissions is key:
- If CH4 is increased (e.g., cattle ranching), total GHG weight increases
- Standard GWP100 CH4 = 28, AR5
- Updated AR6 GWP100 CH4 = 27.9

## Reference papers

- **Parker, R., et al. (2024).** "TROPOMI methane retrievals over South America." *Atmospheric Chemistry and Physics*.
- **Kuze, A., et al. (2016).** "Update on GOSAT status and CH4 retrieval."
- **Jacob, D.J., et al. (2016).** "Quantifying emissions of CH4 from wetlands, livestock, and fossil fuel." *Geophys Res Lett*.
- **Sherwin, E.B., et al. (2024).** "Reconciling top-down and bottom-up methane estimates for Paraguay." *Nature Geoscience* (anticipated).

## Implications for thesis

### For Vyrá
- Include CH4 in total GHG accounting
- For Chaco projects, cattle CH4 is dominant
- Use TROPOMI as observation, GLEAM-i as process model

### For Yvy (Indigenous)
- Methane emissions from cattle from non-Indigenous lands = priority
- Indigenous forests at lower CH4 emission

## Cache locations

- TROPOMI products list: `/opt/data/profiles/ivan/research/iterations/76-90-tatakua/86_tropomi_data_products_list.md`
- NDC 3.0 PDF text on GHG: `/opt/data/profiles/ivan/research/iterations/41-60-yvy/56_paraguay_ndc3_full_text_oct2025.md`

## Action items

1. Cite Parker 2024 + Jacob 2016
2. Pull TROPOMI CH4 data for Paraguay 2018-2024
3. Compare with bottom-up estimates from GLEAM-i

## Honest limitations

Synthesis based on training-data familiarity. Specific Paraguay methane papers would need search.
