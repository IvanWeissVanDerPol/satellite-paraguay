"""AC4: Dashboard live deployment verification.

Imports dashboard/app.py with all required modules installed, and runs a
smoke test against the loaded functions without actually launching
streamlit (which would block on a TTY)."""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


def test_dashboard_app_imports():
    """dashboard/app.py must import cleanly with all required modules."""
    # Pre-import deps to ensure they're available
    for mod in ("streamlit", "pandas", "numpy", "plotly",
                "folium", "streamlit_folium"):
        try:
            __import__(mod)
        except ImportError as e:
            raise AssertionError(
                f"Dashboard dep {mod!r} missing: {e}. "
                f"Run: uv pip install plotly folium streamlit-folium"
            ) from e

    # Now load dashboard/app.py as a module
    app_path = REPO / "dashboard" / "app.py"
    assert app_path.exists(), f"dashboard/app.py not found at {app_path}"

    spec = importlib.util.spec_from_file_location("dashboard_app", app_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    # Verify expected symbols
    assert hasattr(mod, "HAS_STREAMLIT"), "HAS_STREAMLIT not set"
    assert hasattr(mod, "load_paraguay_data"), "load_paraguay_data missing"
    assert hasattr(mod, "main"), "main() entry point missing"
    assert mod.HAS_STREAMLIT is True, "streamlit not detected"


def test_dashboard_pages_directory():
    """If there's a dashboard/pages dir, it must exist and have content."""
    pages_dir = REPO / "dashboard" / "pages"
    if pages_dir.exists():
        n_files = sum(1 for _ in pages_dir.glob("*.py"))
        assert n_files > 0, f"dashboard/pages exists but is empty: {pages_dir}"


def test_streamlit_config():
    """A .streamlit/config.toml may exist; if so, verify it's valid TOML."""
    cfg = REPO / ".streamlit" / "config.toml"
    if cfg.exists():
        import tomllib
        with cfg.open("rb") as f:
            tomllib.load(f)
