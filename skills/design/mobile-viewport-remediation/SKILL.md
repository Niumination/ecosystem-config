---
name: mobile-viewport-remediation
description: "Use when a page is not mobile-friendly on phones."
tags: [mobile, responsive, reflow, tap-target, ux, audit]
version: 1.0.0
---

# Mobile Viewport Remediation

Untuk kerja "halaman X belum mobile-friendly", "tampilan berantakan di HP", tap target kecil, atau permintaan audit
mobile. Menangani **tata letak**, bukan estetika: ukur → perbaiki akar → ukur lagi.

## Gate dari pemilik (jangan dilanggar)

- **Audit dulu; jangan menambal sambil mengaudit.** Permintaan "temukan kegagalan/bug" = laporan bertingkat
  (severity, angka terukur, `file:line`), lalu **TAHAN eksekusi** sampai pemilik mengklarifikasi atau memilih prioritas.
- **Setelah daftar disetujui, kerjakan seluruh batch dalam satu jalan** — jangan pecah balik jadi pertanyaan per item.
- **Cakupan dipersempit** ("cukup halaman X dulu") → ubah **hanya halaman itu**: pakai kelas pembungkus di JSX
  halaman + scope CSS padanya (CSS tak punya selektor rute). Sisa pekerjaan ditulis sebagai **rencana, bukan
  dieksekusi**: `docs/rencana-<topik>-tahap-<N>.md` berisi baseline terukur, dampak, risiko, urutan, kriteria selesai,
  dan daftar yang **tidak** termasuk.
- **Target pemilik: "ringkas tapi padat informasi".** Konten tidak boleh hilang — pangkas tampilannya (clamp/lipat)
  dan sediakan cara membuka penuh.
- **Laporkan temuan yang dibatalkan sendiri** (false positive + mekanisme salah ukurnya). Pemilik menilai kejujuran
  ini lebih tinggi daripada daftar temuan panjang.
- **Temuan destruktif di repo** (binari byte-identik, cadangan, folder besar, bloat riwayat) dilaporkan sebagai tabel
  temuan·ukuran·rekomendasi lalu berhenti — jangan dihapus sendiri.

## Prosedur

### 1. Ukur (jangan menebak dari kode)
Jalankan `scripts/viewport-audit.py <url> [rute...]` — mengukur tiap rute di 390/360/320px dan mencetak: tinggi
halaman (px + setara layar), lebar **anak elemen kartu pertama**, kontrol <44px, keadaan chip/filter, dan sticky.
Angka "sebelum" wajib dari **produksi**, bukan disimpulkan dari sumber.

### 2. Temukan akar tata letak
- Komponen yang mempertahankan tata letak multi-kolom desktop di viewport sempit. Bukti: anak elemen jauh lebih
  sempit dari kartunya (mis. judul ~89px, deskripsi ~72px ≈ 8 karakter/baris pada kartu ~326px).
- Sisa tinggi halaman: ukur tinggi per blok (`main > *` + `<footer>`) sebelum mengutak-atik jarak; blok yang tidak
  kamu sentuh (footer, seksi duplikat) sering penyumbang terbesar.

### 3. Perbaiki dengan pola yang sudah terbukti
Detail + snippet: `references/reflow-remediation.md`.
- **Kartu → satu kolom** di ≤768px; header jadi baris `flex-wrap` (ikon + blok judul `flex:1 1 auto; min-width:0`
  + status `margin-left:auto`), deskripsi selebar kartu, meta `flex-wrap`.
- **Deskripsi panjang: clamp 2 baris DAN lepas saat dibuka** — tanpa pelepasan, teks yang diminta pengguna tetap terpotong.
- **Deret filter/chip: satu baris dapat digeser** (`flex-wrap:nowrap; overflow-x:auto`) + blok filter
  `position:sticky` di bawah header dengan latar solid.
- **Grid statistik 2×2**, jangan 4 baris (`.grid-4` → `1fr` di ≤576px memakan ~1 layar).
- **Target sentuh ≥44px**: `min-height` tidak berlaku pada `display:inline` (anchor harus `inline-flex` dulu) dan
  selektor elemen kalah spesifisitas dari kelas → enumerasi kelas ber-tinggi eksplisit di blok `@media` yang
  diletakkan **di akhir** berkas CSS; sisipkan `p a { display:inline; min-height:0 }` sebagai pengecualian.

### 4. Verifikasi (wajib, di produksi setelah deploy)
- Ulangi **angka yang sama**: lebar kolom, tinggi halaman, kontrol <44px (target 0), ratio kontras.
- **Buktikan pelepasan state** untuk setiap pemangkasan: klik → atribut state berubah → tinggi teks naik,
  `line-clamp` = `none`.
- **Desktop tidak berubah**: ukur di 1440px; kalau ikut berubah, scope CSS-nya salah.
- **Anchor yang tidak unik mengganti di SEMUA kemunculannya** — verifikasi setiap situs yang berubah berdasarkan
  maknanya (apakah blok itu masih memuat konten hidup?), bukan dari jumlah penggantian yang dilaporkan tool. Untuk
  membuang rujukan aset mati: kosongkan array-nya lalu sembunyikan kontainer yang jadi kosong; jangan menghapus
  rentang JSX besar.

### 5. Tutup
Satu commit gabungan kode + DOX (perbarui DOX terdekat dengan kontrak mobile + angka sebelum/sesudah), push, lalu
verifikasi CI — jangan menyimpulkan dari transcript.

## Pitfall pengukuran (menghasilkan temuan PALSU)
- **Screenshot `fullPage=true` tidak memicu IntersectionObserver** → counter count-up dan section reveal tampak nol.
  Pakai `fullPage=false` untuk menilai tumpang tindih; `fullPage=true` hanya untuk tinggi total.
- **Klik via selektor bisa gagal senyap** pada app React → pakai `element.click()` di dalam `evaluate`.
- **`input.scrollWidth` selalu sepanjang placeholder** → bukan overflow.
- **Widget `position: fixed` tampak menimpa konten** di screenshot full-page; di viewport nyata ia mengambang.
- **Emoji mengabaikan `color` CSS** → jangan dilaporkan sebagai kontras gagal.
- **Latar gradient/`color-mix()`** (sidebar, pita berjalan) membuat hitungan kontras lapor ~1.0 → hitung hanya untuk
  latar solid, sisanya tandai "perlu verifikasi mata".
- **Jangan mengirim form di produksi** untuk menguji validasi (menulis data nyata) — baca kode validasinya.

## Support files
- `scripts/viewport-audit.py` — probe siap pakai (butuh camofox di `127.0.0.1:9377`; kalau belum jalan, start sesuai
  skill `camofox-browser`).
- `references/reflow-remediation.md` — tabel gejala→penyebab→perbaikan + snippet CSS yang terbukti.
