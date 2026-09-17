# Public-Repo Leak Audit (local evidence first)

Use when asked to "audit leaks" / "cek public leak" on a repo, especially an external-facing one.
Do this BEFORE querying provider alerts: the local repo proves what is committed, which branches
carry it, and whether a credential file ever existed — alerts only corroborate.

Mask every suspected value in output: show 6 chars + char count (`890329…[MASKED 46 chars]`).
Report `blob_sha` as the durable identifier — line numbers move on the next commit.

## 0. Confirm exposure and blast radius

```bash
gh repo view <owner>/<repo> --json visibility,isPrivate
for b in main dev gh-pages; do git ls-tree -r origin/$b --name-only | wc -l; done
git ls-tree -r origin/<branch> --name-only | grep -c "<suspect-file>"
```

A leak can be present on one branch and absent on others — say which, or the fix targets the wrong
place. Confirm the default branch first (`defaultBranchRef`).

## 1. Name sweep across ALL history (proves whether a credential file ever existed)

```bash
git rev-list --all --objects | grep -Ei "config\.json|\.env|\.db$|\.sqlite|\.pem$|id_rsa|\.key$|secret|token|credential|backup.*\.(tgz|tar\.gz|zip)"
```

Zero hits means no credential FILE was ever committed — a real, reportable clean result, and the
first thing to check before hunting content. Non-zero hits need the commit that touched each path
(`git log --all --oneline -1 -- <path>`).

## 2. Content sweep of tracked files (the actual leaks)

Iterate `git ls-files`, skip binary suffixes, and match with a pattern table; report file + hit
count + masked sample. Patterns worth carrying:

| Shape | Regex |
|---|---|
| Telegram bot token | `\b\d{8,12}:[A-Za-z0-9_\-]{30,}\b` |
| OpenAI/Anthropic-style | `\bsk-[A-Za-z0-9_\-]{20,}` |
| GitHub PAT | `\b(ghp_\|github_pat_\|gho_\|ghu_\|ghs_\|ghr_)[A-Za-z0-9_]{20,}` |
| AWS access key | `\bAKIA[0-9A-Z]{16}\b` |
| JWT | `\beyJ[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}` |
| Private key block | `-----BEGIN [A-Z ]*PRIVATE KEY-----` |
| Bearer | `[Bb]earer\s+[A-Za-z0-9._\-]{20,}` |
| secret-ish env assignment | `(?i)\b(API_KEY\|TOKEN\|SECRET\|PASSWORD)\s*[:=]\s*["']?[A-Za-z0-9_\-]{12,}` |

**Raw session/agent transcripts are a top leak vector.** A committed "full session log" is whatever
the operator pasted mid-session — usually credentials, chat IDs, hostnames — and it reads as
documentation, so nobody re-reads it. Grep transcripts first and treat them as high-risk.

False positives to classify, not fix: provider docs URLs containing `/docs/reference/...`, vendored
`.venv`/`.build`/`node_modules`, and a *sibling repo's own* same-named path.

## 2b. PII that is not a credential (names, NIK, personal-file inventories)

Credential sweeps miss the other half of the problem. Check three surfaces; the first is the one that
gets published by accident because nothing in the file body looks like a secret.

1. **Filenames inside a committed doc.** A cleanup or inventory document that enumerates personal files
   (`Ijazah d3.pdf`, `SK PNS 100-.pdf`, `<16-digit-NIK>-kartu-asn-virtual.png`) publishes a NIK in the
   filename while its body holds no digit at all. Before committing any doc that lists files or paths:

   ```bash
   git status --porcelain | grep '^??'        # untracked candidates first
   grep -nE '[0-9]{16}' <doc>                 # digits anywhere in the listing itself
   ```

   Add `\b\d{16}\b` (Indonesian NIK/KK) to the pattern table above, and context-triage every hit.
2. **Ops prose.** Fix-notes for data imports name the values they were fixing (`"a real NIK from the
   export"`, `"the user's test NIK had KK"`). That wording is proof the value is real, not a hint.
3. **Fixture vs real.** Security/redaction skill docs intentionally carry NIK-shaped strings as bad/good
   examples — leaving them is correct. Real IDs live in ops/import runbooks. Blanket-redacting fixtures
   destroys the example the doc exists to teach.
4. **Share IDs are not PII.** Instagram/Reel and share URLs map to 16-digit IDs; they match any
   16-digit pattern and are not personal data.

Remediation for a doc that merely *lists* personal files (no credential involved): do not commit it,
and do not rewrite history for it — add a path-specific `.gitignore` entry carrying the reason, then
prove the entry actually applies:

```bash
printf '%s\n' '# Dokumen pribadi (PII) — memuat NIK di nama file. Repo PUBLIC: jangan di-commit.' \
  'docs/reports/<PLAN>.md' >> .gitignore
git check-ignore -v docs/reports/<PLAN>.md          # must print the .gitignore line, not silence
git ls-files --error-unmatch docs/reports/<PLAN>.md # must fail == not tracked
git status --short                                  # back to clean
```

Prefer a path-specific entry over ignoring the whole directory — the directory itself is tracked and
active. The file stays on disk for the owner; ignoring it publishes nothing and costs no rewrite.

**An inventory is not an instruction.** A cleanup plan that enumerates the owner's personal files is
evidence, not a work order: never delete, move, or act on those files without explicit per-file
go-ahead, and do not "finish" the plan by executing it. Ask, then wait.

Proof of exposure without cloning — the smallest sufficient evidence, in order:

```bash
git ls-files --error-unmatch <path>                         # tracked at all?
git check-ignore -v <path>                                  # if not, why not
git cat-file -e origin/main:<path> && echo "ADA DI REMOTE (bocor)"
git log --diff-filter=A --format='%h %ci %s' -- <path> | tail -1
```

The first line is also the gate before executing any "commit the dirty files" recommendation: an
untracked doc has published nothing yet, so refusing it at that point costs nothing.

## 3. Submodule / archive exposure

A PUBLIC repo can point at a PRIVATE submodule (backups, media). Verify the submodule's own
visibility rather than assuming the pointer leaks its contents:

```bash
gh repo view <owner>/<submodule-repo> --json isPrivate
```

## 4. Embedded blobs — `.gitignore` does not protect blob content

Bootstrap/deploy scripts often embed a whole archive as a base64 heredoc
(`cat > x.tgz.b64 <<'B64EOF'`). Any gitignored file inside that archive (e.g. `config.json`)
IS committed, and no `.gitignore` pattern can stop it. Decode and inspect:

```python
b64 = re.sub(r"\s+", "", re.search(r"<<'B64EOF'\n(.*?)\nB64EOF", text, re.S).group(1))
tf = tarfile.open(fileobj=io.BytesIO(base64.b64decode(b64)), mode="r:gz")
# list entries, then dump config values MASKED and flag non-empty secret fields
```

Verdict shape: "config present in archive, values empty → safe today, latent risk on next rebuild".
Fix is at build time (exclude the config from the archive), not in git.

## 5. Corroborate with provider alerts (read-only)

`gh api repos/<owner>/<repo>/secret-scanning/alerts` → for each alert keep `state`, `secret_type`,
`validity`, `publicly_leaked`, `first_location_detected.blob_sha`. Fields that drive the response:

- `publicly_leaked: true` → assume compromised regardless of `validity: unknown`. Never send the
  value to the provider to "check if it still works" — that is using a leaked credential.
- `state: open` with the blob still present → redacting the file in a NEW commit does not clear it;
  the blob stays readable in history (this is why `blob_sha`, not the line number, is the handle).

Deeper API triage: `references/secret-alert-triage.md` and `references/github-secret-alert-triage.md`.

## 6. Remediation ladder (report as ordered options, do not auto-execute)

1. **Revoke/rotate at the provider** — the only step that actually neutralizes it, and it is the
   owner's action, not the agent's.
2. **Redact in HEAD** — exact-string replace with `[REDACTED-<TYPE>]`, one commit; clears the
   visible file but not history.
3. **History purge** (`git filter-repo`/BFG + force-push) — destructive, needs explicit owner
   approval; only material while the credential is still valid. State the cost before proposing it:
   every commit SHA changes, so any doc, submission form, or link that cites `commit <sha>` goes
   dangling. On a repo that is a judged/submitted artifact, prefer 1 + 2 and say why.

The ladder is ordered for a reason: revoking neutralizes the value, redacting clears the visible
file, rewriting only removes a now-worthless string from history.

After the redact commit, verify from the **public URL**, not the local file — the working tree being
clean is not evidence that the published copy changed:

```bash
curl -s https://raw.githubusercontent.com/<owner>/<repo>/<branch>/<path> -o /tmp/pub.md
python3 - <<'PY'   # count hits + markers; never print the value
import re; t=open('/tmp/pub.md',encoding='utf-8',errors='ignore').read()
print('hits', len(re.findall(r'\b\d{8,12}:[A-Za-z0-9_-]{30,}\b', t)), 'markers', t.count('[REDACTED-'))
PY
```

Report: hits `0`, marker count equal to what you replaced, gate run green. Alerts stay `open` (they
point at the old blob) — expected, not a failed fix; they close when the owner revokes, with the
resolution recorded against the real reason. Also add a short redaction notice at the top of the
affected transcript/note — what was removed and why — so a future reader (or a later audit) does not
re-flag it as a fresh leak.

Prevention gate belongs in the repo, not in a local hook: a `scripts/secret_scan.py` (pattern table
from §2, `SELF` skip so it never flags its own patterns, mask all output) plus a CI workflow running
it on `push` and `pull_request`. On a public repo a local-only hook protects nobody.

Always pair with a prevention note: keep raw transcripts and embedded archives out of public repos
(private submodule), and add a secret scan to pre-commit/CI — committed, not local-only, so it
covers every contributor.
