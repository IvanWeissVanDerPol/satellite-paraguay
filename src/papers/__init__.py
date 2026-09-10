"""Papers module — 5 thesis sub-projects in parallel.

Note (2026-09-08, Round-12 audit): P0010 Yvyra was removed; the
P0010 paper was np.random.normal-driven fabrication. See commit
message for commit 7c... (Phase 8).
"""

from .p0011_yvytu_deforestation import YvytuPipeline
from .p0012_yvy_indigenous import YvyPipeline
from .p0025_yrupe_yield import YrupePipeline
from .p0026_kai_poaching import KaiPipeline
from .p0030_yvyra_soy import YvyraSoyPipeline
from .p0035_tatakua_air_quality import TatakuaPipeline

__all__ = [
    "YvytuPipeline",
    "YrupePipeline",
    "YvyPipeline",
    "KaiPipeline",
    "YvyraSoyPipeline",
    "TatakuaPipeline",
]
