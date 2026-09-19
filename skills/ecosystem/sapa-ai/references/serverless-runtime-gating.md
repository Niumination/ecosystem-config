# Serverless runtime gating — sapa-ai admin toggles

Depth for the admin on/off panel (`/admin/ai-toggle`) and any future runtime flag
that must apply to every request on Vercel.

## Why `/tmp` state silently fails

Symptom: the panel is set to OFF, the dashboard still answers, and `/api/status`
still reports the AI active with its model.

Mechanism: each serverless instance gets its own ephemeral `/tmp`. The request
handling the panel POST and the request handling `/api/query` are routinely
different instances, and a cold start gets a fresh filesystem. The reading
instance finds no file, falls back to the default (`enabled: true`), and serves
normally — a silent no-op, never an error.

Read and write the state through the shared store (`cacheGet`/`cacheSet` in
`src/lib/store.ts`): Upstash Redis when configured, process memory otherwise.
Toggle key `sapa:ai:toggle:v1`, TTL ~30 days, value
`{ aiEnabled, detEnabled, updatedAt, updatedBy }`.

The memory fallback is per-instance too. That is fine for cache and counters and
useless for a global switch — which is why `UPSTASH_REDIS_REST_URL` +
`UPSTASH_REDIS_REST_TOKEN` are required for a global toggle, and why
`/api/admin/status` exposes `backend: 'redis' | 'memory'` so the panel can warn
loudly instead of failing silently. Make degradation visible; a switch that
looks like it works is worse than one that reports it cannot.

## Gate ordering and enforcement

Ordered by what breaks first:

1. Read the toggle BEFORE the env check, then derive
   `aktif = isAiEnabled(cfg) && aiToggleOn` (same for `shadow`). Otherwise
   `AI_ENABLED=false` plus toggles OFF returns `unconfigured` → HTTP 200 with a
   deterministic narasi instead of 503.
2. Enforce inside `selesai()` — the single funnel every fallback path goes
   through (no evidence, guard, rate limit, daily limit, model failure, parse
   failure) — AND in an early guard before any success path. The successful LLM
   branch returns via `selengkap()`, bypassing `selesai()`.
3. Convert at the route boundary, not in the composer: `/api/query` maps
   `hasil.ai?.limitedBy === 'service-unavailable'` → 503, and
   `/api/query/stream` emits `event: error` before any `result` event.
4. The unavailable payload must still satisfy `HybridResponse`; spread the
   deterministic one: `{ ...dasar.response, narasi: meta.reason, rekomendasi: [] }`.

## Verifying a gate without touching real credentials

Unit tests mock the store, so they prove the branch, not the deployment. Prove
the deployed gate over HTTP by running the built app locally with an invented
admin key:

```bash
cd services/sapa-ai && npm run build
AI_ADMIN_KEY=smoke-test-lokal npm run start -- -p 3104   # background
# readiness: poll /api/admin/status until it answers 200
```

Then assert in this order:

```bash
K=smoke-test-lokal
curl -s -X POST localhost:3104/api/admin/toggle-ai -H "x-admin-key: $K" \
  -H 'Content-Type: application/json' -d '{"aiEnabled":false,"detEnabled":false}'
curl -s -o /tmp/q.json -w "http=%{http_code}\n" -X POST localhost:3104/api/query \
  -H 'Content-Type: application/json' -d '{"query":"berapa prevalensi stunting"}'   # expect 503
curl -s -N -X POST localhost:3104/api/query/stream -d '{"query":"stunting"}' | grep '^event:'  # expect event: error
curl -s -o /dev/null -w "http=%{http_code}\n" -X POST localhost:3104/api/admin/toggle-ai -d '{}'  # expect 401
```

Kill the server afterwards. A local run reports `backend: 'memory'`; that is
expected and does not weaken the gate test.

For a real credential already on disk, read it into a shell variable rather than
writing it literally, so it never lands in a command line or log:

```bash
KEY=$(grep -m1 '^AI_ADMIN_KEY=' .env | cut -d= -f2- | tr -d '"')
```

## After a push

Vercel needs roughly 1–2 minutes; poll the live endpoint instead of assuming the
change is live. `vercel env ls` only works when run from the linked project
directory. Env changes never apply to existing deployments — redeploy, then read
the endpoint back before claiming the change took effect.

## Pitfalls

- Do not widen `dedupUnits()` to satisfy a speculative test: it handles the
  identical unit repeated (`"31,4 Persen persen"`); a synonym invented by the
  model (`"pegawai orang"`) belongs to the grounding gate. Replace the
  assertion with an observable case and state the limit in the test body.
- Adding an example with real-looking figures to the system prompt breaks the
  anti-fabrication prompt test (any number ≥ 10 fails) — phrase the rule
  abstractly.
- `npm run build` passing says nothing about the suite. Run `npx vitest run`:
  a test committed while the runner's output was unreadable shipped failing.
