# AGENTS.md Migration — v3.0 → v4.0 Case Study

> **Source session:** 29 Jul 2026 — Niumination ecosystem audit
> **Trigger:** Jcode audit found root AGENTS.md still referencing `Production/`, `projects/`, `PI/` (v3.0) while the real filesystem was `apps/`, `services/`, `desktop/`, `vault/` (v4.0).

## The Problem

The root DOX (AGENTS.md) had three categories of stale claims:

| Category | Example | Impact |
|----------|---------|--------|
| **Directory structure** | Claimed `Production/` (v3.0) vs reality `apps/` (v4.0) | Every path in project catalog wrong |
| **DOX chain claims** | Claimed `brain/AGENTS.md` exists — it didn't | Agent navigates to non-existent file |
| **Project paths** | `projects/cc-acehtengah/` → actually `services/cc-acehtengah/` | Build pipelines target wrong dir |

## Detection Method

```bash
# Phase 1: Verify ROOT structure claims vs reality
ls -d /Users/zaryu/Desktop/Niumination/*/ 2>/dev/null
# Does DOX say Production/?  Reality says apps/
# Does DOX say projects/?    Reality says services/ sites/ desktop/

# Phase 2: Verify DOX Chain — every claimed AGENTS.md
claims=(
  "apps/Niu-LKH/AGENTS.md"
  "apps/PemdiAcehTengah/AGENTS.md"
  "services/niu-cast/AGENTS.md"
  "brain/AGENTS.md"
  "desktop/flame-ade/AGENTS.md"
  "agents/orchestrator/AGENTS.md"
)
for claim in "${claims[@]}"; do
  test -f "/Users/zaryu/Desktop/Niumination/$claim" && echo "✅ $claim" || echo "❌ $claim"
done

# Phase 3: Verify app/services/etc directory contents match catalog
for dir in apps services sites desktop agents labs sandbox; do
  echo "=== $dir/ ==="
  ls -d "/Users/zaryu/Desktop/Niumination/$dir/"*/
done
```

## What Was Found

### ✅ Verified (18 of 19 claimed)
- `apps/Niu-LKH/AGENTS.md` — ✅ exists
- `apps/PemdiAcehTengah/AGENTS.md` — ✅ + data/ + components/ sub-DOX
- `apps/niu-dash/AGENTS.md` — ✅
- `apps/kune-ya.com/AGENTS.md` — ✅
- `apps/niu-vermilion/AGENTS.md` — ✅
- `services/cc-acehtengah/AGENTS.md` — ✅ (DOX claimed `projects/cc-acehtengah/`)
- `services/niu-cast/AGENTS.md` — ✅
- `labs/niumination-workspace/AGENTS.md` — ✅
- `desktop/didong-code/AGENTS.md` — ✅
- `desktop/flame-ade/AGENTS.md` — ✅
- `desktop/x-downloader/AGENTS.md` — ✅
- `agents/Ultra/AGENTS.md` — ✅
- `agents/profile/AGENTS.md` — ✅
- `agents/characters/*/AGENTS.md` (4) — ✅ all

### ❌ Not Found (1)
- `agents/orchestrator/AGENTS.md` — ❌ never created

### ⚠️ Stale Claims Removed
| Removed | Why |
|---------|-----|
| `brain/AGENTS.md` | Never existed — removed from chain |
| `brain/projects/*/AGENTS.md` (10 files) | Did not exist at verified paths |
| `services/niu-cast/` listed under `projects/` | Wrong directory — moved to `services/` in v4.0 |

## Systematic Fix Applied

### Step 1: Bump DOX Version
```
DOX Version: 3.0 —→ 4.0
```

### Step 2: Fix Directory Structure Section
Replace the **entire** `Directory Structure` tree — don't patch individual lines:
- `Production/` → `apps/` (with correct 11 sub-projects)
- `projects/` → distributed to `services/`, `sites/`, `desktop/`, `labs/`, `sandbox/`
- `PI/` → `vault/`
- `rekap/` → `dotfiles/`
- Add `skills/` as new section (PLANNED / ACTIVE)

### Step 3: Fix Project Catalog Paths
Every row in the 3 Project Catalog tables:
```diff
-| PemdiAcehTengah | `Production/PemdiAcehTengah/`
+| PemdiAcehTengah | `apps/PemdiAcehTengah/`
```
- Flame-ADE: `projects/flame-ade/` → `desktop/flame-ade/`
- cc-acehtengah: `projects/cc-acehtengah/` → `services/cc-acehtengah/`
- x-downloader: `projects/x-downloader/` → `desktop/x-downloader/`
- Niu-MissionControl: `projects/niu-mission-control/` → `services/niu-mission-control/`
- LatticeSend: `projects/latticesend/` → `services/latticesend/`
- dll (total 15+ path corrections)

### Step 4: Fix DOX Chain Rules
Replace the flat list with verified-only entries. Mark missing ones explicitly:
```diff
-  ├── brain/AGENTS.md                           ✅
+  ├── services/cc-acehtengah/AGENTS.md          ✅
-  └── brain/projects/*/AGENTS.md (10 files)     ✅
+  ├── agents/orchestrator/AGENTS.md              ❌ (belum ada)
+  └── docs/skill-ecosystem-guide.md             ✅
```

### Step 5: Update Quick Links
- Remove stale references (`brain/AGENTS.md`, `PI/`)
- Add new references (`vault/`, `skills/`)

### Step 6: Bump Footer Version + Commit
```
Diperbarui: 29 Jul 2026 — v4.0
```

## Key Lesson

**DOX is always stale** — it's a snapshot of intent, not reality. Before any content pipeline, run Phase 1-3 above. The discrepancy between v3.0 claims and v4.0 reality was the single biggest source of wasted work in this ecosystem.

When the DOX says "40+ local projects" but only ~20 exist at the claimed paths, that's not a bug — it's data. Document the discrepancy, fix the DOX, then proceed with the pipeline.
