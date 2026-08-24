# Frontend–Backend Data Contract Debugging

## When to Use

After deploying a new frontend feature that fetches from a backend API endpoint, when the user asks "cekin, ada yang rusak?" or you want to verify the feature works end-to-end.

## The Problem

Frontend features are built assuming a specific API response schema. The actual API may return a different schema (different field names, types, or missing fields). The result: the feature renders with **incomplete data, wrong colors, or empty sections** — but no JavaScript error because the fields are merely `undefined`, not throwing.

**Related problem:** API completely unreachable (server down, CORS block, Mac sleeping). The frontend needs an **offline fallback** that uses data already loaded in the page rather than depending on an external remote URL that may 404.

## The Fix Pattern: Bidirectional Alignment

### 1. Backend: Add Missing Fields

The API endpoint (`server.js`) should serve the fields the frontend needs. Map existing data to the expected schema:

```js
// Example: /api/ecosystem endpoint
const priority = tier === 1 ? 'P1' : tier === 2 ? 'P2' : 'P3';
return {
  name,
  tier,
  priority,                    // NEW: derived from tier
  hasGit,
  git: hasGit ? `github.com/Niumination/${name}` : null,  // NEW: URL string
  hasDox,
  dox: hasDox,                 // NEW: parallel boolean
  cron: false,                 // NEW: default
  status: 'pending',           // NEW: default
  desc: '',                    // NEW: default
  deployUrl: KNOWN_DEPLOYS[name] || null,  // NEW: lookup table
};
```

### 2. Frontend: Resilient Reader

The render function should handle BOTH old and new schema formats, plus any fallback source:

```js
// Resilient priority detection — handles both old (tier:1,2,3) and new (priority:'P1')
var priority = p.priority || (p.tier === 1 ? 'P1' : p.tier === 2 ? 'P2' : 'P3');

// Resilient stats — handles both new (data.git) and old (data.summary.gitRepos) shapes
var gitCount = data.git || (data.summary && data.summary.gitRepos) || 0;
var doxCount = data.dox || (data.summary && data.summary.withDox) || 0;
var cronCount = data.crons || data.cronCount || 0;
```

### 3. API-Unreachable Fallback: Use Local Data

When the API server might be down (Mac sleeping, server not started, CORS block on GH Pages), the fetch should fall back to **already-loaded local data** — NOT an external URL that may also be unreachable:

```js
fetch(KANBAN_API_URL)
  .then(function(r){ return r.json(); })
  .then(function(data){
    ecosystemData = data;
    ecosystemLoaded = true;
    renderEcosystem();
  })
  .catch(function(){
    // BAD: external fallback URL that may 404
    // fetch('https://raw.githubusercontent.com/.../BACKLOG.md')
    
    // GOOD: use data already in the page
    var fbProjects = (typeof flatProjects !== 'undefined' ? flatProjects : []);
    ecosystemData = {
      projects: fbProjects.map(function(p){
        return {
          name: p.name,
          desc: p.desc || '',
          status: p.status || 'pending',
          priority: 'P3',
          git: p.repoUrl || null,
          dox: false,
          cron: false
        };
      }),
      git: 0, dox: 0, crons: 0, tasks: 0
    };
    ecosystemLoaded = true;
    renderEcosystem();
  });
```

This pattern works because:
- `flatProjects` is already loaded in the page (from the static PROJECTS config)
- No network dependency — works even when fully offline
- Users see their actual project list instead of an empty page
- Data is less rich (no tier/priority/dox details) but functional

### 3. Verify the Full Round Trip

After both fixes:

```bash
# 1. Test the raw API output
curl -s http://localhost:5199/api/ecosystem | python3 -c "
import sys,json
d=json.load(sys.stdin)
p=d['projects'][0]
for k,v in sorted(p.items()): print(f'{k}: {v}')
"

# 2. Check a specific project with known values
curl -s ... | python3 -c "
for p in d['projects']:
    if p['name']=='AuditTI-AT':
        print(p['priority'], p['git'])
"

# 3. Verify frontend JS syntax
node -e "
const fs=require('fs');
const html=fs.readFileSync('index.html','utf8');
const scripts=html.match(/<script>([\s\S]*?)<\/script>/g);
for(let s of scripts) { new Function(s.replace(/<\/?script>/g,'')); }
console.log('✅ JS syntax clean');
"
```

## Common Symptoms of Schema Mismatch

| Symptom | Likely Root Cause |
|---------|-------------------|
| **All cards show P3 (gray)** | Field `priority` missing — fallback to `tier` number not mapped |
| **Status all ⬜ pending** | Field `status` missing or field name differs (`state` vs `status`) |
| **Git/DOX tags empty** | Field `git`/`dox` missing — `p.git` is undefined → falsy → tag not rendered |
| **Stats bar shows 0** | Top-level counts (`git`, `dox`, `crons`) not in response |
| **Cards render with no data** | API returns `{projects: []}` or empty array — check scan logic |
| **JS error "Cannot read X of undefined"** | Expected nested object (e.g. `data.summary`) missing from response |

## Real Example: Ecosystem View Schema Mismatch (v2.16.5–v2.16.6)

The Ecosystem View sidebar feature was built expecting:
```js
{ priority: 'P1', git: 'github.com/...', dox: true, status: 'active', desc: '...', deployUrl: '...' }
```

But the Kanban API `GET /api/ecosystem` returned:
```js
{ tier: 1, hasGit: true, hasDox: true }  // no priority, status, deployUrl, desc
```

**Result:** All 28+ projects rendered as gray P3 cards with no tags — no JS error, just silent broken display.

**Fix:**
1. Backend: added `priority`, `git`, `dox`, `status`, `desc`, `deployUrl` to project objects + top-level `git`, `dox`, `crons`, `tasks` counts
2. Frontend: made `renderEcosystem()` check both `p.priority` and `p.tier` for backward compatibility
3. Stats bar: fallback from `data.git` → `data.summary.gitRepos` for old API shape
