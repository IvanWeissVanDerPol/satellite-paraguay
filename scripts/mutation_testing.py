"""Mutation testing for satellite-paraguay using mutmut.

Mutation testing evaluates test quality by introducing small mutations
to source code and verifying tests catch them.

Run: mutmut run --target scripts/per_pixel_carbon.py --tests-dir tests/

This is a wrapper to make mutation testing easy to run.
"""
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent


def check_mutmut():
    """Check if mutmut is installed."""
    try:
        result = subprocess.run(["mutmut", "--version"], capture_output=True, text=True, timeout=5)
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def run_mutmut(target: str, tests_dir: str = "tests/", timeout: int = 600):
    """Run mutmut on a target file."""
    print(f"\nRunning mutmut on {target}...")

    if not check_mutmut():
        print("  ⚠ mutmut not installed. Install with: pip install mutmut")
        return False

    cmd = [
        "mutmut",
        "run",
        f"--target={target}",
        f"--tests-dir={tests_dir}",
        "--runner=python -m pytest tests/test_per_pixel_carbon.py --no-cov -x -q",
        f"--timeout={timeout}",
    ]

    result = subprocess.run(cmd, cwd=REPO_ROOT)
    return result.returncode == 0


def main():
    print("=" * 70)
    print("MUTATION TESTING")
    print("=" * 70)

    targets = [
        "scripts/per_pixel_carbon.py",
        "scripts/uncertainty_quantification.py",
        "scripts/statistical_tests.py",
    ]

    print(f"\nTargets to mutate: {len(targets)}")
    for t in targets:
        print(f"  - {t}")

    print(f"\nMutation testing introduces small code changes and verifies")
    print(f"that tests catch them. A low mutation score means tests are weak.")

    if not check_mutmut():
        print(f"\n  ⚠ mutmut not installed.")
        print(f"  Install with: pip install mutmut")
        print(f"  Then run: mutmut run --target=scripts/per_pixel_carbon.py")

    print(f"\nQuick start:")
    print(f"  pip install mutmut")
    print(f"  mutmut run --target=scripts/per_pixel_carbon.py \\")
    print(f"           --runner='python -m pytest tests/test_per_pixel_carbon.py --no-cov -x'")

    print(f"\nExpected results:")
    print(f"  - Mutation score > 70%: Good test coverage")
    print(f"  - Mutation score 50-70%: Adequate, can be improved")
    print(f"  - Mutation score < 50%: Tests need strengthening")

    # Try to run if mutmut is available
    if check_mutmut():
        for target in targets[:1]:  # Just run on the first one as demo
            print(f"\n--- Demo run on {target} ---")
            run_mutmut(target)


if __name__ == "__main__":
    main()
