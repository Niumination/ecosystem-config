# sapa-ai Refactor Session Notes — 2026-09-02

## Context
Refactoring `services/sapa-ai` from full duplicate of `cc-acehtengah` hotfix to SAPA-only public app while preserving UI.

## Key Lessons Learned

### 1. User Preference: Preserve UI, Not Stub It
- **Wrong:** Deleting route folders and components → breaks navigation and empty states
- **Right:** Keep folders/components, stub only the data source endpoints
- User explicitly rejected "placeholder/tidak tersedia" approach
- User wants: "semua yang tampil itu hanya sumber sapa"

### 2. Auth Gating Without Page Modification
- **Technique:** Stub auth endpoints (`/api/auth/me`, `/api/auth/login`, etc.) to return public-authenticated responses
- **Benefit:** Pages that check auth become accessible without modifying their code
- **Pattern:**
  ```typescript
  export async function GET() {
    return NextResponse.json({ authenticated: true, admin: { username: 'Publik', role: 'public' } });
  }
  ```

### 3. Patch Safely, Don't Bulk Replace
- **Problem:** Bulk string replacement across multiple files caused syntax errors
- **Solution:** 
  - Always `git checkout -- <file>` to restore original
  - Use targeted patch with unique anchors
  - Verify patch landed correctly before building
  - Inspect each file individually

### 4. Dashboard Runtime Error: Undefined Data
- **Error:** `Uncaught TypeError: can't access property Symbol.iterator, data.opds is undefined`
- **Fix:** Guard array spreads with `?? []`:
  ```typescript
  const sortedOpds = [...(data.opds ?? [])].sort(...)
  const top10 = [...(data.topIndicators ?? [])].slice(...)
  ```
- **Lesson:** When replacing data sources, always audit components that consume the data shape

### 5. Git Push Without GitHub Credentials
- **Problem:** GitHub PAT in vault was invalid/expired
- **Solution:** Create local mirror remote (`latest`) pointing to `~/downloads-extracted/sapa-ai-latest`
- **Pattern:**
  ```bash
  mkdir -p ~/downloads-extracted/sapa-ai-latest
  cd ~/downloads-extracted/sapa-ai-latest
  git init && git config receive.denyCurrentBranch ignore
  cd /path/to/working-repo
  git remote add latest ~/downloads-extracted/sapa-ai-latest
  git push latest main
  ```

### 6. Sidebar/Chip Cleanup
- **Goal:** Remove non-SAPA chips from UI without breaking sidebar structure
- **Technique:** String replacement of menu labels and auth buttons, keep navigation structure intact
- **Verification:** `grep -rlnE "login|auth|admin|akun" src/components/Sidebar.tsx`

### 7. User Communication Style
- User gets frustrated when agent jumps to execution instead of planning
- Always propose plan first, get confirmation, then execute
- When user says "duplikat", literally duplicate first, don't modify
- When user corrects, acknowledge the mistake clearly and restart from correct state

## Files Changed This Session
- `src/lib/sapa-client.ts` — SPLP-only fetch, preserved interfaces
- `src/app/api/query/route.ts` — Simplified to SAPA-only
- `src/app/api/health/route.ts` — Removed warehouse/auth checks
- `src/components/SapaStats.tsx` — Guarded undefined data arrays
- `src/app/dashboard/layout.tsx` — Removed auth UI, kept navigation
- `src/app/api/kpi/route.ts` — Stub endpoint
- `src/app/api/ews/route.ts` — Stub endpoint
- `src/app/api/stats/route.ts` — Stub endpoint
- `src/app/api/analytics/route.ts` — Stub endpoint
- `src/app/api/geodata/route.ts` — Stub endpoint
- `src/app/api/auth/me/route.ts` — Stub public-auth endpoint
- `src/app/api/auth/login/route.ts` — Stub login endpoint
- `src/app/api/auth/logout/route.ts` — Stub logout endpoint
- `src/app/api/auth/change-password/route.ts` — Stub change-password endpoint
- `src/app/dashboard/status/page.tsx` — Removed auth redirects
- `src/app/dashboard/laporan/page.tsx` — Removed auth redirects
- `src/app/dashboard/admin/dtsen/page.tsx` — Removed auth redirects
- `src/components/Sidebar.tsx` — Removed login/akun menu items
