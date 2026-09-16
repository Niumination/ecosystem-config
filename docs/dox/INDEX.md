# DOX — Index Dokumentasi Niumination

**Dibuat:** 2026-08-22 · **Diperbarui:** 2026-09-16 · **Sumber:** filesystem `docs/` (142 file, 135 tracked)
**Tujuan:** Peta tunggal seluruh dokumentasi di `docs/` agar tidak ada file yang "tersesat".

---

## 📂 Struktur `docs/`

| Folder | Isi | Status |
|--------|------|--------|
| `docs/dox/` | **Index ini + analisis dox** (joy-connect-for-mac, trancast-protocol, niu-cast) | 🟢 Aktif |
| `docs/architecture/` | Konsep arsitektur (autoskills-pattern, personal-ai-os) | 🟢 Referensi |
| `docs/audit/` | Audit historis (AGENTS.md.pre-slim-53k.bak, CORE-REPAIR, ERRATA-AUDIT-V1) | 🟡 Arsip |
| `docs/references/` | **74 file** — arsip studi/analisis (`archive/` 8 entri + `drafts/` 1 entri) | 🟡 Arsip + draft |
| `docs/registry/` | **8 file** — registry hidup (skill-registry auto-generated, project-catalog, deployment-status, ai-ecosystem, model-mapping, a2a-hermes-mac-vps, composio-integration-plan, composio-free-tier-tools) | 🟢 Hidup |
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
- `docs/references/archive/` — **8 entri** (dibersihkan 16 Sep 2026): `niumination-rebuild-2026-08-18/` (13 file — snapshot rekonstruksi, BUKAN live), `hermes-config-penutup-archive/`, `hermes-config-arena-archive/`, `stale-hermes-config-2026-08-20/`, `migration-portable-to-native/`, `STATUS-REFERENSI-2026-08-13.md`, `ekosistem-status.md`, `ai-memory-collection.md`. Peta lengkap: `docs/references/README.md`
- `docs/references/drafts/` — `niumination-model-selection/` (**DRAFT** OPSI-2, TIDAK dipakai — D-0004 yang sealed)

## ⚪ Perlu dibersihkan
- `docs/superpowers/` — kosong (hapus atau isi)
- `docs/references/akun-login.md` — perlu dipindah ke `vault/` (kemungkinan kredensial; lihat `docs/references/README.md`)
- ~~`docs/references/niumination-rebuild-v2-2026-08-18/preview-root/`~~ — **sudah tidak ada** (terverifikasi 16 Sep 2026)

---

## 🔑 Keputusan Kunci (referensi cepat)
- **Otoritas model:** D-0004 (sealed) → hanya Zen `*-free` + Nous `:free`. Lihat `docs/reports/status-hukum-otoritas-model-2026-08-21.md`.
- **Konstitusi:** `sealed` v2.1 (file beku di `core/`, tidak di `docs/`).
- **Mapping thread TG:** lihat `core/ledger/decisions/thread-model-mapping-plan-2026-08-21.md` (diterapkan 22 Aug).

---
*Index dirawat manual. Update saat ada penambahan/pemindahan dokumen.*
