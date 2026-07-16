# Migrasi Hermes Portable → Native macOS

## Gambaran Besar

**Tujuan:** Memindahkan instalasi Hermes Agent dari USB portable (`/Volumes/HermesAgent/HermesAgentUSB/`) ke native di internal Mac (`/Users/zaryu/.hermes/`).

**Alasan:**
- Performa lebih baik (USB 3.0 vs internal NVMe)
- Latensi lebih rendah (I/O USB bottleneck)
- Tidak bergantung pada koneksi/keberadaan USB
- Ekosistem lebih stabil untuk upgrade ke v0.18.0+

**Risiko Utama:**
- 🔴 15GB data harus dipindah utuh (239MB state.db, 12GB home/, 1.3GB kanban/)
- 🔴 Semua path absolut di config mengandung `/Volumes/HermesAgent/` — harus dimigrasi
- 🔴 Gateway state, auth.json, session DB sensitif — korup = data hilang
- 🔴 Cron job scripts, MCP server paths, launchd plists — semuanya perlu update path

**Prinsip:** *Copy, verify, switch — jangan delete source sampai native confirmed working.*

## Struktur Dokumen

| Dokumen | Isi |
|---------|-----|
| `01-inventory.md` | Daftar lengkap semua aset yang harus dipindah |
| `02-migration-steps.md` | Langkah demi langkah eksekusi migrasi |
| `03-rollback-plan.md` | Recovery plan jika migrasi gagal |
| `04-post-migration.md` | Verifikasi dan konfirmasi after-migration |
| `05-dependency-map.md` | Peta dependensi antar komponen Hermes |

## Status

📅 **Dibuat:** 06 Juli 2026
🔄 **Status:** Planning — BELUM dieksekusi
🎯 **Target Hermes version:** v0.16.0 (saat migrasi) — atau nanti setelah v0.18.0 stabil
