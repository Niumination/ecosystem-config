---
name: snapshot-verification
description: Verify static snapshot deployment and content.
tags: [verification, snapshot, deploy, static-site, integrity]
---

# Snapshot Verification

## Overview

Verify a static snapshot (HTML dashboard, page capture) is correctly deployed and functional.

## Pre-Verification Gate

**ALWAYS check if snapshot already exists before creating/redeploying.**

```bash
# Check if file exists in repo
gh api /repos/{owner}/{repo}/contents/<path> --jq '.download_url, .size'

# Check local file exists
ls -la <path>

# Check git history for recent snapshot commits
git log --oneline --grep='snapshot\|gh-pages' -n 5
```

If the snapshot already exists and is verified, skip re-creating an **identical** artifact. A
snapshot built from a different source — another branch, another commit, fresh data — is a NEW
artifact, not a duplicate. Check what the source is before refusing: compare the branch/commit the
capture came from and the data timestamp baked into the banner.

## Verify the DATA, not the pixels

Rendered-text checks give false failures on real dashboards. Two rules:

1. **Assert against the full DOM, never only visible text.** `page.inner_text('body')` returns only
   what is *currently visible*. Dashboards that render sections as collapsed panels or popups keep
their data in the DOM but out of the visible text, so `inner_text` reports the content missing when
it is perfectly fine. Use `page.content()` (full serialized HTML) for presence assertions, and
`inner_text` only to check that some label is actually on screen.
2. **Exercise the injected fetch stub directly — that is the real test.** A static snapshot's whole
   contract is "`fetch` still resolves without a backend". Call it from the page context:

```javascript
await (async () => {
  const r = await fetch('/api/status');
  return await r.json();          // must return the frozen payload, not throw
})()
```

Assert on **typed fields**, not substrings of the page text. `'14' in body_text` is satisfied by any
version number, price, or year on the page — a false PASS. `json.n_records === 662` is a real check.

Ready-made harness: `scripts/verify_snapshot.py <url>` runs the stub probes, the zero-error check,
and optional DOM presence/absence assertions in one shot.

## Banner leakage from local capture

A snapshot captured from a local server bakes the capture origin into its banner (e.g. a sticky bar
reading "captured from `http://127.0.0.1:<port>`"). That is a cosmetic string — the important check
is that no *live request* still targets a local address. Forbid the request target, not the bare
host:

- Assert absent: `127.0.0.1:<port>/api` (a real leftover fetch — the snapshot would fail offline).
- Do not fail on a lone `127.0.0.1:<port>` mention in a banner label; instead patch the label to a
  human-meaningful origin (branch + commit) with a single exact-string replace, then re-run
  verification to confirm the artifact still passes.

## Capturing From a Non-Default Branch When the Source Is Down

A snapshot of a non-default branch cannot be captured from the live site once that host is gone.
Capture locally without disturbing the primary checkout:

1. `git worktree add /tmp/<proj>-wt origin/<branch>` — the `main` working tree stays clean.
2. Copy the runtime config the worktree lacks (`config.json` is usually gitignored).
3. Restore the runtime DATA, which never lives in git (SQLite DB, JSON caches), from the newest
   backup archive. Backups are often nested — if `tar -tzf` lists a single `.tgz` entry, extract
   twice before concluding the archive is empty.
4. Start the app on a spare port in the background, then probe EVERY endpoint the dashboard calls
   and require 200 before capturing — one 404 endpoint gets baked in as a broken stub.
5. Capture against the local base:
   `python3 scripts/make_snapshot.py --base http://127.0.0.1:<port> --out snapshot/<name>.html`
6. Patch the banner label to the branch + commit before publishing, then re-run verification.
7. Tear down: kill the servers, `git worktree remove <path> --force`.

**Prove the artifact really came from the NEW source.** Compare the branch commit and one data
marker (record/row count) against the previous snapshot; a larger file size is not evidence.

## Verification Checklist

After deploying snapshot to GitHub Pages:

1. **HTTP check**: `curl -sI https://<user>.github.io/<repo>/<path>` → must be HTTP/2 200
2. **Root check**: `curl -sI https://<user>.github.io/<repo>/` → may be 404 if no index.html (expected)
3. **Build status**: `gh api /repos/{owner}/{repo}/pages --jq '.status'` → "built" (wait if "building")
4. **Content integrity**: Check file size matches expected, key data markers present
5. **HTML validation**: `grep -c "<script" <file>` and `grep -c "SNAP\|static mode"` for snapshot-specific markers

### Custom Domain Verification

If a custom domain is configured (e.g., via Cloudflare CNAME):

1. **DNS resolution check**: `curl -sI https://<custom-domain>/` → must NOT return "Could not resolve host". If it does, DNS hasn't propagated yet.
2. **Wait for propagation**: Cloudflare DNS typically propagates in ~5 min. Poll with `curl` every 30s.
3. **HTTPS auto-enable**: GitHub Pages auto-configures HTTPS via Cloudflare. Check `curl -sI https://<custom-domain>/` returns HTTP/2 200.
4. **macOS DNS cache may be stale** — `dig` resolves correctly but `curl` fails with "Could not resolve host". Fix: `sudo dscacheutil -flushcache && sudo killall -HUP mDNSResponder`. Bypass with `curl --resolve <domain>:443:<cloudflare-ip>`. See `references/dns-cloudflare.md` in the `github-pages-deploy` skill.
5. **DO not add CNAME alongside existing A record** — DNS rejects coexisting A + CNAME for the same hostname. REPLACE the A record with CNAME pointing to `niumination.github.io` (Cloudflare proxy ON), or use a NEW subdomain.

### Landing / picker page link check

When the root is a hand-written landing or picker page (several artifacts, one entry point), the
failure mode is a dead or mistyped *relative* link: the page renders perfectly and every card 404s.
Resolve every link from the page context and assert the targets, not the markup:

```python
links = pg.eval_on_selector_all("a[href]", "els => els.map(e => e.getAttribute('href'))")
for href in links:
    if not href.startswith("http"):
        assert pg.request.get(base + "/" + href.lstrip("./")).status == 200
```

Also assert the card count and the `h2` headings so an empty grid cannot pass silently, and keep a
full-page screenshot for the layout check. Harness: `scripts/verify_landing_links.py <url> [cards]`.

## Common Failure Patterns

| Symptom | Root Cause | Fix |
|---------|-----------|-----|
| 404 on file | Wrong path or build not ready | Check `gh api /repos/.../pages` status; wait 60s |
| 404 on root | No index.html at root | Use subdirectory path; create index.html redirect |
| Build failure | Jekyll checkout error | Use clean orphan branch; remove LFS/submodules |
| File too small | Truncated during upload | Re-upload; verify file size matches |
| 500 error | Syntax error in HTML | Check browser console; validate HTML |

## Data Integrity Markers (MATA Dashboard)

- `mata-snapshot-stub` script tag present
- `SNAP` object with `/api/status`, `/api/flags` keys
- `n_records`, `n_flags`, `n_flags_tinggi` values present
- "static mode" in chat/locate responses
- `0 JS runtime error` verification
