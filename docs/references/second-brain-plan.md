# 🧠 Second Brain — Implementation Plan v2
**Berdasarkan kondisi terkini setelah restrukturasi (9 Juni 2026)**

---

## Arsitektur 3 Lapis (Final)

```
┌─────────────────────────────────────────────────────┐
│                   DAILY CAPTURE                      │
│  Telegram ←→ Hermes Agent (cron + auto-respond)     │
│  Web Clipper → Obsidian (net-clip plugin)           │
└──────────────────────┬──────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────┐
│                  KNOWLEDGE BASE                       │
│  Obsidian Vault @ Desktop/Niumination/vault/          │
│  ├── 📥 Inbox/        (daily capture masuk sini)     │
│  ├── 📁 Projects/     (catatan per project)           │
│  ├── 📚 Resources/    (referensi, tutorial)           │
│  ├── 🗄️ Archive/      (notes lama, sudah diproses)    │
│  └── 🔐 PI/           (symlink ke ../PI/ — API keys) │
└──────────────────────┬──────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────┐
│                COMMAND CENTER                         │
│  NIU-DASH @ projects/niu-dash/                        │
│  ├── 📊 Project tracker (105+ project)                │
│  ├── 🚀 Released Projects (production/completed)      │
│  └── 🔗 Link ke Obsidian vault notes                  │
└─────────────────────────────────────────────────────┘
```

---

## Fase 1 — Setup Obsidian Vault

### 1.1 Pilih Lokasi Vault
**Rekomendasi:** `~/Desktop/Niumination/vault/`
- ✅ Satu struktur dengan project lain
- ✅ Gampang diakses dari mana aja
- ✅ Bisa di-sync/integrasi sama NIU-DASH

### 1.2 Pindah `.obsidian/` Config
**Dari:** `~/Documents/ZMP/.obsidian/` (12 MB, 9 plugins, 5 themes)
**Ke:** `~/Desktop/Niumination/vault/.obsidian/`

**Yang dipertahankan:**
- Semua plugin (surfing, terminal, net-clip, read-it-later, opencode, dll)
- Semua themes (AnuPpuccin, LYT Mode, Minimal, Primary, Wasp)
- Workspace layout, hotkeys, core plugins
- Community plugins config

### 1.3 Restore Archived Notes
**Dari `archive/` yang relevan → masuk ke vault:**

| File | Tujuan di Vault | Notes |
|------|-----------------|-------|
| `archive/01-updates/Harini.md` | `📥 Inbox/Harini.md` | Daily news capture |
| `archive/01-updates/Vault Health Report 21-22.md` | `🗄️ Archive/` | Vault health (referensi) |
| `archive/SHORTCUTS.md` | `📚 Resources/Neovim-Shortcuts.md` | Shortcut reference (path udah diupdate) |
| `archive/VAULT-SETUP.md` | Root `_VAULT-SETUP.md` | Dokumentasi setup vault |
| `archive/Untitled 1.md` | `📥 Inbox/Ultra-Automation.md` | Catatan Ultra Automation |
| `archive/obsidian-files/Welcome.md` | Boleh dihapus | Template default |

### 1.4 Struktur Folder di Vault
```
vault/
├── .obsidian/                   ← Config (pindah dari ZMP)
├── _VAULT-SETUP.md              ← Dokumen setup
├── 📥 Inbox/                    ← Daily capture masuk sini
│   ├── Harini.md
│   └── Ultra-Automation.md
├── 📁 Projects/                 ← Catatan per project
│   └── (kosong — isi manual)
├── 📚 Resources/                ← Referensi
│   └── Neovim-Shortcuts.md
├── 🗄️ Archive/                  ← Notes lama
│   └── Vault-Health-Report.md
└── 🔐 PI/ → ../PI/             ← Symlink ke API keys
```

---

## Fase 2 — Daily Capture Pipeline

### 2.1 Telegram → Obsidian Auto-Capture
**Cara:** Hermes cron job tiap malam (21:00 WIB)

```
Setiap jam 21:00:
  1. Hermes scan chat hari ini
  2. Extract: ide, link, task, catatan penting
  3. Format markdown
  4. Tulis ke vault/📥 Inbox/{YYYY-MM-DD}-daily.md
```

**Cron script:** `data/scripts/second-brain-capture.py`
- Baca Telegram history hari ini
- Filter pesan relevant (save, penting, link)
- Tulis ke `vault/📥 Inbox/`

### 2.2 Web Clipper (NetClip)
Plugin net-clip sudah terinstall di Obsidian — bisa langsung dipake:
- **Shortcut:** `Cmd+Shift+V` untuk save halaman web
- **Auto-save** ke `📥 Inbox/` atau `📚 Resources/`

### 2.3 Manual Quick Capture
Via Hermes (Telegram):
- Ketik `save <catatan>` atau `simpan <catatan>`
- Hermes auto-save ke vault inbox
- Atau Hermes yang langsung catat ke file `.md`

---

## Fase 3 — Integrasi dengan NIU-DASH

### 3.1 Link Vault ke Dashboard
- Tambah entry di PROJECTS → kategori `config`:
  ```
  { icon:'🧠', name:'Second Brain Vault', path:'/Users/zaryu/Desktop/Niumination/vault/', desc:'Knowledge base Obsidian — daily capture, project notes, resources.', tags:['Obsidian','Vault','Knowledge','SecondBrain'], date:'Jun 2026' }
  ```

### 3.2 Daily Summary di Dashboard
- NIU-DASH baca file dari `vault/📥 Inbox/` yang terbaru
- Tampilkan sebagai card di sidebar / feed

### 3.3 Project Notes Link
- Setiap project di PROJECTS array bisa punya field `vaultNote`
- Klik "Vault" → buka note Obsidian terkait

---

## Risiko & Mitigasi

| Risiko | Mitigasi |
|--------|----------|
| Obsidian plugin usang (last config May 2026) | Test dulu sebelum full migrate |
| Vault content terpisah dari config | Pindah SEMUA sekaligus, jangan bertahap |
| Cron job nulis ke vault tapi vault gak kebuka | Cron simpan dulu, Obsidian baca dari file statis |
| Netclip plugin perlu API key / setup | Cek dokumentasi plugin |

---

## Ukuran & Dampak

| Item | Size | Impact |
|------|------|--------|
| `.obsidian/` config | 12 MB | ✅ Kecil, pindah instan |
| Archived notes | 40 KB | ✅ Kecil, restore instan |
| Vault total estimasi | ~12.1 MB | ✅ Ringan banget |
| Hermes cron script | < 10 KB | ✅ Satu file Python |

---

## Prioritas Eksekusi

```
🟢 Fase 1: Setup Vault        → Pindah .obsidian + restore notes
🟡 Fase 2: Daily Capture      → Setup cron + script capture
🔵 Fase 3: NIU-DASH Integrasi → Link vault + daily summary di dashboard
```

**Total estimasi:** ~1 jam untuk setup, ~2 jam untuk full integrasi.
