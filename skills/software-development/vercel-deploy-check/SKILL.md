---
name: vercel-deploy-check
description: Verify a Next.js app is ready to deploy on Vercel.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Vercel, Next.js, deploy, readiness, cron, env]
    related_skills: [repo-release-hygiene, finishing-a-development-branch]
---

# Vercel Deploy Check

## When to Use

Load this skill when: asked whether an app is ready for Vercel, before the
first production deploy, or after stripping features left deploy config
(crons, env examples) pointing at dead routes and unused services.

## Checklist (all read-only until the fix step)

### 1. Cron paths must exist

A `crons` entry pointing at a missing route does NOT fail the build — Vercel
keeps executing the job and it 404s daily. Verify every path:

```bash
find src/app/api -name "route.ts" | sort
# every "path" in vercel.json crons must match one of these
```

Dead cron on an app with no warehouse/scheduler backend → delete the `crons`
block, not the route.

### 2. maxDuration fits the plan

Hobby max is 300s (per Vercel docs). `maxDuration: 60` on a query route is
fine; anything above 300 needs Pro. Check `vercel.json` functions block.

### 3. Zero-env audit (can it boot with no env at all?)

```bash
# names used in code...
grep -rhoE "process\.env\.[A-Za-z_]+" src/ | sort -u
# ...vs which are actually REQUIRED: for each name, check for
# hard failures (throw on missing, non-null assertion without fallback).
# Optional-with-fallback (Upstash→memory, base-URL defaults) is deploy-safe.
```

Also grep for `ADMIN_*_TOKEN`, `JWT_SECRET`, `DATABASE_URL`, `prisma` under
`src/app/` — any hit means the deploy needs secrets wired before it works.

### 4. .env.example drift

Template-heritage examples (DB URLs, AI keys, Qdrant, JWT on an app that uses
none) mislead whoever wires Vercel env vars. Rewrite minimal: only vars the
code actually reads, each marked required-or-optional with its fallback.
Note: `.env.example` is often git-ignored — confirm whether it is tracked
before claiming the fix is committed.

### 5. Gate before claiming ready

`npm run build` (must compile) + test suite + `git status` clean apart from
known scratch files. Then push state: `git log origin/main..main`.

## Fix pattern (needs normal file-edit approval)

- Delete dead `crons` block, keep `maxDuration`.
- Rewrite `.env.example` minimal; delete provably-unreferenced dead modules
  (0 `grep` hits) that the example implies are live.
- Re-run build + tests after deletions, then commit.
