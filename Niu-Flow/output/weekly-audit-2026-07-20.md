# Weekly Code Audit — 2026-07-20

**Cron job timestamp:** 2026-07-20
**Auditor:** Hermes Agent (Niu-Flow manual fallback — JCode unavailable due to persistent timeout with deepseek-v4-flash-free)

## Summary
- Projects scanned: 3
- 🔴 Critical: 1
- 🟡 High: 4
- ⚪ Info: 9
- Note: JCode bridge (`jcode run --json --quiet`) timed out on every attempt. Audit performed via manual `search_files` scanning, `npm outdated`, and git inspection.

## Deployment Status
- **PemdiAcehTengah:** 200 OK
- **niu-vermilion:** 307 Redirect (live)
- **kune-ya.com:** DOWN (unreachable — curl timeout/fail)

## Git Status
- All projects: clean working tree, no uncommitted changes.

---

## Per-Project Breakdown

### 1. PemdiAcehTengah
**Path:** `/Users/zaryu/Desktop/Niumination/Production/PemdiAcehTengah/`
**Stack:** Next.js 14, React 18, pure CSS, Supabase
**Git log:** `575af70` fix(opd-slug): fix title warning — use template literal for single text node
**Deploy:** `https://pemdi-aceh-tengah.vercel.app` — 200 OK

**Findings:**
- 🔴 `0` critical | 🟡 `1` | ⚪ `3`

| Severity | Category | File:Line | Description |
|----------|----------|-----------|-------------|
| 🟡 | security | pages/faq.js:141, pages/tanya.js:125, pages/_document.js:26, pages/_app.js:22 | `dangerouslySetInnerHTML` used with custom `sanitizeHtml()`. XSS risk if sanitizer regex fails on edge-case payloads. |
| ⚪ | stale_dep | package.json:17 | Next.js 14.2.35 vs latest 16.2.10 — major version lag |
| ⚪ | stale_dep | package.json:18 | React 18.3.1 vs latest 19.2.7 — major version lag |
| ⚪ | stale_dep | package.json:22 | eslint 8.57.1 vs latest 10.7.0 — major version lag (devDependency) |

---

### 2. niu-vermilion
**Path:** `/Users/zaryu/Desktop/Niumination/Production/niu-vermilion/`
**Stack:** Next.js 16, Supabase, TipTap, Tailwind CSS, iron-session
**Git log:** `a01a558` 🔒 fix session cookie bug + add middleware for dashboard gating + timing-safe password comparison
**Deploy:** `https://niu-vermilion.vercel.app` — 307 Redirect (live)

**Findings:**
- 🔴 `0` critical | 🟡 `1` | ⚪ `4`

| Severity | Category | File:Line | Description |
|----------|----------|-----------|-------------|
| 🟡 | security | src/app/dashboard/bookmarks/BookmarksClient.tsx:346 | `innerHTML` assignment on favicon error fallback. Injects static SVG string. Low risk but type-unsafe and avoidable. |
| ⚪ | stale_dep | package.json:35 | react-dropzone 15.0.0 vs latest 19.1.1 — major version lag |
| ⚪ | stale_dep | package.json:38 | tailwindcss 4.3.0 vs 4.3.3 — patch lag |
| ⚪ | stale_dep | package.json:39 | @tailwindcss/postcss 4.3.0 vs 4.3.3 — patch lag |
| ⚪ | stale_dep | package.json:41-44 | TypeScript 5.9.3 vs 7.x — major gap; @types/node 20.19.42 vs 20.19.43 — patch lag |

---

### 3. kune-ya.com
**Path:** `/Users/zaryu/Desktop/Niumination/Production/kune-ya.com/`
**Stack:** Next.js 15, Prisma, next-auth, OpenAI, mammoth, pdf-parse, Tailwind CSS
**Git log:** `bf36ab9` 🔒 fix analytics auth + fix rate limit path for login
**Deploy:** `https://kune-ya.com` — FAILED (unreachable / timeout)

**Findings:**
- 🔴 `1` critical | 🟡 `2` | ⚪ `2`

| Severity | Category | File:Line | Description |
|----------|----------|-----------|-------------|
| 🔴 | stale_dep | package.json:16 | `next-auth` 5.0.0-beta.31 deployed in production. Stable v4.24.14 available. Beta builds risk API instability and unpatched vulnerabilities. |
| 🟡 | security | middleware.ts:5-16 | CSP header contains `'unsafe-inline'` and `'unsafe-eval'` in `script-src`, weakening XSS mitigation. |
| 🟡 | security | middleware.ts:75-78 | Middleware matcher explicitly excludes `/login` and `/register` routes, meaning security headers and rate limiting are **not applied** to authentication pages. |
| ⚪ | stale_dep | package.json:19 | prisma 6.19.3 vs latest 7.8.0 — major version lag |
| ⚪ | stale_dep | package.json:19 | pdf-parse 1.1.1 vs latest 2.4.5 — major version lag |

---

## Recommendations
1. **Fix kune-ya.com next-auth beta immediately** — pin to stable v4 or upgrade to v5 stable once released. This is the most critical finding.
2. **Restore kune-ya.com deployment** — the site is currently down. Investigate Vercel build/deploy logs and restore service.
3. **Strengthen CSP on kune-ya.com** — remove `'unsafe-inline'` and `'unsafe-eval'` if possible, or scope them to nonce-based delivery. Do not exclude login/register from middleware — these routes need the strongest protection.

---
*Report saved to output/weekly-audit-2026-07-20.md*
