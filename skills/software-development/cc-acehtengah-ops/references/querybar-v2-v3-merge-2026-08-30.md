# QueryBar v2↔v3 — Perbandingan & Bug Duplikasi Merge (30-Agu-2026)

## Konteks: "fitur Top OPD ada di v2-live" = salah ingat branch
User yakin fitur "Top OPD widget" ada di `feat/ai-executive-answer-v2-live`. Faktanya hasil investigasi cross-branch:
- `TopOpdWidget.tsx` HANYA ada di v3/backup (commit `99d5f9e`), **TIDAK pernah ada di v2-live** (`git log v2-live -- TopOpdWidget.tsx` kosong).
- v2-live cuma punya `AIDataWidget.tsx` (bukan Top OPD).
- **v3 adalah SUPERSET v2-live**: `git log v2-live ^v3` = KOSONG (v2 tidak punya commit unik); `git log v3 ^v2-live` = 18+ commit unik (DTSEN_ROOT, TopOpdWidget, Pecah Jawaban, dll).
- Kesimpulan: user salah ingat branch (nama `feat/ai-executive-answer-v2-live` vs `...-v3` mirip). Fitur yang dicari SUDAH ADA di v3.
- Sebelum klaim "fitur ada di branch X", jalankan `git log --all --oneline -- <file>` + `git ls-tree -r <branch> -- <path>` per branch. Jangan asumsi.

## QueryBar: v2 punya 2 hal lebih baik, v3 punya BUG duplikasi
| Aspek | v2-live (125 ln) | v3 (196 ln, diambil dari hotfix) |
|---|---|---|
| Group chips | sapa, dtsen, bapokting (3) | sapa, dtsen, dokumen, bapokting (4 — LEBIH lengkap, jangan hilang) |
| Footer guidance | ✅ "✓ AI memprioritaskan evidence SAPA…" + "Enter untuk mengajukan · Maks. 2.000" | ❌ TIDAK ada |
| Chip Stunting di group SAPA | ✅ `👶 Stunting` (query aktif) | ❌ cuma di Dokumen B (`👶 Stunting (SAPA)`) |
| Render chips | 1x (clean) | ❌ **2x — DUPLIKAT (bug merge!)** |
| Bapokting | disabled (query kosong) | aktif (query isi) |

## BUG: QueryBar v3 render CHIP_GROUPS DUA KALI
v3 `src/components/QueryBar.tsx` memetakan `CHIP_GROUPS` pada DUA blok berurutan:
- Blok 1: ~line 119-140 (style `var(--brand-tint)` / `enabled:hover:border-[#B8D1BB]`)
- Blok 2: ~line 142-164 (style `#E9E6DA` / `hover:bg-[#DCE8DE]`)
Gejala: semua chips muncul GANDA di UI. Penyebab: merge hotfix→v3 menggabungkan render-style v3 + hotfix jadi 2 block `.map(CHIP_GROUPS...)`. **Setelah tiap merge cross-branch, grep `QueryBar.tsx` untuk jumlah `.map((group) =>` — harus 1, bukan 2.**

## Resep: ambil yang v2 lebih baik ke v3 (JANGAN hapus group DTSEN/Dokumen)
1. Hapus SATU dari dua blok `.map(CHIP_GROUPS...)` (pertahankan yang pakai `var(--brand-tint)`).
2. Tambah chip `{ label: '👶 Stunting', query: 'berapa jumlah balita stunting di aceh tengah' }` ke group `sapa` (sebelum `🌾 Pertanian`).
3. Tambah footer setelah `<form>`:
   ```tsx
   <div className="flex flex-col gap-1 text-[10px] text-[var(--text-muted)] sm:flex-row sm:items-center sm:justify-between">
     <span className="inline-flex items-center gap-1.5"><span className="text-[var(--brand)]">✓</span> AI memprioritaskan evidence SAPA sebelum menyusun jawaban.</span>
     <span>Enter untuk mengajukan · Maks. 2.000 karakter</span>
   </div>
   ```
4. Verify: `npx tsc --noEmit` + `npx next build`.

## Status 30-Agu (di-stop user "berhenti" tengah edit)
Hanya step 2 sebagian: chip `👶 Stunting (SAPA)` → `👶 Stunting` sudah diubah di disk. Step 1 (hapus duplikasi) & 3 (footer) BELUM dilakukan. Working tree modified, **BELUM di-commit**, BELUM di-push. Biarkan apa adanya sampai user lanjut.
