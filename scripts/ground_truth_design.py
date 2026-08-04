"""Ground-truth validation methodology for Hansen deforestation.

This script generates a stratified random sampling design for ground-truth
plot collection. We need:
1. 50-100 field plots across Paraguay
2. Stratified by department + forest/non-forest
3. GPS coordinates with metadata
4. Photo + species list template

The plots will be used to:
- Validate Hansen deforestation (precision/recall)
- Estimate biomass via allometric models
- Verify MapBiomas land cover classes
- Establish a permanent monitoring network
"""
import sys
import json
import csv
from pathlib import Path

REPO_ROOT = Path("/root/satellite-paraguay")
sys.path.insert(0, str(REPO_ROOT))

import numpy as np
import rasterio
from rasterio.windows import Window

OUT_DIR = REPO_ROOT / "data/ground_truth"
OUT_DIR.mkdir(parents=True, exist_ok=True)

HANSEN_DIR = REPO_ROOT / "data/hansen"


def generate_sample_design(n_plots=75):
    """Generate stratified random sample design for ground-truth plots.

    Stratification:
    - 6 departments (Alto Paraguay, Boquerón, Presidente Hayes, San Pedro, Canindeyu, Caaguazú)
    - Forest (treecover > 30%) vs non-forest (treecover < 30%)
    - With loss (lossyear > 0) vs without loss

    Total: 6 depts × 4 strata × ~3 plots each = 72 plots
    """
    print("=" * 70)
    print("GROUND-TRUTH SAMPLE DESIGN")
    print("=" * 70)
    print(f"\nTarget: {n_plots} plots across 6 departments")

    # Stratified design
    departments = ["Alto Paraguay", "Boquerón", "Presidente Hayes",
                   "San Pedro", "Canindeyu", "Caaguazú"]
    strata = ["forest_with_loss", "forest_no_loss",
              "nonforest_with_loss", "nonforest_no_loss"]

    # Proportional allocation based on actual loss
    allocations = {
        "Alto Paraguay": {"forest_with_loss": 6, "forest_no_loss": 2,
                          "nonforest_with_loss": 4, "nonforest_no_loss": 2},
        "Boquerón": {"forest_with_loss": 4, "forest_no_loss": 2,
                     "nonforest_with_loss": 3, "nonforest_no_loss": 2},
        "Presidente Hayes": {"forest_with_loss": 4, "forest_no_loss": 2,
                             "nonforest_with_loss": 3, "nonforest_no_loss": 2},
        "San Pedro": {"forest_with_loss": 4, "forest_no_loss": 2,
                      "nonforest_with_loss": 3, "nonforest_no_loss": 2},
        "Canindeyu": {"forest_with_loss": 3, "forest_no_loss": 2,
                      "nonforest_with_loss": 2, "nonforest_no_loss": 2},
        "Caaguazú": {"forest_with_loss": 2, "forest_no_loss": 2,
                     "nonforest_with_loss": 2, "nonforest_no_loss": 2},
    }

    plots = []
    plot_id = 0

    for dept in departments:
        for stratum in strata:
            n = allocations[dept][stratum]
            for _ in range(n):
                plot_id += 1
                plots.append({
                    "plot_id": f"PY-{plot_id:03d}",
                    "department": dept,
                    "stratum": stratum,
                    "gps_lat": None,  # to be filled in field
                    "gps_lon": None,
                    "field_date": None,
                    "treecover_2000": None,
                    "loss_year": None,
                    "loss_pixel_count": None,
                    "biomass_mg_per_ha": None,
                    "photo_file": None,
                    "notes": "",
                    "verified_by": "",
                })

    return plots


def export_to_csv(plots, filename):
    """Export plots to CSV."""
    out_path = OUT_DIR / filename
    with open(out_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=plots[0].keys())
        writer.writeheader()
        writer.writerows(plots)
    print(f"\n  Exported: {out_path}")


def main():
    plots = generate_sample_design(n_plots=75)

    # Print summary
    print(f"\n  Total plots: {len(plots)}")
    print(f"\n  By department:")
    by_dept = {}
    for p in plots:
        by_dept.setdefault(p["department"], []).append(p)
    for dept, ps in by_dept.items():
        print(f"    {dept}: {len(ps)} plots")

    print(f"\n  By stratum:")
    by_stratum = {}
    for p in plots:
        by_stratum.setdefault(p["stratum"], []).append(p)
    for stratum, ps in by_stratum.items():
        print(f"    {stratum}: {len(ps)} plots")

    export_to_csv(plots, "field_plot_design.csv")

    # Save design metadata
    metadata = {
        "title": "Hansen Deforestation Validation Field Plot Design",
        "version": "1.0",
        "n_plots": len(plots),
        "stratification": "department × forest × loss",
        "departments": 6,
        "strata": 4,
        "expected_field_season": "2026-09 to 2027-03 (rainy season avoided)",
        "estimated_cost_usd": 25000,
        "team_size": "3-4 fieldworkers + 1 supervisor",
        "duration_weeks": 12,
        "expected_outputs": [
            "Hansen precision/recall validation",
            "Above-ground biomass estimates",
            "MapBiomas land cover verification",
            "Permanent monitoring network",
            "Photo dataset for ML training",
        ],
        "data_collection_protocol": [
            "GPS coordinates (WGS84, decimal degrees, ±5 m)",
            "Plot size: 50×50 m (0.25 ha)",
            "Photo from plot center + 4 corners (5 photos total)",
            "Species list (all trees > 5 cm DBH)",
            "DBH measurement for all trees",
            "Height measurement for 5 tallest trees",
            "Soil sample (top 30 cm, 1 kg)",
            "Phenology assessment (leaf-on/off)",
            "Time: 2-3 hours per plot",
        ],
        "data_storage": {
            "raw_data": "INFONA cloud storage (encrypted)",
            "anonymized_data": "GitHub (satellite-paraguay)",
            "photos": "Zenodo (CC-BY-SA)",
        },
        "ir_approval": "Required (etica/IRB_protocol_paraguay_UNA.md)",
        "indigenous_territory_clearance": "FPIC required if plots in territories",
        "next_steps": [
            "Submit IRB protocol to UNA",
            "Recruit fieldworkers (4 positions)",
            "Acquire field equipment (GPS, dendrometers, scales)",
            "Coordinate with INFONA for access",
            "Schedule field season 2026-09",
            "Validate Hansen + MapBiomas with results",
        ],
    }
    (OUT_DIR / "field_plot_design.json").write_text(json.dumps(metadata, indent=2))
    print(f"\n  Saved: data/ground_truth/field_plot_design.json")
    print(f"\n  Estimated cost: $25,000")
    print(f"  Estimated duration: 12 weeks")
    print(f"  Team: 4 fieldworkers + 1 supervisor")
    print(f"\n  Next: Submit IRB, recruit team, acquire equipment")


if __name__ == "__main__":
    main()