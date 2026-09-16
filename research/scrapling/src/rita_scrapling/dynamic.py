"""JavaScript-rendering fetch: the seam, and why it is empty here.

Scrapling's ``DynamicFetcher`` is the natural implementation. It cannot be used
in this project: in 0.4.15 importing *any* Scrapling fetcher pulls in patchright
(``scrapling/engines/toolbelt/convertor.py`` imports it at module level), and
installing or integrating patchright is out of scope here.

So this module defines the contract and nothing else. ``fetch_dynamic`` raises
``DEPENDENCY_UNAVAILABLE`` until a renderer is injected, rather than silently
falling back to a static fetch and returning a page whose content never
rendered. A caller that wants rendering supplies a :class:`DynamicRenderer`;
the collector's normalization, evidence and error handling then apply unchanged.
"""

from __future__ import annotations

from typing import Protocol

from .errors import CollectorError, ErrorCode
from .models import RawResponse

DEFAULT_RENDER_TIMEOUT_S = 45.0


class DynamicRenderer(Protocol):
    """Renders a page with JavaScript executed and returns the final DOM.

    Implementations must respect ``timeout``, must terminate the browser
    process on every exit path including failure, and must raise
    :class:`~rita_scrapling.errors.CollectorError` with ``RENDER_ERROR`` or
    ``TIMEOUT`` rather than leaking a driver-specific exception.
    """

    def render(
        self,
        url: str,
        *,
        timeout: float = DEFAULT_RENDER_TIMEOUT_S,
        wait_selector: str | None = None,
    ) -> RawResponse: ...


class UnavailableRenderer:
    """The default. Refuses clearly instead of pretending to render."""

    reason = (
        "no JavaScript renderer is configured: Scrapling's DynamicFetcher requires "
        "patchright, which this project does not install or integrate"
    )

    def render(
        self,
        url: str,
        *,
        timeout: float = DEFAULT_RENDER_TIMEOUT_S,
        wait_selector: str | None = None,
    ) -> RawResponse:
        raise CollectorError(ErrorCode.DEPENDENCY_UNAVAILABLE, self.reason, url=url)
