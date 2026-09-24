# Hermes Cron Routing — Registry

**Update:** 24 Sep 2026
**Sumber kebenaran:** `~/.hermes/cron/jobs.json` (runtime) · dokumen ini = cermin status routing

## Thread Telegram Mission Control

| Thread ID | Nama | Fungsi |
|-----------|------|--------|
| `1` | General / Command Center | Interaktif — percakapan pemilik, patch arena, laporan |
| `802` | Research | Riset |
| `803` | Builder | Kode |
| `804` | QA / Pengawas | Audit |
| `1172` | Konten Kreator | Konten |
| **`7402`** | **Cron / Otomasi** | **Notifikasi terjadwal (output cronjob Hermes)** |

## Routing cron saat ini

| Cron | Jadwal | Tujuan | Catatan |
|------|--------|--------|---------|
| Daily Tab Stash Update & Categorize | `0 22 * * *` (22:00 WIB) | thread 7402 | Dipindah dari thread 1 (24 Sep 2026) |
| Daily Brain — Top 10 URL Update | `0 8 * * *` (08:00 WIB) | thread 7402 | Dipindah dari thread 1 (24 Sep 2026) |
| Model Status Probe — Daily | `0 9 * * *` (09:00 WIB) | thread 7402 + local | Dipindah dari thread 1 (24 Sep 2026) |
| DR Snapshot Refresh | `0 21 * * 0` (Minggu 21:00 WIB) | DM pemilik | deliver `origin`; status `error` — lihat catatan |
| Pemdi Health Watch | `every 15m` | DM pemilik | **paused** — nonaktif |
| up-eco-lightfix | `30 23 * * *` | `local` (file saja) | Tidak ada output Telegram |

## Aturan routing

- **Output cron Hermes → thread `7402`** (Cron / Otomasi). Thread 1 (General) hanya untuk interaksi pemilik.
- **Cron dari DM** (dibuat di chat pribadi) → kembali ke DM pemilik (`deliver: origin`).
- **Cron `local`** → hanya tulis ke `~/.hermes/cron/output/`, tidak ada notifikasi Telegram.

## Cara mengubah tujuan cron

Edit `~/.hermes/cron/jobs.json`:

```json
{
  "origin": {
    "platform": "telegram",
    "chat_id": "-1004204696417",
    "thread_id": "7402"
  },
  "deliver": "origin"
}
```

Format `deliver`:
- `origin` — kirim ke tempat job dibuat (mengikuti `origin`)
- `telegram:<chat_id>:<thread_id>[,local]` — explicit, bisa dikombinasi dengan local
- `local` — hanya file

## Catatan

- **DR Snapshot Refresh (Minggu 21:00):** status `error` — snapshot GAGAL karena gate mendeteksi `credentials/ssh-id_ed25519_niumination.enc` sebagai rahasia plaintext; commit dibatalkan. Bukan masalah routing. Perbaiki lalu jalankan manual: `bash ~/Desktop/Niumination/scripts/dr-restore/sync-all.sh`.
- **Pemintasan:** gateway Hermes membaca `jobs.json` per-turn — perubahan langsung aktif tanpa restart.
- Backup sebelum perubahan routing 24 Sep 2026: `~/.hermes/cron/jobs.json.bak-20260924-184243`.
