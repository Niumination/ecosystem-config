# Rencana Penerapan: Pola autoskills untuk Skill Bank Niumination

> **Status:** Phase 1-4 SELESAI — 2026-08-22 (Jcode)
> **Tanggal:** 2026-08-16
> **Penulis:** Hermes (analisis + rekomendasi)
> **Referensi:** [autoskills.sh](https://www.autoskills.sh/) · [midudev/autoskills](https://github.com/midudev/autoskills) (6.8k⭐, CC BY-NC 4.0)
> **Prinsip:** Non-destruktif · reversible · verifikasi sebelum klaim selesai

---

## 1. Ringkasan Eksekutif

autoskills adalah CLI auto-install skill AI agent oleh midudev. Tiga pola keamanan/arsitekturnya layak diadopsi ke Skill Bank Niumination:

1. **Manifest SHA-256** — setiap skill direkam hash per-file + `bundleHash`, diverifikasi sebelum & sesudah instalasi
2. **Audit konten anti-injection** — skill dari upstream di-review (approved/flagged) sebelum masuk registry
3. **Canonical + symlink + lockfile** — satu sumber benar, link ke semua agent, traceability via `skills-lock.json`

**Temuan utama gap analysis:** `sync-to-agents.sh` saat ini hanya menyalin file `SKILL.md` — seluruh file pendukung (references/, scripts/, data/, assets/) **tidak ikut tersinkron**. Dampak: 8 dari 40 skill (termasuk `impeccable` 152 file, `ui-ux-pro-max` 35 file, `document-content-pipeline` 9 file) terpotong/rusak di semua target agent.

Prioritas: **Phase 2 (fix sync references) → Phase 1 (manifest) → Phase 3 (security scan) → Phase 4 (opsional auto-detect)**.

---

## 2. Latar Belakang — Apa yang Dipelajari dari autoskills

### 2.1 Arsitektur (dari clone repo, `packages/autoskills/`)

| File | Peran |
|---|---|
| `main.ts` (603 baris) | CLI: parse args, flow, banner, multi-select UI |
| `lib.ts` (704) | Deteksi teknologi (6 mekanisme), koleksi skill, workspace support |
| `skills-map.ts` (1416) | Pemetaan tech→skill (218 skill ter-registrasi), combo skills, `AGENT_FOLDER_MAP` |
| `installer.ts` (786) | Integritas SHA-256, download verifikasi, symlink, lockfile |
| `sync-skills.mjs` | Script maintainer: fetch upstream → review LLM → simpan registry + manifest |
| `claude.ts` (38) | Cleanup section `<!-- autoskills:start/end -->` di CLAUDE.md |

### 2.2 Model keamanan (yang paling berharga)

```
Upstream repo ──sync-skills.mjs──▶ skills-registry/<skill>/ + index.json
                                        │  (per-file SHA-256 + bundleHash + review status)
                                        ▼
CLI (runtime) ──▶ pilih skill ──▶ download dari registry (bukan upstream!)
                                        │  verifikasi SHA-256 tiap file
                                        │  verifikasi bundleHash
                                        ▼
                        .agents/skills/<skill>/  (canonical, verified)
                              │
                              ├── symlink → .claude/skills/<skill>
                              ├── symlink → .cline/skills/<skill>
                              └── skills-lock.json (source + hash, traceability)
```

- **Tidak pernah** download langsung dari upstream saat runtime
- `.zip` diblokir; cache per-bundle di `~/.cache/autoskills/`
- Review LLM: `status: approved | flagged` + `flags[]` + `summary` + `model` + `reviewedAt`
- Lisensi CC BY-NC 4.0 → pola boleh diadaptasi (bukan kode ditiru untuk komersial)

### 2.3 Deteksi stack (untuk Phase 4)

6 mekanisme berurutan: package names → package regex → config files → file extensions → Gemfile gems → regex isi config. Support workspace/monorepo (scan sub-direktori workspace). Frontend bonus skills jika terdeteksi ekstensi web.

---

## 3. Gap Analysis — Kondisi Saat Ini (Bukti dari Ekosistem)

| # | Aspek | Kondisi sekarang | Masalah |
|---|---|---|---|
| G1 | **Sync references** | `sync-to-agents.sh` baris 84-194 hanya `cp "$src_file" "$jcode_file"` (SKILL.md saja) | ⚠️ **Kritis**: 8 skill punya file pendukung (total 213 file non-SKILL.md); references/scripts/data tidak pernah tersalin → skill rusak di target |
| G2 | **Integritas** | up-eco Phase 6a/6b hanya cek frontmatter YAML + INDEX sync | Tidak ada hash → tidak bisa deteksi file diubah/di-tamper/drift antar target |
| G3 | **Keamanan konten** | Tidak ada review/scan konten skill | Risiko prompt-injection via skill (skill = instruksi yang dieksekusi agent) |
| G4 | **Duplikasi** | Copy penuh ke 3 target (Jcode, Hermes local, Hermes USB) | 254 file × 3 target; drift antar target mungkin; tidak ada traceability asal-usul |
| G5 | **Auditability** | Tidak ada lockfile | Tidak tahu skill mana dari mana, versi apa, hash berapa |
| G6 | **Discovery** | INDEX.md manual | Tidak ada auto-detect stack → user harus tahu skill apa yang ada |

**Data pendukung (diukur 2026-08-16):**
- 40 SKILL.md, 254 file total di `~/Desktop/Niumination/skills/`
- Skill dengan file pendukung: `impeccable` (152), `ui-ux-pro-max` (35), `document-content-pipeline` (9), `plan-compliance-audit` (6), `pemdi-evidence-management` (6), `gdpr-compliance` (5), `compliance-checklist-dashboard` (3), `agent-reach` (2)

---

## 4. Rencana Fase

### PHASE 1 — Manifest SHA-256 + Verifikasi Integritas

**Tujuan:** Setiap file skill punya hash; up-eco bisa deteksi perubahan/hilang/ekstra; sync bisa verifikasi hasil copy.

**File baru:** `scripts/skill-manifest.py`

**Spesifikasi `skills/manifest.json`:**
```json
{
  "version": 1,
  "generatedAt": "2026-08-16T22:40:00+07:00",
  "skillCount": 40,
  "fileCount": 254,
  "skills": {
    "ponytail-core": {
      "domain": "software-development",
      "bundleHash": "sha256:...",
      "files": {
        "SKILL.md": "sha256:abc...",
        "references/xxx.md": "sha256:def..."
      }
    }
  }
}
```

**Implementasi `skill-manifest.py`:**
- Walk `skills/` per domain → per skill (folder berisi SKILL.md)
- SHA-256 per file (path relatif terhadap folder skill), sorted
- `bundleHash` = SHA-256 dari gabungan `rel:hash` sorted (pola autoskills)
- `--check` mode: verifikasi manifest vs filesystem (deteksi: file berubah, hilang, baru)
- `--verify-target <dir>` mode: verifikasi salinan di target agent (Jcode/Hermes/USB)
- Exit code: 0 = OK, 1 = mismatch (detail per file di stdout)

**Perubahan `scripts/up-eco.sh` (Phase 6c baru):**
```bash
# ── 6c: Verifikasi manifest integritas
if [ -f "$SKILLS_DIR/manifest.json" ]; then
  python3 "$ROOT/scripts/skill-manifest.py" --check
  # pass/fail sesuai exit code
else
  warn "manifest.json belum ada — jalankan scripts/skill-manifest.py"
fi
```

**Kriteria sukses:**
- [ ] `skill-manifest.py` generate manifest tanpa error
- [ ] `--check` → 0 mismatch saat bersih; mendeteksi 1 file diubah (uji dengan `touch`/edit dummy lalu revert)
- [ ] up-eco menampilkan baris integritas manifest

---

### PHASE 2 — Fix Sync References (PALING KRITIS) + Lockfile

**Tujuan:** Seluruh folder skill (bukan cuma SKILL.md) tersinkron + diverifikasi hash + tercatat di lockfile.

**Perubahan `skills/sync-to-agents.sh`:**

2a. **Copy seluruh folder** — ganti loop copy per-file dengan rsync (atau cp -R) per skill:
```bash
# Lama: cp "$src_file" "$jcode_file"          # hanya SKILL.md
# Baru: rsync -a --delete "..."  →  TIDAK. Non-destruktif: rsync -a (tanpa --delete)
rsync -a "$bank_skill_dir/" "$target_skill_dir/"
```
- **PENTING**: non-destruktif — jangan `--delete` (konsisten dengan safety "copy/add only, never delete" yang sudah ada). Skill yang dihapus dari bank dibiarkan di target (atau opsi `--prune` eksplisit).
- Skip jika target lebih baru (`-u` / `--update` rsync) — pertahankan perilaku up-to-date check yang ada.

2b. **Verifikasi pasca-sync** (flag `--verify`, default ON):
```bash
python3 "$ROOT/scripts/skill-manifest.py" --verify-target "$JCODE_DIR"
# hash-check tiap file target vs manifest; lapor mismatch
```

2c. **Lockfile per target** `skills-lock.json` (pola autoskills `updateSkillsLock`):
```json
{
  "version": 1,
  "updatedAt": "2026-08-16T22:40:00+07:00",
  "skills": {
    "ponytail-core": {
      "source": "Bank Pusat",
      "domain": "software-development",
      "bundleHash": "sha256:...",
      "syncedAt": "2026-08-16T22:40:00+07:00"
    }
  }
}
```
Disimpan di: `~/.jcode/skills/skills-lock.json`, `~/.hermes/skills/skills-lock.json`, `/Volumes/HermesAgent/HermesAgentUSB/data/skills/skills-lock.json`.

2d. **AGENTS.md registry** — tambah kolom `File` (jumlah file per skill) supaya DOX injection mencerminkan kelengkapan.

**Risiko & mitigasi:**
- rsync tidak ada di semua macOS? → rsync bawaan macOS tersedia. Fallback: `cp -R` + `-u` per-file.
- Volume beda (Hermes USB) → rsync/cp normal lintas volume OK (bukan symlink di fase ini).
- Ukuran bank naik (254 file vs 40) → tidak masalah; rsync incremental.

**Kriteria sukses:**
- [ ] `sync-to-agents.sh` (tanpa flag) menyalin seluruh folder impeccable (152 file) ke Jcode/Hermes/USB
- [ ] `--verify` menemukan 0 mismatch setelah sync bersih
- [ ] Lockfile ter-generate di 3 target
- [ ] Re-run sync → skip cepat (up-to-date), tidak ada re-copy

---

### PHASE 3 — Security Scan Konten Skill (Anti Prompt-Injection)

**Tujuan:** Deteksi pola berbahaya dalam SKILL.md/references sebelum agent mengeksekusi instruksinya.

**File baru:** `scripts/skill-audit.py`

**Pattern scan (heuristic, warning-level):**
| Kategori | Pola |
|---|---|
| Instruksi tersembunyi | `<!--` instruksi dalam komentar HTML, teks kecil/samar, zero-width chars (`\u200b\u200c\u200d`) |
| Exfil | base64 blob > 200 char, perintah `curl|bash`, `wget|sh`, pipe ke shell |
| URL mencurigakan | URL non-GitHub di bagian "instructions"/"commands" (allowlist: docs resmi, npm, pypi, dll) |
| Token/secret | pattern `sk-`, `api_key=`, `token=`, `AKIA` (AWS) dalam contoh kode |
| Path berbahaya | `~/.ssh`, `~/.aws`, `~/.config`, `/etc/`, `chmod 777`, `rm -rf` (di luar konteks) |
| Self-modification | instruksi "edit SKILL.md", "append to AGENTS.md" tanpa izin |
| Prompt injection klasik | "ignore previous instructions", "you are now", "system prompt" (di dalam skill body) |

**Output:**
```
Skill: impeccable
  ⚠️ [url] line 45: URL non-allowlist: https://evil.example/script.sh
  ⚠️ [exec] line 120: curl|bash pattern
→ 2 findings — review manual disarankan
```

**Integrasi up-eco Phase 6d:** jalankan audit → warning + rekomendasi review manual. Jangan auto-fix (skill adalah konten, audit = saran, konsisten dengan aturan "audit docs = recommendations only").

**Catatan:** versi penuh bisa pakai LLM review seperti autoskills (approved/flagged + summary), tapi mulai dari heuristic dulu (gratis, cepat, deterministik).

**Kriteria sukses:**
- [ ] Audit 40 skill berjalan < 10 detik
- [ ] Skor baseline tercatat (jumlah findings per skill) — hasil awal di-review manual
- [ ] Uji: skill dummy berisi `curl|bash` → terdeteksi

---

### PHASE 4 — Auto-Detect Stack ✅ SELESAI 2026-08-22

**Tujuan:** `scripts/skill-detect.py` — scan proyek → rekomendasi skill dari bank (mirip autoskills).

**Spesifikasi singkat:**
- File: `scripts/skill-detect.py` (Python — ekosistem dominan Python)
- Input: `--dir <proyek>` (default cwd)
- Deteksi: `package.json` (JS/TS), `pyproject.toml`/`requirements.txt` (Python), `composer.json` (PHP), `Gemfile` (Ruby), `go.mod` (Go), `Cargo.toml` (Rust), config files
- Map ke skill bank: `fastapi` → fastapi-templates?, `laravel` → laravel-specialist, `next` → nextjs-ui-interactions, dll.
- Output: daftar skill yang relevan + lokasi di bank + instruksi sync
- Integrasi: bisa jadi command di Mission Control / pre-commit hook (opsional)

**Kriteria sukses:** deteksi benar pada 3 proyek nyata — ✅ Niumination (20 skill), niu-mission-control (13 skill), cc-acehtengah (6 skill).

**Implementasi:** `scripts/skill-detect.py` — 6 mekanisme (package names, package regex, config files, ext, content regex, Gemfile/go.mod/Cargo.toml/composer), map ke 68 skill via SKILL_MAP, dedup evidence, confidence high/medium/low. Usage: `python3 scripts/skill-detect.py --dir <proyek> [--json] [--verbose] [--list-map]`.

---

## 5. Prioritas & Timeline

| Fase | Dampak | Effort | Prioritas |
|---|---|---|---|
| **2 — Fix sync references** | Tinggi (8 skill rusak sekarang) | Rendah (ubah loop copy) | 🥇 P1 |
| **1 — Manifest integritas** | Tinggi (fondasi verifikasi) | Sedang (script baru) | 🥈 P2 |
| **3 — Security scan** | Sedang (defense-in-depth) | Sedang (pattern list) | 🥉 P3 |
| **4 — Auto-detect** | Bonus (discovery) | Tinggi | P4 (opsional) |

Urutan eksekusi disarankan: **2 → 1 → 3** (Phase 1 manifest membantu verifikasi Phase 2; keduanya independen dan bisa digabung dalam satu sesi kerja).

## 6. Risiko & Mitigasi

| Risiko | Mitigasi |
|---|---|
| rsync beda perilaku di macOS | Test dry-run dulu; fallback `cp -R -u` |
| Bank membengkak (file pendukung ikut sync) | Rsync incremental; ukuran masih kecil (< 1 MB) |
| Manifest basi (file diedit manual) | `--check` di up-eco tiap 6h; regenerate manifest saat ada perubahan |
| False positive security scan | Level warning, bukan blocking; allowlist URL resmi |
| Skill dihapus dari bank → target stale | Non-destruktif; opsi `--prune` eksplisit di masa depan |

## 7. Definisi Selesai (Definition of Done)

Phase 1-3 dianggap selesai jika:
1. `skill-manifest.py` + `skill-audit.py` ada, berjalan, terintegrasi di `up-eco.sh`
2. `sync-to-agents.sh` menyinkronkan seluruh folder (bukan cuma SKILL.md) + `--verify` lulus
3. Lockfile ada di 3 target dengan bundleHash benar
4. `bash scripts/up-eco.sh` → Phase 6 menampilkan integritas manifest + audit tanpa error
5. Verifikasi nyata (bukan klaim): `diff -r` satu skill besar (impeccable) bank vs target = identik

---

## Lampiran A — Referensi autoskills

- Repo: https://github.com/midudev/autoskills (main branch, 380 commits, 17 tags)
- Registry manifest: `packages/autoskills/skills-registry/index.json` (218 skills, reviewer gpt-5.4, promptVersion 1.0.0)
- Sync script: `packages/autoskills/scripts/sync-skills.mjs` (download upstream → review → persist)
- Lisensi: CC BY-NC 4.0 — pola diadopsi secara konseptual; tidak menyalin kode untuk produk komersial

## Lampiran B — Perintah audit cepat

```bash
# Verifikasi manifest (setelah Phase 1)
cd ~/Desktop/Niumination && python3 scripts/skill-manifest.py --check

# Sync + verify (setelah Phase 2)
cd ~/Desktop/Niumination && bash skills/sync-to-agents.sh --verbose

# Security scan (setelah Phase 3)
cd ~/Desktop/Niumination && python3 scripts/skill-audit.py

# Auto-detect stack → rekomendasi skill (Phase 4)
cd ~/Desktop/Niumination && python3 scripts/skill-detect.py --dir services/cc-acehtengah
python3 scripts/skill-detect.py --dir services/niu-mission-control --json
python3 scripts/skill-detect.py --list-map
```
