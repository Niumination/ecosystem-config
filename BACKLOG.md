# 📋 BACKLOG — Niumination Ecosystem — MASTER DOCUMENTATION

> **UPDATE: July 28, 2026** — Sync real filesystem state setelah 11 hari tidak diupdate (sejak Jul 17).
> Perubahan besar: cc-acehtengah +27 commit, niu-mission-control +33 commit, PemdiAcehTengah 57 bukti dukung.

---

## 🗂️ Struktur Root Ekosistem — Niumination v4.0 — Jul 29, 2026

```
Desktop/Niumination/
├── apps/               🏭 12 proyek — deployed & battle-tested
├── services/           🔧 7 proyek — backend & engines
├── sites/              🌐 5 proyek — frontend apps
├── desktop/            🖥️ 4 proyek — native apps
├── agents/             🤖 4 proyek — AI agents + characters + profile
├── labs/               🔬 3 proyek — experiments
├── sandbox/            🧪 7 proyek — dormant (ex-incubator)
├── archive/projects/   📦 2 proyek — archived (niuterm, terax-ai)
├── docs/               📚 Dokumentasi terpadu (reference/, reports/, notebooklm/, dox/)
├── scripts/            ⚙️ 21 ecosystem automation scripts
├── skills/             🧠 **22 skill terpusat** (Layer 1-4 ✅, design domain baru ✅)
├── tools/              🛠️ Ponytail MCP
├── vault/              🔐 Secrets & credentials (gitignored)
├── brain/              🧠 Obsidian vault (git, terpisah)
├── core/               ⚖️ Runtime internal (CONSTITUTION, ledger, runtime, templates)
├── dotfiles/              🐚 Terminal dotfiles (gitignored)
├── AGENTS.md           📋 Root DOX — AI orchestration rules
├── BACKLOG.md          📋 Master doc ini
└── .gitleaks.toml      🔒 Security config
```

---

## ⚙️ Kompresi & Backup

| Lapisan | Mekanisme | Fungsi |
|---------|-----------|--------|
| 🗂️ **File** | `BACKLOG.md` | Source of truth utama |
| 🧠 **Memory (Hermes)** | Persistent memory | Compact snapshot survive kompresi |
| 🔄 **Cron checkpoint** | `memory-checkpoint` tiap 6 jam | Backup otomatis |
| 🔍 **Session DB** | SQLite session store | Full transcript via `session_search()` |
| 📓 **Obsidian Vault** | `brain/` | Catatan harian & audit |

---

## 🎯 KANBAN SYSTEM — Jul 29, 2026

**Data source:** `kanban.db` + filesystem audit
**Board:** Niumination Ecosystem
**Status:** 12 apps, 5 services, 5 sites, 4 desktop, 4 agents, 2 labs, 7 sandbox, 2 archived, **22 skills**

### 🏭 apps/ — 12 Proyek Production

| Proyek | Status | Deploy | Aktivitas 14 Hari | Notes |
|--------|:------:|:------:|:------------------:|-------|
| **PemdiAcehTengah** | 🟢 **Active** | Vercel | **PR#4 merged 2026-08-21** | Rumus resmi PermenPANRB 8/2026 + matriks kebutuhan bukti L1-L2 (NotebookLM). Masa penilaian mandiri selesai (bukti diupload eval.spbe.go.id) |
| **Niu-LKH** | ✅ Done | GH Pages | 0 | v3.1.1 — ⚠️ Dirty 1 file |
| **niu-vermilion** | 🟢 Active | Vercel | 0 | Stable — V1-V5 fixed |
| **kune-ya.com** | 🟢 Active | Vercel | 0 | Stable — K1-K5 fixed |
| **niu-dash** | 🟢 Active | GH Pages | **+2 commit** | v2.16.8 — ⚠️ Dirty 3 file |
| **kopi-aceh-app-android** | ⚪ Sandbox | GitHub | 0 | Rancangan & source app Android Gerobak Kopi Keliling Aceh Tengah — peta gerobak, pesan QRIS, antar/jemput. Repo belum dibuat (butuh gh auth) — remote sementara ke ecosystem-config. |
| **JHermUSB-portable** | ✅ Done | GitHub | **committed 2026-08-21** | 2 file skill sync diedit + commit+push (sebelumnya dirty 8 file per BACKLOG lama — sudah tidak valid) |
| **mac-web-dashboard** | ✅ Done | GitHub | +1 | v1.0.0 |
| **arch-web-dashboard** | ✅ Done | GitHub | 0 | v1.0.0 |
| **ai-file-manager-android** | 🟢 Active | Device | 0 | Published & tested |
| **ai-first-os** | ⚪ Minor | GitHub | 0 | Build kit |
| **Niumination** | ⚪ Minor | GitHub | **+7 commit** | Profile config |
| **CC.Switch** | 🟢 **Active** | GitHub | **+8 commit** | Tauri 2 multi-CLI |

### 🔧 services/ — 7 Backend & API

| Proyek | Priority | Status | Aktivitas 14 Hari | Notes |
|--------|:--------:|:------:|:------------------:|-------|
| **cc-acehtengah** | **P2 ⬆** | 🟢 **Active** | **+27 commit** 🏆 | Tema Gayo Highlands, Analytics, GIS, AI orchestrator, QueryBar |
| **niu-mission-control** | **P2 ⬆** | 🟢 **Active** | **+33 commit** 🏆 | v2.6.2 — UP 2026-08-21 (venv lokal recreate, symlink USB rusak). Port 5200 live, health ok |
| **niu-cast** | P2 | 🟢 **Active** | **+27 commit** | v3.6.0 — Mac Connect Bridge, macOS native install |
| **Niu-Flow** | P2 | 🟢 **Remote only** | ✅ GitHub | github.com/Niumination/niu-flow |
| **latticesend** | P3 | 🟢 Active | +1 | P2P file transfer — ✅ sudah punya remote (audit 2026-08-21) |
| **uacc** | P2 🆕 | 🟢 Active | +new | Universal AI Computer Control — MCP server |
| **camofox-browser** | P3 🆕 | ⚪ Third-party | 0 | Anti-detection browser (jo-inc/camofox-browser) — dependency browser toolset |

### 🌐 sites/ — 5 Frontend

| Proyek | Priority | Status | Aktivitas 14 Hari | Notes |
|--------|:--------:|:------:|:------------------:|-------|
| **TEDEO-Kanban** | P2 | 🟡 95% | +1 | Vite/React/Zustand |
| **niu-dash-fullstack** | P3 | ⏸️ Stale | +1 | Next.js 16 |
| **niu-kanban-dash** | P3 | ⏸️ | 0 | Vite/React |
| **AuditTI-AT** (`sites/audit-ti-at/`) | P3 | ✅ Live | 0 | GH Pages |
| **spatial-vision** | P3 | 🟢 Active | +1 | 3D vision |

### 🖥️ desktop/ — 4 Native

| Proyek | Priority | Status | Aktivitas 14 Hari | Notes |
|--------|:--------:|:------:|:------------------:|-------|
| **Flame-ADE** | P2 | ⏸️ Stale | 0 | Tauri/Rust |
| **didong-code** | P2 | 🟢 Active | 0 | Electron ADE Gayo |
| **joy-connect-for-mac** | P2 🆕 | 🟢 Active | 0 | Swift/ADB bridge |
| **x-downloader** | P3 | ✅ Phase 3 | 0 | Tauri 2 |

### 🤖 agents/ — 4 AI & Automation

| Proyek | Priority | Status | Notes |
|--------|:--------:|:------:|-------|
| **profile** (`Niumination/Niumination`) | ⚪ Minor | 🟢 Live | Animated terminal README |
| **orchestrator** | P3 | ⏸️ Stale | Python multi-agent |
| **Ultra** | P3 | ⏸️ Stale | Puppeteer automation |
| **characters/** | ⚪ | 🟢 Active | 4 herdr agents (arsitek, pembangun, pengawas, penjaga) |
| **_shared/** | ⚪ | 🟢 Active | Incident & path registry (INCIDENT.md, PATHS.md) |

### 🔬 labs/ — 3 Experiments

| Proyek | Priority | Status | Notes |
|--------|:--------:|:------:|-------|
| **maze-3d** | P3 | ✅ Live | GH Pages |
| **niumination-workspace** | P3 | ⏸️ Stale | Next.js 16 |
| **eKinerja-AfrizalMunthe** | ⚪ Minor | 🟢 Active | Bukti dukung eKinerja Sem 1 2026 (SKP/DEKP/PAK) — 🔒 private repo |

### 🧪 sandbox/ — 7 Dormant (ex-incubator)

| Proyek | Last Activity | Alasan |
|--------|:------------:|--------|
| niu-studio | Stale 38d | Dual lockfile |
| niude | Stale 31d | Low priority |
| niutui | Stale 13d | Low priority |
| zen | Stale 42d | acehtengah-web/ |
| aistudio-google | Stale | Game files only |
| arena.ai | Stale | Eksperimen |
| x-downloader-backup | Stale | Backup of x-downloader |

### 📦 archive/projects/ — 2 Archived

| Proyek | Size | Alasan |
|--------|:----:|--------|
| niuterm | 621MB | Stale 64 hari |
| terax-ai | 216MB | Stale 58 hari |

---

## 📊 SCOREBOARD EKOSISTEM — Jul 28, 2026

```
Proyek               Kematangan     Prio  Status    Git  Remote    Deploy      Lokasi (baru)
─────────────────────────────────────────────────────────────────────────────────────────
PemdiAcehTengah      ██████████ 95% P1    🟢 Active ✅   ✅ SSH    🟢 Vercel   apps/
cc-acehtengah        ██████████ 90% P2 ⬆  🟢 Active ✅   ✅ SSH    🟢 GitHub   services/
niu-mission-control  ██████████ 85% P2 ⬆  🟢 Active ✅   ✅ SSH    🟢 GitHub   services/
niu-cast             ██████████ v3.6.0 P2 🟢 Active ✅   ✅ SSH    ⚪ macOS    services/
Niu-LKH              ██████████ 100% ✅    ✅ Done   ✅   ✅ SSH    🟢 GH Page  apps/
niu-vermilion        ██████████ V1-V5 P1   🟢 Active ✅   ✅ SSH    🟢 Vercel   apps/
kune-ya.com          ██████████ K1-K5 P1   🟢 Active ✅   ✅ SSH    🟢 Vercel   apps/
TEDEO-Kanban         ██████████ 95% P2     🟡 95%     ✅   ✅ SSH    ✅ GitHub   sites/
CC.Switch            ██████████ v3.17.0 P2 🟢 Active  ✅   ✅ SSH    🟢 GitHub   apps/
Niu-Flow             ██████████ 90% P2     🟢 Remote  ✅   ✅ SSH    🟢 GitHub   services/ (remote only)
Flame-ADE            ██████████ v1.3.0 P2  ⏸️ Stale   ✅   ✅ SSH    ✅ GitHub   desktop/
niu-dash             ██████████ v2.16.8 P2 🟢 Active  ✅   ✅ SSH    🟢 GH Page apps/
JHermUSB-portable    ██████████ 100% ✅ P2 ✅ Done    ✅   ✅ SSH    🟢 GitHub   apps/
mac-web-dashboard    ██████████ v1.0.0 ✅  ✅ Done    ✅   ✅ SSH    🟢 GitHub   apps/
arch-web-dashboard   ██████████ v1.0.0 ✅  ✅ Done    ✅   ✅ SSH    🟢 GitHub   apps/
ai-file-manager      ██████████ 100% P1    🟢 Active ✅   ✅ SSH    🟢 Device   apps/
ai-first-os          █████░░░░░ 45%        ⚪ Minor   ✅   ✅ SSH    🟢 GitHub   apps/
brain                ██████░░░░ 60% P3     🟢 Active  ✅   ✅ SSH    ❌ local     root/
didong-code          ██████░░░░ 50% P2     🟢 Active  ✅   ✅ SSH    ✅ GitHub   desktop/
joy-connect-for-mac  ██████░░░░ 60% P2     🟢 Active  ✅   ✅ SSH    🟢 GitHub   desktop/
x-downloader         ██████████ 100% P3    ✅ Phase 3  ✅   ✅ SSH    🟢 GitHub   desktop/
orchestrator         ██████░░░░ 40% P3     ⏸️ Stale   ✅   ✅ SSH    ✅ GitHub   agents/
Ultra                ████████░░ 80% P3     ⏸️ Stale   ✅   ✅ SSH    ✅ GitHub   agents/
```

### sandbox/ (Dormant)

```
niu-studio            ██████░░░░ 60% P3     Stale     sandbox/
niude                 ██████░░░░ 50% P3     Stale     sandbox/
niutui                ██████░░░░ 20% P3     Stale     sandbox/
zen                   ██░░░░░░░░ 20% P3     Stale     sandbox/
aistudio-google       ██░░░░░░░░ 10% P3     Stale     sandbox/
arena.ai              ██░░░░░░░░ 10% P3     Stale     sandbox/
x-downloader-backup   ░░░░░░░░░░ —          Stale     sandbox/
```

---

## 📊 FILESYSTEM AUDIT — Real Count (Jul 29, 2026 — Ecosystem v4.0)

```
Kategori                 Count  Size    Notes
─────────────────────────────────────────────
apps/                     12   10 GB    Production & deployed
services/                  5   2.1 GB   Backend engines
sites/                     5   1.3 GB   Frontend apps
desktop/                   4   949 MB   Native apps
agents/                    4   33 MB    AI agents + profile + characters
labs/                      3   1.2 GB   Experiments
sandbox/                   7   600 MB   Dormant (ex-incubator)
archive/projects/          2   837 MB   Archived (niuterm, terax-ai)
core/                      1   440 KB   Runtime internal (CONSTITUTION, ledger, runtime, templates)
docs/                     24   240 KB   Documentation (merged from docs/dox/reports)
scripts/                  21   128 KB   Automation scripts
tools/                     1   25 MB    Ponytail MCP
vault/                     3   10 KB    Secrets (gitignored)
brain/                     1   25 MB    Obsidian vault (git, terpisah)
dotfiles/                     1   7.3 MB   Terminal dotfiles
─────────────────────────────────────────────
Total git repos           ~41   18 GB
```

### ⚠️ Dirty Repos (0 — all resolved 2026-08-21)

Semua repo bersih per audit 2026-08-21 (45 repo discan). 3 repo yang sempat dirty telah di-commit+push:
1. `dotfiles/zaryu-terminal-dotfiles` — lazy-lock.json
2. `brain` — ops/ (untracked → committed)
3. `apps/JHermUSB-portable` — 2 file skill sync

Sebelumnya (BACKLOG Jul 28) mencatat niu-dash/Niu-LKH dirty — sudah tidak valid (verified clean 2026-08-21).

---

## 🔐 DEPLOYMENT TRACKING

| Target | Status | Detail |
|--------|:------:|--------|
| GH Pages (lokal) | 5/5 ✅ | Niu-LKH, niu-dash, maze-3d, AuditTI-AT, DiskominfoAT |
| GH Pages (remote) | 5/5 ✅ | Niu-Startpage, niu-private, NiuHomePage, zaryu.startpage, SPBE-DevOps-Academy |
| Vercel | 4/5 ✅ | PemdiAcehTengah, kune-ya.com, niu-vermilion, VirtualAssistance |

---

## 🧠 AI ECOSYSTEM

| Komponen | Provider | Model | Status |
|:---------|:---------|:------|:------:|
| **Hermes (main)** | opencode-zen | **nemotron-3-ultra-free** (default) / hy3-free / big-pickle | ✅ **Live** (free tier) |
| **Nous Portal** | OAuth2 Hermes | model `:free` ter-update | ✅ **Live** (login aktif, exp 13:43 WIB) |
| **Claude Code** | ANTHROPIC_API_KEY | claude-sonnet-4 | ✅ **Live** |
| **JCode** | OPENCODE_API_KEY | — | ✅ **Live** (billing dead) |
| **Delegation** | gemini | gemini-2.5-flash | ✅ Off (concurrent=1, depth=0) |
| **AI-Memory-Collection** | 12 AI tools | Snapshot ~1.7GB | ✅ **Referenced** |

---

## 🚀 Aktivitas 14 Hari (Jul 14 — Jul 28)

| Proyek | Commits | Highlight |
|--------|:-------:|-----------|
| **niu-mission-control** | **33** | Ecosystem scanner, sidebar, gateway monitoring, v2.6.0 |
| **cc-acehtengah** | **27** | Tema Gayo Highlands, Analytics, GIS, AI orchestrator, QueryBar |
| **niu-cast** | **27** | v3.6.0, Mac Connect Bridge, macOS native install |
| **PemdiAcehTengah** | **3** | 57 bukti dukung + preview + 42 file lampiran |
| **cc-switch** | **8** | Tauri 2, build fixes |
| **Niumination (profile)** | **7** | Rename + automation |

### ⏸️ Stale (0 commit 14 hari):
Ultra, AuditTI-AT, Niu-Flow, didong-code, x-downloader, flame-ade, niu-vermilion, kune-ya.com, arch-web-dashboard, ai-file-manager-android, Niu-LKH, JHermUSB-portable, incubator/*

---

## 🔴 Perubahan Hari Ini — Jul 29, 2026 — Niumination Ecosystem v4.0

- 🏛️ **Ecosystem restructure** — Ekosistem diorganisir ulang ke maturity pipeline:
  - `Production/` → `apps/` (12 proyek deployed)
  - `projects/` → split ke `services/` (5), `sites/` (5), `desktop/` (4), `agents/` (2), `labs/` (2)
  - `incubator/` → `sandbox/` (7 dormant)
  - `characters/` → `agents/characters/`
  - `Production/Niumination` → `agents/profile/`
  - `PI/` → `vault/`
- 📚 **Dokumentasi terpadu** — `docs/` + `dox/` + `reports/` → `docs/` (reference/, reports/, notebooklm/, dox/)
- 🗑️ **Niu-Flow** — Dihapus dari tracked root repo, ditambah ke .gitignore
- 📦 **Archive** — `niuterm` (621MB) dan `terax-ai` (216MB) dipindah ke `archive/projects/`
- 📖 **README.md, AGENTS.md, BACKLOG.md** — Update semua path & struktur ke v4.0
- 🔐 **Root remote** → `ecosystem-config` (sudah dipisah dari profile repo)
- ⚠️ **latticesend** — Masih tanpa remote GitHub (perlu dibuatkan repo)
- 🧪 **Sandbox** — 7 proyek sisa dengan total ~600MB

---

## 🔴 Perubahan — 21 Aug 2026 — up-eco Follow-up

*Dokumen diverifikasi langsung dari tool output (up-eco.sh, git, gh, ps, curl, skill-audit) 2026-08-21.*

- 🔧 **Mission Control** — `services/niu-mission-control` v2.6.2 **UP** (port 5200, health ok). venv lama rusak (symlink ke `/Volumes/HermesAgent` USB tidak ter-mount) → recreate venv lokal penuh + install requirements.
- 📦 **Ecosystem audit** — 45 git repos terdeteksi (root + 44 sub). Semua punya remote. 3 dirty repo di-commit+push.
- 🔀 **PemdiAcehTengah PR#4** — squash-merged 2026-08-21 (commit `0369891`). Rumus PermenPANRB 8/2026 + matriks bukti L1-L2.
- 🧠 **Skill Bank** — 68 skill (bank pusat), INDEX+manifest sinkron, 0 duplikat. Skill-audit: 32 finding **warning-only** (url=26 contoh dokumentasi domain security, secret=0).
- 📝 **Root ecosystem** — commit `6391be7` (session-models.json snapshot).
- 🖥️ **Mac** — macOS 26.5 (build 25F71), ReduceMotion=ON.
- 📚 **BACKLOG.md** — diperbarui faktual (Pemdi, MC, JHermUSB, latticesend, dirty repos, AI ecosystem model).

*Catatan: file tersegel (CONSTITUTION, SCOPE, MODEL.policy, AGENTS.slim, VISION, FREEZE.list) TIDAK diubah agen — sesuai Law 4 NIU-FENCE aktif.*
