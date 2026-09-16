"""The collector the rest of the project talks to.

``fetch`` / ``fetch_dynamic`` / ``extract`` -- three entry points, one normalized
result type, one error taxonomy. Transport, renderer and evidence store are all
injectable, so every unit test runs offline.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping, Sequence

from .dynamic import DEFAULT_RENDER_TIMEOUT_S, DynamicRenderer, UnavailableRenderer
from .errors import CollectorError, ErrorCode
from .evidence import EvidenceStore
from .extraction import Document
from .http import DEFAULT_TIMEOUT_S, Transport, UrllibTransport, validate_url
from .models import (
    COLLECTOR_NAME,
    PACKAGE_VERSION,
    ExtractionRule,
    FetchResult,
    RawResponse,
    utc_now_iso,
)

DEFAULT_ADAPTIVE_STORAGE = "output/adaptive/elements.db"


class ScraplingCollector:
    """Public-web acquisition: fetch, keep the evidence, normalize, extract."""

    def __init__(
        self,
        *,
        transport: Transport | None = None,
        renderer: DynamicRenderer | None = None,
        evidence: EvidenceStore | None = None,
        timeout: float = DEFAULT_TIMEOUT_S,
        save_evidence: bool = True,
        adaptive: bool = False,
        adaptive_storage: str | Path = DEFAULT_ADAPTIVE_STORAGE,
    ) -> None:
        self._transport: Transport = transport or UrllibTransport()
        self._renderer: DynamicRenderer = renderer or UnavailableRenderer()
        self._evidence = evidence or EvidenceStore()
        self._timeout = timeout
        self._save_evidence = save_evidence
        self._adaptive = adaptive
        self._adaptive_storage = Path(adaptive_storage)

    # -- acquisition ---------------------------------------------------------

    def fetch(
        self,
        url: str,
        *,
        rules: Sequence[ExtractionRule] = (),
        timeout: float | None = None,
    ) -> FetchResult:
        """Fetch a server-rendered page and normalize it."""
        validate_url(url)
        response = self._transport.get(url, timeout=timeout or self._timeout)
        return self._normalize(response, rules=rules, rendered=False)

    def fetch_dynamic(
        self,
        url: str,
        *,
        rules: Sequence[ExtractionRule] = (),
        timeout: float = DEFAULT_RENDER_TIMEOUT_S,
        wait_selector: str | None = None,
    ) -> FetchResult:
        """Fetch a page with JavaScript executed.

        Raises ``DEPENDENCY_UNAVAILABLE`` unless a renderer was injected. It
        deliberately does not fall back to :meth:`fetch`: returning a static
        snapshot of a page that needs JavaScript would look like success while
        the content the caller asked for was never rendered.
        """
        validate_url(url)
        response = self._renderer.render(url, timeout=timeout, wait_selector=wait_selector)
        return self._normalize(response, rules=rules, rendered=True)

    # -- extraction ----------------------------------------------------------

    def extract(
        self,
        html: str,
        rules: Sequence[ExtractionRule],
        *,
        url: str = "",
    ) -> Mapping[str, Any]:
        """Apply extraction rules to HTML you already have."""
        return self._document(html, url).extract(rules)

    def _document(self, html: str, url: str) -> Document:
        return Document(
            html,
            url=url,
            adaptive=self._adaptive,
            storage_file=self._adaptive_storage if self._adaptive else None,
        )

    # -- internals -----------------------------------------------------------

    def _normalize(
        self,
        response: RawResponse,
        *,
        rules: Sequence[ExtractionRule],
        rendered: bool,
    ) -> FetchResult:
        raw_path: str | None = None
        if self._save_evidence:
            # Evidence is written before extraction, so a page that fails to
            # parse can still be inspected afterwards.
            paths = self._evidence.write_raw(
                response, collector=COLLECTOR_NAME, collector_version=PACKAGE_VERSION
            )
            raw_path = str(paths.raw_html)

        document = self._document(response.body, response.url)
        title = document.title()
        text = document.text()
        if not text:
            raise CollectorError(
                ErrorCode.EMPTY_BODY,
                f"no readable text in the response from {response.url}",
                url=response.url,
                status_code=response.status_code,
            )

        fields = document.extract(rules) if rules else {}

        result = FetchResult(
            source_url=response.url,
            fetched_at=response.fetched_at or utc_now_iso(),
            status="success",
            title=title,
            text=text,
            metadata={
                "final_url": response.final_url,
                "http_status": response.status_code,
                "content_type": response.content_type,
                "content_chars": len(response.body),
                "text_chars": len(text),
                "attempts": response.attempts,
                "elapsed_s": round(response.elapsed_s, 3),
                "rendered": rendered,
                "adaptive": self._adaptive,
                "fields": fields,
            },
            raw_path=raw_path,
        )

        if self._save_evidence:
            self._evidence.write_normalized(result, response)
        return result
