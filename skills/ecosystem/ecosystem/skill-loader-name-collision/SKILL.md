---
name: skill-loader-name-collision
description: "Use when a skill name is reported ambiguous."
version: 1.0.0
author: Niumination (Afrizal Munthe)
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    tags: [skills, loader, collision, external_dirs, sync, manifest, curator]
    related_skills: [skill-bank-management, ecosystem-dox-maintenance, hermes-configuration]
---

# Skill Loader Name Collision

Every Niumination bank skill exists in BOTH `~/.hermes/skills/<rel>` (sync target) and
`~/Desktop/Niumination/skills/<rel>` (source of truth, declared in `config.yaml`
`skills.external_dirs`). Same relative path in both, so the loader refuses to guess.

## Symptom

```
Ambiguous skill name '<name>': 2 skills match across your local skills dir and external_dirs.
Refusing to guess — load one explicitly by its categorized path.
matches:
  /Users/zaryu/.hermes/skills/<rel>
  /Users/zaryu/Desktop/Niumination/skills/<rel>
```

## The loader's disambiguation hint does not work

The error says "pass the full relative path instead of the bare name." **That does not
resolve it** when both copies share the identical relative path. Every variant returns the
same error:

```
skill_view('<name>')          -> ambiguous
skill_view('<category>/<name>') -> ambiguous  (both copies are <category>/<name>)
skill_view('<rel>/SKILL.md')    -> ambiguous
```

**No argument reaches a bank skill.** Any bank skill is unloadable by name while the
duplication stands. Plan around it; do not retry the same call with more path variants.

## Diagnose without skill_view

`skill_view` is unavailable, so use tools that are not:

```bash
# Are the two copies identical, or did one drift?
shasum -a 256 ~/.hermes/skills/<rel>/SKILL.md ~/Desktop/Niumination/skills/<rel>/SKILL.md

# How widespread?
python3 - <<'PY'
import hashlib, pathlib
home = pathlib.Path("/Users/zaryu/.hermes/skills"); bank = pathlib.Path("/Users/zaryu/Desktop/Niumination/skills")
def idx(r):
    return {str(p.relative_to(r)): hashlib.sha256(p.read_bytes()).hexdigest()[:16]
            for p in r.rglob("SKILL.md")} if r.exists() else {}
t, b = idx(home), idx(bank)
both = sorted(set(t) & set(b))
print("target:", len(t), "bank:", len(b), "collide:", len(both),
      "drift:", len([k for k in both if t[k] != b[k]]))
PY
```

Identical content in both locations is the expected healthy state — the sync script copies
bank → target. Identical + colliding is not a content bug; the loader is being conservative
because it cannot prove the copies stay identical.

## Why the duplication exists

`skills/sync-to-agents.sh` copies bank → target and **never prunes**. `config.yaml` lists the
bank in `skills.external_dirs` so the agent reads from it directly. The same skill is
reachable twice, permanently — by design of those two settings working together.

## What this blocks

- `skill_view` on any bank skill, so no reading before editing
- `skill_manage patch` on any bank skill, which refuses without a prior read in the same turn
- background/curator curation of bank skills entirely

Path that does not need the loader: edit the file directly with `patch`/`write_file`, then
run `scripts/skill-manifest.py`, `skills/sync-to-agents.sh`, and
`python3 scripts/skill-manifest.py --check` to re-verify. That is how bank work is done today.

## Watch for the doubled path

A second defect shares this symptom class. `skill_manage create` with an explicit
`category` writes to `skills/<category>/<category>/<skill>/` when the tool already defaults to
that category, producing `ecosystem/ecosystem/<skill>/`. Guard after any skill creation: check
directory depth and confirm no `skills/*/*/` nesting that should be `skills/*/`.
