# 01 — Inventory Lengkap Aset Hermes Portable

> **Source:** `/Volumes/HermesAgent/HermesAgentUSB/data/`
> **Total size:** ~20 GB (termasuk home/, kanban/, lsp/)
> **Hermes version:** v0.16.0 (2026.6.5)
> **Config version:** `_config_version: 27`
> **Last verified:** 2026-07-18

---

## 1. File Konfigurasi Inti

| File | Ukuran | Catatan |
|------|--------|---------|
| `config.yaml` | ~13 KB | Master config — 627 baris, 541 key:value |
| `.env` | ~1.5 KB | 12 variabel environment (API keys, tokens) |
| `auth.json` | ~2.6 KB | Kredensial layanan eksternal |
| `gateway_state.json` | ~700 B | PID, status platform (Telegram connected) |
| `active_profile` | 0 bytes | Kosong — tidak ada profile aktif |
| `SOUL.md` | ~500 B | System prompt untuk agent |
| `channel_directory.json` | ~700 B | Registry channel Telegram |

## 2. Database Files

| File | Ukuran | Isi |
|------|--------|-----|
| `state.db` | **366 MB** | Session DB — 81 session files, memories, user profile |
| `kanban.db` | 1.1 MB | Kanban board — tasks, status, lanes |
| `models_dev_cache.json` | 2.9 MB | Cache model catalog dari model-catalog.json |

## 3. Skills

**Total: 29 skill categories** (direktori) dengan **107 file SKILL.md** di `/Volumes/HermesAgent/HermesAgentUSB/data/skills/`

| # | Skill | Kategori | Status |
|---|-------|----------|--------|
| 1-6 | apple-services, macos-battery-diagnostics, macos-computer-use, macos-disk-cleanup, macos-disk-maintenance, macos-security-scan | apple | ✅ |
| 7-21 | claude-code, codex, discord-gateway, hermes-agent, hermes-configuration-tuning, hermes-cross-platform-setup, hermes-fullstack-architect, hermes-mcp-plugin-management, hermes-skills-setup, hermes-zero-defect-architect, jcode, kanban-codex-lane, niu-flow, opencode, ui-ux-pro-max-setup | autonomous-ai-agents | ✅ |
| 22-41 | architecture-diagram, ascii-art, ascii-video, baoyu-article-illustrator, baoyu-comic, baoyu-infographic, claude-design, comfyui, creative-ideation, design-md, excalidraw, humanizer, manim-video, p5js, pixel-art, popular-web-designs, pretext, sketch, songwriting-and-ai-music, touchdesigner-mcp | creative | ✅ |
| 42 | jupyter-live-kernel | data-science | ✅ |
| 43-45 | kanban-orchestrator, kanban-worker, webhook-subscriptions | devops | ✅ |
| 46-47 | lkh-excel-generator, project-docs-sync | documentation | ✅ |
| 48 | dogfood | dogfood | ✅ |
| 49 | himalaya | email | ✅ |
| 50-51 | minecraft-modpack-server, pokemon-player | gaming | ✅ |
| 52 | github | github | ✅ |
| 53-54 | ekosistem-scaffold, kanban-ecosystem-management | hermes | ✅ |
| 55-58 | gif-search, heartmula, songsee, spotify | media | ✅ |
| 59 | youtube-content | media | ✅ |
| 60-61 | lm-evaluation-harness, weights-and-biases | mlops/evaluation | ✅ |
| 62 | huggingface-hub | mlops | ✅ |
| 63-65 | llama-cpp, obliteratus, vllm | mlops/inference | ✅ |
| 66-67 | audiocraft, segment-anything | mlops/models | ✅ |
| 68 | dspy | mlops/research | ✅ |
| 69 | obsidian | note-taking | ✅ |
| 70-78 | airtable, google-workspace, linear, maps, nano-pdf, notion, ocr-and-documents, powerpoint, teams-meeting-pipeline | productivity | ✅ |
| 79 | godmode | red-teaming | ✅ |
| 80-84 | arxiv, blogwatcher, llm-wiki, polymarket, research-paper-writing | research | ✅ |
| 85 | openhue | smart-home | ✅ |
| 86 | xurl | social-media | ✅ |
| 87-104 | android-ci-build, android-jetpack-compose, codebase-audit, data-migration-seeding, hermes-agent-skill-authoring, hermes-s6-container-supervision, plan-compliance-audit, **codebase-intelligence**, ponytail, portfolio-data-maintenance, project-migration, project-orientation, requesting-code-review, spike, subagent-driven-development, systematic-debugging, tauri-fullstack, test-driven-development, writing-plans | software-development | ✅ |
| 105 | ui-ux-pro-max | ui-ux-pro-max | ✅ |
| 106 | operational-dashboard | web-development | ✅ |
| 107 | yuanbao | yuanbao | ✅ |

**Total: 29 direktori skill, 107 file SKILL.md**

## 4. Plugins

Di `/Volumes/HermesAgent/HermesAgentUSB/data/plugins/`:

| Plugin | Status |
|--------|--------|
| `spotify` | ✅ Enabled (dari `known_plugin_toolsets`) |
| `rtk-rewrite` | ✅ Enabled |
| `hermes-achievements` | ❓ Installed tapi tidak di enable list |
| `codebase-intelligence` | ✅ Installed (skill + 3 scripts) |

## 5. MCP Servers (6 total)

Semua di konfigurasi `mcp_servers:` di config.yaml:

| Server | Command | Args | Path Dependence |
|--------|---------|------|-----------------|
| `time` | `/Users/zaryu/.hermes-portable/venv/bin/mcp-server-time` | — | ✅ Absolute path ke venv |
| `github` | `npx @modelcontextprotocol/server-github` | — | ✅ npx global |
| `filesystem` | `/usr/local/bin/mcp-server-filesystem` | `/Users/zaryu` | ✅ Relative ke home |
| `hermes-sqlite` | `python /Users/zaryu/.local/share/hermes-mcp/mcp-server-sqlite.py` | — | ⚠️ Absolute path |
| `hermes-postgres` | `bash /Users/zaryu/.local/share/hermes-mcp/mcp-server-postgres.sh` | — | ⚠️ Absolute path |
| `ponytail` | `node /Users/zaryu/Desktop/Niumination/tools/ponytail/ponytail-mcp/index.js` | — | ⚠️ Absolute path ke Niumination |

## 6. Cron Jobs (3 active)

Semua dikelola oleh Hermes cron system (bukan crontab macOS).

| Job ID | Nama | Schedule | Script | Status |
|--------|------|----------|--------|--------|
| ~~`2e98df211aaa`~~ | ~~brain-daily-capture~~ | ~~0 21 * * *~~ | ~~`scripts/brain-capture.py`~~ | ❌ Dihapus 5 Agu 2026 |
| `663b902a9ce5` | memory-checkpoint | 0 */6 * * * | `scripts/checkpoint.py` | ✅ Active |
| ~~`22a2fb847f4d`~~ | ~~niu-flow-weekly-audit~~ | ~~0 8 * * 1~~ | ~~(LLM-driven, skill niu-flow)~~ | ❌ Tidak ada di jobs.json |

Script path: Script di `data/scripts/` menggunakan relative path ke `$HERMES_HOME/scripts/`.

## 7. Environment Variables (12)

Dari `.env` (semua nilai [REDACTED] di dokumen ini — migrasi copy-paste langsung file):

| Variable | Source | Required for |
|----------|--------|--------------|
| `OPENCODE_ZEN_API_KEY` | .env | Provider utama |
| `TELEGRAM_BOT_TOKEN` | .env | Telegram messaging |
| `TELEGRAM_ALLOWED_USERS` | .env | Keamanan Telegram |
| `TELEGRAM_HOME_CHANNEL` | .env | Home channel |
| `GOOGLE_API_KEY` | .env | Gemini (4 fitur) |
| `GITHUB_TOKEN` | .env | GitHub API |
| `TAVILY_API_KEY` | .env | Web search |
| `OPENCODE_API_KEY` | .env | JCode |
| `OPENROUTER_API_KEY` | .env | Fallback provider |
| `SUPABASE_PG_URL` | .env | Postgres MCP |
| `VERCEL_TOKEN` | .env | Vercel deploy |
| `HERMES_CUA_DRIVER_CMD` | .env | Computer use tool |

Juga terdaftar di `env_passthrough` config:
`HOME`, `PATH`, `HERMES_HOME`, `OPENROUTER_API_KEY`, `OPENCODE_API_KEY`

## 8. Launchd / System Services

Pengecekan di `~/Library/LaunchAgents/`: **Tidak ada plist aktif** untuk Hermes atau Niumination.

Note: Sebelumnya ada `com.niumination.kanban-server` plist — mungkin sudah dihapus atau di profil lain.

## 9. State & Runtime Data

| Komponen | Lokasi | Size | Catatan |
|----------|--------|------|---------|
| **Session DB** | `data/state.db` | 366 MB | **Kritis** — 81 session files, riwayat chat |
| **Kanban DB** | `data/kanban.db` | 1.1 MB | Semua task, status, lanes |
| **Memories** | `data/memories/MEMORY.md` | 2.2 KB | Persistent memory |
| **User profile** | `data/memories/USER.md` | 1.4 KB | User preferences |
| **Sessions** | `data/sessions/` | 11 MB | 81 session files |
| **Checkpoints** | `data/checkpoints/` | 1.1 MB | State snapshots |
| **Gateway state** | `data/gateway_state.json` | 700 B | PID + platform status |
| **Auth** | `data/auth.json` | 2.6 KB | Kredensial layanan |

## 10. Data Pendukung

| Komponen | Size | Catatan |
|----------|------|---------|
| `data/home/` | **12 GB** | Virtual home (node_modules, caches, temp) |
| `data/kanban/` | 1.3 GB | Kanban worker logs, artifacts |
| `data/lsp/` | 380 MB | LSP server + node_modules |
| `data/logs/` | 34 MB | `agent.log`, `errors.log` (4 rotasi) |
| `data/backup/` | 341 MB | Auto-backup (1 backup: 2026-06-26) |
| `data/bin/tirith` | — | Tirith security binary |
| `data/scripts/` | 416 KB | 13 script files (termasuk codebase/ intelligence) |
| `data/cron/` | 1.5 MB | Cron job outputs (per-job dir) |
| `data/plugins/` | 896 KB | Plugin files |
| `data/sandboxes/` | — | Execution sandboxes |
| `data/skins/` | — | Custom skins |
| `data/cache/` | 96 KB | Temporary cache |
| `data/audio_cache/` | — | TTS audio cache |
| `data/image_cache/` | — | Image cache |
| `data/plans/` | — | Plan files |
| `data/workspace/` | — | Workspace files |
| `data/gateway/` | — | Gateway auxiliary files |
| `data/gateway-service/` | — | Service files |
| `data/hooks/` | — | Custom hooks |
| `data/pairing/` | — | Pairing files |
| `data/images/` | — | Images |
| `data/output/` | — | Command output |
| `.update_check` | 68 B | Update status cache |
| `.skills_prompt_snapshot.json` | 63 KB | Snapshot semua skill prompt |

## 11. Eksternal Dependencies (Non-Hermes)

| Dependency | Lokasi | Catatan |
|------------|--------|---------|
| Python venv | `/Users/zaryu/.hermes-portable/venv/` | Hermes runtime |
| MCP shell scripts | `/Users/zaryu/.local/share/hermes-mcp/` | 3 files |
| Ponytail MCP | `/Users/zaryu/Desktop/Niumination/tools/ponytail/` | Node.js MCP server |
| Tirith binary | `data/bin/tirith` | In Hermes data |
| Niumination ecosystem | `/Users/zaryu/Desktop/Niumination/` | Root proyek |

## 12. Ringkasan Risiko Per Komponen

| Komponen | Risiko Korup | Wajib Backup | Bisa Recreate |
|----------|:------------:|:------------:|:-------------:|
| config.yaml | 🔴 Tinggi | ✅ | ❌ (setting kustom) |
| .env | 🔴 Tinggi | ✅ | ❌ (API keys) |
| state.db | 🔴 Sangat Tinggi | ✅ | ❌ |
| kanban.db | 🟡 Sedang | ✅ | ⚠️ (bisa rebuild) |
| auth.json | 🔴 Tinggi | ✅ | ❌ |
| skills/ | 🟢 Rendah | ✅ | ✅ (bisa re-skill) |
| plugins/ | 🟢 Rendah | ✅ | ✅ (reinstall) |
| memories/ | 🟡 Sedang | ✅ | ⚠️ (konteks hilang) |
| sessions/ | 🟢 Rendah | ✅ | ✅ (histori chat aja) |
| home/ | 🟢 Rendah | ❌ | ✅ (cache + node_modules) |
| kanban/ (artifacts) | 🟢 Rendah | ❌ | ✅ (worker logs) |
| lsp/ | 🟢 Rendah | ❌ | ✅ (reinstall) |
| scripts/ | 🟢 Rendah | ✅ | ⚠️ (12 custom scripts) |
