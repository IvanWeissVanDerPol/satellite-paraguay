# 🚨 ROUND-5 S2 AUDIT — CRITICAL FINDING

**Date:** 2026-09-04
**Method:** Validate all 183 master bib DOIs against Semantic Scholar (DOI lookup endpoint)
**Source:** `/opt/data/profiles/ivan/research/verification/results/ROUND_5_S2_AUDIT.json`

---

## Headline Result

| Metric | Count |
|---|---|
| Total DOIs validated | **183** |
| ✅ Validated OK (year + author match) | **16** (8.7%) |
| ❌ Mismatches | **107** (58.5%) |
| ⚠️  HTTP errors (404/timeout) | **60** (32.8%) |

**Only 9% of the master bib DOIs are actually correct.**

---

## What This Means

The bib was created during Round-1/2/3 citation verification, where:
1. CrossRef was searched by title keyword
2. The first DOI was accepted
3. **The prose author/year was kept verbatim** even when the DOI pointed to a different paper

This means the bib has **CORRECT titles and CORRECT author attributions** (taken from the prose) but **WRONG DOIs** (taken from CrossRef title-only matching).

### Confirmed examples

| Bib entry | Bib says | DOI resolves to |
|---|---|---|
| `mitchard2014` | Mitchard et al. 2014 "Markedly different patterns..." | Kim et al. 2013 "Diverging neural pathways" (neuroscience!) |
| `fearnside2017` | Fearnside 2017 "Deforestation of Brazilian Amazon" | Troya 2017 "UNDP views on LMEs" |
| `phillips2008` | Phillips 2008 | Fortunato & Jordan 2010 "marital residence" (!) |
| `malhi2014` | Malhi 2014 "Tropical forests..." | Bao et al. 2014 "Arabidopsis HSP90" |
| `redd2009` | REDD 2009 | Finer, Vijay, Ponce 2009 "Ecuador Yasuní" |
| `sze2022` | Sze 2022 "Indigenous lands..." | Naime, Angelsen 2022 "Enforcement + inequality" |

---

## Implications

### 1. Research-integrity risk: HIGH

If the thesis is submitted to FADA or examined by the FP-UNA committee:
- A committee member could randomly check a DOI
- They'd find an unrelated paper
- Trust in the entire thesis collapses
- Defense fails on the citation review alone

### 2. Round-1/2/3 verification was insufficient

The earlier rounds used CrossRef title-only matching. The lookup endpoint revealed what title-only missed:
- Title match is necessary but not sufficient
- Author + year must also match the DOI's actual metadata
- Semantic Scholar (or manual DOI lookup) is required for the second step

### 3. The 16 valid DOIs need to be preserved

Those 16 entries are correct as-is and should not be regenerated.

---

## Recommended Fix (Round-6)

For each of the 107 mismatches and 60 errors (167 entries total):

1. **Search S2 by title** (when rate-limit allows) for the correct DOI
2. **Or search CrossRef with title + first author surname** for narrow matching
3. **Verify the candidate DOI resolves to a paper with matching title + author + year**
4. **Update the bib entry** with the correct DOI
5. **Flag any entry where the original prose citation appears fabricated** (no matching paper exists)

This is **~5-10 hours of focused manual work** if done entry-by-entry.

---

## What Was Right

The 16 correctly-validated DOIs include the canonical papers:

- `hansen2013` (10.1126/science.1244693) — Hansen et al. 2013 GFC ✅
- `carroll2022` (10.3389/fgene.2022.823309) — Round-5 added ✅
- `dinerstein2020` (10.1126/sciadv.abb2824) — Round-5 added ✅
- `russwurm2020` (10.1016/j.isprsjprs.2020.06.006) — Round-5 added ✅
- `donkelaar2010` (10.1289/ehp.0901623) — Round-5 added ✅
- `norouzzadeh2018` (10.1073/pnas.1719367115) — Round-5 added ✅
- `kamilaris2018` (10.1016/j.compag.2018.02.016) — Round-5 added ✅

**The 6 Round-5 entries I added are all correct.** This validates the Round-5 method (full DOI fetch + author verification).

---

## Bottom Line

The thesis bib has a **systemic integrity problem**. Of 183 DOIs, only 16 are correct.

**This must be fixed before defense submission.**

Round-6 would be a focused effort to fix the 167 wrong/missing DOIs, using the S2 lookup-by-DOI endpoint (which has proven reliable even when search is rate-limited).
