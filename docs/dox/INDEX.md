# DOX — Index Dokumentasi Niumination

**Dibuat:** 2026-08-22 · **Sumber:** filesystem `docs/` (184 file, terverifikasi)
**Tujuan:** Peta tunggal seluruh dokumentasi di `docs/` agar tidak ada file yang "tersesat".

---

## 📂 Struktur `docs/`

| Folder | Isi | Status |
|--------|------|--------|
| `docs/dox/` | **Index ini + analisis dox** (joy-connect-for-mac, trancast-protocol, niu-cast) | 🟢 Aktif |
| `docs/architecture/` | Konsep arsitektur (autoskills-pattern, personal-ai-os) | 🟢 Referensi |
| `docs/audit/` | Audit historis (AGENTS.md.pre-slim-53k.bak, CORE-REPAIR, ERRATA-AUDIT-V1) | 🟡 Arsip |
| `docs/references/` | **148 file** — snapshot rekonstruksi, draft keputusan model, studi per-repo | 🟡 Mixed (arsip+draft) |
| `docs/reports/` | Laporan status (healthcheck, prioritas kerja, status hukum/otoritas model, rekonstruksi) | 🟢 Aktif |
| `docs/superpowers/` | Kosong (hanya .DS_Store) | ⚪ Kosong |
| `docs/notebooklm/` | README + RECONNECT_GUIDE (integrasi NotebookLM) | 🟢 Aktif |
| `(level-atas)` | `SESSION-2026-08-10.md`, `skill-ecosystem-guide.md` | 🟢 Aktif |

---

## 🟢 Dokumen Aktif (baca ini)
- `docs/dox/INDEX.md` — index ini
- `docs/dox/niu-cast.md`, `trancast-protocol-analysis.md`, `joy-connect-for-mac.md` — analisis dox
- `docs/reports/ekosistem-healthcheck-2026-08-21-autoskills.md`
- `docs/reports/status-hukum-otoritas-model-2026-08-21.md` ← status otoritas model (D-0004)
- `docs/reports/RENCANA-REKONSTRUKSI-2026-08-18.md`
- `docs/reports/prioritas-urutan-kerja-2026-08-20.md`
- `docs/notebooklm/README.md` + `RECONNECT_GUIDE.md`
- `docs/SESSION-2026-08-10.md`, `docs/skill-ecosystem-guide.md`

## 🟡 Arsip / Draft (bukan runtime)
- `docs/audit/` — hasil audit 18 Aug, sudah digantikan D-0004/STATE
- `docs/references/niumination-rebuild-v2-2026-08-18/` (~75 file) — snapshot penuh rekonstruksi (copy reference, BUKAN live)
- `docs/references/migration-portable-to-native/` — log migrasi portable→native
- `docs/references/niumination-model-selection/` — **DRAFT** OPSI-2 (model asing/berbayar) — TIDAK dipakai, D-0004 lah yang sealed
- `docs/references/STATUS-REFERENSI-2026-08-13.md` — tracker lama (superseeded)

## ⚪ Perlu dibersihkan
- `docs/superpowers/` — kosong (hapus atau isi)
- `docs/references/niumination-rebuild-v2-2026-08-18/preview-root/` — duplikat 1:1 (37 file redundan)

---

## 🔑 Keputusan Kunci (referensi cepat)
- **Otoritas model:** D-0004 (sealed) → hanya Zen `*-free` + Nous `:free`. Lihat `docs/reports/status-hukum-otoritas-model-2026-08-21.md`.
- **Konstitusi:** `sealed` v2.1 (file beku di `core/`, tidak di `docs/`).
- **Mapping thread TG:** lihat `core/ledger/decisions/thread-model-mapping-plan-2026-08-21.md` (diterapkan 22 Aug).

---
*Index dirawat manual. Update saat ada penambahan/pemindahan dokumen.*
