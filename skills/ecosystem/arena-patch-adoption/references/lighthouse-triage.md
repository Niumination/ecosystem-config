# Lighthouse CI Triage — niu-oss-dashboard

`niu-oss` runs Lighthouse CI on every push (`.github/workflows/lighthouse.yml`): static export (`npm run export:static`) served from `out/`, 3 runs per URL, assertions in `lighthouserc.json`.

## Assertions (failure = error, blocks CI)

| Assertion | Budget | Common cause when it fails |
|---|---|---|
| `categories:performance` | ≥ 0.8 | CI local-server throttling — cross-check live before calling it a regression |
| `categories:accessibility` | ≥ 0.95 | real a11y regression (contrast, tap targets); the axe-core CI step covers the same surface |
| `categories:best-practices` | ≥ 0.9 | console errors, missing link rel, HTTPS issues |
| `categories:seo` | ≥ 0.9 | missing title/description on a page, duplicate `robots` meta, `font-size` audit |
| `largest-contentful-paint` | < 3800ms (warn < 2500) | heavy initial JS (baseline ~965 KB, creeping) |
| `cumulative-layout-shift` | < 0.05 | client-side re-render post-hydration |

## Reading a failure

```bash
gh run view <run-id> --repo Niumination/Niu-OSS-Dashboard --log-failed \
  | grep -E '✘|expected|found|result\(s\) for'
```
The log prints one `result(s) for <url>` block per failing URL — group fixes by URL, not by symptom.

## SEO failure on 404 / not-found pages

Inspect the exported HTML, not the source:
```bash
grep -oE '<meta name="robots"[^>]*>' out/_not-found.html
grep -o '<title>[^<]*</title>' out/_not-found.html
```
- Missing title/description → add `export const metadata` to `app/not-found.tsx` (title, description, canonical only).
- **Never add `robots: { index: true }` to not-found metadata.** Next.js already emits `<meta name="robots" content="noindex">` on not-found; your key only adds a SECOND robots tag, Lighthouse still reads `noindex`, and SEO stays failed.
- Title renders doubled (`X — Niumination — Niumination`) → `app/layout.tsx` sets `metadata.title.template = '%s — Niumination'`; pass the short title only.

## Performance below budget

The CI build is a local static server on a GitHub Actions runner — scores are throttled and land below live. Before treating a perf failure as a regression, fetch the live page directly (local DNS may be stale, so pin the Vercel IP):
```bash
curl -s --max-time 25 --resolve niumination.web.id:443:216.198.79.1 \
  https://niumination.web.id -o /tmp/oss-live.html
```
If live is healthy and only CI fails, suspect incremental bundle growth rather than a code regression.

## font-size audit (SEO sub-check)

Lighthouse `font-size` flags any text rendered under 12px. This codebase deliberately uses many `text-[8..11.5px]` Tailwind literals (RepoCard, DashboardMetrics, CommandMenu, NavBar, Hero3D …). Find them:
```bash
grep -rnoE 'text-\[[0-9]+(\.[0-9]+)?px\]' app/ components/ \
  | awk -F'text-\[' '{split($2,a,"px"); if (a[1]+0 < 12) print}'
```
Raising them to ≥12px is a **sitewide design change** (layout shifts on nearly every component) — count the occurrences, report, and let the owner decide. Do not batch-rewrite classes unprompted.
