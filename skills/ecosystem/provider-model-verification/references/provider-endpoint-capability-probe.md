# Probing whether a provider endpoint can serve a given model class

Use when a gateway fronts many models behind one API and you must know whether a
specific model works on a specific endpoint (e.g. a decisions/classification
model on a chat-completions-style endpoint).

## Do not trust the model catalog as the capability check

A catalog listing (`/v1/models`) may omit models the endpoint still accepts.
Observed: the catalog exposed 67 model ids and ZERO of the working provider's
prefix, yet requests to that provider's models succeeded. A catalog lookup
returning "not present" does NOT mean the model is unusable — probe the endpoint.

Likewise, a generic capability flag in the catalog (e.g. `tools: true`) says
nothing about whether the model supports a specific endpoint. It describes
tool-calling, not endpoint routing.

Catalog output is a hint, never the gate. Probe.

## The probe is cheap and definitive

One minimal request per candidate model, then read the status as a table:

| HTTP | Meaning |
|---|---|
| 200 | supported |
| 400 naming the endpoint | hard capability limit — wrong endpoint for this model class |
| 401 missing key / needs workspace | credentials or plan gate, NOT capability |
| 500 | model not routable on this endpoint |

Distinguish these: a 401 is a credentials problem you can fix and then the model
may work; a 400 naming the endpoint is a hard limit. Collapsing them into "does
not work" loses both the reason and the next action.

## Look for the internal tag before assuming a routing mechanism

Gateways often carry an internal `kind`/type tag per model in their installed
server bundle that the public catalog does not expose. Search that bundle for the
model id next to a `kind:` field to learn which models are eligible for a
special endpoint.

To learn which models an endpoint supports: grep the installed bundle for the
tag, THEN confirm with a live probe. Never infer eligibility from the catalog.

## Enumerate before concluding "only one works"

Sweep the obvious candidates across providers AND pricing tiers in one pass. The
paid variant and a free variant of the same model often differ in availability as
well as cost, and the non-default one is frequently what the user wants. Probing
only the default leaves the cheapest option undiscovered.

## Distinguish a classifier from an agent before designing safety controls

When a user fears a model "will act on its own" (buy things, play games, send
messages), verify the response shape and the request schema before designing
controls. Grep the endpoint's handler for tool/function/agent/exec/command/shell
fields, and inspect an actual response body. A classifier returning
`{choice, probabilities, confidence}` or `{type, score}` has no execution path —
its blast radius is data egress and cost, not side effects. Say so plainly, and
design the gates around the real risk instead of the feared one.

Also make the gates fail-closed: every guard (kill switch, explicit opt-in flag,
per-call cost cap, size caps) must REFUSE when it fails, not fall through. And
have the reporting distinguish a genuinely free model (absent/null cost field)
from a zero-cost one — a null cost displayed as `0` reads as a billing bug.
