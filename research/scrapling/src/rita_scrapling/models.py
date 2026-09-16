"""Normalized result types.

No Scrapling object ever crosses this boundary. Application code sees
:class:`FetchResult` and nothing else, so swapping the parser or the transport
later is a change inside this package.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Mapping

#: Version of this collector implementation, stamped onto every result.
PACKAGE_VERSION = "0.1.0"

COLLECTOR_NAME = "scrapling"


def utc_now_iso() -> str:
    """Timestamp used on every result, always UTC and always suffixed."""
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


@dataclass(frozen=True)
class RawResponse:
    """What the transport returned, before any parsing.

    Kept separate from :class:`FetchResult` so raw evidence can be written even
    when extraction later fails.
    """

    url: str
    final_url: str
    status_code: int
    body: str
    headers: Mapping[str, str] = field(default_factory=dict)
    fetched_at: str = field(default_factory=utc_now_iso)
    attempts: int = 1
    elapsed_s: float = 0.0

    @property
    def content_type(self) -> str:
        return self.headers.get("content-type", "")


@dataclass(frozen=True)
class FetchResult:
    """The only shape the rest of the project consumes."""

    source_url: str
    fetched_at: str
    status: str
    title: str | None = None
    text: str | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)
    raw_path: str | None = None
    collector: str = COLLECTOR_NAME
    collector_version: str = PACKAGE_VERSION

    def to_dict(self) -> dict[str, Any]:
        return {
            "source_url": self.source_url,
            "fetched_at": self.fetched_at,
            "status": self.status,
            "title": self.title,
            "text": self.text,
            "metadata": dict(self.metadata),
            "raw_path": self.raw_path,
            "collector": self.collector,
            "collector_version": self.collector_version,
        }


@dataclass(frozen=True)
class ExtractionRule:
    """One named field to pull out of a document.

    ``adaptive`` opts this rule into Scrapling's element relocation: the element
    matched on a first successful run is remembered, and a later run whose
    selector no longer matches tries to find the same element again.
    """

    name: str
    selector: str
    attribute: str | None = None
    many: bool = False
    required: bool = False
    adaptive: bool = False
