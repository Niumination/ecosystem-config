---
name: mirai-dashboard-maintenance
description: "Use when editing MIRAI dashboard styling or regressions."
domain: ecosystem
subdomain: mirai
tags: [mirai, dashboard, css, html, visual-verification]
version: "1.0"
author: Hermes Agent (Niumination)
last_updated: "2026-11-07"
---

# MIRAI Dashboard Maintenance

## Arsitektur

- **Single file**: `dashboard.html` berisi semua CSS inline (2 style blocks: @font-face + main CSS) dan JS inline.
- **Server**: `mission-control/server/server.py` (Python 3 stdlib, port 8800).
- **LaunchAgent**: `com.mirai.mission-control`.
- **Repo**: `Niumination/mirai` (GitHub).

## Aturan Utama

1. **JANGAN split CSS/JS ke file terpisah** — P5 split (external `dashboard.css` + `dashboard.js`) menyebabkan regresi visual: brace imbalance, stray `</style>`, dark mode override yang menimpa token warna. Revert ke single-file (commit `4f0f27f`).
2. **Verifikasi visual sebelum commit** — gunakan headless Firefox screenshot (`firefox --headless --screenshot`) dan bandingkan pixel distribution. Jangan klaim selesai dari file di disk saja.
3. **CSS inline** — semua aturan CSS harus inline di `dashboard.html`. Jangan buat file CSS eksternal.
4. **Test layout** — sidebar gelap di kiri (260px), konten cream di kanan. Pixel check: x=0-280 cream, x=300+ dark = SALAH (terbalik).
5. **color-scheme** — gunakan `light dark` (bukan `light` saja). Mode `light` saja menyebabkan native form controls render light-mode yang clash dengan sidebar gelap.
6. **Kontras teks** — `--muted-fg` minimum `oklch(0.32 0.02 60)` pada cream background untuk ≥4.5 AA. Jangan gunakan oklch(0.38) atau lebih terang.
7. **Responsive** — wajib 3 breakpoint: 900px (fleet-mosaic 5-col), 768px (tablet: kpis 2-col, topbar stack), 880px (mobile: full stack). Jangan hanya 1 breakpoint.
8. **Aksesibilitas** — `<main>` wajib `role="main"`, toast wajib `aria-live="polite"` + `role="status"`.
9. **Audit class dari dua sumber** — ekstrak class dari `class="…"` di HTML **dan** dari template literal JS (`RENDERERS.*` / `class=\"…\"` di string renderer), lalu bandingkan keduanya dengan selector di blok `<style>`. Class yang hanya ada di template JS (mis. pembungkus hero / aksi tombol) lolos dari grep HTML statis tapi tetap tanpa styling — grep HTML saja tidak cukup.
10. **Screenshot headless ≠ bukti render async** — halaman cockpit dirender via `fetch` setelah load. Screenshot yang diambil sebelum fetch selesai menampilkan shell kosong; tandai `UNCHECKED` dan verifikasi ulang dengan delay / DOM count, jangan klaim halaman kosong sebagai bug.

## Workflow Edit

1. Edit `dashboard.html` langsung.
2. Sync ke `mission-control/web/dashboard.html`.
3. Restart: `launchctl stop com.mirai.mission-control && sleep 2 && launchctl start com.mirai.mission-control`.
4. Screenshot: `firefox --headless --profile /tmp/ff-profile --screenshot /tmp/mirai.png http://127.0.0.1:8800/`.
5. Verifikasi pixel distribution (sidebar dark left, content cream right).
6. Cek curl: `curl -s http://127.0.0.1:8800/ | grep -o 'color-scheme" content="[^"]*"'` → harus `light dark`.
7. Commit + push.

## Pitfalls

- **CSS split regression**: Memecah CSS ke file eksternal menyebabkan brace imbalance dan stray tags. Selalu inline.
- **Dark mode override**: Blok `@media (prefers-color-scheme:dark)` menimpa token `--ink`/`--cream` dan menyebabkan teks tidak terlihat. Hapus dari CSS.
- **color-scheme light only**: `meta color-scheme="light"` menyebabkan native form controls render light-mode yang clash dengan sidebar gelap. Gunakan `light dark`.
- **Topbar alignment**: Gunakan `align-items: center` (bukan `flex-end`) — flex-end menyebabkan elemen topbar tidak sejajar.
- **Font loading**: @font-face inline dengan base64 woff2 (Instrument Serif). Jangan hapus blok ini.
- **Cache**: Server mengirim `Cache-Control: no-cache` untuk HTML. Browser tetap bisa cache — gunakan hard refresh jika perubahan tidak terlihat.
- **Muted text contrast**: `--muted-fg` di bawah oklch(0.32) menyebabkan teks tidak terbaca pada cream background. Minimum oklch(0.32 0.02 60).
- **Undefined class di template JS**: class yang dipakai di string renderer JS tapi tidak didefinisikan di CSS menyebabkan layout pembungkus (hero, actions) kehilangan grid/flex. Audit harus mencakup template literal, bukan hanya markup statis.
- **Headless screenshot sebelum async render selesai**: shell kosong di screenshot bukan bukti halaman rusak — API-nya bisa 200 semua. Verifikasi dengan DOM setelah fetch, atau tandai UNCHECKED.
