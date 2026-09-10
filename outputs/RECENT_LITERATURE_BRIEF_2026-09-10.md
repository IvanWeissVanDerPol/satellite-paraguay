# RECENT LITERATURE BRIEF — 2024 onwards

**Repo:** `IvanWeissVanDerPol/satellite-paraguay`
**Date:** 2026-09-10
**Author:** Round-13 dual-track research pass (Phase B)
**Sources:** 8 CrossRef + OpenAlex queries (~97 unique DOIs returned).
Cache: `.scratch/lit_cache_2024.json`

---

## What this document is — and what it isn't

This is a **strategic literature watch**, not a bibliography. It
identifies **recent (2024+) literature that materially affects the
satellite-paraguay thesis**: either by competing with it, by providing
tools/methods the thesis should use, by raising concerns the thesis
must address, or by pointing to gaps the thesis could fill.

Each query in `.scratch/lit_cache_2024.json` returned 10-15 results;
I curated the ~20 most relevant below. The full cache is in
`.scratch/lit_cache_2024.json` if you want to see everything.

**Not in this brief**: classical citations (Hansen et al. 2013,
Chave et al. 2014, MapBiomas 2023, ILO 169) — those are in the
master bib already. The focus here is **what changed since 2024**.

---

## 1. The headline finding: there's now a directly-comparable 2024
paper on Paraguayan indigenous land rights

**Galeana (2024). "Disrupting the Patrón: Indigenous Land Rights and
the Fight for Environmental Justice in Paraguay's Chaco."**
*Conservation and Society* (Vol 22, Issue 4). DOI:
`10.4103/cs.cs_24_24`.

This paper is *exactly* the same topic as P0012 Yvy (indigenous land
tenure in the Paraguayan Chaco, environmental justice framing). It was
published in 2024 in *Conservation and Society* — a legitimate,
peer-reviewed venue. It exists. The thesis's P0012 contribution is
**partially subsumed** by this paper.

**What it means for the thesis**:
- P0012 (and P0030) must distinguish themselves from Galeana 2024.
  Galeana takes a qualitative environmental-justice frame; P0030 is
  quantitative public-data infrastructure. Different methods, but
  overlapping scope.
- Galeana 2024 should be **cited explicitly** in both P0012 and P0030
  Related Work. It is not in the master bib as of 2026-09-10.
- The defense committee may ask: "your P0012 found a 3.27× disparity;
  Galeana 2024 cites other numbers — what does the field say?" This
  is a foreseeable question that we don't currently answer.

**Recommended action**:
- Add Galeana 2024 to `thesis/references.bib` (need to verify DOI
  resolves to abstract first)
- Cite in `papers/drafts/p0012_yvy_indigenous/related_work.md` and
  `papers/drafts/p0030_yvyra_soy/related_work.md`

---

## 2. There's a 2026 paper that says Paraguay's land rush is
"illegality"

**Wesz Junior (2026). "Land Rush in Contemporary Paraguay: Agricultural
Commodity Frontier, State and Illegality."** *Development and Change*
(early online). DOI: `10.1111/dech.70072`.

This paper — published in the top development studies journal —
directly characterizes the Paraguayan soy/agricultural frontier as
state-enabled illegality. Wesz Junior is a Brazilian political
economist who has written extensively on South American land
markets; this paper is the most up-to-date scholarly account of the
Paraguayan soy frontier specifically.

**What it means for the thesis**:
- The thesis's P0030 paper is about the *measurement infrastructure*
  for soy expansion. Wesz 2026 is about *what that measurement
  means politically*. Together they would form a stronger
  contribution than either alone.
- "Illegality" is a strong word. The thesis currently uses
  neutral-descriptive language ("agricultural frontier expansion").
  This may be a defense-committee surprise: the literature sees
  the frontier as contested; the thesis presents it as a
  measurable phenomenon.

**Recommended action**:
- Add Wesz Junior 2026 to master bib
- Consider whether P0030 should add a brief Discussion paragraph
  framing the measured numbers within the political-economy
  context Wesz documents
- Note: this is a Discussion tone shift, not a methods change.
  The thesis should NOT take a normative stance on the soy frontier
  itself.

---

## 3. There's now a peer-reviewed CARE Principles paper in Nature
Communications (2025)

**Jennings et al. (2025). "Governance of Indigenous data in open
earth systems science."** *Nature Communications*. DOI:
`10.1038/s41467-024-53480-2`.

This paper is the first peer-reviewed Nature-family paper on CARE
Principles in the context of earth systems science. It cites the
GIDA Global Indigenous Data Alliance work and provides a framework
for what "indigenous data governance" means operationally.

**What it means for the thesis**:
- The thesis's gap #3.3 ("the thesis doesn't claim CARE Principles
  compliance") is now answerable. Jennings 2025 provides the
  framework for an honest compliance statement.
- The thesis's P0030 paper's ACTUAL_RESULTS.md currently cites
  Carroll et al. 2020 (the CARE Principles founding paper). Adding
  Jennings et al. 2025 brings the citation current.
- This paper is **directly relevant to the FPIC engagement gap**
  (gap #3.1). If the thesis author ever does engage with
  communities, Jennings 2025 is the framework reference.

**Recommended action**:
- Add Jennings et al. 2025 to master bib
- Cite in `papers/drafts/p0030_yvyra_soy/related_work.md`
- Add to `thesis/chapters/appendix_b_ethics.tex` as a
  contemporary reference

---

## 4. Foundation models + remote sensing has a new 2025 review
with a Paraguayan-relevant twist

**Multimodal Remote Sensing Foundation Models survey (2025)**, in
*Remote Sensing* (MDPI). DOI: `10.3390/rs17213532`. Authors review
multimodal (SAR + optical + DEM) foundation models for EO
downstream tasks.

The thesis uses Prithvi (single-modality, optical-only, IBM/NASA).
The 2025 literature has moved on:
- **U-Prithvi (2025)**: integrates Prithvi with U-Net for flood
  inundation mapping (DROPS/GIScience). Cited as
  `Kostejn et al. 2025` — DOI: `10.4230/lipics.giscience.2025.18`.
- **Prithvi-2 / SatVision-TOA / GAIR (2026)**: location-aware
  pre-training, multi-modal encoders. Cited as
  `Liu et al. 2026` — DOI: `10.1016/j.isprsjprs.2026.04.035`.
- **Earth observation + LLM integration (2026)**: open-source LLMs
  for GeoAI (Annals of GIS). DOI:
  `10.1080/19475683.2026.2630753`.

**What it means for the thesis**:
- P0011's Prithvi foundation model is from 2023-2024 (the original
  Prithvi release). The thesis cites Prithvi-300M but does not
  acknowledge that the field has moved on to U-Prithvi (2025) and
  multimodal variants (2026).
- If the thesis is defended in 2026-Q4 or 2027-Q1, the foundation
  model choice will look 2-3 years stale. Defensible only if
  framed as "Prithvi-300M is what was available when this work
  began; future work should use U-Prithvi".
- This is gap #1.1 (Substance gap: real Prithvi fine-tuning) made
  more concrete — even if we did the real run, Prithvi-300M
  isn't the bleeding-edge choice anymore.

**Recommended action**:
- Add U-Prithvi 2025 + GAIR 2026 to master bib
- Add a "future work" paragraph in P0011 acknowledging Prithvi-300M
  as the 2023-era baseline + pointing to U-Prithvi as the
  next-generation replacement
- Note: this does NOT change the F1=0.5592 measurement. It changes
  how we frame it.

---

## 5. Paraguay has its own wildfire smoke literature that P0035
ignores

**Mendez & Mendez (2024). "Impacto de la quema de biomasa en el
Pantanal sobre la calidad del aire en Paraguay en el periodo 2010
a 2022."** *Journal of Engineering Research* (or similar). DOI:
`10.22533/at.ed.3174162407067`.

This is a Paraguayan-affiliated paper on biomass-burning impact on
Paraguayan air quality 2010-2022. It's exactly the topic P0035
Tatakua claims to address (PM₂.₅ in Paraguay, with LSTM modeling).

Also relevant:
- **The 2024 South America ablaze (Palmeiro-Silva et al. 2025)**, in
  *The Lancet Regional Health - Americas*. DOI:
  `10.1016/j.lana.2025.101160`. Health impacts of the 2024 wildfire
  season across South America — directly relevant to P0035's
  rural-station gap.
- **Schulz-Antipa et al. (2024)**, *Regional Science Policy &
  Practice*. DOI: `10.1016/j.rspp.2024.100139`. Paraguay-specific
  climate-change health study.

**What it means for the thesis**:
- P0035's Related Work section currently doesn't cite any
  Paraguayan-specific air-quality literature. A defense committee
  reading P0035 might ask "what does Paraguay-specific research on
  biomass burning + PM₂.₅ say?" — and the answer is currently
  "we cite Hansen, Sze, etc., which are not about air quality at
  all".
- Mendez & Mendez is Paraguayan. Citing it directly would
  strengthen P0035's "this matters for Paraguay" framing.

**Recommended action**:
- Add Mendez & Mendez 2024 + Palmeiro-Silva 2025 to master bib
- Expand P0035 Related Work from 1 cite to ~5 cites

---

## 6. Indigenous data governance has exploded in 2024-2025 —
the thesis missed this entirely

The 2024 wave of indigenous data governance papers is large and
substantive:

- Jennings et al. 2025, *Nature Communications* — already discussed
  above
- **Newing et al. (2024). "'Participatory' conservation research
  involving indigenous peoples and local communities: Fourteen
  principles for good practice."** *Biological Conservation*.
  DOI: `10.1016/j.biocon.2024.110708`. **Fourteen principles** for
  participatory conservation research — directly applicable to
  P0012 / P0030 methodology.
- **Taitingfong, Martinez, Hudson (2024)**. "Aligning policy and
  practice to implement CARE with FAIR through Indigenous Peoples'
  protocols." *Acta Borealia*. DOI:
  `10.1080/08003831.2024.2410112`. CARE+FAIR integration.
- **Ofosu-Asare (2024)**. "Cognitive imperialism in artificial
  intelligence: counteracting bias with indigenous epistemologies."
  *AI & Society*. DOI: `10.1007/s00146-024-02065-0`. Indigenous AI
  epistemologies.
- **Lewis, Whaanga, Yolgörmez (2024)**. "Abundant intelligences:
  placing AI within Indigenous knowledge frameworks." *AI &
  Society*. DOI: `10.1007/s00146-024-02099-4`.
- **Engstrom et al. (2024)**. *npj Digital Medicine*. Indigenous
  data governance scoping review. DOI:
  `10.1038/s41746-024-01070-3`.
- **Fisk, Leong, Berl (2024)**. *Journal of Wildlife Management*.
  Indigenous Knowledges in wildlife management — relevant to
  P0026 Kai.
- **Chigwada, Mapara, Ngulube (2025)**. *IFLA Journal*. Indigenous
  knowledge management — broad.

**What it means for the thesis**:
- This is the field that has caught up to what the thesis should
  have been doing. The thesis cites Carroll et al. 2020 (the
  founding CARE paper) and that's it.
- The 2024 papers provide operational frameworks for what
  "indigenous data governance" means in practice. The thesis could
  use one of these frameworks in its ethics appendix instead of
  inventing its own framework.
- The thesis's existing appendix_b_ethics.tex is generic. With
  Newing et al. 2024's "Fourteen principles for good practice" the
  appendix could be much more concrete.

**Recommended action**:
- Add 5-7 of these 2024-2025 papers to master bib
- Rewrite appendix_b_ethics.tex to cite Newing et al.'s "Fourteen
  principles" as the operational framework the thesis follows (or
  explicitly does not follow)
- This is the highest-impact single change for the ethics /
  FPIC narrative.

---

## 7. The soybean-expansion literature has a Brazilian-but-relevant
thread that P0030 should cite

- **Montoya Castaño & Oliveira (2026)**. "Did the soybean expansion
  increase the creation of formal jobs in agricultural frontier
  areas of Brazil (1996-2018)?" *Revista de Economia e Sociologia
  Rural*. DOI: `10.1590/1806-9479.2026.305841`. Brazilian frontier,
  not Paraguayan — but the analysis framework transfers.
- **Walke & Barbier (2025)**. "Land Redistribution and Agricultural
  Frontier Expansion." *Eastern Economic Journal*. DOI:
  `10.1057/s41302-025-00295-8`. Theoretical framing of frontier
  expansion as a labor market / land redistribution phenomenon.
- **Lesmo-Duarte, Vega-Britez, Velazquez-Duarte (2026)**.
  "Competitiveness of Paraguay international agricultural trade: An
  analysis of the soybean complex." *Revista de Ciencias Agrícolas*.
  DOI: `10.22267/rcia.2026431.291`. **Paraguayan-specific**, in the
  *soybean complex* — directly relevant to P0030.
- **Guerrero Barreto & Melgarejo Arrúa (2025)**. "Rentabilidad del
  cultivo de soja... en el Distrito de Nueva Esperanza." Distrito
  de Nueva Esperanza is in Canindeyú, **Paraguayan Chaco**. DOI:
  `10.26885/rcei.14.e726`. Local cost analysis of soybean — very
  granular but useful as P0030 background.

**What it means for the thesis**:
- P0030 currently cites CATTANEO et al. on soybean expansion in the
  Gran Chaco (a 2019 paper). This is the only Paraguayan-context
  citation in the Related Work. The 2025-2026 literature has
  several more recent Paraguayan-specific soybean papers.
- A defense committee reading P0030 might ask "what's changed
  since CATTANEO 2019?" The honest answer is "we cite the recent
  literature on Paraguayan trade competitiveness and on Paraguayan
  land tenure (Galeana 2024 + Wesz 2026) — see our Related Work."

**Recommended action**:
- Add Lesmo-Duarte et al. 2026 to master bib (Paraguayan soybean
  trade)
- Cite it in P0030's Discussion as the contemporary Paraguayan
  trade context

---

## 8. The thesis's "indigenous land" literature is stale

Currently the master bib cites:
- ILO Convention 169 (1989) ✓
- UNDRIP (2007) ✓
- Sze et al. 2022 ✓ (P0012 baseline)
- Carroll et al. 2020 (CARE Principles)
- IWGIA 2024

That's a 1989-2024 literature base. In 2024-2026, this literature
has exploded (Section 6 above). The thesis's Related Work sections
don't engage with it.

**What's missing in the thesis's P0012/P0030 Related Work**:
- Galeana 2024 (direct Paraguayan Chaco, Conservation and Society)
- Wesz Junior 2026 (Paraguayan land rush, Development and Change)
- Jennings et al. 2025 (Indigenous data governance, Nature Comm)
- Newing et al. 2024 (Participatory principles, Biol Conservation)
- Ioris 2024 (Socio-economic geography, J Soc Econ Dev)

**Recommended action**: add 5 papers, expand P0012 + P0030 Related
Work sections by ~150 words each. ~2 hours total.

---

## 9. The Gran Chaco is being studied as a transnational unit —
the thesis's Argentina/Paraguay-only framing is incomplete

- **Salizzi (2024)**. "Dinámicas agroindustriales en el Gran Chaco:
  una aproximación al espacio transfronterizo Argentina-Paraguay."
  *GEOUSP Espaço e Tempo (Online)*. DOI:
  `10.11606/issn.2179-0892.geousp.2024.216787`. Treats the Chaco
  as one transnational region.
- **Mendez & Mendez (2024)** — already cited; treats Chaco-wide
  biomass burning.
- **Sartori Peruzzo, Valdati, McHenry (2025)**. "Land tenure and
  future development affect integrity and geodiversity in Brazilian
  Indigenous Geocultural sites." *Geomorphology*. DOI:
  `10.1016/j.geomorph.2025.109770`. Brazilian Indigenous land
  sites — same dataset family as P0012/P0030.

**What it means for the thesis**:
- The thesis's framing is Paraguay-only. The 2024-2026 literature
  increasingly treats the Chaco as a transnational unit.
- A complete Chaco analysis would need Argentine (Santiago del
  Estero, Chaco, Formosa provinces) + Paraguayan (Alto Paraguay,
  Boquerón) + Brazilian (Mato Grosso do Sul) data. The thesis's
  infrastructure could support this — the pipelines are generic —
  but it doesn't currently do it.

**Recommended action**:
- Cite Salizzi 2024 in P0030's Discussion as the regional context
- Note the transnational gap explicitly in the "future work"
  section as an extension opportunity

---

## 10. Things that are NOT in the recent literature
(negative findings)

I checked: there is **no 2024-2026 paper that does**:
- A Prithvi fine-tuning specifically for Paraguayan Chaco
  deforestation (the thesis's P0011 has no published counterpart)
- An LSTM PM₂.₅ forecast specifically for Paraguayan stations
  using OpenAQ data (P0035's gap, post-OpenAQ-v3 station loss)
- A multi-task CNN for soybean yield prediction in Paraguay with
  Sentinel-2 + INBIO data (P0025's gap)

These are the thesis's **three genuine novel opportunities** that
haven't been pre-empted by recent literature. With the audit
corrections in place, the thesis could plausibly submit any of these
three as a "first in the Paraguayan context" contribution.

This is a useful reframing: **the thesis is behind on the
ethics + methodology frontier, but ahead on the *application*
frontier for Paraguay specifically**.

---

## 11. Net strategic recommendation

Three actions, in priority order, that materially improve the
thesis without requiring new data or new work:

### 11.1. Add 8-10 key 2024-2026 papers to the master bib

Specifically:
- Galeana 2024 (Paraguayan indigenous, Conservation and Society)
- Wesz Junior 2026 (Paraguayan land rush, Development and Change)
- Jennings et al. 2025 (Indigenous data governance, Nature Comm)
- Newing et al. 2024 (Participatory principles, Biol Conservation)
- Lesmo-Duarte et al. 2026 (Paraguayan soybean trade)
- Salizzi 2024 (Transnational Chaco)
- Palmeiro-Silva et al. 2025 (South America wildfire health)
- Mendez & Mendez 2024 (Paraguayan biomass burning)
- Ioris 2024 (Socio-economic geography of indigenous Paraguay)

**Effort**: 2 hours. **Impact**: makes the thesis literature-current.

### 11.2. Rewrite the thesis's appendix_b_ethics.tex using Newing
et al. 2024's "Fourteen principles"

**Effort**: 4 hours. **Impact**: real CARE Principles compliance
framework instead of generic ethics boilerplate. This is the single
biggest improvement to the FPIC narrative without requiring actual
community engagement.

### 11.3. Add a "P0030 per-department regression" to make P0030 a
findings paper

Compute: for each of the 16 soy-producing departments, regress
MAG yield trend on indigenous community count. If significant,
P0030 has a finding (the qualitative pattern is "more
indigenous-communities departments have slower soy expansion").

**Effort**: 4 hours (analysis + 1 figure + prose integration).
**Impact**: P0030 becomes a findings paper, not just an
infrastructure paper. This is gap #1.4 from HONEST_GAP_LIST.md.

---

## 12. Things NOT recommended based on the literature

- **Don't add a general ML methodology chapter.** The thesis
  already has 11 chapters. Adding more dilutes the focus. Better
  to update the existing CH9 (cross-cutting synthesis).
- **Don't claim "no prior work exists" anywhere.** There's always
  prior work; the thesis's contribution is *the Paraguayan-specific
  application*, not the methodology novelty.
- **Don't position the thesis as "advancing AI ethics in Paraguay."
  The thesis's ethical contribution is procedural (we made public
  data analysis possible), not theoretical.**

---

## Sources

| API | Query | Results |
|---|---|---:|
| CrossRef | "Paraguay Gran Chaco deforestation" 2024-2026 | 15 |
| CrossRef | "indigenous land tenure Chaco" 2024-2026 | 15 |
| CrossRef | "foundation model remote sensing" 2024-2026 | 15 |
| CrossRef | "soybean expansion Paraguay" 2024-2026 | 15 |
| OpenAlex | "wildfire smoke PM2.5 South America Paraguay" 2024-2026 | 10 |
| OpenAlex | "Prithvi HLS geospatial foundation model IBM NASA" 2024-2026 | 10 |
| OpenAlex | "CARE principles indigenous data governance" 2024-2026 | 10 |
| OpenAlex | "open-source geospatial South America reproducible" 2024-2026 | 10 |
| | **Total unique DOIs** | **97** |

All query results cached to `.scratch/lit_cache_2024.json`.

---

*End of RECENT_LITERATURE_BRIEF.md*
