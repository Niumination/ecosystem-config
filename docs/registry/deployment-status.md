## Custom Domains (idwebhost.com)

| Domain | Status | Catatan |
|--------|--------|---------|
| `niumination.web.id` | ✅ **LIVE** (Verified Vercel, 21 Sep 2026) — DNS Vercel (`ns1/ns2.vercel-dns.com`) — zona dikelola Vercel | Niu-OSS-Dashboard, Vercel ready |
| `mata.niumination.web.id` | ✅ Existing (Cloudflare) |

---

## Domain Allocation Plan

### niumination.web.id — Stable Hub

| Subdomain | Target | Status |
|-----------|--------|--------|
|| `niumination.web.id` | Landing page (link ke semua proyek) | 🟢 **LIVE** (Verified Vercel, DNS via Cloudflare → A record, 21 Sep 2026) |
|| `mata.niumination.web.id` | MATA Watchdog | ✅ Existing (Cloudflare) |
| `dash.niumination.web.id` | Deployment status / monitoring | 🔴 Planned |
| `docs.niumination.web.id` | Dokumentasi ekosistem | 🔴 Planned |

### abstract.biz.id — Experimental Sandbox

| Subdomain | Target | Status |
|-----------|--------|--------|
| `abstract.biz.id` | Pi Network App Studio aggregator | 🔴 Planned |
| `agents.abstract.biz.id` | A2A agent registry / directory | 🔴 Planned |
| `api.abstract.biz.id` | API gateway (microservices) | 🔴 Planned |
| `lab.abstract.biz.id` | Playground / experimental UI | 🔴 Planned |

---

## Deployment Status

### 🟢 Vercel (5 Live, 1 Down)

|| URL | Status | Catatan |
|-----|--------|---------|
| `niu-oss` (`niumination.web.id` + `www`) | ✅ **200 LIVE** | Niu-OSS-Dashboard — 216 halaman SSG, domain Verified + www configured-correctly (22 Sep 2026), GITHUB_TOKEN ✅ live (source: github-api), HEAD `6891b7e` (2026.17 audit + minor bumps next/framer-motion/marked + fix SEO not-found) |
| `pemdi-aceh-tengah.vercel.app` | ✅ 200 | PemdiAcehTengah — 52 OPD SSG, 67 pages (Patch 8–15, 24 Sep) |
| `kms-spbe.vercel.app` | ✅ 200 | KMS SPBE |
| `kune-ya-com.vercel.app` | ✅ 200 | Kune-Ya AI Chat RAG — K1-K5 ✅ |
| `virtual-assistance.vercel.app` | ✅ 200 | VirtualAssistance |
| `niu-cyber-search-engine.vercel.app` | ❌ 404 | Niu-Cyber-Search-Engine — **belum dideploy** |

### 🟢 GitHub Pages (10 Live)

| URL | Status |
|-----|--------|
| `niumination.github.io/Niu-LKH` | ✅ v3.2.0 (Merged PR #1 + Fix toLocalISODate) |
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
| AI Agent | Hermes Agent v0.16.0 — opencode/hy3-free/nemotron-3-ultra-free |

### 📝 Output
- Bahasa Indonesia untuk semua output
- Terstruktur (tabel, layer breakdown, data-driven)
- 🔴🟡🟢 priorities

### 📝 Comment Conventions
Gunakan marker berikut untuk melacak technical debt dan konteks penting di kode:

- `ponytail:` — Deliberate shortcut dengan ceiling dan upgrade path yang diketahui. Format: `ponytail: <ceiling>, <upgrade path>` (dilacak oleh ponytail-debt).
- `NOTICE:` — Workaround dengan removal condition. Format multi-line: `NOTICE: why needed, root cause, source, removal condition`.
- `REVIEW:` — Concern atau keputusan yang perlu second opinion. Tidak ada format baku, tapi harus jelas apa yang direview.

### 📁 Struktur Repo — Niumination Ecosystem v4.0
- `main` branch utama
- **Remote root repo (index):** `origin` = `git@github.com:Niumination/ecosystem-config.git`
- **Remote profile README:** `agents/profile/` → `git@github.com:Niumination/Niumination.git`
- ⚠️ Dua repo berbeda — jangan tertukar
- **Ecosystem maturity pipeline:** `sandbox💤 → labs🔬 → services/sites/desktop/agents🔧 → apps🏭 → archive📦`
- `.gitignore` melindungi: `apps/`, `services/`, `sites/`, `desktop/`, `labs/`, `sandbox/`, `vault/`, `brain/`, `dotfiles/`, `tools/`, `archive/`
- `agents/characters/` dan `docs/` di-track di root repo 🔄

---

## DOX Chain Rules — Niumination Ecosystem v4.0

```
AGENTS.md (root — ~/Desktop/Niumination/)
  ├── apps/niu-lkh/AGENTS.md                                             ✅
  ├── apps/PemdiAcehTengah/AGENTS.md                                     ✅ + data/ + components/ sub-DOX
  ├── apps/niu-dash/AGENTS.md                                            ✅
  ├── apps/kune-ya.com/AGENTS.md                                         ✅
  ├── apps/niu-vermilion/AGENTS.md                                       ✅
  ├── apps/abstract-studio/AGENTS.md                                     ✅ (21 Sep 2026 — ZARYU ABSTRACT STUDIO, repo Kreator, Git LFS)
  ├── ~~services/cc-acehtengah/AGENTS.md~~                                  💤 **HIATUS** (21 Sep 2026 — folder dihapus; arsip sensitif di `vault/_arsip-sensitif/cc-acehtengah-2026-09-21/`, repo privat `arsip-sensitif`)
  ├── services/niu-cast/AGENTS.md                                        ✅
  ├── tools/camofox-browser/DOX.md                                        ✅ (3 Agu 2026 — clone upstream, AGENTS.md milik upstream)
  ├── sites/spatial-vision/AGENTS.md                                     ✅ (3 Aug 2026)
  ├── labs/niumination-workspace/AGENTS.md                               ✅
  ├── desktop/didong-code/AGENTS.md                                      ✅
  ├── desktop/flame-ade/AGENTS.md                                        ✅
  ├── desktop/x-downloader/AGENTS.md                                     ✅
  ├── desktop/joy-connect-for-mac/AGENTS.md                              ✅ (3 Aug 2026)
  ├── agents/Ultra/AGENTS.md                                             ✅
  ├── agents/profile/AGENTS.md                                           ✅
  ├── agents/orchestrator/AGENTS.md                                      ❌ (belum ada)
  ├── agents/characters/arsitek/AGENTS.md                                ✅
  ├── agents/characters/pembangun/AGENTS.md                              ✅
  ├── agents/characters/pengawas/AGENTS.md                               ✅
  ├── agents/characters/penjaga/AGENTS.md                                ✅
  └── docs/skill-ecosystem-guide.md                                      ✅ (panduan skill ecosystem)
```

**Cara navigasi:**
1. Mau kerja di proyek X → baca AGENTS.md induk (ini) → cari proyek X di catalog
2. Navigasi ke folder baru sesuai maturity: `apps/`, `services/`, `sites/`, `desktop/`, `agents/`, `labs/`, `sandbox/`
3. Baca AGENTS.md proyek X (jika ada) untuk detail teknis
4. Jika proyek X tidak punya AGENTS.md, baca README.md atau direktori utamanya
5. Selesai kerja → update DOX yang relevan sebelum commit

---

## Quick Links — Niumination Ecosystem v4.0

| Sumber | Path/Link |
|--------|-----------|
| **BACKLOG Master** | `BACKLOG.md` |
| **Ecosystem Map** | `README.md` |
| **Secrets & Credentials** | `vault/` — **RAHASIA** (chmod 600 ✅) |
| **Obsidian Vault** | `brain/` |
| **Niu-Flow Pipeline** | Ke remote: `github.com/Niumination/niu-flow` (tidak di lokal) |
|| **AI Agent Hooks** | `scripts/hooks/` — 13 hook scripts (claude, codex, copilot, dll) |
|| **Skill Sync Script (Layer 2)** | `skills/sync-to-agents.sh` — auto-sync bank pusat ke Hermes, cron every 6h |
|| **Profile README** | `agents/profile/` → `gh:Niumination/Niumination` |
|| **Agent Characters** | `agents/characters/` — 4 herdr agents (arsitek, pembangun, pengawas, penjaga) |
|| **Skill Ecosystem Guide** | `docs/skill-ecosystem-guide.md` — Panduan lengkap sistem skill (Hermes, Claude Code, OpenCode, Orca, Herdr) |
|| **Cron Routing Registry** | `docs/registry/hermes-cron-routing.md` — routing output cron Hermes ke thread Telegram (thread 7402 = Cron / Otomasi) |

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
| **uacc** 🆕 | ✅ Active | 68 tools — screen, mouse, keyboard, window, browser CDP, OCR, workflow | `services/uacc/` — Python MCP server |
| **context7** 🆕 | ✅ Active | `resolve-library-id`, `query-docs` — up-to-date library docs | `https://mcp.context7.com/mcp` — Streamable HTTP |

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
- **Laporan audit eksternal** — hasilnya sudah ditindaklanjuti (rincian temuan disimpan di vault lokal, tidak untuk repo publik)

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
| 🔥 **Sekarang** | **Bank Skill Pusat** — Layer 1 scaffold siap, menunggu isian Hermes → Layer 2 sync script |
| 🟢 **1-2 minggu** | brain-capture cron fix, joy-connect-for-mac dev, spatial-vision prototyping |
| 🔄 **4-7 hari** | Niu-Flow maintenance, app management UI untuk niu-cast, latticesend spec review |
| ⚪ **Bulan ini** | Flame-ADE, niu-mission-control dev, didong-code polish, x-downloader |
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


























































































---

> **Dibuat:** 11 Juni 2026
> **Diperbarui:** 30 Jul 2026 — v4.8 — **Comment Conventions** standard (ponytail:, NOTICE:, REVIEW). Ponytail-debt now scans both `ponytail:` and `NOTICE:` markers. Ponytail-review gains `fallback:` tag for undocumented precedence chains. UACC AGENTS.md gets improvement roadmap from AIRI computer-use-mcp insights.
> **Oleh:** Niumination (Afrizal Munthe) — Aceh Tengah
