"""The adapter the rest of the project talks to.

Four entry points -- ``is_available``, ``doctor``, ``capabilities``, ``fetch``.
Nothing below this line leaks upward: callers never see argv, exit codes, gh
JSON or yt-dlp JSON, only :class:`~rita_agent_reach.models.FetchResult`.
"""

from __future__ import annotations

import json
from typing import Any, Mapping

from .errors import AgentReachError, ErrorCode
from .models import (
    ChannelStatus,
    DoctorReport,
    FetchResult,
    as_str_tuple,
    utc_now_iso,
)
from .routing import (
    CHANNEL_BACKENDS,
    CHANNEL_GITHUB,
    CHANNEL_WEB,
    CHANNEL_YOUTUBE,
    build_github_argv,
    build_web_url,
    build_youtube_argv,
    classify,
)
from .runner import DEFAULT_TIMEOUT_S, CommandRunner, SubprocessRunner
from .web_reader import HttpGetter, urllib_get

#: doctor probes several networked backends, so it needs more room than a fetch.
DOCTOR_TIMEOUT_S = 180.0


def _parse_json(stdout: str, *, argv: list[str], what: str) -> Any:
    if not stdout.strip():
        raise AgentReachError(
            ErrorCode.EMPTY_OUTPUT,
            f"{what} produced no output",
            argv=argv,
        )
    try:
        return json.loads(stdout)
    except json.JSONDecodeError as exc:
        raise AgentReachError(
            ErrorCode.MALFORMED_OUTPUT,
            f"{what} did not return valid JSON: {exc}",
            argv=argv,
        ) from exc


def _sub_dict(payload: Mapping[str, Any], key: str) -> Mapping[str, Any]:
    """Nested object from an external payload, or an empty mapping.

    Third-party JSON puts ``null`` where an object is documented, so every
    nested read goes through here rather than assuming a dict.
    """
    value = payload.get(key)
    return value if isinstance(value, dict) else {}


def _split_jina_markdown(body: str) -> tuple[str | None, str]:
    """Pull the ``Title:`` header off a Jina Reader response.

    The response is ``Key: value`` headers, a blank line, then
    ``Markdown Content:`` followed by the page body.
    """
    title: str | None = None
    marker = "Markdown Content:"
    header, _, content = body.partition(marker)
    for line in header.splitlines():
        if line.startswith("Title:"):
            title = line[len("Title:") :].strip() or None
            break
    return title, (content.strip() if content else body.strip())


class AgentReachAdapter:
    """Capability discovery and controlled execution against Agent Reach.

    Agent Reach itself owns installation, health checks and backend selection.
    This class reads that routing metadata and executes the routed upstream
    tool; it never installs anything, never writes Agent Reach config, and never
    touches cookies or browser profiles.
    """

    def __init__(
        self,
        *,
        runner: CommandRunner | None = None,
        http_get: HttpGetter | None = None,
        agent_reach_bin: str = "agent-reach",
        gh_bin: str = "gh",
        ytdlp_bin: str = "yt-dlp",
        timeout: float = DEFAULT_TIMEOUT_S,
        doctor_timeout: float = DOCTOR_TIMEOUT_S,
    ) -> None:
        self._runner: CommandRunner = runner or SubprocessRunner()
        self._http_get: HttpGetter = http_get or urllib_get
        self._agent_reach_bin = agent_reach_bin
        self._gh_bin = gh_bin
        self._ytdlp_bin = ytdlp_bin
        self._timeout = timeout
        self._doctor_timeout = doctor_timeout

    # -- capability discovery ------------------------------------------------

    def version(self) -> str | None:
        """Agent Reach's reported version, or None when the CLI is absent."""
        argv = [self._agent_reach_bin, "--version"]
        try:
            result = self._runner.run(argv, timeout=self._timeout)
        except AgentReachError as exc:
            if exc.code is ErrorCode.NOT_INSTALLED:
                return None
            raise
        if not result.ok:
            return None
        text = (result.stdout or result.stderr).strip()
        return text or None

    def is_available(self) -> bool:
        """True when the Agent Reach CLI can be executed at all.

        Deliberately narrow: this answers "is the capability layer installed",
        not "can we reach any given platform". Use :meth:`capabilities` for that.
        """
        return self.version() is not None

    def doctor(self) -> DoctorReport:
        """Run ``agent-reach doctor --json`` and parse it.

        ``doctor`` is read-only by design -- upstream constructs its config with
        ``read_only=True`` and writes nothing.
        """
        argv = [self._agent_reach_bin, "doctor", "--json"]
        result = self._runner.run(argv, timeout=self._doctor_timeout)
        if not result.ok:
            raise AgentReachError(
                ErrorCode.EXIT_ERROR,
                "agent-reach doctor failed",
                argv=argv,
                exit_code=result.returncode,
                stderr=result.stderr,
            )
        payload = _parse_json(result.stdout, argv=argv, what="agent-reach doctor")
        if not isinstance(payload, dict):
            raise AgentReachError(
                ErrorCode.MALFORMED_OUTPUT,
                f"agent-reach doctor returned {type(payload).__name__}, expected an object",
                argv=argv,
            )
        channels: dict[str, ChannelStatus] = {}
        for name, entry in payload.items():
            if not isinstance(entry, dict):
                raise AgentReachError(
                    ErrorCode.MALFORMED_OUTPUT,
                    f"agent-reach doctor channel {name!r} is not an object",
                    argv=argv,
                )
            channels[str(name)] = ChannelStatus(
                name=str(name),
                description=str(entry.get("name") or name),
                status=str(entry.get("status") or "error"),
                message=str(entry.get("message") or ""),
                tier=int(entry.get("tier") or 0),
                backends=as_str_tuple(entry.get("backends")),
                active_backend=(
                    str(entry["active_backend"]) if entry.get("active_backend") else None
                ),
            )
        return DoctorReport(channels=channels, raw=payload)

    def capabilities(self) -> dict[str, bool]:
        """Channel name -> whether it is usable right now on this machine."""
        return self.doctor().capabilities()

    # -- controlled execution ------------------------------------------------

    def fetch(self, url: str) -> FetchResult:
        """Acquire public content for ``url`` through its routed backend.

        Raises :class:`AgentReachError` with a specific
        :class:`~rita_agent_reach.errors.ErrorCode` on every failure path.
        """
        channel = classify(url)
        if channel == CHANNEL_GITHUB:
            return self._fetch_github(url)
        if channel == CHANNEL_YOUTUBE:
            return self._fetch_youtube(url)
        return self._fetch_web(url)

    def _run_checked(self, argv: list[str], *, what: str) -> str:
        result = self._runner.run(argv, timeout=self._timeout)
        if not result.ok:
            raise AgentReachError(
                ErrorCode.EXIT_ERROR,
                f"{what} exited {result.returncode}",
                argv=argv,
                exit_code=result.returncode,
                stderr=result.stderr.strip()[:2000],
            )
        return result.stdout

    def _result(self, **kwargs: Any) -> FetchResult:
        return FetchResult(fetched_at=utc_now_iso(), status="success", **kwargs)

    def _fetch_github(self, url: str) -> FetchResult:
        argv = build_github_argv(url, gh_bin=self._gh_bin)
        payload = _parse_json(
            self._run_checked(argv, what="gh repo view"), argv=argv, what="gh repo view"
        )
        if not isinstance(payload, dict):
            raise AgentReachError(
                ErrorCode.MALFORMED_OUTPUT, "gh repo view did not return an object", argv=argv
            )
        # Shapes below match real gh 2.88.1 output: repositoryTopics entries are
        # {"name": ...}, licenseInfo carries key/name (no spdxId), and the issue
        # count is nested under issues.totalCount.
        language = _sub_dict(payload, "primaryLanguage")
        licence = _sub_dict(payload, "licenseInfo")
        issues = _sub_dict(payload, "issues")
        branch = _sub_dict(payload, "defaultBranchRef")
        topics = [
            t.get("name")
            for t in payload.get("repositoryTopics") or []
            if isinstance(t, dict) and t.get("name")
        ]
        return self._result(
            source_url=url,
            channel=CHANNEL_GITHUB,
            backend=CHANNEL_BACKENDS[CHANNEL_GITHUB],
            title=payload.get("nameWithOwner"),
            text=payload.get("description") or "",
            metadata={
                "full_name": payload.get("nameWithOwner"),
                "html_url": payload.get("url"),
                "homepage": payload.get("homepageUrl"),
                "stars": payload.get("stargazerCount"),
                "forks": payload.get("forkCount"),
                "open_issues": issues.get("totalCount"),
                "default_branch": branch.get("name"),
                "language": language.get("name"),
                "license": licence.get("name"),
                "license_key": licence.get("key"),
                "archived": payload.get("isArchived"),
                "private": payload.get("isPrivate"),
                "pushed_at": payload.get("pushedAt"),
                "updated_at": payload.get("updatedAt"),
                "topics": topics,
            },
        )

    def _fetch_youtube(self, url: str) -> FetchResult:
        argv = build_youtube_argv(url, ytdlp_bin=self._ytdlp_bin)
        payload = _parse_json(self._run_checked(argv, what="yt-dlp"), argv=argv, what="yt-dlp")
        if not isinstance(payload, dict):
            raise AgentReachError(
                ErrorCode.MALFORMED_OUTPUT, "yt-dlp did not return an object", argv=argv
            )
        subtitle_langs = sorted((payload.get("subtitles") or {}).keys())
        auto_caption_langs = sorted((payload.get("automatic_captions") or {}).keys())
        # A video with no captions is a fact about the video, not a broken
        # integration, so metadata alone still counts as a successful fetch.
        return self._result(
            source_url=url,
            channel=CHANNEL_YOUTUBE,
            backend=CHANNEL_BACKENDS[CHANNEL_YOUTUBE],
            title=payload.get("title"),
            text=payload.get("description") or "",
            metadata={
                "video_id": payload.get("id"),
                "uploader": payload.get("uploader"),
                "channel": payload.get("channel"),
                "channel_url": payload.get("channel_url"),
                "duration_s": payload.get("duration"),
                "upload_date": payload.get("upload_date"),
                "view_count": payload.get("view_count"),
                "webpage_url": payload.get("webpage_url"),
                "subtitle_languages": subtitle_langs,
                "automatic_caption_languages": auto_caption_langs,
                "transcript_available": bool(subtitle_langs or auto_caption_langs),
            },
        )

    def _fetch_web(self, url: str) -> FetchResult:
        reader_url = build_web_url(url)
        status_code, body = self._http_get(reader_url, timeout=self._timeout)
        if status_code >= 400:
            raise AgentReachError(
                ErrorCode.HTTP_ERROR,
                f"HTTP {status_code} from Jina Reader",
                exit_code=status_code,
            )
        if not body.strip():
            raise AgentReachError(ErrorCode.EMPTY_OUTPUT, f"Jina Reader returned nothing for {url}")
        title, text = _split_jina_markdown(body)
        if not text.strip():
            # HTTP 200 with a shell of a page is not a successful acquisition.
            raise AgentReachError(
                ErrorCode.EMPTY_OUTPUT, f"Jina Reader returned no readable content for {url}"
            )
        return self._result(
            source_url=url,
            channel=CHANNEL_WEB,
            backend=CHANNEL_BACKENDS[CHANNEL_WEB],
            title=title,
            text=text,
            metadata={
                "reader_url": reader_url,
                "http_status": status_code,
                "content_chars": len(text),
            },
        )


def build_routing_index(report: DoctorReport) -> Mapping[str, Mapping[str, Any]]:
    """Routing metadata per channel: status, tier and the active backend."""
    return {
        name: {
            "status": channel.status,
            "available": channel.available,
            "tier": channel.tier,
            "backends": list(channel.backends),
            "active_backend": channel.active_backend,
        }
        for name, channel in sorted(report.channels.items())
    }
