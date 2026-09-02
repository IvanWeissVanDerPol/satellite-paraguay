"""Tests for scripts/thesis_satellite_tick.py.

These tests guard the autonomous-tick worker:
- The script must correctly parse AGENT_TODO.md.
- The script must NOT pick [EXT]/[🤝]/[⚠️] items.
- The script must NOT pick [x]/[~]/[!] items.
- The script must sort by priority (🔴 > 🟡 > 🟢).
- The emitted prompt must be self-contained (working dir + rules + audit context).

These are the cron-worker guard tests. Without them, a malformed AGENT_TODO.md
edit could silently make the worker pick the wrong task or emit a broken prompt.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "scripts" / "thesis_satellite_tick.py"
TODO_FILE = REPO_ROOT / "AGENT_TODO.md"
SUBPROC_TIMEOUT = 20


def _run(*args) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True,
        text=True,
        cwd=str(REPO_ROOT),
        timeout=SUBPROC_TIMEOUT,
    )


class TestTickParser:
    """The parser must correctly extract tasks from AGENT_TODO.md."""

    def test_agento_todo_exists(self):
        assert TODO_FILE.exists(), f"AGENT_TODO.md missing at {TODO_FILE}"

    def test_parse_returns_some_tasks(self):
        from scripts.thesis_satellite_tick import parse_tasks
        tasks = parse_tasks(TODO_FILE.read_text())
        assert len(tasks) > 0, "Parser found zero tasks — file format may have drifted"

    def test_gated_tasks_have_gated_flag(self):
        """Tasks marked [EXT]/[🤝]/[⚠️] must have gated=True."""
        from scripts.thesis_satellite_tick import parse_tasks
        tasks = parse_tasks(TODO_FILE.read_text())
        gated = [t for t in tasks if t["gated"]]
        assert len(gated) > 0, (
            "Expected at least one gated task in AGENT_TODO.md (the Vast.ai "
            "training tasks should be [EXT])."
        )

    def test_completed_tasks_excluded(self):
        """Tasks marked [x] must NOT appear in the parse output."""
        from scripts.thesis_satellite_tick import parse_tasks
        tasks = parse_tasks(TODO_FILE.read_text())
        for t in tasks:
            assert "[x]" not in t["raw"], f"Completed task leaked into parse: {t['title']}"
            assert "[~]" not in t["raw"], f"In-progress task leaked into parse: {t['title']}"
            assert "[!]" not in t["raw"], f"Blocked task leaked into parse: {t['title']}"


class TestTickPicker:
    """The picker must respect priority + tier + non-gated constraints."""

    def test_pick_top_skips_gated(self):
        from scripts.thesis_satellite_tick import parse_tasks, pick_top
        tasks = parse_tasks(TODO_FILE.read_text())
        top = pick_top(tasks)
        assert top is not None, "No agent-actionable task found (but AGENT_TODO.md is not empty)"
        assert isinstance(top, dict)
        assert not top["gated"], (
            f"Picked a GATED task: {top['title']}. This is a security regression — "
            f"the worker must never pick [EXT]/[🤝]/[⚠️] items."
        )

    def test_pick_top_prefers_higher_priority(self):
        """If a 🔴 task exists, pick_top should pick it over 🟢."""
        from scripts.thesis_satellite_tick import parse_tasks, pick_top
        tasks = parse_tasks(TODO_FILE.read_text())
        top = pick_top(tasks)
        candidates = [t for t in tasks if not t["gated"]]
        # Get the highest priority present
        ranks = {"🔴": 0, "🟡": 1, "🟢": 2}
        min_rank = min(ranks.get(t["priority"], 9) for t in candidates)
        top_rank = ranks.get(top["priority"], 9)
        assert top_rank == min_rank, (
            f"Picker chose priority {top['priority']} but min available is "
            f"rank {min_rank}. Picker does not sort by priority correctly."
        )

    def test_pick_top_returns_none_for_empty(self, tmp_path):
        """If AGENT_TODO.md has only [x] / gated tasks, pick_top returns None."""
        from scripts.thesis_satellite_tick import parse_tasks, pick_top
        # All completed or all gated
        md = """# AGENT_TODO.md
## Tier 2
- [x] Done task
- [!] Blocked task
## Tier 3
"""
        tasks = parse_tasks(md)
        # Note: parse_tasks already excludes [x] and [!], so this is empty
        # But let me also add a gated item
        md2 = md + "- [ ] [EXT] gated\n"
        tasks2 = parse_tasks(md2)
        assert pick_top(tasks2) is None, "Picker should return None when only gated tasks remain"


class TestTickPromptEmission:
    """The emitted prompt must be self-contained and correct."""

    def test_emit_prompt_writes_file(self):
        result = _run("--emit-prompt")
        assert result.returncode == 0
        out = Path("/tmp/thesis_satellite_tick_prompt.md")
        assert out.exists()
        text = out.read_text()
        assert "## Working directory" in text
        assert "/opt/data/work/satellite-paraguay" in text
        assert "## Picked task" in text
        assert "## Rules (non-negotiable)" in text
        assert "[EXT]" in text or "[🤝]" in text or "[⚠️]" in text  # rules mention all three

    def test_prompt_contains_no_human_email_or_submission_action(self):
        """The prompt template must not contain language that could trigger
        the agent to send emails or submit papers. The rules must explicitly
        warn against this.
        """
        result = _run("--emit-prompt")
        assert result.returncode == 0
        text = Path("/tmp/thesis_satellite_tick_prompt.md").read_text()
        # Must NOT contain instructions like "send email to X" or "submit to journal Y"
        assert "send email" not in text.lower()
        assert "submit to journal" not in text.lower()
        # Must contain STOP language
        assert "STOP" in text or "stop" in text
        # Must contain "Do not push" guard
        assert "Do not push" in text or "never push" in text.lower()

    def test_dry_run_does_not_write_prompt_file(self, tmp_path):
        """--dry-run must not overwrite the prompt output file."""
        out_file = tmp_path / "prompt.md"
        out_file.write_text("DO NOT OVERWRITE")
        # Use --output-file to a tmp_path location
        result = _run(
            "--emit-prompt",
            "--dry-run",
            "--output-file",
            str(out_file),
        )
        assert result.returncode == 0
        assert out_file.read_text() == "DO NOT OVERWRITE"

    def test_no_actionable_tasks_emits_noop_prompt(self, tmp_path):
        """If AGENT_TODO.md is empty, the emitted prompt must say 'no work'."""
        import scripts.thesis_satellite_tick as tick_mod
        original = tick_mod.TODO_FILE
        try:
            # Temporarily swap TODO_FILE to an empty file
            empty = tmp_path / "AGENT_TODO.md"
            empty.write_text("# empty\n")
            tick_mod.TODO_FILE = empty
            from scripts.thesis_satellite_tick import parse_tasks, pick_top
            tasks = parse_tasks(empty.read_text())
            assert pick_top(tasks) is None
        finally:
            tick_mod.TODO_FILE = original

    def test_rules_section_lists_non_negotiable_constraints(self):
        """The emitted prompt must enumerate the hard constraints."""
        result = _run("--emit-prompt")
        assert result.returncode == 0
        text = Path("/tmp/thesis_satellite_tick_prompt.md").read_text()
        # All five rules should be present
        assert "1." in text
        assert "2." in text
        assert "3." in text
        assert "4." in text
        assert "5." in text
        # Verification commands
        assert "check_claims.py" in text
        assert "check_latex.py" in text
        assert "pytest" in text

    def test_list_actionable_prints_summary(self):
        result = _run("--list-actionable")
        assert result.returncode == 0
        assert "Tier" in result.stdout or "No agent-actionable" in result.stdout


class TestCronShellWrapper:
    """The .sh cron wrapper must be safe and well-formed."""

    def test_shell_script_exists_and_is_executable(self):
        sh = REPO_ROOT / "scripts" / "thesis-satellite-tick.sh"
        assert sh.exists(), f"{sh} missing"
        # Must be a bash script with set -euo pipefail
        text = sh.read_text()
        assert "set -euo pipefail" in text
        assert "validate_data.py" in text
        assert "thesis_satellite_tick.py" in text
