# TELEGRAM-UNIFY — Status: ✅ SUDAH DITERAPKAN

**Diperiksa:** 2026-08-21 (pasca "kerjakan telegram unify")

## Fakta
- Sumber kebenaran: `~/.hermes/config.yaml` → `platforms.telegram.channel_overrides`
- Semua 5 thread SUDAH di-set ke `opencode-zen:nemotron-3-ultra-free`:
  - `1`    (General)      → nemotron-3-ultra-free / opencode-zen ✅ (125 pesan)
  - `802`  (MC-Research)  → nemotron-3-ultra-free / opencode-zen ✅ (86 pesan)
  - `803`  (MC-Programmer)→ nemotron-3-ultra-free / opencode-zen ✅ (7 pesan)
  - `804`  (MC-QA)        → nemotron-3-ultra-free / opencode-zen ✅ (23 pesan)
  - `1172` (Konten Kreator)→ nemotron-3-ultra-free / opencode-zen ✅ (148 pesan)
- Verifikasi ganda: `hermes config get` + `telegram_threads.py` (HERMES_HOME lokal).

## Bug tooling yang ditemukan & diperbaiki
- `scripts/telegram_threads.py` menghardcode `HERMES_HOME=/Volumes/HermesAgent/...` (USB).
  Saat USB tidak ter-mount → `state.db` tidak ditemukan → semua thread salah
  dilaporkan `Inactive / default/default` (false-negative di up-eco).
- FIX: baca `HERMES_HOME` dari env, fallback `~/.hermes`, lalu USB. (commit terpisah)

## Kesimpulan
TELEGRAM-UNIFY **bukan referensi yang belum diterapkan** — sudah applied di config.
Yang belum adalah visibilitas tooling (sekarang diperbaiki). Tidak ada pelanggaran
konstitusi aktif pada model thread Telegram.
