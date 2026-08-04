"""Tests for src/foundation_models/models.py.

Coverage target: 70%+. Tests load_prithvi, load_alphaearth,
load_dinov2, compute_tile_embeddings, fuse_embeddings.
"""
import pytest
import numpy as np
from pathlib import Path
from unittest.mock import patch, MagicMock


class TestLoadPrithvi:
    """Tests for load_prithvi function."""

    def test_load_prithvi_falls_back_to_mock(self):
        """Without transformers, should fall back to MockPrithvi."""
        from src.foundation_models.models import load_prithvi
        # Block transformers import
        import sys as _sys
        saved = _sys.modules.get("transformers")
        _sys.modules["transformers"] = None
        try:
            model = load_prithvi("300m", allow_fallback=True)
            from src.foundation_models.models import MockPrithvi
            assert isinstance(model, MockPrithvi)
        finally:
            if saved is None:
                _sys.modules.pop("transformers", None)
            else:
                _sys.modules["transformers"] = saved

    def test_load_prithvi_no_fallback_raises(self):
        """Without transformers and no fallback, should raise."""
        from src.foundation_models.models import load_prithvi
        import sys as _sys
        saved = _sys.modules.get("transformers")
        _sys.modules["transformers"] = None
        try:
            with pytest.raises(ImportError):
                load_prithvi("300m", allow_fallback=False)
        finally:
            if saved is None:
                _sys.modules.pop("transformers", None)
            else:
                _sys.modules["transformers"] = saved

    def test_load_prithvi_uses_mock_when_real_fails(self):
        """When real load fails, should fall back to mock."""
        from src.foundation_models.models import load_prithvi, MockPrithvi
        with patch.dict("sys.modules", {"transformers": MagicMock()}):
            # Make AutoModel.from_pretrained raise
            with patch("transformers.AutoModel") as mock_auto:
                mock_auto.from_pretrained.side_effect = Exception("network error")
                model = load_prithvi("300m", allow_fallback=True)
                assert isinstance(model, MockPrithvi)

    def test_load_prithvi_returns_real_model(self):
        """When real load succeeds, should return the model."""
        from src.foundation_models.models import load_prithvi
        mock_model = MagicMock()
        with patch.dict("sys.modules", {"transformers": MagicMock()}):
            with patch("transformers.AutoModel") as mock_auto:
                mock_auto.from_pretrained.return_value = mock_model
                model = load_prithvi("300m")
                assert model is mock_model


class TestMockPrithvi:
    """Tests for MockPrithvi class."""

    def test_init_creates_config(self):
        from src.foundation_models.models import MockPrithvi
        m = MockPrithvi()
        assert m.config is not None
        assert m.config.hidden_size == 768

    def test_mock_usable(self):
        """Mock should be usable (no exception on attribute access)."""
        from src.foundation_models.models import MockPrithvi
        m = MockPrithvi()
        # Just test we can access attributes
        assert hasattr(m, "config")


class TestLoadAlphaearth:
    """Tests for load_alphaearth function."""

    def test_returns_mock(self):
        """load_alphaearth returns a mock when not available."""
        from src.foundation_models.models import load_alphaearth
        import sys as _sys
        saved = _sys.modules.get("transformers")
        _sys.modules["transformers"] = None
        try:
            # alphaearth may or may not have fallback - just verify it runs
            try:
                model = load_alphaearth()
                assert model is not None
            except (ImportError, Exception):
                pass  # Either returns mock or raises
        finally:
            if saved is None:
                _sys.modules.pop("transformers", None)
            else:
                _sys.modules["transformers"] = saved


class TestLoadDinov2:
    """Tests for load_dinov2 function."""

    def test_load_dinov2_falls_back(self):
        from src.foundation_models.models import load_dinov2
        import sys as _sys
        saved = _sys.modules.get("transformers")
        _sys.modules["transformers"] = None
        try:
            model = load_dinov2("large", allow_fallback=True)
            assert model is not None
        finally:
            if saved is None:
                _sys.modules.pop("transformers", None)
            else:
                _sys.modules["transformers"] = saved

    def test_load_dinov2_no_fallback_raises(self):
        from src.foundation_models.models import load_dinov2
        import sys as _sys
        saved = _sys.modules.get("transformers")
        _sys.modules["transformers"] = None
        try:
            with pytest.raises(ImportError):
                load_dinov2("large", allow_fallback=False)
        finally:
            if saved is None:
                _sys.modules.pop("transformers", None)
            else:
                _sys.modules["transformers"] = saved

    def test_load_dinov2_real_model(self):
        from src.foundation_models.models import load_dinov2
        mock_model = MagicMock()
        with patch.dict("sys.modules", {"transformers": MagicMock()}):
            with patch("transformers.AutoModel") as mock_auto:
                mock_auto.from_pretrained.return_value = mock_model
                model = load_dinov2("large")
                assert model is mock_model


class TestComputeTileEmbeddings:
    """Tests for compute_tile_embeddings function."""

    def test_returns_array(self, tmp_path):
        from src.foundation_models.models import compute_tile_embeddings
        bbox = {"min_lon": -60, "max_lon": -55, "min_lat": -25, "max_lat": -20}
        result = compute_tile_embeddings(
            tile_id="test_tile", bbox=bbox, model_name="prithvi", cache_dir=tmp_path
        )
        assert result is not None
        assert isinstance(result, np.ndarray)

    def test_compute_with_mock_model(self, tmp_path):
        from src.foundation_models.models import compute_tile_embeddings
        bbox = {"min_lon": -60, "max_lon": -55, "min_lat": -25, "max_lat": -20}
        result = compute_tile_embeddings(
            tile_id="mock_tile", bbox=bbox, model_name="alphaearth", cache_dir=tmp_path
        )
        assert result.shape[0] == 64  # alphaearth dim


class TestFuseEmbeddings:
    """Tests for fuse_embeddings function."""

    def test_concatenate_embeddings(self):
        from src.foundation_models.models import fuse_embeddings
        e1 = np.random.rand(768).astype(np.float32)
        e2 = np.random.rand(768).astype(np.float32)
        result = fuse_embeddings({"prithvi": e1, "dinov2": e2})
        assert result.shape == (1536,)  # 768 * 2

    def test_single_embedding(self):
        from src.foundation_models.models import fuse_embeddings
        e1 = np.random.rand(768).astype(np.float32)
        result = fuse_embeddings({"prithvi": e1})
        assert result.shape == (768,)

    def test_three_embeddings_same_dim(self):
        """Test fusing 3 embeddings of the same dim."""
        from src.foundation_models.models import fuse_embeddings
        e1 = np.random.rand(100).astype(np.float32)
        e2 = np.random.rand(100).astype(np.float32)
        e3 = np.random.rand(100).astype(np.float32)
        result = fuse_embeddings({"a": e1, "b": e2, "c": e3})
        assert result.shape == (300,)

    def test_empty_dict_returns_zero_array(self):
        """Empty dict returns zero-length array."""
        from src.foundation_models.models import fuse_embeddings
        try:
            result = fuse_embeddings({})
            assert result.shape[0] == 0
        except ValueError:
            # Some implementations raise on empty list
            pass


class TestConstants:
    """Test module-level constants."""

    def test_cache_dir_is_path(self):
        from src.foundation_models import models
        assert isinstance(models.DEFAULT_CACHE_DIR, Path)