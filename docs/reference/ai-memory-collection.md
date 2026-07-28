# 🧠 AI-Memory-Collection

**Lokasi:** `~/Desktop/AI-Memory-Collection/`
**Ukuran:** ~1.73 GB (12 AI tools)
**Dikumpulkan:** 2026-07-16 oleh JCode agent

Kompilasi memori, konfigurasi, dan cache dari seluruh AI tools yang terinstall di sistem macOS. Berfungsi sebagai **unified knowledge base** dan backup konfigurasi agent.

## 📋 Daftar Tools

| # | Tool | Folder | Ukuran | Isi Penting |
|---|------|--------|--------|-------------|
| 01 | Claude Code CLI | `01-claude-code/` | 1.8 MB | History, settings, project sessions |
| 02 | Claude Desktop | `02-claude-desktop/` | 7.8 MB | Konfigurasi desktop, local agent |
| 03 | JCode (current) | `03-jcode/` | 69 MB | **499 sessions**, memory events, model cache |
| 04 | Codex | `04-codex/` | 3.0 MB | Goals DB, logs, memories |
| 05 | OpenCode | `05-opencode/` | 17 MB | Config, **146 skills**, plugins |
| 06 | GitHub Copilot | `06-github-copilot/` | 8 KB | Apps & versions |
| 07 | Continue.dev | `07-continue-dev/` | 8 KB | Config with OpenCode Zen provider |
| 08 | AionUI | `08-aionui/` | 8 KB | Skills, assistants, cron |
| 09 | Niu-Odysseus Models | `09-niu-odysseus-models/` | **1.4 GB** | GGUF: LFM2-350M, Qwen3.5-2B |
| 10 | **Orca Agent Hooks** | `10-orca-hooks/` | 52 KB | ⚡ Hook scripts — bisa diintegrasi |
| 11 | Cursor | `11-cursor/` | 8 KB | hooks.json, herdr-agent-state |
| 12 | DuetExpertCenter | `12-duet-expert-center/` | 235 MB | macOS system AI |

## 📄 Dokumen Kunci

| Dokumen | Deskripsi |
|---------|-----------|
| `memory.md` (510 baris) | **Knowledge unified** — identitas user, konfigurasi Hermes, state DB, kanban, cron, credentials pool, semua dari 12 AI tools |
| `README.md` | Ringkasan & daftar tools (96 baris) |

## ⚡ Bagian yang Bisa Diintegrasi ke Ekosistem

1. **Script hooks** (`10-orca-hooks/`) — 12 hook scripts untuk berbagai AI agents (Claude, Cursor, Copilot, Codex, Gemini, Grok, dll). Sudah dicopy ke `scripts/hooks/`
2. **memory.md** — Kontennya sudah direferensi di `BACKLOG.md` bagian AI ECOSYSTEM
3. **OpenCode skills** (146 file) — Bisa jadi referensi untuk skill authoring

## 🔗 Referensi

- Root repo: `~/Desktop/Niumination/`
- Hermes config: `/Volumes/HermesAgent/HermesAgentUSB/data/config.yaml`
- BACKLOG.md: AI ECOSYSTEM section
