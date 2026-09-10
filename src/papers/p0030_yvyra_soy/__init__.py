"""Init for paper p0030_yvyra_soy (Yvyra Soy: Indigenous Territory × Soybean Frontier).

Built 2026-09-09 (Phase A of audit remediation plan). Replaces P0012
Yvy as the thesis's indigenous land paper, using real data:

  - INE 2022 indigenous communities census (557 communities, 19 pueblos)
  - OSM indigenous community polygons (30 features; admin_level 10/11)
  - MAG cereal yield 2007/08-2024/25 (soybean, maize, sorghum, etc.)
  - Hansen GFC v1.11 256x256 tile (off-repo, ~56 km^2)

The paper frames the joint analysis as: do indigenous territory
buffers in Paraguay's Gran Chaco show different rates of soybean
expansion vs. the surrounding national average, after controlling
for departmental yield baseline? This is methodologically distinct
from P0012 Yvy (deforestation) — P0030 measures soy expansion, not
forest loss.

All numbers in this paper are derived from public datasets
(datos.gov.py for INE/MAG, Overpass API for OSM, NASA Hansen for
forest cover). The thesis author has not contacted any indigenous
community; this is a public-data analysis only.
"""

from .pipeline import YvyraSoyPipeline, run_p0030_demo

__all__ = ["YvyraSoyPipeline", "run_p0030_demo"]
