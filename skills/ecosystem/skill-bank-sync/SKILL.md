---
name: skill-bank-sync
description: Maintain the Niumination Skill Bank with integrity verification — manifest SHA-256, full-folder sync to agent targets, drift resolution, and the Hermes HOME-cache path pitfall. Use when sync-to-agents.sh --verify reports GAGAL, when skill-manifest.py --check flags mismatch, when skills look truncated at a target, or when writing scripts that resolve the real user home under Hermes env.
tags:
  - ecosystem
  - skills
  - sync
  - integrity
  - niumination
last_updated: "2026-08-16"
version: 1.0.0
---

# Skill Bank Sync & Integrity (Niumination)

Pola autoskills (midudev) diadopsi 2026-08-16: manifest SHA-256 + verifikasi hash + lockfile. Bank pusat = `~/Desktop/Niumination/skills/` (single source of truth), disinkronkan ke 3 target: Jcode (flat), Hermes local (domain), Hermes USB (domain).

## Tools

| Tool | Peran |
|---|---|
| `scripts/skill-manifest.py` | Generate/verify manifest, verify target, tulis lockfile |
| `skills/sync-to-agents.sh` | rsync bank → 3 target + verify + lockfile + AGENTS.md registry |
| `skills/manifest.json` | SHA-256 per file + bundleHash per skill + domain |
| `scripts/up-eco.sh` Phase 6d | Otomatis cek manifest saat `/up-eco` |

## Manifest commands

```bash
python3 scripts/skill-manifest.py                      # generate skills/manifest.json
python3 scripts/skill-manifest.py --check              # verify bank vs manifest ([ubah]/[hilang]/[baru])
python3 scripts/skill-manifest.py --verify-target ~/.jcode/skills --structure flat
python3 scripts/skill-manifest.py --verify-target /Volumes/HermesAgent/HermesAgentUSB/data/skills --structure domain
python3 scripts/skill-manifest.py --lockfile ~/.jcode/skills
```

`--structure`: `flat` = `<dir>/<skill>/` (Jcode), `domain` = `<dir>/<domain>/<skill>/` (Hermes, USB). **Salah struktur → semua skill dilaporkan hilang (false positive).**

## Sync behavior (sejak 2026-08-16)

- rsync `-a -u` **SELURUH folder skill** — SKILL.md + references/scripts/assets/data ikut (sebelumnya hanya SKILL.md → 8 skill dengan file pendukung terpotong di target)
- Non-destruktif: tanpa `--delete`; file target lebih baru TIDAK ditimpa
- Pasca-sync otomatis: verify hash tiap target + tulis `skills-lock.json` (source + bundleHash + syncedAt)
- AGENTS.md registry punya kolom **File** (jumlah file per skill)

## Drift resolution (saat --verify-target GAGAL)

1. Bandingkan timestamp bank vs target: `stat -f '%Sm' -t '%Y-%m-%d %H:%M' <file>`
2. **Target lebih baru** → skill diedit langsung di agent → BACKPORT target → bank (`cp`)
3. **Bank lebih baru/lengkap** → bank otoritatif → force bank → target (`cp` langsung, lewati `-u`)
4. Regenerate manifest + re-sync + verify semua target
5. Commit dengan pesan arah tiap file; `manifest.json` ikut di-commit

Contoh nyata 16-Ags-26: 5 file USB lebih baru (compliance-checklist-dashboard +40 baris Phase 6 & PWA) → backport; `pemdi-evidence-management/SKILL.md` bank 628 baris vs USB 41 → force bank→USB.

## RTK Activation Check (2026-08-18)

Verify RTK is actually usable, not just installed.

Quick probe:
```bash
bash skills/ecosystem/skill-bank-sync/scripts/check-rtk.sh
```

Manual checks:
```bash
which rtk && rtk --version
echo "echo halo" | rtk rewrite
```

Expected healthy state:
- binary present
- `rtk rewrite` returns rewritten command or exits with passthrough code, **not** `No hook installed — run rtk init -g`
- Hermes plugin `rtk-rewrite` enabled at `/Volumes/HermesAgent/HermesAgentUSB/data/plugins/rtk-rewrite/`
- Claude settings hook present in `/Volumes/HermesAgent/.cache/unix-home/.claude/settings.json`
- `CLAUDE.md` references `@RTK.md`

If missing hook, run `rtk init -g`, ensure `settings.json` hook JSON exists, then restart the host process. Do not assume RTK is active just because the binary exists.

## Pitfall — Hermes HOME cache (bug nyata 16-Ags-26)

HOME=`/Volumes/HermesAgent/.cache/unix-home` berisi folder **KOSONG** (mis. `Desktop/Niumination/`) yang menyesatkan resolusi path. Semua script ekosistem (skill-manifest.py, sync-to-agents.sh, MC `skill_monitor.py`) harus resolve home dengan cek folder KONTEKS, bukan folder induk:

```python
# Pola resolve yang BENAR
if os.path.isdir(os.path.join(home, "Desktop", "Niumination", "skills")): return home
# Bukan: os.path.isdir(os.path.join(home, "Desktop/Niumination"))  ← folder kosong = false positive
```

Bug `_get_home()` di MC pernah: bank scan 0 → **43 conflict palsu** "loaded but NOT in bank pusat". Setelah fix: conflicts 43 → 0.

## Pitfall lain

- Setelah refactor `sync_target()`, counter lama (`jcode_copied`/`hermes_copied`/`total`) TIDAK ada — jangan pakai di log/meta-event curl (error `unbound variable`)
- Bash heredoc Python di sync-to-agents.sh: **escape-drift** `\n` jadi `\\n` literal di dalam string Python — selalu `read_file` dulu sebelum patch, jangan patch dari diff saja
- Patch tool: string dengan `\"` bisa kena escape-drift — pecah jadi patch kecil atau baca file aktual dulu

## Verification

- `diff -r` bank vs target untuk skill besar (impeccable 152 file) → harus identik (kecuali file meta: INDEX.md, .gitignore, .bundled_manifest, lockfile)
- Semua target verify LULUS = 348 file, 0 masalah
- `bash scripts/up-eco.sh` → Phase 6d menampilkan "Manifest SHA-256 sinkron (68 skill, 348 file)"

## HOME / data/skills pruning (F4, 2026-08-20)

Saat `data/skills` (Hermes HOME catalog) membengkak melampaui bank — klasifikasi builtin vs rekonstruksi vs dump, arsipkan (MOVE) dump ke `skills_archive_<date>/`, verifikasi. Alur teruji menurunkan 213 → 113 tanpa merusak bank/builtin. Detail + script: `references/home-pruning-f4-2026-08-20.md`.

## Catatan curator

- Skill `up-eco` (USB) berstatus `created_by=None` (hasil sync Bank Pusat) — **tidak bisa di-patch langsung**; perubahan SKILL.md-nya harus di-backport ke Bank Pusat (`~/Desktop/Niumination/skills/ecosystem/up-eco/SKILL.md`) lalu tunggu sync 6h.
- Overlap potensial untuk curator: `up-eco` (report), `ecosystem-state-sync` (filesystem state), skill ini (skill-bank maintenance).
