# Uiverse.io — Mencari & Menggunakan Elemen untuk Animasi

> **Sumber:** https://uiverse.io/elements — 4.400+ elemen UI open-source (CSS & Tailwind).
> Resource untuk command `animate` / `delight` / `bolder` — KANDIDAT BAHAN, bukan hasil akhir.

## Kapan pakai

- Butuh micro-interaction siap pakai: **button, toggle, checkbox, spinner/loader, card hover, input focus, menu, slider, switch**.
- Butuh efek spesifik yang hemat waktu: neon glow, glassmorphism, gradient border, 3D tilt, neumorphism, particle/confetti, text reveal.
- Prototyping cepat: tempel elemen untuk menguji feel sebelum menulis dari nol.

JANGAN pakai untuk: seluruh halaman/template utuh (gaya asing tak terkontrol), komponen yang harus persis mengikuti design tokens project, atau saat elemen punya animasi dekoratif yang melanggar Reduce Motion.

## Cara mencari elemen yang TEPAT

1. **Tentukan kebutuhan dulu** — elemen apa + animasi apa:
   - Toggle/switch → cari `toggle`, `switch`, `checkbox`
   - Loading → `spinner`, `loader`, `progress`, `skeleton`
   - Button → `button`, `neon`, `gradient`, `3d`, `hover`
   - Card/panel → `card`, `glass`, `glow`
   - Efek teks → `text`, `typewriter`, `reveal`, `shimmer`
2. **Gunakan filter di /elements**:
   - **Tailwind vs CSS** — pilih sesuai stack project
   - **Category** — neumorphism, 3D, gradient, dsb.
   - **Sort** — popular / newest / random
3. **Baca preview** — pastikan animasi = yang dicari (bukan sekadar tampilan statis).
4. **Klik "Get code"** — salin HTML/CSS dari halaman detail elemen.

## Workflow adaptasi (WAJIB)

Copy-paste mentah = gaya asing nyangkut di project. Adaptasi dulu:

```
1. TEMPEL: salin HTML + CSS elemen ke project
2. TOKENS: ganti semua warna hardcoded → design tokens project
   (ganti hex langsung: #8B5CF6 → var(--brand-violet), dll.)
   Ganti font → var(--font-*), radius → var(--radius-*)
3. TIMING: sesuaikan duration/easing dengan motion language project
   (lihat timing table di reference/animate.md)
4. AKSESIBILITAS:
   - Animasi loop: wajib berhenti saat offscreen / prefers-reduced-motion
   - @media (prefers-reduced-motion: reduce) { * { animation: none !important; } }
   - State focus: :focus-visible tetap terlihat
5. VERIFIKASI: cek di browser — hover, click, keyboard, mobile
```

## Pitfall

- **Copy mentah** = elemen asing (warna/font/radius beda) → selalu adaptasi ke tokens.
- **Banyak elemen pakai pseudo-element & keyframes kompleks** — pastikan tidak bentrok dengan class project (prefixed class).
- **Lisensi**: open-source (mayoritas MIT-style), tapi cek halaman elemen; atribusi bila diminta.
- **Kinerja**: hindari elemen dengan `filter: blur` / `box-shadow` besar yang di-animasi terus-menerus di banyak tempat — bound ke area kecil, `will-change` saat animasi saja.
- **Motion dekoratif murni** (spinner hias, confetti terus-menerus) = animation debt — pakai hanya untuk state yang bermakna (loading, success, dsb.).
- **Gaya trendi (neumorphism/3D)**: hanya jika sesuai visual world project — jangan paksa masuk ke design yang restrained.

## Contoh pemakaian yang benar

| Kebutuhan | Cari di uiverse | Adaptasi |
|---|---|---|
| Toggle dark mode dashboard | `toggle switch` | warna → tokens, durasi 200ms |
| Spinner saat agent bekerja | `loader spinner` | ukuran → tokens, stop saat offscreen |
| Hover glow pada card KPI | `card glow hover` | blur bounded, focus-visible |
| Progress bar context window | `progress gradient` | fill → var(--brand-*), animasi width 400ms |

## Referensi

- Katalog: https://uiverse.io/elements
- Filter kategori: https://uiverse.io/elements (dropdown Category di UI)
- Design pack (palet/tipografi/komponen): https://uiverse.io/design
