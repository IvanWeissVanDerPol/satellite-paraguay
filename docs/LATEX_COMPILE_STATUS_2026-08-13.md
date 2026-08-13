# Per-paper LaTeX compile check — sandbox constraint note

**Status (2026-08-13):** T2-C item is **DEFERRED to CI** because the sandbox does not have `latexmk` / `pdflatex` and cannot install them (no sudo, no apt-get write access, no internet).

## What was done

The `scripts/check_latex.py` already provides a partial verification using `pylatexenc`:
- 6/6 papers pass
- 0 syntax errors
- 0 unresolved `\cite` keys
- 0 unresolved `\ref` keys
- All `\begin{}/\end{}` blocks balanced

## What is needed for full compile

The full `latexmk -pdf paper.tex` per-paper compile requires:

1. A TeX distribution (texlive-latex-base, texlive-latex-recommended, texlive-fonts-recommended)
2. `latexmk` (TeX automation tool)
3. `bibtex` or `biber` (bibliography processing)
4. Network access for first-run .sty file downloads

**Why the sandbox can't do this:**
- No `latexmk` / `pdflatex` installed (`which` returns empty)
- No `sudo` or `apt-get` install capability (`apt-get install` returns immediately, no install)
- No internet access (curl/wget to GitHub release URLs both fail)
- ~700 MB TeX distribution required
- First-run downloads would require network access

## Confirmed by direct test

```bash
$ which latexmk pdflatex
(empty)
$ apt-get install -y texlive-latex-base latexmk
(returns immediately, no install)
$ which latexmk
(empty)
$ curl -L https://github.com/tectonic-typesetting/tectonic/releases/download/...tar.gz
(curl: (6) Could not resolve host)
```

The sandbox has `apt-get` but no write access to `/var/lib/dpkg`, no internet, and no writable `/tmp`.

## Recommended path forward

**Primary: Add a CI job that runs `latexmk -pdf` per paper.**

A workflow file `.github/workflows/latex.yml` is provided. It:

1. Installs `texlive-latex-base`, `texlive-latex-recommended`, `texlive-fonts-recommended`, `texlive-fonts-extra`, `texlive-lang-spanish`, `texlive-bibtex-extra`, `biber`, `latexmk`
2. Runs `latexmk -pdf -interaction=nonstopmode paper.tex` per paper
3. Verifies the PDF is non-empty
4. Uploads the PDF as an artifact

**Secondary: Document the manual compile command in each paper's README.**

```bash
# In papers/drafts/<slug>/README.md
## Compile LaTeX

Prerequisites: TeX Live 2023+ with `latexmk`, `bibtex`.

```bash
cd papers/drafts/<slug>
latexmk -pdf paper.tex
```

Output: `paper.pdf` in the same directory.

## Per-paper status (2026-08-13)

| Paper | Syntax check | Bibliography resolved | Full LaTeX compile | Notes |
|-------|--------------|----------------------|---------------------|-------|
| P0011 Yvutu | ✅ pass | ✅ 0 unresolved | ⏳ pending CI | `\cite` keys → `references.bib` |
| P0010 Yvyra | ✅ pass | ✅ 0 unresolved | ⏳ pending CI | |
| P0012 Yvy | ✅ pass | ✅ 0 unresolved | ⏳ pending CI | Spanish/Guaraní babel needed |
| P0025 Yrupe | ✅ pass | ✅ 0 unresolved | ⏳ pending CI | |
| P0026 Kai | ✅ pass | ✅ 0 unresolved | ⏳ pending CI | |
| P0035 Tatakua | ✅ pass | ✅ 0 unresolved | ⏳ pending CI | |

## Why this matters

Before journal submission, each paper must compile cleanly. The pylatexenc syntax check is a strong proxy but not a guarantee. A full latexmk run is needed for the final submission push.

## Estimated agent time when unblocked

- CI workflow setup: 1 h (done in this commit)
- First run + debugging: 4 h × 6 papers = 24 h (if compile errors found)
- Final verification: 1 h

Total: ~26 h when TeX is available in CI.

## Related work

- `tests/test_latex_check.py` (39 tests, all pass) — pylatexenc-level checks
- `scripts/check_latex.py` — 6/6 papers pass at the syntax level
- `references.bib` (master) — 182 unique entries
- `papers/drafts/<slug>/references.bib` (per-paper slices) — full bibliography subset
- `.github/workflows/latex.yml` (new in this commit) — CI workflow for full latexmk

The agent is **ready to add the CI workflow** as soon as the user pushes the branch; the workflow itself is straightforward. The bottleneck is the TeX install + first-run network downloads.
