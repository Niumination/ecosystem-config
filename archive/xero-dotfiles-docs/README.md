# xero/dotfiles - Documentation

**Author:** xero (x@xero.style)
**Source:** https://code.x-e.ro/dotfiles | https://git.io/.files

## Overview

Dotfiles dari xero — config Neovim, ZSH, tmux, dan script utility.  
Telah diadaptasi untuk **macOS** (komponen Linux-only di-skip).

## Struktur Folder

```
~/.local/src/dotfiles/          # Git repo (sumber semua config)
  ├── neovim/                   # Neovim config (lazy.nvim, ~40 plugins)
  ├── zsh/                      # ZSH config (XDG dir di ~/.config/zsh)
  ├── tmux/                     # tmux config (prefix: ` backtick)
  └── bin/                      # Script utility di ~/.local/bin

~/.config/
  ├── nvim/        → symlink ke neovim/.config/nvim
  ├── zsh/         → symlink ke zsh/.config/zsh
  ├── tmux/        → symlink ke tmux/.config/tmux
  └── starship.toml → symlink ke zsh/.config/starship.toml

~/.zshenv          → export ZDOTDIR="$HOME/.config/zsh"

~/.local/bin/      → symlink ke bin, fun, tmux-status scripts
```

## Management dengan Stow

Config dikelola dengan **GNU Stow** (symlink farm manager):

```bash
cd ~/.local/src/dotfiles

# Pasang/sync config ke home directory:
stow neovim zsh tmux bin -t ~
# atau stow ulang salah satu:
stow neovim -t ~

# Hapus symlink (tanpa hapus file asli):
stow -D neovim -t ~

# Update dari upstream:
cd ~/.local/src/dotfiles
git pull
stow neovim zsh tmux bin -t ~  # re-stow jika ada file baru
```

## Komponen yang Diinstall

| Komponen | Status | Lokasi |
|----------|--------|--------|
| Neovim | ✅ Full | ~/.config/nvim |
| ZSH | ✅ Full | ~/.config/zsh (via ZDOTDIR) |
| tmux | ✅ Full | ~/.config/tmux |
| bin scripts | ✅ Sebagian | ~/.local/bin |
| Git config | ❌ Skip (manual) | - |
| SSH config | ❌ Skip | - |
| Xorg | ❌ Linux-only | - |
| Blink | ❌ iOS-only | - |

## Brew Packages Terinstall

```bash
brew install stow tmux fzf ripgrep fd starship coreutils
```

## Catatan macOS

- ZSH `ZDOTDIR` di-set via `~/.zshenv` (bukan `/etc/zsh/zshenv`)
- coreutils GNU dipasang untuk kompatibilitas `ls --color=always`
- Starship prompt bisa diaktifkan/nonaktifkan via `~/.config/zsh/05-prompt.zsh`
- Beberapa alias Linux (`apt`, `systemctl`, `srm`) tidak berfungsi di macOS
