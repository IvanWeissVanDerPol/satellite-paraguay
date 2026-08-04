# Dashboard Screenshots — Portfolio

This directory contains the 7-page Streamlit dashboard screenshots taken
automatically with Playwright + Chromium.

**Generated:** 2026-08-04
**Resolution:** 1600 × 900 (16:9 desktop)
**Source:** `src/dashboard/app.py`
**Capture script:** `scripts/capture_dashboard_screenshots.py`

---

## Files

| File | Page | Size | Notes |
|---|---|---|---|
| `01_overview.png` | Overview | 115 KB | 4 headline metrics, real data sources |
| `02_departments.png` | Departments | 94 KB | 16 departments, loss%, bar chart |
| `03_indigenous.png` | Indigenous Territories | 92 KB | 10 territories, statistical finding |
| `04_carbon.png` | Carbon & Verra | 77 KB | Per-pixel carbon, Verra table |
| `05_models.png` | Models | 82 KB | F1 comparison + transfer learning |
| `06_uncertainty.png` | Uncertainty | 65 KB | Bootstrap CIs, AGB sensitivity |
| `07_references.png` | References | 94 KB | Papers, data sources, code |
| `index.json` | Metadata | — | Generation timestamp |

---

## How to regenerate

```bash
# Terminal 1
python3 -m streamlit run src/dashboard/app.py

# Terminal 2
python3 scripts/capture_dashboard_screenshots.py
```

Output goes to `outputs/screenshots/`.

---

## Portfolio use

These screenshots are portfolio-quality — they show:
- Real data (Hansen, MapBiomas, Verra)
- Honest statistics (CI on indigenous disparity: [1.72, 4.20]x, p<0.001)
- Honest negative results (U-Net F1=0.017, H3 transfer NOT confirmed at 0.080)
- Framework approach (one Python package, 6 papers)

Use for:
- LinkedIn (1, 4, 6)
- ResearchGate (3, 4)
- GitHub README (1)
- Email signatures (01_overview thumbnail only)

---

## Maintenance

If `src/dashboard/app.py` is updated:
1. Re-run capture script
2. Update `index.json`
3. Commit screenshots to a new branch (don't pollute main with binary diff)
