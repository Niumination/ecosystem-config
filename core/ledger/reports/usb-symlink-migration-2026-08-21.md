# Laporan Migrasi USB — Symlink & Hardcoded Path

**Tanggal:** 2026-08-21 · **Operator:** zaryu · **Sesi:** Wave 2 (post "perbaiki dokumentasi + cek symlink USB")

## Ringkasan Eksekutif
Ditemukan **1 symlink aktif** yang menunjuk ke USB (`/Volumes/HermesAgent`) dan **rusak**
(target tidak ada karena USB tidak ter-mount). Plus **3 script runtime** yang menghardcode
path USB — sudah diperbaiki agar tidak crash saat USB lepas. Artefak historis (docs/references,
archive/backup) yang masih menyebut USB **tidak diubah** (bukan runtime).

## 1. Symlink ke USB (scan `find -type l`)
| Path | Target | Status | Tindakan |
|------|--------|--------|----------|
| `apps/mac-web-dashboard/hexstrike/venv/bin/python3.11` | `/Volumes/HermesAgent/HermesAgentUSB/.cache/runtimes/macos-x64/python/bin/python3.11` | 🔴 BROKEN (USB tidak mount) | **MIGRASI LANJUTAN** — lihat §3 |

Semua symlink lain di root (dotfiles java/spell, Pemdi `.claude/skills/*`) rusak tapi
**bukan** pointing ke USB — mereka relative (`../../.agents/skills/...`) dan milik bot arena
(Pemdi PR#4), bukan setup kita. Dicatat di §4 sebagai non-USB broken.

## 2. Hardcoded USB di Script Runtime (SUDAH DIPERBAIKI)
| Script | Baris | Masalah | Fix |
|--------|-------|---------|-----|
| `scripts/telegram_threads.py` | 11 | Hardcode `HERMES_HOME=/Volumes/...` → false-negative `default/default` | Baca env `HERMES_HOME`, fallback `~/.hermes`, lalu USB |
| `scripts/kanban-sync.sh` | 12 | DB path USB + `exit 1` jika tidak ada | Env `KANBAN_DB`/`HERMES_HOME`, fallback lokal; guard `if [ -n "$DB" ]` |
| `scripts/generate-ecosystem-json.py` | 18 | DB path USB + `sqlite3.connect(DB)` crash | Env-first, `DB=None` → BACKLOG-only mode (diverifikasi jalan) |

Verifikasi: ketiga script dijalankan **tanpa USB mount** → exit 0 (BACKLOG-only).

## 3. Rencana Migrasi `hexstrike/venv` (butuh USB)
`apps/mac-web-dashboard/hexstrike/venv` adalah virtualenv yang **seluruh binarinya**
menunjuk ke python USB. Saat USB lepas → venv mati (`python3.11` broken).

**STATUS: ✅ SELESAI 2026-08-21 (USB dipasang)**
- `rm -rf venv && /usr/local/bin/python3 -m venv venv` (venv lokal penuh)
- `pip install flask mcp aiohttp psutil requests bs4` (real deps; selenium/mitmproxy/pwn/angr di-stub oleh launch_server.py)
- Verifikasi: `venv/bin/python3.14 → /usr/local/opt/python@3.14/bin/python3.14` (LOKAL)
- `import flask, mcp, aiohttp, psutil, requests, bs4` → ALL_IMPORTS_OK
- Server test: Flask jalan di `127.0.0.1:8888` (HTTP 404 = responsive), process pool workers started
- **0 USB symlink tersisa** di venv
- venv gitignored (`hexstrike/venv/`) → tidak di-commit, benar

## Status Akhir
- ✅ Script runtime tidak lagi bergantung USB (defensive, no-crash).
- ✅ 1 symlink USB rusak (`hexstrike/venv`) → **SUDAH dimigrasi ke venv lokal** (USB dipasang).
- ✅ Dokumentasi salah (TELEGRAM-UNIFY false-diagnosis) dikoreksi + STATE.yaml disinkron.
