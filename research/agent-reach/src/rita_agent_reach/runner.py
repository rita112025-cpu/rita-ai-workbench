"""Controlled execution of external commands.

Rules enforced here, once, so no caller has to remember them:

* argv is always a list, never a string, and ``shell`` is never enabled;
* every call carries a wall-clock timeout and the child is killed if it blows it;
* stdout/stderr are decoded as UTF-8 with replacement, because third-party CLIs
  emit whatever their locale feels like and a UnicodeDecodeError here would be
  indistinguishable from a real failure;
* the child never inherits a mutated parent environment.
"""

from __future__ import annotations

import os
import subprocess
import time
from typing import Mapping, Protocol, Sequence

from .errors import AgentReachError, ErrorCode
from .models import CommandResult

DEFAULT_TIMEOUT_S = 60.0


class CommandRunner(Protocol):
    """Seam that lets every test run offline."""

    def run(
        self,
        argv: Sequence[str],
        *,
        timeout: float = DEFAULT_TIMEOUT_S,
        env: Mapping[str, str] | None = None,
    ) -> CommandResult: ...


def _validate_argv(argv: Sequence[str]) -> list[str]:
    """Reject anything that is not a plain list of strings.

    A string argv would be split by the shell; a non-string element would be
    coerced silently. Both are how user input turns into command injection, so
    they fail loudly instead.
    """
    if isinstance(argv, (str, bytes)):
        raise AgentReachError(
            ErrorCode.MALFORMED_OUTPUT,
            "argv must be a sequence of strings, not a single string",
        )
    items = list(argv)
    if not items:
        raise AgentReachError(ErrorCode.MALFORMED_OUTPUT, "argv must not be empty")
    for item in items:
        if not isinstance(item, str):
            raise AgentReachError(
                ErrorCode.MALFORMED_OUTPUT,
                f"argv elements must be strings, got {type(item).__name__}",
            )
    return items


class SubprocessRunner:
    """The real runner. Everything else in the package talks to the protocol."""

    def __init__(self, *, extra_path: Sequence[str] = (), force_utf8: bool = True) -> None:
        # Agent Reach routes to CLIs that often live in a virtualenv's Scripts/bin
        # directory rather than on the ambient PATH; this lets a caller add those
        # without mutating the parent process environment.
        self._extra_path = tuple(extra_path)
        self._force_utf8 = force_utf8

    def _child_env(self, env: Mapping[str, str] | None) -> dict[str, str]:
        child = dict(os.environ)
        if self._force_utf8:
            # Verified failure, not a precaution: on Windows a Python child whose
            # stdout is a pipe falls back to the ANSI codepage, and
            # `agent-reach doctor --json` then dies with
            # UnicodeEncodeError: 'cp950' codec ... and exits 1. Whether it
            # triggers depends on the inherited environment, which makes it an
            # intermittent failure unless we pin the child to UTF-8. Applied
            # before the caller's overrides so an explicit env still wins.
            child["PYTHONIOENCODING"] = "utf-8"
            child["PYTHONUTF8"] = "1"
        if env:
            child.update(env)
        if self._extra_path:
            existing = child.get("PATH", "")
            child["PATH"] = (
                os.pathsep.join([*self._extra_path, existing])
                if existing
                else (os.pathsep.join(self._extra_path))
            )
        return child

    def run(
        self,
        argv: Sequence[str],
        *,
        timeout: float = DEFAULT_TIMEOUT_S,
        env: Mapping[str, str] | None = None,
    ) -> CommandResult:
        items = _validate_argv(argv)
        started = time.monotonic()
        try:
            proc = subprocess.Popen(  # noqa: S603 - argv list, shell disabled by construction
                items,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.DEVNULL,
                shell=False,
                text=True,
                encoding="utf-8",
                errors="replace",
                env=self._child_env(env),
            )
        except FileNotFoundError as exc:
            raise AgentReachError(
                ErrorCode.NOT_INSTALLED,
                f"executable not found: {items[0]}",
                argv=items,
            ) from exc
        except OSError as exc:
            raise AgentReachError(
                ErrorCode.EXIT_ERROR,
                f"could not start {items[0]}: {exc}",
                argv=items,
            ) from exc

        try:
            stdout, stderr = proc.communicate(timeout=timeout)
        except subprocess.TimeoutExpired as exc:
            # Kill, then drain, so the child never survives us as an orphan.
            proc.kill()
            proc.communicate()
            raise AgentReachError(
                ErrorCode.TIMEOUT,
                f"{items[0]} exceeded {timeout:g}s and was terminated",
                argv=items,
            ) from exc
        except BaseException:
            # Covers KeyboardInterrupt/cancellation: still no orphaned child.
            proc.kill()
            proc.communicate()
            raise

        return CommandResult(
            argv=tuple(items),
            returncode=proc.returncode,
            stdout=stdout or "",
            stderr=stderr or "",
            duration_s=time.monotonic() - started,
        )
