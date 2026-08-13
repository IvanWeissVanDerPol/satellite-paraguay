"""Performance profiling for all 6 paper pipelines.

Usage:
    python scripts/profile_performance.py
"""

import json
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent))


def profile_pipeline(name: str, func, *args, **kwargs):
    """Profile a pipeline function."""
    print(f"\nProfiling {name}...")
    start = time.time()
    try:
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        print(f"  Time: {elapsed:.2f}s")
        return {
            "name": name,
            "time_seconds": elapsed,
            "status": "success",
            "result_size": str(result)[:200] if result else "None",
        }
    except Exception as e:
        elapsed = time.time() - start
        print(f"  Time: {elapsed:.2f}s")
        print(f"  Error: {e}")
        return {
            "name": name,
            "time_seconds": elapsed,
            "status": "error",
            "error": str(e),
        }


def profile_memory(func, *args, **kwargs):
    """Profile peak memory usage."""
    try:
        import os

        import psutil

        process = psutil.Process(os.getpid())
        start_mem = process.memory_info().rss / (1024**2)  # MB

        func(*args, **kwargs)

        end_mem = process.memory_info().rss / (1024**2)
        peak_mem = (
            process.memory_info().peak_wset / (1024**2) if hasattr(process.memory_info(), "peak_wset") else end_mem
        )

        return {
            "start_mb": start_mem,
            "end_mb": end_mem,
            "peak_mb": peak_mem,
        }
    except ImportError:
        return {"error": "psutil not installed"}


def main():
    print("=" * 60)
    print("SatelliteCV-Paraguay Performance Profiling")
    print("=" * 60)

    results = []

    # Profile 1: Sentinel-2 fetch
    from src.satellite_io import fetch_sentinel2_tile

    results.append(
        profile_pipeline(
            "P0011: Sentinel-2 fetch (1 tile, synthetic)",
            fetch_sentinel2_tile,
            tile_id="-54.267_-21.164",
            bbox={"min_lon": -54.317, "max_lon": -54.217, "min_lat": -21.214, "max_lat": -21.114},
            start_date="2024-01-01",
            end_date="2025-01-01",
        )
    )

    # Profile 2: MapBiomas fetch
    from src.satellite_io import download_mapbiomas_paraguay_real

    results.append(
        profile_pipeline(
            "P0011: MapBiomas fetch",
            download_mapbiomas_paraguay_real,
            {"min_lon": -60, "max_lon": -59, "min_lat": -22, "max_lat": -21},
            year=2022,
        )
    )

    # Profile 3: Hansen fetch
    from src.satellite_io import download_hansen_real

    results.append(
        profile_pipeline(
            "P0011: Hansen fetch",
            download_hansen_real,
            {"min_lon": -60, "max_lon": -59, "min_lat": -22, "max_lat": -21},
        )
    )

    # Profile 4: Verra fetch
    from src.external import fetch_verra_paraguay

    results.append(
        profile_pipeline(
            "P0100: Verra Paraguay projects",
            fetch_verra_paraguay,
        )
    )

    # Profile 5: OpenAQ fetch
    from src.external import fetch_openaq_asuncion

    results.append(
        profile_pipeline(
            "P0035: OpenAQ Asunción (1 year)",
            fetch_openaq_asuncion,
            days=365,
            parameter="pm25",
        )
    )

    # Profile 6: Sentinel-5P fetch
    from src.external import fetch_sentinel5p_no2

    results.append(
        profile_pipeline(
            "P0035: Sentinel-5P NO2 (1 year)",
            fetch_sentinel5p_no2,
            {"min_lon": -57.7, "max_lon": -57.4, "min_lat": -25.4, "max_lat": -25.2},
            "2024-01-01",
            "2025-01-01",
        )
    )

    # Profile 7: FIRMS fetch
    from src.external import fetch_firms_fires

    results.append(
        profile_pipeline(
            "P0026: FIRMS fires (7 days)",
            fetch_firms_fires,
            {"min_lon": -61, "max_lon": -58, "min_lat": -22.5, "max_lat": -20},
            days=7,
        )
    )

    # Profile 8: Catastro + indigenous
    from src.paraguay_admin.real_analysis import detect_conflicts_real

    results.append(
        profile_pipeline(
            "P0012: Catastro-Indigenous conflicts",
            detect_conflicts_real,
            buffer_m=100,
        )
    )

    # Profile 9: Baselines (P0011)
    from src.baselines import p0011_yvytu_baselines

    ndvi = np.random.rand(12, 64, 64).astype(np.float32) * 0.5 + 0.3
    gt = np.random.randint(0, 5, (64, 64), dtype=np.int64)
    results.append(
        profile_pipeline(
            "P0011: All baselines (RF + U-Net + persistence)",
            p0011_yvytu_baselines.run_all_baselines,
            ndvi,
            gt,
        )
    )

    # Profile 10: Yvutu pipeline (full)
    from src.papers.p0011_yvytu_deforestation import YvytuPipeline

    pipeline = YvytuPipeline()
    pipeline.load_model = lambda: None  # Skip model load
    results.append(
        profile_pipeline(
            "P0011: Yvutu pipeline (no real data)",
            pipeline.detect_deforestation,
            "-54.267_-21.164",
            ndvi,
            [f"2024-{m:02d}-01" for m in range(1, 13)],
        )
    )

    # Summary
    print("\n" + "=" * 60)
    print("PERFORMANCE SUMMARY")
    print("=" * 60)
    print(f"{'Pipeline':<50} {'Time (s)':<12} {'Status'}")
    print("-" * 80)
    total_time = 0
    for r in results:
        name = r["name"][:50]
        time_str = f"{r['time_seconds']:.2f}"
        status = r["status"]
        print(f"{name:<50} {time_str:<12} {status}")
        total_time += r["time_seconds"]
    print("-" * 80)
    print(f"{'TOTAL':<50} {total_time:.2f}")

    # Save report
    report_path = Path("outputs/performance_report.json")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(results, indent=2))
    print(f"\nDetailed report saved to {report_path}")


if __name__ == "__main__":
    main()
