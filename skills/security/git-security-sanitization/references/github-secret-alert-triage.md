# Triaging GitHub Secret-Scanning Alerts Without a Clone

Use when a repo has secret-scanning alerts but cloning is impractical
(huge repo, or the suspect files may already be gone from HEAD).
All steps are read-only; never download or print a suspected secret value.

## 1. List alerts (metadata only)

`GET /repos/{owner}/{repo}/secret-scanning/alerts?per_page=100`
→ `number`, `secret_type`, `state`, `created_at`, `locations_url`.

## 2. Classify by location, not by type

`GET .../alerts/{n}/locations?per_page=20` → `details.path` per alert.
Group `(secret_type, state, path-prefix)`. In one real audit of 35 alerts
the split was total:

- 33 × `google_api_key` / `google_oauth_access_token` → all under
  `.config/chromium/...` (History, IndexedDB `*.ldb`/`*.log`, CacheStorage,
  `ukm_db`). Cached web pages contain `AIza...`-shaped strings; these are
  junk-blob false positives, not committed credentials.
- 1 × `openai_api_key` (open) → `.config/Code - OSS/User/History/*/KSY0.js`
  (editor backup file) — true positive.
- 1 × `openai_api_key` (resolved) → chromium blob, already self-resolved.

Lesson: alert counts mean nothing until grouped by path prefix.

## 3. HEAD-existence check (no content download)

`GET /repos/{owner}/{repo}/contents/{path}` per distinct path:
`HIT` + `size`/`sha` = still live; `404` = already removed from HEAD
(alert stays `open` until dismissed even when the blob is gone).
Suspect directories can be listed the same way (`chromium/` → 404,
backup dir → 2 files). Never `GET` the blob of a live suspected secret.

## 4. Verdict mapping

- Stale cache/blob alerts, path gone from HEAD → dismiss as
  `false_positive` after cleanup (no rotation needed).
- Live credential file at HEAD (editor history, shell history, dumps) →
  true positive: revoke/rotate FIRST, then delete the file, then dismiss
  as `revoked`.
- Missing `.gitignore` over a home-dir dump (no ignore file at all) is
  the root cause to fix: block `chromium/`, `Code*/User/History/`,
  `History`, `*.ldb`, `*.log`, cache dirs.

## 5. Cleanup without cloning

Small deletions and `.gitignore` can be done via the Contents API
(no 1.6 GB clone for a 183-byte file). Skip history purge when the key
is revoked — copies in history become useless. History rewrite needs a
full clone and is only worth it for still-valid secrets.
