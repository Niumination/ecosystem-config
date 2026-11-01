---
name: egm-drift-report
description: 'Use when checking spec vs code drift. Scans for divergence.'
category: ecosystem
---
# EGM Drift Report

Adopted from Google's EGM (Apache 2.0). Agent workflow comparing specs and READMEs to code.

## Purpose
Detect divergence between checked-in design documents and live codebase. Run periodically (e.g., weekly) to catch documentation drift.

## When to Use
- After significant code changes
- Before onboarding new team members
- Weekly maintenance check
- Before major releases

## Process

### Step 1: Collect specs
Find all design documents in `docs/designs/`, `docs/registry/`, and `README.md`.

### Step 2: Extract claims
From each spec, extract verifiable claims:
- File paths referenced
- Function/class names mentioned
- API endpoints described
- Configuration values stated
- Architecture descriptions

### Step 3: Verify against code
For each claim, verify against live codebase:
- Does the file path exist?
- Does the function/class exist?
- Does the API endpoint exist?
- Are configuration values accurate?
- Does the architecture match?

### Step 4: Generate report
Output a drift report with:
- **Matched**: claims verified against code
- **Drifted**: claims that no longer match (with diff)
- **Orphaned**: code not documented
- **Missing**: documented items not found in code

## Output Format
```
## Drift Report — <date>

### Matched: N claims
### Drifted: N claims
  - <file>: <claim> → <actual>
### Orphaned: N items
  - <file>: <undocumented code>
### Missing: N items
  - <doc>: <referenced but not found>
```

## Rules
- Only report factual discrepancies, not style issues
- Include file:line references for all findings
- Prioritize Blocker-level drift (wrong API, missing files)
