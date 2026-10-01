---
name: earning-opportunity-feasibility
description: "Use when the user asks what can make money from their setup."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos, linux, windows]
metadata:
  hermes:
    tags: [monetization, feasibility, revenue, opportunity, due-diligence]
    category: ecosystem
    related_skills: [ecosystem-tool-adoption, content-monetize]
---

# Earning Opportunity Feasibility

The user asks "what can make money from my setup" or names a specific platform
and asks whether it pays. The failure mode is recommending a platform that
pays well but that the user **cannot actually run** — wrong prerequisite, wrong
country, wrong license, wrong distribution channel. The fix is to inventory
verified local state FIRST, then gate every candidate on hard prerequisites,
then rank by realistic payoff rather than headline rate.

Procedure order matters: gather facts before forming any view. A recommendation
formed before the inventory is a guess, and the user cannot tell the difference
between a confident guess and a verified answer.

## Procedure

### ① Inventory verified local state

Never assume a prerequisite is present. Probe it.

```bash
# Public footprint — the number that decides whether audience-based plays work
gh api user --jq '.login, .public_repos, .followers'
gh api "search/repositories?q=user:<login>" --jq '.total_count'

# Required local software for the candidate platform
command -v <cli> 2>/dev/null || echo "absent"
ls -d /Applications/<Editor>.app 2>/dev/null || echo "absent"

# Existing assets that could be the product
ls -d services/*/ tools/*/ 2>/dev/null
```

Report the counts as measured. "88 repos, 2 followers" is a decisive fact for
any play that depends on traffic; state it plainly rather than burying it.

### ② Gate each candidate on hard prerequisites

A candidate is viable only if ALL gates pass. Record each as pass/fail with the
command that proved it.

| Gate | How to prove it |
|---|---|
| Required software installed | `command -v` / `ls /Applications` |
| Geography permits payout | extract the platform's own country list; do not assume |
| Payout rail reachable from user's country | check the processor's supported-country list |
| Minimum threshold reachable | read the threshold and the per-unit rate together |
| License permits the intended use | read LICENSE, classify usage |
| Distribution channel actually works | confirm the platform is listed where the user operates |
| Employer/policy approval | if the device or data is work-owned, flag the consent clause |

**Geography gate is the most commonly missed.** A platform can support a
country in general terms while excluding it from the specific payout rail it
uses. Read the payout section specifically, not the availability blurb.

**License gate, concretely:** "not open source" licenses split into
use-anywhere (fine internally) and offer-to-third-parties (forbidden). A tool
that exposes a public tunnel for a municipal service is on the offer side, not
the use side. Name the boundary explicitly instead of saying "check the
license".

### ③ Prove the money actually reaches the user

Do not stop at "the platform pays". Verify the full path:

- payout processor and whether the user's country is on ITS list
- minimum threshold amount
- payout cadence
- the earning unit and what actually qualifies (continuous dwell time, caps,
  human-initiated only, no background accrual)
- whether the user's existing tools can even generate the qualifying activity

That last point is the one that decides most "looks viable" platforms. If the
unit of earning is time spent inside a specific product, and that product is not
installed and not the tool the user works in, the payout rate is irrelevant.

### ④ Audit before recommending install

For anything that modifies the machine — extensions, agents, CLIs, launch
daemons:

- Read the install script or manifest before running it.
- Confirm it verifies a checksum or signature.
- Confirm no hardcoded privilege escalation.
- Enumerate the persistent system changes: trust stores, `/etc/hosts`, port
  bindings, login items, launchd agents. State which survive uninstall.
- Check the terms for a clause requiring employer authorization, and for a clause
  on account/device pooling that would block a team trying to share one account.

Recommend the narrowest mode that works (a "private" mode over a "boosted"
one), and name the residual risk of each.

### ⑤ Rank by realistic payoff, and say no out loud

Order by probability × payoff × time-to-first-dollar, not by headline rate.
Then state plainly which options are not worth it and why. A short honest list
beats a long speculative one.

Say the disqualifying fact early: absent software, a country exclusion, a
threshold that outruns the user's activity, a pooling prohibition. Do not lead
with the payout figure and bury the blocker.

## Pitfalls

- **Recommending before inventorying.** A rate without a prerequisite check is
  a guess dressed as advice. Inventory first, always.
- **Skipping the payout rail when checking geography.** Platform availability
  and payout availability are different lists; only the second one decides
  whether money arrives.
- **Treating a "not open source" license as a blocker.** Classify the actual
  use: internal use is usually fine, offering it as a service usually is not.
  Say which side the user's intended use falls on.
- **Auditing the tool after recommending it.** Read the install script and the
  persistent-change list BEFORE saying "install this", not after.
- **Presenting options with equal weight.** When one option is a few weeks of
  work and another cannot work at all, rank them. Equal weighting hides the
  decision.
- **Quoting a pay rate without the qualifying condition.** "$X per impression"
  is meaningless without the dwell time, the caps, and whether background
  activity counts.
- **Assuming the user's tool is the one the platform instruments.** Many earning
  surfaces hook a specific editor or CLI. If the user works elsewhere, say so.
- **Over-researching a target the user already dismissed.** Once they say
  ignore it, drop it and search for the next class, don't re-litigate.

## Verification

Before delivering, confirm each claim about a platform traces to a retrieved
page, and each claim about the machine traces to a command that was run. Mark
anything unverified as `UNCHECKED` with the reason. Attach the commands under
a `## Bukti` section — the user checks infrastructure claims, not prose.

For multi-source research, `research/grounded-citations` owns the citation
ledger; use it when the deliverable is a written report rather than a chat
answer.
