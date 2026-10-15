# autoskills — Study Notes, Gap Analysis & Pola yang Diadopsi

> Sumber: <https://www.autoskills.sh/> + github.com/midudev/autoskills (CC BY-NC 4.0, Node ≥22, 218 skill di registry)
> Rencana adopsi lengkap: `docs/architecture/autoskills-pattern-adoption.md` (repo ekosistem, 292 baris)
> Berkas ini menggabungkan dua catatan lama (`skill-bank-integrity/references/autoskills-patterns.md` +
> `skill-bank-operations/references/autoskills-patterns.md`) saat konsolidasi 18 Sep 2026.

---

## Bagian A — Study Notes & Gap Analysis (2026-08-16)

### Apa itu
`npx autoskills` — scan stack proyek → auto-install skill AI agent kurasi. Tanpa config.
Opsi: `-y/--yes`, `--dry-run`, `-v/--verbose`, `-a <agent>`, `--clear-cache`, `-h`.

### Arsitektur (packages/autoskills/)
- `main.ts` (603 ln): flow CLI + multi-select UI
- `lib.ts` (704 ln): deteksi tech — 6 mekanisme berurutan: package names → package regex → config files → file extensions → Gemfile gems → `configFileContent` (regex isi file config). Support workspace/monorepo.
- `skills-map.ts` (1416 ln): map tech→skill, combo skills, `AGENT_FOLDER_MAP` (.claude→claude-code, .cline, .junie, .codebuddy, .continue, .kiro)
- `installer.ts` (786 ln): integritas SHA-256 per file + `bundleHash`; download dari registry raw GitHub (tag version → fallback main); canonical `.agents/skills/<skill>/` + symlink per agent; `skills-lock.json`
- `sync-skills.mjs`: maintainer-only — fetch upstream → review LLM (status approved/flagged + flags[] + model, default gpt-5.4) → persist ke `skills-registry/` + `index.json`
- `claude.ts`: cleanup section `<!-- autoskills:start/end -->` di CLAUDE.md

### Model keamanan (bagian paling bernilai)
1. Tidak pernah download dari upstream saat runtime — hanya dari registry kurasi
2. Skill di-review LLM anti prompt-injection/supply-chain sebelum masuk registry
3. Setiap file direkam SHA-256 + bundleHash; CLI verifikasi per-file hash, lalu bundle hash, baru tulis
4. `.zip` diblokir; cache per-bundle di `~/.cache/autoskills/`
5. `skills-lock.json` per proyek: `{skill: {source, sourceType, computedHash}}`, keys di-sort

### Gap analysis — Skill Bank Niumination (diukur 2026-08-16)
- Bank saat itu: 40 SKILL.md, 254 file, 8 skill punya file pendukung
- **BUG KRITIS**: `sync-to-agents.sh` (baris 84-194 versi lama) hanya `cp` file SKILL.md per-skill — references/, scripts/, data/, assets/ TIDAK pernah tersinkron. Skill dengan file pendukung terpotong di semua target: impeccable (152 file), ui-ux-pro-max (35), document-content-pipeline (9), plan-compliance-audit (6), pemdi-evidence-management (6), gdpr-compliance (5), compliance-checklist-dashboard (3), agent-reach (2)
- Tidak ada verifikasi hash (up-eco hanya cek frontmatter + INDEX sync)
- Tidak ada audit keamanan konten skill
- Tidak ada lockfile/traceability asal-usul skill

### Rencana adopsi (4 fase) & status
- **Phase 1** — `scripts/skill-manifest.py` → `skills/manifest.json` (sha256 per file + bundleHash per skill, key di-sort) + integrasi up-eco Phase 6c/6d (`--check`, `--verify-target <dir>`). **SELESAI**
- **Phase 2 (P1, paling kritis)** — `sync-to-agents.sh` → rsync `-a -u` seluruh folder skill (TANPA `--delete`), verify via manifest, `skills-lock.json` per target. **SELESAI** (commit `f8b6c53`, `66b7d53`)
- **Phase 3** — `scripts/skill-audit.py` heuristic pattern injection (7 kategori: instruksi tersembunyi/zero-width, exfil base64/`curl|bash`, URL non-allowlist, pola token/secret, path berbahaya, self-modification, frasa prompt-injection klasik). Level warning saja, JANGAN auto-fix. **SELESAI (21 Agu)** + up-eco Phase 6e; baseline 32 temuan (26 URL)
- **Phase 4 (opsional)** — `skill-detect.py`: deteksi stack (pyproject/package.json/composer/Gemfile/go.mod/Cargo.toml) → rekomendasi skill bank. **BELUM**
- Prioritas eksekusi: 2 → 1 → 3

### Definition of Done (versi rencana)
`diff -r` satu skill besar (impeccable) bank vs target = identik; manifest `--check` exit 0; up-eco Phase 6 tampilkan integritas tanpa error.

### Keputusan desain (disepakati)
- Sync tetap non-destruktif (tanpa `--delete`) — konsisten safety "copy/add only, never delete"
- Security scan = warning + rekomendasi, bukan auto-fix (aturan user: audit = saran, bukan mutasi data)
- Adopsi pola secara **konseptual**, bukan salin kode (lisensi CC BY-NC 4.0)
- Multi-fase = tulis plan doc di `docs/architecture/`, minta persetujuan, baru eksekusi

### Risiko yang teridentifikasi
- rsync beda perilaku di macOS → test `--dry-run` dulu; fallback `cp -R -u`
- Manifest basi (file diedit manual) → `--check` berkala via up-eco; regenerate saat ada perubahan
- False positive security scan → level warning + allowlist URL resmi (docs, npm, pypi)
- Skill dihapus dari bank → target stale (non-destruktif; opsi `--prune` eksplisit di masa depan)

---

## Bagian B — 5 Pola yang Diadopsi + Lisensi Skill yang Diadopsi

### 1. Manifest SHA-256
- `skills/manifest.json` — hash per-file + `bundleHash` per skill
- `scripts/skill-manifest.py` — generate, `--check`, `--verify-target`, `--lockfile`
- up-eco Phase 6d menjalankan `--check` otomatis

### 2. Full-folder sync (bukan cuma SKILL.md)
- `rsync -a -u` seluruh folder skill (references/scripts/assets ikut)
- **Bug lama**: dulu hanya copy SKILL.md → 8 skill terpotong di target
- **Fix**: commit `f8b6c53`

### 3. Security audit konten
- Pattern scan: exec patterns, URL mencurigakan, token/secret, self-modification
- Implementasi: `scripts/skill-audit.py` (Phase 3, warning-only)

### 4. Canonical + symlink (belum diadopsi)
- Pola autoskills: 1 canonical di `.agents/skills/` → symlink ke `.claude/skills/`
- Niumination: copy penuh ke tiap target (lebih sederhana, tapi boros ruang)

### 5. skills-lock.json
- Traceability: source + bundleHash + syncedAt per skill per target
- Diimplementasi di `sync-to-agents.sh` (ditulis per target setelah verifikasi hash)

### Lisensi skill yang diadopsi dari registry

| Skill | Lisensi | Source |
|---|---|---|
| accessibility | MIT | addyosmani/web-quality-skills |
| frontend-design | Apache-2.0 | anthropics/skills |
| seo | MIT | addyosmani/web-quality-skills |
| python-testing-patterns | MIT | wshobson/agents |
| fastapi-templates | MIT | wshobson/agents |
| fastapi-python | Apache-2.0 | mindrally/skills |
| flask-api-development | MIT | aj-geddes/useful-ai-prompts |

**Di-skip (4):**
- `python-patterns` — NO-LICENSE (affaan-m)
- `python-executor` — flagged: broad exec + raw install link
- `machine-learning`, `pandas-data-analysis` — tidak relevan

### Limitasi
- `CC BY-NC 4.0` = non-komersial. Pemdi/Diskominfo = instansi pemerintah → boleh.
- Jangan salin kode, adopsi pola secara konseptual.
