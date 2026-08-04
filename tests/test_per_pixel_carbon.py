"""Tests for Chave 2014 AGB model."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import numpy as np
import pytest


def test_chave_agb_zero():
    """Zero treecover → zero biomass."""
    from scripts.per_pixel_carbon import chave_agb
    assert chave_agb(0) == 0
    assert chave_agb(np.array([0])) == 0


def test_chave_agb_clipped():
    """Negative treecover clipped to 0, > 100 clipped to 100."""
    from scripts.per_pixel_carbon import chave_agb
    assert chave_agb(-10) == 0
    assert chave_agb(150) == chave_agb(100)


def test_chave_agb_typical():
    """Typical Chaco treecover 50% → ~42 Mg/ha (IPCC Tier 1)."""
    from scripts.per_pixel_carbon import chave_agb
    agb_50 = chave_agb(50)
    assert 35 < agb_50 < 50, f"Expected 35-50, got {agb_50}"


def test_chave_agb_dense():
    """Dense Chaco treecover 80% → ~137 Mg/ha."""
    from scripts.per_pixel_carbon import chave_agb
    agb_80 = chave_agb(80)
    assert 100 < agb_80 < 200, f"Expected 100-200, got {agb_80}"


def test_carbon_fraction():
    """Carbon stock is 47% of AGB (IPCC)."""
    from scripts.per_pixel_carbon import chave_agb, carbon_stock
    agb = chave_agb(50)
    carbon = carbon_stock(50)
    assert abs(carbon / agb - 0.47) < 0.01


def test_co2e_ratio():
    """CO2e is 44/12 * C (stoichiometric)."""
    from scripts.per_pixel_carbon import carbon_stock, co2e
    c = carbon_stock(50)
    co2 = co2e(50)
    assert abs(co2 / c - 44 / 12) < 0.01


def test_chave_monotonic():
    """AGB monotonically increases with treecover."""
    from scripts.per_pixel_carbon import chave_agb
    prev = 0
    for tc in range(0, 101, 10):
        v = chave_agb(tc)
        assert v >= prev, f"AGB not monotonic at tc={tc}"
        prev = v