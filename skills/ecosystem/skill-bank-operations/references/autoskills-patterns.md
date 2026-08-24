# Autoskills Pattern Adoption — Niumination

> Pola diadopsi dari [midudev/autoskills](https://github.com/midudev/autoskills) (6.8k⭐, CC BY-NC 4.0)
> Dokumen lengkap: `docs/architecture/autoskills-pattern-adoption.md` (commit 37e0c58)

## 5 Pola yang Diadopsi

### 1. Manifest SHA-256
- `skills/manifest.json` — hash per-file + `bundleHash` per skill
- `scripts/skill-manifest.py` — generate, `--check`, `--verify-target`, `--lockfile`
- up-eco Phase 6d menjalankan `--check` otomatis

### 2. Full-folder sync (bukan cuma SKILL.md)
- `rsync -a -u` seluruh folder skill (references/scripts/assets ikut)
- **Bug lama**: dulu hanya copy SKILL.md → 8 skill terpotong di target
- **Fix**: commit f8b6c53

### 3. Security audit konten
- Pattern scan: exec patterns, URL mencurigakan, token/secret, self-modification
- Belum diimplementasi (Phase 3 dari rencana)

### 4. Canonical + symlink (belum diadopsi)
- Pola autoskills: 1 canonical di `.agents/skills/` → symlink ke `.claude/skills/`
- Niumination: copy penuh ke 3 target (lebih sederhana, tapi boros)

### 5. skills-lock.json
- Traceability: source + bundleHash + syncedAt per skill per target
- Sudah diimplementasi di sync-to-agents.sh

## Lisensi Skill yang Diadopsi

| Skill | Lisensi | Source |
|---|---|---|
| accessibility | MIT | addyosmani/web-quality-skills |
| frontend-design | Apache-2.0 | anthropics/skills |
| seo | MIT | addyosmani/web-quality-skills |
| python-testing-patterns | MIT | wshobson/agents |
| fastapi-templates | MIT | wshobson/agents |
| fastapi-python | Apache-2.0 | mindrally/skills |
| flask-api-development | MIT | aj-geddes/useful-ai-prompts |

**Skip (4)**:
- `python-patterns` — NO-LICENSE (affaan-m)
- `python-executor` — flagged: broad exec + raw install link
- `machine-learning`, `pandas-data-analysis` — tidak relevan

## Limitasi
- `CC BY-NC 4.0` = non-komersial. Pemdi/Diskominfo = instansi pemerintah → boleh.
- Jangan salin kode, adopsi pola secara konseptual.
