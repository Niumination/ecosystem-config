---
name: gh-pages-build-fix
description: Fix GitHub Pages Jekyll checkout failures.
tags: [github-pages, jekyll, build-fix, lfs, checkout]
---

# GitHub Pages Build Fix

## Overview

When GitHub Pages `pages-build-deployment` workflow fails with checkout errors, use the clean orphan branch approach.

## Root Cause

GitHub Pages automatic build uses `actions/checkout@v4` which fails on repos with:
- LFS-tracked files
- Git submodules
- Large file counts
- `.gitattributes` with LFS filters

## Fix: Clean Orphan Branch

```bash
# 1. Switch to main and reset
git checkout main
git reset --hard origin/main

# 2. Delete existing gh-pages branch
git branch -D gh-pages 2>/dev/null

# 3. Create fresh gh-pages branch
git checkout -b gh-pages

# 4. Clean working tree entirely
git rm -rf -- . 2>/dev/null || true

# 5. Restore ONLY the files needed for Pages
git checkout main -- snapshot/  # or docs/, assets/, etc.

# 6. Commit and force push
git add snapshot/
git commit -m "gh-pages: static content"
git push -f origin gh-pages
```

## Why This Works

- Clean branch has no LFS objects, submodules, or large files
- Jekyll checkout succeeds because working tree is small and clean
- Force push overwrites the broken gh-pages branch

## Alternative: Use GitHub Pages API

If the clean branch approach still fails:

```bash
# Enable Pages via API (bypasses workflow)
gh api --method POST /repos/{owner}/{repo}/pages \
  -F 'source[branch]=gh-pages' \
  -F 'source[path]=/'
```

If Pages returns 409 (already enabled) — that's OK, the API just re-triggers the build.

## Verification

```bash
sleep 60
curl -sI https://<user>.github.io/<repo>/<file> | head -n 1
# HTTP/2 200 = success
```
