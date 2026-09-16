"""Error taxonomy for the Scrapling collector.

Callers branch on :class:`ErrorCode`. A bare "fetch failed" tells an operator
nothing: a 429 needs backoff, a 404 needs the URL fixed, a selector miss needs
the extraction rule updated, and a render failure needs a browser.
"""

from __future__ import annotations

from enum import Enum


class ErrorCode(str, Enum):
    """Why an acquisition failed."""

    INVALID_URL = "INVALID_URL"
    """Not a public http(s) URL we are willing to request."""

    NETWORK_ERROR = "NETWORK_ERROR"
    """DNS failure, refused connection or transport error before a response."""

    TIMEOUT = "TIMEOUT"
    """The request exceeded its wall-clock budget."""

    HTTP_ERROR = "HTTP_ERROR"
    """A response arrived with a non-success status (404, 500, ...)."""

    RATE_LIMITED = "RATE_LIMITED"
    """HTTP 429, or a 503 carrying Retry-After. Distinct from HTTP_ERROR so
    callers can back off rather than retry blindly or give up."""

    EMPTY_BODY = "EMPTY_BODY"
    """A successful status carrying nothing usable. HTTP 200 is not data."""

    EXTRACTION_ERROR = "EXTRACTION_ERROR"
    """The document parsed, but a required selector matched nothing."""

    RENDER_ERROR = "RENDER_ERROR"
    """A JavaScript-rendering fetch was attempted and failed."""

    DEPENDENCY_UNAVAILABLE = "DEPENDENCY_UNAVAILABLE"
    """A required optional component is not installed or not permitted here."""


class CollectorError(RuntimeError):
    """A classified acquisition failure."""

    def __init__(
        self,
        code: ErrorCode,
        message: str,
        *,
        url: str | None = None,
        status_code: int | None = None,
        retry_after_s: float | None = None,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.url = url
        self.status_code = status_code
        self.retry_after_s = retry_after_s

    @property
    def retryable(self) -> bool:
        """Whether retrying the same request could plausibly succeed."""
        return self.code in _RETRYABLE_CODES

    def __str__(self) -> str:
        parts = [f"[{self.code.value}] {self.message}"]
        if self.status_code is not None:
            parts.append(f"status={self.status_code}")
        if self.url:
            parts.append(f"url={self.url}")
        return " ".join(parts)


_RETRYABLE_CODES = frozenset({ErrorCode.NETWORK_ERROR, ErrorCode.TIMEOUT, ErrorCode.RATE_LIMITED})
