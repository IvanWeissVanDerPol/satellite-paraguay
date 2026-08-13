"""Capture dashboard screenshots for portfolio.

Streamlit dashboard has 7 pages + sidebar. This walks each page,
takes a screenshot at 1600x900, and saves to outputs/screenshots/.

Usage: while streamlit is running on :8501
   python3 scripts/capture_dashboard_screenshots.py
"""

import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

REPO_ROOT = Path(__file__).parent.parent
OUT_DIR = REPO_ROOT / "outputs/screenshots"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def main():
    print("=" * 70)
    print("DASHBOARD SCREENSHOTS")
    print("=" * 70)
    print(f"\n  Output dir: {OUT_DIR}")

    print("\n[1/2] Streamlit is expected to be running at http://localhost:8501")
    import urllib.request

    try:
        response = urllib.request.urlopen("http://localhost:8501/_stcore/health", timeout=5)
        if response.status == 200:
            print("  OK Streamlit is healthy")
        else:
            print(f"  WARN Streamlit returned status {response.status}")
    except Exception as e:
        print(f"  FAIL Streamlit not reachable: {e}")
        print("    Start it: python3 -m streamlit run src/dashboard/app.py")
        return

    print("\n[2/2] Capturing screenshots...")
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as e:
        print(f"  FAIL playwright not installed: {e}")
        print("    pip install playwright && playwright install chromium")
        return

    pages = [
        ("01_overview.png", "Overview"),
        ("02_departments.png", "Departments"),
        ("03_indigenous.png", "Indigenous Territories"),
        ("04_carbon.png", "Carbon & Verra"),
        ("05_models.png", "Models"),
        ("06_uncertainty.png", "Uncertainty"),
        ("07_references.png", "References"),
    ]

    results = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])

        for slug, label in pages:
            page = browser.new_context(viewport={"width": 1600, "height": 900}).new_page()
            try:
                page.goto("http://localhost:8501/", wait_until="domcontentloaded", timeout=30000)
                time.sleep(4)
                # Click sidebar radio button for this page
                radio = page.locator(f'label:has-text("{label}")').first
                radio.click(timeout=5000)
                time.sleep(3)
                # Take screenshot
                filename = OUT_DIR / slug
                page.screenshot(path=str(filename), full_page=False)
                size = filename.stat().st_size
                results.append(
                    {
                        "page": label,
                        "file": str(filename.relative_to(REPO_ROOT)),
                        "size_bytes": size,
                        "status": "ok",
                    }
                )
                print(f"  OK {label}: {size:,} bytes")
            except Exception as e:
                print(f"  FAIL {label}: {str(e)[:80]}")
                results.append({"page": label, "status": "error", "error": str(e)})
            finally:
                page.close()

        browser.close()

    # Save index
    index_path = OUT_DIR / "index.json"
    index_path.write_text(
        json.dumps(
            {
                "captured_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                "results": results,
            },
            indent=2,
        )
    )

    n_ok = sum(1 for r in results if r["status"] == "ok")
    print(f"\n  Summary: {n_ok}/{len(results)} captured")
    print(f"  Index: {index_path.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
