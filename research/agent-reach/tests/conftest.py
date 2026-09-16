"""Shared offline fixtures.

Every unit test runs against a fake runner and a fake HTTP getter, so the suite
needs no network, no agent-reach install and no gh login.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Mapping, Sequence

import pytest

SRC = Path(__file__).resolve().parents[1] / "src"
if str(SRC) not in sys.path:  # pragma: no cover - import bootstrap
    sys.path.insert(0, str(SRC))

from rita_agent_reach.errors import AgentReachError  # noqa: E402
from rita_agent_reach.models import CommandResult  # noqa: E402


class FakeRunner:
    """Replays canned results (or raises) keyed by the first argv element."""

    def __init__(
        self,
        responses: Mapping[str, CommandResult | BaseException] | None = None,
        *,
        default: CommandResult | BaseException | None = None,
    ) -> None:
        self._responses = dict(responses or {})
        self._default = default
        self.calls: list[tuple[tuple[str, ...], float]] = []

    def run(
        self,
        argv: Sequence[str],
        *,
        timeout: float = 60.0,
        env: Mapping[str, str] | None = None,
    ) -> CommandResult:
        items = tuple(argv)
        self.calls.append((items, timeout))
        response = self._responses.get(items[0], self._default)
        if response is None:
            raise AssertionError(f"FakeRunner has no response for {items[0]!r}")
        if isinstance(response, BaseException):
            raise response
        return response

    @property
    def last_argv(self) -> tuple[str, ...]:
        return self.calls[-1][0]


def ok(stdout: str, *, argv: Sequence[str] = ("fake",)) -> CommandResult:
    return CommandResult(argv=tuple(argv), returncode=0, stdout=stdout, stderr="", duration_s=0.01)


def failed(returncode: int, stderr: str, *, argv: Sequence[str] = ("fake",)) -> CommandResult:
    return CommandResult(
        argv=tuple(argv), returncode=returncode, stdout="", stderr=stderr, duration_s=0.01
    )


class FakeHttp:
    """Stand-in for :func:`rita_agent_reach.web_reader.urllib_get`."""

    def __init__(self, status: int = 200, body: str = "", exc: AgentReachError | None = None):
        self.status = status
        self.body = body
        self.exc = exc
        self.urls: list[str] = []

    def __call__(self, url: str, *, timeout: float) -> tuple[int, str]:
        self.urls.append(url)
        if self.exc is not None:
            raise self.exc
        return self.status, self.body


#: Trimmed from a real ``agent-reach doctor --json`` run (v1.5.0, Windows).
DOCTOR_JSON = """
{
  "github": {
    "status": "warn",
    "name": "GitHub repos and code",
    "message": "gh CLI executable, explicit auth config detected",
    "tier": 0,
    "backends": ["gh CLI"],
    "active_backend": null
  },
  "youtube": {
    "status": "off",
    "name": "YouTube subtitles",
    "message": "yt-dlp not installed",
    "tier": 0,
    "backends": ["yt-dlp"],
    "active_backend": null
  },
  "web": {
    "status": "ok",
    "name": "Web pages (any URL)",
    "message": "reads any page through Jina Reader",
    "tier": 0,
    "backends": ["Jina Reader"],
    "active_backend": "Jina Reader"
  },
  "rss": {
    "status": "ok",
    "name": "RSS/Atom feeds",
    "message": "feeds readable",
    "tier": 0,
    "backends": ["feedparser"],
    "active_backend": "feedparser"
  }
}
"""

#: Copied from a real ``gh repo view cli/cli --json ...`` response (gh 2.88.1).
#: Note the shapes: repositoryTopics entries are flat {"name": ...}, licenseInfo
#: has key/name and no spdxId, and the issue count is nested under issues.
GH_REPO_JSON = """
{
  "defaultBranchRef": {"name": "trunk"},
  "description": "GitHub's official command line tool",
  "forkCount": 9031,
  "homepageUrl": "https://cli.github.com",
  "isArchived": false,
  "isPrivate": false,
  "issues": {"totalCount": 1023},
  "licenseInfo": {"key": "mit", "name": "MIT License", "nickname": ""},
  "nameWithOwner": "cli/cli",
  "primaryLanguage": {"name": "Go"},
  "pushedAt": "2026-09-15T14:24:34Z",
  "repositoryTopics": [{"name": "github-api-v4"}, {"name": "cli"}, {"name": "git"}],
  "stargazerCount": 46290,
  "updatedAt": "2026-09-15T23:41:57Z",
  "url": "https://github.com/cli/cli"
}
"""

#: Same call against a repo with no license, no language and no topics: gh sends
#: explicit nulls where an object is documented.
GH_REPO_NULLS_JSON = """
{
  "defaultBranchRef": null,
  "description": null,
  "forkCount": 0,
  "homepageUrl": "",
  "isArchived": false,
  "isPrivate": false,
  "issues": {"totalCount": 0},
  "licenseInfo": null,
  "nameWithOwner": "someone/bare",
  "primaryLanguage": null,
  "pushedAt": "2026-01-01T00:00:00Z",
  "repositoryTopics": [],
  "stargazerCount": 0,
  "updatedAt": "2026-01-01T00:00:00Z",
  "url": "https://github.com/someone/bare"
}
"""

#: Trimmed from a real ``yt-dlp --dump-single-json`` response (no captions).
YT_NO_CAPTIONS_JSON = """
{
  "id": "aqz-KE-bpKQ",
  "title": "Big Buck Bunny 60fps 4K - Official Blender Foundation Short Film",
  "description": "Big Buck Bunny 60fps 4K",
  "uploader": "Blender",
  "channel": "Blender",
  "duration": 635,
  "subtitles": {},
  "automatic_captions": {}
}
"""

#: Same shape, but with captions present.
YT_WITH_CAPTIONS_JSON = """
{
  "id": "abc123",
  "title": "A talk",
  "description": "Slides and notes",
  "uploader": "Someone",
  "duration": 100,
  "subtitles": {"en": [{"ext": "vtt"}]},
  "automatic_captions": {"en": [{"ext": "vtt"}], "es": [{"ext": "vtt"}]}
}
"""

JINA_BODY = """Title: Example Domain

URL Source: https://example.com/

Markdown Content:
This domain is for use in documentation examples without needing permission.

[Learn more](https://iana.org/domains/example)
"""


@pytest.fixture
def doctor_json() -> str:
    return DOCTOR_JSON
