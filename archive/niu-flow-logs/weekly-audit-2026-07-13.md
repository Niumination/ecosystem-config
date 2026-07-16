# Weekly Code Audit — 2026-07-13

## Summary
- **Projects scanned:** 3 (PemdiAcehTengah, niu-vermilion, kune-ya.com)
- **🔴 Critical:** 6 findings (3 new from JCode, 3 carried forward)
- **🟡 High:** 8 findings (4 new from JCode, 4 carried forward)
- **⚪ Info:** 9 findings (3 new from JCode, 6 carried forward)
- **Methodology:** JCode deep audit via Niu-Flow bridge + manual verification

**Changes since last audit (2026-07-06):** ZERO commits across all 3 projects. No changes to any codebase. All last week's stale issues still present. JCode deep audit found **6 new critical/high issues** that manual scanning missed last week.

## Live URL Status

| Project | URL | Status | Change |
|---------|-----|--------|--------|
| PemdiAcehTengah | https://pemdi-aceh-tengah.vercel.app | ✅ HTTP 200 | Unchanged |
| niu-vermilion | https://niu-vermilion.vercel.app | ✅ HTTP 307 → /dashboard | Unchanged |
| kune-ya.com | https://kune-ya.com | ❌ **HTTP 000 (NXDOMAIN)** | **Same as last week — STILL DOWN** |
| kune-ya.com | https://kune-ya-com.vercel.app | ✅ HTTP 200 (Vercel preview) | Working |

## Git Status

| Project | Remote | Last Commit | Status | Changes Since Last Week |
|---------|--------|-------------|--------|-------------------------|
| PemdiAcehTengah | git@github.com:niumination/PemdiAcehTengah.git (SSH ✅) | `d480fc8` — update BACKLOG.md + sitemap | ✅ Clean | **NONE** |
| niu-vermilion | git@github.com:Niumination/Niu-Vermilion.git (SSH ✅) | `6f2f036` — mv: niu-vermilion → Production/ | ✅ Clean | **NONE** |
| kune-ya.com | git@github.com:Niumination/kune-ya.com.git (SSH ✅) | `52f432e` — mv: kune-ya.com → Production/ | ✅ Clean | **NONE** |

---

## Per-Project Breakdown

---

### 1. PemdiAcehTengah (Government Portal)

**Stack:** Next.js 14.2.35, React 18.3.1, Supabase, Pages Router
**Files scanned:** 131 source files
**Deploy:** ✅ Vercel live (HTTP 200)
**JCode session:** `session_fox_1783909187399_f40443114f724065`
**JCode tokens:** 60,663 input / 1,030 output

#### 🔴 NEW CRITICAL FINDINGS (JCode)

| # | Finding | Location | Description |
|---|---------|----------|-------------|
| **1** | **🔴 XSS in sanitize.js — event handlers pass through** | `lib/sanitize.js:24-31` | When `<a>` has no `href` (or relative `/` / `#` href), the **entire original tag** including event handlers (`onclick`, `onerror`, `onfocus`) is returned unchanged. `<a onclick="alert(document.cookie)">click</a>` passes through intact. Exploitable via `faq.js:83` and `tanya.js:125` which use `dangerouslySetInnerHTML`. Compare with `lib/safeRichText.js:23` which correctly strips `on\w+` handlers. |
| **2** | **🔴 Vercel OIDC token hardcoded in `.env.local`** | `.env.local:2` | `VERCEL_OIDC_TOKEN=eyJhb...` — live JWT for workload identity federation. Can be used to access cloud resources that trust Vercel OIDC. Should only exist in Vercel's env dashboard, never in a file. |
| **3** | **🔴 Rate limiting completely bypassed in serverless** | `lib/security.js:16-22` | In-memory `Map`-based `rateLimit()`. Every Vercel serverless invocation has its own fresh memory — counters reset on each cold start. Attacker can fire unlimited POST requests to `/api/lapor`, `/api/skm`, `/api/feedback`. No Turnstile implementation despite `AGENTS.md` claiming it exists. |

#### 🟡 NEW HIGH FINDINGS (JCode)

| # | Finding | Location | Description |
|---|---------|----------|-------------|
| **4** | **🟡 Admin Bearer token stored in `sessionStorage`** | `pages/admin.js:50,98` | Admin token stored in `sessionStorage` and sent as `Authorization: Bearer` on every API call. Any XSS (see #1) can exfiltrate the token. No CSRF protection on PATCH `/api/lapor`. |
| **5** | **🟡 Brute-force protection relies on broken rate-limit** | `lib/adminAuth.js:19` | Admin brute-force protection depends on `rateLimit()` which is non-functional in serverless (#3). No account lockout mechanism. |
| **6** | **🟡 No CSRF on mutation endpoints; missing Turnstile** | `pages/api/*.js` | Mutation endpoints lack CSRF tokens. Turnstile not implemented despite documentation. |

#### 🟡 CARRY OVER FROM LAST WEEK

| # | Finding | Location | Status |
|---|---------|----------|--------|
| 7 | dangerouslySetInnerHTML on user content (faq.js:83) | `pages/faq.js:83` | Still present |
| 8 | dangerouslySetInnerHTML on user content (tanya.js:125) | `pages/tanya.js:125` | Still present |
| 9 | No middleware.ts for edge-level security | — | Still missing |
| 10 | Next.js 14.2.35 → 16.2.10 (2 majors behind) | `package.json` | Still outdated |
| 11 | React 18.3.1 → 19.2.7 (1 major behind) | `package.json` | Still outdated |
| 12 | eslint 8.57.1 → 10.7.0 (2 majors behind) | `package.json` | Still outdated |

#### ⚪ INFO (Carry Over)

| # | Finding | Status |
|---|---------|--------|
| 1 | Security headers via next.config (CSP with 'unsafe-inline') | Still present |
| 2 | Admin auth uses Bearer token | Still present |
| 3 | API security basics present (CORS, sanitizeText) | Still present |
| 4 | Supabase dep minor update available (2.108.1 → 2.110.2) | Still outdated |
| 5 | Git history has no leaked secrets ✅ | Confirmed clean |
| 6 | Admin page protected with noindex | Still present |

---

### 2. niu-vermilion (Second Brain)

**Stack:** Next.js 16.2.7, React 19.2.4, Supabase, TipTap v3, iron-session
**Files scanned:** 205 source files in src/
**Deploy:** ✅ Vercel live (HTTP 307 → /dashboard)
**JCode session:** `session_tigress_1783909409504_5275195a2369adb3`
**JCode tokens:** 54,223 input / 1,211 output

#### 🔴 NEW CRITICAL FINDINGS (JCode)

| # | Finding | Location | Description |
|---|---------|----------|-------------|
| **1** | **🔴 Session cookie never set on login — auth broken** | `src/app/api/auth/route.ts:32,55` | Line 32 creates `const response = NextResponse.json({ success: true })` and passes it to `getIronSession()` which attaches the session cookie to it. But line 55 returns `NextResponse.json({ success: true })` — a **new** response without the cookie. Login returns HTTP 200 but the browser never receives the `Set-Cookie` header → every subsequent API call returns 401. Compare with DELETE handler (line 92-101) which correctly returns the same `response` object. **Fix: change line 55 to `return response;`** |
| **2** | **🔴 Timing-vulnerable password comparison** | `src/app/api/auth/route.ts:40` | `body.password === process.env.ADMIN_PASSWORD` — JavaScript `===` short-circuits on first mismatched character, leaking character-by-character timing differentials. While rate limiting mitigates brute force, a network-local attacker could enumerate the password (~52k requests for 32-char hex). Fix: use `crypto.timingSafeEqual()` after normalizing both strings to same length. |

#### 🟡 NEW HIGH FINDINGS (JCode)

| # | Finding | Location | Description |
|---|---------|----------|-------------|
| **3** | **🟡 No middleware — dashboard pages publicly served** | `src/middleware.ts` (missing) | No Next.js middleware to gate `/dashboard/*` pages. Dashboard page shells (HTML, JS bundles, component structure) are served to anyone, including unauthenticated users. Dashboard layout and all client components are publicly accessible. |
| **4** | **🟡 Rate limiter ineffective on Vercel serverless** | `src/lib/rate-limit.ts:3-5` | File's own comment acknowledges: "On Vercel serverless, memory resets per warm invocation". In-memory Map provides no protection across serverless invocations. Fix: use Upstash Ratelimit or database-backed rate limiter. |

#### ⚪ INFO (New)

| # | Finding | Location | Description |
|---|---------|----------|-------------|
| 5 | ⚪ innerHTML on image error fallback (static string) | `BookmarksClient.tsx:346` | Static SVG string — no user input. Not exploitable but anti-pattern. |

#### ⚪ CARRY OVER FROM LAST WEEK

| # | Finding | Status |
|---|---------|--------|
| 6 | Minor dependency updates: tiptap 3.26.0→3.27.3, tailwindcss 4.3.0→4.3.2, supabase-js 2.108.0→2.110.2, lucide-react 1.17.0→1.23.0 | Still outdated |
| 7 | Clean security posture — no hardcoded secrets, no eval(), no SQL injection ✅ | Confirmed |
| 8 | Supabase config.toml uses `env(VAR_NAME)` pattern properly ✅ | Confirmed |

---

### 3. kune-ya.com (Full Website)

**Stack:** Next.js 15.5.19, React 19.1.0, Prisma 6.19.3, next-auth 5.0.0-beta.31, OpenAI SDK
**Files scanned:** 47 source files in app/
**Deploy:** ❌ Custom domain DOWN (NXDOMAIN — same as last week), ✅ Vercel preview works
**JCode session:** `session_goat_1783909548781_0cce87bf60e29f3e`
**JCode tokens:** 34,136 input / 1,361 output

#### 🔴 NEW CRITICAL FINDINGS (JCode)

| # | Finding | Location | Description |
|---|---------|----------|-------------|
| **1** | **🔴 Weak/Predictable AUTH_SECRET in `.env`** | `.env:3` | `AUTH_SECRET="kune-y...c123"` — low-entropy, predictable secret. If this same value is used in Vercel production env vars, an attacker can forge arbitrary JWT session tokens, impersonate any user including admins, and gain full API access. **Must be a cryptographically random 64-char base64 string** (`openssl rand -base64 64`). |

#### 🟡 NEW HIGH FINDINGS (JCode)

| # | Finding | Location | Description |
|---|---------|----------|-------------|
| **2** | **🟡 GET `/api/analytics` leaks page view data — zero auth** | `app/api/analytics/route.ts:19-21` | No auth check despite comment "admin only for full stats" (line 18). Anyone can call GET and see `totalViews`, `totalPages`, `topPages` — enumerating site structure. POST (line 5-15) also unauthenticated — anyone can pollute analytics data. |
| **3** | **🟡 Rate limiting never applies to login endpoint** | `middleware.ts:28-30` | Middleware checks for `/api/auth/login` and `/api/auth/register` for stricter 10/min rate limit. But next-auth's credential login handler lives at `/api/auth/callback/credentials` — **never matched**. Login attempts fall through to the generic 60/min limit instead of the intended 10/min. |

#### ⚪ NEW FINDINGS (JCode)

| # | Finding | Location | Description |
|---|---------|----------|-------------|
| 4 | ⚪ User enumeration via `/[username]` page | `app/[username]/page.tsx:14-25,47` | Returns 200 vs 404 to distinguish existing vs non-existing usernames. Admin role badge (`"Administrator"` vs `"Pengguna"`) at line 47 enables privilege-target attacks. |
| 5 | ⚪ Live OpenAI API key still on disk, NOT rotated | `.env:4` | Same key as last week (`sk-CN2...EFgA`). `.env` file has **644 permissions** (world-readable). Not git-tracked but exposed on disk. |
| 6 | ⚪ `.env` file permissions 644 (world-readable) | `.env` | File is readable by any user on the system. Should be 600. |

#### 🔴 CARRY OVER FROM LAST WEEK (UNRESOLVED)

| # | Finding | Location | Status |
|---|---------|----------|--------|
| **7** | **🔴 Custom domain DNS NXDOMAIN** | DNS check | **STILL DOWN since last week.** Website inaccessible to users for 7+ days. |
| **8** | **🔴 .env file on disk with live API key** | `.env:4` | Still present. Key NOT rotated despite last week's recommendation. |
| **9** | **🔴 next-auth v5 beta in production** | `package.json` | Still at `5.0.0-beta.31` — beta auth library in production. |

#### 🟡 CARRY OVER FROM LAST WEEK

| # | Finding | Status |
|---|---------|--------|
| 10 | Prisma 6.19.3 → 7.8.0 (1 major behind) | Still outdated |
| 11 | Next.js 15.5.19 → 16.2.10 (1 major behind) | Still outdated |
| 12 | pdf-parse 1.1.1 → 2.4.5 (legacy version) | Still outdated |

#### ⚪ CARRY OVER FROM LAST WEEK

| # | Finding | Status |
|---|---------|--------|
| 13 | Strong middleware security (CSP, rate limiting) ✅ | Still present |
| 14 | API routes properly authenticated with `auth()` ✅ | Still present |
| 15 | dangerouslySetInnerHTML in layout.tsx (static theme script) | Still present |
| 16 | No hardcoded secrets in git history ✅ | Confirmed |
| 17 | Minor updates: openai 6.42.0→6.46.0, tailwindcss 4.3.0→4.3.2 | Still outdated |

---

## JCode Session Summary

| Project | Session ID | Input Tokens | Output Tokens | Status |
|---------|------------|:------------:|:-------------:|--------|
| PemdiAcehTengah | `session_fox_1783909187399` | 60,663 | 1,030 | ✅ Success |
| niu-vermilion | `session_tigress_1783909409504` | 54,223 | 1,211 | ✅ Success |
| kune-ya.com | `session_goat_1783909548781` | 34,136 | 1,361 | ✅ Success |
| **Total** | | **149,022** | **3,602** | |

**Note:** JCode v0.31.2 worked successfully this week (last week it timed out at 300s). Shorter focused prompts per project resolved the timeout issue.

---

## Scoreboard

| Project | 🔴 Critical (New) | 🔴 Critical (Carry) | 🟡 High (New) | 🟡 High (Carry) | ⚪ Info | Health |
|---------|:-----------------:|:-------------------:|:-------------:|:----------------:|:-------:|--------|
| PemdiAcehTengah | 3 | 0 | 3 | 5 | 6 | 🟡 Fair → 🔴 **Needs Attention** |
| niu-vermilion | 2 | 0 | 2 | 0 | 2 | 🟢 Good → 🟡 **Fair** |
| kune-ya.com | 1 | 3 | 2 | 3 | 6 | 🔴 **Needs Attention** |

---

## Recommendations — Top Priority This Week

### 🚨 Fix IMMEDIATELY (This Week)

1. **🔴 [PemdiAcehTengah] Fix XSS in `sanitize.js`** — Replace `sanitize.js` with `safeRichText.js` (which already correctly strips `on\w+` handlers) or add regex to strip event handler attributes from returned tags. This is an active XSS vector.

2. **🔴 [PemdiAcehTengah] Remove Vercel OIDC token from `.env.local`** — Delete `.env.local` from disk and rotate the OIDC token in the Vercel dashboard. This is a workload identity credential.

3. **🔴 [niu-vermilion] Fix login session cookie bug** — Change line 55 of `src/app/api/auth/route.ts` from `return NextResponse.json({ success: true })` to `return response;` so the session cookie is actually sent to the client. Currently login is effectively broken.

4. **🔴 [kune-ya.com] Fix DNS/domain — 7+ days down** — `kune-ya.com` has been inaccessible for a full week. Check domain registration, re-add custom domain in Vercel, verify DNS records.

### 🟡 Address This Month

5. **🟡 [kune-ya.com] Rotate all secrets** — Rotate `OPENAI_API_KEY` and `AUTH_SECRET` immediately. Set `.env` permissions to 600. Use Vercel environment variables instead of `.env` file on disk.

6. **🟡 [niu-vermilion] Add middleware** — Create `src/middleware.ts` to gate `/dashboard/*` pages with session check. Add `crypto.timingSafeEqual()` for password comparison.

7. **🟡 [kune-ya.com] Fix rate limit path for login** — Change middleware path check from `/api/auth/login` to `/api/auth/callback/credentials` (or add both patterns) so login attempts get the intended 10/min rate limit.

8. **🟡 [PemdiAcehTengah] Implement real rate limiting** — Switch from in-memory Map to Vercel KV, Upstash, or at minimum implement Turnstile for post endpoints.

### ⚪ Monitor

9. **⚪ [kune-ya.com] Add auth to analytics GET endpoint** — Add session check to `/api/analytics`.

10. **⚪ [All] Apply dependency updates** — npm update across all projects for minor/patch releases.

11. **⚪ [niu-vermilion] Fix timing-safe password comparison** — Use `crypto.timingSafeEqual()` in auth route.

---

## Audit Notes

- **`kune-ya.com` remains inaccessible at its custom domain for 7+ days.** The Vercel preview URL works. This is the most impactful issue — users cannot access the live website.
- **No code changes in any project since last audit.** All last week's findings are still present, plus 6 new critical/high issues discovered by JCode deep audit.
- **JCode proved its value this week** — the 3 new criticals in PemdiAcehTengah (XSS, OIDC leak, rate-limit bypass) and 2 new criticals in niu-vermilion (session cookie bug, timing attack) were not caught by last week's manual scanning. JCode's ability to read every file and trace execution paths is a genuine differentiator.
- **The `.env.local` file on PemdiAcehTengah** and the **`.env` file on kune-ya.com** both contain live credentials. Neither is git-tracked (✅), but both exist on disk with permissive permissions (644).

---

*Audit conducted: 2026-07-13 by Hermes Agent via Niu-Flow bridge (JCode deep audit + manual verification)*
*Next scheduled: 2026-07-20*
