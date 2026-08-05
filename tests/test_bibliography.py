"""Tests for src/utils/bibliography.py."""
import pytest
from pathlib import Path


class TestBibliography:
    """Tests for bibliography module."""

    def test_shared_refs_complete(self):
        from src.utils.bibliography import SHARED_REFS
        assert "hansen2013" in SHARED_REFS
        assert "chave2014" in SHARED_REFS
        assert all("type" in r for r in SHARED_REFS.values())

    def test_paper_cites_complete(self):
        from src.utils.bibliography import PAPER_CITES
        assert "P0011_yvutu_deforestation" in PAPER_CITES
        assert all(isinstance(v, list) for v in PAPER_CITES.values())

    def test_bibtex_entry_basic(self):
        from src.utils.bibliography import bibtex_entry
        ref = {"type": "article", "author": "Doe, J.", "title": "Test", "year": "2020"}
        result = bibtex_entry("test2020", ref)
        assert "@article" in result
        assert "test2020" in result
        assert "Doe, J." in result

    def test_bibtex_entry_and_to_AND(self):
        from src.utils.bibliography import bibtex_entry
        ref = {"type": "article", "author": "Doe, J. and Smith, K.", "title": "Test", "year": "2020"}
        result = bibtex_entry("test2020", ref)
        assert "Doe, J. AND Smith, K." in result

    def test_bibtex_entry_skip_type_field(self):
        """type field shouldn't appear as a regular bibtex field."""
        from src.utils.bibliography import bibtex_entry
        ref = {"type": "article", "title": "Test"}
        result = bibtex_entry("test", ref)
        assert "  type =" not in result
        assert "@article" in result

    def test_build_bibtex_default(self):
        from src.utils.bibliography import build_bibtex, SHARED_REFS
        result = build_bibtex()
        # Should include all references
        for key in SHARED_REFS:
            assert key in result
        # Header comments
        assert "Master bibliography" in result

    def test_build_bibtex_custom(self):
        from src.utils.bibliography import build_bibtex
        refs = {"x2020": {"type": "article", "title": "X", "year": "2020"}}
        result = build_bibtex(refs)
        assert "x2020" in result

    def test_count_citations(self):
        from src.utils.bibliography import count_citations
        paper_cites = {
            "paper_a": ["ref1", "ref2"],
            "paper_b": ["ref1", "ref3"],
        }
        refs = {"ref1": {}, "ref2": {}, "ref3": {}}
        counts = count_citations(paper_cites, refs)
        assert counts["ref1"] == 2
        assert counts["ref2"] == 1
        assert counts["ref3"] == 1

    def test_count_citations_unknown_ref(self):
        from src.utils.bibliography import count_citations
        # References not in refs dict should be silently ignored
        paper_cites = {"paper_a": ["unknown_ref", "ref1"]}
        refs = {"ref1": {}}
        counts = count_citations(paper_cites, refs)
        # unknown_ref is not in result
        assert "unknown_ref" not in counts
        assert counts["ref1"] == 1

    def test_most_cited(self):
        from src.utils.bibliography import most_cited
        counts = {"a": 3, "b": 1, "c": 5, "d": 0}
        result = most_cited(counts, min_count=2)
        # Sorted by count desc, filtered
        assert result[0] == ("c", 5)
        assert result[1] == ("a", 3)

    def test_most_cited_min_count_zero(self):
        from src.utils.bibliography import most_cited
        counts = {"a": 3, "b": 1, "c": 5}
        result = most_cited(counts, min_count=0)
        assert len(result) == 3

    def test_build_citation_graph(self):
        from src.utils.bibliography import build_citation_graph
        themes = {"deforestation": ["P0011"]}
        graph = build_citation_graph(themes=themes)
        assert "n_papers" in graph
        assert "n_shared_refs" in graph
        assert "papers" in graph
        assert "reference_frequency" in graph
        assert graph["thesis_themes"] == themes

    def test_write_bibtex_file(self, tmp_path):
        from src.utils.bibliography import write_bibtex_file
        refs = {"x2020": {"type": "article", "title": "X", "year": "2020"}}
        out = tmp_path / "refs.bib"
        count = write_bibtex_file(refs, out)
        assert out.exists()
        assert count == 1
        content = out.read_text()
        assert "x2020" in content

    def test_write_bibtex_file_creates_dir(self, tmp_path):
        from src.utils.bibliography import write_bibtex_file
        out = tmp_path / "deep" / "nested" / "refs.bib"
        write_bibtex_file({}, out)
        assert out.exists()

    def test_write_citation_graph(self, tmp_path):
        from src.utils.bibliography import write_citation_graph, build_citation_graph
        graph = build_citation_graph()
        out = tmp_path / "graph.json"
        write_citation_graph(graph, out)
        assert out.exists()

    def test_write_citation_graph_creates_dir(self, tmp_path):
        from src.utils.bibliography import write_citation_graph
        out = tmp_path / "deep" / "nested" / "graph.json"
        write_citation_graph({}, out)
        assert out.exists()