---
name: ecosystem-dox-maintenance
description: Audit and repair DOX/SOUL hygiene across the ecosystem.
tags:
  - ecosystem
  - dox
  - docs
  - maintenance
  - niumination
version: 1.0.0
---

# 🧹 Ecosystem DOX Maintenance

Clean, verify, and enforce DOX hygiene across ecosystem repos.

## Trigger
- `audit DOX`, `rampingkan AGENTS.md`, `ceksize DOX`, `cek duplikasi docs`, `verifikasi SOUL`, `smoke test SOUL`, `one-home rule`, `/dox-audit`
- After any DOX/SOUL change that should be validated before session restart

## Workflow

### 1. Measure DOX size and truncation risk
```bash
wc -c <repo>/AGENTS.md
```
Keep root AGENTS.md < 20KB. Child DOX should also stay under the truncation-sensitive floor; if not, extract the largest tables/sections to `docs/reference/<project>-*.md` and replace with pointers.

### 2. Extract large sections
- Candidate sections: Environment Variables, API route tables, folder structure listings, long deployment notes
- Pattern: extract to `docs/reference/<repo>-<topic>.md`, then replace with:
  ```
  ## Section Name
  > Detail ada di `docs/reference/<repo>-<topic>.md` (auto-generated).
  > Jangan menyalin tabelnya kembali ke sini.
  ```
- Commit extracted files in the same DOX cleanup commit

### 3. Enforce one-home rule
A tracked file must live in exactly one repo. If duplicates exist:
- Pick the owning repo (prefer the project repo for project-specific docs)
- Delete the duplicate from other repos
- Update pointers to absolute/relative paths as appropriate
- Add/update this rule in root Global Agent Rules:
  `Satu file, satu repo-home; berbagi lintas repo hanya via pointer/symlink, bukan salinan tracked.`

### 4. Verify SOUL/dotfiles deployment
```bash
readlink ~/.hermes/SOUL.md
ls -la <dotfiles-repo>/hermes/SOUL.md
shasum -a 256 ~/.hermes/SOUL.md <dotfiles-repo>/hermes/SOUL.md <portable-repo>/SOUL.md
```
Expected: active SOUL.md is a symlink into dotfiles, portable copy matches dotfiles hash.

### 5. Smoke test after restart
Run these checks in a fresh session:
- SOUL identity/persona matches expected version
- `## Bukti` section appears in recap responses
- Prompt injection attempts are refused
- Blind `git add .` is refused
- No truncation warning for root AGENTS.md in session logs

## Mobile-Harness DOX Pattern

Mobile-Harness (`apps/Mobile-Harness/`) requires its own `AGENTS.md` at the project root (not in `docs/`).

The project has extensive documentation:
- `AGENTS.md` — project-level DOX with agent architecture mapping
- `docs/HERMES-AGENT-INTEGRATION.md` — Hermes-specific integration guide
- `docs/DEVELOPMENT-GUIDE.md` — complete development guide
- `README.md` — user-facing documentation

**Rule**: Project-specific integration docs live in `docs/<AGENT>-INTEGRATION.md`. Project-level workflow/docs live in `AGENTS.md`. User-facing docs live in `README.md`. Do not duplicate — reference via pointer.

When updating Mobile-Harness DOX:
1. Update `AGENTS.md` for file mappings and workflow changes
2. Update `docs/HERMES-AGENT-INTEGRATION.md` for Hermes-specific details
3. Update `docs/DEVELOPMENT-GUIDE.md` for development patterns
4. Update `README.md` for user-facing changes
5. Update parent `~/Desktop/Niumination/AGENTS.md` directory tree entry

## Pitfalls
- Do not move files out of a repo without updating pointers; broken pointers are worse than bloat
- Do not commit `file_read_max_chars` or global `context_file_max_chars` increases to mask DOX bloat; fix the DOX instead
- Private repos will 404 from public GitHub API; verify private-repo claims with `git ls-remote`, not raw.githubusercontent.com
- Gateway restart cannot be performed from inside the gateway process; use a separate shell
- **Mobile-Harness specific**: Always update ALL four documentation files when making architectural changes — missing any one creates a DOX gap

## Verification
```bash
wc -c <repo>/AGENTS.md
grep -c "pointer text" <repo>/AGENTS.md
git ls-remote origin HEAD
bash scripts/up-eco.sh 2>&1 | grep -A 3 "SOUL Drift Guard"
```
