"""Init for paper p0030_yvyra_soy (Yvyra Soy: Indigenous Territory × Soybean Frontier).

Built 2026-09-09 (Phase A of audit remediation plan). Replaces P0012
Yvy as the thesis's indigenous land paper. Joins three public datasets:
  - INE 2022 indigenous communities census (557 communities, 19 pueblos)
  - OSM community polygons (30 features, admin_level 10/11)
  - MAG cereal yield 2007/08-2024/25 (soybean by department)

The headline finding (P0030-REG-001) is the per-region regression:
  Occidental Chaco (3 departments, 43.0 indi communities/dept) shows
  2.0x the mean MAG soy yield trajectory of Oriental (14 departments,
  30.6 indi communities/dept). Departments with higher indigenous
  community density show faster soy expansion.
"""

from .pipeline import (
    YvyraSoyPipeline,
    run_p0030_demo,
    run_p0030_regression,
)

__all__ = ["YvyraSoyPipeline", "run_p0030_demo", "run_p0030_regression"]
