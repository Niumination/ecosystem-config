# Temuan: Akar Masalah Instalasi Hermes — Shim Python 3.14 Cacat

**Tanggal:** 8 Okt 2026
**Sumber temuan:** Investigasi kegagalan `sync-all.sh --drill` (repo `niumination-restore`)
**Untuk:** thread #General (tugas rekonsiliasi fork `hermes-agent`), pemilik

---

## Ringkasan

Tiga instalasi `hermes` pernah ada di mesin ini. Dua di antaranya menunjuk ke runtime
Python 3.14 yang **hanya berisi pip** (1 package — tanpa yaml, tanpa openai-sdk), sehingga
setiap pemanggilan `hermes` lewat PATH di shell non-interaktif menghasilkan:

```
ModuleNotFoundError: No module named 'yaml'
```

**Akar masalah:** `hermes_cli/_launchers.py` tidak ada di branch `main`. File ini hanya ada
di `upstream/main` dan `reconcile-upstream-20261007` — branch reconcile yang **belum
selesai**. Saat `hermes update`/sync menulis ulang launcher pada 7 Okt (12:56), ia memilih
store Python dari `~/.hermes/tools/` (bundle tool untuk node/uv/ffmpeg/chromium), yang
kebetulan adalah Python 3.14 — melanggar `requires-python = ">=3.11,<3.14"`.

---

## Bukti

### 1. Tiga instalasi hermes

| # | Path | Python | yaml | OpenAI SDK | Status |
|---|---|---|---|---|---|
| 1 | `~/src/hermes-agent/.venv/bin/hermes` | 3.11.16 | ✓ | ✓ 2.24.0 | sehat — gateway pakai ini |
| 2 | `~/.local/bin/hermes` | — (shim) | — | — | shim → #3 |
| 3 | `~/src/hermes-agent/.hermes/bin/hermes` | 3.14.7 | ✗ | ✗ | rusak |

Reproduksi langsung:

```
$ /Users/zaryu/.local/bin/hermes --version
Hermes Agent v0.21.1 · Python: 3.14.7 · OpenAI SDK: Not installed

$ /Users/zaryu/.local/bin/hermes backup
ModuleNotFoundError: No module named 'yaml'
```

### 2. Runtime 3.14 adalah bundle tool, bukan runtime Hermes

```
$ ls ~/.hermes/tools/python-3.14.7.../lib/python3.14/site-packages/
README.txt  pip  pip-26.2.1.dist-info        ← 1 package

$ ls ~/src/hermes-agent/.venv/lib/python3.11/site-packages/ | grep -c dist-info
115                                   ← venv utuh
```

Python 3.14 ini tercatat di `~/.hermes/tools/facts.json` sebagai package pendamping
node/uv/ffmpeg/chromium/ripgrep — **bukan** runtime Hermes. Mekanisme `resolve_store_python()`
di `_launchers.py` membaca `facts.json` inilah yang mengambilnya.

### 3. `_launchers.py` hilang dari main — divergensi reconcile

```
$ git ls-tree main -- hermes_cli/_launchers.py
(kosong)

$ git ls-tree reconcile-upstream-20261007 -- hermes_cli/_launchers.py
100644 blob 35d53d3b...  hermes_cli/_launchers.py

$ git ls-tree upstream/main -- hermes_cli/_launchers.py
100644 blob 1e15625c...  hermes_cli/_launchers.py
```

Divergensi main vs reconcile-upstream: **568 file berubah, 7946 commit unik di main**.

### 4. Timeline 7 Okt (semua mtime)

```
11:22  python-3.14 runtime dibuat (tool bundle, facts.json)
12:55  commit terakhir reconcile-upstream (01637af "port P5 to has_durably_delivered_text")
12:56  shim .hermes/bin/hermes + .hermes/bin/hermes-acp + ~/.local/bin/hermes ditulis
12:57  __pycache__/_launchers.cpython-314.pyc   ← shim pernah dijalankan
```

Shim ditulis **1 menit setelah** commit terakhir reconcile — konsisten dengan `hermes update`
yang berjalan di main tanpa `_launchers.py`.

### 5. pyproject melarang 3.14

```
$ grep requires-python ~/src/hermes-agent/pyproject.toml
requires-python = ">=3.11,<3.14"
```

---

## Dampak (yang sudah terjadi)

- **`sync-all.sh --drill` gagal 4×** di langkah "hermes backup" — penyebab seluruh kegagalan
  snapshot DR malam ini. Bukan venv, bukan disk, bukan race condition (tiga hipotesis
  pertama yang terbukti salah selama investigasi).
- **`hermes doctor` hang** — jatuh ke shim 3.14 lewat PATH.
- **Backup manual selalu sukses** (~980MB, EXIT=0) karena dipanggil dengan path absolut ke
  venv — inilah yang menyesatkan diagnosis awal.

## Yang TIDAK terkena

- **Gateway tetap jalan normal** — launchd memakai `.venv/bin/python` eksplisit.
- **Cron `run_job` inline** — `from run_agent import AIAgent`, bukan subprocess. Fallback
  `shutil.which("hermes")` di `scheduler_delivery.py:706` hanya untuk bot-chat delivery;
  0 dari 8 job terjadwal memakai mode itu.

---

## Tindakan yang sudah diambil (8 Okt)

1. **Backup 3 shim** ke `vault/_arsip-sensitif/shim-3.14-backup-20261008/` (mode 600)
2. **Hapus shim rusak** — `~/.local/bin/hermes`, `.hermes/bin/hermes`, `.hermes/bin/hermes-acp`
3. **`build-l1-release.sh` di-pin** ke venv eksplisit (commit `ebcbdc2` di repo ekosistem)
4. **Snapshot 8 Okt sudah ter-commit** (`efb739e` di `niumination-restore`)

Hasil verifikasi setelah pembersihan:

```
$ command -v hermes
/Users/zaryu/src/hermes-agent/.venv/bin/hermes

$ bash -c 'command -v hermes && hermes --version'
Python: 3.11.16
OpenAI SDK: 2.24.0
```

---

## Yang perlu thread #General kerjakan

Shim yang dihapus **akan ditulis ulang** oleh `hermes update` berikutnya — kemungkinan besar
kembali ke 3.14 yang sama, karena `_launchers.py` masih hilang dari `main`. Perbaikan
sesungguhnya ada di repo `hermes-agent`, bukan di mesin ini:

1. **Selesaikan `reconcile-upstream-20261007`** hingga `_launchers.py` masuk ke `main`
   (atau cherry-pick file itu sendiri bila ingin cepat)
2. **Setelah merge, jalankan `hermes update`** — launcher akan menulis shim yang benar
3. **Verifikasi** `command -v hermes` menunjuk ke runtime yang punya yaml + openai-sdk

Tanpa langkah 1, penghapusan shim ini hanya bersifat sementara.
