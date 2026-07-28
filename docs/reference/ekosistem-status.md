# 🌐 Ekosistem Niumination — Status Keseluruhan

**Audit:** 20 Jul 2026, 13:17 WIB
**Filesystem:** 29 git + 6 non-git = **35 total item** (DOX: 29)
**Disk:** 8.1 GB
🚫 **Ponytail excluded** per user instruction

---

## 📊 Ringkasan Cepat

| Metrik | Value |
|--------|-------|
| Total Git Repos | 29 |
| Production/ 🏭 | 11 ✅ |
| Projects/ 🟡 | 17 |
| Non-Git Dirs | 6 |
| Dirty Repos | 1 |
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
├── Production/                        ← 12 repos — mature & deployed
│   ├── ai-file-manager-android/       ← Kotlin/Jetpack Compose ✅
│   ├── CC.Switch/                     ← Tauri 2 multi-CLI v3.17.0 🟢
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
└── projects/                          ← 16 dirs
    ├── AuditTI-AT/                    ← GH Pages ✅
    ├── Niu-Flow/                      ← JCode bridge
    ├── TEDEO-Kanban/                  ← 95% ✅
    ├── Ultra/                         ← Puppeteer ✅ GitHub
    ├── cc-acehtengah/                 ← Next.js + Prisma
    ├── didong-code/                   ← 🆕 Electron ADE
    ├── flame-ade/                     ← Tauri 2 v1.3.0
    ├── joy-connect-for-mac/           ← Swift/ADB 🆕
    ├── maze-3d/                       ← GH Pages ✅
    ├── niu-cast/                      ← PyQt5 v1.1.1
    ├── niu-dash-fullstack/            ← Next.js 16
    ├── niu-kanban-dash/               ← Vite/React
    ├── niu-mission-control/           ← 🆕 Ecosystem dashboard
    ├── niumination-workspace/         ← Next.js 16
    ├── orchestrator/                  ← Python
    └── x-downloader/                  ← Tauri 2 Phase 3 ✅
```

🔸 = di disk tapi tidak ada di DOX tree (`docs/`, `Niu-Flow/` root)

---

## 🏭 Production/ — Mature & Deployed (11)

| Project | Stack | Deploy | HEAD | Last Push | Status |
|---------|-------|--------|------|-----------|--------|
| **ai-file-manager-android** | Kotlin/Gemini | GitHub | `8b441da` | 25 Jun | ✅ Production |
| **CC.Switch** | Tauri 2/Rust | GitHub | `0a98f8b` | 20 Jul | ✅ v3.17.0 |
| **JHermUSB-portable** | Shell | GitHub | `f5fa50b` | 22 Jun | ✅ Production |
| **Niu-LKH** | React/Vite/Supabase | 🟢 GH Pages | `e7f3454` | 27 Jun | ✅ 100% Done |
| **PemdiAcehTengah** | Next.js 14 | 🟢 Vercel | `575af70` | 16 Jul | 🟢 Active |
| **ai-first-os** | Arch ISO | GitHub | `5e722eb` | 27 Jun | ✅ v1.0.0 |
| **arch-web-dashboard** | Next.js 14 | GitHub | `e432161` | 9 Jul | ✅ v1.0.0 |
| **kune-ya.com** | Next.js 15 | 🟢 Vercel | `bf36ab9` | 14 Jul | ✅ K1-K5 |
| **mac-web-dashboard** | Next.js 14 | GitHub | `904b956` | 16 Jul | ✅ v1.0.0 |
| **niu-dash** | HTML/CSS/JS | 🟢 GH Pages | `9484640` | 18 Jul | 🟢 v2.16.8 |
| **niu-vermilion** | Next.js 16 | 🟢 Vercel | `a01a558` | 14 Jul | ✅ V1-V5 |

---

## 🟡 projects/ — Active Priority (17)

| Project | Stack | HEAD | Remote | Status |
|---------|-------|------|--------|--------|
| **TEDEO** | Express/React/PostgreSQL | `8c0f6a0` | ✅ SSH | 🔴 **Remote only — butuh VPS** |
| **TEDEO-Kanban** | Vite/React/Zustand | `a6535d4` | ✅ SSH | 🟡 95% |
| **Niu-Flow** | Python/JCode | `0a52845` | ✅ SSH | 🟡 90% |
| **Flame-ADE** | Tauri 2/Rust | `ba9101c` | ✅ SSH | 🟡 v1.3.0 |
| **cc-acehtengah** | Next.js + Prisma | `4b96598` | ✅ SSH | 🟢 Phase 2-3 |
| **didong-code** | Electron/React | `100a14d` | ✅ SSH | 🟢 Active |
| **joy-connect-for-mac** | Swift/ADB bridge | `c5d5959` | ✅ SSH | 🆕 Active |
| **maze-3d** | HTML/JS | `a0a69af` | ✅ SSH | 🟢 GH Pages |
| **niu-cast** | Python/PyQt5 | `afe3c04` | ✅ SSH | 🟡 v1.1.1 |
| **niu-dash-fullstack** | Next.js 16 | `a81c93e` | ✅ SSH | 🟡 Active |
| **niu-kanban-dash** | Vite/React | `e5032f5` | ✅ SSH | 🟡 |
| **niu-mission-control** | Next.js 16 | `db6f0c2` | ✅ SSH | 🟢 New 🆕 |
| **niumination-workspace** | Next.js 16/Prisma | `3deb602` | ✅ SSH | 🟡 Active |
| **orchestrator** | Python | `17aeb97` | ✅ SSH | 🟡 |
| **Ultra** | Puppeteer | `bc8fd35` | ✅ SSH | 🟡 |
| **x-downloader** | Tauri 2/Rust | `0b990ec` | ✅ SSH | ✅ Phase 3 Done |
| **AuditTI-AT** | JS/HTML | `c266c40` | ✅ SSH | 🟢 GH Pages |
| **maze-3d** | HTML/JS | `a0a69af` | ✅ SSH | 🟢 GH Pages |

---

## 🗑️ Dirty Repos

| Repo | Severity | Files |
|------|----------|-------|
| **brain** | 🟡 **Modified + untracked** | `docs/ecosystem-changelog.md` (modified), `logs/divergence-*` (3 new), `inbox/` (2 new daily notes) |

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
| 3 | DOX count: "41 item" | 35 actual (29 git + 6 non-git) | 🟢 Minor |
| 4 | Eco JSON stale | `brain/logs/eco-manifest.json` ada, `total_items` 34 | 🟡 Medium |
| 5 | `reports/` root tidak tercatalog | Ada di disk, bukan git repo | 🟢 Minor |
| 6 | `labs/` di DOX tree | Tidak ada di filesystem | 🟢 Minor |

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
