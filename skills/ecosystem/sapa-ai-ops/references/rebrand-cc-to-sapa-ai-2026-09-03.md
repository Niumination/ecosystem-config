# Rebrand cc-acehtengah → sapa-ai (2026-09-03)

## Trigger
User: `periksa seluruh codebase, dan ganti semua yang di tarik dari cc-acehtengah ke sapa-ai, jangan ada lagi yang menampilkan proyek sapa-ai ini merujuk ke cc-acehtengah.`

## Sweep probe
```
grep -rln "cc-acehtengah" --exclude-dir=node_modules --exclude-dir=.next --exclude-dir=.git → 24 files
src: package.json name, globals.css theme header, status/page.tsx 2 paragraphs, report/status comments, AGENTS.md line 47
docs: 16 docs era stack lama (STATUS-CC, PRODUCTION_SETUP x2, OPENCODE_GO_*, VERCEL_ENV_SETUP, EXECUTION-PLAN-100, AGENT_BRIEF, AUDIT_AI_SISTEM, RENCANA, SESI-2026-08-29, reference/cc-acehtengah-*)
config: .vercel/project.json projectName, .env.local NEXTAUTH_URL host (gitignored)
```

## Execution (full, history-preserving)
1. Runtime: `package.json` + `package-lock.json` name → `sapa-ai` (python json rewrite), `.vercel/project.json` projectName → `sapa-ai` (needs `vercel link`), `.env.local` sed `s/cc-acehtengah.vercel.app/localhost:3000/`
2. UI/code: `globals.css` header `cc-acehtengah — Gayo Highlands` → `sapa-ai — Gayo Highlands`, `status/page.tsx` remove `versi terbatas dari cc-acehtengah` claim → `sapa-ai adalah aplikasi SAPA-only…`, report/status comments neutralized, `AGENTS.md` drift `kini bernama sapa-ai`
3. Docs: 16 docs → `git mv` to `docs/archive/cc-lineage/` + `docs/archive/README.md` (history 100% rename, not rewrite). Keep content intact for historical honesty.
4. README rewrite SPLP-only (3210 chars): tanpa prisma/auth/AI/DB, 36 tests, `npm install && npm run dev` only, route table, env vars (AI_PROVIDER/AI_MODEL optional).

## Verification
```
git grep -i cc-acehtengah -- . ':!docs/archive' ':!package-lock.json' → BERSIH
node -e require(package.json).name → sapa-ai
npx vitest run → 5 files 36 passed
npm run build → Compiled successfully in 7.9s (route table verified)
git commit 4fb93ee 25 files (+63/-55)
```

## Pitfall
- Jangan hapus deps prisma/bcryptjs/jose/next-auth + postinstall di commit sama — needs `npm install` ulang, separate task (AGENTS Known drift).
- `.vercel/` untracked — update tidak ter-commit, report `vercel link` needed.
- Sejarah docs jangan rewrite, `git mv` archive + README.
