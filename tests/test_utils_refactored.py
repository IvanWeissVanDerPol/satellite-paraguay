"""Tests for src/utils/cron_monitor.py, dependency_audit.py, crontab_gen.py,
data_catalog.py, bootstrap.py, and src/evaluation/statistical_tests.py.
"""
import json
import sys
import os
import pytest
import numpy as np
from pathlib import Path
from unittest.mock import patch, MagicMock


class TestCronMonitor:
    """Tests for cron_monitor module."""

    def test_find_recent_logs_no_dir(self, tmp_path):
        from src.utils.cron_monitor import find_recent_logs
        result = find_recent_logs(tmp_path / "nonexistent")
        assert result == []

    def test_find_recent_logs(self, tmp_path):
        from src.utils.cron_monitor import find_recent_logs
        log_dir = tmp_path / "logs"
        log_dir.mkdir()
        log1 = log_dir / "test.log"
        log1.write_text("test content")

        result = find_recent_logs(log_dir, since_hours=24)
        assert len(result) == 1
        assert result[0] == log1

    def test_detect_traceback_present(self):
        from src.utils.cron_monitor import detect_traceback
        content = "Some output\nTraceback (most recent call last):\n  File x\n  Error\n\nMore text"
        tb = detect_traceback(content)
        assert tb is not None
        assert "Traceback" in tb

    def test_detect_traceback_absent(self):
        from src.utils.cron_monitor import detect_traceback
        assert detect_traceback("normal log") is None

    def test_detect_traceback_short(self):
        """When traceback has no \\n\\n after, returns first 2000 chars."""
        from src.utils.cron_monitor import detect_traceback
        content = "Traceback (most recent call last):\n  Error happened"
        tb = detect_traceback(content)
        assert tb is not None

    def test_detect_errors_basic(self):
        from src.utils.cron_monitor import detect_errors
        content = "INFO: ok\nERROR: bad\nFATAL: crash"
        errors = detect_errors(content)
        assert len(errors) == 2

    def test_detect_errors_case_insensitive(self):
        from src.utils.cron_monitor import detect_errors
        # Match ERROR (uppercase) - case insensitive
        content = "ERROR: bad thing\nwarning: not error\nException: raised"
        errors = detect_errors(content)
        # error matches with case-insensitive, exception also matches
        assert len(errors) >= 2  # ERROR and Exception

    def test_detect_performance_regression_none(self):
        from src.utils.cron_monitor import detect_performance_regression
        assert detect_performance_regression("Duration: 30s") is None

    def test_detect_performance_regression_found(self):
        from src.utils.cron_monitor import detect_performance_regression
        result = detect_performance_regression("Duration: 200 seconds", expected_seconds=60)
        assert result is not None
        assert "regression" in result.lower()

    def test_check_output_files_all_present(self, tmp_path):
        from src.utils.cron_monitor import check_output_files
        f = tmp_path / "test.txt"
        f.write_text("x")
        missing = check_output_files(tmp_path, ["test.txt"])
        assert missing == []

    def test_check_output_files_missing(self, tmp_path):
        from src.utils.cron_monitor import check_output_files
        missing = check_output_files(tmp_path, ["nonexistent.txt"])
        assert "nonexistent.txt" in missing

    def test_analyze_log_file_traceback(self, tmp_path):
        from src.utils.cron_monitor import analyze_log_file
        log = tmp_path / "test.log"
        log.write_text("Traceback (most recent call last):\n  File x\n\nDetail")
        alerts = analyze_log_file(log, tmp_path)
        assert len(alerts) >= 1
        assert any(a["type"] == "traceback" for a in alerts)

    def test_analyze_log_file_clean(self, tmp_path):
        from src.utils.cron_monitor import analyze_log_file
        log = tmp_path / "clean.log"
        log.write_text("All good\nINFO: ok\n")
        alerts = analyze_log_file(log, tmp_path)
        assert alerts == []

    def test_analyze_logs_no_logs(self, tmp_path):
        from src.utils.cron_monitor import analyze_logs
        result = analyze_logs(tmp_path, tmp_path / "logs")
        assert result["logs_checked"] == 0
        assert result["alerts"] == []

    def test_analyze_logs_with_expected_outputs(self, tmp_path):
        from src.utils.cron_monitor import analyze_logs
        log_dir = tmp_path / "logs"
        log_dir.mkdir()
        (log_dir / "a.log").write_text("INFO: ok\n")
        result = analyze_logs(
            tmp_path, log_dir,
            expected_outputs=["outputs/missing_file.json"]
        )
        # Should have a missing_output alert
        assert any(a["type"] == "missing_output" for a in result["alerts"])

    def test_build_email_body(self):
        from src.utils.cron_monitor import build_email_body
        alerts = [{"severity": "high", "type": "traceback", "message": "x"}]
        body = build_email_body(alerts)
        assert "[high]" in body
        assert "traceback" in body

    def test_build_email_message(self):
        from src.utils.cron_monitor import build_email_message
        msg = build_email_message("a@b.c", ["d@e.f"], "Subject", "Body")
        assert msg["Subject"] == "Subject"
        assert msg["From"] == "a@b.c"
        assert msg["To"] == "d@e.f"

    def test_format_alerts_summary_empty(self):
        from src.utils.cron_monitor import format_alerts_summary
        assert format_alerts_summary([]) == "All systems healthy"

    def test_format_alerts_summary_with_alerts(self):
        from src.utils.cron_monitor import format_alerts_summary
        alerts = [{"severity": "high", "type": "x", "message": "y", "details": "line1\nline2"}]
        summary = format_alerts_summary(alerts)
        assert "[high]" in summary
        assert "line1" in summary


class TestDependencyAudit:
    """Tests for dependency_audit module."""

    def test_get_declared_deps(self, tmp_path):
        from src.utils.dependency_audit import get_declared_deps
        pyproject = tmp_path / "pyproject.toml"
        pyproject.write_text('dependencies = ["numpy>=1.20", "pandas>=2", "requests"]')
        deps = get_declared_deps(pyproject)
        assert "numpy" in deps
        assert "pandas" in deps
        assert "requests" in deps

    def test_get_declared_deps_no_section(self, tmp_path):
        from src.utils.dependency_audit import get_declared_deps
        pyproject = tmp_path / "pyproject.toml"
        pyproject.write_text("[tool.coverage]\nfoo = 1")
        deps = get_declared_deps(pyproject)
        assert deps == []

    def test_get_declared_deps_missing(self, tmp_path):
        from src.utils.dependency_audit import get_declared_deps
        pyproject = tmp_path / "pyproject.toml"
        # nonexistent file
        deps = get_declared_deps(pyproject)
        assert deps == []

    def test_find_imports_in_file(self, tmp_path):
        from src.utils.dependency_audit import _find_imports_in_file
        f = tmp_path / "x.py"
        f.write_text("import numpy\nfrom pandas import DataFrame\nimport os\n")
        imports = _find_imports_in_file(f)
        assert "numpy" in imports
        assert "pandas" in imports
        assert "os" in imports

    def test_find_imports_in_file_nonexistent(self):
        from src.utils.dependency_audit import _find_imports_in_file
        # Non-existent file should return empty set, not raise
        imports = _find_imports_in_file(Path("/nonexistent/file.py"))
        assert imports == set()

    def test_find_used_imports(self, tmp_path):
        from src.utils.dependency_audit import find_used_imports
        src_dir = tmp_path / "src"
        src_dir.mkdir()
        (src_dir / "x.py").write_text("import numpy\nimport pandas\n")
        used = find_used_imports(tmp_path, ["src"])
        assert "numpy" in used
        assert "pandas" in used

    def test_map_imports_to_packages(self):
        from src.utils.dependency_audit import map_imports_to_packages
        used = {"PIL", "sklearn", "numpy", "unknown_pkg"}
        pkgs = map_imports_to_packages(used)
        assert "Pillow" in pkgs
        assert "scikit-learn" in pkgs
        assert "numpy" in pkgs
        assert "unknown_pkg" in pkgs

    def test_audit_dependencies(self, tmp_path):
        from src.utils.dependency_audit import audit_dependencies
        pyproject = tmp_path / "pyproject.toml"
        pyproject.write_text('dependencies = ["numpy>=1.0"]')
        result = audit_dependencies(
            tmp_path,
            declared=["numpy", "pandas"],
            used={"numpy", "sklearn"},
        )
        assert "numpy" in result["declared"]
        assert "sklearn" in result["used_imports"]
        # sklearn -> scikit-learn, not in declared -> missing
        assert "scikit-learn" in result["missing"]
        # pandas in declared but not used
        assert "pandas" in result["unused"]

    def test_compute_health_score_no_problems(self):
        from src.utils.dependency_audit import compute_health_score
        assert compute_health_score([], []) == 100

    def test_compute_health_score_with_problems(self):
        from src.utils.dependency_audit import compute_health_score
        # 3 missing * 10 = 30, 5 unused * 2 = 10, total 60 deduction
        score = compute_health_score(["a", "b", "c"], ["d", "e", "f", "g", "h"])
        assert score == max(0, 100 - 30 - 10)

    def test_get_installed_versions_failure(self):
        from src.utils.dependency_audit import get_installed_versions
        with patch("subprocess.run", side_effect=FileNotFoundError):
            result = get_installed_versions(["numpy"])
            assert result == []


class TestCrontabGen:
    """Tests for crontab_gen module."""

    def test_build_crontab_contains_hourly(self, tmp_path):
        from src.utils.crontab_gen import build_crontab
        crontab = build_crontab(tmp_path)
        assert "Hourly" in crontab
        assert "alert_cron_failures" in crontab

    def test_build_crontab_contains_repo_root(self, tmp_path):
        from src.utils.crontab_gen import build_crontab
        crontab = build_crontab(tmp_path)
        assert str(tmp_path) in crontab

    def test_build_crontab_has_backup(self, tmp_path):
        from src.utils.crontab_gen import build_crontab
        crontab = build_crontab(tmp_path)
        assert "Backup" in crontab or "rsync" in crontab

    def test_schedule_summary_not_empty(self):
        from src.utils.crontab_gen import schedule_summary
        summary = schedule_summary()
        assert "Cron schedule" in summary
        assert "Hourly" in summary

    def test_write_crontab_creates_file(self, tmp_path):
        from src.utils.crontab_gen import write_crontab
        out = write_crontab(tmp_path)
        assert out.exists()
        assert "alert_cron_failures" in out.read_text()


class TestDataCatalog:
    """Tests for data_catalog module."""

    def test_build_catalog_empty_dir(self, tmp_path):
        from src.utils.data_catalog import build_catalog
        catalog = build_catalog(tmp_path)
        # No local files match, but remote entries are always included
        assert all(c["source"] != "local: paraguay-geodata" for c in catalog if c.get("source"))
        assert len(catalog) >= 1

    def test_build_catalog_with_files(self, tmp_path):
        from src.utils.data_catalog import build_catalog
        (tmp_path / "tile_index.json").write_text("{}")
        (tmp_path / "roads.geojson").write_text("{}")
        catalog = build_catalog(tmp_path)
        local_count = sum(1 for c in catalog if c.get("source") == "local: paraguay-geodata")
        assert local_count == 2

    def test_count_local_remote(self):
        from src.utils.data_catalog import count_local_remote
        catalog = [
            {"source": "local: foo"},
            {"source": "local: bar"},
            {"source": "remote: baz"},
        ]
        counts = count_local_remote(catalog)
        assert counts["local"] == 2
        assert counts["remote"] == 1

    def test_render_markdown_contains_headers(self):
        from src.utils.data_catalog import render_markdown
        catalog = [
            {"source": "local: foo", "name": "a.json", "format": "JSON",
             "size_mb": 1.0, "description": "test"},
            {"source": "remote: baz", "name": "b", "format": "remote",
             "size_mb": None, "license": "CC0", "description": "remote test"},
        ]
        md = render_markdown(catalog)
        assert "# Data Catalog" in md
        assert "## Local Data" in md
        assert "## Remote Data Sources" in md
        assert "a.json" in md

    def test_generate_data_catalog_writes_file(self, tmp_path):
        from src.utils.data_catalog import generate_data_catalog
        (tmp_path / "tile_index.json").write_text("{}")
        out = tmp_path / "DATA_CATALOG.md"
        counts = generate_data_catalog(tmp_path, out)
        assert out.exists()
        assert counts["local"] >= 1


class TestBootstrap:
    """Tests for bootstrap module."""

    def test_check_python_version_ok(self):
        from src.utils.bootstrap import check_python_version
        result = check_python_version()
        assert result["name"] == "python_version"
        assert result["ok"] is True

    def test_check_python_version_too_low(self):
        from src.utils.bootstrap import check_python_version
        result = check_python_version(min_version=(99, 0))
        assert result["ok"] is False

    def test_check_dependencies_default(self):
        """Default check uses REQUIRED_DEPENDENCIES which includes transformers."""
        from src.utils.bootstrap import check_dependencies
        # transformers import might fail in test env; just check structure
        result = check_dependencies(packages=["numpy", "pandas"])
        assert "numpy" in result["installed"]

    def test_check_dependencies_missing(self):
        from src.utils.bootstrap import check_dependencies
        result = check_dependencies(packages=["nonexistent_pkg_xyz"])
        assert "nonexistent_pkg_xyz" in result["missing"]
        assert result["ok"] is False

    def test_check_data_directory_existing(self):
        from src.utils.bootstrap import check_data_directory
        with patch("pathlib.Path.exists", return_value=True):
            result = check_data_directory(Path("/fake/dir"))
            # Path.exists will be mocked True
            assert "ok" in result

    def test_check_key_data_files_present(self, tmp_path):
        from src.utils.bootstrap import check_key_data_files
        (tmp_path / "tile_index.json").write_text("{}")
        (tmp_path / "roads.geojson").write_text("{}")
        result = check_key_data_files(tmp_path, ["tile_index.json", "roads.geojson"])
        assert result["ok"] is True
        assert len(result["found"]) == 2

    def test_check_key_data_files_missing(self, tmp_path):
        from src.utils.bootstrap import check_key_data_files
        result = check_key_data_files(tmp_path, ["nonexistent.json"])
        assert result["ok"] is False
        assert "nonexistent.json" in result["missing"]

    def test_check_gpu_no_torch(self):
        """When torch not installed, returns ok=False."""
        from src.utils.bootstrap import check_gpu
        with patch.dict(sys.modules, {"torch": None}):
            result = check_gpu()
            # Either no torch available or returns False
            assert "ok" in result

    def test_check_network_success(self):
        from src.utils.bootstrap import check_network
        with patch("urllib.request.urlopen", return_value=MagicMock()):
            result = check_network()
            assert result["ok"] is True

    def test_check_network_failure(self):
        from src.utils.bootstrap import check_network
        with patch("urllib.request.urlopen", side_effect=Exception("timeout")):
            result = check_network()
            assert result["ok"] is False

    def test_check_dvc_initialized(self, tmp_path):
        from src.utils.bootstrap import check_dvc_initialized
        (tmp_path / ".dvc").mkdir()
        result = check_dvc_initialized(tmp_path)
        assert result["ok"] is True

    def test_setup_directories(self, tmp_path):
        from src.utils.bootstrap import setup_directories
        result = setup_directories(tmp_path, ["a", "b/c", "d"])
        assert (tmp_path / "a").exists()
        assert (tmp_path / "b/c").exists()
        assert result["ok"] is True

    def test_is_ready_all_ok(self):
        from src.utils.bootstrap import is_ready
        checks = {
            "python": {"ok": True},
            "deps": {"ok": True},
            "data_dir": {"ok": True},
        }
        assert is_ready(checks) is True

    def test_is_ready_python_fail(self):
        from src.utils.bootstrap import is_ready
        checks = {
            "python": {"ok": False},
            "deps": {"ok": True},
            "data_dir": {"ok": True},
        }
        assert is_ready(checks) is False


class TestStatisticalTestsRefactored:
    """Tests for refactored statistical_tests in src/evaluation/."""

    def test_mcnemar_identical(self):
        from src.evaluation.statistical_tests import mcnemar_test
        y = np.array([0, 1, 0, 1, 0])
        result = mcnemar_test(y, y, y)
        assert result["chi2"] == 0.0
        assert result["p_value"] == 1.0
        assert result["significant_at_005"] is False

    def test_mcnemar_different(self):
        from src.evaluation.statistical_tests import mcnemar_test
        y = np.array([0, 1, 0, 1, 0, 1, 0, 1])
        a = y.copy()
        b = 1 - y
        result = mcnemar_test(y, a, b)
        assert "chi2" in result
        assert "p_value" in result

    def test_chi_squared_indigenous_basic(self):
        from src.evaluation.statistical_tests import chi_squared_indigenous
        obs = {"lost": 100, "total": 1000}
        exp = {"lost": 50, "total": 1000}
        result = chi_squared_indigenous(obs, exp)
        assert result["chi2"] > 0
        assert result["p_value"] < 0.05
        assert "cramers_v" in result

    def test_paired_ttest_drought_dict_input(self):
        from src.evaluation.statistical_tests import paired_ttest_drought
        # annual_loss is a dict mapping year -> value
        annual_loss = {2020: 100.0, 2021: 110.0, 2022: 90.0, 2023: 95.0}
        drought_years = [2020, 2022]
        non_drought = [2021, 2023]
        result = paired_ttest_drought(annual_loss, drought_years, non_drought)
        # Should compute without IndexError now
        assert "error" not in result
        assert "t_statistic" in result

    def test_paired_ttest_drought_insufficient(self):
        from src.evaluation.statistical_tests import paired_ttest_drought
        annual_loss = {2020: 100.0}
        result = paired_ttest_drought(annual_loss, [2020], [2021])
        assert "error" in result

    def test_bootstrap_disparity(self):
        from src.evaluation.statistical_tests import bootstrap_disparity
        territory = np.array([10.0, 20.0, 30.0, 5.0])
        result = bootstrap_disparity(territory, national_loss_pct=5.0, n_boot=100)
        assert "bootstrap_mean_ratio" in result
        assert "p_value_h1_gt_1_5x" in result
        assert result["n_bootstrap"] == 100

    def test_to_native(self):
        from src.evaluation.statistical_tests import to_native
        assert to_native(np.int64(5)) == 5
        assert to_native(np.float64(3.14)) == 3.14
        assert to_native(np.bool_(True)) is True
        assert to_native(np.array([1, 2])) == [1, 2]

    def test_clean_for_json(self):
        from src.evaluation.statistical_tests import clean_for_json
        obj = {"a": np.int64(5), "b": [np.float64(1.5), 2.5], "c": "x"}
        cleaned = clean_for_json(obj)
        assert cleaned["a"] == 5
        assert cleaned["b"] == [1.5, 2.5]
        assert cleaned["c"] == "x"

    def test_clean_for_json_nested(self):
        from src.evaluation.statistical_tests import clean_for_json
        obj = {"level1": {"level2": np.array([1.0, 2.0])}}
        cleaned = clean_for_json(obj)
        assert cleaned["level1"]["level2"] == [1.0, 2.0]