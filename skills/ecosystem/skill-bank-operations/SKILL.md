---
name: skill-bank-operations
description: "Operate the Niumination Skill Bank — manifest SHA-256 integrity (scripts/skill-manifest.py), full-folder sync to Jcode/Hermes/USB (sync-to-agents.sh), drift resolution between bank and agent targets, and adoption of third-party skills (from autoskills registry or elsewhere) into the bank. Use when adding/removing skills, verifying sync integrity, resolving [ubah]/[hilang] drift, or adopting external skills. Patterns adopted from autoskills (midudev)."
tags:
  - skills
  - niumination
  - manifest
  - sync
  - autoskills
  - ecosystem
last_updated: "2026-08-16"
version: 1.0.0
---

# 🧠 Skill Bank Operations — Niumination

Bank pusat: `~/Desktop/Niumination/skills/` (single source of truth; 47 skill, 267 file per 2026-08-17). Rencana pola: `docs/architecture/autoskills-pattern-adoption.md` (commit 37e0c58 di ekosistem). Catatan: ada 6 skill-bank skills overlap (operations/sync/management/ops/integrity/maintenance) — konsolidasi diserahkan ke curator. Skill ini (operations) adalah yang paling komprehensif. Jika menemukan salah satu dari ini aktif, konsultasi skill ini (operations) sebagai sumber utama.

## Skills terkait (overlap —待 konsolidasi)
- `skill-bank-sync` — subset dari skill ini
- `skill-bank-management` — subset dari skill ini
- `skill-bank-ops` — subset dari skill ini
- `skill-bank-integrity` — subset dari skill ini
→ Jika menemukan salah satu dari ini aktif, konsultasi skill ini (operations) sebagai sumber utama. Target: `~/.jcode/skills` (flat), `~/.hermes/skills` (domain), `/Volumes/HermesAgent/HermesAgentUSB/data/skills` (domain). Rekomendasi monitor: up-eco Phase 6-8. Rencana pola: `docs/architecture/autoskills-pattern-adoption.md`. Detail kasus nyata (drift USB 6 file, adopsi autoskills, fix MC `_get_home`): `references/cases-2026-08.md`.

## Alat

### scripts/skill-manifest.py (root ecosystem)
- `python3 scripts/skill-manifest.py` — regenerate `skills/manifest.json` (hash SHA-256 per file + bundleHash per skill). WAJIB setelah tambah/ubah/hapus file di bank.
- `--check` — bank vs manifest; deteksi `[ubah] [hilang] [baru]`; exit 1 = mismatch. up-eco Phase 6d menjalankan ini otomatis.
- `--verify-target DIR --structure flat|domain` — verifikasi salinan target (Jcode = flat, Hermes/USB = domain).
- `--lockfile DIR` — tulis `skills-lock.json` (source + bundleHash + syncedAt) di target.

### skills/sync-to-agents.sh
- Sejak 2026-08-16 sync **SELURUH folder skill** (SKILL.md + references/scripts/assets) via `rsync -a -u` — bukan hanya SKILL.md (bug lama: 8 skill terpotong di target).
- Non-destruktif: file target yang lebih baru TIDAK ditimpa (`-u`). Tidak ada `--delete`.
- Pasca-sync: verifikasi hash tiap target + tulis lockfile. Flag: `--dry-run`, `--verbose`.

## Adopsi skill pihak ketiga (checklist — contoh nyata: accessibility + frontend-design dari autoskills, commit b456769)
1. Cek lisensi: MIT/Apache-2.0 aman; CC BY-NC hanya non-komersial.
2. Copy SELURUH folder: `SKILL.md` + `references/` + `LICENSE` ke `skills/<domain>/<name>/`.
3. Sesuaikan frontmatter ke konvensi bank: `name`, `description`, tambah baris `source:` (asal/registry) + `license:` eksplisit.
4. Update `skills/INDEX.md`: baris tabel di domain yang benar + counter `> **Status:** N ✅ Aktif` + header info.
5. Regen manifest: `python3 scripts/skill-manifest.py` lalu `--check` (0 mismatch).
6. Sync: `bash skills/sync-to-agents.sh` → semua target verifikasi LULUS.
7. Commit + push dengan pesan mencantumkan lisensi & source.
- Gunakan autoskills untuk discovery: `cd <proyek> && npx -y autoskills --dry-run` (deteksi stack → rekomendasi skill; registry ada di clone repo autoskills `packages/autoskills/skills-registry`).

## Resolusi drift target vs bank
- Gejala: `--verify-target` lapor `[ubah]`/`[hilang]` di target.
- Penyebab: rsync -u mempertahankan modifikasi lokal target (by design). File target lebih baru = drift historis yang sah, bukan error sync.
- Keputusan butuh PERSETUJUAN USER — jangan auto-mutasi (audit = rekomendasi):
  - Target lebih baru/lengkap → `cp` target → bank (backport), regen manifest.
  - Bank lebih lengkap → `cp` bank → target (force), lalu sync.
- Setelah resolusi: regen manifest → sync → verify semua target → commit.

## Pitfalls
- **Hermes HOME cache**: `HOME=/Volumes/HermesAgent/.cache/unix-home` dapat berisi folder `Desktop/Niumination` KOSONG. Saat resolve home di script, cek marker BERISI — `Desktop/Niumination/skills` — bukan folder induk. Kasus nyata: `skill_monitor.py _get_home()` cek induk → resolve ke cache kosong → bank scan 0 → 43 conflict palsu "NOT in bank pusat" (fix commit ffb13c4). Jangan regress ke pola cek induk.
- rsync -u ≠ hapus file yang hilang dari bank. Skill dihapus dari bank tetap di target (non-destruktif by design) sampai ada opsi `--prune` eksplisit.
- Sinkronisasi bank → agent via sync-to-agents.sh: hasil copy di agent TIDAK bisa di-patch langsung (curator `created_by=None`) — patch harus di bank, lalu sync ulang.
- Verify setelah sync wajib: jangan klaim "tersinkron" tanpa `--verify-target` LULUS.
- **Purge sensitive data dari git history:** gunakan `git filter-repo` HANYA jika diperlukan (chat ID, secrets di commit lama). **WAJIB** backup `.git` dulu. Pattern: `git filter-repo --replace-text <(echo "PATTERN==>REDACTED") --force`. Setelah itu remote hilang → re-add + force push. Semua collaborator harus clone ulang.

## Verifikasi cepat
```bash
cd ~/Desktop/Niumination
python3 scripts/skill-manifest.py --check          # 0 mismatch
bash skills/sync-to-agents.sh --dry-run            # preview 136 = 68 skill × 2 target (USB diparkir 2026-08-20)
diff -rq skills ~/.jcode/skills | grep -v "\.DS_Store\|lock\|manifest"   # hanya file meta yang beda
```
