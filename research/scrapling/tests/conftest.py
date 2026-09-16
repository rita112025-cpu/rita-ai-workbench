"""Shared offline fixtures.

Unit tests use a fake transport and local HTML fixtures, so nothing here touches
the network. Scrapling's parser is real -- it is a declared runtime dependency
and installs without a browser.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

SRC = Path(__file__).resolve().parents[1] / "src"
if str(SRC) not in sys.path:  # pragma: no cover - import bootstrap
    sys.path.insert(0, str(SRC))

from rita_scrapling.errors import CollectorError  # noqa: E402
from rita_scrapling.models import RawResponse  # noqa: E402

FIXTURES = Path(__file__).parent / "fixtures"


def load_fixture(name: str) -> str:
    return (FIXTURES / name).read_text(encoding="utf-8")


class FakeTransport:
    """Replays canned responses, or raises, in order."""

    def __init__(self, *responses: RawResponse | CollectorError) -> None:
        self._queue = list(responses)
        self.calls: list[tuple[str, float]] = []

    def get(self, url: str, *, timeout: float = 30.0) -> RawResponse:
        self.calls.append((url, timeout))
        if not self._queue:
            raise AssertionError(f"FakeTransport ran out of responses at {url!r}")
        item = self._queue.pop(0)
        if isinstance(item, CollectorError):
            raise item
        return item


def response(
    body: str,
    *,
    url: str = "https://shop.example/p/1",
    status: int = 200,
    content_type: str = "text/html; charset=utf-8",
) -> RawResponse:
    return RawResponse(
        url=url,
        final_url=url,
        status_code=status,
        body=body,
        headers={"content-type": content_type},
        fetched_at="2026-09-16T00:00:00+00:00",
        attempts=1,
        elapsed_s=0.12,
    )


@pytest.fixture
def product_v1() -> str:
    return load_fixture("product_v1.html")


@pytest.fixture
def product_v2() -> str:
    return load_fixture("product_v2.html")


@pytest.fixture
def empty_shell() -> str:
    return load_fixture("empty_shell.html")
