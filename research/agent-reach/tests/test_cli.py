"""CLI boundary: argument parsing, JSON output and the error exit path."""

from __future__ import annotations

import json

import pytest

from rita_agent_reach import __version__
from rita_agent_reach.cli import main


def test_version_flag_exits_zero(capsys):
    with pytest.raises(SystemExit) as excinfo:
        main(["--version"])

    assert excinfo.value.code == 0
    assert __version__ in capsys.readouterr().out


def test_unsupported_url_exits_one_with_a_classified_error(capsys):
    # Rejected during classification, so this needs no network and no binaries.
    exit_code = main(["fetch", "file:///etc/passwd"])

    captured = capsys.readouterr()
    assert exit_code == 1
    payload = json.loads(captured.err)
    assert payload["status"] == "error"
    assert payload["code"] == "UNSUPPORTED_SOURCE"
    assert captured.out == ""


def test_missing_agent_reach_binary_reports_unavailable(capsys):
    exit_code = main(["--agent-reach-bin", "definitely-not-a-real-binary-xyz", "available"])

    payload = json.loads(capsys.readouterr().out)
    assert exit_code == 1
    assert payload == {"available": False, "version": None}


def test_a_command_is_required(capsys):
    with pytest.raises(SystemExit) as excinfo:
        main([])

    assert excinfo.value.code != 0
