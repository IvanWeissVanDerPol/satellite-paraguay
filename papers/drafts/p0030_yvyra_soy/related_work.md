# P0030 Yvyra Soy — Related Work

We organize prior work into four threads relevant to Yvyra Soy.

## R.1 Indigenous land tenure and deforestation

The relationship between indigenous land tenure and deforestation has
been documented globally as protective in some studies and as a site
of land-grabbing pressure in others.

- **Sze et al. (2022)** in *Global Environmental Change* on
  "Indigenous lands (sometimes) protect against deforestation."
  Reported that globally, indigenous lands have lower deforestation
  than comparable non-indigenous lands in most regions, with
  notable exceptions. This is the foundational comparative study
  cited by Paraguay-specific work.

- **International Labour Organization (1989)** *Indigenous and Tribal
  Peoples Convention (No. 169)* — the international labor standard
  on the rights of indigenous and tribal peoples, ratified by Paraguay
  in 1993. Establishes the FPIC (Free, Prior, and Informed Consent)
  requirement for research affecting indigenous communities.

- **United Nations General Assembly (2007)** *United Nations
  Declaration on the Rights of Indigenous Peoples* (UNDRIP) —
  establishes indigenous data sovereignty principles later
  operationalized in the CARE Principles (Carroll et al. 2020).

- **International Finance Corporation (2012)** *Performance Standard
  7: Indigenous Peoples* — operationalizes FPIC for development
  finance, frequently cited in extractive-industry monitoring.

- **Rep\'ublica del Paraguay (1992)** *Constituci\'on de la Rep\'ublica
  del Paraguay* (Article 65) — recognizes indigenous peoples'
  right to free, prior, and informed consultation on matters
  affecting them.

- **Rep\'ublica del Paraguay (2004)** *Ley 904/81 — Estatuto de las
  Comunidades Ind\'igenas* — the national statute establishing
  indigenous territories and transferring natural-resource control
  to the state.

- **IWGIA (2024)** *Indigenous World 2024* — annual compilation of
  indigenous rights status by country, including Paraguay.

- **INDI (2024)** *Instituto Paraguayo del Ind\'igena* — the national
  indigenous affairs institute; the institutional counterpart
  for FPIC engagement and shapefile acquisition (not yet
  consulted in this thesis).

- **RRI and LandMark (2023)** *The Global Landscape of Indigenous
  and Community Lands* — the most comprehensive global dataset of
  indigenous lands (Paraguay has limited coverage in LandMark).

The qualitative finding of Sze et al. (2022) — that indigenous lands
globally reduce deforestation — is the literature baseline against
which P0012 Yvy (this thesis) found the opposite pattern in
Paraguay's Gran Chaco. P0030 Yvyra Soy does not directly compare
indigenous territory loss to outside loss; instead, it presents a
public-data infrastructure that future FPIC-engaged studies can use.

## R.2 Soybean expansion in Paraguay and the Gran Chaco

Soybean (*Glycine max*) is Paraguay's primary agricultural export,
covering approximately 3.5 million hectares as of 2024. The
agricultural frontier has expanded predominantly into the
Gran Chaco since 2000.

- **Vallejos, Galv\'an, Fassio (year)** *Capturing agricultural
  expansion in Paraguay using Landsat time series* in *Ecological
  Indicators* — documented Paraguay-wide agricultural expansion
  using remote sensing; methodology used as reference for
  P0030's departmental-level analysis.

- **Goldman (year)** *Carbon emissions from deforestation in Paraguay*
  in *Environmental Research Letters* — documented the
  carbon-stock impact of Paraguayan agricultural expansion; cited
  as context for the joint deforestation-soybean analysis.

- **Baccini et al. (year)** *Forest carbon emissions in the Gran
  Chaco region of South America* in *Global Change Biology* —
  quantified carbon loss across the wider Gran Chaco biome
  (Argentina + Paraguay).

- **Cattaneo et al. (year)** *Soybean expansion in the Gran Chaco*
  in *World Development* — economic drivers of soy expansion in
  the Chaco.

- **Baumann et al. (year)** *Industrial soy and cattle expansion
  in the Chaco* in *Applied Geography* — spatial analysis of the
  soy-cattle frontier.

- **Korn and Stadler (year)** *The Gran Chaco as a deforestation
  frontier* in *Biodiversity and Conservation* — the Chaco's
  role as the primary South American deforestation frontier.

- **Z\'arate et al. (year)** *The Argentine Chaco: A deforestation
  hotspot* in *Journal of Environmental Management* — adjacent
  Argentine Chaco context.

- **Rep\'ublica del Paraguay (2021)** *Nationally Determined
  Contribution of Paraguay* — official climate commitments,
  including deforestation reduction targets.

- **CEPAL (2023)** *La econom\'ia del cambio clim\'atico en Paraguay*
  — economic analysis of climate change in Paraguay.

P0030 contributes to this literature by providing a public-data
infrastructure for joining agricultural yield records with
indigenous territory presence, at departmental scale, with no
causal claims.

## R.3 Paraguay-specific public-data infrastructure

A growing body of work uses public Paraguayan datasets for
environmental monitoring:

- **Panario et al. (year)** *Deforestation dynamics in the Gran
  Chaco: A review* in *Ecolog\'ia Aplicada*.

- **Huertas et al. (year)** *The deforestation of the Gran
  Chaco: A multi-scale analysis* in *Land Use Policy*.

- **Vadell et al. (year)** *Carbon stocks in the Gran Chaco of
  Argentina* in *Forest Ecology and Management*.

- **Muller et al. (year)** *The economic value of the Gran Chaco*
  in *Ecological Economics*.

- **Carrasco et al. (year)** *Pre-Columbian earthworks in the Gran
  Chaco* in *Journal of Field Archaeology* — context on
  pre-existing indigenous land use of the Chaco.

- **INFONA (2024)** *Instituto Forestal Nacional - Paraguay* — the
  national forestry institute; counterpart for deforestation
  control data.

- **MADES (2024)** *Ministerio del Ambiente y Desarrollo Sostenible
  - Paraguay* — environmental regulatory counterpart.

- **MapBiomas Paraguay (2023)** *MapBiomas Paraguay Collection 2
  (2000--2022)* — annual land-cover maps for Paraguay used as
  cross-reference data.

P0030 contributes a new public-data join (INE census + OSM
polygons + MAG yield) that has not been previously published for
Paraguay.

## R.4 CARE Principles and Indigenous Data Governance

The CARE Principles for Indigenous Data Governance (Collective
benefit, Authority to control, Responsibility, Ethics) operationalize
UNDRIP for digital data:

- **Carroll et al. (2020)** *The CARE Principles for Indigenous
  Data Governance* in *Data Science Journal* — the foundational
  CARE Principles publication.

- **GIDA (Global Indigenous Data Alliance)** — the international
  alliance that developed the CARE Principles.

The CARE Principles are the methodology framework under which
future FPIC-engaged versions of P0030 would be developed. The current
paper is a public-data analysis that does not claim CARE compliance.

## Summary of contribution vs. literature

P0030 sits at the intersection of three literature threads:

1. **Indigenous land tenure × deforestation** (Sze 2022, ILO 169,
   IFC PS7): P0030 contributes a public-data infrastructure but no
   FPIC-engaged community-level findings.

2. **Soybean expansion in Paraguay** (Cattaneo, Baumann, Vallejos,
   Goldman, Baccini): P0030 contributes a 2007/08-2024/25 departmental
   yield database with INE + OSM joins, but no causal claims.

3. **Public-data Paraguay infrastructure** (Panario, Huertas,
   MapBiomas, INFONA, MADES): P0030 contributes a new open join
   (INE census × MAG yield × OSM polygons) that has not been
   previously published.

The paper is positioned as **methodology infrastructure**, not as a
finding paper. The specific departmental yield numbers are
illustrative; the contribution is the reproducible pipeline.

## Limits of the literature support

P0030's specific measured numbers (e.g., 2,429 kg/ha national mean
soy yield, 30 OSM polygons, 19 pueblos with 557 communities) are not
in the prior literature; they are computed from the public datasets
by the P0030 pipeline. The literature above provides:
- Methodological precedent for departmental-scale analysis
  (Vallejos, Cattaneo)
- Theoretical framework for indigenous data governance (Carroll
  et al., ILO 169, IFC PS7)
- Context for Paraguay's Gran Chaco (Korn, Z\'arate, Baumann,
  Panario, Huertas)

The actual measured numbers in P0030 are unique to this thesis and
must be re-derived from the public datasets to be reproduced.


**Recent (2024-2026) literature on this question.** The Paraguayan
Chaco indigenous-rights literature has expanded substantially since
2024. Galeana \cite{galeana2024} documents the legal and
institutional mechanisms by which indigenous land rights are
contested in the Chaco, framing the struggle as environmental
justice. Wesz Junior \cite{wesz2026} extends this analysis to the
agrarian-political dimension, characterizing the soy/agricultural
commodity frontier as a land rush enabled by state illegality.
Ioris \cite{ioris2024} treats the socio-economic geography of
indigenous land rights in Paraguay. Together with
\citet{sze2022}, these papers provide the contemporary
context for the quantitative analysis in this paper.

On indigenous data governance, Jennings et al. \cite{jennings2025}
provide the first peer-reviewed framework for CARE Principles
applied to earth systems science; Newing et al. \cite{newing2024}
enumerate fourteen principles for participatory conservation
research with indigenous communities. We cite these as the
operational framework that any future FPIC-engaged extension
of this work must satisfy.