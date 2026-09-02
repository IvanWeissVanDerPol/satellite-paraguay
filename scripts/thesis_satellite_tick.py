"""thesis_satellite_tick.py — Pick the next agent-actionable task from
AGENT_TODO.md and emit a self-contained prompt for the cron runner.

This is the satellite-paraguay equivalent of thesis-active's
autonomous_tick.py, but with a critical difference: it does NOT
auto-execute. It emits a prompt that a parent process (or a human) can
hand to the LLM. This is the safer pattern for a paper-writing repo —
the agent cannot accidentally submit, sign, or send.

Behavior:
- Parse AGENT_TODO.md into a list of tasks.
- Filter out [EXT], [🤝], [⚠️], [x], [~], [!].
- Sort by priority (🔴 > 🟡 > 🟢) + line number (top of file wins).
- Pick the top item.
- Emit a structured prompt that includes:
  - Working directory
  - The chosen task with its context
  - The non-negotiable rules (no money, no email, no submit)
  - The verification commands (check_claims, check_latex, pytest)
  - The data audit snapshot
- Write the prompt to a file (--output-file) AND stdout.

Usage:
    python3 scripts/thesis_satellite_tick.py --emit-prompt
    python3 scripts/thesis_satellite_tick.py --emit-prompt --dry-run
    python3 scripts/thesis_satellite_tick.py --list-actionable
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TODO_FILE = REPO_ROOT / "AGENT_TODO.md"

PRIORITY_RANK = {"🔴": 0, "🟡": 1, "🟢": 2}
GATED_TOKENS = ("[EXT]", "[🤝]", "[⚠️]", "[x]", "[~]", "[!]")
TIER_HEADERS = {
    "Tier 2": 0,
    "Tier 3": 1,
    "Tier 4": 2,  # 🤝 only — agent supports
    "Tier 5": 3,  # ⛔ out of scope
}


def parse_tasks(md_text: str) -> list[dict]:
    """Parse AGENT_TODO.md into a list of task dicts.

    Supports two formats found in this file:
    - The 'old' checklist format: `- [ ] 🔴 A. Title — context [EXT]`
    - The 'new' section-header format: `### 🔴 K. Title` followed by sub-bullets
    """
    tasks = []
    current_tier = None
    line_no = 0
    in_section = False
    section_title = ""
    section_priority = None
    section_id = ""
    section_gated = False
    section_context_lines: list[str] = []

    # Pattern for the new section-header format
    section_re = re.compile(r"^###\s+(🔴|🟡|🟢|🤝|⚠️)?\s*([A-Z0-9]+)\.\s+(.+)$")
    # Sub-bullet context line (in new format)
    sub_bullet_re = re.compile(r"^\s+-\s+(.+)$")

    def flush_section() -> None:
        nonlocal in_section, section_title, section_priority
        nonlocal section_id, section_gated, section_context_lines
        if in_section:
            context = " ".join(section_context_lines).strip()
            tasks.append(
                {
                    "line_no": line_no,
                    "tier": current_tier,
                    "priority": section_priority or "🟢",
                    "gated": section_gated,
                    "title": section_title,
                    "context": context,
                    "raw": f"### {section_id}. {section_title}",
                }
            )
            in_section = False
            section_title = ""
            section_priority = None
            section_id = ""
            section_gated = False
            section_context_lines = []

    for line in md_text.splitlines():
        line_no += 1
        # Tier header
        tier_m = re.match(r"^##\s+(Tier\s+\d+)\b", line)
        if tier_m:
            flush_section()
            current_tier = tier_m.group(1)
            continue
        # New section-header format
        sec_m = section_re.match(line)
        if sec_m:
            flush_section()
            in_section = True
            section_priority = sec_m.group(1) or "🟢"
            section_id = sec_m.group(2)
            section_title = sec_m.group(3).strip()
            section_gated = section_priority in ("🤝", "⚠️")
            continue
        # Inside a new-format section, accumulate sub-bullets
        if in_section:
            sub_m = sub_bullet_re.match(line)
            if sub_m:
                section_context_lines.append(sub_m.group(1).strip())
                continue
            # A blank line ends the section if the next non-blank is not a sub-bullet
            if line.strip() == "":
                continue
            # Any other line (e.g. another ### header, paragraph) ends the section
            # Note: ### header case is handled by section_re.match above
            continue
        # Old checklist format
        if not line.lstrip().startswith("- ["):
            continue
        if any(tok in line for tok in ("[x]", "[~]", "[!]")):
            continue
        prio_m = re.search(r"(🔴|🟡|🟢)\s*([A-Z]\.\s+)?", line)
        priority = prio_m.group(1) if prio_m else "🟢"
        rest = re.sub(r"^\s*-\s*\[\s*\]\s*", "", line)
        rest = re.sub(r"^[🔴🟡🟢]\s*[A-Z]?\.\s*", "", rest)
        title_m = re.match(r"^([^—\-]+?)\s*[—\-]\s*(.*)$", rest)
        if title_m:
            title = title_m.group(1).strip()
            context = title_m.group(2).strip()
        else:
            title = rest.strip()
            context = ""
        gated = any(tok in line for tok in ("[EXT]", "[🤝]", "[⚠️]"))
        tasks.append(
            {
                "line_no": line_no,
                "tier": current_tier,
                "priority": priority,
                "gated": gated,
                "title": title,
                "context": context,
                "raw": line.strip(),
            }
        )
    flush_section()
    return tasks


def pick_top(tasks: list[dict]) -> dict | None:
    """Pick the highest-priority agent-actionable (non-gated) task."""
    candidates = [t for t in tasks if not t["gated"]]
    if not candidates:
        return None
    # Sort: priority ascending (🔴 first), tier ascending (Tier 2 first),
    # line_no ascending (top of file first).
    candidates.sort(
        key=lambda t: (
            PRIORITY_RANK.get(t["priority"], 9),
            TIER_HEADERS.get(t["tier"], 9),
            t["line_no"],
        )
    )
    return candidates[0]


def build_prompt(task: dict, audit_summary: str, audit_path: str) -> str:
    """Build the self-contained prompt to emit to the parent runner."""
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    parts = [
        f"# Thesis tick prompt — {now}",
        "",
        "## Working directory",
        "`/opt/data/work/satellite-paraguay`",
        "",
        "## Picked task",
        "",
        f"**Tier:** {task['tier'] or '(no tier)'}",
        f"**Priority:** {task['priority']}",
        f"**Title:** {task['title']}",
        f"**Context:** {task['context'] or '(none)'}",
        f"**Source line:** AGENT_TODO.md:{task['line_no']}",
        "",
        "## Rules (non-negotiable)",
        "",
        "1. This task is **not** marked [EXT]/[🤝]/[⚠️]. If you find yourself "
        "needing Ivan's input, credentials, real money, real signature, real "
        "submission, or real email — STOP and document the blocker.",
        "2. Run the honest-reporting guards after every change:",
        "   ```",
        "   python3 scripts/check_claims.py",
        "   python3 scripts/check_ethics.py",
        "   python3 scripts/check_latex.py",
        "   ```",
        "3. Run the targeted pytest guards:",
        "   ```",
        "   pytest tests/test_fail_loud_guard.py tests/test_validate_data.py "
        "tests/test_reproducibility.py -q --no-cov",
        "   ```",
        "4. Atomic commit with conventional commit message. **Do not push.**",
        "5. Append a one-paragraph tick summary under " "`AGENT_TODO.md → ## Recent autonomous ticks (2026-09+)`.",
        "",
        "## Data audit context",
        "",
        "```",
        audit_summary,
        "```",
        f"(full audit at `{audit_path}`)",
        "",
        "## Verification commands (must all return 0)",
        "",
        "```bash",
        "cd /opt/data/work/satellite-paraguay",
        "python3 scripts/check_claims.py   # OK -- no unsanctioned claims",
        "python3 scripts/check_latex.py    # 6/6 papers pass",
        ".venv/bin/python -m pytest tests/test_fail_loud_guard.py tests/test_validate_data.py -q --no-cov  # 30 passed",
        "```",
        "",
        "## When done",
        "",
        "Append to `AGENT_TODO.md` under a new " "`## Recent autonomous ticks (2026-09+)` section:",
        "",
        "```",
        f"### {now} — {task['title']}",
        "<one-paragraph summary of what you did, what you committed, what you verified>",
        "```",
        "",
        "Now execute the task.",
    ]
    return "\n".join(parts) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Pick the next agent-actionable task from AGENT_TODO.md.")
    parser.add_argument(
        "--emit-prompt",
        action="store_true",
        help="Emit a self-contained prompt for the cron runner.",
    )
    parser.add_argument(
        "--list-actionable",
        action="store_true",
        help="List all agent-actionable tasks (no prompt emitted).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would be picked without writing the prompt file.",
    )
    parser.add_argument(
        "--output-file",
        type=str,
        default="/tmp/thesis_satellite_tick_prompt.md",
        help="Path to write the emitted prompt.",
    )
    parser.add_argument(
        "--audit-file",
        type=str,
        default="/tmp/thesis_data_audit.txt",
        help="Path to the data audit summary file.",
    )
    args = parser.parse_args()

    if not TODO_FILE.exists():
        print(f"ERROR: {TODO_FILE} does not exist", file=sys.stderr)
        return 1

    md = TODO_FILE.read_text()
    tasks = parse_tasks(md)

    if args.list_actionable:
        candidates = [t for t in tasks if not t["gated"]]
        if not candidates:
            print("No agent-actionable tasks remaining.")
            return 0
        for i, t in enumerate(candidates[:20], 1):
            line = f"{i:2}. [{t['priority']}] {t['tier'] or '-':8} " f"L{t['line_no']:4} {t['title'][:80]}"
            try:
                print(line)
            except BrokenPipeError:
                # Allow piping to head/less without traceback
                sys.stderr.close()
                return 0
        return 0

    if not args.emit_prompt:
        parser.print_help()
        return 0

    top = pick_top(tasks)
    if top is None:
        print("No agent-actionable tasks remaining.")
        # Emit an empty prompt so the cron runner logs "no work" cleanly
        prompt = (
            "# Thesis tick prompt — no agent-actionable tasks remaining\n\n"
            "AGENT_TODO.md has no [ ] / [P#] / [W] / [R] / [A] / [D] items "
            "that are not [EXT]/[🤝]/[⚠️]. Nothing to do this tick.\n"
        )
        if not args.dry_run:
            Path(args.output_file).write_text(prompt)
        print(prompt)
        return 0

    audit_path = Path(args.audit_file)
    audit_summary = audit_path.read_text().strip() if audit_path.exists() else "(no audit file)"

    prompt = build_prompt(top, audit_summary, str(audit_path))

    if not args.dry_run:
        Path(args.output_file).write_text(prompt)
        print(f"Emitted prompt for task: {top['title']}", file=sys.stderr)
        print(f"  → {args.output_file}", file=sys.stderr)
    print(prompt)
    return 0


if __name__ == "__main__":
    sys.exit(main())
