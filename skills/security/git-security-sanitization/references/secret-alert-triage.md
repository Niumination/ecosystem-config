# Secret-Alert Triage via API (stale vs live)

Read-only classification of secret-scanning alerts. Run BEFORE any delete, dismiss, or rotation.

## 1. Scope check

```bash
git remote -v   # local truth: which repo is actually checked out here?
```

Compare against the API repo `full_name`. Same display name ≠ same repo. Out-of-scope findings:
report only, never act.

## 2. List alerts (metadata only)

`GET /repos/{owner}/{repo}/secret-scanning/alerts?per_page=100` → keep
`(number, secret_type, state, locations_url)`. Never print secret values.

## 3. Locations per alert → group by path prefix

`GET .../alerts/{n}/locations?per_page=20` → `details.path`. Bucket by top-level dir.
A clean split (e.g. 33/35 in one cache dir, 1 elsewhere) tells you stale-vs-live immediately.

## 4. HEAD-existence check (metadata only)

`GET /repos/{owner}/{repo}/contents/{path}` → HIT gives `size` + `sha`; MISS gives 404.
Do NOT fetch the blob content of a suspected live secret — size/sha is enough to confirm it exists.

## 5. Classify and act

| Class | Condition | Action |
|---|---|---|
| Live true positive | Path HIT at HEAD | Rotate/revoke credential first, then delete file |
| Stale blob | Path 404, dir gone at HEAD | Dismiss as `false_positive` |
| Cache-data pattern | `google_api_key`/`oauth_token` inside committed browser profile (`chromium/... History, IndexedDB, CacheStorage`) | Stale class; the strings are cached web pages, not committed credentials |

## 6. Non-finding after sweep

If no live file and no ssh/private alert across all repos, but a key was flagged as leaked:
the source was likely removed/rewritten before the sweep. Revocation + local deletion still
fully neutralizes the key — do not block cleanup on finding the original file.
