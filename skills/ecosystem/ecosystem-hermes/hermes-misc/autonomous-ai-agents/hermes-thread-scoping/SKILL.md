---
name: hermes-thread-scoping
description: Use when auditing multi-thread Telegram agent setup.
---

# Thread scoping: what is isolated, what is shared

A multi-thread agent setup feels like N separate agents. It is not. Some layers are
per-thread, some are process-global, and the gap between them is the whole source of
"it worked in another thread" bugs.

## The layer table — check this before diagnosing anything

| Layer | Isolated per thread? | Where it lives |
|---|---|---|
| Conversation / session transcript | YES | session store, one row per thread, rotates on size or manual reset |
| Persona prompt | YES | one entry per thread id |
| Model + provider override | YES | one pair per thread id |
| Skill binding | YES, per key | prompt-injected list, NOT access control |
| Agent memory file | **NO — single global file** | one memory file per agent, shared budget |
| Skill bank | **NO — single global directory** | one bank, every thread reads every skill |
| Filesystem / shell | **NO — one user, one cwd** | every thread gets the same full shell |

The lower three are process-global. Nothing in thread configuration changes them.

## Why skill bindings are not isolation

A skill binding injects names into the thread's context. It does **not** restrict what
the thread can load. A thread with an empty binding can still load any skill in the
global bank by name.

**Rule:** never promise a user that per-thread bindings sandbox a thread. Describe
them as "default context", and be explicit that the bank is shared.

## The measurable consequence: shared bank, no write gate

The skill-authoring tool writes into the global bank immediately. There is no gate
requiring manifest registration or sync to the runtime skills dir. So:

1. A skill authored in thread A is visible to thread B on the next context load.
2. Any integrity check over the bank starts failing at that moment.
3. The thread that did the authoring sees nothing wrong; the failure surfaces in an
   unrelated workflow that merely runs a health check.

This is the dominant real-world complaint about multi-thread setups. It is not a
config bug — it is the missing step in the authoring workflow.

## Standing operating rule

**Authoring a skill is not finished until the bank is registered and committed.**
Before ending a session that created or edited any skill:

1. Regenerate the bank manifest with the project's manifest tool.
2. Sync the bank into the runtime skills directory if the project keeps a separate
   runtime copy (check whether the runtime path is a symlink or a real second tree —
   if it is a real tree, every author must sync or the runtime drifts).
3. Commit bank + manifest + any docs the change invalidated.

Steps 1–3 are the gate. Skipping them is what makes a later, unrelated check fail in
a way that looks unrelated.

## Pitfalls

- **Do not infer isolation from "separate session ids".** Separate transcripts plus a
  global memory file and a global skill bank is the confusing middle case users hit;
  answer the isolation question with the layer table, not with session counts.
- **Config is the source of truth for runtime values; project registry docs drift.**
  Model names, ports, and enabled flags recorded in a registry markdown file go stale
  silently. Report drift as a finding rather than reconciling from the doc.
- **A dispatch endpoint named in a persona prompt may not be a live daemon.** Before
  reporting an orchestration topology as functional, probe the endpoint. A persona that
  instructs cross-thread dispatch through a dead HTTP endpoint means dispatch has never
  run.
- **Instrument failures reported as tool bugs.** If a high-level tool errors while the
  same operation succeeds through the underlying protocol directly, the transport is
  healthy and the defect is in the tool wrapper. Report it that way and use the direct
  path as the workaround; do not report the capability as broken.
- **Never let a thread-to-thread task carry secrets.** Cross-thread or cross-agent
  tasks exchange task text and results. Credentials referenced by reference (env,
  keychain, vault path), never inline.

## Audit procedure

1. Enumerate threads and ids from the config's per-thread sections.
2. For each thread pull the runtime model/provider pair — from config, not docs.
3. Read the memory file and note fill level against the configured threshold; past
   threshold degrades every thread at once.
4. Count skills in the authoring bank vs the runtime skills directory. A difference
   means two divergent trees.
5. Run the bank integrity/manifest check and report each mismatch with the file and
   whether it is new, changed, or unregistered.
6. Report as a layer table plus a ranked fix list, separating "safe, reversible
   hygiene" from "changes agent behaviour, needs approval".

See `references/config-anatomy.md` for the per-thread config keys and how to read them.