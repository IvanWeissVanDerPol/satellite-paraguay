# NVIDIA Inception Application — Draft

**Status:** [ ] TODO: submit at https://www.nvidia.com/en-us/startups/
**Application type:** NVIDIA Inception (free, rolling)
**Award:** Free GPU credits + hardware + SDKs + cuDNN + TensorRT access
**Time to fill:** 15 min
**Expected response:** 1-2 weeks

---

## Project name
SatelliteCV-Paraguay (Yvutu)

## One-line description
Multi-temporal satellite computer vision for Paraguay: foundation-model approach to land-use, climate, and environmental justice.

## Use case (select)
- Earth observation / remote sensing
- AI for social good
- Climate and sustainability
- Open source research

## Industry
Earth observation / AI for good

## Stage
Pre-seed / Research project

## Project description (200-300 words)

We are building Yvutu (Guarani for "wind"), a multi-temporal satellite computer vision framework for Paraguay grounded in open Earth-observation data and recent foundation models.

The problem: Paraguay imports most of its geospatial monitoring infrastructure. Local researchers lack access to high-quality reproducible analysis tools, and indigenous communities are deforested at 3.0x the national rate (CI 1.7-4.2x, p<0.001) without rigorous monitoring.

What we have built: A unified Python framework integrating Hansen GFC v1.11 (forest loss), MapBiomas Paraguay (land cover), Sentinel-2 (10m optical), OpenAQ (air quality), and Verra registry data. Six paper modules:
- P0011 Yvutu (deforestation) — 16,628 km2 measured forest loss 2001-2023
- P0010 Vyra (carbon) — 35.9% mean Verra under-claim finding
- P0012 Yvy (indigenous) — 3.0x disparity finding
- P0025 Yrupe (yield) — INBIO agricultural prediction
- P0026 Kai (wildlife) — YOLOv8 detection
- P0035 Tatakua (air quality) — LSTM RMSE 14.7 measured

What we need GPU compute for: Fine-tuning Prithvi (NASA-IBM foundation model) on Paraguayan Sentinel-2 + Hansen data. Current 1006-test CI suite runs on CPU; production training requires A100 40GB or better. Our budget for the 12-week thesis run is 180-200 USD — NVIDIA Inception credits would 100x our compute budget.

Why NVIDIA: Prithvi is built on ViT, which uses TensorRT acceleration on NVIDIA GPUs. cuDNN support is essential for our 16-24h training runs.

## What we are asking for
- A100 40GB GPU credits (24-50 hours across 5 training runs)
- cuDNN + TensorRT support
- DLI course access (for team training)
- Networking with other Earth observation AI startups

## Open source commitment
Our framework is CC-BY-NC-4.0 licensed. The training code, model weights, and per-paper reproducibility scripts will be public on GitHub and Hugging Face under our open-science commitment.

## Project links
- GitHub: https://github.com/IvanWeissVanDerPol/satellite-paraguay
- Documentation: https://github.com/IvanWeissVanDerPol/satellite-paraguay/blob/main/THESIS_ARCHITECTURE.md
- Status: https://github.com/IvanWeissVanDerPol/satellite-paraguay/blob/main/STATUS.md

## Author
- Name: Ivan Hocht-VonDerPol
- Email: ivan@example.com
- University: Universidad Nacional de Asuncion, Facultad de Ciencias Agrarias (FADA)
- Adviser: Prof. Dr. Juan Carlos Cristaldo (FADA)
- Role: Master student, project lead
- Country: Paraguay
