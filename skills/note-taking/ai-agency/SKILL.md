---
name: ai-agency
description: "AI Agency — generate laporan otomatis, draft konten, data mining dari brain. Use when user says: buat laporan, draft konten, tulis artikel, mining data, ekstrak informasi, agency. Trigger words: laporan otomatis, draft, artikel, mining, ekstrak, agency."
version: "1.0.0"
---

# AI Agency — Output Layer

## When to Use
- User minta laporan otomatis (harian, proyek, progress)
- User minta draft konten (berita, artikel, ringkasan)
- User minta ekstraksi data / data mining dari dokumen

## Komponen (scripts di brain/scripts/)

### 1. Report Generator — `agency_report.py`
```bash
# Rekap harian
python3 brain/scripts/agency_report.py --type daily --days 1

# Laporan proyek
python3 brain/scripts/agency_report.py --type project --project pemdi-aceh-tengah

# Progress semua proyek
python3 brain/scripts/agency_report.py --type progress

# Simpan ke file
python3 brain/scripts/agency_report.py --type daily --days 7 --out daily/2026-08-12-week.md
```

### 2. Content Draft — `agency_content.py`
```bash
# Draft ringkasan dari brain
python3 brain/scripts/agency_content.py "OmniRoute" --style ringkasan --source brain

# Draft berita dari web
python3 brain/scripts/agency_content.py "AI" --style berita --source web

# Simpan ke brain/docs/agency/
python3 brain/scripts/agency_content.py "Topik" --style artikel --out topik.md
```
> Script menghasilkan kerangka + konteks; **agent menulis draft final** berdasarkan instruksi style.

### 3. Data Mining — `agency_mining.py`
```bash
# Mining kata kunci di docs
python3 brain/scripts/agency_mining.py "bukti dukung" --path docs --format table

# JSON output untuk processing
python3 brain/scripts/agency_mining.py "pemilahan" --path docs --format json
```

## Prosedur (untuk agent)

1. **/agency report <type>** → jalankan agency_report.py, tampilkan/simpan hasil
2. **/agency content <topik>** → jalankan agency_content.py, tulis draft final dengan gaya sesuai style, kirim ke user
3. **/agency mine <query>** → jalankan agency_mining.py, sajikan temuan ringkas

## Integrasi

- Data sumber: brain (capture, status proyek, docs)
- Output delivery: Telegram (kirim via `hermes send`) atau file di brain/docs/
- Bisa dijadwalkan via cron (misal laporan mingguan Jumat)

## Pitfalls
- Content draft = kerangka, agent HARUS menulis versi final (jangan kirim kerangka mentah)
- Data mining konteks per file per keyword = 1 hasil — untuk lebih dalam, naikkan limit
- Report daily butuh capture di inbox; kalau kosong, lapor "tidak ada aktivitas"
