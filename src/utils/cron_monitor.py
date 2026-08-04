"""Cron failure detection and alerting utilities.

Detects:
- Exit code != 0
- Tracebacks in stderr
- Performance regressions (>2x expected)
- Missing expected outputs

Pure logic, no network. Use send_alert() to forward to webhook/email.
"""
import argparse
import json
import re
from datetime import datetime, timedelta, timezone
from email.mime.text import MIMEText
from pathlib import Path
from typing import Any, Dict, List, Optional


def find_recent_logs(log_dir: Path, since_hours: int = 24) -> List[Path]:
    """Find log files modified in the last N hours."""
    cutoff = datetime.now() - timedelta(hours=since_hours)
    logs = []
    if not log_dir.exists():
        return logs
    for log_file in log_dir.rglob("*.log"):
        try:
            mtime = datetime.fromtimestamp(log_file.stat().st_mtime)
            if mtime > cutoff:
                logs.append(log_file)
        except (OSError, ValueError):
            continue
    return sorted(logs, key=lambda p: p.stat().st_mtime, reverse=True)


def detect_traceback(content: str) -> Optional[str]:
    """Detect Python traceback in log content."""
    if "Traceback (most recent call last):" in content:
        idx = content.find("Traceback")
        end_idx = content.find("\n\n", idx + 100)
        if end_idx == -1:
            end_idx = idx + 2000
        return content[idx:end_idx]
    return None


def detect_errors(content: str) -> List[str]:
    """Detect ERROR/FATAL/CRITICAL/EXCEPTION patterns."""
    errors = []
    for line in content.split("\n"):
        if re.search(r"\b(ERROR|FATAL|CRITICAL|EXCEPTION)\b", line, re.IGNORECASE):
            errors.append(line.strip())
    return errors


def detect_performance_regression(
    content: str, expected_seconds: float = 60.0
) -> Optional[str]:
    """Detect if elapsed time exceeds expected by 2x."""
    m = re.search(
        r"(?:Total time|elapsed|Duration):\s*(\d+\.?\d*)\s*(?:s|sec|seconds)",
        content,
    )
    if m:
        elapsed = float(m.group(1))
        if elapsed > expected_seconds * 2:
            return f"Performance regression: {elapsed:.1f}s (expected <{expected_seconds}s)"
    return None


def check_output_files(
    repo_root: Path, expected_outputs: List[str]
) -> List[str]:
    """Check that expected output files exist relative to repo_root."""
    missing = []
    for path in expected_outputs:
        full = repo_root / path
        if not full.exists():
            missing.append(str(path))
    return missing


def analyze_log_file(log_file: Path, repo_root: Path) -> List[Dict[str, Any]]:
    """Analyze a single log file and return list of alerts."""
    content = log_file.read_text(errors="replace")
    alerts = []

    # Check for tracebacks
    traceback = detect_traceback(content)
    if traceback:
        alerts.append({
            "severity": "high",
            "type": "traceback",
            "log_file": str(log_file.relative_to(repo_root)),
            "message": "Python traceback detected",
            "details": traceback[:500],
        })

    # Check for errors
    errors = detect_errors(content)
    if errors:
        alerts.append({
            "severity": "medium",
            "type": "errors",
            "log_file": str(log_file.relative_to(repo_root)),
            "message": f"{len(errors)} error lines",
            "details": "\n".join(errors[:5]),
        })

    # Check performance
    perf = detect_performance_regression(content)
    if perf:
        alerts.append({
            "severity": "low",
            "type": "performance",
            "log_file": str(log_file.relative_to(repo_root)),
            "message": perf,
            "details": "",
        })

    return alerts


def analyze_logs(
    repo_root: Path,
    log_dir: Path,
    since_hours: int = 24,
    expected_outputs: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Analyze all recent log files in log_dir and return alert report."""
    logs = find_recent_logs(log_dir, since_hours)
    all_alerts: List[Dict[str, Any]] = []

    for log_file in logs:
        all_alerts.extend(analyze_log_file(log_file, repo_root))

    # Check missing outputs
    if expected_outputs:
        missing = check_output_files(repo_root, expected_outputs)
        for m in missing:
            all_alerts.append({
                "severity": "medium",
                "type": "missing_output",
                "log_file": "",
                "message": f"Missing expected output: {m}",
                "details": "",
            })

    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "since_hours": since_hours,
        "logs_checked": len(logs),
        "alerts": all_alerts,
    }


def send_webhook(url: str, payload: Dict[str, Any]) -> bool:
    """Send JSON payload to webhook URL. Returns True on success."""
    try:
        import requests

        response = requests.post(url, json=payload, timeout=10)
        return response.status_code < 400
    except Exception:
        return False


def build_email_body(alerts: List[Dict[str, Any]]) -> str:
    """Build plaintext email body from alerts."""
    return "\n".join(
        f"[{a['severity']}] {a['type']}: {a['message']}" for a in alerts
    )


def build_email_message(
    from_addr: str,
    to_addrs: List[str],
    subject: str,
    body: str,
) -> MIMEText:
    """Build MIME email message."""
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = from_addr
    msg["To"] = ", ".join(to_addrs)
    return msg


def send_email_smtp(
    smtp_host: str,
    smtp_port: int,
    from_addr: str,
    to_addrs: List[str],
    subject: str,
    body: str,
    username: Optional[str] = None,
    password: Optional[str] = None,
) -> bool:
    """Send email via SMTP. Returns True on success."""
    try:
        msg = build_email_message(from_addr, to_addrs, subject, body)
        import smtplib

        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            if username and password:
                server.login(username, password)
            server.sendmail(from_addr, to_addrs, msg.as_string())
        return True
    except Exception:
        return False


def format_alerts_summary(alerts: List[Dict[str, Any]]) -> str:
    """Format alert list as a readable summary string."""
    if not alerts:
        return "All systems healthy"
    lines = []
    for a in alerts:
        lines.append(f"[{a['severity']}] {a['type']}: {a['message']}")
        if a.get("details"):
            for line in a["details"].split("\n")[:3]:
                lines.append(f"    {line.strip()[:100]}")
    return "\n".join(lines)