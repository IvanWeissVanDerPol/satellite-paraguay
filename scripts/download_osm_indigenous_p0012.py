#!/usr/bin/env python3
"""download_osm_indigenous_p0012.py — Fetch indigenous community polygons
from OpenStreetMap for P0012 Yvy.

Uses the Overpass API to query Paraguay's OSM data for relations
named "Comunidad ..." (admin_level 10/11 = local indigenous community
boundaries). Saves the result as EPSG:4326 GeoJSON.

Source: OpenStreetMap via Overpass API
       (https://overpass-api.de/ or one of its mirrors)
License: ODbL 1.0 (OpenStreetMap)
         https://opendatacommons.org/licenses/odbl/1-0/

Coverage: ~30 of ~557 INE-2022 communities (only those that have
polygon outer ways mapped in OSM). For the full list, see
data/raw/ine_indi/indigenous_communities_2022_summary.csv.

Usage:
  python3 scripts/download_osm_indigenous_p0012.py
  python3 scripts/download_osm_indigenous_p0012.py --mirror kumi
  python3 scripts/download_osm_indigenous_p0012.py --out-dir data/raw/osm_indigenous
"""

import argparse
import json
import os
import sys
from pathlib import Path

import requests
from shapely.geometry import MultiPolygon, Polygon, mapping

REPO_ROOT = Path(__file__).resolve().parent.parent
OVERPASS_MIRRORS = [
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
    "https://overpass.private.coffee/api/interpreter",
]
HEADERS = {"User-Agent": "satellite-paraguay-thesis/1.0 (mailto:ivan@fpuna.edu.py)"}
QUERY = """[out:json][timeout:120];
area["ISO3166-1"="PY"]->.a;
(
  relation["name"~"^Comunidad",i](area.a);
);
out geom;"""


def fetch_overpass(mirror: str) -> dict:
    r = requests.post(
        mirror,
        data={"data": QUERY},
        headers=HEADERS,
        timeout=180,
    )
    r.raise_for_status()
    return dict(r.json())


def overpass_to_geojson(raw: dict) -> dict:
    """Convert Overpass response to GeoJSON FeatureCollection."""
    features = []
    for e in raw.get("elements", []):
        tags = e.get("tags", {})
        outer_polys = []
        for m in e.get("members", []):
            if m.get("role") != "outer":
                continue
            coords = [(p["lon"], p["lat"]) for p in m.get("geometry", [])]
            if len(coords) >= 4:  # closed ring
                try:
                    outer_polys.append(Polygon(coords))
                except Exception:  # invalid geometry — skip
                    pass
        if not outer_polys:
            continue
        geom = MultiPolygon(outer_polys) if len(outer_polys) > 1 else outer_polys[0]
        features.append(
            {
                "type": "Feature",
                "properties": {
                    "osm_id": e["id"],
                    "osm_type": e["type"],
                    "name": tags.get("name", ""),
                    "name_es": tags.get("name:es", ""),
                    "admin_level": tags.get("admin_level", ""),
                    "place": tags.get("place", ""),
                },
                "geometry": mapping(geom),
            }
        )
    return {
        "type": "FeatureCollection",
        "features": features,
        "metadata": {
            "source": "OpenStreetMap via Overpass API",
            "license": "ODbL 1.0 (https://opendatacommons.org/licenses/odbl/1-0/)",
            "tag_filter": 'relation["name"~"^Comunidad",i]',
            "bbox_paraguay": "(-62.5, -27.5, -54.0, -19.0)",
            "count": len(features),
            "note": (
                "admin_level=10/11 = local-level indigenous community "
                "boundaries. ~30 of ~557 INE-2022 communities have "
                "OSM polygon geometries; the rest are points or "
                "unmapped. For full coverage, use the INE census "
                "list (data/raw/ine_indi/) + a FPIC-engaged INDI "
                "shapefile."
            ),
        },
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--mirror", choices=["de", "kumi", "private"], default="kumi")
    p.add_argument("--out-dir", default=str(REPO_ROOT / "data/raw/osm_indigenous"))
    args = p.parse_args()

    mirror = {
        "de": OVERPASS_MIRRORS[0],
        "kumi": OVERPASS_MIRRORS[1],
        "private": OVERPASS_MIRRORS[2],
    }[args.mirror]

    print(f"Fetching Overpass API at {mirror}...")
    raw = fetch_overpass(mirror)
    print(f"  returned {len(raw.get('elements', []))} elements")
    geojson = overpass_to_geojson(raw)
    print(f"  parsed {len(geojson['features'])} polygon features")

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "osm_comunidades_indigenas_py.geojson"
    with open(out_path, "w") as f:
        json.dump(geojson, f)
    print(f"  saved {out_path} ({os.path.getsize(out_path) / 1024:.1f} KB)")


if __name__ == "__main__":
    sys.exit(main())
