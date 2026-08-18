# Weekly Code Audit — 2026-07-06

## Summary
- **Projects scanned:** 3 (PemdiAcehTengah, niu-vermilion, kune-ya.com)
- **🔴 Critical:** 3 findings
- **🟡 High:** 4 findings  
- **⚪ Info:** 5 findings
- **Methodology:** manual scanning via search_files + terminal (JCode timed out at 300s on full audit)

---

## Live URL Status

| Project | URL | Status |
|---------|-----|--------|
| PemdiAcehTengah | https://pemdi-aceh-tengah.vercel.app | ✅ HTTP 200 |
| niu-vermilion | https://niu-vermilion.vercel.app | ✅ HTTP 307 → /dashboard |
| kune-ya.com | https://kune-ya.com | ❌ **NXDOMAIN** (DNS not resolving) |
| kune-ya.com | https://kune-ya-com.vercel.app | ✅ HTTP 200 (Vercel preview URL) |

## Git Status

| Project | Remote | Last Commit | Status |
|---------|--------|-------------|--------|
| PemdiAcehTengah | git@github.com:niumination/PemdiAcehTengah.git (SSH ✅) | `d480fc8` — update BACKLOG.md + sitemap | ✅ Clean |
| niu-vermilion | git@github.com:Niumination/Niu-Vermilion.git (SSH ✅) | `6f2f036` — mv: niu-vermilion → Production/ | ✅ Clean |
| kune-ya.com | git@github.com:Niumination/kune-ya.com.git (SSH ✅) | `52f432e` — mv: kune-ya.com → Production/ | ✅ Clean |

---

## Per-Project Breakdown

---

### 1. PemdiAcehTengah (Government Portal)

**Stack:** Next.js 14.2.35, React 18.3.1, Supabase, Pages Router
**Files scanned:** 29 pages + 9 API routes + 8 lib files
**Deploy:** ✅ Vercel live (HTTP 200)

#### 🔴 CRITICAL

*None found.*

#### 🟡 HIGH

| # | Finding | Location | Description |
|---|---------|----------|-------------|
| 1 | **dangerouslySetInnerHTML on user content** | `pages/faq.js:83` | Uses `dangerouslySetInnerHTML={{ __html: sanitizeHtml(q.jawab) }}` — sanitize mitigates risk, but bypasses React XSS protection. If sanitizeHtml has any bypass, this becomes a stored XSS vector. |
| 2 | **dangerouslySetInnerHTML on user content** | `pages/tanya.js:125` | Same pattern: `dangerouslySetInnerHTML={{ __html: sanitizeHtml(m.text) }}` for chatbot messages. |
| 3 | **No middleware.ts** | — | Security headers are set via `next.config.js` (good), but there's no edge middleware for: path-based access control, rate limiting at CDN level, bot detection, or geo-blocking. |
| 4 | **Major framework version gap** | `package.json` | Next.js 14.2.x → latest 16.2.10 (2 major versions behind). React 18.3.1 → latest 19.2.7 (1 major behind). No minor/patch security updates being applied automatically (pinned to ^14.2.0). |

#### ⚪ INFO

| # | Finding | Location | Description |
|---|---------|----------|-------------|
| 1 | **Security headers via next.config** | `next.config.js` | Good: CSP, X-Frame-Options, X-Content-Type-Options, Referrer-Policy, Permissions-Policy all set. CSP uses `'unsafe-inline'` for scripts (common for Next.js) but could be more restrictive. |
| 2 | **Admin auth uses Bearer token** | `lib/adminAuth.js` | Simple but functional: compares Bearer token against `ADMIN_PASSWORD` env var. Rate-limited (5 attempts/min/IP). No session management — token is stored in `sessionStorage`. |
| 3 | **API security basics present** | `pages/api/lapor.js` | CORS headers, input sanitization (`sanitizeText`), rate limiting (5 POST/min/IP), IP hashing. Good for a government portal. |
| 4 | **Supabase dependency** | `package.json` | `@supabase/supabase-js` is at 2.108.1, latest 2.110.0 — minor update available. |
| 5 | **Git history has no leaked secrets** | — | Scanned git log for `sk-` patterns — no secrets found in commit history. |
| 6 | **Admin page protected** | `pages/admin.js` | Login page has `noindex, nofollow` meta tag, requires Bearer token authentication for all data fetches. |

---

### 2. niu-vermilion (Second Brain)

**Stack:** Next.js 16.2.7, React 19.2.4, Supabase, TipTap v3, App Router
**Files scanned:** ~43 source files in src/
**Deploy:** ✅ Vercel live (HTTP 307 → /dashboard)

#### 🔴 CRITICAL

*None found.*

#### 🟡 HIGH

*None found.*

#### ⚪ INFO

| # | Finding | Location | Description |
|---|---------|----------|-------------|
| 1 | **innerHTML on image error fallback** | `src/app/dashboard/bookmarks/BookmarksClient.tsx:344-347` | Uses `parentElement!.innerHTML = '<svg class="..." .../>'` on image load error. The SVG is hardcoded so no user-input vector, but it bypasses React's DOM management. Minor risk. |
| 2 | **Multiple minor dependency updates** | `package.json` | 20+ packages have minor/patch updates available: tiptap extensions (3.26.0→3.27.1), tailwindcss (4.3.0→4.3.2), @supabase/supabase-js (2.108.0→2.110.0), lucide-react (1.17.0→1.23.0). No major gaps. |
| 3 | **Clean security posture** | — | No dangerous patterns found: uses `iron-session` for auth, no hardcoded secrets in source, no eval(), no direct SQL. Modern framework (Next.js 16 + React 19) ensures latest security patches. |
| 4 | **Config references env vars** | `supabase/config.toml:101,294,326` | Uses `env(VAR_NAME)` pattern for OpenAI key, Twilio auth token, Apple secret — proper approach, no hardcoded values. |

---

### 3. kune-ya.com (Full Website)

**Stack:** Next.js 15.5.19, React 19.1.0, Prisma 6.19.3, next-auth 5.0.0-beta.31, OpenAI SDK
**Files scanned:** ~27 source files in app/
**Deploy:** ❌ **Custom domain down** (NXDOMAIN), ✅ Vercel preview works

#### 🔴 CRITICAL

| # | Finding | Location | Description |
|---|---------|----------|-------------|
| 1 | **🔴 Custom domain DNS NXDOMAIN** | DNS check | `kune-ya.com` returns **NXDOMAIN** — the domain does not resolve at all. The Vercel preview URL `kune-ya-com.vercel.app` works (HTTP 200). **This means the live website is inaccessible to users.** Possible causes: expired domain, deleted DNS records, or misconfigured Vercel domain. |
| 2 | **🔴 .env file on disk with live API key** | `.env` | File contains `OPENAI_API_KEY="sk-CN2...EFgA"` (live key). File is listed in `.gitignore` and NOT tracked in git. However, it exists on the production disk and could be exposed through server-side vulnerabilities. |
| 3 | **🔴 next-auth v5 beta in production** | `package.json` | Using `next-auth@5.0.0-beta.31` — **beta software** for authentication in a production website. Beta versions may have unpatched security vulnerabilities, unstable APIs, or breaking changes on upgrade. |

#### 🟡 HIGH

| # | Finding | Location | Description |
|---|---------|----------|-------------|
| 1 | **Prisma major version gap** | `package.json` | Prisma 6.19.3 → latest 7.8.0 (1 major version behind). Potential security patches missed. |
| 2 | **Next.js major version gap** | `package.json` | Next.js 15.5.19 → latest 16.2.10 (1 major behind). |
| 3 | **pdf-parse legacy version** | `package.json` | `pdf-parse@1.1.1` — latest is 2.4.5. V1 is largely unmaintained with known issues. |

#### ⚪ INFO

| # | Finding | Location | Description |
|---|---------|----------|-------------|
| 1 | **✅ Strong middleware security** | `middleware.ts` | Excellent security setup: CSP (with `'unsafe-inline'` for scripts), rate limiting (60/min general, 10/min auth), X-Content-Type-Options, X-Frame-Options DENY, XSS-Protection, Referrer-Policy, Permissions-Policy. Production-only CSP enforcement. |
| 2 | **✅ API routes properly authenticated** | `app/api/conversations/route.ts` | Uses `auth()` session check from next-auth on all API routes. Returns 401 for unauthenticated requests. |
| 3 | **dangerouslySetInnerHTML for theme script** | `app/layout.tsx:54` | Theme detection script (localStorage) — no user input, acceptable pattern. |
| 4 | **No hardcoded secrets in git history** | — | Scanned git log for `sk-` patterns — .env.example only has placeholder values. No secrets committed. |
| 5 | **Minor dependency updates available** | `package.json` | Several packages have minor/patch updates: openai (6.42.0→6.45.0), tailwindcss (4.3.0→4.3.2), typescript (5.9.3→6.0.3). |

---

## Scoreboard

| Project | 🔴 Critical | 🟡 High | ⚪ Info | Health |
|---------|:-----------:|:-------:|:-------:|--------|
| PemdiAcehTengah | 0 | 4 | 6 | 🟡 Fair |
| niu-vermilion | 0 | 0 | 4 | 🟢 Good |
| kune-ya.com | 3 | 3 | 5 | 🔴 Needs Attention |

---

## Recommendations (Top Priority)

### 🚨 Fix This Week

1. **🔴 [kune-ya.com] Fix DNS/domain**: `kune-ya.com` is completely inaccessible. Options:
   - Check domain registration status (renew if expired)
   - Re-add custom domain in Vercel dashboard (`vercel domains add kune-ya.com`)
   - Verify DNS records point to Vercel's nameservers
   - Temporary: redirect or inform users to use preview URL
   
2. **🔴 [kune-ya.com] Secure API key**: The `.env` file with `OPENAI_API_KEY` exists on disk. Actions:
   - Rotate the OpenAI API key immediately (it was visible in search results)
   - Ensure `.env` is in `.gitignore` (it is ✅)
   - Consider using Vercel Environment Variables instead of .env file

3. **🔴 [kune-ya.com] Upgrade next-auth to stable**: Replace `next-auth@5.0.0-beta.31` with the stable release (`next-auth@5` or `@auth/nextjs` depending on migration path). Beta auth library in production is a security risk.

### 🟡 Address This Month

4. **🟡 [PemdiAcehTengah] Review dangerouslySetInnerHTML usage**: While sanitizeHtml() mitigates risk, audit `faq.js:83` and `tanya.js:125` to ensure content is properly sanitized and consider using a safer rendering approach.

5. **🟡 [PemdiAcehTengah] Plan Next.js 14→16 upgrade**: Major version upgrade needed for security patches. Test thoroughly on staging before deploying.

6. **🟡 [kune-ya.com] Upgrade Prisma 6→7**: Major version bump. Check migration guide for breaking changes.

### ⚪ Monitor

7. **⚪ [niu-vermilion] Apply minor dependency updates**: Run `npm update` for patch/minor updates across 20+ packages.

8. **⚪ [All] Security header audit**: PemdiAcehTengah's CSP allows `'unsafe-inline'` for scripts — consider tightening with nonces or hashes if feasible.

---

## JCode Session

JCode was invoked for full codebase audit but **timed out at 300 seconds** on the deep audit prompt. Manual fallback (search_files + terminal) was used instead. 

For next audit, consider:
- Shorter per-project prompts for JCode (15-20s context limit)
- Or split: 1 project per `jcode run` invocation with reduced scope
- Or accept manual scanning as primary method (faster, no token cost)

---

*Audit conducted: 2026-07-06 10:00 UTC by Hermes Agent via Niu-Flow bridge*
*Next scheduled: 2026-07-13*
