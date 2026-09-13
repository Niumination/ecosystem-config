# Post-Incident 2026-08-27 — Bulk Config Deletion

**Incident window:** ~17:45–18:04 WIB, 2026-08-27
**Cause:** 1 jcode session `cd` to wrong directory, then deleted configs
**Status source:** `~/Desktop/Niumination/docs/ECOSYSTEM-STATUS-2026-08-27.md`

## Files deleted (at time of incident)
- `~/.jcode/config.json` (legacy) — now superseded by `~/.jcode/config.toml` (474 lines, healthy)
- `~/.hermes/.env` — restored by 2026-08-27 23:39 (2431B, contains OPENCODE_ZEN_API_KEY, TELEGRAM, GITHUB_TOKEN, etc.)
- `~/.config/opencode/opencode.jsonc` — now minimal `{"$schema": "https://opencode.ai/config.json"}` (valid; real auth in `~/.local/share/opencode/auth.json`)
- `~/.config/9router/*` — now lives at `~/.9router/` (runtime/ only)
- `vault/secrets.zsh` — present (519B) at `~/Desktop/Niumination/vault/secrets.zsh`

## Session transcript highlights
- `setup.sh --dry-run` showed 18 packages to stow, 5 backups needed (.zshrc, .config/zsh, .config/zsh-abbr, .npmrc, .editorconfig)
- Real `setup.sh` succeeded with `WARNING: skipping target which was current stow directory .` x34 — benign, caused by running stow inside HOME
- Symlink triangle broken: `~/.zshrc` missing, `~/.config/zsh/.zshrc -> /Users/zaryu/.zshrc` dangling
- Manual fix `ln -sf ~/zsh/.zshrc ~/.zshrc` restored triangle; `DOTFILES_DIR` simplified to `"${HOME}/zsh/.."` then reverted to zsh-native `"${${(%):-%x}:A:h:h}"` with fallback
- `bash -c 'source ~/.zshrc'` → `bad substitution` (expected, ignore); `zsh -c 'source ~/.zshrc'` → OK with `typeset -g` warnings from zsh-abbr on system zsh 5.9
- `~/.9router` emptyish, `~/.config/opencode/node_modules` intact, opencode 1.18.23, jcode v0.81.1 healthy

## Two dotfiles roots (intentional)
- `$HOME` (contains `~/setup.sh`, `~/zsh/`, `~/shared/`, `.git -> Desktop/.../.git`) — actual stow dir
- `~/Desktop/Niumination/dotfiles/zaryu-terminal-dotfiles/` — git repo mirror
- `diff -q ~/zsh/.zshrc Desktop/.../zsh/.zshrc` differed only in DOTFILES_DIR fallback block
- `~/shared/environment.sh` and `Desktop/.../shared/environment.sh` identical (1005B)

## Health checks that passed post-recovery
```
opencode --version → 1.18.23
opencode providers list → 1 credential (Zen) + 3 env vars
jcode --version → v0.81.1
jcode auth status → opencode/opencode-go available
zsh -c 'source ~/.zshrc && echo $DOTFILES_DIR' → /Users/zaryu (correct)
ls -la ~/.zshrc ~/.zshenv ~/.config/zsh/.zshrc → symlinks OK
vault/secrets.zsh → present
~/.hermes/.env → present
```

## Freeze rules (until repair confirmed)
1. Don't edit `~/.jcode/*`, `~/.hermes/.env`, `~/.config/opencode/*`, `vault/*`
2. Don't run `scripts/keys.sh set` / broker migration Phase B
3. Agent traffic via 9router `127.0.0.1:20128` is fine
