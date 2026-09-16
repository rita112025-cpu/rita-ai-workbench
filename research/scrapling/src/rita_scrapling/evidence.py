"""Raw evidence: keep what was actually fetched, so a claim can be re-checked.

Layout, all runtime artifacts and all git-ignored:

    output/raw/<host>/<timestamp>-<digest>.html    verbatim response body
    output/raw/<host>/<timestamp>-<digest>.meta.json   url, status, headers, timing
    output/normalized/<host>/<timestamp>-<digest>.json normalized FetchResult

The digest is over the source URL, so the same page fetched twice stays grouped
while each run keeps its own timestamped copy. Nothing here is ever committed:
raw pages are somebody else's content and can be large.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse

from .models import FetchResult, RawResponse

DEFAULT_OUTPUT_DIR = Path("output")

_UNSAFE = re.compile(r"[^A-Za-z0-9._-]+")


def _safe_host(url: str) -> str:
    host = urlparse(url).netloc or "unknown-host"
    return _UNSAFE.sub("_", host)[:80] or "unknown-host"


def _digest(url: str) -> str:
    return hashlib.sha256(url.encode("utf-8")).hexdigest()[:12]


def _stamp(fetched_at: str) -> str:
    return _UNSAFE.sub("", fetched_at)


@dataclass(frozen=True)
class EvidencePaths:
    """Where one acquisition was written."""

    raw_html: Path
    raw_meta: Path
    normalized: Path | None = None


class EvidenceStore:
    """Writes raw and normalized artifacts under one output directory."""

    def __init__(self, output_dir: str | Path = DEFAULT_OUTPUT_DIR) -> None:
        self.output_dir = Path(output_dir)

    @property
    def raw_dir(self) -> Path:
        return self.output_dir / "raw"

    @property
    def normalized_dir(self) -> Path:
        return self.output_dir / "normalized"

    def _basename(self, response: RawResponse) -> str:
        return f"{_stamp(response.fetched_at)}-{_digest(response.url)}"

    def write_raw(
        self, response: RawResponse, *, collector: str, collector_version: str
    ) -> EvidencePaths:
        """Persist the response body plus enough metadata to trace it back."""
        host_dir = self.raw_dir / _safe_host(response.url)
        host_dir.mkdir(parents=True, exist_ok=True)
        base = self._basename(response)

        raw_html = host_dir / f"{base}.html"
        raw_html.write_text(response.body, encoding="utf-8")

        raw_meta = host_dir / f"{base}.meta.json"
        raw_meta.write_text(
            json.dumps(
                {
                    "source_url": response.url,
                    "final_url": response.final_url,
                    "fetched_at": response.fetched_at,
                    "http_status": response.status_code,
                    "content_type": response.content_type,
                    "content_chars": len(response.body),
                    "attempts": response.attempts,
                    "elapsed_s": round(response.elapsed_s, 3),
                    "collector": collector,
                    "collector_version": collector_version,
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )
        return EvidencePaths(raw_html=raw_html, raw_meta=raw_meta)

    def write_normalized(self, result: FetchResult, response: RawResponse) -> Path:
        host_dir = self.normalized_dir / _safe_host(response.url)
        host_dir.mkdir(parents=True, exist_ok=True)
        path = host_dir / f"{self._basename(response)}.json"
        path.write_text(
            json.dumps(result.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8"
        )
        return path
