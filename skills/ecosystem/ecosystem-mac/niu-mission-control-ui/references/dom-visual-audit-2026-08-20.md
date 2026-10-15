# DOM-Based Frontend Audit (tanpa vision model, 20 Ags 2026)

Recipe memverifikasi dashboard MC (atau SPA lain) secara visual-objektif **tanpa** `browser_vision`/
screenshot — dipakai saat auxiliary vision model down (`503 model_not_found`). Hasil = angka DOM
yang bisa dibandingkan antar sesi.

## Kapan dipakai

- Vision auxiliary gagal (`browser_vision` → 503 / `model_not_found` pada `Qwen3.5-397B-A17B` 9router).
- Mau cek "halaman benar terisi data atau cuma placeholder" tanpa interpretasi gambar.
- Verifikasi pasca-rebuild (Phase 5B) — angka DOM = bukti render, bukan "kelihatan jalan".

## Langkah

1. **Buka dashboard**: `browser_navigate http://127.0.0.1:5200/` → snapshot (12 nav + taskbar ada?).
2. **Ukur per halaman** via `browser_console` (jangan switch page via click di iframe — diblokir
   `about:blank`; pakai JS langsung):
   ```js
   (() => {
     const out = {};
     ['page-dashboard','page-ecosystem','page-swarm','page-taskqueue','page-terminal',
      'page-telegram','page-storage','page-skills','page-skills-market','page-system',
      'page-cost','page-deploy'].forEach(id => {
       const el = document.getElementById(id);
       out[id] = el ? (el.innerText||'').trim().length : -1;
     });
     return JSON.stringify(out);
   })()
   ```
   `chars` tinggi (>5k) = HTML/teks statis penuh; diagram apa pun sebenarnya terlihat dari
   elemen anak (`document.querySelectorAll('*').length`) & card selectors.
3. **Cek elemen data terisi** (bukan cuma teks): task cards `[class*=task]`, agent cards,
   rows `tr`, cost values `[class*=cost]`, feed `[class*=msg]`.
4. **Cek fetch route tersedia** (frontend memanggil route yang ada di backend):
   ```bash
   curl -s http://127.0.0.1:5200/openapi.json | python3 -c "import json,sys; d=json.load(sys.stdin); print(sorted(d['paths']))"
   ```
   Lalu bandingkan dengan `grep -oE "fetch\(['\"][^'\"]+" dashboard/app.js`.
5. **Cek error JS**: `browser_console` → konsol clean; `hermes config check` → version OK.
6. **Tulis breakdown** dengan tabel per-halaman: chars, elemen data, status (TERISI/TIPIS/KOSONG).

## Hasil sesi 20 Ags 2026 (baseline comparison)

| Halaman | chars | elemen data | status |
|---|---|---|---|
| dashboard | 9.3K | health cards | TERISI |
| ecosystem | 22.3K | 326 cards | TERISI |
| taskqueue | 6.4K | 243 task cards | TERISI |
| skills | ~19K | rows (async) | TERISI |
| swarm | 1.2K | 19 | TIPIS |
| telegram | 1.4K | 0 msg | KOSONG |
| cost | 1.2K | 0 cost | KOSONG |
| deploy | 636 | 5 | TIPIS |

P0 dari audit: cost & telegram KOSONG padahal backend punya route — prioritaskan sebelum redesign

## Pitfall

- `browser_click` pada iframe/SPA diblokir (`about:blank`) — jangan click; inject via `browser_console`.
- `browser_console` yang bernavigasi (window.location) bisa memicu blokir — batasi ke query DOM saja.
- Vision gagal ≠ dashboard rusak — jangan gabungkan dua diagnosis; audit DOM dulu, lalu cek vision config
  terpisah (lihat `hermes-provider-config` Pitfall 12).