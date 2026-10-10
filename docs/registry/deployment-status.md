## Custom Domains (idwebhost.com)

| Domain | Status | Last Verified | Catatan |
|--------|--------|---------------|---------|
| `niumination.web.id` | ✅ **LIVE** — ⚠️ **SSL exp 19 Des 2026 (~72 hari)** · ⚠️ **NS mismatch**: resolver publik → Vercel, dashboard idwebhost → NS idwebhost | 8 Okt 2026 | Niu-OSS-Dashboard, Vercel ready. DNS Vercel (`ns1/ns2.vercel-dns.com`) — zona dikelola Vercel. Perlu sinkronisasi NS di dashboard idwebhost |
| `mata.niumination.web.id` | ✅ Existing (Cloudflare) | 21 Sep 2026 | |
| `abstract.biz.id` | 🔴 **DNS REFUSED** — semua nameserver mati | 8 Okt 2026 | Tidak bisa diresolve. Perlu perbaikan NS/registrar sebelum bisa dipakai |
| `kelas.niumination.web.id` | 🟢 **LIVE** — T-07 verified (`configured-correctly`), HTTPS 200 (/, /harga, /kelas/ai-agent-self-host, /verify) | 10 Okt 2026 | Domain attach `vercel domains add` ok, NS propagasi bersih (Vercel). Mode demo — tanpa Supabase/Midtrans (T-01/T-02 ditunda Composio, T-03/T-04/T-17 menunggu akun) |
| `kune-ya.com` | 🔴 **DNS NXDOMAIN** | 8 Okt 2026 | Domain tidak terdaftar/expired. Cek registrar |

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

### 🟢 Vercel — 3 Live, 8 Paused, 2 Never Deployed

> **Verifikasi 8 Okt 2026** via `vercel project ls` (CLI 59.3.0, scope `archk4lis-projects`, 13 proyek) + probe HTTP ke tiap hostname. Status **PAUSED** dikonfirmasi dari body respons `DEPLOYMENT_PAUSED`, bukan dari kode 503 saja.
> ⚠️ Seksi ini tadinya mengklaim "5 Live" dengan `kms-spbe` + `virtual-assistance` HTTP 200 — **keduanya salah**: `kms-spbe` tidak ada di akun Vercel (DNS mati, HTTP 000), dan `virtual-assistance` hostname sebenarnya `virtual-assistance-pi` yang ternyata **PAUSED**.
> ⚠️ **8 Okt 2026:** `kms-spbe` dan `niu-cyber-search-engine` **tidak lagi muncul** di `vercel project ls` (13 proyek, sebelumnya 15 dengan keduanya). Keduanya tidak bisa diverifikasi — dihapus dari tabel di bawah, bukan dianggap live.

| Proyek | Hostname | Status | Last Verified | Catatan |
|--------|----------|--------|---------------|---------|
| `niu-oss` | `niumination.web.id` + `www` | ✅ **200 LIVE** | 8 Okt 2026 | Niu-OSS-Dashboard — HTTP 200 terverifikasi ulang 2 Okt 2026 · domain Verified + www configured-correctly · `origin/main` `4e8a7cf` (2 Okt 2026). ⚠️ **SSL exp 19 Des 2026 (~72 hari)** · ⚠️ **NS mismatch** (resolver publik → Vercel, dashboard idwebhost → NS idwebhost). ~~216 halaman SSG / HEAD `6891b7e`~~ — angka itu dari verifikasi 21 Sep 2026, **tidak diverifikasi ulang** (registry 216, AGENTS.md proyek 214) |
| `pemdi-aceh-tengah` | `pemdi-aceh-tengah.vercel.app` | ✅ **308 → 200** | 8 Okt 2026 | PemdiAcehTengah — 52 OPD SSG, 67 pages, CMS admin aktif (Neon pemdi-cms, 3 env Sensitive) · Patch 8–22 · 59 tes · HEAD `ec57d1a` (27 Sep). **✅ Selesai — pengembangan lanjutan hanya atas instruksi pemilik**. 308 = redirect normal ke `/` |
| `sapa-ai` | `sapa-smart-ai.vercel.app` | ✅ **200 LIVE** | 8 Okt 2026 | SAPA Smart AI — redirect ke `/dashboard`. **Produksi tetap 0.1.0 (`main` `ff00eb8`)** — terverifikasi **1 Okt 2026**, `sapa: active` 2.081 record, AI `deepseek-v4.1-flash` (OpenCode Go) **ON** + deterministik ON, 2 kueri nyata HTTP 200 (11,8–12,1 dtk). Cabang `dev` **0.2.0-dev** (`a3f2e9b`, 165 komit, tag `v0.2.0-dev` → `052f2f0` ujung patch arena `0054`–`0067`) — **belum dipromosikan ke produksi, `main` sengaja tidak disentuh** (keputusan pemilik). Backlog aktif 7 butir → `services/sapa-ai/docs/usulan-ai-tingkat-lanjut/37-BACKLOG-TAHAP-BERIKUTNYA.md`. Repo **PUBLIK** (`visibility: PUBLIC`) — jangan masukkan data tak boleh dipublikasikan |
| `tedeo-web` | `tedeo-web.vercel.app` | ⏸️ **PAUSED** (503) | 8 Okt 2026 | **Body: `DEPLOYMENT_PAUSED`**. Kredensial seed lama (`admin123`) ada di repo publik `ecosystem-config` — **aman selama paused** (tidak ada login yang bisa dieksploitasi dari luar). Tidak dihapus dari git history, lihat catatan di bawah |
| `kune-ya-com` | `kune-ya-com.vercel.app` | ⏸️ **PAUSED** (503) | 8 Okt 2026 | Kune-Ya AI Chat RAG — `DEPLOYMENT_PAUSED`. ⚠️ Domain kustom `kune-ya.com` **DNS NXDOMAIN** (8 Okt 2026) |
| `cc-acehtengah` | `cc-acehtengah.vercel.app` | ⏸️ **PAUSED** (503) | 8 Okt 2026 | Sesuai hiatus 21 Sep 2026 — produksi di-pause pemilik |
| `niu-vermilion` | `niu-vermilion-archk4lis-projects.vercel.app` | ⏸️ **PAUSED** (503) | 8 Okt 2026 | Second Brain — `DEPLOYMENT_PAUSED` |
| `niu-dash-fullstack` | `niu-dash-fullstack-archk4lis-projects.vercel.app` | ⏸️ **PAUSED** (503) | 8 Okt 2026 | `DEPLOYMENT_PAUSED` |
| `virtual-assistance` | `virtual-assistance-pi.vercel.app` | ⏸️ **PAUSED** (503) | 8 Okt 2026 | ⚠️ Registry lama salah tulis 200 — hostname tanpa `-pi` (`virtual-assistance.vercel.app`) tidak pernah ada |
| `niu-private` | `niu-private.vercel.app` | ⏸️ **PAUSED** (503) | 8 Okt 2026 | `DEPLOYMENT_PAUSED` |
| `landing` | `landing-beige-theta.vercel.app` | ⏸️ **PAUSED** (503) | 8 Okt 2026 | Landing page — ⚠️ **domain kustom tetap 200** karena `niumination.web.id` diarahkan ke `niu-oss`, bukan ke `landing` |
| `rekapitulasi-pemdi` | — | ⚪ **Never deployed** | 8 Okt 2026 | Tidak ada production URL. Node 22.x (proj lama) |
| `niutui` | — | ⚪ **Never deployed** | 8 Okt 2026 | Tidak ada production URL |

#### 📌 Catatan keputusan — `docs/references/akun-login.md` (26 Sep 2026)

`docs/references/akun-login.md` ada di repo **PUBLIK** `Niumination/ecosystem-config` sejak commit `bbd01ae` (init, ±2 bulan). Isinya **tidak memuat nilai API key** — hanya catatan status rotasi. Yang ada:

- Kredensial seed TEDEO (nomor HP + `admin123`) — baris 14
- Catatan `OPENAI_API_KEY` belum dirotasi

**Keputusan pemilik 26 Sep 2026: tidak perlu rotasi sekarang, cukup pause Vercel.** `tedeo-web` sudah PAUSED sehingga tidak ada endpoint login yang bisa diserang. Nilai kredensial **tidak** dihapus dari riwayat git (perbaikan butuh `git filter-repo` + force-push + klon ulang semua pihak).

**Sisa risiko (diterima pemilik):** kredensial tetap terbaca di arsip git publik. Selama deployment paused, risiko praktisnya rendah. Kalau proyek di-unpause, **harus** rotasi dulu.

### 🟢 GitHub Pages (10 Live, 1 Broken)

> **Verifikasi 8 Okt 2026.**

| URL | Status | Last Verified | Catatan |
|-----|--------|---------------|---------|
| `niumination.github.io/Niu-LKH` | ✅ v3.2.0 (Merged PR #1 + Fix toLocalISODate) | 26 Sep 2026 | |
| `niumination.github.io/niu-dash` | 🔴 **404 — Pages tidak published** | 8 Okt 2026 | Repo ada tapi GitHub Pages belum diaktifkan/di-publish. Perlu cek Settings → Pages di repo |
| `niumination.github.io/niu-private` | ✅ | 26 Sep 2026 | |
| `niumination.github.io/Niu-Startpage` | ✅ | 26 Sep 2026 | |
| `niumination.github.io/DiskominfoAT` | ✅ | 26 Sep 2026 | |
| `niumination.github.io/Diskominfo-Web` | ✅ | 26 Sep 2026 | |
| `niumination.github.io/SPBE-DevOps-Academy` | ✅ | 26 Sep 2026 | |
| `niumination.github.io/Maze-3D-Game---Web-Based` | ✅ | 26 Sep 2026 | |
| `niumination.github.io/AuditTI-AT` | ✅ | 26 Sep 2026 | |
| `niumination.github.io/zaryu.startpage` | ✅ (fork) | 26 Sep 2026 | |
| `niumination.github.io/NiuHomePage` | ✅ (fork) | 26 Sep 2026 | |

---

## 🖥️ Local Services

> **Verifikasi 8 Okt 2026.**

| Service | Port | Status | Last Verified | Catatan |
|---------|------|--------|---------------|---------|
| Mission Control apex-ui | :3000 | 🔴 **Tidak aktif** | 8 Okt 2026 | Tidak berjalan. Perlu di-start manual |
| **MIRAI Mission Control** | :8800 | ✅ **Running** | 10 Okt 2026 | LaunchAgent `com.mirai.mission-control`, bind `127.0.0.1` only. Repo `github.com/Niumination/mirai` (public). Pengganti niu-mission-control (:5200, diarsipkan). Di `mirai/` (root ekosistem) |
| 9router | :20128 | ✅ Running | 8 Okt 2026 | Model router lokal |
| Camofox | :9377 | ✅ Running | 8 Okt 2026 | Stealth browser |

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
  ├── agents/characters/                                             ❌ (archived 5 Okt 2026)
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
|| **Agent Characters** | `agents/characters/` — 4 herdr agents (arsitek, pembangun, pengawas, penjaga) — ❌ archived 5 Okt 2026 |
|| **Skill Ecosystem Guide** | `docs/skill-ecosystem-guide.md` — Panduan lengkap sistem skill (Hermes, Claude Code, OpenCode, Orca, Herdr) |
|| **Cron Routing Registry** | `docs/registry/hermes-cron-routing.md` — routing output cron Hermes ke thread Telegram (thread **12595** = Cron & Otomasi; thread 7402 = Serbaguna/flex) |
|| **Telegram Thread Registry** | `docs/registry/telegram-threads.md` — persona + model + skill binding per thread group (8 thread aktif, di-rename + icon 5 Okt 2026) |
|| **Cross-Thread Dispatch** | `scripts/dispatch-to-thread.py <thread_id> "<msg>"` — kirim pesan antar-thread via Bot API (MC OFF) |
|| **Ecosystem Health Check** | `scripts/ecosystem-health.py` — gateway/relay/cron/disk/system/Tailscale; cron `0 */2 * * *` → thread 12595 |
|| **Orkestrasi Fase** | `docs/registry/ai-ecosystem.md` → "Hermes Orkestrasi (5 Fase)" — Fase 1-4 done, Fase 5 deferred |

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

## 🔧 Host & Toolchain — Mac Pemilik (Intel x86_64, macOS 26.5)

> **Diverifikasi 3 Okt 2026** saat pemasangan LibreOffice via `brew install --cask libreoffice`.

| Tool | Versi | Status |
|---|---|---|
| Homebrew | 7.0.7 | ✅ berfungsi |
| pandoc | 3.11 | ✅ |
| qpdf | 12.4.1 | ✅ |
| python-docx | — | ✅ |
| LibreOffice (`soffice`) | 26.8.0.3 | ✅ terpasang 3 Okt 2026; wrapper `soffice` di-link ke `/usr/local/bin` |
| tesseract | 5.5.3 | ✅ (bahasa: `eng`, `osd`, `snum` — **tidak ada `ind`**) |
| pymupdf / pypdf / pdfplumber | — | ❌ belum terpasang (dibutuhkan Jalur B) |

**⚠️ Homebrew Tier 3 ( Intel x86_64 ) — catatan ketahanan:**

```
We do not provide support for this platform (as-of September 2026, announced August 2025).
Apple have dropped Intel x86_64 support in macOS Golden Gate (27).
GitHub Actions are dropping macOS Intel x86_64 runners in 2027.
Homebrew no longer builds bottles for this configuration.
Existing bottles may still work, but updated formulae may build from source.
```

Konsekuensi untuk ekosistem:

1. `brew upgrade` pada formula/cask populer **mungkin build dari source** — lebih lama, dan bisa gagal bila dependensi toolchain (Xcode CLT versi tertentu) tidak terpenuhi.
2. **Bottle lama tetap valid**; mesin ini tidak akan tiba-tiba kehilangan paket yang sudah terpasang.
3. Paket yang sekarang install dari bottle **tidak ada jaminan dapat bottle pada update berikutnya**. Saat upgrade penting (mis. node, python, postgres), sediakan waktu ekstra dan uji setelahnya.
4. Jalur alternatif jangka panjang: Mac Apps / installer resmi upstream, atau `uv`/`pipx` untuk tool Python ( independen dari Homebrew ).

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
> **Diperbarui:** 8 Okt 2026 — v4.9 — Update deployment status: DNS issues (abstract.biz.id REFUSED, kune-ya.com NXDOMAIN), SSL expiry warning (niumination.web.id ~72 hari), Vercel 3 live/8 paused/2 never-deployed, niu-dash GH Pages 404, Mission Control :3000 down. Kolom "Last Verified" ditambahkan ke semua tabel.
> **Oleh:** Niumination (Afrizal Munthe) — Aceh Tengah
