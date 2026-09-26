# Conditional migrations: fresh install AND upgrade

A migration that only works on an existing old DB is not done. The same
migration file gets applied twice in production reality: once on a DB that
predates the change, once on a DB that never had the old schema at all
(fresh install, CI, a second machine). Design for both or the next install
breaks.

## Why `CREATE TABLE IF NOT EXISTS` does not save you

A baseline file that guards its `CREATE TABLE` but not its `CREATE INDEX` fails
on upgrade: the table already exists so the create is skipped, then the bare
`CREATE INDEX` runs anyway and dies on a column that the old table lacks. The
error surfaces far from its cause — a route handler at collect-time reporting
`no such column: <newcol>`, with nothing pointing at the migration.

Guard indexes explicitly, or do not guard tables and let one code path own shape.

## SQL cannot express conditional schema change

- SQLite has no `ALTER TABLE IF EXISTS`. Neither does `ADD COLUMN IF NOT EXISTS`.
- Triggers do not help. `BEFORE ALTER` is not a valid SQLite trigger event —
  `CREATE TRIGGER ... BEFORE ALTER ON t` is a syntax error. Confirmed by probe,
  not assumed. There is no per-statement conditional DDL hook in SQLite.

So a baseline `.sql` file that needs "only if the old shape is present" has no
representation. Put that decision in code.

## Split the work: shape in code, data in SQL

- **Code** (a function the migration runner calls before the loop): add/rename
  columns, but only after reading the real shape.
- **SQL file**: only statements that are naturally idempotent — `UPDATE ... SET
  new = 'v4' WHERE new = 'v3'` matches zero rows on a fresh DB, which is
  correct and costs nothing.

### Reading the real shape

```sql
SELECT name FROM sqlite_master WHERE type='table';
PRAGMA table_info(<table>);   -- column list, one row per column
```

`table_exists(t)` / `columns_of(t)` helpers built on those two queries keep the
logic short. Everything else becomes a per-column `if` — verbose but linear and
trivially reviewable, which is the right trade for a one-time migration.

## Column order is a real trap

For a rename-with-data: **add the new column, backfill, then rename.** Rename
first and the backfill has no source column left to read. Symptom is a
`no such column` on the very next line, which sends you looking at the wrong
table.

## Test both directions from one harness

One runner, two fixtures, same assertions. Use the project's **real** migration
runner — a reimplementation in another language has different transaction and
error semantics and will disagree with production on exactly the cases that
matter.

```
case 1: fresh empty file      -> full schema created, seed applied, exit 0
case 2: copy of a real old DB -> row counts unchanged, every value mapped
                                   (e.g. status pending->inbox), exit 0
```

Assert **content**, not exit code: row counts per table before vs after, and a
spot-check that each old value became the intended new value. A migration that
drops every row exits 0 and passes an exit-code assertion.

## Harness bugs that fake a data-loss failure

- Re-copying a fixture into the working path *after* the pre-copy unlink wipes
  it. Snapshot the "before" counts from the original fixture, copy, then run.
- Unlinking the target inside the run helper when the caller already copied it
  there. Give the helper a flag for "already in place" or keep copy and run in
  one function.
- Counting seed rows as a migration failure — seeding belongs to the runner's
  init path, not to the migration's contract.

## Multi-worker builds race the migration runner

A framework that evaluates route handlers across parallel workers will start the
same migration file in several processes at once. Each reads the applied-versions
table, each sees the version missing, each inserts. Result: a uniqueness
violation, or the same DDL applied twice.

Make the claim explicit and check it:

```sql
INSERT OR IGNORE INTO schema_migrations (version, applied_at) VALUES (?, ?)
-- then: if (res.changes === 0) continue   -- another worker already claimed it
```

Check `changes` **inside** the transaction and gate the DDL on that check. Also
make the DDL itself tolerant, because a worker can crash between claiming and
finishing.

## Shape decisions worth making

- Never drop a column in the same migration that stops reading it. Rename
  (`created_at` -> `recorded_at`) keeps old rows auditable; dropping is a
  separate, later, deliberate step.
- Keep the baseline file even once every install has migrated. It is the
  statement of what changed and the fixture for testing case 2.
