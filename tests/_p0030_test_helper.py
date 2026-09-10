"""Test helper: run P0030 Yvyra Soy demo in an isolated environment.

CI Python 3.10 does not have geopandas/rasterio installed. We
stub them with full attribute trees so that lazy attribute
references (gpd.GeoDataFrame, rasterio.open, etc.) don't blow up
when src.paraguay_admin loads.
"""

import json
import sys
import types
from pathlib import Path


class _GeoDataFrameStub:
    """Empty stub for geopandas.GeoDataFrame."""

    pass


class _RasterioDatasetStub:
    """Empty stub for rasterio.io.DatasetReader."""

    pass


def _stub_module(name: str, **attrs):
    """Inject a fake module with the given attributes."""
    if name in sys.modules:
        return
    m = types.ModuleType(name)
    m.__version__ = "0.0.0-stub"
    for k, v in attrs.items():
        setattr(m, k, v)
    sys.modules[name] = m


# Build stub trees for geopandas, rasterio, shapely before any
# imports that might chain into them.
_stub_module("geopandas", GeoDataFrame=_GeoDataFrameStub)
_stub_module("rasterio", open=None)

# Add rasterio.io submodule for `from rasterio.io import ...`
rasterio_module = sys.modules["rasterio"]
rasterio_io = types.ModuleType("rasterio.io")
rasterio_io.DatasetReader = _RasterioDatasetStub
rasterio_io.__version__ = "0.0.0-stub"
sys.modules["rasterio.io"] = rasterio_io
rasterio_module.io = rasterio_io

_stub_module("shapely")
shapely_module = sys.modules["shapely"]
shapely_geometry = types.ModuleType("shapely.geometry")
shapely_geometry.__version__ = "0.0.0-stub"
sys.modules["shapely.geometry"] = shapely_geometry
shapely_module.geometry = shapely_geometry

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

# Import the P0030 pipeline (this triggers src.papers.__init__.py
# which loads p0011 -> paraguay_admin -> uses our stubs)
import src.papers.p0030_yvyra_soy.pipeline as p0030_pipeline

result = p0030_pipeline.run_p0030_demo()
print(json.dumps(result, default=str))
