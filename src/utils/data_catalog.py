"""Data catalog generation from local Paraguay geodata + remote sources.

Generates docs/DATA_CATALOG.md from local files and a curated list of remote
data sources.
"""

from datetime import datetime
from pathlib import Path
from typing import Any

LOCAL_DATA_FILES = [
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

REMOTE_SOURCES = [
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


def build_catalog(local_dir: Path) -> list[dict[str, Any]]:
    """Build list of catalog entries from local + remote sources."""
    catalog: list[dict[str, Any]] = []

    for fname, desc, fmt in LOCAL_DATA_FILES:
        f = local_dir / fname
        if f.exists():
            catalog.append(
                {
                    "name": fname,
                    "format": fmt,
                    "size_mb": round(f.stat().st_size / (1024 * 1024), 2),
                    "source": "local: paraguay-geodata",
                    "license": "varies (mostly open)",
                    "description": desc,
                    "path": str(f),
                }
            )

    for name, src, license, desc in REMOTE_SOURCES:
        catalog.append(
            {
                "name": name,
                "format": "remote",
                "size_mb": None,
                "source": src,
                "license": license,
                "description": desc,
                "path": "remote",
            }
        )

    return catalog


def count_local_remote(catalog: list[dict[str, Any]]) -> dict[str, int]:
    """Count local and remote entries in catalog."""
    local = sum(1 for c in catalog if c["source"].startswith("local"))
    return {"local": local, "remote": len(catalog) - local}


def render_markdown(catalog: list[dict[str, Any]]) -> str:
    """Render catalog as markdown document."""
    counts = count_local_remote(catalog)
    lines = [
        "# Data Catalog",
        "",
        f"Generated: {datetime.now().isoformat()}",
        "",
        f"Total items: {len(catalog)}",
        f"Local items: {counts['local']}",
        f"Remote items: {counts['remote']}",
        "",
        "## Local Data",
        "",
        "| File | Format | Size (MB) | Description |",
        "|------|--------|-----------|-------------|",
    ]
    for c in catalog:
        if c["source"].startswith("local"):
            lines.append(f"| `{c['name']}` | {c['format']} | {c['size_mb']} | {c['description']} |")

    lines.extend(
        [
            "",
            "## Remote Data Sources",
            "",
            "| Source | Provider | License | Description |",
            "|--------|----------|---------|-------------|",
        ]
    )
    for c in catalog:
        if not c["source"].startswith("local"):
            lines.append(f"| **{c['name']}** | {c['source']} | {c['license']} | {c['description']} |")

    lines.extend(
        [
            "",
            "## How to Fetch Remote Data",
            "",
            "```bash",
            "# All downloads go through make targets",
            "make data-sentinel      # Sentinel-2",
            "make data-mapbiomas     # MapBiomas",
            "make data-all           # everything",
            "```",
        ]
    )

    return "\n".join(lines) + "\n"


def generate_data_catalog(local_dir: Path, output_path: Path) -> dict[str, int]:
    """Generate data catalog markdown. Returns counts."""
    catalog = build_catalog(local_dir)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_markdown(catalog))
    return count_local_remote(catalog)
