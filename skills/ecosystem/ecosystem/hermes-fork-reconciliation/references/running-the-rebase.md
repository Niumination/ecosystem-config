# Running the rebase — execution mechanics

Depth for the resolution step of `hermes-fork-reconciliation`. Read when you are actually
mid-rebase resolving conflicts, not when planning one.

## Pass `GIT_EDITOR=true` on every `--continue`

```bash
GIT_EDITOR=true git rebase --continue
```

With no editor configured, `--continue` blocks on the commit-message editor and the command
hangs until the tool timeout. The failure is silent and misreads as "a big rebase is slow" —
there is no prompt in the captured output, just no progress. Export it for the whole session
(`export GIT_EDITOR=true`) before starting a multi-patch rebase so no `--continue` can stall.

## Grep for markers AND syntax-check before `git add`

`git add` happily stages a file that still contains `<<<<<<<` markers. The rebase then
continues and commits a broken tree that only fails later, far from the cause. After resolving
each file:

```bash
grep -n '^<<<<<<<\|^=======\|^>>>>>>>\|^|||||||' <file>   # expect no output
python3 -c "import ast; ast.parse(open('<file>').read())"  # expect silence
```

Only then `git add <file>`. A leftover marker usually shows up as a syntax error on the line
after it, so the syntax check catches what the marker grep alone might miss if the marker sits
inside a string or comment.

## Verify an edit landed with the exact string, case included

Confirming a patch by grepping a keyword you invented (an uppercase label, a paraphrased
phrase) returns zero hits and reads as "the edit did not land" — when the file is fine and only
the search term was wrong. Grep a distinctive substring copied verbatim from what was written,
or count a structural marker (`grep -c '^## '` for headings). Distrust a zero-hit verification
before redoing the edit.

## Mixin attribute diagnostics are noise here

The gateway is built from mixins (`GatewayNotificationsMixin` and friends) that reference
attributes and helpers defined on the composed class, not on the mixin itself. The editor/LSP
will report `Cannot access attribute "_foo" for class "...Mixin*"` for lines you never touched.
Do not chase them, and do not "fix" them by adding attribute stubs — they are a property of the
mixin split. Judge an edit by the lint result for *new* errors and by the runtime check, not by
the attribute-access diagnostics.

## Classify a conflict before resolving it

A conflict is not automatically "keep both". Decide which of the three states the carried patch
is in (see SKILL.md), then:

- SUPERSEDED → take upstream's side wholesale for that hunk.
- CONTRADICTED → port: add your branch **around** upstream's path, keep upstream's path intact.
- UNIQUE → take your side.

Concatenating both implementations is the failure mode: two code paths that each try to own the
same decision, where whichever fires first silently wins.
