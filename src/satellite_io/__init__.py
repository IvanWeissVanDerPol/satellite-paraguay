"""Satellite I/O module — Sentinel-2/Landsat/Planet download + preprocess."""

from .hansen import (
    compute_deforestation_year,
    download_hansen_real,
)
from .mapbiomas import (
    compute_parcel_statistics_real,
    download_mapbiomas_paraguay_real,
)
from .real_download import (
    atmospheric_correction,
    download_sentinel2_copernicus,
    download_sentinel2_gee,
    fetch_sentinel2_tile,
    generate_synthetic_sentinel2,
)
from .sources import (
    cloud_mask_s2,
    compute_ndvi,
    download_hansen_gfc,
    download_mapbiomas_paraguay,
    download_sentinel2_tile,
    download_via_gee,
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
