# OpenCode Endpoint Quirks (Zen / Go)

Provider-side restrictions discovered by reading the gateway's own error
bodies during on-device validation. Symptoms look like app bugs; they are
server policy. Always surface the truncated server message in validation
UI before diagnosing further.

## Zen free tier is keyless — but only with the exact wire contract

- Symptom: free-tier IDs listed by public `GET /models` fail from a
  third-party client with 400 `MissingSessionID` or 401 on any bearer.
- Wire contract (verified against the relay): omit the `Authorization`
  header ENTIRELY (the relay 401s any bearer it does not recognize, so
  no placeholder credential), AND send `x-opencode-session` (above).
  A correctly-wired keyless call routes and returns model output — or
  `FreeUsageLimitError` when the shared quota is exhausted, which is a
  server-side limit, not an app bug.
- Implication: offer a keyless provider preset (no key field, session
  header on, correct per-family protocol) instead of telling users the
  free tier is unusable. Surface `FreeUsageLimitError`/`429` distinctly
  from auth failures so users read it as "quota exhausted, retry later"
  rather than "key rejected".

## Session header is required on EVERY opencode.ai host, not just Go

- Symptom: `POST .../zen/v1/chat/completions` returns 400
  `MissingSessionID` while model discovery on the same endpoint works.
- Cause: the relay pins requests sharing one `x-opencode-session` value
  to the same backend (warm prompt cache) and rejects sessionless
  requests on all namespaces — Zen, Go, and the free tier alike. The
  reference client sends it on every OpenCode request.
- Fix: one UUID generated per install, persisted in app preferences,
  attached whenever the URL host is opencode.ai. Thread it through every
  caller of the shared HTTP layer (validation, discovery, ping) — a
  header added only to validation re-breaks at the next call site.

## Base path must include `/v1`

- Symptom: every call 404s (`/models`, validation, ping) against a Zen
  custom base like `https://opencode.ai/zen`.
- Cause: Zen serves only under `/zen/v1` — `GET /zen/models` 404s while
  `GET /zen/v1/models` 200s. The built-in Zen entry already carries the
  full base; custom endpoints must type it in full.
- Implication: when all Zen calls 404, check the base path before
  suspecting keys, protocols, or tiers.

## The Zen model list is public — enumerate IDs from it

- `GET https://opencode.ai/zen/v1/models` returns 200 with no key and
  lists every servable model ID (dozens, including tier-suffixed
  variants like `-contributor-free`).
- Implication: copy exact model IDs from this list instead of guessing
  names into the model field; a 400 naming the model means the ID is
  wrong, not the endpoint.

## One base, per-family paths — derive from the docs endpoint table

- The official Zen docs carry a per-model endpoint table: every path hangs
  under ONE base, `https://opencode.ai/zen/v1`, with the family in the
  tail: `/responses` (GPT, Grok, Muse), `/messages` (Claude, Qwen),
  `/chat/completions` (DeepSeek, Kimi, GLM, MiniMax), `/models/<id>`
  (Gemini per-model paths).
- Implication: never guess the base-URL shape — read the provider's own
  endpoint table first. One correct base plus the matching wire protocol
  covers every model family; a custom base missing `/v1` or paired with
  the wrong protocol 404s on an otherwise healthy account.
- `muse-spark` IDs (including `-contributor-free`) are served from
  `/v1/responses`, but the free-tier lock above still applies — an ID
  existing in the public list does not mean the key's tier may call it.

## Free-tier quota is per model, not per tier — never generalize one 429

- Symptom: one free model returns 429 `FreeUsageLimitError` while the tier
  looks usable.
- Cause: quota is enforced per model, not per tier. The same wire
  contract in the same minute can yield 429 on one ID, 200 on the next,
  and upstream-unavailable on a third — a single-model probe proves
  nothing about its siblings.
- Rule: a quota claim must be a per-model matrix (one minimal chat probe
  per candidate ID), never a tier-wide verdict from one response. When a
  user disputes a quota claim, re-probe per model instead of defending
  the generalization.
- When relay behavior itself is disputed, arbitrate with the reference
  client's own command (e.g. the agent CLI's one-shot chat against the
  same provider/model), not with further hand-rolled curl variants — the
  reference path is the ground truth both sides accept.

## Discovery passing proves nothing about validation

- `GET /models` and the per-protocol `POST` (messages / chat-completions /
  responses) are enforced independently per model and per tier. Exercise
  both with the exact model under test before claiming an endpoint works.
- Key-free probe first: repeat the failing request with an invalid key. A
  401 proves the path exists and auth is layered correctly (the failure is
  then parameters or policy); a 404 means the path itself is wrong.

## Known-bad combos get one-tap correction, not another hint paragraph

- Symptom: a custom base on a wrong namespace (e.g. `.../zen/go/v1`
  typed as a REST base) paired with a model from another family and that
  family's wrong protocol — triple fault, every Test fails, and static
  hint text gets scrolled past.
- Rule: when the base host is recognized but the path is not the canonical
  one, render a button that rewrites the field to the canonical base in
  one tap; when the model prefix implies a family (deepseek→completions,
  muse-spark/gpt/grok→responses, claude/qwen→messages) but the selected
  protocol disagrees, render the mismatch as a red inline warning naming
  the required protocol — before the user ever presses Test.

## Contributor-tier models refuse non-interactive runs without a consent flag

- Symptom: one-shot chat against a `muse-spark` (Meta contributor) ID exits 1 with no answer while the same wire contract returns 200 for other free IDs.
- Cause: training-on-data tiers require explicit opt-in (`security.allow_data_training_tiers_noninteractive` in the agent config); without it the CLI refuses unattended runs.
- Rule: default free presets to a no-consent model, and expose contributor tiers only behind an explicit toggle that writes the flag into the guest config with the training disclosure attached — never silently flip it on.

## Discovery and validation need the same transient-error handling

- Symptom: the Test button rides out free-tier flaps but model-list fetches fail on the same 429/503 blips.
- Cause: retry logic bolted only onto validation while discovery calls the raw request path.
- Rule: one shared retry helper for 429/5xx used by every caller of the shared HTTP layer (validation, discovery, ping).
