"""Tests for src/utils/paper_validators.py."""

import pytest  # noqa: E402

pytest.importorskip("rasterio", reason="CI: requires optional system dep 'rasterio' (not installed)")  # noqa: E402

from unittest.mock import MagicMock, patch  # noqa: E402

import pytest  # noqa: E402


class TestPaperValidators:
    """Tests for paper_validators module."""

    def test_paper_names_complete(self):
        from src.utils.paper_validators import PAPER_NAMES

        assert len(PAPER_NAMES) == 6
        assert all(i in PAPER_NAMES for i in range(1, 7))

    def test_get_validator(self):
        from src.utils.paper_validators import get_validator, validate_paper_1

        assert get_validator(1) == validate_paper_1

    def test_validate_one_invalid_id(self):
        from src.utils.paper_validators import validate_one

        with pytest.raises(ValueError):
            validate_one(99)

    def test_validate_paper_1_mocked(self):
        from src.utils.paper_validators import validate_paper_1

        mock_pipeline = MagicMock()
        with patch(
            "src.papers.p0011_yvytu_deforestation.YvytuPipeline",
            return_value=mock_pipeline,
        ):
            result = validate_paper_1()
        assert result["paper"] == 1
        assert result["status"] == "ok"
        assert "predictions_shape" in result

    def test_validate_paper_2_mocked(self):
        from src.utils.paper_validators import validate_paper_2

        mock_pipeline = MagicMock()
        mock_pipeline.fetch_verra_projects.return_value = [1, 2, 3]
        with patch(
            "src.papers.p0100_yvyra_carbon_credits.YvyraPipeline",
            return_value=mock_pipeline,
        ):
            result = validate_paper_2()
        assert result["paper"] == 2
        assert result["n_projects"] == 3

    def test_validate_paper_3_mocked(self):
        from src.utils.paper_validators import validate_paper_3

        mock_pipeline = MagicMock()
        mock_pipeline.load_inbio_data.return_value = {"key": "value"}
        with patch(
            "src.papers.p0025_yrupe_yield.YrupePipeline",
            return_value=mock_pipeline,
        ):
            result = validate_paper_3()
        assert result["paper"] == 3
        assert "inbio_data" in result

    def test_validate_paper_4_mocked(self):
        from src.utils.paper_validators import validate_paper_4

        mock_pipeline = MagicMock()
        mock_pipeline.detect_conflicts.return_value = {"conflict_parcels": 5}
        with patch(
            "src.papers.p0012_yvy_indigenous.YvyPipeline",
            return_value=mock_pipeline,
        ):
            result = validate_paper_4()
        assert result["paper"] == 4
        assert result["conflict_parcels"] == 5

    def test_validate_paper_5_mocked(self):
        from src.utils.paper_validators import validate_paper_5

        mock_pipeline = MagicMock()
        mock_pipeline.select_tiles.return_value = [1, 2, 3, 4]
        with patch(
            "src.papers.p0026_kai_poaching.KaiPipeline",
            return_value=mock_pipeline,
        ):
            result = validate_paper_5()
        assert result["paper"] == 5
        assert result["n_tiles"] == 4

    def test_validate_paper_6_mocked(self):
        from src.utils.paper_validators import validate_paper_6

        mock_pipeline = MagicMock()
        mock_pipeline.fetch_openaq_data.return_value = [{"v": 1}, {"v": 2}]
        with patch(
            "src.papers.p0035_tatakua_air_quality.TatakuaPipeline",
            return_value=mock_pipeline,
        ):
            result = validate_paper_6()
        assert result["paper"] == 6
        assert result["n_measurements"] == 2

    def test_validate_all_mocked(self):
        """validate_all returns results for all 6 papers."""
        from src.utils.paper_validators import validate_all

        mock_pipeline = MagicMock()
        mock_pipeline.fetch_verra_projects.return_value = []
        mock_pipeline.load_inbio_data.return_value = {}
        mock_pipeline.detect_conflicts.return_value = {"conflict_parcels": 0}
        mock_pipeline.select_tiles.return_value = []
        mock_pipeline.fetch_openaq_data.return_value = []

        with (
            patch(
                "src.papers.p0011_yvytu_deforestation.YvytuPipeline",
                return_value=mock_pipeline,
            ),
            patch(
                "src.papers.p0100_yvyra_carbon_credits.YvyraPipeline",
                return_value=mock_pipeline,
            ),
            patch(
                "src.papers.p0025_yrupe_yield.YrupePipeline",
                return_value=mock_pipeline,
            ),
            patch(
                "src.papers.p0012_yvy_indigenous.YvyPipeline",
                return_value=mock_pipeline,
            ),
            patch(
                "src.papers.p0026_kai_poaching.KaiPipeline",
                return_value=mock_pipeline,
            ),
            patch(
                "src.papers.p0035_tatakua_air_quality.TatakuaPipeline",
                return_value=mock_pipeline,
            ),
        ):
            results = validate_all()
        assert len(results) == 6
        assert all(r["status"] == "ok" for r in results)

    def test_validate_all_with_error(self):
        """If one validator fails, others still run."""
        from src.utils.paper_validators import validate_all

        with patch(
            "src.papers.p0011_yvytu_deforestation.YvytuPipeline",
            side_effect=Exception("boom"),
        ):
            results = validate_all()
        # First one fails, rest succeed
        assert results[0]["status"] == "error"
        assert results[0]["error"] == "boom"
        # Other validators should still work
        assert len(results) == 6
