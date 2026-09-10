# P0030 Yvyra Soy

**Title:** Yvyra Soy: Indigenous territory presence and soybean
frontier expansion in Paraguay's Gran Chaco and Eastern regions —
A public-data analysis using INE 2022 census, OSM community
polygons, and MAG department yield (2007/08--2024/25)

**Author:** Iván Weiss Van der Pol (FP-UNA)

**Target journal:** *Computers and Electronics in Agriculture*

**Status:** Pipeline implemented, measured numbers in
`ACTUAL_RESULTS.md`, paper draft in `paper.tex` and `paper.md`.

## Quick start

```bash
# Run the pipeline
.venv/bin/python -c "
import sys
sys.path.insert(0, '.')
from src.papers.p0030_yvyra_soy import run_p0030_demo
result = run_p0030_demo()
"

# Outputs
ls outputs/p0030/
# p0030_analysis.json
# p0030_analysis.md
```

## Data sources

- **INE 2022 census** — `data/raw/ine_indi/indigenous_communities_2022_summary.csv`
- **OSM polygons** — `data/raw/osm_indigenous/osm_comunidades_indigenas_py.geojson`
- **MAG yield** — `data/raw/fao_mag/mag_soja_*.csv`
- **Hansen GFC** — `data/cache/hansen/hansen_2018_2023.npz` (off-repo, ~56 km² sample)

## License

MIT

## See also

- `outputs/DEFENSE_PREP_15_HAT_AUDIT_2026-09-09.md` — full audit context
- `outputs/data_audit.json` — repository-wide data lineage
- `thesis/references.bib` — master bib (P0030 references generated from this)
