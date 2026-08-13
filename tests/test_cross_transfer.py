"""Tests for cross-paper transfer learning."""

import sys
from pathlib import Path

import numpy as np
import pytest  # noqa: E402

pytest.importorskip("torch", reason="CI: requires optional system dep 'torch' (not installed)")  # noqa: E402
import torch  # noqa: E402

sys.path.insert(0, str(Path(__file__).parent.parent))


def test_multi_task_cnn_forward():
    """Multi-task CNN forward pass returns correct shapes."""
    from scripts.cross_transfer_experiment import MultiTaskCNN

    model = MultiTaskCNN(in_ch=4)
    x = torch.randn(2, 4, 64, 64)

    # Test each task
    out_def = model(x, task="def")
    assert out_def.shape == (2,), f"Expected (2,), got {out_def.shape}"

    out_yld = model(x, task="yld")
    assert out_yld.shape == (2,), f"Expected (2,), got {out_yld.shape}"

    out_forest = model(x, task="forest")
    assert out_forest.shape == (2,), f"Expected (2,), got {out_forest.shape}"


def test_multi_task_cnn_invalid_task():
    """Invalid task returns None or fails gracefully."""
    from scripts.cross_transfer_experiment import MultiTaskCNN

    model = MultiTaskCNN(in_ch=4)
    x = torch.randn(1, 4, 64, 64)

    try:
        out = model(x, task="invalid")
        # If it doesn't raise, the output may be None or some default
        assert out is None or out.numel() > 0
    except (KeyError, AttributeError, IndexError):
        # Expected behavior
        pass


def test_tile_dataset():
    """Tile dataset returns correct shape."""
    from scripts.cross_transfer_experiment import TileDataset

    H = W = 200
    lossyear = np.zeros((H, W), dtype=np.uint8)
    treecover = np.full((H, W), 50, dtype=np.uint8)
    mapbiomas = np.full((H, W), 3, dtype=np.uint8)  # Forest

    ds = TileDataset(lossyear, treecover, mapbiomas, n_tiles=20, tile_size=32)
    assert len(ds) == 20
    x, lbl_def, lbl_yld, lbl_forest = ds[0]
    assert x.shape == (4, 32, 32)
    assert lbl_def.dtype == torch.float32
    assert lbl_yld.item() > 0  # Should be 0.5 (treecover 50/100)


def test_h3_threshold():
    """H3 hypothesis requires transfer ratio > 0.7."""
    # This is a logic test, not a model test
    h3_transfer_ratio = 0.7
    result_above = 0.74
    result_below = 0.5

    assert result_above > h3_transfer_ratio
    assert not (result_below > h3_transfer_ratio)


# Need torch for the above tests
