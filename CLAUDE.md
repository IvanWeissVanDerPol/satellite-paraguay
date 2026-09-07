# CLAUDE.md — satellite-paraguay

> **This file is the first thing any AI session should read.** It encodes
> the project's purpose, conventions, and the things you must NOT do.

---

## What this repo is

**Iván's FADA thesis at FP-UNA** (Universidad Nacional de Asunción, Paraguay).
The thesis is a **monograph made of 6 self-contained papers**, each
answering a research question about earth observation of Paraguay:

| ID | Paper | Topic |
|---|---|---|
| `p0011_yvutu_deforestation` | Yvutu | Deforestation detection (Sentinel-2, Chaco) |
| `p0010_yvyra_carbon_credits` | Yvyra | Carbon credit verification (Sentinel-1) |
| `p0012_yvy_indigenous` | Yvy | Indigenous land monitoring (Landsat time series) |
| `p0025_yrupe_yield` | Yrupe | Soybean yield prediction (Sentinel-2 + MODIS) |
| `p0026_kai_poaching` | Kai | Wildlife poaching detection (camera traps) |
| `p0035_tatakua_air_quality` | Tatakua | Air quality from satellite AOD (MODIS) |

The 6 Guaraní names (Yvutu, Yvyra, Yvy, Yrupe, Kai, Tatakua) are the
**first-author voice** of each paper. They are NOT placeholders.

---

## Repo architecture

```
satellite-paraguay/
├── thesis/                  # 11-chapter monograph + unified references.bib
│   ├── chapters/            # 00_abstract through 11_conclusions (.tex)
│   └── references.bib       # 325 entries, the MASTER bibliography
├── papers/drafts/           # 6 self-contained papers
│   ├── p0011_yvutu_deforestation/
│   │   ├── paper.tex        # LaTeX source
│   │   ├── references.bib   # 325-entry SUPERSET slice (auto-gen)
│   │   ├── related_work.md  # Markdown source for Related Work
│   │   └── figures/
│   ├── ... (5 more)
│   └── AUDIT/               # Citation integrity audits (NEW)
├── scripts/                 # Python tools (24+ files)
│   ├── check_citations.py   # Verify all \cite{} resolve in paper.tex
│   ├── check_claims.py      # Verify prose claims against data
│   ├── convert_related_work.py  # Markdown → LaTeX \citep{}
│   ├── generate_per_paper_bib.py  # Slice master bib per paper
│   ├── verify_bib_dois.py   # CrossRef title+author+year audit (NEW)
│   └── run_tests.sh         # Fast pytest runner (NEW)
├── src/                     # Python package — all paper-specific code
│   ├── papers/              # One subpackage per paper
│   ├── evaluation/          # Shared metrics
│   ├── satellite_io/        # Sentinel/Landsat/MODIS loaders
│   └── ...
├── tests/                   # 24+ test files (mostly pytest)
├── outputs/                 # Generated artifacts (data_audit.json, etc.)
└── pyproject.toml           # uv-managed project (PEP 621)
```

---

## Critical conventions

### 1. Citation system

- **Master bib** lives at `thesis/references.bib` (325 entries)
- **Per-paper slices** are auto-generated supersets of master (not subsets!)
- **All citations in paper.tex** must use `\citep{}` (parenthetical) or `\citet{}` (in-text)
- **NO bare `\cite{}`** — they break BibTeX ordering
- **Verify with**: `scripts/run_tests.sh` + `python3 scripts/check_citations.py <paper>`

### 2. Trademark banlist (CRITICAL)

The following strings are BANNED from public-facing surfaces
(subdomains, page titles, containers, env vars, public strings, code, configs, docs, commits, PR titles, chat output):

`mensaje`, `mensajebusiness`, `mensaje-web`, `wpp`, `facebook`, `meta`,
`instagram`, `insta`, `messenger`, `oculus`, `paypal`, `stripe`, `google`,
`gmail`, `youtube`, `tiktok`, `twitter`, `x-com`, `discord`, `slack`,
`microsoft`, `office365`, `apple`, `icloud`, `amazon`, `aws-`, `openai`,
`chatgpt`, `anthropic`, `claude`

**Reason:** Hostinger suspended a previous deployment in 2026-Q1 for
impersonation. Compliance review depends on this list being absent from
every public surface.

**Carve-outs (allowed):**
- Bare functional terms in code comments ("messaging bridge", "linked device")
- Upstream OSS names (Evolution API, etc.)
- Pre-existing package names (incremental rename only)

### 3. Python environment

- **Toolchain:** `uv` (PEP 621 + lock file)
- **Setup:** `uv sync --all-extras` (creates `.venv`)
- **Run tests:** `scripts/run_tests.sh` (fast, no coverage) or `scripts/run_tests.sh --full`
- **Run paper.tex checks:** `python3 scripts/check_citations.py <paper>`
- **DO NOT use** the system `/opt/hermes/.venv` — it's for the agent, not the project

### 4. Branching

- Default branch: **not yet decided** (currently on `feat/tier2-consistency-thesis-integration`)
- Feature branches: `feat/<short-name>`
- Hotfixes: `fix/<short-name>`
- **DO NOT** push to a remote unless explicitly told
- **DO NOT** rewrite published history

### 5. Data conventions

- Satellite data lives OFF-repo (too large). Canonical paths in `outputs/data_audit.json`
- DO NOT commit raster files (.tif, .nc) — they belong in DVC or S3
- 9 of 17 audited data claims are "off-repo" or "synthetic" — see `outputs/data_audit.json`
- Use `data/cache/` for derived products

---

## Common tasks

| Task | Command |
|---|---|
| Run all tests fast | `scripts/run_tests.sh` |
| Run specific test | `scripts/run_tests.sh test_bibliography` |
| Verify citations for one paper | `python3 scripts/check_citations.py p0011_yvutu_deforestation` |
| Verify all 6 papers | `for p in papers/drafts/*/; do python3 scripts/check_citations.py $(basename $p); done` |
| Regenerate per-paper bib slices | `python3 scripts/generate_per_paper_bib.py` |
| Re-verify all bib DOIs | `python3 scripts/verify_bib_dois.py --batch 0 200` |
| Convert related_work.md → LaTeX | `python3 scripts/convert_related_work.py <paper>` |
| Build unified thesis | (requires LaTeX — run on laptop, not in sandbox) |

---

## What NOT to do

1. **DO NOT** add new citations without re-running `verify_bib_dois.py` first
2. **DO NOT** add bare `\cite{}` (use `\citep{}` or `\citet{}`)
3. **DO NOT** commit raster data or secrets
4. **DO NOT** modify per-paper `references.bib` by hand — they're auto-generated
5. **DO NOT** use any of the banned trademark strings
6. **DO NOT** trust a single API for citation verification — always cross-check
   (Round-5 lesson: S2 lookup-by-DOI returns inconsistent metadata)

---

## Defense timeline (target: 2026-Q4)

- **Tier-A** (mechanical polish): DONE — 28 \cite{} resolved, 6 papers compile
- **Tier-B** (defense prep): in progress
  - B1: Refresh FADA submission packet
  - B2: Update slides.html with honest numbers
  - B3: Author thesis README
  - B4: Thesis-tracker status snapshot
  - B5: Tag round-citation-verified
- **Tier-C** (real blockers): NOT YET
  - LaTeX compile check (needs laptop with TeX Live)
  - Spanish translation CH1-CH11 (4-6h)
  - Unified thesis PDF (1h after LaTeX works)

---

## External dependencies

- **Cross-repo:** `/opt/data/thesis-active` (paraguay-geodata-vlm) — data substrate
- **User home:** `/opt/data` (write-safe root)
- **Audit results:** `/opt/data/profiles/ivan/research/verification/results/`
- **Scratchpad:** `/opt/data/scratchpad/`

---

## Pitfalls observed in this repo

| # | Pitfall | Workaround |
|---|---|---|
| 11 | Python f-string nested `}` in BibTeX entries | Use heredoc / raw strings, not f-strings |
| S2-429 | Semantic Scholar rate limit at free tier | Add `User-Agent: Mozilla/5.0...` and 1 RPS |
| CrossRef-2026 | Some DOIs return wrong authors (cached/stale) | Always cross-validate year + author + title |
| `H.` in bib | Regex bug stripped `doi={` to `H.` | Use `patch` tool, not regex, for surgical edits |

---

## Last review

- **CLAUDE.md authored:** 2026-09-07
- **Master bib entries:** 325 (after Round-6 fixes)
- **Per-paper slices:** 325 each, all 6 papers pass `check_citations.py`
- **Tests:** 24+ files, ~1000 cases, all passing
- **Recent commits:** see `git log --oneline -10`
