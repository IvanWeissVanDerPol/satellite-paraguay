# AWS Activate Application — Draft

**Status:** [ ] TODO: submit at https://aws.amazon.com/startups/credits/
**Application type:** AWS Activate (free, rolling)
**Award:** Up to $200,000 in AWS credits
**Time to fill:** 20 min
**Expected response:** 1-2 weeks

---

## Project name
SatelliteCV-Paraguay (Yvutu)

## Startup stage
Pre-seed / Research project

## Industry
Earth observation / AI for good / Climate

## What we do
Multi-temporal satellite computer vision for Paraguay. We use Hansen GFC v1.11, MapBiomas Paraguay, Sentinel-2, and OpenAQ data. We fine-tune Prithvi, U-Net, YOLOv8, LSTM on Paraguayan data. 6 papers, 1006+ tests.

## What we need AWS for
- **S3** (storage): 50 GB of model checkpoints + 5 GB of intermediate data
- **SageMaker** (training): optional alt to Modal/RunPod
- **EC2 g4dn** (T4 spot): P0035 LSTM refinement (cheaper than RunPod T4)
- **CloudWatch**: drift detector alerts integration
- **Lambda**: serverless API for paper 3 supplementary material

## Why $200K matters
- $180-200 self-fund covers one thesis run
- $200K = 1000+ thesis runs of redundancy
- Lets us run 10+ experimental variants of each paper (currently we can afford 1)
- Lets us host public API indefinitely (paper citations benefit)

## What we are NOT using AWS for
- Production deployment (we use Cloudflare Pages)
- Primary compute (NVIDIA Inception + Modal for that)
- Database (SQLite for drift, D1 for cache)

## Author
- Name: Ivan Hocht-VonDerPol
- Email: ivan@example.com
- University: Universidad Nacional de Asuncion, FADA
- Country: Paraguay

## Project links
- GitHub: https://github.com/IvanWeissVanDerPol/satellite-paraguay
- Website: https://paragu-ai.com
- Roadmap: https://github.com/IvanWeissVanDerPol/satellite-paraguay/blob/main/docs/COMPLETE-PLAN.md
