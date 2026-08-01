"""Generate data catalog from paraguay-geodata + remote sources."""
import json
from pathlib import Path
from datetime import datetime

OUT = Path("docs/DATA_CATALOG.md")


def main():
    catalog = []

    # Local data
    pg_dir = Path("/root/paraguay-geodata/exports/web/data")
    local_files = [
        ("tile_index.json", "Tile index for Paraguay (10x10 km grid)", "JSON"),
        ("roads.geojson", "OSM roads in Paraguay", "GeoJSON"),
        ("buildings_asuncion.geojson", "OSM building footprints in Asunción", "GeoJSON"),
        ("catastro_parcels_sample.geojson", "Catastro land parcels (sample)", "GeoJSON"),
        ("catastro_urba.geojson", "Catastro urban developments", "GeoJSON"),
        ("properties_latest.geojson", "Real estate listings (latest)", "GeoJSON"),
        ("properties_scrubbed.geojson", "Real estate listings (PII-scrubbed)", "GeoJSON"),
        ("architect_export.geojson", "Architectural building export", "GeoJSON"),
        ("water.geojson", "Water bodies in Paraguay", "GeoJSON"),
        ("indigenous_territories.geojson", "Indigenous community territories", "GeoJSON"),
        ("climate_risk.geojson", "Climate risk layer", "GeoJSON"),
        ("flood_risk.geojson", "Flood risk layer", "GeoJSON"),
        ("gbif_paraguay.geojson", "GBIF species observations in Paraguay", "GeoJSON"),
        ("bcp_snapshot.json", "BCP macroeconomic snapshot", "JSON"),
        ("nasa_power_asuncion.json", "NASA POWER climate data for Asunción", "JSON"),
        ("inbio_zafra_2025_2026.json", "INBIO crop area 2025-2026", "JSON"),
    ]

    for fname, desc, fmt in local_files:
        f = pg_dir / fname
        if f.exists():
            catalog.append({
                "name": fname,
                "format": fmt,
                "size_mb": round(f.stat().st_size / (1024 * 1024), 2),
                "source": "local: paraguay-geodata",
                "license": "varies (mostly open)",
                "description": desc,
                "path": str(f),
            })

    # Remote data
    remote_sources = [
        ("Sentinel-2 L2A", "ESA Copernicus", "CC0", "10m, 5-day"),
        ("Landsat 9 L2", "NASA", "CC0", "30m, 16-day"),
        ("Planet (academic)", "Planet.com", "CC BY-NC academic", "3m, daily"),
        ("MapBiomas Paraguay", "MapBiomas", "CC0", "Land cover 1985-2024"),
        ("Hansen GFC", "GFW", "CC0", "Forest loss 2000-2023"),
        ("ESA WorldCover", "ESA", "CC0", "10m land cover 2020/2021"),
        ("WorldClim", "WorldClim", "CC0", "Climate normals"),
        ("ERA5", "ECMWF Copernicus", "CC0", "Hourly climate 1959-present"),
        ("Verra VCS Registry", "Verra", "Public API", "Carbon credit projects"),
        ("Gold Standard", "Gold Standard", "Public", "Carbon credit projects"),
        ("NASA FIRMS", "NASA", "CC0", "Fire alerts MODIS/VIIRS"),
        ("OpenAQ", "OpenAQ", "CC0", "Air quality measurements"),
        ("Sentinel-5P", "ESA Copernicus", "CC0", "Atmospheric NO2/SO2/CO"),
        ("GBIF", "GBIF", "CC0", "Biodiversity observations"),
        ("INFONA forestry", "INFONA Paraguay", "Open", "Forestry registry"),
        ("DGEEC", "Paraguay statistics", "Open", "Demographics"),
    ]

    for name, src, license, desc in remote_sources:
        catalog.append({
            "name": name,
            "format": "remote",
            "size_mb": None,
            "source": src,
            "license": license,
            "description": desc,
            "path": "remote",
        })

    # Write markdown catalog
    with open(OUT, "w") as f:
        f.write("# Data Catalog\n\n")
        f.write(f"Generated: {datetime.now().isoformat()}\n\n")
        f.write(f"Total items: {len(catalog)}\n")
        f.write(f"Local items: {sum(1 for c in catalog if c['source'].startswith('local'))}\n")
        f.write(f"Remote items: {sum(1 for c in catalog if not c['source'].startswith('local'))}\n\n")

        f.write("## Local Data\n\n")
        f.write("| File | Format | Size (MB) | Description |\n")
        f.write("|------|--------|-----------|-------------|\n")
        for c in catalog:
            if c["source"].startswith("local"):
                f.write(f"| `{c['name']}` | {c['format']} | {c['size_mb']} | {c['description']} |\n")

        f.write("\n## Remote Data Sources\n\n")
        f.write("| Source | Provider | License | Description |\n")
        f.write("|--------|----------|---------|-------------|\n")
        for c in catalog:
            if not c["source"].startswith("local"):
                f.write(f"| **{c['name']}** | {c['source']} | {c['license']} | {c['description']} |\n")

        f.write("\n## How to Fetch Remote Data\n\n")
        f.write("```bash\n")
        f.write("# All downloads go through make targets\n")
        f.write("make data-sentinel      # Sentinel-2\n")
        f.write("make data-mapbiomas     # MapBiomas\n")
        f.write("make data-all           # everything\n")
        f.write("```\n")

    print(f"Catalog written to {OUT}")
    print(f"  Local items: {sum(1 for c in catalog if c['source'].startswith('local'))}")
    print(f"  Remote items: {sum(1 for c in catalog if not c['source'].startswith('local'))}")


if __name__ == "__main__":
    main()
