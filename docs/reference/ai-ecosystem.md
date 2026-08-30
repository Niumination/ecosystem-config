## AI Ecosystem

| # | Agent | Role | Provider/Model | Status |
|:-:|-------|------|----------------|:------:|
| 1 | **Hermes Agent** | Main orchestrator | Opencode Zen — `opencode/hy3-free/nemotron-3-ultra-free` | ✅ **Live** — $1/M in, $5/M out |
| 2 | **Claude Code CLI** | Side coding agent | Anthropic — `claude-sonnet-4` | ✅ **Live** — `claude -p "..."` |
| 3 | **JCode** | Hermes↔OpenCode bridge | `OPENCODE_API_KEY` via Niu-Flow pipeline | ✅ **Live** — 5 commits |
| 4 | **Codex CLI** | OpenAI coding agent | OpenAI — Codex CLI | ✅ **Live** — goals DB, logs |
| 5 | **OpenCode CLI** | Standalone coding agent | OpenCode config — 146 skills | ✅ **Live** — ACP headless |
| 6 | **GitHub Copilot** | IDE assistant | GitHub Copilot | ✅ **Live** — VS Code |

### 🧠 AI-Memory-Collection

**Lokasi:** `~/Desktop/AI-Memory-Collection/` (~1.73 GB)
**Status:** ⚪ **BELUM DIVERIFIKASI** — Hermes tidak kenal folder ini. Referensi di `docs/ai-memory-collection.md` dan DOX chain butuh verifikasi langsung.
**Sumber (klaim):** Snapshot 12 AI tools dari seluruh sistem macOS (16 Jul 2026)

| Tool | Ukuran | Isi Penting |
|------|--------|-------------|
| 01 — Claude Code CLI | 1.8 MB | History, project sessions |
| 02 — Claude Desktop | 7.8 MB | Konfigurasi desktop agent |
| 03 — JCode | 69 MB | **499 sessions**, memory events |
| 04 — Codex | 3.0 MB | Goals DB, logs, memories |
| 05 — OpenCode | 17 MB | Config, **146 skills**, plugins |
| 06 — GitHub Copilot | 8 KB | Apps & versions |
| 07 — Continue.dev | 8 KB | Config (OpenCode Zen provider) |
| 08 — AionUI | 24 KB | Skills, assistants, cron |
| 09 — Niu-Odysseus Models | **1.4 GB** | GGUF: LFM2-350M, Qwen3.5-2B |
| 10 — Orca Hooks | 52 KB | 12 hook scripts ✅ dicopy ke `scripts/hooks/` |
| 11 — Cursor | 8 KB | hooks.json, herdr-agent-state |
| 12 — DuetExpertCenter | 235 MB | macOS system AI |

**Dokumen kunci:** `memory.md` (510 baris) — unified knowledge dari seluruh 12 tools.
**Referensi di ekosistem:** `docs/ai-memory-collection.md`, `scripts/hooks/` (12 hooks di-copy).

---
