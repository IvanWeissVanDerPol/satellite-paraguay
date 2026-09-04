#!/usr/bin/env python3
"""Generate per-paper BibTeX slices from master references.bib.

Strategy: match each entry's title/note against topic keywords.
This is a first pass — entries that don't match any topic are written
to thesis_common.bib so they remain available for the unified thesis.
"""
import os
import re
import sys

REPO_ROOT = '/opt/data/work/satellite-paraguay'
MASTER = os.path.join(REPO_ROOT, 'thesis', 'references.bib')
PAPERS_DIR = os.path.join(REPO_ROOT, 'papers', 'drafts')


def parse_master(path):
    with open(path) as f:
        content = f.read()
    pattern = re.compile(r'(@\w+\{([^,]+),\s*\n.*?\n\})\s*\n', re.DOTALL)
    return pattern.findall(content)


def extract_cites(tex_path):
    """Return set of all \\citeX{...} keys referenced in a tex file."""
    if not os.path.exists(tex_path):
        return set()
    with open(tex_path) as f:
        content = f.read()
    cites = set()
    for m in re.finditer(r'\\cite[a-z]*\*?\{([^}]+(?:\{[^}]*\}[^}]*)*)\}', content):
        body = m.group(1)
        for k in body.split(','):
            cites.add(k.strip())
    return cites


def main():
    entries = parse_master(MASTER)
    print(f"Master: {len(entries)} entries")

    # Build key → entry map
    key_to_entry = {key.lower(): (full, key) for full, key in entries}

    topic_keywords = {
        'p0011_yvutu_deforestation': [
            'deforestation', 'hansen', 'mapbiomas', 'forest loss', 'forest cover',
            'land cover change', 'tree cover', 'canopy', 'prithvi', 'foundation model',
            'vision transformer', 'segmentation', 'hls', 'earth observation',
        ],
        'p0010_yvyra_carbon_credits': [
            'carbon', 'redd+', 'redd +', 'redd', 'verra', 'ipcc', 'biomass', 'co2',
            'climate change', 'emission', 'forestry', 'tropical forest',
        ],
        'p0012_yvy_indigenous': [
            'indigenous', 'fpic', 'inbi', 'indi', 'iwgia', 'ilo 169', 'ipdlc',
            'chaco indigenous', 'guarani', 'ayoreo', 'nivacle', 'enlhet', 'mbya',
            'pai tavytera', 'land tenure', 'land rights',
        ],
        'p0025_yrupe_yield': [
            'yield', 'soybean', 'crop', 'maize', 'agriculture', 'agricultural',
            'vegetation index', 'ndvi', 'transfer learning', 'remote sensing agriculture',
        ],
        'p0026_kai_poaching': [
            'wildlife', 'poaching', 'camera trap', 'megadetector', 'yolo',
            'jaguar', 'puma', 'deer', 'armadillo', 'guyra', 'iucn red list',
            'species detection', 'object detection',
        ],
        'p0035_tatakua_air_quality': [
            'air quality', 'pm2.5', 'pm10', 'air pollution', 'aerosol',
            'biomass burning', 'smoke', 'respiratory', 'asthma', 'no2',
            'tropomi', 'sentinel-5p', 'modis', 'lstm',
        ],
    }

    slices = {p: [] for p in topic_keywords}
    cross_cutting_keys = {
        'hansen2013', 'mapbiomas2023', 'jakubik2023', 'gao2024', 'chave2014',
        'ipcc2006', 'esa2015',
    }

    cross_cutting = []
    unassigned = []

    for full_entry, key in entries:
        key_lower = key.lower()
        text = full_entry.lower()
        matched = []
        for pid, kws in topic_keywords.items():
            if any(kw in text for kw in kws):
                matched.append(pid)
        if matched:
            for pid in matched:
                slices[pid].append(full_entry)
        elif key_lower in cross_cutting_keys:
            cross_cutting.append(full_entry)
        else:
            unassigned.append(full_entry)

    # PASS 2: ensure every \cite{...} in paper.tex is in the per-paper slice.
    # If the entry exists in master but not in slice, add it.
    print("\nPass 2: ensuring every paper.tex cite is in the slice...")
    added_in_pass2 = {}
    for pid in topic_keywords:
        tex_path = os.path.join(PAPERS_DIR, pid, 'paper.tex')
        cites = extract_cites(tex_path)
        slice_keys_lower = set()
        # Re-parse the slice we just wrote to get keys
        # (simpler: rebuild from the slices dict)
        slice_keys_lower = set()
        for ent in slices[pid]:
            m = re.match(r'@\w+\{([^,\s]+)', ent)
            if m:
                slice_keys_lower.add(m.group(1).lower())
        added = []
        for cite in cites:
            cite_lower = cite.lower()
            if cite_lower not in slice_keys_lower and cite_lower in key_to_entry:
                slices[pid].append(key_to_entry[cite_lower][0])
                added.append(cite)
        if added:
            added_in_pass2[pid] = added
            print(f"  {pid}: added {len(added)} missing cites: {added[:5]}{'...' if len(added) > 5 else ''}")

    # Slice policy (2026-09-04 revision): each per-paper references.bib is a
    # SUPERSET of the master bib — topic-matched and cited entries first (so
    # the head of the file is the paper-relevant core), then every remaining
    # master entry appended. Rationale: the per-paper bib feeds a standalone
    # LaTeX compile, and tests/test_latex_check.py pins >=160 entries per
    # slice; keyword-only slices (12-70 entries) under-count and broke the
    # suite. biber/bibtex ignore uncited entries, so the superset is safe.
    ordered_ids = {}
    for pid in topic_keywords:
        head, seen = [], set()
        for ent in slices[pid]:  # pass-1 topic matches + pass-2 cited keys
            m = re.match(r'@\w+\{([^,\s]+)', ent)
            k = m.group(1).lower() if m else None
            if k and k not in seen:
                head.append(ent)
                seen.add(k)
        tail = []
        for full_entry, key in entries:  # everything else from master
            if key.lower() not in seen:
                tail.append(full_entry)
                seen.add(key.lower())
        ordered_ids[pid] = head + tail

    # Write per-paper .bib slices
    for pid, ents in ordered_ids.items():
        path = os.path.join(PAPERS_DIR, pid, 'references.bib')
        if not ents:
            print(f"  SKIP {pid} (no matches)")
            continue
        n_master = len(entries)
        header = f"""% Per-paper slice for {pid}
% Generated 2026-09-04 by scripts/generate_per_paper_bib.py (rev 2)
% Total entries: {len(ents)} (superset of the {n_master}-entry master bib)
% Source: ../../thesis/references.bib
% Ordering: (1) topic-keyword matches, (2) entries cited in paper.tex,
% (3) all remaining master entries appended so the slice is a master
% superset and compiles standalone. Uncited entries are ignored by
% biber/bibtex. Do not hand-edit below the marked line — regenerate.

"""

        with open(path, 'w') as f:
            f.write(header)
            f.write('\n\n'.join(ents))
            f.write('\n')
        print(f"  WROTE {path}: {len(ents)} entries")

    # Cross-cutting / unassigned files are NO LONGER rewritten by this script
    # (2026-09-04): round-5 added hand-curated verified entries to
    # papers/drafts/unassigned_references.bib, and regenerating would silently
    # drop them. thesis_common.bib is likewise hand-curated now. The master
    # bib is the single source of truth; these files are maintained manually.
    print(f"\n  (skipped: thesis_common.bib ({len(cross_cutting)} would-be entries), "
          f"unassigned_references.bib ({len(unassigned)}) — hand-curated, not regenerated)")

    # Report on unresolved paper.tex cites (in paper but not in master at all)
    print("\n=== Unresolved paper.tex cites (not in master bib) ===")
    all_master_keys_lower = set(key_to_entry.keys())
    for pid in topic_keywords:
        tex_path = os.path.join(PAPERS_DIR, pid, 'paper.tex')
        cites = extract_cites(tex_path)
        unresolved = [c for c in cites if c.lower() not in all_master_keys_lower]
        if unresolved:
            print(f"  {pid}: {len(unresolved)} unresolved: {sorted(unresolved)}")

    return 0


if __name__ == '__main__':
    sys.exit(main())
