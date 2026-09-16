"""Execution-safety tests for :class:`SubprocessRunner`.

These spawn a real child process, but only ``sys.executable`` running an inline
snippet, so they stay offline and deterministic.
"""

from __future__ import annotations

import sys

import pytest

from rita_agent_reach.errors import AgentReachError, ErrorCode
from rita_agent_reach.runner import SubprocessRunner


def py(code: str) -> list[str]:
    return [sys.executable, "-c", code]


def test_captures_stdout_and_exit_code():
    result = SubprocessRunner().run(py("print('hello')"), timeout=30)

    assert result.returncode == 0
    assert result.ok
    assert result.stdout.strip() == "hello"
    assert result.duration_s >= 0


def test_non_zero_exit_is_reported_not_raised():
    result = SubprocessRunner().run(
        py("import sys; sys.stderr.write('boom'); sys.exit(3)"), timeout=30
    )

    assert result.returncode == 3
    assert not result.ok
    assert "boom" in result.stderr


def test_missing_executable_raises_not_installed():
    with pytest.raises(AgentReachError) as excinfo:
        SubprocessRunner().run(["definitely-not-a-real-binary-xyz"], timeout=5)

    assert excinfo.value.code is ErrorCode.NOT_INSTALLED


def test_timeout_kills_the_child():
    with pytest.raises(AgentReachError) as excinfo:
        SubprocessRunner().run(py("import time; time.sleep(30)"), timeout=1.0)

    assert excinfo.value.code is ErrorCode.TIMEOUT


def test_string_argv_is_rejected():
    # A string argv is what turns into shell word-splitting; refuse it outright.
    with pytest.raises(AgentReachError) as excinfo:
        SubprocessRunner().run("echo hi && rm -rf .", timeout=5)  # type: ignore[arg-type]

    assert excinfo.value.code is ErrorCode.MALFORMED_OUTPUT


def test_non_string_argv_element_is_rejected():
    with pytest.raises(AgentReachError) as excinfo:
        SubprocessRunner().run([sys.executable, 42], timeout=5)  # type: ignore[list-item]

    assert excinfo.value.code is ErrorCode.MALFORMED_OUTPUT


def test_empty_argv_is_rejected():
    with pytest.raises(AgentReachError) as excinfo:
        SubprocessRunner().run([], timeout=5)

    assert excinfo.value.code is ErrorCode.MALFORMED_OUTPUT


def test_shell_metacharacters_are_passed_through_as_a_literal_argument():
    # Proof there is no shell: the argument arrives verbatim rather than being
    # interpreted as a command separator.
    payload = "; echo pwned"
    result = SubprocessRunner().run(py("import sys; print(sys.argv[1])") + [payload], timeout=30)

    assert result.stdout.strip() == payload


def test_undecodable_output_does_not_crash():
    result = SubprocessRunner().run(
        py("import sys; sys.stdout.buffer.write(b'\\xff\\xfe ok')"), timeout=30
    )

    assert result.ok
    assert "ok" in result.stdout


def test_child_is_pinned_to_utf8_output():
    # Regression guard: agent-reach doctor --json emits non-ASCII and dies with
    # UnicodeEncodeError when a Windows child falls back to the ANSI codepage.
    result = SubprocessRunner().run(
        py("import sys; print(sys.stdout.encoding); print('\\u4ed3')"), timeout=30
    )

    assert result.ok
    assert "utf-8" in result.stdout.lower()
    assert "仓" in result.stdout


def test_force_utf8_can_be_turned_off(monkeypatch):
    monkeypatch.delenv("PYTHONIOENCODING", raising=False)
    runner = SubprocessRunner(force_utf8=False)

    env = runner._child_env(None)

    assert "PYTHONIOENCODING" not in env


def test_explicit_env_wins_over_the_utf8_default():
    runner = SubprocessRunner()

    env = runner._child_env({"PYTHONIOENCODING": "latin-1"})

    assert env["PYTHONIOENCODING"] == "latin-1"


def test_extra_path_is_prepended_without_mutating_the_parent_env(monkeypatch):
    monkeypatch.setenv("PATH", "/original")
    runner = SubprocessRunner(extra_path=["/extra"])

    env = runner._child_env(None)

    assert env["PATH"].startswith("/extra")
    assert "/original" in env["PATH"]
    import os

    assert os.environ["PATH"] == "/original"
