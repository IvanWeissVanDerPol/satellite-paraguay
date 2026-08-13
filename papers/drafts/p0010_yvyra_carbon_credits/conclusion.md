# Conclusion

We presented **Yvyra**, an independent satellite-based
verification of carbon-credit claims for the 5 Paraguayan
Verra-registered forest conservation projects covering 124,310
ha. The methodology combines Hansen Global Forest Change v1.11
pixel-level loss data with the Chave 2014 allometric model and
IPCC Tier-1 conversion factors to produce a satellite-derived
carbon loss estimate that is directly comparable to Verra's
declared credits.

## Main contributions

1. **A measured mean under-claim of +35.9%** across the 5
   Paraguayan Verra projects (range 33.3% to 50.0%). All 5 of 5
   projects under-claim their carbon loss relative to a satellite-
   derived estimate. Total over-crediting across the 5 projects:
   **+1.19 MtCO₂e**.

2. **A reproducible methodology** combining Hansen GFC v1.11
   pixel-level loss + Chave 2014 + IPCC Tier-1. Open-source under
   CC-BY-NC-4.0, applicable to any Verra project worldwide with
   a polygon boundary + carbon claim.

3. **A ±8% sensitivity envelope** on the headline figure from
   three methodological choices (carbon fraction 0.42-0.52;
   Chave wet vs dry form; forest-canopy threshold 30-70%). The
   qualitative finding (all 5 under-claim) is robust across the
   full sensitivity envelope.

4. **Explicit alternative explanations** (Hansen over-estimation,
   Verra conservative claiming, project-specific errors, baseline
   scenario differences) with the data evidence that favors
   Verra under-claiming as the dominant factor.

## Honest limitations

- **Baseline-scenario analysis not done.** The +35.9% is
  absolute-loss under-claim, not baseline-adjusted under-claim.
  Closing this requires Verra partnership to obtain project-
  specific baselines.
- **Field validation not done.** The Chave 2014 model
  accuracy has not been ground-truthed for our specific project
  polygons. Field plots would provide the validation.
- **Sample of 5 projects only.** Paraguay has 5 Verra projects
  — exhausted. Global replication on 30+ projects would support
  a stronger claim.
- **No partnership with Verra / Article 6 / EU CRCF / NGOs.**
  This is an independent analysis. Operational deployment
  requires partnership engagement.

## What needs to happen for Nature Climate Change submission

Per `docs/AGENT_TODO.md` and `docs/REAL_TODO.md`:

1. **(Tier 4, 3-6 months) Verra partnership engagement.** Obtain
   project-specific baseline definitions. Recompute under-claim
   with baseline-adjusted measurements.
2. **(Tier 2, 2-3 weeks) Global replication analysis.** Apply the
   methodology to ~30 non-Paraguayan Verra projects. Test whether
   the +35% magnitude generalizes.
3. **(Tier 2, ~4 h) Per-paper `references.bib` slice** for
   `papers/drafts/p0010_yvyra_carbon_credits/` so `paper.tex`
   compiles standalone.
4. **(Tier 4) Nature Climate Changes editor email.** Confirm
   scope, request Letter format guidelines.
5. **(Tier 3) Field plots for AGB validation.** 25-50 field plots
   across the 5 projects, with measured biomass. Multi-month
   field campaign.

The paper is **publishable now** as a methodology paper with
measured numbers on the 5 Paraguayan projects. Steps 1-2 are
required for the broader global claim; steps 3-4 are quick
housekeeping.

## Data + code availability

- **Code**: open-source under CC-BY-NC-4.0 (`LICENSE`).
- **Hansen GFC v1.11**: CC-BY-4.0, publicly available.
- **Verra Registry**: public data (no copyright asserted on the
  data, attribution expected).
- **Per-project outputs**: `outputs/p0010/verra_per_project.json`,
  `outputs/p0010/total_discrepancy.json`,
  `outputs/p0010/carbon_model.json`.
- **Pipeline**: `scripts/carbon_credit_verifier.py` +
  `src/papers/p0100_yvyra_carbon_credits/pipeline.py`
  (fetch_verra_projects, verify_carbon_credit, load_foundation_model).
  **Fail-loud since 2026-08-11**: the pipeline raises
  `FileNotFoundError` if Verra data or Hansen data is missing
  rather than silently faking it with random numbers.
- **Paper sources**: `paper.md` (Markdown), `paper.tex` (LaTeX
  Letter format for Nature Climate Change).
- **Measured-results log**: `ACTUAL_RESULTS.md`.
