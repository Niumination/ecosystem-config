---
name: bridge-migration
description: "Migrate bridge modules lost in refactor to a new runtime."
tags: [migration, bridge, refactor, recovery, typescript, python]
---

# Bridge Migration

## Trigger
- Import errors for deleted modules (`ModuleNotFoundError`)
- Refactor removed bridge logic; new stack lacks equivalent
- Need to reimplement bridge in another language, preserving behavior

## Workflow

### Step 1: Recover Original Logic
1. Find last commit with the module: `git log --all --oneline -- <path>`
2. Extract: `git show <commit>^:<path> > /tmp/original.py`
3. Map public functions and behavior (inputs, outputs, side effects)

### Step 2: Reimplement 1:1 in Target Language
- Preserve function names where possible
- Preserve return types (dict shapes, status strings)
- Preserve error handling (retry, timeout, fallback)
- Add type signatures (TypeScript) for every public function

### Step 3: Add Supporting Infrastructure
- Database tables for new operations (e.g., `dispatches` for dispatch tracking)
- API routes that call new bridge functions
- CLI query handlers in database manager

### Step 4: Verify
- Build project (`npx next build` for TypeScript)
- Test every endpoint with valid and invalid inputs
- Check database state after operations
- Confirm error paths return proper HTTP status codes

## Real Example: Niu-MissionControl (2026-09-07)

**Problem:** `modules/hermes_bridge.py` and `swarm/` deleted during apex-ui refactor. `server.py` crashed with `ModuleNotFoundError`.

**Solution:** Reimplemented bridge in TypeScript at `lib/bridge.ts`:
- `sendChat(text, topicId)` — sends to Telegram via `hermes send` CLI
- `runTerminal(cmd, timeout)` — allowlist-only shell execution
- `runAgentTurn(prompt, sessionId, model, provider, timeout)` — triggers agent via `hermes -z --resume`

**Supporting changes:**
- Added `dispatches` table to `init.sql`
- Added `add_dispatch`, `update_dispatch_status`, `get_dispatches` to `db_manager.py`
- Added API routes: `/api/mc/dispatch`, `/api/mc/dispatches`, `/api/mc/telegram/send`, `/api/mc/tasks/update`

## Pitfalls
- **Git history first:** Always check `git log --all -- <path>` before rewriting from scratch
- **Preserve return shapes:** Frontend depends on dict keys like `status`, `message`, `simulated`
- **Allowlist terminal:** Never allow `python`, `cat`, or shell metacharacters in `runTerminal`
- **Async execution:** Use `execFileAsync` in Node.js to avoid blocking the event loop
- **Hardcode paths:** Reference absolute CLI paths with `shutil.which` fallback

## Related
- `ecosystem-architecture-adoption` — adopting external architectures
- `surgical-refactor` — replace backend logic while keeping UI intact
- `finishing-a-development-branch` — completing migration work
