# Deliverable lifecycle: write, verify, then commit

Rules for the gap between "the content exists in my head" and "the content is safely in the repo".
Every one of these comes from a real loss of a long document.

## Never delete the old version before the new one is written

Removing the previous file and writing its replacement in separate steps means an interruption between
them leaves a commit that records **only the deletion**. The document is gone, and the history reads
as a deliberate removal rather than an accident.

- Write the replacement first, or overwrite in place — never `rm` then write.
- Confirm the file exists with a sane length before committing anything.
- If a deletion-only commit has already landed, the fix is a **fresh commit that writes the file**.
  Reverting the deletion restores nothing, because the deletion is all that commit contained.

## Verify a write by re-reading the file, not by the write call's success

A write that reports success and a file containing the intended content are different facts. The gap
surfaces one step later as a zero-length or missing file. After any write that is the sole copy of the
content, check the length and read back the tail.

For a file you are about to overwrite: the write tool may refuse to clobber a file this task has not
read. That refusal is protection, not a bug — read the file, then write.

## Commit each pass of a multi-pass rebuild

Long documents get built across several rounds, often one round per delegated data collection. Commit
per round:

- every intermediate state stays recoverable
- each round's diff is reviewable on its own
- one bad pass does not discard the others

A single commit at the end couples all rounds to the weakest one.

## Anchor markers for iterative insertion

When appending sections to a large HTML file, leave a sentinel comment (`<!-- CONT-MARK-N -->`) as the
insertion point and replace it with new content plus the next marker. This avoids rewriting the whole
file each round — but it has one failure mode: the replacement text usually carries its own closing
`</body></html>`, so after the final insert check the tail and remove the duplicate before committing.

## Deleting or moving a tracked file

Before deleting a reference or file that is the only copy, confirm a copy exists somewhere reachable —
a branch, a release, an archive directory. "It is in git history" is only true if the deletion itself
was committed; an untracked file that gets deleted is gone for good.
