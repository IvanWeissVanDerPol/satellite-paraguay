"""Tests for scripts/verify_p0030_numbers.py.

This test invokes the independent verification script and asserts
that the pipeline output and the raw-CSV re-derivation agree. If
either the raw CSVs or the pipeline output drift apart, this test
catches it before any defense.
"""

import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
PYTHON = str(REPO_ROOT / ".venv" / "bin" / "python")
if not Path(PYTHON).exists():
    PYTHON = sys.executable


class TestP0030IndependentVerification:
    """Verify P0030 headline numbers match between raw CSVs and pipeline."""

    def test_verify_script_exits_zero(self):
        """scripts/verify_p0030_numbers.py exits with code 0 when all checks match."""
        result = subprocess.run(
            [PYTHON, str(REPO_ROOT / "scripts" / "verify_p0030_numbers.py")],
            capture_output=True,
            text=True,
            cwd=str(REPO_ROOT),
        )
        assert result.returncode == 0, (
            f"verify_p0030_numbers.py failed:\n" f"stdout: {result.stdout}\n" f"stderr: {result.stderr}"
        )
        assert "PASS" in result.stdout, f"Expected PASS in output:\n{result.stdout}"

    def test_verify_script_reports_pueblos_count(self):
        """Output reports 19 pueblos (matches pipeline + ACTUAL_RESULTS.md)."""
        result = subprocess.run(
            [PYTHON, str(REPO_ROOT / "scripts" / "verify_p0030_numbers.py")],
            capture_output=True,
            text=True,
            cwd=str(REPO_ROOT),
        )
        assert "raw=19" in result.stdout
        assert "pipe=19" in result.stdout

    def test_verify_script_reports_557_communities(self):
        """Output reports 557 total communities."""
        result = subprocess.run(
            [PYTHON, str(REPO_ROOT / "scripts" / "verify_p0030_numbers.py")],
            capture_output=True,
            text=True,
            cwd=str(REPO_ROOT),
        )
        assert "raw=557" in result.stdout
        assert "pipe=557" in result.stdout

    def test_verify_script_reports_national_yield(self):
        """Output reports national mean yield of 2,428.8 kg/ha."""
        result = subprocess.run(
            [PYTHON, str(REPO_ROOT / "scripts" / "verify_p0030_numbers.py")],
            capture_output=True,
            text=True,
            cwd=str(REPO_ROOT),
        )
        assert "raw=2428.8" in result.stdout
        assert "pipe=2428.8" in result.stdout
