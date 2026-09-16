"""The one plain-HTTP path in this package.

Agent Reach routes the generic ``web`` channel to Jina Reader, which is an
ordinary HTTP GET returning Markdown. Shelling out to curl for that would add a
binary dependency and an extra failure mode for no benefit, so it uses the
standard library -- behind a protocol, so tests never touch the network.
"""

from __future__ import annotations

import socket
import urllib.error
import urllib.request
from typing import Protocol

from .errors import AgentReachError, ErrorCode

USER_AGENT = "rita-agent-reach/0.1 (+https://github.com/rita112025-cpu/rita-ai-workbench)"


class HttpGetter(Protocol):
    """Returns ``(status_code, body_text)`` or raises :class:`AgentReachError`."""

    def __call__(self, url: str, *, timeout: float) -> tuple[int, str]: ...


def urllib_get(url: str, *, timeout: float) -> tuple[int, str]:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:  # noqa: S310
            charset = response.headers.get_content_charset() or "utf-8"
            body = response.read().decode(charset, errors="replace")
            return int(response.status), body
    except urllib.error.HTTPError as exc:
        # A 4xx/5xx is a real answer from the server, not a transport failure.
        raise AgentReachError(
            ErrorCode.HTTP_ERROR,
            f"HTTP {exc.code} from {url}",
            exit_code=exc.code,
        ) from exc
    except socket.timeout as exc:
        raise AgentReachError(ErrorCode.TIMEOUT, f"timed out after {timeout:g}s: {url}") from exc
    except urllib.error.URLError as exc:
        reason = exc.reason
        if isinstance(reason, socket.timeout):
            raise AgentReachError(
                ErrorCode.TIMEOUT, f"timed out after {timeout:g}s: {url}"
            ) from exc
        raise AgentReachError(ErrorCode.NETWORK_ERROR, f"cannot reach {url}: {reason}") from exc
    except OSError as exc:
        raise AgentReachError(ErrorCode.NETWORK_ERROR, f"cannot reach {url}: {exc}") from exc
