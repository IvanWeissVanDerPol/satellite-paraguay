# Citation Integrity Audits

This folder holds the citation integrity audit trail for the thesis.

## Files

- `ROUND_5_S2_AUDIT.md` — Initial Semantic Scholar validation of 183 DOIs
  - **Method:** S2 lookup-by-DOI for all master bib DOIs
  - **Result:** Found 107 mismatches, 60 errors, 16 valid
  - **Conclusion:** Premature — see ROUND_6 for correction

- `ROUND_5_S2_AUDIT.json` — Machine-readable S2 audit data

- `ROUND_6_AUDIT.md` — Corrected CrossRef re-verification
  - **Method:** CrossRef title+author+year search
  - **Result:** 76 S2-flags were false positives; 7 real fixes applied
  - **Conclusion:** Real integrity risk is much smaller than Round-5 implied

## How to re-verify

```bash
# Re-verify the full bib (slow, ~5min)
python3 scripts/verify_bib_dois.py --batch 0 200

# Quick check: just the 7 Round-6 fixes
python3 scripts/verify_bib_dois.py --verify-only sze2022 fearnside2017 ...
```

## What to do with this folder

- **DO** keep these files in-repo — they're the defense committee's audit trail
- **DO** add new audits as `ROUND_N_*.md` with consistent format
- **DO NOT** delete the older audits — they show the work was done
