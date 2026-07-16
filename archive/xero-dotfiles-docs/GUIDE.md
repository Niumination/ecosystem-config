# Panduan Penggunaan xero/dotfiles

## Neovim

### Leader Key
- Leader = `,` (koma)

### Plugin Highlights
- **blink.cmp** — auto-completion engine
- **lazy.nvim** — plugin manager
- **telescope.nvim** — fuzzy finder (files, grep, buffers, dll)
- **snacks.nvim** — dashboard, notifier, indent, picker, toggle
- **lualine.nvim** — status bar
- **which-key.nvim** — bantuan keybindings (tekan `,` lalu tunggu)
- **nvim-treesitter** — syntax highlighting
- **mason.nvim** — install LSP/linter/formatter
- **conform.nvim** — auto-formatting
- **gitsigns.nvim** — git diff di gutter
- **trouble.nvim** — diagnostics list
- **vim-fugitive** — git integration
- **nvim-surround** — surround text objects
- **copilot.lua** — GitHub Copilot

### Keybindings Neovim

#### Buffer
| Key | Aksi |
|-----|------|
| `Ctrl+n` | Next buffer |
| `Ctrl+p` | Prev buffer |
| `Ctrl+x` | Close buffer |

#### Tabs
| Key | Aksi |
|-----|------|
| `,<tab>l` | Last tab |
| `,<tab>f` | First tab |
| `,<tab><tab>` | New tab |
| `,<tab>]` | Next tab |
| `,<tab>d` | Close tab |
| `,<tab>[` | Previous tab |

#### Toggle (Snacks)
| Key | Aksi |
|-----|------|
| `,s` | Spell check toggle |
| `,w` | Line wrap toggle |
| `,Uc` | Conceal level toggle |
| `,Ud` | Diagnostics toggle |
| `,Ug` | Indent lines toggle |
| `,Uh` | Inlay hints toggle |
| `,Ul` | Line number toggle |
| `,UL` | Relative number toggle |
| `,Um` | Message history |
| `,UT` | Treesitter toggle |
| `,UU` | Undo tree |

#### LSP
| Key | Aksi |
|-----|------|
| `K` | Hover info |
| `gd` | Go to definition |
| `gr` | References |
| `gi` | Implementation |
| `[d` / `]d` | Previous/next diagnostic |
| `<leader>ca` | Code action |
| `<leader>rn` | Rename symbol |
| `<leader>f` | Format buffer |

#### Git (Fugitive)
| Key | Aksi |
|-----|------|
| `:G` | Git status |
| `:G blame` | Git blame |
| `:G log` | Git log |

#### Telescope
| Key | Aksi |
|-----|------|
| `:Telescope find_files` | Cari file |
| `:Telescope live_grep` | Cari teks |
| `:Telescope buffers` | Cari buffer |
| `:Telescope help_tags` | Cari help |
| `:Telescope oldfiles` | Recent files |
| `:Telescope file_browser` | File browser |

#### Utility
| Key | Aksi |
|-----|------|
| `,,` | Clear search highlight |
| `,x` | Chmod +x file |
| `d` | Delete tanpa overwrite register |
| `dd` | Delete line tanpa overwrite register |
| `Ctrl+d/Ctrl+u` | Scroll + center cursor |
| `n` / `N` | Next/prev search + center |
| `Q` | Disabled (ex mode) |
| `:T` | Vertical terminal |

#### Dashboard (Snacks)
| Key | Aksi |
|-----|------|
| `i` | New file |
| `o` | Recent files |
| `f` | Find file |
| `\` | Find text |
| `g` | Git log |
| `l` | Lazy plugin manager |
| `m` | Mason LSP installer |
| `p` | Lazy profile |
| `q` | Quit |

---

## ZSH

### Prompt
- Default: **Starship** (via `starship.toml`)
- Fallback: custom zsh prompt (minimal/ascii/arrows/classic/dual/ninja)
- Atur tema prompt di `~/.config/zsh/05-prompt.zsh` — ubah `PROMPT_STYLE`

### Alias Penting
| Alias | Aksi |
|-------|------|
| `e` | `$EDITOR` (nvim) |
| `c` | Clear screen |
| `ll` | `ls -lahF` |
| `g` | `git` |
| `ec` | `nvim --cmd ":lua vim.g.noplugins=1"` (clean mode) |
| `ZZ` | `exit` |
| `fuck` | `sudo $(fc -ln -1)` |
| `y` | `yank` |
| `unquarantine` | (macOS only) hapus quarantine attribute |

### Git Aliases
| Alias | Aksi |
|-------|------|
| `ga` | `git add` |
| `gc` | `git clone` |
| `gcm` | `git commit -m` |
| `gco` | `git checkout` |
| `gcob` | `git checkout -b` |
| `gp` | `git push` |
| `gs` | `git status -sb` |
| `gd` | `git difftool` |
| `gg` | `git graph` |
| `gr` | `git rebase -i` |
| `gx` | `git reset --hard @` |

### ZDOTDIR
ZSH config di `~/.config/zsh/` bukan di `~/`. Diatur via `~/.zshenv`:
```bash
export ZDOTDIR="$HOME/.config/zsh"
```

---

## tmux

### Prefix Key
- Prefix = `` ` `` (backtick) — bukan `Ctrl+b`

### Keybindings
| Key | Aksi |
|-----|------|
| `` ` `` | Send prefix |
| `h` | Split pane vertical |
| `v` | Split pane horizontal |
| `z` | Zoom pane (smart: kirim `,z` ke vim) |
| `Z` | Zoom pane (paksa) |
| `x` | Kill pane |
| `[` / Escape | Enter copy mode |
| `]` / `p` | Paste buffer |
| `r` | Reload tmux config |
| `t` | Toggle status bar |
| `a` | Toggle synchronize panes |
| `:` | Command prompt |
| `Space` | Clipboard menu (clipmenu) |
| `e` | Emoji picker |

### Copy Mode (vi style)
| Key | Aksi |
|-----|------|
| `v` | Start selection |
| `y` | Yank (copy to system clipboard via OSC52) |
| `Y` | Yank to tmux buffer |

### Tmux Plugins
- **tmux-thumbs** — fuzzy URL/word picker (tekan `f` saat prefix)
- **tmux-mode-indicator** — mode indicator di status bar
- **tmux.nvim** — seamless navigation antara tmux & nvim (`Ctrl+h/j/k/l`)

---

## Scripts (~/.local/bin)

| Script | Fungsi |
|--------|--------|
| `sysinfo` | Informasi sistem |
| `hex256` | 256 color chart |
| `cidr` | CIDR calculator |
| `dnsdumpster` | DNS lookup |
| `pb` | Pastebin |
| `tmpl8` | Template generator |
| `yank` | OSC52 clipboard yank |
| `ansicat.c` | ANSI art viewer |
| `tmux-status` | tmux status bar script |

### Catatan Script
- `xdg-open`, `vpn`, `changememaddr`, `exorg` — **Linux-specific**, mungkin tidak berfungsi di macOS
