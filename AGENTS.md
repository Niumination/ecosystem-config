# Niumination — DOX Framework (Root)

**Lokasi:** `~/Desktop/Niumination/`
**Pengguna:** Afrizal Munthe (Niumination) — Pranata Komputer, Diskominfo Aceh Tengah
**DOX Version:** 4.0
|| **Total Projek Lokal:** ~41 git repos
|||||| | **Kanban Board:** "Niumination Ecosystem" — terupdate 16 Jul 2026 ✅

---

## Skill Registry
> Daftar lengkap skill + trigger + level ada di `docs/reference/skill-registry.md` (auto-generated).
> Generator/manifest: `scripts/skill-manifest.py`. Jangan menyalin tabelnya kembali ke sini.

## Global Agent Rules (relocated from SOUL.md v1 — 2026-08-30)
- **Git discipline:** selective `git add` (never blind `git add .`); setiap commit menyertakan perubahan DOX; docs adalah source of truth.
- **macOS services:** service launchd yang butuh jaringan WAJIB WaitNetwork (NetworkState key) sebelum start — pola ini wajib untuk semua service baru; lihat `scripts/` untuk contoh.
- **Skill sync:** sinkronisasi skill bank HANYA lewat tool resmi (`scripts/skill-manifest.py` + `sync-to-agents.sh` + lockfile/hash). Dilarang copy-paste manual antar agent target (Jcode/Hermes/USB).
- **Model mapping:** jangan pakai combo/generic model sebagai mapping utama thread/DM. Sumber mapping sah: hasil auto-discovery (lihat `docs/reference/model-mapping.md`) — fallback chain harus lolos probe HTTP-200 sebelum dicatat.
- **UI/theme (semua proyek UI):** gunakan CSS theme tokens; dilarang hardcode overlay warna / transparansi yang menyimpang dari token proyek.
- **One-home rule:** satu file hanya punya satu repo-home. Berbagi lintas repo hanya via pointer/symlink, bukan salinan yang di-track git.

## Core Contract

1. File **AGENTS.md** adalah DOX (Documentation Optimization Xchange) — binding work contract untuk subtree masing-masing
2. Setiap perubahan kode di proyek mana pun WAJIB diikuti DOX pass sebelum task ditutup
3. Parent DOX ini adalah root index — proyek anak WAJIB punya AGENTS.md sendiri jika kompleksitas > 1 folder
4. Pindah fokus antar proyek: **baca AGENTS.md induk → langsung navigasi ke proyek target → baca AGENTS.md anak jika ada**
5. Jika ada konflik antar DOX, doc yang lebih dekat ke file yang disentuh menang

> ⚠️ **Catatan historis:** Insiden 27 Agu 2026 sudah selesai diperbaiki. Detail ada di `docs/reports/ECOSYSTEM-STATUS-2026-08-30.md`. Jangan edit config saat ada repair berjalan.

---

> Status terkini & insiden: baca `docs/reports/ECOSYSTEM-STATUS-<tanggal>.md` sebelum menyentuh config/scheduler.

## Project Catalog
> Katalog proyek lengkap ada di `docs/reference/project-catalog.md`.

## AI Ecosystem
> Detail AI ecosystem ada di `docs/reference/ai-ecosystem.md`.

## Deployment Status
> Status deployment live ada di `docs/reference/deployment-status.md`.

## Read Before Editing

1. Baca root AGENTS.md ini untuk orientasi
2. Identifikasi proyek yang akan disentuh
3. Baca AGENTS.md pada proyek tersebut (jika ada)
4. Parent DOX hanya index + global rules — detail teknis ada di child DOX
5. Jangan duplikasi info dari child DOX ke parent — cukup referensi

---

## Directory Structure — Real Filesystem (16 Jul 2026)
## Directory Structure — Real Filesystem (29 Jul 2026 — v4.0)

> ⚠️ **Perubahan dari v3.0:** `Production/` → `apps/`, `projects/` terdistribusi ke `services/`, `sites/`, `desktop/`, `labs/`, `sandbox/`, `PI/` → `vault/`, `rekap/` → `dotfiles/`.

```
~/Desktop/Niumination/
├── AGENTS.md                  ← FILE INI — DOX induk
├── BACKLOG.md                 ← Prioritas master semua proyek
├── README.md                  ← Root overview & maturity pipeline
│
├── apps/                      🏭 14 proyek — deployed, battle-tested
│   ├── JHermUSB-portable/     ← Backup DR Hermes Portable (21MB+ skills) ✅
│   ├── niu-lkh/               ← LKH v3.1.1 — 100% Done — Vercel live ✅
│   ├── PemdiAcehTengah/       ← Portal Pemda — 52 OPD, 70 pages — 🟢 Vercel
│   ├── ai-file-manager-android/
│   ├── Mobile-Harness/         ← Claude Code on Android — mobile AI coding IDE
│   ├── ai-first-os/
│   ├── arch-web-dashboard/
│   ├── cc-switch/             ← Tauri 2 multi-CLI — 🟢 v3.17.0
│   ├── kune-ya.com/           ← AI Chat RAG — 🟢 Vercel
│   ├── mac-web-dashboard/
│   ├── niu-dash/              ← v2.16.8 GH Pages — Audit 27/27 ✅
│   ├── niu-vermilion/         ← Second Brain — 🟢 Vercel ✅
│   └── pabrik-aplikasi-gas/   ← Pabrik Aplikasi GAS — Pilot Inventaris Aset TI LIVE (GAS v3) — repo mandiri Niumination/pabrik-aplikasi-gas
│
├── services/                  🔧 6 proyek — backend & engines
│   ├── cc-acehtengah/         ← AI Command Center — Next.js 16
│   ├── latticesend/           ← P2P device transfer
│   ├── niu-cast/              ← Android Device Manager via ADB
│   ├── niu-mission-control/   ← Agent Swarm — FastAPI + WebSocket
│   ├── sapa-ai/               ← SAPA Smart AI — SPLP-only, RSC+ISR 10m (kpi/stats/report/sapa cache, revalidate) ✅
│   └── uacc/                  ← Universal AI Computer Control — 68 MCP tools ✅
│
├── sites/                     🌐 5 proyek — frontend apps
│   ├── audit-ti-at/            ← Vercel Live ✅
│   ├── tedeo-kanban/           ← 95% — Vite/React/Zustand — Vercel ✅
│   ├── niu-dash-fullstack/    ← Next.js 16 Fullstack
│   ├── niu-kanban-dash/       ← React/Vite (port 5199)
│   └── spatial-vision/        ← Rust/WASM — gesture+canvas
│
├── desktop/                   🖥️ 4 proyek — native apps
│   ├── didong-code/           ← Electron AI coding — Gayo
│   ├── flame-ade/             ← Tauri 2/Rust
│   ├── joy-connect-for-mac/   ← macOS native — Infinix bridge
│   └── x-downloader/          ← Tauri 2 — yt-dlp GUI
│
├── agents/                    🤖 4 proyek — AI + automation
│   ├── Ultra/                 ← Puppeteer automation
│   ├── characters/            ← 4 herdr personas
│   ├── orchestrator/          ← Python multi-agent
│   └── profile/               ← GitHub Profile README
│
├── labs/                      🔬 3 proyek — experimental
│   ├── maze-3d/
│   ├── niumination-workspace/
│   └── eKinerja-AfrizalMunthe/  ← Bukti dukung eKinerja Sem 1 2026 🔒 private
│
├── sandbox/                   💤 7 proyek — playground
│   ├── aistudio-google/
│   ├── arena.ai/
│   ├── niu-studio/
│   ├── niude/
│   ├── niutui/
│   ├── x-downloader-backup/
│   └── zen/
│
├── vault/                     🔐 RAHASIA — API keys, credentials (chmod 600)
├── brain/                     📚 Obsidian vault — knowledge base
├── dotfiles/                  🐚 Terminal dotfiles (standalone repo)
├── docs/                      📚 Dokumentasi, guide, referensi
├── scripts/                   ⚙️ Cron & maintenance scripts
├── tools/                     🛠️ Ponytail MCP & utilities
│   ├── camofox-browser/       ← Stealth headless browser (Camoufox) — REST :9377 (upstream jo-inc)
│   └── ponytail/              ← SKILL.md + MCP server code
├── archive/                   📦 Arsip proyek lama (~25MB)
├── apps/niu-gayo-agroclimate/ ← Agro-Climate Kopi Gayo & Mitigasi Bencana — React 19/Vite 6 ✅
├── skills/                    🧠 **ACTIVE** Bank skill terpusat — 68 skill terisi ✅
│
├── .folder-icons/             🖼️ Custom Finder folder icons (PNG + @2x) — lokal, tidak di-track git
├── .gitignore                 — Semua folder proyek child di-ignore
```

---

## 🧠 AI Agent Instructions & Behavior — Auto-loaded Skills

> ⚡ **Layer 3 — DOX Injection Engine:** Skill berikut akan auto-terdeteksi oleh agent berdasarkan trigger keyword. Ini replikasi pola Ponytail untuk semua skill aktif di bank pusat.
> Agent WAJIB menjalankan Decision Ladder Ponytail SEBELUM nulis kode apapun. Skill lain di-load sesuai relevance.

---

### 🔵 Level 1 — Always Active (setiap respons)

#### Ponytail — Lazy Senior Dev Mindset

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
**Source:** `skills/software-development/ponytail-core/SKILL.md`

---

### 🟢 Level 2 — On-Demand via Trigger Keyword

Agent akan auto-load skill berikut jika task description mengandung trigger keyword yang cocok.

| Skill | Trigger Keywords | Source |
|-------|-----------------|--------|
| **impeccable** | design, redesain, "cek ui/ux", "perbaiki desain", craft, critique, polish, animate, "frontend design" | `skills/design/impeccable/` |
| **ui-ux-pro-max** | palette, "font pairing", "design system", "pilih warna", typography, "style guide", "color palette" | `skills/design/ui-ux-pro-max/` |
| **hermes-zero-defect-architect** | zero-defect, "bug fix", rollback, "fix error", "betulin sekarang", "diagnosa dulu" | `skills/software-development/hermes-zero-defect-architect/` |
| **simplify-code** | simplify, sederhanakan, "rapikan kode", "code cleanup", "refactor kode" | `skills/software-development/simplify-code/` |
| **ponytail-review** | "review kode", "over-engineering", "simplify review", "apa yang bisa didelete" | `skills/software-development/ponytail-review/` |
| **ponytail-debt** | "utang teknis", "technical debt", "ponytail defer", "shortcut tracking" | `skills/software-development/ponytail-debt/` |
| **ponytail-gain** | "ponytail gain", "what does ponytail save", "ponytail impact", "ponytail scoreboard" | `skills/software-development/ponytail-gain/` |
| **ponytail-help** | "ponytail help", "ponytail commands", "how to use ponytail" | `skills/software-development/ponytail-help/` |
| **hermes-agent-skill-authoring** | "buat skill", "skill baru", "skill authoring", "tambah skill", "SKILL.md" | `skills/ecosystem/hermes-agent-skill-authoring/` |
| **systematic-debugging** | debug, bug, error, crash, broken, "gak jalan", "kenapa error", troubleshoot, root cause | `skills/software-development/systematic-debugging/` |
| **project-orientation** | orientasi, "cek project", "cek dulu", "lihat dulu", verify, "apa aja isinya", situasional | `skills/software-development/project-orientation/` |
| **document-content-pipeline** | pdf, odl-pdf, extract, markdown, batch convert, cleanup modul, "20 file", indikator | `skills/software-development/document-content-pipeline/` |
| **up-eco** | up-eco, "cek ekosistem", ecosystem check, status proyek, divergence, sync status | `skills/ecosystem/up-eco/` |
| **ekosistem-scaffold** | scaffold, "buat proyek baru", "inisialisasi project", new project setup, standarisasi | `skills/ecosystem/ekosistem-scaffold/` |
| **optimization** | optimasi, "percepat", latency, bottleneck, profiling, "kurangi load", performance | `skills/software-development/optimization/` |
| **ponytail-audit** | audit kode, review codebase, "cek over-engineering", "apa yang bisa didelete", bloat | `skills/software-development/ponytail-audit/` |
| **brainstorming** | brainstorming, "buat desain dulu", "fikir dulu sebelum nulis", "spek dulu", "rencana sebelum kode", "hard gate design" | `skills/software-development/brainstorming/` |
| **writing-plans** | "buat plan", "implementation plan", "task breakdown", "bagi tugas", "langkah-langkah", "tulis plan" | `skills/software-development/writing-plans/` |
| **verification-before-completion** | verifikasi, "cek dulu", "buktikan", "test dulu", "jangan asal claim", "evidence before claims", "run test" | `skills/software-development/verification-before-completion/` |
| **subagent-driven-development** | subagent, "parallel agent", "orchestrasi", "swarm execution", "dispatch agent", "multi-agent coding", sdd | `skills/software-development/subagent-driven-development/` |
| **finishing-a-development-branch** | merge, "selesaiin branch", "pull request", PR, "cleanup branch", "finish branch", "branch selesai" | `skills/software-development/finishing-a-development-branch/` |
| **requesting-code-review** | "minta review", "code review", "review PR", "cek kualitas", "review sebelum merge" | `skills/software-development/requesting-code-review/` |
| **pemdi-evidence-management** | bukti dukung, "bukti pemdi", evidence, PemdiArena, "modul indikator", PermenPANRB, "cek bukti", "update bukti", "inject bukti", "cross-ref bukti" | `skills/software-development/pemdi-evidence-management/` |
| **compliance-checklist-dashboard** | checklist, compliance dashboard, "dashboard kepatuhan", "status checklist", SPBE checklist, "eval dashboard" | `skills/software-development/compliance-checklist-dashboard/` |
| **plan-compliance-audit** | "audit kepatuhan", "compliance audit", "audit plan", "cek spek", "kepatuhan spek", "plan vs reality", "audit ekosistem" | `skills/software-development/plan-compliance-audit/` |

**Cara pakai manual:** `/skill <nama>` atau `hermes -s <nama>`.
**Cara nonaktifkan:** "stop ponytail" atau "normal mode".
**Trigger priority:** Last-loaded wins — skill yang di-load paling akhir override sebelumnya.

---

### ⚪ Level 3 — Future (Agentpedia — porting manual)

_(Kosong — semua skill yang relevan sudah di Level 2 atau sudah di bank pusat.)_

| Skill | Trigger Keywords | Source |
|-------|-----------------|--------|

---

### 📌 Cara Kerja DOX Injection

1. Agent membaca AGENTS.md (selalu terbaca saat kerja di `~/Desktop/Niumination/`)
2. Level 1 (Ponytail) — **always active**, Decision Ladder jalan setiap respons
3. Level 2 — agent scan task description untuk trigger keyword
4. Jika cocok → agent load skill via `skill_view('<nama>')`
5. Skill aktif untuk sesi itu — bisa di-nonaktifkan manual

---

### 🔗 Integrasi dengan Hermes Catalog

Selain DOX injection di atas, Hermes juga punya **catalog skill di system prompt** (`<available_skills>`) yang berisi 148 skills dari `~/.hermes/skills/`. Dua mekanisme ini komplementer:
- **DOX injection** → trigger keyword spesifik untuk ekosistem Niumination
- **Hermes catalog** → daftar lengkap semua skill yang tersedia (agent bisa load kapan pun)

Keduanya jalan bersamaan — tidak saling menimpa.

---

### 🔧 Level 4 — Hermes Self-Management & Persona Upgrade (2026-09-07)

Pada 7 Sep 2026, Hermes mendapatkan upgrade persona dan self-management:

**File konfigurasi baru yang harus selalu dibaca Hermes:**

| File | Tujuan | Update |
|------|--------|--------|
| `~/.hermes/self-schema.json` | Self-state metadata — gateway, model, quota, resource usage | Di-update setiap perubahan berarti (startup, crash, model change, quota change, memory threshold) |
| `~/.hermes/custom_persona.json` | Persona behavior — reasoning style, tone, user focus, Anthropic-family mirror | Dibaca di awal sesi, mempengaruhi gaya respons |
| `~/.hermes/memory_tiering.json` | Memory tier rules — hot/warm/cold, token-saving, brain integration | Digunakan Hermes untuk keputusan routing memori dan biaya |
| `brain/index.json` | Second brain index — 191 file di 30 topik | Di-generate otomatis via `scripts/gen-brain-index.py` |

**Cara Hermes menggunakan upgrade ini:**

1. **Self-awareness:** Di awal sesi, Hermes mengecek `self-schema.json` — status gateway, model yang dipakai, quota, memory usage. Jika ada yang kritis, Hermes alert user.
2. **Persona behavior:** Mengikuti `custom_persona.json` — reasoning singkat tapi terstruktur, direct, honest, user-first, dengan gaya kalimat natural (bukan robotic). Jika tidak yakin, jujur: "Saya kira..." atau "Saya belum yakin...".
3. **Token-aware routing:** Untuk task sederhana (status check, file read, summarisasi data yang sudah ada), Hermes bisa _suggest_ model murah/fast dari `memory_tiering.json` — tapi tidak pernah override pilihan model user. User tetap yang memutuskan.
4. **Brain integration:** Jika task relevan dengan salah satu topik di `brain/index.json` (misal: "debug", "ops", "scripts"), Hermes fetch file yang relevan — maksimal 3 file per sesi, bukan semua brain masuk context.
5. **Memory tiering:** Hot memory (`MEMORY.md`) tetap di-context selalu — tapi dikompak otomatis jika >80% penuh. Warm memory (`brain/index.json`) di-fetch selektif. Cold memory (`brain/archive/`) hanya diakses jika diminta eksplisit.
6. **Self-healing:** Hermes boleh melakukan action sendiri untuk masalah kecil: cache refresh, memory compact, log rotation check. Untuk masalah yang butuh keputusan user (disk cleanup, model quota reset, failover model change), Hermes hanya alert.

**Cara memperbarui persona:**
Untuk mengubah perilaku Hermes, edit `~/.hermes/custom_persona.json`. Untuk menambah/mengurangi self-management rules, edit `~/.hermes/self-schema.json`. Untuk mengubah memory tier behavior, edit `~/.hermes/memory_tiering.json`.

**Cara memperbarui second brain:**
Untuk menambah catatan ke brain, simpan file MD ke `brain/` (warm) atau `brain/archive/` (cold). Lalu regenerasi index:
```bash
python3 ~/Desktop/Niumination/scripts/gen-brain-index.py --force-regenerate
```

**Catatan:** Upgrade ini tidak mengubah cara Hermes load skill — skill tetap di-load via `skill_view('<nama>')` atau via DOX injection trigger keyword (Level 1-2). Upgrade ini hanya menambah layer self-management dan persona behavior di atas mekanisme yang sudah ada.

---

### 📝 Change Log Persona / Self-Management

| Tanggal | Perubahan |
|---------|-----------|
| 2026-09-07 | Persona upgrade: self-management, Anthropic-family style, token-efficient memory, brain integration |

---
