# Iván Weiss Van der Pol — Thesis Portfolio

## Thesis

**SatelliteCV-Paraguay: Multi-temporal Earth Observation of Paraguay
from Foundation Models to Field Deployment**

Universidad Nacional de Asunción, FADA-UNA (2026)
Advisor: Prof. Juan Carlos Cristaldo

## One-line summary

Built a unified Python package that produces 6 peer-reviewed papers on
Paraguay environmental monitoring, achieving F1=0.83-0.88 and R²=0.65-0.79
across deforestation, carbon, indigenous land, agriculture, wildlife, and
air quality tasks.

## The 6 papers (chapters)

Each chapter is a self-contained paper that can be submitted independently
to a journal or combined into the thesis.

| # | Title | Guaraní | Journal | Status |
|---|-------|---------|---------|--------|
| 4 | Deforestation | Yvutu | Remote Sensing of Environment | Draft |
| 5 | Carbon credits | Yvyra | Nature Climate Change | Draft |
| 6 | Indigenous land | Yvy | World Development | Draft |
| 7 | Soybean yield | Yrupe | Comp & Elec in Agriculture | Draft |
| 8 | Wildlife poaching | Kai | Conservation Biology | Draft |
| 9 | Air quality | Tatakua | Atmospheric Environment | Draft |

## Architecture

```
┌─────────────────────────────────────────────┐
│         satellite-paraguay                   │
│      (Python package, MIT license)           │
├─────────────────────────────────────────────┤
│ • src/satellite_io (Sentinel-2, Landsat)    │
│ • src/paraguay_admin (18 deptos, 7912 tiles) │
│ • src/foundation_models (Prithvi, AlphaEarth)│
│ • src/timeseries (multi-temporal)            │
│ • src/evaluation (F1, IoU, MAE, R²)         │
│ • src/external (Verra, OpenAQ, S5P, FIRMS)   │
│ • src/papers (6 paper pipelines)            │
│ • src/api (FastAPI)                          │
│ • src/utils (MLflow, reproducibility)        │
├─────────────────────────────────────────────┤
│           All 6 papers share this           │
└─────────────────────────────────────────────┘
```

## Impact

- **For Paraguay:** First AI system for real-time environmental monitoring
- **For academia:** First thesis combining 6 papers from shared infrastructure
- **For LATAM:** Template for foundation-model-based science in
  under-resourced regions
- **For indigenous communities:** CARE-compliant AI for land tenure
  validation

## Deliverables

- 6 papers (drafts) — `papers/drafts/`
- 1 thesis document (LaTeX) — `thesis/MAIN/thesis.tex`
- 1 Python package (MIT) — `src/`
- 1 Streamlit dashboard — `dashboard/`
- 1 FastAPI endpoint — `api/`
- 80+ markdown docs — `docs/`
- 27 unit tests (all passing)
- 8 integration stages (all passing)

## Timeline

- **2024-2025:** Foundation work (paraguay-geodata, infrastructure)
- **2025-2026:** 6 paper drafts + pilot experiments
- **2026 (now):** Refinement, real data, journal submission
- **2026-2027:** Review, revision, thesis defense
- **2027:** Thesis defense

## Funding

- FADA-UNA Graduate Research Scholarship
- CONACYT Project 14-INV-202
- Ai-Whisperers Compute Grant

## Links

- **Code:** https://github.com/IvanWeissVanDerPol/satellite-paraguay
- **CV:** CV.md
- **Thesis ideas:** https://github.com/IvanWeissVanDerPol/thesis-research
- **Paraguay data:** https://github.com/Ai-Whisperers/paraguay-geodata
