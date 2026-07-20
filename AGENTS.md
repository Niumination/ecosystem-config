# Niumination — DOX Framework (Root)

**Lokasi:** `~/Desktop/Niumination/`
**Pengguna:** Afrizal Munthe (Niumination) — Pranata Komputer, Diskominfo Aceh Tengah
**DOX Version:** 3.0
||| **Total Projek Lokal:** 44 item (35 git + 9 non-git)
|||||| | **Kanban Board:** "Niumination Ecosystem" — terupdate 16 Jul 2026 ✅
| | **Model aktif:** `opencode/big-pickle` — paid ($1/M in, $5/M out)

---

## Core Contract

1. File **AGENTS.md** adalah DOX (Documentation Optimization Xchange) — binding work contract untuk subtree masing-masing
2. Setiap perubahan kode di proyek mana pun WAJIB diikuti DOX pass sebelum task ditutup
3. Parent DOX ini adalah root index — proyek anak WAJIB punya AGENTS.md sendiri jika kompleksitas > 1 folder
4. Pindah fokus antar proyek: **baca AGENTS.md induk → langsung navigasi ke proyek target → baca AGENTS.md anak jika ada**
5. Jika ada konflik antar DOX, doc yang lebih dekat ke file yang disentuh menang

---

## 📐 Master Direction Protocol — Phase 0 (Foundation ✅)

### Apa itu?
Protocol ini adalah kerangka eksekusi master untuk seluruh ekosistem Niumination. Semua keputusan dan tindakan HERMES harus selaras dengan protocol ini.

### Prinsip Utama
1. **MASTERPLAN.md adalah blueprint final** — semua fase tereksekusi sesuai urutan, tidak ada shortcut
2. **Auto-sync wajib no_agent=true** — script mekanis, bukan LLM, untuk kendali biaya
3. **Format BACKLOG wajib parseable** — `- [STATUS] **Title** — Desc — @project`
4. **Credential cron di .env profile** — bukan di localStorage atau file proyek
5. **Setiap cron wajib workdir + profile** — path absolut, profile opencode
6. **mkdir-based lock** — bukan flock (macOS tidak punya flock)
7. **Pre-flight wajib** — gitleaks, gh auth, jq, sqlite3 sebelum fase baru

### Status Fase
| Fase | Deskripsi | Status |
|------|-----------|:------:|
| 0 | Foundation (14/14) — gitleaks, hooks, creds, dll | ✅ Done |
| 1 | Tier 1 Setup — 10 proyek AGENTS.md + BACKLOG.md | ✅ Done |
| 2.1 | health-checker.sh + cron (every 6h, local) | ✅ Done |
| 2.2 | daily-heartbeat.sh + cron (08:00, deliver=telegram) | ✅ Done |
| 2.3 | remote-poller.sh + cron (every 6h, silent when clean) | ✅ Done |
| 2.4 | changelog-writer.sh + cron (20:00, local) | ✅ Done |
| 2.5 | kanban-sync.sh + cron (every 1h, local) + divergence detection | ✅ Done |
| 2.7 | gitleaks-weekly.sh + cron (Sun 08:00) | ✅ Done |
| 2.8 | Ecosystem page — Vanilla HTML + React (port 5199) | ✅ Done |
| 2.6 | issue-bridge.sh — BACKLOG→GitHub Issues sync | ✅ Done (cron every 6h) |
| 2.9 | Skill Hermes ekosistem-scaffold | ✅ Done |
| 2.10 | Divergence detection (in kanban-sync.sh) | ✅ Done |
| 2.11 | generate-ecosystem-json.sh — Niu-Dash data source | ✅ Done |
| 3 | Phase 3 — Hardening validasi (6/7 ✅, 1 ⏩ skip) | ✅ Done |
| 🎯 | **Goal Besar — TEDEO T1-T4** (4 critical bugs ✅ ALL FIXED 24 Jun) | ✅ Done — committed & pushed |

### Eksekusi Selanjutnya
1. **TEDEO — ✅ T1-T4 ALL FIXED + ✅ Web deployed: https://tedeo-web.vercel.app** (13 Jul)
2. **TEDEO next** — test plan, deploy backend, mobile dev
3. **GitHub push** — ✅ niumination-workspace, niu-kanban-dash, orchestrator, Ultra
4. **Ekosistem** — ✅ eco-manifest updated (30 git + 9 non-git = 39), Niu-Dash ecosystem-status.json regenerated + pushed
5. **Pro...[truncated]
| **Phase 3 sisa** — ✅ issue-bridge (cron every 6h), cron failure simulation (⏩ skip)
| **Audit Fixes (20 Jun)** — ✅ status parsing [~], pre-commit DOX check, .gitleaks.toml custom, niu-vermilion DOX, health checker 10 Tier 1 |
4. **Scoreboard update** — sync BACKLOG scoreboard dengan realita

---

## Read Before Editing

1. Baca root AGENTS.md ini untuk orientasi
2. Identifikasi proyek yang akan disentuh
3. Baca AGENTS.md pada proyek tersebut (jika ada)
4. Parent DOX hanya index + global rules — detail teknis ada di child DOX
5. Jangan duplikasi info dari child DOX ke parent — cukup referensi

---

## Directory Structure — Real Filesystem (16 Jul 2026)

```
~/Desktop/Niumination/
├── AGENTS.md                  ← FILE INI — DOX induk
├── BACKLOG.md                 ← Prioritas master semua proyek
│
├── Niumination/               ← GitHub Profile README — Gitiumination 🆕
├── PI/                        ← Personal Inventory — API keys, rahasia
├── Production/                 ← Projek matang & selesai (🏭) — 11 dir
│   ├── ai-file-manager-android/ ← AI File Organizer (Kotlin/Gemini) ✅ GitHub
│   ├── CC.Switch/              ← Tauri 2 multi-CLI — 🟢 GitHub release v3.17.0
│   ├── JHermUSB-portable/     ← Hermes Agent portable (652K) ✅
│   ├── Niu-LKH/               ← LKH v3.1.1 — 100% Done — GH Pages live ✅
│   ├── PemdiAcehTengah/       ← Portal Pemda — 52 OPD, 70 pages — 🟢 Vercel
│   ├── ai-first-os/           ← Arch Linux ISO builder ✅ GitHub
│   ├── arch-web-dashboard/    ← Arch Linux Dashboard v1.0.0 ✅ GitHub
│   ├── niu-dash/              ← v2.16.8 GH Pages — Audit 27/27 ✅
│   ├── kune-ya.com/           ← AI Chat RAG — 🟢 Vercel (moved 24 Jun)
│   ├── niu-vermilion/         ← Second Brain — 🟢 Vercel (moved 24 Jun)
│   └── mac-web-dashboard/     ← macOS Dashboard v1.0.0 — ✅ GitHub (moved 24 Jun)
├── archive/                   ← Arsip — ~25MB (labs, skills, logs, backup)
│   ├── 01-updates/
│   ├── Belum disentuh/         ← Arsip ZIP belum diproses (~18MB)
│   ├── backup/                 ← Cadangan konfigurasi (2026-06-27)
│   ├── jcode-docs/             ← Dokumentasi JCode CLI
│   ├── labs/                   ← Eksperimen lama
│   ├── niu-flow-logs/          ← Log pipeline Niu-Flow
│   ├── skills-main/            ← Skill backup
│   └── ...
├── labs/                      ← Eksperimen (obsidian-ai-os, html, dll)
├── rekap/                     ← Terminal dotfiles & rekap
├── scripts/                   ← Cron & maintenance scripts (changelog, heartbeat, kanban-sync, dll)
├── tools/                     ← Ponytail MCP server & utilities
│
└── projects/                  ← Projek Eksperimen, Tools, & Aktif
    ├── arena.ai/              ← AI Arena — dashboard.html
    ├── AuditTI-AT/            ← GH Pages Live ✅ — JS/HTML
    ├── cc-acehtengah/         ← Command Center AI — SAPA→SPLP→CC — ✅ github.com/Niumination/cc-acehtengah
    ├── Niu-Flow/              ← JCode bridge — pipeline paralel, 6 commits
    ├── TEDEO/                 ← Delivery Service (Express/React/PostgreSQL)
    ├── TEDEO-Kanban/          ← Kanban untuk TEDEO
    ├── Ultra/                 ← Ultra Automation (Puppeteer) — ✅ github.com/Niumination/ultra-automation
    ├── aistudio-google/       ← Game files (street-racer-offline)
    ├── flame-ade/             ← Tauri 2/Rust desktop app (v1.3.0)
    ├── maze-3d/               ← 3D web maze game (GH Pages)
    ├── niu-cast/              ← Android ADB Tool & Screen Mirror — Gaming Edition v1.1.1 (PyQt5, ADB)
    ├── niu-dash-fullstack/    ← Next.js 16 Fullstack Dashboard — ✅ github.com/Niumination/niu-dash-fullstack
    ├── niu-kanban-dash/       ← React/Vite dashboard — ✅ github.com/Niumination/niu-kanban-dash (port 5199)
    ├── niu-studio/            ← Tauri/React creative studio
    ├── niumination-workspace/    ← Active — 4 commits, Prisma, Three.js — ✅ github.com/Niumination/niumination-workspace
    ├── niude/                 ← Tauri app
    ├── niuterm/               ← Tauri terminal tool
    ├── niutui/                ← Rust/Cargo TUI — ✅ Git
    ├── orchestrator/          ← Python multi-agent — ✅ github.com/Niumination/orchestrator
    ├── terax-ai/              ← Lightweight ADE fork (TS)
    ├── didong-code/           ← Electron AI coding agent — Gayo Aceh tradisi (new)
    ├── x-downloader/          ← Tauri 2 desktop — yt-dlp GUI (batch, format preview)
    └── zen/                   ← acehtengah-web/
```

---

## 🧠 AI Agent Instructions & Behavior

### Ponytail — Lazy Senior Dev Mindset

Ponytail adalah skill/ruleset yang memaksa AI coding agent berpikir seperti senior dev paling malas — selalu pilih solusi paling minimal sebelum nulis kode. Cocok dengan workflow surgical patch ecosystem.

**Decision Ladder (jalankan sebelum nulis kode apapun):**

1. **Perlu ada?** → YAGNI, skip. Kalau ngga diminta eksplisit, jangan nambah.
2. **Udah ada di repo?** → Reuse existing. Jangan rewrite. Cari dulu.
3. **Stdlib bisa?** → Pake stdlib dulu. Ngga perlu import fancy library.
4. **Platform native?** — Fitur OS/browser udah ada? Pake itu.
5. **Dependency terinstall?** → Udah ada di project? Baru pake.
6. **Bisa satu baris?** → Jangan 27 baris kalo bisa 1 baris.
7. **Baru: tulis kode minimal** — kode paling kecil yang solve problem.

**Benchmark:** -54% LOC, -22% token, -20% cost, -27% time, safety 100%.

**Cara pakai:** `/skill ponytail` atau `hermes -s ponytail`.

**MCP tools:** `mcp_ponytail_review_code_diff()`, `mcp_ponytail_audit_repo()`.

---

## Project Catalog

### 🏛️ Pemerintahan & SPBE (Aceh Tengah)

| Projek | Path | Stack | GitHub | Deploy | Last Push | Status |
|--------|------|-------|--------|--------|-----------|--------|
|| **PemdiAcehTengah** | `Production/PemdiAcehTengah/` | Next.js 14, React 18, pure CSS (Gayo Civic Digital v3) | `github.com/Niumination/PemdiAcehTengah` | 🟢 Vercel — 52 OPD SSG, 70 pages, 6 Quick Win ✅ | 16 Jul 2026 | 🟢 **Active — Production dir** |
| **kms-spbe** | — (remote only) | TS, Next.js | `github.com/Niumination/kms-spbe` | 🟢 Vercel | 26 Okt 2025 | ✅ Live |
|| **LKH** | `Production/Niu-LKH/` 🏭 | React 19, Vite 6, Tailwind v4, Supabase | `github.com/Niumination/Niu-LKH` | 🟢 GH Pages — v3.1.1 | 20 Jun 2026 | ✅ **100% Done 🎉 — Production/ 🏭** |
| **DiskominfoAT** | — (remote only) | HTML, CSS | `github.com/Niumination/DiskominfoAT` | 🟢 GH Pages | 13 Okt 2025 | ✅ Live |
| **Diskominfo-Web** | — (remote only) | HTML, CSS | `github.com/Niumination/Diskominfo-Web` | 🟢 GH Pages | 9 Okt 2025 | ✅ Live |
| **SPBE-DevOps-Academy** | — (remote only) | JS, HTML | `github.com/Niumination/SPBE-DevOps-Academy` | 🟢 GH Pages | 5 Nov 2025 | ✅ Live |
| **AuditTI-AT** | `projects/AuditTI-AT/` | JS | `github.com/Niumination/AuditTI-AT` | 🟢 GH Pages — Live | 24 Jun 2026 | ✅ Live |
| **Rekapitulasi-SPBE** | — (remote only) | JS | `github.com/Niumination/Rekapitulasi-SPBE` | ⚪ Not deployed | 1 Nov 2025 | ⚪ Stale |
| **Database-DiskominfoAT** | — (remote only) | — | `github.com/Niumination/Database-DiskominfoAT` | ⚪ Not deployed | 13 Okt 2025 | ⚪ Stale |
| **Automata** | — (remote only) | — | `github.com/Niumination/Automata` | ⚪ Not deployed | 8 Okt 2025 | ⚪ Stale |
| **Prakom-Surgawi** | — (remote only) | — | `github.com/Niumination/Prakom-Surgawi` | ⚪ Not deployed | 26 Sep 2025 | ⚪ Stale |

### 🤖 AI & Coding Agent Ecosystem

| Projek | Path | Stack | GitHub | Deploy | Last Push | Status |
|--------|------|-------|--------|--------|-----------|--------|
| **Flame-ADE** | `projects/flame-ade/` | Tauri 2, Rust, React 19, TS | `github.com/Niumination/Flame-ADE` | ⚪ Desktop app | 20 Jun 2026 | ✅ v1.3.0 |
| **JHermUSB-portable** | `Production/JHermUSB-portable/` | Shell, Hermes Agent v25+v27 | `github.com/Niumination/JHermUSB-portable` | 🟢 GitHub (🏭) | 22 Jun 2026 | ✅ Production |
| **Niu-Flow** | `projects/Niu-Flow/` | Python, JCode bridge | `github.com/Niumination/niu-flow` | ⚪ Local | 20 Jun 2026 | 🟢 **Active** — 5 commits |
| **VirtualAssistance** | — (remote only) | TS | `github.com/Niumination/VirtualAssistance` | 🟢 Vercel | 3 Jun 2026 | ✅ Live |
| **terax-ai** (fork) | `projects/terax-ai/` | TS | `github.com/niumination/terax-ai` | ⚪ Fork | 31 Mei 2026 | 🔄 Fork |
|| **orchestrator** | `projects/orchestrator/` | Python | `github.com/Niumination/orchestrator` | ⚪ Local | 24 Jun 2026 | ✅ **Pushed** |
|| **didong-code** | `projects/didong-code/` | Electron, React 18, TypeScript, Vite, Tailwind CSS | `github.com/Niumination/didong-code` | ⚪ Desktop app | 08 Jul 2026 | 🆕 **New — Gayo Heritage ADE** |
|| **Ultra** | `projects/Ultra/` | Node.js, Puppeteer, Express | `github.com/Niumination/ultra-automation` | ⚪ Local | 25 Jun 2026 | ✅ **Pushed** |
| **flame-code** | — (remote only) | TS | `github.com/Niumination/flame-code` | ⚪ Not deployed | 31 Mei 2026 | ⚪ Stale |
| **free-vps** | — (remote only) | TS | `github.com/Niumination/free-vps` | ⚪ Not deployed | 29 Mei 2026 | ⚪ Stale |
| **Devs-Niu** | — (remote only) | — | `github.com/Niumination/Devs-Niu` | ⚪ Not deployed | 8 Nov 2025 | ⚪ Stale |
| **Continue-Agent** | — (remote only) | — | `github.com/Niumination/Continue-Agent` | ⚪ Not deployed | 26 Okt 2025 | ⚪ Stale |
| **HermesV-Github** | — (remote only) | — | `github.com/Niumination/HermesV-Github` | ⚪ Codespaces | 11 Jun 2026 | 🔄 Stale |
| **AgentRouter** | ❌ **Distop** | Go reverse proxy | lokal | 🔴 **Dibersihkan** | 16 Jun 2026 | ❌ Upstream tidak stabil |

### 🌐 Web Apps & Personal Tools

| Projek | Path | Stack | GitHub | Deploy | Last Push | Status |
|--------|------|-------|--------|--------|-----------|--------|
||| **arch-web-dashboard** | `Production/arch-web-dashboard/` 🏭 | Next.js 14, React 18, TypeScript, Tailwind | `github.com/Niumination/arch-web-dashboard` | 🟢 GitHub | 22 Jun 2026 | ✅ v1.0.0 — **Production/ 🏭** |
|| **mac-web-dashboard** | `Production/mac-web-dashboard/` 🏭 | Next.js 14, React 18, TypeScript, Tailwind | `github.com/Niumination/mac-web-dashboard` | 🟢 GitHub | 11 Jul 2026 | ✅ v1.1.0 — **+AI Workspace (6 tabs), Hermes+Ollama+Agent Discovery** |
|| **CC.Switch** | `Production/cc-switch/` 🏭 | Tauri 2, React, Rust, multi-CLI switcher | `github.com/Niumination/cc-switch` | 🟢 GitHub | 20 Jul 2026 | ✅ v3.17.0 — **release DMG ready** |
|| **AI-First-OS**
| **Niumination** (Profile) | `Production/Niumination/` 🆕 | README, config, scripts | `github.com/Niumination/Niumination` | 🟢 GitHub | 15 Jul 2026 | ✅ **GitHub Profile — Gitiumination v1.0.0** |
| **niu-vermilion** | `Production/niu-vermilion/` 🏭 | Next.js 16, React 19, Supabase, TipTap | `github.com/Niumination/Niu-Vermilion` | 🟢 Vercel | 24 Jun 2026 | ✅ V1-V5 fixed — **Production/ 🏭** |
|| **niu-cast** | `projects/niu-cast/` | Python 3, PyQt5, ADB | `github.com/Niumination/niu-cast` | ⚪ macOS Desktop | 18 Jun 2026 | ✅ v1.1.1 |
| **cc-acehtengah** | `projects/cc-acehtengah/` | Next.js 16, Prisma 7, LLM (Ollama), RAG (Qdrant) | `github.com/Niumination/cc-acehtengah` | ⚪ Local | 13 Jul 2026 | 🔜 **Fase 1 — Foundation ✅** |
|| **niu-dash-fullstack** | `projects/niu-dash-fullstack/` | Next.js 16, React 19, Prisma 7, TanStack Query, next-auth | `github.com/Niumination/niu-dash-fullstack` | ⚪ Local | 13 Jul 2026 | ✅ **3D scene removed — performance improved** |
|| **niu-dash** | `Production/niu-dash/` 🏭 | HTML/CSS/JS Vanilla | `github.com/Niumination/niu-dash` | 🟢 GH Pages — v2.16.8 | 22 Jun 2026 | 🟢 **Audit 27/27 ✅** |
||| **niumination-workspace** | `projects/niumination-workspace/` | Next.js 16, Prisma, Three.js, TanStack Query | `github.com/Niumination/niumination-workspace` | ⚪ Local | 24 Jun 2026 | ✅ **4 commits — pushed to GitHub** |
| **niu-studio** | `projects/niu-studio/` | Tauri/React | `github.com/Niumination/niu-studio` | ⚪ Local | ✅ Git | 🟡 Dual lockfile |
| **niude** | `projects/niude/` | Tauri | `github.com/Niumination/niude` | ⚪ Local | ✅ Git | 🟡 Dual lockfile |
| **niuterm** | `projects/niuterm/` | Tauri | `github.com/niumination/NiuTerm` | ⚪ Local | ✅ Git | 🟡 |
| **niutui** | `projects/niutui/` | Rust/Cargo | lokal | ⚪ TUI | ✅ Git | 🟡 **No remote (0 commits)** |
| **zen** | `projects/zen/` | acehtengah-web/ | `github.com/Niumination/zen` | ⚪ Local | ✅ Git | 🟡 |
| **niu-kanban-dash** | `projects/niu-kanban-dash/` | React 19, Vite, Tailwind v4 | `github.com/Niumination/niu-kanban-dash` | localhost:5199 | 24 Jun 2026 | ✅ **Pushed to GitHub** |
| **maze-3d** | `projects/maze-3d/` | HTML, JS | `github.com/Niumination/Maze-3D-Game---Web-Based` | 🟢 GH Pages | 21 Mei 2026 | ✅ Live |
| **arena.ai** | `projects/arena.ai/` | HTML dashboard | lokal | ⚪ Local | — | 🟡 AI Arena dashboard |
| **x-downloader** | `projects/x-downloader/` | Tauri 2 (Rust) + Vite 5 + React 18 + Three.js 3D orb | `github.com/Niumination/x-downloader` | 🟢 GitHub | 06 Jul 2026 | ✅ **v2.0.0 — P3: playlist, conversion, clipboard, pause/resume, DMG release** |
| **niu-private** | — (remote only) | TS | `github.com/Niumination/niu-private` | 🟢 GH Pages | 8 Jun 2026 | ✅ Live |
| **ai-file-manager-android** | `Production/ai-file-manager-android/` | Android (Kotlin, Jetpack Compose, Gradle), Google Gemini 1.5 Flash, ML Kit OCR | `github.com/Niumination/ai-file-organizer-android` | 🟢 GitHub | 23 Jun 2026 | ✅ **Production** — tested on device, CI green |
| **kune-ya.com** | `Production/kune-ya.com/` 🏭 | TS, Next.js 15 | `github.com/Niumination/kune-ya.com` | 🟢 Vercel | 24 Jun 2026 | ✅ K1-K5 fixed — **Production/ 🏭** |
| **Niu-Startpage** | — (remote only) | HTML, CSS | `github.com/Niumination/Niu-Startpage` | 🟢 GH Pages | 22 Okt 2025 | ✅ Live |
| **NiuHomePage** (fork) | — (remote only) | CSS | `github.com/Niumination/NiuHomePage` | 🟢 GH Pages | 13 Okt 2025 | ✅ Live |
| **zaryu.startpage** (fork) | — (remote only) | JS | `github.com/Niumination/zaryu.startpage` | 🟢 GH Pages | 13 Okt 2025 | ✅ Live |
| **Niu-Cyber-Search-Engine** | — (remote only) | TS | `github.com/Niumination/Niu-Cyber-Search-Engine` | 🔴 Vercel 404 | 22 Okt 2025 | ❌ Down |

### 🖥️ Linux Desktop / Dotfiles (Arch Hyprland)

~25 repositori fork — tidak ada yang ter-clone lokal.

| Projek | GitHub | Deskripsi | Last Push |
|--------|--------|-----------|-----------|
| **dotfiles** | `github.com/Niumination/dotfiles` | 1.6MB — main Arch dotfiles | 17 Des 2024 |
| **Zaryu-HyDE** (fork) | `github.com/Niumination/Zaryu-HyDE` | 1.3GB — rework hyprdots | 17 Jun 2025 |
| **RyuDE** | `github.com/Niumination/RyuDE` | C++ — personal DE | 28 Mei 2025 |
| **hyprnix** | `github.com/Niumination/hyprnix` | NixOS/Hyprland config | 24 Feb 2025 |
| **agsv1-hyprpanel** | `github.com/Niumination/agsv1-hyprpanel` | TS — AGSv1 panel | 9 Jan 2025 |
| **(+ ~20 fork lain)** | — | hyprfloat, Windots, dll | — |

### 📚 Knowledge & Notes

| Projek | Path | GitHub | Deskripsi |
|--------|------|--------|-----------|
| **brain** | `brain/` | `github.com/Niumination/brain` | Obsidian vault — catatan harian, knowledge base |
| **PI** | `PI/` | lokal | **Personal Inventory** — API keys, credentials — **RAHASIA** |
| **aistudio-google** | `projects/aistudio-google/` | lokal | Game files |
| **archive** | `archive/` | lokal | Arsip proyek lama |
| **labs** | `labs/` | lokal | Lab eksperimen |
| **rekap** | `rekap/` | lokal | Terminal dotfiles & rekap |

### 🚚 Delivery Service

| Projek | Path | Deskripsi |
|--------|------|-----------|
| **TEDEO** | `projects/TEDEO/` | Delivery Service (Express, Prisma, PostgreSQL, Socket.IO) — **✅ Web deployed: https://tedeo-web.vercel.app** — T1-T4 ✅ ALL FIXED |
| **TEDEO-Kanban** | `projects/TEDEO-Kanban/` | Kanban board untuk TEDEO — ✅ pushed ke GitHub |

---

## AI Ecosystem

| # | Agent | Role | Provider/Model | Status |
|:-:|-------|------|----------------|:------:|
| 1 | **Hermes Agent** | Main orchestrator | Opencode Zen — `opencode/big-pickle` | ✅ **Live** — $1/M in, $5/M out |
| 2 | **Claude Code CLI** | Side coding agent | Anthropic — `claude-sonnet-4` | ✅ **Live** — `claude -p "..."` |
| 3 | **JCode** | Hermes↔OpenCode bridge | `OPENCODE_API_KEY` via Niu-Flow pipeline | ✅ **Live** — 5 commits |
| 4 | **Codex CLI** | OpenAI coding agent | OpenAI — Codex CLI | ✅ **Live** — goals DB, logs |
| 5 | **OpenCode CLI** | Standalone coding agent | OpenCode config — 146 skills | ✅ **Live** — ACP headless |
| 6 | **GitHub Copilot** | IDE assistant | GitHub Copilot | ✅ **Live** — VS Code |

### 🧠 AI-Memory-Collection

**Lokasi:** `~/Desktop/AI-Memory-Collection/` (~1.73 GB)
**Sumber:** Snapshot 12 AI tools dari seluruh sistem macOS (16 Jul 2026)

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

## Deployment Status

### 🟢 Vercel (4 Live, 1 Down)

| URL | Status | Catatan |
|-----|--------|---------|
| `pemdi-aceh-tengah.vercel.app` | ✅ 200 | PemdiAcehTengah — 52 OPD SSG, 70 pages |
| `kms-spbe.vercel.app` | ✅ 200 | KMS SPBE |
| `kune-ya-com.vercel.app` | ✅ 200 | Kune-Ya AI Chat RAG — K1-K5 ✅ |
| `virtual-assistance.vercel.app` | ✅ 200 | VirtualAssistance |
| `niu-cyber-search-engine.vercel.app` | ❌ 404 | Niu-Cyber-Search-Engine — **belum dideploy** |

### 🟢 GitHub Pages (10 Live)

| URL | Status |
|-----|--------|
| `niumination.github.io/Niu-LKH` | ✅ v3.1.1 |
| `niumination.github.io/niu-dash` | ✅ v2.16.8 |
| `niumination.github.io/niu-private` | ✅ |
| `niumination.github.io/Niu-Startpage` | ✅ |
| `niumination.github.io/DiskominfoAT` | ✅ |
| `niumination.github.io/Diskominfo-Web` | ✅ |
| `niumination.github.io/SPBE-DevOps-Academy` | ✅ |
| `niumination.github.io/Maze-3D-Game---Web-Based` | ✅ |
| `niumination.github.io/AuditTI-AT` | ✅ |
| `niumination.github.io/zaryu.startpage` | ✅ (fork) |
| `niumination.github.io/NiuHomePage` | ✅ (fork) |

---

## Global Conventions

### 🔐 Autentikasi & Keamanan
- **GitHub**: SSH keys only (`git@github.com:`) — jangan pakai HTTPS
- **GitHub Account**: `Niumination` (ID: 123625275) — user account, bukan org
- **API keys**: Hanya di `PI/` — **tidak pernah** di commit ke repo publik
- **Vercel**: CLI auth via `com.vercel.cli/auth.json` di `~/.local/share/`

### 💻 Stack Preferensi
| Kategori | Pilihan |
|----------|---------|
| Web framework | Next.js (14.x/15.x) / React (18.x/19.x) |
| Styling | Tailwind CSS / pure CSS |
| Diagram | Excalidraw, architecture-diagram (SVG dark) |
| Deployment | Vercel (web), GitHub Pages (statis) |
| Desktop | Tauri 2 + Rust |
| AI Agent | Hermes Agent v0.16.0 — opencode/big-pickle |

### 📝 Output
- Bahasa Indonesia untuk semua output
- Terstruktur (tabel, layer breakdown, data-driven)
- 🔴🟡🟢 priorities

### 📁 Struktur Repo
- `main` branch utama
- Remote: `origin` = GitHub
- `.gitignore` standar: `node_modules`, `.next`, `.env`, `*.old`, build artifacts

---

## DOX Chain Rules

```
AGENTS.md (root — ~/Desktop/Niumination/)
  ├── brain/AGENTS.md                                              ✅ (project docs, stats, version)
  ├── Production/Niu-LKH/AGENTS.md                                  ✅
  ├── Production/PemdiAcehTengah/AGENTS.md                          ✅ + 5 sub-DOX
  ├── Production/niu-dash/AGENTS.md                                 ✅
  ├── Production/kune-ya.com/AGENTS.md                              ✅
  ├── Production/niu-vermilion/AGENTS.md                            ✅
  ├── projects/Niu-Flow/AGENTS.md                                   ✅
  ├── projects/TEDEO/AGENTS.md                                      ✅
  ├── projects/Ultra/AGENTS.md                                      ✅
  ├── projects/flame-ade/AGENTS.md                                  ✅
  ├── projects/niu-cast/AGENTS.md                                   ✅
  ├── projects/niumination-workspace/AGENTS.md                      ✅
  ├── projects/niuterm/AGENTS.md                                    ✅
  ├── projects/terax-ai/AGENTS.md                                   ✅
  ├── projects/x-downloader/AGENTS.md                               ✅
  ├── Niumination/AGENTS.md                                       ✅ (profile DOX)
  └── brain/projects/*/AGENTS.md (10 files)                         ✅ (mirror docs)
```

**Cara navigasi:**
1. Mau kerja di proyek X → baca AGENTS.md induk (ini) → cari proyek X di catalog
2. Baca AGENTS.md proyek X (jika ada) untuk detail teknis
3. Jika proyek X tidak punya AGENTS.md, baca README.md atau direktori utamanya
4. Selesai kerja → update DOX yang relevan sebelum commit

---

## Quick Links

| Sumber | Path/Link |
|--------|-----------|
| **BACKLOG Master** | `BACKLOG.md` |
| **Personal Inventory** | `PI/` — API keys, credentials — **RAHASIA** (chmod 600 ✅) |
| **Obsidian Vault** | `brain/` |
| **Niu-Flow Pipeline** | `projects/Niu-Flow/` — Bridge Hermes↔JCode |
| **AI Agent Hooks** | `scripts/hooks/` — 12 hook scripts (claude, codex, copilot, dll) |
| **AI-Memory-Collection** | `docs/ai-memory-collection.md` — unified knowledge 12 AI tools |

---

## 🔌 Hermes MCP & Plugin Config (20 Jun 2026)

### MCP Servers Aktif

| Server | Status | Tools | Path |
|--------|--------|-------|------|
| **time** | ✅ Active | `get_current_time`, `convert_time` | `/Users/zaryu/.hermes-portable/venv/bin/mcp-server-time` |
| **github** | ✅ Active | GitHub API tools | `npx @modelcontextprotocol/server-github` |
| **filesystem** | ✅ Active | File read/write/search | scoped `/Users/zaryu` |
| **postgres** (Supabase) | ✅ Active | `query` — read-only | Wrapper bash + `.env` |
| **hermes-sqlite** | ✅ Active | `query_sqlite`, `get_schema`, `list_tables` | kanban.db (READ ONLY) |

### Plugins

| Plugin | Status | Tools |
|--------|--------|-------|
| **spotify** | ✅ Enabled | 7 tools — playback, devices, queue, search, playlists, albums, library |
| **disk-cleanup** | ⬜ Disabled | Auto-clean ephemeral files |

---

## 🗃️ VAULT — Materi Strategis di `brain/projects/`

### `niumination-audit/`
- **INVENTORY.md** — 62 repositori (34 original + 28 fork), 4 TIER
- **L0-L10 Audit Framework** — metadata→arsitektur, 9 profile matrix

### `arena.ai untuk PemdiAcehTengah/`
- **PROMPT_DEEPSEEK.md** (416 baris) — 12 langkah perbaikan
- **LAPORAN_AUDIT_PemdiAcehTengah.md** — 4🔴 kritis, 5🟡 tinggi (✅ all fixed)

### 8 Kemampuan Tersimpan
1. L0-L10 Audit Framework
2. 9 Profile Matrix — klasifikasi proyek per stack
3. Tier Classification — T0 (flagship) → T3 (fork)
4. Supabase Integration for Pemda
5. Security Utilities
6. IKM Formula
7. "Jujur Pattern"
8. WCAG 2.2 AA + PWA

---

## Prioritas Aktivitas

| Timeline | Projek |
|----------|--------|
| 🔥 **Sekarang** | **TEDEO** — T1-T4 ✅ — butuh test plan + deploy — **PemdiAcehTengah** — 🟢 aktif di Production/ |
| 🟢 **1-2 minggu** | niutui (init remote), brain-capture cron fix, TEDEO deploy test |
| 🔄 **4-7 hari** | Niu-Flow maintenance, niu-cast live preview test |
| ⚪ **Bulan ini** | Flame-ADE, niu-studio, niude, niuterm, polish x-downloader |
| 🗄️ **No rush** | Maze-3D, SPBE tools, Startpages, Dotfiles, Forks, archive/labs cleanup |

---

## Maintenance Rules

1. **Proyek baru ditambahkan** → 1 baris di Project Catalog + path di Directory Structure
2. **Proyek dihapus** → hapus dari catalog, pindah ke `archive/` jika perlu disimpan
3. **Stack berubah** → update kolom Stack di catalog
4. **Deployment berubah** → update kolom Deploy (+ URL)
5. **Status berubah** → update kolom Status (✅/🔄/⚪)
6. **DOX anak diupdate** → parent tidak perlu diubah (cuma index)
7. **Backlog diupdate** → cukup update `BACKLOG.md`, referensi di parent DOX sudah cukup

---

> **Dibuat:** 11 Juni 2026
> **Diperbarui:** 17 Jul 2026 — v3.0 — **6 AI Agents + AI-Memory-Collection expanded**
> **Oleh:** Niumination (Afrizal Munthe) — Aceh Tengah
