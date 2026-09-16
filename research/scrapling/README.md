# Scrapling public web collector

A self-contained Python package for **public web acquisition**: fetch, keep the raw
evidence, normalize, extract. Additive: nothing under `research/scrapling/` touches the
static site at the repository root.

## Scope

- public web acquisition
- HTML extraction
- structured extraction (named CSS rules)
- adaptive selector support (Scrapling element relocation)
- optional JavaScript rendering — **interface only, see below**

This integration is intended for publicly accessible content and does not override site
access controls, robots policies, contractual restrictions, authentication requirements,
or rate limits.

## The patchright constraint, and what it changed

Scrapling 0.4.15's `fetchers` extra declares **patchright** as a dependency, and
`scrapling/engines/toolbelt/convertor.py` imports it at module level. Verified on
2026-09-16: installing `scrapling` + `curl_cffi` + `playwright` **without** patchright
makes `Fetcher`, `DynamicFetcher` and `StealthyFetcher` all fail to import with
`ModuleNotFoundError: No module named 'patchright'`. There is no partial path — even the
plain HTTP `Fetcher` needs it.

This project does not install or integrate patchright. So:

| Concern | Implementation |
| --- | --- |
| HTML parsing | **Scrapling** `scrapling.parser.Selector` |
| adaptive element relocation | **Scrapling** `Selector(adaptive=True)` + SQLite element store |
| HTTP transport | standard library, behind the `Transport` protocol |
| JavaScript rendering | `DynamicRenderer` protocol, **no implementation shipped** |

Scrapling is used for the thing it is uniquely good at. The transport is boring on
purpose and sits behind a seam, so a Scrapling-based transport can replace it later
without touching the collector, the normalized result or the error taxonomy.

## Install

```bash
python -m venv .venv
.venv/Scripts/pip install -e "research/scrapling[dev]"
```

`scrapling>=0.4.15,<0.5` is a real runtime dependency and installs from PyPI with **no
browser download and no `scrapling install` step** — that command exists to fetch the
Fetchers' browser dependencies, which this package does not use.

## Use

```bash
python -m rita_scrapling fetch https://example.com
python -m rita_scrapling fetch https://example.com --field heading=h1
python -m rita_scrapling fetch https://example.com --adaptive --field price=.price
```

```python
from rita_scrapling import ExtractionRule, ScraplingCollector

collector = ScraplingCollector()
result = collector.fetch(
    "https://example.com",
    rules=[ExtractionRule(name="heading", selector="h1", required=True)],
)
result.title            # "Example Domain"
result.metadata["fields"]["heading"]
result.raw_path         # where the verbatim HTML was kept
```

## Normalized result

```json
{
  "source_url": "https://example.com",
  "fetched_at": "2026-09-16T02:50:34+00:00",
  "status": "success",
  "title": "Example Domain",
  "text": "...",
  "metadata": {
    "final_url": "...", "http_status": 200, "content_type": "text/html",
    "content_chars": 559, "text_chars": 127, "attempts": 1, "elapsed_s": 0.219,
    "rendered": false, "adaptive": false, "fields": {"heading": "Example Domain"}
  },
  "raw_path": "output/raw/example.com/...html",
  "collector": "scrapling",
  "collector_version": "0.1.0"
}
```

No Scrapling object crosses this boundary.

## Raw evidence

```
output/raw/<host>/<timestamp>-<digest>.html        verbatim response body
output/raw/<host>/<timestamp>-<digest>.meta.json   url, final url, status, content type,
                                                   size, attempts, timing, collector+version
output/normalized/<host>/<timestamp>-<digest>.json the normalized result
```

Raw evidence is written **before** parsing, so a page that fails extraction can still be
inspected. `output/` is a runtime artifact and is git-ignored: raw pages are someone
else's content, they get large, and no production acquisition data belongs in this
repository.

## Error taxonomy

`INVALID_URL`, `NETWORK_ERROR`, `TIMEOUT`, `HTTP_ERROR`, `RATE_LIMITED`, `EMPTY_BODY`,
`EXTRACTION_ERROR`, `RENDER_ERROR`, `DEPENDENCY_UNAVAILABLE`. Never a bare
"fetch failed". `RATE_LIMITED` is separate from `HTTP_ERROR` so callers can back off
rather than retry blindly or give up.

## Rate limiting and retries

Conservative by default, and no concurrency at all:

| Setting | Default |
| --- | --- |
| request timeout | 30 s |
| max attempts | 3 |
| retryable statuses | 429, 500, 502, 503, 504 |
| backoff | exponential, 1 s base, 10 s cap |
| `Retry-After` | honoured, clamped to 120 s |
| minimum interval between requests | 1 s |
| concurrency | 1 |

404 is never retried. There is no Spider and no parallel crawl in this version.

## Verified behavior (2026-09-16, Scrapling 0.4.15, Python 3.14.2, Windows 11)

**Static page** — `https://example.com`, public, no login, no CAPTCHA, server-rendered:
HTTP 200, `title == "Example Domain"`, body text contains "documentation examples",
`h1` extracted as "Example Domain", raw + normalized evidence written, and two
consecutive fetches produce identical title and text.

**Adaptive relocation** — verified, against real Scrapling storage. A local fixture moves
the element across both container and tag:

```html
<div class="product-card"><span class="price">$100</span></div>            <!-- v1 -->
<section class="product-card-v2"><strong class="product-price">$100</strong></section>  <!-- v2 -->
```

`.price` matches nothing in v2 — asserted separately, so the relocation test cannot pass
for the wrong reason — yet after a v1 run saved the element, a v2 run recovers `$100`.

**JavaScript rendering** — **NOT VERIFIED. Blocked**, because the only Scrapling path to
it requires patchright. What *was* verified is why it matters: a static fetch of the
public React SPA at `https://todomvc.com/examples/react/dist/` returns HTTP 200 and the
title `TodoMVC: React`, with 72 characters of static chrome and none of the application
content. `fetch_dynamic()` raises `DEPENDENCY_UNAVAILABLE` and deliberately does **not**
fall back to a static fetch, because returning that shell would look like success.

## Tests

```bash
# offline: no network, fake transport, local fixtures
.venv/Scripts/python -m pytest research/scrapling

# opt-in: hits example.com and todomvc.com
.venv/Scripts/python -m pytest research/scrapling -m integration
```

Integration tests are deselected by default so CI never depends on a third-party site.

## Lint and types

```bash
.venv/Scripts/ruff check research/scrapling
.venv/Scripts/ruff format --check research/scrapling
.venv/Scripts/mypy --config-file research/scrapling/pyproject.toml
```

## Security / privacy

- No cookies, browser profiles, tokens, `.env` files or sessions are stored or committed;
  the sub-project `.gitignore` blocks those paths, plus `output/` and the adaptive
  element store.
- Only public `http(s)` URLs are accepted.
- No login automation, no CAPTCHA handling, no anti-bot evasion, no fingerprint
  spoofing, no proxy rotation.
- No paid API and no cost-incurring third-party service.
- A polite request interval and a hard retry ceiling are on by default.

This project makes no claim to bypass Cloudflare, bypass anti-bot systems, be
undetectable, or scrape any site — regardless of how upstream markets itself.

## Known limitations

- JavaScript rendering is unimplemented (see above).
- No Spider, no concurrent crawling, no proxy support in this version.
- `Retry-After` in HTTP-date form is ignored in favour of exponential backoff.
- Robots parsing is not implemented here; this package does not override robots policies
  and is meant for publicly accessible pages.
- Verified on Windows only.
- A third-party site being fetchable today is not a guarantee it will stay that way.

## Out of scope

- Patchright
- CAPTCHA bypass
- stealth browser fingerprint bypass
- authenticated social-platform scraping
- proxy rotation infrastructure
- large-scale crawling
