---
name: redteam
description: "Stress-test a plan, project, or system by assuming an adversarial perspective and identifying specific attack surfaces, failure modes, and blind spots before they're exploited in production."
version: 1.1.0
author: Agentpedia (danielmiessler) + Niumination
source: Agentpedia / sisi-tarak/claude-skills
tags: [security, pentest, adversarial, testing]
platforms: [macos, linux]
---

# Redteam — Adversarial Security Testing

## Purpose
Assume an adversarial perspective to identify attack surfaces, failure modes, and blind spots that forward-looking planning misses. Unlike `premortem` (which assumes failure and works backward), redteam actively attacks the plan or system to find where it's weakest.

## When to Use
- Before deploying a system or service to production.
- Before committing to a high-risk architectural decision.
- When a plan has passed its initial review and needs a harder pass.
- As a complement to `premortem` — premortem surfaces causes; redteam stress-tests specific claims.

## Required Context
- The plan, architecture, or system in enough detail to reason about specific attack vectors.
- For security reviews: network topology, data flow, authentication model, dependency list.

## Inputs
- The plan, design doc, architecture diagram, or system under review.

## Outputs
- A prioritized list of vulnerabilities or attack surfaces, each with:
  1. **Attack vector** — how an adversary would exploit it
  2. **Impact** — what damage successful exploitation would cause
  3. **Likelihood** — low/medium/high
  4. **Mitigation** — what to change to close the vector

## Step-by-Step Workflow

1. **Assume the attacker's mindset.** You are not the builder; you are the adversary. Your goal is to break this system or invalidate this plan.

2. **Attack across dimensions, not just technical:**
   - **Security**: Auth bypass, injection, privilege escalation, data leak
   - **Logic**: Edge cases that break assumptions, race conditions, state confusion
   - **Scale**: What works at 100 users but fails at 100,000?
   - **Dependencies**: What if a key dependency goes down, changes license, or gets acquired?
   - **Timing**: What if the timeline slips by 2x? By 5x?
   - **Market**: What if user behavior is fundamentally different from assumed?
   - **Regulatory**: What if compliance requirements change or are stricter than assumed?

3. **For each vector found, state the specific evidence that would confirm it's real** — not "test it" but "if endpoint X returns 200 without a valid token, the auth bypass is confirmed."

4. **Rank severity by impact × likelihood**, not just one or the other.

5. **For each finding, provide a concrete mitigation** — not "fix auth" but "add token validation middleware to all `/api/*` routes."

## Critical vs Non-Critical
- **Critical**: Can cause data breach, service outage, financial loss, or reputational damage
- **High**: Significant impact but requires chained exploits or specific conditions
- **Medium**: Limited blast radius, requires privileged access or unlikely conditions
- **Low**: Informational, best practice gaps with limited exploitability

## Best Practices
- Be specific — "SQL injection in `/api/users?id=`" is actionable; "security issues" is not.
- Distinguish between theoretical vulnerabilities and ones that are practically exploitable.
- Include positive findings too — what's done well is worth documenting.
- Pair with `tripwire` after redteam to identify the single most critical finding to monitor.

## Common Mistakes
- Being too abstract — redteam findings must be concrete enough to test and fix.
- Focusing only on technical security and ignoring business logic, timing, or market risks.
- Generating a laundry list without prioritization — 20 findings with no rank are less useful than 5 ranked findings.

## Related Skills
- `security/redteam/SKILL.md` (this skill)
- `reasoning/premortem — `premortem` for complementary failure analysis
- `reasoning/tripwire — `tripwire` for single-risk prioritization after redteam

## Token Optimization Notes
- Cap initial brainstorm at 10-15 vectors, then rank and cull to top 5-7 for detailed writeup.
- Focus on *exploitable* vulnerabilities, not hypothetical "what ifs" with no practical attack path.
