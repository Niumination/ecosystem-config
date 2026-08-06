# Org-Wide GitHub PR Detection (single query) — for status-check scripts

Verified 6 Agu 2026 in `up-eco.sh` Phase 5b (Niumination ecosystem).

## The pattern

One `gh search prs --owner <org>` call finds ALL open PRs across every repo in an org —
beats looping per-repo (which requires knowing the repo list and makes N API calls).

```bash
gh search prs --owner <org> --state open --limit 50 \
  --json number,title,repository,isDraft,author,createdAt,updatedAt
```

- `--owner <org>` scans every repo in the org; `repository` in the JSON returns `nameWithOwner` per PR.
- **Valid `--json` fields for `gh search prs` DIFFER from `gh pr list`** — `headRefName` is NOT
  accepted (error: `Unknown JSON field: "headRefName"`). Available fields:
  `number, title, repository, isDraft, author, createdAt, updatedAt, url, labels, state,
  assignees, body, commentsCount, isLocked, authorAssociation, closedAt`.
- `--limit 50` caps results (org-wide scans can be large); sort by `updatedAt` client-side for
  oldest-first triage.

## Report enrichment

- Flag **DRAFT** PRs (need finalization before review).
- Flag **STALE** PRs: `updatedAt` older than 14 days → recommend review/close/branch-update.
- Always emit the PR URL: `https://github.com/{nameWithOwner}/pull/{number}`.
- Recommendations go into the same numbered list as the rest of the audit.

## Hermes-env HOME quirk (critical)

Under the Hermes portable agent, `$HOME` points at a cache path
(`/Volumes/HermesAgent/.cache/unix-home`), so `gh auth status` FAILS even though the user IS
logged in at the real home (`/Users/<user>/.config/gh/hosts.yml` exists, keyring auth works).
Result: auth check falsely reports "not logged in" and the scan silently skips.

**Fix — resolve the real home, then run gh with it:**

```bash
local gh_home="$HOME"
if [ ! -d "$gh_home/.config/gh" ] && [ -d "/Users/${USER:-zaryu}/.config/gh" ]; then
  gh_home="/Users/${USER:-zaryu}"
fi

if ! command -v gh &>/dev/null; then
  echo "gh CLI not installed — skipping PR check" >&2
  return
fi
if ! HOME="$gh_home" timeout 8 gh auth status &>/dev/null; then
  echo "gh not authenticated — skipping PR check" >&2
  return
fi

prs_json=$(HOME="$gh_home" timeout 20 gh search prs --owner <org> --state open --limit 50 \
  --json number,title,repository,isDraft,author,createdAt,updatedAt 2>/dev/null || echo "[]")
```

Parse with `python3 -c "import sys,json; print(len(json.load(sys.stdin)))"` for the count,
then render details (author login, age in days, draft/stale flags).

## Related

- `macos-daemon-lifecycle` — launchd-vs-Hermes-cron-vs-crontab scheduler layers (the PR scan is
  one phase of a full scheduler/ecosystem audit; see the four-layer inventory in
  plan-compliance-audit SKILL.md).
