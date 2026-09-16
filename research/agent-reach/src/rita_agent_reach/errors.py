"""Error taxonomy for the Agent Reach adapter.

Every failure path is classified. "Fetch failed" is never an acceptable answer:
the caller has to be able to tell a missing binary from a timeout from a site
that genuinely returned nothing.
"""

from __future__ import annotations

from enum import Enum
from typing import Sequence


class ErrorCode(str, Enum):
    """Why a call failed, in terms the caller can branch on."""

    NOT_INSTALLED = "NOT_INSTALLED"
    """The external executable is not on PATH."""

    TIMEOUT = "TIMEOUT"
    """The external command exceeded its wall-clock budget and was killed."""

    EXIT_ERROR = "EXIT_ERROR"
    """The external command ran and returned a non-zero exit code."""

    MALFORMED_OUTPUT = "MALFORMED_OUTPUT"
    """The command succeeded but its stdout was not the shape we expected."""

    EMPTY_OUTPUT = "EMPTY_OUTPUT"
    """The command succeeded and produced nothing usable."""

    UNSUPPORTED_SOURCE = "UNSUPPORTED_SOURCE"
    """No channel in this adapter knows how to reach that URL."""

    BACKEND_UNAVAILABLE = "BACKEND_UNAVAILABLE"
    """The channel exists but its backend is not usable on this machine."""

    NETWORK_ERROR = "NETWORK_ERROR"
    """DNS, connection or transport failure before any response was read."""

    HTTP_ERROR = "HTTP_ERROR"
    """A response arrived carrying a non-success HTTP status."""


class AgentReachError(RuntimeError):
    """A classified failure from the Agent Reach adapter.

    Carries the argv that produced it so the caller can log something
    actionable, with the caveat that ``stderr`` may contain third-party output.
    """

    def __init__(
        self,
        code: ErrorCode,
        message: str,
        *,
        argv: Sequence[str] | None = None,
        exit_code: int | None = None,
        stderr: str | None = None,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.argv: tuple[str, ...] | None = tuple(argv) if argv is not None else None
        self.exit_code = exit_code
        self.stderr = stderr

    def __str__(self) -> str:
        parts = [f"[{self.code.value}] {self.message}"]
        if self.exit_code is not None:
            parts.append(f"exit={self.exit_code}")
        if self.argv:
            parts.append(f"argv={list(self.argv)!r}")
        return " ".join(parts)
