# 🩺 Healthcheck Ekosistem — Skill Bank vs Pola autoskills

> **Tanggal:** 2026-08-21
> **Lensa referensi:** [midudev/autoskills](https://github.com/midudev/autoskills) (6.8k⭐, 380 commits, 17 tags, CC BY-NC 4.0)
> **Scope:** Skill Bank Niumination (`skills/`) + tooling terkait (`scripts/skill-manifest.py`, `skills/sync-to-agents.sh`, `scripts/up-eco.sh` Phase 6–7)
> **Sifat:** Audit — **rekomendasi, bukan mutasi data.** Tidak ada file yang diubah dalam pemeriksaan ini.
> **Metode:** Perbandingan fitur-keamanan/arsitektur autoskills vs kondisi terukur Skill Bank hari ini (68 skill, 348 file, 8 domain).

> **✅ Pembaruan eksekusi (sama hari):** Temuan 1 diperbaiki (manifest di-regenerate, `--check` 0 mismatch), Phase 3 diimplementasikan (`scripts/skill-audit.py` + up-eco Phase 6e), INDEX.md dirapikan (header + Ringkasan 40→68), status skill-bank-integrity diperbarui. Temuan 3 (konsolidasi `skill-bank-*`) **ditunda** — butuh keputusan curator (non-destruktif). Baseline audit: `docs/reports/skill-audit-baseline-2026-08-21.md`.

---

## 1. Ringkasan Eksekutif

| Lampu | Area | Status |
|:-----:|------|--------|
| 🟢 | Phase 1 — Manifest SHA-256 (`skill-manifest.py`) | **Terpasang & terintegrasi** (up-eco Phase 6d) |
| 🟢 | Phase 2 — Sync seluruh folder + verify + lockfile | **Selesai** (USB diparkir 2026-08-20) |
| 🔴 | Integritas manifest vs filesystem | **DRIFT terdeteksi — 15 file** (manifest basi) |
| 🔴 | Phase 3 — Audit konten anti prompt-injection | **Belum diadopsi** (`skill-audit.py` tidak ada) |
| 🟡 | Konsistensi INDEX.md & STATE.yaml | **Ada inkonsistensi internal** (68 vs 40 vs 47) |
| 🟡 | Meta-skill `skill-bank-*` | **6 skill tumpang-tindih**, belum dikonsolidasi |
| ⚪ | Phase 4 — Auto-detect stack | Belum (opsional) |

**Intinya:** fondasi yang diadopsi dari autoskills (manifest SHA-256 + sync full-folder + lockfile) **sudah jalan dan benar** — dan justru fondasi itu yang hari ini **berhasil menangkap drift nyata** di bank. Yang belum diadopsi adalah lapisan keamanan konten (anti prompt-injection) yang merupakan fitur autoskills paling bernilai secara keamanan.

---

## 2. Baseline Referensi — autoskills (dicek 2026-08-21)

Diambil langsung dari repo & registry saat ini:

- **Registry manifest** `packages/autoskills/skills-registry/index.json`: `version 1`, `generatedAt 2026-05-03`, reviewer `gpt-5.4`, `promptVersion 1.0.0`.
- **Struktur per-skill di registry**: `source`, `skillPath`, `commitSha`, `files[]`, `sha256{}` (per-file), `bundleHash`, dan `review { status: approved|flagged, flags[], summary, model, reviewedAt }`.
- **Model keamanan** (yang jadi acuan):
  1. Runtime **tidak pernah** download dari upstream — hanya dari registry kurasi.
  2. Skill di-**review LLM** (approved/flagged) sebelum masuk registry.
  3. **SHA-256 per-file + bundleHash**, diverifikasi sebelum & sesudah instalasi.
  4. **Canonical + symlink + `skills-lock.json`** untuk traceability.
  5. `.zip` diblokir; cache per-bundle.

Tabel mapping adopsi:

| Fitur autoskills | Niumination | Keterangan |
|---|---|---|
| SHA-256 per-file + bundleHash | 🟢 `skills/manifest.json` | skillCount 68, fileCount 348 |
| Verifikasi integritas | 🟡 Ada (`--check`) | **tapi saat ini GAGAL** — lihat Temuan 1 |
| Registry kurasi (bukan upstream langsung) | 🟢 Bank Pusat = single source of truth | konsep setara |
| Review LLM approved/flagged | 🔴 Tidak ada | tidak ada metadata review |
| Anti prompt-injection scan | 🔴 Tidak ada (`skill-audit.py` hilang) | Phase 3 belum |
| `skills-lock.json` traceability | 🟢 Ditulis per target | via `--lockfile` |
| Sync seluruh folder (bukan cuma SKILL.md) | 🟢 `rsync -a -u` | Phase 2 |
| Canonical + symlink per agent | 🟡 Copy-based | USB beda volume → copy (wajar) |
| Auto-detect stack | ⚪ Tidak ada (`skill-detect.py`) | Phase 4 opsional |

---

## 3. Kondisi Terukur Skill Bank (2026-08-21)

| Metrik | Nilai |
|---|---|
| Total skill | **68** |
| Total file | **348** |
| Domain | **8** (software-development 34, ecosystem 18, design 7, note-taking 3, creative 2, governance 2, autonomous-ai-agents 1, security 1) |
| `manifest.json` | ada — `generatedAt 2026-08-20T14:11:43Z` |
| `skill-manifest.py` | ada — mode: generate / `--check` / `--verify-target` / `--structure` / `--lockfile` |
| `sync-to-agents.sh` | full-folder rsync + verify hash + lockfile; target aktif: Jcode (flat) + Hermes (domain); USB diparkir |
| `up-eco.sh` | Phase 6 (frontmatter, INDEX sync, duplikasi nama, manifest `--check`) + Phase 7 (sync status) |
| `skill-audit.py` | **TIDAK ADA** |
| `skill-detect.py` | **TIDAK ADA** |
| `INDEX.md` | 68 skill tercantum (coverage 68/68 ✅), tapi tabel ringkasan bawah masih menulis **40** |

---

## 4. Temuan

### 🔴 Temuan 1 — Manifest basi: 15 file drift (integrity check GAGAL)

`skill-manifest.py --check` (pola verifikasi autoskills) saat ini **akan melaporkan mismatch**. 15 file berubah isinya sejak `manifest.json` di-generate (2026-08-20T14:11Z), semuanya di skill `ui-ux-pro-max`:

```
data/charts.csv, data/colors.csv, data/landing.csv, data/products.csv,
data/stacks/{flutter,html-tailwind,nextjs,react-native,react,svelte,swiftui,vue}.csv,
data/styles.csv, data/ux-guidelines.csv, scripts/search.py
```

- 13 file data CSV + 1 script. Tidak ada tanda masalah line-ending (CRLF/autocrlf) — murni perubahan isi file setelah manifest dibuat.
- Ini **bukan kegagalan tooling** — ini justru **bukti tooling bekerja**: manifest berhasil mendeteksi perubahan yang tidak tercatat.
- **Rekomendasi:** pastikan perubahan `ui-ux-pro-max` disengaja → lalu regenerate manifest (`python3 scripts/skill-manifest.py`). Jangan regenerate membabi-buta sebelum tahu apa yang berubah (bisa jadi ada edit manual yang perlu dicatat di ledger).

### 🔴 Temuan 2 — Phase 3 (keamanan konten) belum diadopsi

Fitur autoskills yang paling bernilai secara keamanan — **review/audit konten skill terhadap prompt-injection** — belum ada sama sekali:

- `scripts/skill-audit.py` tidak ada (hanya disebut "⬜ Phase 3 (belum)" di `skill-bank-integrity/SKILL.md`).
- Tidak ada metadata `review { approved/flagged }` di `manifest.json` (autoskills punya per-skill).
- Artinya: 348 file instruksi yang dieksekusi agent (termasuk yang diadopsi dari pihak ketiga: autoskills, superpowers, sisi-tarak, heygen, dll.) **belum pernah discan** untuk pola injeksi.
- Rencana heuristic 7 kategori sudah tertulis di `docs/architecture/autoskills-pattern-adoption.md` §PHASE 3 — tinggal dieksekusi.

### 🟡 Temuan 3 — 6 meta-skill `skill-bank-*` tumpang-tindih

Di domain `ecosystem/` ada 6 skill yang mengatur hal yang sama (manifest, sync, drift, adopsi):

`skill-bank-integrity`, `skill-bank-maintenance`, `skill-bank-management`, `skill-bank-operations`, `skill-bank-ops`, `skill-bank-sync`

- `skill-bank-operations` sendiri sudah menulis: *"ada 6 skill-bank skills overlap … konsolidasi diserahkan ke curator. Skill ini (operations) adalah yang paling komprehensif."*
- Konsolidasi **belum dilakukan**. Risiko: instruksi drift antar-skill, agen memuat versi berbeda untuk tugas yang sama.
- **Rekomendasi:** konsolidasi ke 1–2 skill (mis. `skill-bank-operations` sebagai sumber utama + `skill-bank-integrity` untuk aspek keamanan), sisanya di-archive.

### 🟡 Temuan 4 — Inkonsistensi angka antar sumber kebenaran

Tiga sumber menulis angka yang berbeda untuk satu hal yang sama:

| Sumber | Nilai | Catatan |
|---|---|---|
| Filesystem (`find -name SKILL.md`) | **68** | fakta |
| `manifest.json` `skillCount` | **68** | sinkron dgn fs |
| `INDEX.md` header | 68 ✅ | sinkron |
| `INDEX.md` tabel "Ringkasan" bawah | **40** | basi (era sebelum integrasi superpowers) |
| `core/STATE.yaml` `health.skill_bank` | **47** | basi |

- `INDEX.md` juga punya blok tabel di bagian atas **tanpa baris header tabel** (baris `| **skill-bank-integrity** | …` langsung menyusul header teks) — minor, tapi membuat render Markdown tidak rapi.

### ⚪ Temuan 5 — Phase 4 (auto-detect stack) belum ada

`scripts/skill-detect.py` tidak ada — fitur discovery (`npx autoskills` scan proyek → rekomendasi skill) belum diadopsi. Sesuai rencana, ini opsional (prioritas P4).

---

## 5. Rekomendasi (berurutan)

| # | Aksi | Effort | Prioritas |
|---|------|:------:|:---------:|
| 1 | **Investigasi + regenerate manifest** untuk 15 file `ui-ux-pro-max` yang drift, lalu catat perubahannya | Rendah (1 perintah) | 🥇 Sekarang |
| 2 | **Implement Phase 3** — `scripts/skill-audit.py` (heuristic 7 kategori, warning-only) + integrasi up-eco Phase 6e | Sedang | 🥈 Tinggi |
| 3 | **Konsolidasi 6 `skill-bank-*`** → 1–2 skill, archive sisanya | Rendah | 🥉 Sedang |
| 4 | **Perbaiki angka basi** — INDEX.md ringkasan (40→68) + STATE.yaml `health.skill_bank` (47→68) + rapikan header tabel INDEX.md | Sangat rendah | Sedang |
| 5 | (Opsional) Phase 4 — `skill-detect.py` | Tinggi | P4 |

**Catatan governance:** angka `STATE.yaml` dan file di `core/FREEZE.list` hanya diubah oleh pemilik/izin eksplisit — temuan ini dilaporkan, tidak dimutasi. `INDEX.md` & `manifest.json` bukan file beku, tetapi sesuai aturan *"audit = rekomendasi, bukan mutasi data"*, semua perbaikan menunggu persetujuan `zaryu`.

---

## 6. Lampiran — Perintah Verifikasi

```bash
# Reproduksi Temuan 1 (drift manifest):
cd ~/Desktop/Niumination && python3 scripts/skill-manifest.py --check   # expected: exit 1, 15 file mismatch

# Konfirmasi angka skill:
find ~/Desktop/Niumination/skills -name SKILL.md | wc -l                 # 68

# Cek coverage INDEX.md vs filesystem (seharusnya 0 selisih):
# (up-eco.sh Phase 6 melaporkan ini)

# Setelah manifest di-regenerate:
python3 scripts/skill-manifest.py && python3 scripts/skill-manifest.py --check   # exit 0
```
