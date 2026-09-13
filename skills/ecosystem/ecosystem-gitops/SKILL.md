---
name: ecosystem-gitops
description: Use when migrating GitHub remotes HTTPS/SSH or bulk remotes.
---

# Ecosystem GitOps

Bulk Git remote and auth for ~/Desktop/Niumination (~40 repos).

## SSH Recovery Checklist
- Key: `ls ~/.ssh/id_rsa` + reconstruct pub if needed
- PAT scopes: `admin:public_key` + `read:org` (check `x-oauth-scopes`)
- Upload: `POST /user/keys`
- Cleanup: `git config --global --unset url."https://github.com/".insteadOf`
- Mass migrate + verify (see references)

## Bulk Push Audit

Pushing several repos at once starts read-only: one line per repo with branch, dirty-file count, commits ahead/behind upstream (`rev-list --count '@{u}..HEAD'` / `'HEAD..@{u}'`), and remote URL.

- Push only repos whose remote is org-owned and whose ahead commits are already reviewed — plain `git push`, never force; a non-fast-forward rejection is information, not an error to override.
- Dirty working trees stay local: pushing uploads committed work only, so uncommitted WIP is never swept in — report it per repo instead of committing it blind.
- Exclude foreign-upstream checkouts (repos tracking someone else's org) and repos with no upstream tracking — pushing there either writes to the wrong project or invents tracking the owner never asked for.
- `?` ahead/behind counts mean no upstream is set — confirm with `branch -vv` before deciding anything.

## Overlay Pattern — apply a zip/tarball snapshot into an existing repo

When a downstream source (VPS, collaborator) produces a zip of a repo that already exists locally, treat the snapshot as a **patch source**, not a replacement. The local repo may have commits the snapshot does not.

1. **Pull first** — `git pull origin main` (or `git fetch origin && git merge origin/main`) to integrate commits made since the snapshot was taken. Fast-forward is normal; a merge commit means the snapshot is stale and may conflict.
2. **Extract to /tmp** — never extract directly over the worktree; compare first.
3. **rsync with explicit excludes** — skip `.git`, and any file the target's `.gitignore` marks as runtime/secret. Typical excludes for a Python project: `config.json`, `*.db`, `mata-v0.1.tar.gz`. Use `git add -f` only when the file is intentionally versioned despite `.gitignore`.
4. **Review before staging** — `git status --short` first; `git diff --stat` for the big files; selective `git add` (never blind `git add .`).
5. **Commit with the change vector** — mention the source (snapshot zip), what was excluded, and why.

## References
- `references/github-ssh-migration.md` — full SSH migration workflow
- `references/sapa-ai-laporan-status-merge.md` — sapa-ai page merge & report adaptation
