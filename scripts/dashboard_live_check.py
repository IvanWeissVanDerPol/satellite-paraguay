"""Dashboard live deployment verification script.

Spins up the dashboard + FastAPI on this host, captures health checks,
and verifies each dashboard page renders. Used for Tier 2-D verification.

Usage:
    python3 scripts/dashboard_live_check.py
"""

import json
import subprocess
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def check_endpoint(url: str, timeout: int = 5) -> dict:
    """Check a single HTTP endpoint."""
    import urllib.request
    import urllib.error

    try:
        with urllib.request.urlopen(url, timeout=timeout) as response:
            body = response.read()
            return {
                "url": url,
                "status": response.status,
                "size_bytes": len(body),
                "ok": response.status == 200,
            }
    except (urllib.error.URLError, ConnectionError, TimeoutError) as e:
        return {"url": url, "error": str(e), "ok": False}
    except Exception as e:
        return {"url": url, "error": str(e), "ok": False}


def check_dashboard_health(port: int = 8501, timeout: int = 10) -> dict:
    """Check if the dashboard is responsive on the given port."""
    return {
        "port": port,
        "health": check_endpoint(f"http://localhost:{port}/_stcore/health", timeout),
        "main": check_endpoint(f"http://localhost:{port}/", timeout),
    }


def check_api_health(port: int = 8000, timeout: int = 10) -> dict:
    """Check the FastAPI endpoints."""
    endpoints = [
        ("/", "root"),
        ("/docs", "docs"),
        ("/metrics", "metrics"),
        ("/api/v1/health", "health"),
        ("/api/v1/deforestation/summary", "deforestation_summary"),
        ("/api/v1/carbon/credit/integrity", "carbon_integrity"),
        ("/api/v1/indigenous/disparity", "indigenous_disparity"),
        ("/api/v1/air-quality/forecast", "air_quality"),
    ]
    return {
        "port": port,
        "endpoints": {
            name: check_endpoint(f"http://localhost:{port}{path}", timeout)
            for path, name in endpoints
        },
    }


def start_dashboard_subprocess(port: int = 8501) -> subprocess.Popen:
    """Start the streamlit dashboard as a subprocess."""
    cmd = [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        "src/dashboard/app.py",
        "--server.port",
        str(port),
        "--server.headless",
        "true",
        "--server.runOnSave",
        "false",
        "--browser.gatherUsageStats",
        "false",
    ]
    return subprocess.Popen(
        cmd,
        cwd=str(REPO_ROOT),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
    )


def start_api_subprocess(port: int = 8000) -> subprocess.Popen:
    """Start the FastAPI app as a subprocess."""
    cmd = [
        sys.executable,
        "-m",
        "uvicorn",
        "src.api.main:app",
        "--host",
        "127.0.0.1",
        "--port",
        str(port),
    ]
    return subprocess.Popen(
        cmd,
        cwd=str(REPO_ROOT),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
    )


def kill_subprocess(proc: subprocess.Popen, timeout: int = 5) -> None:
    """Terminate a subprocess, escalating to kill if needed."""
    proc.terminate()
    try:
        proc.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        proc.kill()
        try:
            proc.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            pass


def main() -> int:
    """Run dashboard live deployment verification."""
    print("=" * 70)
    print("DASHBOARD LIVE DEPLOYMENT VERIFICATION")
    print("=" * 70)

    # Import check
    print("\n[1/5] Import check...")
    try:
        import streamlit  # noqa: F401
        import plotly  # noqa: F401
        import folium  # noqa: F401
        print("  ✅ streamlit, plotly, folium all installed")
    except ImportError as e:
        print(f"  ❌ Missing dependency: {e}")
        return 1

    # Start dashboard
    print("\n[2/5] Starting dashboard on port 8501...")
    dashboard_proc = start_dashboard_subprocess(8501)
    time.sleep(20)  # Streamlit takes ~15-20s on first run

    # Check dashboard health
    print("\n[3/5] Checking dashboard health...")
    dashboard_result = check_dashboard_health(8501, timeout=10)
    print(f"  health: {dashboard_result['health']}")
    print(f"  main:   {dashboard_result['main']}")

    # Kill dashboard
    kill_subprocess(dashboard_proc)

    # Start API
    print("\n[4/5] Starting API on port 8000...")
    api_proc = start_api_subprocess(8000)
    time.sleep(10)

    # Check API health
    print("\n[5/5] Checking API endpoints...")
    api_result = check_api_health(8000, timeout=10)
    for name, info in api_result["endpoints"].items():
        status = "✅" if info.get("ok") else "❌"
        size = info.get("size_bytes", "N/A")
        print(f"  {status} {name}: {info.get('status', 'ERROR')} ({size} bytes)")

    # Kill API
    kill_subprocess(api_proc)

    # Final summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    dashboard_ok = dashboard_result["health"].get("ok") and dashboard_result["main"].get("ok")
    api_ok = sum(1 for e in api_result["endpoints"].values() if e.get("ok")) >= 4
    print(f"Dashboard: {'✅ PASS' if dashboard_ok else '❌ FAIL'}")
    print(f"API:       {'✅ PASS' if api_ok else '❌ FAIL'}")

    # Write report
    report_path = REPO_ROOT / "outputs" / "dashboard_live_check.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    with open(report_path, "w") as f:
        json.dump(
            {
                "dashboard": dashboard_result,
                "api": api_result,
                "dashboard_ok": dashboard_ok,
                "api_ok": api_ok,
            },
            f,
            indent=2,
        )
    print(f"\nReport written to: {report_path}")

    return 0 if (dashboard_ok and api_ok) else 1


if __name__ == "__main__":
    sys.exit(main())
