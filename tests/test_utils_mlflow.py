"""Tests for src/utils/mlflow_tracking.py.

Coverage target: 100%. The module wraps MLflow with thin helpers; each
function is exercised via mocking or, when mlflow is available, an
in-memory SQLite tracking URI.
"""

import pytest  # noqa: E402

pytest.importorskip("mlflow", reason="CI: requires optional system dep 'mlflow' (not installed)")  # noqa: E402

import sys  # noqa: E402
from unittest.mock import patch  # noqa: E402

import pytest  # noqa: E402

try:
    import mlflow  # noqa: F401

    _HAS_MLFLOW = True
except ImportError:
    _HAS_MLFLOW = False


@pytest.fixture
def tmp_mlruns(tmp_path):
    """Create a tmp mlruns dir for tests that need a real MLflow tracking URI."""
    d = tmp_path / "mlruns"
    d.mkdir()
    return d


@pytest.fixture(autouse=True)
def _silence_mlflow_global_state(monkeypatch):
    """Avoid leaking tracking URI between tests.

    Each test that uses mlflow should set its own MLFLOW_TRACKING_URI
    via monkeypatch.setenv. This fixture only clears any prior URI to
    prevent cross-test contamination.
    """
    monkeypatch.delenv("MLFLOW_TRACKING_URI", raising=False)
    yield
    if _HAS_MLFLOW:
        try:
            import mlflow as _mlflow

            _mlflow.set_tracking_uri("")
        except Exception:
            pass


# =========================
# setup_mlflow
# =========================


class TestSetupMlflow:
    def test_raises_on_import_error(self):
        """If mlflow is missing, raise ImportError."""
        with patch.dict(sys.modules, {"mlflow": None}):
            with patch.dict(sys.modules, {"mlflow.tracking": None}):
                with pytest.raises(ImportError):
                    from src.utils.mlflow_tracking import setup_mlflow

                    setup_mlflow()

    @pytest.mark.skipif(not _HAS_MLFLOW, reason="mlflow not installed")
    def test_default_tracking_uri_uses_env(self, tmp_path, monkeypatch):
        """When MLFLOW_TRACKING_URI is set, use it as default."""
        from src.utils import mlflow_tracking as mt

        uri = f"sqlite:///{tmp_path / 'env_uri.db'}"
        monkeypatch.setenv("MLFLOW_TRACKING_URI", uri)
        client = mt.setup_mlflow()
        assert client is not None
        # Verify the URI was actually set
        import mlflow as _mlflow

        assert _mlflow.get_tracking_uri() == uri

    @pytest.mark.skipif(not _HAS_MLFLOW, reason="mlflow not installed")
    def test_with_explicit_tracking_uri(self, tmp_path):
        from src.utils import mlflow_tracking as mt

        uri = f"sqlite:///{tmp_path / 'explicit.db'}"
        client = mt.setup_mlflow(tracking_uri=uri)
        assert client is not None

    @pytest.mark.skipif(not _HAS_MLFLOW, reason="mlflow not installed")
    def test_custom_experiment_name(self, tmp_path):
        from src.utils import mlflow_tracking as mt

        uri = f"sqlite:///{tmp_path / 'exp_name.db'}"
        client = mt.setup_mlflow(
            tracking_uri=uri,
            experiment_name="custom_experiment",
        )
        assert client is not None


# =========================
# log_experiment
# =========================


class TestLogExperiment:
    def test_raises_on_import_error(self):
        with patch.dict(sys.modules, {"mlflow": None}):
            with patch.dict(sys.modules, {"mlflow.tracking": None}):
                with pytest.raises(ImportError):
                    from src.utils.mlflow_tracking import log_experiment

                    log_experiment(
                        run_name="test",
                        params={},
                        metrics={},
                    )

    @pytest.mark.skipif(not _HAS_MLFLOW, reason="mlflow not installed")
    def test_logs_params_and_metrics(self, tmp_path):
        """End-to-end log_experiment via real mlflow."""
        from src.utils.mlflow_tracking import log_experiment

        # Use sqlite backend (file backend is deprecated in mlflow 3.x)
        db = tmp_path / "mlflow.db"
        uri = f"sqlite:///{db}"
        run_id = log_experiment(
            run_name="test_run",
            params={"lr": 0.001, "batch_size": 32},
            metrics={"f1": 0.85, "accuracy": 0.92},
            tracking_uri=uri,
        )
        assert run_id is not None
        assert isinstance(run_id, str)

    @pytest.mark.skipif(not _HAS_MLFLOW, reason="mlflow not installed")
    def test_logs_artifacts_that_exist(self, tmp_path):
        from src.utils.mlflow_tracking import log_experiment

        # Create an artifact file
        artifact = tmp_path / "model.pkl"
        artifact.write_text("dummy")

        db = tmp_path / "mlflow.db"
        run_id = log_experiment(
            run_name="with_artifact",
            params={},
            metrics={"f1": 0.80},
            artifacts={str(artifact): "model"},
            tracking_uri=f"sqlite:///{db}",
        )
        assert run_id is not None

    @pytest.mark.skipif(not _HAS_MLFLOW, reason="mlflow not installed")
    def test_skips_missing_artifacts_silently(self, tmp_path):
        """If a local artifact path doesn't exist, skip logging without error."""
        from src.utils.mlflow_tracking import log_experiment

        db = tmp_path / "mlflow.db"
        run_id = log_experiment(
            run_name="missing_artifact",
            params={},
            metrics={"f1": 0.7},
            artifacts={"/nonexistent/path.json": "ghost"},
            tracking_uri=f"sqlite:///{db}",
        )
        # Run completes; missing artifact is silently skipped
        assert run_id is not None

    @pytest.mark.skipif(not _HAS_MLFLOW, reason="mlflow not installed")
    def test_logs_tags(self, tmp_path):
        from src.utils.mlflow_tracking import log_experiment

        db = tmp_path / "mlflow.db"
        run_id = log_experiment(
            run_name="tagged",
            params={},
            metrics={"f1": 0.65},
            tags={"paper": "P0011", "branch": "main"},
            tracking_uri=f"sqlite:///{db}",
        )
        assert run_id is not None


# =========================
# get_best_run
# =========================


class TestGetBestRun:
    def test_raises_on_import_error(self):
        with patch.dict(sys.modules, {"mlflow": None}):
            with patch.dict(sys.modules, {"mlflow.tracking": None}):
                with pytest.raises(ImportError):
                    from src.utils.mlflow_tracking import get_best_run

                    get_best_run(metric_name="f1")

    @pytest.mark.skipif(not _HAS_MLFLOW, reason="mlflow not installed")
    def test_returns_none_when_experiment_missing(self, tmp_path, monkeypatch):
        """If the experiment doesn't exist yet, return None."""
        from src.utils.mlflow_tracking import get_best_run

        monkeypatch.setenv(
            "MLFLOW_TRACKING_URI",
            f"sqlite:///{tmp_path / 'db.sqlite'}",
        )
        result = get_best_run(
            metric_name="f1",
            experiment_name="nonexistent_exp_xyz",
        )
        assert result is None

    @pytest.mark.skipif(not _HAS_MLFLOW, reason="mlflow not installed")
    def test_finds_best_run(self, tmp_path, monkeypatch):
        """After logging two runs, get_best_run returns the highest-f1 run."""
        from src.utils.mlflow_tracking import get_best_run, log_experiment

        uri = f"sqlite:///{tmp_path / 'db.sqlite'}"
        monkeypatch.setenv("MLFLOW_TRACKING_URI", uri)
        log_experiment("low", {}, {"f1": 0.50}, tracking_uri=uri)
        log_experiment("high", {}, {"f1": 0.90}, tracking_uri=uri)
        log_experiment("mid", {}, {"f1": 0.70}, tracking_uri=uri)
        best = get_best_run(
            metric_name="f1",
            experiment_name="satellite-paraguay",
            ascending=False,
        )
        assert best is not None
        assert best.data.metrics["f1"] == 0.90

    @pytest.mark.skipif(not _HAS_MLFLOW, reason="mlflow not installed")
    def test_ascending_lowest(self, tmp_path, monkeypatch):
        pass

        from src.utils.mlflow_tracking import get_best_run, log_experiment

        uri = f"sqlite:///{tmp_path / 'db.sqlite'}"
        monkeypatch.setenv("MLFLOW_TRACKING_URI", uri)
        # log_experiment creates runs in the default experiment "satellite-paraguay"
        log_experiment("a", {}, {"loss": 0.5}, tracking_uri=uri)
        log_experiment("b", {}, {"loss": 0.1}, tracking_uri=uri)
        # get_best_run uses setup_mlflow() (default experiment)
        best_lowest_loss = get_best_run(
            metric_name="loss",
            experiment_name="satellite-paraguay",
            ascending=True,
        )
        assert best_lowest_loss is not None
        assert best_lowest_loss.data.metrics["loss"] == 0.1


# =========================
# per-paper wrappers
# =========================


class TestPaperWrappers:
    """The 6 paper-specific helpers just delegate to log_experiment."""

    @pytest.fixture(autouse=True)
    def _set_sqlite_uri(self, tmp_path, monkeypatch):
        """All wrapper tests use a sqlite backend to avoid the deprecated
        file:// default."""
        if _HAS_MLFLOW:
            monkeypatch.setenv(
                "MLFLOW_TRACKING_URI",
                f"sqlite:///{tmp_path / 'paper_wrappers.db'}",
            )

    @pytest.mark.skipif(not _HAS_MLFLOW, reason="mlflow not installed")
    def test_p0011_wrapper(self, tmp_path):
        from src.utils.mlflow_tracking import log_p0011_experiment

        rid = log_p0011_experiment(
            f1_macro=0.85,
            miou=0.80,
            params={"model": "unet"},
        )
        assert rid is not None

    @pytest.mark.skipif(not _HAS_MLFLOW, reason="mlflow not installed")
    def test_p0100_wrapper(self, tmp_path):
        from src.utils.mlflow_tracking import log_p0100_experiment

        rid = log_p0100_experiment(
            r2=0.7,
            rmse=0.5,
            mae=0.3,
            params={"model": "alphaearth"},
        )
        assert rid is not None

    @pytest.mark.skipif(not _HAS_MLFLOW, reason="mlflow not installed")
    def test_p0025_wrapper(self, tmp_path):
        from src.utils.mlflow_tracking import log_p0025_experiment

        rid = log_p0025_experiment(
            r2=0.6,
            rmse=0.4,
            mae=0.2,
            params={"model": "lstm"},
        )
        assert rid is not None

    @pytest.mark.skipif(not _HAS_MLFLOW, reason="mlflow not installed")
    def test_p0026_wrapper(self, tmp_path):
        from src.utils.mlflow_tracking import log_p0026_experiment

        rid = log_p0026_experiment(
            map50=0.65,
            map50_95=0.45,
            epochs=30,
            params={"model": "yolov8"},
        )
        assert rid is not None

    @pytest.mark.skipif(not _HAS_MLFLOW, reason="mlflow not installed")
    def test_p0035_wrapper(self, tmp_path):
        from src.utils.mlflow_tracking import log_p0035_experiment

        rid = log_p0035_experiment(
            val_mae=8.5,
            epochs=20,
            params={"horizon": 24},
        )
        assert rid is not None
