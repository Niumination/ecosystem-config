# Authoring a Regenerator for a Tracked Derived Artifact

Depth for `derived-artifact-consistency`. Use when an artifact (index, registry table, manifest,
lockfile, catalog) is generated from a source of truth and keeps drifting because nothing
regenerates it — the usual root cause is that no generator ever existed and the file is hand-edited.

## Order of work

1. **Read the artifact as a human would before writing code.** Head it, list every heading level,
   and classify each block: generated (per-section tables, counters), or curated (header banner,
   featured table, conflict notes, prose guides, templates). A generator that rewrites curated
   blocks destroys human work that no source can reconstruct.
2. **Capture the schema per section, not per file.** Two sections in one file routinely use different
   column counts. Read each section's own header row and build new rows to match it (a 5-column
   `| Skill | Status | Source | Ukuran | Deskripsi |` row is garbage in a 4-column table).
3. **Write the builder as a pure function** `build(text) -> (text, log)`; no file I/O inside, so the
   harness can call it repeatedly.
4. Harden it in memory, then run it for real (see below).
5. **Ship a `--check` mode**: build, compare to the current content, print the drift list, exit 1 on
   drift, and never write. Read-only status tools call `--check`; only the fixer writes.

## Idempotency harness (run before the first disk write)

```python
import importlib.util
spec = importlib.util.spec_from_file_location("g", "path/to/gen.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

t0 = open(ARTIFACT, encoding="utf-8").read()
t1, log1 = m.build(t0)
t2, log2 = m.build(t1)
t3, log3 = m.build(t2)
print(len(log1), len(log2), len(log3), t2 == t3)   # require: 0, 0, and True
```

Signatures of a non-convergent writer: run 2 still reports changes; the artifact grows every run; a
section count rises (15 headings → 30 → 45) because blocks appended outside the parsed region are
re-added next pass. Assert in the harness what the writer must preserve: the file's first line, total
member rows, identity uniqueness, and each section's column count.

## Identity and counting

- **identity = the key the consumer checks** (directory basename, lockfile id, stable URL). Display
  metadata (frontmatter `name:`, human title) is for text only and must never decide membership.
- **Count parity test**: unique identities in the artifact vs set size on disk. If the artifact
  legitimately lists a member twice (featured block + per-section table), raw row counts can never
  match — compare unique identities and restrict matches to the row shape that denotes a member, so
  summary rows (`| **Total** | 145 |`) are not counted as members.
- Equal totals are not enough: also require zero members missing and zero orphans, and report both.

## Block parse/rebuild recipe

- Walk the lines; when a section heading matches, collect its body up to the next heading, rebuild the
  body, emit `heading + rebuilt body`; pass every other line through verbatim.
- Insert missing rows directly after the last existing member row of that block.
- **Never cache a line position and reuse it after mutating the list** — insertions shift indices, so
  the next `del lines[i]` removes a heading instead of a row while the script still exits 0.
- Log every add/drop/duplicate with the section name so the run is auditable, and print the category
  counts in the one-line summary.

## Recovery

A non-convergent writer that already ran has corrupted the artifact. Restore the tracked file from git
(`git checkout -- <artifact>`), then run the fixed generator. Never hand-repair rows, and never treat
the corrupted text as the new baseline — the derived file is recoverable precisely because it is
tracked and regenerable.

## Wiring a scheduled fixer

- Fixer script order: regenerate source-derived artifacts → regenerate generated tables/counters →
  run the sync/copy tool → verify hashes both sides → append one log line → exit non-zero only on real
  failure so the scheduler surfaces it. Write the run log append-only to a path outside the repo.
- Keep the logic versioned in the repo, and when the scheduler only accepts scripts from its own
  directory, place a one-line `exec` wrapper there instead of duplicating logic.
- Have the status/audit tool verify that both the wrapper and the scheduled job exist, print the job's
  schedule, and re-create whichever is missing — a fixer nobody can see is a fixer nobody notices is
  gone.
- Prefer the scheduler's script/no-agent mode for deterministic maintenance: no model call, no token
  cost, no prompt drift.
- **Scope policy** (state it in the script header so the next reader knows the boundary): auto-fix may
  rewrite only artifacts that are 100% reconstructible from the source of truth. Commits and pushes,
  deletions, config, credentials, and content judgement stay opt-in flags or manual steps. A fixer
  that commits on its own also collides with whatever a human is committing at that moment.
- **Timestamps defeat content equality.** Regenerators that embed a stamp (`generatedAt`, `_Last sync`, a version banner) make the tracked artifact dirty on every scheduled run even when every hash, count, and member is byte-identical — the tree is never clean and the status check keeps reporting a change nobody made. Verify with a field-level diff (parse both revisions, compare key sets and values) rather than reading the rendered diff, then choose one policy deliberately: auto-commit only when the diff is proven meta-only, leave it dirty for the next session, or list that artifact as expected-dirty in the status check. Never widen a fixer into committing arbitrary changes just to keep the tree tidy.
- **Mark the fixer executable.** A status phase testing `[ -x <script> ]` reports a mode-644 fixer as missing, so `chmod +x` is part of shipping it, not an afterthought.
- **Report by-design noise as info; never hide it.** A sweep across many repos will always see items that change daily by nature (append-only note stores, archives, scratch dirs). Keep an explicit allowlist that downgrades them to informational, print the allowlisted paths in the report, and say which class was de-emphasized — silently excluding them is how a real change goes unnoticed, while shouting about them trains the reader to ignore every warning.

## Meta-only guard for timestamp churn

When the chosen policy is "auto-commit only the proven meta-only churn", ship it as its own script
rather than a branch inside the fixer, so it can be tested and reused.

Commit only when ALL of these hold:

1. HEAD exists, and no `MERGE_HEAD`, `rebase-merge`, or `rebase-apply` sits in the git dir.
2. Nothing is staged (`git diff --cached --quiet`) — never commit over work another session staged.
3. The only modified **tracked** files are the allowlisted artifacts; any other tracked modification
   aborts the guard and is named in the log.
4. Each allowlisted file is proven meta-only: compare `git show HEAD:<path>` against the working copy
   after normalization — replace meta key *values* with a placeholder in structured files (key sets and
   structure still compared) and drop timestamp lines in text files. Never grep for the field NAME:
   words like `generated` also appear in real content such as descriptions.

Behaviour that keeps it safe: untracked files are ignored **because `git add` runs with explicit
pathspecs**, yet they are printed so nothing is hidden; the commit echoes its own file list as scope
evidence; the guard never pushes (local commits accumulate deliberately); and it exits 0 on every
refusal so it cannot kill a scheduler that owns other work.

### Prove the guard in a throwaway repo first

Create a temp git repo holding the allowlisted artifacts plus one extra *tracked* file, then run every
scenario — the negative ones matter more than the positive:

| # | Scenario | Expected |
|---|---|---|
| 1 | only the timestamp changed | commits, and the commit contains ONLY allowlisted files |
| 2 | real content changed (a hash, count, or row) | refuses; tree stays dirty |
| 3 | another tracked file modified | refuses and names it |
| 4 | something already staged | refuses |
| 5 | only untracked files present | commits; untracked content untouched |
| 6 | tree already clean | no-op |

## A writer that grows a file every run

Symptom: the tracked artifact gains a line per run even when nothing regenerated differs.
Mechanism: a writer emitting `before + block + suffix + after` where `after` already begins with a
newline adds one blank line per pass; repeated runs leave dozens of trailing blanks.

Detect: run the writer three times and compare the line count each time — a constant count means
idempotent; a count rising by one per run is a writer bug, not regeneration noise.

Fix: strip leading newlines from the captured suffix before joining (`after.lstrip('\n')`) and add a
separator only when the suffix is non-empty. Clean the damaged file by trimming trailing blank lines
back to a single newline, then re-run to prove the count is now stable.

## Tooling notes for the harness

- Write multi-line test scripts and generators to a file and run the file. Nested-quote heredocs sent
  through a tool layer can arrive mangled and fail as *empty output*, which reads exactly like a
  passing test.
- Run Python checkers with `python3`. Interpreter noise means the invocation was wrong, not that the
  repository is broken — verify the verifier before reporting a finding.
