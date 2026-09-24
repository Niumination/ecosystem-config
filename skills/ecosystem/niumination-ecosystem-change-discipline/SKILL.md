---
name: niumination-ecosystem-change-discipline
version: 1.0.0
description: Editing Niumination files or committing to repos.
---

# Niumination Ecosystem Change Discipline

How to change files in the Niumination ecosystem without breaking repo boundaries, leaking secrets, committing another thread's work, or recording a fact that cannot be audited.

## Standing rules

- **Approval gate.** Destructive or risky actions — deleting, force-push, `git reset --hard`, mass chmod, editing a config that is currently "under repair" — only after an explicit trigger word: "gas" / "kerjakan" / "fix". "Pelajari" means study, report, wait. Write the plan first (Docs-then-Execute), then execute.
- **Verification-first.** Never claim done from memory, a transcript, or a subagent's report. Only from a command you ran yourself, with the output attached.
- **No blind `git add`.** Never use `git add -f` on anything a `.gitignore` excludes. The 16 Sep 2026 incident (an API key pushed to a public repo) came exactly from there. Secrets live in `~/.hermes/.env` or `vault/` only; repos carry `.env.example`.
- **Verify before committing, not after.** Confirm the staged list contains only your files and that other active threads' edits are still untouched. Committing a sibling thread's changes in a multi-user setup is a real, recurring failure mode.
- **Never write a derived fact you cannot trace to an artifact.** Before adding a row to a living index or ledger that records status or a score, confirm the artifact it points at exists. A row pointing at a missing folder, carrying a score, is an unauditable claim — report it and hold for the owner; do not backfill to make the registry look complete.
- **Do not touch another thread's tree.** Multiple agents edit this ecosystem concurrently. If `git status` shows modifications you did not make, leave them unstaged and uncommitted — they belong to whoever made them.
- **Skill edits land in the central bank, not the sync target.** `~/Desktop/Niumination/skills/` is the source of truth; `~/.hermes/skills/` is a sync destination. Patch the bank with the file tools, then run `skills/sync-to-agents.sh`. Writing a manual edit only to the target leaves the two trees diverged and the next sync guard will refuse.
- **Laptop is not a server.** No new cron jobs, no background daemons, nothing that assumes 24h uptime. Scheduled work is run manually on demand. This is a standing owner decision.

## Workflow

1. **Scope first.** Identify every file you intend to change and which repo each belongs to. Cross-repo work is normal here; see `references/multi-repo-boundaries.md`.
2. **Edit.** Prefer `patch` for targeted changes over `write_file`, which overwrites a whole file. On a large file you have only partially read, re-read it before any full rewrite.
3. **Cross-check anything derived.** If two or more files must describe the same content, verify mechanically rather than by eye — see `references/cross-file-consistency.md`.
4. **Pre-flight scan.** Grep the changed files for secret markers before staging: `sk-[A-Za-z0-9]{20,}`, `ghp_[A-Za-z0-9]{20,}`, `AKIA[0-9A-Z]{16}`, and bare `<KEY>=<value>` assignments. Expect zero hits. Note that a legitimate security document *mentions* forbidden patterns inside its prohibition text; confirm context before calling a hit.
5. **Commit per repo**, in separate commands, staging only your own paths. Every commit runs the ecosystem pre-commit gate (`secret-scan-staged.py`) — a silent pass is expected output.
6. **Push and verify the SHA.** Compare local and remote. When they differ, suspect the comparison first, not the push.

## Pitfalls

- **Nested repos under `apps/` are independent and ignored by the root.** `apps/` is gitignored at the root, so nothing under it ever enters the root history, and a nested `.git` does not inherit the parent's staging. A change spanning both needs two commits, in two repos, in two commands. Confirm the ignore rule first with `git check-ignore -v <path>` rather than assuming — a missing ignore entry means your nested work lands in the wrong repo silently.
- **`git ls-remote` compares false on identical trees.** Piping through `cut -d' ' -f1` leaves a trailing `\t` on the SHA, so `[ "$local" = "$remote" ]` reports divergence when both ends are byte-identical. Split and strip whitespace explicitly before comparing, then trust the result. This has produced two separate false "DIVERGED" alarms.
- **False-divergence bugs are worth one clean re-verification, not a retry loop.** Diagnose the comparison itself; the repo is almost always correct.
- **Do not `git add` in one repo expecting nested files to follow.** They will not.
- **`skill_manage` writes to the sync target, not the bank.** Use it only to create a new skill or add a new support file, then promote the result to `~/Desktop/Niumination/skills/` and re-sync. Patching the bank directly with the file tools is the correct path for edits to an existing skill.
- **`skill-manifest.py --verify-target` defaults to `structure=flat`** while the Hermes target uses the `domain` layout. Without `--structure domain` it reports over a hundred skills as missing when every file is present.

## References

- `references/multi-repo-boundaries.md` — the repo map, two-stage commit discipline, and the two-stage verification checks before pushing.
- `references/cross-file-consistency.md` — mechanically verifying that files describing the same content agree, and how to read a noisy diff.

## Bukti

- `git check-ignore -v apps/abstract-studio/...` → `.gitignore:27:apps/` — nested repos are excluded from root history.
- Dual commit sequence: root `ecosystem-config` and nested `abstract-studio` pushed as two separate commits, each verified with a whitespace-stripped SHA comparison.
- `skills/sync-to-agents.sh` → 177 skills synced; `scripts/skill-manifest.py --check` → 0 mismatch.
