# Extended Recovery 2026-08-28 — Dotfiles Stow Legacy, Rust, 9Router Backup, Broker Removal, GH Auth

Validated same session as full recover 02:05→15:30.

## Dotfiles Stow legacy (setup.sh fails)

**Symptom:** `./setup.sh` aborts:
```
Ignoring an absolute symlink: .zshrc => /Users/zaryu/zsh/.zshrc
WARNING! stowing zsh would cause conflicts: existing target is not owned by stow: .zshenv/.zshrc
WARNING! stowing bin would cause conflicts: source is an absolute symlink bin/.local/bin/java => /usr/local/Cellar/openjdk@21/21.0.12/...
```

**Root cause:**
- `~/.zshrc → /Users/zaryu/zsh/.zshrc` is legacy absolute symlink (pre-DOTFILES_DIR fix). Current repo is `~/Desktop/Niumination/dotfiles/zaryu-terminal-dotfiles/zsh/.zshrc`.
- `bin/.local/bin/java` pointed to `21.0.12` but brew upgraded to `21.0.12.1` → broken absolute symlink.
- `zsh/.zshenv` had ` . "$HOME/.cargo/env"` without guard → `no such file` when Rust missing.
- `abbr` is zsh function from `zsh-abbr 6.5.2`, not binary — `command -v abbr` in bash correctly fails, `zsh -c 'type abbr'` shows shell function.
- `neovim` binary is `nvim` — `setup.sh` checks `neovim` string.

**Fix:**
```bash
rm ~/.zshrc ~/.zshenv
stow -v -d . -t ~ zsh   # from repo root: ~/Desktop/Niumination/dotfiles/zaryu-terminal-dotfiles
# → .zshrc => Desktop/Niumination/dotfiles/zaryu-terminal-dotfiles/zsh/.zshrc ✓
rm Desktop/Niumination/dotfiles/zaryu-terminal-dotfiles/bin/.local/bin/java
./setup.sh  # → ✅ Setup Complete! 17 packages (starship, tmux, zsh, fzf, git, bin, asdf, node, ruby, lazygit...)
# zsh/.zshenv guard:
# if [[ -f "$HOME/.cargo/env" ]]; then . "$HOME/.cargo/env"; fi
ln -s /usr/local/bin/nvim /usr/local/bin/neovim   # shim for setup.sh check
brew install asdf  # 0.20.0  — also olets/tap/zsh-abbr already 6.5.2
zsh -c 'source ~/.zshrc && echo DOTFILES_DIR=$DOTFILES_DIR'  # verify
```

## Rust install

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y --no-modify-path
~/.cargo/bin/rustup default stable   # first run may error "Missing manifest"
~/.cargo/bin/rustup update           # recovers: rustc 1.98.0 (88d9e12ae 2026-08-18), cargo 1.98.0
zsh -c 'source ~/.zshenv && cargo --version && rustc --version'
# bash non-login won't see cargo — must test via zsh -c
```

Commit: `fix(zsh): guard .cargo/env sourcing + install rust 1.98.0` → `zaryu-terminal-dotfiles@2b0c497`

## 9Router backup gap

- Current location: `~/.9router/` (db/data.sqlite 172K, auth/cli-secret, jwt-secret, machine-id) — NOT `~/.config/9router/` (missing).
- `~/Backups/config-clean-20260828004022/` had hermes.env + jcode + opencode.* but NO 9router → gap post-incident.
- Fix: `cp -R ~/.9router ~/Backups/9router-20260828/` + `cp -R ~/.9router ~/Backups/config-clean-*/9router`
- Live check: `lsof -i :20128` → node cli.js --tray, `curl localhost:20128/v1/models` → 5 models (gemini/*)

## Broker removal (clean HOLD scheme)

User: "hapus aja semua yang berhubungan dengan broker, nanti pikirkan skema lebih baik"
```bash
rm scripts/keys.sh scripts/migrate-keys-to-broker.sh
rm docs/references/credential-broker-design.md docs/references/credential-broker-handoff.md
# up-eco.sh: delete check_credential_broker() function (39 lines) + call site
# docs/ECOSYSTEM-STATUS-2026-08-27.md: strip TL;DR broker line + timeline rows 09:43/10:31/10:16 + ## Credential Broker section + keys.sh list line
```
Commit `chore(eco): hapus broker credential — skema di-review ulang` → `ecosystem-config@c3394b9`
up-eco: `9 → 4 → 3` recommendations after removal (broker line gone).

## GH auth (read:org scope)

- `GITHUB_TOKEN` (from ~/.hermes/.env) scope `read:user, repo` → `gh auth login --with-token` → `error validating token: missing required scope 'read:org'` but `GH_TOKEN=$GITHUB_TOKEN gh auth status` still `✓ Logged in to github.com account Niumination (GH_TOKEN)` with warning `Missing required scopes: 'read:org'` — still functional.
- `gh pr list --owner` flag doesn't exist → use `GH_TOKEN=... gh pr list --limit 10` + `api.github.com/search/issues?q=org:Niumination+is:pr+is:open` (total 3: niu-mission-control#11, ai-file-organizer-android#2, Niu-LKH#1)
- Persist: `GH_TOKEN` already in ~/.hermes/.env (append if missing, dedup with `awk '!seen[$0]++'` if >1). Export needed for up-eco: `GH_TOKEN` env makes Phase 5b flip from `skip PR check` to `Review & merge 3 open PR`.

## References

- This session: up-eco 15:17 (9→3 recs), stow 15:06 (Setup Complete), rust 15:09, broker removal 15:30, GH auth 15:21
- Related: references/full-recover-2026-08-28.md, references/splp-bapokting-chip-2026-08-28.md
