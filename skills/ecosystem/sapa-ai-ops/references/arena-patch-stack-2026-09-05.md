# Arena.ai Patch-Stack Adoption — 2026-09-05

Deliverable: `~/Downloads/sapa-ai-dev-2.zip` (6.3 MB, 603 files) — full `sapa-ai/` snapshot + bundled `.git` with stacked branches `pr1-fondasi-keamanan` (19 files) → `pr2-retrieval-eval` (10 files) → `pr3-ai-shadow` (22 files) on base `ada7885`, plus `review-sapa-ai/` (2 reports, eval evidence, patches `0001/0002/0003` + combined `0000`, per-PR docs, `CARA-BUKA-PR.md`).

## Study phase (no execution on the real repo)

- **Base SHA match first:** zip `main` = local HEAD = `ada7885` → patches applicable. Never copy the extracted worktree: it was checked out at the pr3 tip with sandbox artifacts (`D .claude/skills/*` deletions from lost symlinks). Use git objects (fetch branches or `git am` patches) only.
- **Verify claimed fixes by grep** in the extracted tree before trusting the cover docs: `revalidateTag(t, { expire: 0 })` (not `'max'`), `continue-on-error: true` on the CI eval job, exactly 1 active line in `.env.example` (`REVALIDATE_SECRET=`).
- **Read the evidence files:** `bukti/eval-final-*.txt` (here: 74/78 pass, rank-1 76/78, 0 regressions, 0 invariant violations over ~191 s against live SPLP) and the server log head (`bukti/server-*.log`) to confirm what the numbers were measured against.

## Applicability proof (scratch clone under /tmp only)

- Clone the local repo to `/tmp/sapa-verify` @ base SHA; `git apply --check` patches sequentially 0001→0002→0003 → exit 0 each (37 files total here).
- A patch failing alone against base but passing on-stack is expected for stacked work (here 0002 needs the CI file created by 0001) — not a defect.
- **Ignored-file collision:** a patch creating tracked `.env.example` (2805 B) fails with "already exists in working directory" when the worktree has a git-ignored one (601 B, matched by `.env*` in `.gitignore`). Fix: `cp .env.example .env.example.lokal-<date>.bak && rm .env.example` (the `.bak` stays ignored, status stays clean), apply, then diff backup vs new and keep the superior version.

## Execution (fresh integration branch)

- `git checkout -b integrasi-<source>` from the base SHA; `git am 0001 0002 0003` in order → one commit per patch (keeps per-PR reviewability), zero conflicts here.
- Branch DoD: `npm run typecheck` → OK, `npm run test` → all pass (145/145 here), `npm run build` → EXIT:0, and confirm the route table matches the cache contract (query/stream/revalidate/status = ƒ Dynamic; cached endpoints = ○ ISR).
- No push, no merge, no live-eval until the owner approves. Owner decisions left open in this session: Disdukcapil/Dinsos sign-off on per-person-data refusal, real-model shadow gates before `AI_ENABLED`, prisma dep prune (separate task), DTSEN traces in `docs/archive`.
