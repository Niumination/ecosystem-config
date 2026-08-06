# Inventory Cross-Reference: Declared vs Real

Use when auditing a static inventory/manifest (PROJECTS array in a dashboard, README project table, config.yml) against the actual live inventory (GitHub API repos, filesystem directories, database tables).

## When to Use

- User asks: *"Apakah semua proyek sudah di update ke [dashboard]?"*
- User asks: *"Apakah ada yang belum di update?"*
- Pre-deployment check: does the dashboard/project-listing match reality?
- After adding/removing repos: confirm the listing is in sync

## Methodology

### Step 1: Extract the Declared Inventory

Read the file that contains the project listing. Most common patterns:

**JavaScript array/object in HTML:**
```python
import re
from hermes_tools import read_file

result = read_file('index.html', offset=697, limit=120)
content = result.get('content', '')

# Extract all GitHub repo URLs from the data structure
declared = set()
for m in re.finditer(r'github\.com/Niumination/([^"\'\s,/]+)', content):
    declared.add(m.group(1))
```

**JSON file (released.json, ecosystem.json):**
```python
import json
# parse the JSON and extract path/repo fields
```

**Markdown table in README:**
```python
# Extract repo names from markdown links like [repo-name](https://github.com/Niumination/repo-name)
```

### Step 2: Fetch the Real Inventory

```python
import subprocess, json

# From GitHub API
result = subprocess.run(
    ['curl', '-s', 'https://api.github.com/users/Niumination/repos?per_page=100'],
    capture_output=True, text=True, timeout=30
)
real_repos = set()
for r in json.loads(result.stdout):
    if isinstance(r, dict):
        real_repos.add(r['name'])

# From filesystem (local-only projects)
import os
FS_ONLY_DIRS = {'Production', 'projects', 'TEDEO', 'Niu-Flow'}
# ... walk directories
```

### Step 3: Normalize for Comparison

Names differ by case, delimiter, or prefix across sources:

```python
def normalize(name):
    """Normalize repo/project name for fuzzy comparison."""
    return name.lower().replace('-', '').replace('_', '').replace('.', '').replace(' ', '')

declared_norm = {normalize(n): n for n in declared_repos}
real_norm = {normalize(n): n for n in real_repos}
```

**Common normalization edge cases:**
- **Case mismatch:** `AI-First-OS` vs `ai-first-os` — both exist on GitHub but are treated as different repos by the API. The dashboard may list neither, one, or a locally-sourced variant.
- **Prefix mismatch:** `ai-file-organizer-android` (GitHub) vs `AiFileOrganizer` (older repo) — the Android file manager migrated to a new name but both repos exist.
- **Deep path vs GitHub URL:** Some projects are listed with local paths (`/Users/zaryu/Desktop/Niumination/TEDEO/`) instead of GitHub URLs. Check if the directory exists to confirm the project is real.

### Step 4: Report Discrepancies

```python
# Find missing repos (real but not declared)
missing = []
for n, orig in sorted(real_norm.items()):
    if n not in declared_norm:
        missing.append(orig)

# Find extra entries (declared but not real — stale entries)
extra = []
for n, orig in sorted(declared_norm.items()):
    if n not in real_norm:
        extra.append(orig)
```

**Report format:**

```
## Cross-Reference Results

| Category | Count |
|----------|-------|
| ✅ Declared in dashboard | N |
| 🔴 Missing from dashboard | N |
| 🟡 Extra in dashboard (stale) | N |

### Missing (need adding)
  - repo-A  → GitHub exists, dashboard missing
  - repo-B  → Production/ project, dashboard missing

### Extra (stale entries to remove)
  - stale-project  → no longer exists
```

**Categorization by project location:**
| Where it lives | Action |
|----------------|--------|
| GitHub repo + Production/ | 🔴 **High** — production project, should be in dashboard |
| GitHub repo only (experimental) | 🟡 **Medium** — may not warrant dashboard listing |
| Filesystem only (not on GitHub) | 🟢 **Low** or ✅ skip — local workspace, doesn't need dashboard entry |
| Listed in released.json but not in PROJECTS | 🟡 **Medium** — released projects should be visible |

### Step 5 (Optional): Check Suspect Duplicates

When two repos have similar names or contents but differ in case/prefix, verify if they're duplicates:

```bash
# Check if both repos exist
for repo in "Niumination/AI-First-OS" "Niumination/ai-first-os"; do
    http_code=$(curl -s -o /dev/null -w "%{http_code}" "https://api.github.com/repos/$repo")
    echo "$repo: HTTP $http_code"
done

# Check if they have the same content (compare latest commit)
curl -s "https://api.github.com/repos/Niumination/AI-First-OS/commits?per_page=1" | python3 -c "import sys,json; print(json.load(sys.stdin)[0].get('sha','no commit')[:12])"
```

## Pitfalls

- **GitHub API rate limit** (60 req/hr for unauthenticated). For >100 repos, add authentication: `curl -H "Authorization: token $GITHUB_TOKEN"`.
- **Pagination:** The API returns 30 repos by default. Always specify `per_page=100` and handle pagination with `Link` headers for accounts with 100+ repos.
- **Case-sensitive comparison without normalization:** `AI-First-OS` and `ai-first-os` are different strings but both point to the same project intent. Normalize before comparing.
- **Stale repo entries in dashboards:** A project may have been removed from GitHub but still referenced in PROJECTS. These are extra entries — flag them for cleanup.
- **Self-referential listing:** The dashboard's own repo (e.g. `niu-dash`) may not list itself. This is typically intentional — flag it only if the user expects self-inclusion.
- **Projects duplicated across categories:** The same project may appear in both `ready` and `dev` categories. Flag as duplicate if it matters to the cross-reference.
