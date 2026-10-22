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
- **A probe must exercise the thing the row claims.** "Artifact exists" and "artifact was tested" are different facts, and a green status recorded from the wrong probe is worse than no row: it is retracted later, in public, by whoever finds it. Before writing `LIVE` / `verified` / a route count, confirm the response came from the real surface — check the response *body*, not just its status code, and re-read what you actually hit. When you do discover a status was recorded from a false green, fix the sentence in place and say so in the reply; do not quietly overwrite it.
- **Do not touch another thread's tree.** Multiple agents edit this ecosystem concurrently. If `git status` shows modifications you did not make, leave them unstaged and uncommitted — they belong to whoever made them.
- **Skill edits land in the central bank, not the sync target.** `~/Desktop/Niumination/skills/` is the source of truth; `~/.hermes/skills/` is a sync destination. Patch the bank with the file tools, then run `skills/sync-to-agents.sh`. Writing a manual edit only to the target leaves the two trees diverged and the next sync guard will refuse.
- **Laptop is not a server.** No new cron jobs, no background daemons, nothing that assumes 24h uptime. Scheduled work is run manually on demand. This is a standing owner decision.

## Workflow

1. **Scope first.** Identify every file you intend to change and which repo each belongs to. Cross-repo work is normal here; see `references/multi-repo-boundaries.md`.
2. **Edit.** Prefer `patch` for targeted changes over `write_file`, which overwrites a whole file. On a large file you have only partially read, re-read it before any full rewrite.
3. **Cross-check anything derived.** If two or more files must describe the same content, verify mechanically rather than by eye — see `references/cross-file-consistency.md`.
4. **Pre-flight scan.** Grep the changed files for secret markers before staging: `sk-[A-Za-z0-9]{20,}`, `ghp_[A-Za-z0-9]{20,}`, `AKIA[0-9A-Z]{16}`, and bare `<KEY>=<value>` assignments. Expect zero hits. Note that a legitimate security document *mentions* forbidden patterns inside its prohibition text; confirm context before calling a hit.
5. **Commit per repo**, in separate commands, staging only your own paths. Every commit runs the ecosystem pre-commit gate (`.githooks/pre-commit`) — a silent pass is expected output. It runs four checks: `secret-scan-staged.py`, `scan-stray-glyphs.py`, `scan-env-writers.py --staged`, and `skill-manifest.py --check`. Read the hook when a commit is refused; the failure line names which gate fired.
6. **Push and verify the SHA.** Compare local and remote. When they differ, suspect the comparison first, not the push.

## Pitfalls

- **A stop command means stop probing, not "finish the thought."** When the user interrupts
  with "stop", "berhenti", or "cukup" mid-diagnosis, the correct response is to halt and report
  what is already established — not to run one more probe so the answer is complete. A user who
  has solved the problem themselves is telling you the investigation is over; continuing to
  gather evidence reads as ignoring them and costs trust even when the finding would have been
  right. State the confirmed cause, name anything still unknown as `UNCHECKED`, and stop.
- **Never blame the user's own action for a failure you cannot trace to it.** When a tool fails and
  the user has just changed something nearby (quit an app, toggled a service), the tempting
  explanation is causation — and it is often wrong. Establish the mechanism before naming a
  cause: check what actually owns the resource, not what changed most recently. Report the
  mechanism you proved and the alternative you ruled out; a confident wrong cause sends the next
  session chasing the wrong component.
- **Diagnose resource contention by what holds it, not by what the port reports.** A "port already
  in use" error can come from a socket that no process owns: `lsof -iTCP:<port>` and `netstat -anv`
  may disagree, and `netstat` names the real holder in its owner column. Cross-read both, then
  bind-test the port yourself (`socket.bind`) — a successful bind proves it free and overrules
  both tools. Never conclude "port free" from `lsof` returning nothing when `netstat` shows a
  `LISTEN` row.
- **A random port is a shared resource: two independent services can both pick it.** A service
  that picks its own ephemeral port can collide with another service doing the same, and the
  collision is intermittent by construction. When a failure looks like bad luck on a port, check
  whether the OS ephemeral range is the common cause and whether the service can be pinned to a
  fixed port instead.
- **Nested repos under `apps/`, `sites/`, and the other v4.0 top dirs are independent and ignored by the root.** `apps/` is gitignored at the root, so nothing under it ever enters the root history, and a nested `.git` does not inherit the parent's staging. A change spanning both needs two commits, in two repos, in two commands. Confirm the ignore rule first with `git check-ignore -v <path>` rather than assuming — a missing ignore entry means your nested work lands in the wrong repo silently.
- **`git ls-remote` compares false on identical trees.** Piping through `cut -d' ' -f1` leaves a trailing `\t` on the SHA, so `[ "$local" = "$remote" ]` reports divergence when both ends are byte-identical. Split and strip whitespace explicitly before comparing, then trust the result. This has produced two separate false "DIVERGED" alarms.
- **False-divergence bugs are worth one clean re-verification, not a retry loop.** Diagnose the comparison itself; the repo is almost always correct.
- **Do not `git add` in one repo expecting nested files to follow.** They will not.
- **`skill_manage` writes to the sync target, not the bank.** Use it only to create a new skill or add a new support file, then promote the result to `~/Desktop/Niumination/skills/` and re-sync. Patching the bank directly with the file tools is the correct path for edits to an existing skill.
- **`skill-manifest.py --verify-target` defaults to `structure=flat`** while the Hermes target uses the `domain` layout. Without `--structure domain` it reports over a hundred skills as missing when every file is present.
- **A heredoc commit message can silently truncate into foreign prose.** A multi-line `git commit -F - <<'EOF'` came back as one enormous message containing CJK text and a leftover tool-call fragment, then `git commit --amend -F /tmp/msg.txt` failed with "cannot read file" because the `write_file` that produced it had been corrupted the same way. The commit landed but with a wrecked message. Recovery: check `git log -1 --format='%B'`, confirm the *files* are clean separately (`git show --stat`), then amend from a message file whose content you have re-read. When a commit message matters more than a one-liner, write it to a file, re-read that file, and only then commit — never trust that a long inline heredoc survived.
- **The manifest gate compares the manifest to the working tree, not to the staged set — so regenerate it, do not stage it.** `skill-manifest.py --check` hashes what is on disk now, so running the generator clears the gate even when `skills/manifest.json` is left unstaged. That is the escape from a real trap: the manifest covers the *whole* bank, so staging it to satisfy the gate would commit sibling threads' skill drift as a side effect. Regenerate locally, confirm `0 mismatch`, then `git add` only your own paths and leave the manifest modified in the working tree for whoever owns the other changes. Verify the manifest's own diff is bank-wide before deciding — compare the `skills` keys against `git show HEAD:skills/manifest.json`, not just the line count.
- **A derived artifact shared by every thread cannot be committed by one thread.** When `git status` shows a generated file modified but your change touched only two members, the diff will contain other members' edits. Determine whether each changed key belongs to you by diffing the parsed artifact against `HEAD`, then stage your files only. Do not "tidy up" by committing the whole generated file; that silently takes ownership of another thread's in-progress work.
- **Verify repo visibility from the tool, not the README.** `README.md` claimed `(privat)` while `gh repo view --json visibility` returned `PUBLIC`. Everything written into a public repo is world-readable, so a wrong "privat" label removes the warning that keeps PII out. Check `visibility` before writing any note that assumes secrecy.
- **Visibility is a PRODUCT gate, not only a PII gate — check it before committing gated content.** When a repo holds material the business model sells (paid course content, entitlement-gated sources), a `PUBLIC` repo publishes it outright: the paywall only guards the rendered app, while the raw files stay fetchable at `raw.githubusercontent.com` with no login. So the check is not "does this contain PII" but "is any of this meant to be behind a paywall". Run `gh repo view <owner>/<repo> --json visibility` **before** staging content paths, and if it is `PUBLIC` while the material is meant to be gated, say so at the top of the reply as urgent — a repo left open is a live leak that no test will flag, because every suite passes with the content public.
- **Withhold unlicensed third-party payloads from a public repo and name the withheld path.** When a bundle ships vendor/skill content alongside a notices file that itself flags missing licences, committing it distributes it. Apply the code and docs, leave the encumbered directory out, and record in the commit message both the reason and any README lines that now point at the withheld path — otherwise the next reader sees a broken reference and no explanation.
- **A `gitleaks` count without file paths is not a verdict.** A `--no-git` scan sweeps the whole tree, so gitignored build output (`.next/`, `dist/`, `node_modules/`) reports hits like `generic-api-key` on manifest hashes — build content, not credentials. Triage every finding against `git ls-files | grep <path>`: zero tracked hits means the push is clean. Report findings broken down by path, never a bare total — a bare count reads as "secret leaked" and blocks a legitimate push.

## References

- `references/multi-repo-boundaries.md` — the repo map, two-stage commit discipline, and the two-stage verification checks before pushing.
- `references/cross-file-consistency.md` — mechanically verifying that files describing the same content agree, and how to read a noisy diff.

## Bukti

- `git check-ignore -v apps/abstract-studio/...` → `.gitignore:27:apps/` — nested repos are excluded from root history.
- Dual commit sequence: root `ecosystem-config` and nested `abstract-studio` pushed as two separate commits, each verified with a whitespace-stripped SHA comparison.
- `skills/sync-to-agents.sh` → 177 skills synced; `scripts/skill-manifest.py --check` → 0 mismatch.
