# 99. Citation Hygiene Audit — what to resolve in `references.bib`

**Date:** 2026-09-03

## 11 unresolved cited keys mentioned in earlier turns

These keys appear in PAPER citations but were NOT in the original `references.bib`:

| Cited Key | Likely Paper | Status |
|---|---|---|
| `alphaearth2025` | DeepMind AlphaEarth Foundations | ✅ Added in bibtex_entries_to_add.bib |
| `baumann2022south_american` | Baumann et al. (Kuemmerle group) on soy South America | ✅ Added |
| `bucher2019gran_chaco` | Bucher 2019 on Chaco biodiversity | ✅ Added |
| `bullock2021satellite` | Likely typo — should be `bullock2023_gedi_paraguay_nfi` | ✅ Added |
| `coconier2018defensores` | Coconier et al. Defensores del Chaco | Need to add |
| `garnett2018spatial` | Garnett et al. 2018 Indigenous lands global | ✅ Added |
| `rikap2021indigenous` | Rikap on Indigenous-paraguayan data | Need to add |
| `sep2025` | Sep 2025 Mongabay (?) | Ambiguous — likely Mongabay Verra 2025 |
| `zheng2015fine_grained` | Zheng 2015 fine-grained classification (not Chaco-related — likely U-Net context) | Need to check |
| `vallejos2020deforestation` | Vallejos Paraguay deforestation 2020 | Need to add |
| `huang2021paraguay` | Huang 2021 Paraguay (likely CASA or RSS) | Need to add |

## Action items

1. Verify each key against full reference list at end of each paper's `paper.tex`
2. Insert the missing 5 (coconier, rikap, sep, vallejos, huang)
3. Move `alphaearth2025`, `baumann2022`, `bucher2019`, `bullock2023`, `garnett2018` from `bibtex_entries_to_add.bib` (already done in earlier commit)
4. Consider online lookup via DOI for each missing key

## Quick fix plan

```bash
cd /opt/data/work/satellite-paraguay
grep -oE '\\\\cite[a-z]*\\{[^}]*\\}' papers/drafts/*/paper.tex | tr -d '{}\\cite[' | tr ',' '\n' | sed 's/[a-z]*//' | sort -u > /tmp/all_keys.txt
grep -oE '^@\\w+\\{[^,]+' references.bib | sed 's/^[^{]*{\\s*//' | sort -u > /tmp/bib_keys.txt
# Now any key in /tmp/all_keys.txt NOT in /tmp/bib_keys.txt is unresolved
comm -23 /tmp/all_keys.txt /tmp/bib_keys.txt > /tmp/missing_keys.txt
wc -l /tmp/missing_keys.txt
```

## Also: improve citation style

- Verify all citations use `\citep` or `\citet` consistently
- Add DOI or URL to each BibTeX entry that's missing one
- Convert any arXiv-only entries to updated journal version if now published

## Journal venue mapping per paper

| Paper | Venue Targeted | Why |
|---|---|---|
| Yvutu | *Remote Sensing of Environment* or *Environmental Research Letters* | High-impact journal for satellite + Paraguay |
| Vyrá | *Science* (high risk) or *Climate Policy* | Methodological novelty |
| Yvy | *Environmental Science & Policy* or *World Development* | Ethics + remote sensing |
| Kai | *Ecological Applications* or *Methods in Ecology and Evolution* | Wildlife ML pipeline |
| Yrupe | *Ecological Modelling* or *Environmental Modelling & Software* | Modeling methods |
| Tatakua | *Atmospheric Chemistry and Physics* or *Remote Sensing of Environment* | Air quality + RS |
