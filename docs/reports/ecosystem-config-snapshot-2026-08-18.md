# 📸 LAPORAN LENGKAP EKOSISTEM — Niumination

> **Snapshot aktif:** 2026-08-18 18:45 WIB
> **Metode:** up-eco.sh v5.1 + filesystem audit + probe langsung (bukan estimasi)

---

## 1. 🖥️ macOS — Mesin Aktif

| Item | Detail |
|------|--------|
| **Model** | MacBook Pro 16" (MacBookPro16,2) |
| **Chip** | Intel (4 cores) |
| **RAM** | 16 GB |
| **GPU** | Intel UHD Graphics 620 (2 GB VRAM dynamic) |
| **OS** | macOS 26.5 (25F71) — Darwin 25.5.0 |
| **Secure VM** | Enabled |

### Volume & Filesystem

| Mount Point | FS | Writable | Device |
|-------------|----|:--------:|--------|
| `/` (boot) | APFS | ❌ | Samsung SSD 860 EVO 500GB |
| `/System/Volumes/Data` | APFS | ✅ | Samsung SSD 860 EVO 500GB |
| `/Volumes/HermesAgent` | ExFAT | ✅ | Ultra (USB) |
| `/Volumes/Mac Win` | ExFAT | ✅ | Samsung SSD 860 EVO 500GB |
| `/Volumes/Windows X-Lite` | NTFS | ❌ | Samsung SSD 860 EVO 500GB |
| `/Volumes/Niumination` | NTFS | ❌ | Samsung SSD 860 EVO 500GB |

> ⚠️ **Catatan:** Volume NTFS read-only — semua tulis harus lewat `/Users/zaryu/Desktop/Niumination` atau `/Volumes/HermesAgent`.

---

## 2. 📦 Ekosistem Niumination — Git Status

| Repo | Branch | HEAD | Status |
|------|--------|------|:------:|
| **Ecosystem Root** (`ecosystem-config`) | main | `4e773e8` | ⚠️ **2 file dirty** |
| **Profile README** (`Niumination/Niumination`) | main | `5e35f06` | ✅ Clean |
| **brain/** (Obsidian vault) | main | `b50b0f6` | ✅ Clean |

- **Dirty repos lainnya:** ✅ Semua clean (0)
- **Folder asing (tidak terdaftar):** ✅ Tidak ada
- **BACKLOG.md ↔ filesystem:** ✅ Sinkron
- **Pull Requests:** ✅ Tidak ada open PR di org

---

## 3. 📂 Struktur File/Folder Root

```
Desktop/Niumination/
├── apps/       🏭 12 proyek — production & deployed (1.9 GB)
├── services/   🔧 6 proyek — backend & engines (1.7 GB)
├── sites/      🌐 5 proyek — frontend apps (33 MB)
├── desktop/    🖥️ 4 proyek — native apps (62 MB)
├── agents/     🤖 4 proyek — AI agents + characters + profile (34 MB)
├── labs/       🔬 3 proyek — experiments (102 MB)
├── sandbox/    🧪 7 proyek — dormant (202 MB)
├── archive/    📦 Arsip: projects/ (niuterm 621MB, terax-ai 216MB) + docs
├── docs/       📚 Dokumentasi terpadu (364 KB)
├── scripts/    ⚙️ 26 script automation (248 KB)
├── skills/     🧠 Skill Bank pusat — 47 SKILL.md (4.8 MB)
├── tools/      🛠️ Ponytail MCP (2.6 MB)
├── vault/      🔐 Secrets & credentials (gitignored, 1.2 MB)
├── brain/      🧠 Obsidian vault (27 MB, git terpisah)
├── dotfiles/   🐚 Terminal dotfiles (gitignored)
├── AGENTS.md   📋 Root DOX — AI orchestration (53.7 KB)
├── BACKLOG.md  📋 Master dokumentasi (14.6 KB)
├── README.md   (5.1 KB)
└── .gitleaks.toml  🔒 Secret scanner config
```

### Per-folder Detail

**apps/ (12):** JHermUSB-portable, PemdiAcehTengah, ai-file-manager-android, ai-first-os, arch-web-dashboard, cc-switch, kopi-aceh-app-android, kune-ya.com, mac-web-dashboard, niu-dash, niu-lkh, niu-vermilion

**services/ (6):** camofox-browser, cc-acehtengah, latticesend, niu-cast, niu-mission-control, uacc

**sites/ (5):** audit-ti-at, niu-dash-fullstack, niu-kanban-dash, spatial-vision, tedeo-kanban

**desktop/ (4):** didong-code, flame-ade, joy-connect-for-mac, x-downloader

**agents/ (4):** Ultra (automation), characters/ (arsitek, pembangun, pengawas, penjaga), orchestrator/ (Python), profile/ (README generator)

**labs/ (3):** eKinerja-AfrizalMunthe, maze-3d, niumination-workspace

**sandbox/ (7, dormant):** aistudio-google, arena.ai, niu-studio, niude, niutui, x-downloader-backup, zen

**archive/projects/ (2):** niuterm (621MB), terax-ai (216MB)

---

## 4. 📊 Scoreboard Proyek (BACKLOG.md — Jul 29, 2026)

### Aktif & Production

| Proyek | Kematangan | Status | Deploy | Lokasi |
|--------|:----------:|:------:|:------:|--------|
| PemdiAcehTengah | 95% P1 | 🟢 Active | 🟢 Vercel | apps/ |
| cc-acehtengah | 90% P2 | 🟢 Active | 🟢 GitHub | services/ |
| niu-mission-control | 85% P2 | 🟢 Active | 🟢 GitHub | services/ |
| niu-cast | v3.6.0 P2 | 🟢 Active | ⚪ macOS | services/ |
| Niu-LKH | 100% ✅ | ✅ Done | 🟢 GH Pages | apps/ |
| niu-vermilion | V1-V5 P1 | 🟢 Active | 🟢 Vercel | apps/ |
| kune-ya.com | K1-K5 P1 | 🟢 Active | 🟢 Vercel | apps/ |
| TEDEO-Kanban | 95% P2 | 🟡 95% | ✅ GitHub | sites/ |
| CC.Switch | v3.17.0 P2 | 🟢 Active | 🟢 GitHub | apps/ |
| Niu-Flow | 90% P2 | 🟢 Remote | 🟢 GitHub | services/ (remote only) |
| Flame-ADE | v1.3.0 P2 | ⏸️ Stale | ✅ GitHub | desktop/ |
| niu-dash | v2.16.8 P2 | 🟢 Active | 🟢 GH Pages | apps/ |
| JHermUSB-portable | 100% ✅ | ✅ Done | 🟢 GitHub | apps/ |
| mac-web-dashboard | v1.0.0 ✅ | ✅ Done | 🟢 GitHub | apps/ |
| arch-web-dashboard | v1.0.0 ✅ | ✅ Done | 🟢 GitHub | apps/ |
| ai-file-manager | 100% P1 | 🟢 Active | 🟢 Device | apps/ |
| ai-first-os | 45% | ⚪ Minor | 🟢 GitHub | apps/ |
| didong-code | 50% P2 | 🟢 Active | ✅ GitHub | desktop/ |
| joy-connect-for-mac | 60% P2 | 🟢 Active | 🟢 GitHub | desktop/ |
| x-downloader | 100% P3 | ✅ Phase 3 | 🟢 GitHub | desktop/ |
| orchestrator | 40% P3 | ⏸️ Stale | ✅ GitHub | agents/ |
| Ultra | 80% P3 | ⏸️ Stale | ✅ GitHub | agents/ |
| brain | 60% P3 | 🟢 Active | ❌ local | root/ |

### Sandbox (Dormant / Tidak Aktif)

| Proyek | Kematangan | Alasan |
|--------|:----------:|--------|
| niu-studio | 60% | Stale 38d — dual lockfile |
| niude | 50% | Stale 31d — low priority |
| niutui | 20% | Stale 13d — low priority |
| zen | 20% | Stale 42d — acehtengah-web/ |
| aistudio-google | 10% | Game files only |
| arena.ai | 10% | Eksperimen |
| x-downloader-backup | — | Backup |

---

## 5. 🎛️ Niu-MissionControl

| Item | Status |
|------|--------|
| **Port** | 5200 |
| **Server saat ini** | ❌ **TIDAK MERESPON** (down — perlu `python3 server.py`) |
| **Backend routers** | 15 router: system, tasks, config, deploy, audit, skills, terminal, telegram, hermes, agents, ws, artifacts, routines, cost |
| **Stack** | Python (server.py + backend/), Dockerfile, docker-compose.yml, frontend/, dashboard/, swarm/, fusion/, modules/ |
| **Redesign v3** | Backend v3 routers (tasks/agents/cost/ecosystem) ✅ — frontend visual (Phase 5B-5C) ⏳ BELUM |
| **Test** | pytest.ini + tests/ tersedia |

---

## 6. 💬 Telegram Threads (5 aktif)

| Thread | Status | Model | Provider | Pesan | Last Error |
|--------|:------:|-------|----------|:-----:|------------|
| 1 | Active | gemini/gemini-3.x | 9router | 123 | — |
| 802 | Active | gc/gemini-2.5-pro | 9router | 85 | — |
| 803 | Active | cf/@cf/deepseek-... | 9router | 7 | — |
| 804 | Active | cf/@cf/zai-org/... | 9router | 23 | — |
| 1172 | Active | gemini/gemma-4-... | 9router | 148 | — |

---

## 7. 🧠 Skill Bank

| Item | Status |
|------|--------|
| **Total SKILL.md (bank pusat)** | 47 |
| **Domain** | software-development:30, design:5, ecosystem:4, note-taking:3, creative:2, security:1, governance:1, autonomous-ai-agents:1 |
| **Frontmatter YAML** | ✅ 47/47 valid |
| **INDEX.md** | ✅ Sinkron (47 skills) |
| **Duplikasi** | ✅ Tidak ada |
| **Manifest SHA-256** | ✅ Sinkron (47 skill, 267 file) |
| **Sync terakhir** | 2026-08-18 18:00:21 — 47 skill × 3 target |
| **Hermes USB** | ✅ 213 skills |
| **Hermes HOME** | 2 skills |
| **Jcode** | ⚠️ Dir skills tidak ditemukan |

---

## 8. ⚙️ Hermes Agent — Konfigurasi Aktif

### Model & Provider (config.yaml — 18.6 KB)

```yaml
model:
  default: big-pickle
  provider: opencode-zen
  base_url: https://opencode.ai/zen/v1
  api_mode: chat_completions

providers:
  9router:      http://localhost:20128/v1   (NINE_ROUTER_API_KEY)
  agentrouter:  https://agentrouter.org/v1  (AGENTROUTER_API_KEY)
  juan-router:  https://router.juan.web.id/v1 (JUAN_ROUTER_API_KEY)
  huancheng:    https://api.hcnsec.cn/v1    (HUANCHENG_API_KEY, default DeepSeek-V4-Flash)

fallback_providers:
  - juan-router / agnes-2.0-flash
  - 9router / cf/@cf/deepseek-ai/deepseek-r1-distill-qwen-32b
  - 9router / gratislonggar
```

### Health Probe Provider (live test)

| Provider | HTTP | Status |
|----------|:----:|--------|
| **opencode-zen** | 200 | ✅ **LIVE & AKTIF** (primary) |
| **9router** (localhost:20128) | 200 | ✅ LIVE |
| **juan-router** | 401 | ⚠️ Auth diperlukan (key di .env) |
| **agentrouter** | 401 | ⚠️ Auth diperlukan |
| **huancheng** | 401 | ⚠️ Auth diperlukan (key ada di .env) |

### Plugins

| Plugin | Status |
|--------|--------|
| **rtk-rewrite** | ✅ Enabled (satu-satunya di config) |
| hermes-achievements | 📁 Ada di folder, tidak di config |
| orca-status | 📁 Ada di folder, tidak di config |
| telegram_router | 📁 Ada di folder (Aug 9), tidak di config |

> ⚠️ **Catatan:** Folder plugins berisi 4, tapi config hanya enable 1 (`rtk-rewrite`).

### RTK (Rust Token Killer)

| Item | Nilai |
|------|-------|
| **Version** | 0.45.0 |
| **Total commands** | 2,265 |
| **Input tokens** | 9.2M |
| **Output tokens** | 2.9M |
| **Tokens saved** | **6.3M (68.6%)** |
| **Total exec time** | 78m3s (avg 2.1s) |
| **Top command** | `rtk grep` (323×, 3.9M saved) |

### Cron Jobs (Hermes internal)

| Nama | Jadwal | Mode | Last Run |
|------|--------|------|----------|
| memory-checkpoint | setiap 6 jam | no-agent | ✅ OK (18:00) |
| agent-reach-watch | 08:00 harian | agent | ❌ **ERROR — config drift** (provider 'custom'→'opencode-zen'; unpinned) |
| brain-morning-brief | 07:00 harian | no-agent | ✅ OK |
| brain-daily-report | 23:00 harian | no-agent | ✅ OK |
| Pemdi-Learning-Reminder | Senin 08:00 | agent | ✅ OK (17 Aug) |

> ⚠️ **agent-reach-watch error:** Job unpinned, provider berubah dari `custom` ke `opencode-zen`. Perlu pin: `cronjob action=update job_id=c6ec80ed633f provider=... model=...`

### Gateway

| Item | Status |
|------|--------|
| **State** | 🟢 Running (PID 11393) |
| **Telegram** | 🟢 Connected |
| **Active agents** | 1 |
| **MCP servers** | github, sqlite, time, + watchdog ×5 |

---

## 9. 🌍 Deployment

| Target | Status |
|--------|:------:|
| **GH Pages — niu-dash** | ✅ 301 OK |
| **GH Pages — Niu-LKH** | ✅ 301 OK |
| **GH Pages — ecosystem-config** | ✅ 301 OK |
| **Vercel — PemdiAcehTengah** | ✅ 200 OK |
| **Vercel — kune-ya.com** | ⚠️ Tidak merespon (timeout) |
| **Vercel — niu-vermilion** | ⚠️ 307 redirect |
| **GH Pages lokal (5)** | Niu-LKH, niu-dash, maze-3d, AuditTI-AT, DiskominfoAT |

---

## 10. 🔐 Keamanan & Constraints

| Item | Status |
|------|--------|
| **Gitleaks** | ✅ Config ada (.gitleaks.toml), scan weekly |
| **vault/** | 🔒 Secrets gitignored (android-signing, api-key.md, hermes-backup, secrets.zsh) |
| **Config write protection** | ✅ Hermes config ditolak tulis langsung — harus `hermes config` |
| **NTFS volumes** | Read-only — batasi tulis |
| **Secret di .env** | HUANCHENG_API_KEY, NINE_ROUTER_API_KEY, JUAN_ROUTER_API_KEY, AGENTROUTER_API_KEY, OPENCODE_ZEN_API_KEY |

---

## 11. ⚠️ Open Issues (aktif)

1. **Mission Control server DOWN** — port 5200 tidak merespon
2. **Ecosystem Root 2 file dirty** — belum di-commit
3. **Cron `agent-reach-watch` error** — config drift, perlu pin provider/model
4. **kune-ya.com tidak merespon** (deploy check timeout)
5. **niu-vermilion redirect 307** (perlu verifikasi final)
6. **Jcode skill dir tidak ditemukan** (sync target hilang)
7. **3 plugin di folder tidak enabled** di config (hermes-achievements, orca-status, telegram_router)
8. **Huancheng fallback belum dipasang** — hanya bisa via `/model` manual

---

## 12. 📌 Riwayat Git Terakhir

| Repo | Commit Terakhir |
|------|-----------------|
| **Ecosystem Root** | `4e773e8` docs(agents): skill registry last sync |
| **brain/** | `b50b0f6` docs: pemdi-strategi + hermes-config-fix + spatial-vision |
| **Profile** | `5e35f06` feat(profile): ecosystem-config animated SVG |

---

## 13. 📈 Proyeksi & Rekomendasi

### Prioritas Fix (segera)

1. **Start Mission Control** — `cd services/niu-mission-control && python3 server.py`
2. **Commit 2 file dirty** di ecosystem root
3. **Pin cron agent-reach-watch** — update job dengan provider/model saat ini
4. **Verifikasi kune-ya.com & niu-vermilion** deployment

### Prioritas Config

5. **Huancheng sebagai fallback** — tambah ke `fallback_providers` jika mau
6. **Enablize plugin** — tentukan plugin mana yang benar-benar dipakai
7. **Fix Jcode sync target** — dir `/Volumes/HermesAgent/.cache/unix-home/.jcode/skills`

---

*Snapshot dibuat: 2026-08-18 18:45 WIB*
*Sumber: up-eco.sh v5.1, filesystem audit, config.yaml aktual, probe HTTP langsung*
