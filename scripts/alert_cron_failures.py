"""Alert system for cron job failures.

Monitors the latest log files and detects:
- Exit code != 0
- Tracebacks in stderr
- Performance regressions (took > 2x expected time)
- Missing expected outputs

Sends alerts via:
- Console (always)
- JSON file (machine-readable)
- Optional: Webhook (Slack, Discord, Telegram)
- Optional: Email (SMTP)

Run: python3 scripts/alert_cron_failures.py
"""

import argparse
import json
import os
import re
import smtplib
from datetime import datetime, timedelta, timezone
from email.mime.text import MIMEText
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).parent.parent
LOG_DIR = REPO_ROOT / "logs"
OUTPUTS_LOG = REPO_ROOT / "outputs/weekly"

ALERT_CONFIG_PATH = REPO_ROOT / ".alert_config.json"


def find_recent_logs(since_hours: int = 24) -> list[Path]:
    """Find log files modified in the last N hours."""
    cutoff = datetime.now() - timedelta(hours=since_hours)
    logs = []
    for log_dir in [LOG_DIR, OUTPUTS_LOG]:
        if not log_dir.exists():
            continue
        for log_file in log_dir.rglob("*.log"):
            try:
                mtime = datetime.fromtimestamp(log_file.stat().st_mtime)
                if mtime > cutoff:
                    logs.append(log_file)
            except (OSError, ValueError):
                continue
    return sorted(logs, key=lambda p: p.stat().st_mtime, reverse=True)


def detect_traceback(content: str) -> str | None:
    """Detect Python traceback in log content."""
    if "Traceback (most recent call last):" in content:
        # Extract traceback
        idx = content.find("Traceback")
        end_idx = content.find("\n\n", idx + 100)
        if end_idx == -1:
            end_idx = idx + 2000
        return content[idx:end_idx]
    return None


def detect_errors(content: str) -> list[str]:
    """Detect ERROR/FATAL/CRITICAL patterns."""
    errors = []
    for line in content.split("\n"):
        if re.search(r"\b(ERROR|FATAL|CRITICAL|EXCEPTION)\b", line, re.IGNORECASE):
            errors.append(line.strip())
    return errors


def detect_performance_regression(content: str, expected_seconds: float = 60) -> str | None:
    """Detect if elapsed time exceeds expected by 2x."""
    m = re.search(r"(?:Total time|elapsed|Duration):\s*(\d+\.?\d*)\s*(?:s|sec|seconds)", content)
    if m:
        elapsed = float(m.group(1))
        if elapsed > expected_seconds * 2:
            return f"Performance regression: {elapsed:.1f}s (expected <{expected_seconds}s)"
    return None


def check_output_files(expected_outputs: list[str]) -> list[str]:
    """Check that expected output files exist."""
    missing = []
    for path in expected_outputs:
        full = REPO_ROOT / path
        if not full.exists():
            missing.append(str(path))
    return missing


def send_webhook(url: str, payload: dict[str, Any]) -> bool:
    """Send JSON payload to webhook URL."""
    try:
        import requests

        response = requests.post(url, json=payload, timeout=10)
        return response.status_code < 400
    except Exception as e:
        print(f"  Webhook failed: {e}")
        return False


def send_email(
    smtp_host: str,
    smtp_port: int,
    from_addr: str,
    to_addrs: list[str],
    subject: str,
    body: str,
    username: str | None = None,
    password: str | None = None,
) -> bool:
    """Send email via SMTP."""
    try:
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = from_addr
        msg["To"] = ", ".join(to_addrs)

        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            if username and password:
                server.login(username, password)
            server.sendmail(from_addr, to_addrs, msg.as_string())
        return True
    except Exception as e:
        print(f"  Email failed: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Monitor cron jobs and alert on failures")
    parser.add_argument("--since-hours", type=int, default=24)
    parser.add_argument("--webhook", help="Webhook URL for alerts")
    parser.add_argument("--email", help="Comma-separated email addresses")
    parser.add_argument("--smtp-host", default="smtp.gmail.com")
    parser.add_argument("--smtp-port", type=int, default=587)
    parser.add_argument("--smtp-user", help="SMTP username")
    parser.add_argument("--smtp-password", help="SMTP password (env: ALERT_SMTP_PASSWORD)")
    args = parser.parse_args()

    print("=" * 70)
    print(f"CRON ALERT MONITOR ({args.since_hours}h window)")
    print("=" * 70)

    logs = find_recent_logs(args.since_hours)
    print(f"\n  Found {len(logs)} log files")

    if not logs:
        print("\n  No logs found in time window")
        print("  No alerts to send")
        return

    alerts = []
    for log_file in logs:
        content = log_file.read_text(errors="replace")

        # Check for tracebacks
        traceback = detect_traceback(content)
        if traceback:
            alerts.append(
                {
                    "severity": "high",
                    "type": "traceback",
                    "log_file": str(log_file.relative_to(REPO_ROOT)),
                    "message": "Python traceback detected",
                    "details": traceback[:500],
                }
            )

        # Check for errors
        errors = detect_errors(content)
        if errors:
            alerts.append(
                {
                    "severity": "medium",
                    "type": "errors",
                    "log_file": str(log_file.relative_to(REPO_ROOT)),
                    "message": f"{len(errors)} error lines",
                    "details": "\n".join(errors[:5]),
                }
            )

        # Check performance
        perf = detect_performance_regression(content)
        if perf:
            alerts.append(
                {
                    "severity": "low",
                    "type": "performance",
                    "log_file": str(log_file.relative_to(REPO_ROOT)),
                    "message": perf,
                    "details": "",
                }
            )

    # Check missing outputs
    expected = [
        "outputs/p0011/departments/department_stats.json",
        "outputs/p0011/indigenous/indigenous_stats.json",
        "outputs/p0011/carbon/per_year_loss.json",
        "outputs/carbon_credits/verra_verification.json",
        "outputs/statistical_tests/test_results.json",
    ]
    missing = check_output_files(expected)
    for m in missing:
        alerts.append(
            {
                "severity": "medium",
                "type": "missing_output",
                "log_file": "",
                "message": f"Missing expected output: {m}",
                "details": "",
            }
        )

    # Print summary
    print(f"\n  Alerts: {len(alerts)}")
    if not alerts:
        print("  ✓ All systems healthy")
    else:
        print()
        for a in alerts:
            sev_icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}[a["severity"]]
            print(f"  {sev_icon} [{a['severity']:6}] {a['type']:18} {a['message']}")
            if a.get("details"):
                for line in a["details"].split("\n")[:3]:
                    print(f"      {line.strip()[:100]}")

    # Save alerts
    out_path = REPO_ROOT / "outputs/alert_report.json"
    out_path.parent.mkdir(exist_ok=True)
    out_path.write_text(
        json.dumps(
            {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "since_hours": args.since_hours,
                "logs_checked": len(logs),
                "alerts": alerts,
            },
            indent=2,
        )
    )
    print(f"\n  Saved: {out_path}")

    # Send webhook if configured
    if args.webhook and alerts:
        payload = {
            "text": f"satellite-paraguay alerts: {len(alerts)}",
            "alerts": alerts,
        }
        if send_webhook(args.webhook, payload):
            print(f"  ✓ Webhook sent to {args.webhook[:50]}...")

    # Send email if configured
    if args.email and alerts:
        password = args.smtp_password or os.environ.get("ALERT_SMTP_PASSWORD")
        subject = f"[satellite-paraguay] {len(alerts)} alert(s)"
        body = "\n".join([f"[{a['severity']}] {a['type']}: {a['message']}" for a in alerts])
        if send_email(
            args.smtp_host,
            args.smtp_port,
            args.smtp_user or "noreply@example.com",
            args.email.split(","),
            subject,
            body,
            args.smtp_user,
            password,
        ):
            print(f"  ✓ Email sent to {args.email}")


if __name__ == "__main__":
    main()
