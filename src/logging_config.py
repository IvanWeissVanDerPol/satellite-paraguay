"""Structured logging for satellite-paraguay.

Provides:
- Module-level logger (`get_logger(__name__)`)
- Rotating file handler (logs/satellite-paraguay.log)
- JSON-structured logs for programmatic parsing
- Optional stderr capture for cron jobs
- Per-paper, per-script, per-stage loggers

Usage:
    from src.logging_config import get_logger
    logger = get_logger(__name__)
    logger.info("processing", extra={"tile": "20S_060W"})
"""

import json
import logging
import logging.handlers
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
LOG_DIR = REPO_ROOT / "logs"
LOG_DIR.mkdir(exist_ok=True)


class JSONFormatter(logging.Formatter):
    """Format log records as JSON for structured logging."""

    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "ts": datetime.fromtimestamp(record.created, tz=timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "func": record.funcName,
            "line": record.lineno,
        }
        # Add extra fields
        for key, val in record.__dict__.items():
            if key not in (
                "name",
                "msg",
                "args",
                "levelname",
                "levelno",
                "pathname",
                "filename",
                "module",
                "exc_info",
                "exc_text",
                "stack_info",
                "lineno",
                "funcName",
                "created",
                "msecs",
                "relativeCreated",
                "thread",
                "threadName",
                "processName",
                "process",
                "message",
                "taskName",
            ):
                try:
                    json.dumps(val)
                    payload[key] = val
                except (TypeError, ValueError):
                    payload[key] = str(val)
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        return json.dumps(payload, ensure_ascii=False)


def get_logger(
    name: str,
    level: int = logging.INFO,
    log_file: str | None = None,
    json_format: bool = False,
) -> logging.Logger:
    """Get a configured logger.

    Args:
        name: Logger name (typically __name__)
        level: Logging level
        log_file: Optional file path for additional log file
        json_format: If True, emit JSON-structured logs
    """
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger  # Already configured

    logger.setLevel(level)
    logger.propagate = False

    if json_format:
        fmt = JSONFormatter()
    else:
        fmt = logging.Formatter(  # type: ignore[assignment]
            "%(asctime)s [%(levelname)8s] %(name)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

    # Console handler
    console = logging.StreamHandler(sys.stderr)
    console.setLevel(level)
    console.setFormatter(fmt)
    logger.addHandler(console)

    # Rotating file handler (10 MB, 5 backups)
    log_file_default = LOG_DIR / f"{name.replace('.', '_')}.log"
    try:
        file_handler = logging.handlers.RotatingFileHandler(
            log_file_default,
            maxBytes=10 * 1024 * 1024,  # 10 MB
            backupCount=5,
            encoding="utf-8",
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(fmt)
        logger.addHandler(file_handler)
    except (OSError, PermissionError):
        # Logs dir not writable, skip file handler
        pass

    # Optional extra log file
    if log_file:
        try:
            extra = logging.FileHandler(log_file)
            extra.setLevel(logging.DEBUG)
            extra.setFormatter(fmt)
            logger.addHandler(extra)
        except (OSError, PermissionError):
            pass

    return logger


def configure_root(level: int = logging.INFO, json_format: bool = False) -> None:
    """Configure root logger once for the entire process."""
    root = logging.getLogger()
    if root.handlers:
        return
    root.setLevel(level)

    fmt = (
        JSONFormatter()
        if json_format
        else logging.Formatter(
            "%(asctime)s [%(levelname)8s] %(name)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    )

    console = logging.StreamHandler(sys.stderr)
    console.setLevel(level)
    console.setFormatter(fmt)
    root.addHandler(console)

    file_handler = logging.handlers.RotatingFileHandler(
        LOG_DIR / "satellite-paraguay.log",
        maxBytes=10 * 1024 * 1024,
        backupCount=10,
        encoding="utf-8",
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(fmt)
    root.addHandler(file_handler)


# Auto-configure on import
if os.environ.get("SATELLITE_PARAGUAY_TEST") != "1":
    configure_root(level=os.environ.get("SATELLITE_PARAGUAY_LOG_LEVEL", "INFO"))  # type: ignore[arg-type]
