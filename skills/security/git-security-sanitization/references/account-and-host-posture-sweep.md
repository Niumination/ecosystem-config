# Account & Host Posture Sweep

Use when an incident points at ONE credential but the owner asks "audit everything" — the named
incident is the trigger, not the scope. Sweep three surfaces in this order: the code-hosting account,
every local repo, then the machine itself. Report severity-ordered findings and fix one item at a time
with per-item approval.

Masked output throughout: 6 chars + length, or a computed label. Never a value.

## 1. Code-hosting account

```bash
gh api user --jq '"2FA: \(.two_factor_authentication) | \(.public_repos) pub / \(.total_private_repos) priv"'
gh api user/keys --jq '.[] | "\(.id)  \(.title)  \(.created_at)"'
gh api user/installations --jq '.installations[] | "\(.app_slug) \(.repository_selection)"'
```

Then iterate EVERY repo for the trust entries an intrusion adds. Print a summary count as well as hits —
"no deploy keys, no webhooks, no added collaborator across N repos" is a reportable clean result:

```bash
for r in $(gh repo list <owner> --limit 200 --json name --jq '.[].name'); do
  gh api repos/<owner>/$r/keys          --jq ".[] | \"deploy-key $r \(.title) read_only=\(.read_only)\""
  gh api repos/<owner>/$r/hooks         --jq ".[] | \"webhook    $r \(.config.url) active=\(.active)\""
  gh api repos/<owner>/$r/collaborators --jq ".[] | select(.login!=\"<owner>\") | \"collab $r \(.login)\""
done
```

Foreign pushes: `gh api users/<owner>/events?per_page=100` covers 90 days of PUBLIC repos only. A push you
cannot attribute is the signal; absence is weak evidence, never proof.

**Per-repo scanning / push-protection status must come from a single-repo GET.** The list endpoints
(`user/repos`, `gh repo list --json`) do not return `security_and_analysis`, so counting "scanning
disabled" from a list reports *disabled everywhere* — a fabricated finding that reads as a systemic
crisis. Query each repo:

```bash
gh api repos/<owner>/<name> --jq '.security_and_analysis.secret_scanning.status'
```

A repo whose alert endpoint answers `404 Secret scanning is disabled` is genuinely unguarded; one that
returns an empty array is guarded and clean. Those are different results.

Not answerable by API — hand to the owner as manual checks: personal access tokens (settings/tokens),
authorized OAuth apps and GitHub Apps (settings/applications), and provider-dashboard 2FA + active
sessions (database, model, deploy, DNS accounts).

## 2. Every local repo

Sweep all of them, not the one in the incident. A tracked REAL `.env` (as opposed to `.example`) in a
private repo is a credential bundle waiting for one leaked account key — the two findings compound.

Enumerate by `.git` discovery, then **assert each candidate's identity before scanning it**:

```bash
for d in $(find <root> -maxdepth 3 -name .git -type d); do
  repo=${d%/.git}
  [ "$(git -C "$repo" rev-parse --show-toplevel)" = "$repo" ] || continue   # else it is the umbrella
  printf '%s  %s\n' "$repo" "$(git -C "$repo" remote get-url origin 2>/dev/null)"
done
```

A folder that only *looks* like the target repo — right name, nested inside an umbrella repo, no
`.git` of its own — sends `git -C` up to the umbrella, and the sweep returns a confident `0 findings`
for a repo that was never opened. Match the printed remote against the slug you mean; when a repo has
no local checkout, clone the remote into `/tmp` and scan that rather than scanning a path that
resolves elsewhere.

- tracked sensitive names: `git ls-files | grep -Ei '(^|/)(\.env($|\.)|.*\.(pem|key|p12|jks)$|credentials|secret|id_rsa|id_ed25519)'`
- real vs example: an `.example` carrying filled values is still a finding; classify every value as
  PLACEHOLDER / URL (with-credentials yes-no) / length-N before calling it real
- history names: `git rev-list --all --objects | grep -Ei '<same names>'` — finds files deleted from HEAD
- content: `git grep -I -l -E '<pattern table>' HEAD` (index-backed; a filesystem-wide `grep -r` across
  the ecosystem can exceed the command timeout and return nothing useful)
- gate activation: `git config --get core.hooksPath` + the hook file existing, per repo. Report the
  COUNT of repos lacking it, not a 57-line list.

## 3. The machine

```bash
fdesetup status
/usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate
lsof -nP -iTCP -sTCP:LISTEN | grep '\*:'        # all-interfaces bind: verify reachability + auth before reporting
stat -f '%Lp %N' ~/.ssh/config ~/.ssh/id_* ~/.npmrc ~/.hermes/.env ~/.git-credentials
ssh-add -l ; git config --global --get credential.helper
for p in sshd vnc smbd ARDAgent; do pgrep -x $p; done   # macOS sharing services
```

- `osxkeychain` as the git credential helper is the good state; `store` writes `~/.git-credentials` in
  plaintext.
- **A symlink's mode is not the file's mode.** `ls -l` prints `lrwxr-xr-x` for every symlink regardless of
  what it points at, so a dotfile symlinked into a dotfiles repo reads as `755` while the real file is
  `600`. Resolve before reporting: `[ -L <path> ] && readlink <path>` then `stat -f '%Lp' "$(readlink <path>)"`.
- **Bound to `*:<port>` is a suspicion, not an exposure.** Prove both reachability and authorization
  before writing it up: request the service from the machine's LAN IP
  (`IP=$(ipconfig getifaddr en0); curl -s -o /dev/null -w '%{http_code}' --max-time 6 http://$IP:<port>/`)
  and read the service's auth path (`lib/auth.js`-style middleware, and whether the running process actually
  has its API key set — `ps eww -p <pid>`). A framework that rejects non-loopback requests without a key,
  on a process that has one, means the all-interfaces bind is intentional deployment support and the port is
  not exposed — report that as a corrected assessment rather than as a finding.
- A dev box usually exposes more than the repo does: `127.0.0.1:<port>` is fine, `*:<port>` needs the check
  above. Name the process holding it.
- Private keys should be `600`; `config`, `.npmrc`, and token files should not be group/world-readable. A
  secret file inside a `700` directory is protected in practice — say so rather than reporting bare
  `o+r` bits as an exposure.
- A token typed on a command line lives in the shell history file too; scan history for token shapes and
  report counts.

## 4. Report shape

- Order by blast radius, not discovery order: admin/`service_role` DB keys and code-hosting write
  credentials first, then billing keys, then host posture, then hygiene.
- Every finding carries the command that produced it and the observed result.
- Correct your own earlier claims in the report when a later check contradicts them; a self-corrected
  false positive is far cheaper than an owner acting on a fabricated severity.
- Keep the report out of any public repo, pattern-scan it for credential values before delivering, and
  list what the audit could NOT cover (API-invisible tokens, provider dashboards, other devices, the
  dead VPS/provider account).
- Deleting a trust entry (`gh api -X DELETE user/keys/<id>`) is destructive and needs explicit approval;
  report the command for the owner rather than running it unprompted.
- **Record the owner's accepted risks once, and stop re-raising them.** When the owner states a posture
  finding is accepted for now ("the machine is fully under my control"), write it into the report as
  *accepted by owner — deferred*, with the residual risk in one clause (unencrypted disk contents if the
  device is lost), and carry that status forward instead of re-listing it in the next sweep. Silently
  dropping it is also wrong: an accepted finding is deferred, not remediated, and it becomes live again the
  moment the device or its context changes.

## See also

- `references/public-repo-leak-audit.md` — per-repo leak audit, blob recovery, remediation ladder
- `references/leaked-credential-blast-radius.md` — what each credential class actually reaches
- `scripts/alert_inventory.py` — account-wide open-alert inventory before triaging any single hit
