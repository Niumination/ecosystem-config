# docs/references/ — Arsip Studi & Referensi

> **Peran folder ini:** arsip studi/analisis eksternal dan draft keputusan — **bukan** registry hidup.
> Registry yang di-regenerate (skill-registry, project-catalog, deployment-status, dsb.) ada di **`docs/registry/`**.
>
> ⚠️ **Jangan buat folder `docs/reference/` (singular).** Nama itu dihapus 18-Agu-2026; regresi 30-Agu-2026 (DOX v4.1) sudah diperbaiki 16-Sep-2026.

**Dibersihkan terakhir:** 2026-09-16 · **Total:** 73 file · **Dibuat oleh:** konsolidasi folder referensi (lihat `docs/reports/RENCANA-KONSOLIDASI-REFERENSI-2026-09-16.md`)

## Struktur

| Lokasi | Isi | Catatan |
|---|---|---|
| **`archive/`** | 12 entri — snapshot rekonstruksi, config lama, tracker superseded, draft unsealed, studi lama | Bukti eksplisit: nama folder mengandung `archive`/`stale`, atau dinyatakan arsip/superseded/draft |
| **`drafts/`** | ❌ dihapus 5 Okt 2026 — isi dipindah ke `archive/` |
| **(root)** | Studi/keputusan yang masih relevan + dokumen operasional | Termasuk file yang **ambigu** (sengaja tidak diarsipkan) |

### Isi `archive/`

| Entri | Alasan diarsipkan |
|---|---|
| `niumination-rebuild-2026-08-18/` (13 file) | Snapshot penuh rekonstruksi 18 Agu — copy reference, BUKAN live |
| `hermes-config-penutup-archive/` (3 file) | Config lama; berisi `MIGRASI.md` (catatan historis, tidak diedit) |
| `hermes-config-arena-archive/` (1 file) | Zip config arena v4 — di-`.gitignore` (`*.zip`), ada di disk saja |
| `stale-hermes-config-2026-08-20/` | Nama menyatakan *stale* |
| `migration-portable-to-native/` (6 file) | Log migrasi portable → native (selesai) |
| `STATUS-REFERENSI-2026-08-13.md` | Tracker lama, sudah di-supersede |
| `ekosistem-status.md` | Audit 5 Agu 2026 — digantikan `docs/reports/ECOSYSTEM-STATUS-*.md` |
| `ai-memory-collection.md` | Koleksi 16 Jul 2026, path di luar ekosistem |
| `niumination-model-selection/` (7 file) | Draft OPSI-1 & OPSI-2 — unsealed, tidak dipakai (D-0004 yang sealed) |
| `observer-ecosystem-integration/` (6 file) | Blueprint Observer AI — tidak pernah dieksekusi |
| `munder-difflin-reference.md` | Studi Munder Difflin — tidak di-adopsi |
| `analisis-optimalisasi-hermes-2026-08-18.md` | Analisis Hermes 18 Agu — sebagian sudah diterapkan |

## ⚠️ Perlu tindakan pemilik

- **`akun-login.md`** (di root) — kemungkinan memuat daftar kredensial. **Perlu dipindah ke `vault/`** (aturan Secrets & PII: kredensial tidak disimpan sebagai dokumentasi biasa). Belum dipindah karena keputusan pemilik; isinya tidak diperiksa oleh agent.

## File di root yang sengaja TIDAK diarsipkan (ambigu)

Menunggu keputusan pemilik — tidak ada bukti eksplisit untuk mengarsipkan:

- `second-brain-plan.md` vs `second-brain-plan-v2.1.md` — dua versi, tanggal sama (9 Jun 2026)
- `PLAN_RESTRUKTURISASI_PEMDIACEHTENGAH.md` — proyek sudah jalan; relevansi rencana belum dipastikan
- `SHORTCUTS.md`, `VAULT-SETUP.md`, `JCODE-SAFETY-PROTOCOL.md`, `INSTRUKSI_UNTUK_HERMES.md` — dokumen operasional
- `niu-dash-redesign/`, `terax-ai-analysis/`, `xero-dotfiles-docs/` — studi per-repo

## Cara menambah

1. Studi/analisis baru → simpan di **root** `docs/references/<nama-bermakna>-<YYYY-MM-DD>.md`
2. Registry/status yang di-regenerate → **`docs/registry/`**, bukan di sini
3. Kalau sebuah dokumen digantikan dokumen lain → pindah ke `archive/` dan sebut penggantinya di commit message

---

*Index ini dirawat manual. Perbarui saat ada pemindahan besar.*
