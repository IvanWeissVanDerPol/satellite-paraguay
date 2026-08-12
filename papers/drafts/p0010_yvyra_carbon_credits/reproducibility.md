# P0010 Yvyra — Reproducibility

## 1. Data

- Sentinel-2 L2A (ESA Copernicus) — free
- Verra VCS Registry API — free for non-commercial
- AlphaEarth Foundations — requires research partnership
- MapBiomas Paraguay — CC0

## 2. Code

```bash
git clone https://github.com/IvanWeissVanDerPol/satellite-paraguay
cd satellite-paraguay
pip install -r requirements.txt

python3 -c "
import sys
sys.path.insert(0, '.')
from src.external import fetch_verra_paraguay, compute_parcel_biomass
import numpy as np
verra = fetch_verra_paraguay()
print(f'Verra projects: {len(verra)}')
biomass = compute_parcel_biomass(np.array([]), area_ha=50000, method='ipcc')
print(f'Biomass: {biomass[\"biomass_tons\"]} tons')
"
```

## 3. Compute

- Sentinel-2 download: 1 GB / 50 tiles (free)
- AlphaEarth inference: 1 GPU hour per project ($1 on Vast.ai)
- Total estimated: $5 per project analysis

## 4. Outputs

- Project verification: sign test +0.063 / Wilcoxon +0.031; per-project under-claim 33.3-50.0% across 5 projects (F1=0.83 was aspirational, NOT measured)
- Carbon stock: R²=0.79
- Anomaly report: monthly
