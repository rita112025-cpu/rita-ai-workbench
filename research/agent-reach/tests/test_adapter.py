"""Availability, doctor parsing and failure classification."""

from __future__ import annotations

import pytest

from conftest import DOCTOR_JSON, FakeRunner, failed, ok
from rita_agent_reach.adapter import AgentReachAdapter, build_routing_index
from rita_agent_reach.errors import AgentReachError, ErrorCode


def adapter(runner: FakeRunner, **kwargs) -> AgentReachAdapter:
    return AgentReachAdapter(runner=runner, **kwargs)


def test_is_available_true_when_cli_answers():
    runner = FakeRunner({"agent-reach": ok("Agent Reach v1.5.0")})

    assert adapter(runner).is_available() is True
    assert runner.last_argv == ("agent-reach", "--version")


def test_version_returns_the_reported_string():
    runner = FakeRunner({"agent-reach": ok("Agent Reach v1.5.0\n")})

    assert adapter(runner).version() == "Agent Reach v1.5.0"


def test_is_available_false_when_binary_missing():
    missing = AgentReachError(ErrorCode.NOT_INSTALLED, "executable not found: agent-reach")
    runner = FakeRunner({"agent-reach": missing})

    assert adapter(runner).is_available() is False


def test_is_available_false_on_non_zero_exit():
    runner = FakeRunner({"agent-reach": failed(1, "broken")})

    assert adapter(runner).is_available() is False


def test_is_available_propagates_a_timeout_instead_of_lying():
    # A hung CLI is not the same as an absent one, so it must not be swallowed.
    runner = FakeRunner({"agent-reach": AgentReachError(ErrorCode.TIMEOUT, "too slow")})

    with pytest.raises(AgentReachError) as excinfo:
        adapter(runner).is_available()

    assert excinfo.value.code is ErrorCode.TIMEOUT


def test_doctor_parses_channels():
    runner = FakeRunner({"agent-reach": ok(DOCTOR_JSON)})

    report = adapter(runner).doctor()

    assert runner.last_argv == ("agent-reach", "doctor", "--json")
    assert set(report.channels) == {"github", "youtube", "web", "rss"}
    assert report.channels["web"].active_backend == "Jina Reader"
    assert report.channels["web"].backends == ("Jina Reader",)
    assert report.channels["youtube"].tier == 0


def test_doctor_only_counts_ok_as_available():
    runner = FakeRunner({"agent-reach": ok(DOCTOR_JSON)})

    report = adapter(runner).doctor()

    # "warn" means upstream could not confirm the backend; that is not a yes.
    assert report.channels["github"].status == "warn"
    assert report.channels["github"].available is False
    assert report.available_channels() == ("rss", "web")
    assert report.capabilities() == {
        "github": False,
        "rss": True,
        "web": True,
        "youtube": False,
    }


def test_doctor_uses_a_longer_timeout_than_a_fetch():
    runner = FakeRunner({"agent-reach": ok(DOCTOR_JSON)})

    adapter(runner, timeout=5.0, doctor_timeout=90.0).doctor()

    assert runner.calls[-1][1] == 90.0


def test_doctor_non_zero_exit_is_classified():
    runner = FakeRunner({"agent-reach": failed(2, "kaboom")})

    with pytest.raises(AgentReachError) as excinfo:
        adapter(runner).doctor()

    assert excinfo.value.code is ErrorCode.EXIT_ERROR
    assert excinfo.value.exit_code == 2


def test_doctor_malformed_json_is_classified():
    runner = FakeRunner({"agent-reach": ok("not json at all {{{")})

    with pytest.raises(AgentReachError) as excinfo:
        adapter(runner).doctor()

    assert excinfo.value.code is ErrorCode.MALFORMED_OUTPUT


def test_doctor_empty_output_is_classified():
    runner = FakeRunner({"agent-reach": ok("   \n  ")})

    with pytest.raises(AgentReachError) as excinfo:
        adapter(runner).doctor()

    assert excinfo.value.code is ErrorCode.EMPTY_OUTPUT


def test_doctor_json_of_the_wrong_shape_is_classified():
    runner = FakeRunner({"agent-reach": ok('["github", "web"]')})

    with pytest.raises(AgentReachError) as excinfo:
        adapter(runner).doctor()

    assert excinfo.value.code is ErrorCode.MALFORMED_OUTPUT


def test_doctor_channel_of_the_wrong_shape_is_classified():
    runner = FakeRunner({"agent-reach": ok('{"github": "ok"}')})

    with pytest.raises(AgentReachError) as excinfo:
        adapter(runner).doctor()

    assert excinfo.value.code is ErrorCode.MALFORMED_OUTPUT


def test_routing_index_exposes_backend_metadata():
    runner = FakeRunner({"agent-reach": ok(DOCTOR_JSON)})

    index = build_routing_index(adapter(runner).doctor())

    assert index["web"] == {
        "status": "ok",
        "available": True,
        "tier": 0,
        "backends": ["Jina Reader"],
        "active_backend": "Jina Reader",
    }


def test_error_string_includes_code_and_argv():
    error = AgentReachError(
        ErrorCode.EXIT_ERROR, "gh exited 1", argv=["gh", "repo", "view"], exit_code=1
    )

    rendered = str(error)

    assert "EXIT_ERROR" in rendered
    assert "exit=1" in rendered
    assert "gh" in rendered
