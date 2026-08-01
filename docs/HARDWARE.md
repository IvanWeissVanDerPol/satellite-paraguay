# Hardware Requirements

## Minimum (CPU only)

| Component | Requirement |
|-----------|-------------|
| CPU | 4+ cores (Intel i5 / AMD Ryzen 5 or better) |
| RAM | 8 GB (16 GB recommended for large datasets) |
| Disk | 50 GB free (for Sentinel-2 tiles + embeddings) |
| GPU | None (CPU inference works but slower) |
| Network | 10 Mbps (for downloads) |

**Use cases:**
- Run baselines (Random Forest, U-Net)
- Run XAI dashboards
- Run documentation / notebooks
- Run API (low traffic)
- Run dashboard

**Recommended providers:**
- Old laptop
- Raspberry Pi 4 (8 GB)
- AWS t3.large
- GCP e2-standard-4

## Recommended (1× GPU)

| Component | Requirement |
|-----------|-------------|
| CPU | 8+ cores (Intel i7 / AMD Ryzen 7) |
| RAM | 32 GB |
| Disk | 500 GB SSD |
| GPU | 1× NVIDIA RTX 3060 (12 GB VRAM) |
| Network | 100 Mbps |

**Use cases:**
- Fine-tune Prithvi-100M
- Train YOLOv8 medium
- Train small U-Net
- Run TimesFM on long sequences

**Recommended providers:**
- Desktop PC with RTX 3060 ($1,500-2,000)
- AWS g4dn.xlarge ($0.50/hour)
- GCP n1-standard-8 + T4 ($0.50/hour)
- Lambda Labs GPU ($1-2/hour)
- Vast.ai RTX 3060 ($0.20-0.40/hour)
- RunPod RTX 3060 ($0.20-0.40/hour)

## Optimal (4× GPU)

| Component | Requirement |
|-----------|-------------|
| CPU | 16+ cores (Intel i9 / AMD Ryzen 9) |
| RAM | 128 GB |
| Disk | 2 TB NVMe SSD |
| GPU | 4× NVIDIA A100 (80 GB each) or 8× V100 |
| Network | 1 Gbps |

**Use cases:**
- Fine-tune Prithvi-300M on full Paraguay
- Fine-tune LLaVA-1.6-34B on Paraguay data
- Train multiple models in parallel
- Run hyperparameter sweeps

**Recommended providers:**
- Workstation (4× RTX 4090, $8,000-12,000)
- AWS p4d.24xlarge (8× A100, $32/hour)
- GCP a2-ultragpu-8g (8× A100, $30/hour)
- Lambda Labs 8× A100 ($25-30/hour)

## Cloud GPU Pricing (2024-2026)

| Provider | GPU | Price/hour |
|----------|-----|-----------|
| Colab Pro | T4 | $10/month |
| Colab Pro+ | A100 | $50/month |
| Kaggle | T4×2 | Free (30h/week) |
| Vast.ai | RTX 3060 | $0.20-0.40 |
| Vast.ai | RTX 3090 | $0.40-0.70 |
| RunPod | RTX 3060 | $0.20-0.40 |
| RunPod | A100 | $1.50-2.50 |
| Lambda | A100 | $1.50-2.00 |
| AWS | g4dn.xlarge (T4) | $0.50 |
| AWS | p3.2xlarge (V100) | $3.00 |
| AWS | p4d.24xlarge (8× A100) | $32.00 |
| GCP | T4 | $0.50 |
| GCP | A100 | $3.00 |

## Cost Estimate (Total for Thesis)

| Component | Cost |
|-----------|------|
| Colab free (most usage) | $0 |
| Colab Pro (4 months × $10) | $40 |
| Kaggle free | $0 |
| Cloud GPU (occasional for foundation models) | $100-500 |
| **Total minimum** | **$0** |
| **Total realistic** | **$200-1000** |

## Storage Estimates

| Asset | Size |
|-------|------|
| Paraguay Geodata (already local) | 549 MB |
| Sentinel-2 (1 tile) | 800 MB |
| Sentinel-2 (all 7,912 Paraguay tiles, 5-year) | 500 GB - 5 TB |
| Sentinel-5P (Asunción, 5-year) | 50 GB |
| Embeddings (Prithvi, 7,912 tiles) | 30 GB |
| Model checkpoints | 10 GB |
| Outputs (figures, tables, predictions) | 10 GB |
| **Total minimum** | **700 MB (with local only)** |
| **Total realistic** | **500 GB** |
| **Total optimal** | **5 TB** |

## Compute Estimates

| Task | Compute needed | Time on RTX 3060 |
|------|----------------|-------------------|
| Random Forest (P0011) | CPU | 5 minutes |
| U-Net baseline | GPU | 30 minutes |
| Train Prithvi (fine-tune) | GPU | 8 hours |
| Train LLaVA-1.6 (fine-tune) | GPU | 24 hours |
| Embed 7,912 tiles | GPU | 4 hours |
| Run dashboard | CPU | <1 hour/week |

## Connectivity

- **Local development:** Any (Colab Pro, Kaggle)
- **Cloud training:** 10 Mbps minimum (50 GB+ uploads)
- **Real-time inference:** <100ms latency required

## Backup

- **Code:** Git (already done)
- **Data:** DVC + cloud storage
- **Models:** DVC + cloud storage
- **Outputs:** Git LFS + cloud storage
- **Papers:** Git + cloud backup

## Security

- **API keys:** Use environment variables (.env, never commit)
- **Sensitive data:** Use DVC encryption
- **Indigenous data:** Apply CARE Principles + encryption
