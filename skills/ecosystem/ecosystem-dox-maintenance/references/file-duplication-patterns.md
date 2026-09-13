# File Duplication Patterns — One-home Rule Enforcement

> Contoh nyata dari sesi 30 Agu 2026: `STATUS-CC.md` di dua repo

## Pattern: Same file, multiple repo homes

### Example 1: `docs/STATUS-CC.md`
**Context**: File status proyek cc-acehtengah
**Before**:
- `ecosystem-config/docs/STATUS-CC.md` (root repo)
- `cc-acehtengah/docs/STATUS-CC.md` (project repo)
- MD5 identical: `1c0fb393d4052f614fc069a046e0d7b9`

**Decision**:
- Owning repo: **project repo** (`cc-acehtengah`)
- Delete from: `ecosystem-config`
- Pointer update: `cc-acehtengah/AGENTS.md` → `services/cc-acehtengah/docs/STATUS-CC.md`

**Rule**: Project-specific docs belong to the project's own repo.

### Example 2: `SOUL.md`
**Context**: Agent identity document
**Before**:
- `dotfiles/hermes/SOUL.md` (source of truth)
- `apps/JHermUSB-portable/SOUL.md` (portable copy)
- `~/.hermes/SOUL.md` (active symlink)

**Decision**:
- Owning repo: **dotfiles**
- Portable copy: read-only snapshot
- Symlink: `~/.hermes/SOUL.md` → dotfiles
- SHA-256 drift guard in `up-eco` Phase 6c

**Rule**: Configuration files live in their designated source repo; copies are snapshots.

## Detection checklist
```bash
# 1. Find identical content
md5sum repo1/file repo2/file

# 2. Check git tracking
git -C repo1 ls-files file
git -C repo2 ls-files file

# 3. Examine differences (if not identical)
diff -u repo1/file repo2/file
```

## Ownership decision tree
1. **Project-specific docs** → project repo
2. **Global config** → dotfiles or ecosystem-config root
3. **Reference docs** → ecosystem-config `docs/reference/`
4. **Temporary/transient files** → not tracked at all

## Quick fix command sequence
```bash
# For duplicate STATUS-CC pattern:
cd ~/Desktop/Niumination
git rm docs/STATUS-CC.md
cd services/cc-acehtengah
git add docs/STATUS-CC.md
# Update pointer in AGENTS.md
git commit -m "DOX: deduplicate STATUS-CC.md via one-home rule"
```

## Anti-patterns to avoid
- ❌ Tracking identical copies in multiple repos
- ❌ Copy-pasting DOX sections instead of referencing
- ❌ Letting portable copies diverge from source
- ❌ Forgetting to update pointers after moving files

## Global Agent Rules addition
```markdown
- **One-home rule:** satu file hanya punya satu repo-home. Berbagi lintas repo hanya via pointer/symlink, bukan salinan yang di-track git.
```

---

## Common duplicate candidates
| File | Typical duplicate locations | Owning repo |
|------|-----------------------------|-------------|
| `STATUS-CC.md` | ecosystem-config/docs/, cc-acehtengah/docs/ | Project repo |
| `SOUL.md` | dotfiles/, JHermUSB-portable/ | dotfiles |
| `model-mapping.md` | docs/reference/, scripts/model-checker-report.md | ecosystem-config/docs/reference/ |
| `skill-registry.md` | docs/reference/, AGENTS.md inline table | docs/reference/ |

---

*Last updated: 30 Agu 2026 — based on SOUL v2.2-final + DOX v4.1 audit*