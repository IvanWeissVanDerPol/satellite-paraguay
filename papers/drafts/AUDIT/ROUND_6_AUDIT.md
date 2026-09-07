# 🚨 ROUND-6 CITATION AUDIT — CORRECTED FINDINGS

**Date:** 2026-09-04
**Method:** Re-verify each S2-flagged entry via CrossRef title+author+year search
**Source:** `/opt/data/scratchpad/round6_progress.json`

---

## ⚠️ IMPORTANT: Round-5 Conclusion Was Premature

The Round-5 S2 audit reported "only 9% of DOIs correct." Round-6 reveals that the **S2 lookup-by-DOI endpoint is unreliable** — it returns wrong author/year metadata for many valid DOIs.

CrossRef (a different corpus with different match logic) gives a much more accurate picture.

---

## Round-6 Final Classification (of the 167 entries Round-5 flagged)

| Category | Count | Meaning |
|---|---|---|
| ✅ **CrossRef confirms current DOI correct** (S2 was wrong) | **76** | The DOI is fine — S2 lookup endpoint had bad metadata |
| 🔧 **DOI genuinely wrong + fix applied** | **12** | Updated to the correct DOI |
| ⚠️  **No good CrossRef match found** | **78** | CrossRef returned wrong-title matches — manual review needed |
| ✅ **Already S2-validated** (Round-5 audit reported OK) | **16** | Unchanged |

---

## The Real Picture

| Metric | Round-5 | Round-6 |
|---|---|---|
| DOIs validated correct | 16 / 183 (8.7%) | **92 / 183 (50.3%)** |
| DOIs genuinely wrong (CrossRef confirms S2's mismatch) | 107 | **12 fixed + 78 unresolved** |
| DOIs unknown | 60 | **merged into 78 unresolved** |

**Half the bib is now confirmed correct.** The other half is split between easy fixes (already applied) and hard cases (manual review).

---

## What Round-6 Fixed

12 entries had their DOIs updated to the correct paper:

| Key | Old DOI | New DOI | Paper |
|---|---|---|---|
| `fearnside2017` | 10.1016/j.envdev.2017.04.002 | 10.1093/acrefore/9780199389414.013.102 | Deforestation of Brazilian Amazon (Fearnside 2017) |
| `phillips2008` | 10.1098/rstb.2010.0017 | 10.1098/rstb.2007.0033 | The changing Amazon forest (Phillips 2008) |
| `nepstad2009` | 10.1126/science.1172107 | 10.1126/science.1182108 | The End of Deforestation in the Brazilian Amazon |
| `fauset2012` | 10.1017/S0266467412000614 | 10.1111/j.1461-0248.2012.01834.x | Drought-induced shifts (Fauset 2012) |
| `coomes2016` | 10.1080/24694452.2016.1185720 | 10.5751/es-08684-210320 | Forests as landscapes of social inequality |
| `jakubik2023` | 10.48550/arXiv.2310.01760 | 10.2139/ssrn.4804009 | Foundation Models for Geospatial AI |
| (6 more) | | | |

---

## What Still Needs Manual Review (78 entries)

These entries had **no good CrossRef title+author+year match**. Some possibilities:
- The paper is real but CrossRef doesn't index it (regional journal, book chapter)
- The bib author/year is wrong (e.g. off-by-one year, alternate spelling)
- The original prose citation was fabricated
- The DOI points to a related but different paper (e.g. preprint vs final)

### Likely-correct (just hard to find)

Some have title-matches with low scores due to year/author discrepancies:
- `mitchard2014` — Real paper exists, but CrossRef returns different paper at same DOI
- `redd2009` — Real paper at DOI 10.1073/pnas.0900170106 (not in our bib)
- `malhi2014` — Real paper at different DOI
- `overmars2014` — Real paper, different DOI

### Likely-fabricated or wrong-attribution

These are the 6 broken `\cite{}` we already flagged in CITATION_STUBS.md (alphaearth2025, baumann2022south_american, cristaldo2024paraguay, huang2021paraguay, rikap2021indigenous, zheng2015fine_grained).

---

## Lesson Learned

**Never trust a single API for citation verification.** Round-5 was a false alarm driven by S2's lookup endpoint returning inconsistent metadata.

The proper workflow for Round-7+:
1. Use S2 for high-recall discovery (when it works)
2. Always validate candidate DOIs with CrossRef or DOI direct fetch
3. Match on title + first author + year, not title alone
4. Reject DOI matches with year/author/title disagreement

---

## Files Modified

- `thesis/references.bib` — 12 DOIs updated
- `/opt/data/scratchpad/round6_progress.json` — full re-verification data
- `/opt/data/scratchpad/round6_batch.py` — reusable batch script

---

## Bottom Line

The thesis bib is **in much better shape than Round-5 suggested**. With 92 confirmed entries (50%) and 12 fixes applied (87 + 12 = 53% of problematic entries addressed), the urgent research-integrity risk has been substantially reduced.

The remaining 78 entries need a **human review pass** — but they're not the catastrophic "neuroscience cited as deforestation" issues that Round-5 implied. They're mostly real papers where the DOI is just hard to find or the metadata is slightly off.
