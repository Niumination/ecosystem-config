---
name: egm-bootstrap
description: 'Use when onboarding new repo. Generates bottom-up docs.'
category: ecosystem
---
# EGM Bootstrap

Adopted from Google's EGM (Apache 2.0). Recursive bottom-up codebase documentation generator.

## Purpose
Generate documentation for a codebase from the bottom up, starting with leaf modules and building to system-level overviews. Produces living specification artifacts.

## When to Use
- Onboarding a new repository with no documentation
- After significant refactoring that invalidated existing docs
- When AI agents need structured codebase context

## Process

### Phase 1: Leaf Module Analysis
For each leaf module (file with no internal dependencies):
1. Read the source code
2. Extract: purpose, exports, dependencies, side effects
3. Write a module-level doc: `docs/modules/<module>.md`

### Phase 2: Component Aggregation
For each component (group of related modules):
1. Read module docs from Phase 1
2. Synthesize: component purpose, interfaces, data flow
3. Write component doc: `docs/components/<component>.md`

### Phase 3: System Overview
1. Read all component docs
2. Synthesize: system architecture, entry points, data flow
3. Write system doc: `docs/architecture.md`

### Phase 4: Sentinel Block Upsert
For each documented file, add a sentinel block comment:
```
// EGM-DOC: <doc-path>
// Last updated: <date>
```

## Output
- `docs/modules/` — module-level docs
- `docs/components/` — component-level docs
- `docs/architecture.md` — system overview
- Sentinel blocks in source files

## Rules
- Do not fabricate information. Only document what exists.
- Mark unknowns as "UNCHECKED" or "TODO".
- Prefer reading code over inferring behavior.
- One module per pass. Do not batch.
