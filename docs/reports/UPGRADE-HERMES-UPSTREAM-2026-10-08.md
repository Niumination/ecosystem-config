# Upgrade Hermes ke Upstream Terbaru — 8 Oktober 2026

## Ringkasan

Instalasi Hermes di Mac di-upgrade dari fork yang tertinggal **17.618 commit** ke upstream
`b1a39a1b1b` (8 Okt 2026 00:49 -0700) tanpa kehilangan 5 patch lokal maupun konfigurasi user.

## Masalah Awal

1. `hermes` tidak ditemukan di terminal interaktif — `~/.local/bin/hermes` (shim) dihapus 7 Okt,
   `.zshrc` tidak memuat `.venv/bin`.
2. `main` fork berada 17.618 commit di belakang `upstream/main` dan 5 commit di depan (patch lokal),
   sehingga `git pull` langsung akan menimpa patch.

## Yang Dilakukan

### 1. Perbaikan langsung "hermes not found"

- Dibuat symlink `~/.local/bin/hermes -> ~/src/hermes-agent/.venv/bin/hermes` (`.local/bin` sudah
  ada di PATH `.zshrc`).
- Shebang shim `.venv/bin/hermes` menunjuk ke `.venv/bin/python3` (Python 3.11.16) — bukan
  Python 3.14 runtime-tool yang sebelumnya menjadi akar masalah.

### 2. Pembersihan

- 15 file sampah test (`MagicMock/`, `rite-channel-prompt.py`) ter-unstage dan dihapus dari disk.
- Working tree kembali bersih.

### 3. Upgrade via cherry-pick (bukan merge)

Dibuat branch `upgrade-upstream-20261008` dari `upstream/main`, lalu di-cherry-pick 5 commit patch
dari `main` lama:

| Patch | Commit | Hasil |
|---|---|---|
| P1 free_only (`/model` picker) | `2160f78d84` | bersih |
| P2 cua timeout 20/60s | `6872e8e876` | bersih |
| P3 notif gateway B. Indonesia + bounded-wait | `0da89439d3` | **konflik** — resolved manual |
| P4 suppress stale final | `e1b7e2e6d1` | bersih |
| P5 prevent duplicate final | `c6b22d0edc` | bersih |

Konflik P3 di `gateway/run_notifications.py` (3 area) di-resolve dengan menggabungkan kedua sisi:
kode upstream baru (`utf-8-sig`, per-profile loop, `_free_tier_startup_line`, dedup
`_served_home_channel_transports`) + patch lokal (`_wait_for_send_paths_healthy()`, teks Bahasa
Indonesia). Syntax check OK setelah resolve.

### 4. Sinkronisasi environment

- `hermes pm install` — tools terpasang (ffmpeg, node, python, ripgrep, venv, agent-browser,
  cua-driver).
- `hermes pm repair` — dependency environment diperbaiki.
- Import test: httpx 0.28.1, openai 2.24.0, yaml 6.0.3, aiohttp 3.14.3, telegram 22.8,
  fastapi 0.133.1, uvicorn 0.41.0, pydantic 2.13.4 — semua OK.
- Venv: Python 3.11.16.

### 5. Swap main

- Backup ref `backup-main-pre-upgrade-20261008` dibuat ke `2160f78d84` (main lama).
- `git merge --ff-only` gagal (7946 carried commit vs 2) — diganti `git reset --hard
  upgrade-upstream-20261008` di atas `main`.
- `git push --force-with-lease origin main` — fork GitHub (`Niumination/hermes-agent`) ter-update.

## Verifikasi

- `main` = `4aef7422e7`, **0 commit di belakang upstream**, 5 commit di depan (patch lokal).
- 5 patch terverifikasi ada di working tree (grep count > 0 untuk semua simbol).
- Config utuh: `config.yaml` (32 KB, `free_only: true`), `.env`, `auth.json`.
- Test suite: 32 test di 2 file patch-terkait (`test_stream_final_contract.py`,
  `test_model_catalog.py`) — **32 passed, 0 failed**.
- Smoke test import 5 module ter-patch — semua OK.
- `hermes --version`: v0.21.5+9147.g4aef742, install method git.

## Update 17:39 — Sinkronisasi 3 Commit Upstream (Rebase)

Setelah laporan ini ditulis, `hermes --version` di terminal user menunjukkan `Python: 3.14.7` dan
"Update available". Investigasi menemukan:

- **`Python: 3.14.7` bukan masalah.** Angka itu dilaporkan dari environment PM
  (`~/.hermes/installs/.../venv/`, Python 3.14.7), sedangkan `.venv` repo adalah Python 3.11.16
  yang benar sesuai `requires-python = ">=3.11,<3.15"`. Ini hanya metadata, bukan shim rusak.
- **"Update available" = 3 commit baru** di upstream (`b1a39a1b1b..0240fa4a84`) — semuanya di
  `apps/desktop/`, `.github/workflows/nix.yml`, `scripts/msix-shared.mjs`, dan docs. **Tidak
  menyentuh file patch mana pun.**
- **`hermes update` DIHINDARI.** `hermes_cli/update_cmd.py:911` memakai `git reset --hard` ke
  `origin/main` saat HEAD bukan ancestor target — ini akan membuang 5 patch lokal (diparkir ke
  ref backup yang kedaluwarsa). Karena 3 commit bersih, diambil secara manual saja.

Yang dilakukan:

```
git fetch upstream main
git rebase upstream/main   # fast-forward 5 patch di atas 3 commit baru
git push --force-with-lease origin main
```

Rebase 5/5 sukses **tanpa konflik**.

### Verifikasi tambahan

- `main` = `2aaa1c5e92`, **0 commit di belakang upstream**, 5 commit di depan (patch).
- 5 patch: grep count sesuai untuk semua simbol.
- Smoke test import 5 module: OK. Syntax check 5 file: OK.
- Test suite: **32 passed, 0 failed** (2 file patch-terkait), 9.7s.
- Push ke fork: `4aef7422e7...2aaa1c5e92 main -> main (forced update)`.

## Catatan

- Gateway yang sedang jalan masih memakai kode lama; perlu restart untuk memakai kode baru.
- Backup ref `backup-main-pre-upgrade-20261008` bisa dihapus setelah verifikasi beberapa hari.
- `hermes update` berikutnya aman: `main` sudah berbasis upstream terbaru, jadi updater tidak akan
  menulis shim Python 3.14 lagi.
