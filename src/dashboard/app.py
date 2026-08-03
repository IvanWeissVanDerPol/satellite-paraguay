"""Streamlit dashboard for SatelliteCV-Paraguay.

Visualizes:
- Hansen GFC real data (forest loss)
- MapBiomas real data (land cover)
- Sentinel-2 real data (optical imagery)
- P0011 pilot metrics
- Weekly cron results

Run:
    streamlit run src/dashboard/app.py
"""
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

st.set_page_config(
    page_title="SatelliteCV-Paraguay",
    page_icon="🛰️",
    layout="wide",
)

st.title("🛰️ SatelliteCV-Paraguay")
st.markdown("**Multi-temporal Earth observation of Paraguay from foundation models to field deployment**")

# Sidebar
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", [
    "📊 Overview",
    "🌳 Hansen Deforestation",
    "🗺️ MapBiomas Land Cover",
    "🛰️ Sentinel-2 Imagery",
    "🤖 P0011 Pilot Results",
    "📈 Weekly Cron",
])


def show_overview():
    st.header("📊 Project Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Hansen data", "1.2 GB", "Real")
    with col2:
        st.metric("MapBiomas", "38 MB", "Real")
    with col3:
        st.metric("Sentinel-2", "1.5 GB", "6 files")
    with col4:
        st.metric("Total", "2.7 GB", "Real data")

    st.subheader("6 Papers")
    papers = [
        ("P0011", "Yvutu", "Deforestation", "Remote Sensing of Environment"),
        ("P0010", "Yvyra", "Carbon credits", "Nature Climate Change"),
        ("P0012", "Yvy", "Indigenous conflict", "World Development"),
        ("P0025", "Yrupe", "Soybean yield", "Comp & Elec in Agriculture"),
        ("P0026", "Kai", "Wildlife poaching", "Conservation Biology"),
        ("P0035", "Tatakua", "Air quality", "Atmospheric Environment"),
    ]
    for code, guarani, topic, journal in papers:
        st.markdown(f"- **{code} {guarani}**: {topic} → _{journal}_")


def show_hansen():
    st.header("🌳 Hansen Global Forest Change")
    st.markdown("""
    **Source:** Hansen/UMD/Google/USGS/NASA (Hansen et al., Science 2013)
    **URL:** https://storage.googleapis.com/earthenginepartners-hansen/
    **Coverage:** Paraguay (lat -20 to -30, lon -50 to -70)
    """)

    hansen_dir = REPO_ROOT / "data/hansen"
    if not hansen_dir.exists():
        st.error("No Hansen data. Run: `python3 scripts/download_all_data.py --quick`")
        return

    files = sorted(hansen_dir.glob("*.tif"))
    st.write(f"**{len(files)} files:**")
    for f in files:
        size_mb = f.stat().st_size // 1024 // 1024
        st.write(f"  - `{f.name}` ({size_mb} MB)")

    # Load lossyear
    lossyear_path = hansen_dir / "hansen_lossyear_20S_060W.tif"
    if lossyear_path.exists():
        import rasterio
        with rasterio.open(lossyear_path) as src:
            st.write(f"**Tile 20S_060W:**")
            st.write(f"  - Shape: {src.shape}")
            st.write(f"  - CRS: {src.crs}")
            st.write(f"  - Bounds: {src.bounds}")
            st.write(f"  - Resolution: {src.res}")

            # Load chunk for visualization
            chunk = src.read(1, window=rasterio.windows.Window(8000, 12000, 2000, 2000))

            # Stats
            loss_years, counts = np.unique(chunk[chunk > 0], return_counts=True)
            st.write(f"  - Loss events (2001-2023):")
            for y, c in zip(loss_years, counts):
                st.write(f"    - {int(y) + 2000}: {c:,} pixels")

            # Visualization
            fig, ax = plt.subplots(figsize=(10, 8))
            im = ax.imshow(chunk, cmap="RdYlGn_r", vmin=0, vmax=24)
            ax.set_title("Hansen lossyear (20S_060W, 2000-2023)\nGreen=stable forest, Red=recent loss")
            plt.colorbar(im, ax=ax, label="Year of loss")
            st.pyplot(fig)

            # Annual loss chart
            fig2, ax2 = plt.subplots(figsize=(10, 5))
            ax2.bar(loss_years + 2000, counts, color="darkred", alpha=0.7)
            ax2.set_xlabel("Year")
            ax2.set_ylabel("Loss pixels")
            ax2.set_title("Annual forest loss (central Paraguay)")
            ax2.grid(True, alpha=0.3)
            st.pyplot(fig2)


def show_mapbiomas():
    st.header("🗺️ MapBiomas Paraguay")
    st.markdown("""
    **Source:** MapBiomas Paraguay Collection 2 (2023)
    **URL:** https://plataforma.mapbiomas.org/
    """)

    mb_path = REPO_ROOT / "data/mapbiomas/mapbiomas_paraguay_2023.tif"
    if not mb_path.exists():
        st.error("No MapBiomas data. Run: `python3 scripts/download_all_data.py --quick`")
        return

    import rasterio
    with rasterio.open(mb_path) as src:
        st.write(f"**Shape:** {src.shape}")
        st.write(f"**CRS:** {src.crs}")
        st.write(f"**Bounds:** {src.bounds}")

        chunk = src.read(1, window=rasterio.windows.Window(10000, 10000, 5000, 5000))

        # Class distribution
        unique, counts = np.unique(chunk, return_counts=True)
        # MapBiomas Paraguay Collection 2 legend
        legend = {
            0: "No data",
            1: "Forest",
            3: "Forest Formation",
            4: "Savanna Formation",
            6: "Wetland",
            9: "Forest Plantation",
            11: "Wetland",
            12: "Grassland",
            15: "Pasture",
            18: "Agriculture",
            22: "Mining",
            26: "Water",
        }

        st.subheader("Land Cover Classes (sample)")
        for u, c in zip(unique, counts):
            pct = c / chunk.size * 100
            name = legend.get(int(u), f"Class {u}")
            st.write(f"  - Class {int(u)} ({name}): {c:,} pixels ({pct:.2f}%)")

        # Visualization
        fig, ax = plt.subplots(figsize=(10, 8))
        colors = ["white", "darkgreen", "green", "olive", "lightblue", "purple",
                  "blue", "yellow", "tan", "orange", "red", "cyan"]
        cmap = ListedColormap(colors[:max(unique) + 1])
        im = ax.imshow(chunk, cmap=cmap, vmin=0, vmax=max(unique))
        ax.set_title("MapBiomas Paraguay 2023 (sample)")
        cbar = plt.colorbar(im, ax=ax, ticks=range(max(unique) + 1))
        cbar.set_label("Class ID")
        st.pyplot(fig)


def show_sentinel2():
    st.header("🛰️ Sentinel-2 Imagery")
    st.markdown("""
    **Source:** Microsoft Planetary Computer (free, no auth)
    **URL:** https://planetarycomputer.microsoft.com/
    """)

    s2_dir = REPO_ROOT / "data/sentinel2"
    if not s2_dir.exists():
        st.error("No Sentinel-2 data.")
        return

    files = sorted(s2_dir.glob("*.tif"))
    st.write(f"**{len(files)} files:**")
    for f in files:
        size_mb = f.stat().st_size // 1024 // 1024
        st.write(f"  - `{f.name}` ({size_mb} MB)")

    # Show RGB composite if we have multiple bands for same scene
    scenes = {}
    for f in files:
        # Extract scene ID and band
        parts = f.stem.split("_")
        scene_id = "_".join(parts[:7])
        band = parts[7]
        if scene_id not in scenes:
            scenes[scene_id] = {}
        scenes[scene_id][band] = f

    # Find scene with all RGB bands
    for scene_id, bands in scenes.items():
        if all(b in bands for b in ["B02", "B03", "B04"]):
            st.subheader(f"Scene: {scene_id}")
            try:
                import rasterio
                rgb = []
                for b in ["B04", "B03", "B02"]:  # R, G, B
                    with rasterio.open(bands[b]) as src:
                        # Read 2000x2000 chunk
                        chunk = src.read(1, window=rasterio.windows.Window(2000, 2000, 2000, 2000))
                        # Normalize
                        chunk = chunk.astype(float) / max(chunk.max(), 1) * 255
                        rgb.append(chunk.astype(np.uint8))
                rgb = np.stack(rgb, axis=-1)

                fig, ax = plt.subplots(figsize=(10, 10))
                ax.imshow(rgb)
                ax.set_title(f"True color (R=B04, G=B03, B=B02)\n{scene_id}")
                ax.axis("off")
                st.pyplot(fig)
                break
            except Exception as e:
                st.error(f"Failed: {e}")


def show_p0011():
    st.header("🤖 P0011 Yvutu Pilot Results")
    st.markdown("""
    **Paper:** Multi-temporal satellite computer vision for Chaco deforestation
    **Target:** Remote Sensing of Environment
    """)

    # Show metrics
    metrics_path = REPO_ROOT / "outputs/p0011/metrics.json"
    if metrics_path.exists():
        import json
        metrics = json.loads(metrics_path.read_text())

        st.subheader("Pilot Metrics")
        col1, col2, col3, col4 = st.columns(4)
        for i, (model, m) in enumerate(metrics.items()):
            with [col1, col2, col3, col4][i % 4]:
                if isinstance(m, dict):
                    f1 = m.get("f1_macro", m.get("f1", 0))
                    st.metric(model, f"F1={f1:.3f}")

    # Show figures
    fig_dir = REPO_ROOT / "outputs/p0011/figures"
    if fig_dir.exists():
        st.subheader("Figures")
        for fig_file in sorted(fig_dir.glob("*.png")):
            st.image(str(fig_file), caption=fig_file.name)


def show_weekly():
    st.header("📈 Weekly Cron Results")
    weekly_dir = REPO_ROOT / "outputs/weekly"
    if weekly_dir.exists():
        logs = sorted(weekly_dir.glob("*.log"))
        st.write(f"**{len(logs)} runs:**")
        for log in logs[-5:]:  # last 5
            with open(log) as f:
                content = f.read()
            st.code(content, language="text")


# Page router
if page == "📊 Overview":
    show_overview()
elif page == "🌳 Hansen Deforestation":
    show_hansen()
elif page == "🗺️ MapBiomas Land Cover":
    show_mapbiomas()
elif page == "🛰️ Sentinel-2 Imagery":
    show_sentinel2()
elif page == "🤖 P0011 Pilot Results":
    show_p0011()
elif page == "📈 Weekly Cron":
    show_weekly()

st.sidebar.markdown("---")
st.sidebar.markdown("[GitHub](https://github.com/IvanWeissVanDerPol/satellite-paraguay)")