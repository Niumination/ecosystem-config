---
name: skill-bank-maintenance
description: Maintain the Niumination Skill Bank — manifest SHA-256 integrity, full-folder sync to agents, drift handling, lockfiles. Use when working with ~/Desktop/Niumination/skills, skill-manifest.py, sync-to-agents.sh, or when up-eco reports skill bank integrity/sync issues.
tags:
  - niumination
  - skills
  - sync
  - integrity
  - manifest
last_updated: "2026-08-16"
version: 1.0.0
---

# Skill Bank Maintenance (Niumination)

## Trigger
- Working with `~/Desktop/Niumination/skills/` (Bank Pusat) or its targets
- `up-eco` Phase 6 (Integritas) / Phase 7 (Sync Status) findings
- Regenerating manifest, fixing sync drift, adding/removing skills

## Layout & Topology
- **Bank Pusat**: `~/Desktop/Niumination/skills/<domain>/<skill>/` — single source of truth (68 skill, 348 file)
- **Targets** (synced by `skills/sync-to-agents.sh`):
  - Jcode: `~/.jcode/skills/<skill>/` — **flat** structure
  - Hermes local: `~/.hermes/skills/<domain>/<skill>/` — **domain** structure
  - Hermes USB: `/Volumes/HermesAgent/HermesAgentUSB/data/skills/<domain>/<skill>/` — **domain**
- **Manifest**: `skills/manifest.json` — per-file SHA-256 + bundleHash per skill (pola autoskills/midudev)
- **Lockfile per target**: `skills-lock.json` (source, domain, bundleHash, syncedAt)

## Core Commands
```bash
cd ~/Desktop/Niumination

# Generate manifest (WAJIB setelah edit skill manual, sebelum sync)
python3 scripts/skill-manifest.py

# Verify bank vs manifest (deteksi ubah/hilang/baru)
python3 scripts/skill-manifest.py --check

# Verify salinan target (--structure: flat=Jcode, domain=Hermes/USB)
python3 scripts/skill-manifest.py --verify-target ~/.jcode/skills --structure flat
python3 scripts/skill-manifest.py --verify-target /Volumes/HermesAgent/HermesAgentUSB/data/skills --structure domain

# Full sync + verify + lockfile (semua target)
bash skills/sync-to-agents.sh          # real
bash skills/sync-to-agents.sh --dry-run
```

## Sync Behavior (v3, 2026-08-16)
- **SELURUH folder skill di-rsync** (`rsync -a -u`), bukan cuma SKILL.md — references/scripts/assets ikut. Sebelumnya hanya SKILL.md → 8 skill terpotong di target (impeccable 152 file, ui-ux-pro-max 35, dll). Jangan asumsikan target lengkap tanpa `--verify-target`.
- **Non-destruktif by design**: `-u` (update) TIDAK menimpa file target yang lebih baru. Safety "copy/add only, never delete" dipertahankan.
- Setiap target: verify hash → tulis `skills-lock.json`.
- AGENTS.md registry: kolom File (jumlah file per skill) ditambahkan.

## Drift Policy (PENTING)
- rsync `-u` sengaja membiarkan file target yang lebih baru (drift) — verifikasi hash akan mendeteksinya (`[ubah]` / `[hilang]`).
- **JANGAN overwrite otomatis.** Drift = laporkan + keputusan USER (audit = rekomendasi saja). Contoh nyata: 6 file Hermes USB lebih baru dari bank (diedit langsung di USB, beberapa lebih lengkap, satu lebih ringkas).
- Backport (USB → bank) atau force (bank → target) = minta persetujuan eksplisit dulu.

## HOME Bloat Prune (teknik F4, 2026-08-20)
Saat target Hermes (`/Volumes/HermesAgent/HermesAgentUSB/data/skills/`) jauh melebihi bank (213 vs 47 SKILL.md), jangan hapus langsung — **pindah ke archive dulu** (rollback 1 perintah). Klasifikasi aman:

```bash
# 1. Daftar skill ekstra = di target tapi TIDAK di bank:
comm -13 <(cd /Users/zaryu/Desktop/Niumination/skills && find . -name "SKILL.md" | sort) \
         <(cd /Volumes/HermesAgent/HermesAgentUSB/data/skills && find . -name "SKILL.md" | sort)

# 2. KEEP wajib (JANGAN dipindah): 47 mirror bank + BUILTIN Hermes (cek via `hermes skills list` kolom Source=builtin; ~38-52 skill — computer-use/dogfood/creative-resmi dll) + skill buatan rekonstruksi/inti (provider-fallback, hermes/*, niu-mission-control-ops, skill-bank-*, ecosystem-*)

# 3. Archive sisanya: mv (bukan rm) ke folder di LUAR data/skills
mkdir -p /Volumes/HermesAgent/HermesAgentUSB/data/skills_archive_2026-08-20
mv "$rel" "$BACKUP/$rel"
```

**Pitfall builtin:** skill `builtin` di `hermes skills list` disediakan Hermes (computer-use, dogfood, hermes-desktop-plugins, arsitektur, dll) — menghapusnya merusak katalog. Hanya arsipkan yang berstatus `local` dan tidak dibutuhkan. Verifikasi pasca-prune: `hermes skills list` tanpa error + `hermes config check` bersih + total SKILL.md turun (213→113 contoh nyata, -47%).

## Pitfalls
- **Patch skill yang di-sync dari bank → ditolak**: skill dengan `created_by=None` (bank-synced, mis. `up-eco`) menolak skill_manage patch. Backport perubahan ke Bank Pusat `~/Desktop/Niumination/skills/<domain>/<skill>/SKILL.md`, lalu sync.
- **MC server mati diam-diam** (terbunuh saat session compact/restart) — up-eco lapor "MC tidak merespon di 5200". Verifikasi `curl -s localhost:5200/health` + `lsof -i :5200` dulu, restart `cd services/niu-mission-control && venv/bin/python server.py` (background).
- **Escape-drift saat patch bash heredoc** (sync-to-agents.sh, up-eco.sh): file berisi `\n` literal di heredoc Python sering gagal patch karena escape-drift (`\"`/`\\n`). Fix: patch kecil per baris tanpa backslash-escape, atau read_file dulu sebelum overwrite.
- Manifest basi = false alarm: regenerate manifest sebelum `--check` setelah edit manual.

## Verification (Definition of Done)
- `skill-manifest.py --check` → 0 mismatch
- `diff -r skills/<domain>/<skill> <target>/...` → identik untuk skill besar
- Re-run sync → cepat (skip up-to-date), verify LULUS, lockfile fresh
