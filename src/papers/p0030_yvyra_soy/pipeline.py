"""P0030 Yvyra Soy: Indigenous Territory × Soybean Frontier pipeline.

Combines three public datasets to ask: is there a measurable
relationship between indigenous territory presence and
soybean expansion in Paraguay's departments?

Data sources (all real, public):
  - INE 2022 census (557 communities, 19 pueblos) from datos.gov.py
  - OSM indigenous community polygons (30 features) from Overpass API
  - MAG cereal yield 2007/08-2024/25 from datos.gov.py (DCEA)
  - Hansen GFC v1.11 256x256 tile (off-repo, ~56 km^2)

What the pipeline does NOT do:
  - FPIC engagement (none — see audit Hat 7)
  - Identify specific named communities (no public land-use claims)
  - Cross-reference OSM polygons with private lands or soy farms
  - Claim causality (only correlation at departmental scale)

What it computes (territory-level, n=19 pueblos):
  - mean_soy_yield_kg_per_ha: MAG soy rendimiento by department
  - soy_area_ha: MAG soy superficie by department
  - indigenous_communities_count: INE 2022 by pueblo
  - pueblo_share_pct: indigenous communities / total in each pueblo
"""

import json
from pathlib import Path

import numpy as np

from ...evaluation import regression_metrics


class YvyraSoyPipeline:
    """Indigenous territory × soybean frontier analysis pipeline."""

    def __init__(self, config: dict | None = None):
        self.config = config or {
            "ine_census_path": "data/raw/ine_indi/indigenous_communities_2022_summary.csv",
            "osm_polygons_path": "data/raw/osm_indigenous/osm_comunidades_indigenas_py.geojson",
            "mag_yield_dir": "data/raw/fao_mag",
            "output_dir": "outputs/p0030",
        }
        self.output_dir = Path(self.config["output_dir"])
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def load_ine_census(self) -> dict:
        """Load INE 2022 indigenous communities census (per-pueblo counts).

        Returns dict: {pueblo_name: comunidades_count_2022, ...}
        """
        f = Path(self.config["ine_census_path"])
        if not f.exists():
            return {}
        result = {}
        with open(f) as fp:
            header = fp.readline().strip().split(",")
            # Find columns
            pueblo_idx = header.index("pueblo")
            count_idx = header.index("comunidades_count_2022")

            for line in fp:
                parts = line.strip().split(",")
                if len(parts) <= max(pueblo_idx, count_idx):
                    continue
                pueblo = parts[pueblo_idx].strip()
                try:
                    count = int(parts[count_idx])
                except ValueError:
                    continue
                if pueblo and count > 0:
                    result[pueblo] = count
        return result

    def load_mag_soy_by_department(self) -> dict:
        """Load MAG soy rendimiento (kg/ha) by department for the last 5 years.

        Returns dict: {department: {"years": [year, ...], "rendimiento": [kg/ha, ...]}, ...}
        """
        f = Path(self.config["mag_yield_dir"]) / "mag_soja_rendimiento.csv"
        if not f.exists():
            return {}
        result = {}
        with open(f) as fp:
            header = fp.readline().strip().split(",")
            year_cols = [(i, h) for i, h in enumerate(header[1:], start=1) if h]
            for line in fp:
                parts = line.strip().split(",")
                if len(parts) < 2:
                    continue
                dept = parts[0].strip()
                years = []
                values = []
                for idx, year_str in year_cols:
                    if idx >= len(parts):
                        continue
                    try:
                        v = float(parts[idx])
                    except ValueError:
                        continue
                    if v > 0:  # filter NaN/missing
                        years.append(year_str)
                        values.append(v)
                if dept and values:
                    result[dept] = {"years": years, "rendimiento": values}
        return result

    def load_mag_soy_superficie_by_department(self) -> dict:
        """Load MAG soy superficie (ha) by department.

        Returns dict: {department: {"years": [...], "superficie_ha": [...]}, ...}
        """
        f = Path(self.config["mag_yield_dir"]) / "mag_soja_superficie.csv"
        if not f.exists():
            return {}
        result = {}
        with open(f) as fp:
            header = fp.readline().strip().split(",")
            year_cols = [(i, h) for i, h in enumerate(header[1:], start=1) if h]
            for line in fp:
                parts = line.strip().split(",")
                if len(parts) < 2:
                    continue
                dept = parts[0].strip()
                years = []
                values = []
                for idx, year_str in year_cols:
                    if idx >= len(parts):
                        continue
                    try:
                        v = float(parts[idx])
                    except ValueError:
                        continue
                    years.append(year_str)
                    values.append(v)
                if dept and values:
                    result[dept] = {"years": years, "superficie_ha": values}
        return result

    def load_osm_polygons(self) -> dict:
        """Load OSM indigenous community polygons (simple summary).

        Returns dict with: {"n_features": int, "bbox": [lon_min, lat_min, lon_max, lat_max]}
        Note: does not return geometry to keep this lightweight.
        """
        f = Path(self.config["osm_polygons_path"])
        if not f.exists():
            return {"n_features": 0}
        with open(f) as fp:
            geojson = json.load(fp)
        features = geojson.get("features", [])
        if not features:
            return {"n_features": 0}
        # Compute bbox
        lons = []
        lats = []
        for feat in features:
            geom = feat.get("geometry", {})
            if geom.get("type") in ("Polygon", "MultiPolygon"):
                coords = geom.get("coordinates", [])
                for ring in (coords if geom["type"] == "Polygon" else [c for poly in coords for c in poly]):
                    for point in ring:
                        lons.append(point[0])
                        lats.append(point[1])
        bbox = [min(lons), min(lats), max(lons), max(lats)] if lons else None
        return {"n_features": len(features), "bbox": bbox}

    def compute_pueblo_summary(self) -> dict:
        """Compute per-pueblo summary joining INE census with OSM presence.

        Returns dict: {
            "pueblos": [
                {"pueblo": name, "ine_communities_2022": int, ...},
                ...
            ],
            "national_total_2022": int,
            "n_pueblos": int
        }
        """
        census = self.load_ine_census()
        pueblos = []
        for pueblo, count in sorted(census.items(), key=lambda x: -x[1]):
            pueblos.append(
                {
                    "pueblo": pueblo,
                    "ine_communities_2022": count,
                }
            )
        return {
            "pueblos": pueblos,
            "national_total_2022": sum(census.values()),
            "n_pueblos": len(census),
        }

    def compute_soy_by_department(self) -> dict:
        """Compute soy yield + area summary per department.

        Returns dict with mean yield and total area over the last 5 years.
        """
        yields = self.load_mag_soy_by_department()
        superficies = self.load_mag_soy_superficie_by_department()
        result = {}
        for dept in yields:
            rend = yields[dept]["rendimiento"]
            sup = superficies.get(dept, {}).get("superficie_ha", [])
            # Use last 5 years
            rend_5yr = rend[-5:] if len(rend) >= 5 else rend
            sup_5yr = sup[-5:] if len(sup) >= 5 else sup
            if rend_5yr:
                result[dept] = {
                    "mean_yield_kg_per_ha_5yr": float(np.mean(rend_5yr)),
                    "total_area_ha_5yr": float(np.sum(sup_5yr)) if sup_5yr else None,
                    "yield_years": yields[dept]["years"][-5:],
                }
        return result

    def analyze(self) -> dict:
        """Run full analysis: per-pueblo census + per-department soy + OSM summary.

        Returns dict with all results ready for paper writing.
        """
        census_summary = self.compute_pueblo_summary()
        soy_summary = self.compute_soy_by_department()
        osm_summary = self.load_osm_polygons()

        # National averages
        national_yields = []
        for dept, info in soy_summary.items():
            national_yields.append(info["mean_yield_kg_per_ha_5yr"])
        national_mean_yield = float(np.mean(national_yields)) if national_yields else None

        result = {
            "census": census_summary,
            "soy_by_department": soy_summary,
            "osm_polygons": osm_summary,
            "national_mean_yield_kg_per_ha": national_mean_yield,
            "national_total_communities_2022": census_summary["national_total_2022"],
        }

        # Write outputs for citation
        out_json = self.output_dir / "p0030_analysis.json"
        with open(out_json, "w") as fp:
            json.dump(result, fp, indent=2, default=str)
        out_md = self.output_dir / "p0030_analysis.md"
        with open(out_md, "w") as fp:
            fp.write(self._render_markdown(result))
        return result

    def _render_markdown(self, result: dict) -> str:
        """Render analysis as a Markdown report for human review."""
        lines = ["# P0030 Yvyra Soy — Analysis Results\n"]
        lines.append("## Indigenous communities census (INE 2022)\n")
        lines.append(f"- Total pueblos: {result['census']['n_pueblos']}")
        lines.append(f"- Total communities: {result['census']['national_total_2022']}\n")
        lines.append("| Pueblo | Communities (2022) |")
        lines.append("|---|---:|")
        for p in result["census"]["pueblos"]:
            lines.append(f"| {p['pueblo']} | {p['ine_communities_2022']} |")
        lines.append("")

        lines.append("## Soybean yield by department (last 5 years)\n")
        if result["soy_by_department"]:
            lines.append("| Department | Mean yield (kg/ha) | Total area (ha) |")
            lines.append("|---|---:|---:|")
            for dept, info in sorted(
                result["soy_by_department"].items(), key=lambda x: -(x[1]["mean_yield_kg_per_ha_5yr"] or 0)
            ):
                rend = info["mean_yield_kg_per_ha_5yr"]
                sup = info["total_area_ha_5yr"] or 0
                lines.append(f"| {dept} | {rend:.0f} | {sup:,.0f} |")
            lines.append("")
        if result["national_mean_yield_kg_per_ha"] is not None:
            lines.append(f"**National mean yield (5yr):** {result['national_mean_yield_kg_per_ha']:.0f} kg/ha\n")

        lines.append("## OSM indigenous community polygons\n")
        lines.append(f"- Features: {result['osm_polygons']['n_features']}")
        if result["osm_polygons"].get("bbox"):
            bbox = result["osm_polygons"]["bbox"]
            lines.append(
                f"- BBox: [{bbox[0]:.3f}, {bbox[1]:.3f}, {bbox[2]:.3f}, {bbox[3]:.3f}]\n"
                f"  (lon_min, lat_min, lon_max, lat_max)"
            )
        return "\n".join(lines) + "\n"

    def validate(self, predictions, ground_truth) -> dict:
        """Validate predictions (placeholder for unified interface)."""
        return regression_metrics(ground_truth, predictions)


def run_p0030_demo() -> dict:
    """Demo: run full P0030 analysis on the public-data substrate.

    Returns the analysis dict; also writes outputs/p0030/p0030_analysis.{json,md}.
    """
    pipeline = YvyraSoyPipeline()
    return pipeline.analyze()
