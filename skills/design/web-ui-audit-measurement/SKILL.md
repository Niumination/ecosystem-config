---
name: web-ui-audit-measurement
description: "Audit live web UI dengan bukti terukur."
version: 1.0.0
metadata:
  hermes:
    tags: [ui-ux, audit, accessibility, measurement, frontend, qa]
    related_skills: [dogfood, web-accessibility-wcag, impeccable]
---

# Audit UI/UX web dengan bukti terukur

Kelas tugas: menilai UI/UX aplikasi web yang SUDAH berjalan (produksi atau lokal) dan
melaporkan temuan yang bisa dipertanggungjawabkan. Mencakup audit kontras, tap target,
overflow/terpotong, payload, dan noise kosmetik lintas viewport.

Fokus skill ini adalah **validitas pengukuran** — bukan alur QA eksploratif (itu di
`dogfood`) dan bukan remediasi WCAG terperinci (itu di `web-accessibility-wcag`).
Pakai ini saat hasil ukuran akan dijadikan dasar keputusan perbaikan.

Aturan inti: satu angka tidak cukup, dan angka yang salah lebih merusak daripada tidak
ada angka. Setiap temuan harus lolos filter anti-false-positive di bawah sebelum masuk
laporan.

## 1. Ukur dulu, jangan menyentuh apa pun

Sapu rute × viewport; untuk tiap kombinasi kumpulkan sekaligus:

| Dimensi | Ambang / cara baca |
|---|---|
| Kontras teks | AA: ≥4,5 normal, ≥3 untuk ≥24px atau ≥18,66px bold |
| Tap target | ≥44px (Apple HIG) / 48dp (Material); hitung yang <44px, target 0 |
| Overflow horizontal | `documentElement.scrollWidth > innerWidth + 1` |
| Konten terpotong | `overflow: hidden` + `scrollWidth > clientWidth` (+6px) |
| Tinggi halaman | `body.scrollHeight / innerHeight` = berapa layar |
| Payload | ukuran HTML + `__NEXT_DATA__` (pada SSG) |
| Konsol | error/warn per halaman setelah interaksi |
| Noise | jumlah emoji dalam teks, jumlah input, animasi berjalan |

Viewport minimum: 390 (mobile), 768 (tablet), 1440 (desktop). Tambah 320 kalau menguji
reflow (WCAG 1.4.10).

Template probe siap pakai: `templates/page-probe.js` — satu IIFE untuk dijalankan di
konteks halaman. Salin dan sesuaikan, jangan tulis ulang dari nol.

## 2. Filter anti-false-positive (WAJIB)

Tiap butir di bawah pernah menghasilkan temuan palsu yang menyita waktu; pakai sebagai
gate sebelum melapor.

- **Kontras hanya valid di latar SOLID.** Latar dari `background-image`, gradient, atau
`color-mix()` tidak bisa dihitung dari nilai CSS-nya → tandai "perlu verifikasi mata".
- **Ambil warna dari `getComputedStyle().color`** (selalu `rgb()/rgba()`). Jangan parse
string mentah dengan `[\d.]+`: `color(srgb 1 1 1 / 0.88)` terbaca sebagai `rgb(1,1,1)`
→ puluhan "kontras 1,0" palsu di seluruh halaman.
- **Emoji mengabaikan `color` CSS** → bukan kegagalan kontras.
- **`offsetParent !== null` selalu false untuk `position: fixed`** → probe "elemen
mengambang" melaporkan 0 padahal widget-nya ada. Uji `getComputedStyle().position`.
- **`input.scrollWidth` selalu sepanjang placeholder-nya** → bukan overflow.
- **Screenshot `fullPage` tidak memicu IntersectionObserver** → counter angka dan
section reveal tampak `0`/`opacity:0` padahal normal. Scroll dulu, atau pakai
screenshot viewport.
- **Widget `position: fixed` tampak menimpa konten** di screenshot full-page; di
viewport nyata ia mengambang. Menilai tumpang tindih → `fullPage=false`.
- **Metrik berubah setelah font termuat** → elemen bisa tampak terpotong pada ukuran
pertama. Scroll, tunggu, ukur ulang sebelum menyimpulkan.
- **Teks sewarna latar bisa berarti dekoratif** (watermark, motif, SVG background) →
periksa apakah elemennya memang teks berarti.

## 3. Uji interaksi lewat DOM, bukan selektor klik

Klik berbasis selektor bisa gagal senyap lalu berubah jadi kesimpulan "fitur rusak".
Pakai `element.click()`; untuk input React, native value setter + event:

```js
const set = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value').set;
set.call(input, 'kata');
input.dispatchEvent(new Event('input', { bubbles: true }));
```

Kalau tombol tidak bereaksi, **cek dulu apakah ia `disabled`** — sering "tidak jalan"
itu perilaku benar (guard form). Baca kode (`disabled={...}`, `required`, handler error)
sebelum menyimpulkan fungsionalitas hilang.

## 4. Akar kegagalan yang berulang saat memperbaiki

- **Tap target**: `min-height` tidak berlaku pada `display: inline` → anchor/nav harus
`inline-flex` dulu. Selektor elemen kalah spesifisitas dari kelas (`.btn.btn-sm` tetap
42px walau ada `button { min-height: 44px }`) → enumerasi kelasnya di blok
`@media (max-width: 768px)` **di akhir** berkas CSS, plus `p a { display: inline;
min-height: 0 }` agar tautan naratif tidak ikut membesar.
- **Token dipakai tapi tak pernah didefinisikan** (`var(--x)` banyak pemakaian, 0
definisi) → fallback hardcoded-nya aktif di SEMUA tema. Definisikan sekali sebagai
`var(tokenLain)` yang sudah punya nilai per tema. `var(--x)` **tanpa** fallback membuat
seluruh deklarasi dibuang tanpa error di konsol.
- **Tema gelap yang membalik token**: bila tema gelap mengganti token ke warna terang,
setiap `color:#fff !important` di atasnya gagal (putih di atas emas = 2,31) → rule
ber-scope `[data-theme="dark"] .kelas { color: ... !important }`; selektor atribut
menang spesifisitas dan `!important` tetap perlu untuk mengalahkan `!important` lama.
- **`transition: width` → `transform: scaleX()` tidak selalu aman**: periksa dulu apakah
ada label/sibling yang posisinya beranker pada lebar bar (mis. `right: -2.5rem` di dalam
fill). Kalau ada, biarkan animasinya dan tulis alasannya.
- **Jangan tambah sistem animasi kedua** — cek dulu apakah halaman sudah punya mekanisme
reveal sendiri.

## 5. Edit massal: anchor belum tentu unik

Saat membersihkan atau menyembunyikan banyak blok dengan penggantian string:

1. Tegakkan **jumlah kemunculan yang diharapkan** sebelum menulis — anchor yang cocok di
>1 tempat mengubah semuanya tanpa peringatan.
2. Setelah menulis, **verifikasi isi tiap titik**, bukan cuma jumlahnya. Contoh nyata:
anchor komentar + `<div>` yang sama muncul di dua blok template, sehingga blok yang masih
berisi 4 gambar hidup ikut disembunyikan — tertangkap hanya karena tiap titik diperiksa
isinya.
3. Blok yang dianggap kosong harus dibuktikan kosong secara programatik (hitung entri
array di dalamnya) sebelum disembunyikan.

## 6. Payload & render

- Pada SSG (mis. Next.js Pages Router) hasil `getStaticProps` ditanam ke
`__NEXT_DATA__` di setiap HTML. Ukur **total dan `__NEXT_DATA__`** — total saja
menyembunyikan dari mana beratnya datang. Ukur dari hasil prerender lokal sebelum
deploy, lalu konfirmasi ukurannya di produksi.
- Rampingkan dengan mengirim hanya field yang benar-benar dibaca halaman: cari
pemakaiannya (`grep -n 'namaProp\.'`), jangan menebak dari nama prop.
- Halaman yang datanya dirender **sekaligus dihidrasi** (akordeon, filter, kalkulator)
membutuhkan datanya di klien → jangan dipangkas sebagai patch kecil; laporkan sebagai
item tersendiri.
- Bar ber-`transform: scaleX(p)`: baca tiga angka bersama — `offsetWidth` (layout),
`getBoundingClientRect().width` (visual, sudah termasuk transform), dan lebar induk.
Rasio visual/induk harus sama dengan nilai `p`.

## 7. Disiplin bukti & format laporan

- **Ukur sebelum dan sesudah**, tampilkan pasangan angkanya. Klaim "sudah diperbaiki"
tanpa pasangan sebelum→sesudah tidak diterima.
- **Cabut temuan palsu secara eksplisit** bila probe ternyata cacat, sebut mekanismenya.
Temuan palsu yang dibiarkan lebih merusak daripada temuan yang hilang.
- **Produksi = data nyata.** Jangan submit form, jangan tekan aksi destruktif. Uji
validasi dengan membaca kode.
- Bahasa Indonesia, langsung ke inti, tanpa emoji. Pisahkan **temuan terkonfirmasi** dari
**daftar yang dibatalkan**; cantumkan file:baris dan nilai terukur.
- Tutup dengan seksi `## Bukti` berisi keluaran mentah (perintah + angka), lalu lampirkan
screenshot sebagai `MEDIA:<path>` (viewport untuk tumpang tindih, full-page untuk konteks).
- Sebutkan apa yang **sengaja tidak** diubah beserta alasannya (kontrol dengan cakupan
berbeda, label yang beranker pada lebar bar, payload yang butuh refactor).
- Jangan hapus fungsi demi kosmetik: kontrol yang tampak mirip bisa punya cakupan berbeda.
Untuk halaman padat, lipat blok internal dengan `<details>` native (keyboard-accessible;
`<summary>` ikut `min-height: 44px`) daripada menghapusnya.

## 8. Kalau sesi browser bawaan tidak bisa attach

Cek konfigurasi sesi browser dulu (`browser.camofox.user_id`/`session_key` yang kosong
menghasilkan URL relatif dan error seperti `Invalid URL '/tabs'`). Jalur alternatif yang
setara, dan lebih praktis untuk memproses puluhan rute sekaligus: endpoint REST browser
headless lokal (camofox `127.0.0.1:9377`) — `POST /tabs` → `POST /tabs/:id/viewport` →
`POST /tabs/:id/navigate` → `POST /tabs/:id/evaluate` (ekspresi yang mengembalikan JSON) →
screenshot lewat `GET /tabs/:id/screenshot?userId=..&fullPage=true|false` (PNG mentah,
GET + query — bukan body POST) → bersihkan dengan `DELETE /sessions/:userId`.
