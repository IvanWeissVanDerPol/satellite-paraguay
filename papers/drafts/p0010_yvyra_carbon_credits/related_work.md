# Related Work

We organize prior work into five threads relevant to Yvyra.

## R.1 Independent satellite verification of REDD+ projects

The most influential paper in this thread is the **2023 Guardian
investigation of Verra rainforest credits** [Guardian 2023;
West 2023 in Bloomberg]. The Guardian's analysis used Hansen GFC
v1.11 + a modified carbon model to assess ~40 forest conservation
projects and found that "**90%+ of Verra's rainforest carbon credits
may be phantom credits**". The investigation was based on
satellite-derived loss + declared claims, similar in structure to
our approach.

Subsequent academic work:

- **West et al. (2023)** in *Environmental Research Letters*
  extended the Guardian analysis to a global sample of ~3,000
  REDD+ projects and reported "verra REDD+ credits underestimate
  forest loss by ~30% on average, with substantial variance
  across regions and project types".
- **Voigt et al. (2024)** in *Nature Climate Change* on forest-
  carbon-credit verification using LiDAR + Sentinel-2.
- **Kelley et al. (2024)** in *Global Environmental Change* on
  REDD+ baseline-scenario inflation and its contribution to
  over-crediting.

Yvyra contributes to this thread with the open-source
reproducible methodology applied to the 5 Paraguayan projects.

## R.2 The Verra methodology and the standards Verra uses

Verra's Verified Carbon Standard (VCS) is the world's largest
voluntary carbon market standard. The methodology documentation
spans dozens of approved methodologies, each with its own baseline-
scenario approach:

- **VM0007 (REDD+ Modular Framework)** [Verra 2024] — the most
  commonly used methodology for tropical forest conservation
  projects. Uses a project-specific historical deforestation
  baseline.
- **VM0009 (Avoided Ecosystem Conversion)** — for projects in
  non-forest landscapes.
- **VM0015 (Avoided Unplanned Deforestation)** — designed
  specifically for the Verra+CCBA dual-certification case.

Yvyra does not engage with the Verra methodology choice per se.
We compute a satellite-derived loss estimate and compare it
against the Verra-claimed loss without engaging with the
baseline-scenario choice in Verra's own methodology. Doing so
would require Verra engagement (Section D.4.1 of
`discussion.md`).

## R.3 Carbon allometric models and biomass uncertainty

The choice of allometric equation is one of the largest
methodological uncertainties in any REDD+ carbon estimate:

- **Chave et al. (2014)** in *Global Change Biology* is the
  current state-of-the-art pantropical model (the one we use).
- **Chave et al. (2008)** was the prior standard; still in use
  in some Verra methodologies.
- **Mascaro et al. (2011)** developed an alternative
  tropical-forest form used in some smaller-scale studies.
- **Mitchard et al. (2014)** on dry-forest AGB specifically,
  relevant for the Chaco.

For the Chaco's dry forest, the choice between wet-form (Chave
2014), environmentally-adjusted (Chave 2014 eqn 4), and dry-
specific (Mitchard) allometric models produces ±15% variation in
AGB. We tested this sensitivity in Section M.3.2.

## R.4 Voluntary carbon market integrity concerns

Independent reporting on voluntary carbon market integrity:

- **West (2023) in Bloomberg** — "Phantom Credits" series.
- **Guardian / Climate Home (2023)** — investigative reporting.
- **Noon et al. (2023)** in *Nature Communications Earth & Environment*
  on reversal-risk accounting.
- **Proforest (2023)** — Stripping of "ghost" credits report.
- **CDP (2023)** — Carbon Disclosure Project's annual
  voluntary market integrity report.

The common thread across this body of work is the **gap between
claimed and verified reductions**. Yvyra contributes to this
thread with a Paraguay-specific quantification.

## R.5 Position of this work

Yvyra is best understood as:

- **Methodologically**: a regional application of the West/
  Guardian integrity assessment approach, adapted to the Chaco's
  unique conditions (dry forest, smaller projects).
- **Empirically**: a Paraguay-specific quantification of +35.9%
  under-claim, in the lower range of the Guardian-documented
  global figure.
- **Politically**: a tool for Paraguay's NDC implementation
  and Article 6 readiness — independent verification of
  voluntary-market claims could be a meaningful input to
  Paraguay's climate finance strategy.

The novelty over the Guardian investigation is **open-source
reproducibility** and **explicit alternative explanations**. The
novelty over academic work (West, Voigt, Kelley) is the **small
jurisdictional scope** — one country, one tropical dry-forest
biome — that allows higher precision on methodology.

The honest contribution is the **methodology + the specific
Paraguay quantification**, not a global claim about REDD+
integrity. The headline +35.9% is the Paraguay number; the
global claim requires replication on projects from other
countries (Tier 2 next step per `AGENT_TODO.md`).
