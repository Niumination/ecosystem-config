---
name: arena-patch-adoption
description: "Use when applying arena.ai zip patch stacks to a repo."
tags: [ecosystem, git, adoption, verification, niumination, arena]
last_updated: "2026-09-23"
version: 1.0.0
---

# Arena Patch Adoption

## Trigger
User drops `niu-oss-vN.zip` (or similar) from arena.ai. Apply it to the target repo, verify, push, update DOX.

## Structure of arena zips
Arena bundles are **cumulative** — each new zip includes ALL previous patches PLUS new patches in a subfolder:
```
niu-oss-v12.zip/
  0001-feat-2026.13-*.patch   ← same as v11 (already applied)
  0002-a11y-2026.13-*.patch   ← same as v11 (already applied)
  ...
  patches-2026.15/
    0001-fix-api-v1-*.patch   ← NEW — only apply this
  LAPORAN-KESIAPAN-PRODUKSI.md
  niumination/               ← snapshot (not a git worktree)
```

## Step 1 — Extract and inventory
```bash
rm -rf /tmp/niu-oss-vN
unzip -q ~/Downloads/niu-oss-vN.zip -d /tmp/niu-oss-vN
ls /tmp/niu-oss-vN/
find /tmp/niu-oss-vN -name '*.patch' | sort
```

## Step 2 — Detect duplicates (skip already-applied patches)
Compare MD5 against previous zip:
```bash
md5 /tmp/niu-oss-vN/0001-*.patch
md5 /tmp/niu-oss-v(N-1)/0001-*.patch
```
Identical MD5 = already applied — skip. Only apply patches with new MD5 or from new subfolders.

## Step 3 — Security audit (new patches only)
```bash
grep -nE 'ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|sk-[A-Za-z0-9]{20,}' \
  /tmp/niu-oss-vN/<new-patches> && echo "ADA RAHASIA" || echo "BERSIH"

grep "^diff --git" /tmp/niu-oss-vN/<new-patches> | grep "package.json" || echo "Tidak ada"
grep "^diff --git" /tmp/niu-oss-vN/<new-patches> | grep ".github/workflows" || echo "Tidak ada"

for f in /tmp/niu-oss-vN/<new-patches>; do
  echo "--- $(basename $f) ---"
  grep "^Subject:" "$f" | head -1
  grep "^diff --git" "$f" | sed 's|diff --git a/||' | cut -d' ' -f1
  echo ""
done
```

## Step 4 — Apply
```bash
cd ~/Desktop/Niumination/sites/niu-oss-dashboard
git fetch origin main 2>&1 | tail -2
git rebase origin/main
git am /tmp/niu-oss-vN/<new-patch-1>.patch
git am /tmp/niu-oss-vN/<new-patch-2>.patch
```
arena base commit is NOT an ancestor of local HEAD — normal; `git am` applies cleanly regardless.

## Step 5 — Verify
```bash
npm run typecheck 2>&1 | tail -3; echo "TC_EXIT=$?"
npm test 2>&1 | grep -E "Test Files|Tests |passed|failed" | tail -4; echo "TEST_EXIT=$?"
python3 ~/Desktop/Niumination/scripts/secret-scan-staged.py 2>&1 | tail -3; echo "SCAN_EXIT=$?"
```
All exits must be 0 before pushing. If `npm test` fails with `AssertionError: expected 'X' to contain 'Y'` in `changelog.test.ts`, see sentinel pitfall below.

## Step 6 — Push
```bash
git log --oneline -4
git push origin main 2>&1 | tail -3; echo "PUSH_EXIT=$?"
```

## Step 7 — DOX update
Update `~/Desktop/Niumination/docs/registry/deployment-status.md` row for `niu-oss`:
- Bump static page count (from patch subject or LAPORAN)
- Note new HEAD commit + patch version label (e.g. `2026.13-14`)
- Commit + push root repo

## Pitfalls

- **Cumulative zips: always MD5-check first.** Applying already-applied patches causes conflicts. `md5 <patch>` is the fastest gate.
- **Test sentinel in `changelog.test.ts`**: patches adding new CHANGELOG entries include a test asserting `out[0].version.toContain('YYYY.NN')`. The next patch adding a newer version breaks this with `AssertionError: expected 'YYYY.NN+1' to contain 'YYYY.NN'`. Fix: 1-line bump in `tests/changelog.test.ts`, commit separately as `test(changelog): bump versi sentinel ke YYYY.NN+1`.
- **Trailing whitespace warning from `git am`**: cosmetic only — AM_EXIT stays 0. Ignore.
- **`vercel domains verify` is not pure JSON**: pipe to `grep -E '"field"'`, not to `python3 json.load(sys.stdin)`.
- **`niumination/` folder in zip is a snapshot, not a git worktree**: use `.patch` files only.
- **Base commit mismatch is normal**: skip `merge-base --is-ancestor` check — it always fails for arena patches.
- **Docs page count from patch subject**: arena reports static page count in patch subject line (e.g. `212 statis`). Use that for DOX updates, not filesystem heuristics.
