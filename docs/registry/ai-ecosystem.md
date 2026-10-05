## AI Ecosystem

| # | Agent | Role | Provider/Model | Status |
|:-:|-------|------|----------------|:------:|
| 1 | **Hermes Agent** | Main orchestrator — single gateway, 8 Telegram threads, cron, A2A, cross-thread dispatch, health monitoring | Multi-model per-thread (9router, nous, openrouter, huancheng) | ✅ **Live** — macOS 26.7.1, launchd `ai.hermes.gateway` |
| 2 | **Claude Code CLI** | Side coding agent | Anthropic — `claude-sonnet-4` | ✅ **Live** — `claude -p "..."` |
| 4 | **Codex CLI** | OpenAI coding agent | OpenAI — Codex CLI | ✅ **Live** — goals DB, logs |
| 5 | **OpenCode CLI** | Standalone coding agent | OpenCode config — 146 skills | ✅ **Live** — ACP headless |
| 6 | **GitHub Copilot** | IDE assistant | GitHub Copilot | ✅ **Live** — VS Code |

### Hermes Orkestrasi (5 Fase — 5 Okt 2026)

| Fase | Nama | Status |
|------|------|--------|
| 1 | Stabilize — cleanup dead components (orchestrator, characters, observer, MC) | ✅ Done — commit `41f5026` |
| 2 | Optimize cron routing — thread khusus 12595 untuk cron output | ✅ Done — commit `3a59b9e` |
| 3 | Cross-thread dispatch manual — `dispatch-to-thread.py` via Bot API | ✅ Done — commit `e810fc1` |
| 4 | Monitoring — `ecosystem-health.py` cron tiap 2 jam | ✅ Done — commit `2bbb330` + `7bdf4e0` |
| 5 | Future — multi-agent orchestration (optional, belum dibutuhkan) | 📌 Deferred |

**Live components:** Hermes gateway, 8 Telegram threads, A2A Mac↔Cloud, mac-relay, 9router 77 model, skill bank 230 skills, 6 cron jobs.

**Archived:** Mission Control (off), `agents/orchestrator/`, `agents/characters/`, Observer AI (not installed), Munder Difflin, model selection drafts.

### 🧠 AI-Memory-Collection

**Lokasi:** `~/Desktop/AI-Memory-Collection/` (~1.73 GB)
**Status:** ⚪ **BELUM DIVERIFIKASI** — Hermes tidak kenal folder ini. Referensi di `docs/ai-memory-collection.md` dan DOX chain butuh verifikasi langsung.
**Sumber (klaim):** Snapshot 12 AI tools dari seluruh sistem macOS (16 Jul 2026)

| Tool | Ukuran | Isi Penting |
|------|--------|-------------|
| 01 — Claude Code CLI | 1.8 MB | History, project sessions |
| 02 — Claude Desktop | 7.8 MB | Konfigurasi desktop agent |
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
