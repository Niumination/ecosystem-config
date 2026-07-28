# 📋 BACKLOG — Niumination Ecosystem — MASTER DOCUMENTATION

> **UPDATE: July 28, 2026** — Sync real filesystem state setelah 11 hari tidak diupdate (sejak Jul 17).
> Perubahan besar: cc-acehtengah +27 commit, niu-mission-control +33 commit, PemdiAcehTengah 57 bukti dukung.

---

## 🗂️ Struktur Root Ekosistem — Jul 28, 2026

```
Desktop/Niumination/
├── Production/          🏭 12 proyek — aktif & deployed
├── projects/            🔧 19 proyek — aktif dikerjakan
├── incubator/           💤 9 proyek — dormant / belum dikerjakan
├── archive/             📦 File usang, backup, eksperimen
├── brain/               🧠 Obsidian vault (git)
├── characters/          🤖 herdr agent characters (6)
├── docs/                📚 Dokumentasi ekosistem
├── dox/                 📄 Project DOX files
├── PI/                  🔐 Konfigurasi sensitif (api-key, secrets)
├── rekap/               🐚 Terminal dotfiles
├── scripts/             ⚙️ Ecosystem automation
├── tools/               🛠️ Ponytail MCP
├── AGENTS.md            📋 Root agents file
├── BACKLOG.md           📋 Master doc ini
└── .gitleaks.toml       🔒 Security config
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

## 🎯 KANBAN SYSTEM — Jul 28, 2026

**Data source:** `kanban.db` (43 scratch tasks) + filesystem audit
**Board:** Niumination Ecosystem
**Status:** 11 proyek Production aktif, 19 proyek projects/, 9 incubator dormant

### 🏭 Production — 12 Proyek Aktif

| Proyek | Status | Deploy | Aktivitas 14 Hari | Notes |
|--------|:------:|:------:|:------------------:|-------|
| **PemdiAcehTengah** | 🟢 **Active** | Vercel | **+3 commit** | 57 bukti dukung + preview + 42 file lampiran |
| **Niu-LKH** | ✅ Done | GH Pages | 0 | v3.1.1 — ⚠️ Dirty 1 file |
| **niu-vermilion** | 🟢 Active | Vercel | 0 | Stable — V1-V5 fixed |
| **kune-ya.com** | 🟢 Active | Vercel | 0 | Stable — K1-K5 fixed |
| **niu-dash** | 🟢 Active | GH Pages | **+2 commit** | v2.16.8 — ⚠️ Dirty 3 file |
| **JHermUSB-portable** | ✅ Done | GitHub | 0 | ⚠️ **Dirty 8 file** — config & docs |
| **mac-web-dashboard** | ✅ Done | GitHub | +1 | v1.0.0 |
| **arch-web-dashboard** | ✅ Done | GitHub | 0 | v1.0.0 |
| **ai-file-manager-android** | 🟢 Active | Device | 0 | Published & tested |
| **ai-first-os** | ⚪ Minor | GitHub | 0 | Build kit |
| **Niumination** | ⚪ Minor | GitHub | **+7 commit** | Profile config |
| **CC.Switch** | 🟢 **Active** | GitHub | **+8 commit** | Tauri 2 multi-CLI |

### 🔧 projects/ — 19 Proyek Aktif Dikerjakan

| Proyek | Priority | Status | Aktivitas 14 Hari | Notes |
|--------|:--------:|:------:|:------------------:|-------|
| **cc-acehtengah** | **P2 ⬆** | 🟢 **Active** | **+27 commit** 🏆 | Tema Gayo Highlands, Analytics, GIS, AI orchestrator, QueryBar |
| **niu-mission-control** | **P2 ⬆** | 🟢 **Active** | **+33 commit** 🏆 | v2.6.0 — Ecosystem scanner, sidebar toggle, gateway monitoring |
| **niu-cast** | P2 | 🟢 **Active** | **+27 commit** | v3.6.0 — Mac Connect Bridge, macOS native install |
| **TEDEO-Kanban** | P2 | 🟡 95% | +1 | Vite/React/Zustand |
| **Niu-Flow** | P2 | 🟡 90% | 0 | Python/JCode bridge |
| **Flame-ADE** | P2 | 🟡 93% | 0 | Tauri/Rust |
| **didong-code** | P2 | 🟢 Active | 0 | Electron ADE Gayo |
| **joy-connect-for-mac** | P2 🆕 | 🟢 Active | 0 | Swift/ADB bridge |
| **niumination-workspace** | P3 | ⏸️ Stale | 0 | Next.js 16 |
| **niu-dash-fullstack** | P3 | ⏸️ Stale | +1 | Next.js 16 |
| **orchestrator** | P3 | ⏸️ Stale | 0 | Python multi-agent |
| **Ultra** | P3 | ⏸️ Stale | 0 | Puppeteer automation |
| **AuditTI-AT** | P3 | ✅ Live | 0 | GH Pages |
| **maze-3d** | P3 | ✅ Live | 0 | GH Pages |
| **x-downloader** | P3 | ✅ Phase 3 | 0 | Tauri 2 |
| **niu-kanban-dash** | P3 | ⏸️ | 0 | Vite/React |
| **spatial-vision** | P3 | 🟢 Active | +1 | 3D vision |
| **latticesend** | P3 | 🟢 Active | +1 | File transfer |
| **zaryu-terminal-dotfiles** | P3 | 🟢 Active | +2 | Terminal config |

### 💤 incubator/ — 9 Proyek Dormant

| Proyek | Alasan | Last Activity |
|--------|--------|---------------|
| terax-ai | Fork, 20% | Stale |
| niu-studio | Dual lockfile mess | Stale |
| niude | Low priority | Stale |
| niuterm | Low priority | Stale |
| niutui | No remote, low priority | Stale |
| zen | acehtengah-web/ | Stale |
| aistudio-google | Game files only | Stale |
| arena.ai | Eksperimen | Stale |
| x-downloader-backup | Backup file | Stale |

---

## 📊 SCOREBOARD EKOSISTEM — Jul 28, 2026

```
Proyek               Kematangan     Prio  Status    Git  Remote    Deploy      Lokasi
─────────────────────────────────────────────────────────────────────────────────────────
PemdiAcehTengah      ██████████ 95% P1    🟢 Active ✅   ✅ SSH    🟢 Vercel   Production/
cc-acehtengah        ██████████ 90% P2 ⬆  🟢 Active ✅   ✅ SSH    🟢 GitHub    projects/
niu-mission-control  ██████████ 85% P2 ⬆  🟢 Active ✅   ✅ SSH    🟢 GitHub    projects/
niu-cast             ██████████ v3.6.0 P2 🟢 Active ✅   ✅ SSH    ⚪ macOS     projects/
Niu-LKH              ██████████ 100% ✅    ✅ Done   ✅   ✅ SSH    🟢 GH Page   Production/
niu-vermilion        ██████████ V1-V5 P1   🟢 Active ✅   ✅ SSH    🟢 Vercel    Production/
kune-ya.com          ██████████ K1-K5 P1   🟢 Active ✅   ✅ SSH    🟢 Vercel    Production/
TEDEO                ██████████ 85% ✅✅✅ **MATURE**   ✅ ✅ SSH    ✅ GitHub    ❌ local
TEDEO-Kanban         ██████████ 95% P2     🟡 95%     ✅   ✅ SSH    ✅ GitHub    projects/
CC.Switch            ██████████ v3.17.0 P2 🟢 Active  ✅   ✅ SSH    🟢 GitHub    Production/
Niu-Flow             ██████████ 90% P2     ⏸️ Stale   ✅   ✅ SSH    ❌ local     projects/
Flame-ADE            ██████████ v1.3.0 P2  ⏸️ Stale   ✅   ✅ SSH    ✅ GitHub    projects/
niu-dash             ██████████ v2.16.8 P2 🟢 Active  ✅   ✅ SSH    🟢 GH Page   Production/
JHermUSB-portable    ██████████ 100% ✅ P2 ✅ Done    ✅   ✅ SSH    🟢 GitHub    Production/
mac-web-dashboard    ██████████ v1.0.0 ✅  ✅ Done    ✅   ✅ SSH    🟢 GitHub    Production/
arch-web-dashboard   ██████████ v1.0.0 ✅  ✅ Done    ✅   ✅ SSH    🟢 GitHub    Production/
ai-file-manager      ██████████ 100% P1    🟢 Active ✅   ✅ SSH    🟢 Device    Production/
ai-first-os          █████░░░░░ 45%        ⚪ Minor   ✅   ✅ SSH    🟢 GitHub    Production/
brain                ██████░░░░ 60% P3     🟢 Active  ✅   ✅ SSH    ❌ local     root/
didong-code          ██████░░░░ 50% P2     🟢 Active  ✅   ✅ SSH    ✅ GitHub    projects/
joy-connect-for-mac  ██████░░░░ 60% P2     🟢 Active  ✅   ✅ SSH    ❌ local     projects/
x-downloader         ██████████ 100% P3    ✅ Phase 3  ✅   ✅ SSH    🟢 GitHub    projects/
orchestrator         ██████░░░░ 40% P3     ⏸️ Stale   ✅   ✅ SSH    ✅ GitHub    projects/
Ultra                ████████░░ 80% P3     ⏸️ Stale   ✅   ✅ SSH    ✅ GitHub    projects/
```

### incubator/ (Dormant) — No Change

```
terax-ai              ██░░░░░░░░ 20% P3     Stale
niu-studio            ██████░░░░ 60% P3     Stale
niude                 ██████░░░░ 50% P3     Stale
niuterm               ██████░░░░ 60% P3     Stale
niutui                ██████░░░░ 20% P3     Stale
zen                   ██░░░░░░░░ 20% P3     Stale
aistudio-google       ██░░░░░░░░ 10% P3     Stale
arena.ai              ██░░░░░░░░ 10% P3     Stale
x-downloader-backup   ░░░░░░░░░░ —          Stale
```

---

## 📊 FILESYSTEM AUDIT — Real Count (Jul 28, 2026)

```
Kategori                 Count  Notes
─────────────────────────────────────────
Production/               12    Aktif & deployed
projects/ (active)        19    Aktif dikerjakan
incubator/ (dormant)      9    Belum dikerjakan
archive/                  ~30    File/folder usang
brain/                     1    Obsidian vault (git)
characters/                6    herdr agents (git)
docs/                      8    Documentation dirs
dox/                       4    Project DOX files
scripts/                  11    Ecosystem scripts
tools/                     1    Ponytail (git)
PI/                        3    Sensitive configs
rekap/                     1    Terminal dotfiles
─────────────────────────────────────────
Total filesystem items   ~44    (30 git + 14 non-git)
Total size:              18 GB
```

### ⚠️ Dirty Repos (3)

1. **Production/JHermUSB-portable** — 8 file (config, docs, setup)
2. **Production/niu-dash** — 3 file (README, ecosystem-status, released.json)
3. **Production/Niu-LKH** — 1 file (ExcelPreview.jsx)

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
| **Hermes (main)** | opencode-zen | kimi-K2.6 | ✅ **Live** |
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

## 🔴 Perubahan Hari Ini — Jul 28, 2026

- ✅ **BACKLOG.md** — Diupdate dengan data filesystem real
- ✅ **cc-acehtengah** — Dipromosikan P3 → P2 (aktivitas tinggi)
- ✅ **niu-mission-control** — Dipromosikan P3 → P2 (aktivitas tinggi)
- ✅ **Scoreboard** — Update semua kematangan & status
- ✅ **Aktivitas 14 hari** — Ditambahkan tracking
- ✅ **AI ECOSYSTEM** — Update model (Kimi K2.6)

*Dokumen diverifikasi langsung dari filesystem Jul 28, 2026.*
