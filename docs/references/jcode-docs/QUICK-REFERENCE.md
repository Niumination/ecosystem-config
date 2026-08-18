# Quick Reference — jcode

## Perintah Utama

| Perintah | Deskripsi |
|----------|-----------|
| `jcode` | Buka TUI interaktif |
| `jcode run "prompt"` | Jalankan sekali, non-interactive |
| `jcode --resume <nama>` | Resume session |
| `jcode serve` | Jalankan background server |
| `jcode connect` | Attach ke server |
| `jcode dictate` | Voice input (STT) |
| `jcode --version` | Cek versi |

## Provider

| Perintah | Deskripsi |
|----------|-----------|
| `jcode login --provider claude` | Login Claude |
| `jcode login --provider openai` | Login OpenAI |
| `jcode login --provider copilot` | Login Copilot |
| `jcode login --provider gemini` | Login Gemini |
| `jcode login --provider <p> --no-browser` | Headless login |
| `jcode auth-test --all-configured` | Test semua provider |
| `jcode --provider-profile <name> run "prompt"` | Run dengan profile spesifik |

## Browser

| Perintah | Deskripsi |
|----------|-----------|
| `jcode browser status` | Cek status browser |
| `jcode browser setup` | Setup Firefox bridge |

## Hotkey Default

| Shortcut | Aksi |
|----------|------|
| `Enter` | Kirim input (interleaved) |
| `Shift+Enter` | Kirim input (queue send) |
| `Alt+C` | Toggle centered alignment |
| `Ctrl+C` | Interrupt agent |
| `Ctrl+D` | Exit TUI |

## Keybindings Custom (Sudah Dikonfigurasi)

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

## Slash Commands

| Command | Deskripsi |
|---------|-----------|
| `/alignment` | Ganti alignment mode |
| `/account` | Switch account (multi-provider) |
| `/skill <nama>` | Aktivasi skill manual |
| `/resume` | Resume session dari harness lain |
| `/exit` | Keluar dari TUI |

## File Config

| File | Deskripsi |
|------|-----------|
| `~/.jcode/config.toml` | Config utama (provider, model, UI, keybindings) |
| `~/.jcode/mcp.json` | Global MCP servers |
| `.jcode/mcp.json` | Project-local MCP servers |
| `~/.jcode/auth.json` | Auth credentials |
| `~/.jcode/pending-login/` | Pending login state |
| `~/.config/jcode/openai-compatible.env` | Env untuk openai-compatible provider |

## Environment Variables

| Variable | Deskripsi |
|----------|-----------|
| `JCODE_NO_TELEMETRY=1` | Disable telemetry |
| `OPENROUTER_API_KEY` | OpenRouter API key (sudah diset) |
| `ANTHROPIC_API_KEY` | Claude API key |
| `OPENAI_API_KEY` | OpenAI API key |
| `JCODE_BING_API_KEY` | Bing API key (untuk websearch fallback) |
| `RUSTC_WRAPPER=sccache` | Cache untuk build Rust |

## Direktori Penting

| Path | Deskripsi |
|------|-----------|
| `~/.jcode/` | Config & data jcode |
| `~/.jcode/skills/` | Global skills |
| `.jcode/skills/` | Project-local skills |
| `~/.config/jcode/` | App config (env files) |
| `/usr/local/Cellar/jcode/` | Homebrew install location |

## Config Saat Ini

### Provider
```toml
[provider]
default_provider = "openrouter"
default_model = "z-ai/glm-4.5-air:free"
```

### Fitur Aktif
```toml
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

## Model Gratis di OpenRouter

| Model ID | Nama | Keterangan |
|----------|------|------------|
| `z-ai/glm-4.5-air:free` | GLM 4.5 Air | ✅ Aktif digunakan |
| `qwen/qwen3-coder:free` | Qwen3 Coder 480B | Bagus untuk coding, kadang rate-limited |
| `minimax/minimax-m2.5:free` | MiniMax M2.5 | Alternatif |
| `deepseek/deepseek-v4-flash:free` | DeepSeek V4 Flash | Kualitas rendah |
| `google/gemma-4-31b-it:free` | Google Gemma 4 31B | Alternatif |
| `openai/gpt-oss-120b:free` | GPT-OSS 120B | Alternatif |

Semua model `:free` **tidak consume credits** OpenRouter.

## Performa Reference

| Metric | jcode | Claude Code | Cursor |
|--------|-------|-------------|--------|
| RAM (1 session) | ~28 MB | ~387 MB | ~215 MB |
| RAM (10 sessions) | ~117 MB | ~2301 MB | ~1632 MB |
| Time to first frame | ~14 ms | ~3437 ms | ~1950 ms |
| Time to first input | ~49 ms | ~3513 ms | ~1979 ms |

## Troubleshooting

### Provider tidak terdeteksi
```bash
jcode auth-test --all-configured
```

### Model rate-limited
Ganti model di `~/.jcode/config.toml`:
```toml
[provider]
default_model = "minimax/minimax-m2.5:free"
```

### Cache Claude cold (>5 menit)
UI akan warning — jcode memberitahu jika ada unexpected cache miss.

### Login stuck
```bash
# Hapus pending login
rm -rf ~/.jcode/pending-login/
# Login ulang
jcode login --provider <name>
```

### Browser tool tidak jalan
```bash
jcode browser status
jcode browser setup
```

### Update jcode
```bash
brew update && brew upgrade jcode
```
