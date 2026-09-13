# Probe: "Fitur Hilang" — Buktikan Lewat Source + Live, Bukan Asumsi

Skenario berulang (30–31 Ags 2026): user lapor "fitur X hilang setelah merge / di branch Y",
padahal fitur sebenarnya ADA. Pola verifikasi yang TERBUKTI kerja:

## 1. Cross-branch feature hunt (SEBELUM klaim hilang)
Jangan tebak branch mana user edit. Cari di SEMUA branch:
```bash
cd ~/Desktop/Niumination/services/cc-acehtengah
git branch -a                                    # semua branch lokal + remote
git ls-tree -r --name-only <BRANCH> | grep -iE "opd|drill|analytic|<keyword>"
git log --all --oneline | grep -iE "opd|drill|detail|<keyword>"
git branch -a --contains <COMMIT>               # di branch mana commit fitur ada
git fsck --lost-found                            # dangling commit (perubahan terlepas)
git reflog --all | head -n 20
```
Catatan: fitur detail OPD (`OpdDrilldown.tsx`, `opd-drilldown.ts`, `TopOpdWidget.tsx`,
`?opd=` drilldown di `analytics/page.tsx`) HANYA ada di `feat/ai-executive-answer-v3`
+ `backup/feat-v3-saved` (identik). `v1`/`v2-live`/`hotfix`/`main` TIDAK punya.

## 2. Source-intact check (apakah merge menghapus/ubah?)
```bash
git diff --name-status <V3_BASE> <MERGE_HEAD>   # cari R/D yang tidak diinginkan
diff <(git show <V3_BASE>:src/path/file.tsx) src/path/file.tsx   # identik?
npx next build 2>&1 | tail -n 15                 # compile sukses = tidak ada error fatal
```

## 3. LIVE REPRO — bukti terkuat (paling penting)
Jangan cuma baca source. Jalankan dev server & `curl` endpoint nyata:
```bash
# Cek dulu ada dev server jalan? (jangan start baru — bakal "Another next dev server
# is already running" kalau port 3000 sudah dipakai user)
lsof -iTCP:3000 -sTCP:LISTEN -P -n
# Kalau tidak ada, jalanin: npx next dev -p 3000  (background=true, jangan pakai &)
# TUNGGU ~15s (Turbopack "Ready in ~1.5s" tapi route butuh compile pertama)

# Test halaman + API:
curl -s -o /dev/null -w "analytics page: %{http_code}\n" -m 15 http://127.0.0.1:3000/dashboard/analytics
curl -s -m 20 http://127.0.0.1:3000/api/analytics | head -c 300
curl -s -m 20 "http://127.0.0.1:3000/api/analytics/opd/Dinas%20Kesehatan" | head -c 300
curl -s -o /dev/null -w "ews API: %{http_code}\n" -m 15 http://127.0.0.1:3000/api/ews
```
**Bukti session ini:** semua return 200 + data riil (2032 records, 38 OPD,
`topIndicators` per OPD). → Fitur detail OPD TIDAK hilang, cuma diakses lewat
beranda (`TopOpdWidget` klik OPD → `/dashboard/analytics?opd=NAMA`), bukan langsung
buka `/dashboard/analytics` (tanpa `?opd=` cuma tampil summary).

## Kesimpulan yang boleh diklaim
- Source utuh + build sukses + live 200 = **fitur ADA**, bukan hilang.
- "Hilang" biasanya: (a) belum `vercel deploy` (yang live = hotfix, bukan v3),
  (b) user buka URL tanpa query param yang memicu drilldown,
  (c) perubahan uncommitted di working tree localhost yang tidak masuk commit.
- Baru klaim "hilang" kalau `git diff --name-status` menunjukkan D/R nyata
  (lihat `merge-rename-pitfall-2026-08-30.md`).
