# Vercel latency & timeout budget (sapa-ai)

Use when production answers are slow (30-45s), some end in `503 panggilan model gagal: timeout`, yet the same queries answer in 10-25s from a local server.

## 1. Probe the function region BEFORE touching the model

```bash
curl -sI https://sapa-smart-ai.vercel.app/api/status | grep -i x-vercel-id
# sin1::iad1::...   → edge Singapore, FUNCTION Washington DC   ← the problem
# sin1::sin1::...   → function in Singapore too                ← fixed
```

Vercel runs new projects' functions in `iad1` (US East) by default. With SPLP (Indonesia) as the data source and users in Aceh, every request crossed an ocean twice before the model was even called. Fix:

```json
{
  "regions": ["sin1"],
  "functions": { "src/app/api/query/route.ts": { "maxDuration": 60 } }
}
```

Measured effect: 38.7-41.9s → 15.6-29.9s. The same symptom is easy to misread as a slow upstream or a slow model.

Once the region is right, retrieval is cheap: `ai.latencyMs` from the response is the model time, and it is roughly total request time minus ~1s.

## 2. Layered timeout budget

The three limits must be ordered from the inside out:

| Layer | Owner | Value |
|---|---|---|
| Model call | `AI_TIMEOUT_MS` (default 48000) | 48s |
| Dashboard client | `CLIENT_TIMEOUT_MS` | 55s |
| Platform | `maxDuration` per route | 60s |

- Client loosest of the two app layers: the user must see the server's real error, not a client-invented timeout.
- A route with no `maxDuration` entry silently uses the platform default — list every route that can call the model, including the streaming one the dashboard actually posts to.
- Include the value in the abort message (`timeout setelah ${timeoutMs} ms`). Without it, "timeout" says nothing about which limit is in force in production.

## 3. Retry rules

**Non-stream (JSON) path — retry only 403/429/5xx, never a timeout or an abort:**

```typescript
const bolehLanjut =
  !dibatalkan(e) &&
  (!(e instanceof LlmError) || e.status === undefined || e.status >= 500 || e.status === 429 || e.status === 403);
```

Why it matters: a bare timeout is not an `LlmError`, so the original gate `!(e instanceof LlmError)` passed it through — one doomed answer burned 42.6s (20s + 10s backoff + 20s) instead of failing once. Retrying a timeout does not add a chance of success, only wall time.

## 4. Diagnosing with no log/env access

Surface the failure in the response body: `ai.error`, `ai.reason`, `ai.limitedBy`, `ai.used`. `/api/status` exposes `toggles` (state + active `backend`) and the deterministic/LLM ratio. Both beat guessing from a dashboard you cannot read.

## 5. Benchmark recipe — compare model candidates off-production

Run the real pipeline locally against the provider instead of hand-rolling a curl to the API:

```bash
# secrets go into env vars, never onto the command line or into logs
export OC_KEY=$(python3 -c "import json;print(json.load(open('$HOME/.local/share/opencode/auth.json'))['opencode']['key'])")
export AI_ENABLED=true AI_BASE_URL=https://opencode.ai/zen/go/v1 \
       AI_API_KEY="$OC_KEY" AI_MODEL=<candidate> AI_TIMEOUT_MS=55000 \
       AI_CUSTOM_HEADERS='{"x-opencode-session":"bench-local"}'
npm run start -- -p 3105        # background
curl -s -X POST localhost:3105/api/query -H 'Content-Type: application/json' \
     -d '{"query":"..."}' -w 'waktu=%{time_total}s\n'
```

Run the same query set per candidate and compare `used`, `grounded`, `latencyMs`. OpenCode Go rejects requests without `x-opencode-session` (400 `MissingSessionID`); any stable per-conversation id works — it exists for routing and prompt caching, not authentication. Kill the local server when done.

## 6. Measured and rejected — do not repeat

- `AI_MAX_OUTPUT_TOKENS` 3000 → 1500 to buy speed: 3/4 answers truncated before the JSON closed (`used=false`, template fallback).
- Provider switch justified by production latency alone: locally `glm-5.3` (13.7-23.4s) matched or beat `deepseek-v4-flash` (10.6-27.6s), both 4/4 `grounded=pass`. The model was never the bottleneck.

## 7. Stall vs slow — zero-token probe, watchdog, retry guard

Two failure shapes look identical from the user's side ("timeout setelah N ms") and need opposite responses:

- **slow** — deltas are arriving; waiting is correct, only the budget is too small
- **stalled** — no bytes at all for the whole window; the socket is dead and waiting only burns the budget

Tell them apart by counting `event: token` blocks on `POST /api/query/stream`: a run that ends in `event: error` with `token=0` is a stall. Measured contrast on one query: 12.1s / 995 prompt tokens locally vs 48s with zero output from production.

Fix shape — a progress watchdog, not a longer timeout:

```typescript
const STALL_MS = Number(process.env.AI_FIRST_TOKEN_MS ?? '') || 15_000;
gabungSignal(eksternal, timeoutMs, STALL_MS)   // → { signal, reset, selesai }
// reset() on every chunk read; abort reason 'stall: tidak ada data dalam N ms'
```

- Retry once on stall: 1s pause, second attempt capped at 30s → worst case 15 + 1 + 30 = 46s, inside the 55s client.
- Retry ONLY while `sudahAdaData === false`. Once a delta reached the caller, restarting duplicates the narration.
- Never retry when the caller's own `AbortSignal` fired.
- The watchdog measures the gap with **no provider bytes at all** — not the gap until the first narration token, which is normal at 16-18s. Keep it well below that or healthy calls get killed.

Test the guard with a signal-aware fetch stub: a `ReadableStream` that never enqueues hangs forever unless the stub errors it from `signal.addEventListener('abort', () => controller.error(signal.reason))`. A mock that ignores the signal proves nothing and fails on a 5s test timeout instead.

## 8. Benchmark & verification discipline

- Compare candidates with the **cheap flash model** on the real pipeline. The metered production model is quota-guarded by the owner and must not be spent on broad probes.
- Stop background probes immediately when the owner says so, then confirm: `pkill -f <script>` followed by `ps aux | grep -c "[p]attern"`.
- Prove a deploy landed without model cost: a gibberish query with no evidence short-circuits before the model call, so its *wording* shows whether the new code is live — check the wording changed, not just the HTTP status.
