"""Adaptive element relocation, exercised against real Scrapling storage.

The fixtures change both the container and the target element -- class names and
tag names -- so a passing test means Scrapling genuinely relocated the element
rather than the old selector still happening to match.
"""

from __future__ import annotations

from rita_scrapling.extraction import Document
from rita_scrapling.models import ExtractionRule

PRICE = ExtractionRule(name="price", selector=".price", adaptive=True)
STOCK = ExtractionRule(name="stock", selector=".stock", adaptive=True)
URL = "https://shop.example/p/1"


def test_the_old_selector_really_does_break_on_v2(product_v2):
    # Guards the guard: if this ever passes, the relocation test below proves
    # nothing.
    assert Document(product_v2).select(ExtractionRule(name="price", selector=".price")) is None


def test_element_is_relocated_after_the_dom_changes(tmp_path, product_v1, product_v2):
    storage = tmp_path / "elements.db"

    first = Document(product_v1, url=URL, adaptive=True, storage_file=storage)
    assert first.select(PRICE) == "$100"
    assert storage.exists()

    second = Document(product_v2, url=URL, adaptive=True, storage_file=storage)
    assert second.select(PRICE) == "$100"


def test_relocation_handles_several_fields(tmp_path, product_v1, product_v2):
    storage = tmp_path / "elements.db"

    first = Document(product_v1, url=URL, adaptive=True, storage_file=storage)
    assert first.extract([PRICE, STOCK]) == {"price": "$100", "stock": "In stock"}

    second = Document(product_v2, url=URL, adaptive=True, storage_file=storage)
    assert second.extract([PRICE, STOCK]) == {"price": "$100", "stock": "In stock"}


def test_nothing_is_relocated_without_a_prior_save(tmp_path, product_v2):
    # A cold store cannot invent an element; the rule is optional, so it is None.
    storage = tmp_path / "elements.db"

    assert Document(product_v2, url=URL, adaptive=True, storage_file=storage).select(PRICE) is None


def test_explicit_save_records_the_element(tmp_path, product_v1, product_v2):
    storage = tmp_path / "elements.db"

    first = Document(product_v1, url=URL, adaptive=True, storage_file=storage)
    assert first.save_for_adaptive(PRICE) is True

    second = Document(product_v2, url=URL, adaptive=True, storage_file=storage)
    assert second.select(PRICE) == "$100"


def test_save_reports_false_when_there_is_nothing_to_save(tmp_path, product_v2):
    storage = tmp_path / "elements.db"
    document = Document(product_v2, url=URL, adaptive=True, storage_file=storage)

    assert document.save_for_adaptive(PRICE) is False


def test_adaptive_is_off_by_default(product_v1):
    assert Document(product_v1).adaptive_enabled is False
