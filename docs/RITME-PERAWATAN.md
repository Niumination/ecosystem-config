# RITME-PERAWATAN.md — Jadwal Perawatan Ekosistem

**Tanggal:** 2026-10-15 · **Status:** AKTIF

---

## Harian (0 menit)

- `eco-guard` berjalan sendiri (cron 08:00 & 20:00)
- Hanya bicara bila ada masalah
- Bila ada MASALAH: periksa LOG-PERBAIKAN.md

## Mingguan (15 menit)

- Lihat Telegram + LOG-PERBAIKAN.md
- Promosi skill baru (skill-bank-promote.sh)
- `git status` 3 repo utama (Niumination, brain, wiki)
- Cek heartbeat healthchecks.io

## Bulanan (45 menit)

- Drill DR (`eco-dr-drill.sh`)
- Rotasi 1 kredensial
- Audit disk (`du -sh ~/.hermes ~/Desktop/Niumination`)
- Tinjau 1 keputusan di DECISIONS.md

## Kuartalan (2 jam)

- Tinjau anggaran unit hidup
- Evaluasi curator/kanban
- Hapus yang tidak dipakai (ke arsip)

---

## Cron Job Perawatan

| Job | Schedule | Tujuan |
|---|---|---|
| Eco Guard Verify | 08:00 & 20:00 | Verifikasi kesehatan |
| Backup harian | 21:00 | Snapshot L1 |
| Wiki malam | 02:20-04:10 | Maintenance wiki |
| Skill audit | Sabtu 21:00 | Audit skill mingguan |
| Env writers scan | Sabtu 21:30 | Scan penulis config |
| HC Heartbeat Verify | 07:00 | Healthchecks.io |
| HC Heartbeat Backup | 03:00 | Healthchecks.io |
| HC Heartbeat Wiki | 04:00 | Healthchecks.io |

---

## Catatan

- Semua cron job di atas sudah terdaftar dan aktif
- Bila ada job baru yang gagal 2× → pause dan perbaiki dulu
- Maksimal 3 job baru per minggu
