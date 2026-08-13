"""Observability dashboard for satellite-paraguay.

A Streamlit dashboard showing:
- Test results history
- Code coverage trends
- Performance benchmarks
- Dependency health
- MLflow experiment tracking
- Alert log

Run: streamlit run src/observability_dashboard.py
"""

import json
import sys
from pathlib import Path

import streamlit as st

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))


st.set_page_config(
    page_title="Observability - Satellite Paraguay",
    page_icon="📊",
    layout="wide",
)


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text())  # type: ignore[no-any-return]
    except FileNotFoundError:
        return {}


def main():
    st.title("📊 Satellite Paraguay - Observability Dashboard")
    st.markdown("""
    **System health, test results, performance, dependencies, and alerts**
    """)

    # ========== Top metrics row ==========
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        # Test count
        test_files = list((REPO_ROOT / "tests").glob("test_*.py"))
        test_count = sum(1 for f in test_files if not f.name.startswith("__"))
        st.metric("Test files", test_count)

    with col2:
        # Lines of Python code
        py_files = list((REPO_ROOT / "scripts").rglob("*.py")) + list((REPO_ROOT / "src").rglob("*.py"))
        loc = sum(len(open(f, encoding="utf-8", errors="replace").readlines()) for f in py_files)
        st.metric("Python LOC", f"{loc:,}")

    with col3:
        # Outputs
        output_files = list((REPO_ROOT / "outputs").rglob("*.json"))
        st.metric("Output JSONs", len(output_files))

    with col4:
        # Git commits
        try:
            import subprocess

            result = subprocess.run(
                ["git", "rev-list", "--count", "HEAD"], cwd=REPO_ROOT, capture_output=True, text=True
            )
            commit_count = int(result.stdout.strip()) if result.returncode == 0 else 0
        except Exception:
            commit_count = 0
        st.metric("Git commits", commit_count)

    st.markdown("---")

    # ========== Test results ==========
    st.header("🧪 Test Results")

    col1, col2 = st.columns([2, 1])

    with col1:
        # Test status
        test_report_path = REPO_ROOT / "outputs/test_report.json"
        if test_report_path.exists():
            report = load_json(test_report_path)
            n_pass = report.get("passed", 0)
            n_fail = report.get("failed", 0)
            n_total = n_pass + n_fail
            if n_total > 0:
                pct = 100 * n_pass / n_total
                st.metric("Pass rate", f"{pct:.1f}%", f"{n_pass}/{n_total}")
                if n_fail > 0:
                    st.error(f"{n_fail} failing tests")
        else:
            st.info("Run `pytest tests/ --no-cov -v > outputs/test_report.json`")

    with col2:
        # Coverage
        coverage_path = REPO_ROOT / "coverage.xml"
        if coverage_path.exists():
            content = coverage_path.read_text()
            # Extract line-rate attribute
            import re

            m = re.search(r'line-rate="([\d.]+)"', content)
            if m:
                cov = float(m.group(1)) * 100
                st.metric("Code coverage", f"{cov:.1f}%")
        else:
            st.info("Coverage not generated")

    # ========== Coverage breakdown ==========
    st.header("📈 Coverage by module")
    if coverage_path.exists():
        content = coverage_path.read_text()
        # Parse <class> entries
        import re

        classes = re.findall(r'<class name="([^"]+)" filename="([^"]+)"[^>]*line-rate="([\d.]+)"', content)
        if classes:
            import pandas as pd

            df = pd.DataFrame(classes, columns=["name", "filename", "line_rate"])
            df["line_rate"] = df["line_rate"].astype(float) * 100
            df = df.sort_values("line_rate", ascending=True)
            st.dataframe(
                df[["filename", "line_rate"]].rename(columns={"line_rate": "Coverage %"}),
                use_container_width=True,
            )
        else:
            st.info("Coverage breakdown not parseable")
    else:
        st.info("Run `pytest --cov` to generate coverage")

    st.markdown("---")

    # ========== Performance ==========
    st.header("⚡ Performance Benchmarks")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Carbon model (Chave 2014)")
        # Time test
        import time

        import numpy as np

        from scripts.per_pixel_carbon import chave_agb

        tc = np.random.default_rng(42).uniform(0, 100, (2000, 2000)).astype(np.float32)
        start = time.time()
        chave_agb(tc)
        elapsed = time.time() - start
        st.metric("4M pixels Chave AGB", f"{elapsed:.3f}s", "budget: <1.0s")

    with col2:
        st.subheader("Bootstrap CIs")
        from scripts.uncertainty_quantification import pixel_bootstrap_fast

        lossyear = (np.random.default_rng(42).uniform(0, 1, (1000, 1000)) > 0.8).astype(np.uint8)
        start = time.time()
        pixel_bootstrap_fast(lossyear, n_boot=1000)
        elapsed = time.time() - start
        st.metric("Bootstrap 1000 iter", f"{elapsed:.3f}s", "budget: <2.0s")

    st.markdown("---")

    # ========== Dependency health ==========
    st.header("📦 Dependencies")

    dep_audit = load_json(REPO_ROOT / "outputs/dependency_audit.json")
    if dep_audit:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Declared deps", len(dep_audit.get("declared", [])))
        with col2:
            st.metric("Used packages", len(dep_audit.get("used_packages", [])))
        with col3:
            missing = len(dep_audit.get("missing", []))
            unused = len(dep_audit.get("unused", []))
            score = max(0, 100 - 10 * missing - 2 * unused)
            st.metric("Health score", f"{score}/100")
    else:
        st.info("Run `python3 scripts/audit_dependencies.py`")

    st.markdown("---")

    # ========== Alerts ==========
    st.header("🚨 Recent Alerts")

    alert_path = REPO_ROOT / "outputs/alert_report.json"
    if alert_path.exists():
        alerts = load_json(alert_path).get("alerts", [])
        if not alerts:
            st.success("✓ No alerts in recent window")
        else:
            for a in alerts:
                sev = a.get("severity", "?")
                sev_icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(sev, "⚪")
                st.warning(f"{sev_icon} [{sev}] {a.get('type')}: {a.get('message')}")
    else:
        st.info("Run `python3 scripts/alert_cron_failures.py`")

    st.markdown("---")

    # ========== MLflow runs ==========
    st.header("🔬 MLflow Experiments")
    try:
        from src.mlflow_tracking import list_experiments, search_runs

        experiments = list_experiments()
        if experiments:
            for exp in experiments[:5]:
                runs = search_runs(exp["name"], max_results=5)
                with st.expander(f"📊 {exp['name']} ({len(runs)} recent runs)"):
                    if runs:
                        for r in runs[:5]:
                            run_name = r.get("run_name", r.get("run_id", "?"))
                            start = r.get("start_time", "")
                            st.text(f"  - {run_name} @ {start}")
                    else:
                        st.text("  No runs yet")
        else:
            st.info("MLflow not initialized (install with `pip install mlflow`)")
    except ImportError:
        st.info("MLflow not installed (install with `pip install mlflow`)")

    # Footer
    st.markdown("---")
    st.markdown("""
    **Satellite Paraguay - Observability Dashboard**
    For complete state inventory, see `FINAL_REPORT.md`.
    """)


if __name__ == "__main__":
    main()
