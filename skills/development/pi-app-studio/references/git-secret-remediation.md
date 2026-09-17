# Git-Committed Secret Remediation

## Trigger

When a secret (API key, private key, credential file) gets committed to a git repo.

## Severity Assessment

| Scenario | Risk | Action |
|----------|------|--------|
| Committed + pushed to public repo | **CRITICAL** | Rotate IMMEDIATELY, history rewrite needed |
| Committed + pushed to private repo | **HIGH** | Rotate, consider history rewrite |
| Committed locally, not pushed | **MEDIUM** | Remove from tracking, rotate if unsure |

## Immediate Remediation

### Step 1: Remove from Tracking

```bash
git rm --cached path/to/secret-file
echo "path/to/secret-file" >> .gitignore
git commit -m "chore: remove secret file from tracking"
git push
```

### Step 2: Verify Clean State

```bash
git status
git check-ignore -v path/to/secret-file
git log --oneline -- path/to/secret-file
```

### Step 3: Rotate the Secret

For Pi Network apps:
1. Open Pi Browser → Developer Portal
2. Open app settings → API Key → Regenerate
3. Update vault with new key
4. Update `.env` in local dev environment
5. Update production server env var

## History Rewrite (Private Repos Only)

```bash
# Install git-filter-repo
git filter-repo --force
git filter-repo --path path/to/secret-file --invert-paths
git push origin --force --all
```

## Prevention

- `.gitignore` includes `.env`, `*_key.txt`, `credentials*`, `secrets*`
- Pre-commit hooks with `detect-private-key`
- Always `git status` before `git add -A`
- Store secrets in `~/Desktop/Niumination/vault/`, never in repo folders

## Pi Network Key Storage

| Item | Storage |
|------|--------|
| Server API Key | Vault + server env var |
| Wallet Private Key | Vault only |
| Wallet Address | Can be public |
