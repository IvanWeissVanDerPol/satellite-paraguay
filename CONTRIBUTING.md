# Contributing — SatelliteCV-Paraguay

**License:** CC-BY-NC-4.0 (see `LICENSE`). By contributing, you agree your
contributions are released under the same license.

## Reporting model / data integrity issues

If you spot a number in a `paper.md`, `paper.tex`, or `abstract.md` that does
not match the value in `ACTUAL_RESULTS.md`, please open an issue tagged
`integrity`. The honest-reporting convention is:

> Every abstract headline number must be the **measured** value, not a
> literature benchmark or aspirational target. If a measurement does not
> exist, say so explicitly. The repo carries a CI grep guard
> (`scripts/check_claims.py`) that flags high-headline numbers outside
> `ACTUAL_RESULTS.md` and `README.md`.

## Indigenous territory data (P0012 Yvy)

The indigenous territory polygons and analyses in `outputs/p0012/` and
`papers/drafts/p0012_yvy_indigenous/` follow the **CARE Principles for
Indigenous Data Governance** (Collective benefit, Authority to control,
Responsibility, Ethics).

- **No redistribution** of the per-community territorial-conflict maps
  without written permission from the relevant INDI-registered community
  council and the Instituto Paraguayo del Indígena (INDI).
- **Contact:** Instituto Paraguayo del Indígena (INDI), Av. Brasil 1392,
  Asunción, Paraguay. https://www.indi.gov.py/
- **FPIC engagement** is a **prerequisite** for any operational deployment
  of P0012, not an afterthought.

## Verra VCS project data (P0010 Yvyra)

The Verra project list and boundary polygons are sourced from the public
Verra registry. If you re-run the under-claim analysis with a refreshed
Hansen GFC (v1.12 or later), please cite the version and date.

## Model training (P0011, P0025, P0026)

- **GPU required.** CPU-only pilots are documented in each paper's
  `ACTUAL_RESULTS.md` as honest baselines; they are not operational results.
- Real-data training pipelines are scripted under `scripts/` and target
  Vast.ai A100 80GB instances. Estimated cost per full P0011 re-run: ~$5.
- Prithvi model weights (~1 GB) are downloaded on first run; YOLOv8 weights
  are pulled from Ultralytics; LSTM is trained from scratch.

## Data sources

| Source | License | Auth |
|---|---|---|
| Hansen GFC v1.11 | CC-BY-4.0 | None |
| MapBiomas Paraguay | CC-BY-NC-SA-4.0 | None |
| Sentinel-2 L2A | Copernicus open | Microsoft Planetary Computer |
| OpenAQ | CC-BY-4.0 | API key optional |
| Verra VCS | Public registry | None |
| TROPOMI | Copernicus open | None |
| ERA5 | Copernicus | CDS API key |
| INDI polygons | CARE-controlled | INDI partnership |

## Pull request convention

1. Branch off `main`.
2. Run `python3 scripts/merge_bib.py` after any bibliography change.
3. Run `python3 scripts/check_claims.py` — must exit 0.
4. If the change affects any paper abstract, edit **both** `abstract.md`
   and `paper.tex` (or `paper.md`) and reference `ACTUAL_RESULTS.md`.
5. Add an entry to `CHANGELOG.md` under `[Unreleased]`.
6. Reference the `GAP_AUDIT_*.md` or `REAL_TODO.md` item your PR closes.

## Code of conduct

Be honest. Be precise. Do not cite literature benchmarks as measured results.
Cite measured values.