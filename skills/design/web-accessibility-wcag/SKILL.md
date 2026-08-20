---
name: web-accessibility-wcag
description: "Audit & remediasi aksesibilitas web WCAG 2.1 AA + polish frontend + SEO untuk dashboard/SPA. Use when user minta audit a11y, WCAG compliance, kontras warna, focus/keyboard navigation, ARIA, dark glassmorphism accessibility, meta/SEO tags, atau heading structure — terutama pada dashboard Mission Control, portal Pemdi, atau HTML/CSS/JS vanilla."
tags:
  - accessibility
  - wcag
  - a11y
  - frontend
  - seo
  - dashboard
last_updated: "2026-08-17"
version: 1.0.0
---

# ♿ Web Accessibility (WCAG 2.1 AA) + Frontend Polish + SEO Pipeline

Pipeline 3-tahap yang terbukti pada dashboard Mission Control (HTML/CSS/JS vanilla, dark glassmorphism, floating window manager).

## Tahap 1 — Audit (sebelum menyentuh apa pun)

1. **Inventory**: heading (`<h1..h6>`), elemen interaktif (button/a/div-role), form, img
2. **Focus**: grep `outline: none` — setiap kemunculan WAJIB punya pasangan `:focus-visible` (WCAG 2.4.7)
3. **Kontras**: hitung ratio semua token warna vs background (script: `scripts/wcag-contrast.py`) — AA: teks normal ≥4.5, teks besar ≥3, UI/ikon ≥3
4. **Keyboard**: cek Enter/Space pada div[role=button], Escape, fokus pindah saat dialog/window dibuka (WCAG 2.1.1, 2.4.3)
5. **ARIA**: role dialog/toolbar/nav, aria-label pada tombol ikon-only, aria-hidden dekoratif, aria-pressed toggle
6. **Heading**: harus ada tepat satu `<h1>` → hierarki 1→2→3 logis (SEO + screen reader)

## Tahap 2 — Remediasi (pola yang terbukti)

### Focus ring dark theme
```css
:focus { outline: none; }
:focus-visible {
  outline: 2px solid #00f0ff !important;
  outline-offset: 2px !important;
  box-shadow: 0 0 0 4px rgba(0, 240, 255, 0.18) !important;
}
```

### ARIA untuk floating window manager (JS-created)
```js
win.setAttribute('role', 'dialog');
win.setAttribute('aria-label', cfg.title);
win.tabIndex = -1;
// saat dibuka via keyboard:
if (document.activeElement === srcBtn) win.focus();
// tombol: <button aria-label="Minimize X"><i aria-hidden="true"></i></button>
// launcher toggle: aria-pressed true/false di-sync open/close
```

### Keyboard pada div[role=button]
```js
btn.addEventListener('keydown', e => {
  if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); toggle(); }
});
```

### Kontras
- Hitung dulu, pilih warna yang lolos (lihat script). Contoh fix nyata: `--text-muted` #64748b (4.21 FAIL) → #7c8ba0 (6.06 PASS)
- **Pitfall kritis**: ganti var root BELUM cukup — grep semua fallback hardcoded `var(--t3, #64748b)` di seluruh CSS (6 tempat lolos saat root diganti). `search_files` + `replace_all`.

### Reduced motion (WCAG 2.3.3)
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation-duration: 0.01ms !important; animation-iteration-count: 1 !important; transition-duration: 0.01ms !important; }
}
```

### SEO untuk dashboard internal
- `<meta name="robots" content="noindex, nofollow">` (internal), description, theme-color, color-scheme, OG (type/title/description/locale)
- `<h1 class="visually-hidden">` untuk hierarki tanpa merusak visual; `<nav aria-label>`, `<main>`
- `.visually-hidden` = absolute 1px clip pattern

### Responsive (tanpa regresi window manager)
- Grid stats-strip/footer: `repeat(5,1fr)` → @768 `repeat(2,1fr)` → @480 `1fr`
- Touch target fwin-act ≥34px @480; jangan ubah `.fwin` sizing utama (mobile: `width: calc(100vw-20px) !important` sudah ada)

## Tahap 3 — Verifikasi (wajib, bukan klaim)

1. **Accessibility tree**: `browser_navigate` → snapshot harus menampilkan heading H1, `navigation`, `main`, `toolbar` dengan button berlabel (bukan generic div kosong)
2. **Kontras computed aktual** (browser console): ambil `getComputedStyle` elemen nyata + ancestor background — jangan cuma hitung token; glassmorphism = hitung terhadap bg dasar
3. **Keyboard end-to-end**: dispatch KeyboardEvent Enter/Space/Escape, cek window terbuka/tutup + aria-pressed berubah
4. **Console**: 0 js_errors
5. **Regresi**: pytest milik proyek tetap pass; route HTTP 200; window cascade masih non-overlap

## Pitfall

- **`resizeTo()` tidak berfungsi di headless browser** — viewport tetap. Verifikasi responsivitas via parse CSS media queries (braces balance + rules per breakpoint), bukan resize.
- **JS di dalam f-string Python** (build_unified.py): kurung tunggal `{` `}` dalam JS HARUS di-escape `{{` `}}`; error `f-string: invalid syntax` di line function definition = brace terlewat. Validasi dengan `node -e "new Function(...)"` setelah build.
- **Kontras glassmorphism**: bg card `rgba(22,32,54,.85)` atas `#050811` = gabungan; hitung terhadap warna dasar, bukan token card saja.
- **Grep pattern diawali `--`** (mis. `--t3`) gagal di rg (dianggap flag) — pakai `search_files` dengan pattern berisi `var\(--t3` atau `-e`.

## Referensi

- `scripts/wcag-contrast.py` — kalkulator kontras WCAG (relative luminance, grade A/AA/AAA)
