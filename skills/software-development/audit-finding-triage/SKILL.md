---
name: audit-finding-triage
description: "Triage a large scanner/audit finding set."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [audit, scanner, triage, reporting, verification, security]
    related_skills: [hermes-terminal-workflows, verification-before-completion, git-security-sanitization]
---

# Audit Finding Triage

Turn a large raw finding set from any scanner (secret scanner, content/injection audit, linter, CI warnings, link checker) into something a decision-maker can act on in one read — and stop phantom findings from becoming work.

## When to Use

- A scan/audit produced dozens-to-hundreds of findings and the question is "what do we do with these?"
- The user asks to group, triage, classify, or prioritize findings ("kelompokkan temuan", "mana yang penting", "sort these out")
- Before reporting on any scan whose raw output you have not yet read line by line
- Before acting on a checker's warning: a warning is a claim, not a fact

## Rules

1. **Never hand over a raw finding list.** The deliverable is grouped: a table of `group | count | what it actually is | verdict`, then at most 3–5 concrete actions, then one explicit sentence on how many findings are genuinely risky — which is often zero, and saying so is a useful result, not a cop-out.
2. **Prefer structured output.** Use the tool's JSON mode when it exists (text summaries commonly truncate at ~20 items). Parse it and count per category before reading anything.
3. **Counts must reconcile.** Your group totals must equal the tool's reported total. A mismatch means you mis-parsed the output, not that the tool miscounted.
4. **Verify before acting.** Reproduce each claimed finding with one targeted command (`grep`, `python`) that proves the line does or does not exist. Findings you cannot reproduce are the checker's bug.
5. **Fix the checker, not the data**, when the checker's logic is wrong — otherwise the same phantom finding returns on every run and trains everyone to ignore the checker.
6. **Do not declare the scanner/tool broken from a captured-output artifact.** Read and parse the artifact from disk; a capture layer can differ from the bytes on disk and manufacture a defect. If you already reported one, retract it explicitly in the next message.
7. **A published weakness cannot be un-published by deleting a file.** If a finding concerns a document already pushed to a branch or public repo, remediation is fixing the weakness it describes (run the migration, rotate the credential). Deleting the file only keeps the primary branch tidy — state that limit plainly instead of implying exposure was undone.
8. **Separate "needs action" from "expected" without hiding either.** Members that legitimately change on their own (a notes vault, an archive mirror, a high-churn cache) belong in an explicit allowlist at the check site, keyed by path prefix; their findings stay in the report as information and drop out of the action list and its count. Report the two totals separately ("N need action, M expected") and keep the allowlist an array where the check runs, so admitting a member is a one-line edit. Never suppress an entry silently — a member nobody allowlisted must still surface as actionable, which is the only thing that keeps the allowlist honest.

## Procedure

1. **Bucket by the tool's own categories** first — it already did the cheap classification.
   ```python
   import json, collections
   f = json.load(open("/tmp/scan.json"))
   print(collections.Counter(x["category"] for x in f).most_common())
   ```
2. **Big shallow buckets get a second axis.** URL/host buckets: group by hostname and look only for genuinely risky shapes (IP literals, paste/tunnel services, odd TLDs, lookalike domains). Path buckets: group by directory. Most of these resolve to official documentation — say so with the count.
3. **Small buckets (≤ ~30) get read line by line.** This is where real findings hide and it is the fastest part of the job.
4. **Check the false-positive families** (below) against every remaining finding before calling it real.
5. **Classify each kept finding** as: real and actionable · real but accepted risk (state why) · out of scope. Attach a next step to the first kind only.
6. **Report** in the format from Rule 1, then ask for the decision you need (which group to fix first) rather than offering to fix everything.

## False-Positive Families (check these first)

- **Self-reference** — a document that *describes* the detection pattern gets flagged by it (a scanner's own docs listing `curl|bash`, a skill explaining how the audit works).
- **Keyword collision** — an ordinary word trips a pattern: a UX table containing "Override" next to "system"; documentation containing "Developer Mode" matching a jailbreak pattern.
- **Test fixtures** — `evil.example`, `127.0.0.1.evil.com`, `/etc/passwd` inside a test file are evidence the defence works, not a vulnerability.
- **Tooling markers** — `ascii-guard-ignore`, internal HTML comments, generator banners.
- **Templates and placeholders** — `http://{host}:8188`, `https://url/image.jpg`, `<your-key>` are not endpoints.

## Tuning the Scanner (cut noise without hiding signal)

Fix false positives at the rule, never in the data — an unfixed rule returns the same phantom findings every run and trains everyone to ignore the scanner.

**Fix menu**
- **Expand the allowlist** for hosts/sources you verified by hand, each group with an inline comment naming why it was added. Highest yield when most findings are documentation links.
- **Tighten a pattern that collides with ordinary words** into the context that makes it an instruction (`override … system` → `override … system prompt|instruction|rule|guardrail`) and drop terms legitimate in another domain (`developer mode` on a device/settings table).
- **Skip self-reference** — a document describing the detection pattern is not an instance of it.
- **Skip tooling markers and placeholders** — single-token markers, `{host}`, `<your-key>`, `https://url/image.jpg`.
- **Make a noisy rule contextual instead of deleting it.** Require the dangerous *co-occurrence on one line*: a sensitive path is a finding only when the same line also carries an outbound transmission (`curl|wget|scp|base64|xclip`); an install-pipe (`curl … | sh`) is a finding only when the host is neither the vendor's nor allowlisted. Documentation that *reads* a path or *installs* a tool then stops firing, while the risky shape (upload a private key, pipe an unknown host) still does. State the exempt safe variant in the rule itself — a public `.pub` key beside a private-key path is the case that proves the rule is contextual, not blind.
- **Derive placeholder and fixture vocabulary instead of listing one host at a time.** Uppercase `HOST`/`PORT`, template hosts (`{args.host}`), single-label hosts, any host with no dot, `.local/.example/.invalid/.test`, and any file under `tests|fixtures|examples|samples|mocks` are not endpoints. One pattern per family beats an allowlist that grows forever.

**Verify every noise-cutting edit**
1. Re-run and diff the **per-category** counts (before → after), not just the total.
2. Assert the **highest-severity category is unchanged**. Noise lives in the high-volume, low-severity buckets; if a severity you care about moved, you hid a real finding.
3. After tuning, every survivor should be something you would defend in a report — a real pattern with an accepted reason, a placeholder, or a test fixture. State the survivor count and what it consists of.
4. **Prove detection did not regress with a bait fixture, not by trusting the lower count.** Keep a scratch tree of deliberately dangerous lines (private-key upload, non-vendor install pipe, full-shape token, obviously foreign URL, permissive `chmod`) and run the tuned scanner against it after every pass: each bait line must still produce its finding. A count that dropped while the bait stayed green is an improvement; a count that dropped because a rule stopped firing is silent blindness. Driver: `scripts/bait-bank-check.sh`.
   - **Size the bait to the rule, and keep it out of the repo as a literal.** A bait such as `sk-abc...6789` can never satisfy `\bsk-[A-Za-z0-9]{20,}\b`, so the driver reports a stopped pattern while the scanner is unchanged — the expectation is broken, not the detection. Read the rule regex and give the bait the rule's full shape (minimum length + character classes). Store it assembled at run time (`BAIT="sk-""EXAMPLE""$(printf '%08d' 0)"`) so no key-shaped literal sits in the tree; a commit gate that rejects such a fixture is working correctly and must never be bypassed with `--no-verify` (`git-security-sanitization`).
   - **When a bait line stops firing, diagnose in this order:** (1) does the bait match the rule's regex, (2) does the generated bait file actually contain the token — a placeholder substitution whose anchor does not match writes the file unchanged and still exits 0, (3) only then suspect the rule. Skipping (1) and (2) leads to loosening a rule that was never wrong.
5. **Name the category that must never move.** Usually secrets: its rules stay untouched while the noisy categories are retuned, so any secret-category change during a tuning pass is a bug in the edit, not a discovery.

**A zero-count category is not proof the class is absent — read the rule list.** A scanner reports on the patterns it has. Before telling anyone a category is clean, compare its pattern list against the credential and artifact shapes this estate actually uses (JWTs for hosted backends, provider key prefixes, signed URLs). A missing class reports as "none found", which is indistinguishable from "verified clean" — and it is the one failure mode that looks like good news, so nothing else in the run will flag it.

**When you add a secret pattern, require the full shape and prove it fires.** Secrets also appear in documentation as (a) rule definitions that contain the prefix literally (`eyJ[a-zA-Z0-9_-]+\.…`) and (b) truncated examples (a bare JWT header such as `eyJhbGciOiJIUzI1NiIs`). A prefix-only pattern flags both and gets deleted in disgust. Match the real structure — every segment present, with realistic minimum lengths — then test both directions in one pass: a synthetic full-shape value must match, and both documentation shapes must not. Report which forms you tested; "0 findings" only means something once the pattern is proven able to fire.

**Scan tracked files to answer "is it published?", not the working tree.** The same string in an untracked or retired copy is a different severity than one in a tracked file of a public repo (`git grep` vs a filesystem grep), and the distinction decides whether you are looking at a leak or a local note.

**A count that moves between two runs is not a tool bug until you diff the inputs.** Adding one line that mentions a watched path adds findings legitimately; check whether the two output modes agree with each other on the same input, reproduce from the artifact on disk, and retract plainly if a defect was already reported.

## Pitfalls

- **A checker that dies mid-run produces a normal-looking truncated report.** Later phases silently never execute. Compare section/line counts before and after any edit; exit code 0 proves nothing (mechanism and fix: `hermes-terminal-workflows`, "Checker Scripts: Failure Modes That Hide").
- **Fixed path-component parsing fabricates findings.** `cut -d/ -f2` mis-names nested items (`mlops/inference/llama-cpp` → `inference`), inventing duplicates and "missing" entries. Name items by the directory holding their marker file: `basename "$(dirname "$rel")"`.
- **Hand-maintained counters in docs drift silently.** If a checker validates a derived list, extend it to validate the human-typed total too, against the tool-generated source of truth.
- **Don't equate "many findings" with "many risks".** A high count usually measures the scanner's noise floor, not the system's health; report both numbers so the user can see which is which.
- **Severity must come from potential impact, not from your opinion of the rule.** A finding with no path to harm is low even if the pattern sounds alarming.

## Handing Findings Back to Whoever Must Fix Them

When the fix belongs to an external author (an agent on another platform, a third-party repo, a vendor), the deliverable is not a report alone — it is work they can execute without you:

- **Two messages, not one.** A verdict comment (what is verified good, what must change first, what is optional), then a task list. Mixing them buries the tasks.
- **Make acceptance criteria machine-checkable**, one per task, in the same form you will re-run to verify: a `git ls-tree`/`git show`/grep that must return a specific thing, CI green, and "no changes outside this list". A criterion you cannot execute is not a criterion.
- **Ask for a new commit, not a history rewrite** — review stays cheap and the reviewer's own rules about history stay intact.
- **Keep the public message free of the weakness it asks to remove.** If the task is "take that weakness map out of the public repo", the public comment must not restate the weakness. Describe the follow-up action generically ("make sure the schema in `db/` is applied on the provider"), never the mechanism.
- **Verify their fix by re-running your own criteria commands**, not by reading the summary they post back.
- **Read the commit's file list, not just the tree.** One API call returns status + filename for every file, which is what proves the fix touched exactly what was asked and nothing else — a convenience change smuggled in beside the fix is the failure this catches.
- **Run the tests the pipeline does not run.** If CI only lints and builds, fetch the branch locally and execute the suite yourself before commenting; that is the only thing that turns "N/N tests pass" into evidence.
- **Prove a CI step ran; never accept green alone.** Query the run's jobs and read the per-step conclusions — a step that exists but was skipped still shows a green pipeline.
- **Treat their numbers as approximate.** "Zero occurrences" may mean "one occurrence, correctly placed in a server log". Check the context, state the correction plainly, and still accept a fix that is substantively right.
- **Attribute an owner-run step to the owner when you record it.** When the last mile can only be executed in someone else's dashboard, you can verify your side (public endpoints, repo state, object inventory they paste back) and nothing more. Write the project doc line as *their* check (`checked by owner in the SQL Editor`) instead of phrasing it as your own verification, and say the same in the reply — a doc line that implies you confirmed provider state is a claim you cannot defend later.
- **A closing doc pass is the cheapest moment to fix an overstated line you pass anyway.** While marking the task done you will read surrounding entries; when one claims more than the evidence supports ("tests run in CI" for a pipeline that never ran them, a runner version nobody checked, a count nobody re-counted), correct it in place. Leaving it is a false claim that outlives the session and gets quoted as fact.
- **Widening scope to satisfy a criterion is legitimate — record it.** An author may delete more documents than you named in order to make "that folder is empty" true. Note it as scope expansion and check for dangling references afterwards.
- **When the last step can only be run by the owner (a provider dashboard, a DNS panel), hand over a runnable guide, not a to-do.** Order and idempotence of the scripts; copy the live object definitions before any `create or replace` (the repo script can be older than what is deployed); a **functional** probe, not just a structural one; the automatic-activation path plus the log line that proves it fired; a one-line rollback; and proof that the security setting you recommend is a no-op for the app (count the clients and the anon-key references) instead of asserting it. Recipe: `references/provider-schema-apply.md`.
- **Merging a fix that touched internal documents: squash, never a merge commit.** A merge commit drags the intermediate commits — including the one that *added* the internal document — into the primary branch's history, where the content stays readable forever. A squash carries only the final tree. Verify afterwards that the document folder has zero entries on the primary branch.
- **Deleting a file is not un-publishing it.** If the document was already on the primary branch, its content stays in history. Say so plainly rather than implying exposure was reversed; the real remediation is fixing what the document describes.
- **Sweep your own public repos afterwards.** Neighbouring docs of the *reviewing* repo often name the removed file and even summarise its findings ("report — N critical, M high"). Same leak class, different repo.
- **An external platform's token may be barred from `.github/workflows/`** — GitHub refuses App tokens lacking the workflow permission, so the change they prepared stays stranded in their sandbox. Land it yourself with a token that has the `workflow` scope (check the scopes rather than asking them to retry).

## Reference

- `scripts/bait-bank-check.sh` — generate a bait tree of deliberately dangerous lines and assert the scanner still flags each expected label after a tuning pass (exit 1 on any silent pattern); takes `--expect <LABEL>` per pattern plus the scanner command
- `references/provider-schema-apply.md` — handing a pending provider-side schema/RPC apply to the owner: order, protecting live objects, structure + functional probes, rollback, RLS no-op proof, delivering long SQL across a chat interface without truncation, and the step format an owner already sitting in the dashboard can follow

## Exit Checklist

- [ ] Group counts reconcile with the tool's own total
- [ ] Every bucket has an explicit verdict (including "noise, no action")
- [ ] Findings you kept were reproduced by hand
- [ ] Checker bugs were fixed at the checker, not worked around in the data
- [ ] Report states how many findings are genuinely risky and lists ≤5 next actions
- [ ] An external fix was verified by commit file list + your own criteria commands, with CI step conclusions read (not just "green")
- [ ] Squash merge used whenever branch history carried internal documents; document folder verified empty on the primary branch
- [ ] Any owner-run step is attributed to the owner in the docs, and the reply separates "I verified" from "recorded from your report"
