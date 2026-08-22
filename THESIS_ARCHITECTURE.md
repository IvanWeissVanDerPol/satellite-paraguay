# THESIS ARCHITECTURE — Cross-Repo Map

**This document is the canonical map for Iván's 2026-2027 FADA thesis.**
If you're a future agent or human reading either repo, **start here.**

---

## TL;DR

This thesis is a **single research project** spanning **two GitHub repos**:

| Repo | Role | Local path |
|---|---|---|
| **[IvanWeissVanDerPol/satellite-paraguay](https://github.com/IvanWeissVanDerPol/satellite-paraguay)** | **The thesis** — 6 papers, models, measured findings, LaTeX manuscript | `/opt/data/work/satellite-paraguay` |
| **[IvanWeissVanDerPol/paraguay-geodata-vlm](https://github.com/IvanWeissVanDerPol/paraguay-geodata-vlm)** | **The substrate + autonomous runner** — data acquisition pipeline, OSM/IGN/Sentinel-2 download, 87-task autonomous cron, web app demo | `/opt/data/thesis-active` |

**Thesis title (official):** *Multi-Temporal Satellite Computer Vision for Paraguay: A Foundation-Model Approach to Land-Use, Climate, and Environmental Justice*
**Author:** Iván Hocht-VonDerPol (Universidad Nacional de Asunción, FADA)
**Adviser:** Prof. Dr. Juan Carlos Cristaldo (pending co-sign)

The **second repo** (`paraguay-geodata-vlm` / `P1 GeoData v2`) was originally framed as a standalone thesis by the autonomous agent (Erebus, 2026-08-10). After review, we treat it as the **data substrate + autonomous infrastructure** that feeds the main thesis. Both repos share infrastructure (cron jobs, agents, scripts).

---

## Data Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                  paraguay-geodata-vlm                              │
│              (the SUBSTRATE — /opt/data/thesis-active)             │
│                                                                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐               │
│  │ OSM Paraguay │  │ IGN raster   │  │ Sentinel-2  │               │
│  │ 2.46M feats  │  │ tiles        │  │ tiles        │               │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘               │
│         │                 │                 │                       │
│         └────────┬────────┴────────┬────────┘                       │
│                  ▼                 ▼                                │
│        ┌────────────────┐  ┌────────────────┐                       │
│        │ SAM+Grounding  │  │ 100-question   │                       │
│        │ DINO pipeline  │  │ benchmark      │                       │
│        └────────┬───────┘  └────────┬───────┘                       │
│                 │                   │                                │
│                 ▼                   ▼                                │
│        ┌────────────────────────────────────┐                       │
│        │ 10K annotated + web app demo       │                       │
│        │ "Pregúntale al mapa Paraguay"     │                       │
│        └────────────────┬───────────────────┘                       │
└─────────────────────────┼───────────────────────────────────────────┘
                          │
                          │  data + annotations + reproducibility
                          ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    satellite-paraguay                              │
│              (the THESIS — /opt/data/work/satellite-paraguay)        │
│                                                                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐               │
│  │ Hansen GFC   │  │ Prithvi +    │  │ OpenAQ +     │               │
│  │ 30 tiles     │  │ U-Net + YOLO │  │ TROPOMI      │               │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘               │
│         │                 │                 │                       │
│         └────────┬────────┴────────┬────────┘                       │
│                  ▼                 ▼                                │
│  ┌────────────────────────────────────────────────┐               │
│  │ 6 PAPERS (the thesis)                          │               │
│  │  • P0011 Yvutu  (deforestation 16,628 km²)   │               │
│  │  • P0010 Vyrá   (Verra +35.9% under-claim)     │               │
│  │  • P0012 Yvy    (indigenous 3.0× disparity)    │               │
│  │  • P0025 Yrupe  (yield prediction)              │               │
│  │  • P0026 Kai    (wildlife YOLOv8)               │               │
│  │  • P0035 Tatakua (LSTM RMSE 14.7 µg/m³)        │               │
│  └────────────────┬───────────────────────────────┘               │
│                   ▼                                                   │
│  ┌────────────────────────────────────────────────┐               │
│  │ Thesis manuscript (CH1-CH11) + defense prep    │               │
│  └────────────────────────────────────────────────┘               │
└─────────────────────────────────────────────────────────────────────┘
```

**Direction of value flow:** paraguay-geodata-vlm → satellite-paraguay (raw data and reproducibility artifacts feed the papers).

**Reverse direction:** satellite-paraguay publishes finished analysis back to paraguay-geodata-vlm's web app demo.

---

## What goes in which repo (canonical split)

### satellite-paraguay (the THESIS)

| What | Why this repo |
| |
| 6 papers (P0010-P0035) | These ARE the thesis |
| Thesis manuscript (CH1-CH11, 52K words) | The deliverable for FADA defense |
| Trained models (`models/*.pt`) | Reproducible weights |
| Pre-prints, submission package | Journal/arxiv targets |
| Foundational findings (16,628 km², 3.0× disparity, 35.9% under-claim) | Headline results |

### paraguay-geodata-vlm (the SUBSTRATE)

| What | Why this repo |
| |
| 9-dataset manifest | Where the data comes from |
| OSM Paraguay downloader | Data ingestion layer |
| SAM/GroundingDINO/CLIP pipeline | Annotation tooling (not the analysis itself) |
| Web app "Pregúntale al mapa del Paraguay" | Public-facing demo of thesis impact |
| 100-question benchmark | How to evaluate territorial-question-answering |
| 87-task autonomous queue | The agent's daily work |
| Cron infrastructure | Daily tick, weekly review, git maintenance |

### Shared infrastructure (lives in `~/.hermes/scripts/`)

| Component | Used by |
| |
| Cron daemon (49 jobs total) | Both repos' autonomous agents |
| `thesis-active-autonomy` skill | Loads on resume in either repo |
| `aiw-thesis-tracker` agent | Weekly brief on both repos |
| Storage layer (`/opt/data/state/`) | Cross-agent memory |

---

## Cron jobs that span both repos

These are scheduled in `~/.hermes/scripts/` via `hermes cron create`:

| Cron job | Schedule | Repo it works on | What it does |
|---|---|---|---|
| `thesis-daily-tick` | 06:00 UTC daily | **paraguay-geodata-vlm** | Picks next P0 task from `TASK_QUEUE.md`, executes, marks done, logs |
| `thesis-weekly-review` | Sun 18:00 UTC | **paraguay-geodata-vlm** | Computes weekly stats, writes summary |
| `thesis-git-maintenance` | Sun 23:00 UTC | **paraguay-geodata-vlm** | gc + prune + reflog |
| `thesis-watchdog` | every 15m | **paraguay-geodata-vlm** | Detects stalled ticks, alerts |
| `aiw-thesis-tracker-daily` | 16:00 UTC daily | **both** (cross-repo brief) | Writes weekly brief covering both repos |

The **first four** are pinned to `paraguay-geodata-vlm` (workdir `/opt/data/thesis-active`). The **last** is an agent prompt that reads state from both.

---

## State that lives across the boundary

Three state files act as the cross-repo "memory bus":

| File | Owner | Read by |
| |
| `/opt/data/state/org-state.json` | `aiw-management-coord-biwk` cron | `aiw-thesis-tracker` agent, humans via dashboard |
| `/opt/data/thesis-active/PROGRESS.md` | `autonomous_tick.py` | Humans via `git log`, agents via resume |
| `/opt/data/work/satellite-paraguay/STATUS.md` | Manual update after CI passes | Submission reviewers, defense committee |

When `aiw-thesis-tracker-daily` runs, it reads:
- `STATUS.md` → paper scorecard (P0010-P0035 metrics, ethics)
- `PROGRESS.md` → what substrate ran today
- `MASTER_PLAN.md` → 26-week shipping calendar
- `thesis/CH9_cross-cutting.md` → cross-paper findings

---

## Documents that **must stay synchronized**

When one changes, the other should too. These are the cross-reference docs:

| Topic | In satellite-paraguay | In paraguay-geodata-vlm |
| |
| **Thesis title** | `THESIS_ABSTRACT.md` | `FORMAL_PROPOSAL.md` |
| **Status snapshot** | `STATUS.md` | `PROGRESS.md` |
| **Headline findings** | `README.md` (TL;DR table) | `THESIS_SUMMARY.md` |
| **Roadmap** | `docs/12-week-roadmap-2026-Q3.md` | `MASTER_PLAN.md` (autonomous 30-day) |
| **Def**" | `DEFENSE_PLAN.md` | (substrate side has none yet — gap) |
| **References** | `references.bib` (182 entries) | `REFERENCES.bib` (24 entries, starter) |

**Rule**: when you update a sync doc in one repo, run a quick `grep` in the other for the same keyword and update the matching entry.

---

## How to read each repo (orientation)

If you're new to one repo:

1. **Start here**: this file (`THESIS_ARCHITECTURE.md`)
2. **Then the local README**:
 - satellite-paraguay: `README.md` → TL;DR table of 8 findings, then per-paper summary
 - paraguay-geodata-vlm: `README.md` → document reading order table
3. **Then the state file**:
 - satellite-paraguay: `STATUS.md` → per-paper scorecard + per-axis definitions
 - paraguay-geodata-vlm: `PROGRESS.md` → chronological tick history
4. **Then the canonical plan**:
 - satellite-paraguay: `docs/12-week-roadmap-2026-Q3.md`
 - paraguay-geodata-vlm: `TASK_QUEUE.md` + `MASTER_PLAN.md`
5. **Then the thesis itself**:
 - satellite-paraguay: `thesis/` (CH1-CH11), `papers/drafts/P00*/paper.tex`
 - paraguay-geodata-vlm: `CAPITULOS/` (work in progress)

---

## Key dates and milestones

| Date | Event | Source repo |
|---|---|---|
| 2026-07-22 | Hansen data acquisition started | satellite-paraguay |
| 2026-07-31 | `thesis-research` repo: 1439-idea decision atlas created | thesis-research |
| 2026-08-01 | `satellite-paraguay` repo created on GitHub | satellite-paraguay |
| 2026-08-03 | `THESIS_SUMMARY.md` documents 6 paper drafts + infra in one session | satellite-paraguay |
| 2026-08-10 | `paraguay-geodata-vlm` repo created on GitHub (= `P1 GeoData v2`) | paraguay-geodata-vlm |
| 2026-08-10 | First autonomous tick runs (T025-T028) | paraguay-geodata-vlm |
| 2026-08-13 | CI green-build pass on satellite-paraguay (1006 pytest pass, mypy strict) | satellite-paraguay |
| 2026-08-15 | Roadmap written for satellite-paraguay (12-week plan) | satellite-paraguay |
| **2027-08 (target)** | **Thesis defense at FADA** | satellite-paraguay |

---

## Anti-patterns (don't do these)

1. **Don't treat them as separate theses.** They aren't. The thesis title is in satellite-paraguay's `THESIS_ABSTRACT.md`. If you find yourself writing a defense chapter in paraguay-geodata-vlm, stop — it belongs in satellite-paraguay.

2. **Don't reference one repo without the other.** Any doc that mentions "thesis" must mention both. If you see a doc that talks about only one, that's a sign it predates the cross-reference architecture update (2026-08-15).

3. **Don't push data directly across repos.** The substrate repo downloads, processes, and exposes. The thesis repo reads, analyzes, and publishes. Don't `git pull` data from one to the other; use a shared storage path (`/opt/data/thesis-active/data/raw/`) that satellite-paraguay imports via `pyproject.toml` extras.

4. **Don't create cron jobs in satellite-paraguay's CI.** Substrate cron jobs go in `~/.hermes/scripts/` via `hermes cron create`. The thesis repo's CI is for paper compilation, lint, tests — not autonomous tickers.

5. **Don't conflate the THESIS title with the SUBSTRATE title.** The substrate was pitched as "P1 GeoData v2" — that's the old working name. The thesis title is "Multi-Temporal Satellite Computer Vision for Paraguay". They are NOT interchangeable.

---

## How to extend this doc

When you add a new artifact that crosses the boundary (a new paper, a new dataset, a new autonomous task, a new defense slide):

1. Add it to the **right table above** (substrate vs thesis)
2. Add the **cron** that produces/uses it (if any)
3. Add the **state file** it reads or writes
4. Update the **sync docs** in both repos
5. Commit this `THESIS_ARCHITECTURE.md` to both repos with the same content

Last updated: 2026-08-15
Maintained by: Hermes agent (cross-repo architecture review)