#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/../../.."
python3 -c "
import sys
sys.path.insert(0, '.')
from src.external import fetch_verra_paraguay, compute_parcel_biomass
import numpy as np
verra = fetch_verra_paraguay()
print(f'Verra projects: {len(verra)}')
print(f'Total area: {verra[\"area_ha\"].sum():,.0f} ha')
print(f'Total credits: {verra[\"estimated_annual_emission_reductions_tco2e\"].sum():,.0f} tCO2e')
biomass = compute_parcel_biomass(np.array([]), area_ha=50000, method='ipcc')
print(f'Biomass in 50k ha: {biomass[\"biomass_tons\"]:,} tons')
"
