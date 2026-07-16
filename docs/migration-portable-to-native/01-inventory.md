# 01 — Inventory Lengkap Aset Hermes Portable

> **Source:** `/Volumes/HermesAgent/HermesAgentUSB/data/`
> **Total size:** 15 GB
> **Hermes version:** v0.16.0 (2026.6.5)
> **Config version:** `_config_version: 27`

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
| `state.db` | **239 MB** | Session DB — 49 sessions, memories, user profile |
| `kanban.db` | 734 KB | Kanban board — tasks, status, lanes |
| `models_dev_cache.json` | 2.9 MB | Cache model catalog dari model-catalog.json |

## 3. Skills

**Total: 28 skills** (di `/Volumes/HermesAgent/HermesAgentUSB/data/skills/`)

| # | Skill | Kategori | Status |
|---|-------|----------|--------|
| 1 | apple-services | apple | ✅ |
| 2 | macos-battery-diagnostics | apple | ✅ |
| 3 | macos-computer-use | apple | ✅ |
| 4 | macos-disk-cleanup | apple | ✅ |
| 5 | macos-disk-maintenance | apple | ✅ |
| 6 | macos-security-scan | apple | ✅ |
| 7 | claude-code | autonomous-ai-agents | ✅ |
| 8 | codex | autonomous-ai-agents | ✅ |
| 9 | discord-gateway | autonomous-ai-agents | ✅ |
| 10 | hermes-agent | autonomous-ai-agents | ✅ |
| 11 | hermes-configuration-tuning | autonomous-ai-agents | ✅ |
| 12 | hermes-cross-platform-setup | autonomous-ai-agents | ✅ |
| 13 | hermes-fullstack-architect | autonomous-ai-agents | ✅ |
| 14 | hermes-mcp-plugin-management | autonomous-ai-agents | ✅ |
| 15 | hermes-skills-setup | autonomous-ai-agents | ✅ |
| 16 | hermes-zero-defect-architect | autonomous-ai-agents | ✅ |
| 17 | jcode | autonomous-ai-agents | ✅ |
| 18 | kanban-codex-lane | autonomous-ai-agents | ✅ |
| 19 | niu-flow | autonomous-ai-agents | ✅ |
| 20 | opencode | autonomous-ai-agents | ✅ |
| 21 | ui-ux-pro-max-setup | autonomous-ai-agents | ✅ |
| 22 | architecture-diagram | creative | ✅ |
| 23 | ascii-art | creative | ✅ |
| 24 | ascii-video | creative | ✅ |
| 25 | baoyu-article-illustrator | creative | ✅ |
| 26 | baoyu-comic | creative | ✅ |
| 27 | baoyu-infographic | creative | ✅ |
| 28 | claude-design | creative | ✅ |
| 29 | comfyui | creative | ✅ |
| 30 | creative-ideation | creative | ✅ |
| 31 | design-md | creative | ✅ |
| 32 | excalidraw | creative | ✅ |
| 33 | humanizer | creative | ✅ |
| 34 | manim-video | creative | ✅ |
| 35 | p5js | creative | ✅ |
| 36 | pixel-art | creative | ✅ |
| 37 | popular-web-designs | creative | ✅ |
| 38 | pretext | creative | ✅ |
| 39 | sketch | creative | ✅ |
| 40 | songwriting-and-ai-music | creative | ✅ |
| 41 | touchdesigner-mcp | creative | ✅ |
| 42 | jupyter-live-kernel | data-science | ✅ |
| 43 | kanban-orchestrator | devops | ✅ |
| 44 | kanban-worker | devops | ✅ |
| 45 | webhook-subscriptions | devops | ✅ |
| 46 | lkh-excel-generator | documentation | ✅ |
| 47 | project-docs-sync | documentation | ✅ |
| 48 | dogfood | dogfood | ✅ |
| 49 | himalaya | email | ✅ |
| 50 | minecraft-modpack-server | gaming | ✅ |
| 51 | pokemon-player | gaming | ✅ |
| 52 | github | github | ✅ |
| 53 | ekosistem-scaffold | hermes | ✅ |
| 54 | kanban-ecosystem-management | hermes | ✅ |
| 55 | gif-search | media | ✅ |
| 56 | heartmula | media | ✅ |
| 57 | songsee | media | ✅ |
| 58 | spotify | media | ✅ |
| 59 | youtube-content | media | ✅ |
| 60 | lm-evaluation-harness | mlops/evaluation | ✅ |
| 61 | weights-and-biases | mlops/evaluation | ✅ |
| 62 | huggingface-hub | mlops | ✅ |
| 63 | llama-cpp | mlops/inference | ✅ |
| 64 | obliteratus | mlops/inference | ✅ |
| 65 | vllm | mlops/inference | ✅ |
| 66 | audiocraft | mlops/models | ✅ |
| 67 | segment-anything | mlops/models | ✅ |
| 68 | dspy | mlops/research | ✅ |
| 69 | obsidian | note-taking | ✅ |
| 70 | airtable | productivity | ✅ |
| 71 | google-workspace | productivity | ✅ |
| 72 | linear | productivity | ✅ |
| 73 | maps | productivity | ✅ |
| 74 | nano-pdf | productivity | ✅ |
| 75 | notion | productivity | ✅ |
| 76 | ocr-and-documents | productivity | ✅ |
| 77 | powerpoint | productivity | ✅ |
| 78 | teams-meeting-pipeline | productivity | ✅ |
| 79 | godmode | red-teaming | ✅ |
| 80 | arxiv | research | ✅ |
| 81 | blogwatcher | research | ✅ |
| 82 | llm-wiki | research | ✅ |
| 83 | polymarket | research | ✅ |
| 84 | research-paper-writing | research | ✅ |
| 85 | openhue | smart-home | ✅ |
| 86 | xurl | social-media | ✅ |
| 87 | android-ci-build | software-development | ✅ |
| 88 | android-jetpack-compose | software-development | ✅ |
| 89 | codebase-audit | software-development | ✅ |
| 90 | data-migration-seeding | software-development | ✅ |
| 91 | hermes-agent-skill-authoring | software-development | ✅ |
| 92 | hermes-s6-container-supervision | software-development | ✅ |
| 93 | plan-compliance-audit | software-development | ✅ |
| 94 | ponytail | software-development | ✅ |
| 95 | portfolio-data-maintenance | software-development | ✅ |
| 96 | project-migration | software-development | ✅ |
| 97 | project-orientation | software-development | ✅ |
| 98 | requesting-code-review | software-development | ✅ |
| 99 | spike | software-development | ✅ |
| 100 | subagent-driven-development | software-development | ✅ |
| 101 | systematic-debugging | software-development | ✅ |
| 102 | tauri-fullstack | software-development | ✅ |
| 103 | test-driven-development | software-development | ✅ |
| 104 | writing-plans | software-development | ✅ |
| 105 | ui-ux-pro-max | ui-ux-pro-max | ✅ |
| 106 | operational-dashboard | web-development | ✅ |
| 107 | yuanbao | yuanbao | ✅ |

**Total: ~107 skill files (SKILL.md) di 28 kategori + 1 skill ekstra**

## 4. Plugins

Di `/Volumes/HermesAgent/HermesAgentUSB/data/plugins/`:

| Plugin | Status |
|--------|--------|
| `spotify` | ✅ Enabled (dari `known_plugin_toolsets`) |
| `rtk-rewrite` | ✅ Enabled |
| `hermes-achievements` | ❓ Installed tapi tidak di enable list |

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
| `2e98df211aaa` | brain-daily-capture | 0 21 * * * | `scripts/brain-capture.py` | ⚠️ Error (script path?) |
| `663b902a9ce5` | memory-checkpoint | 0 */6 * * * | `scripts/checkpoint.py` | ✅ OK |
| `22a2fb847f4d` | niu-flow-weekly-audit | 0 8 * * 1 | (LLM-driven, skill niu-flow) | ✅ OK |

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
| **Session DB** | `data/state.db` | 239 MB | **Kritis** — 49 sessions, riwayat chat |
| **Kanban DB** | `data/kanban.db` | 734 KB | Semua task, status, lanes |
| **Memories** | `data/memories/MEMORY.md` | 2.2 KB | Persistent memory |
| **User profile** | `data/memories/USER.md` | 1.4 KB | User preferences |
| **Sessions** | `data/sessions/` | 11 MB | 49 session files |
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
| `data/scripts/` | 416 KB | 12 script files |
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
