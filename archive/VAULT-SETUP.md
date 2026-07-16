# Vault Setup Documentation

> File ini mendokumentasikan seluruh proses setup dan konfigurasi Obsidian sebagai Central Workspace System.

## Status Setup

| Komponen | Status | Tanggal | Catatan |
|----------|--------|---------|---------|
| Surfing Plugin | ✅ Selesai | 2026-05-21 | Browser dalam Obsidian |
| NetClip Plugin | ✅ Selesai | 2026-05-21 | Web clipping & organize |
| ReadItLater Plugin | ✅ Selesai | 2026-05-21 | Simpan artikel untuk dibaca nanti |
| App Launcher | ✅ Selesai | 2026-05-21 | Launch GitHub Desktop dari ribbon |
| Struktur Vault | ✅ Sebagian | 2026-05-21 | Clips, ReadItLater folders created |
| Link Iframe | ⏳ Pending | - | Embed media (alternatif: Local HTML Embed) |
| Dataview | ⏳ Pending | - | Query & dashboard |
| Templater | ⏳ Pending | - | Template system |
| Tasks | ⏳ Pending | - | Task management |
| Calendar | ⏳ Pending | - | Navigasi waktu |
| Style Settings | ✅ Terinstall | 2026-05-21 | Kustomisasi UI |

---

## 1. Surfing Plugin - Browser dalam Obsidian

### Status: ✅ Selesai

**Deskripsi**: Plugin yang memungkinkan browsing web langsung di dalam Obsidian dengan tabbed interface.

**Fitur yang dikonfigurasi**:
- [x] Hijack link http/https → buka di Obsidian
- [x] Tabbed browsing interface
- [x] Web search dari editor
- [x] Browsing history (back/forward)
- [x] Dark mode support

**Cara Penggunaan**:
1. Klik link http/https di catatan → otomatis terbuka di tab Surfing
2. Command palette → `Surfing: Open URL` untuk buka URL manual
3. Klik kanan keyword di editor → `Search in browser`
4. Gunakan tombol back/forward di toolbar untuk navigasi history

**Konfigurasi**:
- Plugin sudah terinstall di `.obsidian/plugins/surfing/`
- Sudah aktif di `community-plugins.json`

---

## 2. NetClip Plugin - Web Clipping & Organize

### Status: ✅ Selesai

**Deskripsi**: Plugin untuk browse web dan clip halaman langsung ke vault dengan metadata terorganisir.

**Fitur yang dikonfigurasi**:
- [x] Default folder: `30-Resources/Clips`
- [x] Categories: Articles, Research, Tech, Video, Tutorial
- [x] Auto-save by domain mapping (YouTube → Clips/Video, GitHub → Clips/Tech)
- [x] AdBlock enabled
- [x] Card display lengkap (author, date, thumbnail, domain, description)
- [x] Keep original content enabled
- [x] Shortcuts: GitHub, YouTube, Reddit, Obsidian Forum
- [x] Home tab: recent files + saved articles
- [x] AI prompts: Summarize, Format as Note (disabled by default, butuh API key)

**Cara Penggunaan**:
1. Klik icon **NetClip** di sidebar atau Command palette → `Open NetClip View`
2. Paste URL di input field → pilih category → klik **Clip**
3. Atau gunakan **Webview mode** → browse → klik **Quick Save**
4. Lihat clipped content di `30-Resources/Clips/`

---

## 3. ReadItLater Plugin - Simpan Artikel untuk Dibaca Nanti

### Status: ✅ Selesai

**Deskripsi**: Plugin untuk menyimpan artikel/URL ke vault untuk dibaca nanti dengan metadata lengkap.

**Fitur yang dikonfigurasi**:
- [x] Default folder: `30-Resources/ReadItLater`
- [x] Metadata extraction: title, author, date, thumbnail, tags
- [x] Format as Markdown enabled
- [x] Auto-tag dengan `read-it-later`
- [x] Strip ads & navigation enabled
- [x] Keep images enabled
- [x] Clipboard support enabled
- [x] Drag & drop support enabled
- [x] Prompt before save enabled
- [x] File name format: `{{title}}`
- [x] Max content length: 50000 chars

**Cara Penggunaan**:
1. Copy URL dari browser atau catatan
2. Command palette → `ReadItLater: Save URL` atau paste URL
3. Artikel tersimpan di `30-Resources/ReadItLater/` dengan tag `read-it-later`
4. Filter di Notebook Navigator by tag untuk lihat queue

---

## Struktur Vault

### Folder yang sudah dibuat:

```
30-Resources/
├── Clips/
│   ├── Articles/
│   ├── Tech/
│   ├── Video/
│   └── Research/
└── ReadItLater/
    └── images/
```

**Keterangan**:
- `30-Resources/Clips/` - Tempat menyimpan hasil clip dari NetClip
  - `Articles/` - Artikel umum
  - `Tech/` - Konten teknologi (GitHub, docs, dll)
  - `Video/` - Konten video (YouTube, dll)
  - `Research/` - Konten riset
- `30-Resources/ReadItLater/` - Queue artikel untuk dibaca nanti
- `30-Resources/ReadItLater/images/` - Gambar dari artikel yang disimpan

---

## Changelog

### 2026-05-21
- ✅ Install dan konfigurasi Surfing plugin
- ✅ Buat dokumentasi VAULT-SETUP.md
- ✅ Install Style Settings untuk kustomisasi UI
- ✅ Install dan konfigurasi NetClip plugin
- ✅ Install dan konfigurasi ReadItLater plugin
- ✅ Setup folder structure: Clips, ReadItLater
- ✅ Install dan konfigurasi App Launcher untuk GitHub Desktop
- ❌ Hapus Notebook Navigator plugin dan konfigurasi

### 2026-05-21 - Optimasi & Cleanup

**Surfing Plugin**:
- ✅ Enable webview untuk render lebih baik
- ✅ Enable custom icons
- ✅ Set markdownPath ke `30-Resources/Clips`
- ✅ Update highlight format: blockquote style
- ✅ Disable random background
- ✅ Enable Live Preview inline URL support
- ✅ Clear bookmark tree data (bersihkan data lama)

**NetClip Plugin**:
- ✅ Pindahkan folder lama `NetClip/` ke `30-Resources/Clips/`
- ✅ Hapus folder `NetClip/` yang tidak terpakai

**ReadItLater Plugin**:
- ✅ Hapus folder `ReadItLater Inbox/` yang kosong
- ✅ Pastikan save location sesuai config: `30-Resources/ReadItLater/`

**Workspace**:
- ✅ Resize left sidebar: 200px → 350px
- ✅ Disable Web Viewer core plugin (tidak bentrok dengan Surfing)
- ✅ Hapus Notebook Navigator plugin dan konfigurasi

**Struktur Vault Final**:
```
30-Resources/
├── Clips/
│   ├── Articles/
│   ├── Tech/
│   ├── Video/
│   └── Research/
└── ReadItLater/
    └── images/
```

**App Launcher Plugin**:
- ✅ Konfigurasi GitHub Desktop via direct path
- ✅ Desktop path: `/Applications/GitHub Desktop.app`
- ✅ Mobile URL scheme: `x-github-client://`
- ✅ Ribbon icon tooltip: "Launch GitHub Desktop"
