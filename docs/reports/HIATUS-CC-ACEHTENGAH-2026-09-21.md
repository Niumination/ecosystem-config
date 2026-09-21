# Hiatus cc-acehtengah — 21 Sep 2026

**Status:** 💤 Hiatus (bukan dihapus) · **Pemilik keputusan:** Afrizal Munthe
**Alasan:** Proyek pindah ke `sapa-ai` sesuai permintaan client. Produksi Vercel di-pause oleh pemilik.

Semua aset dipertahankan utuh. Tidak ada satu pun berkas lokal yang dihapus.

## Kondisi Saat Hiatus

| Aset | Kondisi | Lokasi |
|------|---------|--------|
| Folder lokal | **Utuh, 0 berkas dihapus** — 873 MB, working tree bersih, branch lokal tetap ada | `services/cc-acehtengah/` |
| Repo GitHub | **Archived + private** — read-only, branch & history aman | `github.com:Niumination/cc-acehtengah` |
| Tag penanda | `v-hiatus-2026-09-21` (HEAD `hotfix/meeting-ready` `c8416f9`) | sudah ter-push |
| Branch utama | `hotfix/meeting-ready` = sumber kebenaran (produksi terakhir); `main` tertinggal 2 commit (dokumen rilis) | keduanya ter-push |
| Branch pengembangan | 4 branch fitur (329 commit) ter-push; isinya sama dengan lokal, SHA berbeda karena pernah di-rebase sisi remote | ter-push |
| Produksi Vercel | **Paused** — `DEPLOYMENT_PAUSED` 503 (di-pause pemilik, bukan error kode) | `cc-acehtengah.vercel.app` |
| Kode terakhir | `npx vitest run` 24 file / 418 tes lulus · `npm run typecheck` 0 error · `pii-gate.sh` LEAK_COUNT 0 | diverifikasi 21 Sep 2026 |

## Cara Restore ke Ekosistem

### Langkah 1 — Buka kunci repo GitHub

```bash
source ~/.hermes/.env && unset GITHUB_TOKEN

# Unarchive
curl -X PATCH -H "Authorization: Bearer $GH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"archived":false}' \
  https://api.github.com/repos/Niumination/cc-acehtengah

# Set public (opsional — hanya bila memang ingin publik lagi)
curl -X PATCH -H "Authorization: Bearer $GH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"private":false}' \
  https://api.github.com/repos/Niumination/cc-acehtengah
```

### Langkah 2 — Sinkronkan folder lokal

```bash
cd ~/Desktop/Niumination/services/cc-acehtengah
git fetch --all
git checkout hotfix/meeting-ready
git pull --ff-only
```

Folder lokal tidak pernah dihapus, jadi `git pull` langsung mengambil semua perubahan.

### Langkah 3 — Aktifkan produksi Vercel

- Dashboard Vercel → project `cc-acehtengah` → **Resume** (unpause deployment)
- Redeploy: `vercel deploy --prod` dari folder repo
- Verifikasi: `/api/health`, `/api/ews` (fail-closed tanpa sesi admin), `/api/query`

### Langkah 4 — Kembalikan status ekosistem

Perbarui 3 file ini ke 🟢 Active:

- `BACKLOG.md` — baris `cc-acehtengah`
- `docs/registry/project-catalog.md` — baris `cc-acehtengah`
- `docs/registry/deployment-status.md` — baris `services/cc-acehtengah/AGENTS.md`

Lalu commit + push repo `ecosystem-config`.

## ⚠️ Catatan Keamanan

**Kebocoran kredensial ditemukan di branch `feat/ai-executive-answer-v3`** (riwayat GitHub, file `docs/ai/SESI-2026-08-29-dtsen-root-bnba.md`):

- NIK + nama lengkap warga (data pribadi teridentifikasi)
- Password user `dtsen_root` (password DB, bukan API key)
- `DTSEN_DATA_KEY` disebut tapi nilainya tidak tercetak

Branch lokal sudah berisi versi **teredaksi** ([REDACTED] / [NIK REDACTED]) — tidak perlu mengubah apa pun secara lokal.

Saat restore: **jangan set repo menjadi public** sampai branch tersebut dibersihkan, atau ganti password `dtsen_root` + lakukan rotasi `DTSEN_DATA_KEY` di Vercel lebih dulu (data `DtsenIndividu.namaAsliEnc` terenkripsi dengan key ini — rotasi key butuh re-encrypt data).

## Yang TIDAK Diubah Saat Hiatus

- Folder `services/cc-acehtengah/` — utuh, tidak dipindah, tidak dihapus
- Skill `sapa-ai-ops` + referensinya (riwayat rebrand cc→sapa-ai) — dokumentasi riwayat
- Dokumen lama di `docs/` (`ECOSYSTEM-STATUS-*.md`, `docs/references/*`, dll.) — riwayat ekosistem
- Referensi di `apps/niumination-restore/` (RESTORE-PATHS.md, SOUL.md) — skrip pemulihan, sebutan repo lama tetap
- Vercel project — hanya di-pause, tidak dihapus (env vars tetap tersimpan)
