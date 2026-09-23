# GitHub Token Probe Pattern

## Why this reference exists

Probe GitHub PAT tokens correctly. The most common failure: using `/orgs/<org>` as the first probe, getting 404, and concluding the token is invalid. It is not — it means the token lacks `read:org` or `repo` scope.

## Probe order (always follow this sequence)

1. **`/user`** — authenticates the token, returns login, id, public_repos
   - 401 = token invalid/expired
   - 200 = token valid, but may have limited scope
2. **`/repos/<owner>/<repo>`** — token can access specific repo
   - 404 = repo not found OR token lacks repo access
   - 200 = token has repo access
3. **`/orgs/<org>`** — only works if token has `read:org` scope
   - 404 = token lacks org scope, NOT token invalid

## Distinguishing failure modes

| HTTP | Body | Meaning | Action |
|------|------|---------|--------|
| 401 | "Bad credentials" | Token expired/invalid | Ask user to regenerate |
| 403 | "Resources do not belong to organization" | Token valid but no org access | Token works for user-level, needs org scope |
| 404 | "Not Found" | Insufficient scope for org endpoint | Token is VALID — probe `/user` to confirm |
| 200 | JSON with login | Token fully valid | ACTIVE |

## Key rule

**Never declare a GitHub token invalid based on `/orgs/<org>` 404.** Always verify via `/user` first. A 404 on org endpoints means the token works but lacks org-level scopes (common with fine-grained PATs that only grant specific repo access).

## Fine-grained PAT considerations

- Fine-grained PATs may only grant access to specific repositories, not the entire org
- `/user` endpoint always works if token is valid (it returns the authenticated user)
- `/repos/Niumination/<repo-name>` works if the PAT has access to that specific repo
- `/orgs/Niumination` returns 404 if PAT lacks `read:org` — this is EXPECTED for fine-grained tokens
- Verify token validity at `/user`, not `/orgs`

## Vercel env integration

When setting `GITHUB_TOKEN` in Vercel:
- Use `vercel env update GITHUB_TOKEN production --value <token> --yes`
- `--value` flag is REQUIRED (not optional) — without it, CLI returns `action_required` / `missing_value`
- Verify with `vercel env list production | grep GITHUB_TOKEN`
- Test after Vercel deploy restart, not just env update — Vercel caches env between deploys
