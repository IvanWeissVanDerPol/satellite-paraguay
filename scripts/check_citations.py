#!/usr/bin/env python3
"""Citation cross-check: verify every \\cite{key} in a .tex file resolves
in the .bib file.

Usage:
  python3 check_citations.py paper.tex references.bib
  python3 check_citations.py --all  # check all papers
"""
import os
import re
import sys
import argparse

PAPERS_DIR = '/opt/data/work/satellite-paraguay/papers/drafts'


def parse_bib(path):
    """Return set of all bib keys."""
    with open(path) as f:
        content = f.read()
    keys = set()
    for m in re.finditer(r'@\w+\{([^,\s]+)\s*,', content):
        keys.add(m.group(1).strip())
    return keys


def extract_cites(tex_path):
    """Return set of all \\cite{...} / \\citep{...} / \\citet{...} keys."""
    with open(tex_path) as f:
        content = f.read()
    cites = set()
    # Match \cite, \citep, \citet, \citealp, etc. (any \citeX command)
    for m in re.finditer(r'\\cite[a-z]*\*?\{([^}]+(?:\{[^}]*\}[^}]*)*)\}', content):
        # \cite{key1, key2, ...} (with optional nested braces for each key)
        # Split on commas at the top level
        body = m.group(1)
        for k in body.split(','):
            cites.add(k.strip())
    return cites


def check_paper(pid):
    tex_path = os.path.join(PAPERS_DIR, pid, 'paper.tex')
    bib_path = os.path.join(PAPERS_DIR, pid, 'references.bib')
    if not os.path.exists(tex_path):
        return {'error': f'{tex_path} not found'}
    if not os.path.exists(bib_path):
        return {'error': f'{bib_path} not found'}

    bib_keys = parse_bib(bib_path)
    cites = extract_cites(tex_path)

    missing = cites - bib_keys
    unused = bib_keys - cites  # entries in .bib not cited in .tex (informational)

    return {
        'paper': pid,
        'cite_count': len(cites),
        'bib_count': len(bib_keys),
        'missing_in_bib': sorted(list(missing)),
        'unused_in_bib_count': len(unused),
        'ok': not missing,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--all', action='store_true', help='Check all papers')
    parser.add_argument('paper', nargs='?', help='Single paper directory')
    args = parser.parse_args()

    papers = [
        'p0011_yvutu_deforestation',
        'p0010_yvyra_carbon_credits',
        'p0012_yvy_indigenous',
        'p0025_yrupe_yield',
        'p0026_kai_poaching',
        'p0035_tatakua_air_quality',
    ]

    targets = papers if args.all else ([args.paper] if args.paper else [])

    if not targets:
        parser.print_help()
        return 1

    all_ok = True
    for pid in targets:
        if pid not in papers:
            print(f"Unknown paper: {pid}")
            all_ok = False
            continue
        r = check_paper(pid)
        if 'error' in r:
            print(f"\n{pid}: ERROR — {r['error']}")
            all_ok = False
            continue
        status = 'OK' if r['ok'] else 'BROKEN'
        print(f"\n[{status}] {r['paper']}: {r['cite_count']} \\cite{{}} vs {r['bib_count']} bib entries")
        if r['missing_in_bib']:
            all_ok = False
            print(f"  Missing in .bib (broken \\cite{{}}):")
            for k in r['missing_in_bib']:
                print(f"    - {k}")
        if r['unused_in_bib_count'] > 0:
            print(f"  Unused bib entries: {r['unused_in_bib_count']} (informational)")
        print(f"  -- {r['paper']}: {r['cite_count']} cites, {r['bib_count']} bib entries, missing={len(r['missing_in_bib'])}, unused={r['unused_in_bib_count']}")

    print()
    if all_ok:
        print("ALL CITATIONS RESOLVE")
    else:
        print("BROKEN CITATIONS — see above")
    return 0 if all_ok else 1


if __name__ == '__main__':
    sys.exit(main())
