---
name: skill-bank-mirror-integrity
description: Use when a skill bank or its scanner disagrees on count.
version: 1.0.0
---

# Skill bank and mirror integrity

Two classes of task: proving a bank scanner actually sees every skill, and
diagnosing a mirrored bank that makes the skill loader refuse to resolve names.

## Rule 1 — a scanner's printed total is not coverage

A tool reporting "N skills scanned" proves only that it iterated something. The
only coverage evidence is a **set diff** between the keys the scanner discovers
and the keys the manifest declares. Run that diff before trusting any finding
count.

A finding count from a scanner with known coverage gaps is not a finding count:
fix coverage first, then re-count.

## Rule 2 — walk the tree the bank actually has, not the shape you assume

Three traps, all of which produce silently *undercounted* audits rather than
errors:

- **Derive the key from the path, never from a directory object's name.** For a
  hierarchy deeper than `domain/skill`, `parent.name` collapses every subtree to
  the top-level name, so `ecosystem/creative/ffmpeg-ken-burns-motion` and
  `ecosystem/devops/vercel-domain-pointing` both key as `ecosystem`. Use
  `parent.relative_to(bank).as_posix()`.
- **A folder can be a domain *and* a skill.** If `SKILL.md` sits directly in a
  top-level domain folder, a two-level walk never yields it. Check for
  `SKILL.md` in the domain folder itself and emit a bare-name key.
- **Retired skills are not live drift.** Skip any dotted directory (`.git`,
  `.archive`) rather than hardcoding names — hardcoding a plain name like
  `archive` will silently swallow a live domain if one is ever added.

After any scanner fix, require `discovered == manifest` before reading a single
finding.

## Rule 3 — sync through the official pipeline, never by hand

Regenerate the manifest, then sync, then verify, in that order. Copying files
between the bank and a target by hand desynchronises the SHA-256 lockfile and
the registry table, and the drift stays invisible until the next integrity check.

## Rule 4 — a mirrored bank can make the loader refuse every name

When the bank is registered as an external directory **and** it is also synced
into the agent's own skills directory, both copies sit at the *same relative
path*. The loader then sees two candidates for every name, refuses to guess, and
`skills_list` / `skill_view` / curator writes all degrade at once.

Diagnostic signature, in order of appearance:

- `skill_view` returns `Ambiguous skill name '<x>': 2 skills match` and prints
  two paths differing only by parent directory.
- The error advises passing "the full relative path". **That advice cannot work
  here** — both copies already share the full relative path. An absolute path is
  also rejected ("must be a relative path within the skills directory").
- `skills_list` still works, and `skill_manage` refuses writes with
  `read_before_write_required`, because the guard demands a `skill_view` that
  cannot succeed.

Consequence worth stating plainly: a read-before-write guard plus an
unresolvable name means **no existing skill can be patched**. Creating a new
skill still works, since a new name has no prior-read requirement. Do not work
around the guard by reconstructing file contents from a transcript — write the
new umbrella, and hand patches for existing skills to a foreground session where
the collision is resolved.

Also note: a bank registered as an external directory is read-only to
autonomous curation. Skills created *into* that bank may be accepted for the
SKILL.md while support files are refused. When a batch write is refused this
way, everything in the batch rolls back, including the create.

Remedies for the collision, in order of preference, all owner-approved since
they touch config:

1. Exclude the synced mirror from the loader's search path so only the bank
   registers (the mirror becomes a build artifact, not a second source).
2. Keep the mirror but register it under a distinct namespace so relative paths
   differ.
3. Collapse the mirror: stop syncing into the agent skills dir and load from the
   bank directly.

## Reporting shape for a bank-integrity finding

Give exact counts on both sides (discovered, manifest, missing keys, extra
keys), name the fix, and state which side is authoritative. Do not report a
finding count without the coverage diff that justifies it.
