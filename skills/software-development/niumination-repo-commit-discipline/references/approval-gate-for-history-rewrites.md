# Destructive operations need an explicit trigger, including self-correction

The gate is not limited to big obvious commands. History-rewriting operations
are destructive, they qualify, and the fact that they arrive as a side effect of
an unrelated fix does not exempt them.

## When a fix rewrites published history

Typical case: a commit was already pushed, then the commit message turns out to
contain a problem — a mangled character, a wrong claim, a secret. The obvious
repair is `commit --amend` followed by a push.

`--amend` on a pushed commit changes the SHA, so delivering it requires a
force-push. That is a history rewrite. It does not become a small operation
because the content is nearly identical.

Correct sequence:

1. Fix the message locally and verify the result.
2. Tell the user the fix requires a force-push, and why.
3. Wait for approval.

Reporting it afterward as a footnote is not the same as asking first. The
approval gate exists to let the owner stop a rewrite before it happens, which is
only possible if the request comes first.

## What is actually irreversible here

Be precise rather than apologetic, and let the user decide:

- Already-pushed commit + `--amend` + force-push: the old SHA becomes
  unreachable from the branch. Anyone with a clone keeps their copy, and if they
  pushed based on it, reconciling costs them a rebase.
- Plain force-push of an unpushed commit: no shared history touched, low risk.
- Deleting a branch, tag, or submodule pointer: shared state, needs approval.
- `git reset --hard`, `clean -fd`, bulk `chmod`, unloading a launchd job: always
  destructive, never assumed.

## A subtle ordering trap

A *new* commit that fixes a problem is always safe. Amending a *pushed* commit
is not. If the fix has not been pushed yet, prefer a new commit over an amend
and the question never arises. Choose the amend path only when the wrong commit
is already public, and ask then.

## Related recurring friction: mangled characters in generated text

This comes up enough in Indonesian/English technical prose to be worth naming.
Long generated files occasionally pick up stray CJK glyphs, usually at a
word boundary where a transliteration was interrupted. Two consequences:

- Commit messages and documentation pick up the same defect.
- The repair triggers the force-push situation above, compounding the cost.

Defensive measure: after writing a long file or a commit message, scan for
characters outside the expected set and print them with their codepoint names.
Catching it before the commit exists removes the need for an amend entirely.
