"""Real evaluation of the satellite-paraguay repo.

Produces STATS.md with actual metrics:
- File counts
- LOC counts
- Test coverage
- Real working modules
- Stub modules
- Fabricated vs measured metrics
"""

import ast
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))


def count_files(root):
    """Count files by type."""
    counts = {
        "total": 0,
        "python": 0,
        "markdown": 0,
        "yaml": 0,
        "tensorboard": 0,
        "notebook": 0,
        "weights": 0,
        "image": 0,
        "html": 0,
    }
    for p in Path(root).rglob("*"):
        if not p.is_file():
            continue
        if ".git" in p.parts or ".dvc" in p.parts:
            continue
        counts["total"] += 1
        if p.suffix == ".py":
            counts["python"] += 1
        elif p.suffix == ".md":
            counts["markdown"] += 1
        elif p.suffix in (".yaml", ".yml"):
            counts["yaml"] += 1
        elif p.suffix == ".ipynb":
            counts["notebook"] += 1
        elif p.suffix in (".pt", ".pth"):
            counts["weights"] += 1
        elif p.suffix in (".png", ".jpg", ".gif"):
            counts["image"] += 1
        elif p.suffix == ".html":
            counts["html"] += 1
    return counts


def count_loc(root):
    """Count lines of Python code."""
    total = 0
    for p in Path(root).rglob("*.py"):
        if ".git" in p.parts:
            continue
        try:
            total += sum(1 for line in p.open() if line.strip() and not line.strip().startswith("#"))
        except BaseException:
            pass
    return total


def count_tests():
    """Count test files."""
    test_dir = Path("str(REPO)/tests")
    return list(test_dir.glob("test_*.py"))


def analyze_modules():
    """Analyze each module for actual vs stub status."""
    modules = []
    src_dir = Path("str(REPO)/src")
    for py_file in src_dir.rglob("*.py"):
        if ".git" in py_file.parts or "__pycache__" in py_file.parts:
            continue
        if py_file.name == "__init__.py":
            continue
        try:
            content = py_file.read_text()
        except BaseException:
            continue

        # Check if has stub patterns
        is_stub = False
        signatures = []
        stub_patterns = ["pass  # TODO", "raise NotImplementedError", "TODO", "FIXME"]

        for pattern in stub_patterns:
            if pattern in content:
                is_stub = True
                break

        # Count actual functions/classes
        classes = []
        functions = []
        try:
            tree = ast.parse(content)
            classes = [n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]
            functions = [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
            for cls in classes:
                signatures.append(f"class {cls.name}")
            for fn in functions:
                if not fn.name.startswith("_"):
                    signatures.append(f"def {fn.name}")
        except BaseException:
            pass

        loc = sum(1 for line in content.split("\n") if line.strip() and not line.strip().startswith("#"))

        modules.append(
            {
                "path": str(py_file.relative_to(src_dir)),
                "loc": loc,
                "n_classes": len(classes),
                "n_functions": len(functions),
                "is_stub": is_stub,
                "signatures": signatures[:10],
            }
        )
    return modules


def main():
    print("=" * 70)
    print("SatelliteCV-Paraguay — Real Repo Evaluation")
    print("=" * 70)

    repo = Path(str(Path(__file__).resolve().parent.parent))

    # File counts
    counts = count_files(repo)
    print("\nFiles:")
    for k, v in counts.items():
        if v > 0:
            print(f"  {k:12s}: {v}")

    # LOC
    loc = count_loc(repo)
    print(f"\nLines of Python code (non-empty, non-comment): {loc}")

    # Tests
    tests = count_tests()
    print(f"\nTest files: {len(tests)}")
    for t in tests:
        print(f"  - {t.name}")

    # Module analysis
    print("\nModule analysis (real work vs stub):")
    modules = analyze_modules()
    stubs = [m for m in modules if m["is_stub"]]
    real = [m for m in modules if not m["is_stub"]]
    print(f"  Real modules: {len(real)}")
    print(f"  Stub modules: {len(stubs)}")

    # Save
    output = {
        "file_counts": counts,
        "python_loc": loc,
        "n_test_files": len(tests),
        "n_modules": len(modules),
        "n_real_modules": len(real),
        "n_stub_modules": len(stubs),
        "modules": modules,
    }
    (repo / "outputs" / "repo_evaluation.json").write_text(json.dumps(output, indent=2))

    # Markdown report
    md_path = repo / "outputs" / "REPO_EVALUATION.md"
    with open(md_path, "w") as f:
        f.write("# SatelliteCV-Paraguay — Real Repo Evaluation\n\n")
        f.write(f"**Generated:** {Path.cwd()}\n\n")
        f.write("## File counts\n\n")
        for k, v in counts.items():
            if v > 0:
                f.write(f"- **{k}:** {v}\n")
        f.write("\n## Code metrics\n\n")
        f.write(f"- **Python LOC** (non-empty, non-comment): **{loc}**\n")
        f.write(f"- **Test files:** {len(tests)}\n")
        f.write("\n## Module analysis\n\n")
        f.write(f"- **Real modules** (no TODO/stub markers): {len(real)}\n")
        f.write(f"- **Stub modules** (contains TODO/NotImplementedError): {len(stubs)}\n")
        f.write("\n## What's actually working\n\n")
        for m in real[:20]:
            f.write(f"- `{m['path']}` ({m['loc']} LOC, {m['n_classes']} classes, {m['n_functions']} funcs)\n")
        if len(real) > 20:
            f.write(f"- ... and {len(real) - 20} more\n")
        f.write("\n## What's stub\n\n")
        for m in stubs[:20]:
            f.write(f"- `{m['path']}` ({m['loc']} LOC)\n")
        if len(stubs) > 20:
            f.write(f"- ... and {len(stubs) - 20} more\n")
    print(f"\nReport saved to {md_path}")


if __name__ == "__main__":
    main()
