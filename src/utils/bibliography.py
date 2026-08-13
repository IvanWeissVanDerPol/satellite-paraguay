"""Thesis bibliography utilities.

Builds citation graph and BibTeX file for the thesis.
"""

import json
from typing import Any

SHARED_REFS: dict[str, dict[str, str]] = {
    "hansen2013": {
        "type": "article",
        "author": "Hansen, M. C. and Potapov, P. V. and Moore, R. and Hancher, M. and Turubanova, S. A. and Tyukavina, A. and Thau, D. and Stehman, S. V. and Goetz, S. J. and Loveland, T. R. and Kommareddy, A. and Egorov, A. and Chini, L. and Justice, C. O. and Townshend, J. R. G.",  # noqa: E501
        "title": "High-Resolution Global Maps of 21st-Century Forest Cover Change",
        "journal": "Science",
        "year": "2013",
        "volume": "342",
        "pages": "850--853",
        "doi": "10.1126/science.1244693",
    },
    "mapbiomas2023": {
        "type": "misc",
        "author": "MapBiomas Paraguay",
        "title": "MapBiomas Paraguay Collection 2 (2000-2022)",
        "year": "2023",
        "url": "https://paraguay.mapbiomas.org/",
    },
    "prithvi2023": {
        "type": "misc",
        "author": "NASA-IBM Hugging Face Team",
        "title": "Prithvi-100M: A Geospatial Foundation Model for Earth Observation",
        "year": "2023",
        "url": "https://huggingface.co/ibm-nasa-geospatial/Prithvi-100M",
    },
    "planetarycomputer2022": {
        "type": "misc",
        "author": "Microsoft",
        "title": "Microsoft Planetary Computer",
        "year": "2022",
        "url": "https://planetarycomputer.microsoft.com/",
    },
    "verra2021": {
        "type": "misc",
        "author": "Verra",
        "title": "Verified Carbon Standard (VCS) Program",
        "year": "2021",
        "url": "https://verra.org/programs/verified-carbon-standard/",
    },
    "openaq2024": {
        "type": "misc",
        "author": "OpenAQ",
        "title": "OpenAQ Air Quality Data",
        "year": "2024",
        "url": "https://openaq.org/",
    },
    "ipcc2006": {
        "type": "book",
        "author": "IPCC",
        "title": "2006 IPCC Guidelines for National Greenhouse Gas Inventories",
        "publisher": "IGES",
        "year": "2006",
    },
    "chave2014": {
        "type": "article",
        "author": "Chave, J. and Rejou-Mechain, M. and Burquez, A. and Chidumayo, E. and Colgan, M. S. and Delitti, W. B. C. and Duque, A. and Eid, T. and Fearnside, P. M. and Goodman, R. C. and Henry, M. and Martinez-Yrizar, A. and Mugasha, W. A. and Muller-Landau, H. C. and Mencuccini, M. and Nelson, B. W. and Ngomanda, A. and Nogueira, E. M. and Ortiz-Malavassi, E. and Pelissier, R. and Ploton, P. and Ryan, C. M. and Saldarriaga, J. G. and Vieilledent, G.",  # noqa: E501
        "title": "Improved allometric models to estimate the aboveground biomass of tropical trees",
        "journal": "Global Change Biology",
        "year": "2014",
        "volume": "20",
        "pages": "3177--3190",
        "doi": "10.1111/gcb.12629",
    },
    "hochtleitner2022": {
        "type": "misc",
        "author": "Hocht-VonDerPol, I.",
        "title": "satellite-paraguay: Multi-temporal Earth observation of Paraguay",
        "year": "2022",
        "url": "https://github.com/IvanWeissVanDerPol/satellite-paraguay",
    },
    "inbio2024": {
        "type": "misc",
        "author": "INBIO Paraguay",
        "title": "Instituto de Biotecnología Agrícola Paraguay",
        "year": "2024",
        "url": "https://inbio.org.py/",
    },
    "iwgia2024": {
        "type": "misc",
        "author": "IWGIA",
        "title": "Indigenous World 2024",
        "year": "2024",
        "url": "https://iwgia.org/en/resources/indigenous-world",
    },
    "indi2024": {
        "type": "misc",
        "author": "INDI",
        "title": "Instituto Paraguayo del Indígena",
        "year": "2024",
        "url": "https://indi.gov.py/",
    },
    "unesco2023": {
        "type": "misc",
        "author": "UNESCO",
        "title": "Indigenous Languages in Paraguay",
        "year": "2023",
        "url": "https://en.unesco.org/indigenous-knowledge",
    },
    "gao2024": {
        "type": "article",
        "author": "Gao, Y. and others",
        "title": "Foundation models for Earth observation",
        "journal": "Nature Reviews Earth & Environment",
        "year": "2024",
    },
}

# Paper -> citations
PAPER_CITES: dict[str, list[str]] = {
    "P0011_yvutu_deforestation": [
        "hansen2013",
        "mapbiomas2023",
        "prithvi2023",
        "planetarycomputer2022",
        "chave2014",
        "ipcc2006",
        "gao2024",
        "hochtleitner2022",
    ],
    "P0010_yvyra_carbon_credits": [
        "verra2021",
        "hansen2013",
        "mapbiomas2023",
        "ipcc2006",
        "chave2014",
        "hochtleitner2022",
    ],
    "P0012_yvy_indigenous": ["iwgia2024", "indi2024", "unesco2023", "hansen2013", "mapbiomas2023", "hochtleitner2022"],
    "P0025_yrupe_yield": ["inbio2024", "mapbiomas2023", "prithvi2023", "planetarycomputer2022", "hochtleitner2022"],
    "P0026_kai_poaching": ["planetarycomputer2022", "prithvi2023", "hansen2020", "hochtleitner2022"],
    "P0035_tatakua_air_quality": ["openaq2024", "ipcc2006", "planetarycomputer2022", "hochtleitner2022"],
}


def bibtex_entry(key: str, ref: dict[str, str]) -> str:
    """Format a BibTeX entry from key and ref dict."""
    fields = []
    for k, v in ref.items():
        if k in ("type",):
            continue
        if k == "author":
            v = v.replace(" and ", " AND ")
        fields.append(f"  {k} = {{{v}}}")
    return f"@{ref['type']}{{{key},\n" + ",\n".join(fields) + "\n}\n\n\n"


def build_bibtex(refs: dict[str, dict[str, str]] | None = None) -> str:
    """Build full BibTeX file content."""
    if refs is None:
        refs = SHARED_REFS
    bib = "% Master bibliography for satellite-paraguay mega-thesis\n"
    bib += "% Auto-generated by src/utils/bibliography.py\n"
    bib += f"% {len(refs)} shared references across 6 papers\n\n"

    for key, ref in refs.items():
        bib += bibtex_entry(key, ref)
    return bib


def count_citations(
    paper_cites: dict[str, list[str]] | None = None,
    refs: dict[str, dict[str, str]] | None = None,
) -> dict[str, int]:
    """Count how many papers cite each reference."""
    if paper_cites is None:
        paper_cites = PAPER_CITES
    if refs is None:
        refs = SHARED_REFS
    counts: dict[str, int] = {key: 0 for key in refs}
    for paper, citations in paper_cites.items():
        for c in citations:
            if c in counts:
                counts[c] += 1
    return counts


def most_cited(citation_counts: dict[str, int], min_count: int = 1) -> list[tuple]:
    """Return list of (ref, count) sorted by count desc, filtered by min_count."""
    return sorted(
        [(r, c) for r, c in citation_counts.items() if c >= min_count],
        key=lambda x: -x[1],
    )


def build_citation_graph(
    paper_cites: dict[str, list[str]] | None = None,
    refs: dict[str, dict[str, str]] | None = None,
    themes: dict[str, list[str]] | None = None,
) -> dict[str, Any]:
    """Build full citation graph dict."""
    if paper_cites is None:
        paper_cites = PAPER_CITES
    if refs is None:
        refs = SHARED_REFS
    counts = count_citations(paper_cites, refs)
    return {
        "n_papers": len(paper_cites),
        "n_shared_refs": len(refs),
        "papers": paper_cites,
        "reference_frequency": counts,
        "thesis_themes": themes or {},
    }


def write_bibtex_file(refs: dict[str, dict[str, str]], output_path) -> int:
    """Write BibTeX file. Returns number of entries written."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    content = build_bibtex(refs)
    output_path.write_text(content)
    return len(refs)


def write_citation_graph(graph: dict[str, Any], output_path) -> None:
    """Write citation graph JSON."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(graph, indent=2))
