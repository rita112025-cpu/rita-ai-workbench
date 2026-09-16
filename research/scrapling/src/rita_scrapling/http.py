"""Transport layer: one conservative, bounded, retrying HTTP GET.

Scrapling 0.4.15 cannot supply this. Its `fetchers` extra -- including the plain
HTTP ``Fetcher`` -- imports patchright at module level
(``scrapling/engines/toolbelt/convertor.py``), and this project does not install
or integrate patchright. So the transport is the standard library, sitting
behind a protocol; Scrapling is used for what it is uniquely good at, parsing
and adaptive element relocation.

Defaults are deliberately timid: one request at a time, a real delay between
requests, three attempts at most, exponential backoff, and ``Retry-After``
honoured when the server sends it.
"""

from __future__ import annotations

import socket
import time
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from typing import Callable, Protocol
from urllib.parse import urlparse

from .errors import CollectorError, ErrorCode
from .models import RawResponse

DEFAULT_TIMEOUT_S = 30.0
DEFAULT_USER_AGENT = (
    "rita-scrapling-collector/0.1 (+https://github.com/rita112025-cpu/rita-ai-workbench)"
)

#: 503 is included because it is usually "try later", and it frequently carries
#: Retry-After. 500/502/504 are transient often enough to be worth one retry.
DEFAULT_RETRYABLE_STATUSES = frozenset({429, 500, 502, 503, 504})

MAX_RETRY_AFTER_S = 120.0


@dataclass(frozen=True)
class RetryPolicy:
    """Conservative by default. Raise the numbers deliberately, never casually."""

    max_attempts: int = 3
    backoff_base_s: float = 1.0
    backoff_max_s: float = 10.0
    retryable_statuses: frozenset[int] = field(default=DEFAULT_RETRYABLE_STATUSES)
    respect_retry_after: bool = True

    def delay_for(self, attempt: int, *, retry_after_s: float | None = None) -> float:
        """Seconds to wait before attempt ``attempt + 1`` (1-based attempts)."""
        if self.respect_retry_after and retry_after_s is not None:
            # Clamp: a hostile or broken server must not park us for an hour.
            return max(0.0, min(retry_after_s, MAX_RETRY_AFTER_S))
        return min(self.backoff_base_s * (2 ** (attempt - 1)), self.backoff_max_s)


class Transport(Protocol):
    """Seam that lets every unit test run without a network."""

    def get(self, url: str, *, timeout: float = DEFAULT_TIMEOUT_S) -> RawResponse: ...


def validate_url(url: str) -> str:
    """Accept only public http(s) URLs."""
    try:
        parsed = urlparse(url)
    except ValueError as exc:
        raise CollectorError(ErrorCode.INVALID_URL, f"unparseable URL: {url!r}", url=url) from exc
    if parsed.scheme not in ("http", "https"):
        raise CollectorError(
            ErrorCode.INVALID_URL,
            f"only http(s) is supported, got {parsed.scheme or 'no scheme'!r}",
            url=url,
        )
    if not parsed.netloc:
        raise CollectorError(ErrorCode.INVALID_URL, f"URL has no host: {url!r}", url=url)
    return url


def parse_retry_after(value: str | None) -> float | None:
    """Parse a ``Retry-After`` header expressed in seconds.

    The HTTP-date form is ignored rather than half-parsed; the caller then falls
    back to exponential backoff, which is the safe direction to be wrong in.
    """
    if not value:
        return None
    try:
        seconds = float(value.strip())
    except ValueError:
        return None
    return seconds if seconds >= 0 else None


class UrllibTransport:
    """Standard-library GET with bounded retries and a polite request interval."""

    def __init__(
        self,
        *,
        user_agent: str = DEFAULT_USER_AGENT,
        retry_policy: RetryPolicy | None = None,
        min_interval_s: float = 1.0,
        sleep: Callable[[float], None] = time.sleep,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        self._user_agent = user_agent
        self._retry = retry_policy or RetryPolicy()
        self._min_interval_s = min_interval_s
        self._sleep = sleep
        self._clock = clock
        self._last_request_at: float | None = None

    @property
    def retry_policy(self) -> RetryPolicy:
        return self._retry

    def _throttle(self) -> None:
        """One request at a time, never faster than the configured interval."""
        if self._last_request_at is None or self._min_interval_s <= 0:
            return
        waited = self._clock() - self._last_request_at
        if waited < self._min_interval_s:
            self._sleep(self._min_interval_s - waited)

    def _open(self, url: str, timeout: float) -> RawResponse:
        request = urllib.request.Request(url, headers={"User-Agent": self._user_agent})
        started = self._clock()
        with urllib.request.urlopen(request, timeout=timeout) as response:  # noqa: S310
            charset = response.headers.get_content_charset() or "utf-8"
            body = response.read().decode(charset, errors="replace")
            headers = {k.lower(): v for k, v in response.headers.items()}
            return RawResponse(
                url=url,
                final_url=response.geturl(),
                status_code=int(response.status),
                body=body,
                headers=headers,
                elapsed_s=self._clock() - started,
            )

    def get(self, url: str, *, timeout: float = DEFAULT_TIMEOUT_S) -> RawResponse:
        validate_url(url)
        last_error: CollectorError | None = None

        for attempt in range(1, self._retry.max_attempts + 1):
            self._throttle()
            self._last_request_at = self._clock()
            try:
                response = self._open(url, timeout)
            except urllib.error.HTTPError as exc:
                last_error = _classify_http_error(exc, url)
            except socket.timeout as exc:
                last_error = CollectorError(
                    ErrorCode.TIMEOUT, f"timed out after {timeout:g}s", url=url
                )
                last_error.__cause__ = exc
            except urllib.error.URLError as exc:
                last_error = _classify_url_error(exc, url, timeout)
            except OSError as exc:
                last_error = CollectorError(
                    ErrorCode.NETWORK_ERROR, f"cannot reach {url}: {exc}", url=url
                )
            else:
                if not response.body.strip():
                    # A 200 with an empty body is not a successful acquisition.
                    raise CollectorError(
                        ErrorCode.EMPTY_BODY,
                        f"empty body from {url}",
                        url=url,
                        status_code=response.status_code,
                    )
                return RawResponse(
                    url=response.url,
                    final_url=response.final_url,
                    status_code=response.status_code,
                    body=response.body,
                    headers=response.headers,
                    fetched_at=response.fetched_at,
                    attempts=attempt,
                    elapsed_s=response.elapsed_s,
                )

            retryable = last_error.retryable or (
                last_error.status_code in self._retry.retryable_statuses
                if last_error.status_code is not None
                else False
            )
            if not retryable or attempt >= self._retry.max_attempts:
                raise last_error
            self._sleep(self._retry.delay_for(attempt, retry_after_s=last_error.retry_after_s))

        raise (
            last_error
            if last_error
            else CollectorError(  # pragma: no cover - unreachable
                ErrorCode.NETWORK_ERROR, f"no attempt was made for {url}", url=url
            )
        )


def _classify_http_error(exc: urllib.error.HTTPError, url: str) -> CollectorError:
    retry_after = parse_retry_after(exc.headers.get("Retry-After") if exc.headers else None)
    if exc.code == 429:
        return CollectorError(
            ErrorCode.RATE_LIMITED,
            f"rate limited by {url}",
            url=url,
            status_code=429,
            retry_after_s=retry_after,
        )
    return CollectorError(
        ErrorCode.HTTP_ERROR,
        f"HTTP {exc.code} from {url}",
        url=url,
        status_code=exc.code,
        retry_after_s=retry_after,
    )


def _classify_url_error(exc: urllib.error.URLError, url: str, timeout: float) -> CollectorError:
    reason = exc.reason
    if isinstance(reason, socket.timeout):
        return CollectorError(ErrorCode.TIMEOUT, f"timed out after {timeout:g}s", url=url)
    if isinstance(reason, socket.gaierror):
        return CollectorError(ErrorCode.NETWORK_ERROR, f"DNS failure for {url}", url=url)
    return CollectorError(ErrorCode.NETWORK_ERROR, f"cannot reach {url}: {reason}", url=url)
