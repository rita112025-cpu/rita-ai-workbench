"""Agent Reach capability adapter for the Rita AI workbench.

Agent Reach is used here as a *capability layer only*: discovery, backend
availability, health check, routing metadata and controlled CLI execution.
It is not this project's only or general-purpose crawler.
"""

from __future__ import annotations

from .adapter import AgentReachAdapter, build_routing_index
from .errors import AgentReachError, ErrorCode
from .models import PACKAGE_VERSION, ChannelStatus, CommandResult, DoctorReport, FetchResult
from .routing import (
    CHANNEL_GITHUB,
    CHANNEL_WEB,
    CHANNEL_YOUTUBE,
    SUPPORTED_CHANNELS,
    classify,
)
from .runner import CommandRunner, SubprocessRunner

__version__ = PACKAGE_VERSION

__all__ = [
    "AgentReachAdapter",
    "AgentReachError",
    "CHANNEL_GITHUB",
    "CHANNEL_WEB",
    "CHANNEL_YOUTUBE",
    "ChannelStatus",
    "CommandResult",
    "CommandRunner",
    "DoctorReport",
    "ErrorCode",
    "FetchResult",
    "SUPPORTED_CHANNELS",
    "SubprocessRunner",
    "__version__",
    "build_routing_index",
    "classify",
]
