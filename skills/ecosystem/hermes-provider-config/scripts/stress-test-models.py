#!/usr/bin/env python3
"""
Stress-test model rate limits against an OpenAI-compatible endpoint.

Why: a single "ping" probe does NOT reveal rate limits — they only show
under burst load. This script fires N rapid requests per model and ranks
by success rate, so you can pick models with the loosest quota for
thread mappings and fallback chains.

Usage:
    python3 stress-test-models.py [--base-url URL] [--burst N] [--models m1 m2 ...]

Defaults read NINE_ROUTER_API_KEY from Hermes USB .env and hit
http://localhost:20128/v1 (9router). Pass --models to override the default
candidate list. Exit code 0 always; read the ranking output.

Verified 13 Ags 2026 against 9router v0.5.50 (33 models, incl. JuanRouter):
    nvidia/z-ai/glm-5.2         → 2/8  (weak — was a thread's main model)
    nvidia/minimaxai/minimax-m3 → 1/8  (weak)
    gemini/gemini-3.6-flash     → 7/8 then 2/8 an hour later (drifts!)
    gemini/gemini-3.5-flash-lite→ 8/8  (stable)
    cf/@cf/zai-org/glm-4.7-flash→ 8/8  (stable, Cloudflare)
    JuanRouter/*                → 8/8  (but paid/balance-based)
"""
import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request

DEFAULT_MODELS = [
    "gratislonggar",
    "gemini/gemini-3.5-flash-lite",
    "gemini/gemini-3.6-flash",
    "gemini/gemma-4-31b-it",
    "gc/gemini-2.5-flash",
    "gc/gemini-2.5-flash-lite",
    "nvidia/z-ai/glm-5.2",
    "cf/@cf/zai-org/glm-4.7-flash",
    "cf/@cf/deepseek-ai/deepseek-r1-distill-qwen-32b",
    "JuanRouter/glm-5.2",
    "JuanRouter/gemini-3.5-flash-lite",
    "JuanRouter/gemini-3.6-flash",
    "JuanRouter/qwen3.7-plus",
]

DEFAULT_ENV_PATH = "/Volumes/HermesAgent/HermesAgentUSB/data/.env"


def load_key(env_path: str) -> str:
    """Read NINE_ROUTER_API_KEY from a .env file."""
    with open(env_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("NINE_ROUTER_API_KEY="):
                return line.split("=", 1)[1]
    raise SystemExit("NINE_ROUTER_API_KEY not found in " + env_path)


def parse_response(raw: bytes) -> dict | None:
    """Handle both plain JSON and SSE stream responses."""
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


def probe(base_url: str, key: str, model: str, max_tokens: int = 8, timeout: int = 30) -> str:
    """One chat completion call; returns 'OK' or the HTTP code / error tag."""
    body = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": "say OK"}],
        "max_tokens": max_tokens,
        "stream": False,
    }).encode()
    req = urllib.request.Request(
        base_url.rstrip("/") + "/chat/completions", data=body, method="POST"
    )
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


def main() -> int:
    ap = argparse.ArgumentParser(description="Burst-test model rate limits")
    ap.add_argument("--base-url", default="http://localhost:20128/v1", help="OpenAI-compatible base URL (default 9router)")
    ap.add_argument("--burst", type=int, default=8, help="requests per model (default 8)")
    ap.add_argument("--env", default=DEFAULT_ENV_PATH, help="path to .env with NINE_ROUTER_API_KEY")
    ap.add_argument("--models", nargs="+", default=DEFAULT_MODELS, help="model ids to test")
    args = ap.parse_args()

    key = load_key(args.env)
    print(f"Base: {args.base_url} | burst={args.burst} | models={len(args.models)}")

    scores: dict[str, tuple[int, dict]] = {}
    for m in args.models:
        results = [probe(args.base_url, key, m) for _ in range(args.burst)]
        ok = sum(1 for r in results if r == "OK")
        from collections import Counter
        scores[m] = (ok, Counter(results))
        tag = "OK" if ok == args.burst else ("WEAK" if ok >= args.burst // 2 else "BAD")
        print(f"  {tag:4} {m:55s} {ok}/{args.burst}  " +
              " ".join(f"{k}x{c}" for k, c in sorted(Counter(results).items(), key=lambda x: -x[1])))

    print("\n=== RANKING ===")
    for m, (ok, _) in sorted(scores.items(), key=lambda x: -x[1]):
        print(f"  {ok}/{args.burst}  {m}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
