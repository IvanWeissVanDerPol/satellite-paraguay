"""Repository verification utilities.

Verifies imports, paper pipelines, and data loaders.
"""

from typing import Any

REQUIRED_MODULES = [
    "src",
    "src.paraguay_admin",
    "src.satellite_io",
    "src.foundation_models",
    "src.parcel_analysis",
    "src.timeseries",
    "src.evaluation",
    "src.papers",
]

REQUIRED_PAPER_CLASSES = [
    ("src.papers.p0011_yvytu_deforestation", "YvytuPipeline"),
    ("src.papers.p0100_yvyra_carbon_credits", "YvyraPipeline"),
    ("src.papers.p0025_yrupe_yield", "YrupePipeline"),
    ("src.papers.p0012_yvy_indigenous", "YvyPipeline"),
    ("src.papers.p0026_kai_poaching", "KaiPipeline"),
    ("src.papers.p0035_tatakua_air_quality", "TatakuaPipeline"),
]

REQUIRED_DATA_LOADERS = [
    "load_departamentos",
    "load_distritos",
    "load_tile_index",
    "load_catastro_parcels",
    "load_indigenous_territories",
]


def verify_imports(modules: list[str] | None = None) -> dict[str, Any]:
    """Verify all required modules import cleanly.

    Returns dict with: ok (bool), imported (list), failed (list).
    """
    if modules is None:
        modules = REQUIRED_MODULES
    imported: list[str] = []
    failed: list[dict[str, str]] = []
    for mod in modules:
        try:
            __import__(mod)
            imported.append(mod)
        except ImportError as e:
            failed.append({"module": mod, "error": str(e)})
    return {"ok": len(failed) == 0, "imported": imported, "failed": failed}


def verify_pipelines(
    pipeline_specs: list[tuple[str, str]] | None = None,
) -> dict[str, Any]:
    """Verify all paper pipelines can be instantiated.

    pipeline_specs: list of (module_path, class_name) tuples.
    Returns dict with: ok, instantiated, failed.
    """
    if pipeline_specs is None:
        pipeline_specs = REQUIRED_PAPER_CLASSES
    import importlib

    instantiated: list[str] = []
    failed: list[dict[str, str]] = []
    for mod_path, cls_name in pipeline_specs:
        try:
            module = importlib.import_module(mod_path)
            cls = getattr(module, cls_name)
            cls()
            instantiated.append(cls_name)
        except Exception as e:
            failed.append({"pipeline": cls_name, "error": str(e)})
    return {
        "ok": len(failed) == 0,
        "instantiated": instantiated,
        "failed": failed,
    }


def verify_data_loaders(data_dir=None) -> dict[str, Any]:
    """Verify Paraguay data loaders work.

    Returns dict with: ok, loaders (name -> count or None), failed.
    """
    if data_dir is not None:
        import sys

        sys.path.insert(0, str(data_dir.parent))
    from src.paraguay_admin import (
        load_catastro_parcels,
        load_departamentos,
        load_distritos,
        load_indigenous_territories,
        load_tile_index,
    )

    results: dict[str, Any] = {}
    failed: list[dict[str, str]] = []
    loaders = [
        ("departamentos", load_departamentos),
        ("distritos", load_distritos),
        ("tiles", load_tile_index),
        ("catastro", load_catastro_parcels),
        ("indigenous", load_indigenous_territories),
    ]
    for name, loader in loaders:
        try:
            data = loader()
            results[name] = len(data)
        except Exception as e:
            results[name] = None
            failed.append({"loader": name, "error": str(e)})
    return {"ok": len(failed) == 0, "loaders": results, "failed": failed}


def all_checks_passed(*check_results: dict[str, Any]) -> bool:
    """Return True only if all check dicts have ok=True."""
    return all(r.get("ok", False) for r in check_results)


def overall_summary(*check_results: dict[str, Any]) -> dict[str, Any]:
    """Combine multiple check results into a single summary."""
    return {
        "ok": all_checks_passed(*check_results),
        "n_checks": len(check_results),
        "checks": check_results,
    }
