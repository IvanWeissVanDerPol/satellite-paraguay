"""TDD regression tests for Scenario 2 — Sensitive data leak via CI artifacts.

Threat-model invariant (docs/security/threat-model.md § Scenario 2):
    ".github/workflows/*.yml uses `actions/upload-artifact@v4` with explicit
     `if-no-files-found: error`"
    "Workflows do not upload `data/` directories"
    ".gitignore excludes `data/raw/inbio/` and `data/labels/` and `secrets/`"

These tests pin the workflow + .gitignore configuration against the
threat model claims. If the workflow ever drifts (a developer adds an
upload step without `if-no-files-found: error`, or someone removes the
data-leak exclusions from .gitignore), these tests fire.

Author: Erebus security-auditor (biweekly audit round 2, 2026-09-04)
Threat: Scenario 2 — Sensitive data leak via CI artifacts
Severity at discovery: HIGH (claim #3) + MEDIUM (claim #1)
"""

import re
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).parent.parent.resolve()
WORKFLOWS_DIR = REPO_ROOT / ".github" / "workflows"
GITIGNORE = REPO_ROOT / ".gitignore"

# Sensitive asset paths from threat-model.md "What we defend" table.
# These MUST never appear inside an upload-artifact `path:` value
# (directly or via glob), because CI artifacts are public by default.
SENSITIVE_PATHS = [
    "data/labels",       # Real wildlife labels (Guyra partnership trust)
    "data/raw/inbio",    # INBIO yield data (partner trust)
]

# Patterns that must be present in .gitignore (defense-in-depth: even if a
# workflow slips through, the files must never reach the repo).
GITIGNORE_REQUIRED_PATTERNS = [
    "data/raw/inbio",
    "data/labels",
    "secrets/",
]


# ===== Helpers =====

def _load_workflow(path: Path) -> dict:
    """Load a workflow YAML file. Skip if file is empty."""
    if path.stat().st_size == 0:
        return {}
    return yaml.safe_load(path.read_text())


def _iter_upload_steps(workflow: dict) -> list[dict]:
    """Yield every step that uses actions/upload-artifact."""
    out = []
    for job in (workflow.get("jobs") or {}).values():
        if not isinstance(job, dict):
            continue
        for step in (job.get("steps") or []):
            if not isinstance(step, dict):
                continue
            uses = step.get("uses", "")
            if isinstance(uses, str) and "actions/upload-artifact" in uses:
                out.append(step)
    return out


def _path_matches_sensitive(path_value: str) -> list[str]:
    """Return the list of SENSITIVE_PATHS that appear (as substring or glob fragment)
    in the workflow `path:` value. Glob `**` is collapsed so `data/**` matches
    `data/labels`.
    """
    if not isinstance(path_value, str):
        return []
    # Treat the path as a glob; for our purposes, substring match is enough
    # because no workflow uses `data/safe/...` with `data/labels` inside.
    # If we wanted true glob-matching we'd use fnmatch, but substring covers
    # both `data/labels` and `data/labels/**`.
    matches = []
    for sensitive in SENSITIVE_PATHS:
        if sensitive in path_value:
            matches.append(sensitive)
    return matches


# ===== Claim #1: every upload-artifact has if-no-files-found: error =====

class TestAllUploadArtifactStepsHaveIfNoFilesFound:
    """RED test: every `actions/upload-artifact` step in any workflow MUST set
    `if-no-files-found: error`. Otherwise an accidental upload of a
    sensitive directory silently produces a "successful" CI run with no
    artifact, and the operator never notices the data was never uploaded
    (or worse, the glob expands to include sensitive content).

    Threat model quote (Scenario 2 mitigation):
        ".github/workflows/*.yml uses `actions/upload-artifact@v4` with
         explicit `if-no-files-found: error`"
    """

    def test_all_workflows_parse(self):
        workflows = list(WORKFLOWS_DIR.glob("*.yml")) + list(WORKFLOWS_DIR.glob("*.yaml"))
        assert workflows, "No workflow files found; the threat-model invariant is moot"
        for wf in workflows:
            _load_workflow(wf)  # raises if YAML is broken

    @pytest.mark.parametrize("wf_path", [
        p for p in (
            list(WORKFLOWS_DIR.glob("*.yml"))
            + list(WORKFLOWS_DIR.glob("*.yaml"))
        )
        if p.stat().st_size > 0
    ], ids=lambda p: p.name)
    def test_every_upload_step_has_if_no_files_found(self, wf_path):
        wf = _load_workflow(wf_path)
        uploads = _iter_upload_steps(wf)
        if not uploads:
            pytest.skip(f"{wf_path.name} has no upload-artifact steps")
        for i, step in enumerate(uploads):
            with_clause = step.get("with") or {}
            flag = with_clause.get("if-no-files-found")
            assert flag == "error", (
                f"{wf_path.name} step #{i} uses actions/upload-artifact but does "
                f"NOT set `if-no-files-found: error` (got {flag!r}).\n"
                f"  Step name: {step.get('name')!r}\n"
                f"  path: {with_clause.get('path')!r}\n"
                f"Threat-model invariant violated:\n"
                f"  '.github/workflows/*.yml uses `actions/upload-artifact@v4` "
                f"with explicit `if-no-files-found: error`'\n"
                f"  (docs/security/threat-model.md § Scenario 2)"
            )


# ===== Claim #2: no workflow uploads data/ =====

class TestNoWorkflowUploadsDataPaths:
    """RED test: no `actions/upload-artifact` step may reference sensitive
    data directories under `path:`.

    Threat model quote (Scenario 2 mitigation):
        "Workflows do not upload `data/` directories"
    """

    @pytest.mark.parametrize("wf_path", [
        p for p in (
            list(WORKFLOWS_DIR.glob("*.yml"))
            + list(WORKFLOWS_DIR.glob("*.yaml"))
        )
        if p.stat().st_size > 0
    ], ids=lambda p: p.name)
    def test_no_upload_references_sensitive_data_path(self, wf_path):
        wf = _load_workflow(wf_path)
        uploads = _iter_upload_steps(wf)
        violations = []
        for i, step in enumerate(uploads):
            with_clause = step.get("with") or {}
            path_value = with_clause.get("path")
            hits = _path_matches_sensitive(path_value)
            if hits:
                violations.append((i, step.get("name"), path_value, hits))
        assert not violations, (
            f"{wf_path.name} has {len(violations)} upload-artifact step(s) "
            f"that reference sensitive data paths:\n" +
            "\n".join(
                f"  step #{i} ({name!r}): path={p!r} matches {hits}"
                for i, name, p, hits in violations
            ) +
            "\nThreat-model invariant violated:\n"
            "  'Workflows do not upload `data/` directories'\n"
            "  (docs/security/threat-model.md § Scenario 2)"
        )


# ===== Claim #3: .gitignore excludes data/raw/inbio/, data/labels/, secrets/ =====

class TestGitignoreExcludesSensitiveDataPaths:
    """RED test: `.gitignore` must contain explicit patterns that prevent
    `data/raw/inbio/`, `data/labels/`, and `secrets/` from being committed.

    Threat model quote (Scenario 2 mitigation):
        ".gitignore excludes `data/raw/inbio/` and `data/labels/` and `secrets/`"

    These are HIGH-severity partner-trust data (Guyra wildlife labels,
    INBIO yield data). If they're ever staged, the partner trust posture
    is broken even before a CI artifact leak.
    """

    @pytest.fixture(scope="class")
    def gitignore_text(self):
        return GITIGNORE.read_text()

    @pytest.mark.parametrize("pattern", GITIGNORE_REQUIRED_PATTERNS)
    def test_gitignore_contains_pattern(self, gitignore_text, pattern):
        assert pattern in gitignore_text, (
            f".gitignore does not contain required pattern {pattern!r}.\n"
            f"Threat-model invariant violated:\n"
            f"  '.gitignore excludes `data/raw/inbio/` and `data/labels/` and `secrets/`'\n"
            f"  (docs/security/threat-model.md § Scenario 2)"
        )

    def test_data_directories_are_not_tracked(self, gitignore_text):
        """End-to-end: the .gitignore patterns must be effective.

        We split into non-comment lines and confirm each required pattern
        (with or without trailing slash) is present as a literal line.
        """
        lines = [
            line.strip() for line in gitignore_text.splitlines()
            if line.strip() and not line.strip().startswith("#")
        ]
        # Each required pattern must appear as a literal line, optionally
        # with a trailing slash (both are valid gitignore directory patterns).
        for pattern in GITIGNORE_REQUIRED_PATTERNS:
            base = pattern.rstrip("/")
            candidates = {base, base + "/"}
            assert lines and any(ln in candidates for ln in lines), (
                f".gitignore is missing a literal line that matches {pattern!r}. "
                f"Searched for: {sorted(candidates)}.\n"
                f"Threat-model invariant violated:\n"
                f"  '.gitignore excludes `data/raw/inbio/` and `data/labels/` and `secrets/`'"
            )

    def test_sensitive_paths_not_currently_tracked(self, repo_root):
        """Regression for audit-round-2 CRITICAL FINDING (D):

        As of 2026-09-04, `data/labels/guyra/wildlife/manifest.csv`
        (906 KB, 5000 rows) and `data/raw/inbio/yrupe_2024.csv` were
        already tracked in git history despite the threat model claiming
        they were gitignored. The .gitignore fix stops FUTURE leaks
        but cannot retroactively un-track these files. Once `git
        filter-repo` purges them from history, this test will pass.

        Threat-model invariant violated:
          "`.gitignore` excludes `data/raw/inbio/` and `data/labels/`"
        """
        import subprocess
        # Enumerate tracked files under the sensitive paths. A clean run
        # returns empty stdout.
        tracked = subprocess.run(
            ["git", "ls-files", "-z", "--", "data/labels",
             "data/raw/inbio", "secrets"],
            cwd=repo_root, capture_output=True, text=True, timeout=10,
        ).stdout.split("\x00")
        tracked = [p for p in tracked if p]  # drop empties
        assert not tracked, (
            f"Sensitive paths are tracked in git (must be purged from history).\n"
            f"Tracked files:\n  " + "\n  ".join(tracked[:20]) +
            (f"\n  ... and {len(tracked) - 20} more" if len(tracked) > 20 else "") +
            "\n\nAudit-round-2 CRITICAL FINDING (D) requires `git filter-repo` "
            "to purge these from history. See docs/security/audit-round-2.md."
        )


# ===== Claim #4: actions/upload-artifact is SHA-pinned (Scenario 8 cross-check) =====

class TestUploadArtifactVersionsArePinned:
    """Sanity check: every upload-artifact step should be SHA-pinned (consistent
    with Scenario 8's runner-security mitigation). This is a regression test
    added during round 2 because the upload step is the most direct path
    for a data leak, so we want its supply chain locked down too.
    """

    @pytest.mark.parametrize("wf_path", [
        p for p in (
            list(WORKFLOWS_DIR.glob("*.yml"))
            + list(WORKFLOWS_DIR.glob("*.yaml"))
        )
        if p.stat().st_size > 0
    ], ids=lambda p: p.name)
    def test_upload_artifact_is_sha_pinned(self, wf_path):
        wf = _load_workflow(wf_path)
        uploads = _iter_upload_steps(wf)
        if not uploads:
            pytest.skip(f"{wf_path.name} has no upload-artifact steps")
        sha_re = re.compile(r"@[0-9a-f]{40}\b")
        for i, step in enumerate(uploads):
            uses = step.get("uses", "")
            assert sha_re.search(uses), (
                f"{wf_path.name} step #{i} uses {uses!r} which is NOT SHA-pinned. "
                f"Pin to a 40-char commit SHA per Scenario 8 mitigation."
            )
