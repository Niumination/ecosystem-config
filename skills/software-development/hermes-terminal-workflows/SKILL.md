---
name: hermes-terminal-workflows
description: "Hermes terminal shell pitfalls."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [terminal, shell, workflow, hermes, pitfall]
    related_skills: [plan, project-orientation, verification-before-completion]
---

# Hermes Terminal Workflows

## Background Process Environment

Background terminal processes do not inherit variables exported in earlier foreground calls — a watcher that authenticates fine interactively fails with 401 in background. Inline every export the command needs inside the background command string itself (`export GH_TOKEN=...; gh ...`); never rely on session-persisted env. When a background watcher reports auth errors, suspect the missing environment first, not the credential.

## Extracting Secrets From Files

Extract secret-shaped values with python, never `grep -oE`: the shell layer may route grep through rg, which misparses patterns like `ghp_...` as an encoding flag and fails the whole command. Prefer `python3 -c "import re;print(re.findall(r'PATTERN', open('FILE').read())[0])"`. The `(eval):1: can't change option: zle` preamble on background shells is harmless noise — judge the command by its real output, not the header.

## Core Rule: Foreground-Only

The Hermes `terminal()` tool runs in **foreground only**. It does **not** accept shell backgrounding syntax. Appending `&`, `>/dev/null &`, `nohup ... &`, or `setsid ... &` causes immediate rejection.

**Wrong:**
```python
terminal(command="npm run build &")
terminal(command="sleep 10 &")
```

**Right:**
```python
terminal(command="npm run build", background=true, notify_on_complete=true)
```

The dedicated `background=true` parameter handles process tracking, completion notification, and timeouts correctly. Shell backgrounding bypasses Hermes process management entirely.

## Heredoc Pitfalls

When using heredoc (`<<'EOF'`) in `terminal()`:

1. The terminator (`EOF`) must be the **last thing on its own line** — no trailing spaces, no shell operators after it.
2. Do not append `&` or redirection after the heredoc terminator.
3. If the snippet is long or complex, prefer `write_file()` first, then run it with `terminal()`. A heredoc-fed command can fail SILENTLY (empty stdout, no error line) — treat empty output from a heredoc-fed snippet as FAILURE and re-run it as a written file, never as a legitimate empty result. Anything that must be byte-exact (commit messages, multi-line scripts, generator probes) belongs in a file passed by path (`git commit -F /tmp/msg.txt`, `bash /tmp/x.sh`) rather than a heredoc.
4. An apostrophe inside a `'''` Python string is legal — a `SyntaxError: unterminated string` there means a REAL quoting bug elsewhere in the snippet, so re-read the flagged line instead of re-escaping blindly.
5. If the terminal tool refuses a file-editing command at the approval gate, do not reword and resend shell — switch to the patch/write_file tools for the edit; repeated terminal attempts after a refusal burn turns against the same gate.
6. For batch multi-replacement scripts, assert each old string matches EXACTLY once (`count == 1`) and abort before any write on mismatch — a partial write is harder to unwind than a failed run. Re-include the matched text in the replacement unless you actually mean to delete it: swapping a heading for a new block and forgetting to re-emit the heading silently orphans the section under it. After a batch of replacements, re-read the file and confirm the sections you did NOT touch are still intact.
7. Tool output RENDERS text: non-ASCII separators (e.g. U+2028) display as familiar glyphs and line continuations may appear or vanish. When an exact match fails unexpectedly, `hexdump -C` the region and match the bytes, not the rendering.

## Shell Correctness in Checker/Automation Scripts

Scripts that REPORT on state (checkers, auditors, generators) fail worst when they fail silently: they keep running and print a confident "all clean". Rules that each cost a real false-negative:

- **`find ... -name .git -not -path '*/\.*'` matches NOTHING.** Every `.git` path contains `/.`, so the exclusion clause drops all of them; the loop body never runs and the script reports "no dirty repos". The `-not -path '*/\.*'` idiom is correct for scanning folders, wrong for `.git`. Verify a sweep by running the same `find` bare and comparing counts.
- **`[ test ] && cmd` aborts the script under `set -e`.** When the test is false, the compound command returns 1 and the shell exits — mid-report, with no error message. Use `if ... then ... fi`.
- **`grep -c` in command substitution exits 1 on zero matches** and kills the script under `set -e`. Guard with `|| true` and normalize with `${var:-0}`.
- **`@{upstream}` is fatal when the branch has no upstream configured**: `git rev-list --count '@{upstream}'..HEAD` fails, the `|| echo 0` fallback turns it into a permanent 0, and "N commits ahead" is silently never reported. Resolve the ref defensively and fall back to `origin/<branch>`. Do not assume branches are uniform — in one repo the children tracked upstream and the root did not.
- **Appending a block with `content + '\n' + after` grows the file when `after` already starts with a newline** — one blank line per run, forever. Strip leading newlines from the remainder before joining, then add exactly one separator. Symptom to watch for: a generated file whose line count creeps up on every run while the diff shows only blank lines.
- **Before trusting a generator that rewrites a tracked file, prove idempotency in memory** (`build(build(x)) == build(x)`) rather than on disk, and verify it by running twice and diffing. A non-convergent generator rewrites the file on every cron run and masks the drift it was meant to expose.
- **A false positive is the same bug class as a false negative.** A secret scanner that flags a deliberate bait fixture (`sk-abc...6789` in a scanner self-test) refuses legitimate content forever. Skip candidates carrying placeholder markers (`...`, `<`, `{{`, `REDACTED`, `EXAMPLE`, `xxxx`) rather than loosening the whole pattern.
- **"Skipped" is not "done".** A guard path that prints a notice and `exit 0` (lock contention, empty work queue, missing precondition) makes the caller print `✓` with empty output and `rc=0` — the pipeline can stop doing its job indefinitely while every report stays green. Give "skipped" its own code (e.g. `3`) and make the caller branch on all three cases: `0` done · `3` skipped · anything else failed. Capture with `out=$(cmd 2>&1); rc=$?` between `set +e`/`set -e`, never bare `if out=$(...); then`.

## Copying a Source Tree Over a Mirror (one-way sync)

Pattern: one directory is the source of truth (`bank/`, `dotfiles/`, a config repo) and gets copied
onto one or more mirrors (`~/.hermes/skills/`, `$HOME`, agent config dirs). The copy is usually
`rsync -a` **without** `--delete`, which has two consequences people get wrong in both directions:

- **Mirror-only files survive; divergent same-path files are DESTROYED.** A file created in the mirror
  is never touched (safe, but invisible to the source and to any generated index). A file that exists
  on both sides but was edited in the mirror is silently overwritten by the source version — the newer,
  richer side loses. Never assume `-u`/"only newer" semantics: verify the flags, then assume the source
  wins.
- **`rsync` without `--checksum` may skip a file whose content differs.** The default quick-check
  compares size + mtime, so two files of equal size and equal timestamp but different bytes are treated
  as identical and never copied — the mirror stays stale while the sync reports success. Use
  `rsync -a --checksum` whenever the job is "make the mirror match the source".

To protect mirror-side work while still propagating source updates:

1. **Detect divergence before copying, per file** — compare each mirror file against both the current
   source hash and a snapshot of the last synced state. Divergent + unchanged-since-last-sync means the
   *source* moved (safe to overwrite); divergent + changed-since-last-sync means the *mirror* was edited
   (quarantine: skip that item entirely and report it, never overwrite).
2. **Quarantine, don't merge.** Skipping the item keeps the mirror edit intact and surfaces it for a
   human decision; the sync must still propagate everything else in the same run.
3. **Keep the snapshot honest.** A post-sync state snapshot must NOT record entries for items that were
   quarantined: recording the mirror's edited hash makes the next run read "mirror == state" and conclude
   the source changed, so the protection evaporates after exactly one cycle. Preserve the previous entry.
4. **Ledger the decisions** (promoted / ignored / rejected, plus tombstones for items deliberately
   deleted from the source). Without tombstones, a deleted item still present in the mirror gets
   "re-promoted" and resurrects. Classify mirror-only items before acting: framework-bundled
   (e.g. `.bundled_manifest`), package-manager-installed (e.g. `.hub/lock.json`), tombstoned, or
   genuinely local — only the last class is a promotion candidate. Identify an item by BOTH its folder
   name and its frontmatter `name:`; the two can diverge.
5. **Order matters:** guard (read-only) → promote mirror → regenerate derived manifests → sync →
   verify → commit. Promotion must run before the manifest is regenerated, or promoted items miss the
   index for a whole cycle.
6. **Never auto-commit the results of a promotion/backport step** unless asked — leave the source tree
   dirty so a human reviews what crossed the boundary. When you do commit them, a repo-level secret gate
   may reject a legitimately-planted fixture that came along with a promoted item — fix the fixture
   (assemble the token at runtime so no key-shaped literal exists) and never bypass with `--no-verify`;
   details in `git-security-sanitization`.

**Test the whole pipeline in a sandbox first.** Support env-var path overrides (`BANK_DIR` /
`MIRROR_DIR` read from `os.environ`) since scripts with hardcoded absolute paths cannot be exercised
safely, then drive a matrix: new mirror item → promoted; bundled/installed/tombstoned → ignored;
mirror-edited → conflict; source-changed → not a conflict; run twice → zero changes; state write while a
conflict exists → conflict still detected; sync with a quarantine list → quarantined item untouched while
source changes are still copied. Both defects above surfaced only because the sandbox ran before real data.

## Piped Downloads

Never `curl <url> | <interpreter>` (`curl | python3`, `| bash`) — the security scanner blocks piped-to-interpreter execution as uninspected code. Download to a file first, then run or parse it:
```bash
curl -s --max-time 25 -o /tmp/x.json <url>   # inspectable bytes on disk
python3 -c "import json; d=json.load(open('/tmp/x.json')); ..."
```
Same data, no gate.

## Changing a Multi-Layer Automation Pipeline (map first)

Applies when the task is to change an existing pipeline of scripts (checker → sync → generators →
cron) rather than to write a new one. The correction that produced this section: a day of
individually-correct fixes was rejected as "kenapa hasil kerjamu jadi ribet gini" — the answers were
right, the ordering was wrong.

1. **Map before code.** Before proposing or writing anything, present two things: the structure as it
   exists (which script calls which, which state files must stay consistent) and the list of problems
   still open. Then offer options. Fixing problems one after another without that map loses the reader
   even when every fix is correct.
2. **Budget the layers out loud.** Count the two numbers that make a pipeline expensive: scripts in the
   chain and state files that must stay consistent. Prefer changing a script that exists over adding a
   new one; when a new layer is unavoidable, name its partner explicitly ("script X + state file Y")
   instead of hiding it behind one feature name.
3. **Normalize before refactoring.** Run the pipeline until green, then commit and push everything
   dangling (generated artifacts, promoted content) BEFORE changing or deleting anything. Refactoring on
   a dirty tree risks unsaved work and mixes unrelated diffs into the refactor.
4. **State the data direction.** Say which side is the source of truth and which is the mirror. Adding a
   second direction to a deliberately one-way pipeline has real costs (guard, state snapshot, ledger) —
   write those costs down and get a decision before coding.
5. **Offer decisions as numbered options (A/B/C) with a recommendation**, not as an open question. This
   user answers in one word ("gas", "kerjakan", a letter) and works fastest when the trade-off is
   already stated; do not make them read implementation detail to choose.

## User Continuation Signals

When the user says **"lanjutkan"**, **"continue"**, **"proceed"**, or **"gas"**, treat it as an explicit instruction to continue immediately.

Do **not**:
- Re-summarize completed work
- Ask for confirmation unless the next step is destructive, requires approval, or genuinely ambiguous
- Re-verify already-verified steps

## Persisting Execution State Across Model Switches

For multi-session, multi-PR execution plans, persist state to a durable docs file in the project repo:

- **File location:** `docs/EXECUTION-PLAN-100.md` or equivalent
- **Content per PR:** completed PR with commit SHA, current PR/task, verification evidence, remaining PRs in order
- **Trigger to read:** at the start of any session that says "lanjutkan" or "continue" — read this file before doing anything else

This survives model switches, context compaction, and session restarts.

## Verification-First Pattern

Before claiming work is complete, run the verification commands and confirm output:

```python
terminal(command="npx tsc --noEmit", workdir="/path/to/project")
terminal(command="npx vitest run --reporter=dot", workdir="/path/to/project")
```

Report exact test counts and exit codes. Do not claim success from memory or prior session output.

## Inspecting GUI Terminals Headlessly

`screencapture` needs a live display and fails on a dimmed/locked Mac — prefer the app's own remote control for terminal verification:
- kitty listens on `/tmp/kitty.sock-<pid>` when `allow_remote_control` is on — find it via `lsof -p <kitty-pid> | grep unix`, then address it with `kitty @ --to unix:<sock> ls`.
- Read a tab's scrollback with no display at all: `kitty @ --to unix:<sock> get-text --match id:<window-id>` (match takes WINDOW ids from `ls`, not tab ids).
- Only fall back to `screencapture -x` with a lit display, and say so when reporting.
