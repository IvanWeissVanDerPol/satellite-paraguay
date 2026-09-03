"""TDD regression tests for `infra/cost-cap.sh` Scenario 1 (compromised cron credentials).

Threat-model invariant (docs/security/threat-model.md § Scenario 1):
    "Daily cost cap (`infra/cost-cap.sh`) kills runaway spend at $5/day."

If cost-cap.sh is buggy and does not detect that the daily cap has been
exceeded, the residual risk reverts from LOW to UNMITIGATED. The whole
point of Scenario 1's mitigation is that the cap actually triggers.

These tests pin the numeric behaviour of the script. They run the script
against synthetic cost logs and assert the spend values and exit status
are correct.

Author: Erebus security-auditor (biweekly audit round 1, 2026-08-28)
Threat: Scenario 1 - Compromised cron credentials
Severity at discovery: HIGH
"""

import json
import re
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).parent.parent.resolve()
SCRIPT = REPO_ROOT / "infra" / "cost-cap.sh"
TODAY = subprocess.run(
    ["date", "-u", "+%Y-%m-%d"], capture_output=True, text=True, check=True
).stdout.strip()


def _run_cost_cap(csv_path: Path, mode: str = "--dry-run", daily_cap: str = "5.00",
                  monthly_cap: str = "50.00", alert_pct: str = "80") -> subprocess.CompletedProcess:
    """Run cost-cap.sh against a synthetic CSV log and capture JSON output."""
    env = {
        "PATH": "/usr/bin:/bin:/usr/local/bin",
        "COST_LOG_FILE": str(csv_path),
        "COST_CAP_DAILY": daily_cap,
        "COST_CAP_MONTHLY": monthly_cap,
        "COST_ALERT_PCT": alert_pct,
    }
    return subprocess.run(
        ["bash", str(SCRIPT), mode],
        capture_output=True, text=True, timeout=10, env=env,
    )


def _make_csv(tmp_path: Path, rows: list[dict]) -> Path:
    """Write a cost_log.csv with the canonical header + the given rows."""
    p = tmp_path / "cost_log.csv"
    p.write_text("date,paper_id,provider,gpu_type,duration_hr,cost_usd,status\n")
    with p.open("a") as f:
        for r in rows:
            f.write(
                f"{r.get('date', TODAY)},{r['paper_id']},{r['provider']},"
                f"{r['gpu_type']},{r['duration_hr']},{r['cost_usd']},{r['status']}\n"
            )
    return p


class TestCostCapUsesCostUsdNotDurationHr:
    """RED test: cost-cap.sh must sum the `cost_usd` column (col 6), not `duration_hr` (col 5).

    Original bug: awk used `$5` (duration_hr) instead of `$6` (cost_usd),
    so a $7.50 spend over a $5 daily cap was reported as $2.00 (40%) and
    the cap never triggered. The cost cap is Scenario 1's primary mitigation.
    """

    def test_over_daily_cap_is_detected(self, tmp_path):
        """$7.50 spend > $5 daily cap must report OVER_DAILY and exit 1."""
        csv = _make_csv(tmp_path, [
            {"paper_id": "P0001", "provider": "runpod", "gpu_type": "A100",
             "duration_hr": 2.0, "cost_usd": 7.50, "status": "active"},
        ])
        result = _run_cost_cap(csv)
        assert "OVER_DAILY" in result.stdout, (
            f"cost-cap.sh failed to detect $7.50 over $5 daily cap.\n"
            f"Output:\n{result.stdout}\n"
            f"This means Scenario 1's mitigation is UNMITIGATED."
        )
        assert result.returncode == 1, (
            f"cost-cap.sh must exit 1 on OVER_DAILY, got {result.returncode}.\n"
            f"Output:\n{result.stdout}"
        )

    def test_at_daily_cap_triggers_alert(self, tmp_path):
        """$5.00 spend == $5 daily cap must report OVER_DAILY (>= boundary)."""
        csv = _make_csv(tmp_path, [
            {"paper_id": "P0001", "provider": "runpod", "gpu_type": "A100",
             "duration_hr": 1.0, "cost_usd": 5.00, "status": "active"},
        ])
        result = _run_cost_cap(csv)
        assert "OVER_DAILY" in result.stdout, (
            f"At-cap spend ($5.00 == $5.00) must trigger OVER_DAILY.\n"
            f"Output:\n{result.stdout}"
        )

    def test_eighty_percent_triggers_alert(self, tmp_path):
        """$4.00 spend (80% of $5 daily cap) must report ALERT_DAILY and exit 1."""
        csv = _make_csv(tmp_path, [
            {"paper_id": "P0001", "provider": "runpod", "gpu_type": "A100",
             "duration_hr": 0.8, "cost_usd": 4.00, "status": "active"},
        ])
        result = _run_cost_cap(csv)
        assert "ALERT_DAILY" in result.stdout, (
            f"80% of daily cap ($4.00 / $5.00) must trigger ALERT_DAILY.\n"
            f"Output:\n{result.stdout}"
        )
        assert result.returncode == 1, (
            f"Alert threshold must exit 1, got {result.returncode}."
        )

    def test_under_cap_does_not_alert(self, tmp_path):
        """$3.00 spend (60% of $5 daily cap) must report OK and exit 0."""
        csv = _make_csv(tmp_path, [
            {"paper_id": "P0001", "provider": "runpod", "gpu_type": "A100",
             "duration_hr": 0.5, "cost_usd": 3.00, "status": "active"},
        ])
        result = _run_cost_cap(csv)
        assert result.returncode == 0, (
            f"Under-cap spend must exit 0, got {result.returncode}.\n"
            f"Output:\n{result.stdout}"
        )
        assert "Status: OK" in result.stdout, (
            f"Under-cap spend must show OK status.\nOutput:\n{result.stdout}"
        )

    def test_sums_correct_column_in_report_mode(self, tmp_path):
        """--report mode must emit numeric JSON with cost_usd (not duration_hr) summed."""
        csv = _make_csv(tmp_path, [
            {"paper_id": "P0001", "provider": "runpod", "gpu_type": "A100",
             "duration_hr": 2.0, "cost_usd": 4.00, "status": "active"},
            {"paper_id": "P0002", "provider": "vastai", "gpu_type": "A100",
             "duration_hr": 0.5, "cost_usd": 2.00, "status": "active"},
            {"paper_id": "P0003", "provider": "runpod", "gpu_type": "A100",
             "duration_hr": 0.2, "cost_usd": 0.80, "status": "active"},
        ])
        result = _run_cost_cap(csv, mode="--report")
        # Tolerate any single-line JSON variant the script emits.
        match = re.search(r"\{.*\}", result.stdout, re.DOTALL)
        assert match, f"No JSON object in --report output:\n{result.stdout}"
        report = json.loads(match.group(0))
        # Must be 4.00 + 2.00 + 0.80 = 6.80 USD, NOT 2.0 + 0.5 + 0.2 = 2.70 hours
        assert abs(report["today_spend_usd"] - 6.80) < 0.01, (
            f"today_spend_usd must be 6.80 (sum of cost_usd col 6), "
            f"got {report['today_spend_usd']}. "
            f"Wrong column being summed? See cost-cap.sh line ~66."
        )
        assert abs(report["month_spend_usd"] - 6.80) < 0.01, (
            f"month_spend_usd must be 6.80, got {report['month_spend_usd']}."
        )
        assert report["status"] == "OVER_DAILY", (
            f"$6.80 > $5 daily cap must set status=OVER_DAILY, "
            f"got status={report['status']!r}."
        )


class TestCostCapDateFiltering:
    """Sanity: date filtering works correctly (it does; keep it pinned)."""

    def test_old_dates_excluded_from_today(self, tmp_path):
        csv = _make_csv(tmp_path, [
            {"date": "2020-01-01", "paper_id": "P0001", "provider": "runpod",
             "gpu_type": "A100", "duration_hr": 100.0, "cost_usd": 999.00,
             "status": "active"},
        ])
        result = _run_cost_cap(csv, mode="--report")
        match = re.search(r"\{.*\}", result.stdout, re.DOTALL)
        report = json.loads(match.group(0))
        assert report["today_spend_usd"] == 0.0, (
            f"Old dates must not count toward today_spend_usd, got "
            f"{report['today_spend_usd']}."
        )

    def test_past_month_excluded_from_this_month(self, tmp_path):
        csv = _make_csv(tmp_path, [
            {"date": "2026-07-15", "paper_id": "P0001", "provider": "runpod",
             "gpu_type": "A100", "duration_hr": 1.0, "cost_usd": 60.00,
             "status": "active"},
        ])
        result = _run_cost_cap(csv, mode="--report")
        match = re.search(r"\{.*\}", result.stdout, re.DOTALL)
        report = json.loads(match.group(0))
        assert report["month_spend_usd"] == 0.0, (
            f"Past-month spend must not count toward month_spend_usd, got "
            f"{report['month_spend_usd']}."
        )

    def test_empty_log_is_ok(self, tmp_path):
        csv = _make_csv(tmp_path, [])  # header only
        result = _run_cost_cap(csv)
        assert result.returncode == 0
        assert "Status: OK" in result.stdout


class TestCronJobsJsonHasNoCredentials:
    """Threat-model invariant for Scenario 1:
    'API keys are stored in environment vars on the cron-runner host,
     not in the JSON.' Pin that `~/.hermes/cron/jobs.json` does not embed
    any credential value, regardless of what natural-language prompts say.
    """

    def test_jobs_json_does_not_contain_api_key_values(self):
        candidates = [
            Path.home() / ".hermes" / "cron" / "jobs.json",
            Path("/opt/data/.hermes/cron/jobs.json"),
        ]
        path = next((p for p in candidates if p.exists()), None)
        if path is None:
            pytest.skip("No cron jobs.json found on this host")
        raw = path.read_text()
        # Heuristic: a real credential value is a long (>=32 char) high-entropy
        # string. Cron slug names like "aiw-eval-gate-runner-on-agent-run" are
        # 40+ chars but use hyphens + dictionary words — exclude those.
        for m in re.finditer(r'"[A-Za-z0-9_\-]{32,}"', raw):
            value = m.group(0).strip('"')
            # UUIDs and ISO timestamps are not credentials.
            if re.fullmatch(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", value):
                continue
            if re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.*", value):
                continue
            # Cron slug names: lowercase + hyphens, contain at least 2 hyphens
            # and have no uppercase letters.  These are job names, not tokens.
            if value == value.lower() and value.count("-") >= 2 and re.search(r"[a-z]", value):
                continue
            pytest.fail(
                f"Suspicious high-entropy string in {path}: {value[:24]}…\n"
                f"This may be a leaked API key. See threat-model.md Scenario 1."
            )
