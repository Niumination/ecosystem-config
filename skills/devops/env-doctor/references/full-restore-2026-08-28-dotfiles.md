# Dotfiles Full Restore 2026-08-28 — Stow Conflicts, Cargo Guard, Rust 1.98

**Date:** 2026-08-28 15:06-15:12 WIB  
**Repo:** `~/Desktop/Niumination/dotfiles/zaryu-terminal-dotfiles` → `zaryu-terminal-dotfiles:main@2b0c497`  
**Trigger:** User requested full dotfiles restore + install optional tools after `up-eco` showed `10 files dirty` and `setup.sh --dry-run` flagged `zsh` conflicts.

## Sequence that succeeded

1. **Pre-check optional tools** — `jq/tldr/lazygit/gh` OK, `asdf` missing, `neovim` flagged missing (shim needed), `abbr` flagged missing (zsh function, not binary), `node 26.7.0/python 3.14.7/ruby 2.6.10/go 1.27.0` OK.
2. **`brew install asdf` (0.20.0)** + `ln -s /usr/local/bin/nvim /usr/local/bin/neovim` (brew neovim binary is `nvim`).
3. **`./setup.sh --dry-run`** predicted: backup `~/.config/zsh` and `~/.config/zsh-abbr` with timestamped `.backup.2026*`.
4. **First real `./setup.sh`** backed up both dirs but aborted on `zsh`:
   ```
   stowing zsh would cause conflicts: .zshenv/.zshrc not owned by stow
   Ignoring absolute symlink: .zshenv => /Users/zaryu/zsh/.zshenv
   ```
   Root cause: legacy absolute symlinks `~/.zshrc -> /Users/zaryu/zsh/.zshrc` (outside stow DOTFILES_DIR).
5. **Fix:** `rm ~/.zshrc ~/.zshenv` then `stow -v -d . -t ~ zsh` → 4 links OK (`~/.zshenv`, `~/.zshrc`, `~/.config/zsh`, `~/.config/zsh-abbr`).
6. **Second `./setup.sh` pass** then aborted on `bin`:
   ```
   WARNING! stowing bin would cause conflicts: source is an absolute symlink .../bin/.local/bin/java => /usr/local/Cellar/openjdk@21/21.0.12/...
   ```
   Root cause: `bin/.local/bin/java` absolute symlink pointed to `21.0.12` which bumped to `21.0.12.1`. Fix: `rm bin/.local/bin/java` in repo.
7. **Third `./setup.sh`** → `✅ Setup Complete!` 17 packages: starship, tmux, zsh, fzf, git, bin, asdf, node, ruby, lazygit, yamllint, markdown, rc, brew, nvim, spell, kitty. `ZDOTDIR .zshrc symlink OK`, `fzf keybindings OK`, `TPM already installed`.
8. **Post-restore guard for `~/.cargo/env`:**
   `zsh/.zshenv` was ` . "$HOME/.cargo/env"` (unguarded) → every `zsh -c` warned `no such file`. Patched to:
   ```zsh
   if [[ -f "$HOME/.cargo/env" ]]; then . "$HOME/.cargo/env"; fi
   ```
   Commit `2b0c497 fix(zsh): guard .cargo/env sourcing + install rust 1.98.0`.
9. **Rust install:** `curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y --no-modify-path` timed out at 180s but succeeded partially; required `~/.cargo/bin/rustup default stable` (set toolchain) then `rustup update` to recover from `Missing manifest in toolchain` → `rustc 1.98.0 (88d9e12ae)` / `cargo 1.98.0 (797e8a9bc)`. `zsh -c 'source ~/.zshenv && cargo --version'` now OK; bash non-login still needs `.cargo/bin` but zsh is canonical.

## Pitfalls to capture

- **Absolute symlinks in stow packages** (`bin/.local/bin/java -> /usr/local/Cellar/...`) break stow after brew upgrades. Never commit absolute Cellar paths; use `brew --prefix` wrapper or document as transient.
- **Runtime stow conflicts:** `zsh/.config/zsh/.zcompdump` (50112B), `.zsh_history` (18611B), `.zsh_sessions` are zsh-generated. `setup.sh` correctly backs up `~/.config/zsh` before restow; `stow --no` flagging them is expected, not a failure.
- **`abbr: command not found` in bash** after `zsh-abbr 6.5.2` install is not a bug — `abbr` is a zsh function. Formula is `olets/tap/zsh-abbr`, not `abbr`. Verify via `zsh -c 'source ~/.zshrc && type abbr'`.
- **Neovim shim:** `setup.sh` checks `neovim` but brew provides `nvim`. Shim `ln -s nvim neovim` makes the check pass.
- **Cargo guard:** always guard `.cargo/env` sourcing; Rust may be absent on fresh macOS.

## Verification

```
zsh -c 'source ~/.zshenv && source ~/.zshrc && echo ✅ zsh full OK'
~/.cargo/bin/rustc --version → 1.98.0
~/.cargo/bin/cargo --version → 1.98.0
asdf --version → 0.20.0
nvim --version → 0.12.5
./setup.sh --dry-run → All required tools installed, only `abbr` (expected) optional missing
```

## Follow-up

- `zsh-abbr` warning `typeset -g` on system zsh 5.9 remains cosmetic.
- `~/zsh/` legacy dir at `$HOME/zsh/` (6 files, 192B) differs from `DOTFILES_DIR` repo's `zsh/` (2 files) — keep repo canonical, `$HOME/zsh` is stow artefact.
