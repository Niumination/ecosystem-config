---
name: ekosistem-scaffold
description: "Scaffold new or missing projects in the Niumination ecosystem. Creates AGENTS.md + BACKLOG.md + brain/projects/ entry with standardized templates. Validates git, deploy, and DOX completeness."
tags: [scaffold, ecosystem, project-setup, templates, niumination]
---

# Ekosistem Scaffold

## ⚡ Bot Utama Pattern — PAKAI INI DI SEMUA INTERAKSI

User pattern: **perintah→kerjakan→lapor→selesai**

- **Jangan tambah kerjaan** yang tidak diminta. Kalau user minta A, kerjakan A saja — jangan lancar ke B/C/D "biar lengkap".
- **Jangan aktifkan hal yang tidak diminta.** Kalau user bilang "abaikan" atau "tidak perlu", stop segera. Jangan bikin file/script/cron yang belum diizinkan.
- **Jangan over-explain.** Data → opsi → pilih → eksekusi. Bukan essay.
- **Verifikasi dulu sebelum klaim.** Cek actual state pakai tool. Kalau gak tau timing/kronologi, akui "belum dicek" — jangan bikin alasan palsu.
- **Kalau dikoreksi:** akui langsung, stop alasan, JANGAN pernah bikin penjelasan palsu untuk menutupi kesalahan.
- **Format laporan:** bullet list atau key: value. Jangan analysis paralysis.
- **Jika user ingin sesuatu yang butuh sudo/password:** berikan perintah yang HARUS dijalankan user sendiri di terminal, jangan coba jalankan via Hermes jika ada hard block.

Scaffold a new project into the Niumination ecosystem — or fill in a project that's missing its DOX.

## When to Use

- A new project directory appeared in `~/Desktop/Niumination/` without AGENTS.md/BACKLOG.md
- A sub-agent or cron added a new project that needs ecosystem registration
- The user says "setup DOX for [project]"
- A project exists but doesn't show up in the ecosystem catalog
- The user wants a cron-based watcher for new folders in `projects/` or `incubator/` → see `references/project-folder-watcher.md`

## Workflow

### Step 0: Incoming External Archive (zip/tar)

When the user provides an external archive to be added as a new project — either via upload or found in `Belum disentuh/`:

1. **Locate & inspect:**
   ```bash
   # Check if in Belum disentuh (common Niumination source)
   ls ~/Desktop/Niumination/Belum\ disentuh/<archive-name>.zip 2>/dev/null
   
   # Preview contents
   unzip -l /path/to/file.zip
   ```

2. **Extract & clean extraction artifacts:**
   ```bash
   unzip -o /path/to/file.zip -d /tmp/<project-name>/
   ```
   
   **Watch for these common extraction artifacts and remove them:**
   - `home/user/<project>/` — duplicate path from the original dev's home dir. Compare with the real project root; if identical, delete the `home/` branch.
   - `.config/`, `.local/` — node.js tooling configs and caches (create-next-app-nodejs, nextjs-nodejs, prisma-dev-nodejs). Never part of the actual project.
   - `niu-dash-repo/` — old static HTML backup; the real project is the framework version (app/components/package.json). See Pitfalls for detection.
   - `.wget-hsts` — junk file from wget download
   - `<project>.tar.gz` or `<project>.zip` nested inside the zip — a redundant archive
   - `__MACOSX/` — macOS metadata folder
   - `.DS_Store` — macOS hidden files

3. **Understand the structure:**
   - Does the build script expect a specific directory layout?
   - Are files at root level vs nested in a single subdirectory?
   - **Flatten if zip has a single root directory:** if `unzip -l` shows only files inside e.g. `AIFileOrganizer/` and nothing at zip root, move the contents up one level so the project path is clean.
   - **Read ALL source files before writing docs** — the README you write must accurately reflect actual code, not just the zip name. Minimal coverage for a thorough README: AndroidManifest.xml, build.gradle (dependencies, minSdk, compileSdk), MainActivity.kt, ViewModel, core organizer files, models/data classes, UI screens, CI workflow, strings/colors/themes. Map out the architecture before writing.
   - **Preserve CI workflows:** check `.github/workflows/` in the extraction — CI files often live only in a duplicate path (`home/user/...`) and get lost during cleanup. Search with `find /tmp/extracted -path '*/.github/workflows/*' -type f` before cleanup, and copy `.github/` to project root. Rebuild the CI file from memory of the original if the duplicate is already deleted.

4. **Audit before writing docs:**
   After understanding the structure, run a Ponytail audit (if skill is loaded) to classify issues by severity:
   - **P0 🚨** — Would crash at runtime (missing deps, broken imports, dead code that blocks build)
   - **P1 🟡** — Logic bugs, type mismatches, config errors
   - **P2 🔧** — Code quality (unused imports, dead code that doesn't block build)
   - **P3 📦** — Polish, docs, formatting
   
   Fix P0-P1 before git init. Log P2-P3 as deferred items in BACKLOG.md.

5. **Create project directory & organize:**
   ```bash
   mkdir -p ~/Desktop/Niumation/projects/<name>/
   # If flattening: copy contents one level up
   cp -r /tmp/<project-name>/<source>/* /tmp/<project-name>/<source>/.* ~/Desktop/Niumation/projects/<name>/ 2>/dev/null
   # Or if simple: move the root dir
   mv /tmp/<project-name>/<source> ~/Desktop/Niumation/projects/<name>/
   # Clean temp
   rm -rf /tmp/<project-name>
   ```

6. **Write (or leverage existing) project README.md** — if the project already has a high-quality README.md, SPEC.md, FEATURES_COMPARISON.md, etc., **don't rewrite them** — extract key info (purpose, architecture, features) for your AGENTS.md instead. Update the README.md only if it has factual errors or omits critical build/run instructions.
   - Filosofi / purpose dari proyek (1 paragraf)
   - Struktur direktori (tree view)
   - Cara build/run (dengan prasyarat)
   - Tabel komponen jika relevan
   - Gunakan bahasa Indonesia jika user meminta output berbahasa Indonesia

7. **Write .gitignore** — stack-specific entries. Common patterns:
   - Generic: `*.log`, `.DS_Store`, `node_modules/`, `work/`, `out/`, `build/`, `.env`
   - Android: `*.iml`, `.gradle/`, `/local.properties`, `/.idea`, `/build`, `/captures`, `.externalNativeBuild`, `.cxx`, `local.properties`, `/app/build`, `*.apk`, `*.aab`, `*.jks`, `*.keystore`
   - Python: `__pycache__/`, `*.pyc`, `.venv/`, `venv/`, `*.egg-info/`, `.pytest_cache/`
   - Rust: `/target/`, `Cargo.lock` (for libraries)
   - Node: `node_modules/`, `dist/`, `.next/`, `*.tsbuildinfo`

7.5. **Pre-publish file audit** — scan for binary blobs and non-project artifacts BEFORE git init:
   ```bash
   # Large binary blobs (>10MB) that shouldn't be committed
   find . -type f -size +10M -not -path './.git/*' | head -20
   
   # Non-project artifacts at root level — common offenders:
   #   bin/       — compiled binaries (ffprobe, ffmpeg static builds)
   #   .config/   — user config from dev's own machine
   #   Videos/    — media directories
   #   .claude/   — project-specific Claude instructions for the original repo
   #   node_modules/, venv/, __pycache__/ — dependency dirs
   # Check with:
   find . -maxdepth 1 -type d \( -name "bin" -o -name ".config" -o -name "Videos" \
     -o -name "node_modules" -o -name "venv" -o -name ".venv" \
     -o -name ".claude" -o -name ".git" \) | head -10
   
   # Existing AGENTS.md / CLAUDE.md — preserve these! Do NOT overwrite them
   ls AGENTS.md CLAUDE.md README.md 2>/dev/null

   # PKGBUILD URL check — if the project is a fork/port, the url field
   # likely points to the ORIGINAL upstream repo, not the actual publish target:
   grep -n "url=" PKGBUILD 2>/dev/null
   ```
   Add entries to `.gitignore` for each discovered artifact. For PKGBUILD URLs, fix them right after git init.

8. **Initialize git & push to GitHub:**
   ```bash
   cd ~/Desktop/Niumination/projects/<name>
   git init && git add -A && git commit -m "initial: <Nama> — <short description>"
   
   # Create remote and push in one command
   gh repo create Niumination/<Repo-Name> --public --description "<description>" --source=. --remote=origin --push
   ```
   
   If `gh repo create --push` fails (token auth issue on macOS keychain), try these fallbacks in order:

   **A) SSH (preferred — matches all other Niumination repos):**
   ```bash
   git remote add origin git@github.com:Niumination/<Repo-Name>.git
   git push -u origin main
   ```

   **B) HTTPS with inline token (token exposed in remote URL — fix immediately):**
   ```bash
   git remote add origin "https://x-access-token:$(gh auth token)@github.com/Niumination/<Repo-Name>.git"
   git push -u origin main
   # Then fix remote URL to clean HTTPS
   git remote set-url origin https://github.com/Niumination/<Repo-Name>.git
   ```

   **C) If both fail (e.g. timeout on large push):** verify the push actually didn't succeed first with `git log --oneline origin/main` after the remote URL is cleaned up. If the remote is behind, force-push with:
   ```bash
   git push --force origin main
   ```

   **Note:** After verification, always clean the remote URL to either `git@github.com:Niumination/<Repo>.git` (SSH, stable) or `https://github.com/Niumination/<Repo>.git` (HTTPS, clean). Never leave the token-embedded URL in the config.

9. **Sync ecosystem documentation:**
   - **AGENTS.md:** Add row to Project Catalog (cari section yang tepat), update footer timestamp + file count. 4 surfaces to patch: header banner, directory tree, project catalog table, DOX footer.
   - **BACKLOG.md:** Update header audit count, add/move task entry with `@project-tag`, update footer timestamp
   - Format AGENTS.md Project Catalog row: `|| **Nama** | \`projects/<path>/\` | Stack | \`github.com/Niumination/<repo>\` | 🟢 GitHub | <date> | ✅ v1.0.0 — <description> 🆕 |`
   - Fix any formatting issues in the target file before inserting (e.g. literal `\n` that should be real newlines)
   - Use `search_files()` to find ALL occurrences of 🆕 or "no commits yet" in AGENTS.md that need updating

10. **Memory:** Save durable facts if space permits (repo URL, path, stack, purpose — keep under 150 chars)

11. **Remove temp files:** `/tmp/<extracted-files>`

### Step 1: Gather Metadata

Check these before creating anything:

```bash
cd ~/Desktop/Niumination

# Does the project exist?
ls -d <project-name>/ 2>/dev/null

# Does it have a git remote?
cd <project-name> && git remote -v 2>/dev/null

# What stack does it use?
ls <project-name>/*.json <project-name>/*.yaml <project-name>/*.toml <project-name>/Cargo.toml 2>/dev/null

# Does it have existing docs?
ls <project-name>/AGENTS.md <project-name>/BACKLOG.md <project-name>/README.md 2>/dev/null
```

### Step 2: Create AGENTS.md

Use the tier1 template as reference (in `brain/templates/tier1.md`):

```markdown
# <Project Name> — Project AGENTS.md

**Lokasi:** `<path>`
**Stack:** <stack>
**Remote:** `github.com/Niumination/<repo>`
**Status:** 🟢 Active / 🟡 Pending

## Overview

<1-2 sentence description>

## Tasks

Lihat `BACKLOG.md` untuk task detail.
```

Key sections every AGENTS.md needs:
- Name + location (absolute path)
- Stack tags
- Remote URL (if git-enabled)
- Overview (1-2 sentences)
- Status: 🟢 Active / 🟡 Pending / ⚪ Stale / ✅ Done

**For projects with substantial source code** (15+ files, multiple modules, existing README/SPEC/companion docs), use the richer DOX format instead — see `references/rich-dox-example.md` for a module-breakdown + feature-status-table + task-next layout. It gives onboarding agents much faster architectural orientation than the minimal template.

### Step 3: Create BACKLOG.md

Format must be parseable by kanban-sync cron:

```
# <Project> — Sub-BACKLOG

**Master:** `BACKLOG.md` (root)

## Tasks

- [ ] **Task name** — Description — @project-tag
```

**Rules:**
- Lowecase kebab-case for `@project-tag`
- Status: `[ ]` (todo), `[o]` (in_progress), `[x]` (done)
- One `@project-tag` per line (last wins)

### Step 4: Create brain/projects/ entry

```bash
mkdir -p brain/projects/<slug>
```

Create `brain/projects/<slug>/readme.md` with project overview data.

### Step 5a: Bulk Register Multiple Untracked Projects Into Ecosystem

When the user says "daftarkan semua yang belum terdaftar" or multiple projects are missing from the ecosystem catalog, use this bulk workflow instead of looping Step 5a individually:

⚠️ **Pre-flight:** Run the Pre-flight Environment Check above first. The bulk workflow assumes `scripts/eco-collect.py`, `scripts/generate-ecosystem-json.py`, root `AGENTS.md`/`BACKLOG.md`, and `brain/logs/` all exist. If any are missing, report the gaps to the user before running the JSON overwrite step — never write `ecosystem-status.json` into a path that doesn't exist yet.

**1. Discover untracked dirs in `projects/` and `incubator/`:**
```python
import json, os
root = '/Users/zaryu/Desktop/Niumination'
with open(root + '/Production/niu-dash/public/data/ecosystem-status.json') as f:
    eco = json.load(f)
registered = {p["git"].split("/")[-1].lower() for p in eco["projects"] if p.get("git")}

for base in ['projects', 'incubator']:
    d = root + '/' + base
    if os.path.isdir(d):
        for item in sorted(os.listdir(d)):
            if os.path.isdir(os.path.join(d, item)) and item.lower() not in registered:
                print(f'{base}/{item}')
```

**2. Map folder name → GitHub repo under Niumination:**
- Infer from folder name (e.g. `maze-3d` → `Maze-3D-Game---Web-Based`, `niuterm` → `NiuTerm`)
- Verify via `gh repo view Niumination/<inferred-name>` if unsure
- Note which are expected private vs public based on prior knowledge

**3. Infer tier:**
- `projects/` folders → **Tier 2** (active development)
- `incubator/` folders → **Tier 3** (experimental/prototype)
- Special cases: `brain` = Tier 1, `Niu-Flow` already registered as Tier 1

**4. Batch-write both JSON files atomically:**

*ecosystem-status.json* fields per new entry:
```
{
  "name": "<Project Name>",
  "tier": <1|2|3>,
  "status": "<in_progress|prototype|done>",
  "priority": "<P1|P2|P3>",
  "git": "Niumination/<repo-name>",
  "dox": false,
  "desc": "<short description>"
}
```

*released.json* fields per new entry:
```
{
  "repoName": "<repo-name>",
  "name": "<Project Name>",
  "status": "<status>",
  "version": "",
  "notes": "<desc>",
  "dateMarked": "2026-07-22T00:00:00.000Z",
  "_autoDetected": False
}
```
Also append an `activityLog` entry for each new release.

**5. After writing:** verify no duplicate names/repoNames, confirm counts increased.

**Pitfall:** Some folder names don't match GitHub repo names exactly (e.g. `niuterm` → `NiuTerm`, `maze-3d` → `Maze-3D-Game---Web-Based`). Always verify the repo exists before assuming the mapping.

### Step 5a: Register Existing Untracked Project Into Ecosystem

When the user has placed a project directory (with or without AGENTS.md) into `projects/` but it's not yet tracked in the ecosystem manifest or root AGENTS.md project catalog:

**Detection:**
```bash
# Compare manifest vs actual filesystem
python3 -c "
import json, os
root = '/Users/zaryu/Desktop/Niumination'
with open(root + '/brain/logs/eco-manifest.json') as f:
    data = json.load(f)
manifest_paths = {r['path'] for r in data.get('git_repos', [])}
manifest_paths |= {n['path'] for n in data.get('non_git', [])}

for item in os.listdir(root + '/projects'):
    p = 'projects/' + item
    if p not in manifest_paths and os.path.isdir(root + '/' + p) and not item.startswith('.'):
        print(f'[UNTRACKED] {p}')
for item in os.listdir(root + '/Production'):
    p = 'Production/' + item
    if p not in manifest_paths and os.path.isdir(root + '/' + p) and not item.startswith('.'):
        print(f'[UNTRACKED] {p}')
"
```

**Registration workflow:**

⚠️ **Pre-flight:** Run the Pre-flight Environment Check above first. Steps 2–6 all depend on `scripts/eco-collect.py`, root `AGENTS.md`/`BACKLOG.md`, and `brain/logs/` existing. If any are missing, report the gap to the user before running pipeline commands.

1. **If non-git directory:** Add path to `NON_GIT_DIRS` in `scripts/eco-collect.py`:
   ```python
   NON_GIT_DIRS = [
       ...
       "projects/x-downloader",
   ]
   ```

2. **Regenerate manifest:**
   ```bash
   cd ~/Desktop/Niumination
   python3 scripts/eco-collect.py --force
   ```

3. **Verify the project appears in the output:**
   ```bash
   python3 scripts/eco-collect.py --force 2>&1 | grep -A1 "<project-name>"
   ```

4. **Update root AGENTS.md project catalog:**
   - Add a row to the Project Catalog table (find the correct section with `search_files()`)
   - Format: `| **Nama** | \`projects/<path>/\` | Stack | lokal | ⚪ Local | <date> | 🆕 Description |`
   - Update the total project count in the header banner (line ~6)
   - Update any stale count references (search `22 git`, `19 git`, `28 item`, etc.)

5. **Regenerate ecosystem-status.json for Niu-Dash dashboard:**
   ```bash
   python3 scripts/generate-ecosystem-json.py
   ```

6. **Verify final manifest reflects correct counts:**
   ```bash
   python3 -c "
   import json
   data = json.load(open('/Users/zaryu/Desktop/Niumination/brain/logs/eco-manifest.json'))
   print(f\"{data['total_git']} git + {data['total_non_git']} non-git = {data['total_items']} items\")
   for n in data.get('non_git', []):
       if 'x-downloader' in n['path']:
           print(f\"  ✅ {n['path']}: {n.get('file_count',0)} files registered\")
   "
   ```

**Common pitfalls:**
- `eco-collect.py` auto-discovers git repos in `projects/*/` and `Production/*/` — no NON_GIT_DIRS entry needed for git repos
- **After `git init`, REMOVE the project from `NON_GIT_DIRS`** — otherwise it appears twice in the manifest (once as git, once as non-git). Then regenerate with `--force`.
- Only non-git directories need `NON_GIT_DIRS` entries — check if the project has `.git` first BEFORE adding it to NON_GIT_DIRS
- After updating AGENTS.md, always check the table format is consistent (`| **Name** |` not `|| **Name** |`)
- Run `generate-ecosystem-json.py` after ALL eco-collect changes are done (it reads the manifest)
- If the project already has its own AGENTS.md in the directory, DO NOT overwrite it — only update root references

### Step 5: Update Ecosystem Surfaces

| # | Surface | What to update |
|---|---------|----------------|
| 1 | `BACKLOG.md` | Add task entries with `@project-tag`, update scoreboard counts |
| 2 | `AGENTS.md` | Add to Directory Structure tree + Project Catalog table |
| 3 | `docs/ekosistem-status.md` | Add to production table + directory tree, update header counts |
| 4 | `brain/logs/eco-manifest.json` | Add git_repo entry, increment totals (local-only; file is gitignored) |
| 5 | `brain/docs/ecosystem-changelog.md` | Log the new addition |

**⚠️ docs/ekosistem-status.md must stay in sync** — this file has its own copy of the Production/ directory tree and production table. Updating only AGENTS.md and BACKLOG.md leaves a stale dashboard reference.

**⚠️ eco-manifest.json edits are local-only** — the file is gitignored. Manual JSON edits do not get committed to the Niumination repo unless you `git add -f`.

**Quick refresh pattern:** When you only need to update `head`, `last_commit`, or `remote_url` fields without regenerating the whole manifest, use a targeted Python script:
```python
import json
with open('brain/logs/eco-manifest.json') as f: data = json.load(f)
for repo in data['git_repos']:
    # repo['head'] = '<new sha>'
    # repo['last_commit'] = '<iso date>'
    # repo['remote_url'] = repo['remote_url'].replace('https://', 'git@github.com:Niumination/').replace('.git.git','.git')
    pass
# Update totals if structure changed
# data['total_items'] = data['total_git'] + data['total_non_git']
json.dump(data, open('brain/logs/eco-manifest.json','w'), indent=2, ensure_ascii=False)
```
After editing, verify with:
```bash
python3 -c "import json; d=json.load(open('brain/logs/eco-manifest.json')); print(f\"{d['total_git']} git + {d['total_non_git']} non-git = {d['total_items']} items\")"
```

**⚠️ Ponytail must be excluded from all GitHub pushes** — never stage, commit, or push `ponytail/` from any project directory. This is a permanent exclusion per user policy.

**⚠️ SSH enforcement** — every Niumination remote must use `git@github.com:Niumination/<Repo>.git`. After any scaffolding or bulk remote change, verify with:
```bash
for d in ~/Desktop/Niumination/Production/*/ ~/Desktop/Niumination/projects/*/ ~/Desktop/Niumination/brain; do
  [ -d "$d/.git" ] || continue
  u=$(git -C "$d" remote get-url origin)
  case "$u" in https://*) echo "HTTPS_VIOLATION: $d -> $u" ;; esac
done
```

### Step 5.5: Bulk Remote Normalization (HTTPS → SSH)

When registering a new project or refreshing ecosystem state, always normalize remotes to SSH. A single project can slip in with HTTPS; do a full scan instead of checking one project.

```bash
cd ~/Desktop/Niumination
for d in Production/*/ projects/*/ brain; do
  [ -d "$d/.git" ] || continue
  u=$(git -C "$d" remote get-url origin 2>/dev/null || true)
  case "$u" in
    https://github.com/Niumination/*.git)
      ssh=${u/https:\/\/github.com\/Niumination/git@github.com:Niumination}
      git -C "$d" remote set-url origin "$ssh"
      echo "FIXED: $d -> $ssh"
      ;;
  esac
done
```

**Pitfall:** Some remotes use the org lowercase (`git@github.com:niumination/...`). These are functionally valid because SSH resolves both forms. Fix only if the remote is on a personal fork repo — otherwise preserve the exact casing already in use. For the complete scan+fix script, see `references/remote-normalization.md`.

### Step 6: Promote to Production

After a project in `projects/` has matured — bugs fixed, deployed, tested, CI green — promote it to `Production/` for archival as a completed release.

**When to promote:**
- User explicitly says "pindahkan ke production" / "move to production"
- Project meets maturity criteria: deployed live, CI green, tested, documented, git pushed, no P0/P1 bugs

**⛔ Do NOT preemptively promote** — wait for the user to ask. Production/ is read-only after promotion.

**Promotion workflow:**

1. **Add final notes — do NOT implement anything**
   If the user mentions future design/improvement work alongside the promotion request, note them in BACKLOG.md **only**. Do not implement. See `project-orientation` skill's "Catat aja / Note only means DO NOT IMPLEMENT" pitfall for the canonical failure story.
   ```bash
   # Correct: add deferred design note to BACKLOG.md
   - [ ] **🎨 Polish UI** — Custom theme, animations, splash screen — @project-tag
   ```

2. **Update BACKLOG.md** — Mark current tasks done, add deferred items as P4:
   - Change `[o]` or `[ ]` to `[x]` for completed tasks
   - **Header stats:** increment `✅ done` count (e.g. `5 ✅ done` -> `9 ✅ done`), decrement active
   - **P1/P2/P3 task statuses:** update each promoted project's line from `[~]` to `[x]`
   - **Scoreboard (SCOREBOARD EKOSISTEM):** append `🏭 Production` to each promoted project's row
   - **D1 entries:** add a new entry line for the promotion (e.g. `- **[24 Jun] Promotion: <project> moved to Production/` before existing lines)
   - Add new deferred entries with descriptive emoji prefix (🎨 Design, 🔧 Tech debt, 📦 Feature)
   - Update scoreboard counts if applicable
   - Update footer timestamp

3. **Move the directory:**
   ```bash
   mv ~/Desktop/Niumination/projects/<name> ~/Desktop/Niumination/Production/<name>
   ```

4. **Commit with standard message:** After moving, commit + push from the new location:
   ```bash
   cd ~/Desktop/Niumination/Production/<name>
   git add <modified files>   # e.g. AGENTS.md if it had path updates
   git commit -m "mv: <name> -> Production/"
   git push
   ```
   The standard commit message format is `"mv: <name> -> Production/"`.

5. **Verify git integrity after move:**
   ```bash
   cd ~/Desktop/Niumination/Production/<name>
   git log --oneline -3      # should show history
   git status                 # should be clean
   ```
   Git repos survive directory moves on macOS — `.git/` stores paths relative to the repo root, not absolute.

6. **Patch AGENTS.md root DOX** (up to 6 surfaces, not just the 4 for scaffolding):
   - **Directory tree:** Remove `├── <name>/` from `projects/` subtree, add to `Production/` subtree. ALSO update the Production/ count in the header comment (e.g. `— 7 dir` -> `— 10 dir`)
   - **Project catalog table:** Change path prefix from `projects/<path>/` to `Production/<path>/`, update Status column to `✅ Production` / `🏭 Production`, update Last Push date
   - **DOX Chain (catalog footer):** If the project was listed under the DOX validation chain, update its path from `projects/...` to `Production/...`
   - **Timeline / Priority section:** If the project was listed under a priority/timeline section (e.g. `| 🟡 **1-3 hari** | <project> |`), remove or move it. Typically the project graduates from "upcoming/short-term" to "completed/production"
   - **Eksekusi Selanjutnya (top section):** Add a completed action item if one doesn't exist yet
   - **Header banner stats:** Increment Production folder count if present

7. **Update memory:**
   - Replace the old `projects/` path entry with `Production/` path
   - Increment the Production project count (e.g., "7 proyek mature" -> "8 proyek mature")
   - Compact other entries if near the 2,200 char limit

8. **Update ecosystem surfaces:**
   | # | Surface | What to update |
   |---|---------|----------------|
   | 1 | `BACKLOG.md` | Header stats, task statuses, scoreboard, D1 entry |
   | 2 | `AGENTS.md` | Tree, catalog table, DOX Chain, timeline, eksekusi selanjutnya |
   | 3 | `brain/docs/ecosystem-changelog.md` | Log the promotion |
   | 4 | `scripts/eco-collect.py` | Remove from `NON_GIT_DIRS` if listed. ALSO ensure `scan_dirs += sorted(NIUMINATION.glob("Production/*"))` exists in `auto_discover_git_repos()` |
   | 5 | Ecosystem pipeline | Run `python3 scripts/eco-collect.py --force && python3 scripts/generate-ecosystem-json.py`, commit + push brain + niu-dash |
   | 6 | Memory | Update path + increment count |
   
   See `references/eco-pipeline.md` for full ecosystem pipeline details.

**Verification:**
```bash
ls ~/Desktop/Niumation/Production/<name>/
git -C ~/Desktop/Niumation/Production/<name> log --oneline -1
```

**Pitfalls:**
- **Production/ is READ-ONLY after promotion** — do NOT modify project source files inside Production/ after moving. Only update root-level docs (BACKLOG.md, AGENTS.md) that reference the project.
- **Ecosystem manifest must be updated after promotion** — `eco-collect.py`'s auto-discovery skips `NON_GIT_DIRS`. If you promoted a project out of `NON_GIT_DIRS`, remove it from that list. If you promoted INTO `Production/`, ensure `auto_discover_git_repos()` has `scan_dirs += sorted(NIUMINATION.glob("Production/*"))` or the repo won't be counted. After all changes, run `python3 scripts/eco-collect.py --force && python3 scripts/generate-ecosystem-json.py` and push both brain + niu-dash — see `references/eco-pipeline.md`.
- **Memory limit** — after 7+ Production projects, memory entries can exceed 2,200 chars. Remove old/deleted project entries when adding new ones.
- **Shell path access loss** — if `~/Desktop/Niumation` is a macOS Finder alias to an external volume (NTFS/exFAT), the background shell may lose access to it mid-session. `stat -f %R ~/Desktop/Niumation` reveals the resolved real path. If the alias stops resolving, **immediately fall back to terminal + sed/perl** — Hermes file tools (read_file/patch/write_file) use a different sandbox path than the shell. When they fail, terminal still works. Do NOT explain the failure to the user; just use `sed`, `perl -i -pe`, or `grep` via terminal to edit files instead. Keep explanations minimal.
- **".no commits yet" after move** — If the project had `git init` but zero commits, `.git/` moves with the project. `git status` will still work; `git log` will error — report it as "init done, needs first commit" rather than broken git.

### Step 9: Rename an Existing Project

When the user asks to rename a project that's already set up with git, docs, and ecosystem references:

1. **Rename the directory:**
   ```bash
   mv ~/Desktop/Niumation/{old-name} ~/Desktop/Niumation/{new-name}
   ```

2. **Find all references across root docs:**
   ```bash
   grep -rn "old-name" AGENTS.md BACKLOG.md
   ```

3. **Update all surfaces (terminal + sed/perl since file tools may fail on root path):**
   ```bash
   cd ~/Desktop/Niumation
   # AGENTS.md: tree line, table line (name + path), footer
   perl -i -pe 's/old-name/new-name/g' AGENTS.md
   # BACKLOG.md: audit table, task entries
   perl -i -pe 's/old-name/new-name/g' BACKLOG.md
   # Project's own AGENTS.md
   perl -i -pe 's/old-name/new-name/g' projects/new-name/AGENTS.md
   ```

4. **Git survives the rename** — `.git/` stores paths relative to repo root, not absolute. Verify:
   ```bash
   git -C ~/Desktop/Niumation/projects/new-name status
   ```

5. **Verify zero stale references remain:**
   ```bash
   grep -rn "old-name" AGENTS.md BACKLOG.md projects/new-name/AGENTS.md
   ```

## Priority Determination

| If project has... | Assign |
|-------------------|--------|
| Active development, critical bugs | P1 🚨 |
| Active development, maintained | P2 🟡 |
| Stale / experimental / no pushes in 30+ days | P3 🟢 |
| No remote, no deploy, single file | ⚪ Registry only |

## Templates Location

Templates live at `brain/templates/`:
- `tier1.md` — Full AGENTS.md template (10+ fields)
- `tier2.md` — Lightweight sub-BACKLOG template for Tier 2
- `readme.md` — Standard README template

## Reference Files

- `references/android-gitignore.md` — Android .gitignore entries
- `references/eco-pipeline.md` — Full pipeline steps for eco-collect + generate-ecosystem-json
- `references/rich-dox-example.md` — Example of richer DOX format for projects with substantial code
- `references/remote-normalization.md` — Full scan+fix script for HTTPS→SSH normalization
- `references/ecosystem-json-fields.md` — Field definitions for ecosystem-status.json and released.json
- `references/terminal-tool-loop-recovery.md` — Recovery pattern when `terminal()` fails on relative paths in portable Hermes setups
- `references/project-folder-watcher.md` — Cron-based detection for new folders in `projects/` or `incubator/` (sentinel + lock + Hermes cron `repeat=0` pattern)

### Step 7.5: Post-Publish — Fix CI Build (if CI workflow is present)

After pushing to GitHub, the CI almost always fails on a new project. This is expected. Fix in order:

**1. Read CI logs to find actual errors:**
```bash
# List recent runs
gh run list --repo Niumination/<Repo> --limit 3

# View failed log — search for actionable errors
gh run view <RUN_ID> --repo Niumination/<Repo> --log | grep -E "(e:|Unresolved|FAILED|error:)" | head -20

# Or get the full log tail
gh run view <RUN_ID> --repo Niumination/<Repo> --log | tail -100
```

**2. Common Android CI failure patterns & fixes:**

| Symptom | Root Cause | Fix |
|---------|-----------|-----|
| `Unresolved reference: tasks` + `Unresolved reference: await` | Missing `kotlinx-coroutines-play-services` (`.await()` on ML Kit / Play Services `Task`) | Add `implementation("org.jetbrains.kotlinx:kotlinx-coroutines-play-services:1.7.3")` to `app/build.gradle.kts` |
| `lintVitalRelease FAILED` — `InvalidFragmentVersionForActivityResult` | False positive: activity-compose already bundles fragment >= 1.3.0 | Add `lint { disable += "InvalidFragmentVersionForActivityResult" }` to `android {}` block |
| `No files were found with the provided path: app/build/outputs/apk/release/app-release-unsigned.apk` | Release APK path is `app-release.apk` (not `-unsigned`) when minify + signing is configured | Fix `path:` in upload-artifact step to match actual output |
| `Create Release` 403 — `Resource not accessible by integration` | Default `GITHUB_TOKEN` in Actions **cannot create releases** (needs `contents: write` PAT) | Add `continue-on-error: true` to the release step, or skip auto-release and use `gh release create` manually |
| `BUILD FAILED` with no Kotlin errors | Lint, resource linking, or missing SDK component | Scroll up in logs past the stack trace to find the actual error. Look for `Lint found fatal errors` or `AAPT2` errors |

**3. Fix → Commit → Push:**
```bash
git add -A && git commit -m "fix: <deskripsi singkat>"
git push origin main
```

**4. Wait and check the new run:**
```bash
sleep 240  # CI typically takes 2-3 minutes
gh run list --repo Niumination/<Repo> --limit 1 --json status,conclusion
```

**5. Download artifacts from successful CI run:**
```bash
# List artifacts for a run
gh run view <RUN_ID> --repo Niumination/<Repo>

# Download specific artifact
gh run download <RUN_ID> --repo Niumination/<Repo> --name <artifact-name> --dir ./<dir>
```

**6. Create a GitHub Release from CLI (bypass Actions token limitation):**
```bash
# The Actions GITHUB_TOKEN cannot create releases by default.
# Use gh CLI (user token) directly from terminal:
gh release create v1.0.<N> --repo Niumination/<Repo> \
  --title "<Project> v1.0.<N>" \
  --notes "<changelog>" \
  <path-to-apk-or-binary>
```

**7. Loop** — repeat steps 1-4 until CI is green. One fix at a time.

**Important:** Do NOT push every individual CI fix commit as separate pushes. Batch fixes per-cycle: gather all errors from one run log, fix them together, push once. Each CI run costs time and GitHub Actions minutes.

## Pre-flight Environment Check

Before running any registration workflow or pipeline, verify the Niumination root is actually set up the way the skill assumes. Missing pieces are common on fresh or stripped-down machines.

```bash
cd ~/Desktop/Niumination

# 1. Root docs
[ -f AGENTS.md ] && [ -f BACKLOG.md ] || echo "MISSING: root AGENTS.md and/or BACKLOG.md"

# 2. Pipeline scripts
[ -f scripts/eco-collect.py ] && [ -f scripts/generate-ecosystem-json.py ] || echo "MISSING: pipeline scripts"

# 3. Expected directories
for d in brain projects Production incubator; do
  [ -d "$d" ] || echo "MISSING: $d/"
done

# 4. brain target dirs used by registration
for d in brain/logs brain/docs brain/projects; do
  [ -d "$d" ] || echo "MISSING: $d (mkdir -p before proceeding)"
done

# 5. Verify eco-manifest.json exists before reading it
[ -f brain/logs/eco-manifest.json ] && echo "manifest OK" || echo "MANIFEST MISSING — run eco-collect.py first"
```

If any directory is missing, create it with `mkdir -p` before continuing. If root docs or pipeline scripts don't exist yet, report the gap to the user — don't silently skip registration surfaces that depend on them.

## Verification

After scaffolding, verify:

```bash
# DOX files exist
ls <project>/AGENTS.md <project>/BACKLOG.md 2>/dev/null

# Git hook active (if git repo)
ls <project>/.git/hooks/pre-commit 2>/dev/null

# BACKLOG format parseable
grep '@<project-tag>' BACKLOG.md

# brain dir exists
ls brain/projects/<slug>/ 2>/dev/null
```

## Pitfalls

- **Project already has existing docs** — read first, merge don't overwrite. Check for `AGENTS.md`, `CLAUDE.md`, `README.md`, and `BACKLOG.md` before writing anything. The existing project AGENTS.md may contain architecture notes, conventions, or run commands that took the developer time to document.
- **Hermes portable HOME discrepancy in scripts/cron** — `launch.sh` sets `HOME=$PORTABLE_ROOT/.cache/unix-home`, but session evidence shows active tool configs and symlinks in `data/home/.local/`, `data/home/.config/`, and `data/home/.notebooklm-mcp-cli/`. Cron jobs and scripts should **always use absolute paths for Niumination dirs** (`/Users/zaryu/Desktop/Niumination/...`) regardless of which HOME is active. In a previous session, a watcher script silently failed because Hermes inherited a HOME that pointed to the USB, causing `find` on `$HOME/Desktop/Niumination/projects` to return nothing when the dir was actually on the internal Mac SSD.
- **Migration source vs active project** — When a project has multiple versions of the same app side by side (e.g. `niu-dash-repo/` = static HTML, and `niu-dash-fullstack/` = Next.js framework), the **framework version is the active project**, not the static HTML copy. Common signs:
  - `index.html`, `ecosystem.html`, `development.html` at root = old static page (migration source)
  - `app/`, `components/`, `prisma/`, `package.json` = framework project (active)
  - `home/user/<project>/` inside the project dir = extraction artifact from original dev environment, NOT the actual project
  - Before cleaning, confirm with the user: "mau simpan yang mana — static page atau framework?" Or check if the framework version has a `package.json` with modern dependencies (Next.js, React, Prisma — these are active signals).
- **User says \"proyek yang terakhir kita update\"** — this refers to the framework/Next.js project they most recently worked on, not the static HTML backup or migration source.
- **PKGBUILD url points to wrong upstream** — If the project is a fork or port from another developer, `PKGBUILD`'s `url=` and `source=` fields almost certainly point to the original repo (e.g. `yt-dlp/yt-dlp`). Fix them to point to the actual GitHub repo before the first commit. Also check any `install.sh` or `README.md` for stale remote references.
- **Empty directory** — still create AGENTS.md/BACKLOG.md, mark as ⚪ Empty. Check for stale duplicates first: a dir with only `.DS_Store` and no git may be a leftover copy (e.g. JHcode was a stale duplicate of PemdiAcehTengah). Read AGENTS.md project catalog to confirm.
- **Non-standard path** (in `projects/` vs root) — use correct relative path in AGENTS.md
- **@project-tag collision** — check BACKLOG.md first to avoid duplicate tags
- **git remote doesn't match Niumination org** — note as "fork" or "personal" in status
- **CI workflow lost in duplicate path** — zip dari external source (`home/user/`, `Belum disentuh/`) sering bawa `.github/workflows/` hanya di duplikat path. Cari dulu `find /tmp/extracted -path '*/.github/workflows/*'` sebelum cleanup, lalu copy ke root project.
- **Android .gitignore reference** — lihat `references/android-gitignore.md` di skill ini untuk daftar lengkap entries Android saat scaffolding proyek Android
- **`gradlew` not executable** — `chmod +x gradlew` is required before any Gradle build. Add it to the init commit: `git add -A && chmod +x gradlew && git add gradlew && git commit`. Without it, CI runner will also fail on first push.
- **CI runs survive agent crash** — CI runs on GitHub's servers, not locally. If the Mac crashes mid-task while a CI run was triggered, the CI run continues and completes independently. After recovery, check `gh run list` to see if the build finished.
- **macOS crash recovery** — Jika Mac mati/direstart di tengah scaffolding (power loss, kernel panic):
  - Git database survives (journaled writes) — commit history tetap utuh
  - BACKLOG.md, AGENTS.md, dan file proyek lain **mungkin rollback ke state sebelum patch** karena write cache belum di-flush
  - Setelah restart, WAJIB re-verify: `search_files()` untuk AGENTS.md + `read_file()` untuk BACKLOG.md, cek apakah patch sebelumnya masih intact
  - 4 AGENTS.md surfaces perlu dicek: header banner, directory tree, project catalog table, DOX footer
  - 2 BACKLOG.md surfaces: header audit line, task entry status + description
  - Re-remote URL: cek `git remote -v` — token-embedded URL mungkin masih terpasang, ganti ke SSH
- **Missing pipeline scripts / root docs** — `scripts/eco-collect.py`, `scripts/generate-ecosystem-json.py`, root `AGENTS.md`, and `BACKLOG.md` may not exist on a fresh or stripped-down Niumination checkout. Always run the Pre-flight Environment Check before bulk registration or pipeline steps. Do not attempt `python3 scripts/eco-collect.py --force` if the file is missing.
- **Missing `Production/` or `incubator/` directories** — Tier inference in bulk registration assumes these dirs exist. If one or both are absent, infer tier from what exists (`projects/` → Tier 2 if present, else skip). The detection loop should `if os.path.isdir(d):`-guard each base dir before listing.
- **eco-pipeline.json writes without path existence check** — `generate-ecosystem-json.py` outputs to `Production/niu-dash/public/data/ecosystem-status.json`. If `Production/niu-dash/` doesn't exist yet, the write will fail. Verify the output path exists before running the script.
