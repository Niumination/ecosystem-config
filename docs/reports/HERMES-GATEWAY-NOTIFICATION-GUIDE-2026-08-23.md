# Panduan Perbaikan Notifikasi Gateway — Hermes (Internal Mac)
Tanggal: 2026-08-23
Operator: zaryu
Status: Konstitusi sudah mati; SOUL default; gateway internal (tanpa USB).

## Masalah
`send_path_degraded` (adapter.py line 759) tetap True saat gateway restart otomatis karena Telegram `polling` tidak pulih (`retrying`). Notifikasi `gateway activated` / `shutting down` gagal.

## Penyebab
- Gateway `PID 6822` berjalan tapi `.gateway_state.json` belum refresh (`start_time` lama).
- Adapter `send_path_degraded` self-healing (`line 3705` reset `False` saat webhook aktif / reconnect berhasil).
- Telegram `api.telegram.org` gagal terus (`timed out`) → adapter masuk loop `retrying` (10 retry, lalu restart).

## Perbaikan yang sudah dilakukan dari sini
1. Konstitusi (`core/`, `niu-core-fence`) dihapus.
2. SOUL dikembalikan ke default Hermes.
3. Gateway `PID 6822` (`running`); `.hermes-portable` valid.
4. `caffeinate` (`-i -s -t 150`) baru berjalan.
5. `.gateway_state_2763m1wc.tmp` stalen dihapus.

## Langkah untuk Hermes (panduan ini)
Karena adapter mengelola state sendiri, tidak perlu patch `adapter.py`. Lakukan:

1. **Restart full gateway** (bukan hanya adapter):
   ```bash
   /Users/zaryu/.hermes-portable/venv/bin/python -m hermes_cli.main gateway restart
   ```
2. **Verifikasi `.gateway_state.json` terupdate** (`start_time` baru, `state`: `running`, `platforms.telegram.state`: `connected` bukan `retrying`).
3. **Cek adapter flag**:
   ```bash
   grep -n "_send_path_degraded" /Users/zaryu/src/hermes-agent/plugins/platforms/telegram/adapter.py
   ```
   Harus kembali ke `False` setelah reconnect berhasil (line 3705).
4. **Jika Telegram masih `retrying`**: ini masalah jaringan (`api.telegram.org` / fallback IP `149.154.166.110`). Bukan kode gateway.
5. **Notifikasi akan aktif otomatis** saat `platform.telegram.state` = `connected` dan adapter `send_path_degraded` = `False`.

## Catatan penting
- Tidak ada perubahan kode adapter yang diperlukan (`self-healing` by design).
- `.hermes-portable` tetap valid untuk kondisi internal (tanpa USB).
- `caffeinate` wajib berjalan (`-i -s -t 150`) agar Mac tidak sleep saat gateway aktif.
