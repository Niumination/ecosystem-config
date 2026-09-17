# Path migration sweep — classifying and clearing stale pointers

Companion to the "Rename / migrate a docs folder" workflow. Use after any ecosystem-wide path change.

## Where stale pointers actually hide

Sweep these, not just the repo you moved the folder in:

| Location | Why it goes stale |
|---|---|
| Root `AGENTS.md` (DOX) | Pointer lines to registry/status docs |
| `docs/dox/INDEX.md` | Table rows + archive lists + file counts |
| Skill bank `SKILL.md` + `references/` | Conventions that instruct where to extract files |
| Generator scripts (`.sh`, inline Python) | Output paths, often assembled from components |
| `dotfiles/*/SOUL.md`, portable/USB agent copies | Carry the ecosystem pointer list verbatim |
| `skills/manifest.json`, `skills-lock.json` | Hashes change the moment a skill file changes |
| Generated status dumps | Snapshot of an earlier `git status` |

## Classifying residue — live pointer vs noise

After the sweep, every remaining match must be justified. Decide with this table:

| Residue | Verdict |
|---|---|
| Same path string inside **another repo** (e.g. `services/<app>/docs/reference/`) where that folder exists in that repo | **Not ours** — leave it |
| Upstream documentation URLs (`…/docs/reference/foo`) | False positive — leave it |
| Vendored/build trees (`.venv/`, `.build/`, `node_modules/`) | Out of scope — leave it |
| Generated status file (gitignored snapshot) | Regenerates correctly — leave it |
| Historical transcripts, dated archives, plan documents narrating the old path | Leave it; history is allowed to be stale |
| A **live pointer** in DOX, skill, script, or identity file | Must be fixed |

Report the residue as a short list with the verdict per file — "0 left" without this list is unverifiable.

## Commands

**Scope the sweep to the trees you own.** Run it from the ecosystem root only with an explicit path
list (`AGENTS.md docs skills scripts dotfiles apps/<portable>`) — a bare recursive grep from
`~/Desktop/Niumination` descends into `.venv/`, `.build/`, and vendored checkouts, and exceeds a
2-minute tool timeout before it prints anything.

```bash
# 1. Full sweep with counts per file (verifiable total)
grep -rn "<old-path>/" . --exclude-dir=.git --exclude-dir=node_modules \
  | grep -v "<new-path>"
for f in <files>; do printf '%-60s %s\n' "$f" "$(grep -o '<old-path>/' "$f" | wc -l)"; done

# 2. Assembled-path hunt (escapes string replacement)
grep -rn "'<leaf>'", scripts/ skills/*.sh

# 3. Structural proof
ls <new-dir> | wc -l          # expected count
ls <old-dir> 2>&1 | head -1   # expect: No such file or directory
find <new-dir> -type f | wc -l
```

## Ordering rules that bite

- Update the **generator** path before running the generator. Running it first recreates the old folder and turns a finished migration into a live regression.
- Regenerate downstream artifacts **after** all source edits, in dependency order (manifest → check → sync). Intermediate failures (`N mismatch`) usually mean the manifest still holds pre-edit hashes, not that the copy failed.
- `git mv` cannot move a directory whose only contents are gitignored — use `mv`, then re-count.

## Downstream re-sync (skill bank → agent targets)

When the migration touched skill files (a `SKILL.md`, a `references/*.md`), the bank copy and its agent copies must be reconciled. The bank-maintenance skills are user-owned; this is the sequence to follow:

```bash
cd ~/Desktop/Niumination
python3 scripts/skill-manifest.py          # regen — NO --write flag, run bare
python3 scripts/skill-manifest.py --check  # expect: 0 mismatch
bash skills/sync-to-agents.sh              # expect: 0 masalah + verifikasi hash LULUS
```

Reading the output correctly:

| Observation | Meaning | Action |
|---|---|---|
| `[FAIL] — N mismatch (M file dicek)` right after a sync | Manifest still holds pre-edit hashes; the rsync copy itself was fine | Regen manifest, then sync again |
| `[ok] — M file diverifikasi, 0 masalah` + `verifikasi hash LULUS` | Target truly matches the bank | Done |
| `FileNotFoundError: …/<old-path>/registry.md` **after** the copy phase | The script's registry output path is still the old one | Fix the path literal in the script, re-run |

- Never judge success from exit code or a `tail -N` window: grep the log for `verifikasi hash LULUS` / `file diverifikasi, 0 masalah` — those are exactly the lines a short tail cuts off.
- A registry/generator that reappears under the **new** path is the proof the migration held; one that still writes to the old path undoes the whole rename.

## Close-out: nothing left behind

A path migration touches several repos at once (root, nested dotfiles/portable repos, project repos).
Committing locally is not the finish line — check each touched repo against its upstream:

```bash
for r in <repo-1> <repo-2> <repo-3>; do
  printf '%-40s ahead=%s  %s\n' "$r" "$(git -C "$r" rev-list --count @{u}..HEAD)" "$(git -C "$r" log --oneline -1)"
done
```

Every repo must report `ahead=0`. A root repo showing `ahead=N` while the nested repos are clean is
the normal shape here — the migration's commits land in the root first and nothing pushes them for
you. Verify with `git status -sb | head -1` per repo, not from memory of what you committed.

Also re-count the moved payload: the file total must be **identical before and after** the move
(`find <dir> -type f | wc -l`). A count that grew by exactly the number of files you created
deliberately (e.g. a new index) is correct; any other delta means the move dropped or duplicated
content.

