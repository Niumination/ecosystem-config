---
name: ultrathink
description: "Force deep architectural and system-level reasoning before writing code — channels a master craftsman who thinks in trade-offs, invariants, and long-term maintainability rather than rushing to implementation."
version: 1.0.0
author: HaydenLundin/ultrathink + Niumination
source: HaydenLundin/ultrathink (GitHub)
tags: [software-development, craftsmanship, architecture, reasoning]
platforms: [macos, linux]
---

# Ultrathink — Craftsmanship & Deep Reasoning

## Purpose
Force deep architectural and system-level reasoning **before** writing code. Channels a master craftsman who thinks in trade-offs, invariants, and long-term maintainability rather than rushing to implementation. This is the opposite of "move fast and break things" — it's "think hard, then move precisely."

## When to Use
- Before starting a new feature, module, or system.
- When the problem is complex or poorly understood.
- When an existing solution feels "hacked together" and needs rethinking.
- When you need to evaluate trade-offs between multiple approaches.
- **As a counterbalance to overly-agile/YAGNI approaches** — use when ponytail would be too minimal.

## Required Context
- The problem statement or requirements.
- Existing architecture and constraints (stack, performance targets, team size).
- Any prior attempts or failed approaches.

## Inputs
- The problem to solve.
- Constraints: language, framework, deployment target, performance budgets, team context.

## Outputs
- **Architecture decision record**: chosen approach with rationale, rejected alternatives, and reasoning.
- **Invariants identified**: what must always be true for the system to work correctly.
- **Trade-off map**: what was sacrificed and why.
- **Implementation boundary**: what parts are well-understood vs what needs prototyping.

## Step-by-Step Workflow

### Phase 1: Problem Deepening (Don't Start Here)
1. **Restate the problem in your own words.** If you can't explain it simply, you don't understand it yet.
2. **Identify the actual constraint.** Is it performance? Maintainability? Time-to-market? Developer experience? The real constraint dictates the trade-offs.
3. **Question every assumption.** What if the data doesn't fit in memory? What if the API changes? What if scale is 10x what was stated?
4. **Find the invariants.** What must remain true at all times? These are the things you can't trade away.

### Phase 2: Solution Exploration
5. **Generate at least 2-3 distinct approaches.** If you only have one approach, you haven't thought hard enough.
6. **For each approach, identify:**
   - Complexity (implementation + maintenance)
   - Performance characteristics
   - Failure modes under stress
   - How it affects future changes
7. **Compare trade-offs explicitly.** Use a table or decision matrix. Don't hand-wave.

### Phase 3: Commitment
8. **Choose the approach that optimizes for the actual constraint** — not the most elegant or the most fun, but the one that best serves the invariant.
9. **Document why the alternatives were rejected.** This prevents re-debating later.
10. **Define the implementation boundary clearly:** what parts are well-understood (go ahead and build) vs what needs prototyping first (build a spike to reduce risk).

## Decision Matrix Template
```
| Criteria              | Approach A | Approach B | Approach C |
|-----------------------|:----------:|:----------:|:----------:|
| Implementation time   |    2d      |    5d      |    1d      |
| Maintenance burden    |   low      |   high     |   medium   |
| Performance (p99)     |   10ms     |   5ms      |   50ms     |
| Extensibility         |   high     |   medium   |   low      |
| Risk (unknowns)       |   low      |   high     |   medium   |
| **Verdict**           |   ✅      |   ❌       |   ❌       |
```

## Relationship with Ponytail
Ultrathink and ponytail serve **different phases of the same workflow:**

| Phase | Skill | Purpose |
|-------|-------|---------|
| **Before coding** | Ultrathink | Think deep, explore trade-offs, decide the right approach |
| **During coding** | Ponytail | Write the *minimum* code that realizes the chosen approach |

**Rule of thumb:** Ultrathink for *what* and *why*; ponytail for *how much*. They are complementary, not conflicting.

## Best Practices
- Time-box deep thinking: 15-30 min for most decisions, up to 2h for critical architecture.
- Write the decision down — an unwritten decision is a decision that will be re-debated.
- Distinguish reversible decisions (quick, try something) from irreversible ones (think harder).
- Don't use ultrathink as an excuse for analysis paralysis — if the decision is reversible, just pick one and move on.

## Common Mistakes
- **Analysis paralysis:** Spending hours on a decision that takes 5 minutes to implement and 2 minutes to change. Match the depth of thinking to the cost of being wrong.
- **Premature optimization:** Optimizing for scale that never comes. If scale isn't the actual constraint, don't optimize for it.
- **Ignoring context:** The same technical decision can be right or wrong depending on team skill, timeline, and business context.

## Token Optimization Notes
- Output should be concise — a decision record of 200-500 words is usually sufficient.
- Focus on the *reasoning*, not the output format. A good decision in a messy doc beats a bad decision in a beautiful doc.

## Dependencies
- None, but works best when there's clear problem definition.

## Related Skills
- `software-development/ponytail-core/SKILL.md` — use after ultrathink for minimal implementation
- `software-development/ponytail-audit/SKILL.md` — audit existing code before applying ultrathink
