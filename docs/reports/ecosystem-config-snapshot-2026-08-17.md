# Ecosystem Config Snapshot — 2026-08-17

Generated from: `/up-eco`, `BACKLOG.md`, `server.py`, `system_profiler`, Hermes config.

---

## 🖥️ macOS — Active Machine
- **Host:** Zhall’s MacBook Pro
- **Model:** MacBookPro16,2
- **CPU:** Quad-Core Intel Core i5 @ 2.2 GHz
- **RAM:** 16 GB
- **GPU:** Intel UHD Graphics 620
- **OS:** macOS 26.5 (25F71) — TahoeRa / Darwin 25.5.0
- **Display:** 1920×1080 internal
- **Primary USB:** HermesAgent (SanDisk Ultra, 30.75 GB)
- **Active Volumes:**
  - `/Volumes/HermesAgent` — writable
  - `/Volumes/Niumination` — **read-only** NTFS (Ignore Ownership: Yes)
  - `/Volumes/Windows X-Lite` — NTFS, read-only
  - `/Volumes/Mac Win` — ExFAT, writable
  - Boot volume APFS: ~43.6 GB free of 137.4 GB

---

## 🌐 Niumination Ecosystem — Git Status
- **Root:** `Niumination/ecosystem-config` @ `4e773e8` — clean
- **Profile README:** `Niumination/Niumination` @ `5e35f06` — clean
- **Brain:** `Niumination/brain` @ `b50b0f6` — clean
- **Dirty repos:** none

### Project Registry
| Repo | Category | Status | Remote |
|---|---|---|---|
| PemdiAcehTengah | apps | 🟢 Active | Vercel |
| Niu-LKH | apps | ✅ Done | GH Pages |
| niu-vermilion | apps | 🟢 Active | Vercel |
| kune-ya.com | apps | 🟢 Active | Vercel |
| niu-dash | apps | 🟢 Active | GH Pages |
| CC.Switch | apps | 🟢 Active | GitHub |
| JHermUSB-portable | apps | ✅ Done | GitHub |
| mac-web-dashboard | apps | ✅ Done | GitHub |
| arch-web-dashboard | apps | ✅ Done | GitHub |
| ai-file-manager-android | apps | 🟢 Active | Device |
| ai-first-os | apps | ⚪ Minor | GitHub |
| Niumination | apps/profile | ⚪ Minor | GitHub |
| cc-acehtengah | services | 🟢 Active | GitHub |
| niu-mission-control | services | 🟢 Active | GitHub |
| niu-cast | services | 🟢 Active | macOS |
| Niu-Flow | services | 🟢 Remote | GitHub |
| latticesend | services | 🟢 Active | none |
| uacc | services | 🟢 Active | GitHub |
| TEDEO-Kanban | sites | 🟡 95% | GitHub |
| niu-dash-fullstack | sites | ⏸️ Stale | — |
| niu-kanban-dash | sites | ⏸️ | — |
| AuditTI-AT | sites | ✅ Live | GH Pages |
| spatial-vision | sites | 🟢 Active | — |
| Flame-ADE | desktop | ⏸️ Stale | GitHub |
| didong-code | desktop | 🟢 Active | GitHub |
| joy-connect-for-mac | desktop | 🟢 Active | GitHub |
| x-downloader | desktop | ✅ Phase 3 | GitHub |
| orchestrator | agents | ⏸️ Stale | GitHub |
| Ultra | agents | ⏸️ Stale | GitHub |
| characters | agents | 🟢 Active | local |

---

## 📂 Filesystem Layout
- `apps/` — 12 production projects
- `services/` — 7 backend engines
- `sites/` — 5 frontend apps
- `desktop/` — 4 native apps
- `agents/` — 4 AI/automation projects
- `labs/` — 3 experiments
- `sandbox/` — 7 dormant projects
- `archive/projects/` — 2 archived
- `docs/` — unified documentation
- `scripts/` — 21 automation scripts
- `skills/` — 47 skills in bank pusat
- `tools/` — Ponytail MCP
- `vault/` — secrets, gitignored
- `brain/` — Obsidian vault, git-tracked
- `dotfiles/` — terminal dotfiles, gitignored

---

## 🎛️ Mission Control
- **Port:** `http://localhost:5200`
- **Version:** `v2.6.2`
- **Dashboard:** `/Users/zaryu/Desktop/Niumination/services/niu-mission-control/dashboard`
- **Backend:** `services/niu-mission-control/backend/app/main.py`
- **Stack:** FastAPI + Uvicorn + SQLite + WebSocket
- **Auth:** `MC_API_KEY` env var (optional)
- **CORS:** default localhost only, overridable via `MC_CORS_ORIGINS`
- **Rate limit:** default 60 req/min per IP (`MC_RATE_LIMIT`)
- **Logging:** JSON logs when `MC_JSON_LOGS=true`
- **Status:** server processes observed as port-bound CLOSED in netstat; health checks timed out
- **Main script:** `services/niu-mission-control/server.py`
- **WS endpoint:** `/ws/swarm`
- **API prefix:** `/api/mc` + v1 router `/api/v1`

### v3 API Routers Present
- `/api/mc/tasks` — kanban + delegate + clear logs
- `/api/mc/agents` — fleet status
- `/api/mc/cost/agents`, `/api/mc/cost/task/{task_id}`, `/api/mc/cost/agent/{agent_id}`
- `/api/mc/telegram-feed`, `/api/mc/send-telegram`
- `/api/mc/artifacts`, `/api/mc/artifact-content`
- `/api/mc/system`, `/api/mc/config`, `/api/mc/hermes`
- `/api/mc/skills`, `/api/mc/skills/stats`, `/api/mc/skills/stale`, `/api/mc/skills/conflicts`
- `/api/mc/wal-checkpoint`, `/api/mc/ecosystem`

---

## 💬 Telegram Threads — Mission Control
| Thread | Status | Model | Provider | Messages | Last Error |
|---|---|---|---|---|---|
| 1 | Active | gemini/gemini-3... | 9router | 123 | — |
| 802 | Active | gc/gemini-2.5-pro | 9router | 85 | — |
| 803 | Active | cf/@cf/deepseek... | 9router | 7 | — |
| 804 | Active | cf/@cf/zai-org/... | 9router | 23 | — |
| 1172 | Active | gemini/gemma-4-... | 9router | 148 | — |

- Last activity for all threads: 2026-08-17 21:33 WIB

---

## 🧠 Skill Bank
- **Bank pusat:** 47 `SKILL.md`
- **Domains:** software-development 30, design 5, ecosystem 4, note-taking 3, creative 2, security 1, governance 1, autonomous-ai-agents 1
- **INDEX.md:** sinkron
- **Frontmatter:** semua valid
- **Duplikasi:** none
- **Manifest SHA-256:** sinkron (47 skill, 267 file)
- **Sync terakhir:** 2026-08-17 18:00:49
- **Targets:** Jcode (missing), Hermes USB 211 skills, Hermes 2 skills

---

## ⚙️ Hermes Config
- **Providers:**
  - `9router`
  - `huancheng` → `https://api.hcnsec.cn/v1`, mode `chat_completions`, key env `HUANCHENG_API_KEY`
- **Profile:** default
- **Active model saat ini:** `stepfun/step-3.7-flash:free` via Nous
- **Free-tier fallback kandidat:** OpenRouter 19 `:free` models

---

## 🌍 Deployment
- **GitHub Pages:** 5/5 OK — Niu-LKH, niu-dash, maze-3d, AuditTI-AT, DiskominfoAT
- **Remote GH Pages:** 5/5 OK — Niu-Startpage, niu-private, NiuHomePage, zaryu.startpage, SPBE-DevOps-Academy
- **Vercel:** 4/5 OK — PemdiAcehTengah, kune-ya.com, niu-vermilion, VirtualAssistance
- **PemdiAcehTengah:** CLI + `VERCEL_OIDC_TOKEN`, push GH tidak auto-deploy

---

## 🔐 Security & Notes
- **Gitleaks:** no secrets detected on brain commit
- **SIP:** Disabled
- **Hermes config write protection:** aktif untuk `config.yaml` USB path; gunakan `hermes config set ...`
- **Niumination volume:** NTFS read-only; write via `/Users/zaryu/Desktop/Niumination`
- **Open issues:**
  1. Mission Control server tidak merespon di port 5200
  2. Backend v3 routers ada, tetapi `app.js` belum sepenuhnya terintegrasi ke format respons v3
  3. `latticesend` belum punya remote GitHub

---

## 📌 Git History References
- `brain`: `b50b0f6` docs: add pemdi-strategi-2026, hermes-config-fix, spatial-vision skeleton
- `ecosystem-config`: `4e773e8` docs(agents): update skill registry last sync timestamp
- `Niumination` profile README: `5e35f06`

---

*Snapshot created at 2026-08-17 21:33 WIB.*
