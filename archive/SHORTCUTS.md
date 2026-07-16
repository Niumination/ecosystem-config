# Neovim Shortcut Reference — LazyVim + TokyoNight

> Berdasarkan konfigurasi dotfiles: `~/.config/nvim` → `Desktop/Niumination/rekap/zaryu-terminal-dotfiles/nvim/.config/nvim`

---

## 1. Custom Keymaps (dotfiles overrides)

### Normal Mode

| Key | Aksi | Deskripsi |
|-----|------|-----------|
| `<Up>` | `:resize +5` | Tingkatkan tinggi window |
| `<Down>` | `:resize -5` | Kurangi tinggi window |
| `<Left>` | `:vertical resize -10` | Kurangi lebar window |
| `<Right>` | `:vertical resize +10` | Tingkatkan lebar window |
| `<leader>b=` | `:wincmd =` | Balance window splits |
| `<leader>bz` | `:wincmd _ \| :wincmd \|` | Zoom buffer (full screen) |
| `<leader>m` | `MiniMap.toggle()` | Toggle MiniMap |
| `<leader>qQ` | `:noautocmd w` | Save tanpa formatting |
| `<leader>uo` | `toggle_option('cursorcolumn')` | Toggle CursorColumn |
| `<leader>uO` | `toggle_colorcolumn()` | Toggle ColorColumn |

### Insert Mode

| Key | Aksi | Deskripsi |
|-----|------|-----------|
| `jj` | `<ESC>` | Kembali ke normal mode |

### Visual Mode

| Key | Aksi | Deskripsi |
|-----|------|-----------|
| `<leader>cs` | `:'<,'>sort` | Sort baris terpilih |

### Removed (konflik macOS)

| Key | Alasan |
|-----|--------|
| `<C-Up>` `<C-Down>` `<C-Left>` `<C-Right>` | Konflik dengan Mission Control macOS |

---

## 2. Tmux Navigator — Neovim ↔ Tmux

Navigasi seamless antar split Neovim dan pane Tmux.

| Key | Mode | Aksi |
|-----|------|------|
| `<C-h>` | normal / terminal | TmuxNavigateLeft |
| `<C-j>` | normal / terminal | TmuxNavigateDown |
| `<C-k>` | normal / terminal | TmuxNavigateUp |
| `<C-l>` | normal / terminal | TmuxNavigateRight |
| `<C-\>` | normal / terminal | TmuxNavigatePrevious |

> Juga dikonfigurasi di `tmux/tmux.conf` via plugin `vim-tmux-navigator`.

---

## 3. LazyVim Default Keymaps (inherited)

LazyVim menyediakan ~200+ keymaps default. Berikut yang paling sering digunakan:

### File & Pencarian

| Key | Aksi | Deskripsi |
|-----|------|-----------|
| `<leader><space>` | Find Files (cwd) | Pencarian file di direktori kerja |
| `<leader>ff` | Find Files (root) | Pencarian file di root proyek |
| `<leader>fg` | Live Grep | Pencarian teks real-time |
| `<leader>fw` | Grep Word | Cari kata di bawah cursor |
| `<leader>fr` | Recent Files | File terbaru |
| `<leader>fp` | Projects | Pilih proyek |
| `<leader>fC` | Find Config | Cari file konfigurasi |

### Buffer & Tab

| Key | Aksi | Deskripsi |
|-----|------|-----------|
| `<Tab>` | Next Buffer | Buffer berikutnya |
| `<S-Tab>` | Prev Buffer | Buffer sebelumnya |
| `<leader>bd` | Delete Buffer | Hapus buffer |
| `<leader>bD` | Delete Buffer (force) | Hapus buffer paksa |
| `[b` | BufferLineMovePrev | Pindah posisi buffer ke kiri |
| `]b` | BufferLineMoveNext | Pindah posisi buffer ke kanan |

### Split & Window

| Key | Aksi | Deskripsi |
|-----|------|-----------|
| `<leader>w` | Save file | Simpan file |
| `<leader>q` | Close window | Tutup window |
| `<leader>Q` | Quit Neovim | Keluar Neovim |
| `<leader>\\|` | Split right | Split vertikal |
| `<leader>-` | Split below | Split horizontal |

### LSP (Language Server Protocol)

| Key | Aksi | Deskripsi |
|-----|------|-----------|
| `gd` | Go to Definition | Ke definisi |
| `gr` | Go to References | Ke referensi |
| `gD` | Go to Declaration | Ke deklarasi |
| `K` | Hover | Dokumentasi hover |
| `gI` | Go to Implementation | Ke implementasi |
| `<leader>ca` | Code Action | Aksi kode (refactor, fix) |
| `<leader>rn` | Rename | Rename simbol |
| `<leader>D` | Type Definition | Ke definisi tipe |
| `[d` | Diagnostic prev | Diagnostic sebelumnya |
| `]d` | Diagnostic next | Diagnostic berikutnya |
| `<leader>e` | Toggle Trouble | Toggle diagnostic trouble |
| `<leader>le` | Line Diagnostics | Lihat diagnostic baris |

### Git

| Key | Aksi | Deskripsi |
|-----|------|-----------|
| `<leader>gg` | LazyGit | Buka LazyGit |
| `<leader>gj` | Next hunk | Hunk berikutnya |
| `<leader>gk` | Prev hunk | Hunk sebelumnya |
| `<leader>gs` | Stage hunk | Stage hunk |
| `<leader>gr` | Reset hunk | Reset hunk |
| `<leader>gS` | Stage buffer | Stage seluruh buffer |
| `<leader>gR` | Reset buffer | Reset seluruh buffer |
| `<leader>gb` | Git Blame | Blame line |
| `<leader>gd` | Git Diff | Diff hunk |
| `<leader>gB` | Git Blame Line | Blame preview |
| `<leader>gl` | Git Log | Log file |
| `<leader>gL` | Git Log All | Log seluruh repo |

### Toggle

| Key | Aksi | Deskripsi |
|-----|------|-----------|
| `<leader>ul` | Toggle Line Numbers | Toggle nomor baris |
| `<leader>uL` | Toggle Relative Numbers | Toggle nomor relatif |
| `<leader>us` | Toggle Spellcheck | Toggle spellcheck |
| `<leader>uw` | Toggle Wrap | Toggle line wrap |
| `<leader>ud` | Toggle Diagnostics | Toggle diagnostic |
| `<leader>uT` | Toggle Treesitter | Toggle highlight Treesitter |
| `<leader>uC` | Toggle Conceal | Toggle conceal |
| `<leader>uf` | Toggle Format | Toggle auto-format |
| `<leader>uu` | Toggle UndoTree | Toggle undotree |

---

## 4. Dashboard Keymaps (Snacks Dashboard)

Tampil saat Neovim dibuka tanpa file.

| Key | Aksi |
|-----|------|
| `f` | Find File |
| `n` | New File |
| `p` | Projects |
| `g` | Find Text (Live Grep) |
| `r` | Recent Files |
| `c` | Config (nvim) |
| `s` | Restore Session |
| `x` | Lazy Extras |
| `l` | Lazy (plugin manager) |
| `q` | Quit |

---

## 5. LazyVim Extras Aktif

28 extras dari `lazyvim.json`:

| Kategori | Extras |
|----------|--------|
| **AI** | copilot |
| **Coding** | mini-surround, yanky |
| **Editor** | dial, inc-rename, mini-move, snacks_explorer, snacks_picker |
| **Format** | prettier |
| **Language** | ansible, docker, git, json, markdown, python, ruby, sql, tailwind, toml, typescript, vue, yaml |
| **Linting** | eslint |
| **Test** | test.core |
| **Utility** | dot, mini-hipatterns, project |

---

## 6. LSP Servers

| Bahasa | LSP Server | Install |
|--------|-----------|---------|
| TypeScript/JavaScript | `ts_ls` | Mason |
| Vue | `volar` | Mason |
| Ruby | `ruby_lsp` | asdf (bukan Mason) |
| Python | `pyright` | Mason |
| Docker | `docker-compose-language-service`, `dockerfile-language-service` | Mason |
| JSON | `json-lsp` | Mason |
| YAML | `yaml-language-server` | Mason |
| TOML | `taplo` | Mason |
| Markdown | `marksman` | Mason |
| SQL | `sqlls` | Mason |
| Tailwind CSS | `tailwindcss-language-server` | Mason |
| Ansible | `ansible-language-server` | Mason |
| Git | `gitlab-ci-ls` | Mason |
| HTML | `html-lsp` | Mason |
| CSS | `css-lsp` | Mason |
| Lua | `lua-language-server` | LazyVim bawaan |

### Ruby LSP

```lua
-- options.lua
vim.g.lazyvim_ruby_lsp = "ruby_lsp"
vim.g.lazyvim_ruby_formatter = "standardrb"
```

Ruby LSP dan formatter menggunakan `standardrb` via `~/.asdf/shims/` (bukan Mason).

---

## 7. Formatters & Linters

| Tool | Untuk | Config |
|------|-------|--------|
| Prettier | TypeScript, Vue, JSON, YAML, Markdown | `extend-conform.lua` |
| standardrb | Ruby | `~/.asdf/shims/standardrb` |
| ESLint | JavaScript, TypeScript | `lazyvim.plugins.extras.linting.eslint` |
| markdownlint-cli2 | Markdown | `.markdownlint-cli2.yaml` |

---

## 8. Struktur File Konfigurasi

```
~/.config/nvim/                          → stow → dotfiles/nvim/.config/nvim/
├── init.lua                             # Entry: require("config.lazy")
├── lazy-lock.json                       # Versi plugin terkunci
├── lazyvim.json                         # 28 extras aktif
├── stylua.toml                          # Format Lua
├── spell -> ../../../spell              # Symlink ke spell files
├── after/queries/gotmpl/injections.scm  # Treesitter HTML injection Go template
└── lua/
    ├── config/
    │   ├── lazy.lua                     # Bootstrap lazy.nvim
    │   ├── options.lua                  # Opsi editor (listchars, Ruby LSP)
    │   ├── keymaps.lua                  # Custom keymaps
    │   ├── autocmds.lua                 # Autocommands (filetype, format)
    │   └── util.lua                     # Helper (toggle, cowboy — disabled)
    └── plugins/
        ├── colorscheme.lua              # TokyoNight
        ├── tokyonight.lua               # Tema TokyoNight Moon
        ├── vim-tmux-navigator.lua       # Tmux navigasi
        ├── rails-vim.lua                # Rails.vim
        ├── extend-blink.lua             # Autocomplete UI
        ├── extend-bufferline.lua        # Buffer line
        ├── extend-claudecode.lua        # Claude Code (commented out)
        ├── extend-conform.lua           # Formatter
        ├── extend-dashboard.lua         # Dashboard
        ├── extend-mason.lua             # Mason tools
        ├── extend-mini-map.lua          # MiniMap
        ├── extend-neotest.lua           # Test runner
        ├── extend-nvim-lint.lua         # Linter
        ├── extend-nvim-lspconfig.lua    # LSP config
        ├── extend-nvim-ts-autotag.lua   # Auto close tag
        ├── extend-snacks.lua            # Snacks picker/explorer
        ├── extend-treesitter.lua        # Treesitter parsers
        └── extend-trouble.lua           # Diagnostic trouble
```

---

## Referensi

- [LazyVim Keymaps](https://www.lazyvim.org/keymaps)
- [LazyVim Configuration](https://www.lazyvim.org/configuration)
