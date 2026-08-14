"""Tests for src/utils/bootstrap.py.

Covers:
- check_pre_commit_installed: returns the right shape
- install_pre_commit_hooks: handles missing config / missing binary
- run_all_checks includes pre_commit_hooks in its output
"""

from pathlib import Path
from unittest.mock import patch

from src.utils.bootstrap import (
    check_pre_commit_installed,
    install_pre_commit_hooks,
    is_ready,
    run_all_checks,
)


class TestCheckPreCommitInstalled:
    """Tests for check_pre_commit_installed()."""

    def test_returns_dict_with_required_fields(self, tmp_path: Path) -> None:
        """Should return a dict with name, ok, path, fix fields."""
        result = check_pre_commit_installed(tmp_path)
        assert result["name"] == "pre_commit_hooks"
        assert "ok" in result
        assert "path" in result
        assert "fix" in result
        assert isinstance(result["ok"], bool)

    def test_ok_false_when_hook_missing(self, tmp_path: Path) -> None:
        """When .git/hooks/pre-commit doesn't exist, ok should be False."""
        result = check_pre_commit_installed(tmp_path)
        assert result["ok"] is False
        assert ".git/hooks/pre-commit" in result["path"]

    def test_ok_true_when_hook_present(self, tmp_path: Path) -> None:
        """When .git/hooks/pre-commit exists, ok should be True."""
        hooks_dir = tmp_path / ".git" / "hooks"
        hooks_dir.mkdir(parents=True)
        (hooks_dir / "pre-commit").write_text("#!/bin/sh\n")
        result = check_pre_commit_installed(tmp_path)
        assert result["ok"] is True


class TestInstallPreCommitHooks:
    """Tests for install_pre_commit_hooks()."""

    def test_missing_config_returns_failure(self, tmp_path: Path) -> None:
        """When .pre-commit-config.yaml is missing, return ok=False."""
        result = install_pre_commit_hooks(tmp_path)
        assert result["ok"] is False
        assert ".pre-commit-config.yaml not found" in result["reason"]

    @patch("subprocess.run")
    def test_successful_install(self, mock_run, tmp_path: Path) -> None:
        """When pre-commit install succeeds, ok=True."""
        (tmp_path / ".pre-commit-config.yaml").write_text("repos: []\n")
        mock_run.return_value = type("MockResult", (), {"returncode": 0, "stdout": "", "stderr": ""})()
        result = install_pre_commit_hooks(tmp_path)
        assert result["ok"] is True
        mock_run.assert_called_once()
        args, kwargs = mock_run.call_args
        assert args[0] == ["pre-commit", "install"]

    @patch("subprocess.run", side_effect=FileNotFoundError("pre-commit not installed"))
    def test_missing_binary_returns_failure(self, mock_run, tmp_path: Path) -> None:
        """When pre-commit binary is missing, return ok=False with reason."""
        (tmp_path / ".pre-commit-config.yaml").write_text("repos: []\n")
        result = install_pre_commit_hooks(tmp_path)
        assert result["ok"] is False
        assert "pre-commit not installed" in result["reason"]


class TestIsReady:
    """Tests for is_ready() with pre_commit_hooks field."""

    def test_is_ready_includes_pre_commit_field(self, tmp_path: Path) -> None:
        """is_ready should tolerate pre_commit_hooks being absent or present."""
        base = {
            "python": {"ok": True},
            "deps": {"ok": True},
            "data_dir": {"ok": True},
        }
        # No pre_commit_hooks field — should default to True (treat as optional)
        assert is_ready(base) is True
        # With pre_commit_hooks: True
        base["pre_commit_hooks"] = {"ok": True}
        assert is_ready(base) is True
        # With pre_commit_hooks: False (acceptable, just a warning)
        base["pre_commit_hooks"] = {"ok": False}
        assert is_ready(base) is True  # pre-commit failure is non-blocking

    def test_is_ready_fails_on_missing_deps(self) -> None:
        """When deps are missing, is_ready should return False."""
        base = {
            "python": {"ok": True},
            "deps": {"ok": False},
            "data_dir": {"ok": True},
        }
        assert is_ready(base) is False


class TestRunAllChecks:
    """Tests that run_all_checks includes pre_commit_hooks."""

    @patch("src.utils.bootstrap.setup_directories")
    @patch("src.utils.bootstrap.check_dvc_initialized")
    @patch("src.utils.bootstrap.check_network")
    @patch("src.utils.bootstrap.check_gpu")
    @patch("src.utils.bootstrap.check_key_data_files")
    @patch("src.utils.bootstrap.check_data_directory")
    @patch("src.utils.bootstrap.check_dependencies")
    @patch("src.utils.bootstrap.check_python_version")
    def test_run_all_checks_includes_pre_commit(
        self,
        mock_py,
        mock_deps,
        mock_data_dir,
        mock_data_files,
        mock_gpu,
        mock_network,
        mock_dvc,
        mock_dirs,
        tmp_path: Path,
    ) -> None:
        """run_all_checks should include 'pre_commit_hooks' key in output."""
        # Make all sub-checks return ok=True
        for mock in [mock_py, mock_deps, mock_data_dir, mock_data_files, mock_gpu, mock_network, mock_dvc, mock_dirs]:
            mock.return_value = {"ok": True, "name": "stub"}

        # Don't actually call check_pre_commit_installed (it touches real paths)
        # Patch it explicitly
        with patch(
            "src.utils.bootstrap.check_pre_commit_installed",
            return_value={"name": "pre_commit_hooks", "ok": False, "path": "/tmp/.git/hooks/pre-commit"},
        ):
            result = run_all_checks(tmp_path)

        assert "pre_commit_hooks" in result
        assert result["pre_commit_hooks"]["name"] == "pre_commit_hooks"
