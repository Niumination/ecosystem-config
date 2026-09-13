# Port OPD drill-down dev → main tanpa merge-base (2026-09-03, sapa-ai)

## Kondisi awal
- `git log main..dev` / `dev..main` divergen penuh; `git diff dev...main` → `fatal: tidak ada dasar penggabungan` (427 file beda).
- Merge/cherry-pick tidak aman → port per file konten.

## Studi sebelum janji (wajib)
1. `git log main..dev --oneline` + `git diff --name-status dev main | grep ^D` untuk inventarisasi.
2. Untuk tiap kandidat, verifikasi impor terhadap `src/` target (contoh: `getUniqueOpd:303`, `SapaDataOrigin:67` ada di main) — klaim portabilitas hanya dari simbol yang terbukti ada.
3. Laporkan paket portable vs tidak-portable + dampak; minta trigger eksplisit (`gas port-<nama>`) + keputusan mounting.

## Paket yang diport (5 file, ~500 baris, 0 dependensi DB/auth)
- `src/services/opd-drilldown.ts` — logika murni; parser didelegasikan ke `parseNilaiSapa` (kanonis main, menangani ekor `.00` khas SPLP).
- `src/app/api/analytics/opd/[slug]/route.ts` — dibawa apa adanya (impor resolve).
- `src/components/TopOpdWidget.tsx` — dialihkan ke `/api/sapa` yang SUDAH ADA di main (bentuk `opdBreakdown` kompatibel) agar tidak ada route ganda.
- `src/components/OpdDrilldown.tsx` — dibawa; emoji dibuang (aturan repo).
- Test asal dibawa + kasus adaptasi (ekor `.00`, tren ≥2 titik).

## Konflik parser yang muncul (jangan diulang tanpa sadar)
- Test asal dev: `parseNumericId('-5') → null` dan `'12a' → null` (regex ketat dev).
- Parser kanonis main `parseNilaiSapa`: menerima `-5` (benar), tapi melonggarkan `'12a' → 12` (berbahaya untuk tren — mengarang angka dari teks).
- Resolusi: wrapper ketat — tolak dulu string berhuruf (`/[A-Za-z]/ → null`), lalu delegasikan numerik ke parser kanonis. Test diselaraskan ke perilaku gabungan dengan komentar alasan.
- Aturan umum: bila ekspektasi test asal bertentangan dengan parser kanonis target, menangkan parser kanonis + catat di test dan commit.

## Verifikasi format lintas permukaan
Lead, bucket summary, narasi eksekutif, kartu KPI/metric, panel KPI dashboard, tren drill-down → satu sumber (`headlineParts`/`singkatNarasi`/`parseNilaiSapa`).
Uji dengan skrip sweep sementara terhadap SPLP live (10 chip × lead/headline/narasi), temuan bonus: `618.700.433.221.00` → `618,7 Miliar` (bukan `61,87 Triliun`).
Skrip sweep DIHAPUS setelah verifikasi; hasilnya dicatat di commit message.

## Hasil
- Commit `a4caecb` (10 files, +613/−7) + `5c32c38` (parser fix).
- `npx vitest run` → 5 files, 36 passed. `npm run build` → compiled successfully.
