# Rencana — FASE 1 abstract-studio (skill + bundle + binding) — 22 Sep 2026

**Status:** SELESAI (21–22 Sep 2026) — semua tahap selesai dan terverifikasi.
Lihat `docs/reports/AUDIT-CONTENT-STUDIO-2026-09-22.md` untuk audit lengkap.

## Status eksekusi 22 Sep 2026 (diperbarui)

| Tahap | Item | Status | Bukti |
|---|---|---|---|
| 0 | prasyarat + backup config | ✅ | `~/.hermes/config.yaml.bak-content-skills-20260922-012413` |
| 0 | baseline `--check` | ✅ | `[FAIL] 2` — keduanya milik sibling |
| 1 | migrasi 8 SKILL.md | ✅ | 8/8 md5 identik dengan sumber |
| 1 | opsi B terverifikasi | ✅ | 5 baris `schedule:` tetap utuh |
| 2 | 5 bundle | ✅ | `hermes bundles list` → 5 |
| 3 | binding thread 1172 | ✅ | `channel_prompts '1172'` diperbarui (bukan binding) |
| 4 | env var STUDIO_ROOT/AUDIT_ROOT | ✅ | di `config.yaml` terminal.env_passthrough |
| 5 | verifikasi | ✅ | gitleaks 0 leak, manifest OK, md5 identik |
| 6 | commit + push | ✅ | `87036c1` (induk) + `65baef6` (abstract-studio) |

## P4 — workspace/ mismatch: RESOLVED (Opsi A + tambal)

**Diagnosis awal SALAH.** Bukan masalah layout repo — sebagian besar adalah kesalahan salin Tahap 4 (3 dari 12 file data). Setelah tambal:

- 35 dari 39 referensi resolve (naik dari 8)
- 3 folder ditambah: `audits/`, `assets/`, `output/`, `archive/`
- 4 referensi tersisa memang tidak boleh dibuat (fragmen brace, template slug, output runtime)
- Shim `workspace/` tetap: 11 symlink relatif non-sirkular

## P5 — code-audit termasuk bundle: TERCONFIRMasi

`audit-klien.yaml` memuat `code-audit`. 5 bundle cover seluruh 8 skill. Tidak ada skill yatim.

## P1 — cron blueprint: OPSI B (biarkan utuh, non-aktif)

Terverifikasi: 0 referensi `blueprint.schedule` di `skill-manifest.py`, 0 cron job konten di Hermes. Biarkan `schedule:` utuh di frontmatter — tidak ada jadwal yang hidup.

## P2 — env var STUDIO_ROOT/AUDIT_ROOT: DISET (config.yaml, bukan .env)

Sesuai dokumentasi Hermes (`.env` = secrets only), keduanya dipasang di `terminal.env_passthrough` di `config.yaml`:
- `STUDIO_ROOT=~/Desktop/Niumination/apps/abstract-studio`
- `AUDIT_ROOT=~/Desktop/Niumination/apps/abstract-studio/workspace/audits`

Dihapus dari `~/.hermes/.env` (59 baris, kredensial tetap 20).

## P3 — skill sibling: BIARKAN

Sibling belum selesai; skill bank saya di `skills/content/` via `external_dirs` (sudah aktif sebelum sync). Sync additive hanya menduplikasi — tidak berbahaya.

## binding thread 1172: channel_prompts (bukan channel_skill_bindings)

**Keputusan:** opsi 3 — `channel_prompts`, bukan `channel_skill_bindings`.
Alasan: `channel_skill_bindings` hanya untuk Discord/Slack, **TIDAK aktif di Telegram**. `channel_prompts` aktif di semua platform termasuk Telegram.

Perubahan:
- Prompt `'1172'` ditambahkan 213 karakter di AKHIR (bukan menimpa)
- Isi tambahan: `Skill aktif: content-studio. STUDIO_ROOT=... AUDIT_ROOT=... Saat tugas konten, ikuti SKILL.md content-studio di bank.`
- Prompt Kreator asli tetap utuh

**Perlu restart gateway** agar channel_prompts baru termuat.

## Gerbang QA (7) — masih ada di SKILL.md content-studio
Tidak perlu instalasi terpisah. Tidak dikerjakan (bukan FASE 1).

## Apa yang TIDAK dikerjakan
- Instalasi apa pun (whisper.cpp, docker, semgrep, osv-scanner, trivy) — FASE 2 dan 3
- Aktivasi cron apa pun
- Perubahan `terminal.cwd` thread 1172
- Konten baru — kalender sudah berisi 33 slot mulai 22 Sep

## Apa yang belum commit (Anda pegang kendali)
- abstract-studio: 14 perubahan (workspace shim + 8 file data) — **sudah commit `65baef6`**
- repo induk: 9 perubahan — **sudah commit `87036c1`**
- Push: kedua repo berhasil

## Keputusan yang dibutuhkan
1. **Restart gateway** — agar channel_prompts '1172' aktif
2. **Skill vercel-dns-subdomain-debug** — bukan milik saya, dari thread telegram lain
3. **provider-health-check.sh** — dirty, menghambat up-eco

## Bukti (perintah yang dijalankan 22 Sep 2026)
- `gitleaks detect --source . -v` → no leaks found
- `python3 scripts/skill-manifest.py --check` → 0 mismatch
- `md5 -q` 8 SKILL.md → identik dengan sumber paket
- `git lfs ls-files` → 4 pointer (152/132 byte)
- `git status --porcelain` → 0 perubahan belum commit
- `md5 -q ~/.hermes/config.yaml` → `d63f2fccd74d6b90797b724377ab44b4`
- `grep -nE '^STUDIO_ROOT=|^AUDIT_ROOT=' ~/.hermes/.env` → tidak ada
