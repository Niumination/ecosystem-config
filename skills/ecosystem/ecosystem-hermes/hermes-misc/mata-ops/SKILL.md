---
name: mata-ops
description: Pull repo MATA dari GitHub & jalankan dashboard lokal :8080.
tags: [mata, repo-ops, pull, localhost, niumination]
---

# MATA Ops — pull & run dari Mac

MATA = watchdog pengadaan (INAPROC). Repo: `~/Desktop/Niumination/labs/mata-aihackfest-2026`.
VM Batch 3 **dinonaktifkan 15 Sep 2026 23.59 WIB** — jalur Kitty/VPS sudah tidak ada. Mac kini
boleh mengerjakan repo ini **atas instruksi user**: membuat snapshot statis, DOX pass, dan deploy
`gh-pages`. Yang tetap absolut: jangan pernah menyentuh atau menginvestigasi VPS (mati), dan jangan
pernah meng-commit kredensial / `mata/config.json` / `mata.db`.

## Aturan keras
1. **Pull = git dari GitHub origin saja.** JANGAN pernah mencoba SSH ke VPS, berburu IP/port/key VPS, atau menginvestigasi akses VPS supaya membantu — kalau butuh sesuatu yang hanya ada di VPS, minta user menjalankannya di Kitty-nya. Repo ini tidak terhubung ke ekosistem (jangan masukkan ke up-eco / sync skill bank).
2. **Commit dari Mac = boleh, tapi hanya untuk artefak.** Snapshot statis, dokumentasi/DOX, dan
   `gh-pages` adalah sah dari Mac. Yang tidak pernah di-commit: `mata/config.json`, `mata/data/mata.db`,
   `mata/output/`, dan seluruh isi kredensial. Sebelum commit: `git status --short` dan `git add <path>`
   spesifik — jangan `git add .`.
3. Pull adalah SATU aksi — setelah pull, laporkan ringkas (HEAD tiap branch, commit baru oneline, working tree clean) lalu berhenti. Jangan lanjut ke aksi lain tanpa diminta.

## Prosedur pull (dari root repo)
```bash
git fetch origin main && git pull --ff-only origin main   # main
git fetch . origin/dev:dev                                 # dev tanpa checkout
cd assets/media && git fetch origin main && git log --oneline -1 && cd ../..   # submodule
git status --short                                         # kosong = clean
```
Pull semuanya = main + dev + submodule (ketiganya di atas).

## Jalankan lokal (branch main)
```bash
cd mata
uv venv .venv                                              # PEP 668 — pip sistem ditolak
uv pip install --python .venv/bin/python -r requirements.txt   # requests, fpdf2, openpyxl
.venv/bin/python run.py web -p 8080                        # background
curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:8080/   # harus 200
```
Cek port dulu `lsof -nP -iTCP:8080 -sTCP:LISTEN`. Stop: kill proses background, verifikasi port bebas lagi.

## Perilaku lokal yang NORMAL (jangan salah diagnosa)
- Badge **MODE: SYNTHETIC** benar di Mac: `_mode()` (mata/web.py) hanya menandai LIVE jika tabel `announcements` di `data/mata.db` berisi record `INP-*` (koleksi live hanya pernah berjalan di VPS); mata.db Mac = 48 record demo.
- **Angka produksi (662 paket TA2026, 171 penyedia, Rp 134,5 M) tetap tampil** — bersumber snapshot `data/realisasi_2026_full.json` / `rup_2026_full.json` yang di-commit, bukan mata.db. Dashboard menggabungkan: panel analisis = produksi, panel pantau per-paket = demo. Ini desain, bukan bug.
- **`/api/health` `ok:false` lokal** — mengecek `mata.service`/`mata-web.service` (systemd) yang memang tidak ada di Mac.
- Dashboard lokal sepenuhnya LIVE butuh `run.py live-collect` (jaringan ke INAPROC publik) — hanya atas perintah eksplisit user.
- **`run.py web` cukup stdlib** — dashboard web tidak butuh venv/`requirements.txt` (itu untuk
  kolektor & PDF). `python3 mata/run.py web -p <port>` langsung jalan.

## Jalankan cabang lain tanpa mengusik `main` (worktree)

`main` dan `dev` berbeda jauh (`dev` jauh lebih baru). Untuk menyalakan dashboard dari cabang lain
(atau membandingkan UI) tanpa mengotori working tree:

```bash
git worktree add /tmp/mata-dev-wt origin/dev   # atau <rev> apa pun
cd /tmp/mata-dev-wt && python3 mata/run.py web -p 8181
# ...selesai...
pkill -f "run.py web -p 8181"
git worktree remove /tmp/mata-dev-wt --force   # bersihkan; git worktree list harus kosong
```

Jangan pindah cabang di repo utama untuk ini — `git checkout` bolak-balik meninggalkan file sisa
dan membuat status kotor.

## Dashboard setia-hasil-produksi: pulihkan `mata.db` dari backup VPS

`/api/status`, `/api/flags`, dan `/api/analisis` dibaca dari **SQLite `mata.db`** (`db.read_flags()`,
`db.load_records()`) — bukan dari JSON yang di-commit. Tanpa `mata.db`, dashboard tetap 200 tapi
angka indikator kosong. Data produksi terakhir ada di submodule backup:
`assets/media/mata-final-backup-20260915.tgz` (≈37 MB).

```bash
git submodule update --init assets/media      # submodule bisa belum ter-checkout
mkdir -p /tmp/mata-restore && cd /tmp/mata-restore
tar -xzf <repo>/assets/media/mata-final-backup-20260915.tgz   # ekstrak ke-1
tar -xzf mata-backup-FINAL-20260915.tgz                       # ekstrak ke-2 — WAJIB
# → root/Arck4li-AIHackfest/mata/data/ · /etc/systemd · /etc/cron.d
```

> **Perangkap:** berkas itu **tar bersarang dua lapis** — ekstraksi pertama hanya menghasilkan tar
yang sama di dalamnya (`tar -tzf` menampilkan 1 entri). Ekstrak dua kali; setelah itu 1706 entri.

Salin ke worktree yang dituju: `mata.db`, `status.json`, `flags_latest.json`, `kutipan.json`,
`realisasi_20{25,26}_full.json`, `rup_20{25,26}_full.json`, plus cache `iklim_/inaproc_/sapa_/spse_cache.json`.

Dengan `mata.db` produksi terpasang, angka jadi final (662 paket · 14 indikasi · 3 tinggi) dan
catatan "mata.db Mac = 48 record demo" di atas tidak berlaku lagi.
