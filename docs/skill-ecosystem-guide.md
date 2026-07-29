# Panduan Skill Ecosystem — Niumination

> **Audiens:** Afrizal Munthe (Niumination)
> **Tujuan:** Memahami bagaimana skill AI bekerja di ekosistem — mana yang auto-load, mana yang manual, mana yang terintegrasi
> **Catatan Revisi v3:** Koreksi setelah tanggapan Hermes. Perubahan: (1) 148 skills → dibedakan "total installed" vs "~10-15 actively used", (2) Catalog injection dijelaskan lebih teknis — loading isi skill tetap manual via `skill_view()`, (3) Ditambahkan skill `document-content-pipeline` + UACC MCP server, (4) AI-Memory-Collection ditandai ⚪ belum diverifikasi, (5) Section 14 diisi jawaban Hermes untuk 6 pertanyaan, (6) Ditambahkan rekomendasi Hermes: update AGENTS.md dulu sebelum Layer 1.
> **Update 29 Jul 2026 — AGENTS.md sync v4.0 ✅ + Layer 1 bank skill terisi 8 skill ✅.** Semua prasyarat Layer 1 terpenuhi. Siap lanjut ke Layer 2 (sync script).

---

## Daftar Isi

1. [Apa Itu "Skill" dalam Konteks AI Coding Agent?](#1-apa-itu-skill-dalam-konteks-ai-coding-agent)
2. [Map Lengkap — 6 Sistem Skill di Ekosistem](#2-map-lengkap--6-sistem-skill-di-ekosistem)
3. [Jcode Skills](#3-jcode-skills)
4. [Hermes Agent Skills](#4-hermes-agent-skills)
   - [Apa Itu Skills di Hermes?](#apa-itu-skills-di-hermes)
   - [Skill vs Memory](#skill-vs-memory)
   - [Mekanisme Loading](#mekanisme-loading)
   - [Struktur Penyimpanan](#struktur-penyimpanan)
   - [Format SKILL.md](#format-skillmd)
   - [Siapa yang Mengelola?](#siapa-yang-mengelola)
   - [Keterbatasan & Hal Penting](#keterbatasan--hal-penting)
   - [Kapan Skill Ter-trigger?](#kapan-skill-ter-trigger)
   - [Contoh Real di Ekosistem](#contoh-real-di-ekosistem)
   - [Skills vs Tools](#skills-vs-tools)
   - [Siklus Hidup Skill](#siklus-hidup-skill)
   - [Ponytail — Satu Skill yang Auto-load](#ponytail--satu-skill-yang-auto-load)
5. [Claude Code Native Skills](#5-claude-code-native-skills)
6. [OpenCode Skills (146 skills)](#6-opencode-skills-146-skills)
7. [Orca Hooks — Pipeline Telemetry (BUKAN Skill)](#7-orca-hooks--pipeline-telemetry-bukan-skill)
8. [Herdr Characters — Persona Agent](#8-herdr-characters--persona-agent)
9. [macOS System AI — DuetExpertCenter](#9-macos-system-ai--duetexpertcenter)
10. [Ringkasan — Auto vs Manual](#10-ringkasan--auto-vs-manual)
11. [Matriks Trigger Detection](#11-matriks-trigger-detection)
12. [Rekomendasi Praktis](#12-rekomendasi-praktis)
13. [Kesimpulan — Jcode vs Hermes](#13-kesimpulan--jcode-vs-hermes)
14. [Roadmap: Menuju Bank Skill Terpusat](#14-roadmap-menuju-bank-skill-terpusat)

---

## 1. Apa Itu "Skill" dalam Konteks AI Coding Agent?

**Skill = seperangkat instruksi/injeksi prompt** yang mengubah perilaku AI agent saat merespons. Analogi:

| Konsep | Analogi |
|--------|---------|
| Skill tanpa AI | Seperti plugin di VS Code — menambah kemampuan |
| Skill di AI agent | Seperti "mode" atau "kepribadian" yang di-inject ke system prompt |
| Mekanisme | Saat skill diaktifkan, perintah/rule ditambahkan ke konteks LLM |

**Skill BUKAN kode yang berjalan** — skill adalah teks instruksi yang mempengaruhi bagaimana AI berpikir dan menulis kode.

---

## 2. Map Lengkap — 6 Sistem Skill di Ekosistem

```
                    ┌──────────────────────────────────────────────────┐
                    │           EKOSISTEM SKILL NIUMINATION           │
                    └──────────────────────────────────────────────────┘
                                      │
         ┌───────────┬───────────┬────┴────┬───────────┬───────────┐
         │           │           │         │           │           │
         ▼           ▼           ▼         ▼           ▼           ▼
     ┌──────┐  ┌────────┐  ┌────────┐ ┌────────┐  ┌────────┐  ┌──────────┐
     │Jcode │  │ Hermes │  │ Claude │ │OpenCode│  │ Orca   │  │ macOS    │
     │Skill │  │ Skills │  │ Code   │ │(146    │  │ Hooks  │  │ System   │
     │System│  │(Hub +  │  │Skills  │ │skills) │  │(12     │  │ AI       │
     │      │  │Curator)│  │        │ │        │  │hooks)  │  │(Duet)    │
     └──────┘  └────────┘  └────────┘ └────────┘  └────────┘  └──────────┘
         │          │          │          │             │             │
         ▼          ▼          ▼          ▼             ▼             ▼
     ┌──────┐  ┌────────┐  ┌────────┐ ┌────────┐  ┌────────┐  ┌──────────┐
     │0     │  │Catalog │  │Agent-  │ │OpenCode│  │Event   │  │ Apple    │
     │skills│  │dalam   │  │pedia   │ │CLI     │  │Pipeline│  │Intellige-│
     │loaded│  │system  │  │(2000   │ │Bridge  │  │(bukan  │  │nce       │
     │      │  │prompt  │  │skills) │ │(Python)│  │ skill) │  │(bukan    │
     │      │  │+ Curat-│  │        │ │        │  │        │  │ skill)   │
     │      │  │or      │  │        │ │        │  │        │  │          │
     └──────┘  └────────┘  └────────┘ └────────┘  └────────┘  └──────────┘
                                                         ┌──────────┐
     ┌──────────┐                                        │ 4 Herdr  │
     │USB Backup│                                        │Characters│
     │/Volumes/ │                                        │(persona) │
     │Hermes... │                                        └──────────┘
     └──────────┘
```

---

## 3. Jcode Skills

### Status Saat Ini: **0 skill ter-load**

### Mekanisme

| Aspek | Detail |
|-------|--------|
| **Lokasi file** | `~/.jcode/skills/<nama>/SKILL.md` (global) |
| | `.jcode/skills/<nama>/SKILL.md` (per-project) |
| | `.claude/skills/<nama>/SKILL.md` (kompatibilitas Claude) |
| **Format** | YAML frontmatter + Markdown instruksi |
| **Cek via** | `skill_manage list` (tool yang ada di Jcode) |
| **Auto-load?** | **TIDAK** — harus di-load manual |
| **Trigger?** | Manual via `/nama_skill` di prompt atau `skill_manage load` |
| **Katalog dalam system prompt** | **TIDAK** — Jcode tidak inject daftar skill ke system prompt |
| **Management otomatis** | **TIDAK** — tidak ada curator/auto-cleanup |
| **Allowed tools** | ✅ Bisa batasi tool mana yang boleh skill akses via `allowed-tools` |

### Cara Aktivasi

```
skill_manage load <nama>   → load skill ke sesi saat ini
skill_manage reload <nama> → reload setelah diedit
skill_manage list          → lihat semua skill yang tersedia
skill_manage read <nama>   → baca isi skill
```

### Skill Bawaan yang Tersedia (belum diinstal)

Jcode merekomendasikan 3 skill bawaan:

| Skill | Fungsi | Source |
|-------|--------|--------|
| `/optimization` | Improve performance, latency, throughput | Bundled di jcode repo |
| `/todo-planning-skill` | Todo list untuk task panjang | Bundled |
| `/firefox-browser` | Kontrol Firefox via skill | Bundled |

Ada juga katalog Anthropic (`/frontend-design`) dan NVIDIA CUDA-X (18 items).

### Mekanisme Loading — yang Sebenarnya Terjadi

**Jcode TIDAK memiliki auto-detection.** Cara kerjanya:

1. Jcode startup → scan `~/.jcode/skills/*/SKILL.md` dan `./.jcode/skills/*/SKILL.md`
2. Skill terdaftar di **katalog internal** — bisa dilihat via `skill_manage list`
3. Tapi **tidak ada daftar skill di system prompt** — agent tidak tahu skill apa yang tersedia kecuali dicek manual
4. User harus explicit `skill_manage load <nama>` atau panggil `/nama`
5. Setelah di-load, instruksi skill masuk ke konteks sesi saat ini
6. **Hilang saat sesi berakhir**

### Perbedaan Kritis dengan Hermes

| Aspek | Jcode | Hermes |
|-------|-------|--------|
| **Skill di system prompt?** | ❌ Tidak — agent buta soal skill yang ada | ✅ Ada — daftar nama+deskripsi di system prompt |
| **Auto-load by relevance?** | ❌ Tidak — harus manual | ✅ Agent bisa load sendiri jika relevan |
| **Curator management?** | ❌ Tidak | ✅ Ada background Curator |

### Kesimpulan untuk Jcode
- **Tidak ada skill yang aktif secara default**
- **System prompt tidak mengandung daftar skill** — agent tidak sadar skill apa yang tersedia
- Harus di-load manual per sesi
- Tidak ada auto-detection berdasarkan task
- Cocok untuk skill yang jarang dipakai / spesifik

---

## 4. Hermes Agent Skills

### Status: **148 skills (total) — ~10-15 actively used**

> ✅ **Confirmed by Hermes:** 148 skills dari `skills_list()`, catalog di-inject ke system prompt tiap sesi, agent bisa auto-load skill yang relevan.
> ⚠️ **Penting:** 148 adalah **total installed**. Sebagian besar creative, MLops, gaming — **tidak relevan** untuk ekosistem Niumination. Yang rutin dipakai hanya **~10-15 skill**.
> ✅ **Model:** Sama seperti Jcode — `big-pickle` via OpenCode Zen, beda API key dan akun.

### Apa Itu Skills di Hermes?

Skills di Hermes adalah prosedur reusable yang disimpan sebagai file `SKILL.md`. Isinya: instruksi, kode, konvensi, dan best practices untuk tugas tertentu.

Skills adalah **"otot" Hermes** — agent tahu skill itu ada dari katalog di system prompt, lalu agent load secara sadar pas lagi butuh. Kalau tidak relevan, skill tidak pernah di-load dan tidak makan konteks sama sekali.

### Skill vs Memory

| Aspek | Memory | Skills |
|-------|--------|--------|
| **Isi** | Fakta, preferensi, environment | Prosedur, workflow, kode |
| **Durasi** | Permanen (lintas session) | Permanen (lintas session) |
| **Kapan dimuat** | Setiap turn (**otomatis**) | Manual / load |
| **Ukuran** | Terbatas (2.2KB) | Bisa besar (full dokumen) |
| **Tujuan** | "Ingat ini tentang user/env" | "Tahu cara melakukan X" |

### Mekanisme Loading

Ada **3 cara** skill bisa aktif:

#### 1. Auto-load via System Prompt (Paling Sering Digunakan)

Setiap awal sesi, Hermes membaca semua available skills dan menyisipkan daftarnya ke system prompt sebagai referensi katalog:

```
<available_skills>
  ponytail: Lazy senior dev mindset...
  up-eco: Ecosystem status check...
  systematic-debugging: 4-phase debug...
  project-orientation: Verify from source...
  ...
</available_skills>
```

**Instruksi di system prompt:**
> "Before replying, scan the skills below. If a skill matches or is even partially relevant to your task, you MUST load it with `skill_view(name)` and follow its instructions"

**⚠️ Penting — clarify teknis:** Yang auto-load ke system prompt hanya **katalog (nama + deskripsi)**, BUKAN isi skill. Isi skill tetap di-load manual oleh agent via `skill_view(name)`.

Ini kuncinya: Hermes sendiri yang memutuskan skill mana yang relevan berdasarkan task. Agent tidak perlu diberi tahu manual — cukup deskripsi task, agent tahu skill apa yang cocok. Tapi agent tetap harus explicit `skill_view(name)` untuk membaca konten lengkap.

#### 2. Manual Load (`/skill <name>`)

Kamu bisa langsung load skill dari chat:

```
/skill ponytail
```

Ini manggil `skill_view(name)` yang menaruh full konten skill ke konteks.

#### 3. CLI flags (`hermes -s <name>`)

Pas start sesi:

```
hermes -s ponytail -s up-eco
```

Atau di cron job:

```
cronjob create ... --skills ponytail
```

### Struktur Penyimpanan

```
~/.hermes/skills/
├── ecosystem/
│   ├── up-eco/SKILL.md
│   └── ekosistem-scaffold/SKILL.md
├── software-development/
│   ├── ponytail/SKILL.md
│   ├── systematic-debugging/SKILL.md
│   └── project-orientation/SKILL.md
├── creative/
│   └── excalidraw/SKILL.md
└── ...
```

Setiap skill adalah folder dengan `SKILL.md` plus optional `references/`, `templates/`, `scripts/`.

**USB Hermes** (portable):
```
/Volumes/HermesAgent/HermesAgentUSB/data/skills/<category>/<name>/SKILL.md
```

### Format SKILL.md

```yaml
---
name: ponytail
description: "Lazy senior dev mindset — YAGNI, stdlib first..."
version: 1.0.0
author: Hermes Agent
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [software-development, standards]
---
# Ponytail — Lazy Senior Dev Mindset
## Trigger
Gunakan skill ini ketika...
## Prosedur
1. Jalankan Decision Ladder...
2. Pilih solusi paling sederhana...
## Pitfalls
...
```

### Siapa yang Mengelola?

Ada **3 pihak** yang mengelola skill di Hermes:

#### 1. Curator (Background Agent Otomatis)

Hermes punya Curator — background process yang otomatis:

- **Tracking** — usage statistik per skill (`last_activity_at`, `use_count`)
- **Stale detection** — skill yang 30+ hari tidak dipakai → marked stale
- **Archive** — skill yang 90+ hari tidak dipakai → diarsipkan (bukan dihapus)
- **Backup** — sebelum pruning, bikin tar.gz backup

**Config Curator:**
```yaml
curator:
  enabled: true
  interval_hours: 168  # tiap 7 hari
  stale_after_days: 30
  archive_after_days: 90
```

**Caveat:** Curator cuma sentuh skill dengan `created_by: "agent"`. Skill built-in/hub aman. **Never deletes** — paling parah di-archive.

#### 2. Agent (Hermes) — Create, Patch, Delete

Lewat tool `skill_manage()`:

```
# Buat skill baru
skill_manage(action="create", name="my-skill", content="...")

# Update (patch) — prefered
skill_manage(action="patch", name="my-skill", old_string="...", new_string="...")

# Edit — full rewrite
skill_manage(action="edit", name="my-skill", content="...")

# Delete
skill_manage(action="delete", name="my-skill")
```

#### 3. Kamu (User) — CLI

```
hermes skills list              # Lihat semua
hermes skills search QUERY      # Cari di hub
hermes skills install ID        # Install dari hub
hermes skills config            # Enable/disable per platform
hermes skills check             # Cek update
hermes skills update            # Update outdated
hermes skills uninstall N       # Hapus
hermes skills browse            # Browse katalog
```

**Hub/Skill Registry:** Repository publik di GitHub yang berisi ribuan skill. Bisa install langsung:

```
hermes skills install opencode
```

### Keterbatasan & Hal Penting

| Aspek | Kondisi |
|-------|---------|
| **Auto-load** | ❌ Skill TIDAK otomatis di-load ke konteks. Hanya daftar nama + deskripsi yang masuk system prompt |
| **Full load** | ✅ Agent harus explicit `skill_view(name)` untuk baca full konten |
| **Inject ke konteks** | ✅ Setelah di-load, skill jadi bagian dari system prompt |
| **Memory vs Skill** | ❌ Skill tidak muncul di memory. Memory itu fakta singkat, skill itu prosedur |
| **Skill conflict** | ⚠️ Kalau ada 2 skill kontradiktif, yang di-load paling akhir yang menang |
| **Pinned skill** | 🔒 Skill yang di-pin tidak bisa di-delete — cuma curator yang skip |
| **Cron job** | ✅ Bisa attach skills ke cron: `cronjob create ... --skills ponytail` |

### Kapan Skill Ter-trigger?

**Tidak otomatis** — Hermes yang menentukan dari **3 sinyal**:

1. **Task description** — "gas /up-eco" → agent tahu up-eco relevan
2. **Konteks masalah** — "dotfiles broken" → agent load ponytail (YAGNI approach) + systematic-debugging
3. **Pola berulang** — setelah beberapa kali agent lihat polanya, skill jadi referensi

### Contoh Real di Ekosistem

**Skenario:** Kamu bilang "cek dulu kenapa dotfiles tidak jalan"

1. System prompt bilang "scan available skills"
2. Agent lihat: `macos-disk-maintenance`, `ponytail`, `systematic-debugging`, `project-orientation`
3. Loading: `skill_view('systematic-debugging')` — buat 4-phase debug
4. Loading: `skill_view('project-orientation')` — biar verifikasi dari source
5. Eksekusi: `find /Users/zaryu -type l ! -exec test -e {} \;` → ketemu broken symlink
6. Loading: `skill_view('ponytail')` — pilih solusi paling sederhana (re-stow, bukan rebuild)
7. Selesai ✅

**Skenario Lain — document-content-pipeline (dibuat 29 Jul 2026):**

1. Task: "Ekstrak 20 PDF modul indikator → Markdown → JSON → Website"
2. Agent detect match: `document-content-pipeline` cocok untuk workflow batch ODL-PDF
3. Loading: `skill_view('document-content-pipeline')` — baca prosedur batch convert + cleanup
4. Eksekusi: 20 file PPT as PDF → Markdown → cleanup duplikat → JSON → website
5. Hasil: 20 file Markdown terstruktur, 500MB duplikat gambar siap cleanup ✅

> Skill ini punya struktur `scripts/` (odl-pdf-batch.py) + `references/` — jadi template untuk skill kompleks di bank pusat.

### Skills vs Tools

| Aspek | Skills | Tools |
|-------|--------|-------|
| **Isi** | Instruksi + prosedur | Fungsi executable |
| **Contoh** | "Systematic debugging: 4-phase" | `read_file`, `terminal`, `web_search` |
| **Dibaca oleh** | Agent (LLM) — agent bacanya | Runtime — dijalankan langsung |
| **Format** | Markdown | Python/API |

### Siklus Hidup Skill

```
Create (agent) → Active (dipakai) → Stale (30 hari idle)
→ Archived (90 hari) → Restored (kalau dipakai lagi)
                ↓
           Deleted (manual)
```

### Ponytail — Satu Skill yang Auto-load

#### Status: **Terdefinisi di DOX root** + **file SKILL.md di tools/**

**Ponytail adalah satu-satunya skill di ekosistem yang auto-load — tapi dengan mekanisme berbeda dari Hermes biasa.**

| Aspek | Detail |
|-------|--------|
| **Lokasi definisi (utama)** | `AGENTS.md` baris 136-154 (root DOX Niumination) |
| **Juga ada di** | `tools/ponytail/skills/ponytail/SKILL.md` (standalone — path salah untuk Jcode) |
| **MCP server** | `tools/ponytail/ponytail-mcp/` — review dan audit tools (kode ada, tapi TIDAK terdaftar di MCP config Hermes) |
| **MCP ecosystem lain** | **UACC** — 68 MCP tools desktop control (screen, mouse, keyboard, window, browser CDP, OCR, workflow) — **sudah terintegrasi** via `services/uacc/` |
| **Auto-load?** | **YA** — "ACTIVE EVERY RESPONSE" via DOX system prompt |
| **Cara auto-load** | Karena root AGENTS.md terbaca sebagai konteks saat kerja di `~/Desktop/Niumination/` |
| **Trigger keyword** | "ponytail", "be lazy", "lazy mode", "yagni", "do less", "minimal solution" |
| **Level** | `lite` / `full` (default) / `ultra` — via `/ponytail lite` |
| **Nonaktif** | "stop ponytail" atau "normal mode" |
| **Persistence** | **Stay aktif antar respons** sampai dimatikan eksplisit |

#### Decision Ladder (7 Langkah)

Setiap respons menjalankan ladder ini:

```
1. Perlu ada?           → YAGNI, skip
2. Udah ada di repo?    → Reuse
3. Stdlib bisa?         → Pake stdlib
4. Platform native?     → Fitur OS/browser
5. Dependency terinstal?→ Baru pake
6. Bisa satu baris?     → 1 baris
7. Baru: kode minimal   → Solusi paling kecil
```

#### Kenapa Ponytail Auto-load Tapi Skill Lain Tidak?

**Ponytail di Hermes bukan skill Hermes biasa.** Ponytail:

1. **Ditulis langsung di AGENTS.md** — bukan file `~/.hermes/skills/` terpisah
2. **Menggunakan DOX injection** — root AGENTS.md terbaca sebagai konteks kerja
3. **Perintah "ACTIVE EVERY RESPONSE"** — ini instruksi ke AI agent, bukan mekanisme sistem

Jadi sebenarnya **Ponytail bukan contoh mekanisme skill Hermes**. Dia adalah contoh **DOX injection** yang kebetulan isinya mirip skill. Skill Hermes yang proper harus di-load via `skill_view()` meskipun sudah di-catalog di system prompt.

#### Integrasi MCP (Belum Aktif)

Ponytail punya 2 MCP tools di kode (`tools/ponytail/ponytail-mcp/`):
- `mcp_ponytail_review_code_diff()` — review diff dengan lensa minimalis
- `mcp_ponytail_audit_repo()` — audit repo untuk kode berlebih

**TAPI:** Kode sudah ada, MCP server tidak terdaftar di konfigurasi Hermes. Jadi tools ini tidak bisa dipanggil.

---

## 5. Claude Code Native Skills

### Status: **Terinstal di macOS sebagai CLI terpisah** (`claude`)

| Aspek | Detail |
|-------|--------|
| **Skill bawaan** | Ya — Claude Code punya built-in optimization, planning, dll |
| **Katalog resmi** | `anthropics/skills` (official Anthropic catalog) |
| **Katalog komunitas** | **Agentpedia** (`agentpedia.codes`) — **2000+** Agent Skills |
| **Cara instal** | `npx skills add anthropics/skills --skill <nama>` |
| **Auto-load?** | **TIDAK** — manual via slash command |
| **Trigger** | `/optimization`, `/frontend-design`, dll |
| **Format** | Slash command — `/nama_skill` |
| **Kompatibilitas** | Format SKILL.md cross-platform (Claude, Cursor, Antigravity, Windsurf) |

### Cara Kerja di Ekosistem

Claude Code dijalankan sebagai **CLI independen** melalui:
- `claude -p "prompt"` — langsung di terminal
- `claude-repl.sh` — REPL mode via herdr agent send (lihat Herdr section)
- Orca hook — event telemetry (lihat Orca section)

### Agentpedia

**Agentpedia** adalah marketplace komunitas (bukan resmi Anthropic) dengan **2000+ Agent Skills** untuk Claude Code, Cursor, Antigravity, Windsurf. Juga punya **1500+ MCP servers**, **500+ AI Rules**, dan **workflows**.

**Perbedaan Agentpedia dengan Hermes Hub:**
| Aspek | Agentpedia | Hermes Hub |
|-------|-----------|------------|
| **Platform target** | Antigravity, Claude Code, Cursor, Windsurf | Hermes Agent |
| **Jumlah** | 2000+ skills | Ribuan (via GitHub) |
| **Model bisnis** | Marketplace independen | Open registry |
| **Format** | SKILL.md (cross-platform) | SKILL.md (Hermes-specific) |

Contoh 5 skill yang relevan:

| Skill | Agentpedia | GitHub | Domain |
|-------|-----------|--------|--------|
| `/ultrathink` | ✅ Ada | HaydenLundin | Craftsmanship |
| `/tripwire` | Mungkin | sisi-tarak | Risk detection |
| `/premortem` | Mungkin | procoders | Strategic failure |
| `/redteam` | ✅ Ada | danielmiessler | Security pentest |
| `/ghost` | ✅ Ada | sisi-tarak | AI text humanizer |

### Kesimpulan untuk Claude Code
- Sistem skill paling matang (katalog official + komunitas besar)
- Hanya aktif untuk sesi Claude Code, tidak untuk Jcode/Hermes
- Butuh porting manual jika mau dipakai di Jcode
- Format SKILL.md kompatibel dengan Jcode (path yang sama)
- **2000+ skills via Agentpedia** — potensi terbesar untuk diadopsi

---

## 6. OpenCode Skills (146 skills)

### Status: **Terinstal sebagai CLI** — 146 skills (data dari DOX, belum diverifikasi langsung)

| Aspek | Detail |
|-------|--------|
| **Jumlah** | 146 skills (klaim DOX — belum diverifikasi) |
| **Akses** | `opencode run skill <nama>` |
| **Integrasi** | via `opencode_bridge.py` di Orchestrator |
| **Auto-load?** | **TIDAK** — harus dipanggil eksplisit |
| **Bridge** | `agents/orchestrator/utils/opencode_bridge.py` |

### Cara Integrasi dengan Orkestrator

```python
bridge = OpenCodeBridge()
bridge.call_skill("ponytail")  # → opencode run skill ponytail
bridge.call_prompt("Buat API route untuk user")
```

Ini berarti OpenCode bisa dipanggil dari Python orchestrator, tapi **tidak auto-load** ke sesi manapun.

**Catatan:** Angka 146 perlu diverifikasi dengan `opencode run skill list | wc -l` langsung.

### Kesimpulan untuk OpenCode
- Skills terbanyak (146 claimed) tapi harus dipanggil manual
- Terintegrasi via orchestrator (Python bridge)
- Tidak aktif di Jcode/Hermes/Claude — hanya di OpenCode CLI sendiri

---

## 7. Orca Hooks — Pipeline Telemetry (BUKAN Skill)

### Status: **12 hook scripts** di `scripts/hooks/`

**Ini BUKAN skill.** Orca hooks adalah **pipeline telemetry** yang mengirim data saat AI agent mulai/selesai bekerja.

### Cara Kerja

```
Terminal event (session start/stop)
        │
        ▼
Hook script terpicu (otomatis via shell hook)
        │
        ▼
Mengirim HTTP POST ke localhost:${ORCA_AGENT_HOOK_PORT}
        │
        ▼
Orca receiver (server) mencatat event
        │
        ▼
Data tersedia untuk analytics/monitoring
```

### 12 Hook Scripts

| File | Untuk Agent | Fungsi |
|------|------------|--------|
| `claude-hook.sh` | Claude Desktop | Kirim session event |
| `codex-hook.sh` | Codex CLI | Kirim session event |
| `command-code-hook.sh` | Command Code | Kirim session event |
| `copilot-hook.sh` | GitHub Copilot | Kirim session event |
| `cursor-hook.sh` | Cursor | Kirim session event |
| `antigravity-hook.sh` | Antigravity | Kirim session event |
| `devin-hook.sh` | Devin | Kirim session event |
| `droid-hook.sh` | Droid | Kirim session event |
| `gemini-hook.sh` | Gemini | Kirim session event |
| `grok-hook.sh` | Grok | Kirim session event |
| `kimi-hook.sh` | Kimi | Kirim session event |
| `openclaude-hook.sh` | OpenClaude | Kirim session event |

### Kesimpulan untuk Orca Hooks
- **Bukan skill** — tidak mengubah perilaku AI agent
- **Otomatis** — terpicu oleh shell events (session start/stop)
- **Read-only** — hanya mengirim data, tidak menerima instruksi
- **Infrastruktur** — untuk monitoring, logging, analytics

---

## 8. Herdr Characters — Persona Agent

### Status: **4 karakter** di `agents/characters/`

Ini adalah **persona/presets** untuk AI agent, bukan skill teknis.

| Karakter | Peran | Trigger |
|----------|-------|---------|
| 🏛️ **Arsitek** | Visioner, struktural, big picture | `herdr agent send arsitek "..."` |
| 🔧 **Pembangun** | Cepat, praktis, deliver-oriented | `herdr agent send pembangun "..."` |
| 👁️ **Pengawas** | Reviewer, kritikal, perfeksionis | `herdr agent send pengawas "..."` |
| 🛡️ **Penjaga** | Sistematis, cron, auto-pilot | `herdr agent send penjaga "..."` |

### Cara Kerja

```
herdr agent send arsitek "Desain database schema untuk user management"
        │
        ▼
Membaca AGENTS.md arsitek (personality + rules)
        │
        ▼
Meneruskan prompt ke AI agent backend
        │
        ▼
Kembalikan respons dengan gaya arsitek (diagram ASCII, ADR)
```

Setiap karakter punya file `AGENTS.md` sendiri yang mendefinisikan:
- Personality statement
- Motto
- Aturan kerja
- Gaya komunikasi (format respons)

### Hubungan dengan REPL

Ada 2 REPL script untuk interaksi dengan karakter:
- `agy-repl.sh` — menggunakan Antigravity CLI
- `claude-repl.sh` — menggunakan Claude Code CLI

Keduanya bekerja dengan pola: kirim prompt → akhiri dengan `---PROCESS---` → dapatkan respons.

### Kesimpulan untuk Herdr Characters
- **Persona, bukan skill** — mengubah gaya komunikasi, bukan logika teknis
- **Manual** — harus dipanggil eksplisit via `herdr agent send`
- **Orkestrasi** — bisa dipanggil dari orchestrator untuk workflow multi-agent
- **Independent** — tidak terkait dengan skill system Jcode/Hermes/Claude

---

## 9. macOS System AI — DuetExpertCenter

### Status: **235 MB — proses sistem macOS**

| Aspek | Detail |
|-------|--------|
| **Apa itu** | AI on-device Apple untuk macOS |
| **Lokasi** | System process (bukan bagian dari ekosistem dev) |
| **Fungsi** | Apple Intelligence, Siri, on-device ML |
| **Relasi ke skill** | **TIDAK ADA** — tidak bisa di-load skill |
| **Integrasi** | Bisa via macOS shortcuts/AppleScript (terbatas) |

### Kesimpulan untuk macOS System AI
- **Tidak relevan** dengan sistem skill development
- Berjalan independen sebagai proses sistem
- Tidak bisa dikonfigurasi atau di-load skill dari ekosistem Niumination

---

## 10. Ringkasan — Auto vs Manual

### Tabel Perbandingan

| Agent/Sistem | Auto-load? | Cara Aktivasi | Jumlah Skill | Persistence |
|-------------|-----------|---------------|-------------|-------------|
| **Jcode** | ❌ Tidak | `skill_manage load` atau `/nama` | 0 loaded, 3+ tersedia | Per sesi — hilang saat sesi berakhir |
| **Hermes** | ✅ **Catalog di system prompt** | Agent detect sendiri + `skill_view(name)` | Tergantung install | Stay aktif untuk sesi itu |
| **Hermes (Ponytail via DOX)** | ✅ **YA — DOX injection** | Terbaca dari AGENTS.md | 1 | Stay sampai dimatikan |
| **Claude Code** | ❌ Tidak | `/nama_skill` | ~2000+ (via Agentpedia) | Per sesi |
| **OpenCode** | ❌ Tidak | `opencode run skill` | 146 (claim) | Per command |
| **Orca Hooks** | ✅ **YA** | Shell event trigger | 12 hook scripts (bukan skill) | Otomatis |
| **Herdr Characters** | ❌ Tidak | `herdr agent send` | 4 persona | Per command |
| **macOS System AI** | ✅ **YA** | Sistem level | N/A | Selalu jalan |

### Yang PENTING dipahami:

**Skill dan Persona adalah 2 hal berbeda:**
- **Skill** → mengubah BAGAIMANA AI menulis kode (Ponytail: minimal solution, Ultrathink: craftsmanship)
- **Persona** → mengubah SIAPA AI tersebut (Arsitek: visioner, Pembangun: praktis)

**Auto-load hanya terjadi di 3 tempat:**
1. **Hermes catalog** — daftar skill di-inject ke system prompt tiap sesi (tapi isi skill tetap harus di-load manual via `skill_view()`)
2. **Ponytail via DOX** — karena di-inject ke system prompt Hermes via AGENTS.md
3. **Orca Hooks** — karena terpicu oleh shell events (bukan skill, tapi pipeline)

**Skill TIDAK auto-load ke konteks** — hanya katalog (nama + deskripsi) yang masuk system prompt.

---

## 11. Matriks Trigger Detection

Apakah skill bisa otomatis terdeteksi berdasarkan task?

| Skill | Auto-detect? | Trigger |
|-------|:-----------:|---------|
| Hermes skills (via catalog) | ✅ **Catalog (nama+deskripsi) di system prompt** | Agent detect relevance, lalu `skill_view(name)` untuk load isi |
| Ponytail (Hermes DOX) | ✅ Parsial | Keyword: "lazy", "yagni", "minimal", keluhan over-engineering |
| Ponytail (via Hermes skill) | ✅ Catalog + agent decision | Agent lihat relevan dari konteks |
| Ponytail (Jcode) | ❌ | Harus di-load manual |
| Jcode skills (general) | ❌ | Harus `skill_manage load` atau `/nama` |
| Ultrathink | ❌ | Harus di-load atau `/ultrathink` |
| Tripwire | ❌ | Harus dipanggil eksplisit |
| Premortem | ❌ | Harus dipanggil eksplisit |
| Redteam | ❌ | Harus dipanggil eksplisit |
| Ghost | ❌ | Harus dipanggil eksplisit |
| Orca Hooks | ✅ Selalu | Event-driven (bukan skill) |
| Herdr Characters | ❌ | Harus `herdr agent send` |

**Hermes adalah satu-satunya sistem yang punya auto-detection** — karena daftar skill (nama + deskripsi) selalu ada di system prompt. Agent bisa memutuskan skill mana yang relevan tanpa perlu diberi tahu.

**Tapi ingat:** Auto-detection hanya untuk katalog. Isi skill tetap harus di-load manual via `skill_view(name)`.

---

## 12. Rekomendasi Praktis

### Untuk Daily Workflow

```
┌─────────────────────────────────────────────────────────┐
│                     DAILY DEFAULT                        │
│                                                         │
│  Hermes: catalog otomatis di system prompt               │
│          agent auto-load skill jika relevan              │
│          Ponytail aktif via DOX                         │
│  Orca Hooks (auto) — telemetry ke receiver              │
│  Jcode: 0 skills loaded — clean state                   │
│                                                         │
│  → Ideal untuk hotfix, bug, surgical patch              │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                TASK ARSITEKTUR BERAT                     │
│                                                         │
│  Hermes: catalog → agent load ultrathink + tripwire      │
│          (auto-detect dari task description)             │
│  Jcode:  skill_manage load ultrathink                    │
│          + tripwire untuk identifikasi risiko            │
│  Herdr:   herdr agent send arsitek "desain..."           │
│                                                         │
│  → Ideal untuk cc-acehtengah, niu-mission-control       │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                 SECURITY / AUDIT                         │
│                                                         │
│  Claude Code: /redteam — 32 agen adversarial             │
│  Hermes:      catalog → agent load redteam jika terinstal│
│  Jcode:       skill_manage load premortem                │
│                                                         │
│  → Ideal untuk audit Pemdi, SIBER, SPBE                 │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                DOKUMENTASI / KONTEN                      │
│                                                         │
│  Hermes: catalog → agent load ghost secara otomatis      │
│  Jcode:  skill_manage load ghost                         │
│                                                         │
│  → Ideal untuk laporan pemda, artikel, publikasi         │
└─────────────────────────────────────────────────────────┘
```

### Checklist Instalasi Skill Baru

```
□ 1. Untuk sistem mana? (Jcode / Hermes / Claude Code)
□ 2. Format frontmatter sesuai?
□ 3. Path benar? (~/.jcode/skills/ vs ~/.hermes/skills/ vs tools/)
□ 4. Bentrok dengan Ponytail? (cek domain)
□ 5. Perlu auto-load atau on-demand?
```

### Pertanyaan untuk Diri Sendiri

| Pertanyaan | Jawaban |
|-----------|---------|
| "Apakah saya perlu skill yang dipilih otomatis?" | Hermes — catalog di system prompt + agent auto-detect |
| "Apakah saya perlu skill manual?" | Jcode — `skill_manage load` / `/nama` |
| "Apakah saya perlu workflow multi-agent?" | Herdr characters + orchestrator |
| "Apakah saya perlu monitoring?" | Orca hooks handle ini otomatis |
| "Skill ini untuk Jcode atau Hermes?" | Cek format — kompatibel jika YAML frontmatter |

---

## 13. Kesimpulan — Jcode vs Hermes

### Perbandingan Langsung

| Aspek | Jcode | Hermes Agent |
|-------|-------|-------------|
| **Model** | Beda provider — punya sendiri | ✅ Sama — `big-pickle` via OpenCode Zen, beda API key & akun |
| **Skill di system prompt?** | ❌ Tidak ada | ✅ **Ada — daftar skill di-inject tiap sesi** |
| **Agent bisa load sendiri?** | ❌ Tidak — harus manual | ✅ **Ya — agent detect relevance** |
| **Curator management?** | ❌ Tidak | ✅ Background auto-cleanup |
| **Skill conflict handling?** | ❌ Tidak | ✅ Last-loaded wins |
| **Pinned skills?** | ❌ Tidak | ✅ Bisa pin biar gak ke-delete |
| **Cron integration?** | ❌ Tidak | ✅ `cronjob create --skills` |
| **CLI user management?** | ❌ Terbatas (`skill_manage list`) | ✅ `hermes skills install/search/browse/update` |
| **Hub/Registry publik?** | ❌ Tidak | ✅ Ya — GitHub registry |
| **Backup otomatis?** | ❌ Tidak | ✅ Curator backup sebelum pruning |
| **Portable?** | ❌ Tidak | ✅ USB Hermes Agent |

### Insight Utama

**1. Hermes punya "Skill Awareness" — Jcode tidak**

Perbedaan paling fundamental: Hermes menyisipkan **daftar skill (nama + deskripsi)** ke system prompt setiap sesi. Agent sadar bahwa skill X, Y, Z ada dan tahu kegunaannya. Agent bisa memutuskan untuk load atau tidak.

Jcode tidak melakukan ini. Agent buta terhadap skill apa yang tersedia. Satu-satunya cara tahu adalah `skill_manage list` — yang harus dipanggil manual.

**2. Ponytail adalah outlier — bukan representasi mekanisme Hermes**

Ponytail auto-load karena di-inject via DOX `AGENTS.md`, bukan karena mekanisme skill Hermes. Cara kerja Ponytail adalah **DOX injection**, bukan **skill system**.

Skill Hermes yang proper: catalog di system prompt → agent decide → `skill_view(name)` → full load ke konteks.

**3. Ekosistem Niumination saat ini fragmented**

| Komponen | Status |
|----------|--------|
| Hermes skill system | Siap pakai — tinggal install skill via `hermes skills install` |
| Jcode skill system | 0 terpakai — folder `~/.jcode/skills/` kosong |
| Ponytail SKILL.md | Path salah — di `tools/` bukan `~/.jcode/skills/` |
| Ponytail MCP server | Kode ada — tidak terdaftar di MCP config |
| Orca hooks | Berfungsi — 12 scripts aktif |
| Claude Code / OpenCode | Independent — tidak terintegrasi dengan Jcode/Hermes |

**4. Tujuan Akhir — Satu Bank Skill Terpusat untuk Semua Agent**

Ekosistem saat ini fragmented. Tujuan akhirnya adalah arsitektur 4 layer:

```
~ /Desktop/Niumination/skills/          ← Layer 1: BANK PUSAT (single source of truth)
  ├── software-development/ponytail/
  ├── software-development/debugging/
  ├── security/redteam/
  ├── creative/ghost/
  └── ... (berkembang seiring waktu)

Sync Script                                 ← Layer 2: AUTO-SYNC ke Jcode + Hermes + Claude Code
DOX Injection Engine                        ← Layer 3: AUTO-TRIGGER dari prompt (replikasi pola Ponytail)
Mission-Control Dashboard                   ← Layer 4: LIVE MONITOR skill usage & stats
```

**5. Rekomendasi Immediate (Foundation)**

1. **Update AGENTS.md root dulu** — sinkronkan DOX v3.0 dengan realita v4.0 (ditemukan audit: banyak path salah, catalog tidak sinkron)
2. **Bangun Layer 1** — buat `~/Desktop/Niumination/skills/` sebagai bank pusat
3. **Sync Ponytail** — copy SKILL.md dari `tools/ponytail/` ke bank pusat
4. **Sync Hermes ~10-15 active skills** — inventory skills yang benar-benar dipakai
5. **Bangun Sync Script (Layer 2)** — auto-copy ke `~/.jcode/skills/` dan `~/.hermes/skills/`

> 🔔 **Urutan dari Hermes:** Jangan bangun Layer 1 sebelum AGENTS.md diperbaiki. Bank skill yang dibangun di atas DOX yang salah akan menghasilkan struktur yang salah.

---

## 14. Roadmap: Menuju Bank Skill Terpusat

### Filosofi

Bank skill ini bukan proyek satu-kali-selesai. Ini adalah **living system** yang akan berkembang seiring waktu — semakin banyak agent bergabung dan semakin banyak skill ditambahkan.

```
Sekarang → 1 bank pusat → auto-sync → auto-trigger → live monitor
  │            │             │            │              │
  v            v             v            v              v
fragmented   Layer 1      Layer 2      Layer 3        Layer 4
```

### Target Agent yang Akan Terintegrasi

| Agent | Saat Ini | Target |
|-------|:--------:|:------:|
| **Hermes** (148 skills) | ✅ Mandiri | ✅ Baca dari bank pusat |
| **Jcode** (0 skills) | ❌ Kosong | ✅ Baca dari bank pusat |
| **Claude Code** | ❌ Terpisah | ✅ Baca dari bank pusat |
| **OpenCode** | ❌ Terpisah | ✅ Baca dari bank pusat |
| **Agent lain (future)** | — | ✅ Baca dari bank pusat |

### Prinsip Desain

1. **Satu source of truth** — `~/Desktop/Niumination/skills/` adalah master. Semua agent baca dari sini.
2. **Non-destructive** — Layer 1 hanya nulis file. Tidak menghapus/mengubah konfigurasi agent yang sudah jalan. Aman dijalankan kapan pun.
3. **Evolusioner, bukan revolusioner** — mulai dari layer 1 dulu, lalu layer 2, 3, 4. Setiap layer stabil sebelum lanjut.
4. **Semua agent setara** — bank ini tidak memihak Hermes atau Jcode. Semua punya akses yang sama.

### Tahapan Implementasi

**Tahap 1: Foundation (Layer 1) — Bank Pusat**
```
~/Desktop/Niumination/skills/
├── software-development/
│   ├── ponytail/        ← copy dari tools/ponytail/skills/ponytail/
│   ├── debugging/       ← dari Hermes 148 skills
│   └── optimization/    ← dari Jcode bundled
├── security/
│   └── redteam/         ← dari Agentpedia (future)
├── creative/
│   └── ghost/           ← dari sisi-tarak (future)
└── INDEX.md             ← katalog semua skill
```

**Tahap 2: Sync (Layer 2) — Auto-copy Script ✅**
```
skills/sync-to-agents.sh          ← ✅ ACTIVE
├── sync ke ~/.jcode/skills/     → ✅ 10 skill ter-copy
├── sync ke ~/.hermes/skills/    → ✅ 10 skill ter-copy
├── sync ke AGENTS.md (DOX)      → ✅ skill registry auto-update
└── cron job (setiap 6 jam)      → 🔜 Manual setup (CRON_SETUP.md)
```

**Tahap 3: Trigger (Layer 3) — DOX Injection Engine ✅**
- Replikasi pola Ponytail untuk 7 skill tambahan ✅
- Format: 3 level (Always Active / On-Demand / Future) di AGENTS.md ✅
- Agent baca → detect relevance → load otomatis ✅
- Integrasi komplementer dengan Hermes catalog ✅

**Tahap 4: Monitor (Layer 4) — Dashboard ✅**
- Integrasi dengan Mission-Control (FastAPI + WebSocket) ✅
- `modules/skill_monitor.py` — SQLite tracker + 5 API endpoints ✅
- Stats: skill yg di-load hari ini, frekuensi, stale detection ✅
- Notifikasi jika ada skill conflict ✅
- Halaman Skill Monitor di Mission Control v2.6 ✅
- WebSocket real-time push skill events ✅
- sync-to-agents.sh → POST ke mission-control saat sync ✅
- **4 layer selesai semua — checklist lengkap** 🎯

### ✅ Jawaban Hermes untuk 6 Pertanyaan

> Berikut jawaban langsung dari Hermes Agent. Diskusi selesai — siap eksekusi.

1. **Format kategorisasi — per domain atau per agent?**
   **Per domain.** Satu skill yang bagus (misal Ponytail) bisa dipakai Hermes AND Jcode. Kategorisasi per agent hanya bikin duplikasi. Domain-based memudahkan cross-agent reuse.

2. **Naming convention — bagaimana bedain ponytail(audit) vs ponytail(review)?**
   `<domain>/<nama>-<variant>/SKILL.md` — contoh: `software-development/ponytail-core/`, `software-development/ponytail-audit/`. **Gunakan suffix, bukan prefix.** Prefix bikin alphabetical sorting kacau.

3. **Versi skill — perlu versioning atau cukup replace?**
   **Cukup replace** untuk tahap awal. Versioning lewat git history: `git log -- skills/<nama>/SKILL.md`. Kalau sudah >20 skill, baru pikirkan version field di frontmatter.

4. **Trigger priority — kalau 2 skill cocok dengan task yang sama?**
   **Last-loaded wins.** Sama seperti Hermes sekarang. Agent baca semua skill yang relevan, lalu pilih yang paling sesuai. Kalau konflik, yang di-load paling akhir efektif override sebelumnya. Tidak perlu sistem prioritas eksplisit — terlalu kompleks untuk benefit yang kecil.

5. **Backup strategy — bank pusat di-backup ke Hermes USB?**
   **Iya.** Hermes USB (`/Volumes/HermesAgent/`) adalah backup fisik yang tepat. Tapi untuk Layer 1, **cukup git repo** dulu. `~/Desktop/Niumination/skills/` bisa di-commit ke `ecosystem-config` atau repo terpisah. USB untuk cold backup.

6. **Agentpedia sync — pull otomatis atau manual?**
   **Manual dulu.** Agentpedia punya 2000+ skill — otomatis akan flooding. Pilih manual 2-3 skill yang paling relevan (ghost, tripwire, ultrathink), porting ke format bank pusat, evaluasi, baru scale.

### 📋 Rekomendasi Tambahan dari Hermes

**Sebelum bangun Layer 1, update AGENTS.md root dulu.** ✅ Selesai oleh Hermes.

**Layer 2 sync script** ✅ Selesai oleh Jcode — `skills/sync-to-agents.sh` aktif.

**Urutan yang benar (sudah selesai):**

1. Update AGENTS.md → sinkronkan dengan realita v4.0
2. Baru bangun Layer 1 (bank pusat)
3. Layer 2 (sync)
4. Layer 3 (DOX injection)
5. Layer 4 (monitor)

**Satu lagi: `skills/` perlu `.gitignore` yang ketat**

Bank pusat akan berisi file dari berbagai sumber — Hermes, Jcode, Agentpedia. Beberapa mungkin punya struktur `references/` dengan `scripts/` yang punya dependencies:
- `node_modules/` di-ignore
- `.venv/` di-ignore
- File binary (gambar, PDF) di-ignore
- Hanya SKILL.md + markdown references yang di-track

### 🎯 Kesimpulan Hermes + Status Terkini

> "Guide v2 sudah jauh lebih akurat dibanding v1. Jcode melakukan audit yang solid. 4 layer roadmap-nya realistis. Tinggal jawab 6 pertanyaan (sudah saya jawab) dan eksekusi bertahap. Siap mulai?"
> — Hermes Agent

**Update 29 Jul 2026:** Layer 1 scaffold selesai — 8 skill terisi Hermes. Layer 2 sync script (`skills/sync-to-agents.sh`) aktif: sync bank pusat → Jcode + Hermes + AGENTS.md. Cron every 6h via `CRON_SETUP.md`.

---

## Referensi

| Sumber | Path/Link |
|--------|-----------|
| DOX root | `~/Desktop/Niumination/AGENTS.md` |
| Ponytail SKILL.md | `~/Desktop/Niumination/tools/ponytail/skills/ponytail/SKILL.md` |
| Ponytail MCP | `~/Desktop/Niumination/tools/ponytail/ponytail-mcp/` |
| Orca Hooks | `~/Desktop/Niumination/scripts/hooks/` |
| Herdr Characters | `~/Desktop/Niumination/agents/characters/*/AGENTS.md` |
| Orchestrator Bridge | `~/Desktop/Niumination/agents/orchestrator/utils/opencode_bridge.py` |
| Agentpedia | `https://agentpedia.codes` |
| Jcode Skills (global) | `~/.jcode/skills/` |
| Jcode Skills (local) | `./.jcode/skills/` |
| Hermes Skills | `~/.hermes/skills/` |
| Hermes USB Skills | `/Volumes/HermesAgent/HermesAgentUSB/data/skills/` |
||| **Bank Skill Pusat** | `~/Desktop/Niumination/skills/` | 🧠 **ACTIVE** — Layer 1-4 ✅ |
||| **Sync Script (Layer 2)** | `~/Desktop/Niumination/skills/sync-to-agents.sh` | ✅ Auto-sync bank → Jcode + Hermes + AGENTS.md, cron every 6h |
||| **DOX Injection (Layer 3)** | `AGENTS.md` — Auto-loaded Skills section | ✅ 3 level: Always Active (Ponytail), On-Demand (7 skill), Future (2) |
||| **Mission-Control (Layer 4)** | `services/niu-mission-control/` | ✅ Skill Monitor v2.6 — WebSocket, stats, stale, conflicts |
|| AI-Memory-Collection | `~/Desktop/AI-Memory-Collection/` (1.73 GB) | ⚪ **BELUM DIVERIFIKASI** — Hermes tidak kenal folder ini. Butuh verifikasi langsung. |
| Hermes Hub Registry | GitHub — `hermes skills install <nama>` |

---

> **Dibuat:** 29 Juli 2026
> **Diperbarui:** 29 Juli 2026 v7 — +Layer 4 Skill Mission-Control Dashboard ✅ oleh Jcode. Semua 4 layer selesai 🎯.
> **Oleh:** Jcode + Hermes Agent — Niumination Ecosystem
> **Tujuan:** Dokumentasi referensi — bisa di-copy ke NotebookLM untuk query lebih lanjut
