"""Normalized result types.

Nothing Agent-Reach-shaped or gh-shaped or yt-dlp-shaped is allowed to escape
the adapter; callers only ever see the types in this module.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Mapping, Sequence

#: Version of this collector implementation, stamped onto every result.
#: Re-exported as ``rita_agent_reach.__version__``; it lives here so the
#: dataclass can reference it without importing the package root.
PACKAGE_VERSION = "0.1.0"


def utc_now_iso() -> str:
    """Timestamp used on every result, always UTC and always suffixed."""
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


@dataclass(frozen=True)
class CommandResult:
    """The raw outcome of one external command execution."""

    argv: tuple[str, ...]
    returncode: int
    stdout: str
    stderr: str
    duration_s: float

    @property
    def ok(self) -> bool:
        return self.returncode == 0


@dataclass(frozen=True)
class ChannelStatus:
    """One channel as reported by ``agent-reach doctor --json``.

    ``status`` is Agent Reach's own vocabulary: ok / warn / off / error.
    """

    name: str
    description: str
    status: str
    message: str
    tier: int
    backends: tuple[str, ...] = ()
    active_backend: str | None = None

    @property
    def available(self) -> bool:
        """Only ``ok`` counts as ready.

        ``warn`` means Agent Reach could not positively confirm the backend, so
        treating it as available would be guessing.
        """
        return self.status == "ok"


@dataclass(frozen=True)
class DoctorReport:
    """Parsed capability snapshot of the local machine."""

    channels: Mapping[str, ChannelStatus]
    raw: Mapping[str, Any] = field(default_factory=dict)

    def get(self, name: str) -> ChannelStatus | None:
        return self.channels.get(name)

    def available_channels(self) -> tuple[str, ...]:
        return tuple(sorted(n for n, c in self.channels.items() if c.available))

    def capabilities(self) -> dict[str, bool]:
        return {name: channel.available for name, channel in sorted(self.channels.items())}


@dataclass(frozen=True)
class FetchResult:
    """What the rest of the project is allowed to consume."""

    source_url: str
    channel: str
    backend: str
    fetched_at: str
    status: str
    title: str | None = None
    text: str | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)
    collector: str = "agent-reach"
    collector_version: str = PACKAGE_VERSION

    def to_dict(self) -> dict[str, Any]:
        return {
            "source_url": self.source_url,
            "channel": self.channel,
            "backend": self.backend,
            "fetched_at": self.fetched_at,
            "status": self.status,
            "title": self.title,
            "text": self.text,
            "metadata": dict(self.metadata),
            "collector": self.collector,
            "collector_version": self.collector_version,
        }


def as_str_tuple(values: Sequence[Any] | None) -> tuple[str, ...]:
    """Coerce a possibly-untrusted JSON list into a tuple of strings."""
    if not values:
        return ()
    return tuple(str(v) for v in values)
