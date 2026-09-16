"""Fetch happy paths and failure classification, all offline."""

from __future__ import annotations

import pytest

from conftest import (
    GH_REPO_JSON,
    GH_REPO_NULLS_JSON,
    JINA_BODY,
    YT_NO_CAPTIONS_JSON,
    YT_WITH_CAPTIONS_JSON,
    FakeHttp,
    FakeRunner,
    failed,
    ok,
)
from rita_agent_reach import __version__
from rita_agent_reach.adapter import AgentReachAdapter
from rita_agent_reach.errors import AgentReachError, ErrorCode


def test_github_fetch_normalizes_the_payload():
    runner = FakeRunner({"gh": ok(GH_REPO_JSON)})

    result = AgentReachAdapter(runner=runner).fetch("https://github.com/cli/cli")

    assert result.status == "success"
    assert result.channel == "github"
    assert result.backend == "gh CLI"
    assert result.collector == "agent-reach"
    assert result.collector_version == __version__
    assert result.source_url == "https://github.com/cli/cli"
    assert result.title == "cli/cli"
    assert "command line tool" in (result.text or "")
    assert result.metadata["stars"] == 46290
    assert result.metadata["language"] == "Go"
    assert result.metadata["license"] == "MIT License"
    assert result.metadata["license_key"] == "mit"
    assert result.metadata["open_issues"] == 1023
    assert result.metadata["default_branch"] == "trunk"
    assert result.metadata["topics"] == ["github-api-v4", "cli", "git"]
    assert result.fetched_at.endswith("+00:00")


def test_github_fetch_survives_null_nested_objects():
    # gh sends explicit nulls for license/language/branch on a bare repo.
    runner = FakeRunner({"gh": ok(GH_REPO_NULLS_JSON)})

    result = AgentReachAdapter(runner=runner).fetch("https://github.com/someone/bare")

    assert result.status == "success"
    assert result.metadata["license"] is None
    assert result.metadata["language"] is None
    assert result.metadata["default_branch"] is None
    assert result.metadata["topics"] == []
    assert result.text == ""


def test_github_fetch_surfaces_a_non_zero_exit():
    runner = FakeRunner({"gh": failed(1, "could not resolve to a Repository")})

    with pytest.raises(AgentReachError) as excinfo:
        AgentReachAdapter(runner=runner).fetch("https://github.com/cli/nope")

    assert excinfo.value.code is ErrorCode.EXIT_ERROR
    assert excinfo.value.exit_code == 1
    assert "Repository" in (excinfo.value.stderr or "")


def test_github_fetch_surfaces_malformed_output():
    runner = FakeRunner({"gh": ok("<html>login required</html>")})

    with pytest.raises(AgentReachError) as excinfo:
        AgentReachAdapter(runner=runner).fetch("https://github.com/cli/cli")

    assert excinfo.value.code is ErrorCode.MALFORMED_OUTPUT


def test_github_fetch_surfaces_empty_output():
    runner = FakeRunner({"gh": ok("")})

    with pytest.raises(AgentReachError) as excinfo:
        AgentReachAdapter(runner=runner).fetch("https://github.com/cli/cli")

    assert excinfo.value.code is ErrorCode.EMPTY_OUTPUT


def test_youtube_fetch_without_captions_still_succeeds():
    # The video has no transcript. That is a property of the video, and the
    # integration must report it as a fact rather than as a failure.
    runner = FakeRunner({"yt-dlp": ok(YT_NO_CAPTIONS_JSON)})

    result = AgentReachAdapter(runner=runner).fetch("https://www.youtube.com/watch?v=aqz-KE-bpKQ")

    assert result.status == "success"
    assert result.channel == "youtube"
    assert result.title.startswith("Big Buck Bunny")
    assert result.metadata["uploader"] == "Blender"
    assert result.metadata["duration_s"] == 635
    assert result.metadata["transcript_available"] is False
    assert result.metadata["subtitle_languages"] == []


def test_youtube_fetch_reports_available_caption_languages():
    runner = FakeRunner({"yt-dlp": ok(YT_WITH_CAPTIONS_JSON)})

    result = AgentReachAdapter(runner=runner).fetch("https://youtu.be/abc123")

    assert result.metadata["transcript_available"] is True
    assert result.metadata["subtitle_languages"] == ["en"]
    assert result.metadata["automatic_caption_languages"] == ["en", "es"]


def test_youtube_fetch_timeout_is_classified():
    runner = FakeRunner({"yt-dlp": AgentReachError(ErrorCode.TIMEOUT, "too slow")})

    with pytest.raises(AgentReachError) as excinfo:
        AgentReachAdapter(runner=runner).fetch("https://youtu.be/abc123")

    assert excinfo.value.code is ErrorCode.TIMEOUT


def test_youtube_fetch_missing_binary_is_classified():
    runner = FakeRunner({"yt-dlp": AgentReachError(ErrorCode.NOT_INSTALLED, "no yt-dlp")})

    with pytest.raises(AgentReachError) as excinfo:
        AgentReachAdapter(runner=runner).fetch("https://youtu.be/abc123")

    assert excinfo.value.code is ErrorCode.NOT_INSTALLED


def test_web_fetch_extracts_title_and_body():
    http = FakeHttp(200, JINA_BODY)

    result = AgentReachAdapter(runner=FakeRunner(), http_get=http).fetch("https://example.com")

    assert result.channel == "web"
    assert result.backend == "Jina Reader"
    assert result.title == "Example Domain"
    assert "documentation examples" in (result.text or "")
    assert "Markdown Content:" not in (result.text or "")
    assert http.urls == ["https://r.jina.ai/https://example.com"]
    assert result.metadata["http_status"] == 200
    assert result.metadata["content_chars"] > 0


def test_web_fetch_rejects_a_200_with_no_readable_content():
    # HTTP 200 is not evidence that the data is there.
    http = FakeHttp(200, "Title: Empty\n\nMarkdown Content:\n   \n")

    with pytest.raises(AgentReachError) as excinfo:
        AgentReachAdapter(runner=FakeRunner(), http_get=http).fetch("https://example.com")

    assert excinfo.value.code is ErrorCode.EMPTY_OUTPUT


def test_web_fetch_rejects_an_empty_body():
    http = FakeHttp(200, "")

    with pytest.raises(AgentReachError) as excinfo:
        AgentReachAdapter(runner=FakeRunner(), http_get=http).fetch("https://example.com")

    assert excinfo.value.code is ErrorCode.EMPTY_OUTPUT


def test_web_fetch_classifies_an_http_error_status():
    http = FakeHttp(503, "upstream unavailable")

    with pytest.raises(AgentReachError) as excinfo:
        AgentReachAdapter(runner=FakeRunner(), http_get=http).fetch("https://example.com")

    assert excinfo.value.code is ErrorCode.HTTP_ERROR
    assert excinfo.value.exit_code == 503


def test_web_fetch_classifies_a_network_error():
    http = FakeHttp(exc=AgentReachError(ErrorCode.NETWORK_ERROR, "dns failure"))

    with pytest.raises(AgentReachError) as excinfo:
        AgentReachAdapter(runner=FakeRunner(), http_get=http).fetch("https://example.com")

    assert excinfo.value.code is ErrorCode.NETWORK_ERROR


def test_fetch_rejects_an_unsupported_scheme():
    with pytest.raises(AgentReachError) as excinfo:
        AgentReachAdapter(runner=FakeRunner()).fetch("file:///etc/passwd")

    assert excinfo.value.code is ErrorCode.UNSUPPORTED_SOURCE


def test_result_round_trips_to_a_plain_dict():
    runner = FakeRunner({"gh": ok(GH_REPO_JSON)})

    payload = AgentReachAdapter(runner=runner).fetch("https://github.com/cli/cli").to_dict()

    assert set(payload) == {
        "source_url",
        "channel",
        "backend",
        "fetched_at",
        "status",
        "title",
        "text",
        "metadata",
        "collector",
        "collector_version",
    }
    assert isinstance(payload["metadata"], dict)
