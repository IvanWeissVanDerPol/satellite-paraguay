#!/usr/bin/env bash
# P0030 Yvyra Soy — Quickstart
# Run the full pipeline and write outputs.
set -euo pipefail

cd "$(dirname "$0")/../.."
.venv/bin/python -c "
import sys
sys.path.insert(0, '.')
from src.papers.p0030_yvyra_soy import run_p0030_demo
result = run_p0030_demo()
print('--- P0030 results ---')
print(f'pueblos: {result["census"]["n_pueblos"]}')
print(f'total communities (2022): {result["census"]["national_total_2022"]}')
print(f'national mean yield: {result["national_mean_yield_kg_per_ha"]:.0f} kg/ha')
print(f'departments in soy: {len(result["soy_by_department"])}')
print(f'OSM features: {result["osm_polygons"]["n_features"]}')
"
echo "Outputs:"
ls -la outputs/p0030/
