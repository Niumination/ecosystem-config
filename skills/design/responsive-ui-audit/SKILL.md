---
name: responsive-ui-audit
description: "Use when auditing or fixing live web UI/UX."
version: 1.0.0
tags: [ui-ux, responsive, mobile, audit, wcag, verification]
---

# Audit UI/UX Live & Perbaikan Responsif

Kelas pekerjaan: pemilik melaporkan halaman web "berantakan / tidak mobile friendly / sulit dipakai di HP",
atau meminta audit UI/UX. Cakupan: tata letak responsif, tap target, kontras, konten bertumpuk, dan
jebakan pengukuran yang menghasilkan temuan palsu.
Alurnya: **ukur dulu → daftar temuan → tahan eksekusi → perbaiki → buktikan dengan angka**.

Melengkapi (bukan menggantikan): `web-accessibility-wcag` (pipeline WCAG/kontras), `pemdi-uiux-refinement`
(animasi & anti-pattern portal Pemdi), `dark-theme-a11y` (fallback token tema gelap).

## Aturan kerja (preferensi pemilik)

1. **Audit dulu, eksekusi belakangan.** Saat diminta "audit", kirim temuan + angka + bukti, lalu **tahan
eksekusi** sampai pemilik menyetujui atau memilih prioritas. Jangan langsung memperbaiki.
2. **Tahap lanjut = rencana tertulis, bukan eksekusi.** Tulis `docs/rencana-<topik>.md` di repo aplikasi,
tandai **RENCANA (belum dieksekusi)**: baseline terukur per halaman, item + dampak + risiko, urutan eksekusi,
kriteria selesai — lalu tunggu. Daftarkan di `docs/AGENTS.md`.
3. **Angka sebelum/sesudah**, bukan kesan: tinggi halaman, lebar kolom, jumlah kontrol <44px, bita HTML,
rasio kontras, plus tangkapan layar viewport.
4. **Tarik kembali temuan sendiri bila alat ukurnya cacat** — sebut mana yang batal dan kenapa. Satu parser
salah bisa memproduksi kesalahan yang sama di puluhan halaman.
5. **Batasi perubahan ke halaman yang diminta.** Aturan global (`.grid-4`, `.service-desc`) di-scope lewat
kelas khusus halaman atau `@media` sempit.
6. **Commit gabungan kode + DOX** pada commit yang sama.

## Urutan pengukuran (lakukan sebelum menebak dari screenshot)

1. Tinggi halaman di **390px dan 320px** + setara layar (`scrollHeight / innerHeight`).
2. **Lebar anak di dalam kartu berulang** — ini yang menemukan tata letak kolom (lihat bawah).
3. Baris chip/tag filter (tinggi + `scrollWidth > clientWidth`).
4. Uji blok `sticky` dengan menggulir, lalu baca rect `top`-nya.
5. Jumlah kontrol <44px (`a, button, select, summary, [role=button]`).
6. Screenshot **viewport** (`fullPage=false`) untuk menilai tumpang tindih nyata.

## Kartu berulang: "bertumpuk/kolom sempit" bukan masalah spasi

Jika isi kartu tampak bertumpuk, hampir selalu kartu masih memakai tata letak multi-kolom desktop di lebar
sempit. Ukur rect anak-anaknya:
```js
const c = document.querySelector('.card');
[...c.children].map(e => Math.round(e.getBoundingClientRect().width));
// anak selebar 60-90px di viewport 390px = tata letak kolom yang harus diturunkan
```
Perbaikan (di dalam `@media (max-width: 768px)`, desktop tidak tersentuh): kartu `display: block`; header
`flex-wrap: wrap` dengan blok judul `flex: 1 1 auto; min-width: 0` dan status `margin-left: auto`; deskripsi
& baris meta `width: auto !important`; meta jadi satu baris `flex-wrap: wrap; gap: 8px`. `!important` sering
perlu karena nilai komponen React berupa inline style.

- **Memangkas tinggi tanpa menghilangkan informasi**: `-webkit-line-clamp: 2` untuk deskripsi di mobile,
  **lepas saat kartu dibuka**: `.card[aria-expanded="true"] .desc { display: block; -webkit-line-clamp: unset; overflow: visible }`.
  Tanpa override ini pengguna yang membuka kartu tetap melihat teks terpotong. Cek dulu apakah komponen
  sudah punya mekanisme `expanded ? penuh : terpangkas` — jangan dobel.
- **Halaman daftar panjang**: chip filter `flex-wrap: nowrap; overflow-x: auto` + `flex: 0 0 auto` pada tag
  (dinding 200px → satu baris 50px); blok filter `position: sticky` di bawah topbar; grid statistik 2×2
  lewat **kelas khusus halaman** (mis. `.halaman-stats`), bukan mengubah grid global.
- **Tap target ≥44px**: `min-height` **tidak berlaku** pada elemen `display: inline` (anchor harus
  `inline-flex` dulu), dan selektor elemen (`button`) **kalah spesifisitas** dari kelas (`.btn.btn-sm` tetap
  42px) — enumerasi kelasnya di blok media **paling akhir** `globals.css`, dengan `p a { display: inline; min-height: 0 }`
  agar tautan naratif tidak ikut membesar.
- **Animasi layout**: `transition: width` → `width: 100%` + `transform: scaleX(p)` + `transform-origin: left`.
  Jangan konversi bila ada label yang diposisikan terhadap lebar bar (mis. `right: -2.5rem`) — label ikut pindah.

Resep lengkap + checklist: `references/mobile-compact-layout.md`.

## Token & kontras: cacat yang paling luput di tema gelap

1. **Token dipakai tapi tidak pernah didefinisikan** — `var(--primary-bg, #e3edff)` dipakai 9x tanpa definisi
   → fallback hardcoded ikut terpakai di **semua** tema: saat tema gelap, baris tabel berlatar biru terang
   dengan teks beige = kontras 1,15, badge emas di atasnya 1,96. Cara aman: definisikan sekali di `:root`
   dengan menunjuk token ramp yang sudah punya nilai per tema (`--primary-bg: var(--primary-50)`), lalu
   verifikasi `getComputedStyle(document.documentElement).getPropertyValue('--primary-bg')` di **kedua** tema.
   `var(--token)` **tanpa** fallback membuat deklarasi dibuang browser (elemen kehilangan latar di semua tema).
2. **Warna teks dipaksa putih di atas warna aksen** — `.btn-primary { color: #fff !important }` aman di tema
   terang (putih di navy) tapi gagal begitu `--primary` menjadi emas di tema gelap (2,31). Override
   ber-scope tema: `[data-theme="dark"] .btn-primary { color: #0B101C !important }`.
3. **Token "light" yang dipakai sebagai warna teks** — `--muted-light` (`#99A2B8`) pada teks 11px di atas
   putih = 2,56. Sebelum menggelapkan token, telusuri dulu pemakaiannya: mengarahkan ulang token teks
   (`--gray-500: var(--muted)`) memperbaiki banyak tempat sekaligus tanpa menyentuh komponen.
4. **Verifikasi di mode gelap juga**, bukan hanya terang: set `data-theme` langsung lewat evaluasi DOM bila
   tombol toggle sulit diklik, lalu ukur `backgroundColor`/`color` elemen terdampak dan hitung rasionya.
5. **Konten internal di halaman publik** (blok rumus/notasi, nomor halaman lampiran) lebih baik dilipat
   `<details>` — halaman jadi lebih pendek dan tetap bisa dibuka yang membutuhkan.

## Temuan PALSU yang paling sering muncul (saring sebelum melapor)

1. **Screenshot `fullPage=true` tidak memicu IntersectionObserver** → counter dan section reveal tampak
   `0`/`opacity:0` padahal normal. Scroll dulu, atau pakai screenshot viewport.
2. **`input.scrollWidth` selalu sepanjang placeholder** → bukan overflow.
3. **Widget `position: fixed`** tampak menimpa konten di screenshot full-page; di viewport nyata ia mengambang.
4. **Latar gradient / `color-mix`** membuat hitungan kontras lapor ~1,0. Sintaks modern
   `color(srgb 1 1 1 / 0.88)` dibaca regex `[\d.]+` sebagai `rgb(1,1,1)` nyaris hitam → satu bar salah parse
   bisa melaporkan "kontras 1,17" di **semua** halaman. Ambil nilai dari aturan CSS-nya, atau tandai
   "perlu verifikasi mata"; hitung kontras hanya bila latar efektif `rgb()` solid.
5. **Emoji mengabaikan `color` CSS** → bukan kegagalan kontras.
6. **`getComputedStyle(e).transform` mengembalikan `matrix(...)`**, bukan `scaleX(...)`. Cari via atribut
   inline (`getAttribute('style').includes('scaleX')`) lalu bandingkan lebar rect dengan lebar induk.
7. **Kelas tidak ditemukan ≠ komponen rusak**: periksa apakah komponennya memang dipasang di halaman itu.
8. **Tombol `disabled`**: klik pada tombol yang memang disabled tidak menghasilkan apa-apa — baca kode
   (`disabled={!valid}`, `required`, handler error) sebelum melapor "validasi form tidak ada".
9. **Klik selektor di browser bisa gagal senyap** — pakai `element.click()` lewat evaluasi DOM sebelum
   menyimpulkan fitur/toggle rusak.

Aturan turunannya: **temuan tanpa bukti yang bisa diulang bukan temuan** — sertakan bukti, atau tandai
"belum terkonfirmasi".

## Verifikasi & suntingan massal

- **Suntingan massal dengan anchor fuzzy**: `patch`/replace bisa cocok di beberapa tempat sekaligus. Bila
  maksudnya menghapus/menyembunyikan blok berulang, verifikasi **setiap** blok setelah suntingan (hitung
  entri hidup di dalamnya) sebelum commit — pernah satu anchor cocok 2x dan salah satunya masih memuat
  konten hidup. Pola aman: hapus baris entri mati lalu pastikan grep sisa referensi = 0, bukan menyembunyikan
  wadahnya.
- **Jangan uji form di produksi**: submit bisa menulis data nyata. Uji validasi dengan membaca kode.
- **Gate sebelum commit**: build/lint/test repo hijau + ukur ulang di produksi setelah deploy (jangan klaim
  dari build lokal saja).
- **Efek samping yang wajar**: tinggi halaman bisa tidak banyak turun setelah kartu diturunkan jadi satu
  kolom — sebelumnya kartu "pendek" justru karena isinya terjepit. Laporkan keterbacaan dan tinggi keduanya.
