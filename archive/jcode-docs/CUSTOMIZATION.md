# Rekomendasi Kustomisasi jcode

## 1. Config File (`~/.jcode/config.toml`)

### Config Saat Ini
```toml
[provider]
default_provider = "openrouter"
default_model = "z-ai/glm-4.5-air:free"

[features]
memory = true
swarm = true
message_timestamps = true

[websearch]
engine = "duckduckgo"
fallback_engines = ["bing"]

[safety]
desktop_notifications = true

[compaction]
mode = "reactive"
lookahead_turns = 15
```

### Model dengan Context Window Besar
```toml
[[providers.openrouter.models]]
id = "z-ai/glm-4.5-air:free"
context_window = 128000
```

## 2. Enable Fitur yang Masih Non-Aktif

### Ambient Mode (Auto-Work Saat Idle)
```toml
[ambient]
enabled = true
allow_api_keys = false
min_interval_minutes = 5
max_interval_minutes = 120
pause_on_active_session = true
proactive_work = true
work_branch_prefix = "ambient/"
visible = true
```
Agent akan otomatis bekerja saat tidak ada sesi aktif, membuat branch `ambient/` untuk perubahan.

### Memory Sidecar (AI Verification untuk Memory)
```toml
[agents]
memory_sidecar_enabled = true
```
Sideagent akan verify memory yang di-retrieve, potentially do more work untuk information retrieval.

### Browser Automation
```bash
# Install Firefox
brew install --cask firefox

# Setup jcode browser
jcode browser setup
```
Setelah setup, agent bisa menggunakan `browser` tool untuk buka URL, screenshot, klik, ketik, dll.

### Dictation / Voice Input
```bash
# Install STT tool (contoh: whisper)
brew install openai-whisper

# Set di config:
[dictation]
command = "whisper --model base --language en"
mode = "send"
key = "off"
timeout_secs = 90
```

### Diagram Mode (Mermaid)
```toml
[display]
diagram_mode = "inline"  # atau "side_panel"
```
Render mermaid diagrams inline di chat atau side panel.

### Show Thinking
```toml
[display]
show_thinking = true
```
Tampilkan proses berpikir/reasoning agent di chat.

### Centered Mode
```toml
[display]
centered = true
```
Atau toggle saat runtime dengan `Alt+C`.

### Gateway (API Server)
```toml
[gateway]
enabled = true
port = 7643
bind_addr = "0.0.0.0"
```
Expose jcode sebagai API server.

### Autoreview
```toml
[autoreview]
enabled = true
```
Auto-review code changes.

### Autojudge
```toml
[autojudge]
enabled = true
```
Auto-judge safety/approval.

---

## 3. MCP Server Configuration

MCP (Model Context Protocol) memungkinkan integrasi tool eksternal.

### Global MCP Config
File: `~/.jcode/mcp.json`

```json
{
  "servers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/workspace"],
      "env": {},
      "shared": true
    },
    "database": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres", "postgresql://localhost/mydb"],
      "env": {},
      "shared": true
    }
  }
}
```

### Project-Local MCP Config
File: `.jcode/mcp.json` (di root project)

```json
{
  "servers": {
    "custom-tool": {
      "command": "/path/to/mcp-server",
      "args": ["--config", "custom.json"],
      "env": {"MY_VAR": "value"},
      "shared": false
    }
  }
}
```

### Fallback dari Claude/Codex
jcode otomatis import dari:
- `~/.claude/mcp.json`
- `~/.codex/config.toml`

(jika `~/.jcode/mcp.json` belum ada)

## 4. Skills

Skills tidak diload semua saat startup. jcode menggunakan semantic embedding untuk inject skill yang relevan.

### Lokasi Skills
- Global: `~/.jcode/skills/`
- Project: `.jcode/skills/`

### Aktivasi Skill
- Otomatis via embedding similarity
- Manual: `/skill <nama-skill>` atau gunakan skill tool

### Membuat Skill Kustom
Buat folder di `.jcode/skills/` dengan file `SKILL.md`:

```markdown
# nama-skill

Deskripsi singkat skill ini.

## Trigger
Kapan skill ini harus aktif.

## Instructions
Langkah-langkah yang harus diikuti agent.
```

## 5. Keybindings Custom

Keybindings yang sudah dikonfigurasi di `~/.jcode/config.toml`:

| Aksi | Shortcut |
|------|----------|
| Scroll up | `Ctrl+K` |
| Scroll down | `Ctrl+J` |
| Scroll page up | `Alt+U` |
| Scroll page down | `Alt+D` |
| Switch model next | `Ctrl+Tab` |
| Switch model prev | `Ctrl+Shift+Tab` |
| Increase effort | `Alt+Right` |
| Decrease effort | `Alt+Left` |
| Toggle centered | `Alt+C` |
| Scroll prompt up | `Ctrl+[` |
| Scroll prompt down | `Ctrl+]` |
| Scroll bookmark | `Ctrl+G` |
| Workspace left | `Alt+H` |
| Workspace down | `Alt+J` |
| Workspace up | `Alt+K` |
| Workspace right | `Alt+L` |
| Session picker enter | `new-terminal` |

### Tambah Keybinding Baru
Edit `[keybindings]` di `~/.jcode/config.toml`.

## 6. Optimasi Performa

### RAM Minimal
```bash
# Disable local embedding jika butuh RAM minimal
jcode --no-local-embedding
```

### Fast Boot
jcode sudah optimal (~14ms TTFF). Tidak perlu tuning khusus.

### sccache untuk Build
```bash
# Install sccache
brew install sccache

# Set environment
export RUSTC_WRAPPER=sccache
```

## 7. Alias & Shell Helper

Tambahkan ke `~/.config/zsh/06-aliases.zsh`:

```bash
alias jc='jcode'
alias jcr='jcode run'
alias jcs='jcode serve'
alias jcc='jcode connect'
alias jcl='jcode login'
alias jcb='jcode browser'
```

## 8. Environment Variables

Sudah dikonfigurasi di `~/.config/zsh/01-environment.zsh`:

```bash
# jcode telemetry opt-out
export JCODE_NO_TELEMETRY=1

# OpenRouter API key
export OPENROUTER_API_KEY="sk-or-v1-..."
```

### Tambahan yang Bisa Dikonfigurasi
```bash
# Bing API key (untuk websearch fallback)
export JCODE_BING_API_KEY="your-key"

# sccache untuk build jcode dari source
export RUSTC_WRAPPER=sccache
```

## 9. Self-Dev Mode

jcode bisa memodifikasi source code-nya sendiri:

### Cara Aktif
Katakan ke agent: "enter self dev mode"

### Workflow
1. Agent edit source code
2. Build binary
3. Test perubahan
4. Reload binary
5. Continue work

### Rekomendasi Model
Gunakan frontier model (GPT 5.5, Claude Sonnet/Opus) karena codebase jcode kompleks.

## 10. Clipboard & Side Panel

### Side Panel
- Load file: minta agent load file ke side panel
- Write: agent bisa write langsung ke side panel
- Diff viewer: gunakan side panel untuk melihat diff
- Mermaid diagrams: render inline di side panel

### Info Widgets
Info widgets hanya pakai negative space — tidak mengganggu area respons.

## 11. Pending Login State

Login state yang pending disimpan di `~/.jcode/pending-login/`:
- Auto-expire
- Cleanup otomatis saat login baru dimulai
