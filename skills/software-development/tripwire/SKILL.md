---
name: tripwire
description: "Identify the single most critical risk that could derail a project — forcing prioritization down to one thing when a full risk analysis has produced too many findings to act on all at once."
version: 1.0.0
author: sisi-tarak/claude-skills + Niumination
source: sisi-tarak/claude-skills
tags: [software-development, reasoning, risk, prioritization]
platforms: [macos, linux]
---

# Tripwire — Single-Risk Prioritization

## Purpose
Force prioritization down to one thing, when a full risk analysis (`premortem`, `redteam`) has already produced a list that's too long to act on uniformly.

## When to Use
- Right after scoping a project, before work begins.
- After a `premortem` or `redteam` pass has produced multiple findings and they need to be triaged to what matters most.
- When resources only allow monitoring/mitigating one risk closely.

## Required Context
- Either a prior risk list (from premortem/redteam) or enough project detail to reason about risk directly.

## Inputs
- The project or plan, and any prior risk-analysis output.

## Outputs
- A single named risk, stated precisely, with the specific signal that would indicate it's materializing and what to do the moment that signal appears.

## Step-by-Step Workflow
1. **If a risk list already exists** (from premortem/redteam), evaluate each by: "if this happens, does the whole project fail, or does it just get worse?" — the tripwire is the one where the answer is "fails."
2. **If no prior list exists**, ask directly: what's the one assumption that, if wrong, invalidates everything else in this plan?
3. **State it precisely** — not "the market might not want this" but "if fewer than X% of pilot users convert by [date], the core assumption is wrong."
4. **Define the trigger signal concretely** — a number, a date, an observable event — not a vague feeling.
5. **Define the response in advance**, before the tripwire is hit — deciding what to do in the moment, under pressure, produces worse decisions than deciding calmly ahead of time.

## Best Practices
- Resist the urge to name more than one tripwire — the entire value of this pattern is forcing a single, clear priority.
- Make the trigger measurable, not subjective, so there's no ambiguity about whether it's been hit.
- Revisit the tripwire as the project evolves — the single biggest risk early on often isn't the same one later.

## Common Mistakes
- Naming several "top risks" instead of committing to one — this just reproduces the original unprioritized list.
- Choosing the most interesting or discussable risk instead of the one that would actually be most damaging.
- Defining the trigger vaguely enough that it's unclear in the moment whether it's actually been tripped.

## Token Optimization Notes
- This pattern is meant to be fast — a few sentences of output, not an essay. If the output is long, the prioritization step didn't actually happen.

## Dependencies
- Works best after `premortem` or `redteam`, but can be used standalone.

## Related Skills
- `software-development/premortem/SKILL.md`
- `security/redteam/SKILL.md`
