---
name: agent-thread-latency-diagnosis
description: "Use when a chat thread is slow or unresponsive."
version: 1.0.0
platforms: [macos, linux]
metadata:
  hermes:
    tags: [telegram, latency, state-db, model-routing, providers]
    related_skills: [model-status-checker, provider-fallback, provider-model-verification]
---

# Diagnosing Slow or Unresponsive Agent Threads

A user reporting "that thread is slow" names a symptom, not a cause. The reported model is
frequently not the model currently serving that thread. Confirm identity first, then isolate
the layer.

## Step 1 — Confirm which model the thread is ACTUALLY on

Never trust the model the user names, or the model sitting in the config mapping. Runtime
routing changes mid-session, and config drifts out of date as soon as anyone uses `/model`.

```bash
python3 - <<'PY'
import sqlite3
con = sqlite3.connect('/Users/zaryu/.hermes/state.db')
cur = con.cursor()
cur.execute("""SELECT thread_id, model, last_activity_at FROM sessions
               WHERE last_activity_at IS NOT NULL ORDER BY last_activity_at DESC""")
for tid, model, ts in cur.fetchall():
    if tid is not None:
        print(tid, model, ts)
con.close()
PY
```

`last_activity_at` is a unix epoch float; the newest row per thread is the live model.
Compare it against what the user reports and against the config mapping — a three-way
mismatch is itself the finding, and it means the user is describing a past state.

## Step 2 — Is the model even reachable from the router?

A model absent from the local gateway catalog can still be configured, and can still be
served directly by its own provider. Absence proves nothing on its own — it just removes
one explanation.

```bash
curl -s --max-time 15 http://localhost:20128/v1/models -o /tmp/m.json -w "HTTP %{http_code}\n"
python3 -c "import json;d=json.load(open('/tmp/m.json'));ids=[m['id'] for m in d.get('data',[])];print(len(ids),[i for i in ids if 'needle' in i.lower()])"
```

## Step 3 — Probe latency directly against the provider, not through the agent

Measure the provider with a minimal payload, repeating 3x. Read the shape of the response,
not just the status.

```bash
# write key lookup to a file, never inline a secret in the command
python3 - <<'PY'
import os, json, time, urllib.request
key = next((l.split('=',1)[1].strip().strip('"')
            for l in open(os.path.expanduser('~/.hermes/.env'), errors='replace')
            if l.startswith('PROVIDER_API_KEY')), None)
req = urllib.request.Request('https://provider/v1/chat/completions',
    data=json.dumps({"model":"M","messages":[{"role":"user","content":"say ok"}],
                     "max_tokens":5}).encode(),
    headers={"Authorization": f"Bearer {key}", "Content-Type":"application/json"})
for i in range(3):
    t = time.time()
    try:
        r = urllib.request.urlopen(req, timeout=90); body = r.read(300)
        print(f"try{i+1} HTTP {r.status} {time.time()-t:.2f}s {body[:120]}")
    except Exception as e:
        print(f"try{i+1} ERR {time.time()-t:.2f}s {type(e).__name__} {str(e)[:100]}")
PY
```

Read three things off the probe:
- **First call much slower than the rest** → cold start / cache miss, not a broken provider.
- **Payload returns `reasoning_content` with `content: null`** → reasoning tokens are
  billed and streamed before any visible text. A "slow" model may simply think out loud
  first; multiply the minimal-payload latency by task length before blaming the provider.
- **401 on the provider that config lists as default** → the default path is dead. Every
  request that lands there retries, which reads to the user as slowness rather than failure.

## Step 4 — Separate provider latency from agent overhead

Only after steps 1–3 attribute the wait. Agent-side contributors worth checking: retry
count on a dead provider, tool-loop length, context size, and a queue ahead of the thread.
Provider latency is a hypothesis; the probe is what makes it evidence.

## Reporting

Lead with the correction when the user's stated model is wrong — the fastest fix for a
"slow thread" complaint is often "it already moved off that model". Then give the measured
latency, the layer responsible, and the next decision. Do not claim a root cause the probe
did not show.

Keep secrets out of output: report key prefix, last four characters, and length only.
