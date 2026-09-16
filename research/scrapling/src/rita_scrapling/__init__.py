"""Scrapling-based public web collector for the Rita AI workbench.

Scope: public web acquisition, HTML extraction, structured extraction, adaptive
selector support, and a seam for optional JavaScript rendering. It targets
publicly accessible content and does not override site access controls, robots
policies, contractual restrictions, authentication requirements or rate limits.
"""

from __future__ import annotations

from .collector import ScraplingCollector
from .dynamic import DynamicRenderer, UnavailableRenderer
from .errors import CollectorError, ErrorCode
from .evidence import EvidencePaths, EvidenceStore
from .extraction import Document, extract_from_html
from .http import RetryPolicy, Transport, UrllibTransport, validate_url
from .models import (
    PACKAGE_VERSION,
    ExtractionRule,
    FetchResult,
    RawResponse,
)

__version__ = PACKAGE_VERSION

__all__ = [
    "CollectorError",
    "Document",
    "DynamicRenderer",
    "ErrorCode",
    "EvidencePaths",
    "EvidenceStore",
    "ExtractionRule",
    "FetchResult",
    "RawResponse",
    "RetryPolicy",
    "ScraplingCollector",
    "Transport",
    "UnavailableRenderer",
    "UrllibTransport",
    "__version__",
    "extract_from_html",
    "validate_url",
]
