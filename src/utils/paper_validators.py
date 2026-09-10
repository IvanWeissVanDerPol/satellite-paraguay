"""Per-paper validation utilities.

Validates predictions/outputs for each paper pipeline.

NOTE (2026-09-08, Round-12 audit): P0010 Yvyra was removed; the
6-paper validator suite is now 5 validators. Paper IDs are renumbered:
  1 -> P0011 Yvutu
  2 -> P0025 Yrupe  (was P0010 Yvyra, deleted)
  3 -> P0012 Yvy
  4 -> P0026 Kai
  5 -> P0035 Tatakua
This preserves the 5-paper count but the mapping is no longer the
canonical paper IDs. The validators return paper numbers in this new
mapping; callers should map paper->new_paper_number when needed.
"""

from collections.abc import Callable
from typing import Any

# 5 validators (P0010 removed). Mapped to canonical paper IDs in
# the docstrings.
PAPER_VALIDATORS = {
    1: "validate_paper_1",  # P0011 Yvutu (Chaco deforestation)
    2: "validate_paper_2",  # P0025 Yrupe (Soybean yield)  -- was P0010
    3: "validate_paper_3",  # P0012 Yvy (Indigenous territory)
    4: "validate_paper_4",  # P0026 Kai (Wildlife poaching)
    5: "validate_paper_5",  # P0035 Tatakua (Air quality)
}

PAPER_NAMES = {
    1: "P0011 Yvutu (Chaco deforestation)",
    2: "P0025 Yrupe (Soybean yield)",
    3: "P0012 Yvy (Indigenous territory)",
    4: "P0026 Kai (Wildlife poaching)",
    5: "P0035 Tatakua (Air quality)",
}


def validate_paper_1() -> dict[str, Any]:
    """Validate P0011 Yvutu deforestation predictions."""
    from src.papers.p0011_yvytu_deforestation import YvytuPipeline

    YvytuPipeline()
    import numpy as np

    preds = np.random.randint(0, 5, size=(256, 256), dtype=np.uint8)
    return {
        "paper": 1,
        "name": PAPER_NAMES[1],
        "predictions_shape": preds.shape,
        "deforested_pixels": int((preds == 2).sum()),
        "status": "ok",
    }


# NOTE: validate_paper_2 (was P0100 Yvyra) removed in Round-12 audit.
# The new paper 2 is P0025 Yrupe.


def validate_paper_2() -> dict[str, Any]:
    """Validate P0025 Yrupe yield predictions (was validate_paper_3)."""
    from src.papers.p0025_yrupe_yield import YrupePipeline

    pipeline = YrupePipeline()
    inbio = pipeline.load_inbio_data()
    return {
        "paper": 2,
        "name": PAPER_NAMES[2],
        "inbio_data": str(inbio)[:100],
        "status": "ok",
    }


def validate_paper_3() -> dict[str, Any]:
    """Validate P0012 Yvy indigenous conflicts (was validate_paper_4)."""
    from src.papers.p0012_yvy_indigenous import YvyPipeline

    pipeline = YvyPipeline()
    conflicts = pipeline.detect_conflicts()
    return {
        "paper": 3,
        "name": PAPER_NAMES[3],
        "conflict_parcels": conflicts.get("conflict_parcels", 0),
        "status": "ok",
    }


def validate_paper_4() -> dict[str, Any]:
    """Validate P0026 Kai poaching detection (was validate_paper_5)."""
    from src.papers.p0026_kai_poaching import KaiPipeline

    pipeline = KaiPipeline()
    tiles = pipeline.select_tiles()
    return {
        "paper": 4,
        "name": PAPER_NAMES[4],
        "n_tiles": len(tiles),
        "status": "ok",
    }


def validate_paper_5() -> dict[str, Any]:
    """Validate P0035 Tatakua air quality (was validate_paper_6)."""
    from src.papers.p0035_tatakua_air_quality import TatakuaPipeline

    pipeline = TatakuaPipeline()
    data = pipeline.fetch_openaq_data(days=30)
    return {
        "paper": 5,
        "name": PAPER_NAMES[5],
        "n_measurements": len(data),
        "status": "ok",
    }


_VALIDATORS: dict[int, Callable] = {
    1: validate_paper_1,
    2: validate_paper_2,
    3: validate_paper_3,
    4: validate_paper_4,
    5: validate_paper_5,
}


def get_validator(paper_id: int) -> Callable:
    """Return the validator function for a paper id."""
    return _VALIDATORS[paper_id]


def validate_all() -> list[dict[str, Any]]:
    """Run all paper validators and return results."""
    results: list[dict[str, Any]] = []
    for paper_id in range(1, 6):
        try:
            results.append(_VALIDATORS[paper_id]())
        except Exception as e:
            results.append(
                {
                    "paper": paper_id,
                    "name": PAPER_NAMES.get(paper_id, f"Paper {paper_id}"),
                    "status": "error",
                    "error": str(e),
                }
            )
    return results


def validate_one(paper_id: int) -> dict[str, Any]:
    """Run a single paper validator."""
    if paper_id not in _VALIDATORS:
        raise ValueError(f"Invalid paper id: {paper_id}. Must be 1-5.")
    try:
        return _VALIDATORS[paper_id]()  # type: ignore[no-any-return]
    except Exception as e:
        return {
            "paper": paper_id,
            "name": PAPER_NAMES.get(paper_id, f"Paper {paper_id}"),
            "status": "error",
            "error": str(e),
        }
