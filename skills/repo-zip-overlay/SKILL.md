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

### 2. Extract zip to temp

```bash
rm -rf /tmp/zip-extract
mkdir -p /tmp/zip-extract
unzip -o /path/to/file.zip -d /tmp/zip-extract
```

### 3. Rsync overlay (preserve local config)

```bash
rsync -av \
  --exclude='*.tar.gz' \
  --exclude='config.json' \
  --exclude='data/*.db' \
  --exclude='.git' \
  /tmp/zip-extract/ /path/to/repo/
```

### 4. Force-add ignored files

Some files may be git-ignored but should be tracked:

```bash
git add -f path/to/ignored-file.json
```

### 5. Commit and push

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
- **Don't commit secrets.** If the zip contains actual credentials (not templates), add them to `.gitignore` and exclude from overlay.

## Verification

```bash
# Check status
git status --short

# Review diff
git diff --stat

# Verify no secrets in diff
git diff | grep -i "api_key\|token\|secret\|password" || echo "No secrets in diff"
```
