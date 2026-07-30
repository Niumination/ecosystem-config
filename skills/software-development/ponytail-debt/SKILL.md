---
name: ponytail-debt
description: >
  Harvest every `ponytail:` and `NOTICE:` comment in the codebase into a debt
  ledger, so deliberate shortcuts, deferrals, and workarounds get tracked
  instead of rotting into "later means never". Use when the user says "ponytail
  debt", "/ponytail-debt", "what did ponytail defer", "list the shortcuts",
  "ponytail ledger", or "what did we mark to do later". One-shot report,
  changes nothing.
---

This skill tracks two kinds of code-level debt markers:

| Marker | Purpose | Format |
|--------|---------|--------|
| `ponytail:` | Deliberate shortcut with known ceiling | `ponytail: <ceiling>, <upgrade path>` |
| `NOTICE:` | Workaround with removal condition | `// NOTICE: why needed, root cause, source, removal condition` |

## Scan

Grep the repo for comment markers, skipping `node_modules`, `.git`, and build
output:

`grep -rnE '(#|//) ?(ponytail:|NOTICE:)' .`  (add other comment prefixes if your stack uses them)

Each hit is one ledger row. The comment prefix keeps prose that merely mentions
the convention out of the ledger.

## Output

One row per marker, grouped by file.

For `ponytail:`:
`<file>:<line>, <what was simplified>. ceiling: <the limit named>. upgrade: <the trigger to revisit>.`

For `NOTICE:`:
`<file>:<line>, <what the workaround does>. removal: <condition for safe deletion>.`

The `ponytail:` convention is `ponytail: <ceiling>, <upgrade path>`, so pull
the ceiling and the trigger straight from the comment. The `NOTICE:` convention
uses a structured block: notices what, root cause, source, removal condition.

Flag the rot risk: any marker that names no upgrade path, removal trigger, or
removal condition gets a `no-trigger` tag — those are the ones that silently rot.

End with `<N> markers, <M> with no trigger.` Nothing found: `Clean ledger.`

## Boundaries

Reads and reports only, changes nothing. To persist it, ask and it writes the
ledger to a file (e.g. `PONYTAIL-DEBT.md`). One-shot. "stop ponytail-debt" or
"normal mode" to revert.
