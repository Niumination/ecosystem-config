---
name: repo-zip-overlay
description: "Overlay a zip onto a git repo, preserving local config."
version: "1.0.0"
author: Niumination (Afrizal Munthe)
license: MIT
platforms: [macos, linux]
tags: [git, zip, overlay, repo-update, niumination]
---

# Repo Zip Overlay

Overlay a zip file onto a git repo while preserving local config and excluded files.

## Trigger

User asks to overlay/apply a zip file to a git repository.

## Procedure

### 1. Pull latest from origin

```bash
cd /path/to/repo
git pull origin main
```

### 2. Inspect zip structure first

```bash
unzip -l /path/to/file.zip | head -20
```

Identify which subdirectory holds the project (e.g., `mirai/`). Skip `.hermes/`, `google_drive/`, or other non-project trees.

### 3. Extract zip to temp

```bash
rm -rf /tmp/zip-extract
mkdir -p /tmp/zip-extract
unzip -o /path/to/file.zip -d /tmp/zip-extract
```

### 4. Rsync overlay (project subdirectory only)

```bash
rsync -av \
  --exclude='*.tar.gz' \
  --exclude='config.json' \
  --exclude='data/*.db' \
  --exclude='.git' \
  /tmp/zip-extract/<project>/ /path/to/repo/
```

### 5. Restore regressed files

After rsync, check `git diff` on every modified file. If the zip contained older versions that reverted local fixes:

```bash
git checkout -- <file-that-regressed>
```

### 6. Restore executable bits

```bash
chmod +x memory/skill/wiki/wiki.sh mission-control/tests/mac-verify.sh  # etc.
```

### 7. Force-add ignored files

Some files may be git-ignored but should be tracked:

```bash
git add -f path/to/ignored-file.json
```

### 8. Commit and push

```bash
git add .
git commit -m "feat: overlay <source> — <summary of changes>"
git push origin main
```

## Pitfalls

- **Always pull first.** Overlaying onto a stale repo causes merge conflicts. `git pull` before every overlay.
- **Exclude runtime/secret files.** Never overwrite local `config.json`, `*.db`, `*.log`, or `.env` files from a zip. These are machine-specific.
- **Use `git add -f` for ignored files.** Files like `config.json` are typically git-ignored. If the zip contains a template that should be tracked, use `git add -f`.
- **Check `git diff --stat` before commit.** Verify the overlay produced expected changes. Large unexpected diffs may indicate wrong exclusions.
- **Zip may contain stale versions of recently-fixed files.** Overlaying blindly reverts local fixes (e.g., health.py sysctl paths, traffic.py SQL quoting). After rsync, run `git diff` on every modified file; restore any file that regressed with `git checkout -- <file>`.
- **Executable bits are lost during zip extraction/rsync.** After overlay, re-apply `chmod +x` on shell scripts (.sh, wiki.sh, tests) and verify with `git diff --stat` (mode changes show as 0 insertions).
- **Skip non-project directories in the zip.** Zips may bundle `.hermes/` (test fixtures, not real config), `google_drive/`, or other unrelated trees. Overlay only the project subdirectory (e.g., `mirai/`), not the zip root.
- **Don't commit secrets.** If the zip contains actual credentials (not templates), add them to `.gitignore` and exclude from overlay.

## Verification

```bash
# Check status
git status --short

# Review diff (look for regressed files and mode changes)
git diff --stat

# Verify no secrets in diff
git diff | grep -i "api_key\|token\|secret\|password" || echo "No secrets in diff"

# Verify server still works (if applicable)
curl -s http://127.0.0.1:8800/api/health | python3 -c "import json,sys; d=json.load(sys.stdin); print('ok:', d.get('ok'))"
```
