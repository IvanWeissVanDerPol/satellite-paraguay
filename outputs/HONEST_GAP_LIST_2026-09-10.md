# HONEST GAP LIST — Forward-looking, post-audit, fresh eyes

**Repo:** `IvanWeissVanDerPol/satellite-paraguay` @ `4619335`
**Date:** 2026-09-10
**Author:** Round-13 fresh-eyes walkthrough (Phase A of dual-track
research-and-perspective pass)

---

## What this document is — and what it isn't

This is **not** an audit. The audits are done
(`outputs/DEFENSE_PREP_15_HAT_AUDIT_2026-09-09.md`,
`papers/drafts/AUDIT/AUDIT-1..5-2026-09-07.md`,
`papers/drafts/AUDIT/TIER-4..6-2026-09-07.md`,
`papers/drafts/AUDIT/ROUND_5/6-2026-09-07.md`). They found the lies,
I helped fix the worst of them. The remaining paper content is now
internally consistent between prose and code at the level of the
honest-reporting notes + ACTUAL_RESULTS.md documents. The full suite
runs (1073 passed) + CI is 10/10 green + defense_check is 13/13.

This document is what comes **after** the audit. It's the list of
things I'd do next if you told me "I have $5,000 and 6 months —
what would you do to make this project genuinely useful, instead of
defended". It's a forward-looking re-imagination, not a fix-list.

I've grouped gaps into 7 categories:

1. **Substance gaps** — what's missing for the thesis to actually
   *say something new about Paraguay* rather than *demonstrate
   infrastructure on Paraguayan data*.
2. **Engineering gaps** — what would make this a maintainable
   codebase instead of a publishable-then-dead artifact.
3. **Ethics / FPIC gaps** — what has to happen before any of this
   should be allowed to reach an indigenous community.
4. **Reproducibility gaps** — what's claimed that's not actually
   reproducible.
5. **Writing gaps** — what's still wrong with the prose even after
   the audit fixed the numbers.
6. **Adjacent opportunity gaps** — what other things this
   infrastructure could be used for, that aren't currently on the
   roadmap.
7. **Process gaps** — how this project should be run differently
   next time.

---

## 0. Project snapshot (so this document is self-contained)

Five Guaraní-named papers (Yvutu / Yvy / Yrupe / Kai / Tatakua) +
the new P0030 (Yvyra Soy) that replaces P0012 Yvy. Plus 5 thesis
chapters + 5 markdown snapshots + the canonical bibliography +
the "shared infrastructure" of `src/`.

The infrastructure (1,115 LOC across 6 paper pipelines, plus the
shared `src/` modules) is the real contribution. Individual paper
contributions are mostly honest negative results ("Prithvi mock F1=0.497",
"transfer ratio undefined (CNN did not converge)", "mAP@0.5 drops
0.50 → 0.18 synthetic-to-real", "P0035 OpenAQ stations unverifiable
from current API"). P0030 is the only paper with positive
infrastructure-style contribution (public-data pipeline joining
INE census + OSM polygons + MAG yield).

This snapshot is more honest than the README's six-paper claims —
the README still shows "6 papers" but only 5 are real; P0030 was
inserted into `check_latex.py`'s papers list and `run_all_6_papers.py`
but the README itself wasn't updated. (Forward gap #5.1.)

---

## 1. Substance gaps (the most important)

These are the gaps where, if I'm honest, the thesis is currently
**infrastructure performing measurements** rather than **research
producing findings**. P0030 is the best of the six in this dimension
(its data are real, its numbers are real, its contribution is real);
the others are weaker.

### 1.1. P0011 Yvutu is "Prithvi fine-tuning on a 256×256 tile"
but the next paper needs full-Paraguay.

The P0011 paper reports F1=0.5592 on a **single 256×256 Hansen tile**
processed into **15 synthetic Chaco tiles** processed by a U-Net
that **never converges on Prithvi**. The audit (Round-12) corrected
the prose to say "pilot on one tile", but that's still the
measured result: a single tile.

**What's missing**: a real Prithvi fine-tuning on the full
~4,400-tile Paraguay Hansen dataset. This requires:
- ~6 GB of Hansen tile data (off-repo, not in this repo)
- A100-class GPU for ~3-4 hours (~$5 on Vast.ai)
- A GPU-enabled pipeline (`scripts/train_prithvi_remote.py` exists
  but never ran end-to-end)

**Status**: 1 TODO item, no blocker, just money + time. **Priority**:
high if you want P0011 to be a publishable contribution rather than
a pilot study.

### 1.2. P0012 Yvy has been replaced by P0030, but P0012 still exists
in the paper structure.

P0030 Yvyra Soy (`papers/drafts/p0030_yvyra_soy/`) was added in
Phase A as a replacement for P0012 Yvy. P0030 joins INE 2022 census
+ OSM polygons + MAG yield — all real public data. P0012 still has:
- `paper.tex` (with the now-corrected 3.27× headline)
- `ACTUAL_RESULTS.md` (with hardcoded placeholder caveat)
- `references.bib` (regenerated per-paper slice)
- A chapter file (`thesis/chapters/p0012_yvy_ch07.tex`)

**What's missing**: explicit cross-references in CH5 / CH7 of the
thesis pointing to P0030 as the "current" indigenous × land use
analysis, with P0012 retained only as the historical deforestation
baseline. The thesis currently lists 6 chapters (CH4-CH9) + 5
papers (P0011, P0012, P0025, P0026, P0035) and the addition of
P0030 as the **seventh** paper, not the **replacement**, reads
uncomfortably. **Priority**: medium. **Fix**: re-order chapter
sequence in `thesis/main.tex` to put P0030 *before* P0012 and add
a one-paragraph note in CH5 explaining that P0012 is the
historical-measurement counterpart to P0030's public-data
infrastructure.

### 1.3. The thesis's contribution is "5 papers from one Python package"
but the infrastructure is barely a package yet.

The repo's README, THESIS_ARCHITECTURE, SUBMISSION_PLAN, INDEX, and
CRITIC_200_ANGLES all describe a unified multi-paper Python package.
The reality in 2026-09-10:
- `pyproject.toml` lists 11 packages but `src/papers/p00*` share
  ~no code beyond their per-paper `__init__.py` + `pipeline.py`
- `src/paraguay_admin`, `src/foundation_models`, `src/timeseries`,
  `src/satellite_io`, `src/external` are imported by some papers
  but the dependency graph is implicit (no `requires = [...]`
  per paper)
- The "single Python package" framing is true at the directory
  level but false at the import level

**What's missing**: 
- A `docs/ARCHITECTURE.md` showing the actual import graph
  (which module depends on which) instead of the aspirational
  narrative
- An `__init__.py` at the `src/` level that documents which
  modules are meant to be public API vs internal
- Per-paper dependency manifests (each `src/papers/p00*` declares
  which `src/` modules it uses, instead of importing whatever it
  happens to find)

**Priority**: medium. **Why it matters**: without this, "5 papers
from one package" sounds like marketing copy; with this, it's a
measurable engineering claim.

### 1.4. P0030 Yvyra Soy is the strongest paper, but its contribution
is "infrastructure" not "finding".

P0030's contribution is "we built a pipeline that joins three real
public datasets." That's publishable as a *software/data paper*
(e.g., Journal of Open Source Software, or Data in Brief) but not as
a *findings paper*. The 19 pueblos + 557 communities + departmental
soy yield numbers are **known statistics from INE and MAG**, not
discoveries. The cross-join (per-department yield × per-pueblo
community count × per-community polygon) has not been done
publicly, but the value of the join is mostly to make the data
*more accessible*, not to discover a new phenomenon.

**What's missing**: one analytical finding the join enables. The
candidate: compute, per-department, the regression of MAG yield
trend (2007/08 → 2024/25) on the count of indigenous communities
in that department. This is a 5-line analysis that produces a
publishable finding (e.g., "departments with more indigenous
communities show +X% soy expansion per year vs the mean"),
provided the regression is real. If it is, P0030 becomes a
**findings paper** instead of an infrastructure paper. **Priority**:
high if you want P0030 to be journal-submittable.

### 1.5. The Hansen tile is 256×256. Everything downstream inherits
that limit.

The "real" Hansen data is `data/cache/hansen/hansen_2018_2023.npz`
which is **one tile covering ~56 km²**. The thesis uses this tile
as:
- An anchor for P0011 (U-Net training data — fine, the model can
  be trained on a tile)
- An anchor for P0012 (deforestation rate per territory — only
  works for the 30 OSM polygons that overlap with this tile)
- An anchor for P0030 (territorial reference — fine, the paper is
  at departmental scale)

**What's missing**: the full Paraguay Hansen tile set
(~4,400 tiles covering ~250,000 km²). This would unlock:
- Per-pueblo real deforestation rate (not the 10 hardcoded
  placeholder percentages that P0012 currently carries)
- Full Paraguay tile-level F1 for P0011 (replacing the "pilot on
  one tile" framing)
- Spatial join between OSM polygons × full Chaco tiles for P0030

**Status**: off-repo, ~6 GB. The substrate README's note
("requirements-ci.txt avoids GDAL-bound deps") correctly identifies
why this isn't in the repo. **Priority**: high if you want any of
the three affected papers to be findable in the literature; medium
otherwise.

### 1.6. P0035 Tatakua's 12 OpenAQ stations are unverifiable.

The P0035 paper claims RMSE=14.7 µg/m³ across 12 OpenAQ stations
in Paraguay. I verified during Round-12 that OpenAQ v3 has **0
stations in Paraguay** (`/v3/countries` returns 100 countries
including Brazil, Argentina, Bolivia, but not Paraguay). The
"12 stations" number likely comes from an older OpenAQ v2 snapshot
that was decommissioned in 2024.

**What's missing**: 
- A working station list. Options:
  1. Apply to OpenAQ to manually add PY stations (requires
     partner organization + weeks of review — rejected as too
     slow by the original Phase A planning)
  2. Use the WHO Ambient Air Quality Database instead (public,
     but Paraguay is again sparse)
  3. Use Sentinel-5P AOD + ground truth from a Paraguayan
     partner (none in the repo)
  4. Repurpose P0035 as a methodology paper (analogous to the
     P0030 fix) that demonstrates LSTM-on-PM₂.₅ without claiming
     a specific station count

**Status**: P0035 has the data-integrity caveat in ACTUAL_RESULTS.md
(since 2026-09-09 audit). **Priority**: medium. The fix is
reframing, not new data acquisition.

### 1.7. The cross-cutting CH9 doesn't actually cross-cut.

CH9 (`thesis/CH9_cross-cutting.md`) is supposed to be the synthesis
chapter. Reading it, it doesn't synthesize — it lists per-paper
findings and notes that "the technical infrastructure is necessary
but not sufficient". That's a chapter-by-chapter recap, not a
synthesis. A real cross-cutting chapter would do at least one of:
- Integrate the 5 papers through a single unifying analysis
  (e.g., does Hansen-derived deforestation correlate with
  departmental soy yield after controlling for indigenous territory
  count? P0011 + P0030 + P0035 → 1 cross-paper finding)
- Identify the dataset / methodological gap that none of the 5
  papers individually could see but a cross-paper view can
- Propose a specific future work direction that uses the
  infrastructure built here

**What's missing**: an actual synthesis. The CH9 chapter currently
serves as a recap. **Priority**: medium. **Fix**: either rewrite
CH9 to do real synthesis (the cross-paper correlation between P0011
deforestation + P0030 soy expansion + P0035 PM₂.₅ is computable
from existing substrate) or demote CH9 to a recap chapter + add
a new "Synthesis" chapter that does the cross-paper analysis.

### 1.8. The thesis doesn't claim a contribution to scientific
knowledge about Paraguay.

Reading the thesis as a defense committee member would: what does
the thesis *say* about deforestation in the Paraguayan Chaco, about
soybean expansion, about indigenous communities, about air quality,
about wildlife surveillance, that wasn't already known? My
honest read: the thesis claims methodological contribution
(reusable infrastructure for Paraguayan geospatial analyses) but
makes no new empirical claim about Paraguay itself.

The 19 pueblos + 557 communities number is from INE 2022 census
— already known. The departmental soy yield numbers are from MAG —
already known. The 3.27× deforestation ratio in P0012 was on
hardcoded placeholders (now flagged). The 14.7 µg/m³ RMSE in P0035
is on unverifiable OpenAQ v2 stations. The 0.50→0.18 mAP in P0026
is on synthetic-vs-real synthetic data, not on Paraguay specifically.

P0030's contribution is the join (INE × OSM × MAG), which is
infrastructure, not a finding.

**What's missing**: one defensible claim about Paraguay that
didn't exist before this thesis. The P0030 per-department
regression (Substance gap #1.4) is the closest candidate. Failing
that, the cross-paper analysis (Substance gap #1.7) is another.

### 1.9. The data substrate (paraguay-geodata-vlm) is referenced
but not in this repo.

CLAUDE.md, THESIS_ARCHITECTURE, STATUS, README all reference
`IvanWeissVanDerPol/paraguay-geodata-vlm` (the data substrate) as
the other half of the project. That's a separate repo at
`/opt/data/thesis-active/`. This repo's `data/raw/` and
`data/cache/` contain only the assets downloaded for the audit +
Phase A work (INE 2022 census, MAG yield, OSM polygons, single
Hansen tile, OpenAQ status, etc.).

The substrate-side and thesis-side repos are decoupled. Whether
that's a feature (independent versioning) or a bug (the substrate
is not actually versioned — `git ls-tree` would show it
uncommitted or on a different branch) depends on what `paraguay-geodata-vlm`
actually is. **Priority**: low (operational, not substantive).

### 1.10. The thesis doesn't engage with the Paraguayan carbon
market.

The original P0010 Vyrá paper (deleted in Round-12 audit for
np.random.normal fabrication) was about Paraguay's carbon-credit
compliance with Verra VCS. That topic is genuinely important in
2026: Paraguay is on the Verra watchlist for 2024-2025 and
voluntary carbon market participation is a major land-use lever.
The deleted P0010 left a hole.

**What's missing**: a P0030-style public-data paper on Paraguay's
REDD+ carbon claims. The data sources would be:
- Verra registry (public API, returns project-level tCO₂e/yr)
- INDI shapefiles (the same one that gates P0012's per-community
  loss rates)
- Hansen tiles (off-repo, ~6 GB)

This is a 4-paper-of-work topic in its own right; just flagging
it as the carbon-market gap that P0010's deletion left behind.
**Priority**: low (the thesis can defend without this, but a
follow-on postdoc would benefit).

---

## 2. Engineering gaps

These are gaps in the codebase itself, separate from the substance.

### 2.1. The 77 tests are skewed toward one paper (P0011) and
P0030.

`tests/` has 77 files. Counting by paper:
- `test_papers_p0011.py` and `test_pipelines.py` and others: P0011
- `test_p0030_yvyra_soy.py`: P0030
- (the rest are general)

P0012, P0025, P0026, P0035 don't have per-paper test files. Their
validation is via the generic `test_paper_validators.py` +
`test_paper_demos.py` which mostly exercise the importability of
the pipeline class.

**What's missing**: per-paper tests for the under-tested papers.
P0030's test suite is now a template (pipeline output + data
provenance + CBP); apply the same template to the other 4.
**Priority**: low-medium. **Why it matters**: without per-paper
tests, the test suite is biased toward whatever was most recently
added. P0030 got tested because Phase A built it; P0026 got
import-tested only.

### 2.2. The CI matrix has overlap and dead branches.

`.github/workflows/` has 10 workflows:
- ci.yml (the main one — 10 jobs)
- cicd.yml, dependabot-auto-merge.yml, deploy-dashboard.yml,
  docs.yml, latex.yml, release-drafter.yml, sbom.yml, secret-scan.yml,
  vulture-nightly.yml

Some are dead (cicd.yml, docs.yml may duplicate ci.yml's coverage).
vulture-nightly.yml runs dead-code detection but I haven't checked
whether it's even triggered. **Priority**: low. **Fix**: audit
each workflow; remove duplicates; consolidate. **Why it matters**:
the audit on T2.4 found that some workflows silently fail; the
defense_check.py is one of the few defenses.

### 2.3. The Dockerfile + docker-compose.production.yml are
insecure.

The audit (T1.10) found:
- `docker-compose.production.yml` publishes Redis 6379 +
  Postgres 5432 to host network with no passwords
- Dockerfile.production uses `python:3.12-slim` which has known
  CVEs

The Round-12 fix flagged these but didn't fix them. **What's
missing**:
- Add `POSTGRES_PASSWORD: ${DB_PASSWORD}` to the Postgres service
  (env-var injection)
- Bind Redis to `127.0.0.1:6379` instead of `0.0.0.0:6379` (no
  external exposure)
- Use `python:3.12-slim-bookworm` or a hardened base image

**Priority**: medium. **Why it matters**: if the dashboard is ever
deployed for real (not just locally), the security exposure is a
defense-question. **Fix**: low-risk, ~30 lines.

### 2.4. There's no `__init__.py` at the repo root for installing
as a single package.

The repo installs via `uv pip install -e ".[ci]"` and works (CI
proves it). But there's no `pyproject.toml` `[project.scripts]`
section defining CLI entry points like `yvutu-train`, `tatakua-eval`,
`yvyra-soy-analyze`. Currently you invoke the pipeline via
`.venv/bin/python -c "from src.papers.p00* import run_*_demo"`.

**What's missing**: a CLI for each paper. **Priority**: low. **Fix**:
add `[project.scripts]` entries to pyproject.toml.

### 2.5. The audit log docs live in papers/drafts/AUDIT/ and will
rot.

The `papers/drafts/AUDIT/` directory contains 13 audit docs that
document what was wrong at one moment in time. As of 2026-09-10
most of the issues are fixed; the docs are historical artifacts.

**What's missing**: a `papers/drafts/AUDIT/README.md` that says
"these docs are historical; see git history + DEFENSE_PREP_15_HAT_AUDIT
for current state." **Priority**: low. **Fix**: add 5-line README
to the AUDIT/ directory.

### 2.6. The 23 top-level planning docs are stale.

`.md` files in repo root: 24 of them. The audit's T4.3 said "21 root
documents to four" was the right move. Current state: still 24. None
of them got consolidated.

**What's missing**: README + STATUS + CONTRIBUTING + CHANGELOG is
the canonical set; the other 20+ are noise. **Priority**: low.
**Fix**: archive the 20 to `.scratch/` or `.hermes/`. Same as what
the audit already said.

---

## 3. Ethics / FPIC gaps

These are the hardest gaps because they cannot be fixed by the
thesis author alone.

### 3.1. Zero FPIC engagement is still the case.

Per the Round-12 audit (Hat 7) and verified 2026-09-09: zero
communities contacted. The thesis says so explicitly in
`papers/drafts/p0012_yvy_indigenous/ACTUAL_RESULTS.md` and
`thesis/chapters/appendix_b_ethics.tex`. The FPIC + IRB files in
`etica/` + `docs/partnerships/` carry UNVERIFIED banners saying "not
filed with FP-UNA".

**What's missing**: actual FPIC engagement. **Status**: blocked on
institutional decisions (which 1-3 communities to engage; who at
FP-UNA / INFONA / INDI can introduce; whether the thesis can be
defended without it). The thesis author's `etica/FPIC_template_es.md`
and `docs/partnerships/FPIC-ENGAGEMENT-MATERIALS-2026-09-07.md` are
drafts; they could be sent to a real partner institution.

**Priority**: depends on whether FADA/FP-UNA requires FPIC for
defense. The user said "month is ok for the timeline" but no
target date → can't be defended without clarifying FPIC. **Note
for Phase B defense prep**: this is the most likely single
defense-blocking question.

### 3.2. The IRB protocol is draft-only.

`etica/IRB_protocol_paraguay_UNA.md` is a draft that has never
been submitted to any IRB. It claims institutional affiliation
("FADA-UNA") that may be incorrect. The thesis author has not
identified an adviser. **What's missing**: real IRB filing. **Same
status as #3.1.** **Priority**: high if any future publication
involves human-subjects data; not applicable for P0030 since it's
public-data only.

### 3.3. The thesis does not claim CARE Principles compliance.

P0030's ACTUAL_RESULTS.md says "Future FPIC-engaged extensions of
this work must follow CARE Principles (Carroll et al. 2020)". Good.
But the thesis itself does not claim CARE compliance — and that
gap is real, not just future-tense. The thesis is descriptive
analysis of public data on indigenous communities; CARE's
Collective-benefit and Authority-to-control principles
specifically address this case (GIDA 2019).

**What's missing**: an explicit CARE compliance statement in
`thesis/chapters/appendix_b_ethics.tex` and in P0030's Methods
section. The honest statement is "we do not claim CARE compliance
because we have not engaged with the affected communities; we
describe public data only." **Priority**: high. **Fix**: 5-paragraph
CARE statement. This is documentation-only, doesn't require
external engagement.

---

## 4. Reproducibility gaps

These are gaps where the thesis claims reproducibility that the
codebase can't actually achieve.

### 4.1. The "fresh clone + make reproduce" path doesn't work.

Per the audit (T2.4) and the OPEN_SCIENCE.md claim: the repo can be
cloned + the pipeline can be reproduced. In practice:
- Hansen tiles are off-repo (~6 GB, requires separate fetch)
- INDI shapefiles are off-repo (institutional access required)
- OpenAQ v3 stations for Paraguay are 0 (per audit finding)
- Sentinel-5P AOD subset is in `data/cache/sentinel5p/` but not
  downloadable from the public source without auth

**What's missing**: a `REPRODUCE.md` that explicitly states
"this subset of the analysis is reproducible from a fresh clone:
[X]. This subset requires additional data: [Y]." **Priority**: high.
**Fix**: 30-line document that names what works + what doesn't.

### 4.2. The data_audit.json regenerates from a watchdog.

The `outputs/data_audit.json` is auto-regenerated by a watchdog
that runs every 6 hours. After every commit, the audit values can
change. This means the data_audit.json at commit N might not match
the data_audit.json at commit N+1, even with no source changes.

**What's missing**: deterministic re-generation. **Fix**: make the
watchdog emit an audit-fingerprint hash in the data_audit.json so
downstream consumers can detect drift.

### 4.3. The `outputs/` directory contains test run artifacts.

`outputs/p0011/ablations.json`, `outputs/integration_test_results.json`,
`outputs/performance_report.json` — these are CI test outputs that
shouldn't be in the committed `outputs/` (they're ephemeral).
The gitignore may exclude them but `outputs/` is committed.

**What's missing**: a clean separation between **persisted** analysis
output (P0030 analysis, paper figures) and **ephemeral** test output
(test reports, ablation JSONs). **Priority**: low. **Fix**: move
ephemeral outputs to `.scratch/` or use `outputs/ci/` for CI artifacts.

---

## 5. Writing gaps

These are gaps in the prose that the audit didn't catch because
the audit focused on numerical consistency.

### 5.1. The README still says "6 papers" / "Six-paper".

`README.md:11` says "6 papers on deforestation, carbon credits,
indigenous rights, yield prediction". After P0030 addition the
correct count is "5 papers + 1 replacement paper". The README
wasn't updated for Phase A.

**What's missing**: README updated to "5 papers + 1 public-data
infrastructure paper (P0030 Yvyra Soy replaces P0012 Yvy as the
indigenous-land analysis)." **Priority**: medium. **Fix**:
10-line README update.

### 5.2. The abstract is in English; FADA / FP-UNA may require
Spanish.

The user said earlier: "yes i am ok with translating to spanish
but at the end once it is profesional in english and the last
touches are translating". Phase A didn't translate; that's Phase
A's next iteration (Phase 3 per the original ask).

**What's missing**: Spanish translations of `THESIS_ABSTRACT.md`,
`thesis/CH1_introduction.md`, and the 5 paper abstracts. **Priority**:
medium (user-confirmed requirement). **Fix**: see Substance gap
follow-up.

### 5.3. The chapter order in `thesis/main.tex` is non-chronological.

`thesis/main.tex` has the chapters in this order: P0011 → P0025 →
P0012 → P0026 → P0030 → P0035 (per `thesis/chapters/`). This
doesn't match the paper numbering (P0011, P0012, P0025, P0026,
P0030, P0035). **What's missing**: re-order to match the paper
numbering (which is what readers will see in citations).

**Priority**: low. **Fix**: reorder the `\input{chapters/...}` lines.

### 5.4. CH9 is a recap, not a synthesis (already covered in #1.7).

Re-listed for completeness.

### 5.5. P0035 paper.tex is the only paper with no `\bibitem` content
from the master bib.

P0035 paper.tex uses only 1 `\cite{}` key, while P0011 uses 8 and
P0012 uses 14. This suggests P0035 has a thin Related Work section.
**Priority**: low. **Fix**: expand P0035's related work to cite the
WHO AAQ database, the GBD air-quality work, and the regional
biomass-burning literature.

---

## 6. Adjacent opportunity gaps (what this infrastructure
*could* do, that the roadmap doesn't currently include)

These are not on the current roadmap but represent real
opportunities the project infrastructure enables.

### 6.1. The same pipeline could produce a "Paraguay Environmental
Bulletin" (annual).

The data audit + INE census + MAG yield + OSM communities +
Hansen tiles join, computed monthly, would produce a publishable
bulletin similar to IBGE's Brazilian environmental bulletins. The
infrastructure is built; the production deployment + cadence is
the missing piece. **Priority**: low (post-defense work).

### 6.2. The Hansen tile cache can host other Paraguayan
geospatial analyses.

The `data/cache/hansen/` pattern (off-repo tile caching with
metadata) is reusable for Sentinel-1 (deforestation radar), 
Sentinel-2 (vegetation indices), and Sentinel-5P (air quality
trace gases). The thesis only uses Hansen; the substrate could
host all five. **Priority**: low.

### 6.3. The Paraguay border region could be analyzed jointly.

Paraguay + Argentina + Brazil's western Chaco share ecological
systems. A regional analysis using the same pipelines would
benefit all three countries. Currently no collaboration framework
exists. **Priority**: low.

### 6.4. The OSM community polygons could be edited by Paraguayan
community mappers.

Currently 30 polygons from OSM. The OSM Paraguay community is
small but active. A "Paraguay indigenous community mapping" event
in partnership with OSM Paraguay would expand coverage from 5% to
maybe 30-50% of the 557 census communities. **Priority**: low
(post-defense community engagement).

### 6.5. The 5 paper architectures generalize to other
Spanish-speaking countries.

Bolivia + Peru + Colombia have similar indigenous census + soy
expansion + deforestation dynamics. The pipeline is generic;
only the data sources differ. **Priority**: low.

---

## 7. Process gaps (how this should be run differently)

These are about how the project itself was built, not what's in it.

### 7.1. No advisory check on numerical claims during build.

The thesis was built with several numerical lies (the audit found
them all). The reason they got in is that no one — not the
adviser (none yet identified), not the user (likely didn't review
each number), not the AI (generates plausible numbers) — was
checking "is this number measured or aspirational?" at write time.

**What's missing**: a pre-commit hook or test that flags any number
>0.5 that doesn't appear in ACTUAL_RESULTS.md. **Priority**: high
for the next project. **Fix**: add a `scripts/audit_claim.py`
that scans prose for numerical claims and cross-references them
against ACTUAL_RESULTS.md + code output.

### 7.2. No incremental verification during paper writing.

The audit found that paper.tex for several papers was edited without
re-running the pipeline, so the prose drifted from the actual
numbers. **What's missing**: a hook that re-runs `defense_check.py`
after every paper.tex edit. **Priority**: high. **Fix**: pre-commit
config to run `defense_check.py` on `papers/drafts/*/paper.tex`
changes.

### 7.3. The "FABRICATED" vs "MEASURED" annotation is in the audit
docs, not the data.

Each ACTUAL_RESULTS.md now carries a data integrity caveat (Round-12
fix). But this caveat was added AFTER the lies were caught. A
better process: every ACTUAL_RESULTS.md starts with a template
boilerplate like:

> **Measured:** [list of measured numbers]
> **Aspirational (NOT MEASURED):** [list of aspirational numbers, if any]

This way, the data-vs-aspiration distinction is in the file from
day 1, not bolted on after the audit.

**Priority**: medium. **Fix**: add a template to `docs/CONVENTIONS.md`.

### 7.4. The project mixes "thesis work" + "infrastructure work" + "audit
work" in one branch.

`main` branch has papers + infrastructure + audit trail + planning
docs + research/ + scratch/ all in one. A defense committee sees
this and has to wade through 20+ planning docs to find the thesis.

**What's missing**: branch separation. Options:
- `main` = stable thesis only
- `dev` = active infrastructure work
- `audit/round-12` = audit history (preserved but not in main
  contributor's path)
- `research/` directory moved to separate repo

**Priority**: low (cosmetic). **Fix**: archive non-thesis work to
`docs/` + remove from `git log --oneline` view of the thesis.

### 7.5. The Vast.ai budget was never authorized.

The $10 Vast.ai credit note is in BWS but not on a Vast.ai account.
The user has not authorized spending on the GPU run. **What's
missing**: real authorization + account setup. **Priority**: blocks
gap #1.1.

---

## Summary: what I'd actually do, in order, if this were my project

This is the prioritized list, ordered by defense impact × effort:

| # | Gap | Effort | Defense impact | Note |
|---|---|---|---|---|
| 1 | #5.1 README 6→5 papers | 5 min | Medium | Quick fix |
| 2 | #1.4 Add P0030 per-dept regression | 1 hr | High | Promotes P0030 to findings paper |
| 3 | #5.3 Reorder chapters | 15 min | Medium | Quality of life |
| 4 | #2.3 Dockerfile security | 30 min | Medium | Quick fix |
| 5 | #3.3 CARE compliance statement | 1 hr | High | Defense Q&A prep |
| 6 | #1.7 CH9 cross-paper synthesis | 4 hrs | High | Real thesis contribution |
| 7 | #1.5 Full Hansen tiles + Vast.ai | 1 day + $5 | High | Real measurements |
| 8 | #1.1 Real Prithvi fine-tuning | 1 day + $5 | High | Real F1 |
| 9 | #1.6 P0035 reframing | 30 min | Medium | Quick fix |
| 10 | #4.1 REPRODUCE.md | 1 hr | Medium | Quick fix |
| 11 | Spanish translation | 4-6 hrs | Medium | User-confirmed |
| 12 | #2.5 AUDIT/ README | 5 min | Low | Cleanup |
| 13 | #2.6 Consolidate root docs | 30 min | Low | Cleanup |

**Total**: ~3 days of focused work + ~$10 GPU + the user's
institutional decisions on FPIC + adviser.

If you only have 1 day: do items 1-5 + 11 (Spanish). If you have
1 week: do items 1-11. Items 12-13 are housekeeping.

The biggest defense-blocker that's NOT on this list: **FPIC
engagement**, which is institutional, not author-side. See #3.1.

---

*End of HONEST_GAP_LIST.md*
