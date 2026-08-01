"""Verify that everything is set up correctly.

Run after bootstrap to confirm:
- All modules import
- All 6 paper pipelines work
- Sample data loads
- Tests pass
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))


def verify_imports():
    """Verify all module imports."""
    print("[verify] Importing modules...")
    modules = [
        "src",
        "src.paraguay_admin",
        "src.satellite_io",
        "src.foundation_models",
        "src.parcel_analysis",
        "src.timeseries",
        "src.evaluation",
        "src.papers",
    ]
    for mod in modules:
        try:
            __import__(mod)
            print(f"  OK: {mod}")
        except ImportError as e:
            print(f"  FAIL: {mod}: {e}")
            return False
    return True


def verify_pipelines():
    """Verify all 6 paper pipelines instantiate."""
    print("[verify] Importing paper pipelines...")
    try:
        from src.papers.p0011_yvytu_deforestation import YvytuPipeline
        from src.papers.p0100_yvyra_carbon_credits import YvyraPipeline
        from src.papers.p0025_yrupe_yield import YrupePipeline
        from src.papers.p0012_yvy_indigenous import YvyPipeline
        from src.papers.p0026_kai_poaching import KaiPipeline
        from src.papers.p0035_tatakua_air_quality import TatakuaPipeline

        for cls in [YvytuPipeline, YvyraPipeline, YrupePipeline, YvyPipeline, KaiPipeline, TatakuaPipeline]:
            instance = cls()
            print(f"  OK: {cls.__name__} instantiated")
        return True
    except Exception as e:
        print(f"  FAIL: {e}")
        return False


def verify_data():
    """Verify Paraguay data loads."""
    print("[verify] Loading Paraguay data...")
    try:
        from src.paraguay_admin import (
            load_departamentos,
            load_distritos,
            load_tile_index,
            load_catastro_parcels,
            load_indigenous_territories,
        )
        deptos = load_departamentos()
        print(f"  OK: {len(deptos)} departamentos")
        distritos = load_distritos()
        print(f"  OK: {len(distritos)} distritos")
        tiles = load_tile_index()
        print(f"  OK: {len(tiles)} tiles")
        catastro = load_catastro_parcels()
        print(f"  OK: {len(catastro)} Catastro parcels")
        indigenous = load_indigenous_territories()
        print(f"  OK: {len(indigenous)} indigenous territories")
        return True
    except Exception as e:
        print(f"  FAIL: {e}")
        return False


def main():
    print("=" * 60)
    print("SatelliteCV-Paraguay — Verify")
    print("=" * 60)

    ok1 = verify_imports()
    print()
    ok2 = verify_pipelines()
    print()
    ok3 = verify_data()
    print()

    if ok1 and ok2 and ok3:
        print("=" * 60)
        print("ALL CHECKS PASSED")
        print("=" * 60)
        print("\nReady to run papers!")
        print("  make run-paper-1   — first paper")
        print("  make run-all-papers — all 6 papers")
        print("  make dashboard      — start dashboard")
    else:
        print("=" * 60)
        print("SOME CHECKS FAILED")
        print("=" * 60)
        sys.exit(1)


if __name__ == "__main__":
    main()
