"""Transport behaviour: URL validation, retries, backoff and error classification.

All offline: the socket layer is replaced by a fake opener.
"""

from __future__ import annotations

import socket
import urllib.error

import pytest

from rita_scrapling.errors import CollectorError, ErrorCode
from rita_scrapling.http import (
    RetryPolicy,
    UrllibTransport,
    parse_retry_after,
    validate_url,
)
from rita_scrapling.models import RawResponse


class RecordingSleep:
    def __init__(self) -> None:
        self.delays: list[float] = []

    def __call__(self, seconds: float) -> None:
        self.delays.append(seconds)


def transport_with(*outcomes, **kwargs) -> tuple[UrllibTransport, RecordingSleep, list[str]]:
    """Build a transport whose ``_open`` replays ``outcomes`` in order."""
    sleep = RecordingSleep()
    calls: list[str] = []
    queue = list(outcomes)
    transport = UrllibTransport(sleep=sleep, min_interval_s=0.0, **kwargs)

    def fake_open(url: str, timeout: float) -> RawResponse:
        calls.append(url)
        item = queue.pop(0)
        if isinstance(item, BaseException):
            raise item
        return item

    transport._open = fake_open  # type: ignore[method-assign]
    return transport, sleep, calls


def html_response(url: str = "https://example.com", body: str = "<html>ok</html>") -> RawResponse:
    return RawResponse(url=url, final_url=url, status_code=200, body=body)


def http_error(code: int, headers: dict[str, str] | None = None) -> urllib.error.HTTPError:
    return urllib.error.HTTPError(
        "https://example.com",
        code,
        "boom",
        headers or {},
        None,  # type: ignore[arg-type]
    )


# -- URL validation ---------------------------------------------------------


@pytest.mark.parametrize("url", ["https://example.com", "http://example.com/a?b=c"])
def test_valid_urls_pass(url):
    assert validate_url(url) == url


@pytest.mark.parametrize(
    "url", ["file:///etc/passwd", "ftp://example.com", "not-a-url", "", "https://"]
)
def test_invalid_urls_are_classified(url):
    with pytest.raises(CollectorError) as excinfo:
        validate_url(url)

    assert excinfo.value.code is ErrorCode.INVALID_URL


# -- success ----------------------------------------------------------------


def test_successful_fetch_returns_the_body():
    transport, sleep, calls = transport_with(html_response())

    result = transport.get("https://example.com")

    assert result.status_code == 200
    assert result.body == "<html>ok</html>"
    assert result.attempts == 1
    assert sleep.delays == []
    assert len(calls) == 1


def test_a_200_with_an_empty_body_is_not_success():
    transport, _, _ = transport_with(html_response(body="   \n  "))

    with pytest.raises(CollectorError) as excinfo:
        transport.get("https://example.com")

    assert excinfo.value.code is ErrorCode.EMPTY_BODY


# -- non-retryable ----------------------------------------------------------


def test_404_is_http_error_and_is_not_retried():
    transport, sleep, calls = transport_with(http_error(404))

    with pytest.raises(CollectorError) as excinfo:
        transport.get("https://example.com")

    assert excinfo.value.code is ErrorCode.HTTP_ERROR
    assert excinfo.value.status_code == 404
    assert excinfo.value.retryable is False
    assert len(calls) == 1
    assert sleep.delays == []


# -- rate limiting ----------------------------------------------------------


def test_429_is_rate_limited_not_a_generic_http_error():
    transport, _, _ = transport_with(http_error(429), http_error(429), http_error(429))

    with pytest.raises(CollectorError) as excinfo:
        transport.get("https://example.com")

    assert excinfo.value.code is ErrorCode.RATE_LIMITED
    assert excinfo.value.status_code == 429


def test_429_is_retried_and_recovers():
    transport, sleep, calls = transport_with(http_error(429), html_response())

    result = transport.get("https://example.com")

    assert result.status_code == 200
    assert result.attempts == 2
    assert len(calls) == 2
    assert sleep.delays == [1.0]


def test_retry_after_header_overrides_exponential_backoff():
    transport, sleep, _ = transport_with(http_error(429, {"Retry-After": "7"}), html_response())

    transport.get("https://example.com")

    assert sleep.delays == [7.0]


def test_an_absurd_retry_after_is_clamped():
    transport, sleep, _ = transport_with(http_error(429, {"Retry-After": "99999"}), html_response())

    transport.get("https://example.com")

    assert sleep.delays == [120.0]


@pytest.mark.parametrize("value", [None, "", "Wed, 21 Oct 2026 07:28:00 GMT", "soon", "-1"])
def test_unparseable_retry_after_falls_back_to_backoff(value):
    assert parse_retry_after(value) is None


# -- server errors ----------------------------------------------------------


def test_5xx_is_retried_then_reported():
    transport, sleep, calls = transport_with(http_error(503), http_error(503), http_error(503))

    with pytest.raises(CollectorError) as excinfo:
        transport.get("https://example.com")

    assert excinfo.value.code is ErrorCode.HTTP_ERROR
    assert excinfo.value.status_code == 503
    assert len(calls) == 3
    assert sleep.delays == [1.0, 2.0]


def test_backoff_is_exponential_and_capped():
    policy = RetryPolicy(max_attempts=5, backoff_base_s=1.0, backoff_max_s=4.0)

    assert [policy.delay_for(n) for n in (1, 2, 3, 4)] == [1.0, 2.0, 4.0, 4.0]


def test_default_policy_is_conservative():
    policy = RetryPolicy()

    assert policy.max_attempts == 3
    assert 429 in policy.retryable_statuses
    assert 404 not in policy.retryable_statuses


# -- transport failures -----------------------------------------------------


def test_dns_failure_is_network_error():
    transport, _, calls = transport_with(
        urllib.error.URLError(socket.gaierror("no such host")),
        urllib.error.URLError(socket.gaierror("no such host")),
        urllib.error.URLError(socket.gaierror("no such host")),
    )

    with pytest.raises(CollectorError) as excinfo:
        transport.get("https://nonexistent.invalid")

    assert excinfo.value.code is ErrorCode.NETWORK_ERROR
    assert len(calls) == 3


def test_connection_timeout_is_classified_and_retried():
    transport, sleep, calls = transport_with(socket.timeout("slow"), html_response())

    result = transport.get("https://example.com")

    assert result.attempts == 2
    assert len(calls) == 2
    assert sleep.delays == [1.0]


def test_timeout_that_never_recovers_is_reported():
    transport, _, _ = transport_with(
        socket.timeout("slow"), socket.timeout("slow"), socket.timeout("slow")
    )

    with pytest.raises(CollectorError) as excinfo:
        transport.get("https://example.com", timeout=5)

    assert excinfo.value.code is ErrorCode.TIMEOUT


def test_invalid_url_is_rejected_before_any_request():
    transport, _, calls = transport_with(html_response())

    with pytest.raises(CollectorError) as excinfo:
        transport.get("file:///etc/passwd")

    assert excinfo.value.code is ErrorCode.INVALID_URL
    assert calls == []


# -- politeness -------------------------------------------------------------


def test_requests_are_throttled_by_default():
    sleep = RecordingSleep()
    # Clock reads, in order: request 1 stamps 0.0; request 2 throttles at 0.1,
    # then stamps 0.1.
    clock_values = iter([0.0, 0.1, 0.1])
    transport = UrllibTransport(sleep=sleep, min_interval_s=1.0, clock=lambda: next(clock_values))
    transport._open = lambda url, timeout: html_response(url)  # type: ignore[method-assign]

    transport.get("https://example.com")
    transport.get("https://example.com")

    # Second request waited out the remainder of the interval.
    assert sleep.delays and sleep.delays[0] == pytest.approx(0.9, abs=0.01)
