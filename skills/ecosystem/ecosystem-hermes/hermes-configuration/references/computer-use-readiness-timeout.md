# computer_use "daemon did not become ready" — lambatnya probe socket

> **AKHIRNYA TERJELASKAN (28 Sep 2026, 11:0x):** akar masalahnya versi driver, bukan
> timeouts. `hermes computer-use install --upgrade` (0.22.0 → 0.30.2) menurunkan probe dari
> **5.76–13.08s menjadi 0.12s konsisten** (5/5 probe). 48–100× lebih cepat. Patch timeout
> (`673f3c3fa2`) jadi tidak lagi dibutuhkan sebagai perbaikan — hanya sisa insurance.
> **Coba upgrade driver DULU** sebelum menyentuh konstanta timeout.

**Date:** 28 Sep 2026
**Symptom:** setiap panggilan `computer_use` gagal dengan
`computer_use backend unavailable: embedded cua-driver startup timed out: daemon did not become ready`
—even though `hermes computer-use doctor` reports every permission green.

## Diagnosis lebih dulu — jangan mulai dari proses

Dua jalur yang sering disalahartikan:

| Dugaan | Kenyataan |
|---|---|
| proses `cua-driver serve` orphan menumpuk | bukan penyebab; itu sisa sebelum restart. Ketiganya terdaftar sah di `launchctl` sebagai `application.com.trycua.driver.*` — kill hanya memicu respawn |
| permission TCC / binary hilang | bukan; `doctor` hijau semua, binary 0.22.0 jalan |
| wrapper `cua-driver-hermes` yang force HOME salah | bukan; wrapper dan path app langsung sama-sama bisa start |
| `CAMOFOX_URL` ter-archive | itu untuk browser, bukan computer_use |

**Reproduksi langsung ke kode yang sama** — satu-satunya jalur yang perlu diuji:

```bash
cd ~/src/hermes-agent && .venv/bin/python -c "
import time
from tools.computer_use import cua_backend_driver as drv
from tools.computer_use.cua_backend_daemon import _EmbeddedCuaDaemon
d = _EmbeddedCuaDaemon(drv.resolve_cua_driver_cmd(), 'unrestricted')
t = time.monotonic()
try:
    d.start(); print(f'START OK in {time.monotonic()-t:.2f}s')
except Exception as e:
    print(f'START FAIL in {time.monotonic()-t:.2f}s: {e}')
" 2>&1 | grep -v 'env passthrough'
```

Config `computer_use.permission_mode` harus `unrestricted` atau `bounded` — `standard` ditolak constructor (`embedded permission override supports unrestricted or bounded only`). Mode `standard` dipilih otomatis saat approval bypass aktif.

## Akar masalah (SEMU AKHIR): driver 0.22.0, bukan konstanta

Konstanta timeout cuma gejala, bukan akar. Bukti setelah upgrade:

| driver | probe `status --socket` |
|---|---|
| 0.22.0 | 5.76 – 13.08s (5 probe: 8.00 12.25 13.08 9.46 5.56) |
| **0.30.2** | **0.12s (5/5 probe, tanpa variasi)** |

`hermes computer-use install --upgrade` memang perlu — driver belum di-upgrade sejak Jun 2026 (`/usr/local/bin/cua-driver` → app, mtime 1:22). Hermes
sudah memberi tahu sejak 09:58:36 (`cua-driver 0.30.2 is available (you have 0.22.0)`).

## Gejalanya: probe lebih lambat dari plafonnya

`cua-driver status --socket` di host ini:

```
tanpa daemon hidup : 0.03s   (balas "daemon is not running")
dengan daemon hidup: 5.76–13.08s   (5 probe berturut: 8.00 12.25 13.08 9.46 5.56)
```

Perhatikan — cek pertama yang dilakukan bisa **lebih lambat dari Budget pun**, tapi error-nya
identik, karena `_run_quiet(..., swallow=_QUIET_ERRORS)` mengembalikan `None` pada
`TimeoutExpired`, lalu loop tetap jalan dan tidak pernah melihat daemon siap.

Plafon lama menelan seluruh start budget:

```python
_PROBE_TIMEOUT_SECONDS = 20.0    # baru — lebih dari probe terburuk yang terukur
_START_TIMEOUT_SECONDS  = 15.0 → 60.0
probe = _run_quiet([...], timeout=2.0)   # lama — satu probe 13s langsung habis
```

Satu baris tidak cukup: dengan start budget 15s, satu probe 13 detik menghabiskan kuota
sebelum sempat probe kedua. Perlu dua.

## Verifikasi

```bash
cd ~/src/hermes-agent
# 1. START OK, catat waktunya
# 2. test suite
scripts/run_tests.sh tests/tools/test_computer_use_cua_0_9.py \
                    tests/tools/test_computer_use_cua_macos_identity.py \
                    tests/tools/test_computer_use_cua_backend_linux.py
# 3. restart gateway DARI SHELL LUAR (konstanta dibaca saat import modul)
# 4. uji nyata
computer_use(action="list_apps")            # count > 0
computer_use(action="capture", app="<app>", mode="ax")
```

Commit lokal: `673f3c3fa2` (+8 −2, 1 file).

## Catatan efisiensi — jangan ulangi riset

- `.venv` tidak punya pytest. Pasang sekali: `uv pip install --python .venv/bin/python pytest pytest-asyncio`
- `scripts/run_tests.sh` menolak jalan tanpa pytest — pesan "skipping venv without pytest", bukan failure test
- `process_manage` tidak ada sebagai tool; pakai `terminal(background=True)`
- `hermes gateway restart` dari dalam proses gateway **ditolak sistem** (bukan kebijakan): `Blocked: … cannot restart … from inside the gateway process`. Tetap perlu shell luar.

## Yang tidak boleh dilakukan

- Jangan `--permission-mode unrestricted` tanpa `--dangerously-bypass-approvals`; driver menolak startup dengan `authorization startup error: permission mode unrestricted requires --dangerously-bypass-approvals at trusted daemon startup`
- Jangan deserialize `capture mode=ax` tanpa/app yang spesifik: mode `ax` membaca AXMenuBar global termasuk daftar file terbaru user
