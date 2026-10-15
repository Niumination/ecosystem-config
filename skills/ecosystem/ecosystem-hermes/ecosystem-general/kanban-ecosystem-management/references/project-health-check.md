# Project Health Check Reference

A standard checklist for inspecting a Niumination project's health — git status, deployment, and package integrity.

Use this when the user asks "cek status [project]" or before making changes to any project.

## Checklist

```bash
# ── 1. Git Status ──
cd ~/Desktop/Niumination/<ProjectName>

git log --oneline -5           # Recent commits + HEAD
git remote -v                  # Remotes (origin should point to Niumination/...)
git branch -a                  # Local + remote branches
git status --short             # Dirty state (empty = clean)

# ── 2. GitHub Remote ──
# Via MCP GitHub tools:
# mcp_github_list_commits(owner="Niumination", repo="<ProjectName>", perPage=5)

# ── 3. Live Deployment ──
# For GH Pages:
curl -s -o /dev/null -w "HTTP %{http_code} — %{time_total}s\n" https://niumination.github.io/<RepoName>/

# For Vercel:
curl -s -o /dev/null -w "HTTP %{http_code} — %{time_total}s\n" https://<project>.vercel.app/

# ── 4. Package Metadata ──
node -e "const p=require('./package.json'); console.log('Name:', p.name); console.log('Version:', p.version); console.log('Deps:', Object.keys(p.dependencies||{}).join(', ')); console.log('Scripts:', JSON.stringify(p.scripts))"

# ── 5. Project Structure (quick view) ──
ls -la
```

## Expected Healthy State

| Check | Healthy Signal |
|-------|----------------|
| Git status | `git status --short` empty (clean working tree) |
| Recent push | Last commit ≤ 7 days for active projects |
| Remote | `origin → github.com:Niumination/...` |
| Live URL | HTTP 200, under 2s response |
| package.json | Has `name`, `version`, scripts that work (`build`, `dev`) |
| node_modules | Present for dev, but CI will `npm install` on build |

## Reporting Format

Present results in a table:

| Aspek | Status |
|-------|--------|
| **Versi** | vX.Y.Z |
| **Live** | 🟢 HTTP 200 (Xs) |
| **Stack** | React X, Vite X, etc. |
| **HEAD** | `abcd123` — Date |
| **Git status** | ✅ Clean / ⚠️ N dirty files |
| **CI/CD** | ✅ Auto-deploy / ⚪ Manual |

## Common Issues & Signals

| Symptom | Likely Meaning |
|---------|----------------|
| `gh-pages` branch exists + CI workflow | Project uses GH Pages auto-deploy |
| `main` + `gh-pages` branches both present | Standard GH Pages dual-branch pattern |
| `git status` shows untracked files | Forgot to add/commit before previous session ended |
| Stale last commit (months ago) | Project is inactive / P3 monitoring |
| No `dist/` or `build/` | May need `npm run build` first, or CI handles it |
