"""Parsing and rule-based extraction against local fixtures."""

from __future__ import annotations

import pytest

from rita_scrapling.errors import CollectorError, ErrorCode
from rita_scrapling.extraction import Document, extract_from_html
from rita_scrapling.models import ExtractionRule


def test_title_is_extracted(product_v1):
    assert Document(product_v1).title() == "Widget Pro - Example Shop"


def test_text_excludes_script_and_style(product_v1):
    text = Document(product_v1).text()

    assert "Widget Pro" in text
    assert "Ships in two business days." in text
    # The fixture carries both; folding them into the text would silently
    # poison every downstream consumer.
    assert "var tracking" not in text
    assert "color: red" not in text


def test_a_javascript_shell_has_a_title_but_no_body_text(empty_shell):
    document = Document(empty_shell)

    assert document.title() == "Loading"
    assert document.text() == ""


def test_rule_returns_the_element_text(product_v1):
    rule = ExtractionRule(name="price", selector=".price")

    assert Document(product_v1).select(rule) == "$100"


def test_rule_can_read_an_attribute(product_v1):
    rule = ExtractionRule(name="lang", selector="html", attribute="lang")

    assert Document(product_v1).select(rule) == "en"


def test_rule_with_many_returns_every_match(product_v1):
    rule = ExtractionRule(name="cells", selector=".product-card span", many=True)

    assert Document(product_v1).select(rule) == ["$100", "In stock"]


def test_optional_missing_selector_returns_none(product_v1):
    rule = ExtractionRule(name="discount", selector=".discount")

    assert Document(product_v1).select(rule) is None


def test_optional_missing_selector_with_many_returns_empty(product_v1):
    rule = ExtractionRule(name="discounts", selector=".discount", many=True)

    assert Document(product_v1).select(rule) == []


def test_required_missing_selector_is_an_extraction_error(product_v1):
    rule = ExtractionRule(name="discount", selector=".discount", required=True)

    with pytest.raises(CollectorError) as excinfo:
        Document(product_v1).select(rule)

    assert excinfo.value.code is ErrorCode.EXTRACTION_ERROR
    assert "discount" in excinfo.value.message


def test_an_unusable_selector_is_an_extraction_error(product_v1):
    rule = ExtractionRule(name="broken", selector="div::::")

    with pytest.raises(CollectorError) as excinfo:
        Document(product_v1).select(rule)

    assert excinfo.value.code is ErrorCode.EXTRACTION_ERROR


def test_extract_applies_every_rule(product_v1):
    rules = [
        ExtractionRule(name="price", selector=".price"),
        ExtractionRule(name="stock", selector=".stock"),
        ExtractionRule(name="missing", selector=".nope"),
    ]

    assert extract_from_html(product_v1, rules) == {
        "price": "$100",
        "stock": "In stock",
        "missing": None,
    }


def test_adaptive_without_storage_is_refused(product_v1):
    with pytest.raises(CollectorError) as excinfo:
        Document(product_v1, adaptive=True)

    assert excinfo.value.code is ErrorCode.EXTRACTION_ERROR
