#!/usr/bin/env python3
"""defense_check.py — One command to verify defense-readiness.

Runs every check that determines whether this thesis can be submitted to FADA.
Each check is run as a subprocess so failures are isolated; the wrapper
collects results and prints a single summary table.

If ANY check fails, this script exits non-zero. The intent is that running
this script should be the last thing you do before declaring the thesis
defense-ready.

Checks (in order):
    1. Citation resolution     — check_citations.py --all
    2. Paper claim integrity   — check_claims.py
    3. Ethics gates            — check_ethics.py
    4. LaTeX syntax            — check_latex.py
    5. Cite-pattern guards     — pytest tests/test_citation_patterns.py
    6. Bib DOI audit summary   — verify_bib_dois.py --summary
    7. Data audit freshness    — outputs/data_audit.json <30 days old
    8. Inline citation resolution — check_inline_citations.py

Usage:
    scripts/defense_check.py             # Run all checks, fail on any FAIL
    scripts/defense_check.py --verbose   # Print full output of each check
    scripts/defense_check.py --json      # JSON summary for CI / cron

Exit codes:
    0  — all checks pass
    1  — at least one check failed
    2  — at least one check errored (could not run)
"""

import argparse
import json
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
PYTEST = ".venv/bin/python -m pytest"

CHECKS = [
    {
        "name": "Citation resolution",
        "cmd": [".venv/bin/python", "scripts/check_citations.py", "--all"],
        "expect_zero_exit": True,
        "weight": "critical",
        "description": "All \\cite{} in paper.tex must resolve to master bib",
    },
    {
        "name": "Paper claims integrity",
        "cmd": [".venv/bin/python", "scripts/check_claims.py"],
        "expect_zero_exit": True,
        "weight": "critical",
        "description": "No specific claims (MAE < X, etc) without backing in ACTUAL_RESULTS.md",
    },
    {
        "name": "Ethics gates",
        "cmd": [".venv/bin/python", "scripts/check_ethics.py"],
        "expect_zero_exit": True,
        "weight": "critical",
        "description": "Each paper passes its ethics gate (FPIC, partnerships, etc.)",
    },
    {
        "name": "LaTeX syntax",
        "cmd": [".venv/bin/python", "scripts/check_latex.py"],
        "expect_zero_exit": True,
        "weight": "critical",
        "description": "All 6 papers compile clean (braces, citations, labels)",
    },
    {
        "name": "Cite-pattern regression",
        "cmd": [".venv/bin/python", "-m", "pytest", "tests/test_citation_patterns.py", "--no-cov", "-q"],
        "expect_zero_exit": True,
        "weight": "guard",
        "description": "No bare \\cite{}, every paper has \\section{Conclusion}",
    },
    {
        "name": "Bib DOI audit",
        "cmd": [".venv/bin/python", "scripts/verify_bib_dois.py", "--summary"],
        "expect_zero_exit": False,  # summary always returns 0
        "weight": "informational",
        "description": "Round-6 audit: 7 fixes applied, 76 false-positive confirmed",
    },
    {
        "name": "Inline citation resolution",
        "cmd": [".venv/bin/python", "scripts/check_inline_citations.py"],
        "expect_zero_exit": True,
        "weight": "critical",
        "description": "All (Author, Year) inline citations must resolve to master bib",
    },
    # ===== Tier-6 regression-protection layer =====
    # These tests encode the lessons from the 2026-09-07 Tier-6 deep review
    # (commits cb6363d, 27592fb, e8bd893). Each catches a class of bug that
    # the 7 critical checks above missed.
    {
        "name": "Numerical consistency regression",
        "cmd": [".venv/bin/python", "-m", "pytest", "tests/test_numerical_consistency.py", "--no-cov", "-q"],
        "expect_zero_exit": True,
        "weight": "critical",
        "description": "Tier-6 fix: stale numerical values from earlier drafts must not "
        "reappear in papers or thesis chapters",
    },
    {
        "name": "Input reference resolution",
        "cmd": [".venv/bin/python", "-m", "pytest", "tests/test_input_references.py", "--no-cov", "-q"],
        "expect_zero_exit": True,
        "weight": "critical",
        "description": "Tier-6 fix: every include directive in master tex must point to an existing file",
    },
    {
        "name": "LaTeX safety (compile-breakers)",
        "cmd": [".venv/bin/python", "-m", "pytest", "tests/test_latex_safety.py", "--no-cov", "-q"],
        "expect_zero_exit": True,
        "weight": "critical",
        "description": "Tier-6 fix: no unescaped percent inside command arguments, cite commands require natbib",
    },
    {
        "name": "Citation completeness",
        "cmd": [".venv/bin/python", "-m", "pytest", "tests/test_citation_completeness.py", "--no-cov", "-q"],
        "expect_zero_exit": True,
        "weight": "critical",
        "description": "Tier-6 fix: every \\cite{key} in paper.tex must have a bib entry (no [?] renders)",
    },
]

# Full pytest suite (only run with --full). Runs ~6 minutes.
# Excludes tests that require GEE/network/rasters — these are skipped by
# importorskip at the module level, but full mode still surfaces their
# state. The previous 3 rasterio failures are now properly skipped.
FULL_PYTEST_CMD = [
    ".venv/bin/python",
    "-m",
    "pytest",
    "tests/",
    "--no-cov",
    "-q",
    "--tb=no",
    # Skip slow integration + property-based + perf
    "--ignore=tests/test_performance.py",
    "--ignore=tests/test_integration.py",
    "--ignore=tests/test_properties.py",
    "--ignore=tests/test_property_based.py",
    "--ignore=tests/test_real_download.py",
    "--ignore=tests/test_real_download_gee.py",
    "--ignore=tests/test_thesis_satellite_tick.py",
    "--ignore=tests/test_thesis_sync_watchdog.py",
    "--ignore=tests/test_reproducibility.py",
]


def run_check(check, verbose=False):
    """Run a single check, return dict with status + duration."""
    started = time.time()
    cmd = check["cmd"]
    if verbose:
        print(f"\n{'=' * 70}")
        print(f"▶ {check['name']}")
        print(f"  command: {' '.join(cmd)}")
        print(f"  what: {check['description']}")
        print(f"{'=' * 70}")

    try:
        r = subprocess.run(
            cmd,
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True,
            timeout=600,
        )
        elapsed = time.time() - started
        status = "PASS" if r.returncode == 0 else ("FAIL" if check["expect_zero_exit"] else "PASS")
        result = {
            "name": check["name"],
            "status": status,
            "exit_code": r.returncode,
            "elapsed_seconds": round(elapsed, 1),
            "weight": check["weight"],
            "stdout_tail": (r.stdout or "")[-400:].strip(),
            "stderr_tail": (r.stderr or "")[-400:].strip(),
        }
    except subprocess.TimeoutExpired:
        result = {
            "name": check["name"],
            "status": "ERROR",
            "exit_code": -1,
            "elapsed_seconds": 600.0,
            "weight": check["weight"],
            "stderr_tail": "(timed out after 600s)",
        }
    except Exception as e:
        result = {
            "name": check["name"],
            "status": "ERROR",
            "exit_code": -2,
            "elapsed_seconds": 0.0,
            "weight": check["weight"],
            "stderr_tail": str(e),
        }

    if verbose:
        if result["status"] == "PASS":
            print(f"  ✓ PASS ({result['elapsed_seconds']}s)")
        else:
            print(f"  ✗ {result['status']} ({result['elapsed_seconds']}s)")
            if result.get("stderr_tail"):
                print(f"  stderr: {result['stderr_tail'][-300:]}")
            if result.get("stdout_tail"):
                print(f"  stdout: {result['stdout_tail'][-300:]}")

    return result


def check_data_audit_freshness():
    """Quick check: outputs/data_audit.json timestamp < 30 days old."""
    audit_path = REPO_ROOT / "outputs" / "data_audit.json"
    if not audit_path.exists():
        return {
            "name": "Data audit freshness",
            "status": "ERROR",
            "weight": "informational",
            "stderr_tail": "outputs/data_audit.json not found",
        }
    try:
        with open(audit_path) as f:
            data = json.load(f)
        ts_str = data.get("timestamp_utc", "")
        if not ts_str:
            return {
                "name": "Data audit freshness",
                "status": "WARN",
                "weight": "informational",
                "stderr_tail": "no timestamp_utc field",
            }
        ts = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
        age_days = (datetime.now(timezone.utc) - ts).days
        status = "PASS" if age_days < 30 else "WARN"
        msg = f"data audit is {age_days} days old (limit 30)"
        return {
            "name": "Data audit freshness",
            "status": status,
            "weight": "informational",
            "stdout_tail": msg,
            "elapsed_seconds": 0.0,
            "exit_code": 0,
        }
    except (json.JSONDecodeError, ValueError) as e:
        return {
            "name": "Data audit freshness",
            "status": "ERROR",
            "weight": "informational",
            "stderr_tail": f"could not parse data_audit: {e}",
        }


def print_summary_table(results):
    """Print a clean summary table at the end. Returns exit code (0 = ready, 1 = not ready)."""
    print(f"\n{'=' * 70}")
    print("DEFENSE CHECK SUMMARY")
    print(f"{'=' * 70}")
    print(f"{'Status':<8} {'Time':<8} {'Weight':<14} {'Check':<40}")
    print("-" * 70)
    for r in results:
        elapsed = f"{r['elapsed_seconds']:.1f}s" if r.get("elapsed_seconds") else "-"
        status_icon = {"PASS": "✓ PASS", "FAIL": "✗ FAIL", "WARN": "⚠ WARN", "ERROR": "✗ ERROR"}.get(
            r["status"], r["status"]
        )
        print(f"{status_icon:<8} {elapsed:<8} {r.get('weight', '-'):<14} {r['name']:<40}")
    print(f"{'=' * 70}")

    # Hard counts
    fail = sum(1 for r in results if r["status"] == "FAIL")
    err = sum(1 for r in results if r["status"] == "ERROR")
    warn = sum(1 for r in results if r["status"] == "WARN")
    passed = sum(1 for r in results if r["status"] == "PASS")
    print(f"Total: {passed} passed, {warn} warnings, {fail} failed, {err} errored")

    # Move banner BEFORE this so --json gets clean output
    if fail == 0 and err == 0:
        print("\n✓ DEFENSE READY — all critical checks passed")
        return 0
    else:
        print("\n✗ DEFENSE NOT READY — fix critical failures before submission")
        return 1


def main():
    parser = argparse.ArgumentParser(
        description="One command to verify defense-readiness of the thesis repo",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--verbose", action="store_true", help="Print full output of each check")
    parser.add_argument("--json", action="store_true", help="Emit JSON summary instead of human-readable output")
    parser.add_argument("--full", action="store_true", help="Also run full pytest suite (~6 min, 740+ tests)")
    args = parser.parse_args()

    if not args.json:
        print("Running 11 critical defense checks (7 base + 4 Tier-6 regression tests)...")
        if args.full:
            print("Plus full pytest suite (740+ tests, ~6 min)...")
        print("(For verbose output, run with --verbose)")

    results = []
    checks_to_run = list(CHECKS)
    if args.full:
        checks_to_run.append(
            {
                "name": "Full pytest suite",
                "cmd": FULL_PYTEST_CMD,
                "expect_zero_exit": True,
                "weight": "guard",
                "description": "All 740+ tests across 80 files (skips slow/integration)",
            }
        )
    for check in checks_to_run:
        results.append(run_check(check, verbose=args.verbose))
    # Add data audit freshness (cheap, no subprocess)
    results.append(check_data_audit_freshness())

    if args.json:
        # Pure JSON output (no banner) so scripts/CI can pipe to jq
        print(json.dumps(results, indent=2))
        any_critical_fail = any(
            r["status"] in ("FAIL", "ERROR") and r.get("weight") in ("critical", "guard") for r in results
        )
        return 1 if any_critical_fail else 0

    return print_summary_table(results)


if __name__ == "__main__":
    sys.exit(main())
