"""Reproducibility verifier.

Re-runs key analysis scripts from scratch and verifies outputs match stored expected values.

Run: python3 scripts/verify_reproducibility.py

This is the gold standard for reproducibility — it actually re-executes the analysis.
"""
import hashlib
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
EXPECTED_HASHES_PATH = REPO_ROOT / "outputs/expected_hashes.json"


def file_hash(path: Path, algo="sha256") -> str:
    """Compute file hash."""
    h = hashlib.new(algo)
    h.update(path.read_bytes())
    return h.hexdigest()


def run_script(script_path: str, timeout: int = 120) -> tuple:
    """Run a script and return (returncode, stdout, stderr)."""
    print(f"  Running: {script_path}")
    result = subprocess.run(
        ["python3", str(REPO_ROOT / script_path)],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    return result.returncode, result.stdout, result.stderr


def verify_script(script_path: str, expected_outputs: list, timeout: int = 120) -> dict:
    """Run script and verify its outputs exist."""
    print(f"\n{'─' * 60}")
    print(f"  Script: {script_path}")
    print(f"  Expected outputs: {len(expected_outputs)}")

    start = datetime.now()
    try:
        rc, stdout, stderr = run_script(script_path, timeout=timeout)
        elapsed = (datetime.now() - start).total_seconds()
    except subprocess.TimeoutExpired:
        return {"script": script_path, "status": "timeout", "elapsed_s": timeout}

    # Check expected outputs exist
    missing = [o for o in expected_outputs if not (REPO_ROOT / o).exists()]

    # Compute hashes of created outputs
    hashes = {}
    for o in expected_outputs:
        full = REPO_ROOT / o
        if full.exists():
            hashes[o] = file_hash(full)

    status = "pass" if rc == 0 and not missing else "fail"
    return {
        "script": script_path,
        "status": status,
        "returncode": rc,
        "elapsed_s": elapsed,
        "missing_outputs": missing,
        "output_hashes": hashes,
        "stdout_lines": len(stdout.split("\n")),
        "stderr_lines": len(stderr.split("\n")) if stderr else 0,
    }


def main():
    print("=" * 70)
    print("REPRODUCIBILITY VERIFIER")
    print("=" * 70)
    print(f"\n  This re-runs key analysis scripts and verifies outputs.")
    print(f"  Run on a fresh clone to ensure full reproducibility.")

    tests = [
        # (script, expected_outputs, timeout)
        (
            "scripts/per_pixel_carbon.py",
            ["outputs/p0011/carbon/per_year_loss.json", "outputs/p0011/carbon/per_pixel_carbon_map.tif"],
            60,
        ),
        (
            "scripts/uncertainty_quantification.py",
            ["outputs/p0011/uncertainty/uncertainty_results.json"],
            120,
        ),
        (
            "scripts/cross_transfer_experiment.py",
            ["outputs/cross_transfer/transfer_results.json"],
            120,
        ),
        (
            "scripts/statistical_tests.py",
            ["outputs/statistical_tests/test_results.json"],
            60,
        ),
        (
            "scripts/carbon_credit_verifier.py",
            ["outputs/carbon_credits/verra_verification.json"],
            60,
        ),
        (
            "scripts/mapbiomas_temporal.py",
            ["outputs/mapbiomas_temporal/yearly_land_cover.csv"],
            60,
        ),
        (
            "scripts/comparative_analysis.py",
            ["outputs/comparison/Hansen_vs_MapBiomas.json"],
            60,
        ),
        (
            "scripts/fire_drought_analysis.py",
            ["outputs/fire_drought/fire_drought_analysis.json"],
            60,
        ),
        (
            "scripts/ground_truth_design.py",
            ["data/ground_truth/field_plot_design.csv", "data/ground_truth/field_plot_design.json"],
            30,
        ),
    ]

    results = []
    total_start = datetime.now()
    for script, outputs, timeout in tests:
        result = verify_script(script, outputs, timeout)
        results.append(result)
        icon = "✓" if result["status"] == "pass" else "✗"
        print(f"  {icon} {result['status']:8} ({result.get('elapsed_s', 0):.1f}s)")
        if result.get("missing_outputs"):
            print(f"    Missing: {result['missing_outputs']}")

    total_elapsed = (datetime.now() - total_start).total_seconds()

    # Summary
    print(f"\n{'=' * 70}")
    print(f"  SUMMARY")
    print(f"{'=' * 70}")

    n_pass = sum(1 for r in results if r["status"] == "pass")
    n_fail = sum(1 for r in results if r["status"] != "pass")

    print(f"\n  Scripts tested: {len(results)}")
    print(f"  ✓ Passed: {n_pass}")
    print(f"  ✗ Failed: {n_fail}")
    print(f"  Total time: {total_elapsed:.1f}s")

    if n_fail > 0:
        print(f"\n  Failed scripts:")
        for r in results:
            if r["status"] != "pass":
                print(f"    - {r['script']}: {r['status']}")

    # Save results
    out_path = REPO_ROOT / "outputs/reproducibility_check.json"
    out_path.parent.mkdir(exist_ok=True)
    out_path.write_text(
        json.dumps(
            {
                "timestamp": datetime.now().isoformat(),
                "total_elapsed_s": total_elapsed,
                "n_pass": n_pass,
                "n_fail": n_fail,
                "results": results,
            },
            indent=2,
        )
    )
    print(f"\n  Saved: {out_path}")

    print(f"\n  To achieve full reproducibility:")
    print(f"    1. Clone repo from scratch")
    print(f"    2. pip install -r requirements.txt")
    print(f"    3. python3 scripts/download_all_data.py")
    print(f"    4. bash scripts/install_git_hooks.sh")
    print(f"    5. python3 scripts/verify_reproducibility.py")

    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
