---
name: env-doctor
description: Recover dotfiles and shell after Stow or bulk delete.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [dotfiles, stow, zsh, opencode, hermes, disaster-recovery, env-health]
    related_skills: [opencode, hermes-agent, systematic-debugging]
---

# Env Doctor — Post-Incident Environment Recovery

Recover and verify a developer environment after `setup.sh` / GNU Stow misruns or bulk config deletion (e.g. jcode session deleting `~/.jcode/*`, `~/.hermes/.env`, `~/.config/opencode/*`, `vault/*`).

## When to Use
- `stow --restow` aborts with `WARNING: skipping target which was current stow directory .` or `cannot stow ... over existing target`
- `~/.zshrc` / `~/.zshenv` missing or `DOTFILES_DIR` resolves to `/Users` / wrong path
- Post-incident check requested: "cek opencode dan jcode pasca insiden dan restow"
- `opencode.jsonc`, `~/.jcode/config.toml`, `~/.hermes/.env`, `~/.9router/*`, `vault/secrets.zsh` suspected deleted (see `docs/ECOSYSTEM-STATUS-*.md`)
- Any `source ~/.zshrc` produces `bad substitution` / `bindkey: command not found`

## Quick Health Check (read-only, run first)

```bash
# ONE-LINER — health check lengkap via setup.sh (18 pemeriksaan):
# shell, stow symlinks, tools, syntax zsh, git repo, config agent + residu juan-router
bash ~/Desktop/Niumination/dotfiles/zaryu-terminal-dotfiles/setup.sh --doctor

# Exit code 0 = sehat; 1 = ada gagal. Tabel ✅/⚠️/❌ tercetak.
```

Detail manual (kalau perlu probe spesifik di luar doctor):

```bash
pwd; ls -la ~ | head -n 40
ls -la ~/.config/ | sort
cat ~/.config/opencode/opencode.jsonc 2>&1 | head -n 20
cat ~/.hermes/.env 2>&1 | head -n 20; ls -la ~/.hermes/.env
ls -la ~/.9router/ 2>&1 | head -n 20; ls -la ~/.config/9router 2>&1 | head
cat ~/Desktop/Niumination/vault/secrets.zsh 2>&1 | head -n 20
cat ~/Desktop/Niumination/docs/ECOSYSTEM-STATUS-*.md 2>&1 | head -n 120
which -a opencode; opencode --version; opencode providers list 2>&1 | head -n 20
zsh -c 'source ~/.zshrc && echo DOTFILES_DIR=$DOTFILES_DIR && echo OK' 2>&1 | tail -n 20
ls -la ~/.zshrc ~/.zshenv ~/.config/zsh/.zshrc 2>&1
```

Interpretation:
- `opencode.jsonc` with only `{"$schema":...}` is **valid minimal** — real auth lives in `~/.local/share/opencode/auth.json`. Empty ≠ broken.
- `~/.9router` (not `~/.config/9router`) is current location on this ecosystem.
- `DOTFILES_DIR=/Users/zaryu` is correct when `~/zsh/` and `~/shared/` live at `$HOME` (HOME itself is the stow dir, `.git -> Desktop/.../.git`).

## Recovery Procedure

### 1. Do NOT re-run blind `stow` from the wrong directory
`setup.sh` sets `DOTFILES_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"`. If `setup.sh` lives at `~/setup.sh`, DOTFILES_DIR is `$HOME`. Running `stow -t ~ zsh` **inside** `~` always warns `skipping target which was current stow directory .`. Run from the repo root:

```bash
DOTFILES=~/Desktop/Niumination/dotfiles/zaryu-terminal-dotfiles
cd "$DOTFILES" && stow --restow -t ~ zsh   # or: ~/setup.sh --dry-run first
```

If conflicts like `cannot stow ... over existing target .fzf.zsh`, remove the blocking file **only after** confirming it is not stow-owned:
```bash
rm -f ~/.zshrc ~/.config/zsh/.zshrc ~/.fzf.zsh
cd "$DOTFILES" && stow --restow -t ~ zsh git fzf bin starship tmux nvim lazygit yamllint markdown rc asdf node ruby brew kitty spell
```

### 2. Fix the symlink triangle (idempotent)
```bash
ln -sf ~/zsh/.zshrc ~/.zshrc
ln -sf ~/zsh/.zshenv ~/.zshenv
mkdir -p ~/.config/zsh && ln -sf ~/.zshrc ~/.config/zsh/.zshrc
ls -la ~/.zshrc ~/.zshenv ~/.config/zsh/.zshrc
```

### 3. Restore `DOTFILES_DIR` logic in `~/zsh/.zshrc`
Must be the zsh-native form, not a bash fallback. Do **not** simplify to `DOTFILES_DIR="${HOME}/zsh/.."` — it breaks when sourced under bash or hides the fallback:

```zsh
# Shared environment variables — robust detection (stow + ZDOTDIR symlink)
DOTFILES_DIR="${${(%):-%x}:A:h:h}"
# Fix: when stowed at $HOME/.zshrc or via ZDOTDIR symlink, detection yields /Users
if [[ ! -d "$DOTFILES_DIR/zsh" ]]; then
    DOTFILES_DIR="$HOME/Desktop/Niumination/dotfiles/zaryu-terminal-dotfiles"
fi
export DOTFILES_DIR
source "$DOTFILES_DIR/shared/environment.sh"
```

Test only under `zsh`, never `bash`:
```bash
zsh -c 'source ~/.zshrc && echo DOTFILES_DIR=$DOTFILES_DIR; ls $DOTFILES_DIR/shared/environment.sh'
# bash -c 'source ~/.zshrc' will always show "bad substitution" — ignore it
```

### 4. Verify shell loads cleanly
```bash
zsh -c 'source ~/.zshrc && echo "✅ Zsh loaded successfully"' 2>&1 | tail -n 20
# Expected benign warnings: ~/.cargo/env missing, zsh-abbr typeset -g on old zsh
```

### 5. Verify agents (no writes during repair window)
```bash
opencode --version          # 1.18.x
opencode providers list      # expect Zen + env vars
```
If `ECOSYSTEM-STATUS.md` says repair is still running (`~17:45-18:04` incident window), **do not** edit `~/.jcode/*`, `~/.hermes/.env`, `~/.config/opencode/*`, `vault/*`, nor run `scripts/keys.sh set` until user confirms repair done.

## Pitfalls
- **Testing zshrc with bash** always fails (`${${(%):-%x}:A:h:h}: bad substitution`). Use `zsh -c 'source ~/.zshrc'`.
- **`typeset -g` errors from zsh-abbr** on macOS system zsh (5.9) vs newer zsh — cosmetic, not fatal.
- **`~/.fzf.zsh` and `bin/.local/bin/java` absolute symlink conflicts** during stow — expected; re-run with `rm -f` or `--adopt` only for the conflicting target.
- **Two dotfiles roots** (`~/` and `~/Desktop/Niumination/dotfiles/...`) coexist; diff them with `diff -u` before assuming which is canonical. HOME being the stow dir is intentional when `~/setup.sh` exists.
- **9router location drift**: check `~/.9router/` when `~/.config/9router/` is missing.
- **Don't capture** `command not found` / missing binary as a durable skill rule — capture the install fix instead.

## References
- `references/post-incident-2026-08-27.md` — full transcript and file states from the 2026-08-27 bulk-delete incident
- `docs/ECOSYSTEM-STATUS-2026-08-27.md` — broadcast status and temporary freeze rules
- `~/Desktop/Niumination/AGENTS.md` — DOX root contract

## Verification
- `zsh -c 'source ~/.zshrc && echo $DOTFILES_DIR'` prints existing dir containing `zsh/` and `shared/environment.sh`
- `opencode run 'Respond with exactly: OPENCODE_SMOKE_OK'` succeeds
- `ls -la ~/.zshrc ~/.zshenv ~/.config/zsh/.zshrc` all are symlinks, not regular files
