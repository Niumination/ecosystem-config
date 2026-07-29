---
name: systematic-debugging
description: "4-phase root cause debugging: understand bugs before fixing."
version: 1.5.0
author: Hermes Agent (adapted from obra/superpowers)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [debugging, troubleshooting, problem-solving, root-cause, investigation]
    related_skills: [test-driven-development, writing-plans, subagent-driven-development]
---

# Systematic Debugging

## Overview

Random fixes waste time and create new bugs. Quick patches mask underlying issues.

**Core principle:** ALWAYS find root cause before attempting fixes. Symptom fixes are failure.

**Violating the letter of this process is violating the spirit of debugging.**

## The Iron Law

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

If you haven't completed Phase 1, you cannot propose fixes.

## When to Use

Use for ANY technical issue:
- Test failures
- Bugs in production
- Unexpected behavior
- Performance problems
- Build failures
- Integration issues

**Use this ESPECIALLY when:**
- Under time pressure (emergencies make guessing tempting)
- "Just one quick fix" seems obvious
- You've already tried multiple fixes
- Previous fix didn't work
- You don't fully understand the issue

**Don't skip when:**
- Issue seems simple (simple bugs have root causes too)
- You're in a hurry (rushing guarantees rework)
- Someone wants it fixed NOW (systematic is faster than thrashing)

## The Four Phases

You MUST complete each phase before proceeding to the next.

---

## Phase 1: Root Cause Investigation

**BEFORE attempting ANY fix:**

### 1. Read Error Messages Carefully

- Don't skip past errors or warnings
- They often contain the exact solution
- Read stack traces completely
- Note line numbers, file paths, error codes

**Action:** Use `read_file` on the relevant source files. Use `search_files` to find the error string in the codebase.

### 2. Reproduce Consistently

- Can you trigger it reliably?
- What are the exact steps?
- Does it happen every time?
- If not reproducible → gather more data, don't guess

**Action:** Use the `terminal` tool to run the failing test or trigger the bug:

```bash
# Run specific failing test
pytest tests/test_module.py::test_name -v

# Run with verbose output
pytest tests/test_module.py -v --tb=long
```

### 3. Check Recent Changes

- What changed that could cause this?
- Git diff, recent commits
- New dependencies, config changes

**Action:**

```bash
# Recent commits
git log --oneline -10

# Uncommitted changes
git diff

# Changes in specific file
git log -p --follow src/problematic_file.py | head -100
```

### 4. Gather Evidence in Multi-Component Systems

**WHEN system has multiple components (API → service → database, CI → build → deploy):**

**BEFORE proposing fixes, add diagnostic instrumentation:**

For EACH component boundary:
- Log what data enters the component
- Log what data exits the component
- Verify environment/config propagation
- Check state at each layer

Run once to gather evidence showing WHERE it breaks.
THEN analyze evidence to identify the failing component.
THEN investigate that specific component.

### 5. Trace Data Flow

**WHEN error is deep in the call stack:**

- Where does the bad value originate?
- What called this function with the bad value?
- Keep tracing upstream until you find the source
- Fix at the source, not at the symptom

**For data persistence bugs ("data gone after refresh"):** Use the two-direction trace:
1. **Forward** from user action through every storage target (localStorage → server API)
2. **Backward** from page load through every data source (localStorage read → server fetch)

See `references/persistence-chain-debugging.md` for a concrete worked example on a GitHub Pages dashboard.

**Action:** Use `search_files` to trace references:

```python
# Find where the function is called
search_files("function_name(", path="src/", file_glob="*.py")

# Find where the variable is set
search_files("variable_name\\s*=", path="src/", file_glob="*.py")
```

### Phase 1 Completion Checklist

- [ ] Error messages fully read and understood
- [ ] Issue reproduced consistently
- [ ] Recent changes identified and reviewed
- [ ] Evidence gathered (logs, state, data flow)
- [ ] Problem isolated to specific component/code
- [ ] Root cause hypothesis formed

**STOP:** Do not proceed to Phase 2 until you understand WHY it's happening.

### Phase 1 Special Case: Recurring Bug After "Fix"

When the user reports a bug that **was already fixed** in a prior session has returned:

1. **Assume the previous fix was incomplete** — recurrence IS evidence it addressed symptoms, not all root causes
2. **Do NOT re-verify the old fix first** — the user is telling you something changed or the fix missed a path
3. **Investigate as a first-time report** — fresh reproduction, fresh evidence gathering
4. **Distinguish "same symptom" from "same root cause"** — the user sees the same failure (gateway dead after lock screen) but the underlying cause may differ (disk sleep vs system sleep vs USB controller power-down)
5. **Check what changed** between when the fix seemed to work and when the bug returned — this is the most valuable diagnostic data
6. **Report findings before proposing another fix** — especially important when the previous fix took significant effort
7. **Don't skip Phase 1** because "this looks like the same issue from last time" — the recurrence demands fresh eyes

**Common scenario:** Multiple masking fixes (adding caffeinate, disabling disksleep, removing --replace) each addressed one mechanism but missed the underlying architecture problem (USB flash drive as HERMES_HOME). The 3rd recurrence is the signal to question the architecture, not patch another symptom.

---

### Phase 1 Critical Rule: Dilarang Fabrikasi Penyebab Tanpa Bukti

**This is the single most dangerous AI debugging failure mode.**

When you lack evidence for what went wrong, you will feel pressure to offer an explanation. RESIST IT. Fabricating a root cause — even one that sounds plausible — is worse than saying "I don't know" because:

1. It wastes the user's time chasing the wrong problem
2. It erodes trust when the real cause is found to be different
3. A wrong theory biases all subsequent data interpretation

**Rules:**
- Never say "probably [cause X]" without checking log/data evidence first
- If logs show SIGTERM, don't assume the cause (sleep, crash, intentional kill) — check parent_pid, signal sender, and surrounding log context
- If you can't determine the cause, say: *"Saya tidak tahu penyebab pastinya. Data yang saya lihat menunjukkan [fact A] dan [fact B], tapi belum cukup untuk menyimpulkan."*
- Document what you DO know (facts, timestamps, log lines) and what you DON'T know (cause, trigger)
- An evidence-based statement like *"Signal SIGTERM dari parent_pid=1 (launchd)"* is a VERIFIABLE FACT. *"Karena Mac sleep"* is a GUESS unless confirmed by system sleep/wake log assertions

**Example dari sesi debugging nyata:**
- ❌ **Salah:** *"Gateway crash kemungkinan karena Mac sleep saat charger dilepas"* — fabrikasi tanpa bukti sleep di log
- ✅ **Benar:** *"Gateway menerima SIGTERM dari launchd (parent_pid=1). Interval restart ~2-3 menit. Belum diketahui penyebab SIGTERM — bisa crash, bisa intentional restart dari launchd. Perlu data tambahan (crash log, system sleep log) untuk konfirmasi."*

**Golden rule untuk AI agents:**
> State verifiable facts. Say "I don't know" for what you can't verify. Never fill gaps with plausible-sounding guesses.

---

## Phase 2: Pattern Analysis

**Find the pattern before fixing:**

### 1. Find Working Examples

- Locate similar working code in the same codebase
- What works that's similar to what's broken?

**Action:** Use `search_files` to find comparable patterns:

```python
search_files("similar_pattern", path="src/", file_glob="*.py")
```

### 2. Compare Against References

- If implementing a pattern, read the reference implementation COMPLETELY
- Don't skim — read every line
- Understand the pattern fully before applying

### 3. Identify Differences

- What's different between working and broken?
- List every difference, however small
- Don't assume "that can't matter"

### 4. Understand Dependencies

- What other components does this need?
- What settings, config, environment?
- What assumptions does it make?

---

## Phase 3: Hypothesis and Testing

**Scientific method:**

### 1. Form a Single Hypothesis

- State clearly: "I think X is the root cause because Y"
- Write it down
- Be specific, not vague

### 2. Test Minimally

- Make the SMALLEST possible change to test the hypothesis
- One variable at a time
- Don't fix multiple things at once

### 3. Verify Before Continuing

- Did it work? → Phase 4
- Didn't work? → Form NEW hypothesis
- DON'T add more fixes on top

### 4. When You Don't Know

- Say "I don't understand X"
- Don't pretend to know
- Ask the user for help
- Research more

---

## Phase 4: Implementation

**Fix the root cause, not the symptom:**

### 1. Create Failing Test Case

- Simplest possible reproduction
- Automated test if possible
- MUST have before fixing
- Use the `test-driven-development` skill

### 2. Implement Single Fix

- Address the root cause identified
- ONE change at a time
- No "while I'm here" improvements
- No bundled refactoring

### 3. Verify Fix

```bash
# Run the specific regression test
pytest tests/test_module.py::test_regression -v

# Run full suite — no regressions
pytest tests/ -q
```

### 4. If Fix Doesn't Work — The Rule of Three

- **STOP.**
- Count: How many fixes have you tried?
- If < 3: Return to Phase 1, re-analyze with new information
- **If ≥ 3: STOP and question the architecture (step 5 below)**
- DON'T attempt Fix #4 without architectural discussion

### 5. If 3+ Fixes Failed: Question Architecture

**Pattern indicating an architectural problem:**
- Each fix reveals new shared state/coupling in a different place
- Fixes require "massive refactoring" to implement
- Each fix creates new symptoms elsewhere

**STOP and question fundamentals:**
- Is this pattern fundamentally sound?
- Are we "sticking with it through sheer inertia"?
- Should we refactor the architecture vs. continue fixing symptoms?

**Discuss with the user before attempting more fixes.**

This is NOT a failed hypothesis — this is a wrong architecture.

---

## Operating Within the User's Project

When debugging an active production project (not your own code or a personal experiment), follow these rules to avoid wasting the user's trust and time.

### Never Make Unilateral Changes

- **Do NOT revert code** without asking the user first — even if your fix is broken. The user's repo state is their current working state; reverting changes a second variable without authorization.
- **Do NOT deploy untested fixes** to a production/shared environment.
- **Do NOT change scope** (skip a bug, add a feature, refactor unrelated code) without asking.
- If you're unsure whether a change will break things: **ask, don't guess**.

### Local Test Before Deploy

Every client-side fix must be verified locally before it touches the deployed environment:

1. **Serve the page locally** using a static HTTP server:
   ```bash
   cd project-dir
   python3 -m http.server 9876
   ```
2. **Load the page in a real browser** (Safari, Chrome) and check the console for JS errors
3. **For headless checks**, use curl to verify the page doesn't show known error patterns:
   ```bash
   curl -s http://localhost:9876/ | grep -c 'Render error'
   ```
4. **Only then** commit and push to production

For SPAs that rely on localStorage data, the bug may not reproduce in a clean browser. Options:
- Add a visible error div (`<div id="_niuErr" style="display:none"></div>`) with a JS error handler that writes to it
- Override `showToast` to also write error messages to the error div
- Ask the user to share their localStorage export

### Fix Iteration Loop

When the user says "it's still broken" or "you made it worse":

1. **Do NOT panic-revert** — ask what specifically is broken
2. **Reproduce locally** if possible (serve the page, check the error)
3. **Trace the EXACT error** — read error messages fully, don't guess
4. **Apply ONE fix** at a time (not a bundle)
5. **Verify locally** before committing
6. **Show the diff** to the user before deploying when in doubt
7. **Repeat** until the user confirms it works

If you've made multiple changes and things broke:
- **Stop applying more fixes immediately**
- Tell the user what you changed and offer to revert — let them choose
- Don't decide for them

### Golden Rule for Multi-Fix Sessions

```
ONE VARIABLE AT A TIME.
```

- One fix → one test → one verify → one commit
- If the fix breaks something, you know exactly which change caused it
- If you apply 3 fixes at once and it breaks, you cannot isolate which one is the problem
- If the user reports a new bug after your 3-fix commit, you have no idea which fix caused it

---

## Red Flags — STOP and Follow Process

If you catch yourself thinking:
- "Quick fix for now, investigate later"
- "Just try changing X and see if it works"
- "Add multiple changes, run tests"
- "Skip the test, I'll manually verify"
- "It's probably X, let me fix that"
- "I don't fully understand but this might work"
- "Pattern says X but I'll adapt it differently"
- "Here are the main problems: [lists fixes without investigation]"
- Proposing solutions before tracing data flow
- **"One more fix attempt" (when already tried 2+)**
- **Each fix reveals a new problem in a different place**
- **"I should revert this to clean state" (without asking the user first)**
- **"Let me just deploy and see if it fixes the issue"**
- **"The most likely cause is probably X" (based on intuition, not evidence)**
- **Inventing a root cause when you don't have enough data** — "I don't know" is always better than a fabricated explanation

**ALL of these mean: STOP. Return to Phase 1.**

**If 3+ fixes failed:** Question the architecture (Phase 4 step 5).

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Issue is simple, don't need process" | Simple issues have root causes too. Process is fast for simple bugs. |
| "Emergency, no time for process" | Systematic debugging is FASTER than guess-and-check thrashing. |
| "Just try this first, then investigate" | First fix sets the pattern. Do it right from the start. |
| "I'll write test after confirming fix works" | Untested fixes don't stick. Test first proves it. |
| "Multiple fixes at once saves time" | Can't isolate what worked. Causes new bugs. |
| "Reference too long, I'll adapt the pattern" | Partial understanding guarantees bugs. Read it completely. |
| "I see the problem, let me fix it" | Seeing symptoms ≠ understanding root cause. |
| "One more fix attempt" (after 2+ failures) | 3+ failures = architectural problem. Question the pattern, don't fix again. |
| "I'll revert it to the known-good state and retry" | You're changing two variables at once (revert + new fix). Ask the user first. |
| "Just deploy the debug version to production, I'll check it there" | Debug code on production is a last resort. Test locally first. |
| "I don't have the data but I can guess the cause" | Guessing without evidence is hallucination. Say "I don't know" and state only verifiable facts. |
| "Let me check the logs to see if my theory is right" | Backwards. Check logs FIRST to form a theory, not to retrofit evidence to a preconceived guess. |

## Quick Reference

| Phase | Key Activities | Success Criteria |
|-------|---------------|------------------|
| **1. Root Cause** | Read errors, reproduce, check changes, gather evidence, trace data flow | Understand WHAT and WHY |
| **2. Pattern** | Find working examples, compare, identify differences | Know what's different |
| **3. Hypothesis** | Form theory, test minimally, one variable at a time | Confirmed or new hypothesis |
| **4. Implementation** | Create regression test, fix root cause, verify | Bug resolved, all tests pass |

## Hermes Agent Integration

### Investigation Tools

Use these Hermes tools during Phase 1:

- **`search_files`** — Find error strings, trace function calls, locate patterns
- **`read_file`** — Read source code with line numbers for precise analysis
- **`terminal`** — Run tests, check git history, reproduce bugs
- **`web_search`/`web_extract`** — Research error messages, library docs

### Local Verification for Client-Side Projects

When debugging a web app (SPA, static site, dashboard):

1. **Start a local server** in the project directory:
   ```bash
   cd /Users/zaryu/Desktop/Niumination/projects/niu-dash
   python3 -m http.server 9876
   ```
2. **Open Safari/Chrome** to `http://localhost:9876/`
3. **Check console errors** — use AppleScript or the Develop menu to read errors
4. **Use curl/terminal** to grep for known error patterns:
   ```bash
   curl -s http://localhost:9876/ | grep -c 'Render error\|nonaktif'
   ```
5. **Add diagnostic divs** to the page for errors that only appear at runtime:
   ```javascript
   // Global error catcher
   var _niuErrors = [];
   function _niuLog(e) {
       var msg = e.message || e || '?';
       _niuErrors.push(msg);
       try {
           var d = document.getElementById('_niuErr');
           if(d) d.textContent = _niuErrors.join(' | ');
       } catch(_) {}
   }
   window.addEventListener('error', function(e) { _niuLog(e.error || e); });
   ```

### Electron / CDP Runtime Capture

For **Electron apps** (especially headless, CI, or container environments):
1. Launch with `--remote-debugging-port=9222`
2. Fetch `http://localhost:9222/json/list` to discover the page target
3. Open a WebSocket to the target's `webSocketDebuggerUrl`
4. Subscribe to `Console.enable`, `Runtime.enable`, `Log.enable`
5. Call `Page.reload` to capture startup errors from scratch
6. Collect events for ~8s, then print the structured output

**See `references/electron-cdp-runtime-capture.md`** for the full Node.js capture script, CDP event reference, pitfalls, and error-pattern classification.

### With delegate_task

For complex multi-component debugging, dispatch investigation subagents:

```python
delegate_task(
    goal="Investigate why [specific test/behavior] fails",
    context="""
    Follow systematic-debugging skill:
    1. Read the error message carefully
    2. Reproduce the issue
    3. Trace the data flow to find root cause
    4. Report findings — do NOT fix yet

    Error: [paste full error]
    File: [path to failing code]
    Test command: [exact command]
    """,
    toolsets=['terminal', 'file']
)
```

### With test-driven-development

When fixing bugs:
1. Write a test that reproduces the bug (RED)
2. Debug systematically to find root cause
3. Fix the root cause (GREEN)
4. The test proves the fix and prevents regression

## Real-World Impact

From debugging sessions:
- Systematic approach: 15-30 minutes to fix
- Random fixes approach: 2-3 hours of thrashing
- First-time fix rate: 95% vs 40%
- New bugs introduced: Near zero vs common

**No shortcuts. No guessing. Systematic always wins.**

## Reference Files

### Language/Environment-Specific Debugging References

- `references/python-debugpy.md` — Python debugger reference: pdb command cheat sheet, `breakpoint()` usage, `python -m pdb`, debugpy remote debugging (listen/attach/wait-for-client), `remote-pdb` for terminal-based agent debugging, post-mortem debugging, and Hermes-specific targets (gateway, tui_gateway, _SlashWorker, tests under xdist).
- `references/node-inspect-debugger.md` — Node.js V8 inspector reference: `node inspect` CLI REPL command cheat sheet, attaching to running processes via SIGUSR1, programmatic CDP with `chrome-remote-interface`, heap snapshots, CPU profiles, debugging Hermes ui-tui (Ink/tsx), and Vitest under the debugger.
- `references/electron-cdp-runtime-capture.md` — Scriptable Electron renderer error capture via Chrome DevTools Protocol: `--remote-debugging-port`, WebSocket subscription, `Console`/`Runtime`/`Log` event collection, headless/CI setup, and error-pattern classification (code vs environment).
- `references/debugging-hermes-tui-commands.md` — Cross-layer debugging for the three-tier Hermes TUI slash command architecture (Python COMMAND_REGISTRY → gateway JSON-RPC → Ink/TypeScript frontend). Covers missing autocomplete, CLI/TUI behavior mismatch, config persistence without live UI update, gateway silent drops, and the full add-a-command workflow from TypeScript handler through Python handler.
- `references/ci-debugging-github-actions.md` — Debugging failed GitHub Actions CI runs for Next.js projects: reading annotations from web_extract, reproducing CI commands locally, getting detailed ESLint JSON output, common Next.js CI failure patterns (duplicate imports, undefined components, missing hook deps), and the verify-and-push loop.

### Bug-Pattern References

- `references/css-component-regression-trace.md` — Tracing UI features that stopped rendering after version upgrades or zip-file overwrites: bisect-style git CSS presence checks, zip snapshot comparison, the triad check (component + import + CSS), and common regression mechanisms (CSS cleanup commits, zip-export mismatch).
- `references/prisma-adapter-silent-misconfig.md` — Prisma 7 `@prisma/adapter-pg` silent misconfiguration: schema option in wrong constructor argument, `DATABASE_URL` undefined in standalone tsx scripts, and the `P2021: TableDoesNotExist` false-positive bug class.
- `references/nextjs-turbopack-build-patterns.md` — Next.js Turbopack build error patterns: surfacing hidden errors via stderr redirect, Prisma 7 generated client import path (`.ts` output, no `.js`), NextAuth v5 beta route handler `{ handlers: { GET, POST } }` destructuring, lucide-react v1 brand icon removal, and RTK output compression.
- `references/persistence-chain-debugging.md` — Technique for debugging data-loss bugs in client-side apps with dual storage (localStorage + server API). Includes forward/backward trace patterns, CSP pitfalls, and a worked example on a GH Pages dashboard.
- `references/dom-render-cache-invalidation.md` — Pattern for debugging "disappearing content" and stale filter counts in single-page JS apps where DOM elements are cached across view switches. Covers cache invalidation, status filter leaks, sessionStorage-based tab-switch persistence, and defensive `Array.isArray` guards for stats aggregation.
- `references/docs-vs-filesystem-debugging.md` — Debugging bugs documented in project AGENTS.md that reference stale paths, wrong file extensions, or non-existent directories. Covers the "doc claims vs filesystem reality" mismatch pattern and bash subprocess variable propagation via temp files.
- `references/python-startup-silent-failure.md` — Debugging Python project startup scripts that silently exit: `pip install -q` hiding Rust build failures, `set -e` causing abrupt exit, and `pydantic-core` incompatibility with Python 3.14+ (removed CPython API symbols in `jiter`). Covers the full investigation chain from venv state check to version pin upgrade.
- `references/express-prisma-bug-patterns.md` — Four reproducible bug classes in Express+Prisma backends: JWT `TokenExpiredError` discrimination, Prisma `$transaction` atomicity for token rotation, third-party webhook signature tolerance across environments, and pre-condition validation for foreign key constraints. Each pattern has symptom, root cause, fix code, and prevention rule.
- `references/multi-surface-counter-staleness.md` — Debugging display count mismatches where sidebar, stat panel, and content list derive counts from different data sources (static PROJECTS vs. runtime flatProjects). Covers auto-categorization scope, investigation technique (identify all surfaces, trace data origins, map pipeline), and the unify-to-runtime fix pattern.
- `references/browser-js-runtime-debugging.md` — Browser JS runtime debugging: Playwright headless verification, Node.js mock-DOM error isolation, common pitfalls (`requestAnimationFrame` timestamp domain mismatch, CSP blocking, IndexedDB in private mode, service-worker cache stale), and a decision tree for deployed-page diagnostics.
- `references/terminal-input-masking-pitfall.md` — Terminal tool masks secret-like values (hex keys, tokens) in command-line arguments, sending `***` instead of the real value. Detection via Content-Length mismatch. Fix: write to temp file, read back separately.
- `references/patch-tool-boundary-pitfall.md` — Patch tool overremoval when old_string extends beyond intended boundaries, absorbing closing tags near end-of-file blocks. Detection signs, prevention (include sentinel context below the replacement), and recovery steps.
- `references/crash-loop-launchd-investigation.md` — Diagnosing macOS processes that restart repeatedly (crash loop via launchd). How to identify parent_pid=1 (launchd) signal, distinguish crash vs intentional restart vs sleep, and the critical rule against fabricating "Mac sleep" as a default cause without evidence.
- `references/innerhtml-script-execution.md` — `innerHTML` silently drops `<script>` blocks in SPA tab-switching: tabs render HTML but init functions never execute. Also covers the secondary pitfall where the SPA server's catch-all redirect blocks static file serving, plus how `translate_path` overrides affect file location. Fix: extract all JS to a globally-loaded file and add explicit server routes for static assets.
