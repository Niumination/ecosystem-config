# Standards for Verifiable Evidence in SKP Concepts

## Purpose
Define standards for evidence used in SKP (Surat Keterangan Pelaksanaan) concepts to ensure all activities are verifiable and auditable.

## Evidence Levels

### Level 1: Verified (✅)
- Has DOX file in `~/Desktop/Niumination/docs/reports/`
- Has git commit hash with verifiable message
- Has deployment URL that responds (HTTP 200)
- Has session log with timestamp
- Has manifest file with SHA-256 hash

### Level 2: Partially Verified (⚠️)
- Has file path but no direct link to report
- Has description but no commit hash
- Has domain category but no specific date
- Has approximate count without exact number

### Level 3: Unverified (❌)
- Based on memory only
- No file path or report reference
- No git commit or log
- No deployment URL

## Evidence Standards

### File Evidence
```
Path: ~/Desktop/Niumination/docs/reports/FILENAME.md
Requirement: File must exist and be readable
Verification: read_file() → success = ✅
```

### Git Evidence
```
Commit: abc1234
Command: git log --oneline -1 abc1234
Requirement: Must show commit date and message
Verification: git log → 1 line with date + message = ✅
```

### URL Evidence
```
URL: https://example.com
Command: curl -s -o /dev/null -w "%{http_code}" URL
Requirement: Must return HTTP 200
Verification: curl → 200 = ✅
```

### Session Evidence
```
Query: session_search(query="...", limit=1, sort="newest")
Requirement: Must return session with timestamp + content
Verification: session_search → result found = ✅
```

## Evidence Collection Order

1. Check `docs/reports/` for matching report file
2. Check git log for commit
3. Check deployment URLs
4. Query session history
5. Check `brain/` for audit docs
6. Check `skills-lock.json` for skill bank evidence

## Anti-Patterns

- Never include unverified activities without marking
- Never mark Level 3 as Level 1
- Never forget to verify URL with curl
- Never rely on memory for evidence
- Never skip the evidence collection step

## Evidence Format in SKP

Each activity in the SKP table must have a **Bukti** column:

```markdown
| No | Tanggal | Kegiatan | Area | Bukti |
|----|---------|----------|------|-------|
| 1 | 1 Jul | Aktivasi skill bank | Skill Bank | `skills/INDEX.md` |
| 2 | 6 Jul | TEDEO T1-T4 fixed | Development | `https://tedeo-web.vercel.app` |
```

## Quality Gate

Before generating SKP concept:
- [ ] Every activity has at least Level 1 evidence
- [ ] URLs verified with curl
- [ ] Git commits verified with `git log`
- [ ] File paths verified with `read_file`
- [ ] No Level 3 (unverified) activities included without marking
- [ ] Bukti column filled for every activity
- [ ] Evidence paths are relative to `~/Desktop/Niumination/`