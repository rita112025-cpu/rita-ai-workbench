"""Opt-in tests against a live public site.

Deselected by default (``addopts = -m 'not integration'``). Run deliberately:

    pytest -m integration

Target is public, needs no login, has no CAPTCHA, is server-rendered and is
about as stable as the web gets. Assertions are on actual expected content, not
on a non-empty string.
"""

from __future__ import annotations

import pytest

from rita_scrapling.collector import ScraplingCollector
from rita_scrapling.evidence import EvidenceStore
from rita_scrapling.models import ExtractionRule

pytestmark = pytest.mark.integration

STATIC_URL = "https://example.com"
JS_HEAVY_URL = "https://todomvc.com/examples/react/dist/"


def _collector(tmp_path, **kwargs) -> ScraplingCollector:
    return ScraplingCollector(evidence=EvidenceStore(tmp_path / "output"), **kwargs)


def test_static_page_returns_real_content(tmp_path):
    result = _collector(tmp_path).fetch(STATIC_URL, timeout=30)

    assert result.status == "success"
    assert result.source_url == STATIC_URL
    assert result.metadata["http_status"] == 200
    assert result.title == "Example Domain"
    assert "documentation examples" in (result.text or "")
    assert result.collector == "scrapling"


def test_static_page_writes_raw_evidence(tmp_path):
    result = _collector(tmp_path).fetch(STATIC_URL, timeout=30)

    raw_files = list((tmp_path / "output" / "raw").rglob("*.html"))
    normalized = list((tmp_path / "output" / "normalized").rglob("*.json"))
    assert len(raw_files) == 1
    assert len(normalized) == 1
    assert result.raw_path == str(raw_files[0])
    assert "Example Domain" in raw_files[0].read_text(encoding="utf-8")


def test_structured_extraction_against_the_live_page(tmp_path):
    rules = [ExtractionRule(name="heading", selector="h1", required=True)]

    result = _collector(tmp_path).fetch(STATIC_URL, rules=rules, timeout=30)

    assert result.metadata["fields"]["heading"] == "Example Domain"


def test_a_client_rendered_page_is_visibly_incomplete_without_a_renderer(tmp_path):
    """The JS-heavy case, recorded honestly rather than claimed.

    TodoMVC's React build is public, has no login and no CAPTCHA, and renders
    its list in the browser. A static fetch returns HTTP 200 and a title, and
    none of the application content -- which is exactly why a static fetch
    returning 200 must never be read as "the data is there".
    """
    result = _collector(tmp_path).fetch(JS_HEAVY_URL, timeout=30)

    assert result.metadata["http_status"] == 200
    assert result.title == "TodoMVC: React"
    text = result.text or ""
    # Only the static chrome is present; the app's own rendered rows are not.
    assert "Double-click to edit a todo" in text
    assert len(text) < 400


def test_dynamic_fetch_is_refused_rather_than_silently_downgraded(tmp_path):
    from rita_scrapling.errors import CollectorError, ErrorCode

    with pytest.raises(CollectorError) as excinfo:
        _collector(tmp_path).fetch_dynamic(JS_HEAVY_URL)

    assert excinfo.value.code is ErrorCode.DEPENDENCY_UNAVAILABLE


def test_repeated_fetches_are_stable(tmp_path):
    subject = _collector(tmp_path)

    first = subject.fetch(STATIC_URL, timeout=30)
    second = subject.fetch(STATIC_URL, timeout=30)

    assert first.title == second.title
    assert first.text == second.text
