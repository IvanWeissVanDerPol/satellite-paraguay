#!/usr/bin/env python3
"""Update the fabricated/stub rows in papers/drafts/CITATION_STUBS.md.

Marks the 6 keys deleted from paper.tex on 2026-09-04 as DELETED (per
round-5 verification: no CrossRef match / wrong-author match), so the
stub ledger reflects the cleanup instead of still saying "STUB".
"""

import re
from pathlib import Path

STUBS = Path("/opt/data/work/satellite-paraguay/papers/drafts/CITATION_STUBS.md")
DELETED = {
    "alphaearth2025": "DELETED 2026-09-04: cited CH3 'Physically Interpretable AlphaEarth' "
    "(Rahman 2026 SSRN) does not exist as claimed; round-5 found no CrossRef match. "
    "Removed \\cite from p0011 paper.tex (jakubik2023 + cong2022 carry the claim).",
    "baumann2022south_american": "DELETED 2026-09-04: round-5 search yielded only Macchi "
    "et al. 2019 (wrong year + topic) — fabricated key. Removed \\cite from p0011 "
    "paper.tex (vallejos2020 carries the Chaco deforestation claim).",
    "cristaldo2024paraguay": "DELETED 2026-09-04: no CrossRef match for any 2024 Cristaldo "
    "paper on Paraguay satellite topics; the thesis/references.bib @misc entry has no "
    "DOI or URL and round-5 flagged it fabricated. Removed \\cite from p0011 paper.tex "
    "(IGN geodata provenance stated in prose instead) and from "
    "thesis/chapters/02_literature_review.tex.",
    "huang2021paraguay": "DELETED 2026-09-04: no CrossRef match for Huang 2021 Paraguay — "
    "fabricated key. Removed \\cite from p0011 paper.tex (hansen2013 carries the "
    "forest-loss claim).",
    "rikap2021indigenous": "DELETED 2026-09-04: no Rikap author found — fabricated key. "
    "Removed \\cite from p0012 paper.tex (garnett2018 carries the indigenous-land "
    "claim).",
    "zheng2015fine_grained": "DELETED 2026-09-04: fabricated key (no CrossRef match; "
    "'fine_grained' suffix is a topic string, not a real citation). Removed \\cite "
    "from p0035 paper.tex; the >70% dry-season claim now carries a "
    "TODO: ivan-review comment pending a real source or softening.",
}

text = STUBS.read_text()
changed = 0
for key, note in DELETED.items():
    # rows look like: | `key` | STUB | ...notes... |
    pattern = re.compile(r"(\|\s*`" + re.escape(key) + r"`\s*\|\s*)STUB(\s*\|)", re.M)
    new_text, n = pattern.subn(r"\1DELETED\2", text)
    if n:
        text = new_text
        changed += n
    else:
        print(f"WARN: no STUB row found for {key}")

STUBS.write_text(text)
print(f"Updated {changed} rows -> DELETED in {STUBS}")
