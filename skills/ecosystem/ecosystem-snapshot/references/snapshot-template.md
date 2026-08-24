# Ecosystem Config Snapshot — YYYY-MM-DD

Generated from: `/up-eco`, `BACKLOG.md`, `system_profiler`, Hermes config, Mission Control `server.py`.

---

## 🖥️ macOS — Active Machine
- **Host:** 
- **Model:** 
- **CPU:** 
- **RAM:** 
- **GPU:** 
- **OS:** macOS XX.X (XXY) — <codename> / Darwin XX.X.X
- **Display:** 
- **Primary USB:** 
- **Active Volumes:**
  - `<path>` — writable/read-only, filesystem
  - Boot volume APFS: `<free>` free of `<capacity>`

---

## 🌐 Niumination Ecosystem — Git Status
- **Root:** `Niumination/ecosystem-config` @ `<sha>` — clean/dirty
- **Profile README:** `Niumination/Niumination` @ `<sha>` — clean/dirty
- **Brain:** `Niumination/brain` @ `<sha>` — clean/dirty
- **Dirty repos:** none / list

### Project Registry
| Repo | Category | Status | Remote |
|---|---|---|---|
| <repo1> | apps | 🟢 Active | Vercel/GitHub |
| <repo2> | services | 🟢 Active | GitHub |

---

## 📂 Filesystem Layout
- `apps/` — <count> production projects
- `services/` — <count> backend engines
- `sites/` — <count> frontend apps
- `desktop/` — <count> native apps
- `agents/` — <count> AI/automation projects
- `labs/` — <count> experiments
- `sandbox/` — <count> dormant projects
- `archive/projects/` — <count> archived
- `docs/` — <count> documentation files
- `scripts/` — <count> automation scripts
- `skills/` — <count> skills in bank pusat
- `tools/` — <count> tools
- `vault/` — secrets, gitignored
- `brain/` — Obsidian vault, git-tracked
- `dotfiles/` — terminal dotfiles, gitignored

---

## 🎛️ Mission Control
- **Port:** `http://localhost:<port>`
- **Version:** `<version>`
- **Dashboard:** `<path>`
- **Backend:** `<path>`
- **Stack:** FastAPI + Uvicorn + SQLite + WebSocket
- **Auth:** `MC_API_KEY` env var (optional/enabled)
- **CORS:** default/configured origins
- **Rate limit:** default `<n>` req/min per IP
- **Logging:** JSON logs when `MC_JSON_LOGS=true`
- **Status:** server processes observed / health check result
- **Main script:** `<path>`
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
| <id> | Active | <model> | <provider> | <count> | — |

- Last activity for all threads: YYYY-MM-DD HH:MM WIB

---

## 🧠 Skill Bank
- **Bank pusat:** <count> `SKILL.md`
- **Domains:** <breakdown>
- **INDEX.md:** sinkron/mismatch
- **Frontmatter:** semua valid / issues found
- **Duplikasi:** none / list
- **Manifest SHA-256:** sinkron (<count> skill, <count> file) / drift
- **Sync terakhir:** YYYY-MM-DD HH:MM:SS
- **Targets:** Jcode (missing/ok), Hermes USB <count> skills, Hermes <count> skills

---

## ⚙️ Hermes Config
- **Providers:**
  - `<provider1>`
  - `<provider2>` → `<url>`, mode `<mode>`, key env `<KEY_ENV>`
- **Profile:** default/<name>
- **Active model saat ini:** `<model>` via `<provider>`
- **Plugins:** enabled list
- **Free-tier fallback kandidat:** <list if any>

---

## 🌍 Deployment
- **GitHub Pages:** X/5 OK — list
- **Remote GH Pages:** X/5 OK — list
- **Vercel:** X/5 OK — list
- **Special notes:** e.g., CLI deploy, push GH not auto-deploy

---

## 🔐 Security & Notes
- **Gitleaks:** no secrets detected / issues
- **SIP:** Disabled/Enabled
- **Hermes config write protection:** active/inactive
- **Volume/filesystem constraints:** NTFS read-only paths, USB paths
- **Open issues:**
  1. <issue>
  2. <issue>

---

## 📌 Git History References
- `<repo>`: `<sha>` <message>
- `<repo>`: `<sha>` <message>

---

*Snapshot created at YYYY-MM-DD HH:MM WIB.*
