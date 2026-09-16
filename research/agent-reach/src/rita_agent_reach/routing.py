"""URL -> Agent Reach channel -> concrete backend argv.

Agent Reach is explicitly a *capability layer*: it selects, installs and
health-checks the access path for each platform, and the calling agent invokes
the upstream tool itself (see its README, "Design Philosophy"). There is no
``agent-reach fetch`` subcommand. This module is therefore where the routing
metadata that ``doctor`` reports gets turned into an actual argv.

Only the three zero-config, no-login channels this project has verified are
routed here. Anything needing a cookie, a login or a browser session is
deliberately absent.
"""

from __future__ import annotations

import re
from urllib.parse import urlparse

from .errors import AgentReachError, ErrorCode

CHANNEL_GITHUB = "github"
CHANNEL_YOUTUBE = "youtube"
CHANNEL_WEB = "web"

SUPPORTED_CHANNELS = (CHANNEL_GITHUB, CHANNEL_YOUTUBE, CHANNEL_WEB)

#: Backend each channel is routed to, matching what ``agent-reach doctor`` reports.
CHANNEL_BACKENDS = {
    CHANNEL_GITHUB: "gh CLI",
    CHANNEL_YOUTUBE: "yt-dlp",
    CHANNEL_WEB: "Jina Reader",
}

JINA_READER_BASE = "https://r.jina.ai/"

_YOUTUBE_HOSTS = {
    "youtube.com",
    "www.youtube.com",
    "m.youtube.com",
    "music.youtube.com",
    "youtu.be",
}

_GITHUB_HOSTS = {"github.com", "www.github.com"}

# owner/repo, rejecting the reserved first path segments that are not repos.
_REPO_SLUG_RE = re.compile(r"^[A-Za-z0-9][\w.-]*/[A-Za-z0-9][\w.-]*$")
_GITHUB_NON_REPO_ROOTS = {
    "orgs",
    "settings",
    "notifications",
    "explore",
    "topics",
    "sponsors",
    "marketplace",
    "features",
    "pricing",
    "search",
    "login",
    "collections",
}


def _require_http_url(url: str) -> str:
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        raise AgentReachError(
            ErrorCode.UNSUPPORTED_SOURCE,
            f"not an http(s) URL: {url!r}",
        )
    return parsed.netloc.lower()


def github_repo_slug(url: str) -> str | None:
    """Return ``owner/repo`` for a repository URL, or None if it is not one."""
    parsed = urlparse(url)
    if parsed.netloc.lower() not in _GITHUB_HOSTS:
        return None
    parts = [p for p in parsed.path.split("/") if p]
    if len(parts) < 2:
        return None
    owner, repo = parts[0], parts[1]
    if owner.lower() in _GITHUB_NON_REPO_ROOTS:
        return None
    repo = repo[:-4] if repo.endswith(".git") else repo
    slug = f"{owner}/{repo}"
    return slug if _REPO_SLUG_RE.match(slug) else None


def classify(url: str) -> str:
    """Pick the channel for a URL.

    Falls back to the generic web reader rather than refusing, because "we have
    no dedicated channel" is not the same as "this page is unreachable".
    """
    host = _require_http_url(url)
    if host in _YOUTUBE_HOSTS:
        return CHANNEL_YOUTUBE
    if host in _GITHUB_HOSTS and github_repo_slug(url):
        return CHANNEL_GITHUB
    return CHANNEL_WEB


#: gh fields requested for a repository. Public data only.
#: Verified against ``gh repo view --json`` on gh 2.88.1. The accepted names are
#: not guessable -- there is no ``openIssues`` field, the count lives under
#: ``issues.totalCount`` -- so only change this against that list.
GH_REPO_FIELDS = (
    "nameWithOwner,description,url,homepageUrl,stargazerCount,forkCount,"
    "primaryLanguage,licenseInfo,isArchived,isPrivate,pushedAt,updatedAt,"
    "repositoryTopics,issues,defaultBranchRef"
)


def build_github_argv(url: str, *, gh_bin: str = "gh") -> list[str]:
    slug = github_repo_slug(url)
    if slug is None:
        raise AgentReachError(
            ErrorCode.UNSUPPORTED_SOURCE,
            f"not a GitHub repository URL: {url!r}",
        )
    return [gh_bin, "repo", "view", slug, "--json", GH_REPO_FIELDS]


def build_youtube_argv(url: str, *, ytdlp_bin: str = "yt-dlp") -> list[str]:
    _require_http_url(url)
    return [
        ytdlp_bin,
        "--skip-download",
        "--dump-single-json",
        "--no-warnings",
        "--no-playlist",
        "--",
        url,
    ]


def build_web_url(url: str) -> str:
    """Jina Reader takes the target URL appended to its own base."""
    _require_http_url(url)
    return f"{JINA_READER_BASE}{url}"
