#!/usr/bin/env python3
"""Integrate verified_round-2 citations into references.bib, deduplicating by DOI."""

import json
import re
from pathlib import Path

NEW_BIB = Path("/opt/data/profiles/ivan/research/verification/verified_bibtex.bib")
EXISTING_BIB = Path("/opt/data/work/satellite-paraguay/references.bib")
BACKUP_BIB = Path("/opt/data/work/satellite-paraguay/references.bib.pre-verify-v3.bak")
EXISTING_BIB_BACKUP = Path(
    "/opt/data/profiles/ivan/research/verification/references.bib.before-verify"
)

# Make a backup of current references.bib (only first time)
if not BACKUP_BIB.exists():
    EXISTING_BIB_BACKUP.write_text(EXISTING_BIB.read_text())
    BACKUP_BIB.write_text(EXISTING_BIB.read_text())

# Extract DOIs from existing refs
existing_dois = set()


def find_doi(text):
    m = re.search(r"doi\s*=\s*\{([^}]+)\}", text, re.IGNORECASE)
    return m.group(1).strip().lower() if m else None


current = EXISTING_BIB.read_text()
# Split entries by @
for entry in re.split(r"(?=^@)", current, flags=re.MULTILINE):
    doi = find_doi(entry)
    if doi:
        existing_dois.add(doi)
print(f"Existing DOIs in references.bib: {len(existing_dois)}")

# Parse new entries
new_text = NEW_BIB.read_text()
new_entries = []
for entry in re.split(r"(?=^@)", new_text, flags=re.MULTILINE):
    if "@" not in entry:
        continue
    # Strip "note" line
    entry_clean = re.sub(r"\n\s*note\s*=.*\n", "\n", entry)
    entry_clean = re.sub(r"%.*", "", entry_clean)
    doi = find_doi(entry)
    if doi is None:
        print(f"WARNING no DOI: {entry[:60]}")
        continue
    if doi.strip().lower() in existing_dois:
        print(f"  SKIP (already present): {doi}")
        continue
    # Clean up empty lines
    entry_clean = entry_clean.strip() + "\n\n"
    new_entries.append((doi.lower(), entry_clean))
    existing_dois.add(doi.lower())

print(f"\n{len(new_entries)} new entries to add (out of 47 verified)")

# Append to references.bib
HEADER_MARKER = "% ===== Round-2 verified citations (2026-09-03 via CrossRef) ====="
with open(EXISTING_BIB, "a") as f:
    if not current.endswith("\n"):
        f.write("\n")
    # Only write the section header if it's not already there
    existing_now = EXISTING_BIB.read_text()
    if HEADER_MARKER not in existing_now:
        f.write(f"\n{HEADER_MARKER}\n")
    else:
        # Header already exists - strip it before appending so we don't double up
        pass  # re-read below to strip dup
    for doi, entry in new_entries:
        f.write(entry)

# Post-process: dedup any double-added header blocks (defensive)
content = EXISTING_BIB.read_text()
header_re_single = re.compile(rf"(?:\n*{re.escape(HEADER_MARKER)}\n)+")
content = header_re_single.sub(f"\n{HEADER_MARKER}\n", content)
EXISTING_BIB.write_text(content)

# Show what was added
print("\nAdded entries:")
for doi, entry in new_entries[:5]:
    # Get first line for display
    key_match = re.search(r"@(\w+)\{([^,]+)", entry)
    print(f"  {key_match.group(2)}")

print(f"\nNew references.bib size: {EXISTING_BIB.stat().st_size} bytes")
print(f"Backup at: {BACKUP_BIB}")
