"""Paraguay admin module."""

from .loader import (
    get_country_boundary,
    get_tile_bbox,
    list_tiles_in_region,
    load_catastro_parcels,
    load_catastro_urbanizaciones,
    load_departamentos,
    load_distritos,
    load_indigenous_territories,
    load_priority_tiles,
    load_tile_index,
)

__all__ = [
    "load_departamentos",
    "load_distritos",
    "load_catastro_parcels",
    "load_catastro_urbanizaciones",
    "load_indigenous_territories",
    "load_tile_index",
    "load_priority_tiles",
    "get_country_boundary",
    "get_tile_bbox",
    "list_tiles_in_region",
]
