# Pitfall: ExecutiveAnswerRenderer DROPS BreakdownExplorer (tombol "Pecah Jawaban")

**Ditemukan:** 30-Agu-2026, sesi merge hotfix→v3 + review fitur "Pecah Jawaban hilang".

## Gejala
- User buka `cc-acehtengah` di localhost (branch v3) → output AI **TIDAK ada tombol "Pecah Jawaban"**.
- Di `hotfix/meeting-ready` (PROD live) tombol ADA. User yakin fitur "ada di v2-live" — ternyata salah ingat (v3 yang punya; hotfix yang render langsung).

## Akar Masalah (flag-routing, BUKAN bug merge)
`src/components/AIResponseRenderer.tsx`:
```tsx
const useExecutiveUi = process.env.NEXT_PUBLIC_AI_EXECUTIVE_UI !== 'false';
if (useExecutiveUi) {
  return <ExecutiveAnswerRenderer response={response} onFollowUp={onFollowUp} />; // default TRUE → ini yang jalan
}
// legacy path (hanya kalau flag=false):
<BreakdownExplorer sourceLabel={response.dataSource} program={programHint} />  // tombol Pecah Jawaban ada di sini
```
`ExecutiveAnswerRenderer` tidak memuat `BreakdownExplorer` sama sekali (grep `BreakdownExplorer` di file itu = kosong). Maka di mode default (Executive UI), tombol Pecah Jawaban **tidak di-render**.

Di `hotfix` tidak ada `ExecutiveAnswerRenderer.tsx` → `AIResponseRenderer` langsung render `BreakdownExplorer` → tombol muncul. Itu sebabnya beda antara hotfix (ada) dan v3 (hilang).

**JANGAN salah diagnosis** sebagai:
- bug merge `.bak` (ews/datasets route mati) — itu endpoint, bukan UI button
- QueryBar double-render — itu chips GANDA, bukan tombol hilang
- "source hilang" — `BreakdownExplorer.tsx` UTUH ada di v3 (`git diff` analytics/OPD KOSONG)

## Diagnosis Cepat
```bash
cd ~/Desktop/Niumination/services/cc-acehtengah
# 1. Apakah BreakdownExplorer ada di ExecutiveAnswerRenderer? (harus KOSONG = bug)
grep -n "BreakdownExplorer" src/components/ExecutiveAnswerRenderer.tsx
# 2. Apakah flag diset? (kosong = default true = Executive mode)
grep -rn "NEXT_PUBLIC_AI_EXECUTIVE_UI" .env* 2>/dev/null
```

## Fix (terapkan di v3)
1. Import di `ExecutiveAnswerRenderer.tsx` (setelah import `getExecutivePresentation`):
   ```tsx
   import BreakdownExplorer from './BreakdownExplorer';
   ```
2. Di main component `export default function ExecutiveAnswerRenderer(...)`, SETELAH header div (baris `<div className="flex flex-wrap items-center justify-between gap-3">...AnswerBadge...</div>`), TAPI SEBELUM `<div className="grid items-start gap-4 xl:grid-cols-[minmax(0,1fr)_320px]">`, inject:
   ```tsx
   {/* Tombol "Pecah Jawaban" — paling atas output AI (deterministik, tanpa LLM) */}
   <BreakdownExplorer sourceLabel={response.dataSource} />
   ```
   - `program` prop **optional** → boleh di-skip (hanya relevan di level kabupaten/kecamatan untuk filter bansos).
   - `sourceLabel` ambil dari `response.dataSource` (field ada di `HybridResponse`).

## Verifikasi
```bash
npx tsc --noEmit 2>&1 | grep -iE "ExecutiveAnswerRenderer|BreakdownExplorer"  # harus kosong
grep -n "BreakdownExplorer" src/components/ExecutiveAnswerRenderer.tsx          # harus ada 2 baris (import + usage)
# Dev server hot-reload; cek log .next/dev/logs/next-development.log tidak ada ERROR compile
curl -s -o /dev/null -w "%{http_code}\n" -m 15 http://127.0.0.1:3000/dashboard   # 200
```
Lalu commit + push v3 (experimental, jangan deploy Vercel):
```bash
git add src/components/ExecutiveAnswerRenderer.tsx
git -c user.name="Afrizal Munthe" -c user.email="afrizal@diskominfo.acehtengahkab.go.id" \
  commit -m "feat(AI): tampilkan tombol Pecah Jawaban (BreakdownExplorer) di mode Executive UI"
git push origin feat/ai-executive-answer-v3
```

## Commits terkait (30-Agu)
- `af9a404` fix(QueryBar): hapus duplikasi render CHIP_GROUPS
- `c2dfe9f` fix(merge): restore ews/datasets route.ts dari .bak + restore scripts/seed.ts
- `eba4dae` feat(AI): tampilkan tombol Pecah Jawaban (BreakdownExplorer) di mode Executive UI
