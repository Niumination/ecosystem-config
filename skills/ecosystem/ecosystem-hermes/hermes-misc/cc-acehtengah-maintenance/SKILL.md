---
name: cc-acehtengah-maintenance
description: cc-acehtengah branch reconciliation and UI or role fixes.
category: ecosystem
---

# cc-acehtengah Maintenance

Service path: `~/Desktop/Niumination/services/cc-acehtengah` (Next.js 16 + Prisma 6 + React 19 + Tailwind).
Canonical project facts (roles, endpoints, encryption, deploy state) live in **`services/cc-acehtengah/AGENTS.md`** — read it first, this skill only carries the *workflow* and *pitfalls*.

## SACRED BRANCH RULES (from user, non-negotiable)
- `main` = FINAL, **untouched**. Do not edit.
- `hotfix/meeting-ready` = DEV branch **AND LIVE PROD** on Vercel. This is the real production code. Verify live URL + commit in `docs/STATUS-CC.md` before claiming deploy.
- `feat/ai-executive-answer-v3` (alias `v3`) = **EXPERIMENTAL / GitHub-only. NEVER deploy v3.**
- When tasked on **one** branch, do **NOT** modify the others — only *view or copy missing features* from them.
- User sometimes forgets which branch a change was made on. Before declaring work "lost", **search ALL local branches + dangling commits**:
  `git branch -a` then `git log --all --oneline -- <path>` and `git fsck --lost-found` (inspect `*.commit`/`*.tree` in `.git/lost-found`).

## Provenance: zip/snapshot vs working tree
- A zip/snapshot from the user may predate current branch state. Always diff `git status --short` + `git log --oneline -5` against the archive before saying "everything is done". Missing new files in the zip = stale snapshot.
- Treat `cc-acehtengah-v7.zip` as historical reference only; state after execution is the live branch.

## Workflow: feature missing in branch X, present in Y
The recurring task is reconciling features across branches after a merge. Proven sequence:
1. **List differing files:** `git diff --name-status <Y> <X>` (e.g. `hotfix/meeting-ready feat/ai-executive-answer-v3`).
2. **For a suspect file, dump both versions:** `git show <Y>:src/components/Foo.tsx` vs `git show <X>:src/components/Foo.tsx` (or working tree).
3. **Find symbols present in one but not the other** (catches lost functions/exports, not just line diffs):
   ```bash
   diff <(git show <Y>:src/services/ai-orchestrator.ts | grep -oE 'export (function|const|async function) [A-Za-z0-9_]+') \
        <(git show <X>:src/services/ai-orchestrator.ts | grep -oE 'export (function|const|async function) [A-Za-z0-9_]+')
   ```
4. **Read the render paths**, not just diffs — a feature can be "present" in source but unreachable because an earlier `return` short-circuits it (see Gotcha A).
5. **Verify before claiming fixed:** `npx tsc --noEmit 2>&1 | grep -iE '<File>'`, then curl the dev server (`http://127.0.0.1:3000/dashboard`) and check `.next/dev/logs/next-development.log` for compile errors. Dev server hot-reloads; a fresh request triggers recompile.

## Known gotchas (PITFALLS — check these first)
Details + exact fixes in `references/known-ui-pitfalls.md`.
- **A. Pecah Jawaban (BreakdownExplorer) invisible in v3 Executive UI.** `AIResponseRenderer` early-returns `<ExecutiveAnswerRenderer>` when `NEXT_PUBLIC_AI_EXECUTIVE_UI !== 'false'` (the default). `ExecutiveAnswerRenderer` does **NOT** render `BreakdownExplorer`. Fix: inject `<BreakdownExplorer sourceLabel={response.dataSource} />` at the top of `ExecutiveAnswerRenderer` (after the header, before the narrative).
- **B. QueryBar chips render twice.** A merge left both the v3-asli render block AND the hotfix render block for `CHIP_GROUPS` (identical maps, different styling). Fix: delete the duplicate block; keep one; add `|| !chip.query` to `disabled` (hotfix safety so empty-query chips can't be clicked).
- **C. Header buttons look like a translucent overlay.** They used hardcoded hex with low opacity (`bg-[#2D6A4F]/30`, `bg-[#B3261E]/30`) stacked on a header that is itself `bg-[var(--surface-card)]/95 backdrop-blur-md` → double-transparency. Fix: use solid theme tokens — `var(--brand-tint)` bg + `var(--brand)` text + `var(--border)` border for Online/Akun/Login; `var(--danger-tint)` bg + `var(--danger)` text + `var(--danger)` border for Logout; header bg solid `var(--surface-card)`. Grep `src/app/globals.css` for token values (light + dark `:root`).

## Role-gated BNBA access (frequent confusion point)
- To see **full BNBA identity** (nama asli + NIK terdekripsi AES-256-GCM) you MUST log in as **`dtsen_root`** (role `DTSEN_ROOT`). `master_admin` / `SUPERADMIN` see only **masked** names — by design (UU 27/2022, UU PDP).
- `ROLES_PERSONAL = ['DTSEN_LOOKUP', 'SUPERADMIN', 'DTSEN_ROOT']` — `master_admin` is **NOT** in this list, so it cannot open per-person BNBA at all (401/403 fail-closed).
- Endpoint gate: `src/app/api/dtsen/breakdown/route.ts` -> `decideDataAccess(role, 'RESTRICTED_PERSONAL')` + `canSeeFullIdentitas(role)`.
- If the user reports "BNBA still masked", first confirm they used the `dtsen_root` account, not `master_admin`. (This mistake was raised and self-corrected by the user on 2026-08-30.)

## Branch promotion: hotfix → main
- When `hotfix/meeting-ready` is clearly the intended production state and `main` is stale, promote by **fast-forwarding `main` to `hotfix/meeting-ready`** rather than merging. This avoids resolving legacy conflicts from old `main` state.
- Sequence: checkout `main`, `git reset --hard origin/hotfix/meeting-ready`, `git push origin main --force`. Verify both branches now point to the same commit with `git branch -vv`.
- Only use a true merge if you need to preserve `main`-only history. Otherwise, fast-forward is safer and cleaner for this repo.

## Vercel env / setup token workflow
- `vercel env ls` shows sensitive values as `Hidden`; it does **not** reveal the actual token.
- To retrieve a secret value, use `vercel env pull .env.local --yes --only=<NAME>`. Do **not** commit the pulled file; delete it after use.
- `.env.example` contains placeholders, not production secrets. Do not assume its `ADMIN_SETUP_TOKEN` value is valid for production setup.
- `/api/setup` will reject requests if the token/env state is not actually configured for the target environment, even if the code path looks correct.

## Golden live probe
- Use `scripts/eval-live.mjs` for production golden-query verification. It reads `data/golden-queries.json` and probes `POST /api/query` against a configurable `BASE`.
- Default `BASE` is `https://cc-acehtengah.vercel.app`. Override with `BASE=http://127.0.0.1:3000` for local checks.
- The script sleeps 7s between requests to avoid rate limits. Run from the repo root.

## Stale artifact cleanup
- If imported brief/prototype artifacts are older than the implemented codebase and cause confusion, **remove them** instead of patching docs. The live branch is the source of truth.
- Before deleting, confirm the implemented features exist in `src/` and that `vitest`/`tsc` remain green. Then commit removal with a clear message like `chore: remove stale <name> artifacts`.

## Verification before completing
- `npx tsc --noEmit` clean for touched files.
- `git status --short` shows only intended files.
- Dev server returns 200 and log shows `✓ Compiled` with no `PrismaClientValidationError` from *your* change (pre-existing EWS/SPLP 401 warnings are unrelated — note them, do not chase unless asked).
- Commit with a descriptive Indonesian message; push the **tasked branch only**.
- **Production deploy verification:** after `vercel deploy --prod`, curl `/api/health` and `/api/ews` against `https://cc-acehtengah.vercel.app`. Expect `status: "healthy"`, `warehouse: "skip"` before `POST /api/setup`, and `/api/ews` returning `{"ready":false,"error":"Forbidden — EWS membutuhkan sesi admin."}` without an admin session. Record the deployment URL + timestamp in `docs/STATUS-CC.md`.
- **Vitest reporter quirk:** `--reporter=verbose` may return truncated/missing output in this environment. Use `--reporter=dot` for reliability, then `grep` or `tail` the summary block. Full-suite pass/fail counts appear reliably in the final summary lines.
- **New test files:** vitest auto-discovers `*.test.ts`; no `vitest.config.ts` change needed when adding tests.
- **Production readiness:** `next build` must be clean before claiming deploy-ready. A green `tsc`/`vitest` is necessary but not sufficient.

## Security / PII workflow (WP0.00)
- **Pre-commit hook** is mandatory for this repo. Use `.git/hooks/pre-commit` to run both:
  - `rm -rf .next && npx tsc --noEmit` — typecheck before commit.
  - `bash scripts/pii-gate.sh .` — scan the **entire** repo tree for leaked credentials, 16-digit NIK, and real names.
- `pii-gate.sh` must exclude: `.git/`, `node_modules/`, `.next/`, `__tests__/`, `.vercel/`, `.cache/`, and itself. It should skip `.env` files.
- When redacting synthetic test data, replace real-looking NIKs with `[NIK TEST REDACTED]` everywhere: test files, golden queries, docs. Do **not** leave 16-digit numbers in test fixtures.
- Docs/vault discipline: never write literal passwords, `sk-...`, or `DTSEN_DATA_KEY` values into docs. Reference them by name only.

## DTSEN import data-quality workflow (WP0.0)
- `no_kk` is mandatory for formats that include it. If `no_kk` is missing or invalid:
  - reject the row with a clear message, OR
  - accept the row but set `keluargaId = null` and append a warning: `jumlah keluarga tidak tersedia`.
- Never use `individu:<nikHash>` as a proxy for `keluargaId`. That causes `jumlahKeluarga === jumlahJiwa` and corrupts all downstream aggregation.
- `buildAgregatWilayah` already counts `keluargaProksi`. After fixing importers, update tests so they expect `null` / warning, not proxy ids.

## Statistics regression tests (WP0.15 / WP3)
- `bapokting-viz.test.ts` only tests visualization. Add `bapokting-stats.test.ts` for engine behavior:
  - `<14` data points → `cukupData=false`, `trend='stabil'`, `persentasePerubahan=0`, with a warning.
  - empty input → `volatility.overallIndex = 0`, no crash.
  - category `hargaAvg` must be weighted by historis count, not simple average of commodity averages.
  - single-commodity input must not produce both "paling fluktuatif" and "paling stabil" recommendations.
- When passing synthetic data to typed engine functions, import the type and cast explicitly to satisfy `tsc`.
