#!/usr/bin/env python3
"""
Drift detector: compare measured scores in STATUS.md vs a snapshot.

If `docs/security/scorecard-snapshot.json` exists, compares today's
scorecard to it. Reports drifts >threshold_pct.

First run: snapshots current STATUS.md as baseline.
Subsequent runs: alerts on drift.

Cron: run daily at 06:00 UTC, alert on drift via org-state.
"""

import argparse
import json
import re
import sys
from pathlib import Path


SCORE_PATTERN = re.compile(
    r"^\|\s*P(\d{4})\s+(\w+)\s*\|"
    r"\s*(?:\*\*)?(\d+)/100(?:\*\*)?\s*\("
    r"[^)]*\)\s*\|"
    r"\s*(?:\*\*)?(\d+)/100(?:\*\*)?\s*\("
    r"[^)]*\)\s*\|"
    r"\s*(?:\*\*)?(\d+)/100(?:\*\*)?\s*/100\s+"  # paper score like "100/100"
    r"(?:\d+)\s+words?[^|]*\|\s*"
    r"(?:\*\*)?(\d+)/100(?:\*\*)?(?:\s*\([^)]*\))?\s*\|",
    re.MULTILINE,
)


def parse_scorecard(path):
    """Parse a per-paper scorecard table.

    Returns dict like {"P0011": {"data": 5, "model": 0, "paper": 100, "ethics": 0}}.
    """
    if not path.exists():
        return {}

    text = path.read_text()
    scores = {}

    for line in text.split("\n"):
        if not line.startswith("| P"):
            continue
        cells = [c.strip() for c in line.split("|")]
        if len(cells) < 7:
            continue

        m = re.match(r"P(\d{4})\s+(\w+)", cells[1])
        if not m:
            continue
        pid = f"P{m.group(1)}"

        def first_score(cell):
            mm = re.search(r"(\d+)/100", cell)
            return int(mm.group(1)) if mm else 0

        scores[pid] = {
            "data": first_score(cells[2]),
            "model": first_score(cells[3]),
            "paper": first_score(cells[4]),
            "ethics": first_score(cells[5]),
            "overall": first_score(cells[6]),
        }

    return scores


def check_drift(current, baseline, threshold_pct=10.0):
    """Compare current scores vs baseline. None baseline = first run."""
    from datetime import datetime
    alerts = []
    info = []
    new_papers = []

    if baseline is None:
        # First run: nothing to compare
        for pid, axes in current.items():
            info.append({
                "paper_id": pid,
                "axis": "ALL",
                "current_score": max(axes.values()),
                "baseline_score": None,
                "drift_pct": None,
                "message": "First run — no baseline yet",
            })
        return {
            "checked_at": datetime.utcnow().isoformat() + "Z",
            "threshold_pct": threshold_pct,
            "papers_checked": len(current),
            "alerts_count": 0,
            "alerts": alerts,
            "info_count": len(info),
            "info": info,
            "first_run": True,
        }

    for pid in set(current) | set(baseline):
        cur = current.get(pid, {})
        base = baseline.get(pid, {})

        if not cur and base:
            new_papers.append(pid)
            continue
        if not base and cur:
            new_papers.append(pid)
            continue

        for axis in ("data", "model", "paper", "ethics", "overall"):
            c_val = cur.get(axis, 0)
            b_val = base.get(axis, 0)
            if c_val == 0 and b_val == 0:
                continue

            max_val = max(c_val, b_val, 1)
            drift_pct = abs(c_val - b_val) / max_val * 100

            if drift_pct > threshold_pct:
                alerts.append({
                    "paper_id": pid,
                    "axis": axis,
                    "current_score": c_val,
                    "baseline_score": b_val,
                    "drift_pct": round(drift_pct, 1),
                    "direction": "improvement" if c_val > b_val else "regression",
                    "severity": "HIGH" if drift_pct > 25 else "MEDIUM",
                })
            else:
                info.append({
                    "paper_id": pid,
                    "axis": axis,
                    "current_score": c_val,
                    "baseline_score": b_val,
                    "drift_pct": round(drift_pct, 1),
                })

    return {
        "checked_at": datetime.utcnow().isoformat() + "Z",
        "threshold_pct": threshold_pct,
        "papers_checked": len(set(current) | set(baseline)),
        "alerts_count": len(alerts),
        "alerts": alerts,
        "info_count": len(info),
        "info": info[:10],
        "first_run": False,
        "new_papers": new_papers,
    }


def snapshot(repo_root):
    """Write current scorecard to snapshot file."""
    from datetime import datetime
    status_path = repo_root / "STATUS.md"
    snapshot_path = repo_root / "docs" / "security" / "scorecard-snapshot.json"

    scores = parse_scorecard(status_path)
    snapshot_path.parent.mkdir(parents=True, exist_ok=True)
    snapshot_path.write_text(json.dumps({
        "snapshot_at": datetime.utcnow().isoformat() + "Z",
        "scores": scores,
    }, indent=2))
    return scores


def main():
    parser = argparse.ArgumentParser(description="Drift detector for satellite-paraguay papers")
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--threshold", type=float, default=10.0,
                        help="Drift threshold in percent (default: 10)")
    parser.add_argument("--json", action="store_true", help="JSON output")
    parser.add_argument("--strict", action="store_true",
                        help="Exit 1 on any drift >threshold")
    parser.add_argument("--snapshot", action="store_true",
                        help="Snapshot current scorecard as new baseline")
    parser.add_argument("--reset", action="store_true",
                        help="Delete existing snapshot, then take new one")
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()
    status_path = repo_root / "STATUS.md"
    snapshot_path = repo_root / "docs" / "security" / "scorecard-snapshot.json"

    if not status_path.exists():
        print(f"ERROR: {status_path} not found", file=sys.stderr)
        sys.exit(2)

    if args.reset and snapshot_path.exists():
        snapshot_path.unlink()

    current = parse_scorecard(status_path)

    if args.snapshot:
        snapshot(repo_root)
        print(f"Snapshot written to {snapshot_path}")
        print(f"Papers snapshotted: {len(current)}")
        sys.exit(0)

    if snapshot_path.exists():
        baseline_data = json.loads(snapshot_path.read_text())
        baseline = baseline_data.get("scores", {})
    else:
        # No baseline: take one and report
        snapshot(repo_root)
        print(f"No baseline found. Snapshot written to {snapshot_path}")
        print("Run again tomorrow (or any later date) to detect drift.")
        sys.exit(0)

    result = check_drift(current, baseline, args.threshold)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print("=" * 70)
        print("DRIFT DETECTOR — satellite-paraguay")
        print(f"Threshold: {args.threshold}%")
        print("=" * 70)

        if result.get("first_run"):
            print(f"\n[first run] {result['papers_checked']} papers, no baseline yet")
        elif result["alerts_count"] == 0:
            print(f"\n✓ All {result['papers_checked']} papers within drift threshold")
            print(f"  ({result['info_count']} axis-paper pairs checked)")
        else:
            print(f"\n⚠ {result['alerts_count']} drift alert(s):")
            for a in result["alerts"]:
                arrow = "↑" if a["direction"] == "improvement" else "↓"
                print(f"  {a['severity']}  {a['paper_id']} {a['axis']}: "
                      f"{a['baseline_score']} → {a['current_score']} {arrow} "
                      f"({a['drift_pct']}% drift)")

        if result.get("new_papers"):
            print(f"\nNew papers (no baseline): {result['new_papers']}")

        if result["info"]:
            print(f"\nInfo (drift < {args.threshold}%):")
            for i in result["info"]:
                print(f"  · {i['paper_id']} {i['axis']}: "
                      f"{i['baseline_score']} → {i['current_score']} ({i['drift_pct']}%)")

        if args.strict and result["alerts_count"] > 0:
            sys.exit(1)


if __name__ == "__main__":
    main()