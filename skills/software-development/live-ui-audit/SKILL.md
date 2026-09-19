---
name: live-ui-audit
description: "Use when auditing a live web UI on mobile and desktop."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    tags: [ui-ux, audit, mobile, accessibility, measurement, verification]
    related_skills: [derived-artifact-consistency, plan-compliance-audit]
---

# Audit UI/UX Halaman Live

Audit tampilan pada halaman yang **sudah deploy**, lalu buktikan perbaikannya di produksi. Prinsip tunggal:
**ukur, jangan menilai** — dari kode, dari ingatan, atau dari kesan atas tangkapan layar.

## Trigger

- "audit UI/UX", "cek tampilan di HP", "berantakan / terpotong / tumpang tindih", "susah dipencet", "kontras"
- Sesudah deploy perubahan tampilan: buktikan efeknya di produksi, jangan menyimpulkan dari kode
- Sebelum menyusun rencana perbaikan UI: kumpulkan angka dasar per halaman lebih dulu

## Urutan kerja

1. **Kumpulkan angka dasar** untuk setiap rute pada tiga lebar: 390 (ponsel), 768 (tablet), 1440 (desktop).
   Minimal: tinggi halaman (dalam satuan layar), jumlah kontrol interaktif <44px, overflow horizontal, ukuran
   HTML dan data inline yang dikirim ke klien.
2. **Ukur anatomi sebelum beropini.** Untuk setiap kartu/baris yang dicurigai, catat `display`, arah flex, dan
   **lebar tiap anak** — bukan hanya wadahnya. Lebar blok teks <120px pada viewport 390px = kolom terjepit.
3. **Perbaiki hanya di blok media query** (`@media (max-width: 768px)`). Tata letak desktop tidak boleh berubah;
   bila perlu pengecualian per halaman, beri kelas khusus halaman alih-alih mengubah kelas generik.
4. **Build → deploy → ukur ulang di produksi.** Angka sesudah perbaikan wajib berasal dari halaman live.
5. **Buktikan tidak ada regresi**: overflow horizontal, kontrol <44px = 0, dan lebar kolom anak.
6. **Laporkan dengan angka sebelum → sesudah** plus tangkapan layar viewport, dan sebutkan apa yang
   **sengaja tidak diubah** beserta alasannya.

## Ambang yang dipakai

| Properti | Ambang |
|---|---|
| Target sentuh | ≥44px (Apple HIG) / 48dp (Material) di layar ≤768px |
| Overflow horizontal | `documentElement.scrollWidth == innerWidth` |
| Konten terpotong | elemen `overflow: hidden` dengan `scrollWidth/scrollHeight` lebih besar dari kotaknya |
| Kontras teks | WCAG AA: 4,5 (teks normal) / 3,0 (besar) — hanya dihitung pada latar **solid** |
| Panjang halaman | laporkan dalam satuan layar, bukan hanya piksel |

## Akar "tampilan rusak di ponsel" yang paling sering

**Tata letak desktop dipertahankan pada lebar ponsel.** Kartu yang di desktop berupa baris multi-kolom
(`display:flex; flex-direction:row`) tetap multi-kolom di 390px → judul terjepek, deskripsi menjadi kolom ~70px
(≈8 karakter per baris), badge sempit. Dari mata pengguna ini terbaca sebagai teks tumpang tindih.

Perbaikan di `@media (max-width: 768px)`:
- wadah kartu → satu kolom (`display: block`), header membungkus, blok judul `flex: 1 1 auto; min-width: 0`
- deskripsi di-clamp 2 baris, **dan clamp dilepas saat kartu dibuka**
  (`.kartu[aria-expanded="true"] .desc { -webkit-line-clamp: unset; display: block }`) — tanpa ini teks penuh yang
  diminta pengguna tetap tersembunyi
- daftar panjang: chip filter jadi satu baris yang digeser (`flex-wrap: nowrap` + `overflow-x: auto`), blok filter
  `position: sticky` di bawah topbar, dan panel/notasi internal dilipat dengan `<details>` native

## Jebakan pengukuran yang menghasilkan temuan PALSU

Semua ini pernah lolos ke laporan sebagai "temuan" padahal bukan cacat:

- **Tangkapan `fullPage` tidak memicu IntersectionObserver** → counter animasi dan elemen reveal tampak `0` /
  `opacity:0` padahal normal. Scroll dulu, atau pakai tangkapan viewport.
- **`input.scrollWidth` selalu sepanjang placeholder** → bukan overflow.
- **Widget `position: fixed`** tampak menimpa konten di tangkapan full-page; di viewport nyata ia mengambang.
- **Latar gradient** (sidebar, hero, strip berjalan) membuat hitungan kontras lapor ≈1,0, dan sintaks warna modern
  `color(srgb 1 1 1 / 0.88)` terbaca sebagai rgb(1,1,1) oleh parser angka naif. Tandai "perlu verifikasi mata".
- **Emoji mengabaikan `color` CSS** → bukan masalah kontras.
- **Klaim atribut JSX** (`rel=`, `aria-*`) harus dari DOM ter-render; grep satu baris melewatkan JSX multi-baris.
- **Interaksi diuji lewat `element.click()` dari evaluate**, bukan klik berbasis selektor — selektor bisa tidak kena
  dan membuat fitur yang normal terlihat rusak.

## Pitfall

- **Perbaikan ukuran gagal karena dua hal**: `min-height` tidak berlaku pada `display: inline` (jadikan
  `inline-flex` dulu), dan selektor elemen kalah spesifisitas dari kelas — enumerasi kelas yang punya tinggi
  eksplisit di akhir berkas.
- **Anchor template berulang**: halaman yang dirender dari template punya komentar/penanda JSX identik, sehingga
  satu anchor bisa cocok N kali dan menyembunyikan blok yang masih hidup. Hitung isi tiap wadah sebelum commit
  dan simpan hitungan regresi untuk blok yang harus tetap tampil.
- **Jangan menguji form di produksi** — submit live menulis data nyata. Uji validasi dengan membaca kode
  (`required`, handler error) atau di lingkungan lokal.
- **Jangan menurunkan ambang agar laporan terlihat hijau.** Bila sisa temuan marginal (mis. 42px vs 44px),
  sebutkan angkanya dan alasannya, jangan dibulatkan menjadi lulus.

## Verifikasi

- [ ] Angka sebelum/sesudah per halaman, dari halaman live
- [ ] Kontrol <44px = 0 pada beberapa halaman sekaligus (bukan hanya halaman yang diperbaiki)
- [ ] Tidak ada overflow horizontal; desktop (1440px) tidak berubah
- [ ] Empat jebakan temuan palsu diperiksa sebelum melaporkan
- [ ] Bukti: build/CI hijau, lint bersih, tes suite lulus
- [ ] Pemilik menerima tangkapan layar viewport + daftar yang sengaja tidak diubah

Resep pengukuran lengkap (protokol browser via REST, skrip per halaman, tabel verifikasi per jenis perbaikan):
`references/measurement-recipes.md`.

Untuk pemeriksa yang melaporkan "bersih": pastikan ia bisa MERAH lebih dulu — lihat `derived-artifact-consistency`.
