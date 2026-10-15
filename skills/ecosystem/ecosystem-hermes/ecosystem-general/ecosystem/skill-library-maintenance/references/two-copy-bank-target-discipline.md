# Two-copy skill library (bank + target): which copy a write lands in

The library is two parallel trees: a **bank** (source of truth, version-controlled) and a **target**
(the agent's runtime skills dir, produced by a sync script). Every skill exists in BOTH. This file
covers the discipline that follows from that, and the failure modes that show up when it is ignored.

## The copy question comes FIRST, before writing anything

Determine, for the skill you are about to touch, which tree you are writing to — and confirm it after
the write by diffing the two files. A write that lands in only one tree is the single most common way
skill work is silently lost:

- A change made only in the target is not source of truth. The next full sync overwrites it.
- A change made only in the bank is not live. Sessions keep running the old version until sync.
- A sync run may **quarantine** a target file it considers locally modified rather than overwrite it,
  and then report a hash-verification failure. That failure line is the signal: a quarantined skill
  means your edit went to the wrong place, not that the sync script is broken.

Verify both trees match after any single-skill edit:

```bash
diff -q "<bank>/<category>/<skill>/SKILL.md" "<target>/<category>/<skill>/SKILL.md"
```

## If you cannot name the skill unambiguously, do not guess

When the same name resolves in multiple roots, a loader may refuse to pick one and demand an explicit
path. That refusal is a feature — it means picking wrong would have loaded or edited the wrong copy.

If the ambiguity covers *every* skill (the normal state for a synced two-copy library, because each
skill legitimately exists twice), then:

- Do **not** retry the same name with different prefixes; the collision is structural, not spelling.
- Do **not** create a fresh umbrella skill to work around it. A third copy of the topic is worse than
  an unreachable edit — it fragments the library and hides the real problem.
- Instead: write topical depth into an **existing** skill's `references/` (new support files do not
  require a prior read), and report the loader limitation in your reply so the collision gets a human
  decision (rename, pin, or an explicit-path convention).

## Single-edit checklist

1. Resolve the name to ONE explicit path.
2. Read that file (a read of the other copy's path does not satisfy a read-before-write guard).
3. Edit, then re-read to confirm the edit landed in the file you intended.
4. Diff bank vs target; reconcile by backporting whichever side has the real change.
5. Regenerate the manifest, run the sync, and read the whole sync output — a hash-failure or
   quarantine line means step 1 was wrong.
6. Re-run the sync/manifest in check mode; only a clean result proves convergence.