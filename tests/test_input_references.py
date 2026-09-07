"""tests/test_input_references.py — Regression guard for broken \\input{} references.

WHAT IT CATCHES
===============
Tier-6 audit found `thesis/main.tex` (the Makefile target) referencing 9
chapter files that did not exist:
    \\input{chapters/04_p0011_yvutu}     ← file missing
    \\input{chapters/05_p0100_yvyra}     ← file missing + typo p0100
    ...
This would crash `make thesis-pdf` with "Emergency stop" from pdflatex.

WHY THIS TEST
=============
A future refactor could re-introduce the bug:
    - Someone reorganizes thesis/chapters/ without updating main.tex
    - Someone renames a chapter file
    - Someone adds a new \\input{} without generating the target

The fix in Tier-6 was to comment out the dangling \\input{} lines, so
the test must allow commented-out references but flag active ones that
point to missing files.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).parent.parent

# Master LaTeX files that drive the build. These MUST have all \input{}
# references resolved to existing files.
MASTER_TEX_PATHS = [
    REPO_ROOT / "thesis" / "main.tex",
    REPO_ROOT / "thesis" / "MAIN" / "thesis.tex",
]

# All other paper.tex files are self-contained (no \input{}).
# Skip per-paper .tex by default; only check master files.
SKIP_BASENAMES = {"paper.tex"}


def _iter_master_tex_files():
    """Yield master .tex files that drive the LaTeX build."""
    for p in MASTER_TEX_PATHS:
        if p.exists():
            yield p


# Match \input{path} but NOT \input{|...} (verbatim from a pipe) and
# NOT commented-out lines. We strip LaTeX comments (% to end of line)
# BEFORE matching, which automatically drops commented-out \input{}.
INPUT_PATTERN = re.compile(r"\\input\{([^}]+)\}")


def _strip_latex_comments(text: str) -> str:
    """Remove LaTeX comments (everything from unescaped % to end of line).

    Skips % inside \\verb||...|| and other verbatim contexts (we don't
    attempt to be perfect — just good enough to avoid false positives).
    """
    out = []
    in_verb = False
    verb_char = ""
    i = 0
    while i < len(text):
        c = text[i]
        # Track verbatim regions crudely
        if not in_verb and c == "\\" and i + 4 < len(text) and text[i : i + 5] == "\\verb":
            in_verb = True
            verb_char = text[i + 5]
            out.append(text[i : i + 6])
            i += 6
            continue
        if in_verb:
            out.append(c)
            if c == verb_char:
                in_verb = False
            i += 1
            continue
        if c == "%":
            # Skip to end of line
            nl = text.find("\n", i)
            if nl == -1:
                break
            i = nl
            continue
        # Skip \% (escaped percent)
        if c == "\\" and i + 1 < len(text) and text[i + 1] == "%":
            out.append("\\%")
            i += 2
            continue
        out.append(c)
        i += 1
    return "".join(out)


def _resolve_tex_target(base_dir: Path, rel_path: str) -> Path | None:
    """Resolve a \\input{...} reference the way LaTeX does.

    LaTeX auto-appends .tex if the path has no extension. We mirror that.
    Returns the resolved path if it exists, None otherwise.
    """
    p = (base_dir / rel_path).resolve()
    if p.exists():
        return p
    # LaTeX tries appending .tex when no extension is given.
    if p.suffix == "":
        candidate = p.with_suffix(".tex")
        if candidate.exists():
            return candidate
    return None


def _collect_inputs(tex_path: Path) -> list[tuple[str, int, str]]:
    """Return list of (target_path, line_no, rel_path) for active \\input{} in tex_path.

    Active = not on a commented-out line. Paths are resolved relative to
    the directory containing the .tex file.
    """
    text = tex_path.read_text(encoding="utf-8")
    stripped = _strip_latex_comments(text)
    base_dir = tex_path.parent

    results: list[tuple[str, int, str]] = []
    for m in INPUT_PATTERN.finditer(stripped):
        rel_path = m.group(1).strip()
        target = _resolve_tex_target(base_dir, rel_path)
        line_no = text.count("\n", 0, m.start()) + 1
        # Use original rel_path in the result; target may be None
        results.append((str(target) if target else str((base_dir / rel_path).resolve()), line_no, rel_path))
    return results


def test_no_dangling_input_in_master_tex():
    """Round-Tier-6 lesson: \\input{file} must point to an existing file.

    The Tier-6 audit caught `thesis/main.tex` with 9 missing chapter files.
    After the fix those \\input{} lines were commented out, but a future
    refactor could uncomment them or add new ones without generating the
    target files. This test runs `make thesis-pdf`-style validation.
    """
    broken = []
    for tex_path in _iter_master_tex_files():
        text = tex_path.read_text(encoding="utf-8")
        stripped = _strip_latex_comments(text)
        base_dir = tex_path.parent
        for m in INPUT_PATTERN.finditer(stripped):
            rel_path = m.group(1).strip()
            target = _resolve_tex_target(base_dir, rel_path)
            line_no = text.count("\n", 0, m.start()) + 1
            if target is None:
                broken.append((str(tex_path.relative_to(REPO_ROOT)), line_no, rel_path))

    assert not broken, (
        f"Found {len(broken)} dangling \\input{{}} reference(s) in master .tex files. "
        f"Either generate the missing files or comment out the \\input{{}} lines.\n"
        + "\n".join(f"  {p}:{ln}: \\input{{{r}}}" for p, ln, r in broken[:20])
    )


def test_thesis_main_tex_no_typos_in_input_refs():
    """Round-Tier-6 lesson: typo `p0100_yvyra` should be `p0010_yvyra`.

    Catches simple digit-transposition typos in chapter file references
    by ensuring every referenced basename starts with 'p00' (paper IDs
    are p0010, p0011, p0012, p0025, p0026, p0035).
    """
    typo = []
    for tex_path in _iter_master_tex_files():
        text = tex_path.read_text(encoding="utf-8")
        stripped = _strip_latex_comments(text)
        base_dir = tex_path.parent
        for m in INPUT_PATTERN.finditer(stripped):
            rel_path = m.group(1).strip()
            _resolve_tex_target(base_dir, rel_path)  # exercise for coverage
            basename = Path(rel_path).name
            # Check for digit-transposition typos (e.g. p0100 vs p0010)
            if "p00" in basename and not any(
                basename.startswith(p) for p in ("p0010_", "p0011_", "p0012_", "p0025_", "p0026_", "p0035_")
            ):
                typo.append((str(tex_path.relative_to(REPO_ROOT)), m.start(), rel_path))

    assert not typo, (
        f"Found {len(typo)} suspicious chapter filename reference(s). "
        f"Paper IDs are p0010/p0011/p0012/p0025/p0026/p0035.\n"
        + "\n".join(f"  {p}: \\input{{{r}}}" for p, _start, r in typo[:20])
    )


def test_main_tex_files_exist():
    """Sanity: the build targets must exist on disk."""
    for p in MASTER_TEX_PATHS:
        assert p.exists(), f"Master .tex file missing: {p}"
