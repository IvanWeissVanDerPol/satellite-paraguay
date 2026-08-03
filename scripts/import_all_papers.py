# Run all 6 papers in parallel
# This is the main runner for the thesis project.

import sys
sys.path.insert(0, '.')

from src.papers.p0011_yvutu_deforestation import YvutuPipeline
from src.papers.p0012_yvy_indigenous import YvyPipeline
from src.papers.p0025_yrupe_yield import YrupePipeline
from src.papers.p0026_kai_poaching import KaiPipeline
from src.papers.p0035_tatakua_air_quality import TatakuaPipeline
from src.papers.p0100_yvyra_carbon_credits import YvyraPipeline

print("All 6 paper pipelines import OK")
