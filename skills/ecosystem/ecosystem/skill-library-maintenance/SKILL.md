---
name: skill-library-maintenance
description: "Use when moving, patching, or syncing skills."
version: "1.0.0"
tags: [skills, sync, manifest, bank, quarantine, curation]
---

# Skill Library Maintenance

## Overview

A mirrored skill library keeps two copies of every skill: a **bank** (source of truth, usually
version-controlled) and a **per-agent target** (what the running agent actually loads). This skill
covers the mechanics of changing one without desynchronising the other: which tool writes where,
how paths go wrong, how to resolve drift, and what to prune by hand. It does not restate what the
bank's own management skill says about manifest generation or the ecosystem's DOX rules — it covers
the *mechanics of moving and patching skills across the mirror*.

## Write paths: know which side you hit

| Tool | Writes to | Consequence |
|------|-----------|-------------|
| `skill_manage(create/patch/write_file)` | **target** (`~/.hermes/skills/<domain>/`) | Bank stays stale → next sync quarantines the skill as a conflict. Mirror the file into the bank afterwards. |
| `write_file` / `patch` on the bank path | bank | Target stays stale until you sync. |
| `sync-to-agents.sh` | target (copy only) | Never deletes. Prune removed paths yourself. |

After any `skill_manage` write, diff bank against target. A mismatch means the bank copy is stale
and the skill will be quarantined on the next sync — that is the mechanism behind "target was
edited but git shows nothing".

## Path traps

**`category:` nests once more than expected.** `skill_manage(action='create', category='ecosystem')`
writes to `skills/ecosystem/ecosystem/<name>/`, because the category is appended to a path that
already contains the domain. Omit `category` for a domain-level skill. Detect the damage with
`find skills ~/.hermes/skills -type d -regex '.*/<domain>/<domain>$'` — anchor the regex on the
full doubled path, since a bare `<domain>` pattern also matches skills merely *named* after a domain
and produces a long false-positive list.

**A duplicated skill name cannot be addressed at all.** Once a skill exists in both bank and
target, `skill_view` rejects it as ambiguous — and the bare name, `category/skill`, and
`category/skill/SKILL.md` forms all fail identically, because both sides match by design. When that
happens, skip `skill_view` and read the bank copy directly with
`read_file('~/Desktop/Niumination/skills/<domain>/<skill>/SKILL.md')`. Note that
`skill_manage`'s read-before-write guard demands a `skill_view` that cannot succeed, so a mirrored
skill can be neither read nor patched through the tool path — edit the bank file directly and sync.

## Moving or renaming a skill

1. Back up both sides (`cp -R` the bank dir and the target dir) — a move plus a later prune leaves
   no single artifact holding the old state.
2. `git mv` each tracked skill to the correct path. For an untracked skill, `git add` it first,
   then `git mv`, so the move is recorded as a rename rather than a delete plus an add.
3. `rmdir` the emptied parent directory; `rmdir` refuses while it still has contents, which is a
   free assertion that the move was complete.
4. **Prune the stale target copy yourself.** The sync script only copies, so a bank-only move leaves
   a duplicate in the target forever — a second source of ambiguity errors.
5. Regen the manifest, re-sync, and confirm the hash verification passes with zero quarantined.

## Resolving quarantined drift

A quarantined skill (`⛔ DIKARANTINA (disunting di target)`) is silently not synced. Both sides
drift in practice, and **the newer mtime is often the worse text** — decide by content.

1. `diff` bank against target in full and read the hunks; do not stop at file stats.
2. Ask which side carries the **correction** — a claim later disproved, a hardcoded count that has
   drifted, a richer procedure. That side wins regardless of mtime. A side that merely *looks
   newer* because it absorbed an unverified edit loses.
3. Compare `find <skill> -type f` on both sides. Extra `references/` on one side usually means
   knowledge that never reached the bank; migrate it rather than discarding it.
4. Grep both sides for `references/<file>.md` pointers and confirm each file exists. A pointer to a
   file absent from every commit is a pre-existing dangling ref — drop the pointer instead of
   recreating the file from nothing.
5. Copy the winning side over the loser, regen the manifest, re-sync, confirm `LULUS` / `0 DIKARANTINA`.

## Proving a change landed

Config and routing edits are not self-verifying, and neither are skill moves. Check the specific
claim, not the absence of an error:

- `skill-manifest.py --check` reports 0 mismatch after a path repair or content change.
- The sync output names the skill count and says hash verification passed with nothing quarantined.
- `grep -c ""` on both files when a content change was supposed to be line-count-neutral.
- The target copy exists at the new path **and** the old path is gone.

## Always-on rules

- The bank is the source of truth. A change that lives only in the target is unfinished.
- Never leave a stale copy in a target: the sync does not prune, so you must.
- Never bake a live count (skill totals, catalog sizes, repo counts) into a skill. Write "count
  live, never quote a remembered figure" plus the command that produces the number — a remembered
  figure is wrong by the next sync.
- Flag drift in a DOX or pinned file to the owner instead of editing it silently; DOX files are
  approval-gated.

## Pitfalls

1. **Never treat "sync finished" as "everything synced."** The summary line reports skills copied
   and separately reports quarantined ones; a non-zero quarantine count means content was left
   behind. Read both numbers.
2. **Do not resolve quarantine by forcing the newer file over the older one.** Timestamps record
   when a text was written, not whether it is true; content comparison is the only test.
3. **Do not prune a target directory you have not backed up.** It may be the only copy of
   references the bank never received.
4. **Do not let a `category:` argument silently relocate a skill.** Confirm the resulting path
   before writing the body, or the skill lands one level too deep and gets missed by path-based
   lookups while still appearing in the manifest.
5. **Do not assume a duplicated name is a tool bug to retry around.** It is the expected state of a
   healthy mirror; use the absolute bank path instead.

## Related skills

- `skill-bank-management` — manifest generation, sync pipeline, ecosystem DOX rules (user-owned)
- `hermes-agent-skill-authoring` — SKILL.md frontmatter, validator, structure
- `hermes-config-mutation-safety` — editing `~/.hermes/config.yaml` without silent truncation
