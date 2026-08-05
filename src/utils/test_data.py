"""Test data versioning utilities.

Content-addressable storage (CAS) for test fixtures using SHA256.
"""
import hashlib
import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any, Dict


def compute_hash(path: Path, algo: str = "sha256") -> str:
    """Compute hash of file using specified algorithm."""
    h = hashlib.new(algo)
    h.update(path.read_bytes())
    return h.hexdigest()


def index_directory(directory: Path) -> Dict[str, Dict[str, Any]]:
    """Index all files in directory with hashes.

    Returns dict mapping relative_path -> {hash_sha256, size_bytes, modified}.
    """
    if not directory.exists():
        return {}
    index: Dict[str, Dict[str, Any]] = {}
    for f in directory.rglob("*"):
        if f.is_file():
            rel = str(f.relative_to(directory))
            index[rel] = {
                "hash_sha256": compute_hash(f),
                "size_bytes": f.stat().st_size,
                "modified": datetime.fromtimestamp(f.stat().st_mtime).isoformat(),
            }
    return index


def save_index(index: Dict[str, Dict[str, Any]], index_path: Path) -> None:
    """Save test data index to disk."""
    index_path.parent.mkdir(parents=True, exist_ok=True)
    index_path.write_text(
        json.dumps(
            {
                "version": "1.0",
                "created": datetime.now().isoformat(),
                "files": index,
            },
            indent=2,
        )
    )


def verify_against_index(
    data_dir: Path, index_path: Path
) -> Dict[str, Dict[str, Any]]:
    """Verify current files match stored index.

    Returns dict mapping rel_path -> {status, expected, actual}.
    Status: 'match', 'modified', 'missing'.
    """
    if not index_path.exists():
        return {}
    expected = json.loads(index_path.read_text()).get("files", {})
    results: Dict[str, Dict[str, Any]] = {}
    for rel, info in expected.items():
        full = data_dir / rel
        if not full.exists():
            results[rel] = {"status": "missing"}
            continue
        actual_hash = compute_hash(full)
        expected_hash = info["hash_sha256"]
        results[rel] = {
            "status": "match" if actual_hash == expected_hash else "modified",
            "expected": expected_hash,
            "actual": actual_hash,
        }
    return results


def summarize_verification(results: Dict[str, Dict[str, Any]]) -> Dict[str, int]:
    """Count match/modified/missing in verification results."""
    summary = {"match": 0, "modified": 0, "missing": 0}
    for r in results.values():
        status = r.get("status")
        if status in summary:
            summary[status] += 1
    return summary


def copy_to_test_data(source: Path, data_dir: Path) -> Path:
    """Copy a file into the test data directory."""
    data_dir.mkdir(parents=True, exist_ok=True)
    target = data_dir / source.name
    shutil.copy(source, target)
    return target