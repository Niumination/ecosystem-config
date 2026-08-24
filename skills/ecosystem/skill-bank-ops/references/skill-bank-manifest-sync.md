# Skill Bank Manifest & Sync — Detail Referensi

## Skema skills/manifest.json

```json
{
  "version": 1,
  "generatedAt": "2026-08-17T00:00:00+07:00",
  "skillCount": 47,
  "fileCount": 267,
  "skills": {
    "ponytail-core": {
      "domain": "software-development",
      "bundleHash": "sha256-hex",
      "files": {
        "SKILL.md": "sha256-hex",
        "references/xxx.md": "sha256-hex"
      }
    }
  }
}
```

- `bundleHash` = SHA-256 dari gabungan `"rel:hash"` per file, sorted, join `\n` (pola autoskills installer.ts)
- SKIP: `.DS_Store`, `.git`

## skills-lock.json per target

```json
{
  "version": 1,
  "updatedAt": "ISO8601",
  "skills": {
    "name": { "source": "Bank Pusat", "domain": "...", "bundleHash": "...", "syncedAt": "ISO8601" }
  }
}
```

## Kasus Drift Nyata (2026-08-16)

6 file mismatch di Hermes USB setelah verifikasi hash pertama:

| File | Bank | USB | Keputusan |
|---|---|---|---|
| compliance-checklist-dashboard/SKILL.md | 281 baris | 321 (+Phase 6 indeks aktual, PWA) | backport USB→bank |
| document-content-pipeline/SKILL.md | 30.9KB | 35.8KB | backport USB→bank |
| project-orientation/SKILL.md | 64KB | 74KB | backport USB→bank |
| telegram-router-orchestration/SKILL.md | 17.8KB | 30.4KB | backport USB→bank |
| pemdi-evidence-management/scripts/ocr_macos_vision.py | 1602B | 1805B (+catatan wajib venv Hermes/pyobjc) | backport USB→bank |
| pemdi-evidence-management/SKILL.md | 628 baris | 41 baris (ringkas) | force bank→USB |

Pelajaran: backport bisa membawa perbaikan runtime penting (venv pyobjc note). Selalu cek diff singkat sebelum force satu arah.

## Adopsi 7/11 skill autoskills (2026-08-16)

| Skill | Lisensi | Source repo | Status |
|---|---|---|---|
| accessibility | MIT | addyosmani/web-quality-skills | ✅ adopsi (WCAG 2.2 + references) |
| frontend-design | Apache-2.0 | anthropics/skills | ✅ adopsi |
| seo | MIT | addyosmani/web-quality-skills | ✅ adopsi |
| python-testing-patterns | MIT | wshobson/agents | ✅ adopsi |
| fastapi-templates | MIT | wshobson/agents | ✅ adopsi |
| fastapi-python | Apache-2.0 | mindrally/skills | ✅ adopsi |
| flask-api-development | MIT | aj-geddes/useful-ai-prompts | ✅ adopsi |
| python-patterns | **NO-LICENSE** | affaan-m/everything-claude-code | 🚫 skip |
| python-executor | - | inferen-sh | 🚫 skip (review FLAGGED) |
| machine-learning / pandas-data-analysis | - | pluginagentmarketplace | 🚫 skip (tidak relevan) |

Cek lisensi cepat: `curl -s https://api.github.com/repos/OWNER/REPO/license` → `.license.spdx_id` atau NO-LICENSE.

## Bug _get_home() (MC skill_monitor.py)

```python
# SALAH — folder induk kosong eksis di HOME cache Hermes
if os.path.isdir(os.path.join(home, "Desktop/Niumination")): return home
# BENAR — cek folder BERISI
if os.path.isdir(os.path.join(home, "Desktop", "Niumination", "skills")): return home
```

Gejala: `_scan_skill_bank()` → 0 skills → 40+ conflict palsu "loaded but NOT in bank pusat". Fix: cek `skills/` (folder berisi), bukan folder induk. `_get_home()` di MC: `os.path.expanduser("~")` = `/Volumes/HermesAgent/.cache/unix-home` di env Hermes — folder kosong `Desktop/Niumination/` ada di sana.
