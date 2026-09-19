# Resep pengukuran audit live

Perkakas untuk mengukur halaman produksi dan membuktikan hasil perbaikan.

## 1. Menjalankan browser untuk audit

Audit dijalankan lewat REST camofox (`127.0.0.1:9377`, header `Authorization: Bearer hermes-camofox-2026`). Jalur ini
memberi tab/viewport paralel dan tidak bergantung pada kondisi UI satu tool browser.

```
POST   /tabs                {userId, sessionKey, url}      → {tabId}
POST   /tabs/:id/viewport   {userId, width, height}
POST   /tabs/:id/navigate   {userId, url}
POST   /tabs/:id/evaluate   {userId, expression}           → {result}
GET    /tabs/:id/screenshot?userId=..&fullPage=true|false  → PNG mentah (GET + query, bukan POST body)
GET    /tabs/:id/snapshot?userId=..                        → accessibility tree (ref e1, e2, …)
DELETE /sessions/:userId                                   → tutup semua tab user
```

Pakai `userId` unik per run dan selalu tutup dengan `DELETE /sessions/:userId`. `evaluate` mengembalikan `{result}`,
dan `result` sering berupa **string JSON** — parse di sisi pemanggil, jangan menganggapnya dict.

## 2. Daftar periksa per halaman × viewport

```js
(() => {
  const de = document.documentElement, vw = innerWidth;
  const small = [...document.querySelectorAll('a,button,select,summary,[role=button]')]
    .filter(e => { const r = e.getBoundingClientRect(); return r.width > 0 && r.height > 0 && r.height < 44; });
  return JSON.stringify({
    vw, scrollW: de.scrollWidth, hOverflow: de.scrollWidth > vw + 1,
    tinggi: document.body.scrollHeight, layar: Math.round(document.body.scrollHeight / innerHeight),
    kontrolKecil: small.length,
    contoh: small.slice(0, 8).map(e => e.tagName + '.' + (e.className || '').toString().split(/\s+/)[0]
      + ' ' + Math.round(e.getBoundingClientRect().height) + 'px'),
  });
})()
```

## 3. Anatomi kartu — ukur sebelum menata ulang

```js
(() => {
  const c = document.querySelector('.service-card'), cr = c.getBoundingClientRect();
  return JSON.stringify({ wadah: Math.round(cr.width), display: getComputedStyle(c).display,
    arah: getComputedStyle(c).flexDirection,
    anak: [...c.children].map(e => ({ el: e.tagName + '.' + (e.className || '').toString().split(/\s+/)[0],
      w: Math.round(e.getBoundingClientRect().width), h: Math.round(e.getBoundingClientRect().height) })) });
})()
```

## 4. Tabel verifikasi per jenis perbaikan

| Yang diperbaiki | Cara membuktikan |
|---|---|
| Target sentuh | jumlah kontrol <44px = **0** di beberapa halaman sekaligus |
| Tata letak kartu | lebar judul/deskripsi/meta sesudah; `display` wadah = satu kolom |
| Clamp teks | `aria-expanded` false→true, tinggi deskripsi bertambah, `line-clamp: none` |
| Filter dapat digeser | `flexWrap: nowrap` dan `scrollWidth > clientWidth` pada wadah chip |
| Filter melekat | setelah `scrollTo(0, 1800)`, `getBoundingClientRect().top` wadah ≈ nilai `top` sticky |
| Grid statistik | `gridTemplateColumns` menghasilkan 2 kolom, bukan 1 |
| Animasi transform | bandingkan `offsetWidth` (layout) vs `getBoundingClientRect().width` (visual) — rasionya = nilai `scaleX` |
| Panel terlipat | `<details>` ada, `open === false`, tinggi halaman turun |
| Berat halaman | panjang HTML + ukuran `__NEXT_DATA__` sebelum/sesudah |

## 5. Kontras: hitung hanya di latar solid

Telusuri leluhur sampai menemukan `backgroundColor` opak; bila salah satu leluhur punya `background-image`
(gradient), tandai **perlu verifikasi mata** dan jangan laporkan sebagai temuan. Hitung rasio WCAG dari komponen
luminance relatif, lalu bandingkan dengan ambang menurut ukuran/bobot teks (3,0 untuk teks besar, 4,5 selain itu).

Token yang dipakai tetapi tidak pernah didefinisikan di `:root` (mis. `--primary-bg` dengan fallback hardcoded)
` membuat nilai fallback ikut terpakai di **semua** tema — periksa lebih dulu:

```js
getComputedStyle(document.documentElement).getPropertyValue('--token').trim() || '(TIDAK TERDEFINISI)'
```

## 6. Tema gelap

Ukur tanpa mengubah preferensi tersimpan: `document.documentElement.setAttribute('data-theme','dark')` di dalam
`evaluate`. Untuk menguji togglenya sendiri, klik lewat DOM lalu periksa `dataset.theme` dan token `--bg` berubah.

## 7. Bukti visual

Simpan tangkapan **viewport** (`fullPage=false`) pada lebar ponsel sebelum dan sesudah, plus satu tangkapan mode
gelap bila ada tema gelap. Tangkapan full-page tetap berguna untuk melihat panjang halaman, tetapi jangan dipakai
menilai tumpang tindih.
