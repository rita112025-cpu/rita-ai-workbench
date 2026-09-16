"""URL classification and command construction."""

from __future__ import annotations

import pytest

from rita_agent_reach.errors import AgentReachError, ErrorCode
from rita_agent_reach.routing import (
    CHANNEL_GITHUB,
    CHANNEL_WEB,
    CHANNEL_YOUTUBE,
    build_github_argv,
    build_web_url,
    build_youtube_argv,
    classify,
    github_repo_slug,
)


@pytest.mark.parametrize(
    ("url", "expected"),
    [
        ("https://github.com/cli/cli", CHANNEL_GITHUB),
        ("https://github.com/cli/cli/issues/42", CHANNEL_GITHUB),
        ("https://github.com/cli/cli.git", CHANNEL_GITHUB),
        # Not a repository page, so it falls back to the generic reader.
        ("https://github.com/explore", CHANNEL_WEB),
        ("https://github.com/orgs/cli/people", CHANNEL_WEB),
        ("https://www.youtube.com/watch?v=aqz-KE-bpKQ", CHANNEL_YOUTUBE),
        ("https://youtu.be/aqz-KE-bpKQ", CHANNEL_YOUTUBE),
        ("https://example.com/page", CHANNEL_WEB),
    ],
)
def test_classify(url, expected):
    assert classify(url) == expected


@pytest.mark.parametrize("url", ["ftp://example.com", "not-a-url", "", "file:///etc/passwd"])
def test_classify_rejects_non_http(url):
    with pytest.raises(AgentReachError) as excinfo:
        classify(url)

    assert excinfo.value.code is ErrorCode.UNSUPPORTED_SOURCE


@pytest.mark.parametrize(
    ("url", "expected"),
    [
        ("https://github.com/cli/cli", "cli/cli"),
        ("https://github.com/cli/cli/tree/trunk/pkg", "cli/cli"),
        ("https://github.com/cli/cli.git", "cli/cli"),
        ("https://github.com/cli", None),
        ("https://github.com/settings/profile", None),
        ("https://example.com/cli/cli", None),
    ],
)
def test_github_repo_slug(url, expected):
    assert github_repo_slug(url) == expected


def test_github_argv_is_a_list_with_the_slug_as_one_argument():
    argv = build_github_argv("https://github.com/cli/cli")

    assert argv[:4] == ["gh", "repo", "view", "cli/cli"]
    assert "--json" in argv
    assert all(isinstance(part, str) for part in argv)


def test_github_argv_honours_a_custom_binary():
    argv = build_github_argv("https://github.com/cli/cli", gh_bin="/opt/bin/gh")

    assert argv[0] == "/opt/bin/gh"


def test_github_argv_rejects_non_repository_urls():
    with pytest.raises(AgentReachError) as excinfo:
        build_github_argv("https://github.com/explore")

    assert excinfo.value.code is ErrorCode.UNSUPPORTED_SOURCE


def test_youtube_argv_never_downloads_and_terminates_option_parsing():
    url = "https://www.youtube.com/watch?v=aqz-KE-bpKQ"
    argv = build_youtube_argv(url)

    assert argv[0] == "yt-dlp"
    assert "--skip-download" in argv
    assert "--dump-single-json" in argv
    # "--" guards against a URL that starts with a dash being read as a flag.
    assert argv[-2:] == ["--", url]


def test_web_url_is_the_reader_prefix_plus_the_target():
    assert build_web_url("https://example.com") == "https://r.jina.ai/https://example.com"


def test_web_url_rejects_non_http():
    with pytest.raises(AgentReachError):
        build_web_url("javascript:alert(1)")
