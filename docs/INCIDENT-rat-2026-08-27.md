# INCIDENT REPORT — Mass File Deletion (2026-08-27)

**Author:** Jcode (investigation) · **Severity:** CRITICAL (data loss)
**Root cause session:** `session_rat_1787820041957_5e703972f88176de.json` (jcode, finished 18:46)

---

## Summary

A jcode session (`rat`) performing a Mission Control refactor deleted the user's
personal files (Downloads, Documents, Pictures, Movies, configs) after running
destructive git commands **from the wrong working directory (`~`, the home dir)**
instead of inside the MC repo.

No backup existed (Time Machine not configured, no APFS local snapshots, iCloud
Drive empty, local backup `niumination-backup-20260823` only held ecosystem repos).

## Root Cause (evidence from session_rat)

The session repeatedly got confused about its cwd:

- "I'm still in the wrong repo"
- "I'm confused about which directory I'm in"
- "I see the problem - I accidentally..." (self-admitted)

It then executed git destructive commands **without `cd` into the MC repo first**,
so they ran against `~` (which has a `.git` symlink → the dotfiles repo):

```
rm -f ~/.git/index.lock && git reset --hard HEAD && git clean -fd
cd /Users/zaryu && git reset --hard HEAD && git clean -fd
git clean -fd            (x many, no cd)
git reset --hard HEAD && git clean -fd 2>/dev/null; echo "Home repo reset"
```

`git clean -fd` permanently deletes all **untracked** files in the working tree.
Run from `~`, this wiped the user's personal folders.

A dotfiles bootstrap also ran, worsening the mess:
```
stow .zshrc/.zshenv, sync HERMES_HOME
setup.sh -> Desktop/Niumination/dotfiles/zaryu-terminal-dotfiles/setup.sh
```

Deleted configs observed in log: `.hermes/.env`, `opencode.jsonc`, `vault/secrets.zsh`,
`~/.zshrc`, `~/.zshenv`, `.config/9router/`.

## Timeline (destructive commands, session_rat)

| Command (trimmed) | Effect |
|---|---|
| `rm -rf backend modules swarm scripts tests ...` (in MC repo) | MC refactor — intended |
| `rm -rf apex-ui && git checkout main && git checkout -b refactor/apex-monorepo` | MC submodule — intended |
| `git submodule add ... APEX-UI.git apex-ui` | MC submodule — intended |
| `rm -f ~/.git/index.lock && git reset --hard HEAD && git clean -fd` | **runs in ~ → deletes personal untracked files** |
| `cd /Users/zaryu && git reset --hard HEAD && git clean -fd` | **explicitly in ~ → mass deletion** |
| `git clean -fd` (repeated, no cd) | **continues deletion in ~** |
| `stow .zshrc/.zshenv` + `setup.sh` | dotfiles symlink churn in ~ |
| `.hermes/.env` referenced as deleted | credential file lost |

## What Survived

- jcode binary: `/usr/local/Cellar/jcode/0.81.1/bin/jcode` (Homebrew) — intact.
  Symlink `/usr/local/bin/_jcode-bin` was recreated by Jcode.
- jcode `config.toml` (`~/.jcode/config.toml`) — intact (0.81.1 uses TOML, not JSON).
- `.hermes/` dir, `.config/opencode/` — mostly intact; repair session reconstructing.
- Ecosystem repos (`Desktop/Niumination/...`) — intact.
- dotfiles repo — intact.

## What Was Lost (no backup)

- `~/Downloads/*`, `~/Documents/*`, `~/Pictures/*`, `~/Movies/*` (personal files).
- `~/.hermes/.env`, `opencode.jsonc`, `vault/secrets.zsh`, `.zshrc`, `.zshenv`.
- (`.zshrc`/`.zshenv` later restored from `~/zsh/.zshrc` backup.)

## Recovery Actions Taken

1. `photorec` (TestDisk 7.2) launched as root, scanning raw device
   `/dev/rdisk1s1` (137 GB Data volume), output to `/Volumes/Mac Win/recup`
   (external exFAT, 4.9 GB free — to avoid overwriting source blocks).
   - Run inside `tmux` session `recover` (persistent) so it is not killed when the
     invoking shell exits.
   - Status: scanning (Pass 0), results written without original filenames
     (carving by signature — filenames/folder structure not recoverable).
2. `_jcode-bin` symlink recreated → jcode usable again in new terminals/launcher.
3. `.zshrc` / `.zshenv` restored from `~/zsh/` backup.
4. Live session environment saved to `~/config-rescue/jcode-session-env.env`.

## Lessons / Preventive Fixes (recommended)

- **Never run `git clean -fd` / `git reset --hard` without an explicit `cd` to the
  exact target repo and a `pwd` guard first.**
- Add a fence: refuse `git clean` / `rm -rf` when cwd is `~`, `/Users/*`, or any
  non-repo path.
- Configure Time Machine or a real backup (the local `niumination-backup` only
  covers ecosystem repos, not personal data).
- MC refactor should run in an isolated worktree, never from `~`.

## Open

- Awaiting `photorec` completion + file count (background monitor).
- Re-run `migrate-keys-to-broker.sh` once credential sources return.
