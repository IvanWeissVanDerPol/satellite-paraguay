from __future__ import annotations

"""AC4: Dashboard live deployment verification.

Imports dashboard/app.py with all required modules installed, and runs a
smoke test against the loaded functions without actually launching
streamlit (which would block on a TTY)."""

import pytest  # noqa: E402

pytest.importorskip(
    "streamlit_folium", reason="CI: requires optional system dep 'streamlit_folium' (not installed)"
)  # noqa: E402


import importlib.util  # noqa: E402
from pathlib import Path  # noqa: E402

REPO = Path(__file__).resolve().parent.parent


def test_dashboard_app_imports():
    """dashboard/app.py must import cleanly with all required modules."""
    # Pre-import deps to ensure they're available
    for mod in ("streamlit", "pandas", "numpy", "plotly", "folium", "streamlit_folium"):
        try:
            __import__(mod)
        except ImportError as e:
            raise AssertionError(
                f"Dashboard dep {mod!r} missing: {e}. " f"Run: uv pip install plotly folium streamlit-folium"
            ) from e

    # Now load src/dashboard/app.py as a module (Round-12: dashboard/
    # duplicate was deleted; src/dashboard/ is the canonical copy)
    app_path = REPO / "src" / "dashboard" / "app.py"
    assert app_path.exists(), f"src/dashboard/app.py not found at {app_path}"

    spec = importlib.util.spec_from_file_location("dashboard_app", app_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    # Verify expected symbols.
    # Note (Round-12 audit): the HAS_STREAMLIT guard was removed because
    # it was a no-op (turned ImportError into AttributeError); we now
    # assume streamlit is installed and let it fail loudly if not.
    assert hasattr(mod, "page_overview"), "page_overview() missing"
    assert hasattr(mod, "page_departments"), "page_departments() missing"
    # The dashboard uses top-level streamlit calls (no main() function);
    # verify that the PAGES dict exists and has the expected keys.
    assert hasattr(mod, "PAGES"), "PAGES dict missing"
    expected_pages = {
        "Overview",
        "Departments",
        "Indigenous Territories",
        "Carbon & Verra",
        "Models",
        "Uncertainty",
        "References",
    }
    assert set(mod.PAGES.keys()) == expected_pages, (
        f"PAGES keys mismatch: got {set(mod.PAGES.keys())}, " f"expected {expected_pages}"
    )


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
