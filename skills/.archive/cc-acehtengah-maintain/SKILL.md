---
name: cc-acehtengah-maintain
description: Merge hotfix into v3, catch silent merge bugs.
---

# cc-acehtengah Repo Maintenance

Repo: `~/Desktop/Niumination/services/cc-acehtengah` (Next.js 16, Prisma, Turbopack).
Multi-branch experimental workflow. User (Afrizal Munthe, Diskominfo Aceh Tengah) develops features on `feat/ai-executive-answer-v3` and periodically merges `hotfix/meeting-ready` (the LIVE PROD branch) into it.

## Branch roles (HARD — from user)
- `main` = FINAL (untouched)
- `hotfix/meeting-ready` = DEV + LIVE PROD Vercel (do NOT deploy v3 to PROD unless explicitly told)
- `feat/ai-executive-answer-v3` = EXPERIMENTAL / GitHub-only (NEVER deploy to PROD)
- `backup/feat-v3-saved` = safety snapshot of v3
- `feat/ai-executive-answer-v2-live` = older parallel branch (subset of v3, NOT a parent)

**Discipline:** when working on ONE branch (e.g. v3), do NOT modify other branches. You MAY `git show <other>:<path>` / `git diff` to view or `git checkout <other> -- <file>` to COPY a file in — but never commit to or push another branch. If a feature "was on another branch", copy it into the active branch; don't edit the other branch.

## Merge workflow (hotfix → v3)
1. `git checkout feat/ai-executive-answer-v3 && git merge hotfix/meeting-ready`
2. Resolve the 11 known conflict files by reading both sides; prefer keeping v3's structure unless hotfix carries a security/correctness fix.
3. **After merge, run the silent-bug scan below BEFORE building.**

## Silent merge bugs (no conflict shown — must scan manually)
These do NOT appear as `<<<<<<<` conflict markers. Always scan after every merge.

### Bug A — `.bak` rename detection kills API routes
If hotfix stores a route as `route.ts.bak` (intentional disable) and v3 has `route.ts`, git's similarity detection reports `R100  route.ts -> route.ts.bak` (100% rename). Result: the live `route.ts` is DELETED and only `.bak` remains → endpoint 404s silently.
- **Detect:** `git diff --name-status <v3-base> <merge-head> | grep -E "^[DR]"` and look for `.bak` targets or `D` deletions.
- **Fix:** `git mv src/app/api/X/route.ts.bak src/app/api/X/route.ts` for each; verify `diff <(git show <v3-base>:path) path` is identical (hotfix only renamed, didn't change content). Then `git checkout <v3-base> -- scripts/seed.ts` for any `D`eleted file.
- **Verify no `.bak` left:** `find src/app/api -name "*.bak"` must be empty.

### Bug B — duplicated JSX / double render
If both branches edited the same JSX block with DIFFERENT structure (not a clean conflict), git concatenates both versions → element renders twice (e.g. chips appear double).
- **Detect:** `grep -c "CHIP_GROUPS.map"` on the component; >1 means duplicated. Also eyeball the merged section for two `CHIP_GROUPS.map` blocks.
- **Fix:** delete the duplicate block; keep ONE render. When merging best-of-both, preserve the active branch's theme vars (e.g. `var(--brand-tint)`) and port only the missing safety/UX from the other block (e.g. `disabled || !chip.query` so empty-query chips can't be clicked).

## Verification (zero-tolerance — user requires "jangan ada kesalahan")
1. `npx tsc --noEmit` — note: build uses `ignoreBuildErrors`, so tsc errors about missing Prisma models (e.g. `prisma.dataset`) do NOT fail the build but WILL 500 at runtime. Treat them as known preexisting, not merge regressions.
2. `npx next build` — must say "✓ Compiled successfully".
3. **Localhost repro:** a `next dev` server may already be running on :3000 (user's). Check with `curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:3000/<route>` BEFORE starting a new one (starting :3939 fails if :3000 is occupied). Test: page route, the API JSON, and the endpoint you just fixed.
4. Only claim "fixed / not missing" after build + at least one live curl returns 200.

## "Missing feature after merge" investigation pattern
User often reports a feature "hilang" — usually it is NOT deleted. Sequence:
1. `git diff --stat <v3-base> <merge-head> -- <feature-path>` — empty diff = file unchanged by merge.
2. `git ls-tree -r --name-only <branch> -- <path>` across ALL branches to find where the feature actually lives (v3/backup usually own `OpdDrilldown.tsx`, `TopOpdWidget.tsx`; v2-live does NOT).
3. `git log --all --oneline -- <file>` to trace history; `git fsck --lost-found` / `git stash list` for uncommitted work that may have been lost.
4. Repro live (build + curl) — a feature can be "missing" only because the user opened the page without the required query param (e.g. `/dashboard/analytics` shows summary; drill-down needs `?opd=<nama>` from the Top OPD widget on the beranda).
5. `git diff --name-only <other-branch> <active> | grep -E "src/.*\.(ts|tsx)$"` then symbol-diff per file to find hotfix-only functions. Usually v3 is a SUPERSET; the only hotfix-only symbols are tergantikan (e.g. `integrateDtsenData` replaced by `dtsen-multisource.ts`) or 1-line minors (`health/route.ts` `allOk`).

## User workflow preferences (embedded)
- **Stop discipline:** if user says stop / "istirahat" / "jika ragu bertanya atau berhenti", HALT all edits immediately and revert any uncommitted working-tree change (`git checkout -- <file>`). Do not continue modifying.
- **Confirm before broad changes:** for repo-wide or branch-affecting ops, report the plan + ask, don't assume.
- **Teliti:** verify with build + repro before declaring done; never claim "fixed" on a hunch.
