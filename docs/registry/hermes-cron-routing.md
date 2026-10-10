# Hermes Cron Routing — Registry

**Update:** 11 Okt 2026
**Sumber kebenaran:** `~/.hermes/cron/jobs.json` (runtime) · dokumen ini = cermin status routing
**Verifikasi:** `hermes cron list` — 14 job aktif. Tabel di bawah dibaca ulang dari perintah itu, bukan dari ingatan.

## Thread Telegram Mission Control

| Thread ID | Nama | Fungsi |
|-----------|------|--------|
| `1` | General / Command Center | Interaktif — percakapan pemilik, patch arena, laporan |
| `802` | Research | Riset |
| `803` | Builder | Kode |
| `804` | QA / Pengawas | Audit |
| `1172` | Konten Kreator | Konten |
| `7402` | Serbaguna / Cadangan | Flex-thread (tugas umum saat thread lain sibuk) |
| `12595` | **Cron & Otomasi** | **Output cronjob Hermes (terjadwal)** |
| `12707` | Edu Content | Pipeline buku edukasi |
| `8853` | ASN | Administrasi dinas, SKP/eKinerja |
| `13902` | Orkestrator | Koordinator ekosistem |

## Routing cron saat ini (14 job)

| ID | Cron | Jadwal | Tujuan | Catatan |
|---|---|---|---|---|
| `6789760172b1` | Daily Tab Stash Update & Categorize | `0 22 * * *` | thread 12595 | Dipindah dari 7402 → 12595 (5 Okt 2026) |
| `69fe96da4c90` | Daily Brain — Top 10 URL Update | `0 8 * * *` | thread 12595 | Dipindah dari 7402 → 12595 (5 Okt 2026) |
| `15d9127ab8b0` | Model Status Probe — Daily | `0 9 * * *` | thread 12595 + local | Script `model-status-probe-cron.sh`, non-agent |
| `525b540c1e86` | DR Snapshot Refresh | `0 21 * * 0` | thread 12595 | **Diperbarui 11 Okt** — registry lama menulis `local`, aktual thread 12595. Script `dr-restore-sync.sh` |
| `e439b66b40b4` | up-eco-lightfix | `30 23 * * *` | thread 12595 | **Diperbarui 11 Okt** — registry lama menulis `local`, aktual thread 12595 |
| `d0ab0fde1b2e` | Ecosystem Health Check | `0 */2 * * *` | thread 12595 | `ecosystem-health.py` — gateway, relay, cron, disk, thermal, Tailscale |
| `524a941977dd` | Dettack Daily Security Check | harian 09:00 | thread 12595 | **Ditambahkan 11 Okt** — belum tercatat sebelumnya |
| `f431f7c358b1` | A2A Cloud Health Check | `0 10 * * *` | thread 12595 | **Ditambahkan 11 Okt** — belum tercatat sebelumnya |
| `034116abd040` | **Sync 9router models to config** | `every 30m` | thread 12595 + local | **Baru 11 Okt 2026.** `sync-models-to-config.py`, non-agent. Lihat bagian di bawah |
| `6bef77289daf` | wiki-dropbox | `*/30 * * * *` | `local` | **Ditambahkan 11 Okt** — paket wiki MIRAI |
| `0c82a4b64495` | wiki-librarian | `30 2 * * *` | `local` | Paket wiki MIRAI |
| `59f3d966b912` | wiki-lint | `50 2 * * *` | `local` | Paket wiki MIRAI |
| `67400ef79e74` | wiki-opening-snapshot | `20 2 * * *` | `local` | Paket wiki MIRAI |
| `b5fdcff7dcd3` | wiki-closing-snapshot | `10 3 * * *` | `local` | Paket wiki MIRAI |

**Dihapus dari daftar 11 Okt 2026:** `Pemdi Health Watch` — sudah tidak ada di runtime
(registry lama mencatatnya `paused`). Job `model-status-probe-cron.sh` masih aktif lewat `15d9127ab8b0`.

## Job: Sync 9router models to config (`034116abd040`)

Dibuat 11 Okt 2026 untuk menutup celah yang membuat picker `/model` menampilkan daftar kosong.

**Masalah yang diselesaikan:** jalur chat gateway membaca katalog provider *cache-only*
(`non_blocking_catalogs=True, probe_custom_providers=False`). Provider custom yang bukan endpoint
aktif tidak di-probe live, sehingga saat cache dingin hanya menyisakan `default_model`. Reproduksi:
WARM 9router 141 / huancheng 14; COLD 9router 0 / huancheng 1.

**Perilaku:** menyinkronkan `models:` 9router di `~/.hermes/config.yaml` dengan katalog live, lalu
menghapus entri `provider_models_cache.json` agar picker langsung memakai daftar baru.
`models:` adalah **fallback, bukan pin** — cache hangat menang, jadi keduanya harus dilakukan bersama.

**Guard anti-flapping.** Katalog 9router terukur berflapping `168 ↔ 126` dalam hitungan detik
(provider pixz 83 model keluar-masuk agregat saat upstream-nya error lalu pulih; pixz langsung ke
`api-inference.pixz.dev` stabil di 83, jadi flapping ada di lapisan agregasi 9router). Script membaca
katalog 3× jeda 3 detik dan hanya bertindak kalau **dua bacaan berturut-turut sama**. Katalog yang
masih bergerak → job diam, run berikutnya menangkap nilai stabil. Tanpa guard, job 30 menit akan
mengirim notifikasi ke thread 12595 setiap kali katalog bergoyang.

**Output:** hanya bicara kalau `models:` benar-benar berubah. Tidak ada perubahan → senyap
(exit 0 tanpa stdout). Error → exit 1, dikirim ke `--failure-deliver`.

## Aturan routing

- **Output cron Hermes → thread `12595`** (Cron & Otomasi). Thread 7402 (Serbaguna) hanya untuk flex-thread. Thread 1 (General) hanya untuk interaksi pemilik.
- **Cron dari DM** (dibuat di chat pribadi) → kembali ke DM pemilik.
- **Cron `local`** → hanya tulis ke `~/.hermes/cron/output/`, tidak ada notifikasi Telegram.

### ⚠️ `origin` = konteks PEMBUATAN, bukan maksud

`origin` menyelesaikan ke **thread/sesi tempat job dibuat**, bukan ke tempat job itu "seharusnya"
berada. Konsekuensinya: job yang dibuat dari thread 802 (Research) akan mengirim outputnya ke thread
riset **selamanya**, bahkan setelah tujuannya berubah.

Karena itu, **jangan pakai `origin` untuk job yang tujuannya sudah diketahui** — pakai bentuk
eksplisit `telegram:<chat_id>:<thread_id>[,local]`. Ini pernah membuat job `034116abd040` salah arah
(lihat riwayat di bawah).

## Cara mengubah tujuan cron

```bash
# 1. Ambil ID dari daftar — jangan pernah mengetik ulang dari ingatan
hermes cron list

# 2. Ubah target
hermes cron edit <id-dari-list> --deliver "telegram:-1004204696417:12595,local"
hermes cron edit <id-dari-list> --failure-deliver "telegram:-1004204696417:12595"

# 3. Baca ulang untuk konfirmasi — exit 0 dari edit BUKAN bukti
hermes cron list | grep -A 9 <id>
```

Format `deliver`:
- `telegram:<chat_id>:<thread_id>[,local]` — **bentuk yang dianjurkan**; `,local` menyimpan artefak juga
- `origin` — kirim ke tempat job dibuat (hindari; lihat peringatan di atas)
- `local` — hanya file, tanpa pesan Telegram

**Catatan:** `hermes cron update` bukan verbnya; yang benar `hermes cron edit`. Perubahan target
**tidak butuh restart gateway**.

## Riwayat

- **11 Okt 2026 — job `034116abd040` salah arah, diperbaiki.** Dibuat dengan `--deliver local` +
  `--failure-deliver origin`. `origin` di sini berarti thread 802 (Research) karena job dibuat dari
  sana — output sinkronisasi 9router akan mendarat di thread riset. Diperbaiki ke
  `telegram:-1004204696417:12595,local` dan failure-deliver ke thread yang sama. Konvensi sekarang:
  9 dari 9 job otomasi non-wiki mengarah ke 12595.
- **11 Okt 2026 — tabel routing disinkronkan.** Ditemukan 4 drift dari runtime: DR Snapshot dan
  up-eco-lightfix tercatat `local` padahal thread 12595; Dettack dan A2A tidak tercatat; Pemdi Health
  Watch sudah tidak ada; 5 job wiki belum tercatat. Semua dikoreksi di atas.
- **5 Okt 2026 — thread 12595 dibuat.** Cron output dipindah dari flex-thread 7402 untuk
  memisahkannya dari percakapan serbaguna.
- **24 Sep 2026** — perubahan routing massal. Backup: `~/.hermes/cron/jobs.json.bak-20260924-184243`.

## Catatan

- **Pemintasan:** gateway Hermes membaca `jobs.json` per-turn — perubahan langsung aktif tanpa restart.
- **Cron output tidak masuk riwayat percakapan thread tujuan.** Setiap pengiriman berjalan di sesi
  sendiri dengan frame header/footer, agar pergantian pesan thread utama tetap utuh. Jangan berharap
  job cron menjadi konteks percakapan di thread tujuannya.
