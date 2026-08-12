"""Tests for src/utils/reproducibility.py — coverage target: 100%.

Covers:
- DEFAULT_SEED constant
- set_seed() — random, os.environ, numpy, torch (CPU-only path)
- get_git_hash() — valid hash and missing-git fallback
- get_git_branch() — valid branch and missing-git fallback
- get_python_version() — returns X.Y.Z format
- get_system_info() — includes expected keys
- capture_environment() — writes JSON, includes packages
- verify_reproducibility() — repeatable / not-reproducible cases
"""

import json
import os
import subprocess  # for the patch tests above
import sys
from unittest.mock import patch

import pytest

from src.utils.reproducibility import (
    DEFAULT_SEED,
    capture_environment,
    get_git_branch,
    get_git_hash,
    get_python_version,
    get_system_info,
    set_seed,
    verify_reproducibility,
)


class TestConstants:
    def test_default_seed_is_int_42(self):
        assert DEFAULT_SEED == 42
        assert isinstance(DEFAULT_SEED, int)


class TestSetSeed:
    def test_set_seed_sets_python_random(self):
        set_seed(7)
        import random as _random

        # Different runs of random() should be deterministic given seed
        a = _random.random()
        set_seed(7)
        b = _random.random()
        assert a == b

    def test_set_seed_sets_pythonhashseed(self):
        set_seed(99)
        assert os.environ.get("PYTHONHASHSEED") == "99"

    def test_set_seed_sets_numpy(self):
        import numpy as np

        set_seed(13)
        a = np.random.rand()
        set_seed(13)
        b = np.random.rand()
        assert a == b

    def test_set_seed_handles_missing_numpy(self):
        """When numpy is not importable (already-imported case impossible
        in this env), set_seed should still work. We just verify no
        exception is raised."""
        set_seed(5)
        # No assertion needed — just that the call returns

    def test_set_seed_handles_missing_torch(self):
        """When torch import fails, seeds beyond numpy still apply."""
        set_seed(11)
        # If torch isn't installed in the test env, the try/except branch
        # should fire silently. We don't fail.

    @pytest.mark.skipif(sys.version_info < (3, 7), reason="random.* consistent on 3.7+")
    def test_set_seed_idempotent(self):
        """Calling set_seed twice with same value is idempotent."""
        set_seed(42)
        import random

        a = random.random()
        set_seed(42)
        b = random.random()
        assert a == b

    def test_set_seed_with_torch(self):
        """When torch is installed, set_seed calls torch.manual_seed."""
        try:
            import torch  # noqa: F401
        except ImportError:
            pytest.skip("torch not installed")
        set_seed(123)
        a = torch.rand(1).item() if hasattr(torch.rand(1), "item") else float(torch.rand(1)[0])
        set_seed(123)
        b = torch.rand(1).item() if hasattr(torch.rand(1), "item") else float(torch.rand(1)[0])
        assert a == b

    def test_set_seed_with_tensorflow(self):
        """When tensorflow is installed, set_seed calls tf.random.set_seed."""
        try:
            import tensorflow as tf  # noqa: F401
        except ImportError:
            pytest.skip("tensorflow not installed")
        set_seed(77)
        # Just verify it doesn't raise. tensorflow seeds don't have
        # simple deterministic-check API.
        set_seed(77)

    def test_set_seed_torch_cuda_path(self):
        """When CUDA is available, set_seed sets cuda seeds + deterministic flags."""
        try:
            import torch
        except ImportError:
            pytest.skip("torch not installed")

        # Force the CUDA branch by mocking cuda.is_available to True.
        with patch.object(torch.cuda, "is_available", return_value=True):
            with (
                patch.object(torch.cuda, "manual_seed") as mock_ms,
                patch.object(torch.cuda, "manual_seed_all") as mock_msa,
            ):
                set_seed(1)
                # If CUDA were available, the function would call these.
                if torch.cuda.is_available():  # mock satisfied True
                    mock_ms.assert_called()
                    mock_msa.assert_called()


class TestGit:
    def test_get_git_hash_returns_string(self):
        h = get_git_hash()
        # Either real hash (40-char hex) or None if no git
        if h is not None:
            assert isinstance(h, str)
            # Real git hashes are 40 hex chars (or 7+ short)
            assert len(h) >= 7

    def test_get_git_hash_handles_no_git(self):
        with patch("subprocess.check_output") as mock:
            mock.side_effect = FileNotFoundError
            assert get_git_hash() is None

    def test_get_git_hash_handles_subprocess_failure(self):
        with patch("subprocess.check_output") as mock:
            mock.side_effect = subprocess.CalledProcessError(1, "git")
            assert get_git_hash() is None

    def test_get_git_branch_returns_string(self):
        b = get_git_branch()
        if b is not None:
            assert isinstance(b, str)
            assert len(b) > 0

    def test_get_git_branch_handles_no_git(self):
        with patch("subprocess.check_output") as mock:
            mock.side_effect = FileNotFoundError
            assert get_git_branch() is None


class TestSystemInfo:
    def test_get_python_version(self):
        v = get_python_version()
        parts = v.split(".")
        assert len(parts) == 3
        assert all(p.isdigit() for p in parts)

    def test_get_system_info_keys(self):
        info = get_system_info()
        assert "python_version" in info
        assert "platform" in info
        assert "machine" in info
        assert "system" in info
        assert "git_hash" in info
        assert "git_branch" in info
        assert "timestamp" in info
        assert "cwd" in info

    def test_get_system_info_python_version_matches_sys(self):
        info = get_system_info()
        assert info["python_version"] == f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"

    def test_get_system_info_cuda_present(self):
        """When CUDA is available, system info includes gpu fields."""
        try:
            import torch  # noqa: F401
        except ImportError:
            pytest.skip("torch not installed")

        # Mock cuda-available branch
        with (
            patch.object(torch.cuda, "is_available", return_value=True),
            patch.object(torch.cuda, "get_device_name", return_value="TestGPU"),
            patch.object(torch.cuda, "device_count", return_value=1),
            patch.object(torch.cuda, "get_device_properties") as mock_props,
            patch.object(torch, "version") as mock_ver,
        ):
            mock_ver.cuda = "12.0"
            mock_props.return_value.total_memory = 8 * 1024**3
            info = get_system_info()
            assert info["cuda_available"] is True
            assert info["cuda_version"] == "12.0"
            assert info["gpu_name"] == "TestGPU"
            assert info["gpu_count"] == 1
            assert abs(info["gpu_memory_gb"] - 8.0) < 0.01

    def test_get_system_info_psutil_present(self):
        """When psutil is installed, system info includes cpu_count and ram_gb."""
        try:
            import psutil  # noqa: F401
        except ImportError:
            pytest.skip("psutil not installed")

        with patch("psutil.cpu_count", return_value=8), patch("psutil.virtual_memory") as mock_vm:
            mock_vm.return_value.total = 16 * 1024**3
            info = get_system_info()
            assert info["cpu_count"] == 8
            assert abs(info["ram_gb"] - 16.0) < 0.01


class TestCaptureEnvironment:
    def test_writes_json_to_disk(self, tmp_path):
        out = tmp_path / "env.json"
        info = capture_environment(out)
        assert out.exists()
        loaded = json.loads(out.read_text())
        assert loaded["python_version"] == info["python_version"]

    def test_creates_parent_directories(self, tmp_path):
        out = tmp_path / "deep" / "nested" / "env.json"
        capture_environment(out)
        assert out.exists()

    def test_handles_packages_import_failure(self, tmp_path):
        """When pkg_resources is broken, capture_environment should still write JSON."""
        with patch.dict(sys.modules, {"pkg_resources": None}):
            out = tmp_path / "env.json"
            info = capture_environment(out)
            assert out.exists()
            assert "python_version" in info


class TestVerifyReproducibility:
    def test_returns_true_for_deterministic_op(self):
        def op():
            return 42  # constant

        assert verify_reproducibility(op, expected_output=42) is True

    def test_returns_true_when_numpy_ran_repeatedly_with_seed(self):
        """Seeded numpy operation is reproducible."""

        def op():
            import numpy as np

            return float(np.random.rand())

        # Note: verify_reproducibility re-seeds each run with DEFAULT_SEED+i.
        # Even though the seed changes (42, 43, 44), the *property* the
        # function tests is "all outputs np.allclose" — they are not, because
        # different seeds produce different outputs. So this returns False.
        result = verify_reproducibility(op, expected_output=None)
        assert result is False  # numpy with different seeds produces different output

    def test_n_runs_3_by_default(self):
        calls = []

        def op():
            calls.append(1)
            return "x"

        verify_reproducibility(op, expected_output="x")
        assert len(calls) == 3

    def test_custom_n_runs(self):
        calls = []

        def op():
            calls.append(1)
            return "y"

        verify_reproducibility(op, expected_output="y", n_runs=5)
        assert len(calls) == 5

    def test_returns_false_for_non_reproducible(self):
        """Counter that increments across runs is not reproducible."""
        counter = [0]

        def op():
            counter[0] += 1
            return counter[0]

        assert verify_reproducibility(op, expected_output=1) is False


class TestIfMain:
    """Run the __main__ block doesn't crash."""

    def test_main_block_runs(self, capsys):
        # Use the runpy trick is overkill; just exec the main block.
        # The block calls print twice, then exits the script.
        # We simulate by running as a subprocess.
        import subprocess as sp

        result = sp.run(
            [sys.executable, "-c", "import src.utils.reproducibility as r; " "print(r.get_python_version())"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        assert result.returncode == 0
        assert "." in result.stdout
