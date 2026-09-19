# Laporan — Adopsi Stack 2026 `Niu-OSS-Dashboard` (CVE-2025-66478 tertutup)

**Tanggal:** 19 Sep 2026 · **Status:** SELESAI — kode di push, Vercel auto-deploy berjalan
**Pemilik:** Afrizal Munthe · **Repo:** `github.com/Niumination/Niu-OSS-Dashboard` (lokal: `sites/niu-oss-dashboard/`)

## Latar Belakang

Deploy Vercel 19 Sep 2026 (2× gagal) diblokir Vercel karena `next@15.3.3` terdampak
**CVE-2025-66478 (React2Shell, CVSS 10)** — Vercel menolak deploy versi rentan
15.0.0–16.0.6. Pemilik membuat upgrade mayor di arena.ai dan mengirim
`~/Downloads/niu-oss-v2.zip` (19 Sep): 1 commit `1dbd396` berbasis `0df5f3c` +
patch `stack-2026-1dbd396.patch`.

## Tindakan (agent)

| Langkah | Hasil |
|---|---|
| Audit patch (rahasia, `.gitignore`, base SHA, tree hash) | ✅ basis `0df5f3c` tree identik lokal (`c1c6a21`); rahasia 0 temuan; `.gitignore` tidak tersentuh |
| `git apply --check` ke salinan 0df5f3c | ✅ bersih (125 berkas, +1078/-839) |
| Terapkan patch di lokal | ✅ `git apply` exit 0 |
| `secret-scan-staged.py` (semua staged) | ✅ exit 0 |
| `npm ci` | ✅ exit 0 |
| `npm test` | ✅ 41/41 (4 berkas) |
| `npm run typecheck` | ✅ exit 0 |
| `npm run build` | ✅ exit 0 (20 halaman SSG + dinamika) |
| `SITE_URL= npm run build` (emulasi Vercel) | ✅ exit 0 — pitfall env kosong tetap tertutup |
| Commit + merge `origin/main` (cron `fde2853` uptime) | ✅ 1 konflik `public/api/v1/uptime.json` — selesaikan: ambil versi baru (patch, 13:47) |
| `git push origin main` | ✅ `fde2853..b3e85a3` |
| DOX pass root (`deployment-status.md`, `project-catalog.md`, `BACKLOG.md`) | ✅ |

## Yang Berubah (commit `513c468`, 125 berkas)

- `next 15.3.3 → 16.3.5` (menutup CVE-2025-66478 — versi terpatch Vercel)
- `react 19.1.0 → 19.2.8`, `@types/node 20 → 22`, `typescript 5.8 → 7.0.2`, `vitest 4 → 5`
- `framer-motion 12 → 13`, `three 0.178 → 0.186`, `drei/fiber` minor, `lucide-react 0.518 → 1.47`
- `package.json` name → `niu-oss-dashboard`, `engines.node >=20.9`, script `build:webpack`
- `next.config.ts`: hapus `eslint.ignoreDuringBuilds` (lint dinonaktifkan Next 16 tanpa config ESLint)
- `tsconfig.json`: include `.next/dev/types`
- 101 berkas `public/api/v1/` diregenerasi (timestamp 19 Sep 13:47, data sama)
- `AGENTS.md`/`BACKLOG.md` proyek: upgrade DOX (flag CVE dicoret "SELESAI")

## Efek pada Vercel (tidak dicek dari sini)

Push `b3e85a3` memancing auto-deploy proyek Vercel `niu-oss` (team `archk4lis-projects`).
Karena `next@16.3.5` di luar rentang rentan, blocker "Vulnerable version detected"
perluang hilang. Status deploy baru diverifikasi dengan `vercel ls niu-oss` saat
pemilik memberi tahu. **UNCHECKED** per laporan ini — belum di-probe.

## Catatan Risiko Kecil

1. `react` 19.2.8: CVE-2025-55182 (sisi React) belum ditelusuri ke registry npm
   (perintah query diblokir gate keamanan) — UNGUJI; bila deploy Vercel tetap
   ter-flag, naikkan react 19.2.8 atau lebih.
2. Workflow cron `uptime.yml`/`refresh-data.yml` aktif: setiap commit = deploy
   produksi. Setelah patch stack 2026, ini kembali sehat.
3. `engines.node >=20.9` (masih range, bukan pin mayor) — Vercel auto-upgrade
   bisa mengubah perilaku build; pin bila build mendadak berubah.

## Bukti

```
git rev-parse HEAD → b3e85a3c50d74a13d146587baf6ca83ef5a63022 (== origin/main)
APPLY_EXIT=0  (git apply --verbose, 125 berkas)
npm ci exit=0 / npm test exit=0 (41/41) / typecheck exit=0 / build exit=0
SITE_URL= npm run build exit=0
secret-scan-staged.py exit=0
git push: fde2853..b3e85a3 main -> main (PUSH_EXIT=0)
audit: (un)grep sk-/ghp_/AIza/service_role/PRIVATE KEY/xox pada baris + patch → 0
```

## Rekomendasi Lanjut (tunggu keputusan pemilik)

- Pantau `vercel ls niu-oss` — kalau deploy baru `Ready`, lanjut **Fase 4**:
  isi DNS `niumination.web.id` (A `@` → 76.76.21.21, CNAME `www` → cname.vercel-dns.com
  di idwebhost). Domain masih parking.
- `BACKLOG.md` proyek: item "Upgrade next" sudah dicoret, tidak perlu tindak lanjut.
