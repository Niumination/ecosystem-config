# Writes and reads under a mirrored bank

Depth for Rule 4: what happens to `skill_manage` writes when the bank is both registered
as an `external_dirs` entry and mirrored into the agent skills dir, and how to recover when
the collision blocks the read side.

## Where a write lands

`skill_manage` writes go to the agent's own skills dir — the **mirror**. The bank, which is
the committed source of truth, is left untouched. A patch can report success while the repo
shows no change at all, so a successful write is not evidence the bank was updated.

## Propagating bank-ward

1. Patch via `skill_manage`.
2. Diff the two copies. The edit must appear only on the mirror side, and as pure
   additions. **Zero deletions is the safety check** — a deletion means the copies had
   diverged and copying would destroy bank-only edits.
3. Copy bank-ward, then hash both sides and require them equal.
4. Regenerate the manifest and require 0 mismatch before committing.

Commit only the files you touched. A shared generated artifact (manifest, index, promotion
ledger) may also carry entries from another session's untracked skills — leave that artifact
unstaged rather than absorbing another session's work into your commit.

## The read side deadlocks

The `skill_view` refusal is not limited to loading a skill for use. It also blocks
*inspection*, which makes any read-before-write guard unsatisfiable:

- The bare name fails.
- The categorized path the error message recommends fails identically, because both copies
  already share the full relative path. There is no path form that disambiguates.
- Any workflow requiring a prior read of the colliding skill is therefore unavailable —
  patches to existing skills get refused until the collision is resolved.

Recovery order:

1. Read the file directly by absolute path when you only need the content. Reading does not
   require the loader to disambiguate.
2. Creating a **new** skill still works — a new name has no prior-read requirement and no
   collision. Use this only when a new class-level skill is genuinely warranted; it does not
   solve an existing skill's problem and adds a name that will itself need mirroring.
3. Adding a **new** support file (e.g. under `references/`) needs no prior read either, so it
   remains a viable way to preserve a learning when the SKILL.md body is unreachable.
4. Resolve the collision itself before starting work that depends on reading skills. Treat it
   as a blocker, not a cosmetic warning.

## Blast radius

One collision is not one broken skill — it is every consumer that names a skill by bare
name. Before recommending a remedy, classify each binding as **ambiguous** (present in both
trees), **missing** (name never existed — renamed or never created), or **ok**, and report
`N broken of M total` per consumer. The two failure modes look identical from the outside
and need different fixes.
