---
name: pre-cleanup-artifact-preservation
description: "Before deleting refs or files, preserve the only copy."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    tags: [git, cleanup, recovery, artifacts, vault, provenance]
    related_skills: [production-secret-rotation, repo-release-hygiene, integration-verification]
---

# Pre-Cleanup Artifact Preservation

Cleanup deletes content that often has exactly one copy. Recover it first, prove the recovery, then delete — and leave a record of where the copy went.

## When to Use

- About to delete a branch, remote-tracking ref, or clone that holds commits whose files were removed from the mainline.
- About to remove files from a repo, or delete a directory, when the only other copy is a workspace you do not control.
- Any "archived privately" artifact produced by an agent or external collaborator: an ephemeral sandbox is not storage, even when the other side describes it as saved.

## Rules

1. **Order is recover → verify → delete.** Never the reverse. A ref that only appears redundant is the usual case: it holds the removed file's last reachable copy.
2. **The other side's claim of a private copy is a self-report.** Verify the *location*: a path inside someone's sandbox, a git-ignored temp dir, or an unpowered volume is not a copy you can restore from. Treat "archived safely" as unproven until you see a durable path.
3. **Verification is size, not count.** "6 files copied" is not a check. Compare each preserved file's byte size against `git ls-tree -r --long <rev>` and require an exact match for every file.
4. **Preserved material goes to a git-ignored path at 600, with a provenance note.** The note names the source commit, why it was removed from the repo, and that it must not be committed. A vault copy without provenance becomes mystery data nobody dares delete.
5. **Deleting is still the owner's call.** Preparing and proving a recovery is reversible work you can do; `git branch -D`, `push --delete`, or removing tracked content is not, until asked.
6. **Keep an unmerged branch alive as a tag, not as a bundle.** `git tag arsip/<tahun>-<bulan>-<topik> <sha>` holds the commits reachable at zero disk cost and restores with `git branch <nama> <tag>`; a `git bundle` duplicates history into a large file for the same guarantee. Deleting a branch whose commits never reached the mainline is a real loss the moment reflog expires — the tag is what makes "cleanup" reversible. Say in the report whether the tag was pushed: a local-only tag is not in any off-device backup, so the user may want it pushed (or dropped) deliberately.
7. **A file counts as a removable duplicate only after two proofs.** (a) Nothing in the repo refers to it — check dependencies, imports, npm/py scripts, build and lint config, and documentation, not one grep. (b) The surviving copy is **byte-identical** — `shasum -a 256` on both sides, not the same filename and not the same size. Report both proofs per file when the owner asks you to confirm nothing needed is being deleted; a batch-level "already checked" does not satisfy that request.
8. **Before deleting a directory, list symlinks that point into it.** A symlink resolved through a deleted directory becomes a dangling entry that still appears in `git ls-files`, so the repo looks intact while twenty paths are broken. Delete the dangling links in the same pass, and mention them in the report — a link to a shared bank outside the repo is useless to a recipient who does not get that bank.

## Procedure

### 1. Inventory what is at risk before touching refs

```bash
git ls-tree -r --long <rev>^ -- <dir>/          # names + sizes of what the ref holds
git log --oneline -1 <rev>                       # confirm this is the commit you think
git reflog --all | grep -E '<sha>|<branch>'      # is it still reachable some other way?
```

### 2. Recover the content from the git objects

```bash
for f in $(git ls-tree -r --name-only <rev>^ -- <dir>/); do
  git show "<rev>^:$f" > "<vault>/$(basename "$f")"
done
chmod 600 <vault>/*
```

Objects stay readable while any ref, reflog entry, or unreachable object holds them — so recovery is still possible *after* a branch delete, but not after a GC that prunes it (`git gc --prune=now`). If the content matters, recover before the cleanup, not after.

### 3. Prove the recovery

```bash
git ls-tree -r --long <rev>^ -- <dir>/ | awk '{print $4}' | sort > /tmp/expect.txt
for f in <vault>/*; do stat -f '%z' "$f"; done | sort > /tmp/got.txt
diff /tmp/expect.txt /tmp/got.txt && echo "sizes match, 1:1"
```

### 4. Confirm the destination is ignored, then write the provenance note

```bash
git check-ignore -q <vault>/<file> || echo "NOT IGNORED — pick another path"
```

The note states: source commit + path, who produced it, why it left the repo, restore command, and "do not commit". Reports that must stay local belong in the same place as this file, never in a public repo.

### 5. Then delete, and say where the copy lives

Delete only what was asked and only after step 3 passed. In the report name the vault path and the backup/ref names, so the next session does not re-derive them or assume the content is gone.

## Pitfalls

- **"Nothing depends on it" must be a sweep, not a grep.** Content can be referenced from outside the repo — agent tooling directories, wrapper scripts, config stores, cron. Enumerate the consumers, and if your first pass was narrow, say so and finish it rather than reporting the narrow result as the conclusion. For a file inside a repo the sweep is concrete: dependency manifest, source imports, package scripts, build/lint/tsconfig config, CI workflow, and the docs. `git status` and `git ls-files` alone prove nothing — symlinks, ignored files, and files referenced only by prose never show up there, which is how leftovers from another project survive a "clean" pass. Find them by grepping the whole tree for the other project's tell-tale names (stack names, the originating repo's name, its distinctive env vars) and inspecting every hit.
- **Deleting a directory silently breaks symlinks elsewhere.** See rule 8: run a dangling-link check before the delete, not after the user notices.
- **A branch that reads like a duplicate still costs a recovery when wrong.** The cheap move is preserve → verify → delete; reconstructing from memory later is not possible.
- **Branch deletion in a clone is not upstream deletion.** `git remote prune` removes stale local copies of refs already deleted remotely — harmless; deleting a local branch that holds the last copy is not. Keep the two apart in both action and wording.
- **Do not "restore" preserved material into a tracked path** to make it visible. That republishes exactly what was deliberately removed.

## Verification

- [ ] Every at-risk file identified from the tree listing (names + sizes)
- [ ] Content extracted to a git-ignored path, 600
- [ ] Size-for-size match against `ls-tree -r --long`, not a file count
- [ ] Provenance note written (source commit, reason, do-not-commit)
- [ ] Deletion limited to what was asked; the report names where the copy lives (vault path **and** any tag/ref kept, with push status)
