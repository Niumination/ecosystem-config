# Auditing changes you did not make

Autonomous jobs (cron, watcher scripts, sync daemons) edit tracked files on
their own schedule. Those edits land in `git status` as "uncommitted changes"
and carry no commit message, so they look exactly like work a human or agent
just did. Auditing them is a different task from auditing your own work: the
author cannot be asked what it meant, so every claim has to be re-derived.

## The default failure is trusting the edit and re-committing it

The edits read as plausible because they *are* plausible — they were written
against the same machine. The failure mode is committing a claim that was never
probed, into the bank, where the next session reads it as verified fact.

Rule: **split automated edits into "verified true", "verified false", and
"not testable" before touching git.** Committing a file whose claims you
merely re-read is laundering an unverified claim into a source of truth.

## Test every concrete claim, not the file's overall tone

Factual assertions are individually checkable. A file can be 80% right and
still contain one claim that will mislead the next reader for months. Pull out
each checkable assertion and probe it:

- a count → query the live source, not the file that states the count
- a model / endpoint / service name → does it exist in the live listing?
- a state claim ("healthy", "running", "requires auth") → curl it, check the
  process table, check launchd
- a behavioural claim ("needs a header", "routes through X") → issue the
  request both with and without the thing, and diff

Report the split explicitly — verified-correct, verified-wrong, unverifiable —
so the owner can judge the file rather than take your word for it.

## Never paraphrase a failure cause you did not reproduce

A log line naming a subsystem is not a diagnosis. Reproduce the failing path
yourself and read the real error. Common divergence: the log blames a
permission or auth layer while the actual exit code points at a shell parse
error in an input file several steps earlier. Trace the exit code back to the
line that produced it.

## Run the changed program before trusting the change

A code edit is a claim about behaviour. Execute the edited entry point and
compare its real output against the numbers the edit asserts. In one case an
edited probe script was still reporting the pre-edit count and labelling —
which meant the edit had never been run at all, and several of its new claims
were unexercised code.

## Fix the root cause the edit introduced, not just the text

When a machine-generated edit is wrong, the wrongness usually has a cause in
the code or config that produced it. An edit that routes a provider through the
wrong endpoint is a symptom; the cause is that the code looked for a credential
in a file that never contained it. Fixing only the prose leaves tomorrow's run
to regenerate the same error.

## Dynamic sources are not stable enough to transcribe

Live catalogues, quotas, and endpoint listings change between runs, sometimes
within an hour. When you must record such a number, record three things: the
value, the timestamp, and an explicit warning that it is a snapshot. If you
observe the same source reporting different values in one session, that
volatility is itself the finding — say so instead of picking one number.

## Names are not derivable from family or vendor

Do not infer that a model, package, or service exists because a sibling with a
similar name exists. A model's namespace prefix, a service's port, and a
provider's credential location are independent facts; each needs its own
lookup. Transcribed lists are where this goes wrong — check each name against
the live listing individually and drop the ones that are not there.
