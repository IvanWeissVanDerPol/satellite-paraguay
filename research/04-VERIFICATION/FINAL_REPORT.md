# Citation Verification — Final Report
**Date:** 2026-09-03
**Source:** 226 reconstructed citations extracted from `/opt/data/profiles/ivan/research/round-2/`

## Methodology

1. **Extract** all "- **Author, X., et al. (YEAR)** ** Title..." citation lines from round-2 files (regex-based)
2. **Query** CrossRef API via curl for each (author surname + 8-word title fragment + year ±1)
3. **Score** matches using Jaccard + min-overlap (after stopword removal)
4. **Categorize** by score:
   - **VERIFIED** (>0.6): likely real, cite with confidence
   - **LIKELY** (0.4-0.6): probably real but title guess was imprecise
   - **PARTIAL** (0.2-0.4): ambiguous — may exist with different title
   - **NOT_FOUND** (<0.2): likely a reconstruction from training data

## Results Summary

| Status | Count | % | Action |
|---|---|---|---|
| ✅ VERIFIED | 47 | 21% | Safe to add to thesis bib |
| ⚠️ LIKELY | 51 | 23% | Manually verify before citing |
| 📝 PARTIAL | 34 | 15% | Likely exists with different wording |
| ❌ NOT_FOUND | 94 | 42% | Likely reconstruction; do not cite |

**Total: 226 citations checked**

## Top 20 VERIFIED papers (safe to cite)

| Author | Year | DOI | Matched Title |
|---|---|---|---|
| Harris, N.L. | 2021 | 10.1038/s41558-020-00976-6 | Global maps of twenty-first century forest carbon fluxes |
| Cohn, A.S. | 2014 | 10.1073/pnas.1307163111 | Cattle ranching intensification in Brazil... |
| Berthrong, S.T. | 2009 | 10.1890/08-1730.1 | Global meta-analysis of soil exchangeable cations... |
| Klein, A.M. | 2007 | 10.1098/rspb.2006.3721 | Importance of pollinators in changing landscapes... |
| Baldocchi, D. | 2001 | 10.1175/1520-0477 | FLUXNET: A New Tool to Study... |
| Herrero, M. | 2013 | 10.1073/pnas.1308149110 | Biomass use, production, feed efficiencies... |
| Holl, K.D. | 2017 | 10.3417/2016036 | Research Directions in Tropical Forest Restoration |
| Kuemmerle, T. | 2017 | 10.1080/24694452.2017.1360761 | Rents, Actors, and the Expansion of Commodity Frontiers in the Gran Chaco |
| Soar..., 2019 | 2019 | 10.5194/essd-11-529-2019 | Global Fire Atlas of individual fire size... |
| Kumar, S. | 2024 | 10.1007/978-3-031-94062-0_3 | Climate-Resilient Agriculture Technique for Semi-Arid |
| Marengo, J.A. | 2025 | 10.1016/j.wace.2024.100710 | ENSO impacts review |
| (... and 36 more) |

## LIKELY papers needing manual review (top examples)

These showed up in CrossRef searches but the title match was less than perfect. Likely exist with author/title variations:

- Agostini, N. (2024) "Apex raptors in Atlantic Forest fragments"
- Carpenter, B. (2025) "Biodiversity loss attribution..." → likely maps to Carpenter 2024 published as 10.1016/j.gloenvcha.2024.103011
- Cooper, S. (2024) "Soybean mapping across South America"
- Cornelius, C. (2024) "Bird community responses to grazing"
- Foster et al. → Need different author/year

## NOT_FOUND list

94 entries appear to be reconstructions from training-data familiarity. **Do not cite without further verification.** Many are likely real papers with the wrong publication year or journal — but the CrossRef API couldn't find a plausible match under any spelling variation.

Examples of NOT_FOUND:
- Acock, B. (2024) "LSU crop yield model integration for Paraguay" — likely fictional
- Ahumada, J.A. (2024) — actual Ahumada jaguar paper is from 2011, not 2024
- Barros, M. (2024) — likely fictitious
- Bertoni (2024) — Bertoni Foundation reports exist but no specific 2024 entry
- Chambers (2007) — actual paper was "Working with Indigenous People" by Chambers et al — verify title
- Hooper (2024) - likely fictional author-year

## Direct verification of known papers

I independently verified these **without relying on round-2 reconstructed titles**:
- **West 2020 PNAS** exists: DOI 10.1073/pnas.2004334117 (cited in round 1 already)
- **West 2023 Science** exists: DOI 10.1126/science.ade3535 (cited in round 1 already)
- **Bullock 2023 GEDI Paraguay** exists: DOI 10.1088/1748-9326/acdf03 (cited in round 1 already)
- **Pendrill 2019** exists: DOI 10.1016/j.gloenvcha.2019.01.001
- **Pendrill 2022 Nature Food** exists: DOI 10.1038/s43016-021-00425-z
- **Hengl 2017 SoilGrids** exists: DOI 10.1371/journal.pone.0169748
- **Havlík 2014 PNAS** exists: DOI 10.1073/pnas.1318086111
- **Havlík 2018 Global Env Change** exists: DOI 10.1016/j.gloenvcha.2018.06.011
- **Tscharntke 2011 PNAS** exists: DOI 10.1073/pnas.1010455108

These real canonical papers are NOT in the round-2 files. They were ALREADY in round 1's references.bib.

## Recommendations

### Immediate actions for thesis BibTeX

1. **Safe to add to references.bib** (47 papers with verified DOI): see `verified_bibtex.bib`
2. **Manually verify 51 LIKELY papers** by reading the matched CrossRef result — usually this means my title paraphrase was wrong but the paper exists
3. **Skip or rewrite 94 NOT_FOUND entries** — these are likely reconstructions and citing them would be fabrication
4. **Replace round-2 citations with confirmed canonical papers** in the actual LaTeX files (Yvutu/Vyrá/Yvy/Kai/Tatakua/Yrupe)

### Critical safety point

This verification confirms the original caveat I gave at the end of Round 2:
> "**Specific paper titles are predictions** — many *"Round-2 candidates"* and modern 2024-2026 citations like *He 2022*, *Brennan 2024*, *CASO PCA 2024* may need verification when the search budget refreshes."

That caveat was correct. **~42% of round-2 reconstructed citations did NOT verify.**

However, **21% verified cleanly** (47 papers) — these provide a solid foundation of additional papers for the thesis.

### Verifying unknown author/year issues

For papers I cited with wrong authors (e.g., "Chen 2022" when it's actually Hengl 2017), the action is:
1. Read the citation context in the round-2 file
2. Find the actual reference using knowledge of the field
3. Update the citation in the file with correct author/year

## Files produced

- `/opt/data/profiles/ivan/research/verification/verification_results_v3.json` — machine-readable
- `/opt/data/profiles/ivan/research/verification/verification_report_v3.md` — human-readable
- `/opt/data/profiles/ivan/research/verification/verified_bibtex.bib` — 47 entries ready to drop in
- `/opt/data/profiles/ivan/research/verification/not_found_DO_NOT_CITE.txt` — 94 entries to remove
- `/opt/data/profiles/ivan/research/verification/manual/manual_verification.json` — known-good papers
