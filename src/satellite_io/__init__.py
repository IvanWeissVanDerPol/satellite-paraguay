"""Satellite I/O module — Sentinel-2/Landsat/Planet download + preprocess."""
from .sources import (
    download_sentinel2_tile,
    download_via_gee,
    compute_ndvi,
    cloud_mask_s2,
    download_mapbiomas_paraguay,
    download_hansen_gfc,
)
from .real_download import (
    fetch_sentinel2_tile,
    download_sentinel2_gee,
    download_sentinel2_copernicus,
    generate_synthetic_sentinel2,
    atmospheric_correction,
)
from .mapbiomas import (
    download_mapbiomas_paraguay_real,
    compute_parcel_statistics_real,
)
from .hansen import (
    download_hansen_real,
    compute_deforestation_year,
)

__all__ = [
    # Original stubs (return paths)
    "download_sentinel2_tile",
    "download_via_gee",
    "compute_ndvi",
    "cloud_mask_s2",
    "download_mapbiomas_paraguay",
    "download_hansen_gfc",
    # Real Sentinel-2 (returns dict of arrays)
    "fetch_sentinel2_tile",
    "download_sentinel2_gee",
    "download_sentinel2_copernicus",
    "generate_synthetic_sentinel2",
    "atmospheric_correction",
    # Real MapBiomas
    "download_mapbiomas_paraguay_real",
    "compute_parcel_statistics_real",
    # Real Hansen
    "download_hansen_real",
    "compute_deforestation_year",
]
