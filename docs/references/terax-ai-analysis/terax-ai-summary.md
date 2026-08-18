# Terax AI — Analisis Lengkap

## Ringkasan Eksekutif

**Terax** adalah terminal emulator AI-native open-source yang ringan (~7MB), cross-platform (macOS, Linux, Windows), dibangun dengan **Tauri 2 + Rust + React 19**. Proyek ini dikembangkan oleh **crynta**, berlisensi **Apache-2.0**, dan saat ini berada di versi **0.7.0** (rilis terbaru v0.6.6 pada 16 Mei 2026).

- **GitHub**: https://github.com/crynta/terax-ai
- **Stars**: 4.1k | **Forks**: 426 | **Commits**: 255
- **Website**: https://terax.app

---

## Apa Itu Terax?

Terax adalah **ADE (Agentic Development Environment)** — terminal yang mengintegrasikan AI sebagai primitif native, bukan sekadar sidebar. Filosofi utamanya:

1. **AI sebagai native primitive** — agent, tools, autocomplete, voice adalah first class
2. **Ringan selalu** — binary 7-8 MB, setiap dependency harus ada justifikasinya
3. **Terminal-first** — xterm.js correctness, PTY fidelity, TUI compatibility
4. **Cross-platform parity** — macOS, Linux, Windows, WSL tanpa eksklusivitas
5. **Security by default** — path guards, SSRF protection, OSC trust, IPC sandboxing

### Apa yang BUKAN Terax:
- Bukan pengganti IDE berat (VS Code/Cursor/Zed)
- Bukan browser
- Bukan workspace general-purpose
- Bukan CLI replacement serba bisa

---

## Tech Stack

| Layer | Teknologi |
|-------|-----------|
| **Backend** | Rust (Tauri 2), `portable-pty` untuk PTY handling |
| **Frontend** | React 19, TypeScript, Vite 7 |
| **Terminal** | xterm.js + WebGL renderer |
| **Editor** | CodeMirror 6 (Vim mode, multiple themes) |
| **AI SDK** | Vercel AI SDK v6 (`ai` package) |
| **UI** | Tailwind v4, shadcn/ui, radix-ui, motion (Framer Motion) |
| **State** | Zustand |
| **Package Manager** | pnpm |

### Dependensi Rust Utama:
- `portable-pty` — native PTY backend
- `keyring` — OS keychain untuk API keys
- `ignore` + `grep-*` — fuzzy file finder & content search
- `dirs` — cross-platform home/cache directories
- `reqwest` (rustls) — HTTP client dengan SSRF protection

---

## Arsitektur

### Two-Process Model

```
+-----------------------------------------+
|           Webview (React 19)            |
|  Terminal  |  Editor  |  Explorer  | AI |
+----------------------+------------------+
                       | invoke() / Channel
+----------------------+------------------+
|          Rust Backend (Tauri)           |
|  PTY  |  FS  |  Search  |  Secrets  |   |
+-----------------------------------------+
```

**Rust (`src-tauri/`)** memiliki semua akses OS. Webview tidak pernah langsung menyentuh filesystem, proses, atau shell — semuanya melalui `invoke()` ke commands yang terdaftar di `src-tauri/src/lib.rs`.

### Modul Rust Commands:
| Command | Fungsi |
|---------|--------|
| `pty::pty_*` | Long-lived interactive PTY sessions |
| `fs::tree::*`, `fs::file::*`, `fs::mutate::*` | File explorer + editor IO |
| `fs::search::*`, `fs::grep::*` | Fuzzy file finder + content search |
| `shell::shell_run_command` | One-shot subshell exec untuk AI tools |
| `shell::shell_session_*` | Persistent agent shell dengan state |
| `shell::shell_bg_*` | Long-running background processes |
| `secrets::secrets_*` | OS keychain via `keyring` crate |

### Frontend Modules (`src/modules/`):
| Module | Fungsi |
|--------|--------|
| `terminal/` | Multi-tab xterm.js, OSC handlers, themes |
| `editor/` | CodeMirror 6 stack, language modes, vim |
| `explorer/` | File tree, fuzzy search, context actions |
| `preview/` | Auto-detected dev server preview |
| `tabs/` | Tab management, workspace CWD |
| `ai/` | Agent, sub-agents, sessions, tools, voice |
| `header/` | Top bar, inline search, window controls |
| `statusbar/` | Bottom bar, CWD breadcrumb, AI indicator |
| `shortcuts/` | Keymap registry + global shortcuts |
| `settings/` | Settings store, preferences |
| `updater/` | Auto-updater UI |

---

## Fitur Lengkap

### Terminal
- Multi-tab dengan WebGL renderer
- Native PTY backend (zsh, bash, pwsh, fish, cmd)
- Split panes
- Shell integration (cwd tracking, prompt markers via OSC 7 & OSC 133)
- Inline search, link detection, true-color
- Private terminal tabs dengan AI-context redaction
- WSL bridge sebagai workspace environment

### Editor (CodeMirror 6)
- Multi-language: TS/JS, Rust, Python, HTML/CSS, JSON, Markdown, Go, C/C++/Java/C#, PHP
- Inline AI autocomplete
- AI edit diffs (side-by-side diff tab)
- Vim mode
- 7 prebuilt themes: Tokyo Night, Nord, GitHub, Atom One, Aura, Copilot, Xcode

### File Explorer
- Catppuccin icon theme (Material Icon Theme resolver)
- Fuzzy search, keyboard navigation, inline rename, context actions

### Git / Source Control
- Source control panel (stage, commit, branch)
- Git history dengan commit graph
- Per-file diffs

### Web Preview
- Auto-detect local dev servers
- Image dan PDF viewers
- Sandboxed iframe

### AI (BYOK — Bring Your Own Key)
**Providers yang didukung:**
- OpenAI, Anthropic, Google, Groq, xAI, Cerebras
- OpenAI-compatible (custom endpoint)
- LM Studio untuk local/offline models

**Fitur AI:**
- Multi-agent dan sub-agents dengan system prompts terpisah
- Voice input (streamed transcription)
- Slash commands dan skills (reusable prompt fragments)
- Project memory via `TERAX.md`
- Tools dengan approval flow:
  - Auto-execute: `read_file`, `list_directory`, `fs_search`, `fs_grep`
  - Needs approval: `write_file`, `create_directory`, `rename`, `delete`, `run_command`
- Edit diffs — user accept/reject per hunk sebelum apply
- Auto-compact untuk long context
- Session persistence via `tauri-plugin-store`

### Security
- API keys di OS keychain (tidak pernah di disk/localStorage)
- No telemetry, no account required
- Hardened AI tool surface (filesystem, network, IPC)
- SSRF dan DNS rebinding defense pada outbound HTTP
- Trust gating di terminal escape-sequence handling
- Sandboxed preview surface
- Security deny-list untuk secret paths (`.env*`, `.ssh/`, credentials, keychain dirs)

### Platform Integration
- macOS, Linux (.deb/.rpm/AppImage), Windows (NSIS), WSL
- AUR (Arch): `yay -S terax-bin`
- Windows Explorer context-menu integration
- Auto-updater (minisign public key)
- OS keychain untuk API keys
- Custom window controls (Linux/Windows), native traffic lights (macOS)

---

## Struktur Proyek

```
terax-ai/
+-- src/                          # Frontend React
|   +-- modules/
|   |   +-- terminal/             # xterm.js terminal
|   |   +-- editor/               # CodeMirror 6 editor
|   |   +-- explorer/             # File explorer
|   |   +-- preview/              # Web preview
|   |   +-- ai/                   # AI subsystem
|   |   |   +-- lib/              # agent, sessions, composer, security
|   |   |   +-- tools/            # AI tools (read_file, write_file, dll)
|   |   |   +-- agents/           # Sub-agent registry
|   |   +-- tabs/                 # Tab management
|   |   +-- header/               # Top bar
|   |   +-- statusbar/            # Bottom bar
|   |   +-- shortcuts/            # Keyboard shortcuts
|   |   +-- settings/             # Settings
|   |   +-- updater/              # Auto-updater
|   +-- components/
|   |   +-- ui/                   # shadcn/ui primitives
|   |   +-- ai-elements/          # @ai-elements components
|   +-- App.tsx                   # Root coordinator
+-- src-tauri/                    # Rust backend
|   +-- src/
|   |   +-- lib.rs                # Main entry, plugin registration
|   |   +-- modules/
|   |   |   +-- pty/              # PTY management
|   |   |   |   +-- scripts/      # Shell init scripts (zsh, bash, pwsh)
|   |   |   |   +-- session.rs    # PTY session lifecycle
|   |   |   +-- fs/               # Filesystem operations
|   |   |   +-- shell/            # Shell command execution
|   |   |   +-- secrets/          # Keychain integration
|   +-- Cargo.toml
|   +-- capabilities/
|   |   +-- default.json          # Tauri capability allowlist
|   +-- tauri.conf.json           # Tauri config
+-- package.json
+-- pnpm-lock.yaml
+-- tsconfig.json
+-- vite.config.ts
+-- components.json               # shadcn/ui config
+-- README.md
+-- TERAX.md                      # Living architecture doc
+-- ROADMAP.md                    # Project roadmap
+-- CHANGELOG.md
+-- CONTRIBUTING.md
+-- SECURITY.md
+-- CODE_OF_CONDUCT.md
+-- LICENSE                       # Apache-2.0
```

---

## Shell Integration Detail

### Unix (zsh/bash)
Init scripts di-inject via `ZDOTDIR` (zsh) atau `--rcfile` (bash):
- Emit OSC 7 untuk cwd reporting
- Emit OSC 133 A/B/C/D untuk prompt boundaries dan exit code
- Host bisa track cwd dan detect command boundaries tanpa re-parsing prompt

### Windows (PowerShell)
- `profile.ps1` dipass via `pwsh -NoLogo -NoExit -ExecutionPolicy Bypass -File`
- Wrap user's existing `prompt` function setelah `$PROFILE` runs
- Shell priority: `pwsh.exe` (PS 7+) -> `powershell.exe` (PS 5.1) -> `cmd.exe`
- cwd dinormalisasi ke backslashes sebelum pass ke ConPTY

### ConPTY Windows Gotchas
- `SPAWN_LOCK` (Mutex) diperlukan di sekitar `openpty + spawn_command` — concurrent spawns menyebabkan stalled output pipe
- Per-session **Job Object** dengan `JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE` — memastikan semua descendant process terkill saat Terax closes

---

## AI Subsystem Detail

### Agent Architecture
```
Main Agent (Experimental_Agent)
+-- System Prompt (dari config.ts)
+-- Tools (tools.ts)
|   +-- read_file (auto)
|   +-- list_directory (auto)
|   +-- fs_search (auto)
|   +-- fs_grep (auto)
|   +-- write_file (approval)
|   +-- create_directory (approval)
|   +-- rename (approval)
|   +-- delete (approval)
|   +-- run_command (approval)
|   +-- shell_session_run (approval)
|   +-- shell_bg_spawn (approval)
+-- Sub-agents (registry)
    +-- Named sub-agents dengan system prompts sendiri
    +-- Tool subsets yang berbeda
```

### Session Management
- Conversations organized dalam named sessions
- Persisted via `tauri-plugin-store` di `terax-ai-sessions.json`
- `chatStore.ts` module-scoped `Map<sessionId, Chat<UIMessage>>`
- `AgentRunBridge` mirror active-session messages ke disk
- Auto-derive titles dari first user message
- Switching API key wipes chat map; sessions persist

### Live Context Bridge
`App.tsx` calls `setLive({ getCwd, getTerminalContext, ... })` sehingga tools bisa baca:
- CWD dari terminal yang aktif
- Last 300 lines dari buffer terminal
- Lazy by design — tidak pre-snapshot

---

## Roadmap

### Coming Next
- [ ] SSH support (PTY auth, known_hosts -> SFTP, port forwarding)
- [ ] Inline terminal auto-suggestions (history-based -> AI-powered opt-in)
- [ ] Themes dan customizations (terminal themes, UI accents, keybindings, layout)
- [ ] AI autocomplete improvements (project-aware context, lower latency)
- [ ] Drag and drop di terminal
- [ ] AI agent meta-orchestration (spawn external coding agents seperti Claude Code/OpenCode)
- [ ] More slash commands dan skills
- [ ] Approval flow improvements (YOLO/auto-approve, project-scoped policies)
- [ ] Persistent terminal sessions dan layout restore
- [ ] Test coverage expansion

### Longer Horizon
- [ ] Release automation (CHANGELOG, version bump, tag flow)
- [ ] Bundle optimization (lazy-load language packs, tree-shake)
- [ ] Selective TS -> Rust migration
- [ ] AI tools/skills sebagai installable bundles
- [ ] Live filesystem updates

### Out of Scope (TIDAK akan dibangun)
- Heavy IDE features (full LSP, debugger, refactoring engines)
- Notebook dan document workspaces
- Package manager UIs
- Full web browser features
- Telemetry, analytics, accounts
- Extension marketplaces at IDE scale
- Third-party subscription session bridges

---

## Build & Development

### Prerequisites
- Rust (stable) — https://rustup.rs
- Node 20+ dan pnpm
- Platform-specific Tauri prerequisites

### Commands
```bash
pnpm install              # Install dependencies
pnpm tauri dev            # Development mode
pnpm tauri build          # Production build
pnpm exec tsc --noEmit    # Frontend type-check
cd src-tauri && cargo clippy  # Rust lint
pnpm test                 # Run tests (vitest)
```

---

## Distribusi

| Platform | Format | Notes |
|----------|--------|-------|
| macOS | `.dmg` | Minimum macOS 10.15 |
| Linux | `.deb` | Depends: libwebkit2gtk-4.1-0, libgtk-3-0 |
| Linux | `.rpm` | Depends: webkit2gtk4.1, gtk3 |
| Linux | AppImage | Butuh FUSE, atau `--appimage-extract-and-run` |
| Linux (Arch) | AUR | `yay -S terax-bin` |
| Windows | NSIS | `currentUser` mode (no admin), WebView2 embedded |

---

## Key Technical Decisions

1. **Tabs tidak di-unmount saat switch** — hidden via `invisible pointer-events-none` agar PTY dan dev servers tetap streaming di background
2. **AiComposerProvider mounted unconditionally** — conditional wrapper akan remount seluruh tree saat keys load
3. **React 19 strict mode** double-mounts `useEffect` di dev — SPAWN_LOCK mutex serializes PTY spawns
4. **Cross-platform paths** — canonical form forward-slash di frontend, normalize di boundary
5. **Terminal input** — kirim `\r` (CR) untuk Enter, bukan `\n` (LF) — PowerShell butuh CR

---

## Statistik Bahasa

| Bahasa | Persentase |
|--------|------------|
| TypeScript | 81.9% |
| Rust | 16.3% |
| CSS | 0.9% |
| Shell | 0.5% |
| PowerShell | 0.1% |
| HTML | 0.1% |
| Lainnya | 0.2% |

---

## Kesimpulan

Terax adalah proyek yang well-architected dengan filosofi yang jelas: **terminal-first, AI-native, lightweight, cross-platform, secure**. Proyek ini aktif berkembang (255 commits, 9 releases) dengan community yang growing (4.1k stars). Area yang paling menarik untuk kontribusi adalah test coverage, bundle optimization, platform-specific bugs, dan SSH support yang ada di roadmap.
