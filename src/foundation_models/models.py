"""Foundation models for satellite imagery.

Models:
- Prithvi (IBM-NASA, Apache 2.0) — HLS satellite foundation model
- AlphaEarth (Google, free research) — Earth embeddings
- DINOv2 (Meta, Apache 2.0) — Visual foundation model

All open-source. Each can be used for transfer learning on Paraguay satellite tiles.
"""

from pathlib import Path
from typing import Dict, Optional

import numpy as np

DEFAULT_CACHE_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "cache" / "embeddings"


def load_prithvi(model_size: str = "300m", allow_fallback: bool = True):
    """Load IBM-NASA Prithvi foundation model.

    Source: https://huggingface.co/ibm-nasa-geospatial/Prithvi-300M
    License: Apache 2.0

    Falls back to mock model if transformers/numpy incompatible.
    """
    try:
        from transformers import AutoModel
    except (ImportError, ValueError) as e:
        if not allow_fallback:
            raise ImportError(f"transformers unavailable: {e}")
        print(f"[prithvi] transformers unavailable ({e}), using mock model")
        return MockPrithvi()

    model_id = f"ibm-nasa-geospatial/Prithvi-{model_size.upper()}"
    print(f"[prithvi] Loading {model_id} (Apache 2.0)")
    try:
        model = AutoModel.from_pretrained(model_id)
        return model
    except Exception as e:
        if not allow_fallback:
            raise
        print(f"[prithvi] Could not load {model_id} ({e}), using mock model")
        return MockPrithvi()


class MockPrithvi:
    """Mock Prithvi model for testing without HF dependencies."""

    def __init__(self):
        self.config = type("Config", (), {"hidden_size": 768})()

    def parameters(self):
        return iter([])

    def to(self, device):
        return self

    def eval(self):
        return self

    def forward(self, x):
        # x shape: (B, C, H, W) or (T, C, H, W)
        # Return mock embeddings
        if x.ndim == 5:
            T, B, C, H, W = x.shape
            # Flatten T and B
            return np.zeros((T * B, 768), dtype=np.float32)
        elif x.ndim == 4:
            B, C, H, W = x.shape
            return np.zeros((B, 768), dtype=np.float32)
        else:
            raise ValueError(f"Unexpected input shape: {x.shape}")


def load_alphaearth():
    """Load Google AlphaEarth foundation model.

    Source: https://github.com/google-deepmind/alphaearth
    License: Free for research
    """
    print("[alphaearth] Loading (free for research)")
    # Real implementation uses google-deepmind/alphaearth
    raise NotImplementedError("AlphaEarth requires research access. Apply at https://deepmind.google/forms/")


def load_dinov2(model_size: str = "large", allow_fallback: bool = True):
    """Load Meta DINOv2 visual foundation model.

    Source: https://huggingface.co/facebook/dinov2-large
    License: Apache 2.0
    """
    try:
        from transformers import AutoModel
    except (ImportError, ValueError) as e:
        if not allow_fallback:
            raise ImportError(f"transformers unavailable: {e}")
        print(f"[dinov2] transformers unavailable ({e}), using mock model")
        return MockPrithvi()

    model_id = f"facebook/dinov2-{model_size}"
    print(f"[dinov2] Loading {model_id} (Apache 2.0)")
    try:
        model = AutoModel.from_pretrained(model_id)
        return model
    except Exception as e:
        if not allow_fallback:
            raise
        print(f"[dinov2] Could not load {model_id} ({e}), using mock model")
        return MockPrithvi()


def compute_tile_embeddings(
    tile_id: str,
    bbox: Dict[str, float],
    model_name: str = "prithvi",
    cache_dir: Path = DEFAULT_CACHE_DIR,
    embedding_dim: Optional[int] = None,
) -> np.ndarray:
    """Compute foundation model embeddings for a tile.

    Args:
        tile_id: tile identifier
        bbox: tile bounding box
        model_name: 'prithvi', 'alphaearth', 'dinov2'
        cache_dir: where to cache
        embedding_dim: expected output dim (varies by model)

    Returns:
        Numpy array of embeddings (typically 768 or 1024-dim)
    """
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_path = cache_dir / f"{tile_id}_{model_name}.npy"

    if cache_path.exists():
        return np.load(cache_path)  # type: ignore[no-any-return]

    # Real implementation: load model, run inference on tile
    print(f"[{model_name}] Computing embeddings for {tile_id}")

    # Placeholder: random embedding
    if embedding_dim is None:
        embedding_dim = {"prithvi": 768, "alphaearth": 64, "dinov2": 1024}.get(model_name, 768)

    embedding = np.random.randn(embedding_dim).astype(np.float32)

    np.save(cache_path, embedding)
    return embedding


def fuse_embeddings(
    embeddings: Dict[str, np.ndarray],
    method: str = "concat",
) -> np.ndarray:
    """Fuse multiple foundation model embeddings.

    Args:
        embeddings: {model_name: embedding}
        method: 'concat' (concatenate), 'mean' (average), 'max' (element-wise max)

    Returns:
        Fused embedding
    """
    if method == "concat":
        return np.concatenate(list(embeddings.values()))
    elif method == "mean":
        return np.mean(list(embeddings.values()), axis=0)  # type: ignore[no-any-return]
    elif method == "max":
        return np.max(list(embeddings.values()), axis=0)  # type: ignore[no-any-return]
    else:
        raise ValueError(f"Unknown fusion method: {method}")


if __name__ == "__main__":
    print("Foundation models module")
    print(f"Cache: {DEFAULT_CACHE_DIR}")
