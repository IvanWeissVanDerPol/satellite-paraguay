"""Papers module — 6 thesis sub-projects in parallel."""

from .p0011_yvytu_deforestation import YvytuPipeline
from .p0012_yvy_indigenous import YvyPipeline
from .p0025_yrupe_yield import YrupePipeline
from .p0026_kai_poaching import KaiPipeline
from .p0035_tatakua_air_quality import TatakuaPipeline
from .p0100_yvyra_carbon_credits import YvyraPipeline

__all__ = [
    "YvytuPipeline",
    "YvyraPipeline",
    "YrupePipeline",
    "YvyPipeline",
    "KaiPipeline",
    "TatakuaPipeline",
]
