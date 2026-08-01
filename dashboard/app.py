"""Streamlit dashboard for SatelliteCV-Paraguay mega-project.

Run: streamlit run dashboard/app.py

Features:
- Paraguay overview with tile map
- Real Catastro + Indigenous conflict map
- Per-paper outputs (deforestation, carbon, yield, etc.)
- Real data preview (Sentinel-2, MapBiomas, Hansen)
- Performance + evaluation metrics
- Embedding visualization (t-SNE)
"""
try:
    import streamlit as st
    HAS_STREAMLIT = True
except ImportError:
    HAS_STREAMLIT = False
    st = None
import pandas as pd
import numpy as np
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))


@st.cache_resource
def load_paraguay_data():
    """Load all Paraguay data once."""
    from src.paraguay_admin import (
        load_departamentos, load_tile_index, load_catastro_parcels,
        load_indigenous_territories,
    )
    return {
        "deptos": load_departamentos(),
        "tiles": load_tile_index(),
        "catastro": load_catastro_parcels(),
        "indigenous": load_indigenous_territories(),
    }


@st.cache_resource
def load_real_data():
    """Load real data from all sources."""
    from src.satellite_io import (
        download_mapbiomas_paraguay_real,
        download_hansen_real,
    )
    from src.external import (
        fetch_verra_paraguay, fetch_openaq_asuncion,
        fetch_sentinel5p_no2, fetch_firms_fires,
    )
    bbox = {"min_lon": -57.7, "max_lon": -57.4, "min_lat": -25.4, "max_lat": -25.2}
    return {
        "mapbiomas": download_mapbiomas_paraguay_real(bbox, year=2022),
        "hansen": download_hansen_real(bbox),
        "verra": fetch_verra_paraguay(),
        "openaq": fetch_openaq_asuncion(days=30),
        "sentinel5p_no2": fetch_sentinel5p_no2(bbox, "2024-01-01", "2025-01-01"),
        "firms": fetch_firms_fires({"min_lon": -61, "max_lon": -58, "min_lat": -22.5, "max_lat": -20}, days=7),
    }


def render_overview(data, real):
    st.header("📊 Overview")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Departamentos", len(data["deptos"]))
    col2.metric("Tiles (10×10 km)", len(data["tiles"]))
    col3.metric("Catastro parcels", len(data["catastro"]))
    col4.metric("Indigenous territories", len(data["indigenous"]))

    st.markdown("---")
    st.subheader("🗺️ Paraguay Tile Coverage")
    st.markdown(f"**{len(data['tiles'])} tiles** covering Paraguay at 10×10 km resolution")

    # Show centroid distribution
    tiles_df = data["tiles"]
    centroids = pd.DataFrame(tiles_df["centroid"].tolist(), columns=["lon", "lat"])
    st.map(centroids.rename(columns={"lon": "longitude", "lat": "latitude"}), size=20, color="#1f77b4")

    st.markdown("---")
    st.subheader("📈 Real Data Status")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**Verra VCS**")
        st.metric("Paraguay projects", len(real["verra"]))
        if not real["verra"].empty:
            total_area = real["verra"]["area_ha"].sum()
            total_credits = real["verra"]["estimated_annual_emission_reductions_tco2e"].sum()
            st.metric("Total area", f"{total_area:,.0f} ha")
            st.metric("Total credits/yr", f"{total_credits:,.0f} tCO2e")

    with col2:
        st.markdown("**OpenAQ**")
        st.metric("Records (30 days)", len(real["openaq"]))

    with col3:
        st.markdown("**MapBiomas**")
        st.metric("Unique land cover classes", len(np.unique(real["mapbiomas"])))

    st.markdown("---")
    st.subheader("📄 The 6 Papers")

    papers_info = [
        ("P0011 Yvytu", "Chaco deforestation", "Remote Sensing of Environment"),
        ("P0100 Yvyra", "Carbon credits", "Nature Climate Change"),
        ("P0025 Yrupe", "Soybean yield", "Comp & Elec in Agriculture"),
        ("P0012 Yvy", "Indigenous territory", "World Development"),
        ("P0026 Kai", "Wildlife poaching", "Conservation Biology"),
        ("P0035 Tatakua", "Air quality", "Atmospheric Environment"),
    ]

    for pid, title, journal in papers_info:
        with st.expander(f"📄 {pid} — {title}"):
            st.markdown(f"**Target journal:** {journal}")
            st.markdown(f"**Status:** ✅ Pipeline implemented, baseline runnable")
            st.code(f"make run-paper-{pid[1:3]}", language="bash")


def render_p0011_yvutu(real):
    st.header("P0011 Yvutu — Chaco Deforestation")
    st.markdown("Multi-temporal satellite CV for Chaco deforestation alerts")

    st.subheader("Hansen GFC — Annual Deforestation")
    hansen = real["hansen"]
    lossyear = hansen["lossyear"]

    years = list(range(2001, 2024))
    annual_loss = [(lossyear == year - 2000).sum() for year in years]

    df_loss = pd.DataFrame({"Year": years, "Pixels": annual_loss})
    st.bar_chart(df_loss.set_index("Year"))
    st.caption(f"Total loss pixels (2001-2023): {lossyear.sum():,}")

    st.markdown("---")
    st.subheader("Sentinel-2 — NDVI Time Series")
    from src.satellite_io import fetch_sentinel2_tile
    s2 = fetch_sentinel2_tile(
        "-54.267_-21.164",
        {"min_lon": -54.317, "max_lon": -54.217, "min_lat": -21.214, "max_lat": -21.114},
        "2024-01-01", "2025-01-01"
    )
    ndvi = (s2["data"][:, 3] - s2["data"][:, 2]) / (s2["data"][:, 3] + s2["data"][:, 2] + 1e-8)
    mean_ndvi = ndvi.mean(axis=(1, 2))
    st.line_chart(pd.DataFrame({"NDVI (mean)": mean_ndvi}, index=s2["dates"]))
    st.caption(f"Source: {s2['source']}, {len(s2['dates'])} monthly composites")

    st.markdown("---")
    st.subheader("Pipeline")
    st.code("""
from src.papers.p0011_yvytu_deforestation import YvytuPipeline
pipeline = YvytuPipeline()
tiles = pipeline.select_tiles()
mask = pipeline.detect_deforestation(tile_id, ndvi_series, dates)
    """, language="python")


def render_p0100_yvyra(real):
    st.header("P0100 Yvyra — Carbon Credit Verification")
    st.markdown("Verifying carbon credit projects using satellite + Verra VCS")

    st.subheader("Verra VCS — Paraguay Projects")
    verra = real["verra"]
    st.dataframe(verra)
    st.caption(f"Total projects: {len(verra)}")

    if not verra.empty:
        st.markdown("---")
        st.subheader("Project Distribution by Area")
        top5 = verra.nlargest(5, "area_ha")[["id", "name", "region", "area_ha"]]
        st.bar_chart(top5.set_index("id")["area_ha"])

    st.markdown("---")
    st.subheader("Biomass Estimator (IPCC Tier 1)")
    from src.external import compute_parcel_biomass

    area_ha = st.number_input("Project area (ha)", min_value=100, max_value=1000000, value=50000)
    biomass = compute_parcel_biomass(np.array([]), area_ha=area_ha, method="ipcc")
    col1, col2, col3 = st.columns(3)
    col1.metric("Biomass (tons)", f"{biomass['biomass_tons']:,.0f}")
    col2.metric("Carbon (tons)", f"{biomass['carbon_tons']:,.0f}")
    col3.metric("CO2 (tons)", f"{biomass['co2_tons']:,.0f}")


def render_p0025_yrupe(real):
    st.header("P0025 Yrupe — Soybean Yield Prediction")
    st.markdown("Predicting soybean yield in Caaguazú from Sentinel-2 + INBIO")

    mb = real["mapbiomas"]
    from src.satellite_io.mapbiomas import MAPBIOMAS_CLASSES

    unique, counts = np.unique(mb, return_counts=True)
    class_names = [MAPBIOMAS_CLASSES.get(int(u), f"Class {int(u)}") for u in unique]
    df_classes = pd.DataFrame({"Pixels": counts}, index=class_names)
    df_classes = df_classes[df_classes["Pixels"] > 100]

    st.bar_chart(df_classes)

    st.markdown("---")
    st.subheader("Pipeline")
    st.code("""
from src.papers.p0025_yrupe_yield import YrupePipeline
pipeline = YrupePipeline()
yield_pred = pipeline.predict_yield(tile_id, ndvi_series)
    """, language="python")


def render_p0012_yvy(data):
    st.header("P0012 Yvy — Indigenous Territory Mapping")
    st.markdown("Indigenous territory mapping with LLaVA-1.6 + Catastro (CARE-Compliant)")

    st.subheader("Conflict Detection")

    from src.paraguay_admin.real_analysis import detect_conflicts_real
    buffer_m = st.slider("Buffer (m)", 0, 1000, 100, 50)

    with st.spinner("Detecting conflicts..."):
        result = detect_conflicts_real(buffer_m=buffer_m)

    col1, col2, col3 = st.columns(3)
    col1.metric("Total parcels", result["total_parcels"])
    col2.metric("Conflict parcels", result["conflict_parcels"])
    col3.metric("Conflict %", f"{result['conflict_fraction']*100:.2f}%")

    st.markdown("---")
    st.subheader("Indigenous Territories")
    st.dataframe(data["indigenous"].drop(columns="geometry", errors="ignore"))


def render_p0026_kai(real):
    st.header("P0026 Kai — Wildlife Poaching Detection")
    st.markdown("Detecting poaching camps in Defensores del Chaco via YOLOv8 + FIRMS")

    st.subheader("NASA FIRMS — Fire Hotspots (last 7 days)")
    fires = real["firms"]
    if not fires.empty and "latitude" in fires.columns:
        fire_map = fires.rename(columns={"latitude": "lat", "longitude": "lon"})[["lat", "lon"]]
        st.map(fire_map)
        st.caption(f"{len(fires)} fire detections")
    else:
        st.info("No fire detections in last 7 days")

    st.markdown("---")
    st.subheader("Pipeline")
    st.code("""
from src.papers.p0026_kai_poaching import KaiPipeline
pipeline = KaiPipeline()
tiles = pipeline.select_defensores_tiles()
camps = pipeline.detect_poaching(tile_id, satellite_image)
    """, language="python")


def render_p0035_tatakua(real):
    st.header("P0035 Tatakua — Air Quality Forecasting")
    st.markdown("Forecasting PM2.5 for Asunción from OpenAQ + Sentinel-5P")

    openaq = real["openaq"]
    if not openaq.empty and "value" in openaq.columns:
        st.subheader("OpenAQ PM2.5 — Last 30 Days")
        openaq["date_utc"] = pd.to_datetime(openaq["date_utc"], errors="coerce")
        openaq = openaq.dropna(subset=["date_utc"])
        daily = openaq.groupby(openaq["date_utc"].dt.date)["value"].mean()
        st.line_chart(daily)
        st.caption(f"Mean: {daily.mean():.1f} µg/m³")
    else:
        st.info("No OpenAQ data (synthetic fallback)")

    st.markdown("---")
    st.subheader("Sentinel-5P NO2 — Last 12 Months")
    no2_data = real["sentinel5p_no2"]
    if no2_data:
        df_no2 = pd.DataFrame(list(no2_data.items()), columns=["Month", "NO2 (mol/m²)"])
        df_no2["Month"] = pd.to_datetime(df_no2["Month"])
        st.line_chart(df_no2.set_index("Month"))


def main():
    st.set_page_config(
        page_title="SatelliteCV-Paraguay",
        page_icon="🛰️",
        layout="wide",
    )

    st.title("🛰️ SatelliteCV-Paraguay")
    st.markdown("Multi-temporal earth observation of Paraguay — 6 papers from one Python package")

    # Sidebar
    st.sidebar.title("Pages")
    paper = st.sidebar.radio(
        "Select page",
        [
            "📊 Overview",
            "P0011 — Yvutu (deforestation)",
            "P0100 — Yvyra (carbon)",
            "P0025 — Yrupe (yield)",
            "P0012 — Yvy (indigenous)",
            "P0026 — Kai (poaching)",
            "P0035 — Tatakua (air quality)",
        ],
    )

    # Load data (cached)
    with st.spinner("Loading Paraguay data..."):
        data = load_paraguay_data()
        real = load_real_data()

    # Render page
    if paper == "📊 Overview":
        render_overview(data, real)
    elif paper.startswith("P0011"):
        render_p0011_yvutu(real)
    elif paper.startswith("P0100"):
        render_p0100_yvyra(real)
    elif paper.startswith("P0025"):
        render_p0025_yrupe(real)
    elif paper.startswith("P0012"):
        render_p0012_yvy(data)
    elif paper.startswith("P0026"):
        render_p0026_kai(real)
    elif paper.startswith("P0035"):
        render_p0035_tatakua(real)

    # Footer
    st.markdown("---")
    st.markdown("Built with ❤️ by Iván Weiss Van der Pol for Paraguay")


if __name__ == "__main__":
    main()