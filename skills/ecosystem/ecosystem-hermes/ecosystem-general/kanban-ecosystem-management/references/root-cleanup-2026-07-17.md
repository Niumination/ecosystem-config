# Root Ecosystem Cleanup — 17 Jul 2026

**Trigger:** User asked: (1) hapus TEDEO dari lokal + tandai mature di GitHub, (2) rapikan root Desktop/Niumination — pisahkan proyek aktif/dormant, catat semua isi, archive file usang.

## Structure Changes

### Before
```
Desktop/Niumination/
├── Production/       🏭
├── projects/         🔧 ~27 dir — active + dormant + TEDEO bercampur
├── brain/            🧠
├── Root files:       MASTERPLAN.md, REKAP-NIU-DASH.md, AGENTS.md.bak, dll
├── Niu-Flow/         root-level (duplikat dari projects/)
├── projects/niu-dash/  duplikat dari Production/niu-dash/
```

### After
```
Desktop/Niumination/
├── Production/       🏭 11 deployed
├── projects/         🔧 16 active
├── incubator/        💤 9 dormant (terax-ai, niu-studio, aistudio-google, niude, dll)
├── archive/          📦 Consolidated: Belum disentuh, backup, labs, media-lib, skills-main, 
│                       terax-ai-analysis, xero-dotfiles-docs, jcode-docs, ocmux
├── brain/            🧠 Obsidian vault
├── docs/ / dox/ / scripts/ / tools/ / rekap/
├── characters/ / .vscode/
├── .gitignore, AGENTS.md, BACKLOG.md, .gitleaks.toml  (tracked in root git repo)
```

## TEDEO Handling

1. `gh repo edit Niumination/TEDEO --description "MATURE — Delivery Service. Butuh VPS untuk production deployment." --add-topic mature --add-topic production-ready`
2. `gh issue create --repo Niumination/TEDEO --title "PRIORITAS: butuh VPS untuk production" --label priority`
3. `rm -rf projects/TEDEO/` — removed locally
4. Local GitHub fork (`https://github.com/zaryuv2/TEDEO`) verified, working remote

## Git Repo Created

`github.com/Niumination/ecosystem-config` (private) — tracks the root ecosystem files:

- Commits: `init` → `fix: add .gitignore, remove secrets/PI/.DS_Store` → `fix: gitignore archive dirs with binary files, track only .md docs`
- PI/ was accidentally committed in init commit; removed in second commit via `git rm -r --cached`
- Archive binary dirs (Belum disentuh/, backup/, labs/, media-lib/, skills-main/, jcode-docs/) removed from tracking
- Final tracked count: 148 files (mostly .md + submodule references)
- `.gitignore` now excludes: .DS_Store, PI/, node_modules, .env, *.zip, archive binary dirs, etc.

## Duplicates Removed

- `projects/niu-dash/` — canonical at `Production/niu-dash/`
- `Niu-Flow/` root directory — was a copy of projects/ structure, archived
- `projects/TEDEO/` — deleted (mature on GitHub only)

## Key Insights

1. **Git security**: Always write `.gitignore` BEFORE first `git add` when a directory contains PI/ or credentials
2. **Archive strategy**: Zips and binary dirs in archive/ should be git-ignored, only .md tracked
3. **`gh repo create --private --push --source=.`** — quick way to push a local dir to GitHub with no manual remote setup
4. **Submodule behavior**: A root git repo containing subdirs with their own `.git/` tracks them as gitlinks; `git status` shows `m <path>` (modified submodule) — expected, not an error
5. **eco-collect.py** needs explicit scan scope for `incubator/` and `Production/` — it doesn't auto-discover them
