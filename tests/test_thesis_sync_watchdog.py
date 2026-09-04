"""Tests for scripts/thesis_sync_watchdog.py.

These tests guard the cross-repo sync worker:
- The watchdog must NOT auto-edit STATUS.md (it only writes drift_note.md).
- The watchdog must detect drift signals (missing datasets, etc).
- The watchdog must be idempotent (running twice produces the same output
  when nothing has changed).

These are the cron-worker guard tests for the second autonomous worker.
"""

import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "scripts" / "thesis_sync_watchdog.py"
AUDIT_JSON = REPO_ROOT / "outputs" / "data_audit.json"
WATCHDOG_LOG = REPO_ROOT / "logs" / "thesis_sync_watchdog.log"
DRIFT_NOTE = REPO_ROOT / "outputs" / "drift_note.md"
SUBPROC_TIMEOUT = 60


def _run(*args) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True,
        text=True,
        cwd=str(REPO_ROOT),
        timeout=SUBPROC_TIMEOUT,
    )


class TestWatchdogRuns:
    """The watchdog must run cleanly end-to-end."""

    def test_run_succeeds(self):
        result = _run()
        assert result.returncode == 0, f"Watchdog exited {result.returncode}. STDERR:\n{result.stderr[:500]}"

    def test_run_writes_audit_json(self):
        # First ensure the audit exists
        if not AUDIT_JSON.exists():
            _run()
        assert AUDIT_JSON.exists()

    def test_run_writes_drift_note(self):
        _run()
        assert DRIFT_NOTE.exists(), f"Drift note not written to {DRIFT_NOTE}"
        text = DRIFT_NOTE.read_text()
        assert "drift" in text.lower()
        assert "Present" in text or "present" in text

    def test_run_appends_to_log(self):
        _run()
        assert WATCHDOG_LOG.exists()
        last = WATCHDOG_LOG.read_text().strip().splitlines()[-1]
        assert "audit_sha=" in last
        assert "changed=" in last
        assert "signals=" in last


class TestWatchdogSafety:
    """The watchdog must not accidentally mutate STATUS.md or other state."""

    def test_status_md_not_modified(self):
        """STATUS.md must NEVER be auto-edited by the watchdog. This is a
        hard invariant — STATUS.md is human-curated.
        """
        status_path = REPO_ROOT / "STATUS.md"
        if not status_path.exists():
            pytest.skip("STATUS.md not present in this checkout")
        mtime_before = status_path.stat().st_mtime
        _run()
        mtime_after = status_path.stat().st_mtime
        assert mtime_before == mtime_after, "STATUS.md mtime changed — watchdog must not auto-edit STATUS.md"

    def test_papers_not_modified(self):
        """No paper.md or paper.tex file may be touched by a watchdog run."""
        papers_dir = REPO_ROOT / "papers" / "drafts"
        if not papers_dir.exists():
            pytest.skip("No papers dir")
        before = {p.name: p.stat().st_mtime for p in papers_dir.rglob("paper.*")}
        _run()
        after = {p.name: p.stat().st_mtime for p in papers_dir.rglob("paper.*")}
        for name, mtime in before.items():
            assert after.get(name) == mtime, f"Paper file {name} was modified by watchdog — forbidden."


class TestWatchdogDriftDetection:
    """The watchdog must correctly detect drift signals."""

    def test_drift_note_contains_signal_section(self):
        _run()
        text = DRIFT_NOTE.read_text()
        assert "Drift signals" in text or "No drift detected" in text

    def test_missing_datasets_produce_warning_signal(self):
        """If validate_data.py reports any missing, the drift note must flag it."""
        _run()  # ensure audit is fresh
        audit = json.loads(AUDIT_JSON.read_text())
        missing_count = audit["by_status_count"].get("missing", 0)
        if missing_count > 0:
            text = DRIFT_NOTE.read_text()
            assert (
                "MISSING" in text or "missing" in text
            ), f"Drift note should warn about {missing_count} missing datasets"


class TestWatchdogIdempotency:
    """Running the watchdog twice must not corrupt state."""

    def test_double_run_is_stable(self):
        r1 = _run()
        r2 = _run()
        assert r1.returncode == 0
        assert r2.returncode == 0
        # Drift note should still exist and still be valid markdown
        assert DRIFT_NOTE.exists()
        text = DRIFT_NOTE.read_text()
        # Header must be present (any 2nd run overwrites the same file)
        assert text.startswith("# Thesis sync watchdog drift note")

    def test_check_mode_prints_changed_flag(self):
        r1 = _run()
        r2 = _run("--check")
        assert r1.returncode == 0
        assert r2.returncode == 0
        assert "changed=" in r2.stdout
        assert "signals=" in r2.stdout


class TestWatchdogPromptEmission:
    """The emitted prompt must be cron-ready and self-contained."""

    def test_emit_prompt_runs(self):
        result = _run("--emit-prompt")
        assert result.returncode == 0
        text = result.stdout
        assert "## What this tick does" in text
        assert "/opt/data/work/satellite-paraguay" in text
        assert "audit" in text.lower()
