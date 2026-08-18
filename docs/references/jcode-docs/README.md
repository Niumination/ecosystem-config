# jcode Documentation

Dokumentasi instalasi, penggunaan, dan kustomisasi **jcode** — Coding Agent Harness generasi berikutnya.

> Versi terinstall: **v0.12.2** | Install via: **Homebrew** | Tanggal: **May 18, 2026**
> Provider: **OpenRouter** | Model: **z-ai/glm-4.5-air:free** (gratis)

## Daftar Isi

| Dokumen | Deskripsi |
|---------|-----------|
| [INSTALL.md](./INSTALL.md) | Langkah-langkah instalasi jcode |
| [USAGE.md](./USAGE.md) | Panduan penggunaan dasar + fitur aktif |
| [PROVIDERS.md](./PROVIDERS.md) | Setup AI provider (Claude, OpenAI, Copilot, dll) |
| [CUSTOMIZATION.md](./CUSTOMIZATION.md) | Rekomendasi kustomisasi (config, MCP, skills, browser, swarm) |
| [QUICK-REFERENCE.md](./QUICK-REFERENCE.md) | Cheat sheet perintah, hotkey, keybindings |

## Apa itu jcode?

jcode adalah **coding agent harness** berbasis terminal yang dirancang untuk:

- **Multi-session workflow** — jalankan beberapa agent secara bersamaan
- **Resource efisien** — ~27 MB RAM untuk 1 sesi (jauh lebih ringan dari Claude Code, Cursor, dll)
- **Booting cepat** — ~14ms time to first frame
- **Memory system** — embedded semantic vector untuk recall otomatis
- **Swarm mode** — multi-agent collaboration dengan conflict resolution otomatis
- **Self-dev mode** — agent bisa memodifikasi source code-nya sendiri
- **Browser automation** — kontrol browser via Firefox Agent Bridge

## Sistem

- **OS:** macOS Darwin 25.5.0 (x86_64)
- **Shell:** zsh (ZDOTDIR=$HOME/.config/zsh)
- **Package manager:** Homebrew 5.1.11
- **Install path:** `/usr/local/Cellar/jcode/0.12.2`
- **Config directory:** `~/.jcode/`

## Review Fitur — Status Saat Ini

### ✅ Fitur Aktif

| Fitur | Status | Keterangan |
|-------|--------|------------|
| **Provider** | OpenRouter | Model `z-ai/glm-4.5-air:free` (gratis) |
| **Memory** | ON | Semantic vector memory, auto-extract & recall |
| **Swarm** | ON | Multi-agent collaboration, spawn mode: visible |
| **Web Search** | DuckDuckGo | Fallback ke Bing (perlu API key) |
| **Desktop Notifications** | ON | Via ntfy.sh |
| **Message Timestamps** | ON | Tampilkan timestamp di chat |
| **Cross-provider Failover** | ON | Countdown mode |
| **Compaction** | Reactive | Auto-compress context setelah 15 turn lookahead |
| **Native Scrollbars** | ON | Chat & side panel |
| **Prompt Preview** | ON | Preview sebelum kirim |
| **Idle Animation** | ON | Animasi saat idle |
| **Mouse Capture** | ON | Support mouse di terminal |
| **Diff Mode** | Inline | Diff tampilan inline |
| **Markdown Spacing** | Compact | Spasi markdown padat |
| **Pin Images** | ON | Gambar di-pin di chat |
| **Auto Server Reload** | ON | Reload server otomatis |
| **Update Channel** | Stable | Update dari channel stable |

### ❌ Fitur Non-Aktif

| Fitur | Status | Cara Enable |
|-------|--------|-------------|
| **Ambient Mode** | OFF | `enabled = true` di `[ambient]` |
| **Memory Sidecar** | OFF | `memory_sidecar_enabled = true` di `[agents]` |
| **Browser Automation** | OFF | `jcode browser setup` (perlu Firefox) |
| **Gateway** | OFF | `enabled = true` di `[gateway]` |
| **Autoreview** | OFF | `enabled = true` di `[autoreview]` |
| **Autojudge** | OFF | `enabled = true` di `[autojudge]` |
| **Dictation (Voice)** | OFF | Set `command` di `[dictation]` |
| **Diagram Mode** | OFF | `diagram_mode = "inline"` di `[display]` |
| **Show Thinking** | OFF | `show_thinking = true` di `[display]` |
| **Centered Mode** | OFF | `Alt+C` atau `centered = true` |
