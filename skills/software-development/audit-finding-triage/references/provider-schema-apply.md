# Provider-Side Schema Apply — handover recipe

Use when a repo ships SQL (tables, views, RPC/functions) that must be applied by hand in a provider dashboard (Supabase/Neon/…), and the code path degrades gracefully until the objects exist. The deliverable is a guide the owner can run and self-verify, plus the probes they paste back — not a to-do line in your report.

## 1. Enumerate what the code expects

- Grep the app for every RPC/table/view it touches: `.rpc('x')`, `.from('y')`.
- Diff that list against what the SQL files actually create (`create table|view|function`). Anything used but not created is either already live in the provider or silently running on a fallback path.
- Check the call site for a fallback (`try { rpc() } catch { legacy() }`). With one, applying the SQL activates the good path with **no deploy** — say that explicitly so the owner does not wait for a release.

## 2. State order and properties

- File order, plus the fact that the scripts are idempotent (`create table if not exists`, `create or replace`, `create index if not exists`, `alter table … enable row level security`) — so re-running is safe.
- Paste whole files: a truncated paste leaves an object half-defined.

## 3. Protect live objects before overwriting

`create or replace` overwrites whatever is live, and the repo script can be older than the provider's copy (someone edited it in the dashboard). Copy current definitions first:

```sql
select p.proname, pg_get_functiondef(p.oid)
from pg_proc p join pg_namespace n on n.oid = p.pronamespace
where n.nspname = 'public' and p.proname in ('<fn1>','<fn2>');

select pg_get_viewdef('public.<view>', true);   -- ignore the error if it does not exist yet
```

If a live definition differs from the repo script, stop and reconcile before replacing.

## 4. Structure probe (run before and after)

```sql
select p.proname, pg_get_function_identity_arguments(p.oid)
from pg_proc p join pg_namespace n on n.oid = p.pronamespace
where n.nspname = 'public' and p.proname in ('<fn1>','<fn2>');

select table_name, table_type from information_schema.tables
where table_schema = 'public' order by table_type, table_name;

select c.relname, c.relrowsecurity from pg_class c
join pg_namespace n on n.oid = c.relnamespace
where n.nspname = 'public' and c.relname in ('<t1>','<t2>');
```

## 5. Functional probe — structure alone proves nothing

- An atomic counter/limiter must increment: two consecutive calls return 1 then 2, then clean up the probe row.
- An aggregate RPC must return the expected shape, not just exist.

```sql
select public.<bump_fn>('probe:verify', 60000);   -- expect 1
select public.<bump_fn>('probe:verify', 60000);   -- expect 2
select * from public.<table> where key = 'probe:verify';
delete from public.<table> where key = 'probe:verify';
select public.<aggregate_fn>();
```

## 6. State the rollback up front

One line — `drop function public.<fn>(<args>);` — returns the app to its fallback path with no deploy and no data damage. Saying this up front is what stops the owner treating the change as risky.

## 7. Prove RLS is a no-op for the app before recommending it

Enabling RLS is safe only if the app never uses an anon/client key. Count the clients (`createClient`) and the anon-key references: one server-side service-role client plus zero anon references means RLS changes nothing at runtime and the tables close to anon keys. If anon usage exists, policies must be written first.

## 8. Confirm the good path activated

Point at the evidence the owner will see: the fallback's warning line (e.g. `RPC … error`) stops appearing once the object exists. Absence of that warning is the post-apply signal.

## 9. Deliver the SQL so it survives the chat

A long paste-ready block gets truncated in transit (a ~110-line script arrives cut mid-statement), and the owner reports it as a broken message rather than a broken script. Do not resend it the same way — offer, in this order:

1. **Clipboard straight from the repo file** — exact bytes, no retyping, one command:
   `cat <repo>/db/<file>.sql | pbcopy` → "paste into the editor, Run".
2. **Attach the file** (`MEDIA:<absolute path>` on its own line) when they may read it on another device.
3. **Split into labeled parts** (`Part A`, `Part B`), each roughly ≤60 lines, applied in order — safe because the scripts are idempotent.

Say which method you picked and why when a previous attempt was cut off short. Never ask the owner to retype SQL by hand or reflow it from a screenshot.

## 10. Guide format an owner can actually follow

Numbered steps, **one pasteable block per step**, and an explicit **expected result** for each. The failure mode is a wall of theory plus one giant block: the owner cannot attribute an error to an action, and you lose the turn to clarifying questions.

- **One action per step — say so out loud.** "Do not merge the steps" is what makes an error locatable.
- **Expectation line after every step:** `Success. No rows returned` for DDL, the expected row count for a structure probe, `1` then `2` for the counter probe, `{}` being a valid result when there is no data yet.
- **One branching decision, up front:** "if the snapshot is empty → continue; if it has content → paste it here first." A branch, not prose to interpret.
- **Name the error path:** "copy the red message here; do not retry and do not hand-edit — a half-applied `create or replace` can overwrite a live definition."
- **Assert what they should *not* expect:** no deploy, no downtime, rollback is one line.
- **Lead with the step, not the theory** — they are already sitting in the editor. Detail belongs after the steps, or in your own notes.

## 11. "Did it survive?" — the editor is not a transaction

The owner will close the tab, or be offered a **Discard changes** button, and ask whether the apply was thrown away. State the semantics plainly: in these dashboards each **Run** executes and commits immediately — there is no rollback — and discard only drops the unsaved text in the editor buffer. Only an explicit `DROP`/`DELETE` removes an object, so the working assumption is "still there" and the question is confirmable in one query.

Collapse the structure probe into a single row so they can answer with one number each:

```sql
select
  (select count(*) from pg_proc p join pg_namespace n on n.oid = p.pronamespace
    where n.nspname = 'public' and p.proname in ('<fn1>','<fn2>','<fn3>','<fn4>')) as jumlah_fungsi,
  (select count(*) from pg_class c join pg_namespace n on n.oid = c.relnamespace
    where n.nspname = 'public' and c.relname in ('<t1>','<t2>','<t3>','<t4>') and c.relrowsecurity) as tabel_rls_aktif,
  (select to_regclass('public.<table>') is not null) as tabel_ada;
```

Expected `4 | 4 | true`. Put the recovery path in the same message — "if any number is lower, the scripts are idempotent: re-run Part A, Part B, then this query" — so a shortfall is a rerun, not a panic, and never a hand-edit.

**You may not be able to verify provider state yourself — say that instead of implying you did.** A credential in your own env store can point at a different (retired or paused) project, or carry a rotated password, and app-level responses often cannot distinguish "the new object ran" from "the fallback ran" when both produce the same shape — check the call site before claiming you could tell them apart. When neither path works, hand over the single query above and record the outcome as **the owner's check** in the project doc, not as your verification.

## 12. Housekeeping jobs: a commented-out statement is not a scheduler

A table written on every request (rate-limit counters, idempotency keys, event rows) grows without bound unless something deletes it — and schema files usually ship the cleanup as a **comment**, which is easy to read past while verifying "the SQL was applied". If the repo has no `vercel.json`/`crons` entry and no scheduler in the provider, nothing runs it. Say which of the two it is.

Hand the owner the schedule in one paste, with verification and a way back:

```sql
create extension if not exists pg_cron;

select cron.schedule(
  '<job-name>', '17 3 * * *',                      -- UTC; state the local-time equivalent
  $$delete from public.<table> where <expiry-col> < now() - interval '1 hour'$$
);
```

- `cron.schedule` returns the job id (the editor labels the column `schedule`) — a bare `1` is success, not an error. A job id of 1 also means the project had no other scheduled job.
- Verify with `select jobid, jobname, schedule, active from cron.job;`, and read the first run from `cron.job_run_details`.
- Ship the manual `delete … where <expiry>` as both an immediate cleanup and a way to measure how much would be removed, plus `select cron.unschedule('<job-name>')` as the undo.
- Collapse the check into one row (registered / active / rows / expired rows) so the owner replies with four numbers.
- **Quantify the risk instead of dramatising it**: rows × bytes and expected volume, then call it hygiene rather than an incident when that is the truth. A table holding a handful of rows is not a crisis, and saying so is what makes the finding believable.
- If `pg_cron` is unavailable on the plan, offer the app-side fallback (a route plus the platform's cron) as a second option rather than leaving the owner stuck.
