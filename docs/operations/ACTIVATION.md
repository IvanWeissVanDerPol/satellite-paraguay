# ACTIVATION — One-page operator guide

**Audience:** Iván Hocht-VonDerPol
**Goal:** Get the 12-week thesis roadmap + funding pipeline running
**Time:** 1.5 hours total (spread over 1 week)
**Cost:** $0 (5 free grant applications)

---

## Step 1: Apply to 4 Tier S programs (45 min)

1. **NVIDIA Inception** (15 min) — https://www.nvidia.com/en-us/startups/
   - Open `docs/operations/applications/01-nvidia-inception.md` and copy-paste
2. **Modal Startups** (15 min) — https://modal.com/startups
   - Open `docs/operations/applications/02-modal-startups.md` and copy-paste
3. **Cloudflare for Startups** (10 min) — https://www.cloudflare.com/startups/
   - Open `docs/operations/applications/03-cloudflare-startups.md` and copy-paste
4. **AWS Activate** (20 min) — https://aws.amazon.com/startups/credits/
   - Open `docs/operations/applications/04-aws-activate.md` and copy-paste

**After each application:** update the checkbox in `funding-applications.log`:
- `- [ ] **NVIDIA Inception** ...` becomes `- [S] **NVIDIA Inception** ...`

## Step 2: Email Prof. Cristaldo (30 min)

Subject: "Solicitud de FADA Research Grant — SatelliteCV-Paraguay 2026"

Body:
```
Estimado Prof. Cristaldo,

Me permito escribirle para informarle sobre el avance de mi
trabajo de tesis "Multi-Temporal Satellite Computer Vision for Paraguay"
y solicitar su apoyo para el FADA Research Grant anual.

Resultados medidos a la fecha (ver STATUS.md en el repo):
- Forest loss 2001-2023: 16,628 km2 (Hansen GFC)
- Indigenous disparity: 3.0x national rate, p<0.001
- Verra carbon credit under-claim: 35.9% mean
- Air quality LSTM: RMSE 14.7 ug/m3 (real OpenAQ data)

6 papers en submission-readiness. CI green: 1006 tests pass.
Plan completo: docs/COMPLETE-PLAN.md en el repo.

Solicito su apoyo para:
1. Carta de recomendacion para FADA Research Grant
2. Confirmar su disponibilidad como adviser en el FADA grant
3. Sugerencias de partnerships institucionales (INBIO, INDI, etc.)

Plazo: FADA grant cierra en febrero. Idealmente completar
application antes de fin de mes.

Quedo a su disposicion para una reunion cuando le sea conveniente.

Atentamente,
Ivan Hocht-VonDerPol
Maestria en Tecnologia de la Arquitectura
FADA - Universidad Nacional de Asuncion
```

Send to: cristaldo@example.com (replace with actual)

## Step 3: Verify everything is in place (1 min)

```bash
# Check the 4 new crons are active
hermes cron list | grep -E "funding|drift|security"

# Check the funding log shows 4 [ ] boxes
cat /opt/data/work/satellite-paraguay/docs/operations/funding-applications.log

# Run the drift detector once to verify
cd /opt/data/work/satellite-paraguay
.venv/bin/python scripts/drift-detector.py --json | head -20
```

## Step 4: Wait + monitor (the agent handles this)

| Cron | Schedule | What happens |
|---|---|---|
| `aiw-funding-daily-check` | every 6h | Silent unless alert |
| `aiw-funding-weekly-sweep` | Mon 09:00 PYT | Discovers + drafts new programs |
| `aiw-drift-detector-weekly` | Mon 12:00 UTC | STATUS.md vs snapshot |
| `aiw-security-audit-biweekly` | every other Fri | TDD-shaped threat audit |

You will receive **1 weekly brief** (Mondays) with `[NEW]`, `[IN-FLIGHT]`, `[DECIDED]`, `[NEXT-ACTIONS]`.

If a Tier S program is approved within 1-2 weeks, the agent will alert you in origin chat immediately.

## What happens after approval (weeks 5+)

1. Activate approved GPU credits (NVIDIA / Modal / Cloudflare / AWS)
2. Run `bash infra/cost-cap.sh --snapshot` (initial baseline)
3. Trigger `make reproduce-paper P=P0011` for Prithvi fine-tune
4. Continue Phase 2.2 (GPU training) per docs/12-week-roadmap-2026-Q3.md

---

## Files referenced

| File | What |
|---|---|
| `docs/operations/FUNDING_PLAN.md` | The 4-path strategy (read this first if confused) |
| `docs/operations/funding-applications.log` | Tracker (check off as you apply) |
| `docs/operations/applications/01-04*.md` | Pre-drafted cover letters (copy-paste) |
| `docs/COMPLETE-PLAN.md` | The 12-week roadmap master doc |
| `docs/12-week-roadmap-2026-Q3.md` | Original timeline |

---

**Status:** READY TO ACTIVATE
**Next action:** Open the 4 application URLs above and submit (45 min total).
**Expected outcome:** $300K+ in GPU + cloud credits within 1-2 weeks.
