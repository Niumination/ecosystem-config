# Safe commits in a shared repo with concurrent agents

Thread groups and sibling agents share one git index. Your partial work and
their partial work sit in the same index simultaneously, so a plain
`git add` + `git commit` can silently publish another agent's staged work
under your commit message. Apply this whenever you commit in
`~/Desktop/Niumination` (repo root, repo SHARED) or any repo another thread
touches.

## Before adding anything

1. Inspect what is ALREADY staged — that is someone else's work-in-flight:
   ```
   git diff --cached --name-only
   ```
   Treat every path listed there as foreign. Do not commit, re-stage, or
   touch it.

2. Stage only your own paths, never a glob or `git add .`.

3. Decide whether to use the index or the pathspec form. If the index is
   clean you may `git add <paths>` then `git commit`. If the index already
   holds foreign staged paths, use `git commit --only` so your commit is
   built from pathspecs and the foreign staging survives untouched.

## The pathspec form (foreign work is already staged)

```git
# 1. unstage my own files so the foreign staging stays exactly as-is
git restore --staged <my-paths>

# 2. confirm the foreign staging is still present
git diff --cached --name-only

# 3. commit by pathspec — this builds a tree from HEAD + my paths only
git commit --only -m "<message>" -- <my-paths>
```

`git commit --only <paths>` is the mechanism. It writes your paths into the
commit without touching the rest of the index, so the foreign staged files
remain staged for their owner.

## After committing, verify three things

```git show --stat --format='%h %s' HEAD   # only my files, no foreign paths
git diff --cached --name-only            # foreign staging still intact
git status --porcelain                   # my edits gone (committed)
```

Do not report success until all three hold. A commit that carries a foreign
path is a worse outcome than a late commit, because the other agent believes
their work is staged and uncommitted.

## Regenerating shared metadata files

If your commit changes the files that a shared index/hash manifest tracks,
expect a disagreement: your regeneration and a concurrent agent's
regeneration both want to be the only one. Do not overwrite the other
agent's in-flight diff to make yours true. Either leave the metadata to
the agent who owns it and note the mismatch, or regenerate only after
confirming no one else is mid-regeneration. A stale metadata file is
recoverable; overwriting another agent's work is not.

## Why this matters

`git add` mutates shared state; `git commit --only` does not. The failure
mode is invisible: the commit succeeds, the pre-commit gates pass (they scan
only what the commit carries, and a foreign path may be harmless), and the
other agent loses a staged file with no warning. The cost is one foreign
path's worth of work with no signal that it is gone.
