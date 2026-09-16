"""Small CLI over the collector, for exercising it by hand.

python -m rita_scrapling fetch https://example.com
python -m rita_scrapling fetch https://example.com --field price=.price
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Sequence

from . import __version__
from .collector import ScraplingCollector
from .errors import CollectorError
from .evidence import EvidenceStore
from .models import ExtractionRule

EXIT_OK = 0
EXIT_FAILED = 1


def _force_utf8_streams() -> None:
    """Print UTF-8 regardless of the console codepage.

    Without this, a page title in any non-Latin script becomes mojibake, or
    raises UnicodeEncodeError on a Windows console and exits non-zero.
    """
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is None:
            continue
        try:
            reconfigure(encoding="utf-8", errors="replace")
        except (ValueError, OSError):  # pragma: no cover - already redirected
            pass


def _parse_field(spec: str) -> ExtractionRule:
    name, sep, selector = spec.partition("=")
    if not sep or not name.strip() or not selector.strip():
        raise argparse.ArgumentTypeError(f"expected name=css-selector, got {spec!r}")
    return ExtractionRule(name=name.strip(), selector=selector.strip(), adaptive=True)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="rita-scrapling",
        description="Public web collector (static fetch, extraction, raw evidence).",
    )
    parser.add_argument("--version", action="version", version=f"rita-scrapling {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    p_fetch = sub.add_parser("fetch", help="Fetch one public URL and normalize it.")
    p_fetch.add_argument("url", help="Public http(s) URL.")
    p_fetch.add_argument(
        "--field",
        action="append",
        default=[],
        type=_parse_field,
        metavar="NAME=SELECTOR",
        help="Extra field to extract, repeatable.",
    )
    p_fetch.add_argument("--timeout", type=float, default=30.0)
    p_fetch.add_argument("--output-dir", default="output", help="Where evidence is written.")
    p_fetch.add_argument(
        "--no-evidence", action="store_true", help="Do not write raw/normalized files."
    )
    p_fetch.add_argument(
        "--adaptive",
        action="store_true",
        help="Enable Scrapling adaptive element relocation for --field selectors.",
    )
    p_fetch.add_argument(
        "--text-chars",
        type=int,
        default=600,
        help="Truncate the text field in the printed output (0 = no truncation).",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    _force_utf8_streams()
    args = _build_parser().parse_args(argv)

    if args.command != "fetch":  # pragma: no cover - argparse enforces this
        return EXIT_FAILED

    collector = ScraplingCollector(
        evidence=EvidenceStore(args.output_dir),
        timeout=args.timeout,
        save_evidence=not args.no_evidence,
        adaptive=args.adaptive,
    )
    try:
        result = collector.fetch(args.url, rules=args.field).to_dict()
    except CollectorError as exc:
        print(
            json.dumps(
                {
                    "status": "error",
                    "code": exc.code.value,
                    "message": exc.message,
                    "url": exc.url,
                    "http_status": exc.status_code,
                },
                ensure_ascii=False,
                indent=2,
            ),
            file=sys.stderr,
        )
        return EXIT_FAILED

    if args.text_chars and result.get("text") and len(result["text"]) > args.text_chars:
        result["text"] = result["text"][: args.text_chars] + "..."
        result["metadata"]["text_truncated"] = True
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return EXIT_OK


if __name__ == "__main__":  # pragma: no cover - exercised via __main__.py
    raise SystemExit(main())
