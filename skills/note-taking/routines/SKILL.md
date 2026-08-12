---
name: routines
description: "Routine workflows — morning brief, daily report, project sync. Use when user says: /routine, morning brief, laporan harian, rekap harian, update status proyek, daily report. Trigger words: routine, brief, laporan harian, rekap, status proyek."
version: "1.0.0"
---

# Routines — Workflow Harian Otomatis

## When to Use
- User mengetik `/routine <nama>` di Telegram
- "Morning brief" / "brief pagi"
- "Laporan harian" / "rekap hari ini"
- "Update status proyek X"

## Routines Available

### 1. morning-brief
Rekap pagi: status brain + proyek + berita teknologi → kirim ke Telegram DM.
```bash
python3 brain/scripts/routine_morning.py --send
# tanpa berita:
python3 brain/scripts/routine_morning.py --send --no-news
```

### 2. daily-report
Rekap aktivitas harian dari capture → brain/docs/daily/.
```bash
python3 brain/scripts/routine_daily.py
# tanggal spesifik:
python3 brain/scripts/routine_daily.py --date 2026-08-11
```

### 3. project-sync
Update status proyek → brain/projects/<nama>/status.md.
```bash
python3 brain/scripts/routine_project.py <nama-proyek> "status text" --tag pemdi,audit
```

## Prosedur (untuk agent)

1. **/routine morning-brief** → jalankan `routine_morning.py --send`, konfirmasi ke user
2. **/routine daily-report** → jalankan `routine_daily.py`, tampilkan path hasil
3. **/routine project-sync <nama> <status>** → jalankan `routine_project.py`, konfirmasi

## Integrasi Cron (opsional)
Bisa dijadwalkan via `hermes cron`:
- `0 7 * * *` → morning brief otomatis ke Telegram
- `0 23 * * *` → daily report otomatis

## Pitfalls
- Morning brief butuh `feedparser` (sudah terinstall)
- Daily report hanya memproses capture di `brain/inbox/YYYY-MM-DD-daily.md`
- Project sync membuat folder baru jika belum ada
