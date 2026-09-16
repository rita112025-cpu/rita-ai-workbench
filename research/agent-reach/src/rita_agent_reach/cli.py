"""Small CLI over the adapter, mainly so the integration can be exercised by hand.

python -m rita_agent_reach doctor
python -m rita_agent_reach capabilities
python -m rita_agent_reach fetch https://github.com/cli/cli
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Sequence

from . import __version__
from .adapter import AgentReachAdapter, build_routing_index
from .errors import AgentReachError

EXIT_OK = 0
EXIT_FAILED = 1


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="rita-agent-reach",
        description="Agent Reach capability adapter (discovery, health check, routed fetch).",
    )
    parser.add_argument("--version", action="version", version=f"rita-agent-reach {__version__}")
    parser.add_argument(
        "--agent-reach-bin",
        default="agent-reach",
        help="Path to the agent-reach executable (default: agent-reach on PATH).",
    )
    parser.add_argument("--gh-bin", default="gh", help="Path to the gh executable.")
    parser.add_argument("--ytdlp-bin", default="yt-dlp", help="Path to the yt-dlp executable.")
    parser.add_argument(
        "--timeout", type=float, default=60.0, help="Per-command timeout in seconds."
    )

    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("available", help="Is the Agent Reach CLI installed?")
    sub.add_parser("doctor", help="Full channel report, as JSON.")
    sub.add_parser("capabilities", help="Channel -> available, as JSON.")
    sub.add_parser("routing", help="Routing metadata per channel, as JSON.")

    p_fetch = sub.add_parser("fetch", help="Fetch one public URL through its routed backend.")
    p_fetch.add_argument("url", help="Public http(s) URL. No login-gated sources.")
    p_fetch.add_argument(
        "--text-chars",
        type=int,
        default=600,
        help="Truncate the text field to this many characters (0 = no truncation).",
    )
    return parser


def _force_utf8_streams() -> None:
    """Print UTF-8 regardless of the console codepage.

    Without this our own CLI reproduces the upstream Windows bug this adapter
    works around: a non-ASCII title on a cp950/cp1252 console either becomes
    mojibake or raises UnicodeEncodeError and exits non-zero.
    """
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is None:
            continue
        try:
            reconfigure(encoding="utf-8", errors="replace")
        except (ValueError, OSError):  # pragma: no cover - already redirected
            pass


def _emit(payload: object) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def main(argv: Sequence[str] | None = None) -> int:
    _force_utf8_streams()
    args = _build_parser().parse_args(argv)
    adapter = AgentReachAdapter(
        agent_reach_bin=args.agent_reach_bin,
        gh_bin=args.gh_bin,
        ytdlp_bin=args.ytdlp_bin,
        timeout=args.timeout,
    )

    try:
        if args.command == "available":
            version = adapter.version()
            _emit({"available": version is not None, "version": version})
            return EXIT_OK if version else EXIT_FAILED

        if args.command == "doctor":
            _emit(dict(adapter.doctor().raw))
            return EXIT_OK

        if args.command == "capabilities":
            _emit(adapter.capabilities())
            return EXIT_OK

        if args.command == "routing":
            _emit(dict(build_routing_index(adapter.doctor())))
            return EXIT_OK

        if args.command == "fetch":
            result = adapter.fetch(args.url).to_dict()
            if args.text_chars and result.get("text"):
                text = result["text"]
                if len(text) > args.text_chars:
                    result["text"] = text[: args.text_chars] + "..."
                    result["metadata"]["text_truncated"] = True
            _emit(result)
            return EXIT_OK
    except AgentReachError as exc:
        # Failures stay classified all the way out to the exit boundary.
        print(
            json.dumps(
                {"status": "error", "code": exc.code.value, "message": exc.message},
                ensure_ascii=False,
                indent=2,
            ),
            file=sys.stderr,
        )
        return EXIT_FAILED

    return EXIT_FAILED


if __name__ == "__main__":  # pragma: no cover - exercised via __main__.py
    raise SystemExit(main())
