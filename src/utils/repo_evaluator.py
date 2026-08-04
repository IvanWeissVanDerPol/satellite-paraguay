"""Repository evaluation utilities.

Counts files, lines of code, tests, and analyzes module stub status.
"""
import ast
from pathlib import Path
from typing import Any, Dict, List

EXCLUDED_DIRS = (".git", ".dvc", "__pycache__", "node_modules", "mlruns")

STUB_PATTERNS = ["pass  # TODO", "raise NotImplementedError", "TODO", "FIXME"]


def count_files_by_type(root: Path) -> Dict[str, int]:
    """Count files by extension type."""
    counts = {
        "total": 0,
        "python": 0,
        "markdown": 0,
        "yaml": 0,
        "notebook": 0,
        "weights": 0,
        "image": 0,
        "html": 0,
    }
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        if any(excluded in p.parts for excluded in EXCLUDED_DIRS):
            continue
        counts["total"] += 1
        suffix = p.suffix.lower()
        if suffix == ".py":
            counts["python"] += 1
        elif suffix == ".md":
            counts["markdown"] += 1
        elif suffix in (".yaml", ".yml"):
            counts["yaml"] += 1
        elif suffix == ".ipynb":
            counts["notebook"] += 1
        elif suffix in (".pt", ".pth"):
            counts["weights"] += 1
        elif suffix in (".png", ".jpg", ".gif", ".jpeg"):
            counts["image"] += 1
        elif suffix == ".html":
            counts["html"] += 1
    return counts


def count_loc(root: Path) -> int:
    """Count non-blank, non-comment lines of Python code."""
    total = 0
    for p in root.rglob("*.py"):
        if any(excluded in p.parts for excluded in EXCLUDED_DIRS):
            continue
        try:
            with p.open() as f:
                for line in f:
                    stripped = line.strip()
                    if stripped and not stripped.startswith("#"):
                        total += 1
        except (OSError, UnicodeDecodeError):
            pass
    return total


def count_test_files(test_dir: Path) -> List[Path]:
    """Return list of test files matching test_*.py pattern."""
    if not test_dir.exists():
        return []
    return list(test_dir.glob("test_*.py"))


def is_module_stub(content: str) -> bool:
    """Check if module content matches stub patterns."""
    for pattern in STUB_PATTERNS:
        if pattern in content:
            return True
    return False


def extract_signatures(content: str, max_signatures: int = 10) -> List[str]:
    """Extract class and function signatures from Python code."""
    signatures: List[str] = []
    try:
        tree = ast.parse(content)
        classes = [n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]
        functions = [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
        for cls in classes:
            signatures.append(f"class {cls.name}")
        for fn in functions:
            if not fn.name.startswith("_"):
                signatures.append(f"def {fn.name}")
    except SyntaxError:
        pass
    return signatures[:max_signatures]


def analyze_module(py_file: Path, src_dir: Path) -> Dict[str, Any]:
    """Analyze a single module for stub status and signatures."""
    try:
        content = py_file.read_text()
    except (OSError, UnicodeDecodeError):
        return None

    is_stub = is_module_stub(content)
    signatures = extract_signatures(content)

    # Count LOC
    loc = sum(
        1
        for line in content.split("\n")
        if line.strip() and not line.strip().startswith("#")
    )

    # Count classes/functions
    try:
        tree = ast.parse(content)
        n_classes = sum(1 for n in ast.walk(tree) if isinstance(n, ast.ClassDef))
        n_functions = sum(1 for n in ast.walk(tree) if isinstance(n, ast.FunctionDef))
    except SyntaxError:
        n_classes = 0
        n_functions = 0

    return {
        "path": str(py_file.relative_to(src_dir)),
        "loc": loc,
        "n_classes": n_classes,
        "n_functions": n_functions,
        "is_stub": is_stub,
        "signatures": signatures,
    }


def analyze_modules(src_dir: Path) -> List[Dict[str, Any]]:
    """Analyze all Python modules in src_dir."""
    modules = []
    for py_file in src_dir.rglob("*.py"):
        if any(excluded in py_file.parts for excluded in EXCLUDED_DIRS):
            continue
        if py_file.name == "__init__.py":
            continue
        result = analyze_module(py_file, src_dir)
        if result is not None:
            modules.append(result)
    return modules


def count_real_vs_stub(modules: List[Dict[str, Any]]) -> Dict[str, int]:
    """Count real (non-stub) and stub modules."""
    real = sum(1 for m in modules if not m["is_stub"])
    stub = sum(1 for m in modules if m["is_stub"])
    return {"real": real, "stub": stub, "total": len(modules)}


def total_loc_by_status(modules: List[Dict[str, Any]]) -> Dict[str, int]:
    """Sum LOC for real vs stub modules."""
    real_loc = sum(m["loc"] for m in modules if not m["is_stub"])
    stub_loc = sum(m["loc"] for m in modules if m["is_stub"])
    return {"real": real_loc, "stub": stub_loc, "total": real_loc + stub_loc}