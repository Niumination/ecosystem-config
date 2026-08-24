# autoskills Patterns — Study Notes & Gap Analysis (2026-08-16)

Sumber: https://www.autoskills.sh/ + github.com/midudev/autoskills (6.8k⭐, CC BY-NC 4.0, Node ≥22, 218 skill di registry).
Rencana adopsi lengkap: `docs/architecture/autoskills-pattern-adoption.md` di repo ekosistem (292 baris).

## Apa itu
`npx autoskills` — scan stack proyek → auto-install skill AI agent kurasi. Tanpa config.
Opsi: `-y/--yes`, `--dry-run`, `-v/--verbose`, `-a <agent>`, `--clear-cache`, `-h`.

## Arsitektur (packages/autoskills/)
- `main.ts` (603 ln): flow CLI + multi-select UI
- `lib.ts` (704 ln): deteksi tech — 6 mekanisme berurutan: package names → package regex → config files → file extensions → Gemfile gems → `configFileContent` (regex isi file config). Support workspace/monorepo.
- `skills-map.ts` (1416 ln): map tech→skill, combo skills, `AGENT_FOLDER_MAP` (.claude→claude-code, .cline, .junie, .codebuddy, .continue, .kiro)
- `installer.ts` (786 ln): integritas SHA-256 per file + `bundleHash`; download dari registry raw GitHub (tag version → fallback main); canonical `.agents/skills/<skill>/` + symlink per agent; `skills-lock.json`
- `sync-skills.mjs`: maintainer-only — fetch upstream → review LLM (status approved/flagged + flags[] + model, default gpt-5.4) → persist ke `skills-registry/` + `index.json`
- `claude.ts`: cleanup section `<!-- autoskills:start/end -->` di CLAUDE.md

## Model keamanan (bagian paling bernilai)
1. Tidak pernah download dari upstream saat runtime — hanya dari registry kurasi
2. Skill di-review LLM anti prompt-injection/supply-chain sebelum masuk registry
3. Setiap file direkam SHA-256 + bundleHash; CLI verifikasi per-file hash, lalu bundle hash, baru tulis
4. `.zip` diblokir; cache per-bundle di `~/.cache/autoskills/`
5. `skills-lock.json` per proyek: `{skill: {source, sourceType, computedHash}}`, keys di-sort

## Gap analysis — Skill Bank Niumination (diukur 2026-08-16)
- Bank: 40 SKILL.md, 254 file, 8 skill punya file pendukung
- **BUG KRITIS**: `sync-to-agents.sh` baris 84-194 hanya `cp` file SKILL.md per-skill — references/, scripts/, data/, assets/ TIDAK pernah tersinkron. Skill dengan file pendukung terpotong di semua target agent:
  - impeccable (152 file), ui-ux-pro-max (35), document-content-pipeline (9), plan-compliance-audit (6), pemdi-evidence-management (6), gdpr-compliance (5), compliance-checklist-dashboard (3), agent-reach (2)
- Tidak ada verifikasi hash (up-eco cuma cek frontmatter + INDEX sync)
- Tidak ada audit keamanan konten skill
- Tidak ada lockfile/traceability asal-usul skill

## Rencana adopsi (4 fase)
- **Phase 1**: `scripts/skill-manifest.py` → `skills/manifest.json` (sha256 per file + bundleHash per skill, key di-sort) + integrasi up-eco Phase 6c (`--check`, `--verify-target <dir>`)
- **Phase 2 (P1, paling kritis)**: `sync-to-agents.sh` → rsync `-a` seluruh folder skill (TANPA `--delete`, tetap non-destruktif), flag `--verify` via manifest, `skills-lock.json` per target
- **Phase 3**: `scripts/skill-audit.py` — heuristic pattern injection (7 kategori: instruksi tersembunyi/zero-width, exfil base64/curl|bash, URL non-allowlist, pola token/secret, path berbahaya, self-modification, frasa prompt-injection klasik). Level warning saja, JANGAN auto-fix.
- **Phase 4 (opsional)**: `skill-detect.py` — deteksi stack (pyproject/package.json/composer/Gemfile/go.mod/Cargo.toml) → rekomendasi skill bank
- Prioritas: **2 → 1 → 3** (Phase 1 membantu verifikasi Phase 2; independen, bisa digabung)
- Definition of Done: `diff -r` satu skill besar (impeccable) bank vs target = identik; manifest `--check` exit 0; up-eco Phase 6 tampilkan integritas tanpa error

## Keputusan desain (sudah disepakati dalam rencana)
- Sync tetap non-destruktif (tanpa `--delete`) — konsisten safety "copy/add only, never delete"
- Security scan = warning + rekomendasi, bukan auto-fix (aturan user: audit = saran, bukan mutasi data)
- Adopsi pola secara konseptual, bukan salin kode (lisensi CC BY-NC 4.0)
- User memilih "buat rencana detail dulu sebagai dokumen" sebelum eksekusi multi-fase → tulis plan doc di `docs/architecture/`, minta persetujuan, baru eksekusi

## Risiko yang diidentifikasi
- rsync beda perilaku di macOS → test dry-run dulu; fallback `cp -R -u`
- Manifest basi (file diedit manual) → `--check` tiap 6h via up-eco; regenerate saat ada perubahan
- False positive security scan → level warning, allowlist URL resmi (docs, npm, pypi)
- Skill dihapus dari bank → target stale (non-destruktif; opsi `--prune` eksplisit di masa depan)
