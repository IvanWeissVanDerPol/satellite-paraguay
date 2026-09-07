"""tests/test_latex_safety.py — Regression guard for Tier-6 LaTeX compile-breakers.

WHAT IT CATCHES
===============
Tier-6 audit found 3 LaTeX bugs that would crash pdflatex silently
(or with confusing "Emergency stop" errors):

  1. **%-in-braces** bug: `\\textbf{90%+ of Verra's ...}` — the unescaped
     `%` starts a comment that swallows the closing `}`, so the rest of
     the document parses incorrectly. Affects p0010, p0012, p0026.

  2. **\\citep without natbib** bug: `\\citep{key}` requires
     `\\usepackage{natbib}`. Affects p0010, p0026.

  3. **Bare % in inline text** less critical but still noise: `22%`
     should be `22\\%`.

WHY THIS TEST
=============
A future paper author could re-introduce these bugs without realising.
The existing check_latex.py does brace-balancing but does not detect
%-in-braces (since from a brace perspective the opening and closing
braces still match — the bug is semantic, not syntactic).
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable

import pytest

REPO_ROOT = Path(__file__).parent.parent

# All paper.tex files + main thesis.tex files.
PAPER_TEX_GLOB = "papers/drafts"
MAIN_TEX_GLOB = "thesis"

SKIP_BASENAMES = {"paper.bbl"}


def _iter_tex_files() -> Iterable[Path]:
    """Yield all .tex files under papers/drafts/ and thesis/.

    Skip thesis/chapters/*.tex — those are \\input{} fragments whose
    preamble comes from thesis/MAIN/thesis.tex, not standalone files.
    """
    for sub in (PAPER_TEX_GLOB, MAIN_TEX_GLOB):
        base = REPO_ROOT / sub
        if not base.exists():
            continue
        for p in base.rglob("*.tex"):
            if p.name in SKIP_BASENAMES:
                continue
            # Skip chapter fragments — they're not compilable on their own
            if "thesis/chapters/" in str(p.relative_to(REPO_ROOT)):
                continue
            yield p


def _strip_latex_comments(text: str) -> str:
    """Remove LaTeX comments (everything from unescaped % to end of line).

    Skips \\% (escaped percent), \\verb||...||, and other verbatim contexts.
    """
    out = []
    in_verb = False
    verb_char = ""
    i = 0
    while i < len(text):
        c = text[i]
        if not in_verb and c == "\\" and i + 5 < len(text) and text[i : i + 5] == "\\verb":
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
            # Check if escaped
            if i > 0 and text[i - 1] == "\\":
                out.append("%")
                i += 1
                continue
            # Skip to end of line
            nl = text.find("\n", i)
            if nl == -1:
                break
            i = nl
            continue
        out.append(c)
        i += 1
    return "".join(out)


# =====================================================================
# TEST 1: %-in-braces bug
#
# Pattern: a LaTeX command argument like \textbf{X%Y} where the % is
# not escaped. LaTeX treats %Y} as a comment, so the argument is
# never closed.
# =====================================================================

# Match \command{...%...} where % is NOT preceded by a backslash (i.e. is
# truly unescaped). LaTeX treats % as a comment, so an unescaped % inside
# a command argument swallows the closing brace. A `\%` is fine — it's
# the LaTeX-escaped percent sign and prints as "%".
#
# Implementation: walk character-by-character inside each {...} argument
# and look for `%` whose previous non-whitespace char is not `\`.

def _iter_command_arguments(text: str):
    """Yield (cmd_name, body_start, body_end, full_match_end) for each \\cmd{...} arg.

    Skips verbatim contexts and arguments containing nested braces
    (we recurse on inner braces via a simple depth counter, but stop
    on unbalanced input).
    """
    i = 0
    n = len(text)
    in_verb = False
    verb_char = ""
    while i < n:
        c = text[i]
        # Track verbatim
        if not in_verb and c == "\\" and i + 5 < n and text[i : i + 5] == "\\verb":
            in_verb = True
            if i + 5 < n:
                verb_char = text[i + 5]
            i += 6
            continue
        if in_verb:
            if c == verb_char:
                in_verb = False
            i += 1
            continue
        # Skip LaTeX comments
        if c == "%" and (i == 0 or text[i - 1] != "\\"):
            nl = text.find("\n", i)
            if nl == -1:
                break
            i = nl
            continue
        # Detect \cmd{
        if c == "\\" and i + 1 < n and text[i + 1].isalpha():
            # Find command name
            j = i + 1
            while j < n and text[j].isalpha():
                j += 1
            cmd = text[i + 1 : j]
            # Skip whitespace
            while j < n and text[j] in " \t":
                j += 1
            if j < n and text[j] == "{":
                # Find matching closing brace (single level of nesting)
                depth = 1
                k = j + 1
                while k < n and depth > 0:
                    if text[k] == "{":
                        depth += 1
                    elif text[k] == "}":
                        depth -= 1
                    elif text[k] == "%" and (k == 0 or text[k - 1] != "\\"):
                        # LaTeX comment
                        nl = text.find("\n", k)
                        k = nl if nl != -1 else n
                        continue
                    k += 1
                if depth == 0:
                    yield (cmd, j + 1, k - 1, k)
                i = k
                continue
        i += 1


def test_no_unescaped_percent_in_command_arguments():
    """Round-Tier-6 lesson: \\textbf{X%Y} silently swallows the closing brace.

    Found 3 instances in p0010, p0012, p0026 before Tier-6. Each one
    made the rest of the document compile incorrectly.

    An UNESCAPED % (preceded by something other than \\) inside a
    command argument starts a comment that runs to end-of-line. The
    closing } is then part of the comment, so the command is never
    closed.
    """
    findings = []
    for tex_path in _iter_tex_files():
        text = tex_path.read_text(encoding="utf-8")
        for cmd, body_start, body_end, _ in _iter_command_arguments(text):
            body = text[body_start:body_end]
            # Walk body and find % whose previous non-whitespace char is NOT \
            for m in re.finditer(r"(?<!\\)%", body):
                # Double-check: the previous char in raw text isn't \
                abs_pos = body_start + m.start()
                if abs_pos > 0 and text[abs_pos - 1] == "\\":
                    continue
                # Whitelist certain commands
                if cmd in ("includegraphics", "url", "href"):
                    continue
                line_no = text.count("\n", 0, abs_pos) + 1
                line = text.split("\n")[line_no - 1].strip()
                rel = str(tex_path.relative_to(REPO_ROOT))
                findings.append(
                    f"  {rel}:{line_no}: cmd=\\{cmd}, unescaped '%' in: {line[:80]}"
                )

    assert not findings, (
        f"Found {len(findings)} unescaped %-in-braces bug(s). "
        f"Replace X%Y inside \\cmd{{...}} with X\\\\%Y.\n"
        + "\n".join(findings[:20])
    )


# =====================================================================
# TEST 2: \citep/\citet without \usepackage{natbib}
# =====================================================================

CITE_COMMAND_PATTERN = re.compile(r"\\(?:cite|citet|citep|citealp|citeauthor|citeyear|citeyearpar)\{")


def _has_natbib(text: str) -> bool:
    """True if the file declares natbib package OR uses elsarticle (which auto-loads it).

    The elsarticle document class automatically loads the natbib package
    for citation handling, so papers using \\citep under elsarticle
    compile correctly without an explicit \\usepackage{natbib}.
    """
    if re.search(r"\\usepackage(?:\[[^\]]*\])?\s*\{[^}]*\bnatbib\b", text):
        return True
    if re.search(r"\\documentclass(?:\[[^\]]*\])?\s*\{[^}]*\belsarticle\b", text):
        return True
    return False


def test_cite_commands_have_natbib_declared():
    """Round-Tier-6 lesson: \\citep without \\usepackage{natbib} → pdflatex crash.

    Found in p0010 and p0026 before Tier-6. Note: elsarticle document
    class auto-loads natbib so papers using elsarticle don't need an
    explicit \\usepackage{natbib}.
    """
    findings = []
    for tex_path in _iter_tex_files():
        text = tex_path.read_text(encoding="utf-8")
        if not CITE_COMMAND_PATTERN.search(text):
            continue
        if _has_natbib(text):
            continue
        # Count offending lines
        cite_lines = []
        for m in CITE_COMMAND_PATTERN.finditer(text):
            line_no = text.count("\n", 0, m.start()) + 1
            line = text.split("\n")[line_no - 1].strip()
            cite_lines.append((line_no, line[:80]))
        if cite_lines:
            rel = str(tex_path.relative_to(REPO_ROOT))
            findings.append((rel, cite_lines))

    assert not findings, (
        f"Found {len(findings)} file(s) using \\citep/\\citet but NOT declaring natbib. "
        f"Either add '\\usepackage[round]{{natbib}}' to the preamble, or change "
        f"\\documentclass to 'elsarticle' (which auto-loads natbib).\n"
        + "\n".join(f"  {p}:\n" + "\n".join(f"    line {ln}: {l}" for ln, l in lines[:5]) for p, lines in findings)
    )


# =====================================================================
# TEST 3: Brace balance per command argument
# =====================================================================

def test_braces_balance_per_command_argument():
    """Round-Tier-6 heuristic: each \\cmd{...} has matched braces.

    This is a coarse sanity check. Real compile errors are detected
    above by specific patterns.
    """
    findings = []
    # This test only fires on egregiously wrong braces (e.g. an unclosed
    # brace that has been the issue in some prior commits).
    for tex_path in _iter_tex_files():
        text = tex_path.read_text(encoding="utf-8")
        # Strip comments + verbatim
        stripped = _strip_latex_comments(text)
        # Track brace depth
        depth = 0
        for i, c in enumerate(stripped):
            if c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
                if depth < 0:
                    line_no = stripped.count("\n", 0, i) + 1
                    rel = str(tex_path.relative_to(REPO_ROOT))
                    findings.append(f"  {rel}:{line_no}: brace depth went negative at char {i}")
                    break
        if depth != 0:
            line_no = stripped.count("\n") + 1
            rel = str(tex_path.relative_to(REPO_ROOT))
            findings.append(f"  {rel}:{line_no}: unbalanced braces (final depth={depth})")

    assert not findings, (
        f"Found {len(findings)} brace-balance issue(s):\n" + "\n".join(findings[:20])
    )
