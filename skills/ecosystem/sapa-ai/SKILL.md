---
name: sapa-ai
description: "Use when working on sapa-ai."
version: "1.0.0"
author: Niumination (Afrizal Munthe)
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [sapa-ai, nextjs, ai, splp, indonesia, public-service]
    homepage: https://sapa-smart-ai.vercel.app
---

# SAPA Smart AI — Development & Operations

Build and maintain sapa-ai: AI-powered portal for Aceh Tengah public service data (SPLP). Next.js 16 + Vercel, deterministic + LLM hybrid pipeline.

## Architecture

- **Framework:** Next.js 16 + Vercel (ISR 10m)
- **Production URL:** https://sapa-smart-ai.vercel.app
- **Repo:** `services/sapa-ai/` (Niumination/sapa-ai)
- **AI Provider:** OpenCode Go (`glm-5.3`) with deterministic fallback
- **Cache:** 10m ISR + LRU per-instance
- **No database:** SPLP API direct fetch only

## Workflow — Making Code Changes

1. Edit files in `services/sapa-ai/src/`
2. Build locally: `cd services/sapa-ai && npm run build`
3. Stage only intended files: `git add src/path/to/file.ts`
4. NEVER stage untracked artifacts: `.hermes/plans/`, `rekons.md`
5. Commit: `fix: <what>` or `feat: <what>`
6. Push: `git push origin main` (requires `gas`/`fix` trigger)
7. Vercel auto-deploys

## Workflow — Admin Toggle Panel (AI + Deterministic)

Hidden panel at `/admin/ai-toggle` to globally disable/enable AI and Deterministik independently.

Setup:
1. Set env var `AI_ADMIN_KEY` in Vercel Dashboard — empty means every toggle call answers 401
2. Set `UPSTASH_REDIS_REST_URL` + `UPSTASH_REDIS_REST_TOKEN` (Upstash free tier) — without them the store degrades to per-instance memory and the toggle is not global
3. Redeploy: env changes never apply to existing deployments
4. Access `https://sapa-smart-ai.vercel.app/admin/ai-toggle`

Control matrix — "deterministic" means the TEMPLATE answer, so Det OFF forbids template output, NOT the service:
- AI ON + Det ON → LLM answer, template fallback when the model fails
- AI ON + Det OFF → LLM answer only; no template fallback
- AI OFF + Det ON → template answer only
- AI OFF + Det OFF → service unavailable (503)
- AI ON + Det OFF with the model failing or timing out → honest error to the user, never a silent template

State lives in the shared store (`src/lib/store.ts` → Upstash Redis, memory fallback), never in a file. Key `sapa:ai:toggle:v1`, TTL ~30 days. `/api/admin/status` returns `backend: 'redis' | 'memory'` — `memory` means the toggle is per-instance and not global. Read: `await isAiToggleEnabled()` / `await isDetToggleEnabled()` (async since the state moved into the store). Full mechanism + verification recipe: `references/serverless-runtime-gating.md`.

Gate in `answer-compose.ts` — toggles first, then derive, then enforce in the funnel:

```typescript
const aiToggleOn = await isAiToggleEnabled();
const detToggleOn = await isDetToggleEnabled();
const deterministikMati = !detToggleOn;

const selesai = (alasan?: string, limitedBy?: AiMeta['limitedBy'], errorMsg?: string): ComposeResult => {
  meta.latencyMs = Date.now() - mulai;
  if (alasan) meta.reason = alasan;
  if (limitedBy) meta.limitedBy = limitedBy;
  if (errorMsg) meta.error = errorMsg.slice(0, 200);
  if (deterministikMati) {                  // one funnel closes every fallback path
    meta.limitedBy = 'service-unavailable';
    meta.reason = `${alasan ? `${alasan} — ` : ''}jawaban deterministik dinonaktifkan admin dan AI tidak menghasilkan jawaban`;
    meta.grounded = 'skipped';
    meta.used = false;
    return selengkap(meta, { ...dasar.response, narasi: meta.reason, rekomendasi: [] });
  }
  recordMetrics('deterministic');
  return selengkap(meta, dasar.response);
};

// NO early guard here. An `if (deterministikMati) return ...` at this point kills the
// whole service and suppresses answers the model can still produce — the owner rejects
// that outright. The LLM success path returns via selengkap() and must stay open; only
// the template funnel (selesai) is gated.
const cfg = getAiConfig();
const aktif = isAiEnabled(cfg) && aiToggleOn;   // runtime toggle outranks AI_ENABLED
const shadow = isAiShadow(cfg) && aiToggleOn;
if (!aktif && !shadow) {
  return selesai(aiToggleOn ? (aiStatusReason(cfg) ?? 'AI nonaktif') : 'AI dinonaktifkan oleh admin', 'unconfigured');
}
```

Route boundary: `/api/query` maps `hasil.ai?.limitedBy === 'service-unavailable'` → 503; `/api/query/stream` emits `event: error` before any `result` event.

Toggle state interface:
```typescript
interface ToggleState {
  aiEnabled: boolean;   // default: true
  detEnabled: boolean;  // default: true
  updatedAt: string;
  updatedBy: string;
}
```

API endpoints:
- `GET /api/admin/status` → `{ aiEnabled: boolean, detEnabled: boolean }` (public)
- `POST /api/admin/toggle-ai` → body: `{ aiEnabled?, detEnabled? }` (requires `x-admin-key` header)

## Workflow — Exposing AI Errors in API Response

When LLM calls fail, surface the error in the response instead of hunting logs — dashboard log and env views may be unavailable to the CLI:

- Add an optional `errorMsg` parameter to the SINGLE funnel `selesai()` shown above. Never declare a second `selesai()`; a duplicate without the gate reintroduces the leak.
- Call it from the failure paths: `return selesai(`panggilan model gagal: ${errMsg}`, undefined, errMsg);`
- Read `ai.error` and `ai.reason` from the response body.
- Make abort messages carry the numeric limit (`timeout setelah 48000 ms`) so the effective production budget is readable without inspecting env vars.

## Workflow — Custom Headers for LLM Provider

When provider requires headers beyond Authorization (e.g., `x-opencode-session`):

1. Add `customHeaders?: Record<string, string>` to `AiConfig`
2. Merge in `llm-client.ts`: `...cfg.customHeaders`
3. Load from env: `JSON.parse(process.env.AI_CUSTOM_HEADERS)`
4. Set in Vercel Dashboard: `AI_CUSTOM_HEADERS={"x-opencode-session": "..."}`
5. Redeploy

## Workflow — Tracking Deterministic vs LLM Ratio

```typescript
async function recordMetrics(kind: 'llm' | 'deterministic'): Promise<void> {
  const key = `metrics:query:${kind}:${tanggalHariIni()}`;
  await incrementCounter(key, 24 * 60 * 60 * 1000);
}
```

- `recordMetrics('deterministic')` on EVERY deterministic output path
- `recordMetrics('llm')` only on successful LLM response
- Keys: `metrics:query:{deterministic,llm}:YYYY-MM-DD`

## Workflow — Fixing Duplicate Units After Token Eject

Problem: Model writes unit after token → `"31,4 Persen persen"`

Two-layer fix:
1. **Prompt:** "Jangan menulis satuan setelah token {{id}}"
2. **Code:** `dedupUnits()` removes repeated unit strings

## Pitfalls

- **NEVER commit `.hermes/plans/` or `rekons.md`** — always `git add` specific files.
- **Custom headers need valid JSON env var** — malformed JSON breaks all LLM calls silently.
- **Duplicate unit fix is defense-in-depth** — prompt instruction alone insufficient.
- **`recordMetrics()` on every path** — missing one path skews ratio.
- **Never persist runtime state in `/tmp` on Vercel** — each serverless instance has its own ephemeral `/tmp`, so the value the admin panel writes is invisible to the request that reads it; the gate falls back to its default and the toggle silently does nothing. Use the shared store, and show which backend is live in the panel.
- **Runtime toggle outranks env flags** — read the toggle before `AI_ENABLED`/`AI_SHADOW` and derive `aktif = isAiEnabled(cfg) && aiToggleOn`; a `selesai()` call placed after the env check answers 200 with a narasi instead of 503.
- **Enforce the gate in the template funnel only** — every template answer leaves through `selesai()`, so gating there closes all of them at once (no-evidence, rate limit, model failure, parse failure). The LLM success path returns through `selengkap()` and MUST stay open: an early `if (deterministikMati) return ...` before the model call suppresses answers the model can still produce and is the mistake the owner corrected.
- **Build green is not tests green** — run `npx vitest run` before committing; a test added while the runner's output was unreadable is unverified and has shipped failing.
- **Don't widen an output helper to satisfy a speculative test** — replace an assertion for behaviour that was never implemented with an observable case plus a note stating the limit.
- **No data-like numbers in the system prompt** — the anti-fabrication prompt test rejects any figure ≥ 10, so phrase rules abstractly.
- **Smoke-test gates with a throwaway local `AI_ADMIN_KEY`** — the real key never belongs in a command line or log.
- **Route imports must use alias** — import `isAiToggleEnabled`/`isDetToggleEnabled` from `@/lib/ai/toggle`, never from relative `'../toggle-ai/route'` (Turbopack fails to resolve re-exports from route files).
- **Both-OFF returns 503** — `/api/query/route.ts` checks `hasil.ai?.limitedBy === 'service-unavailable'` and returns 503, not 200.
- **Vercel env var propagation** — redeploy required after env var changes.
- **Build before commit** — `npm run build` passes before pushing to avoid deploy failures.
- **limitedBy type includes `'service-unavailable'`** for det-toggle-off state.
- **Det OFF is not a service kill switch** — gate the template funnel only. Placing the det-off guard at the entry of `composeAnswer` makes AI ON + Det OFF answer with an error even though the model is healthy; the owner's correction is "deterministic = the template answer".
- **Probe the function region before blaming the model** — `curl -sI <prod-url>/api/status | grep -i x-vercel-id`; the format is `<edge>::<function>`. Vercel defaults new projects to `iad1` (US East), which cost ~20s per request against an Indonesian data source and Indonesian users. Fix with `"regions": ["sin1"]` in `vercel.json`. See `references/vercel-latency-and-timeouts.md`.
- **Retry a timeout only where progress is observable — never on the JSON path** — a retry gate written as `!(e instanceof LlmError)` is TRUE for a bare `Error('timeout')`, so the non-stream path retried timeouts and burned 42.6s (20 + 10 backoff + 20) on an answer that was already lost; exclude abort/timeout there (403/429/5xx stay retryable). With no progress signal there is no way to tell "provider is slow" from "socket is dead", so the only safe rule is no retry. The SSE path CAN see progress and retries under a stricter guard — see the stall bullet below.
- **Layer the timeout budget: model < client < platform** — 48s model, 55s dashboard client, 60s platform `maxDuration`. The client must be the loosest of the two app layers so the user receives the server's real message instead of a fake client-side timeout. Every route that can call the model needs its own `maxDuration` entry; a route with no entry falls back to the platform default.
- **Measure a model candidate through the app's own pipeline before proposing a switch** — a provider that looks slow in production can be equal or faster locally, meaning config (region, timeout), not the model, is at fault. Two candidates indistinguishable on latency do not justify changing a locked model decision.
- **Do not shrink `AI_MAX_OUTPUT_TOKENS` to buy speed** — at 1500 the model runs out of room before finishing the JSON (3/4 answers truncated to `used=false`, falling back to template). 3000 is the calibrated sweet spot.
- **A stalled model connection is not a slow one** — on the SSE path count `token` events: zero deltas across the entire timeout means the socket is dead, and waiting can only waste the budget (the same query answered in ~12s locally while production produced nothing for 48s). Watchdog `AI_FIRST_TOKEN_MS` (default 15000) aborts early and retries once at a 30s cap: 15 + 1 + 30 = 46s, inside the 55s client. Retry ONLY while `sudahAdaData === false` — restarting after a delta reached the caller duplicates the narration; a caller-initiated abort is never retried. The watchdog measures the gap with NO provider bytes at all, which is why 15s is safe even though the first *narration* token normally appears at 16-18s.
- **Verify a deploy on a path that never calls the paid model** — a gibberish query (no SPLP evidence) short-circuits before the model call, so its wording proves whether the new code is live at zero quota cost. A green build or a push is not evidence the deploy landed.
- **Never blame the model for an empty evidence set** — with Det OFF every non-LLM answer leaves through the funnel as `service-unavailable`; branch the message on `limitedBy === 'no-evidence'` ("no relevant SAPA data for this question"), otherwise the user reads a model failure for a question the model was never asked.
- **Benchmark with the cheap flash model, never the metered production model** (owner rule) — run candidate comparisons on the real pipeline with the flash model; probes against the paid model spend a quota the owner is guarding, and every background probe stops the moment the owner says so (verify with `pkill -f <script>` + `ps aux | grep -c "[p]attern"`).

## References

- `references/serverless-runtime-gating.md` — why `/tmp` state fails on Vercel, the shared-store fix, gate ordering/enforcement, and the local smoke-test recipe that proves 503/401 without touching real credentials.
- `references/vercel-latency-and-timeouts.md` — function region probe (`x-vercel-id`) and fix, the layered timeout budget, stall-vs-slow diagnosis with the stream watchdog and its retry guard, the zero-cost deploy probe, and the local benchmark recipe plus quota discipline for comparing model candidates.