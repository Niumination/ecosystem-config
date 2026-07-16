# 🧠 Second Brain — Implementation Plan v2.1 (Revised)
**Kondisi terkini: 9 Juni 2026 — SETELAH restrukturasi**
**Disimpan: lanjut besok**

---

## 🏗️ Arsitektur 3 Lapis

```
TELEGRAM/HERMES     →   OBSIDIAN VAULT    →   NIU-DASH
(DAILY CAPTURE)         (KNOWLEDGE BASE)       (COMMAND CENTER)
                         
#save <note>  ─────┐
net-clip  ─────────┤
manual  ───────────┼──→  brain/inbox/  ──→  Dashboard link
                   │                     
Hermes malam ──────┘   brain/projects/   →  Project tracker
                        brain/resources/  →  Reference hub
```

---

## 🟢 FASE 1 — Setup Obsidian Vault

### 1.1 Lokasi Vault
**→ `~/Desktop/Niumination/brain/`** (diubah dari `vault/` — lebih pendek, tematik)

### 1.2 Pindah `.obsidian/` Config
- **Dari:** `~/Documents/ZMP/.obsidian/` (12 MB)
- **Ke:** `~/Desktop/Niumination/brain/.obsidian/`
- **Status:** 9 plugins siap (surfing, terminal, net-clip, read-it-later, opencode, app-launcher, media-extended, workspaces-plus, style-settings) + 5 themes

### 1.3 Struktur Folder (Tanpa Emoji — Revisi Penting!)
```
brain/                          ← ROOT VAULT
├── .obsidian/                  ← Config (plugins + themes)
├── _index.md                   ← Landing page + navigation
├── inbox/                      ← Daily capture & quick notes
│   └── {YYYY-MM-DD}-daily.md  ← Hermes auto-generated
├── projects/                   ← Catatan per project
│   └── flame-ade.md           ← Manual entry
├── resources/                  ← Referensi & learning
│   ├── neovim-shortcuts.md    ← SHORTCUTS.md restored
│   └── vault-setup.md         ← VAULT-SETUP.md restored
└── archive/                    ← Notes lama (diproses)
    ├── health-report.md
    └── ultra-automation.md    ← Untitled 1.md restored
```
**⚠️ Emoji di nama folder dihapus** — biar aman di CLI/scripts/Obsidian plugins.

### 1.4 Restore Archived Notes
| Archive File | → brain/ | Catatan |
|-------------|----------|---------|
| `archive/01-updates/Harini.md` | `inbox/Harini.md` | Daily news capture |
| `archive/01-updates/Vault Health Report 21-22.md` | `archive/health-report.md` | Referensi |
| `archive/SHORTCUTS.md` | `resources/neovim-shortcuts.md` | Path updated ✅ |
| `archive/VAULT-SETUP.md` | `resources/vault-setup.md` | Setup docs |
| `archive/Untitled 1.md` | `archive/ultra-automation.md` | Catatan UAS |
| `archive/obsidian-files/Welcome.md` | ❌ Skip | Template default |

### 1.5 PI (API Keys) — REVISI: Jangan di Symlink!
**❌ Tidak dimasukkan ke vault** — risiko bocor kalo vault di-sync ke cloud/GitHub.
Cukup catat path di `_index.md`:
```md
🔐 API Keys: `../../PI/api-key.md` (jangan di-sync!)
```

### 1.6 Buka Vault di Obsidian
Setelah semua siap, buka **Obsidian.app** → "Open folder as vault" → pilih `~/Desktop/Niumination/brain/`

---

## 🟡 FASE 2 — Daily Capture Pipeline (Revisi)

### 2.1 Telegram → Obsidian — REVISI Strategi

❌ **Cron scan Telegram history** — Hermes tidak punya tool untuk baca history.
✅ **Ganti jadi passive capture:**

| Metode | Cara | Status |
|--------|------|--------|
| **Telegram #brain** | User kirim `#brain <catatan>` → Hermes save ke `inbox/{date}.md` | ✅ Via Hermes cron |
| **Telegram #save** | User kirim `#save <link/ide>` → Hermes format markdown | ✅ Via Hermes cron |
| **Hermes daily prompt** | Cron 21:00 tanya "Apa yang kamu catat hari ini?" → user reply → simpan | ⏳ Setup cron |
| **net-clip plugin** | `Cmd+Shift+V` di Obsidian → save halaman web langsung ke vault | ✅ Udah terinstall |
| **Manual markdown** | Buka `brain/inbox/` → tulis langsung | ✅ Paling sederhana |

### 2.2 Hermes Cron Setup
**Script:** `data/scripts/brain-capture.sh`
```
Setiap 21:00:
  1. Tanya user: "📝 Catatan hari ini? (balas #brain <isi>)"
  2. User reply → Hermes tulis ke brain/inbox/{date}-daily.md
```

---

## 🔵 FASE 3 — Integrasi NIU-DASH

### 3.1 Link Vault di Dashboard
Tambah entry di PROJECTS → kategori `config`:
```js
{ icon:'🧠', name:'Second Brain', path:'/Users/zaryu/Desktop/Niumination/brain/_index.md', desc:'Knowledge base Obsidian — daily capture, project notes, resources.', tags:['Obsidian','Vault','Knowledge','SecondBrain'], date:'Jun 2026' }
```

### 3.2 Daily Summary — REVISI
**Masalah:** NIU-DASH di GitHub Pages gak bisa baca file lokal.
**Solusi:**
- **Local mode** (file://) — JS bisa baca `brain/inbox/` → tampilkan summary card
- **Published mode** (GitHub Pages) — skip, atau inject lewat `data/daily-summary.json`

Prioritas rendah — bisa ditunda.

---

## 📊 Ringkasan

| Fase | Item | Status | Waktu |
|------|------|--------|-------|
| 🟢 1.1 | Buat folder `brain/` | ⏳ | 1 menit |
| 🟢 1.2 | Pindah `.obsidian/` | ⏳ | 5 menit |
| 🟢 1.3 | Restore archived notes | ⏳ | 3 menit |
| 🟢 1.4 | Buka vault di Obsidian | ⏳ | 1 menit |
| 🟡 2.1 | Setup passive capture (#brain) | ⏳ | 15 menit |
| 🟡 2.2 | Setup cron daily prompt | ⏳ | 10 menit |
| 🔵 3.1 | Link vault di NIU-DASH | ⏳ | 5 menit |
| 🔵 3.2 | Daily summary (local) | ⏳ | Tunda |

**Estimasi:** ~40 menit untuk Fase 1 + setup dasar Fase 2.

---

## ⚠️ Risiko Final

| Risiko | Mitigasi |
|--------|----------|
| Obsidian plugins usang (last update May) | Update di Obsidian → Community plugins |
| net-clip perlu konfigurasi | Cek settings plugin |
| Vault gak muncul di Obsidian | Open folder as vault manual |
| Pipiline Hermes error | Test manual dulu → baru cron |
