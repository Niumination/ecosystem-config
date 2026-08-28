# 📋 BACKLOG — Niumination Ecosystem — MASTER DOCUMENTATION

> **UPDATE: August 27, 2026** — Sync real filesystem + GitHub state. Major: pabrik-aplikasi-gas pilot LIVE (GAS v3), niu-mission-control redesign v3.0 (APEX-MC orb, PR#10 merged, localhost mati, docs update), Trio Governance v2 approved, Skill Bank 68. Mac REDUCE-MOTION ON.

---

## 🗂️ Struktur Root Ekosistem — Niumination v4.0 — Aug 26, 2026

```
Desktop/Niumination/
├── apps/               🏭 13 proyek — deployed & battle-tested
├── services/           🔧 6 proyek — backend & engines
├── sites/              🌐 5 proyek — frontend apps
├── desktop/            🖥️ 4 proyek — native apps
├── agents/             🤖 4 proyek — AI agents + characters + profile
├── labs/               🔬 3 proyek — experiments
├── sandbox/            🧪 7 proyek — dormant (ex-incubator)
├── archive/projects/   📦 2 proyek — archived (niuterm, terax-ai)
├── docs/               📚 Dokumentasi terpadu (reference/, reports/, notebooklm/, dox/)
├── scripts/            ⚙️ 21 ecosystem automation scripts
├── skills/             🧠 **68 skill terpusat** (Layer 1-4 ✅, ecosystem domain, design, software-development, dll)
├── tools/              🛠️ Ponytail MCP + pdf-inspector
├── vault/              🔐 Secrets & credentials (gitignored)
├── brain/              🧠 Obsidian vault (git, terpisah)
├── dotfiles/           🐚 Terminal dotfiles (gitignored)
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

### 🏭 apps/ — 13 Proyek Production

| Proyek | Status | Deploy | Aktivitas Terakhir | Notes |
|--------|:------:|:------:|:------------------:|-------|
| **PemdiAcehTengah** | 🟢 **Active** | Vercel | **PR#4 merged 2026-08-21** | Rumus resmi PermenPANRB 8/2026 + matriks kebutuhan bukti L1-L2 (NotebookLM). Masa penilaian mandiri selesai (bukti diupload eval.spbe.go.id) |
| **Niu-LKH** | ✅ Done | GH Pages | 2026-08-18 | v3.1.1 — clean |
| **niu-vermilion** | 🟢 Active | Vercel | 2026-08-07 | Stable — V1-V5 fixed |
| **kune-ya.com** | 🟢 Active | Vercel | 2026-07-13 | Stable — K1-K5 fixed |
| **niu-dash** | 🟢 Active | GH Pages | 2026-08-21 | v2.16.8 — clean |
| **kopi-aceh-app-android** | ⚪ Sandbox | GitHub | — | Rancangan & source app Android Gerobak Kopi Keliling Aceh Tengah |
| **JHermUSB-portable** | ✅ Done | GitHub | 2026-08-21 | committed 2 file skill sync |
| **mac-web-dashboard** | ✅ Done | GitHub | 2026-08-18 | v1.0.0 |
| **arch-web-dashboard** | ✅ Done | GitHub | 2026-08-18 | v1.0.0 |
| **ai-file-manager-android** | 🟢 Active | Device | 2026-08-10 | Published & tested |
| **ai-first-os** | ⚪ Minor | GitHub | 2026-06-27 | Build kit |
| **Niumination** (profile) | ⚪ Minor | GitHub | **2026-08-26** | Animated terminal README — live |
| **CC.Switch** | 🟢 **Active** | GitHub | 2026-08-07 | Tauri 2 multi-CLI |
| **pabrik-aplikasi-gas** | 🟢 **Active** | Google Apps Script | **2026-08-27** | Pabrik Aplikasi GAS — Pilot 1: Inventaris Aset TI LIVE (v3). Repo mandiri: Niumination/pabrik-aplikasi-gas |

### 🔧 services/ — 6 Backend & API

| Proyek | Priority | Status | Aktivitas Terakhir | Notes |
|--------|:--------:|:------:|:------------------:|-------|
| **cc-acehtengah** | **P2 ⬆** | 🟢 **Active** | **2026-08-29** | DTSEN Multi-Source → AI Smart Query (sumber offline BAPPEDA Des 2025 aktif), EWS, KPI Pimpinan, Laporan Eksekutif. Model AI: huancheng auto |
| **niu-mission-control** | **P2 ⬆** | 🟢 **Active** | **2026-08-27** | v3.0.0 → Redesign APEX-MC (orb golden ring + particle core + reasoning graph + overview HUD + status bar; vanilla JS/CSS, reduced-motion safe). PR#10 merged, PR#11 apex5 draft. MC OFF (localhost mati per "matikan localhost & update dokumentasi"). Swarm orchestrator |
| **niu-cast** | P2 | 🟢 **Active** | 2026-07-21 | v3.6.0 — Mac Connect Bridge |
| **Niu-Flow** | P2 | 🟢 **Remote only** | 2026-07-28 | github.com/Niumination/niu-flow |
| **latticesend** | P3 | 🟢 Active | 2026-08-10 | P2P file transfer — ✅ sudah punya remote |
| **uacc** | P2 🆕 | 🟢 Active | 2026-08-18 | Universal AI Computer Control — MCP server |
| **camofox-browser** | P3 🆕 | ⚪ Third-party | 2026-08-18 | Anti-detection browser |

### 🌐 sites/ — 5 Frontend

| Proyek | Priority | Status | Aktivitas Terakhir | Notes |
|--------|:--------:|:------:|:------------------:|-------|
| **TEDEO-Kanban** | P2 | 🟡 95% | 2026-08-18 | Vite/React/Zustand |
| **niu-dash-fullstack** | P3 | ⏸️ Stale | 2026-07-30 | Next.js 16 |
| **niu-kanban-dash** | P3 | ⏸️ | 2026-08-18 | Vite/React |
| **AuditTI-AT** | P3 | ✅ Live | 2026-08-13 | GH Pages |
| **spatial-vision** | P3 | 🟢 Active | 2026-08-18 | Rust/WASM 3D vision |

### 🖥️ desktop/ — 4 Native

| Proyek | Priority | Status | Aktivitas Terakhir | Notes |
|--------|:--------:|:------:|:------------------:|-------|
| **Flame-ADE** | P2 | ⏸️ Stale | 2026-06-27 | Tauri/Rust |
| **didong-code** | P2 | 🟢 Active | 2026-07-07 | Electron ADE Gayo |
| **joy-connect-for-mac** | P2 🆕 | 🟢 Active | 2026-08-03 | Swift/ADB bridge |
| **x-downloader** | P3 | ✅ Phase 3 | 2026-07-15 | Tauri 2 |

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
| **eKinerja-AfrizalMunthe** | ⚪ Minor | 🟢 Active | Bukti dukung eKinerja Sem 1 2026 — 🔒 private repo |

### 🧪 sandbox/ — 7 Dormant (ex-incubator)

| Proyek | Last Activity | Alasan |
|--------|:------------:|--------|
| niu-studio | Stale 62d | Dual lockfile |
| niude | Stale 54d | Low priority |
| niutui | Stale 36d | Low priority |
| zen | Stale 66d | acehtengah-web/ |
| aistudio-google | Stale | Game files only |
| arena.ai | Stale | Eksperimen |
| x-downloader-backup | Stale 46d | Backup of x-downloader |

### 📦 archive/projects/ — 2 Archived

| Proyek | Size | Alasan |
|--------|:----:|--------|
| niuterm | 621MB | Stale 87 hari |
| terax-ai | 216MB | Stale 81 hari |

---

## 📊 SCOREBOARD EKOSISTEM — 21 Aug 2026 (audit git real)

```text
Repo (rel path)                          Days  Status  Remote  Dirty
-----------------------------------------------------------------
.                                          0  🟢     yes     no
agents/orchestrator                        2  🟢     yes     no
agents/profile                            23  🟡     yes     no
agents/Ultra                              56  ⏸️     yes     no
apps/JHermUSB-portable                     0  🟢     yes     no
apps/PemdiAcehTengah                       2  🟢     yes     no
apps/arch-web-dashboard                    2  🟢     yes     no
apps/mac-web-dashboard                     2  🟢     yes     no
apps/niu-lkh                               2  🟢     yes     no
apps/ai-file-manager-android              10  🟢     yes     no
apps/niu-dash                             10  🟢     yes     no
apps/niu-vermilion                        23  🟡     yes     no
apps/cc-switch                            26  🟡     yes     no
apps/kune-ya.com                          38  ⏸️     yes     no
apps/ai-first-os                          54  ⏸️     yes     no
apps/mac-web-dashboard/hexstrike/repo    115  📦     yes     no
brain                                      0  🟢     yes     no
desktop/joy-connect-for-mac               17  🟡     yes     no
desktop/didong-code                       44  ⏸️     yes     no
desktop/x-downloader                      46  ⏸️     yes     no
desktop/flame-ade                         54  ⏸️     yes     no
dotfiles/zaryu-terminal-dotfiles           0  🟢     yes     no
labs/eKinerja-AfrizalMunthe               14  🟢     yes     no
labs/maze-3d                              54  ⏸️     yes     no
labs/niumination-workspace                58  ⏸️     yes     no
sandbox/niutui                            36  ⏸️     yes     no
sandbox/x-downloader-backup               46  ⏸️     yes     no
sandbox/niude                             54  ⏸️     yes     no
sandbox/niu-studio                        62  📦     yes     no
sandbox/zen                               66  📦     yes     no
services/niu-mission-control               1  🟢     yes     no
tools/camofox-browser                       2  🟢     yes     no
services/uacc                              2  🟢     yes     no
services/cc-acehtengah                     8  🟢     yes     no
services/latticesend                      24  🟡     yes     no
services/niu-cast                         30  🟡     yes     no
sites/niu-kanban-dash                      2  🟢     yes     no
sites/spatial-vision                       2  🟢     yes     no
sites/tedeo-kanban                         2  🟢     yes     no
sites/audit-ti-at                          7  🟢     yes     no
sites/niu-dash-fullstack                  21  🟡     yes     no
tools/pdf-inspector                        1  🟢     yes     no
tools/ponytail                            34  ⏸️     yes     no
archive/backup/*                           12-70 📦     yes     no (5 backup repos, non-aktif)
archive/projects/terax-ai                 81  📦     yes     no
archive/projects/niuterm                  87  📦     yes     no
```

**Total: 48 repos** — 🟢 Active ≤14d: 21 · 🟡 15–30d: 7 · ⏸️ Stale 31–60d: 12 · 📦 Archive/>60d: 8

*Audit 2026-08-21 dari `git log` real (days = sejak commit terakhir). Tidak ada repo tanpa remote. `archive/backup/*` ter-scan tapi bukan proyek aktif.*

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

*Catatan: era konstitusi/core governance sudah DIHAPUS dari ekosistem (keputusan pemilik, 24 Agu 2026). Tidak ada file tersegel; semua folder terbuka untuk agen sesuai DOX.*

---

## 🔴 Perubahan — 26 Aug 2026 — BACKLOG Sync + Entire.io Discovery

*Dokumen diverifikasi langsung dari GitHub org (`gh repo list Niumination`) + filesystem audit 2026-08-26.*

- 📊 **GitHub Org Audit** — 77 repositori terdeteksi (public ~45, private ~32). Fokus: AI Agents, Desktop Apps (Tauri/Electron), Web Dashboards, GovTech, Infra.
- 🏆 **Top Active (Aug 2026):** `Niumination` (profile, Aug 26), `cc-acehtengah` (Aug 24), `hermes-agent` fork (Aug 24), `ecosystem-config` (Aug 24), `niu-mission-control` (Aug 20), `PemdiAcehTengah` (Aug 21).
- 🧠 **Skill Bank** — 42 skill aktif (INDEX.md) — naik dari 22 (Jul 28) / 68 (audit bank pusat Aug 21).
- 🔧 **cc-acehtengah** — DTSEN Multi-Source → AI Smart Query (PR-4b/4c/4d), EWS, KPI Pimpinan, Laporan Eksekutif. 200/200 Vitest passing.
- 🤖 **Entire.io Discovery** — Organisasi open-source untuk **agent memory layer**. Repo kunci: `cli` (⭐5k checkpoint search), `skills` (⭐217 cross-agent), `entire-graph` (entity graph), `external-agents` (Hermes/Claude/Codex/OpenCode plugins), `git-sync`, `pgr` (MCP search). Relevan untuk mengatasi amnesia agen + handoff antar agen di swarm.
- 📝 **BACKLOG.md** — sync faktual: update tanggal, aktivitas terakhir (bukan "14 hari"), hapus "dirty" yang sudah resolved, perbaiki agents 4→5, tools +pdf-inspector.

**Rekomendasi Tindak Lanjut:**
1. Evaluasi `entire-cli` di `ecosystem-config` untuk checkpoint sesi Hermes/JCode/OpenCode.
2. Fork `entireio/skills` → `skills/ecosystem/entire-skills/` sebagai upstream skill bank eksternal.
3. Archive ~10 repo Linux ricing lama di GitHub (`ryuland`, `Zaryu-HyDE`, `RyuDE`, dll) yang sudah di-archive lokal.

---

## 🔴 Perubahan — 24 Aug 2026 — cc-acehtengah: DTSEN Multi-Source → AI Smart Query

- 🔀 **DTSEN agregat → AI pipeline** — `src/services/ai-orchestrator.ts` diintegrasikan dengan `fetchDtsenAgregatPublik()`. Pertanyaan DTSEN agregat (desil, bansos, pembagian wilayah) kini menjawab berdasarkan gabungan SAPA + DTSEN (one door), bukan hanya SAPA.
- 🎯 **Provenance tracking** — setiap evidence DTSEN dilabeli `opd="DTSEN (Kemensos/BPS)"`, `id="dtsen:..."`; narasi WAJIB menyertakan provenance chip + teks "Menurut DTSEN…".
- 🔒 **Privacy tetap** — NIK/per-orang tetap defleksi ke konsol DTSEN terbatas (audit trail, UU 27/2022). k-anonymity sensor k≥5 diterapkan saat publish, bukan di query.
- ✅ **200/200 Vitest passing**, production build clean, TypeScript `tsc --noEmit` clean.
- 📄 **AGENTS.md** — update arsitektur diagram, stack, feature table, dan dokumentasi integrasi DTSEN-AI (DOX pass).
- 🚀 **Push** — commit `f6d7cb2` ke `github.com:Niumination/cc-acehtengah`.

---

## 🔴 Perubahan — 27 Aug 2026 — Pabrik GAS LIVE + MC Retheme + Trio Gov v2

*Dokumen diverifikasi langsung dari tool output (clasp, gh pr, up-eco.sh) 2026-08-27.*

- 🏭 **pabrik-aplikasi-gas** — Pilot 1 **LIVE** (Google Apps Script v3). Inventaris Aset TI ter-deploy: dashboard CRUD + riwayat + self-healing tab Sheet. Repo mandiri: `Niumination/pabrik-aplikasi-gas` (private). Fix: `doGet` createHtmlOutputFromFile + serialisasi Date di `_readAsetRaw`. URL web app verified working.
- 🎨 **niu-mission-control PR#10** — MERGED → Redesign total APEX-MC (faithful replika https://apex-ui-xi.vercel.app). 12 pages → 1 orb view: golden ring R=220 + sound waves + particle core (SVG dots, pengganti three.js) + equalizer + reasoning graph nodes orbit + overview HUD + status bar. Vanilla JS/CSS (zero deps, no FontAwesome/-400k lines). Reduced-motion guard (Mac REDUCE-MOTION ON). Source APEX-UI: https://apex-ui-xi.vercel.app (bukan GitHub repo). PR#11 (apex5) — iterasi tambahan particle core + equalizer kiri/kanan, pending review.
- 🎨 **niu-mission-control PR#6** — MERGED (`8a8b631`) → Mission Core retheme (token APEX gold-ring + cyan-core, 12 halaman). Produksi direstart (pid baru), `healthz`/`readyz` 200. WCAG AA lulus, reduce-motion hormati OS. Issue #5 auto-closed.
- 📜 **Trio Governance v2** — commit `1442732`: intent-based, bukan folder-bound. Aturan dampak + klarifikasi sebelum eksekusi.
- 🧠 **Skill Bank** — 68 skill (bank pusat), INDEX+manifest sinkron, 0 duplikat. Sync-to-agents jalan harian (JCode/Hermes). 3 conflict MC = **abaikan** (bank = katalog, tidak jalan barengan).
- 📊 **Struktur** — apps 13 (tambah pabrik-aplikasi-gas), services 6, agents 4. Mac REDUCE-MOTION ON.

*Status: ekosistem sehat & stabil. PR bot (Niu-LKH#1, afoa#2) masih menganggur — tahan review.*

@cc-acehtengah

- [HOLD] **Credential Broker Phase B — tunggu 2 session jcode selesai** — broker (scripts/keys.sh) sudah jalan & ter-test; migrasi live key DITAHAN karena PID 22342 & 1028 sedang kerja. Lanjut hanya kalau session selesai atau user bilang "lanjut". Ref: docs/references/credential-broker-handoff.md @scripts
