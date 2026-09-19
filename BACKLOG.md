# 📋 BACKLOG — Niumination Ecosystem — MASTER DOCUMENTATION

> **UPDATE: September 7, 2026** — Sync real filesystem + GitHub state. Major: pabrik-aplikasi-gas pilot LIVE (GAS v3), niu-mission-control redesign v3.0 (APEX-MC orb, PR#10 merged, localhost mati, docs update), Trio Governance v2 approved, Skill Bank 70. Mac REDUCE-MOTION ON.

---

## 🔄 Alur Kerja Multi-Tempat — 18 Sep 2026

**Klarifikasi pemilik (dikonfirmasi 18 Sep 2026):** ekosistem ini adalah platform utama, tetapi **bukan satu-satunya tempat kerja**. Proyek ekosistem juga dikerjakan di luar (arena.ai, designarena.ai) dan eksperimen berjalan di sandbox terpisah — itu **disengaja** (agar fokus per proyek; pelajaran dari insiden jcode yang merusak internal Mac), **bukan drift**.

Alurnya: hasil dari luar → **konfirmasi ke ekosistem sebelum adopsi besar** → ekosistem memeriksa & melaporkan → keputusan akhir tetap di pemilik. Konflik di masa lalu muncul karena ekosistem memperlakukan pekerjaan luar sebagai anomali; aturan ini menutup celah itu.

- Aturan mengikat ada di `AGENTS.md` → Global Agent Rules: *"Kerja di luar ekosistem & gerbang adopsi"*
- Prosedur auditnya: skill bank `ecosystem/external-pr-audit`
- Pola `skills-lock.json` + skill vendored dari registry upstream (Vercel/Anthropic/addyosmani) = **pola autoskills yang sudah diadopsi ekosistem** (lihat `docs/architecture/autoskills-pattern-adoption.md`), bukan hal asing

**Kasus pertama di bawah aturan ini — PR #5 `PemdiAcehTengah`** (245 berkas, `app/arena-ai-coding-agent`), diaudit 18 Sep 2026:

| Pemeriksaan | Hasil |
|---|---|
| CI (`lint-build`, Vercel) | hijau — tapi **`npm test` belum dijalankan CI** |
| Rahasia di seluruh diff (termasuk dokumen baru) | 0 temuan |
| Import ke 20 komponen yang dihapus | 0 tersisa (bukan fitur hilang) |
| CSP `connect-src 'self'` | aman — Supabase selalu server-side (diverifikasi via grep) |
| SEO (`robots.txt`/sitemap dihapus dari repo) | aman — `next-sitemap` + `postbuild` tetap membuatnya |
| Perubahan DB | aditif saja (`CREATE OR REPLACE FUNCTION`), 0 perintah destruktif |
| Skill vendored `.agents/skills/` + `skills-lock.json` | sesuai pola autoskills; sumber + hash + lisensi tercatat |

**Syarat sebelum merge:** (1) keluarkan 3 dokumen `audit/` dari repo publik (peta kelemahan + pernyataan internal sensitif), (2) perbaiki regresi `.gitignore` (`.data/*.bak-*` → `data/*.bak-*`; 4 berkas backup di disk jadi tidak ter-ignore), (3) `/api/health` berhenti membocorkan `error.message` + nama env ke pemanggil anonim.

**Status: MERGED 18 Sep 2026** sebagai squash `96e018a` (squash dipilih agar commit yang menambahkan `audit/` tidak masuk riwayat `main`; cabang Arena dihapus). Arena mengerjakan ketiganya di cabang (`89f6d4a`); diverifikasi independen: `audit/` 0 entri di cabang & `main`, `.gitignore` membaik, `/api/health` respons generik (detail hanya di `console.error`), 20/20 tes regresi dijalankan sendiri (`node --test`), CI hijau. Tindak lanjut: `ci.yml` menambahkan langkah `npm test` (`c5bdb0a`, dikerjakan pemilik — token GitHub App ditolak GitHub untuk berkas workflow).

**Catatan pasca-merge: SELESAI 18 Sep 2026** — SQL RPC (`bump_rate_limit`, `skm_stats_dimensi`, `rate_limits` + RLS) sudah diterapkan di Supabase (dicek di SQL Editor: 4 fungsi + RLS aktif, counter atomik 1→2). Rate limit kini berjalan di jalur atomik, dan `/api/skm/stats` memakai 1 panggilan RPC. Diverifikasi dari luar: `/api/health` 200 `db:ok`, `/api/skm/stats` 200 terisi, `/api/skm` 200 (view tetap benar setelah ditimpa).

---

## 🧠 Bank Skill — Konsolidasi 18 Sep 2026

Enam skill `skill-bank-*` mendokumentasikan prosedur yang sama (manifest SHA-256 + sync seluruh folder + lockfile) dengan trigger nyaris identik → prosedur yang dipakai bergantung urutan load, bukan mana yang benar. Dikonsolidasikan menjadi **satu**: `ecosystem/skill-bank-management` (naik ke v2.0.0).

- Diserap ke dalamnya: `skill-bank-integrity` (10 poin unik), `skill-bank-maintenance` (10), `skill-bank-ops` (3), `skill-bank-operations` (2), `skill-bank-sync` (0 — murni duplikat)
- Berkas pendukung **dipindah, bukan dibuang**: `autoskills-patterns.md` (gabungan dua versi lama), `cases-2026-08.md`, `skill-bank-manifest-sync.md`, `home-pruning-f4-2026-08-20.md`, `scripts/check-rtk.sh`
- Dihapus di **dua tempat** (bank + target Hermes) karena sync bersifat non-destruktif — skill yang dihapus dari bank tetap hidup di target bila tidak dibersihkan
- **Bank: 149 → 144 skill**, 711 berkas · `--check` 0 mismatch · `--verify-target --structure domain` 0 masalah · lockfile 144 = manifest 144
- `skills/INDEX.md` diperbarui: 5 baris dihapus, counter 121 → 144

**Fakta yang ikut terdokumentasi** (temuan saat verifikasi): target Hermes berisi **bank + skill bawaan Hermes** (±54 skill, author `Hermes Agent`/`Nous Research`/`community` — mis. `apple/*`, `autonomous-ai-agents/codex`). Angka otoritatif "skill kita" adalah isi `manifest.json`, **bukan** jumlah direktori di target. Sinkronisasi sengaja tidak pernah menghapus agar skill bawaan Hermes aman.

**Tindak lanjut (sesi yang sama):**

- **`scripts/up-eco.sh` diperbaiki — bug serius.** `check_backlog_sync` berakhir dengan `[ "$issues" -eq 0 ] && pass ...`; saat ada issue, fungsi mengembalikan *false* → di bawah `set -euo pipefail` **seluruh script mati**. Akibatnya **Phase 5 s/d 12 tidak pernah berjalan** (GitHub Pages, PR, integritas bank skill, SOUL drift, sync status, Mission Control, Telegram, MCP, plugin, Composio) — tanpa pesan error, jadi tampak seperti laporan normal. Bukti perbaikan: keluaran 27 → **245 baris**, exit 0. Dipindai: hanya 1 dari 15 fungsi yang punya pola rawan ini; diberi `return 0` + komentar.
- **Guard baru di Phase 6b-2:** baris counter `> **Status:** N ✅ Aktif` di `skills/INDEX.md` kini dibandingkan dengan `skillCount` manifest (angka otoritatif). Diuji dua arah: counter 999 → ⚠️ mismatch + rekomendasi; counter 144 → ✅ sinkron.
- **`scripts/check-rtk.sh` dipindah** dari bank skill ke `ecosystem/hermes-provider-config/scripts/` (RTK = plugin shell-rewrite, bukan urusan bank; rumah baru sudah punya `references/rtk-verification.md`). Lokasi lama dibersihkan juga di target Hermes.
- **~~Temuan tersisa — belum dikerjakan (menunggu keputusan):~~ ✅ SELESAI 19 Sep 2026** — `skills/INDEX.md` sempat kehilangan **27 baris skill** (ecosystem 6 · creative 6 · mlops 5 · devops 4 · root 4 · development 1 · smart-home 1) — drift lama yang baru terlihat karena up-eco sekarang berjalan penuh. Baris-baris itu sudah dilengkapi. Selisih sisa **144 vs 145** ternyata bukan tabel yang kurang (lihat "Perbaikan Konsistensi & Cron — 19 Sep 2026" di bawah): akarnya manifest/sync ikut menghitung folder tersembunyi.

---

## 🔧 Perbaikan Konsistensi, Cron & Housekeeping — 19 Sep 2026

- **Akar selisih 144 vs 145 (bank skill) — diselaraskan.** Bukan tabel INDEX yang kurang: tabel sudah memuat **144 skill aktif**, dan satu-satunya `SKILL.md` tanpa baris adalah `skills/.archive/cc-acehtengah-maintain` (memang diarsipkan, wajar tidak diindeks). Yang keliru justru **manifest + sync + registry** — ketiganya hanya mengecualikan `.git`, sehingga skill arsip ikut terhitung (145) dan bahkan **terkirim ke target Hermes** (`~/.hermes/skills/.archive/`), padahal `up-eco.sh` sudah memakai aturan `find … -not -path '*/.*'` (144). Perbaikan: `scripts/skill-manifest.py` (semua dot-directory diabaikan), `skills/sync-to-agents.sh` (perintah `find` + `os.walk` registry), counter INDEX 145 → 144, salinan arsip di target dibuang. Verifikasi: filesystem **144** = INDEX **144** = counter **144** = manifest **144** (711 berkas), dan skill arsip **0 kemunculan** di manifest/registry/lockfile.
- **Cron rusak 9–11 hari — akar & perbaikan.** Dua job (`Daily Tab Stash Update`, `Daily Brain — Top 10 URL`) gagal berulang dengan `HTTP 404: No active credentials for provider: meituan`. Akar: `~/.hermes/config.yaml` memaku sesi cron ke `cron.model: meituan/longcat-2.0:free` via `model_provider: 9router`, sementara provider `meituan` **sudah tidak ada lagi** di katalog router (98 model; provider aktif: kr 44 · gh 33 · cf 13 · gemini 8). Perbaikan: `cron.model` → **`gemini/gemini-3.8-flash`**, diuji HTTP 200 **dan tool-calling OK** (syarat wajib — job memakai toolset terminal/file/brain). Cadangan config: `~/.hermes/config.yaml.bak-cron-model-20260919-021552`.
- **Housekeeping cabang — repo `PemdiAcehTengah`.** `verifikasi-arena` (isinya sudah masuk `main` sebagai squash `96e018a`), `fix/sprint-redesign-award-level`, dan `salvage/old-award-redesign` dihapus. Dua cabang lama memuat 2 commit Juni 2026 yang **tidak pernah ada di `main`** → diarsipkan lebih dulu sebagai tag lokal `arsip/2026-06-sprint-redesign` dan `arsip/2026-06-salvage-old-redesign` (pemulihan: `git branch <nama> <tag>`). **Tag belum di-push**, jadi belum ikut cadangan GitHub — menunggu keputusan pemilik.
- **Arsip audit eksternal diselamatkan.** 6 dokumen audit Arena (±104 KB) ternyata hanya hidup di sandbox ephemeral mereka (komentar PR bahkan menyebutnya "disimpan pemilik di lokasi privat" — tidak akurat). Dipulihkan dari objek git `89f6d4a^` ke `vault/_arsip-audit-eksternal/` (izin 600, git-ignored) + README asal-usul. Utang komunikasi ditutup dengan balasan penutup di PR #5 (`issuecomment-5734905208`).
- **Semua mapping model dipindahkan ke provider `nous` (bawaan Hermes) — 19 Sep 2026.** Ditemukan 7 mapping yang menunjuk `explabs` (provider yang sudah tidak ada di katalog 9router): 5 channel Telegram (1/802/803/804/1172), `auxiliary.delegation`, dan `x_search` — dengan bukti nyata (24 sesi `explabs/gpt-5.4-mini` di state.db + 7 error kredensial di log). Akun nous ternyata **tier gratis tanpa kredit**, jadi hanya model `:free` yang bisa dipakai; 7 model gratis diuji dan semuanya lolos HTTP-200 + tool-calling. Mapping kini: delegation & channel 804 → `stepfun/step-3.7-flash:free`; x_search → `upstage/solar-pro4:free`; channel 1/802/803/1172 → `ling-3.0-flash-fin:free` / `ling-3.0-flash-sante:free` / `meituan/longcat-2.0:free` / `poolside/laguna-s-2.1:free`; `cron.model` kembali ke `meituan/longcat-2.0:free` (kini di nous). Detail + tabel lengkap: `docs/registry/model-mapping.md`. Verifikasi: probe katalog+tool-calling, sesi CLI nyata di provider nous, dan cron run ulang.
- **Tindak lanjut (19 Sep, keputusan pemilik: gratis selamanya):** mapping disesuaikan ke opsi gratis terverifikasi. Slot berat (`auxiliary.delegation`, channel 804) → model `:free` OpenRouter (`nvidia/nemotron-3-ultra-550b-a55b:free`, `deepseek/deepseek-v4-flash-0731:free`); sisanya tetap nous `:free`. **`opencode-free` tidak bisa dipakai** — upstream menolak klien luar: `403 FreeTierError "OpenCode's free tier can only be used from within OpenCode"`. Inventaris lengkap (12 model OpenRouter `:free` lolos tool-calling, 7 nous `:free`, jalur cadangan 9router) ada di `docs/registry/model-mapping.md`. **`model.key_env` di blok provider nous dihapus** — provider OAuth, tidak butuh env key; diverifikasi masih jalan lewat uji CLI nyata.
- **Rekomendasi up-eco ditutup — skill-audit.py dipertajam (41 → 0).** Ke-41 temuan diperiksa satu per satu: 21 `path` (dokumentasi SSH sah + fixture uji + komentar kode), 14 `url` (placeholder `HOST`/`PORT`/`{host}`/`url`, fixture `evil.*`), 6 `exfil` (installer vendor: rustup, composio, installer Hermes sendiri, hf.co). Tiga aturan diperbaiki tanpa melonggarkan kategori `secret`: (a) URL placeholder/fixture — host huruf besar, template `{…}`, single-label, `.local/.example/.invalid/.test`, dan berkas di `tests|fixtures|examples|samples|mocks`; (b) `curl … | sh` hanya jadi temuan bila sumbernya bukan domain vendor/allowlist; (c) transmisi dari path sensitif hanya jadi temuan bila satu baris memuat transmisi keluar DAN path privat (kunci publik `.pub` dikecualikan, komentar dikecualikan). **Verifikasi dua arah:** bank nyata 0 temuan; bank umpan berbahaya tetap 8 temuan (kunci privat + installer non-vendor + token sk- + /etc & chmod 777).
- **Kredensial mati dibersihkan.** `SUPABASE_PG_URL` (project `xwljsn…`; password sudah dirotasi di sisi Supabase, entri lokal tak pernah diperbarui) dihapus dari `~/.hermes/.env` setelah dipastikan tidak ada pemakai — MCP `hermes-postgres` yang dulu membacanya sudah tidak ada. Diagnosis lengkap: `docs/reports/SECURITY-AUDIT-2026-09-18.md` → addendum 19 Sep (lokal, git-ignored).

---

## 💤 Pensiun Proyek — 18 Sep 2026

**`JHermUSB-portable` dipensiunkan** (keputusan pemilik). Digantikan oleh `niumination-restore`, yang menyimpan kredensial sebagai ciphertext terenkripsi alih-alih `.env` plaintext.

- Repo `Niumination/JHermUSB-portable`: **diarsipkan (read-only)**, tetap privat
- `config/.env` (20 rahasia nyata) **dikeluarkan dari repo** — commit `d7f5703`; berkas lokal tetap utuh. Nilai lama masih ada di riwayat repo privat
- Folder lokal dipindah: `apps/JHermUSB-portable/` → `inactive-2026-09/JHermUSB-portable/` (27 MB)
- Diverifikasi sebelum dipindah: tidak ada skrip/cron/wrapper maupun entri allowlist DR yang merujuk repo ini
- Temuan sampingan (gate kredensial repo itu): gate **memblokir penghapusan `.env`** (positif palsu yang menghalangi perbaikan) dan punya bug `grep -c … || echo 0` yang menghasilkan nilai `0\n0` sehingga **bisa meloloskan `.env` asli**. Keduanya diperbaiki dan diuji dua arah: `git add -f` berkas `.env` → **diblokir**; penghapusan `.env` → **lolos**.

---

## 🗂️ Struktur Root Ekosistem — Niumination v4.0 — Aug 26, 2026

```
Desktop/Niumination/
├── apps/               🏭 15 proyek — deployed & battle-tested
├── services/           🔧 6 proyek — backend & engines
├── sites/              🌐 5 proyek — frontend apps
├── desktop/            🖥️ 4 proyek — native apps
├── agents/             🤖 3 proyek — AI agents + characters + profile
├── labs/               🔬 2 proyek — experiments
├── sandbox/            🧪 7 proyek — dormant (ex-incubator)
├── archive/projects/   📦 2 proyek — archived (niuterm, terax-ai)
├── docs/               📚 Dokumentasi terpadu (reference/, reports/, notebooklm/, dox/)
├── scripts/            ⚙️ 21 ecosystem automation scripts
├── skills/             🧠 **121 skill terpusat** (Layer 1-4 ✅, ecosystem domain, design, software-development, dll)
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
**Status:** 15 apps, 9 services, 5 sites, 4 desktop, 3 agents, 2 labs, 5 sandbox, 6 archived, **70 skills**

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
| **ai-first-os** | ⚪ Minor | GitHub | 2026-06-27 | Build kit — AGENTS.md missing |
| **Niumination** (profile) | ⚪ Minor | GitHub | **2026-08-26** | Animated terminal README — live |
| **CC.Switch** | 🟢 **Active** | GitHub | 2026-08-30 | Tauri 2 multi-CLI |
| **pabrik-aplikasi-gas** | 🟢 **Active** | Google Apps Script | **2026-09-07** | Pabrik Aplikasi GAS — Pilot 1: Inventaris Aset TI LIVE (v3). Repo mandiri: Niumination/pabrik-aplikasi-gas |

### 🔧 services/ — 6 Backend & API

| Proyek | Priority | Status | Aktivitas Terakhir | Notes |
|--------|:--------:|:------:|:------------------:|-------|
| **cc-acehtengah** | **P2 ⬆** | 🟢 **Active** | **2026-08-29** | DTSEN Multi-Source → AI Smart Query (sumber offline BAPPEDA Des 2025 aktif), EWS, KPI Pimpinan, Laporan Eksekutif. Model AI: huancheng auto |
| **niu-mission-control** | **P2 ⬆** | 🟢 **Active** | **2026-09-07** | v3.0.0 → Redesign APEX-MC (orb golden ring + particle core + reasoning graph + overview HUD + status bar; vanilla JS/CSS, reduced-motion safe). PR#10 merged, PR#11 apex5 draft. MC OFF (localhost mati per "matikan localhost & update dokumentasi"). Swarm orchestrator |
| **niu-cast** | P2 | 🟢 **Active** | 2026-07-21 | v3.6.0 — Mac Connect Bridge |
| **Niu-Flow** | P2 | 🟢 **Remote only** | 2026-07-28 | github.com/Niumination/niu-flow |
| **latticesend** | P3 | 🟢 Active | 2026-08-10 | P2P file transfer — ✅ sudah punya remote |
| **uacc** | P2 🆕 | 🟢 Active | 2026-08-18 | Universal AI Computer Control — MCP server |
| **sapa-ai** | P2 🆕 | 🟢 Active | 2026-08-31 | SAPA Smart AI — SPLP-only public app |
| **camofox-browser** | P3 🆕 | ⚪ Third-party | 2026-08-18 | Anti-detection browser |

### 🌐 sites/ — 7 Frontend

|| Proyek | Priority | Status | Aktivitas Terakhir | Notes |
||--------|:--------:|:------:|:------------------:|-------|
|| **TEDEO-Kanban** | P2 | 🟡 95% | 2026-08-18 | Vite/React/Zustand |
|| **niu-dash-fullstack** | P3 | ⏸️ Stale | 2026-07-30 | Next.js 16 |
|| **niu-kanban-dash** | P3 | ⏸️ | 2026-08-18 | Vite/React |
||| **AuditTI-AT** | P3 | ✅ Live | 2026-08-13 | GH Pages |
||| **landing-web-id** | P3 🆕 | ⚪ Ready | 2026-08-30 | Landing page Bahasa Indonesia — niumination.web.id — Vercel deploy ready |
||| **niu-oss-dashboard** | P2 🆕 | 🟢 Active | 2026-09-19 | Next.js 15 — landing + dashboard OSS 91 repo, API v1, PWA, i18n id/en — repo `Niu-OSS-Dashboard`, CI/test/build hijau, fase 4 go-live pending |
||| **spatial-vision** | P3 | 🟢 Active | 2026-08-18 | Rust/WASM 3D vision |


### 🆕 apps/ — Newly tracked

|| Proyek | Status | Deploy | Aktivitas Terakhir | Notes |
||--------|:------:|:------:|:------------------:|-------|
|| **niu-gayo-agroclimate** | 🟢 Active | Vercel | 2026-09-07 | React 19/Vite 6 |
|| **pi-app-studio-mata** | 🟢 Active | Pi App Studio (Testnet) | 2026-09-16 | MATA Watchdog di Pi Network — `web/` repo mandiri `Niumination/mata-watchdog-pi`, `server/` Express Pi Payments |

### 🖥️ desktop/ — 4 Native

| Proyek | Priority | Status | Aktivitas Terakhir | Notes |
|--------|:--------:|:------:|:------------------:|-------|
| **Flame-ADE** | P2 | ⏸️ Stale | 2026-06-27 | Tauri/Rust |
| **didong-code** | P2 | 🟢 Active | 2026-07-07 | Electron ADE Gayo |
| **joy-connect-for-mac** | P2 🆕 | 🟢 Active | 2026-08-03 | Swift/ADB bridge |
| **x-downloader** | P3 | ✅ Phase 3 | 2026-07-15 | Tauri 2 |

### 🤖 agents/ — 3 AI & Automation

| Proyek | Priority | Status | Notes |
|--------|:--------:|:------:|-------|
| **profile** (`Niumination/Niumination`) | ⚪ Minor | 🟢 Live | Animated terminal README |
| **orchestrator** | P3 | ⏸️ Stale | Python multi-agent |
| ~~**Ultra**~~ | **Archived** | → inactive-2026-09 | Puppeteer automation |
| **characters/** | ⚪ | 🟢 Active | 4 herdr agents (arsitek, pembangun, pengawas, penjaga) |
| **_shared/** | ⚪ | 🟢 Active | Incident & path registry (INCIDENT.md, PATHS.md) |

### 🔬 labs/ — 2 Experiments

| Proyek | Priority | Status | Notes |
|--------|:--------:|:------:|-------|
| **maze-3d** | P3 | ✅ Live | GH Pages |
| ~~**niumination-workspace**~~ | **Archived** | → inactive-2026-09 | Next.js 16 |
| **eKinerja-AfrizalMunthe** | ⚪ Minor | 🟢 Active | Bukti dukung eKinerja Sem 1 2026 — 🔒 private repo |

### 🧪 sandbox/ — 5 Dormant (ex-incubator)

| Proyek | Last Activity | Alasan |
|--------|:------------:|--------|
| ~~niu-studio~~ | **Archived** | → inactive-2026-09 |
| niude | Stale 54d | Low priority |
| niutui | Stale 36d | Low priority |
| ~~zen~~ | **Archived** | → inactive-2026-09 |
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
apps/Mobile-Harness                       0  🟢     yes     no
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

**Total: 50 repos** — 🟢 Active ≤14d: 22 · 🟡 15–30d: 7 · ⏸️ Stale 31–60d: 12 · 📦 Archive/>60d: 8

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
sandbox/                   5   400 MB   Dormant (ex-incubator)
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
| **JCode** | OPENCODE_API_KEY | — | ⚪ Deprecated — not used in ecosystem
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

## 🔴 Perubahan Hari Ini — Sep 7, 2026 — Niumination Ecosystem sync

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
1. Evaluasi `entire-cli` di `ecosystem-config` untuk checkpoint sesi Hermes/OpenCode.
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
- 🧠 **Skill Bank** — 70 skill (bank pusat), INDEX+manifest sinkron. Sync-to-agents jalan ke Hermes saja (JCode dihapus dari pipeline). 3 conflict MC = **abaikan** (bank = katalog, tidak jalan barengan).
- 📊 **Struktur** — apps 13 (tambah pabrik-aplikasi-gas), services 6, agents 4. Mac REDUCE-MOTION ON.

*Status: ekosistem sehat & stabil. PR bot (Niu-LKH#1, afoa#2) masih menganggur — tahan review.*

@cc-acehtengah

- [HOLD] **Credential Broker Phase B — tunggu 2 session jcode selesai** — broker (scripts/keys.sh) sudah jalan & ter-test; migrasi live key DITAHAN karena PID 22342 & 1028 sedang kerja. Lanjut hanya kalau session selesai atau user bilang "lanjut". Ref: docs/references/credential-broker-handoff.md @scripts

@cc-acehtengah

- [ACTIVE] **Rencana eksekusi 100% cc-acehtengah** — pakai `docs/EXECUTION-PLAN-100.md`. Urutan: PR-M00 (WP0.00 credential/PII) → PR-M0a (WP0.0 jiwa==keluarga) → PR-M0f (WP0.14 kunci 32 byte) → PR-M0g (WP0.15 Bapokting) → PR-M0h (WP0.16 normalisasi kecamatan) → PR-M0c (WP0.12 role/BNBA) → PR-M0d (WP0.13 tata kelola branch) → PR-M0e (WP0.5/0.3/0.1 gerbang mutu) → PR-M1 (WP1 semantic layer) → PR-M2 (WP2 router) → PR-M3a+PR-M3 (WP3 stat engine) → PR-M4 (WP4 rekonsiliasi) → PR-M5 (WP5 narasi) → PR-M6 (WP6 eval harness) → PR-M7 (WP7 hardening) → PR-M8 (deploy + doc). Setiap PR berdiri sendiri; jangan merge ke main sebelum PR-M00 + PR-M0a lolos.
- [HOLD] **Jangan deploy production sebelum WP0.00 + WP0.0 selesai** — credential + PII + jiwa==keluarga adalah P0.
- [PENDING] **Audit berkas `cc-acehtengah-v7.zip`** — 92 golden query + 73 audit test sudah diverifikasi. Sisa WP0–WP7 belum dijalankan.

---

## 🔴 Mendesak — 11 Sep 2026 — AI HackFest Batch 3: MATA (Hari-1/5)

- [ACTIVE] **MATA × AI HackFest 2026 — sprint 11–15 Sep** — Watchdog akuntabilitas pengadaan (Python, rule engine D1–D6, dossier PDF). Lokasi: `labs/mata-aihackfest-2026/` (DOX proyek + sub-BACKLOG harian). Sumber: `~/Downloads/aihackfest.zip`. VPS dikelola owner via Kitty; Hermes tidak menyentuh VPS. Deadline karya: 15 Sep (VM dinonaktifkan pasca-batch). Detail harian: `labs/mata-aihackfest-2026/BACKLOG.md` @mata-aihackfest

---

## 🔴 Perubahan — 16 Sep 2026 — Proyek baru: pi-app-studio-mata (MATA di Pi Network)

- 🆕 **`apps/pi-app-studio-mata/`** — MATA Watchdog dibawa ke Pi Network via Pi App Studio AI (Beta). Isi: DOX proyek (`AGENTS.md`), BACKLOG sprint, 3 dokumen teknis + prompt, 2 referensi strategi, demo data 48 records.
- 🌐 **`web/`** — front-end Pi (repo mandiri `github.com/Niumination/mata-watchdog-pi`, sudah punya remote).
- 🔐 **`server/`** — Express backend Pi Payments; `PI_API_KEY` di `.env` **tidak di-track** (`.env.example` disediakan sebagai gantinya).
- 📦 **Repo proyek** — `git init` + commit awal `fe6b3c0` (17 file). `web/` di-ignore di repo proyek karena punya repo sendiri.
- 🧹 **Higiene ekosistem** — `docs/reference/` (regresi dari thread #General MC) dihapus ulang; 5 dokumen PI dipindah ke `docs/reports/`; aturan struktur docs ditambahkan ke Global Agent Rules + prompt 5 thread MC.
- 🧠 **SOUL.md** — pointer lama `docs/reference/` → `docs/registry/` di ketiga salinan (kanonik + portable).

---

## 🔴 Perubahan — 17 Sep 2026 — DR: repo `niumination-restore` DIBANGUN & TERVERIFIKASI

- 🆕 **Repo privat `Niumination/niumination-restore`** — memulihkan Hermes + kredensial + data ekosistem ke device baru **dari GitHub** (tanpa disk eksternal). Tiga lapis, semua **ciphertext**: L1 Hermes (aset Release `*.zip.enc.part-NN`, 130 MB), L1 kredensial (`credentials/*.enc`), L2 data gitignored (`l2-data/*.tar.zst.enc`, 105 berkas → 31 MB).
- ✅ **Drill macOS end-to-end dari GitHub: 20 lulus / 0 gagal** — klon repo dari remote → unduh+verifikasi+dekripsi L1 → `hermes import` (77 sesi) → SOUL.md symlink otomatis → 7 kredensial → L2 156 entri → substitusi **125 berkas** (32 placeholder + **355 path lama**, aman untuk username berbeda) → verify.
- 🧭 **Sisi BUILD** di `scripts/dr-restore/` — `build-credentials.sh`, `build-l2.sh`, `build-services.sh`, `build-l1-release.sh`, `sync-all.sh` (satu perintah refresh), `drill.sh` (bukti dari GitHub).
- 🧯 **Insiden ditutup di hari yang sama:** blob L1 versi pertama terunggah **plaintext** (memuat `~/.hermes/.env`). Release lama dihapus total → diganti ciphertext. Aturan baru: rahasia terenkripsi di **semua** lapis sebelum menyentuh GitHub.
- 🐞 **9 cacat ditemukan & diperbaiki** lewat build+drill (semuanya kelas "lolos-diam-diam"): urutan restore salah (credentials sebelum clone), `openssl -iter` beda build/restore (semua dekripsi akan gagal), `*.age` vs `*.enc` (loop 0 berkas), nama blob L2 (dilewati senyap), target `9router-auth` ke path direktori, `unzip -l | grep -q` + pipefail (laporan "HILANG" palsu), `GH_TOKEN` warisan basi, `python3` di jalur pra-restore, `mapfile` (bash 3.2).
- 📈 **Temuan kecepatan:** `api.github.com/…/assets` **2,35 MB/s** vs `codeload`/git-over-HTTPS **30 KB/s** pada saat yang sama → `fetch-release.sh` memakai API + `curl -C -` (resume).
- 📚 **Docs:** `docs/reports/DR-BUILD-2026-09-17.md` (baru), UJI 7 di `DR-DRILL-2026-09-17-rev3-uji.md`; di repo restore: `README.md` (panduan macOS/Linux/Windows), `docs/UPDATE.md` (mekanisme refresh), `AGENTS.md` (kontrak 9 aturan).
- ⏭️ **Berikutnya:** uji nyata di **Windows** dan **Arch Linux** (belum divalidasi — status ditandai eksplisit, tidak diklaim). Layanan launchd/systemd/Task Scheduler disiapkan tapi belum dijalankan saat drill (sengaja: me-restart gateway dari dalam sesi akan memutus sesi).
- 🔐 **Gate ditutup:** passphrase enkripsi sudah disalin ke cloud oleh pemilik (sebelumnya hanya di Keychain = satu titik kegagalan total).
- ⏰ **Refresh otomatis aktif:** Hermes cron **non-agent** job `525b540c1e86` — **setiap Minggu 21:00 WIB**, menjalankan `~/.hermes/scripts/dr-restore-sync.sh` (membangun ulang 4 lapis → commit → push → pangkas rilis L1 lama), hasilnya dikirim ke **#General grup Niu-MissionControl** (`telegram:-1004204696417:1`). Non-agent = **tanpa LLM**: nol biaya token dan tidak bergantung pada provider model (dua job agent lain di mesin ini sedang `error` dengan `No active credentials for provider: meituan`).
- 🧪 **Terbukti sebelum dipakai:** uji nyata dalam lingkungan mirip cron (`env -i`, PATH minimal) → **exit 0, 7m 45s**, commit `6f52e4d` ter-push, rilis `l1-2026-09-18` lengkap (3 bagian + SHA256SUMS). Dua cacat ditemukan lewat uji itu, bukan ditebak: (1) wrapper menimpa `PATH` sehingga `hermes` hilang → gagal di langkah 4/6 (perbaikan: tambah PATH + guard `command -v`); (2) `gh release upload` tanpa retry — satu `connection reset by peer` menghapus seluruh rilis (perbaikan: unggah per bagian dengan backoff 4 percobaan).
- 🔒 **Audit pasca-cron menemukan tiga celah**, semuanya ditutup: repo restore sama sekali **tidak punya gate anti-rahasia** (`git add -f` adalah satu-satunya jalan rahasia lolos ke riwayat) → `.githooks/pre-commit` baru, diuji 5 kasus, `sync-all.sh` mengaktifkannya otomatis; **kredensial tak dikenal dulu dilewati diam-diam** (restore tetap "sukses" padahal rahasia hilang) → kini restore berhenti + penjaga kontrak di sisi build (7/7 kredensial terpetakan); gate baru saya sempat **memblokir commit sendiri** karena README yang mendokumentasikan pola dianggap kebocoran → pola kini menuntut nilai realistis ≥20 karakter.
- 🧰 **Autoskills (manifest SHA-256) di repo restore:** `integrity.sha256` (40 berkas) + `scripts/integrity-check.sh`; `restore.sh` menjalankannya sebagai **langkah 0** sebelum menyentuh apa pun. Dua bug implementasi tertangkap pengujian: manifest berbasis berkas-di-disk menuduh klon sehat sebagai rusak (atribut `eol` di `.gitattributes`) → kini hash **blob git** dari index + deteksi perubahan lokal; `tr` gagal pada berkas biner → `LC_ALL=C`.
- 🧠 **Premortem** (`apps/niumination-restore/docs/PREMORTEM.md`): 10 cara restore gagal di device lain + tanda peringatan dini + status mitigasi. Tiga langsung ditutup: **klon bisa menggantung selamanya** (terukur 0 KB/30 detik, proses hidup, tanpa error) → timeout 120s ×2 + fallback HTTPS + tarball API; **`--apply` bisa menimpa mesin hidup** (`TARGET_HOME` default `$HOME`) → `live_guard` menolaknya; dan integritas tooling. Tripwire yang belum tertutup: **passphrase dari salinan cloud belum pernah diuji** — semua drill membaca Keychain.
