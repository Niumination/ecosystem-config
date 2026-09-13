---
name: safe-branch-refactor
description: Safe refactor by duplicating branch and preserving UI.
---

# Safe Branch Refactor

## Trigger
User asks to:
- "duplikat branch X ke Y"
- "bedah sumber non-SAPA"
- "hapus sumber X, sisakan hanya Y"
- "preserve UI, ganti hanya data source"

## Core Principle
**Duplicate first, modify second.** Never start modifying before the duplicate is verified identical to source.

## Workflow

### 1. Full Duplicate
```bash
git checkout source-branch
git archive --format=tar --prefix=repo/ HEAD | tar -x -C /tmp
mv /tmp/repo target-repo
cd target-repo
git init && git add -A && git commit -m "chore: duplicate from source-branch"
```

### 2. Verify Identical
```bash
# Compare file counts, structure, and build
find src -type f | wc -l
npx next build
```

### 3. Preserve UI, Modify Data Sources
- **DO NOT delete** pages, components, layouts, sidebar, navigation
- **DO NOT delete** route folders even if their data source is removed
- **DO** stub API endpoints to return empty/placeholder data
- **DO** replace data-fetching logic in service files only
- **DO** keep all UI components intact; they may show empty states

### 4. Auth Gating → Stub Endpoints
Instead of deleting protected pages:
```typescript
// src/app/api/auth/me/route.ts
export async function GET() {
  return NextResponse.json({ authenticated: true, admin: { username: 'Publik', role: 'public' } });
}
```
This makes auth-dependent pages visible without modifying page code.

### 5. Patch Safely
- Always `git checkout -- <file>` to restore original before patching
- Use targeted `patch` or `sed` with unique anchors
- Verify patch landed correctly before building
- Never bulk-replace strings across multiple files without inspection

### 6. Verify After Each Change
```bash
npx tsc --noEmit
npx next build
# Then manually test in browser
```

## Pitfalls

| Pitfall | Consequence | Prevention |
|---------|-------------|------------|
| Deleting route folders | 404s break navigation | Keep folders, stub routes |
| Removing auth UI before stubbing endpoints | Pages crash on fetch errors | Stub endpoints first, then clean UI |
| Bulk string replacement across files | Syntax errors, broken imports | Inspect each file, patch surgically |
| Starting modifications before verifying duplicate | Working on wrong base state | Always verify identical first |
| Assuming remote `origin` works | Push fails silently | Configure local `latest` mirror first |

## Git Remote Pattern for Local Push

When GitHub credentials are unavailable, create a local mirror remote:
```bash
mkdir -p ~/downloads-extracted/sapa-ai-latest
cd ~/downloads-extracted/sapa-ai-latest
git init
git config receive.denyCurrentBranch ignore
git remote add origin /path/to/working-repo
cd /path/to/working-repo
git remote add latest ~/downloads-extracted/sapa-ai-latest
git push latest main
```

## References
- `references/sapa-ai-refactor-2026-09-02.md` — Session notes: preserving UI while stripping non-SAPA sources from `sapa-ai`