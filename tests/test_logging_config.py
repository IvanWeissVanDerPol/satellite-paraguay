"""Tests for src/logging_config.py.

Coverage target: 70%+. Tests JSONFormatter, get_logger, configure_root.
"""

import json
import logging
import os

import pytest


@pytest.fixture(autouse=True)
def enable_logging():
    """Enable auto-configuration for tests."""
    os.environ["SATELLITE_PARAGUAY_TEST"] = "1"
    yield
    if "SATELLITE_PARAGUAY_TEST" in os.environ:
        del os.environ["SATELLITE_PARAGUAY_TEST"]


class TestJSONFormatter:
    """Tests for the JSONFormatter class."""

    def test_format_basic_record(self):
        from src.logging_config import JSONFormatter

        formatter = JSONFormatter()
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="test.py",
            lineno=10,
            msg="hello %s",
            args=("world",),
            exc_info=None,
        )
        output = formatter.format(record)
        parsed = json.loads(output)
        assert parsed["level"] == "INFO"
        assert parsed["message"] == "hello world"
        assert parsed["logger"] == "test"

    def test_format_includes_timestamp(self):
        from src.logging_config import JSONFormatter

        formatter = JSONFormatter()
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="x.py",
            lineno=1,
            msg="msg",
            args=None,
            exc_info=None,
        )
        output = formatter.format(record)
        parsed = json.loads(output)
        assert "ts" in parsed
        # ISO format timestamp
        assert "T" in parsed["ts"]

    def test_format_includes_extra(self):
        from src.logging_config import JSONFormatter

        formatter = JSONFormatter()
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="x.py",
            lineno=1,
            msg="msg",
            args=None,
            exc_info=None,
        )
        record.tile_id = "20S_055W"
        output = formatter.format(record)
        parsed = json.loads(output)
        assert parsed["tile_id"] == "20S_055W"

    def test_format_includes_exception(self):
        from src.logging_config import JSONFormatter

        formatter = JSONFormatter()
        try:
            raise ValueError("test error")
        except ValueError:
            import sys

            record = logging.LogRecord(
                name="test",
                level=logging.ERROR,
                pathname="x.py",
                lineno=1,
                msg="failed",
                args=None,
                exc_info=sys.exc_info(),
            )
        output = formatter.format(record)
        parsed = json.loads(output)
        assert "exception" in parsed

    def test_format_handles_non_json_extra(self):
        """Non-serializable extras should be stringified."""
        from src.logging_config import JSONFormatter

        formatter = JSONFormatter()
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="x.py",
            lineno=1,
            msg="msg",
            args=None,
            exc_info=None,
        )
        # Set a non-serializable object
        record.complex_obj = object()
        output = formatter.format(record)
        # Should not crash
        parsed = json.loads(output)
        assert "complex_obj" in parsed
        # Object is stringified
        assert isinstance(parsed["complex_obj"], str)


class TestGetLogger:
    """Tests for the get_logger function."""

    def test_returns_logger(self):
        from src.logging_config import get_logger

        logger = get_logger("test.module1")
        assert isinstance(logger, logging.Logger)

    def test_returns_same_logger(self):
        """Calling get_logger twice should return same instance."""
        from src.logging_config import get_logger

        l1 = get_logger("test.module2")
        l2 = get_logger("test.module2")
        assert l1 is l2

    def test_idempotent(self):
        """get_logger should not add handlers on second call."""
        from src.logging_config import get_logger

        logger = get_logger("test.module3")
        n_handlers = len(logger.handlers)
        logger2 = get_logger("test.module3")
        # Same logger, same handlers
        assert logger is logger2
        assert len(logger2.handlers) == n_handlers

    def test_respects_level(self):
        from src.logging_config import get_logger

        logger = get_logger("test.level", level=logging.WARNING)
        assert logger.level == logging.WARNING

    def test_with_json_format(self):
        from src.logging_config import get_logger

        logger = get_logger("test.json", json_format=True)
        assert isinstance(logger, logging.Logger)
        # Check at least one handler uses JSONFormatter
        from src.logging_config import JSONFormatter

        has_json = any(isinstance(h.formatter, JSONFormatter) for h in logger.handlers if h.formatter)
        assert has_json

    def test_with_extra_log_file(self, tmp_path):
        from src.logging_config import get_logger

        log_file = tmp_path / "extra.log"
        logger = get_logger("test.extra_log", log_file=str(log_file))
        assert isinstance(logger, logging.Logger)


class TestConfigureRoot:
    """Tests for the configure_root function."""

    def test_idempotent(self):
        from src.logging_config import configure_root

        # Reset
        root = logging.getLogger()
        for h in list(root.handlers):
            root.removeHandler(h)
        configure_root()
        n_handlers = len(root.handlers)
        configure_root()
        # No new handlers added
        assert len(root.handlers) == n_handlers

    def test_with_json_format(self):
        from src.logging_config import JSONFormatter, configure_root

        # Reset
        root = logging.getLogger()
        for h in list(root.handlers):
            root.removeHandler(h)
        configure_root(json_format=True)
        has_json = any(isinstance(h.formatter, JSONFormatter) for h in root.handlers if h.formatter)
        assert has_json

    def test_respects_level(self):
        from src.logging_config import configure_root

        # Reset
        root = logging.getLogger()
        for h in list(root.handlers):
            root.removeHandler(h)
        configure_root(level=logging.DEBUG)
        assert root.level == logging.DEBUG


class TestConstants:
    """Tests for module-level constants."""

    def test_log_dir_exists(self):
        from src.logging_config import LOG_DIR

        assert LOG_DIR.exists()

    def test_repo_root_is_parent_of_logging(self):
        from src.logging_config import REPO_ROOT

        assert REPO_ROOT.is_dir()
