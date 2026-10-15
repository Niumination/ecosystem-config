---
name: sqlite-schema-migration
description: "Migrate a local SQLite schema without losing rows."
---

# SQLite Schema Migration

For repos that ship a real SQLite file per developer (local-first apps, agent
control planes, dashboards). The failure mode is specific: the new version's
`CREATE TABLE IF NOT EXISTS` migration passes on a fresh clone and dies on the
user's existing DB.

## Procedure

1. **Snapshot read-only before touching anything.** List tables, column names per
   table, and row counts. Decide whether the rows are real data or test noise —
   that decision sets how much care the migration needs.
   ```bash
   sqlite3 "file:$DB?mode=ro" ".tables"
   sqlite3 "file:$DB?mode=ro" "PRAGMA table_info(tasks);"
   ```
2. **Confirm the migration is the problem, not the driver.** Check whether the
   native module is actually built for this arch
   (`node_modules/<sqlite>/build/Release/*.node`). A missing binding and a schema
   conflict surface as the same error class.
3. **Diff old vs new column lists** per table. Any renamed, dropped, or added
   column means `IF NOT EXISTS` will not carry the data across.
4. **Replay the shipped migrations against a COPY, using the app's own runner.**
   Copy the DB, apply migrations in filename order, print row counts before and
   after. The app's runner — not a hand-rolled harness — is the reference.
5. **Write a baseline migration** numbered BELOW the initial one (`000_…`), built
   from `ALTER TABLE` only. No drops, no renames-by-recreate.
6. **Normalize legacy rows that steer runtime behavior.** Old rows carry values a
   fresh seed would never produce — endpoint, adapter, provider, enum status,
   retry policy. Map them onto the values the new version's own seed uses, so an
   upgraded DB behaves like a fresh install.
7. **Re-verify with the real data in place.** Full build, typecheck, lint, and the
   project's integration tests against the upgraded DB.

## Pitfalls

- **`CREATE TABLE IF NOT EXISTS` is not a migration.** It silently skips a table
  that already exists, then `CREATE INDEX` later in the same file still runs
  against the OLD columns and fails with `no such column: <new col>`. The fix is
  an explicit baseline migration, not more `IF NOT EXISTS`.
- **Never trust a green run on an empty DB.** The worst bugs in this class are
  invisible with no rows: a broken index, and a stuck worker queue. If the local
  DB is the deliverable, it is the only test input that matters.
- **`ALTER TABLE … ADD COLUMN … DEFAULT CURRENT_TIMESTAMP` is rejected** — SQLite
  requires a constant default. Add the column bare, then backfill with a literal
  or an `UPDATE` in the same migration.
- **A hand-rolled harness diverges from the real runner.** Implicit-commit and
  transaction behavior differ between drivers and between raw-SQL and
  `executescript` paths, so a harness can report failures the app never sees, or
  hide ones it does. Mirror the runner exactly, including the bookkeeping table
  it creates before the first migration.
- **A relative data path resolved from `cwd` opens a fresh empty DB** when the
  server starts from the wrong directory — which "reproduces" the migration
  cleanly and proves nothing. Resolve the data path once, print it, and assert on
  row counts before and after.
- **Back up before the first write, and verify the backup** by opening it and
  comparing counts. A backup you never opened is a hope, not a rollback.

## Per-mismatch cookbook

| Mismatch | Fix in baseline migration |
|---|---|
| Column renamed | `ALTER TABLE t RENAME COLUMN old TO new;` (SQLite ≥ 3.25) |
| Column added, nullable | `ALTER TABLE t ADD COLUMN new TYPE;` then backfill separately |
| Column added, needs a default | `NOT NULL DEFAULT <const>` — never `CURRENT_TIMESTAMP` |
| Timestamp column added | Add bare, then `UPDATE t SET ts = <literal> WHERE ts IS NULL;` |
| Column dropped upstream | Leave it. Never `DROP COLUMN` — irreversible |
| New table | `CREATE TABLE IF NOT EXISTS` is safe (no pre-existing table) |
| Table the new version ignores | Leave it and its rows in place |

## Fresh-install path

A baseline of `ALTER TABLE` statements fails on an empty DB — there is nothing to
alter. Pick one and document it in the README next to the migration: fresh
installs delete the baseline file, or the runner skips migrations below a
version marker, or each step is guarded by a column check. Undocumented here
becomes the next person's broken clone.

## Verification that counts

- Row counts and table count identical before vs after, on the real DB
- Migration ledger lists every file that ran, in order
- Build + typecheck + lint clean
- Integration suite passing **against the migrated DB**, not a copy
- Fresh-install path still works
