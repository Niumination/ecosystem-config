---
name: pemdi-evidence-management
description: >-
  Kelola bukti dukung Pemerintah Digital (Pemdi) untuk evaluasi PermenPANRB
  8/2026 — cross-referensi data dari PemdiArena audit CSV, Excel master list,
  modul page JSON, dan JDIH/OpenData API. Inject validated evidence ke
  dashboard Next.js dengan inline PDF preview.
version: 1.0.0
author: Hermes Agent — Niumination Ecosystem
tags: [pemerintah-digital, pemdi, spbe, bukti-dukung, nextjs, evidence-management]
platforms: [macos, linux]
---

# Pemdi Evidence Management

Workflow untuk mengelola bukti dukung Pemdi (Pemerintah Digital) berdasarkan PermenPANRB No. 8 Tahun 2026 — dari audit bukti publik hingga inject ke dashboard.

## Trigger

Gunakan skill ini ketika:
- Ada file ZIP hasil scan PemdiArena (`BuktiDukungPemdiArena-*.zip`)
- Ada file Excel `Daftar_Lengkap_Bukti_Dukung_PEMDI_*.xlsx`
- Perlu validasi data dari modul-indikator page vs audit vs Excel
- Perlu inject bukti dukung ke dashboard Next.js `/modul-indikator`
- User menyebut "pemdi", "bukti dukung", "evaluasi SPBE", "PermenPANRB 8/2026"

## Prasyarat

- Next.js project dengan halaman `/modul-indikator` dan `data/pemdi.json`
- File ZIP dari PemdiArena (berisi `02_INDEKS_BUKTI_FINAL.csv`)
- File Excel `Daftar_Lengkap_Bukti_Dukung_PEMDI_*.xlsx`
- Akses ke Python dengan `openpyxl` untuk baca Excel
- Konten halaman modul page JSON (dari `modul_chunk.js` atau `data/modul-indikator.json`)

## Prosedur

### 1. Initial Data Extraction

```bash
# Extract ZIP
unzip -q "path/to/BuktiDukungPemdiArena-*.zip" -d /tmp/pemdi-unpack
```

Structure yang dihasilkan:
```
bukti_dukung_pemdi_aceh_tengah_L1_L2/
├── 00_MATRIKS_KEBUTUHAN_L1_L2.md    # Matriks I01-I20
├── 02_INDEKS_BUKTI_FINAL.csv        # 57 bukti final (kunci!)
├── 03_REKAP_KEKURANGAN.md           # Gap analysis
├── 04_KANDIDAT_DITOLAK.csv          # 30 ditolak (alasan)
└── 05_LOG_SCAN.md                   # Metodologi audit

downloads_jdih/       # Perbup PDF dari JDIH
downloads_opendata/   # File dari OpenData CKAN
downloads_repo/       # File dari GitHub repo
indicators_raw.json   # 20 indikator L1-L5
```

### 2. Level Naming Validation (KRITIS)

PermenPANRB 8/2026 menggunakan skema nama level yang berbeda dengan yang sering tertulis di Excel:

| Level | Module Page (BENAR) | Excel (sering SALAH) |
|:-----:|---------------------|----------------------|
| L1 | **Initiate** | Initiate/Kurang ✅ |
| L2 | **Emerging** | Emerging/Cukup ✅ |
| L3 | **Established** | ❌ Developing/Baik |
| L4 | **Leading** | ❌ Embedded/Sangat Baik |
| L5 | **Transformative** | ❌ Leading/Memuaskan |

**Jika Excel salah, koreksi dulu sebelum dipakai.** Nama harus sesuai yang digunakan di modul page.

### 3. Cross-Reference 3 Sumber

```python
import csv, json

# 1. Arena CSV (57 bukti)
arena = []
with open('02_INDEKS_BUKTI_FINAL.csv') as f:
    for row in csv.DictReader(f):
        arena.append(row)

# 2. Modul page JSON (20 indikator)
with open('modul_chunk.js') as f:
    content = f.read()
import re
m = re.search(r"JSON\.parse\('(.+?)'\)", content, re.DOTALL)
data = json.loads(m.group(1).replace("\\'", "'").replace('\\n', '\n'))

# 3. Excel master (177 item)
import openpyxl
wb = openpyxl.load_workbook('Daftar_Lengkap_*.xlsx', data_only=True)
ws = wb['02_Daftar_Lengkap_Bukti_Dukung']
```

Key checks:
- **Coverage**: Apakah semua indikator L1-L2 tercover?
- **Naming**: Apakah level naming sesuai PermenPANRB?
- **Files**: Apakah bukti dari CSV bisa di-match ke file di ZIP?
- **Gaps**: Apa yang gagal publik? (biasanya I09 audit + I12 CSIRT)

### 4. Build Structured JSON

Format bukti-dukung.json yang benar:

```json
{
  "bukti_dukung": {
    "I01": [
      {
        "level": 1,
        "judul": "Peraturan Bupati ...",
        "nama_file": "I01_L1_Perbup_48_2025.pdf",
        "local_path": "/bukti/I01_L1_Perbup_48_2025.pdf",
        "url_sumber": "https://jdih.acehtengahkab.go.id/dih/detail/...",
        "sumber_label": "JDIH Aceh Tengah",
        "icon": "⚖️",
        "status": "lengkap"
      }
    ]
  }
}
```

**Sumber icon mapping:**
| URL Pattern | Label | Icon |
|-------------|-------|:----:|
| `jdih.*` | JDIH Aceh Tengah | ⚖️ |
| `opendata.*` | OpenData Aceh Tengah | 📊 |
| `github.*` | GitHub (Repo Publik) | 💻 |

### 5. Inject ke pemdi.json

Gunakan mapping `I1 → I01`, `I2 → I02` untuk conciliate ID:
```python
def pad_indicator(ind):
    num = ind.replace('I', '')
    return f"I{int(num):02d}"
```

Tiap evidence item harus punya:
- `id`: unik (contoh: `V1.I1_1`)
- `level`: integer
- `nama`: judul pendek
- `detail`: sumber label
- `opd`: array OPD terkait
- `status`: "lengkap" atau "belum" atau "proses"
- `catatan`: deskripsi relevansi
- `url_preview`: URL untuk preview (pakai source URL, bukan local path!)
- `url_sumber`: original source

**Critical**: Jangan pakai local path `/bukti/` untuk `url_preview` jika file di-gitignore. Gunakan source URL (JDIH/OpenData/GitHub raw) sebagai fallback agar preview jalan di Vercel/production.

### 6. Add Inline Preview to Page

Di halaman `modul-indikator.js`:
1. **State**: `previewDoc` = `{ url, title, isPdf } | null`
2. **Aksi column**: tombol "👁️ Lihat" untuk PDF, "📥 Unduh" untuk XLSX
3. **Modal**: overlay fixed dengan iframe untuk PDF
4. **Conditional warning**: hanya muncul jika `status.lengkap === 0`

```jsx
const [previewDoc, setPreviewDoc] = useState(null);

// In table row:
{hasPreview && bd.status === 'lengkap' ? (
  isPdf ? (
    <button onClick={() => setPreviewDoc({url, title, isPdf: true})}>
      👁️ Lihat
    </button>
  ) : (
    <a href={url} target="_blank">📥 Unduh</a>
  )
) : (
  <span>—</span>
)}

// Modal:
{previewDoc && (
  <div className="fixed-overlay" onClick={() => setPreviewDoc(null)}>
    <div className="modal-content" onClick={e => e.stopPropagation()}>
      <div className="modal-header">
        <span>{previewDoc.isPdf ? '📄' : '📊'} {previewDoc.title}</span>
        <button onClick={() => setPreviewDoc(null)}>✕</button>
      </div>
      <div className="modal-body">
        {previewDoc.isPdf ? (
          <iframe src={previewDoc.url} style={{width:'100%',height:'100%',border:'none'}} />
        ) : (
          <div>File spreadsheet — <a href={previewDoc.url}>📥 Unduh File</a></div>
        )}
      </div>
    </div>
  </div>
)}
```

### 7. File Management

**Gitignore file bukti** (302MB+ tidak perlu di-git):
```gitignore
# Bukti dukung PDF/XLSX
/public/bukti/
```

**Copy file dari ZIP ke project:**
```python
import shutil
FILE_MAP = {
    'I01_L1_Perbup_48_2025_Arsitektur_SPBE': 'downloads_jdih/Perbup_48_2025_Arsitektur_SPBE.pdf',
    # ... map semua
}
for csv_stem, src_path in FILE_MAP.items():
    ext = os.path.splitext(src_path)[1]
    dest = f"public/bukti/{csv_stem}{ext}"
    shutil.copy2(f"/tmp/pemdi-unpack/{src_path}", dest)
```

### 8. Build & Deploy

```bash
npm run build
# Expected: ✅ build sukses, halaman modul-indikator static
# Live: https://pemdi-aceh-tengah.vercel.app/modul-indikator
git push origin main
# Vercel auto-deploy
```

### 9. Generate Markdown Ringkasan (per Indikator per Level)

Untuk laporan/review progres, generate file `.md` ringkasan dari `data/pemdi.json` + `data/modul-indikator.json` (keduanya sudah ada di repo — tidak perlu API):

```
pemdi.json            → 7 aspek → 20 indikator → bukti_dukung[] (id, level, nama, status, opd, url_sumber)
modul-indikator.json  → 20 modul → level_kriteria[0..5] (teks kriteria per level)
```

Struktur file yang dihasilkan (simpan ke `~/Downloads/`):
- Header: tahun, target indeks/predikat, total item
- **Statistik Ringkas**: tabel per aspek (indikator count, lengkap/proses/belum/total) + TOTAL
- **Detail per indikator** (I1..I20): untuk tiap level yang ada → `#### 🎯 Level N — <label> (x item)` + kriteria (1 kalimat pertama) + status ringkas + tabel bukti `| # | Bukti Dukung | Status | OPD | Sumber |` dengan link `url_sumber`

Tips implementasi:
- Level label: `{0:'Baseline',1:'Initiate',2:'Emerging',3:'Established',4:'Leading',5:'Transformative'}`
- Ringkas kriteria ke 1 kalimat: `k.split('.')[0] + '.'` setelah strip `#`/`*` marker
- Kelompokkan bukti per level: `by_level[lv].append(b)` lalu sort keys
- Status: `lengkap` → ✅, `proses` → 🔄, `belum`/missing → ⬜

### 10. Integrate "Peta Dokumen Kunci" (31 dokumen) — append, don't modify

User menyediakan dokumen `Peta_Dokumen_Kunci_Bukti_Dukung_PEMDI.md` (dari Excel `Daftar_Lengkap_*.xlsx` sheet 02 & 06 — 31 dokumen kunci, tiap dokumen punya substansi wajib + indikator yang dicakup + prioritas). Integrasi ke halaman `/modul-indikator`:

**⚠️ USER PREFERENCE (dikoreksi eksplisit 4 Aug 2026): JANGAN ubah bagian modul yang sudah sesuai dengan modul asli — TAMBAHKAN konten baru sebagai penjelasan detail bukti dukung DI BAWAH.** Modul asli (`modul-indikator.json`, `pemdi.json`, section modul di `pages/modul-indikator.js`) tetap 100% utuh; section dokumen kunci diletakkan setelah `</section>` modul, sebelum PREVIEW MODAL.

Langkah:
1. Simpan dokumen sumber ke `brain/docs/Peta_Dokumen_Kunci_Bukti_Dukung_PEMDI.md` (referensi ekosistem).
2. Parse ke `data/dokumen-kunci.json` (script Python: parse matriks `●` → `indikator[]` per dokumen + parse Bagian B `### 📄 N.` → jenis, penanggung_jawab, unit_pendukung, indikator_level, prioritas, substansi[]). Matriks adalah sumber indikator yang paling andal; Bagian A tabel sering gagal di-parse karena format `| **1** |`.
3. `pages/modul-indikator.js`: import `dokumenKunci`, tambah state `bukaDokumen` (accordion), render section baru di bawah modul cards: header 🗂️ + stat badges (total dokumen, prioritas tertinggi, total item substansi) + accordion per dokumen (nomor, nama, prioritas berwarna, badge indikator, ▾). Body accordion: Jenis, Penanggung Jawab, Unit Pendukung, Indikator & Level Dicakup, ul substansi wajib.
4. Verifikasi: `npx next build` (halaman modul asli tetap build), `curl localhost:PORT/modul-indikator | grep "Peta Dokumen Kunci"` — section baru tampil, modul asli utuh.
5. Commit `data/dokumen-kunci.json` + `pages/modul-indikator.js`; jangan commit file `.backup`.

Dokumen 6 (SK Tim Asesor) sengaja tanpa indikator di matriks (indikator_level: "Fondasi lintas indikator") — render badge "Lintas indikator".

### 11. Analisis Kesesuaian Dokumen Kebijakan (RPJMD) — verified 4 Aug 2026

Alur untuk membuktikan "apakah dokumen kebijakan (RPJMD 2025-2029, 409 hal) sudah memuat substansi yang dibutuhkan" dan menampilkannya sebagai section baru di halaman modul-indikator:

1. **Ekstrak dengan ODL-PDF** (lihat skill `document-content-pipeline` Step 1): `opendataloader_pdf.convert(input, output_dir, format='markdown,json')`. Untuk 409 hal / 9.9MB butuh ~1-2 menit; hasil `.md` 8.491 baris + 755 gambar. Java wajib ada (`brew install openjdk@21`, `export JAVA_HOME=...`, `export PATH="$JAVA_HOME/bin:$PATH"`).
2. **Scan kehadiran substansi**: loop keyword dari substansi wajib Peta Dokumen Kunci (SPBE, transformasi digital, portal layanan, interoperabilitas, persandian, satu data, kompetensi digital, dll) → `grep -o -i "$kw" file.md | wc -l` untuk melihat mana yang termuat (count > 0) vs kosong. Lalu `grep -n` untuk konteks baris spesifik.
3. **Lokasi halaman + screenshot** (teknik Step 2b di document-content-pipeline): cari halaman fisik via PyMuPDF text search dengan frasa unik dari isi halaman (bukan judul bab — judul muncul di daftar isi). Verifikasi halaman dengan print 400 chars pertama, lalu `get_pixmap(dpi=150-160)` → PNG.
4. **Rekap kesesuaian**: tabel 9 substansi Dokumen #1 dengan status (✅ termuat / ⚠️ perlu penguatan) + lokasi di dokumen (bab/nomor halaman cetak). Contoh hasil nyata: RPJMD memuat 6/9 (bab 2.3.4 Transformasi Digital II-116, Indeks SPBE target 1,92, portal terpadu III-40, interoperabilitas, anggaran Kominfo/Persandian); 3 perlu penguatan (matriks mapping RAN Pemdi, manajemen layanan digital, referensi eksplisit SIAP Digital).
5. **Render section baru** (additive — sesuai preferensi user): section "Analisis Kesesuaian RPJMD 2025-2029" di bawah Peta Dokumen Kunci: stat badges (x/y substansi termuat) + tabel kesesuaian + grid screenshot (klik perbesar via `previewDoc` modal yang sudah ada — reuse state yang sama, src PNG `public/docs/rpjmd/*.png`) + kotak kesimpulan (materi verifikasi I1 Level 1-2).
6. **Commit hanya file relevan** — `pages/modul-indikator.js` + `public/docs/rpjmd/*.png`; jangan ikutkan `.claude/skills/` atau `skills-lock.json` yang kadang muncul sebagai untracked (git reset HEAD lalu add selektif).

### 12. Perluas Analisis ke Indikator Lain ("RPJMD untuk Indikator Lainnya") — verified 4 Aug 2026

Setelah section Analisis Kesesuaian (Dokumen #1), user biasanya minta: "apakah substansi RPJMD juga dibutuhkan untuk indikator lain?" — untuk dokumen payung seperti RPJMD jawabannya hampir selalu YA. Alur:

1. **Scan keyword per indikator lain** di hasil ODL markdown: I3 (kompetensi digital / SDM digital / talenta digital), I5 (satu data / e-walidata / forum satu data), I7 (statistik sektoral / EPSS), I10-12 (keamanan siber / persandian), I14 (infrastruktur TIK / broadband / akses internet), I15 (proses bisnis / ketatalaksanaan), I17 (command center / portal), I20 (indeks kepuasan masyarakat / SKM). Gunakan `grep -o -i "$kw" file.md | wc -l` + `grep -n` untuk konteks. Kata kunci pendek ("big", "SDM") false-positive — gabungkan dengan kata kedua untuk konfirmasi.
2. **Lokasi halaman fisik**: cari via PyMuPDF text search per frasa unik isi halaman (mis. "Aceh Tengah satu data" → hal 281; "Pemenuhan Prinsip Satu Data Indonesia" → hal 333/381; "Indeks Survey Kepuasan Masyarakat" → hal 400; "Command Center dan sistem egovernment" → hal 239). Render PNG `get_pixmap(dpi=160)` → `public/docs/rpjmd/`.
3. **Tabel mapping** per indikator: Substansi RPJMD yang Termuat + Dokumen Kunci Terkait (#18 bukti eksternal SDI/EPSS, #20 IKASANDI, #22 kriptografi, #23-24 CSIRT, #26 infrastruktur, #27 BPMN, #29 portal, #31 SKM) + Lokasi (bab/halaman cetak).
4. **Render section baru** "RPJMD untuk Indikator Lainnya" dengan pola identik section 11: stat badges + tabel + grid screenshot (reuse `previewDoc` modal) — additive, jangan sentuh section/modul lain.
5. Contoh hasil nyata: RPJMD memuat substansi untuk 10 indikator lain (I3, I5, I7, I10, I11, I12, I14, I15, I17, I20) — termasuk target IKM per OPD (82,13→88,40), program persandian, dan program unggulan "Aceh Tengah Satu Data".

### 13. Batch Ekstraksi Dokumen Pendukung Diskominfo ("Bukti Dukung Dokumen Pendukung") — verified 4 Aug 2026

User menyediakan folder `~/Documents/odl-pdf bukti dukung/` berisi 4 PDF + 1 xlsx pendukung (RENSTRA 25-29, Ranhir Renja 2026, DPA 2026, RKA Rincian Belanja SPBE, capaian realisasi RKPD). Alur batch:

1. **Inventaris dulu**: `ls -la` folder + hitung halaman tiap PDF via PyMuPDF (`fitz.open(path)` → `len(doc)`). Contoh riil: Renstra 53 hal, Renja 33, DPA 97, RKA 3.
2. **Ekstraksi batch ODL-PDF** (loop per file, `format='markdown,json'`, output ke `/tmp/odl-bukti/`). DPA 97 hal butuh ~2-3 menit; gunakan `timeout` generous. xlsx → `openpyxl` dump semua sheet ke JSON; formula cell muncul sebagai string (`'=F9/E9*100'`) — baca nilai yang terisi + header kolom, jangan andalkan formula.
3. **Scan keyword per indikator** di tiap markdown: SPBE, arsitektur, peta rencana, proses bisnis, portal, persandian, keamanan informasi, aplikasi, infrastruktur, kepuasan → `grep -o -i "$kw" file.md | wc -l` + `grep -n` konteks. Hasil riil: RENSTRA → tujuan-sasaran SPBE 2,6→2,9 + program aplikasi informatika 2,88-2,96 + 7 dokumen kebijakan tata kelola SPBE (sub kegiatan 0037) → **I1,I2,I4,I13,I15,I16**; DPA → rincian anggaran (portal Rp 90 jt, tata kelola SPBE Rp 154,6 jt, kabupaten cerdas Rp 179,4 jt, persandian Rp 86,4 jt) → **I1,I10,I11,I14,I17**; realisasi RKPD xlsx → Indeks SPBE realisasi **2,59** (target 2,8), IPS, IKM → **I1,I7,I20**.
4. **Screenshot**: PyMuPDF text-search frasa unik isi halaman → `get_pixmap(dpi=160)` → `public/docs/bukti/<dok>-<label>.png`. Untuk bukti xlsx: buat PNG tabel via PIL (`ImageDraw` + font truetype Helvetica) — tidak perlu headless office.
5. **Section baru** "Bukti Dukung Dokumen Pendukung": tabel 5 dokumen × substansi yang termuat × indikator terkait × dokumen kunci (#1, #4, #9, #18, #20, #22, #26, #27, #29, #31) + grid screenshot (reuse `previewDoc` modal) + stat badges (jumlah dokumen, indikator terdukung, nilai kunci seperti "SPBE realisasi 2,59"). Additive — jangan ubah section/modul lain.
6. **Commit selektif**: `pages/modul-indikator.js` + `public/docs/bukti/*.png` saja. `.claude/` dan `skills-lock.json` sering muncul untracked (dari aktivitas JCode/Claude) — `git reset HEAD` lalu `git add` selektif, jangan `git add -A`.

### 14. Penyelarasan Bukti Existing ↔ Peta Dokumen Kunci (analisis inkonsistensi) — planned 4 Aug 2026

Setelah Peta Dokumen Kunci (31 dok) + analisis RPJMD + bukti pendukung live di halaman modul-indikator, user minta: **sesuaikan bukti dukung pada section "Kondisi Existing" dengan peta dokumen kunci di bawahnya** (hindari inkonsistensi nomenklatur/gap).

**Model 3 sumber** (semua sudah ada di repo, tidak perlu API):
- `data/modul-indikator.json` → level_kriteria + `data_dukung_modul` (46 item, hanya 14/20 modul terisi)
- `data/pemdi.json` → `bukti_dukung` (114 item: V1/V2/B) = tabel "Kondisi Existing"
- `data/dokumen-kunci.json` → 31 dokumen kunci + substansi wajib + `indikator[]` (dari matriks ●)

**Temuan inkonsistensi** (pola script: loop aspek→indikator, bandingkan `len(ind.bukti_dukung)` vs `[d for d in dokumen if ind in d['indikator']]`):
1. Bukti existing TIDAK punya relasi ke dokumen kunci — tabel existing hanya level+status+catatan, tanpa badge nomor dok.
2. Nomenklatur tidak seragam: bukti "Perbup 48/2025 Arsitektur SPBE" sebenarnya = dok #3 (Arsitektur SIAP Digital); "Dokumen Peta Kompetensi ASN" = #9 — tapi tidak ditandai, user tak bisa lihat korelasi.
3. Gap volume: I8 existing 7 item kecil vs dok #17 = **35 item PDP** (terbesar); I1 8 item vs 6 dok kunci (38 substansi).
4. Halaman `requirement.js` (Peta Proses Bisnis, Permenpan 19/2018) kategori F (SPBE & TIK) tidak mereferensikan dok #27 (BPMN) & I15.

**✅ Dieksekusi 5 Aug 2026 — commit `fc428cd` (lihat `references/bukti-dokumen-keyword-map.md` untuk KEYWORD_MAP lengkap).**

Alur eksekusi terbukti:

1. **Build `data/bukti-dokumen-mapping.json`** via script Python:
   - `KEYWORD_MAP`: dict `{ fragment_nama_bukti: [nomor_dokumen_kunci] }` — mis. `'arsitektur': [3]`, `'dpa'/'rka'/'kak': [4]`, `'peta kompetensi': [9]`, `'ikasandi': [20]`, `'skm'/'fgd': [31]`.
   - **TEKNIK KRITIS — filter by indicator coverage**: setelah keyword match, intersect dengan `{d.no for d in dokumenKunci if indikator_id in d['indikator']}`. Tanpa filter ini muncul false positive parah: "terka**i**t" → keyword `'ai'` → #13; "Perbup ... tentang Sist**em**" → `'sist'` fragment → salah dok. Dengan filter: 110/114 terpetakan (96.5%), 4 yang tak terpetakan memang wajar (Perbup SOTK I3, bukti salah penempatan).
   - **Nama bukti di pemdi.json TERPOTONG** ("Peraturan Bupati ... tentang Ars" = Arsitektur, "tentang Sat" = Satu Data) — tambah keyword fragment aman: `'tentang ars': [3]`, `'tentang sat': [18]`, `'tentang sist': [17]`.
   - Urutan keyword penting: fragment spesifik DULU (`'peta kompetensi'` sebelum `'kompetensi'`, `'reviu laporan kinerja'` sebelum `'reviu'`) karena iterasi pertama yang match menang (pakai `set.update` bukan break — gabungkan semua match lalu filter).
   - Simpan `stats: {total_bukti, terpetakan, belum_terpetakan}` di root JSON untuk badge UI.

2. **`pages/modul-indikator.js` tabel "Kondisi Existing"** — implementasi terbukti:
   - Import `buktiMapping` + helpers: `getDokumenForBukti(indId, buktiId)` (lookup id → dokumen_kunci[]), `getDokumenInfo(no)` (nama dok dari dokumen-kunci.json), `groupBuktiByDokumen(indId, buktis)` (Map by no; grup 0 = "Tanpa Dokumen Kunci" ditaruh terakhir).
   - State `viewMode = {}` per modul: `{ [modul.nomor]: 'level' | 'dokumen' }` — toggle per-modul, bukan global.
   - View "Per Level" (default): tambah kolom **"Dokumen Kunci"** — badge `#3` diklik → `setBukaDokumen(no)` (reuse accordion state dokumen kunci di bawah, scroll otomatis karena render section bawah).
   - View "Per Dokumen Kunci": kartu per dok — tombol `#no` (klik → buka dokumen di bawah) + nama dok + badge `X/Y lengkap` (🟢 semua / 🟡 sebagian / 🔴 belum, dari `status` bukti anggota).
   - Badge statistik di header toggle: `{buktiMapping.stats.terpetakan}/{total_bukti} bukti terpetakan`.

3. **`pages/requirement.js` + `pages/api/requirement.js`**: tiap item kategori F (SPBE & TIK) dapat field `dokumenKunci` (`'#3'`, `'#2'`, `'#27'`, `'#25'`, `'#28'`) → render kolom "Dok. Kunci" di tabel (badge hijau) — kategori lain `—`.

4. **Validasi & deploy**: `next build` (0 error) → test lokal (curl section + API) → commit selektif 4 file (`bukti-dokumen-mapping.json`, `modul-indikator.js`, `requirement.js`, `api/requirement.js`).

### 15. Audit Konsistensi Menyeluruh (semua halaman & data Pemdi) — verified 5 Aug 2026

Saat user minta "periksa seluruh halaman yang berkaitan dengan pemdi, apakah masih ada inkonsistensi data/gap/ketidaksesuaian mengacu modul indikator asli dan turunannya" — lakukan audit checklist ini SEBELUM eksekusi, lalu laporkan temuan (jangan langsung fix tanpa laporan):

1. **Indikator & aspek identity**: `pemdi_ind == modul_ind` (harus 20=20) dan set aspek modul == set aspek pemdi (7=7). Script: `[i['id'] for a in pemdi['aspek'] for i in a['indikator']]` vs `[m['indikator_id'] for m in moduls['modules']]`.
2. **Bobot konsisten**: sum bobot aspek == sum bobot indikator == 100; per aspek `sum(i.bobot)` == `a.bobot`. (Aktual: semua ✅.)
3. **Level subset**: `set(bd.level) ⊆ set(level_kriteria modul)` untuk tiap indikator. (Bukti L1-2 ⊆ modul L1-5 ✅.)
4. **`total_item` vs bukti aktual** (T1): `sum(a.total_item)` = 178 tapi `len(bukti_dukung)` = 114 → **gap 64 item** (item yang belum dibuat, contoh terbesar I8 PDP: total_item 35 vs 7 bukti). Jangan samakan angka ini; tampilkan sebagai gap.
5. **Metadata stale** (T2): `total_item_bukti: 57` sudah outdated vs 114 aktual (57 V1/V2 + 57 B). Cek juga AGENTS.md/README klaim lama.
6. **Dokumen kunci tanpa bukti** (T3): hitung `{d.no for d in dokumenKunci} - used` dari `bukti-dokumen-mapping.json` → dok #2, #6, #11, #12, #14 tanpa bukti existing (padahal #2/#6 prioritas Tertinggi) → butuh placeholder "Perlu disusun".
7. **Duplikasi nama V1/V2** (T4): 18/20 indikator punya nama bukti sama di L1 dan L2 (satu dokumen mendukung 2 level — pola VALID, bukan bug). Group by `nama[:55]` via Counter; kalau >1 dengan nama sama, tandai penjelasan di UI (tooltip "Dokumen sama mendukung L1 & L2").
8. **Nilai indikator statis** (T6): semua `nilai: 1.0` di pemdi.json TIDAK diturunkan dari status bukti (57 lengkap) — halaman pemdi tampil indeks 1.0 padahal ada bukti lengkap. Opsi: hitung nilai dari % bukti lengkap per level.
9. **False positive mapping** (T5): audit `bukti-dokumen-mapping.json` — I19 "Survei Kepuasan Masyarakat" → #31 (bukan #30); I3 "Asesmen BKN" → #9 saja (bukan [4,9,10,13]).
10. **Klaim lintas halaman**: "7 aspek, 20 indikator" konsisten (✅); badge dokumen kunci baru ada di kategori F requirement saja (T7) — kategori lain belum.

Format laporan: tabel ✅ Konsisten / 🔴 Kritis (gap, stale metadata, dok tanpa bukti) / 🟠 Sedang (duplikat nama, false positive, nilai statis) / 🟡 Minor — lalu tawarkan prioritas eksekusi (rekomendasi: data + UI utama dulu).

### 16. Eksekusi Perbaikan Audit T1-T9 — verified 5 Aug 2026, commit `fb812cf`

Setelah laporan audit (section 15) disetujui, eksekusi 9 fix berurutan. Formula & pitfall yang terbukti:

1. **T1+T2 (metadata & gap)** — `total_item_bukti` 57→**114** (realita), tambah `target_item_bukti` 178 (target Excel asli) + `item_aktual`/`item_gap` per aspek. ⚠️ **Backup dulu** (`cp data/pemdi.json data/pemdi.json.bak-t1`) sebelum edit massal JSON. Stat bar modul-indikator jadi `114/178 bukti dukung` + badge `Gap: 64 item`.
2. **T6 (nilai dari bukti)** — formula terbukti: `nilai = max(level dengan ≥1 bukti lengkap)` minimum 1.0; nilai aspek = rata-rata bobot indikator; ⚠️ **PITFALL**: JANGAN timpa `baseline_spbe` (2.59 = nilai SPBE 2025 historis) — simpan indeks hasil hitung di field terpisah `indeks_terkini` (hasil: 1.92). Kalau terlanjur tertimpa, restore dari backup. Label pemdi.js: "Indeks Pemdi (dari Bukti Dukung)".
3. **T3 (placeholder dok tanpa bukti)** — helper `getDokumenTanpaBukti(indId)` = `{d.no for d in dokumenKunci if indId in d['indikator']}` minus `{no for b in mapping[indId] for no in b.dokumen_kunci}`; render di view Per-Dokumen: border dashed warn + badge "🆕 Perlu Disusun". (5 dok: #2, #6, #11, #12, #14.)
4. **T4 (duplikat V1/V2)** — helper `deteksiDuplikat(buktis)`: Counter atas `nama[:55]`, id yang muncul >1x ditandai badge "🔁 multi-level" + tooltip "Dokumen sama dipakai di lebih dari satu level — wajar sesuai kriteria level".
5. **T5 (mapping → 114/114)** — setelah keyword+filter indikator, tambah **override manual per-id** di fungsi match: `asesmen bkn→[9]`, `survei kepuasan→[31]`, `reviu laporan kinerja→[1]`, `sotk→[9]`, `'126'→[30]`, `'48' and 'ars'→[19]` (I9) / `[23]` (I12).
6. **T7 (requirement semua kategori)** — semua 83 item kategori A-L diberi `dokumenKunci`. ⚠️ **PITFALL**: saat menulis ulang seluruh `pages/api/requirement.js`, JANGAN hilangkan `export default function handler(req,res){...}` di akhir — kehilangannya → HTTP 500 "Page /api/requirement does not export a default function". Selalu cek tail file sebelum commit, lalu test `curl /api/requirement -w "%{http_code}"` = 200.
7. **T8 (data_dukung_modul kosong)** — 8 modul kosong diisi dari substansi dokumen kunci (urut prioritas tertinggi, max 2 dok × 3 substansi, cap 6): 46→**85** item.
8. **Verifikasi** — `curl /modul-indikator | grep "114/178\|Gap"`, `curl /pemdi | grep "1,92"`, `curl /api/requirement | python json.count(dokumenKunci) == 83`.

### 17. Inject Bukti Baru dari Portal Evaluasi (eval.spbe.go.id) & Documents — verified 5 Aug 2026, commit `6a5c187`

Sumber baru yang ditemukan user (selain JDIH/OpenData/Arena):
- `~/Documents/REAL-PEMDI-DATA DUKUNG/` — **7 PDF yang SUDAH diunggah ke portal eval.spbe.go.id**. Prefix nama file = kode portal: `PG_04_*` (tata kelola pemerintahan) & `TD_13_*` (teknologi digital). Contoh nyata: `PG_04_01_SK-Koordinasi_2026.pdf` (SK Bupati 555/395/2026 Tim Koordinasi PEMDI), `PG_04_02_DPA_2026.pdf` + `TD_13_02/05_DPA_2026.pdf` (RKA/DPA sub kegiatan 0037 tata kelola SPBE Rp154,6 jt), `PG_04_03_RapatPemdi_2026.pdf` (undangan+rundown Rapat Transformasi Digital 25-26 Jun 2026, narasumber KemenPANRB), `TD_13_01_KAK-Bapokting_2026.pdf` + `TD_13_04_LaporanBapokting_2026.pdf` (SDLC aplikasi Bapokting).
- `~/Documents/` root + `~/Documents/odl-pdf bukti dukung/` — **13 file belum diunggah**: Indeks KAMI 5.0 (xlsx, skor 563 "Cukup Baik", 13 Apr 2026), 2 Perbup persandian, SK Forum Satu Data 188.55/375/BAPPEDA/2025, RPJMD 2025-2029 (409 hal), Renstra/Renja/DPA/RKA Diskominfo 2026, capaian realisasi RKPD (xlsx).

Alur terbukti:
1. **Inventaris & klasifikasi**: `ls -la` kedua folder + hitung halaman via fitz + cek text layer (`pdftotext -l 2 f - | head` — output hanya `\\f` = scan → OCR via `scripts/ocr_macos_vision.py` — macOS Vision via pyobjc, offline & gratis, WAJIB flags Fast + en-US + no language correction, jangan swiftc; detail di `references/macos-vision-ocr.md`).
2. **Mapping ke dokumen kunci**: SK Tim Koordinasi→#5, DPA/RKA→#4, rapat koordinasi→#7, KAK/Laporan aplikasi→#25, Indeks KAMI→#20 (+#17 bagian PDP), Perbup persandian→#22, SK Forum SDI→#18, RPJMD/Renstra/Renja→#1, capaian RKPD→#1/#18, Perbup SOTK→`[]` (pendukung, sengaja tanpa dokumen kunci).
3. **Copy ke `public/bukti-dukung/05-portal-pemdi/`** (file portal) + **`06-dokumen-2026/`** (dokumen). ⚠️ PITFALL: nama file >255 char → macOS `cp: File name too long` — copy ulang dengan nama pendek.
4. **Preview xlsx**: `qlmanage -t -s 1200 -o /tmp <file.xlsx>` → thumbnail PNG (bisa dipakai `url_preview` dengan `_ext: "png"`, `url_sumber` = xlsx asli).
5. **Inject `data/pemdi.json`**: id `P1.<ind>_<n>` (tidak bentrok dengan V1/V2/B), flags `_sumber_baru: true`, `_dokumen_kunci: [nos]`, `_portal: true|false`, `_ext`. Status: `proses` (sudah di portal tapi belum diverifikasi level) / `belum` (belum diunggah). Update `total_item_bukti` = hitung aktual (114 → 134: 57 lengkap, 70 belum, 7 proses). ⚠️ Backup dulu.
6. **Regenerate `data/bukti-dokumen-mapping.json`**: di script build, item dengan `_sumber_baru` pakai `_dokumen_kunci` LANGSUNG (bukan keyword match) — tambah field `sumber: "baru"|"existing"` di tiap entry.
7. **UI section baru** (additive, sesuai preferensi user): helpers `getBuktiBaru()` (loop aspek→indikator, kumpulkan `_sumber_baru`, tambah `_indikator`) & `hitungBuktiBaru()` (return total/proses/belum/dokumen-unik). Tabel: Ind badge, nama+detail+catatan+link preview, level, tombol dokumen kunci (`setBukaDokumen`), status badge, sumber (`🖥️ Portal eval.spbe.go.id` / `📁 Documents 2026`).
8. **Verifikasi & deploy**: build → test lokal → commit selektif. ⚠️ File public dengan spasi di nama: browser handle otomatis, tapi `curl` perlu `%20` encoding (HTTP 000 ≠ error, jangan panik). Status `proses`/`belum` TIDAK mengubah indeks — hanya `lengkap` yang dihitung.

### 18. Checklist Bukti Dukung per Indikator di Halaman /pemdi — verified 5 Aug 2026, commit `3c62762`

User minta section baru di **halaman `/pemdi`** (bukan hanya modul-indikator): per indikator → checklist ketersediaan bukti per level, preview dokumen yang tersedia, rekomendasi pelengkap, dan **catatan mandiri** (dibutuhkan saat upload bukti di portal eval.spbe.go.id). Semua angka harus **dihitung runtime dari data** (pemdi.json + modul-indikator.json + bukti-dokumen-mapping.json), jangan hardcode.

Kartu per indikator (20 kartu, dikelompokkan per aspek):
1. **Header**: badge `I#`, nama, `Nilai X / Target Y`, stat `✅ lengkap · 🔄 proses · ⬜ belum`, link `Modul →` (`/modul-indikator?modul=<no>`).
2. **Grid level L1-L5**: tiap box → chip level (`LEVEL_WARNA[lv]` dengan bg `18`% alpha), hitungan `lengkap/total`, daftar bukti (icon status + nama + badge `#dok` dari `getDokumenForBukti` + tombol `👁️ preview`). Box kosong → italic "— belum ada bukti".
3. **Preview**: reuse komponen `DetailModal` (side-panel, `maxWidth 820`) + iframe. **PITFALL**: URL JDIH tanpa ekstensi → regex `\.(pdf|png|jpe?g|gif|webp)(\?|$)` gagal → render fallback link "Buka file sumber" (jangan iframe kosong).
4. **Rekomendasi** (`rekomendasiInd(ind, kriteriaFn)`): (a) 📈 level berikutnya untuk capai target + snippet kriteria `L{next}` dari `level_kriteria` modul (strip `#`/`*`, wrap 180 char); (b) 🆕 level 1..nilai+1 yang belum punya bukti sama sekali; (c) 🔄 n bukti proses → verifikasi kesesuaian kriteria; (d) ⬜ n bukti belum → lengkapi & unggah; (e) 🗂️ dokumen kunci belum ter-cover untuk indikator itu (via mapping).
5. **Catatan mandiri**: `defaultCatatan(ind)` auto-generate teks ("Catatan Mandiri I# — nama\n\nBukti dukung disusun untuk memenuhi kriteria…\nDokumen yang dilampirkan:\n- nama (Level n, status: X)\n…"), textarea `value = catatan[ind.id] ?? defaultCatatan(ind)`, onChange → state + `localStorage['pemdi.catatan.'+ind.id]` (persist lintas sesi), tombol `📋 Salin` (navigator.clipboard).

**Verifikasi SSR**: React render angka sebagai text node terpisah → `curl | grep -o ">134<"` TIDAK match, `grep "134"` hit banyak (false positive). Pakai `browser_console` (querySelector + getComputedStyle + classList) untuk cek DOM aktual; `grep -c "Judul Section"` cukup untuk cek section ada.

**Audit data sebelum commit** — jalankan `scripts/audit_sync.py` (7 checkpoint: total vs aktual, nilai == level bukti lengkap, mapping ids, _dokumen_kunci konsisten, modules coverage, URL lokal → file ada, distribusi bukti baru). Terbukti menemukan: `rekomendasi` kosong di semua 20 modul (diisi dari logika sama), dan false-positive URL (raw.githubusercontent.com di-skip — file ada tapi di luar repo).

### 19. Tata Letak Floating Widget & Lebar Side Panel — verified 5 Aug 2026, commit `676fd1b`

User melaporkan 2 bug UI: (a) widget survei SKM hilang, (b) tombol kembali ke atas tertimpa tombol rating. Akar masalah: **3 widget `position: fixed` semuanya di kanan-bawah dengan z-index berbeda**:

| Widget | Posisi lama | z-index | Masalah |
|--------|-------------|:-------:|---------|
| SkmPrompt (survei) | `bottom:1.5rem; right:1.5rem` | 1000 | Tertutup rating (z lebih rendah) |
| RatingWidget ★ | `bottom:28; right:28` (52×52) | 9999 | Menutupi survei & scroll-top |
| ScrollTop ↑ | `bottom:22; right:22` | 999 | Tertimpa rating (posisi sama) |

**Alur fix (audit dulu, baru susun ulang):**
1. Audit SEMUA widget fixed: `grep -rn "position: fixed\|position:fixed" components/ pages/ styles/` — jangan perbaiki satu widget sendirian, pasti ada widget lain yang bertabrakan.
2. Susun ulang secara sengaja:
   - **Survei → kanan-atas** di bawah sticky header: `top: calc(var(--gov-strip-h, 36px) + 70px)` (gov-strip 36px + topbar ≈54-70px), `bottom: auto`, animasi `slide-down` (bukan slide-up). Mobile: `top: calc(var(--gov-strip-h) + 64px)`, `left/right: 1rem`.
   - **Rating ★ → tetap kanan-bawah** (bottom 28, right 28, 52×52, z 9999).
   - **ScrollTop ↑ → di ATAS rating, sejajar terpusat**: `bottom: 28 + 52 + 10 = 90px`, `right: 28 + (52-44)/2 = 32px`, `z-index: 9999`.
3. **PITFALL DetailModal/PreviewModal lebar mentok 480px**: CSS `.sp-panel { width: 480px }` FIXED — prop `maxWidth` hanya override `max-width`, jadi panel preview `maxWidth={820/1000}` tetap render 480px. Fix di `components/DetailModal.js`: `style={{ width: maxWidth, maxWidth: '90vw' }}` (width mengikuti prop, dibatasi 90vw di layar kecil). Verifikasi ukuran via `browser_console`: `document.querySelector('.sp-panel.open').getBoundingClientRect()` → preview 1000, detail 680.
4. **PITFALL orphan next-server pegang port**: `pkill -f "next start"` membunuh parent npm TAPI anak `next-server` tetap hidup memegang port → server baru exit `errno: -48` (EADDRINUSE; `lsof -i :PORT` masih LISTEN). Sebelum restart: `lsof -i :PORT | grep LISTEN` → `kill -9 PID` → start ulang. Gejala test browser gagal padahal build OK = cek port dulu.

### 20. Audit Stale File di Repo PemdiAcehTengah — verified 6 Agu 2026

User minta "periksa PemdiAcehTengah" — audit kebersihan repo (bukan data). Pola yang terbukti & temuan riil:

**DUA folder bukti paralel (kritis — jangan tertukar):**
| Folder | Ukuran | Status | Referensi |
|--------|--------|--------|-----------|
| `public/bukti/` | **302 MB** (57 PDF per-indikator `I05_L1_*.pdf`) | ❌ **LEGACY MATI** | 0 referensi di `data/*.json` + `pages/`; di-`.gitignore` (`/public/bukti/`); tidak ter-track git |
| `public/bukti-dukung/` | 67 MB (66 file, 00-manifest s/d 06-dokumen-2026) | ✅ **LIVE (canonical)** | 44+ referensi `url_preview` di pemdi.json; 62 file tracked |

**Konteks**: bukti lama (`Ixx_Ly_*.pdf`) pernah jadi canonical (section 7 skill ini), lalu restrukturisasi pindah ke `public/bukti-dukung/` — folder lama tidak dihapus. Verifikasi sebelum rekomendasi hapus: `grep -rl "/bukti/" data/*.json pages/ components/ lib/` → harus 0 (hanya `/bukti-dukung/` & `/docs/bukti/` yang valid — **PITFALL: `docs/bukti/*.png` = screenshot Renstra/DPA yang DIPAKAI modul-indikator.js, jangan ikut dihapus**).

**Checklist audit repo Pemdi (urutan terbukti):**
1. `git status --short` + `git rev-list --count @{upstream}..HEAD` (ahead/behind) — repo harus sinkron.
2. Artifact proses: `find . -name "out*.txt" -o -name "*.bak*" -o -name "*.tmp"` (di luar node_modules) → `public/bukti-dukung/05-portal-pemdi/out1-3.txt` = sisa redirect output OCR (13KB teks SK; out3 = 9 byte form-feed). Tidak ter-track git → aman hapus.
3. Backup JSON di `data/`: `pemdi.json.bak-p1/.bak-t1`, `modul-indikator.json.bak-t8` (dari sesi inject) → aman hapus (data valid, backup tidak ter-track).
4. `.DS_Store` di root/docs/public/pages.
5. **Sebelum merekomendasikan hapus**: `git ls-files | grep <path>` — untracked + 0 referensi = safe-to-delete; tracked = cek riwayat dulu.
6. Ukuran: `du -sh public/*/ node_modules .next .git` — hapus `public/bukti/` (302MB) memangkas repo 869M → ~567M.
7. **Verifikasi production sebelum & sesudah**: `curl -s -o /dev/null -w "%{http_code}" https://pemdi-aceh-tengah.vercel.app/modul-indikator` = 200 (membuktikan folder lama memang tidak dipakai).

**Preferensi user (5-6 Agu 2026)**: ROOT ekosistem cleanup = **laporan dulu, jangan eksekusi** ("jangan langsung di eksekusi, cukup periksa dan berikan laporan serta rekomendasi saja"); item jelas aman (Icon\r 0-byte, __pycache__, out*.txt, .bak JSON) boleh langsung eksekusi setelah user menyetujui.

### 21. Verifikasi Konten Modul Indikator + Fokus Mode (ODL re-extraction) — verified 6 Agu 2026
User menduga konten section modul indikator "kacau" setelah banyak perubahan bertumpuk, dan minta: periksa ulang / ekstrak ulang dengan ODL-PDF dari sumber asli, lalu **sembunyikan semua section lain** di halaman modul-indikator agar fokus ke section bersumber modul asli dulu. **TIDAK di-push — cukup localhost** ("tidak perlu di push dulu, cukup jalankan di localhost untuk lihat hasilnya, aku mau fokus disini dulu").

**1. Ground truth = ODL re-extraction dari PDF asli:**
- Sumber: `~/Documents/Modul Indikator 1-20/` — 20 PDF (nama `N 20260622 Revamp [2] Modul Indikator N.pptx.pdf`, Indikator 8 = `Revisi Materi PEMDI_Indikator 8 ...pdf`).
- Jalankan `scripts/odl-pdf-batch.py` (SOURCE_DIR → `apps/PemdiAcehTengah/docs/modul-indikator/`, output `<nama>.md` + `<nama>_images/`). ~1-2 menit untuk 20 file.
- **PITFALL: folder `docs/modul-indikator/` kosong (0 file) sebelum re-extract** — hasil batch lama terhapus; output baru 20 .md + folder images. Ini jadi pembanding (source of truth) melawan `data/modul-indikator.json`.

**2. Deteksi "kacau" di modul-indikator.json (pola yang terbukti):**
- **Duplikasi frasa**: kriteria L1 modul 1 punya "...dalam tahap penyusunan. **Nasional Pemerintah Digital pada perencanaan Instansi Pemerintah dalam tahap penyusunan**" — frasa terulang. Cek: normalisasi whitespace lowercase lalu hitung frekuensi frasa 20-30 char (`norm.count(frag) > 1`).
- **Deskripsi = judul**: deskripsi I2 berisi "Aspek 1 - Indikator 2 Tingkat Kematangan..." (heading, bukan deskripsi).
- **Kriteria lintas modul identik**: I1 L2 ≈ I14 L2 ≈ I18 L1/L2 (frasa RAN Pemdi) — bisa jadi wajar (level awal berbasis perencanaan) ATAU tertukar; verifikasi ke PDF asli sebelum menyimpulkan.
- **Penyebab akar**: di PDF asli (PPT→PDF), sebagian tabel level = **GAMBAR** (`imageFileNNN.png`), bukan teks — isi JSON kemungkinan transkripsi manual dengan error penggabungan. OCR gambar kriteria sering cuma dapat logo/teks header (panrb, rAKHLA) — **jangan andalkan OCR gambar; andalkan teks markdown dari ODL + cek baris konteks** (`grep -n "tahap penyusunan" <md>`).

**3. Fokus mode — sembunyikan section (teknik `{false && (...)}`):**
User minta hanya 5 blok inti modul yang tampil: 20 indikator, kriteria level, contoh bukti dukung, penanggung jawab, bukti dukung kondisi existing. Semua section tambahan (Bukti Dukung Baru 2026, Peta Dokumen Kunci, Analisis Kesesuaian RPJMD, RPJMD Indikator Lain, Bukti Dukung Dokumen Pendukung, Quick Actions) **disembunyikan, bukan dihapus** — bungkus dengan `{false && (<section>...)}` + komentar `DISEMBUNYIKAN (fokus modul asli)` sehingga mudah dikembalikan.

Peta section di `pages/modul-indikator.js` (6 Agu 2026): HERO 331-367 · FILTER+MODUL LIST 369-871 · BUKTI BARU 873-972 · DOKUMEN KUNCI 974-1098 · RPJMD 1100-1235 · RPJMD LAIN 1237-1370 · DOKUMEN PENDUKUNG 1372-1481 · PREVIEW MODAL 1483+. Quick Actions di dalam accordion (847-857) juga di-disable.

**4. Verifikasi fokus mode:**
- `npx next build` → bundle modul-indikator turun 12 kB → **6.85 kB** (section tersembunyi ikut di-tree-shake — bukti berfungsi).
- SSR grep: section tampil (`grep -c 'Modul Indikator Pemdi'` > 0), section tersembunyi = 0 (`grep -c 'Peta Dokumen Kunci'` = 0, dst).
- Konten accordion hanya render saat klik — cek via browser (`browser_console` + `dispatchEvent` mousedown/mouseup/click), bukan SSR grep (Kriteria/Contoh/PJ/Existing = 0 di HTML awal, true setelah klik).
- Server: `PORT=3457 npx next start` di background; **cek port sebelum restart** — orphan `next-server` memegang port → `errno: -48` (lihat section 19).

**5. Alur lanjutan — EKSEKUSI PERBAIKAN DATA (selesai 6 Agu 2026):** 20 markdown hasil ODL dipakai sebagai ground truth untuk memperbaiki `data/modul-indikator.json`. Hasil nyata: 12/20 modul di-rebuild penuh dari markdown (parser label level `Kurang/Initiate (1 < nilai < 1,5)` dst, dengan regex yang menerima `Label (`, `Label(`, dan label nyangkut di heading `...PemerintahDigitalCukup/Emerging(1,5<nilai<2,5)`); 8 modul fallback = cleanup artefak JSON lama (heading `#{2,6}` nyangkut di tengah kalimat → `([^\s#])(\s*)(#{2,6}\s+)` → `\1\n\3`; `<br>` → `\n`; collapse 3+ newline); level yang hilang di-merge dari backup `.bak-odl`; **8 level yang backup-nya juga kosong diisi via manual line-mapping dari markdown** (detail + line-map di `document-content-pipeline` Step 2d). Akhir: **0 level kosong, 0 artefak** di 20 modul. Simpan backup `.bak-odl`/`.bak-odl2` — merge tergantung padanya. Baru setelah data rapi, tampilkan kembali section lain satu per satu (per user).

**6. ⚠️ USER PREFERENCE (6 Agu 2026, dikoreksi 2×) — kriteria level = CARD dalam GRID, bukan tabel dan BUKAN bertumpuk ke bawah**: JCode pernah mengubah render kriteria per level menjadi `<table>` — user menolak eksplisit ("kembalikan ke tampilan card per level"). Versi berikutnya yang bertumpuk vertikal (`flexDirection:column`) JUGA ditolak: "card pada kriteria tidak rapi... harusnya card disusun lebih rapi, bukan disusun ke bawah". Pola yang diterima = **CSS grid responsif**: wrapper `display:'grid'; gridTemplateColumns:'repeat(auto-fill, minmax(340px, 1fr))'; gap:'0.75rem'; alignItems:'start'` → 2-3 kartu per baris di desktop, 1 kolom di layar sempit. Tiap level = kartu `borderRadius:10px; overflow:'hidden'`, `display:'flex'; flexDirection:'column'; height:'100%'` (baris sama tinggi), header `background:${lvColor}12` + badge solid `L{n}` (`background:lvColor; color:'#fff'`) + `LEVEL_LABEL`, body render `formatKriteria()` + `overflowWrap:'break-word'`. Verifikasi horizontal via browser: 3 kartu baris sama harus punya `y` sama dan `x` naik (getBoundingClientRect). Jangan pernah mengubah ke tabel ATAU stacked column tanpa bertanya.

**6b. Deskripsi modul juga wajib render markdown** (dikoreksi 6 Agu 2026): `{modul.deskripsi}` sebagai `<p>` polos menampilkan `- 1. Manajemen Risiko,` dan `#### Dasar Hukum` sebagai teks mentah. Render via `<div className="kriteria-render" dangerouslySetInnerHTML={{__html: formatKriteria(modul.deskripsi)}} />` dalam panel `surface-2` (border-radius 8, padding, border). Berlaku untuk semua modul dengan deskripsi panjang (I2, I13, I15).

### 22. Analisis Sumber Bukti Dukung & Kanonisasi public/bukti-dukung — verified 6 Agu 2026

User bertanya "apakah semua bukti dukung yang ditampilkan punya 1 sumber atau banyak sumber?" lalu minta kumpulkan semua file bukti dari Documents & bersihkan folder yang tidak dipakai. Pola yang terbukti:

**1. Semantik sumber (jangan salah lapor):** 1 bukti = 1 dokumen. Field `url_preview` vs `url_sumber` BUKAN 2 sumber berbeda — itu 2 cara akses dokumen yang sama:
- JDIH: preview = `/download/produk-hukum/<uuid>` (PDF langsung), sumber = `/detail/<uuid>` (halaman). Bandingkan **UUID** (regex `[0-9a-f]{8}-...-{12}`) — sama = dokumen sama. Verified 43/43 UUID sama, 0 beda.
- Lokal: preview = thumbnail PNG (`Capaian_RKPD_preview.png`), sumber = file asli xlsx. Nama file berbagi prefix → dokumen sama.
- Audit script: kumpulkan URL unik per bukti → klasifikasi `tanpa_sumber / satu_sumber / banyak_sumber`; banyak_sumber hanya jika UUID/prefix BERBEDA.

**2. Tiga lapisan penyimpanan sumber:**
| Lapisan | Lokasi | Status |
|---------|--------|--------|
| Lokal (canonical) | `public/bukti-dukung/` (tracked, deploy Vercel) | ✅ aktif |
| Eksternal online | `jdih.acehtengahkab.go.id` (43 bukti, 86 referensi) | ✅ aktif, tak perlu file |
| Arsip asli | `~/Documents/REAL-PEMDI-DATA DUKUNG/`, `odl-pdf bukti dukung/`, `Modul Indikator 1-20/` | sumber awal, tak di-track |

**3. Kanonisasi folder (62 → 20 file):** klasifikasi tiap file `public/bukti-dukung/` vs referensi pemdi.json:
- Referensi lokal (`/bukti-dukung/...`) + referensi raw GitHub (`raw.githubusercontent.com/.../main/public/bukti-dukung/...` → ekstrak path setelah `/main/`) = DIPAKAI.
- Sisanya UNUSED → **pindah ke arsip, jangan hapus permanen**: `archive/bukti-dukung-unused-<tanggal>/` (pertahankan struktur subfolder; 41 file, 28MB — recoverable).
- ⚠️ PITFALL: file yang di-referensikan via `raw.githubusercontent` (mis. `pedoman_pengaduan_rsud.pdf` → V2.I2_4, `skm_kebayakan_2025.pdf` → V1.I20_2) tampak "unused" di audit lokal — WAJIB masukkan refs_raw ke set dipakai, kalau tidak link preview bukti itu putus.
- Verifikasi: audit ulang → 0 MISSING, 0 UNUSED (setelah raw refs); `curl` file tersisa = 200, file diarsip = 404; `npx next build` OK.
- Dokumen yang sama dipakai banyak indikator (Perbup 48/2025 → ~15 indikator) = WAJAR, bukan duplikasi sumber; file cukup 1 copy.

**4. 57 bukti tanpa sumber** = hanya deskripsi, belum ada file fisik (konsisten status `belum`) — ini to-do list pengumpulan, bukan error.

## Pitfalls

- ❌ **Local path assumption**: File di `public/bukti/` (LEGACY, 302MB, gitignored) tidak ter-deploy ke Vercel — it's the dead pre-restrukturisasi folder. File live ada di `public/bukti-dukung/` (tracked, 62 file) atau pakai source URL sebagai `url_preview` fallback. Jangan copy bukti baru ke `public/bukti/` — gunakan `public/bukti-dukung/`.
- ❌ **Level naming dari Excel**: Jangan copas nama level dari Excel — bisa beda dengan PermenPANRB. Validasi dulu ke modul page.
- ❌ **ID mismatch**: `pemdi.json` pakai ID `I1` (tanpa leading zero), tapi bukti dari Arena pakai `I01`. Mapping `pad_indicator()` wajib.
- ❌ **I09 & I12 L2**: Audit keamanan + insiden CSIRT bersifat rahasia. Tandai "Perlu Manual" bukan "Belum".
- ⚠️ **Duplicate files**: Banyak evidence item pakai file yang sama (misal Perbup 48/2025 dipakai untuk ~15 indikator). File hanya perlu di-copy sekali.
- ⚠️ **Excel Eksternal indicator**: I05 (SDI) dan I18 (Interop Data) kadang ditandai "Eksternal" — nilainya otomatis dari sistem nasional. Tapi tetap perlu bukti pendukung untuk verifikasi.
- ⚠️ **pemdi.json berisi duplikasi ID: V1/V2 (legacy) + B (baru)** — verified 4 Aug 2026. `total_item_bukti` di metadata = 57, TAPI `bukti_dukung` di semua aspek berjumlah **114** item: 33 `V1.*` (level 1 lama) + 24 `V2.*` (level 2 lama) + 57 `B*` (baru). V1/V2 = bukti lengkap legacy, B = item baru (umumnya belum). Halaman modul-indikator menampilkan SEMUA (114). **Jangan pakai `total_item_bukti` untuk menghitung total tampil** — hitung dari `len(ind.bukti_dukung)` per indikator. Saat generate ringkasan, tampilkan angka 114 dengan catatan komposisi V1/V2/B.
- ⚠️ **`url_preview` bisa kosong** — bukti dari OpenData kadang hanya punya `url_sumber` tanpa `url_preview`. Saat render link, fallback ke `url_sumber` jika `url_preview` kosong; jangan render link kosong.
- ⚠️ **JANGAN ubah section modul asli saat menambah konten** (preferensi user, 4 Aug 2026): halaman `/modul-indikator` memuat modul asli yang sudah disetujui user. Konten baru (Peta Dokumen Kunci / penjelasan bukti) WAJIB ditambahkan sebagai section terpisah DI BAWAH — bukan modifikasi inline. `modul-indikator.json` & `pemdi.json` tidak boleh diubah strukturnya.
- ⚠️ **File name too long** (5 Aug 2026): `cp` file Documents dengan nama >255 char (mis. judul RKA panjang) gagal dengan `File name too long` — copy ulang dengan nama pendek di `public/bukti-dukung/`.
- ⚠️ **URL file dengan spasi**: nama file public ber-spasi bekerja di browser (auto-encode) tapi `curl` perlu `%20` — HTTP 000 dari curl ≠ file hilang, encode dulu.
- ⚠️ **API route export**: saat menulis ulang `pages/api/*.js`, jangan hilangkan `export default function handler(req,res)` — HTTP 500 "does not export a default function". Cek tail file + `curl -w "%{http_code}"` = 200 sebelum deploy.
- ⚠️ **Komponen class tanpa CSS** (5 Aug 2026): `<button class="scroll-top">` tampil memanjang karena class-nya TIDAK punya definisi CSS sama sekali di globals.css. Sebelum asumsi styling ada, cek `grep -rn "scroll-top" --include="*.css" .` — kalau kosong, tambahkan CSS (fixed 44×44, radius 50%, kanan-bawah, fade-in; jangan lupa `.visible` state + media query mobile).
- ⚠️ **Struktur modul-indikator.json**: top-level keys = `total_modul` + `modules[]` (tiap module: `indikator_id`, `level_kriteria`, `data_dukung_modul`, `rekomendasi`) — BUKAN key `modul`/`data_dukung_modul` di root. Audit/script yang mengasumsikan struktur lama langsung gagal — cek keys dulu dengan `list(json.load(...))`.
- ⚠️ **STATUS_META punya 3 state**: `belum` ⬜ / `proses` 🔄 / `lengkap` ✅ — helper hitung harus filter `b.status === 'lengkap'` untuk nilai, dan UI harus handle 'proses' (bukan hanya 2 state).
- ⚠️ **Test textarea React via browser console**: `ta.value = x` saja tidak memicu onChange React — pakai native setter `Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype,'value').set.call(ta, x)` lalu `dispatchEvent(new Event('input', {bubbles:true}))`.

## Domain Knowledge

### 20 Indikator Pemdi (PermenPANRB 8/2026)

| Indikator | Aspek | L1 Initiate | L2 Emerging |
|-----------|-------|-------------|-------------|
| I01 | Tata Kelola & Manajemen | ✅ Perbup 48/2025 + RPD | ✅ + Reviu Kinerja |
| I02 | Tata Kelola & Manajemen | ✅ Standar Pelayanan + Adminduk | ✅ + RSUD |
| I03 | Penyelenggara | ✅ Literasi Digital + SOTK | ✅ Analisis |
| I04 | Penyelenggara | ✅ Perbup 70/2019 + Arsitektur | ✅ Arsitektur |
| I05 | Data | ✅ Satu Data + SOP | ✅ Satu Data |
| I06 | Data | ✅ Data RDTR | ✅ Data RDTR |
| I07 | Data | ✅ SOP Statistik | ✅ SOP + SDI |
| I08 | Data | ✅ Klasifikasi Arsip + Adminduk | ✅ + PPID |
| I09 | Keamanan | ✅ Pengawasan Kinerja | ❌ RAHASIA |
| I10 | Keamanan | ✅ Klasifikasi + Arsitektur | ✅ Klasifikasi |
| I11 | Keamanan | ✅ Arsitektur | ✅ Arsitektur |
| I12 | Keamanan | ✅ Arsitektur | ❌ RAHASIA |
| I13 | Teknologi | ✅ Arsitektur + SOTK | ✅ Arsitektur |
| I14 | Teknologi | ✅ Arsitektur | ✅ Arsitektur |
| I15 | Keterpaduan | ✅ Arsitektur | ✅ Arsitektur |
| I16 | Keterpaduan | ✅ Arsitektur | ✅ Arsitektur |
| I17 | Keterpaduan | ✅ MPP + Arsitektur | ✅ MPP + Adminduk |
| I18 | Keterpaduan | ✅ Satu Data + Arsitektur | ✅ Satu Data |
| I19 | Kepuasan | ✅ SP4N + Standar | ✅ SP4N + SKM |
| I20 | Kepuasan | ✅ SKM 2026 + Kebayakan | ✅ SKM 2026 |

### Sumber Data Publik untuk Aceh Tengah

| Sumber | URL | Jenis Data |
|--------|-----|------------|
| JDIH | `jdih.acehtengahkab.go.id` | Perbup, regulasi (670+ dokumen) |
| OpenData | `opendata.acehtengahkab.go.id` | Dataset CKAN (862 dataset) |
| CSIRT | `csirt.acehtengahkab.go.id` | Keamanan siber |
| Pemdi Portal | `pemdi-aceh-tengah.vercel.app` | Dashboard Pemdi |
| GitHub | `github.com/Niumination/PemdiAcehTengah` | Repositori publik |

### 23. Audit Excel Daftar Lengkap vs Modul — level naming & sinkronisasi (verified 6 Agu 2026)

Saat user minta "sesuaikan bukti dukung dengan modul (bahasa umum) dulu, lalu dengan Excel Daftar Lengkap (sheet 2, breakdown Aceh Tengah)": Excel = `docs/pemdi-evaluasi-2026/Daftar_Lengkap_Bukti_Dukung_PEMDI_Aceh_Tengah.xlsx` — sheet `02_Daftar_Lengkap_Bukti_Dukung` (177 item: 173 upload manual + 4 eksternal I5/I6/I7/I18). Header sheet 2 di **row 4** (No | No. Ind. | Aspek | Indikator | Level Kematangan | No. Level | Item Bukti Dukung (sesuai modul) | Jenis Output | Bentuk Output Nyata | PJ | Unit Pendukung | Keterangan); data mulai row 5.

**⚠️ Level naming Excel pakai skema LAMA PermenPANRB 59/2020, modul pakai skema BARU 8/2026:**
| Excel (lama) | Modul (baru) |
|---|---|
| Initiate/Kurang | Initiate (L1) |
| Emerging/Cukup | Emerging (L2) |
| **Developing/Baik** | **Established (L3)** |
| **Embedded/Sangat Baik** | **Leading (L4)** |
| **Leading/Memuaskan** | **Transformative (L5)** |

Koreksi di Excel: rename `Developing/Baik`→`Established/Baik`, `Embedded/Sangat Baik`→`Leading/Sangat Baik`, `Leading/Memuaskan`→`Transformative/Memuaskan` di SEMUA sheet (02 col5, 01 catatan #6 + legend, 05 checklist R13 "Initiate → Emerging → Developing", 06 col5 "Developing–Leading"→"Established–Leading", "Embedded & Leading"→"Leading & Transformative"), plus deskripsi "level Developing/Embedded" di col9 → Established/Leading. ⚠️ Jangan global-replace string pendek (`"Developing"` tanpa `/Baik`) — kena kata di teks lain; dan global replace `"Keterpaduan Layanan Digital"` bisa kena **konten item** (bukan hanya kolom aspek) — R15C7 item_modul I1 ikut berubah, harus revert dari backup. Sel R36C1 (catatan 6) resisten terhadap replace bertahap — assign nilai penuh langsung.

**Temuan koreksi lain (semua sudah dieksekusi):**
- **I9 L3↔L4 tertukar**: Excel L3="Tindak Lanjut Audit (internal)", L4="Audit Eksternal" — modul: L3=Eksternal, L4=Tindak lanjut atas audit eksternal. Swap label level kedua baris (R98↔R99 sheet 2).
- **I18 salah**: "Interoperabilitas Data **(Indeks Satu Data Indonesia)**" — suffix itu milik I5; modul I18 = "Tingkat Kematangan Interoperabilitas Data". I6 sheet 2 juga beda dengan sheet 1 ("(Indeks Simpul Jaringan Informasi Geospasial)" vs "(Indeks SJIG)") — seragamkan ke "(Indeks SJIG)".
- **I20**: "Tingkat Kepuasan Pengguna" → modul "Tingkat Kematangan **Pengelolaan** Kepuasan Pengguna".
- **I15-I19**: tambah prefix "Tingkat Kematangan" (sheet 2 col4 + sheet 1 col4).
- **Aspek**: "Keterpaduan Layanan Digital Pemerintah" (Excel) → "Keterpaduan" (modul/pemdi.json) — sheet 1/2/4.

**pemdi.json sinkronisasi (backup dulu):**
- **P1.\* (bukti 2026) semua L1 tapi isinya level lain** — 8 item naik L1→L2: DPA/RKA & RKA (I1 L2 "Perencanaan & Anggaran sebagian substansi"), Undangan/Rapat konsolidasi (I1/I4 L2 "konsolidasi kolaboratif"), Renstra/Renja/RPJMD (I1 L2 "dokumen perencanaan sebagian substansi"), DPA-SKPD 97 hal (I1 L2). SK Tim Koordinasi tetap L1 (I4 L1 "Penetapan Tim").
- **`target_item_bukti` = 177** (bukan 178 — selisih 1 dari aspek Keterpaduan yang tadinya 26): samakan dengan Excel; `aspek.total_item` per aspek = 20/32/38/25/18/25/19 (sum 177). UI modul-indikator & pemdi otomatis baca dari data ("134/177", "Gap: 43").
- Verifikasi: `sum(a.total_item) == target_item_bukti == 177`, level bukti ⊆ level_kriteria modul, `npx next build` 0 error, browser check stat + catatan mandiri per indikator.

⚠️ **Level lama di `docs/modul-indikator/*.md` (hasil ODL) JANGAN diubah** — itu ground-truth mentah dari PDF asli. "178" di `.next/` = build artifacts, regenerated otomatis.

### 24. Kanonisasi Bukti Eksternal → Lokal (preview modal rusak) — verified 6 Agu 2026

User: "bukti dari link eksternal tidak bisa dibuka di preview — download semua bukti eksternal ke public/bukti-dukung, goal semua bukti punya 1 sumber (lokal)."

**Sumber eksternal & cara download (19 dokumen unik):**
- **JDIH (11 PDF)**: `https://jdih.acehtengahkab.go.id/dih/download/produk-hukum/<uuid>` — langsung PDF (6MB-38MB). ⚠️ Download beruntun kena HTTPError transien (rate-limit) — retry per-file dengan delay 0.5-1s; UUID diekstrak dari URL preview/sumber (`[0-9a-f]{8}-...-{12}`), 1 UUID = 1 dokumen walau dipakai banyak bukti (Perbup 48/2025 → 8+ bukti).
- **OpenData (6)**: URL `/dataset/<slug>` = halaman, BUKAN file. Query CKAN API `https://opendata.acehtengahkab.go.id/api/3/action/package_show?id=<slug>` → `result.resources[].url` = file asli. ⚠️ 4 dari 6 resource = **XLSX** (magic `PK\x03\x04`), bukan PDF — simpan dengan ekstensi benar, jangan paksa PDF.
- **raw GitHub (2)**: sudah ada lokal (`public/bukti-dukung/04-layanan/pedoman_pengaduan_rsud.pdf`, `skm_kebayakan_2025.pdf`) — cukup update JSON.

**Lokasi**: `public/bukti-dukung/07-eksternal/` (folder baru). Nama: `jdih-{uuid8}-{slug}.pdf` / `opendata-{tag}-{resource-slug}.{ext}`. Total 129MB — OK untuk GitHub.

**Update `data/pemdi.json`**: semua bukti lengkap (57) — `url_preview` http → path lokal `/bukti-dukung/07-eksternal/...` + `_ext: 'pdf'|'xlsx'` (yang tadinya cuma `url_sumber` http juga dapat preview lokal). `url_sumber` DIPERTAHANKAN sebagai atribusi (bukan "2 sumber" — itu metadata asal, preview/akses = 1 sumber lokal). Verifikasi: 0 url_preview http, 0 bukti lengkap tanpa preview, 0 file hilang.

**Fix kode (2 halaman):**
- `pages/modul-indikator.js` — `toProxyUrl()`: `if (url.startsWith('/')) return url;` (lokal langsung, same-origin bebas XFO) sebelum fallback ke `/api/proxy-pdf?url=...` (proxy tetap untuk URL http masa depan). Tanpa fix ini modal preview nunjuk proxy → "URL tidak diizinkan" (403) karena proxy hanya izinkan jdih.*.
- `pages/pemdi.js` — iframe langsung pakai `url_preview` (tanpa proxy) → otomatis jalan setelah JSON lokal.

**Preview**: PDF (`_ext:'pdf'`) → iframe render (browser PDF viewer); XLSX (`_ext:'xlsx'`) → link "Buka/Unduh" (bukan iframe). Verifikasi di browser: klik 👁️ → iframe src `/bukti-dukung/07-eksternal/...pdf` + `contentDocument.contentType === 'application/pdf'`.

**Screenshot bukti → section "Bukti Dukung Dokumen Pendukung"** (lanjutan, user: "semua bukti dukung dibuatkan dengan metode yang sama & ditambahkan ke section screenshot"):
- PDF (13): PyMuPDF `get_pixmap(dpi=150)` halaman pertama yang mengandung judul (`PERATURAN BUPATI`/`SOP`/`LITERASI`/dll — scan 3 hal pertama) → `public/docs/bukti/{tag}.png` (tag: `perbup-48-arsitektur-spbe`, `perbup-6-sistem-pemdi`, `literasi-digital-2023`, `sop-epss`, `pedoman-pengaduan-rsud`, `skm-kebayakan-2025`, dst).
- XLSX (4): render tabel PNG via PIL (`ImageDraw.rectangle` grid + `ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 18)`, header biru muda, 40 baris max) → `public/docs/bukti/{data-peta-rdtr,hasil-survei-kepuasan,laporan-pengawasan-kinerja,laporan-reviu-kinerja}.png`.
- JSX: array screenshot eksternal (19 item: src/title/desc dengan indikator terkait) ditambahkan sebagai grid kedua di bawah grid dokumen pendukung existing (7 item) — reuse pola yang sama (`setPreviewDoc({url,title})` modal perbesar via iframe — iframe render PNG juga valid). Total 26 screenshot di `public/docs/bukti/`.
- Build + verifikasi browser: scroll bawah → header "Bukti Visual Dokumen Eksternal (JDIH & OpenData)" + 19 kartu; klik → modal iframe src `/docs/bukti/<file>.png`.
