---
name: second-brain
description: "Second Brain PKM — simpan catatan ke brain/inbox dan cari pengetahuan lama. Use when user says: simpan ini, catat ini, ingat ini, capture, cari di brain, apa yang kita bahas, knowledge base. Trigger words: simpan, catat, capture, brain, knowledge, recall."
version: "1.0.0"
---

# Second Brain — Personal Knowledge Management

## When to Use
- User berkata "simpan ini ke brain" / "catat ini" / "ingat ini" / "#capture"
- User bertanya tentang keputusan/diskusi lama ("apa yang kita bahas soal X?")
- Research/riset perlu konteks dari catatan sebelumnya
- Menyimpan ide cepat sebelum hilang

## Komponen
- **Brain root**: `/Users/zaryu/Desktop/Niumination/brain/`
- **Scripts**:
  - `brain/scripts/brain_capture.py` — simpan ke daily note
  - `brain/scripts/brain_search.py` — cari dengan ranking

## Commands

### Capture (simpan catatan)
```bash
python3 brain/scripts/brain_capture.py "teks catatan" --tag #proyek/xxx --source telegram-802
```
- Append ke `brain/inbox/YYYY-MM-DD-daily.md`
- Format: `- [HH:MM] teks (#tag) · src:sumber`
- Tag opsional: `--tag #pemdi`, `--tag #riset`, dll

### Search (cari pengetahuan)
```bash
python3 brain/scripts/brain_search.py "kata kunci" --limit 10 --path docs
```
- Ranking: keyword hits + title match + recency (file baru > lama)
- Path opsional: `inbox`, `projects`, `docs`, `resources`, kosong = semua

### Daily note
- Otomatis dibuat saat capture pertama di hari itu
- Format: `# YYYY-MM-DD — Daily` + `## Capture` section

## Prosedur (untuk agent)

1. **Capture**: Saat user minta simpan → jalankan brain_capture.py dengan teks + tag + source
2. **Search**: Saat user tanya "apa yang kita bahas soal X" → jalankan brain_search.py, baca top 3 file yang relevan
3. **Konteks proyek**: Saat mulai kerja proyek → cari `brain/projects/<nama>/` untuk context
4. **Auto-detect proyek**: Jika teks mengandung `#proyek/xxx` atau `#pemdi`, tag otomatis

## Capture via Telegram

User bisa mengirim pesan di Telegram dengan pola:
- `#capture <teks>` — simpan langsung ke brain/inbox
- `simpan ini: <teks>` — simpan sebagai capture
- `catat: <teks>` — alias simpan
- `<teks> #pemdi` — simpan dengan tag proyek otomatis

Agent harus:
1. Deteksi pola trigger di pesan Telegram (DM atau thread)
2. Jalankan: `python3 brain/scripts/brain_capture.py "<teks>" --tag <deteksi> --source telegram-<thread>`
3. Balas konfirmasi singkat: `✅ Disimpan ke brain/inbox/2026-08-12-daily.md`

## Hybrid Retrieval

- **On-demand**: User tanya soal keputusan lama → `brain_search.py` → baca file relevan
- **Konteks proyek aktif**: Saat session fokus proyek X → auto baca `brain/projects/X/` context

## Pitfalls
- Jangan simpan teks mentah terlalu panjang — ringkas poin penting
- Jangan override daily note — selalu append
- Search default seluruh brain — gunakan `--path` untuk persempit
- File di `brain/docs/` = laporan resmi, jangan di-edit untuk capture harian
