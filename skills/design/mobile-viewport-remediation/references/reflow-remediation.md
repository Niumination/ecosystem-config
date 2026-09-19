# Reflow remediation — gejala, penyebab, snippet

Angka di tabel adalah **magnitudo contoh** yang terukur pada viewport 390px; ukur ulang untuk kasusmu.

## Tabel gejala → penyebab → perbaikan

| Gejala terukur | Penyebab | Perbaikan (≤768px) |
|---|---|---|
| Judul ~89px, deskripsi ~72px pada kartu ~326px; isi tampak bertumpuk | Kartu mempertahankan baris flex multi-kolom desktop | Kartu `display:block`; header `flex-wrap`; blok judul `flex:1 1 auto; min-width:0`; status `margin-left:auto` |
| Deskripsi 6–8 baris per item (ratusan px) | Teks penuh dirender di daftar | Clamp 2 baris + **lepas** pada `[aria-expanded="true"]` |
| Deret chip setinggi 200–356px | `flex-wrap: wrap` di kontainer chip | Kontainer `flex-wrap:nowrap; overflow-x:auto`; chip `flex:0 0 auto; white-space:nowrap` |
| Filter tak terjangkau setelah menggulir 2 layar | Blok filter statis | Filter `position:sticky` di bawah header + latar `var(--bg)` |
| 4 kartu statistik jadi 4 baris | `.grid-4` jatuh ke `1fr` di ≤576px | 2×2 lewat **kelas halaman** khusus |
| Kontrol setinggi 14–30px | `min-height` tak berlaku pada `display:inline`; kelas kalah spesifisitas | Anchor `inline-flex` dulu; enumerasi kelas ber-tinggi eksplisit di akhir berkas CSS |
| Halaman makin panjang saat layar menyempit | Grid kolom → 1 kolom, padding tetap | Turunkan padding di ≤768px; pindahkan blok duplikat ke lipatan |

## Snippet yang terbukti

```css
@media (max-width: 768px) {
  /* Kartu: satu kolom, header membungkus */
  .card { display: block; padding: 14px; }
  .card > .head { display: flex; flex-wrap: wrap; align-items: flex-start; gap: 10px; margin-bottom: 8px; }
  .card > .head > .title-block { flex: 1 1 auto; min-width: 0; }
  .card > .head > .status { margin-left: auto; }
  .card > .desc { width: auto; margin: 6px 0 10px; }
  .card > .meta { display: flex; flex-wrap: wrap; align-items: center; gap: 8px; width: auto; }

  /* Deskripsi: clamp, dan lepas saat kartu dibuka */
  .card .desc {
    display: -webkit-box; -webkit-line-clamp: 2; line-clamp: 2;
    -webkit-box-orient: vertical; overflow: hidden;
  }
  .card[aria-expanded="true"] .desc {
    display: block; -webkit-line-clamp: unset; line-clamp: unset; overflow: visible;
  }

  /* Filter: satu baris bergeser, melekat di bawah header */
  .tags { flex-wrap: nowrap; overflow-x: auto; -webkit-overflow-scrolling: touch; }
  .tags > .tag { flex: 0 0 auto; white-space: nowrap; }
  .filter-block {
    position: sticky;
    top: calc(var(--header-strip-h, 36px) + env(safe-area-inset-top, 0px) + 61px);
    z-index: 30; background: var(--bg);
  }

  /* Target sentuh: anchor harus inline-flex lebih dulu */
  a, button, select, summary { min-height: 44px; display: inline-flex; align-items: center; }
  p a { display: inline; min-height: 0; }                    /* tautan naratif tidak ikut membesar */
  .btn, .btn-sm, .btn.btn-sm, .tag { min-height: 44px; }      /* kelas ber-tinggi eksplisit */

  /* Grid statistik halaman ini saja */
  .page-stats { grid-template-columns: repeat(2, minmax(0, 1fr)) !important; }
}
```

## Panel yang bisa dilipat (ringkas tanpa kehilangan informasi)

Untuk blok panjang atau teknis (notasi rumus, daftar panjang, kolom footer) gunakan native `<details>` —
accessible, keyboard, tanpa JS:

```css
.collapse-sec > summary.collapse-sum {
  cursor: pointer; list-style: none; min-height: 44px; padding: 10px 14px;
  background: var(--surface-2); border: 1px solid var(--line); border-radius: var(--r-sm); font-weight: 700;
}
.collapse-sec > summary.collapse-sum::-webkit-details-marker { display: none; }
.collapse-sec > summary.collapse-sum::after { content: '▾'; margin-left: auto; transition: transform .2s ease; }
.collapse-sec[open] > summary.collapse-sum::after { transform: rotate(180deg); }
```

## Probe yang dipakai (potongan penting)

```js
// lebar anak-anak kartu — pembeda antara "masalah spasi" dan "tata letak desktop di layar sempit"
(() => [...document.querySelector('.card').children].map(e => {
  const r = e.getBoundingClientRect();
  return { el: e.tagName + '.' + e.className.split(/\s+/)[0],
           w: Math.round(r.width), h: Math.round(r.height), disp: getComputedStyle(e).display };
}))()

// tinggi per blok (ke mana tinggi halaman pergi)
(() => [...document.querySelector('main').children]
  .map(e => ({ el: e.tagName + '.' + e.className.split(/\s+/)[0], h: Math.round(e.getBoundingClientRect().height) }))
  .filter(o => o.h > 60))()

// apakah filter benar-benar melekat setelah menggulir
(() => { window.scrollTo(0, 1800);
  const f = document.querySelector('.filter-block');
  return JSON.stringify({ pos: getComputedStyle(f).position, top: Math.round(f.getBoundingClientRect().top) }); })()

// pelepasan clamp saat kartu dibuka
(() => { const c = document.querySelector('.card'); c.click();
  return new Promise(r => setTimeout(() => { const d = c.querySelector('.desc');
    r(JSON.stringify({ aria: c.getAttribute('aria-expanded'),
                       h: Math.round(d.getBoundingClientRect().height),
                       clamp: getComputedStyle(d).webkitLineClamp })); }, 500)); })()
```
