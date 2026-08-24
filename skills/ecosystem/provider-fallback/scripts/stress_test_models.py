#!/usr/bin/env python3
"""
Stress-test model candidates for rate-limit tolerance against an
OpenAI-compatible router (9router / JuanRouter / AgentRouter etc).

Why: model quality alone is not enough to pick a thread/fallback model —
quota per provider ROUTE varies wildly for the same model name
(e.g. nvidia/z-ai/glm-5.2 2/8 vs JuanRouter/glm-5.2 8/8), and quota
changes between runs. Measure, don't assume.

Usage:
    python3 stress_test_models.py \
        --base http://localhost:20128/v1 \
        --env-file /Volumes/HermesAgent/HermesAgentUSB/data/.env \
        --key-env NINE_ROUTER_API_KEY \
        --bursts 8 \
        --probe "say OK" \
        nvidia/z-ai/glm-5.2 cf/@cf/zai-org/glm-4.7-flash gemini/gemma-4-31b-it

Output: per-model result summary + ranking by success count.
Exit code: 0 always (report-only). Print plain lines for cron/automation.

Notes:
- Sends `"stream": false` EXPLICITLY — 9router sometimes replies SSE anyway,
  so the parser below handles both plain JSON and SSE chunks.
- 8 bursts per model at ~25s timeout can take a few minutes; reduce --bursts
  for a quick pass. ALWAYS re-run before choosing — quota drifts intraday.
"""
import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from collections import Counter


def load_env(path: str) -> dict:
    env = {}
    if not path or not os.path.exists(path):
        return env
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                env[k] = v
    return env


def parse_response(raw: bytes):
    """Plain JSON OR SSE stream (9router sometimes streams despite stream:false)."""
    text = raw.decode("utf-8", errors="replace")
    try:
        return json.loads(text)
    except Exception:
        pass
    contents = []
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("data:"):
            payload = line[5:].strip()
            if payload and payload != "[DONE]":
                try:
                    chunk = json.loads(payload)
                    for c in chunk.get("choices", []):
                        delta = c.get("delta", {})
                        if delta.get("content"):
                            contents.append(delta["content"])
                except Exception:
                    pass
    return {"choices": [{"message": {"content": "".join(contents)}}]} if contents else None


def call_once(base: str, key: str, model: str, probe: str, timeout: int) -> str:
    body = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": probe}],
        "max_tokens": 8,
        "stream": False,
    }).encode()
    req = urllib.request.Request(base.rstrip("/") + "/chat/completions", data=body, method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("Authorization", f"Bearer {key}")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            d = parse_response(r.read())
            return "OK" if d and d.get("choices") else "ERR"
    except urllib.error.HTTPError as e:
        return str(e.code)  # 429 = rate limited
    except Exception:
        return "ERR"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("models", nargs="+", help="model ids to test")
    ap.add_argument("--base", default="http://localhost:20128/v1")
    ap.add_argument("--env-file", default="/Volumes/HermesAgent/HermesAgentUSB/data/.env")
    ap.add_argument("--key-env", default="NINE_ROUTER_API_KEY")
    ap.add_argument("--bursts", type=int, default=8)
    ap.add_argument("--probe", default="say OK")
    ap.add_argument("--timeout", type=int, default=30)
    args = ap.parse_args()

    key = os.getenv(args.key_env) or load_env(args.env_file).get(args.key_env, "")
    if not key:
        print(f"ERROR: key {args.key_env} not found in env or {args.env_file}")
        sys.exit(2)

    scores = {}
    for m in args.models:
        results = [call_once(args.base, key, m, args.probe, args.timeout) for _ in range(args.bursts)]
        ok = sum(1 for r in results if r == "OK")
        scores[m] = ok
        cnt = Counter(results)
        summary = " ".join(f"{k}x{c}" for k, c in sorted(cnt.items(), key=lambda x: -x[1]))
        print(f"{'✅' if ok >= args.bursts - 1 else '⚠️'} {m:55s} {ok}/{args.bursts}  [{summary}]")

    print("\n=== RANKING ===")
    for m, ok in sorted(scores.items(), key=lambda x: -x[1]):
        print(f"  {ok}/{args.bursts}  {m}")


if __name__ == "__main__":
    main()
