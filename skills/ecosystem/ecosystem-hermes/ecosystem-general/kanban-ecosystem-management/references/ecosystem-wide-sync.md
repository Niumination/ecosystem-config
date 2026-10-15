# Ecosystem-Wide Documentation Sync

## When User Says "update semua dokumentasi" / "kerjakan sesuai rekomendasi"

Execute ALL items in one pass — do not ask individually.

## Sync Checklist

| # | Target | What to update |
|---|--------|---------------|
| 1 | `BACKLOG.md` (root) | Audit counts, project table, scoreboard, activity tracking, footer timestamp |
| 2 | `AGENTS.md` (root) | Directory tree, project catalog table, priority sections, footer |
| 3 | Project `AGENTS.md` | Status, HEAD commit, stack info, deployed URL |
| 4 | Hermes `memory` | Ecosystem counts, most-active projects, path changes |
| 5 | `brain/` vault | Daily note in `brain/inbox/ecosystem-update-YYYY-MM-DD.md` |
| 6 | Dirty repos | `git add -A && commit + push` for each |
| 7 | Final verification | Scan all repos for remaining dirty state |

## Execution Order

```
1. GATHER: scan all repos (git status, git log --oneline -N, last commit dates)
2. UPDATE DOCS: BACKLOG.md → AGENTS.md (root) → project AGENTS.md → memory → brain
3. COMMIT: dirty repos one by one, push each
4. VERIFY: re-scan, report summary
```

## Commit Messages
```
chore: update BACKLOG.md & AGENTS.md — sync real filesystem state <date>
chore: batch daily notes <date range> + ecosystem changelog
```

## Pitfalls

- **HTTPS remote after force push**: Root Niumination repo may have HTTPS remote that fails auth. Fix: `git remote set-url origin git@github.com:Niumination/Niumination.git`
- **Shell CWD lost after rm -rf**: Always `cd` to safe root before deleting directories
- **Prisma table not found (Supabase)**: If ChatSession or similar table doesn't exist in Supabase, the API route should return empty results gracefully (not 500). Provide SQL migration file for user to run manually in Supabase SQL Editor.
- **Auto-migration via prisma.$executeRawUnsafe may fail**: Supabase free tier or limited DB users may not have CREATE TABLE permission. Always have a manual SQL fallback.
