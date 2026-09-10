# Yvyra Soy — Experiments

## E.1 Experimental setup

### E.1.1 Hardware and runtime environment

| Component | Specification |
|-----------|---------------|
| CPU | Intel x86_64, ~3 GB peak RAM |
| GPU | None (CPU-only constraint; no CUDA available in the experiment sandbox) |
| Wall-clock budget | <2 minutes end-to-end |
| Wall-clock per query | <100 ms per department |
| Python | 3.12 (sandbox default; project supports 3.10 / 3.11 / 3.12) |
| Random seed | None (deterministic pipeline; no random sampling) |

### E.1.2 Datasets

| Dataset | Size | Records | Source |
|---------|------|---------|--------|
| INE 2022 census | 600 bytes | 19 pueblos | datos.gov.py |
| OSM polygons | 51 KB | 30 features | Overpass API |
| MAG rendimiento | 4 KB | 18 depts × 18 years | datos.gov.py |
| MAG superficie | 2 KB | 18 depts × 18 years | datos.gov.py |
| Hansen GFC | 59 KB | 256×256 tile | NASA MEaSUREs (off-repo) |

### E.1.3 Pipeline versions

- Pipeline version: `p0030_yvyra_soy/pipeline.py`, 2026-09-09 commit
- Python: 3.12
- pandas: 2.x
- numpy: 2.x
- No GPU required; no neural network training

## E.2 Reproducibility

```bash
# Run the pipeline
.venv/bin/python -c "
import sys
sys.path.insert(0, '.')
from src.papers.p0030_yvyra_soy import run_p0030_demo
result = run_p0030_demo()
print(f'pueblos: {result["census"]["n_pueblos"]}')
print(f'communities: {result["census"]["national_total_2022"]}')
print(f'mean yield: {result["national_mean_yield_kg_per_ha"]:.0f} kg/ha')
print(f'departments: {len(result["soy_by_department"])}')
print(f'OSM features: {result["osm_polygons"]["n_features"]}')
"

# Expected output:
# pueblos: 19
# communities: 557
# mean yield: 2429 kg/ha
# departments: 16
# OSM features: 30
```

## E.3 Threats to validity

- **Single Hansen tile** — only one 256×256 sample tile; no
  spatial generalization to all of Paraguay.
- **30 OSM polygons** — partial coverage of the 557 census
  communities; not a representative sample.
- **MAG sub-department duplicates** — the "Caaguazú" entry
  appears twice in the source data; pipeline counts both.
- **No causal identification** — correlation only at
  departmental scale.

## E.4 Outputs

All outputs are deterministic given the input data:

- `outputs/p0030/p0030_analysis.json` — full structured result
- `outputs/p0030/p0030_analysis.md` — human-readable report

Re-running `run_p0030_demo()` should produce identical output.
