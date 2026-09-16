# Research acquisition layer

Two independent, self-contained Python sub-projects. Neither touches the static site at
the repository root, and the GitHub Pages deployment is unaffected by either.

| Directory | What it is | Docs |
| --- | --- | --- |
| `agent-reach/` | Agent Reach capability adapter — discovery, backend availability, health check, routing metadata, controlled CLI execution | [README](agent-reach/README.md) |
| `scrapling/` | Scrapling parsing and adaptive extraction layer, with a stdlib HTTP transport | [README](scrapling/README.md) |

They share no files and no code. Each has its own `pyproject.toml`, `.gitignore`, tests
and README, so either can be worked on, upgraded or removed without disturbing the other.

## Verification snapshot — 2026-09-16

Recorded at `main = fd71292`, immediately after both integration PRs were merged
([#1](https://github.com/rita112025-cpu/rita-ai-workbench/pull/1) Agent-Reach,
[#2](https://github.com/rita112025-cpu/rita-ai-workbench/pull/2) Scrapling Phase 1).
Every number below was produced by an actual run on merged `main`, not by a run on the
feature branches.

### Environment

| Component | Version |
| --- | --- |
| OS | Windows 11 |
| Python | 3.14.2 |
| pytest | 9.1.1 |
| agent-reach | 1.5.0 (installed from the GitHub archive — see caution below) |
| yt-dlp | 2026.08.19 |
| gh | 2.88.1 |
| scrapling | 0.4.15 |

### Results

| Layer | Offline suite | Live suite | Status |
| --- | --- | --- | --- |
| Agent-Reach | **72 passed**, 5 deselected | **5 passed** | VERIFIED |
| Scrapling Phase 1 | **60 passed**, 6 deselected | **6 passed** | VERIFIED |

**0 skipped, 0 failed** across all four runs. No test was skipped, relaxed or rewritten
to make a run pass.

Live tests that actually executed:

- Agent-Reach — `agent-reach --version`; `doctor --json` (real channel report); a public
  GitHub repo through `gh`; a public YouTube video's metadata through `yt-dlp`; a public
  web page through Jina Reader.
- Scrapling — a static public page fetched, parsed and normalized; raw evidence written
  to disk; structured extraction against the live page; two consecutive fetches proven
  stable; a client-rendered SPA shown to be **incomplete** without a renderer; and
  `fetch_dynamic()` shown to **refuse** rather than silently downgrade to a static fetch.

### What is NOT verified

- **JavaScript rendering: NOT IMPLEMENTED — BLOCKED.** In Scrapling 0.4.15 every fetcher,
  including the plain HTTP one, imports patchright at module level, and patchright is out
  of scope for this project. `scrapling/src/rita_scrapling/dynamic.py` ships the
  `DynamicRenderer` contract and a refusal, nothing more.
- Agent Reach channels other than `github`, `youtube` and `web`. Everything requiring a
  cookie, a login or a browser session is deliberately unrouted.
- Spider / concurrent crawling / proxy rotation / anti-bot handling — none exist here.
- Linux and macOS. Nothing is Windows-specific by design, but neither was tested.

### Security and cost at the time of recording

| Check | Result |
| --- | --- |
| Patchright installed | NO |
| Paid API used | NO |
| New cookies / login state created | NO |
| Browser profile used | NO |
| Working tree | clean |

## This snapshot expires

It proves that on 2026-09-16, at approximately 03:10 UTC, 11 live integration tests
actually ran and passed. **It is not a standing guarantee.** Upstream releases, site
restructures, CLI version changes, rate limits and plain network conditions can all
change the outcome of a later run.

When a later run disagrees with this page, the two suites are built to tell you which
kind of change caused it:

- **offline suite fails** → the change is in our code
- **offline passes, live fails** → upstream, the target site, a CLI version, or the
  network. Not our code.

## Re-running the verification

```bash
py -m venv .venv
.venv/Scripts/pip install -e "research/agent-reach[dev]"
.venv/Scripts/pip install -e "research/scrapling[dev]"

# offline: no network, no external CLI required
.venv/Scripts/python -m pytest research/agent-reach
.venv/Scripts/python -m pytest research/scrapling
```

The live suites are opt-in (`-m integration`) and deselected by default, so CI never
depends on a third-party site.

```bash
.venv/Scripts/python -m pytest research/agent-reach -m integration -v
.venv/Scripts/python -m pytest research/scrapling -m integration -v
```

The Agent-Reach live suite needs `agent-reach` and `yt-dlp`; each test skips rather than
fails when its backend is absent. Point the suite at binaries that are not on `PATH` with
`RITA_AGENT_REACH_BIN`, `RITA_YTDLP_BIN` and `RITA_GH_BIN`.

> **Caution when installing Agent Reach.** Use the GitHub archive:
> `pip install "https://github.com/Panniantong/agent-reach/archive/main.zip"`.
> The PyPI package named `agent-reach` (0.1.0) is an **unrelated project by a different
> author** and will not provide this CLI. Verify with `pip show agent-reach` — the
> home page must be `github.com/Panniantong/agent-reach`.

## Standing constraints

Both layers are built for **publicly accessible content**. Neither overrides site access
controls, robots policies, contractual restrictions, authentication requirements or rate
limits. No login automation, no CAPTCHA handling, no anti-bot or fingerprint evasion, no
proxy rotation, no paid APIs. No cookies, tokens, browser profiles, `.env` files or
session state are stored or committed.

A failure to reach a source never implies the source has no data.
