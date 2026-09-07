# GPU Provider Decision — satellite-paraguay

**Generated:** 2026-08-22 (Phase 0.1 of 12-week roadmap)
**Decision needed by:** Iván (Phase 0 unblock week)
**Author:** Hermes agent

---

## TL;DR

For satellite-paraguay's GPU needs (Prithvi fine-tune, YOLOv8 retrain, LSTM refinement, AlphaEarth training), use **RunPod** as primary with **Vast.ai** as fallback.

**Estimated total spend:** $120-180 for the 12-week thesis run.
**Daily cap:** $5/day (`infra/cost-cap.sh` enforces).
**Alert threshold:** 80% of monthly cap.

---

## Why we need GPU

The 6 papers each need a real (non-mock) fine-tune or training pass on a foundation model:

| Paper | Model | GPU required | Estimated time |
|---|---|---|---|
| P0011 Yvutu | Prithvi fine-tune (Sentinel-2 + Hansen) | A100 40GB or 4090 24GB | 16-24 h |
| P0010 Vyrá | AlphaEarth fine-tune | A100 40GB | 18-24 h |
| P0025 Yrupe | GRU training (real INBIO data) | 4090 or T4 | 2-4 h |
| P0026 Kai | YOLOv8 retrain (real labels) | 4090 or T4 | 6-10 h |
| P0035 Tatakua | LSTM refinement (24 stations) | CPU OK, T4 fast | 1-2 h |

**Total:** ~50 GPU-hours, mostly on A100/4090.

---

## Provider options

### Option A: RunPod (PRIMARY recommendation)

| Aspect | Detail |
|---|---|
| On-demand $/hr (A100 40GB) | $1.64 |
| On-demand $/hr (4090 24GB) | $0.79 |
| Spot $/hr (A100, ~30-50% off) | $0.80-1.10 |
| Cold start | <30 seconds |
| Storage | $0.20/GB/month (persistent volume) |
| Billing unit | Per-second, $5 minimum top-up |
| Payment | Credit card, crypto, PayPal |
| Argentina-friendly? | Crypto yes, card declined for some PY banks |
| Data egress | Free within EU/US regions, $0.05/GB elsewhere |
| Tooling | RunPod CLI + Python SDK + Jupyter template |
| Cold storage | $0.20/GB/mo for persistent volumes |
| Termination grace | 10s ( SIG, SIGTERM, SIGKILL fallback after 10s) |
| Best for | **Long training runs**, serverless endpoints, predictable billing |

**Pros for us:**
- Highest reliability
- Per-second billing (no wasted money on idle)
- Persistent volume keeps our data + checkpoints across runs
- Native Docker + Python SDK = we can write `scripts/train_prithvi_yvutu.py --provider runpod`
- Spot pricing available (30-50% off if we're flexible)

**Cons:**
- Slightly higher on-demand rate than Vast.ai
- $5 minimum top-up (one-time, refundable)

---

### Option B: Vast.ai (FALLBACK for spot pricing)

| Aspect | Detail |
|---|---|
| On-demand $/hr (A100 40GB) | $1.10-1.50 |
| On-demand $/hr (4090 24GB) | $0.35-0.55 |
| Spot $/hr (A100, ~70% off) | $0.30-0.50 |
| Cold start | 30-90 seconds |
| Storage | NFS persistent, $0.10/GB/month |
| Billing unit | Per-minute (rounded up) |
| Payment | Credit card, PayPal, crypto |
| Argentina-friendly? | Crypto yes |
| Data egress | Free |
| Best for | **Cheap spot capacity**, when we can tolerate interruptions |

**Pros for us:**
- Lowest spot prices (A100 for $0.30-0.50/hr)
- Good for fault-tolerant training (we can checkpoint + resume)

**Cons:**
- Spot can be interrupted (need to implement checkpoint + resume in every script)
- Less polished UX than RunPod
- More manual SSH setup

---

### Option C: Linode / Hetzner bare-metal (NOT recommended for GPU)

Linode and Hetzner don't have competitive A100/4090 spot pricing. Their GPU instances are A100 dedicated at $2-3/hr, same as on-demand RunPod. Skip.

### Option D: AWS / GCP (NOT recommended)

AWS p4d.24xlarge (8x A100) is $32/hr — way more than we need. g4dn.xlarge (T4) is $0.53/hr but slow for Prithvi. Skip.

---

## Decision

**RunPod primary + Vast.ai fallback.**

| Need | Provider | Rate | Justification |
|---|---|---|---|
| A100 for Prithvi fine-tune (P0011, P0010) | **RunPod on-demand** | $1.64/hr | Reliability + Python SDK. ~$30/run. |
| 4090 for YOLOv8 retrain (P0026) | **RunPod on-demand** | $0.79/hr | Same instance, ~$8/run. |
| 4090 for GRU training (P0025) | **RunPod on-demand** | $0.79/hr | Same instance, ~$3/run. |
| Cheapest possible spot fallback | **Vast.ai spot** | $0.30-0.50/hr | If RunPod is unavailable. ~$10/run for Prithvi. |

**Estimated 12-week spend:**
- 4 × A100 @ $1.64/hr × ~20 hr/run = **$131**
- 1 × 4090 @ $0.79/hr × ~10 hr = **$8**
- 1 × 4090 @ $0.79/hr × ~3 hr = **$2.5**
- Buffer for retries, exploration, errors: **$40-50**
- **Total: ~$180-200 for full thesis run**

---

## Cost cap + alerting (`infra/cost-cap.sh`)

- **Daily cap:** $5/day (auto-kill instance if exceeded)
- **Alert at 80%:** Post to `/opt/data/state/org-state.json` + cron heartbeat
- **Monthly cap:** $50/month (alerts at 80% = $40)
- **Tracking:** Per-paper cost logged to `models/cost_log.csv`

---

## Queue strategy

When training scripts run, they use a "queue and resume" pattern:

1. `scripts/queue_train.py --paper P0011 --provider runpod --gpu a100-40gb`
2. Script checks RunPod for available instance → launches if under daily cap
3. On interruption: snapshots to persistent volume, kills instance
4. Resumes from snapshot next run
5. Final model → downloaded via `runpodctl` to `models/`

This protects against:
- RunPod spot instance being reclaimed
- Manual interruption by Iván
- Network issues during download
- Out-of-budget (cost-cap kills at $5/day)

---

## Pre-flight checklist for Iván

Before running any GPU job:

1. [ ] Create RunPod account at https://runpod.io
2. [ ] Add $20 credit (~$20 lasts through 4 fine-tunes)
3. [ ] Generate API key in Settings → API Keys
4. [ ] Add to GitHub secrets as `RUNPOD_API_KEY`
5. [ ] Install RunPod CLI: `pip install runpod`
6. [ ] Create persistent volume: `runpodctl create volume --name satellite-paraguay-data --size 100`
7. [ ] Upload existing data to volume: `runpodctl send satellite-paraguay-data < /opt/data/cache.tar.gz`
8. [ ] Document volume ID in `docs/infra/runpod-config.md`

Once these are done, `scripts/queue_train.py` works automatically.

---

## Fallback to Vast.ai (if RunPod blocks payment)

1. Sign up at https://vast.ai
2. Add $10 via crypto (BTC, ETH, USDC)
3. Generate API key
4. Add as `VASTAI_API_KEY` secret
5. Set `GPU_PROVIDER=vastai` env var → `queue_train.py` switches automatically

---

## Files to commit after this decision

- [x] `docs/infra/gpu-decision.md` (this file)
- [ ] `docs/infra/runpod-config.md` (volume ID + API key path)
- [ ] `infra/cost-cap.sh` (Phase 0.3)
- [ ] `scripts/queue_train.py` (Phase 2.1)

---

**Reviewed-by:** Hermes agent (Phase 0.1 of 12-week roadmap)
**Decision deadline:** End of Phase 0 (1 week from start)
**Estimated cost after all phases:** $180-200 (within $200 budget)