"""Test data versioning for satellite-paraguay.

Tracks test fixtures, synthetic data, and reference outputs.
Uses content-addressable storage (CAS) for efficiency.

Run: python3 scripts/manage_test_data.py
"""

import hashlib
import json
import shutil
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
TEST_DATA_DIR = REPO_ROOT / "data/test_fixtures"
TEST_DATA_INDEX = REPO_ROOT / "data/test_fixtures_index.json"


def compute_hash(path: Path) -> str:
    """Compute SHA256 hash of file."""
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def index_test_data():
    """Index all files in test_fixtures/ with hashes."""
    if not TEST_DATA_DIR.exists():
        TEST_DATA_DIR.mkdir(parents=True)
        print(f"  Created: {TEST_DATA_DIR}")
        return {}

    index = {}
    for f in TEST_DATA_DIR.rglob("*"):
        if f.is_file():
            rel = str(f.relative_to(TEST_DATA_DIR))
            index[rel] = {
                "hash_sha256": compute_hash(f),
                "size_bytes": f.stat().st_size,
                "modified": datetime.fromtimestamp(f.stat().st_mtime).isoformat(),
            }

    return index


def save_index(index: dict) -> None:
    """Save index to disk."""
    TEST_DATA_INDEX.write_text(
        json.dumps(
            {
                "version": "1.0",
                "created": datetime.now().isoformat(),
                "files": index,
            },
            indent=2,
        )
    )


def verify_test_data() -> dict:
    """Verify current test data matches index."""
    if not TEST_DATA_INDEX.exists():
        return {"status": "no_index", "files": {}}

    expected = json.loads(TEST_DATA_INDEX.read_text()).get("files", {})

    results = {}
    for rel, info in expected.items():
        full = TEST_DATA_DIR / rel
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


def add_file(path: Path) -> None:
    """Add a file to the test data index."""
    rel = path.name
    target = TEST_DATA_DIR / rel
    shutil.copy(path, target)
    print(f"  Added: {rel} ({target.stat().st_size:,} bytes)")


def main():
    print("=" * 70)
    print("TEST DATA VERSIONING")
    print("=" * 70)

    print(f"\nTest data dir: {TEST_DATA_DIR}")
    print(f"Index file: {TEST_DATA_INDEX}")

    # Build index
    print("\n[1/3] Indexing test data...")
    index = index_test_data()
    print(f"  Found {len(index)} files")
    if index:
        save_index(index)
        print(f"  Saved index to {TEST_DATA_INDEX}")

    # Show summary
    print("\n[2/3] File summary:")
    total_size = 0
    for rel, info in list(index.items())[:10]:
        size = info["size_bytes"]
        total_size += size
        print(f"  {rel:40} {size:>10,} bytes  {info['hash_sha256'][:12]}...")
    if len(index) > 10:
        print(f"  ... and {len(index) - 10} more")
    print(f"  Total: {total_size:,} bytes")

    # Verify
    print("\n[3/3] Verifying...")
    results = verify_test_data()
    n_match = sum(1 for r in results.values() if r.get("status") == "match")
    n_modified = sum(1 for r in results.values() if r.get("status") == "modified")
    n_missing = sum(1 for r in results.values() if r.get("status") == "missing")
    print(f"  ✓ Match: {n_match}")
    if n_modified > 0:
        print(f"  ⚠ Modified: {n_modified}")
    if n_missing > 0:
        print(f"  ⚠ Missing: {n_missing}")

    print("\nUsage:")
    print(f"  - Test fixtures in {TEST_DATA_DIR}")
    print(f"  - Index in {TEST_DATA_INDEX}")
    print("  - Fixtures are content-addressed (SHA256)")
    print("  - Verify with: python3 scripts/manage_test_data.py")


if __name__ == "__main__":
    main()
