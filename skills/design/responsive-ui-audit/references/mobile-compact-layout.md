# Resep: Tata Letak Mobile Ringkas

Pola yang terbukti saat memadatkan halaman daftar/dashboard untuk layar sempit. Semua intervensi dibatasi
`@media (max-width: 768px)` supaya tata letak desktop tidak berubah.

## Urutan kerja

1. Ukur tinggi halaman di 390px **dan** 320px (320px sering lebih buruk).
2. Ukur lebar anak di dalam kartu berulang (menemukan tata letak kolom).
3. Ukur baris chip/tag filter (tinggi + `scrollWidth > clientWidth`).
4. Uji `sticky` dengan menggulir, lalu baca rect `top`.
5. Hitung kontrol <44px.
6. Screenshot viewport untuk menilai tumpang tindih nyata.

## Baseline pembanding (viewport 390px)

- Halaman daftar sehat: **~8.000-9.000px** untuk puluhan item.
- Beranda panjang yang sudah dipadatkan: **~10 layar**.
- Daftar >15 layar biasanya karena (a) kartu multi-kolom, (b) semua blok terbuka, (c) footer belum dipadatkan.

## Pola CSS

### 1. Kartu berulang → satu kolom
```css
@media (max-width: 768px) {
  .card { display: block; padding: 14px !important; }
  .card > div:first-child { display: flex; flex-wrap: wrap; align-items: flex-start; gap: 10px; margin-bottom: 8px; }
  .card > div:first-child > div:nth-child(2) { flex: 1 1 auto; min-width: 0; }   /* blok judul */
  .card > div:first-child > span { margin-left: auto; }                           /* status/badge */
  .card-desc { width: auto !important; margin: 6px 0 10px !important; }
  .card > div:last-child { display: flex; flex-wrap: wrap; align-items: center; gap: 8px; width: auto !important; }
}
```

### 2. Batas baris yang dilepas saat kartu dibuka
```css
@media (max-width: 768px) {
  .card-desc { display: -webkit-box; -webkit-line-clamp: 2; line-clamp: 2;
               -webkit-box-orient: vertical; overflow: hidden; }
  .card[aria-expanded="true"] .card-desc {
    display: block; -webkit-line-clamp: unset; line-clamp: unset; overflow: visible;
  }
}
```

### 3. Chip filter jadi satu baris yang bisa digeser
```css
@media (max-width: 768px) {
  .tags { flex-wrap: nowrap !important; overflow-x: auto; -webkit-overflow-scrolling: touch; padding-bottom: 6px; }
  .tags > * { flex: 0 0 auto; white-space: nowrap; }
}
```

### 4. Blok filter melekat di bawah topbar
```css
@media (max-width: 768px) {
  .filter-bar {
    position: sticky;
    top: calc(var(--gov-strip-h, 36px) + env(safe-area-inset-top, 0px) + 61px);
    z-index: 30; background: var(--bg); padding: 6px 0;
  }
}
```

### 5. Grid statistik 2×2 khusus satu halaman
```css
@media (max-width: 768px) {
  .halaman-stats { grid-template-columns: repeat(2, minmax(0, 1fr)) !important; }
  .halaman-stats > * { padding: 0.75rem 0.6rem !important; }
}
```
Kelas ditambahkan di JSX halaman (`<div className="grid grid-4 halaman-stats">`) agar halaman lain yang
memakai `.grid-4` tidak ikut berubah.

### 6. Tap target ≥44px (pola menyeluruh)
```css
@media (max-width: 768px) {
  a, button, [role="button"], select, summary, input[type="submit"] {
    min-height: 44px; display: inline-flex; align-items: center;
  }
  p a { display: inline; min-height: 0; }              /* tautan naratif tetap inline */
  .btn, .btn-sm, .btn.btn-sm, .hbtn, .link-more { min-height: 44px; }  /* kelas ber-tinggi eksplisit */
  .icon-btn { min-width: 44px; justify-content: center; }
}
```

### 7. Hentikan animasi dekoratif di layar sempit
```css
@media (max-width: 768px) {
  .marquee-track { animation: none !important; transform: none !important; }
  .marquee { overflow-x: auto; }
}
```

## Snippet pengukuran (via browser `evaluate`)

```js
// lebar anak kartu
const c = document.querySelector('.card');
[...c.children].map(e => Math.round(e.getBoundingClientRect().width));

// chip: satu baris atau dinding?
const box = document.querySelector('.tags').parentElement;
({ tinggi: Math.round(box.getBoundingClientRect().height),
   bisaDigeser: box.scrollWidth > box.clientWidth, wrap: getComputedStyle(box).flexWrap });

// sticky: scroll dulu, baru baca
window.scrollTo(0, 1800);
document.querySelector('.filter-bar').getBoundingClientRect().top;

// clamp lepas saat dibuka
const card = document.querySelector('.card'); card.click();
setTimeout(() => getComputedStyle(card.querySelector('.card-desc')).webkitLineClamp, 500);

// kontrol <44px
[...document.querySelectorAll('a,button,select,summary,[role=button]')]
  .filter(e => { const r = e.getBoundingClientRect(); return r.width > 0 && r.height > 0 && r.height < 44; }).length;
```

## Checklist sebelum melapor

1. Tinggi halaman + tinggi kartu rata-rata di 390px dan 320px.
2. Lebar judul/deskripsi/meta ≈ lebar kartu.
3. Kontrol <44px = 0 di 390px.
4. Desktop tidak berubah (ukur ulang di 1440px).
5. Kartu dibuka → teks penuh (`line-clamp: unset`), `aria-expanded` true.
6. Filter tetap terjangkau setelah menggulir ~2 layar.
7. Build/lint/test hijau; ukur ulang di produksi setelah deploy.
8. Screenshot viewport sebagai bukti.
