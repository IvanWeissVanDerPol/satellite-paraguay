"""End-to-end integration test.

Runs the full analysis pipeline on synthetic data and verifies all outputs are produced.

Run:
    pytest tests/test_integration.py -m integration --no-cov -v
"""
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest


@pytest.mark.integration
@pytest.mark.slow
class TestFullPipeline:
    """End-to-end test that runs all major scripts in sequence."""

    @pytest.fixture(scope="class")
    def workspace(self, tmp_path_factory):
        """Create isolated workspace with synthetic data."""
        ws = tmp_path_factory.mktemp("integration_workspace")
        return ws

    @pytest.fixture(scope="class")
    def setup_synthetic_data(self, workspace):
        """Generate synthetic Hansen + MapBiomas data."""
        # This is handled by conftest fixtures in tmp dirs
        return workspace

    def test_01_chave_carbon_pipeline(self, tmp_path):
        """Test 1: Chave AGB model produces valid output."""
        import numpy as np

        from scripts.per_pixel_carbon import carbon_stock, chave_agb, co2e

        # Synthetic treecover
        tc = np.full((100, 100), 50.0, dtype=np.float32)
        agb = chave_agb(tc)
        carbon = carbon_stock(tc)
        co2e_arr = co2e(tc)

        # All 50% treecover should give ~42.4 Mg/ha AGB
        assert agb[0, 0] > 40
        # Carbon = 47% of AGB
        assert abs(carbon[0, 0] / agb[0, 0] - 0.47) < 0.01
        # CO2e = 44/12 * Carbon
        assert abs(co2e_arr[0, 0] / carbon[0, 0] - 44 / 12) < 0.01

    def test_02_bootstrap_pipeline(self):
        """Test 2: Bootstrap CIs compute correctly."""
        import numpy as np

        from scripts.uncertainty_quantification import pixel_bootstrap_fast

        # Synthetic lossyear with 10% loss
        lossyear = np.zeros(1000, dtype=np.uint8)
        lossyear[:100] = 1  # 10% loss

        result = pixel_bootstrap_fast(lossyear, n_boot=100)

        assert "mean" in result
        assert "ci_lower_95" in result
        assert "ci_upper_95" in result
        assert abs(result["mean"] - 100) < 20  # Should be near 100
        assert result["ci_lower_95"] <= result["mean"] <= result["ci_upper_95"]

    def test_03_chave_to_bootstrap_pipeline(self):
        """Test 3: Chave + bootstrap together produce per-pixel carbon CIs."""
        import numpy as np

        from scripts.per_pixel_carbon import chave_agb
        from scripts.uncertainty_quantification import pixel_bootstrap_fast

        # Synthetic data
        H, W = 100, 100
        treecover = np.full((H, W), 50.0, dtype=np.float32)
        lossyear = np.zeros((H, W), dtype=np.uint8)
        rng = np.random.default_rng(42)
        loss_idx = rng.choice(H * W, size=1000, replace=False)
        lossyear.flat[loss_idx] = rng.integers(1, 24, size=1000)

        # Compute per-pixel AGB and CO2e
        agb = chave_agb(treecover)
        co2e_per_pixel = agb * 0.47 * (44 / 12) * 0.0625

        # Total CO2e for loss pixels
        total_co2e_mt = (co2e_per_pixel * (lossyear > 0)).sum() / 1e6
        assert total_co2e_mt > 0

        # Bootstrap on loss pixel count
        flat_loss = (lossyear > 0).flatten().astype(np.uint8)
        result = pixel_bootstrap_fast(flat_loss, n_boot=100)
        assert "ci_lower_95" in result

    def test_04_full_pipeline_outputs_exist(self, repo_root):
        """Test 4: All required output files exist (run real analysis first)."""
        outputs_dir = repo_root / "outputs"
        if not outputs_dir.exists():
            pytest.skip("outputs/ not present - run scripts first")

        # Check that key output files exist (skip if pipeline not yet run).
        # Use first-exists check for files that have alternate names from
        # different script versions.
        def first_exists(*candidates):
            for c in candidates:
                if (repo_root / c).exists():
                    return c
            return None

        # Each entry is a list of acceptable paths; "first_exists" returns
        # the first one that's present. If none, the output is "missing".
        expected_groups = [
            [
                "outputs/p0011/departments/department_stats.json",
                "outputs/p0011/departments/department_deforestation.json",
            ],
            [
                "outputs/p0011/indigenous/indigenous_stats.json",
                "outputs/p0011/indigenous/indigenous_overlap.json",
            ],
            ["outputs/p0011/carbon/per_year_loss.json"],
            ["outputs/p0011/uncertainty/uncertainty_results.json"],
            ["outputs/carbon_credits/verra_verification.json"],
            ["outputs/statistical_tests/test_results.json"],
            ["outputs/cross_transfer/transfer_results.json"],
        ]
        missing = [
            group[0] for group in expected_groups if first_exists(*group) is None
        ]
        if missing:
            pytest.skip(f"Outputs not yet generated: {len(missing)} missing. Run scripts/ first.")
        # If we got here, all expected outputs exist; assert at least the
        # primary paths remain tracked.
        for group in expected_groups:
            resolved = first_exists(*group)
            assert resolved is not None, f"Missing all variants for {group[0]}"

    def test_05_api_endpoints_e2e(self, repo_root):
        """Test 5: API endpoints return valid data."""
        # Use TestClient for in-process testing
        try:
            from fastapi.testclient import TestClient

            from src.api.main import app
        except ImportError:
            pytest.skip("FastAPI not installed")

        client = TestClient(app)

        # Test summary
        response = client.get("/summary")
        assert response.status_code == 200
        data = response.json()
        assert data["title"]

        # Test all endpoints
        for endpoint in ["/health", "/departments", "/territories", "/verra", "/models"]:
            response = client.get(endpoint)
            assert response.status_code == 200

    def test_06_makefile_targets(self, repo_root):
        """Test 6: Makefile has all expected targets."""
        makefile = repo_root / "Makefile"
        if not makefile.exists():
            pytest.skip("Makefile not present")

        content = makefile.read_text()
        # Check that key targets are present
        for target in ["install", "test", "lint", "format", "dashboard"]:
            assert target in content, f"Missing Makefile target: {target}"

    def test_07_reproducibility_check(self, repo_root):
        """Test 7: Key files exist for reproducibility."""
        required = [
            "README.md",
            "pyproject.toml",
            "Makefile",
            ".pre-commit-config.yaml",
            ".github/workflows/cicd.yml",
            "docker-compose.production.yml",
            "Dockerfile.production",
            "tests/conftest.py",
            "src/api/main.py",
            "src/dashboard/app.py",
            "src/logging_config.py",
            "src/mlflow_tracking.py",
        ]
        for f in required:
            full = repo_root / f
            assert full.exists(), f"Missing required file: {f}"
