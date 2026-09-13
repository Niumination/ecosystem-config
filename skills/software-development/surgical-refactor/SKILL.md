---
name: surgical-refactor
description: Keep UI intact, replace only data/backend logic.
---

# Surgical Refactor

Refactor codebases while preserving UI/structure, replacing only data sources and backend logic.

## Core Principle
**Preserve UI/structure, replace only data/backend logic.** Never delete folders/routes that contain visible UI unless explicitly told to remove the feature entirely.

## When to Use
- User asks to "hapus fitur X" or "remove source Y"
- User asks to migrate an app to use only one data source
- User asks to "bedah" or refactor while keeping the UI intact

## Workflow

### 1. Duplicate First
Always duplicate the source repo/branch before destructive changes. User prefers:
```bash
cp -R source-repo target-repo
```

### 2. Audit Before Cutting
Inspect what imports/uses the target feature:
- Grep for imports, API routes, UI components
- Identify which files are purely UI vs purely backend vs mixed

### 3. Replace, Don't Delete UI
- **DO**: Stub out backend logic, replace API responses, neutralize auth checks
- **DON'T**: Delete UI components, pages, or routes unless explicitly told to remove the feature
- **DON'T**: Use placeholder messages like "Fitur tidak tersedia" unless explicitly requested

### 4. Handle Auth-Gated Features
When making previously-auth pages public:
- Remove middleware auth gate
- Remove auth state from layout/components
- Stub `/api/auth/*` endpoints to return public-authenticated responses
- Remove login redirects from pages (don't rewrite page content)
- Keep original page components intact

### 5. Guard Against Undefined Data
When replacing API responses, add fallbacks for all data accesses:
```typescript
const overview = data?.overview ?? { totalRecords: 0, totalOpd: 0, ... };
const items = [...(data.items ?? [])];
```

### 6. Verify Incrementally
After each change:
- Run `tsc --noEmit`
- Run `next build`
- Test in browser with hard refresh

## Common Pitfalls

1. **Deleting folders with UI** — causes broken layouts, missing routes
2. **Rewriting page components** — loses original UI structure and styling
3. **Removing API routes without stubs** — causes 404s from existing page fetches
4. **Breaking JSX when removing conditional auth blocks** — always verify balanced tags
5. **Forgetting sidebar/auth filters** — pages may be accessible but hidden from nav

## User Preferences
- User prefers **delete code** over **stub/hide/redirect** when removing features
- User gets frustrated when UI breaks after refactoring
- User wants to see all previously hidden pages after auth removal
- Always commit and push to `latest` mirror before GitHub push if credentials unavailable

## Verification Checklist
- [ ] `tsc --noEmit` passes with 0 errors
- [ ] `next build` succeeds
- [ ] All original routes/pages still exist
- [ ] No auth gates remain (middleware, redirects, auth fetches)
- [ ] All data accesses guarded against undefined
- [ ] No broken JSX/JS syntax from removals