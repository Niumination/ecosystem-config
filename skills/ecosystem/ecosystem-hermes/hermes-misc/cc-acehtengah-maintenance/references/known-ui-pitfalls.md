# Known cc-acehtengah UI Pitfalls — exact fixes

All fixes verified working on `feat/ai-executive-answer-v3` (Aug 30, 2026). File paths relative to `services/cc-acehtengah/`.

---

## A. "Pecah Jawaban" (BreakdownExplorer) tombol tidak muncul di v3
**Symptom:** Di hotfix tombol ada, di v3 localhost tidak muncul.
**Root cause:** `src/components/AIResponseRenderer.tsx`
```tsx
const useExecutiveUi = process.env.NEXT_PUBLIC_AI_EXECUTIVE_UI !== 'false';
if (useExecutiveUi) {
  return <ExecutiveAnswerRenderer response={response} ... />;  // default → ini yang jalan
}
// legacy path (cuma kalau flag=false) yang render BreakdownExplorer
<BreakdownExplorer sourceLabel={response.dataSource} program={programHint} />
```
`ExecutiveAnswerRenderer` TIDAK memuat `BreakdownExplorer` → tombol hilang.
**Fix:** di `src/components/ExecutiveAnswerRenderer.tsx`, import `BreakdownExplorer`, lalu di main `return` (setelah header `<h2>Executive answer</h2>`, sebelum grid artikel) inject:
```tsx
<BreakdownExplorer sourceLabel={response.dataSource} />
```
Sesuai instruksi user: tombol di PALING ATAS output AI.

---

## B. QueryBar keyword chips muncul double
**Root cause:** merge left TWO render blocks for `CHIP_GROUPS` (v3-asli + hotfix), identical maps, different styling (`var(--brand-tint)` vs `#E9E6DA`).
**Fix:**
1. Hapus blok duplikat (biasanya blok dengan `comment {/* Keyword Chips */}` / `bg-[#E9E6DA]`).
2. Di blok yang dipertahankan, ubah:
   `disabled={isLoading || group.disabled}` →
   `disabled={isLoading || group.disabled || !chip.query}` (hotfix safety: chip dg query kosong jadi disabled, tidak bisa diklik).

---

## C. Tombol header (Logout/Akun/Login/Online/SAPA) terlihat seperti overlay transparan
**Root cause:** hardcoded hex + opacity tipis (`bg-[#2D6A4F]/30`, `bg-[#B3261E]/30`, text `#52B788`/`#E58B7F`) ditumpuk di header yang jg transparan (`bg-[var(--surface-card)]/95 backdrop-blur-md`) → double-transparency.
**Fix (pakai token tema solid dari `src/app/globals.css`):**
| Elemen | Sebelum | Sesudah |
|---|---|---|
| Online / SAPA / Akun / Login | `bg-[#2D6A4F]/30` + `text-[#52B788]` | `bg-[var(--brand-tint)]` + `text-[var(--brand)]` + `border-[var(--border)]` |
| Logout | `bg-[#B3261E]/30` + `text-[#E58B7F]` | `bg-[var(--danger-tint)]` + `text-[var(--danger)]` + `border-[var(--danger)]` |
| Header bg | `bg-[var(--surface-card)]/95 backdrop-blur-md` | `bg-[var(--surface-card)]` (solid) |
| Divider admin | `border-[#2D6A4F]/40` | `border-[var(--border)]` |
| SAPA text | `text-[#D9C284]` | `text-[var(--accent)]` |
Hover: `hover:brightness-95` (bukan opacity lagi).
Token values ada di `:root` (light) dan `:root` kedua (dark) di `globals.css`:
`--brand:#1B4332`, `--brand-tint:#DCE8DE`, `--danger:#B3261E`, `--danger-tint:#FBE3DE`, `--accent:#D9C284`, `--border:#9A9683` (light); dark variants berbeda.

**Verifikasi:** grep sisa hex `#2D6A4F|#52B788|#B3261E|#E58B7F` di `layout.tsx` harus kosong (teks muted `#C6C3B4`/`#767D6F` sengaja dibiar).
