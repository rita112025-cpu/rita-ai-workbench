# Agent Reach capability adapter

A self-contained Python package that gives this project a **capability layer** for
research acquisition. It is additive: nothing under `research/agent-reach/` touches
the static site at the repository root, and the GitHub Pages deployment is unaffected.

## What Agent Reach is used for here

[Agent Reach](https://github.com/Panniantong/Agent-Reach) is, by its own design, a
capability layer rather than a scraper — it selects, installs and health-checks the
most reliable access path per platform, and the calling agent invokes the upstream
tool itself. There is no `agent-reach fetch` subcommand.

This adapter therefore uses it for exactly five things:

| Purpose | How |
| --- | --- |
| capability discovery | `agent-reach doctor --json` |
| backend availability | per-channel `status` / `active_backend` |
| health check | `AgentReachAdapter.is_available()` / `.doctor()` |
| routing metadata | `build_routing_index(report)` |
| controlled CLI execution | `AgentReachAdapter.fetch(url)` |

**Agent Reach is not this project's only or general-purpose crawler.**

## Install

Agent Reach is an *optional external tool*. This package has **no runtime
dependencies** and its unit tests run offline without it.

```bash
python -m venv .venv
.venv/Scripts/pip install -e "research/agent-reach[dev]"
```

To install Agent Reach itself, use the **GitHub archive**, not PyPI:

```bash
pip install "https://github.com/Panniantong/agent-reach/archive/main.zip"
```

> The PyPI package named `agent-reach` (version 0.1.0) is a **different, unrelated
> project** by another author. Installing it will not give you the CLI this adapter
> talks to. Verified 2026-09-16.

Install it into a virtualenv, not globally. Point the adapter at it with
`--agent-reach-bin` / `RITA_AGENT_REACH_BIN` when it is not on `PATH`.

## Health check

```bash
python -m rita_agent_reach available
python -m rita_agent_reach doctor
python -m rita_agent_reach capabilities
python -m rita_agent_reach routing
python -m rita_agent_reach fetch https://github.com/cli/cli
```

## Platforms

### Verified in this repository (2026-09-16, Agent Reach v1.5.0, Windows 11, Python 3.14.2)

| Channel | Backend | Evidence |
| --- | --- | --- |
| `github` | `gh` CLI 2.88.1 | `gh repo view cli/cli --json …` returns real repo data; adapter normalizes it |
| `youtube` | `yt-dlp` 2026.8.19 | `--dump-single-json` returns real title, uploader and duration |
| `web` | Jina Reader | `https://r.jina.ai/https://example.com` returns HTTP 200 with the real page text |

### Not verified here

Every other channel Agent Reach ships — `twitter`, `reddit`, `bilibili`, `xiaohongshu`,
`facebook`, `instagram`, `linkedin`, `xueqiu`, `xiaoyuzhou`, `boss`, `v2ex`, `rss`,
`exa_search`. `doctor` will report their status on your machine; this project makes no
claim about them and routes nothing to them.

### Channels that need a cookie or a login

`twitter`, `reddit`, `xiaohongshu`, `facebook`, `instagram`, `linkedin`, `xueqiu` and
`boss` all require an authenticated session upstream. **This adapter deliberately routes
to none of them.** `routing.SUPPORTED_CHANNELS` contains only `github`, `youtube` and
`web`, all of which are zero-config and need no login.

## Security limits

- **Authenticated browser state is not stored or committed by this project.** No
  cookies, no browser profiles, no tokens, no `.env`, no session files. The sub-project
  `.gitignore` blocks those paths as a second line of defence.
- No login automation, no CAPTCHA handling, no paywall or access-control circumvention,
  no proxy rotation, no fingerprint evasion.
- Subprocesses are launched from an **argv list with `shell=False`**; a string argv or a
  non-string element is rejected before execution. No user input is ever concatenated
  into a shell command.
- Every external call carries a timeout and the child is killed if it exceeds it,
  including on interrupt.
- Only public, non-login `http(s)` URLs are accepted; `file:`, `ftp:` and other schemes
  are refused.
- This integration targets publicly accessible content and does not override site
  access controls, robots policies, contractual restrictions, authentication
  requirements or rate limits.

## Fallback principles

1. **An Agent Reach failure does not imply the target source has no data.** `doctor`
   reports what is reachable *from this machine, right now, with this PATH* — nothing
   more. Treat `off` as "not configured here", never as "the platform is empty".
2. `warn` is not `available`. It means upstream could not positively confirm the
   backend, so `ChannelStatus.available` stays `False`. A `github` channel reporting
   `warn` while `gh` works fine is the expected case: `doctor` deliberately avoids
   running `gh auth status` because that command writes a device id.
3. A missing feature is not a broken integration. A YouTube video with no captions
   still returns a successful result with `transcript_available: false`.
4. HTTP 200 is not evidence of data. A reader response with no readable body is
   reported as `EMPTY_OUTPUT`, not as success.
5. Failures stay classified — `NOT_INSTALLED`, `TIMEOUT`, `EXIT_ERROR`,
   `MALFORMED_OUTPUT`, `EMPTY_OUTPUT`, `UNSUPPORTED_SOURCE`, `BACKEND_UNAVAILABLE`,
   `NETWORK_ERROR`, `HTTP_ERROR` — never a bare "fetch failed".

## Known upstream quirk (worked around)

On Windows, `agent-reach doctor --json` prints non-ASCII text and crashes with
`UnicodeEncodeError: 'cp950' codec …` (exit 1) whenever its child stdout falls back to
the ANSI codepage. Whether it triggers depends on the inherited environment, which makes
it an intermittent failure. `SubprocessRunner` pins every child to UTF-8
(`PYTHONIOENCODING`, `PYTHONUTF8`), and the CLI reconfigures its own streams for the
same reason. Covered by a regression test.

## Tests

```bash
# offline, no network, no agent-reach install required
.venv/Scripts/python -m pytest research/agent-reach

# opt-in, hits real CLIs and real public sites
.venv/Scripts/python -m pytest research/agent-reach -m integration
```

Integration tests are deselected by default (`addopts = -m 'not integration'`) so that a
third-party site having a bad afternoon never turns CI red, and each one skips rather
than fails when its backend is absent.

## Lint and types

```bash
.venv/Scripts/ruff check research/agent-reach
.venv/Scripts/ruff format --check research/agent-reach
.venv/Scripts/mypy --config-file research/agent-reach/pyproject.toml
```

## Out of scope

Patchright, authenticated browser automation, CAPTCHA bypass, proxy rotation, and
scraping protected or private content.
