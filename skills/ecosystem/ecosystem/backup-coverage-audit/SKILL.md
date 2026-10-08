---
name: backup-coverage-audit
description: Audit backup gaps before device migration.
---

# Backup Coverage Audit

Use when preparing to sell/migrate a device and need to identify what data is NOT covered by the existing restore/backup repo, then backup those gaps to an external partition.

## Always-on rules

1. **Push uncommitted changes first.** Any git repo with uncommitted changes must be committed and pushed to remote before backup — otherwise the backup is incomplete.
2. **Use `cp -R`, not `rsync`, when symlinks are present.** `rsync -av` follows symlinks and can timeout on large `.git` directories. `cp -R` copies symlinks as symlinks and is more reliable for backup operations.
3. **Check restore repo coverage before identifying gaps.** Read the restore repo's MANIFEST.md and RESTORE-PATHS.md to understand what's already covered.
4. **Verify backup integrity after copy.** Check that key files exist and have correct sizes/permissions.
5. **Socket files cannot be copied.** SSH agent sockets, etc. will fail with `cp` — skip them, they're not valid on another device anyway.

## Procedure

### 1. Inventory the home directory

```bash
du -sh ~/*/ | sort -rh | head -25
ls -la ~/
```

Identify:
- Large directories (>100M)
- Git repos (check for uncommitted changes with `git status --short`)
- Dotfiles and config directories
- Credential files (.env, .ssh, etc.)

### 2. Check restore repo coverage

Read the restore repo's:
- `MANIFEST.md` — what's covered and why
- `RESTORE-PATHS.md` — mapping of repo files to device paths
- `AGENTS.md` — rules and constraints

### 3. Identify gaps

Compare the inventory against the restore coverage. Common gaps:
- `vault/` — often only partially covered (e.g., only secrets.zsh)
- `dotfiles/` — may not have a git remote
- `brain/` — may have uncommitted changes
- `.ssh/` — often only private key is covered
- `~/Backups/` — separate backup folder
- `~/Downloads/` — user files
- Proyek terpisah — separate git repos not in the main ecosystem

### 4. Classify by priority

- **KRITIS**: Credentials, signing keys, uncommitted work, config files
- **TINGGI**: User files, project data, existing backups
- **SEDANG**: Separate tools, plugins
- **RENDAH**: Regenerable cache, test environments, old artifacts

### 5. Backup to external partition

```bash
mkdir -p "/Volumes/<Partition>/Backup Jual Mac"
cp -R <source> "/Volumes/<Partition>/Backup Jual Mac/<destination>/"
```

For directories >1G, run in background with `background=true` and `notify=true`.

### 6. Verify integrity

```bash
ls -la "/Volumes/<Partition>/Backup Jual Mac/<destination>/"
du -sh "/Volumes/<Partition>/Backup Jual Mac/<destination>/"
```

Check key files exist and have correct sizes.

## Pitfalls

- **`rsync -av` follows symlinks and can timeout.** Use `cp -R` for backup operations, especially when `.git` directories are present.
- **Socket files cannot be copied.** SSH agent sockets (`~/.ssh/agent/s.*`) will fail with `cp` — skip them.
- **`.git` directories can be large.** A dotfiles repo with 900M+ of git objects will take time to copy. This is normal.
- **Uncommitted changes in git repos.** Always check `git status` before backup. Push uncommitted changes first.
- **`~/.Trash/` may contain credentials.** Check before deleting or backing up.
- **Large directories can timeout.** Use `timeout` parameter or run in background for directories >1G.
- **Git push may fail if remote has moved.** Use `git pull --rebase` then `git push` to resolve.

## References

- `references/restore-coverage.md` — Niumination ecosystem restore repo coverage map