"""Extended tests for src/foundation_models/models.py.

Coverage target: 90%+. Tests all loading paths, MockPrithvi forward,
compute_tile_embeddings caching, fuse_embeddings methods.
"""

import sys
from unittest.mock import MagicMock, patch

import numpy as np
import pytest


class TestLoadPrithvi:
    """Tests for load_prithvi function."""

    def test_returns_mock_when_transformers_unavailable(self):
        from src.foundation_models.models import MockPrithvi, load_prithvi

        # Block transformers
        saved = sys.modules.get("transformers")
        sys.modules["transformers"] = None
        try:
            result = load_prithvi()
            assert isinstance(result, MockPrithvi)
        finally:
            if saved is None:
                sys.modules.pop("transformers", None)
            else:
                sys.modules["transformers"] = saved

    def test_transformers_missing_raises_when_no_fallback(self):
        from src.foundation_models.models import load_prithvi

        saved = sys.modules.get("transformers")
        sys.modules["transformers"] = None
        try:
            with pytest.raises(ImportError):
                load_prithvi(allow_fallback=False)
        finally:
            if saved is None:
                sys.modules.pop("transformers", None)
            else:
                sys.modules["transformers"] = saved

    def test_loads_real_model_when_available(self):
        """When transformers works, returns real model."""
        from src.foundation_models.models import load_prithvi

        # Mock transformers
        mock_transformers = MagicMock()
        mock_model = MagicMock()
        mock_transformers.AutoModel.from_pretrained.return_value = mock_model

        with patch.dict(sys.modules, {"transformers": mock_transformers}):
            result = load_prithvi()
        assert result == mock_model
        mock_transformers.AutoModel.from_pretrained.assert_called_once()

    def test_real_model_load_fails_falls_back(self):
        """When model download fails, returns mock."""
        from src.foundation_models.models import MockPrithvi, load_prithvi

        mock_transformers = MagicMock()
        mock_transformers.AutoModel.from_pretrained.side_effect = Exception("download fail")

        with patch.dict(sys.modules, {"transformers": mock_transformers}):
            result = load_prithvi()
        assert isinstance(result, MockPrithvi)

    def test_real_model_load_fails_no_fallback(self):
        """When model download fails and no fallback, re-raises."""
        from src.foundation_models.models import load_prithvi

        mock_transformers = MagicMock()
        mock_transformers.AutoModel.from_pretrained.side_effect = Exception("download fail")

        with patch.dict(sys.modules, {"transformers": mock_transformers}):
            with pytest.raises(Exception):
                load_prithvi(allow_fallback=False)

    def test_different_model_sizes(self):
        """Different model sizes map to different model IDs."""
        from src.foundation_models.models import load_prithvi

        mock_transformers = MagicMock()
        mock_model = MagicMock()
        mock_transformers.AutoModel.from_pretrained.return_value = mock_model

        for size in ["100m", "300m", "600m"]:
            with patch.dict(sys.modules, {"transformers": mock_transformers}):
                load_prithvi(model_size=size)
            call = mock_transformers.AutoModel.from_pretrained.call_args
            assert size.upper() in call.args[0]


class TestMockPrithvi:
    """Tests for MockPrithvi class."""

    def test_init_creates_config(self):
        from src.foundation_models.models import MockPrithvi

        m = MockPrithvi()
        assert m.config.hidden_size == 768

    def test_parameters_returns_empty(self):
        from src.foundation_models.models import MockPrithvi

        m = MockPrithvi()
        params = list(m.parameters())
        assert params == []

    def test_to_returns_self(self):
        from src.foundation_models.models import MockPrithvi

        m = MockPrithvi()
        result = m.to("cuda")
        assert result is m

    def test_eval_returns_self(self):
        from src.foundation_models.models import MockPrithvi

        m = MockPrithvi()
        result = m.eval()
        assert result is m

    def test_forward_4d(self):
        """Forward pass on (B, C, H, W) returns (B, 768)."""
        from src.foundation_models.models import MockPrithvi

        m = MockPrithvi()
        x = np.zeros((4, 6, 64, 64), dtype=np.float32)
        out = m.forward(x)
        assert out.shape == (4, 768)

    def test_forward_5d(self):
        """Forward pass on (T, B, C, H, W) returns (T*B, 768)."""
        from src.foundation_models.models import MockPrithvi

        m = MockPrithvi()
        x = np.zeros((2, 4, 6, 64, 64), dtype=np.float32)
        out = m.forward(x)
        assert out.shape == (8, 768)

    def test_forward_invalid_shape(self):
        """Invalid shapes raise ValueError."""
        from src.foundation_models.models import MockPrithvi

        m = MockPrithvi()
        x = np.zeros((10, 10))  # 2D
        with pytest.raises(ValueError):
            m.forward(x)


class TestLoadAlphaearth:
    """Tests for load_alphaearth function."""

    def test_raises_not_implemented(self):
        from src.foundation_models.models import load_alphaearth

        with pytest.raises(NotImplementedError):
            load_alphaearth()


class TestLoadDinov2:
    """Tests for load_dinov2 function."""

    def test_returns_mock_when_transformers_unavailable(self):
        from src.foundation_models.models import MockPrithvi, load_dinov2

        saved = sys.modules.get("transformers")
        sys.modules["transformers"] = None
        try:
            result = load_dinov2()
            assert isinstance(result, MockPrithvi)
        finally:
            if saved is None:
                sys.modules.pop("transformers", None)
            else:
                sys.modules["transformers"] = saved

    def test_loads_real_model(self):
        from src.foundation_models.models import load_dinov2

        mock_transformers = MagicMock()
        mock_model = MagicMock()
        mock_transformers.AutoModel.from_pretrained.return_value = mock_model

        with patch.dict(sys.modules, {"transformers": mock_transformers}):
            result = load_dinov2()
        assert result == mock_model

    def test_load_fails_falls_back(self):
        from src.foundation_models.models import MockPrithvi, load_dinov2

        mock_transformers = MagicMock()
        mock_transformers.AutoModel.from_pretrained.side_effect = Exception("fail")

        with patch.dict(sys.modules, {"transformers": mock_transformers}):
            result = load_dinov2()
        assert isinstance(result, MockPrithvi)

    def test_different_sizes(self):
        from src.foundation_models.models import load_dinov2

        mock_transformers = MagicMock()
        mock_transformers.AutoModel.from_pretrained.return_value = MagicMock()

        for size in ["small", "base", "large", "giant"]:
            with patch.dict(sys.modules, {"transformers": mock_transformers}):
                load_dinov2(model_size=size)
            call_args = mock_transformers.AutoModel.from_pretrained.call_args.args[0]
            assert size in call_args


class TestComputeTileEmbeddings:
    """Tests for compute_tile_embeddings function."""

    def test_cache_miss_creates_file(self, tmp_path, monkeypatch):
        from src.foundation_models.models import compute_tile_embeddings

        cache_dir = tmp_path / "embeddings"
        with patch("src.foundation_models.models.DEFAULT_CACHE_DIR", cache_dir):
            # Patch np.random to be deterministic
            with patch("src.foundation_models.models.np.random.randn") as mock_rand:
                mock_rand.return_value = np.zeros(768)
                result = compute_tile_embeddings("tile_001", {"x": 0, "y": 0})
        assert result.shape == (768,)

    def test_cache_hit_returns_from_file(self, tmp_path):
        """When cache file exists, returns it without recomputation."""
        from src.foundation_models.models import compute_tile_embeddings

        cache_dir = tmp_path / "embeddings"
        cache_dir.mkdir(parents=True, exist_ok=True)
        # Pre-populate cache
        cached_emb = np.random.rand(768).astype(np.float32)
        cache_path = cache_dir / "tile_002_prithvi.npy"
        np.save(cache_path, cached_emb)

        # Pass cache_dir explicitly (default uses function-definition-time const)
        result = compute_tile_embeddings("tile_002", {"x": 0, "y": 0}, model_name="prithvi", cache_dir=cache_dir)
        np.testing.assert_array_equal(result, cached_emb)

    def test_custom_embedding_dim(self, tmp_path):
        from src.foundation_models.models import compute_tile_embeddings

        cache_dir = tmp_path / "embeddings"
        with patch("src.foundation_models.models.DEFAULT_CACHE_DIR", cache_dir):
            with patch("src.foundation_models.models.np.random.randn") as mock_rand:
                mock_rand.return_value = np.zeros(128)
                result = compute_tile_embeddings("tile_003", {"x": 0, "y": 0}, embedding_dim=128)
        assert result.shape == (128,)

    def test_unknown_model_uses_default_dim(self, tmp_path):
        from src.foundation_models.models import compute_tile_embeddings

        cache_dir = tmp_path / "embeddings"
        with patch("src.foundation_models.models.DEFAULT_CACHE_DIR", cache_dir):
            with patch("src.foundation_models.models.np.random.randn") as mock_rand:
                mock_rand.return_value = np.zeros(768)
                result = compute_tile_embeddings("tile_004", {"x": 0, "y": 0}, model_name="unknown_model")
        assert result.shape == (768,)

    def test_alphaearth_default_dim(self, tmp_path):
        from src.foundation_models.models import compute_tile_embeddings

        cache_dir = tmp_path / "embeddings"
        with patch("src.foundation_models.models.DEFAULT_CACHE_DIR", cache_dir):
            with patch("src.foundation_models.models.np.random.randn") as mock_rand:
                mock_rand.return_value = np.zeros(64)
                result = compute_tile_embeddings("tile_005", {"x": 0, "y": 0}, model_name="alphaearth")
        assert result.shape == (64,)

    def test_dinov2_default_dim(self, tmp_path):
        from src.foundation_models.models import compute_tile_embeddings

        cache_dir = tmp_path / "embeddings"
        with patch("src.foundation_models.models.DEFAULT_CACHE_DIR", cache_dir):
            with patch("src.foundation_models.models.np.random.randn") as mock_rand:
                mock_rand.return_value = np.zeros(1024)
                result = compute_tile_embeddings("tile_006", {"x": 0, "y": 0}, model_name="dinov2")
        assert result.shape == (1024,)


class TestFuseEmbeddings:
    """Tests for fuse_embeddings function."""

    def test_concat(self):
        from src.foundation_models.models import fuse_embeddings

        e1 = np.array([1, 2, 3])
        e2 = np.array([4, 5])
        result = fuse_embeddings({"a": e1, "b": e2}, method="concat")
        np.testing.assert_array_equal(result, [1, 2, 3, 4, 5])

    def test_mean(self):
        from src.foundation_models.models import fuse_embeddings

        e1 = np.array([1.0, 2.0, 3.0])
        e2 = np.array([3.0, 4.0, 5.0])
        result = fuse_embeddings({"a": e1, "b": e2}, method="mean")
        np.testing.assert_allclose(result, [2.0, 3.0, 4.0])

    def test_max(self):
        from src.foundation_models.models import fuse_embeddings

        e1 = np.array([1, 2, 3])
        e2 = np.array([3, 4, 5])
        result = fuse_embeddings({"a": e1, "b": e2}, method="max")
        np.testing.assert_array_equal(result, [3, 4, 5])

    def test_unknown_method(self):
        from src.foundation_models.models import fuse_embeddings

        with pytest.raises(ValueError):
            fuse_embeddings({"a": np.array([1, 2])}, method="unknown")

    def test_single_embedding(self):
        from src.foundation_models.models import fuse_embeddings

        emb = np.array([1.0, 2.0, 3.0])
        result = fuse_embeddings({"only": emb}, method="mean")
        np.testing.assert_array_equal(result, emb)
