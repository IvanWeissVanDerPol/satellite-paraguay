#!/usr/bin/env python3
"""AC3: per-paper LaTeX syntax + bib-resolve check."""
import re
from pathlib import Path
from pylatexenc.latexwalker import LatexWalker, LatexWalkerError

base = Path("papers/drafts")
papers = ["p0011_yvutu_deforestation", "p0010_yvyra_carbon_credits",
          "p0012_yvy_indigenous", "p0025_yrupe_yield",
          "p0026_kai_poaching", "p0035_tatakua_air_quality"]

def get_bib_keys(refs_path):
    if not refs_path.exists():
        return set()
    text = refs_path.read_text()
    return {m.group(1).strip() for m in re.finditer(r"@\w+\s*\{\s*([^,]+),", text)}

print("AC3 -- LaTeX syntax + bib-resolve check")
print("=" * 60)
results = {}
for p in papers:
    paper_tex = base / p / "paper.tex"
    refs_bib = base / p / "references.bib"
    if not paper_tex.exists():
        print(f"\n{p}: MISSING")
        continue
    text = paper_tex.read_text()
    bib_keys = get_bib_keys(refs_bib)

    walker = LatexWalker(text)
    try:
        _, errors, _ = walker.get_latex_nodes()
        syntax_ok = errors == 0 or (hasattr(errors, "__len__") and len(errors) == 0)
        syntax_errs = len(errors) if hasattr(errors, "__len__") else int(errors)
    except (LatexWalkerError, TypeError):
        syntax_ok = False
        syntax_errs = -1

    cite_keys = set()
    for m in re.finditer(r"\\cite[a-z]?\*?(?:\[[^\]]*\])?\{([^}]+)\}", text):
        for k in m.group(1).split(","):
            cite_keys.add(k.strip())
    ref_keys = set(re.findall(r"\\ref\{([^}]+)\}", text))
    label_keys = set(re.findall(r"\\label\{([^}]+)\}", text))
    begin_envs = set(re.findall(r"\\begin\{(\w+)\}", text))
    end_envs = set(re.findall(r"\\end\{(\w+)\}", text))
    unbalanced_envs = begin_envs - end_envs

    unresolved_cite = cite_keys - bib_keys
    unresolved_ref = ref_keys - label_keys

    status = "OK" if (syntax_ok and not unresolved_cite and not unresolved_ref and not unbalanced_envs) else "FAIL"
    results[p] = status

    print(f"\n--- {p}: {status} ---")
    print(f"  syntax errors: {syntax_errs}")
    print(f"  cite keys: {len(cite_keys)} total, {len(unresolved_cite)} unresolved")
    print(f"  ref keys: {len(ref_keys)} total, {len(unresolved_ref)} unresolved")
    print(f"  label keys: {len(label_keys)}")
    if unresolved_cite:
        print(f"  UNRESOLVED CITE: {sorted(unresolved_cite)[:8]}")
    if unresolved_ref:
        print(f"  UNRESOLVED REF: {sorted(unresolved_ref)[:8]}")
    if unbalanced_envs:
        print(f"  UNBALANCED ENV: {unbalanced_envs}")

print("\n" + "=" * 60)
print(f"FINAL: {sum(1 for v in results.values() if v == 'OK')}/{len(results)} papers pass")
