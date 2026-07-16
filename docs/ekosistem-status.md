# 🌐 Ekosistem Niumination — Status Keseluruhan

**Audit:** 9 Jul 2026, 11:15 WIB
**Filesystem:** 33 git + 9 non-git = **42 total item** (DOX: 41)
**Disk:** 8.1 GB
🚫 **Ponytail excluded** per user instruction

---

## 📊 Ringkasan Cepat

| Metrik | Value |
|--------|-------|
| Total Git Repos | 33 (incl. 4 tmux plugins) |
| Production/ 🏭 | 10 ✅ |
| Projects/ 🟡 | 20 |
| Non-Git Dirs | 9 |
| Dirty Repos | 2 (+1 ponytail ⏭️) |
| Cron Jobs | 3 (1 errored ❌) |
| Services | Gateway ✅, Kanban ✅ |
| Eco JSON | ⚠️ Stale — 5 Jul (4 hari) |

---

## 📁 Directory Structure (Filesystem Reality)

```
Niumination/
├── AGENTS.md                          ← DOX v2.6
├── BACKLOG.md                         ← v3.1 redesigned
├── docs/                              ← 🔸 Missing from DOX tree
├── PI/                                ← API keys & credentials
├── Production/                        ← 10 repos — mature & deployed
│   ├── ai-file-manager-android/       ← Kotlin/Jetpack Compose ✅
│   ├── JHermUSB-portable/             ← Shell ✅
│   ├── Niu-LKH/                       ← v3.1.1 GH Pages ✅
│   ├── PemdiAcehTengah/               ← Next.js 14 Vercel 🟢
│   ├── ai-first-os/                   ← Arch ISO builder ✅
│   ├── arch-web-dashboard/            ← Next.js 14 🟢
│   ├── niu-dash/                      ← v2.16.8 GH Pages ✅
│   ├── kune-ya.com/                   ← RAG Vercel 🟢
│   ├── niu-vermilion/                 ← Second Brain Vercel 🟢
│   └── mac-web-dashboard/            ← Next.js 14 🟢
├── archive/
├── backup/
├── brain/                             ← Obsidian vault (git)
├── labs/
├── Niu-Flow/                          ← 🔸 Not in DOX (log/output dir)
├── rekap/                             ← Terminal dotfiles
├── scripts/                           ← Cron & maintenance
├── tools/                             ← Ponytail MCP (⏭️ excluded)
├── Belum disentuh/
└── projects/                          ← 20 dirs
    ├── arena.ai/                      ← AI Arena dashboard
    ├── AuditTI-AT/                    ← GH Pages ✅
    ├── Niu-Flow/                      ← JCode bridge
    ├── TEDEO/                         ← T1-T4 ✅
    ├── TEDEO-Kanban/                  ← 95% ✅
    ├── Ultra/                         ← Puppeteer ✅ GitHub
    ├── aistudio-google/
    ├── didong-code/                   ← 🆕 Electron ADE
    ├── flame-ade/                     ← Tauri 2
    ├── maze-3d/                       ← GH Pages ✅
    ├── niu-cast/                      ← PyQt5
    ├── niu-dash-fullstack/            ← Next.js 16
    ├── niu-kanban-dash/               ← Vite/React
    ├── niu-studio/                    ← Tauri/React
    ├── niude/                         ← Tauri
    ├── niumination-workspace/         ← Next.js 16
    ├── niuterm/                       ← Tauri
    ├── niutui/                        ← Rust/Cargo
    ├── orchestrator/                  ← Python
    ├── terax-ai/                      ← Fork
    ├── x-downloader/                  ← Tauri 2 Phase 3 ✅
    ├── x-downloader-backup/           ← Backup redundant
    └── zen/                           ← acehtengah-web/
```

🔸 = di disk tapi tidak ada di DOX tree (`docs/`, `Niu-Flow/` root)

---

## 🏭 Production/ — Mature & Deployed (10)

| Project | Stack | Deploy | HEAD | Last Push | Status |
|---------|-------|--------|------|-----------|--------|
| **ai-file-manager-android** | Kotlin/Gemini | GitHub | `8b441da` | 23 Jun | ✅ Production |
| **JHermUSB-portable** | Shell | GitHub | `f5fa50b` | 22 Jun | ✅ Production |
| **Niu-LKH** | React/Vite/Supabase | 🟢 GH Pages | `e7f3454` | 20 Jun | ✅ 100% Done |
| **PemdiAcehTengah** | Next.js 14 | 🟢 Vercel | `d480fc8` | ~24 Jun | 🟢 Active |
| **ai-first-os** | Arch ISO | GitHub | `ccb12b3` | 22 Jun | ✅ v1.0.0 |
| **arch-web-dashboard** | Next.js 14 | GitHub | `c056e9d` | 22 Jun | ✅ v1.0.0 |
| **niu-dash** | HTML/CSS/JS | 🟢 GH Pages | `1c20433` | 22 Jun | 🟢 v2.16.8 |
| **kune-ya.com** | Next.js 15 | 🟢 Vercel | `52f432e` | 24 Jun | ✅ K1-K5 |
| **niu-vermilion** | Next.js 16 | 🟢 Vercel | `6f2f036` | 24 Jun | ✅ V1-V5 |
| **mac-web-dashboard** | Next.js 14 | GitHub | `1fd937c` | 24 Jun | ✅ v1.0.0 |

---

## 🟡 projects/ — Active Priority (20)

| Project | Stack | HEAD | Remote | Status |
|---------|-------|------|--------|--------|
| **TEDEO** | Express/React/PostgreSQL | `8c0f6a0` | ✅ SSH | 🔴 **T1-T4 ✅ — butuh deploy** |
| **TEDEO-Kanban** | Vite/React/Zustand | `1bbc96d` | ✅ SSH | 🟡 95% |
| **Niu-Flow** | Python/JCode | `2b92dea` | ✅ SSH | 🟡 90% |
| **Flame-ADE** | Tauri 2/Rust | `fb43693` | ✅ SSH | 🟡 v1.3.0 |
| **niu-cast** | Python/PyQt5 | `8ef4057` | ✅ HTTPS | 🟡 v1.1.1 |
| **didong-code** | Electron/React | 🆕 | ✅ GitHub | 🆕 **Baru publish** |
| **niumination-workspace** | Next.js 16/Prisma | ⚪ | ✅ GitHub | 🟡 4 commits |
| **niu-kanban-dash** | Vite/React | ⚪ | ✅ GitHub | 🟡 |
| **orchestrator** | Python | ⚪ | ✅ GitHub | 🟡 |
| **Ultra** | Puppeteer | ⚪ | ✅ GitHub | 🟡 |
| **niu-dash-fullstack** | Next.js 16 | ⚪ | ✅ GitHub | 🟡 |
| **x-downloader** | Tauri 2/Rust | ⚪ | ✅ SSH | ✅ Phase 3 Done |
| **x-downloader-backup** | — | ⚪ | ❌ | ⚪ Redundant |
| **niu-studio** | Tauri/React | ⚪ | ✅ SSH | ⚪ Dual lockfile |
| **niude** | Tauri | ⚪ | ✅ SSH | ⚪ Dual lockfile |
| **niuterm** | Tauri | ⚪ | ✅ SSH | ⚪ |
| **niutui** | Rust/Cargo | ⚪ | ❌ No remote | ⚪ |
| **zen** | acehtengah-web | ⚪ | ✅ SSH | ⚪ |
| **terax-ai (fork)** | TS | ⚪ | ✅ SSH | ⚪ |
| **AuditTI-AT** | JS/HTML | `c266c40` | ✅ SSH | 🟢 GH Pages |
| **maze-3d** | HTML/JS | ⚪ | ✅ SSH | 🟢 GH Pages |

---

## 🗑️ Dirty Repos

| Repo | Severity | Files |
|------|----------|-------|
| **brain** | 🟡 **Modified + untracked** | `docs/ecosystem-changelog.md` (modified), `logs/divergence-*` (3 new), `inbox/` (2 new daily notes) |
| **arch-web-dashboard** | 🟢 Low | `.DS_Store` (untracked) |
| **niu-dash-fullstack** | 🟡 **Modified source** | `components/DashboardClient.tsx` |
| **tools/ponytail** | ⏭️ **Excluded** | `ponytail-mcp/package-lock.json` (untracked) |

---

## ⏰ CRON STATUS

| Job | Schedule | Last Run | Status |
|-----|----------|----------|--------|
| **brain-daily-capture** | Setiap 21:00 | 8 Jul 21:54 | ❌ **Error** — script error |
| **memory-checkpoint** | Setiap 6 jam | 9 Jul 00:00 | ✅ OK |
| **niu-flow-weekly-audit** | Setiap Senin 08:00 | 6 Jul 09:59 | ✅ OK |

---

## 🌐 SERVICES

| Service | Status | PID | Notes |
|---------|--------|-----|-------|
| **Gateway** (ai.hermes.gateway) | ✅ Running | 2331 | KeepAlive via launchd |
| **Kanban Server** (com.niumination.kanban-server) | ✅ Running | 2332 | launchd |
| **Ecosystem JSON** | ⚠️ Stale | — | `generated_at`: 5 Jul (4 hari) |
| **eco-collect** | — | — | launchd loaded, no PID |
| **health-checker** | — | — | launchd loaded, no PID |
| **changelog-writer** | — | — | launchd loaded, no PID |
| **kanban-sync** | — | — | launchd loaded, no PID |

---

## 🔩 Hermes Agent — Konfigurasi Aktif

| Komponen | Detail |
|----------|--------|
| **Version** | v0.16.0 |
| **Provider** | opencode-zen |
| **Model** | big-pickle |
| **Profile** | default (active) |
| **Gateway** | ✅ launchd KeepAlive |
| **Cron Active** | 3 jobs |
| **MCP Servers** | postgres, sqlite, ponytail, github, time, filesystem |
| **Migration** | ⏸️ Ditunda — portable→native belum dieksekusi |
| **Upgrade** | ⏸️ v0.18.0 — tunggu ekosistem matang |

---

## 🔸 Anomali DOX vs Filesystem

| # | DOX Claim | Filesystem Reality | Severity |
|:-:|-----------|-------------------|----------|
| 1 | DOX tree tidak include `docs/` | `docs/` ada di root — berisi migration docs + audit | 🟢 Minor |
| 2 | DOX tree tidak include `Niu-Flow/` (root) | `Niu-Flow/` di root — cuma log/output | 🟢 Minor (leftover) |
| 3 | DOX count: "41 item" | 42 actual (+ `docs/` + `Niu-Flow/` root) | 🟢 Minor |
| 4 | Eco JSON: 24 proyek | Harusnya ~33+ proyek — stale data | 🟡 Medium |
| 5 | `x-downloader-backup/` di DOX tree? | Ada di disk, perlu cek apakah di-catalog | 🟢 Minor |
| 6 | `labs/` di DOX tree | Tidak ditemukan sub-content, OK | ✅ Match |

---

## 🎯 Prioritas Saat Ini (dari BACKLOG.md)

### 🔥 Sekarang
- **TEDEO** — T1-T4 ✅, butuh test plan + deploy (backend + web frontend)
- **kune-ya.com** — K1-K5 ✅ di Production/, maintenance
- **PemdiAcehTengah** — 52 OPD, 70 pages, Vercel live 🟢

### 🟡 1-2 Minggu
- **TEDEO-Kanban** — 95%, final touches
- **niu-cast** — live preview test
- **Niu-Flow** — butuh maintenance

### 🔄 4-7 Hari
- **didong-code** — 🆕 baru publish, pantau initial issues
- **brain** — inbox cleanup + 2 daily notes belum di-commit
- **x-downloader** — Phase 3 ✅, maintain

---

## ✅ Catatan

1. **brain-daily-capture cron error** — script error kemarin (8 Jul 21:54). Perlu dicek `brain-capture.py`
2. **Ecosystem JSON** — perlu di-regenerate (stale since 5 Jul). `npm run sync-data` di niu-dash-fullstack
3. **niu-dash-fullstack dirty** — `DashboardClient.tsx` modified, belum di-commit
4. **x-downloader-backup** — 995 MB, cek apakah masih diperlukan
5. **Ponytail** — excluded per user instruction ✅
6. **docs/** directory — ada di disk tapi tidak di DOX tree
