# Incoming Contribution Review (external coding agent)

Use when work arrives as a PR — typically hundreds of files from an external
coding agent (Arena / Copilot / Codex-style) with a confident body and green CI. The deliverable is a
verified review, not a merge.

## 1. Enumerate before reading

`gh pr diff` returns an EMPTY body on very large diffs — that is "cannot render", not "no changes".
Enumerate through the files API, paginated, and look at distribution first:

```bash
R=owner/repo; N=5
gh pr view $N --repo $R --json title,isDraft,mergeable,mergeStateStatus,changedFiles,additions,deletions,reviews,comments
gh pr checks $N --repo $R
gh api "repos/$R" --jq '"visibility=\(.visibility) forks=\(.forks_count)"'      # public ⇒ docs in the PR are published

gh api "repos/$R/pulls/$N/files?per_page=100" --paginate \
  --jq '.[] | "\(.status)\t\(.filename)\t+\(.additions)\t-\(.deletions)"' > /tmp/pr-files.txt
cut -f1 /tmp/pr-files.txt | sort | uniq -c                                          # added / modified / removed
cut -f2 /tmp/pr-files.txt | awk -F/ '{print $1}' | sort | uniq -c | sort -rn | head
```

One directory holding most of the files is usually vendored material (a bundled skill set, fixtures):
separate it from the code that ships and review only the latter in detail.

## 2. Verify on the PR's own commit, without touching the working tree

```bash
cd <local-clone>
git fetch -q origin <pr-branch>                    # FETCH_HEAD == PR tip
git rev-parse --short FETCH_HEAD                   # compare against origin/<base>
git show FETCH_HEAD:<path>                         # full content of a new/changed file
git diff origin/<base> FETCH_HEAD -- <path>        # one file's patch
git grep -n <pattern> FETCH_HEAD -- <dirs>         # search the PR's content, not the checkout
```

## 3. Claim → proof table

| Claim in the PR body | What actually proves it |
|---|---|
| CSP tightened (`connect-src 'self'`) | grep the CLIENT tree for the provider: `git grep -il '<provider>' FETCH_HEAD -- pages components` — zero hits (server-side only) = safe; any client call = broken at runtime, and the build will not tell you |
| "atomic rate limit" / new RPC | a `CREATE FUNCTION` present only in the diff means it is NOT applied in the database; read the fallback chain in code and report which layer is live |
| constant-time auth compare | read the function: equal lengths then `timingSafeEqual`, plus a dummy same-length compare on the mismatch branch |
| "XSS/SSRF closed" | the proxy/handler needs a positive allowlist (exact host prefix, content-type whitelist); a bare `fetch(userUrl)` or a denylist is a finding |
| "dead code removed" | anchored import grep (`^import .*<Name>`), never substrings — `Modal` matches `DetailModal` and makes a clean removal look like a broken build; the compile is the real proof |
| "no design change" | diff the theme variables before alleging a redesign: self-hosting an existing font looks like a font swap at a glance |

## 4. Added lines — credential scan

```bash
git diff origin/<base> FETCH_HEAD -- . ':(exclude)<vendored-dir>' \
  | grep -E '^\+' | grep -v '^\+\+\+' \
  | grep -nE 'sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{20,}|AIza[A-Za-z0-9_-]{30,}|eyJ[A-Za-z0-9_-]{20,}\.|BEGIN [A-Z ]*PRIVATE KEY' | head
```

A hit that is a variable NAME inside prose (an env-var table in a doc) is not a value — measure before
reporting, and never paste matched text into the report. New files in the diff show as `+` lines, so a
single scan of the diff covers them too.

## 5. Metadata files — small diffs, expensive mistakes

- **`.gitignore`** — inspect the branch's own blob (`git show FETCH_HEAD:.gitignore`), then test the paths
  that exist on disk: a rule replaced by a typo'd path (`data/*.bak-*` → `.data/*.bak-*`) un-ignores real
  backups, and the next `git add -A` sweeps them in.
- **`.github/workflows/*`** — a new or changed workflow runs arbitrary code with the repo's secrets; treat
  it as the highest-severity file in the PR.
- **`package.json` / lockfile** — a new dependency is a supply-chain decision; added `engines`/`scripts`
  entries are not.
- **Removed assets** — `git grep -F '<asset>' FETCH_HEAD -- <src dirs> public` before agreeing that a
  deleted image/file is unreferenced.

## 6. Discipline that prevents wrong findings

- **The source of a rule is not the rule.** Before reporting "document X contradicts reality" — e.g. a
  SOUL/AGENTS claim about which directory is authoritative — grep that document for the phrase itself.
  Handoff summaries, compaction notes, memory entries and transcript quotes are not sources. A
  contradiction reported from a summary ends in a visible self-correction and makes the rest of the
  review suspect.
- **A counting method is part of the claim.** A glob such as `*/*/SKILL.md` only sees entries at one
  depth; the authoritative list is the manifest or the tool's own output. Compare *named* lists, state
  which method produced the number, and never announce "drift" from a gap that is an artifact of two
  different enumerations.
- **Vendored third-party content is legitimate when it is pinned.** A bundled skill or asset set is
  acceptable if a lockfile records `source` plus a hash per entry and the upstream licence ships
  alongside; without those, raise it as a condition rather than ignoring it. Do not ask for vendored
  sets to be moved into a central skill bank — project-level vendoring is an accepted pattern, and
  relocating them breaks the workflow that produced them.
- **Publication is a separate decision from correctness.** A PR adding audit/report documents to a
  public repo needs its own check: are the findings closed in this same PR, or does the document list
  open items (unapplied SQL/RPC, claimed-but-missing CAPTCHA, shared admin password, history not
  cleaned)? Does it disclose internals that aid probing (table/view/RPC names, env-var names, provider
  outage history)? Does it carry statements sensitive for the owner rather than for security
  (institutional claims, external evaluation results)? Recommend audit reports stay local and only the
  outcome ships — the owner decides.

## 7. Report shape

Verdict first (merge-ready / needs N fixes / needs an owner decision), then the verification actually
performed, then the open decisions — with "what I proved" separated from "what the PR claims" and from
"what the owner must apply". Do not merge, approve, comment, or push unless asked: on a CI/Vercel-backed
repo a merge is a production deploy. State the next-step options and wait.
