---
name: skill-bank-ops
description: "Operasi Skill Bank Niumination — manifest SHA-256, sync seluruh folder ke agent, resolve drift bank<->target, adopsi skill eksternal. Use when regenerating skills/manifest.json, verifikasi integritas skill, sync-to-agents.sh error/mismatch, drift USB vs bank, menambah skill baru ke bank (dari autoskills registry atau repo lain), atau up-eco Phase 6 melaporkan manifest mismatch."
tags:
  - niumination
  - skill-bank
  - manifest
  - sync
  - sha256
  - autoskills
last_updated: "2026-08-17"
version: 1.0.0
---

# 🧠 Skill Bank Ops — Manifest, Sync, Drift, Adopsi

Pola diadopsi dari autoskills (midudev): manifest SHA-256 + canonical copy + lockfile. Berlaku untuk `~/Desktop/Niumination/skills/` (Bank Pusat, single source of truth).

## Arsitektur

```
Bank Pusat (skills/<domain>/<skill>/)  ← source of truth
  │  skill-manifest.py (generate)
  ▼
skills/manifest.json  (SHA-256 per file + bundleHash per skill)
  │
  ▼  sync-to-agents.sh (rsync -a -u seluruh folder)
  ├── ~/.jcode/skills/<skill>/          (flat)
  ├── ~/.hermes/skills/<domain>/<skill>/ (domain)
  └── /Volumes/HermesAgent/.../skills/<domain>/<skill>/ (domain, USB)
        └── skills-lock.json per target (source + bundleHash + syncedAt)
```

**Kritis:** sync meng-copy SELURUH folder skill (SKILL.md + references/scripts/assets), bukan hanya SKILL.md — bug lama hanya copy SKILL.md membuat skill besar (impeccable 152 file, ui-ux-pro-max 35) rusak parsial di agent.

## Perintah

```bash
# Generate manifest (setelah ada perubahan bank)
python3 scripts/skill-manifest.py

# Verifikasi bank vs manifest (up-eco Phase 6d memakai ini)
python3 scripts/skill-manifest.py --check

# Verifikasi salinan target (Jcode flat; Hermes/USB domain!)
python3 scripts/skill-manifest.py --verify-target ~/.jcode/skills --structure flat
python3 scripts/skill-manifest.py --verify-target ~/.hermes/skills --structure domain

# Tulis lockfile di target
python3 scripts/skill-manifest.py --lockfile <target-dir>

# Sync + verify + lockfile otomatis (3 target)
bash skills/sync-to-agents.sh [--dry-run] [--verbose]
```

## Alur Resolve Drift bank↔target

Verifikasi hash mendeteksi mismatch saat file target **lebih baru** dari bank (rsync `-u` benar TIDAK menimpa modifikasi lokal — non-destruktif). Drift = file pernah diedit langsung di USB/agent.

1. Cek timestamp + size bank vs target (`stat -f '%Sm' -t '%Y-%m-%d'`)
2. **Target lebih baru/lengkap** → backport ke bank: `cp target/... bank/...` (konten Phase baru, perbaikan runtime)
3. **Bank lebih lengkap** (mis. bank 628 baris vs USB 41) → force bank → target: `cp bank/... target/...`
4. Regenerate manifest → `bash skills/sync-to-agents.sh` → verifikasi SEMUA target LULUS (0 mismatch)
5. Commit + push

Jangan pernah resolve drift tanpa konfirmasi user (audit = rekomendasi; mutasi butuh izin).

## Adopsi Skill Eksternal (autoskills registry / repo lain)

1. **Cek lisensi dulu** — GitHub API: `curl -s https://api.github.com/repos/{owner}/{repo}/license`
   - `NO-LICENSE` → **SKIP** (preferensi user: free/open-source only; adopsi NO-LICENSE = pelanggaran)
2. Cek review status di registry (autoskills: `review.status` approved/flagged; `flagged` → skip, mis. python-executor: broad exec + raw install link)
3. Copy file skill ke `skills/<domain>/<skill>/` (ikut references/scripts/LICENSE)
4. Tambah frontmatter: `license: <SPDX>` + `source: autoskills registry — owner/repo` (konvensi bank)
5. Update `skills/INDEX.md`: entri tabel per domain + counter "Status: N ✅ Aktif"
6. `python3 scripts/skill-manifest.py` → `bash skills/sync-to-agents.sh` → verify 3 target
7. Commit + push

## Pitfall

- **`_get_home()`-style path resolution (MC skill_monitor)**: cek folder **berisi** (`Desktop/Niumination/skills`), BUKAN folder induk (`Desktop/Niumination`) — HOME cache Hermes punya folder induk KOSONG yang menyesatkan → `_scan_skill_bank()` = 0 → puluhan conflict palsu "NOT in bank pusat". Same bug class in sync scripts & manifest resolvers.
- **Manifest basi**: file diedit manual tanpa regenerate → `--check` FAIL. Regenerate setelah setiap perubahan bank.
- **Jcode flat vs Hermes/USB domain**: `--structure` salah → seluruh skill di-flag hilang. Jcode = flat, sisanya = domain.
- **rsync lintas volume (USB)**: normal copy, bukan symlink — jangan pakai `--delete` (non-destruktif).

## Referensi

- `references/skill-bank-manifest-sync.md` — skema manifest.json, kasus drift nyata, detail adopsi
