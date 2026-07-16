# 📋 BACKLOG — Niumination Project — MASTER DOCUMENTATION

> **REORGANIZATION: Jul 17, 2026** — Root ekosistem telah dirapikan:
> - ✅ **incubator/** baru — 9 proyek dormant dipindahkan
> - ✅ **archive/** diperluas — Belum disentuh, labs, backup, duplikat diarsipkan
> - ✅ **TEDEO** dihapus dari lokal, ditandai mature di GitHub (butuh VPS)
> - ✅ **Duplikat** projects/niu-dash dihapus (canonical di Production/)

---

## 🗂️ Struktur Root Ekosistem — Jul 17, 2026

```
Desktop/Niumination/
├── Production/          🏭 11 proyek — aktif & deployed
├── projects/            🔧 16 proyek — aktif dikerjakan
├── incubator/           💤 9 proyek — dormant / belum dikerjakan
├── archive/             📦 File usang, backup, eksperimen
├── brain/               🧠 Obsidian vault
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
| 🗂️ **File** | `~/Desktop/Niumination/BACKLOG.md` | Source of truth utama |
| 🧠 **Memory (Hermes)** | Persistent memory | Compact snapshot survive kompresi |
| 🔄 **Cron checkpoint** | `memory-checkpoint` tiap 6 jam | Backup otomatis |
| 🔍 **Session DB** | SQLite session store | Full transcript via `session_search()` |
| 📓 **Obsidian Vault** | `brain/` | Catatan harian & audit |

**Prosedur update:** Bicara saja "update backlog" — saya edit file ini + sync memory.

---

## 🎯 KANBAN SYSTEM — Jul 17, 2026

**Total task: 123** (24 done, 1 completed, 98 ready)
**Board:** Niumination Ecosystem
**Note:** TEDEO dipromosikan ke **MATURE ✅** — dihapus dari lokal, catatan "butuh VPS untuk production"

### 🏭 Production — 11 Proyek Aktif

| Proyek | Status | Deploy | Notes |
|--------|--------|--------|-------|
| **PemdiAcehTengah** | 🟢 Active | Vercel | 52 OPD, 70 pages |
| **Niu-LKH** | ✅ Done | GH Pages | v3.1.1 |
| **niu-vermilion** | 🟢 Active | Vercel | 65% |
| **kune-ya.com** | 🟢 Active | Vercel | 80% |
| **niu-dash** | 🟢 Active | GH Pages | v2.16.8 |
| **JHermUSB-portable** | ✅ Done | GitHub | 100% |
| **mac-web-dashboard** | ✅ Done | GitHub | v1.0.0 |
| **arch-web-dashboard** | ✅ Done | GitHub | v1.0.0 |
| **ai-file-manager-android** | 🟢 Active | Device | Published & tested |
| **ai-first-os** | ⚪ Minor | GitHub | Build kit |
| **Niumination** | ⚪ Minor | GitHub | Profile config |
| **niu-mission-control** | 🟢 New 🆕 | GitHub | Ecosystem dashboard — repo baru |

### 🔧 projects/ — 16 Proyek Aktif Dikerjakan

| Proyek | Priority | Status | Notes |
|--------|----------|--------|-------|
| **TEDEO-Kanban** | P2 | 95% ✅ | Vite/React/Zustand |
| **Niu-Flow** | P2 | 90% ✅ | Python/JCode bridge |
| **Flame-ADE** | P2 | 93% | Tauri/Rust v1.3.0 |
| **niu-cast** | P2 | 95% | PyQt5 Gaming Edition |
| **joy-connect-for-mac** | P2 🆕 | Active | Swift/ADB bridge |
| **didong-code** | P2 | Active | Electron ADE Gayo |
| **cc-acehtengah** | P3 | Active | Next.js + Prisma |
| **niumination-workspace** | P3 | Active | Next.js 16 |
| **niu-dash-fullstack** | P3 | Active | Next.js 16 |
| **niu-mission-control** | P3 | Active | Ecosystem dashboard |
| **AuditTI-AT** | P3 | ✅ Live | GH Pages |
| **maze-3d** | P3 | ✅ Live | GH Pages |
| **x-downloader** | P3 | ✅ Phase 3 | Tauri 2 |
| **niu-kanban-dash** | P3 | Active | Vite/React |
| **orchestrator** | P3 | Active | Python multi-agent |
| **Ultra** | P3 | 80% | Puppeteer automation |

### 💤 incubator/ — 9 Proyek Dormant / Belum Dikerjakan

| Proyek | Alasan | Last Activity |
|--------|--------|---------------|
| **terax-ai** | Fork, 20% | Stale |
| **niu-studio** | Dual lockfile mess | Stale |
| **niude** | Low priority | Stale |
| **niuterm** | Low priority | Stale |
| **niutui** | No remote, low priority | Stale |
| **zen** | acehtengah-web/ | Stale |
| **aistudio-google** | Game files only | Stale |
| **arena.ai** | Eksperimen | Stale |
| **x-downloader-backup** | Backup file | Stale |

### 🟢 Completed (3)

- [x] **mac-web-dashboard** — macOS Pro Max Dashboard v1.0.0 — Homebrew, launchd, Darwin — @mac-web-dashboard
- [x] **arch-web-dashboard** — Arch Linux Pro Max Web Dashboard v1.0.0 — @arch-web-dashboard
- [x] **Niu-LKH** — v3.1.1 React/Vite, GH Pages, Supabase — @niu-lkh

### 🔴 P1 — Critical (5)

- [x] ~~**TEDEO** — Delivery Service — **MATURE ✅** — Butuh VPS untuk production. Dihapus dari lokal. GitHub: `github.com/Niumination/TEDEO` — @tedeo~~
- [x] **kune-ya.com** — AI Chat RAG — ✅ deployed — @kune-ya
- [x] **PemdiAcehTengah** — Portal Pemda Aceh Tengah — 6 Quick Win 100% — @pemdi-aceh-tengah
- [x] **niu-vermilion** — Second Brain — V1-V5 auth fixed ✅ — @niu-vermilion
- [x] **ai-file-manager-android** — AI File Organizer — ✅ Production — @android

### 🟡 P2 — Active (9)

| Proyek | Status | Notes |
|--------|--------|-------|
| joy-connect-for-mac | 🆕 Active | Swift/ADB bridge |
| TEDEO-Kanban | 95% ✅ | Vite/React/Zustand |
| niu-cast | 95% ✅ | PyQt5 Gaming Edition |
| Niu-Flow | 90% ✅ | Python/JCode bridge |
| Flame-ADE | 93% | Tauri/Rust |
| didong-code | Active | Electron ADE |
| niu-dash | ✅ Live | v2.16.8 GH Pages |
| brain (Obsidian Vault) | Active | Daily logs |
| AuditTI-AT | ✅ Live | GH Pages |

---

## 🔥 TEDEO — Status Perubahan

**Status:** ✅ **MATURE — Local development dihentikan**
- **Catatan:** Butuh VPS untuk production deployment (Express + PostgreSQL)
- **GitHub:** `github.com/Niumination/TEDEO` — private, mature topic
- **Issue:** [#2 — PRIORITAS: butuh VPS](https://github.com/Niumination/TEDEO/issues/2)
- **Local:** ✅ Dihapus dari `projects/TEDEO/`
- **Last commit:** `a94f724` — fix V1-V3 Vercel deployment fixes

---

## 🗺️ Project Status — Per Proyek (Filesystem Reality)

### PemdiAcehTengah — `Production/PemdiAcehTengah/`
- **HEAD:** 791f1c3 | **Remote:** ✅ SSH (github.com/Niumination/PemdiAcehTengah) | **Deploy:** 🟢 Vercel
- **Stack:** Next.js 14, React 18, pure CSS, Supabase
- **Status:** 🟢 **Active — Production dir** | 6 Quick Win 100% ✅

### Niu-LKH — `Production/Niu-LKH/`
- **Status:** ✅ **100% Done** — v3.1.1 — GH Pages live ✅

### niu-vermilion — `Production/niu-vermilion/`
- **Status:** 65% — V1-V5 auth bugs fixed ✅

### kune-ya.com — `Production/kune-ya.com/`
- **Status:** 80% — K1-K5 all fixed ✅ — analytics + rate limiting ✅

### niu-dash — `Production/niu-dash/` 🏭 (canonical)
- **HEAD:** aa2198e | **Remote:** ✅ SSH | **Deploy:** 🟢 GH Pages — v2.16.8
- **Status:** **Audit 27/27 ✅** — Duplikat di `projects/niu-dash` sudah dihapus
- **Note:** ONLY canonical copy exists in Production/

### JHermUSB-portable — `Production/JHermUSB-portable/`
- **Status:** 100% ✅

### Flame-ADE — `projects/flame-ade/`
- **Stack:** Tauri 2, Rust, React 19, TypeScript
- **Status:** v1.3.0 — 172 TS files, 21 Rust files

### Niu-Flow — `projects/Niu-Flow/` (canonical)
- **Stack:** Python, JCode bridge
- **Status:** 90% — Root-level Niu-Flow (logs/output) sudah di-archive

### TEDEO-Kanban — `projects/TEDEO-Kanban/`
- **Stack:** Vite + React + Zustand + @dnd-kit + PWA
- **Status:** 95% ✅

### joy-connect-for-mac — `projects/joy-connect-for-mac/`
- **Stack:** Swift 5.9/XcodeGen, ADB+scrcpy bridge
- **Status:** 🆕 Active — Infinix GT 30 Pro

### didong-code — `projects/didong-code/`
- **Stack:** Electron, multi AI provider
- **Status:** Active — Gayo Heritage

---

## 📊 SCOREBOARD EKOSISTEM — Jul 17, 2026

```
Proyek               Kematangan  Priority   Git  Remote    Deploy      Lokasi
────────────────────────────────────────────────────────────────────────────────
PemdiAcehTengah      ██████████ 95% P1     ✅   ✅ SSH    🟢 Vercel   Production/
Niu-LKH              ██████████ 100% ✅ P2     ✅   ✅ SSH    🟢 GH Page  Production/
niu-vermilion        ██████░░░░ 65% P1     ✅   ✅ SSH    🟢 Vercel   Production/
kune-ya.com          ████████░░ 80% P1     ✅   ✅ SSH    🟢 Vercel   Production/
TEDEO                ██████████ 85% ✅ **MATURE** ✅   ✅ SSH    ✅ GitHub   ❌ local — remote only
TEDEO-Kanban         ██████████ 95% P2     ✅   ✅ SSH    ✅ GitHub   projects/
JHermUSB-portable    ██████████ 100% ✅   P2     ✅   ✅ SSH    🟢 GitHub   Production/
Niu-Flow             ██████████ 90% P2     ✅   ✅ SSH    ❌ local    projects/
arch-web-dashboard   ██████░░░░ 60% P2     ✅   ✅ HTTPS  🟢 GitHub   Production/
mac-web-dashboard    ██████████ 95% P2     ✅   ✅ SSH    🟢 GitHub   Production/
Flame-ADE            ██████████ 93% P2     ✅   ✅ SSH    ✅ GitHub   projects/
Niu-Dash             ██████████ 95% P2     ✅   ✅ SSH    🟢 GH Page  Production/ 🏭
niu-cast             ██████████ 95% P2     ✅   ✅ HTTPS  ⚪ macOS    projects/
brain                ██████░░░░ 60% P3     ✅   ✅ SSH    ❌ local    root/
x-downloader         ██████████ 100% P3   ✅   ✅ SSH    🟢 GitHub   projects/
joy-connect-for-mac  ██████░░░░ 60% P2 🆕 ✅   ✅ SSH    ❌ local    projects/
niu-mission-control  █████░░░░░ 40% P3 🆕 ✅   ✅ SSH    ✅ GitHub   projects/
didong-code          ██████░░░░ 50% P2 🆕 ✅   ✅ SSH    ✅ GitHub   projects/
```

### incubator/ (Dormant)
```
Proyek               Kematangan  Priority   Git  Remote    Deploy      Lokasi
────────────────────────────────────────────────────────────────────────────────
niu-studio           ██████░░░░ 60% P3     ✅   ✅ SSH    ❌ local    incubator/
niude                ██████░░░░ 50% P3     ✅   ✅ SSH    ❌ local    incubator/
niuterm              ██████░░░░ 60% P3     ✅   ✅ SSH    ❌ local    incubator/
maze-3d              ████████░░ 70% P3     ✅   ✅ SSH    🟢 GH Page  projects/ (active)
terax-ai (fork)      ██░░░░░░░░ 20% P3     ✅   ✅ SSH    ❌ local    incubator/
zen                  ██░░░░░░░░ 20% P3     ✅   ✅ SSH    ❌ local    incubator/
niutui               ██░░░░░░░░ 20% P3     ✅   ❌       ❌ local    incubator/
aistudio-google      ██░░░░░░░░ 10% P3     ❌   ❌       ❌ local    incubator/
arena.ai             ██░░░░░░░░ 10% P3     ❌   ❌       ❌ local    incubator/
x-downloader-backup  —            —        ✅   ✅ SSH    ❌ local    incubator/
```

---

## 📊 FILESYSTEM AUDIT — Real Count (Jul 17, 2026)

```
Kategori                 Count  Notes
─────────────────────────────────────────
Production/               11    Aktif & deployed
projects/ (active)        16    Aktif dikerjakan
incubator/ (dormant)       9    Belum dikerjakan
archive/                  ~30    File/folder usang
brain/                     1    Obsidian vault
characters/                5    herdr agents
docs/                      8    Documentation dirs
dox/                       3    Project DOX
scripts/                  11    Ecosystem scripts
tools/                     1    Ponytail
PI/                        3    Sensitive configs
rekap/                     1    Terminal dotfiles
─────────────────────────────────────────
Total filesystem items    ~44    (30 git + 14 non-git)
Remote-only monitoring   ~20    Forks, stale repos
Git status:              34 clean ✅, 2 dirty ⚠️
```

### ⚠️ Dirty Repos (2)
1. **Production/niu-dash** — 1 file (ecosystem-status.json, auto-generated — normal)
2. **brain** (Root) — 8 files (inbox harian + divergence logs — normal)

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
| **Hermes (main)** | opencode-zen | opencode/big-pickle | ✅ **Live** |
| **Claude Code** | ANTHROPIC_API_KEY | claude-sonnet-4 | ✅ **Live** |
| **JCode** | OPENCODE_API_KEY | — | ✅ **Live** |
| **Delegation** | gemini | gemini-2.5-flash | ✅ Off (concurrent=1, depth=0) |
| **AI-Memory-Collection** | 12 AI tools | Snapshot ~1.7GB | ✅ **Referenced** |

> **🧠 AI-Memory-Collection** — Kompilasi memori dari 12 AI tools (Claude, JCode, Codex, OpenCode, Copilot, Orca, Cursor, dll). Berisi `memory.md` (510 baris — knowledge unified), hooks, config, cache, dan 2 model GGUF lokal. Berlokasi di `~/Desktop/AI-Memory-Collection/`. Lihat `docs/ai-memory-collection.md` untuk detail.

---

## 🔴 Perubahan Hari Ini — Jul 17, 2026

- ✅ **TEDEO** — Dihapus dari lokal, GitHub description + topics (mature), issue #2 dibuat
- ✅ **incubator/** — Dibuat, 9 proyek dormant dipindahkan
- ✅ **archive/** — Diperluas: Belum disentuh, labs, backup, root Niu-Flow duplikat
- ✅ **projects/niu-dash** — Dihapus (duplikat dari Production/niu-dash)
- ✅ **Root Niu-Flow** — Logs/output diarsipkan (canonical di projects/Niu-Flow/)
- ✅ **BACKLOG.md** — Diupdate dengan struktur baru
- ✅ **Root ecosystem-config dibersihkan** — Hapus sub-project gitlinks, cuma track config/docs/scripts
- ✅ **joy-connect-for-mac** — Remote GitHub dibuat & push
- ✅ **niu-mission-control** — Remote GitHub dibuat & push
- ✅ **.gitignore root** — Exclude sub-projects, archive, PI/; .DS_Store removed from MC
- ✅ **Scoreboard** — Add niu-mission-control entry
- ✅ **AI-Memory-Collection** — Referensi dimasukkan ke AI ECOSYSTEM

*Dokumen ini diverifikasi langsung dari filesystem Jul 17, 2026.*
