# Pitfall: Git Rename-Detection False Positive Saat Merge Cross-Branch

Ditemukan 30-Agu-2026 saat merge `hotfix/meeting-ready` → `feat/ai-executive-answer-v3`.

## Gejala
Setelah merge selesai & conflict resolve, user lapor "masih ada bug dari hasil merge" /
endpoint tiba-tiba MATI (500/404 padahal sebelumnya jalan).

## Akar Masalah
`hotfix` sengaja me-rename beberapa API route jadi `.bak` (disable endpoint sementara):
- `src/app/api/ews/route.ts` → `route.ts.bak`
- `src/app/api/datasets/route.ts` → `route.ts.bak`
- `src/app/api/datasets/[slug]/route.ts` → `route.ts.bak`

Saat merge ke `v3` (yang MASIH punya `route.ts` asli), git similarity detection
(R100 = 100% similar) **salah mengira** v3 melakukan rename `route.ts` → `route.ts.bak`.
Hasil merge:
- `route.ts` lenyap, diganti `route.ts.bak` → Next.js tidak load `.bak` → endpoint MATI
- `scripts/seed.ts` ikut ter-DELETE (D) — efek samping merge

`git diff --name-status e028d84 7cd1d84` menunjukkan:
```
R100  src/app/api/datasets/[slug]/route.ts   → .bak
R100  src/app/api/datasets/route.ts          → .bak
R100  src/app/api/ews/route.ts               → .bak
D     scripts/seed.ts
```

## Deteksi (WAJIB setelah tiap merge)
```bash
cd ~/Desktop/Niumination/services/cc-acehtengah
git diff --name-status <BASE> <MERGE_HEAD> | grep -E "^[RD]"
# R = rename (curiga kalau .bak), D = delete (curiga kalau file penting)
```
Juga cek tidak ada `.bak` tersisa di `src/app/api`:
```bash
find src/app/api -name "*.bak"
```

## Fix
```bash
# 1. Rename balik .bak -> .ts
git mv src/app/api/ews/route.ts.bak src/app/api/ews/route.ts
git mv src/app/api/datasets/route.ts.bak src/app/api/datasets/route.ts
git mv "src/app/api/datasets/[slug]/route.ts.bak" "src/app/api/datasets/[slug]/route.ts"
# 2. Restore file yang ter-delete
git checkout <BASE> -- scripts/seed.ts
# 3. Verify isi .bak == base route.ts (hotfix cuma rename, tidak ubah isi)
diff <(git show <BASE>:src/app/api/ews/route.ts) src/app/api/ews/route.ts
# 4. Build verify
npx next build 2>&1 | tail -n 15
git add -A && git commit -m "fix(merge): restore ews/datasets route.ts + seed.ts"
git push origin feat/ai-executive-answer-v3
```

## Pencegahan
- Hotfix memang sengaja pakai `.bak`; jangan asumsi `.bak` = bug. TAPI saat merge KE
  branch yang punya `route.ts` asli, git akan false-rename. Selalu diff `--name-status`
  pasca-merge.
- Jika perlu disable endpoint, prefer hapus route handler dari tree, bukan rename `.bak`
  (renameless git detection aman).
