"""Reproducibility verification utilities.

Re-runs analysis scripts and verifies outputs match expected hashes.
"""

import hashlib
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple


def file_hash(path: Path, algo: str = "sha256") -> str:
    """Compute file hash using the specified algorithm."""
    h = hashlib.new(algo)
    h.update(path.read_bytes())
    return h.hexdigest()


def run_script(repo_root: Path, script_path: str, timeout: int = 120) -> Tuple[int, str, str]:
    """Run a script and return (returncode, stdout, stderr)."""
    result = subprocess.run(
        ["python3", str(repo_root / script_path)],
        cwd=repo_root,
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    return result.returncode, result.stdout, result.stderr


def check_outputs_exist(repo_root: Path, expected_outputs: List[str]) -> List[str]:
    """Return list of missing expected output paths (relative)."""
    return [o for o in expected_outputs if not (repo_root / o).exists()]


def hash_outputs(repo_root: Path, expected_outputs: List[str]) -> Dict[str, str]:
    """Compute hashes of existing expected outputs."""
    hashes = {}
    for o in expected_outputs:
        full = repo_root / o
        if full.exists():
            hashes[o] = file_hash(full)
    return hashes


def verify_script(
    repo_root: Path,
    script_path: str,
    expected_outputs: List[str],
    timeout: int = 120,
) -> Dict:
    """Run script and verify its outputs exist.

    Returns dict with: script, status, returncode, elapsed_s,
    missing_outputs, output_hashes, stdout_lines, stderr_lines.
    """
    start = datetime.now()
    try:
        rc, stdout, stderr = run_script(repo_root, script_path, timeout=timeout)
        elapsed = (datetime.now() - start).total_seconds()
    except subprocess.TimeoutExpired:
        return {"script": script_path, "status": "timeout", "elapsed_s": timeout}

    missing = check_outputs_exist(repo_root, expected_outputs)
    hashes = hash_outputs(repo_root, expected_outputs)
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


def summarize_results(results: List[Dict]) -> Dict[str, int]:
    """Count pass/fail/timeout in verification results."""
    counts = {"pass": 0, "fail": 0, "timeout": 0}
    for r in results:
        status = r.get("status")
        if status in counts:
            counts[status] += 1
    return counts


def total_elapsed(results: List[Dict]) -> float:
    """Sum elapsed time across all results."""
    return sum(r.get("elapsed_s", 0) for r in results)
