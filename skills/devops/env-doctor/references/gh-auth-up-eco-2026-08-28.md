# GH Auth + up-eco PR Check — 2026-08-28

## GH_TOKEN vs GITHUB_TOKEN
- Hermes stores token as `GITHUB_TOKEN` in `~/.hermes/.env` (classic PAT `ghp_...` with scopes `read:user,repo`).
- `gh auth status` expects `read:org` and warns `Missing required token scopes: 'read:org'` — **not fatal**.
- `gh` still works via `GH_TOKEN` env: `GH_TOKEN=$GITHUB_TOKEN gh auth status` shows `✓ Logged in (GH_TOKEN)` and `gh pr list` works.
- Fix persistence: ensure `~/.hermes/.env` has both lines:
  ```
  GITHUB_TOKEN=ghp_...
  GH_TOKEN=ghp_...
  ```
  and deduplicate if script appended duplicate. `up-eco` reads `GH_TOKEN` for `gh pr list`.

## gh pr list flag pitfall
- `up-eco.sh` tried `gh pr list --owner Niumination --state open` → `unknown flag: --owner` (gh 2.98.0).
- `gh pr list` has no `--owner`; it operates on current repo. For org-wide open PRs use API search:
  ```bash
  curl -s -H "Authorization: token $GITHUB_TOKEN" \
    "https://api.github.com/search/issues?q=org:Niumination+is:pr+is:open" \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['total_count']); ..."
  ```
  Found 3 open: `niu-mission-control#11` (APEX-MC orb), `ai-file-organizer-android#2`, `Niu-LKH#1`.

## Verification
```bash
GH_TOKEN=$(grep ^GITHUB_TOKEN ~/.hermes/.env | cut -d= -f2- | tr -d ' \r\n')
GH_TOKEN=$GITHUB_TOKEN gh auth status  # should show Logged in
GH_TOKEN=$GITHUB_TOKEN bash scripts/up-eco.sh | grep -E "PR|Pull Requests"
```

## stow + Rust follow-up (same session)
- `setup.sh` required `GITHUB_TOKEN` for dotfiles push fallback when SSH `Permission denied (publickey)`: `git remote set-url origin "https://oauth2:${GITHUB_TOKEN}@github.com/Niumination/zaryu-terminal-dotfiles.git"`.
- See `references/full-restore-2026-08-28-dotfiles.md` for Cargo guard, neovim shim, abbr function, and absolute symlink fixes applied same day.
