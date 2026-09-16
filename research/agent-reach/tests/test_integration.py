"""Opt-in tests that hit real CLIs and real public sites.

Deselected by default (``addopts = -m 'not integration'``) so CI never goes red
because a third-party site had a bad afternoon. Run them deliberately:

    pytest -m integration

Each test skips rather than fails when its backend is absent, because "the tool
is not installed here" is not a defect in this adapter. Override binary
locations with RITA_AGENT_REACH_BIN / RITA_GH_BIN / RITA_YTDLP_BIN when they
live in a virtualenv rather than on PATH.
"""

from __future__ import annotations

import os
import shutil

import pytest

from rita_agent_reach.adapter import AgentReachAdapter

pytestmark = pytest.mark.integration

AGENT_REACH_BIN = os.environ.get("RITA_AGENT_REACH_BIN", "agent-reach")
GH_BIN = os.environ.get("RITA_GH_BIN", "gh")
YTDLP_BIN = os.environ.get("RITA_YTDLP_BIN", "yt-dlp")

# Public, no login, no CAPTCHA, stable.
GITHUB_URL = "https://github.com/cli/cli"
YOUTUBE_URL = "https://www.youtube.com/watch?v=aqz-KE-bpKQ"
WEB_URL = "https://example.com"


def _require(binary: str) -> None:
    if shutil.which(binary) is None and not os.path.exists(binary):
        pytest.skip(f"{binary} is not available on this machine")


def _adapter(**kwargs) -> AgentReachAdapter:
    return AgentReachAdapter(
        agent_reach_bin=AGENT_REACH_BIN, gh_bin=GH_BIN, ytdlp_bin=YTDLP_BIN, **kwargs
    )


def test_agent_reach_cli_is_available():
    _require(AGENT_REACH_BIN)

    version = _adapter().version()

    assert version is not None
    assert "Agent Reach" in version


def test_doctor_returns_real_channels():
    _require(AGENT_REACH_BIN)

    report = _adapter().doctor()

    # Upstream ships a fixed channel registry; a report with none of these in it
    # means the output shape changed, not that the machine is unhealthy.
    assert {"github", "youtube", "web", "rss"} <= set(report.channels)
    for channel in report.channels.values():
        assert channel.status in {"ok", "warn", "off", "error"}


def test_github_public_repo_returns_real_data():
    _require(GH_BIN)

    result = _adapter().fetch(GITHUB_URL)

    assert result.status == "success"
    assert result.channel == "github"
    assert result.title == "cli/cli"
    assert result.metadata["html_url"] == GITHUB_URL
    assert result.metadata["private"] is False
    assert isinstance(result.metadata["stars"], int)
    assert result.metadata["stars"] > 1000


def test_youtube_public_video_returns_real_metadata():
    _require(YTDLP_BIN)

    result = _adapter(timeout=120).fetch(YOUTUBE_URL)

    assert result.status == "success"
    assert result.channel == "youtube"
    assert result.metadata["video_id"] == "aqz-KE-bpKQ"
    assert "Big Buck Bunny" in (result.title or "")
    assert result.metadata["duration_s"] > 0
    # transcript_available may legitimately be False for this video; the point
    # is that it is reported, not that it is True.
    assert isinstance(result.metadata["transcript_available"], bool)


def test_public_web_page_returns_readable_content():
    result = _adapter(timeout=90).fetch(WEB_URL)

    assert result.status == "success"
    assert result.channel == "web"
    assert result.source_url == WEB_URL
    assert result.title == "Example Domain"
    # Assert on actual expected words, not merely on a non-empty string.
    assert "documentation examples" in (result.text or "")
