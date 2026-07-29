---
name: premortem
description: "Assume a project or plan has already failed, then work backward to identify the most likely causes before committing to it. Catches failure modes that forward-looking planning misses."
version: 1.0.0
author: sisi-tarak/claude-skills + Niumination
source: sisi-tarak/claude-skills
tags: [software-development, reasoning, risk, planning]
platforms: [macos, linux]
---

# Premortem — Failure Pre-Mortem Analysis

## Purpose
Catch failure modes that forward-looking planning misses, by reasoning backward from an assumed failure instead of forward from an assumed success.

## When to Use
- Before committing significant time/resources to a plan.
- Before a launch, release, or irreversible decision.
- As a structured complement to `redteam` — premortem assumes failure and asks why; redteam attacks the plan directly.

## Required Context
- The plan in enough detail to imagine a concrete failed outcome, not just an abstract one.

## Inputs
- The plan or project under review.

## Outputs
- A ranked list of plausible failure causes, each with an early warning sign that would have indicated it was happening, and a mitigation.

## Step-by-Step Workflow
1. **State the failure as fact**, not hypothetical: "It's six months from now and this failed. What happened?" — this framing produces more specific answers than "what could go wrong?"
2. **Generate causes independently across categories** — technical, market/user, resourcing, timing, external/competitive — so the exercise doesn't fixate on one type of risk.
3. **For each cause, ask what the earliest observable warning sign would have been** — this turns abstract risks into concrete things to monitor.
4. **Rank by combination of likelihood and damage**, not either alone.
5. **Attach a mitigation or explicit monitoring plan** to each of the top causes — an unranked list of scary scenarios isn't actionable on its own.

## Best Practices
- Do this before the plan is finalized, not after — its value is in changing the plan, not documenting regret later.
- Push past the first few obvious causes; the third or fourth generated cause is often more informative than the first.
- Pair with `redteam` for full coverage — premortem surfaces causes, redteam stress-tests specific claims.
- Pair with `tripwire` to identify which one risk to watch most closely after the analysis.

## Common Mistakes
- Treating it as a one-time brainstorm disconnected from actually changing the plan afterward.
- Generating only technical failure causes and skipping market, timing, or resourcing failure modes.
- Skipping the "early warning sign" step, which is what makes the exercise actionable rather than just anxious.

## Token Optimization Notes
- Cap the initial brainstorm (e.g. 8-10 causes) before ranking, rather than exhaustively generating every conceivable failure mode.

## Dependencies
- None.

## Related Skills
- `security/redteam/SKILL.md`
- `software-development/tripwire/SKILL.md`
