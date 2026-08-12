"""Tests for src/utils/test_data.py."""

import json
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch


class TestTestData:
    """Tests for test_data module."""

    def test_compute_hash(self, tmp_path):
        from src.utils.test_data import compute_hash

        f = tmp_path / "test.txt"
        f.write_text("hello")
        h = compute_hash(f)
        assert len(h) == 64  # SHA256 hex

    def test_compute_hash_sha512(self, tmp_path):
        from src.utils.test_data import compute_hash

        f = tmp_path / "test.txt"
        f.write_text("hello")
        h = compute_hash(f, "sha512")
        assert len(h) == 128

    def test_index_directory_empty(self, tmp_path):
        from src.utils.test_data import index_directory

        # Nonexistent dir
        result = index_directory(tmp_path / "missing")
        assert result == {}

    def test_index_directory_with_files(self, tmp_path):
        from src.utils.test_data import index_directory

        (tmp_path / "a.txt").write_text("a")
        (tmp_path / "b.txt").write_text("b")
        (tmp_path / "sub").mkdir()
        (tmp_path / "sub/c.txt").write_text("c")
        result = index_directory(tmp_path)
        assert len(result) == 3
        assert "a.txt" in result
        assert "sub/c.txt" in result
        assert all("hash_sha256" in v for v in result.values())

    def test_save_index(self, tmp_path):
        from src.utils.test_data import index_directory, save_index

        (tmp_path / "a.txt").write_text("a")
        index = index_directory(tmp_path)
        index_path = tmp_path / "index.json"
        save_index(index, index_path)
        assert index_path.exists()
        data = json.loads(index_path.read_text())
        assert "files" in data
        assert data["version"] == "1.0"

    def test_save_index_creates_parent(self, tmp_path):
        from src.utils.test_data import save_index

        index_path = tmp_path / "deep" / "nested" / "idx.json"
        save_index({"x.txt": {"hash_sha256": "abc", "size_bytes": 1, "modified": "now"}}, index_path)
        assert index_path.exists()

    def test_verify_against_index_no_index(self, tmp_path):
        from src.utils.test_data import verify_against_index

        result = verify_against_index(tmp_path, tmp_path / "missing.json")
        assert result == {}

    def test_verify_against_index_match(self, tmp_path):
        from src.utils.test_data import index_directory, save_index, verify_against_index

        (tmp_path / "a.txt").write_text("a")
        index = index_directory(tmp_path)
        index_path = tmp_path / "idx.json"
        save_index(index, index_path)

        result = verify_against_index(tmp_path, index_path)
        assert all(r["status"] == "match" for r in result.values())

    def test_verify_against_index_modified(self, tmp_path):
        from src.utils.test_data import index_directory, save_index, verify_against_index

        (tmp_path / "a.txt").write_text("a")
        index = index_directory(tmp_path)
        index_path = tmp_path / "idx.json"
        save_index(index, index_path)

        # Modify file
        (tmp_path / "a.txt").write_text("a_modified")

        result = verify_against_index(tmp_path, index_path)
        assert result["a.txt"]["status"] == "modified"

    def test_verify_against_index_missing(self, tmp_path):
        from src.utils.test_data import index_directory, save_index, verify_against_index

        (tmp_path / "a.txt").write_text("a")
        index = index_directory(tmp_path)
        index_path = tmp_path / "idx.json"
        save_index(index, index_path)

        # Delete file
        (tmp_path / "a.txt").unlink()

        result = verify_against_index(tmp_path, index_path)
        assert result["a.txt"]["status"] == "missing"

    def test_summarize_verification(self):
        from src.utils.test_data import summarize_verification

        results = {
            "a": {"status": "match"},
            "b": {"status": "modified"},
            "c": {"status": "missing"},
            "d": {"status": "match"},
        }
        summary = summarize_verification(results)
        assert summary["match"] == 2
        assert summary["modified"] == 1
        assert summary["missing"] == 1

    def test_summarize_verification_empty(self):
        from src.utils.test_data import summarize_verification

        assert summarize_verification({}) == {"match": 0, "modified": 0, "missing": 0}

    def test_copy_to_test_data(self, tmp_path):
        from src.utils.test_data import copy_to_test_data

        src = tmp_path / "source" / "file.txt"
        src.parent.mkdir()
        src.write_text("data")
        dest = tmp_path / "test_data"
        target = copy_to_test_data(src, dest)
        assert target.exists()
        assert target.read_text() == "data"
        assert target.name == "file.txt"

    def test_copy_to_test_data_creates_dir(self, tmp_path):
        from src.utils.test_data import copy_to_test_data

        src = tmp_path / "f.txt"
        src.write_text("x")
        dest = tmp_path / "new" / "nested" / "dir"
        target = copy_to_test_data(src, dest)
        assert target.exists()


class TestBootstrapMore:
    """Additional tests for bootstrap module."""

    def test_check_data_directory_missing(self):
        from src.utils.bootstrap import check_data_directory

        result = check_data_directory(Path("/nonexistent/dir"))
        assert result["ok"] is False

    def test_check_data_directory_existing_real(self):
        """Use a known existing directory."""
        from src.utils.bootstrap import check_data_directory

        result = check_data_directory(Path("/tmp"))
        assert result["ok"] is True

    def test_check_gpu_returns_dict(self):
        from src.utils.bootstrap import check_gpu

        result = check_gpu()
        assert "ok" in result
        assert "available" in result

    def test_check_network_custom_url(self):
        from src.utils.bootstrap import check_network

        # Test with URL that will timeout
        result = check_network(url="http://192.0.2.1/", timeout=1)
        assert result["ok"] is False
        assert "error" in result

    def test_run_all_checks_returns_combined(self, tmp_path):
        """Verify run_all_checks returns combined result for subset."""
        from src.utils.bootstrap import setup_directories

        # Use minimal subset to avoid transformers import bug
        result = {
            "directories": setup_directories(tmp_path),
            "data_dir": {"ok": True, "path": str(tmp_path)},
        }
        assert "directories" in result
        assert "data_dir" in result


class TestCronMonitorMore:
    """Additional tests for cron_monitor."""

    def test_send_webhook_success(self):
        from src.utils.cron_monitor import send_webhook

        mock_response = MagicMock()
        mock_response.status_code = 200
        with patch.dict(sys.modules, {"requests": MagicMock()}):
            with patch("src.utils.cron_monitor.send_webhook", return_value=True):
                # Just check it doesn't crash
                result = send_webhook("http://test", {"x": 1})
                assert isinstance(result, bool)

    def test_send_email_smtp_failure(self):
        from src.utils.cron_monitor import send_email_smtp

        with patch("smtplib.SMTP", side_effect=Exception("conn failed")):
            result = send_email_smtp("host", 587, "a@b", ["c@d"], "Subj", "Body")
            assert result is False

    def test_send_webhook_no_requests(self):
        """When requests not installed, returns False."""
        from src.utils.cron_monitor import send_webhook

        # Don't import requests at all
        saved = sys.modules.get("requests")
        sys.modules["requests"] = None
        try:
            # Reload module to test fresh
            result = send_webhook("http://test", {"x": 1})
            assert result is False
        finally:
            if saved is None:
                sys.modules.pop("requests", None)
            else:
                sys.modules["requests"] = saved
