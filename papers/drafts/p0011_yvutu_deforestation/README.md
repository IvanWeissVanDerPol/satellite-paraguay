# P0011 Yvutu — Complete paper package

This directory contains the complete submission package for **P0011 Yvutu**:
a multi-temporal satellite computer vision system for deforestation alert
generation in the Paraguayan Chaco.

## Target journal

**Remote Sensing of Environment** (Elsevier)
- IF = 13.5 (2024)
- CiteScore = 22.1
- Median time to first decision: 6 weeks
- Open access option: $3,290
- Paraguay waiver: typically granted for developing countries

## Contents

```
papers/drafts/p0011_yvutu_deforestation/
├── README.md                       # This file
├── paper.md                        # Full paper text (draft)
├── paper.tex                       # LaTeX submission template (RSE format)
├── cover_letter.md                 # Cover letter for RSE editor
├── submission_checklist.md         # RSE submission requirements
├── ACTUAL_RESULTS.md               # Honest reporting of pilot experiment
├── reproducibility.md               # Reproducibility checklist
├── quickstart.sh                   # One-command reproduction script
└── outputs/
    ├── metrics.json                # Pilot experiment metrics
    ├── dataset_stats.json          # Dataset statistics
    ├── unet_weights.pt             # Trained U-Net checkpoint
    ├── yvutu_weights.pt            # Trained Yvutu checkpoint
    ├── figures/                    # 4 paper figures (PNG)
    └── tables/                     # 4 paper tables (JSON + LaTeX)
```

## Status

- **Pipeline:** ✅ Complete and tested
- **Pilot experiment:** ✅ Run with synthetic data (proof-of-concept)
- **Real-data experiment:** ⏳ Not yet run (requires GEE auth + GPU rental)
- **Paper text:** ✅ Draft complete (honest reporting)
- **Submission materials:** ✅ Cover letter, checklist, reproducibility docs
- **Submission to RSE:** ⏳ Ready after real-data run

## Quick reproduction

```bash
cd /root/satellite-paraguay
./papers/drafts/p0011_yvutu_deforestation/quickstart.sh
```

## Key contributions

1. **First Paraguay-specific fine-tuning of Prithvi** foundation model
2. **Comprehensive evaluation** on synthetic + planned real data
3. **Operational pipeline** with monthly Sentinel-2 ingestion
4. **Open-source release** under MIT license

## Next steps

1. Download real Sentinel-2 data (GEE authentication, ~30 minutes)
2. Train on real data with cloud GPU (Vast.ai, $5)
3. Update paper.md with real metrics
4. Submit to RSE

## Authors

- Iván Weiss Van der Pol (corresponding author) - FADA-UNA, Paraguay
- Juan Carlos Cristaldo (advisor) - FADA-UNA, Paraguay

## License

All code and paper text: MIT License
Sentinel-2 data: ESA Copernicus (free)
MapBiomas data: CC0
Hansen GFC data: CC0
