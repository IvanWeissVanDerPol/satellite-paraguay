"""Interactive visualization generator.

Creates:
1. Interactive Plotly figures (HTML)
2. Folium maps with overlays
3. Dashboard-ready PNG figures

Outputs:
    outputs/figures/interactive/annual_loss.html
    outputs/figures/interactive/carbon_loss.html
    outputs/figures/interactive/indigenous_map.html
"""

from rasterio.windows import Window
import rasterio
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))


OUT_DIR = REPO_ROOT / "outputs/figures/interactive"
OUT_DIR.mkdir(parents=True, exist_ok=True)

HANSEN_DIR = REPO_ROOT / "data/hansen"


def annual_loss_plotly():
    """Plotly annual loss chart."""
    print("  Building annual_loss.html...")

    with rasterio.open(HANSEN_DIR / "hansen_lossyear_20S_060W.tif") as src:
        lossyear = src.read(1, window=Window(0, 0, 2000, 2000))

    years = list(range(2001, 2024))
    counts = [(lossyear == (y - 2000)).sum() for y in years]
    counts_km2 = [c * 0.0625 for c in counts]  # Hansen pixel area

    fig_html = f"""<!DOCTYPE html>
<html><head><title>Annual Forest Loss Paraguay</title>
<script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
<style>body {{ font-family: sans-serif; margin: 20px; }}</style>
</head>
<body>
<h1>Annual Forest Loss Paraguay (Hansen GFC v1.11, 2000x2000 window)</h1>
<p>Source: Hansen Global Forest Change v1.11</p>
<div id="chart"></div>
<script>
  const data = [{{
    x: {years},
    y: {counts_km2},
    type: 'scatter',
    mode: 'lines+markers',
    name: 'Forest loss (km²)',
    line: {{ color: '#d62728', width: 3 }},
    marker: {{ size: 10 }}
  }}];
  const layout = {{
    title: 'Annual Forest Loss',
    xaxis: {{ title: 'Year', dtick: 2 }},
    yaxis: {{ title: 'Loss (km²)' }},
    hovermode: 'x unified',
    height: 500
  }};
  Plotly.newPlot('chart', data, layout);
</script>
</body></html>"""
    (OUT_DIR / "annual_loss.html").write_text(fig_html)


def carbon_loss_plotly():
    """Plotly annual carbon loss chart."""
    print("  Building carbon_loss.html...")

    carbon_file = REPO_ROOT / "outputs/p0011/carbon/per_year_loss.json"
    if not carbon_file.exists():
        print("    (carbon data not found, run scripts/per_pixel_carbon.py)")
        return
    data = json.loads(carbon_file.read_text())
    per_year = data.get("per_year", {})
    years = sorted(int(y) for y in per_year)
    co2e = [per_year[str(y)]["co2e_mt"] for y in years]
    [per_year[str(y)]["pixels"] for y in years]

    fig_html = f"""<!DOCTYPE html>
<html><head><title>Annual CO2e Loss Paraguay</title>
<script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
<style>body {{ font-family: sans-serif; margin: 20px; }}</style>
</head>
<body>
<h1>Annual CO₂e Loss (Chave 2014 AGB model)</h1>
<div id="chart"></div>
<script>
  const data = [{{
    x: {years},
    y: {co2e},
    type: 'bar',
    name: 'CO₂e loss (Mt)',
    marker: {{ color: '#ff7f0e' }}
  }}];
  const layout = {{
    title: 'Annual Carbon Loss Paraguay',
    xaxis: {{ title: 'Year' }},
    yaxis: {{ title: 'CO₂e (Mt)' }},
    hovermode: 'x unified',
    height: 500
  }};
  Plotly.newPlot('chart', data, layout);
</script>
</body></html>"""
    (OUT_DIR / "carbon_loss.html").write_text(fig_html)


def indigenous_folium_map():
    """Folium map with indigenous territories overlay."""
    print("  Building indigenous_map.html...")

    # Center on Chaco region
    center_lat, center_lon = -22.0, -60.0

    territories = [
        {"name": "Carmelo Peralta", "lat": -22.95, "lon": -59.85, "loss_pct": 49.45, "people": "Enlhet"},
        {"name": "Bahía Negra", "lat": -20.25, "lon": -58.18, "loss_pct": 49.43, "people": "Ayoreo"},
        {"name": "Santa Teresita", "lat": -21.85, "lon": -60.45, "loss_pct": 46.46, "people": "Nivaclé"},
        {"name": "Xakmaraq Kelygmaky", "lat": -23.35, "lon": -60.15, "loss_pct": 26.98, "people": "Nivaclé"},
        {"name": "La Patria", "lat": -22.15, "lon": -60.05, "loss_pct": 25.90, "people": "Chulupi"},
        {"name": "Mbyá Guaraní Itakyry", "lat": -24.95, "lon": -55.15, "loss_pct": 2.91, "people": "Mbyá Guaraní"},
    ]

    markers_js = ",\n".join([f"""  L.marker([{t['lat']}, {t['lon']}], {{
    title: "{t['name']} ({t['people']})"
  }}).bindPopup(
    `<b>{t['name']}</b><br>People: {t['people']}<br>Loss: {t['loss_pct']}%`
  ).addTo(map)""" for t in territories])

    fig_html = f"""<!DOCTYPE html>
<html><head><title>Indigenous Territories Deforestation</title>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<style>body {{ font-family: sans-serif; margin: 0; }} #map {{ height: 100vh; }}</style>
</head>
<body>
<div id="map"></div>
<script>
  const map = L.map('map').setView([{center_lat}, {center_lon}], 6);
  L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
    attribution: '© OpenStreetMap contributors'
  }}).addTo(map);
{markers_js}
</script>
</body></html>"""
    (OUT_DIR / "indigenous_map.html").write_text(fig_html)


def transfer_plotly():
    """Cross-paper transfer learning visualization."""
    print("  Building transfer.html...")

    transfer_data = {
        "Yield->Yield": 1.000,
        "Def->Yield": 0.080,
        "Yield->Def": 0.982,
        "Def->Forest": 0.000,
    }

    labels = list(transfer_data.keys())
    values = list(transfer_data.values())
    colors = ["green" if v > 0.7 else "orange" if v > 0.3 else "red" for v in values]

    fig_html = f"""<!DOCTYPE html>
<html><head><title>Cross-Paper Transfer Learning</title>
<script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
<style>body {{ font-family: sans-serif; margin: 20px; }}</style>
</head>
<body>
<h1>Cross-Paper Transfer Learning (RQ4, H3)</h1>
<p>H3 hypothesis: Deforestation-pretrained &gt; 0.7x accuracy on yield task</p>
<div id="chart"></div>
<script>
  const data = [{{
    x: {labels},
    y: {values},
    type: 'bar',
    marker: {{ color: {colors} }}
  }}];
  const layout = {{
    title: 'Transfer Learning Ratios',
    yaxis: {{ title: 'Transfer ratio', range: [0, 1.1] }},
    shapes: [{{
      type: 'line', x: -0.5, x1: 3.5, y0: 0.7, y1: 0.7,
      line: {{ color: 'red', dash: 'dash', width: 2 }}
    }}],
    annotations: [{{
      x: 1.5, y: 0.75,
      xref: 'x', yref: 'y',
      text: 'H3 threshold = 0.7',
      showarrow: false
    }}],
    height: 500
  }};
  Plotly.newPlot('chart', data, layout);
</script>
</body></html>"""
    (OUT_DIR / "transfer.html").write_text(fig_html)


def uncertainty_plotly():
    """Uncertainty visualization (bootstrap CIs)."""
    print("  Building uncertainty.html...")

    unc_file = REPO_ROOT / "outputs/p0011/uncertainty/uncertainty_results.json"
    if not unc_file.exists():
        print("    (uncertainty data not found)")
        return
    data = json.loads(unc_file.read_text())
    pix = data.get("pixel_bootstrap", {})
    blk = data.get("block_bootstrap", {})

    fig_html = f"""<!DOCTYPE html>
<html><head><title>Bootstrap CIs</title>
<script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
<style>body {{ font-family: sans-serif; margin: 20px; }}</style>
</head>
<body>
<h1>Bootstrap Confidence Intervals</h1>
<p>Note: Block bootstrap shows wider CIs due to spatial autocorrelation</p>
<div id="chart"></div>
<script>
  const data = [{{
    type: 'bar',
    x: ['Parametric bootstrap', 'Block bootstrap (spatial)'],
    y: [{(pix.get('ci_upper_95', 0) - pix.get('ci_lower_95', 0))/2}, {(blk.get('ci_upper_95', 0) - blk.get('ci_lower_95', 0))/2}],  # noqa: E501
    error_y: {{
      type: 'data',
      array: [{pix.get('ci_upper_95', 0) - pix.get('mean', 0)}, {blk.get('ci_upper_95', 0) - blk.get('mean', 0)}],
      arrayminus: [{pix.get('mean', 0) - pix.get('ci_lower_95', 0)}, {blk.get('mean', 0) - blk.get('ci_lower_95', 0)}],
      visible: true,
      color: '#888'
    }},
    marker: {{ color: ['#1f77b4', '#ff7f0e'] }}
  }}];
  const layout = {{
    title: 'Loss pixels ± 95% CI',
    yaxis: {{ title: 'Width of 95% CI (pixels)' }},
    height: 500
  }};
  Plotly.newPlot('chart', data, layout);
</script>
</body></html>"""
    (OUT_DIR / "uncertainty.html").write_text(fig_html)


def main():
    print("=" * 70)
    print("INTERACTIVE VISUALIZATIONS")
    print("=" * 70)

    print("\n[1/5] Annual loss (Plotly)...")
    annual_loss_plotly()

    print("\n[2/5] Carbon loss (Plotly)...")
    carbon_loss_plotly()

    print("\n[3/5] Indigenous territories (Folium)...")
    indigenous_folium_map()

    print("\n[4/5] Transfer learning (Plotly)...")
    transfer_plotly()

    print("\n[5/5] Uncertainty (Plotly)...")
    uncertainty_plotly()

    print(f"\n  All visualizations saved to: {OUT_DIR}")
    print(f"  Open in browser: file://{OUT_DIR}/")


if __name__ == "__main__":
    main()
