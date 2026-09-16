"""Collector behaviour: normalization, evidence, dynamic seam."""

from __future__ import annotations

import json

import pytest

from conftest import FakeTransport, response
from rita_scrapling import __version__
from rita_scrapling.collector import ScraplingCollector
from rita_scrapling.dynamic import UnavailableRenderer
from rita_scrapling.errors import CollectorError, ErrorCode
from rita_scrapling.evidence import EvidenceStore
from rita_scrapling.models import ExtractionRule, RawResponse


def collector(tmp_path, transport, **kwargs) -> ScraplingCollector:
    return ScraplingCollector(
        transport=transport, evidence=EvidenceStore(tmp_path / "output"), **kwargs
    )


def test_fetch_produces_a_normalized_result(tmp_path, product_v1):
    transport = FakeTransport(response(product_v1))

    result = collector(tmp_path, transport).fetch("https://shop.example/p/1")

    assert result.status == "success"
    assert result.source_url == "https://shop.example/p/1"
    assert result.title == "Widget Pro - Example Shop"
    assert "Ships in two business days." in (result.text or "")
    assert result.collector == "scrapling"
    assert result.collector_version == __version__
    assert result.fetched_at.endswith("+00:00")
    assert result.metadata["http_status"] == 200
    assert result.metadata["rendered"] is False


def test_fetch_applies_extraction_rules(tmp_path, product_v1):
    transport = FakeTransport(response(product_v1))
    rules = [ExtractionRule(name="price", selector=".price")]

    result = collector(tmp_path, transport).fetch("https://shop.example/p/1", rules=rules)

    assert result.metadata["fields"] == {"price": "$100"}


def test_raw_evidence_is_written_and_referenced(tmp_path, product_v1):
    transport = FakeTransport(response(product_v1))

    result = collector(tmp_path, transport).fetch("https://shop.example/p/1")

    raw = tmp_path / "output" / "raw"
    html_files = list(raw.rglob("*.html"))
    meta_files = list(raw.rglob("*.meta.json"))
    assert len(html_files) == 1
    assert len(meta_files) == 1
    assert result.raw_path == str(html_files[0])
    # The stored bytes are the response verbatim, not a re-serialized parse.
    assert html_files[0].read_text(encoding="utf-8") == product_v1

    meta = json.loads(meta_files[0].read_text(encoding="utf-8"))
    assert meta["source_url"] == "https://shop.example/p/1"
    assert meta["http_status"] == 200
    assert meta["collector"] == "scrapling"
    assert meta["collector_version"] == __version__
    assert meta["fetched_at"] == "2026-09-16T00:00:00+00:00"


def test_normalized_output_is_written_with_the_source_url(tmp_path, product_v1):
    transport = FakeTransport(response(product_v1))

    collector(tmp_path, transport).fetch("https://shop.example/p/1")

    files = list((tmp_path / "output" / "normalized").rglob("*.json"))
    assert len(files) == 1
    payload = json.loads(files[0].read_text(encoding="utf-8"))
    assert payload["source_url"] == "https://shop.example/p/1"
    assert payload["collector"] == "scrapling"
    assert payload["raw_path"]


def test_evidence_can_be_turned_off(tmp_path, product_v1):
    transport = FakeTransport(response(product_v1))

    result = collector(tmp_path, transport, save_evidence=False).fetch("https://shop.example/p/1")

    assert result.raw_path is None
    assert not (tmp_path / "output").exists()


def test_a_javascript_shell_is_not_reported_as_success(tmp_path, empty_shell):
    # HTTP 200 with a <div id="root"></div> and nothing else is not data.
    transport = FakeTransport(response(empty_shell))

    with pytest.raises(CollectorError) as excinfo:
        collector(tmp_path, transport).fetch("https://shop.example/p/1")

    assert excinfo.value.code is ErrorCode.EMPTY_BODY


def test_raw_evidence_survives_a_failed_extraction(tmp_path, empty_shell):
    transport = FakeTransport(response(empty_shell))

    with pytest.raises(CollectorError):
        collector(tmp_path, transport).fetch("https://shop.example/p/1")

    # Written before parsing, so the page can still be inspected afterwards.
    assert list((tmp_path / "output" / "raw").rglob("*.html"))


def test_transport_errors_reach_the_caller_classified(tmp_path):
    transport = FakeTransport(
        CollectorError(ErrorCode.RATE_LIMITED, "slow down", url="https://shop.example/p/1")
    )

    with pytest.raises(CollectorError) as excinfo:
        collector(tmp_path, transport).fetch("https://shop.example/p/1")

    assert excinfo.value.code is ErrorCode.RATE_LIMITED


def test_invalid_url_never_reaches_the_transport(tmp_path):
    transport = FakeTransport()

    with pytest.raises(CollectorError) as excinfo:
        collector(tmp_path, transport).fetch("file:///etc/passwd")

    assert excinfo.value.code is ErrorCode.INVALID_URL
    assert transport.calls == []


def test_repeated_fetches_produce_the_same_normalized_content(tmp_path, product_v1):
    transport = FakeTransport(response(product_v1), response(product_v1))
    subject = collector(tmp_path, transport)

    first = subject.fetch("https://shop.example/p/1")
    second = subject.fetch("https://shop.example/p/1")

    assert first.title == second.title
    assert first.text == second.text


# -- dynamic seam -----------------------------------------------------------


def test_fetch_dynamic_refuses_without_a_renderer(tmp_path):
    transport = FakeTransport()

    with pytest.raises(CollectorError) as excinfo:
        collector(tmp_path, transport).fetch_dynamic("https://shop.example/p/1")

    assert excinfo.value.code is ErrorCode.DEPENDENCY_UNAVAILABLE
    assert "patchright" in excinfo.value.message
    # It must not silently fall back to a static fetch.
    assert transport.calls == []


def test_fetch_dynamic_uses_an_injected_renderer(tmp_path, product_v1):
    class StubRenderer:
        def __init__(self) -> None:
            self.calls: list[tuple[str, float, str | None]] = []

        def render(self, url, *, timeout=45.0, wait_selector=None):
            self.calls.append((url, timeout, wait_selector))
            return RawResponse(url=url, final_url=url, status_code=200, body=product_v1)

    renderer = StubRenderer()
    result = collector(tmp_path, FakeTransport(), renderer=renderer).fetch_dynamic(
        "https://shop.example/p/1", timeout=12.0, wait_selector=".price"
    )

    assert result.metadata["rendered"] is True
    assert result.title == "Widget Pro - Example Shop"
    assert renderer.calls == [("https://shop.example/p/1", 12.0, ".price")]


def test_unavailable_renderer_states_why(tmp_path):
    with pytest.raises(CollectorError) as excinfo:
        UnavailableRenderer().render("https://shop.example/p/1")

    assert excinfo.value.code is ErrorCode.DEPENDENCY_UNAVAILABLE


def test_error_string_carries_code_and_status():
    error = CollectorError(
        ErrorCode.HTTP_ERROR, "HTTP 404", url="https://example.com", status_code=404
    )

    assert "HTTP_ERROR" in str(error)
    assert "status=404" in str(error)
