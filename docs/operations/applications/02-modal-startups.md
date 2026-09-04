# Modal Startups Application — Draft

**Status:** [ ] TODO: submit at https://modal.com/startups
**Application type:** Modal Startups (free, rolling)
**Award:** Up to $25,000 in GPU serverless credits
**Time to fill:** 15 min
**Expected response:** 1-2 weeks

---

## Project name
SatelliteCV-Paraguay (Yvutu)

## What we do
We fine-tune foundation models (Prithvi, U-Net, YOLOv8, LSTM) on Paraguayan Earth observation data to produce 6 research papers and a unified multi-temporal satellite CV framework.

## Why we need Modal
We need GPU compute for **5 fine-tune runs** over 12 weeks:
1. Prithvi fine-tune on Sentinel-2 (16-24h on A100)
2. AlphaEarth fine-tune on Verra (18-24h on A100)
3. YOLOv8 retrain on wildlife (6-10h on 4090)
4. GRU training on agricultural (2-4h on 4090)
5. LSTM refinement on 24 stations (1-2h on T4)

**Total: ~50 GPU-hours, mostly A100 + 4090.**

Modal's serverless model is perfect for this:
- Pay per second, no idle waste
- A100/4090/H100 access on demand
- Snapshots + resume for fault tolerance
- $25K credits would cover 4-5 full thesis runs

## What we will use it for
- Weekly batched training jobs
- One-off evaluation runs
- Public demo API hosting (paper supplementary material)

## Project links
- GitHub: https://github.com/IvanWeissVanDerPol/satellite-paraguay
- Documentation: https://github.com/IvanWeissVanDerPol/satellite-paraguay/blob/main/docs/operations/RUNBOOK.md

## Use case
AI/ML research, Earth observation, climate/sustainability

## Stage
Pre-seed / Research

## Author
Ivan Hocht-VonDerPol
Universidad Nacional de Asuncion, Paraguay
