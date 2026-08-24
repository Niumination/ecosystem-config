---
name: skill-bank-management
description: "Kelola Skill Bank Niumination (single source of truth ~/Desktop/Niumination/skills/) — generate & verifikasi manifest SHA-256, sync seluruh folder skill ke agent target (Jcode/Hermes/USB) dengan verifikasi hash + lockfile, tangani drift antar target, dan adopsi skill dari registry eksternal (autoskills, GitHub). Gunakan saat ada skill baru masuk bank, sync-to-agents.sh dijalankan/gagal, up-eco melaporkan manifest mismatch, drift file antara bank vs target, atau user minta adopsi skill X."
tags:
  - ecosystem
  - skills
  - manifest
  - sha256
  - sync
  - niumination
last_updated: "2026-08-17"
version: 1.1.0
changes:
  - v1.0: Initial — pola dari adopsi autoskills (midudev) 2026-08-16
  - v1.1: Added explicit license-checking workflow (autoskills registry pattern), noted 6x skill-bank-* overlap for curator consolidation
---

# 🧠 Skill Bank Management — Niumination

## Trigger
- User menambah/mengubah skill di bank, atau minta "adopsi skill dari autoskills/registry"
- up-eco Phase 6d melaporkan manifest mismatch
- Sync skill gagal / drift antar target

## Arsitektur

```
skills/ (Bank Pusat — source of truth)
  ├── manifest.json        ← SHA-256 per file + bundleHash per skill
  ├── INDEX.md             ← daftar skill per domain (manual, sinkron dgn fs)
  └── <domain>/<skill>/{SKILL.md, references/, scripts/, assets/}
       │
       ▼ scripts/skill-manifest.py  (generate/check/verify/lockfile)
       ▼ skills/sync-to-agents.sh   (rsync -a -u SELURUH folder)
       ▼
  Jcode  (~/.jcode/skills/<skill>/ flat)
  Hermes (~/.hermes/skills/<domain>/<skill>/)
  USB    (/Volumes/HermesAgent/HermesAgentUSB/data/skills/<domain>/<skill>/)
  + skills-lock.json di tiap target (source + bundleHash + syncedAt)
```

## Workflow inti

### 1. Regenerate manifest setelah perubahan bank
```bash
cd ~/Desktop/Niumination
python3 scripts/skill-manifest.py          # tulis manifest.json
python3 scripts/skill-manifest.py --check  # 0 mismatch = OK
```

### 2. Sync + verifikasi
```bash
bash skills/sync-to-agents.sh              # rsync seluruh folder + verify + lockfile
```
Ekspektasi output: 3 target `✅ verifikasi hash LULUS` (semua file SHA-256 cocok).
- Jcode = structure `flat`; Hermes & USB = structure `domain` (argumen `--structure` di skill-manifest.py)
- rsync `-u` = non-destruktif: file target yang LEBIH BARU tidak ditimpa → drift terdeteksi oleh verifikasi hash, bukan di-silent-overwrite

### 3. Verifikasi manual satu target
```bash
python3 scripts/skill-manifest.py --verify-target /Users/zaryu/.jcode/skills --structure flat
python3 scripts/skill-manifest.py --verify-target ~/.hermes/skills --structure domain
```

## Pitfalls (dipelajari dari sesi nyata)

1. **Home-resolution empty-folder trap**: script yang resolve HOME di env Hermes HARUS cek marker folder BERISI (`Desktop/Niumination/skills`), bukan cuma folder induk (`Desktop/Niumination`). Folder stub KOSONG eksis di `/Volumes/HermesAgent/.cache/unix-home/Desktop/Niumination/` dan menyesatkan `_get_home()`/`_resolve_home()` → bank scan 0 skill → 43 conflict palsu di skill_monitor MC. Bug nyata ini diperbaiki di `services/niu-mission-control/modules/skill_monitor.py` (cek `os.path.isdir(home/"Desktop"/"Niumination"/"skills")`).
2. **Drift USB = file lebih baru di target** (pernah diedit langsung di USB). rsync -u dengan benar TIDAK menimpa; verifikasi hash mendeteksinya. Jangan auto-resolve — tanya user: backport target→bank (file lebih lengkap) atau force bank→target. Dokumentasikan keputusan di commit.
3. **Skill di bank harus utuh**: sync lama hanya copy SKILL.md → 8 skill rusak parsial di target (references/scripts hilang). Selalu copy SELURUH folder skill.
4. **Flag security registry**: saat adopsi dari autoskills registry, cek `index.json` → `review.status` (approved/flagged) + `flags[]`. Skill flagged (mis. python-executor: broad code exec, raw GitHub install link) → jangan adopsi tanpa review manusia.
5. **Lisensi**: cek frontmatter license sebelum adopsi. MIT/Apache-2.0 aman; skill tanpa field license → cek repo upstream dulu (autoskills sendiri CC BY-NC = pola boleh diadopsi konseptual, bukan salin kode untuk komersial).

## Adopsi skill eksternal → bank

Prosedur lengkap: `references/adopt-external-skill.md`
Ringkas: cek license+review → copy folder ke `skills/<domain>/<skill>/` (ikutkan references/scripts) → sesuaikan frontmatter (tambah `version`/`source`, konvensi bank) → update INDEX.md (baris tabel + counter "Status: N ✅ Aktif") → regenerate manifest → sync → verify 3 target → commit+push.

## Catatan overlap (untuk curator)
- Overlap dengan `up-eco` (Phase 6/7 di up-eco.sh) — skill ini fokus operasional bank; up-eco = health check. `up-eco` di Hermes USB curator-protected (created_by=None); update prosedur di sini atau backport manual ke `~/Desktop/Niumination/skills/ecosystem/up-eco/SKILL.md`.
