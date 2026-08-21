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
**Tindakan lanjutan (perlu USB dipasang):**
1. Pasang USB `/Volumes/HermesAgent`.
2. Recreate venv lokal: `cd apps/mac-web-dashboard/hexstrike && rm -rf venv && python3 -m venv venv && venv/bin/pip install -r requirements.txt` (jika ada).
3. Verifikasi: `venv/bin/python -c "import sys; print(sys.executable)"` → harus `/Users/zaryu/...` bukan `/Volumes/...`.
4. Atau jika hexstrike tidak dipakai lagi → hapus folder (arsip ke `archive/`).

**Catatan:** Saya tidak recreate sekarang karena butuh USB (Anda bilang akan pasang jika perlu).
Saya hanya laporkan; eksekusi migrasi menunggu USB atau konfirmasi hapus.

## 4. Broken Symlinks Non-USB (dicatat, bukan kita)
- `dotfiles/zaryu-terminal-dotfiles/bin/.local/bin/java` → Homebrew openjdk (path berubah)
- `dotfiles/zaryu-terminal-dotfiles/nvim/.config/nvim/spell` → `~/spell` (tidak ada)
- `apps/PemdiAcehTengah/.claude/skills/*` (20 item) → `../../.agents/skills/*` (milik bot arena)

## 5. Artefak Historis (TIDAK diubah)
`docs/references/niumination-rebuild-v2-2026-08-18/**` dan `archive/backup/**` masih
menyebut `/Volumes/HermesAgent` — itu dokumentasi migrasi masa lalu, bukan runtime.
Biarkan sebagai arsip.

## Status Akhir
- ✅ Script runtime tidak lagi bergantung USB (defensive, no-crash).
- 🔴 1 symlink USB rusak tersisa (`hexstrike/venv`) → migrasi lanjutan butuh USB.
- ✅ Dokumentasi salah (TELEGRAM-UNIFY false-diagnosis) dikoreksi + STATE.yaml disinkron.
