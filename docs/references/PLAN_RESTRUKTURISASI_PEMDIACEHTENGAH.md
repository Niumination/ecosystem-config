# Rencana Restrukturisasi Portal PemdiAcehTengah

> **Berdasarkan:** Panduan Peningkatan Indeks Pemdi Aceh Tengah ✅, PermenPANRB 8/2026 ✅, Laporan SPBE 2025 Aceh Tengah ✅
> **Tujuan:** Portal yang ringkas, padat, berbobot — data akurat 100%, desain konsisten, detail via panel/pop-up

---

## 🎯 Visi Restrukturisasi

**"Progressive disclosure" — Tiap halaman cukup tunjukkan esensi. Detail bisa di-klik, jangan ditumpuk."**

Prinsip:
1. **Ringkas di permukaan** — judul, angka kunci, visualisasi langsung terbaca
2. **Bobot di klik** — detail kebijakan, data mentah, penjelasan panjang melalui modal/panel
3. **Konsisten** — semua halaman pakai template layout yang sama
4. **Akurat 100%** — setiap angka bersumber dari dokumen resmi (SPBE 2025, PermenPANRB 8/2026, Panduan)

---

## 📊 GAP ANALYSIS — Dokumen vs Website Saat Ini

### A. DATA TIDAK AKURAT di `pemdi.json`

| Indikator | Website (Lama) | Dokumen Panduan | Sumber | Tindakan |
|-----------|---------------|-----------------|--------|----------|
| **Aspek 1** Tata Kelola & Manajemen | 1.85 | **1.5** | Panduan §4 | → Turunkan ke 1.5 |
| **Aspek 2** Penyelenggara / SDM | 1.65 | **2.5** | Panduan §4 (Tim Koord nilai 3) | → Naikkan ke 2.0 |
| **Aspek 3** Data | 1.50 | **1.5-2.0** | Panduan §4 | → 1.75 (rata-rata) |
| **Aspek 4** Keamanan Pemdi | 1.25 | **1.0** | Panduan §4 (baseline 1.0) | → 1.0 |
| **Aspek 5** Teknologi Pemdi | 1.85 | **1.0** | Panduan §4 (Pembangunan Apl 1.00) | → Turunkan ke 1.0 |
| **Aspek 6** Keterpaduan Layanan | 1.88 | **2.5** | Panduan §4 (modal bagus) | → Naikkan ke 2.5 |
| **Aspek 7** Kepuasan Pengguna | **1.0** | **3.5** 🚨 | Panduan §1 (Layanan 3.75) | → **3.5** (koreksi besar!) |

**Catatan:** Aspek 7 (Kepuasan) adalah kesalahan kritis — website mencatat 1.0, padahal dokumen SPBE 2025 menunjukkan Layanan Administrasi 3.80 dan Layanan Publik 3.67. Portal ini SENDIRI adalah bukti digital yang sudah live.

### B. SPBE 2025 — Indikator Detail

Dari dokumen resmi Laporan SPBE 2025 Aceh Tengah (47 indikator), berikut yang belum tercantum di website:

|# Indikator SPBE|Nilai|Butuh di Website?|
|---|----|----------------|
|1. Arsitektur SPBE (kebijakan)|2|✅ Ada di konteks|
|2. Peta Rencana (kebijakan)|2|⬜ Perlu ditambahkan|
|3. Manajemen Data (kebijakan)|**4**|✅ Pintar|
|4. Pembangunan Aplikasi (kebijakan)|**1**|✅ Ada|
|5. Layanan Pusat Data (kebijakan)|2|⬜ Perlu|
|6. Layanan Jaringan Intra (kebijakan)|**3**|⬜ Perlu|
|... dan seterusnya 47 indikator |||
|**Layanan Publik Sektor 1-3**|**4, 4, 4**|✅ Modal utama|

### C. Gap Design/UX

|Issue|Contoh|Solusi|
|-----|------|------|
|❌ Teks panjang inline|8 Misi dengan deskripan full, 47 baris indikator|→ Card ringkas + "Lihat Detail" modal|
|❌ Tidak ada pop-up/panel|Detail SPBE, indikator terpaksa scroll panjang|→ Modal universal untuk detail|
|❌ Tidak konsisten|/pemdi vs /probis vs /layanan beda layout|→ Template hero + section + card konsisten|
|❌ Info overload di homepage|Hero stats + SPBE gauge + rekomendasi + daftar OPD|→ Homepage sebagai dashboard eksekutif|
|❌ Data mentah tidak tersaring|/pemdi page menampilkan I1-I20 mentah|→ Kategorisasi + ringkasan interaktif|

---

## 🏛️ DESAIN SISTEM BARU

### Komponen Baru yang Dibutuhkan

#### 1. `DetailModal` — Modal Universal
```
Fungsi: Menampilkan detail apa pun (indikator, misi, OPD, dokumen)
Trigger: Klik card / tombol "Lihat Detail"
Props: title, content (nodes/data), source, onClose
Perilaku: Scrollable, close-on-backdrop, ESC close, animasi fade-in
```

#### 2. `ExpandablePanel` — Panel Lipat
```
Fungsi: Untuk teks yang cukup panjang tapi bukan modal penuh
Perilaku: Accordion style, inline expand tanpa navigasi
Props: title, children, defaultOpen (false), icon
Gunakan di: Deskripsi OPD, FAQ di /pemdi, detail probis
```

#### 3. `DataBadge` — Badge Indikator Ringkas
```
Fungsi: Nilai + status dalam satu baris
Props: label, value, target, warna, href (optional untuk ke modal)
Ukuran: compact (di card) atau large (di hero)
```

#### 4. `DetailPageLayout` — Template Halaman Konsisten
```
Layout:
  <section-hero-xxx>
    container → back-link, badge, h1, p, CTA
  </section-hero-xxx>
  <section class="section">
    container → content (cards, grid, dll)
  </section>
```

### Pola Interaksi Baru

```
[Card Ringkas] → Klik → [Modal Detail]
[Badge Indikator] → Klik → [ExpandablePanel penjelasan]
[Item Daftar Panjang] → Klik → [Modal dengan tabel/data]
```

---

## 📋 RESTRUKTURISASI PER HALAMAN

### 1. Halaman Index (`/`) — Dashboard Eksekutif

**Sekarang:** Hero + SPBE Gauge + Proses Bisnis + Daftar OPD + Rekomendasi → **terlalu panjang**

**Baru:**
- Hero → ✅ Dipertahankan (statistik ringkas sudah pas)
- ✅ Gauge SPBE (2.59) — dipertahankan di `#spbe` section
- **Card navigasi cepat** — grid 4 card besar: Pemdi, PPB, Layanan, SKM
- **Daftar OPD** — jangan ditampilkan semua; cukup **50 OPD dalam grid ringkas + filter/search + klik buka modal detail**
- **Rekomendasi** — jangan inline; cukup 3 prioritas dengan "Selengkapnya → /pemdi"

### 2. Halaman PPB (`/probis`) — Peta Proses Bisnis

**Sekarang:** Hero + 3-level chain + 8 Misi + 24 Urusan + 37 Proses + Regulasi → **semua inline, teks panjang**

**Baru:**
- ✅ Hero — dipertahankan
- ✅ Chain 3-level — dipertahankan
- **Level 0 (Visi & Misi)** — 8 Misi dalam **card ringkas**:
  ```
  | Misi 1 | Misi 2 | Misi 3 | Misi 4 |
  | Nama singkat | ... | ... | ... |
  | [Detail]      |     |     |     |
  ```
  Nama misi saja di card. Klik "Detail" → Modal tampilkan deskripsi lengkap + fokus strategis + OPD
- **Level 1 (24 Urusan)** — Grid 6×4 atau list dengan badge nilai:
  ```
  [Urusan Wajib 1] ● ● ○ 12 OPD  [Detail]
  ```
  Klik Detail → Modal tampilkan OPD pelaksana, kebijakan terkait
- **Level 2 (Proses Bisnis)** — 6 kategori dengan jumlah proses:
  ```
  | Perencanaan (6 proses) | Keuangan (5) | Kepegawaian (4) |
  | Pengadaan (3) | Pengawasan (4) | Pelayanan (15) |
  ```
  Klik kategori → Modal tampilkan daftar proses + OPD terkait

### 3. Halaman Pemdi (`/pemdi`) — Indeks Pemerintah Digital

**Sekarang:** Hero + Radar + Score Ring + 7 Aspek × 20 Indikator inline → **semua indikator ditampilkan mentah**

**Baru:**
- ✅ Hero dengan score ring — dipertahankan, tapi tambahkan badge "SPBE 2.59" sebagai pembanding
- ✅ Radar chart — dipertahankan (visualisasi bagus)
- **7 Aspek Cards** — setiap aspek jadi card ringkas:
  ```
  ┌─────────────────────────────────────┐
  │ [icon] Tata Kelola & Manajemen      │ 10%
  │ Nilai: 1.5 ●●●○○  Target: 2.5 ○○○○○│
  │ Gap: 1.0   ━━━━━━━━━━━━━━━━━━━      │
  │ 2 Indikator: I1 (2.0), I2 (1.7)    │
  │ [Lihat Detail Indikator]            │
  └─────────────────────────────────────┘
  ```
- Klik "Lihat Detail Indikator" → **Modal** tampilkan full detail I1–I2
- Hapus daftar indikator inline panjang
- **Bottom section:** Ringkasan road map / rekomendasi dalam card kecil

### 4. Halaman Layanan (`/layanan`) — Direktori Layanan

**Sekarang:** 27 layanan dalam card dengan status badge — **cukup baik, tapi deskripsi inline**

**Baru:**
- ✅ Hero — dipertahankan
- ✅ Filter kategori + search — dipertahankan
- **Card layanan lebih ringkas:**
  ```
  | Izin Mendirikan Bangunan | ⚡ Online |
  | DISPUPR                  | [Daftar] [Detail] |
  ```
  Klik "Detail" → Modal dengan alur layanan, syarat, biaya, waktu, link
- **Tambah:** Badge status layanan di pojok card (Online/Offline/Hybrid)

### 5. Halaman SKM (`/skm`) — Survei Kepuasan Masyarakat

**Sekarang:** Form 3-step + dimensi SKM

**Baru:**
- ✅ Hero + form 3-step — dipertahankan
- **Tambah:** Dashboard ringkas 8 dimensi SKM dengan nilai (data dari Panduan)
- Klik dimensi → Modal tampilkan penjelasan + hasil survei

### 6. Halaman FAQ (`/faq`) — Tanya Jawab

**Sekarang:** Accordion 4 kategori — **sudah cukup baik**

**Minor:**
- Tambahkan kategori "Pemdi & SPBE" (indeks, evaluasi, target)

---

## 🔧 DATA ACCURACY UPDATES

### Update `data/pemdi.json`

```json
{
  "tentang": "Indeks Pemerintah Digital (Indeks Pemdi) — PermenPANRB 8/2026",
  "tahun": 2026,
  "target_indeks": 2.5,
  "target_predikat": "Baik",
  "baseline_spbe": 2.59,
  "baseline_predikat": "Cukup",
  "catatan": "Nilai baseline Pemdi adalah estimasi berdasarkan konversi dari data SPBE 2025 (Laporan Resmi KemenPANRB Jan 2026) dan Panduan Peningkatan Indeks Pemdi Aceh Tengah (Diskominfo, Juni 2026). Sumber data: 47 indikator SPBE 2025 + 20 indikator Pemdi PermenPANRB 8/2026.",
  "aspek": [
    {
      "id": 1,
      "nama": "Tata Kelola & Manajemen",
      "bobot": 10,
      "nilai": 1.5,
      "target": 2.5,
      "indikator": [
        {"id": "I1", "nama": "Tata Kelola Pemdi", "nilai": 1.5, "target": 2.5, "sumber": "Arsitektur SPBE 1.00 + Peta Rencana 1.00 (SPBE 2025)"},
        {"id": "I2", "nama": "Manajemen Layanan Digital", "nilai": 1.5, "target": 2.5, "sumber": "Manajemen Risiko 1.00 + Manajemen Layanan 1.00 (SPBE 2025)"}
      ]
    },
    {
      "id": 2,
      "nama": "Penyelenggara",
      "bobot": 10,
      "nilai": 2.0,
      "target": 2.5,
      "indikator": [
        {"id": "I3", "nama": "SDM Pemdi", "nilai": 1.5, "target": 2.5, "sumber": "Kompetensi SDM 1.00 (SPBE 2025)"},
        {"id": "I4", "nama": "Kolaborasi Pemdi", "nilai": 2.5, "target": 2.5, "sumber": "Tim Koordinasi 3.00 + Kolaborasi 3.00 (SPBE 2025)"}
      ]
    },
    {
      "id": 3,
      "nama": "Data",
      "bobot": 15,
      "nilai": 1.75,
      "target": 2.5,
      "indikator": [
        {"id": "I5", "nama": "Tata Kelola Data", "nilai": 2.0, "target": 2.5, "sumber": "Manajemen Data (kebijakan) 4.00 (SPBE 2025)"},
        {"id": "I6", "nama": "Informasi Geospasial", "nilai": 1.5, "target": 2.0, "sumber": "Estimasi — dataset BIG belum aktif"},
        {"id": "I7", "nama": "Statistik Sektoral", "nilai": 1.5, "target": 2.0, "sumber": "Estimasi — perlu koordinasi BPS (EPSS)"},
        {"id": "I8", "nama": "Pelindungan Data Pribadi", "nilai": 1.0, "target": 2.0, "sumber": "Indikator baru — belum diterapkan"}
      ]
    },
    {"id": 4, "nama": "Keamanan Pemdi", "bobot": 15, "nilai": 1.0,
      "target": 2.5, "indikator": []},
    {"id": 5, "nama": "Teknologi Pemdi", "bobot": 10, "nilai": 1.0,
      "target": 2.5, "indikator": []},
    {"id": 6, "nama": "Keterpaduan Layanan", "bobot": 15, "nilai": 2.5,
      "target": 2.5, "indikator": []},
    {"id": 7, "nama": "Kepuasan Pengguna", "bobot": 25, "nilai": 3.5,
      "target": 3.0, "indikator": []}
  ]
}
```

---

## 🗓️ TAHAPAN IMPLEMENTASI

### Fase 1: Fondasi — Komponen & Data ⏰ 1 hari
- [ ] 1.1 Buat komponen `DetailModal` (universal, reusable)
- [ ] 1.2 Buat komponen `ExpandablePanel`
- [ ] 1.3 Buat komponen `DataBadge` (nilai + progress bar)
- [ ] 1.4 Update `data/pemdi.json` dengan nilai akurat dari dokumen
- [ ] 1.5 Buat `STRATEGI_PEMDIACEHTENGAH.md` baru dengan data SPBE 2025 lengkap

### Fase 2: Restrukturisasi Halaman ⏰ 2 hari
- [ ] 2.1 Restruktur `/pemdi` — 7 aspek cards + modal detail indikator
- [ ] 2.2 Restruktur `/probis` — misi cards + modal detail misi/urusan/proses
- [ ] 2.3 Restruktur `/` — navigasi cepat, ringkas, eksekutif
- [ ] 2.4 Update `/layanan` — card ringkas + modal layanan detail
- [ ] 2.5 Update `/skm` — dashboard SKM + modal penjelasan

### Fase 3: Polish & Data ⏰ 1 hari
- [ ] 3.1 Integrasi SPBE 2025 indicator breakdown (47 indikator) di modal
- [ ] 3.2 Tambah data 24 urusan + 37 proses bisnis di halaman PPB
- [ ] 3.3 CSS polish — spacing, typography, mobile
- [ ] 3.4 Build & deploy Vercel

### Fase 4: Lanjutan (Post-Deploy) ⏰ Bertahap
- [ ] 4.1 Integrasi data real SPBE 2025 per OPD
- [ ] 4.2 Dashboard SKM real-time (Google Data Studio embed)
- [ ] 4.3 Pencarian global lintas halaman
- [ ] 4.4 SLA badge dinamis

---

## 🧠 PRINSIP DESAIN

### Typography
```
Heading h1: 1.75rem, weight 700, tracking -0.02em
Heading h2: 1.375rem, weight 600
Heading h3: 1rem, weight 600
Body: 0.9375rem, line-height 1.6
Small: 0.8125rem, color var(--muted)
```

### Warna Pemerintah (Konsisten)
```
Primary: #1d70b8 (biru GOV.UK)
Primary dark: #003078
Success: #00703c
Warning: #e65100
Danger: #d4351c
Neutral: #f3f2f1 (bg), #505a5f (text muted)
```

### Spacing
```
Section padding: 2.5rem 0
Card padding: 1rem
Grid gap: 1rem-1.5rem
Container max-width: 960px
```

---

## 📁 FILE YANG AKAN BERUBAH

| File | Perubahan |
|------|-----------|
| `data/pemdi.json` | ✏️ Koreksi total — 7 aspek × 20 indikator |
| `components/DetailModal.js` | 🆕 Komponen modal universal |
| `components/ExpandablePanel.js` | 🆕 Panel lipat untuk penjelasan |
| `components/DataBadge.js` | 🆕 Badge ringkas indikator |
| `pages/pemdi.js` | ✏️ Restruktur besar — cards + modal |
| `pages/probis.js` | ✏️ Restruktur sedang — misi/urusan/proses cards + modal |
| `pages/index.js` | ✏️ Restruktur ringan — navigasi cepat |
| `pages/layanan.js` | ✏️ Update card + modal detail |
| `pages/skm.js` | ✏️ Tambah dashboard SKM |
| `pages/faq.js` | ✏️ Tambah kategori Pemdi & SPBE |
| `styles/globals.css` | ✏️ Tambah utility card modal |

---

## ✅ VERIFIKASI

Setelah implementasi, pastikan:
- [ ] Build Next.js sukses (59/59 halaman)
- [ ] Setiap halaman punya hero + back-link
- [ ] Tidak ada teks panjang inline — semua detail via modal/panel
- [ ] Nilai Indeks Pemdi akurat: 7 aspek sesuai Panduan
- [ ] Data SPBE 2025 bisa diakses (modal atau halaman terpisah)
- [ ] Mobile responsive — modal tetap nyaman di layar kecil
- [ ] Deploy ke Vercel
- [ ] Update BACKLOG.md

---

*Dokumen ini disusun berdasarkan analisis 3 dokumen resmi + audit kode portal PemdiAcehTengah.*
*Disimpan di: ~/Desktop/Niumination/archive/PLAN_RESTRUKTURISASI_PEMDIACEHTENGAH.md*
