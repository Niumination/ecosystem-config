#!/usr/bin/env python3
"""Probe OpenAI-compatible provider endpoint dengan chat-completion (non-streaming).

Usage:
  KEY_ENV=JUAN_ROUTER_API_KEY python3 probe-provider-models.py \
      https://router.juan.web.id/v1 agnes-2.0-flash gemma-4-31b-it
  # UA default hermes-agent/0.19.0; untuk opencode-zen: UA='opencode/1.18.18' ...

Meng-encode 3 aturan probe (verified 15 Ags 2026):
  1. User-Agent header WAJIB — plain urllib/curl UA -> 403 di banyak router
     (opencode-zen butuh `opencode/<ver>`; juan-router/agentrouter terima `hermes-agent/<ver>`)
  2. stream:false selalu — streaming bisa return chunk kosong padahal model hidup
  3. Listed model != usable — /v1/models menampilkan tapi chat bisa 401 (ling-3.0-flash-free)

Key dibaca dari /Volumes/HermesAgent/HermesAgentUSB/data/.env via KEY_ENV.
"""
import json
import os
import sys
import urllib.error
import urllib.request

ENV_PATH = "/Volumes/HermesAgent/HermesAgentUSB/data/.env"


def load_env(path: str) -> dict:
    env = {}
    try:
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if "=" in line and not line.startswith("#"):
                    k, v = line.split("=", 1)
                    env[k.strip()] = v.strip().strip('"')
    except FileNotFoundError:
        pass
    return env


def probe(base_url: str, model: str, key: str, ua: str) -> str:
    url = base_url.rstrip("/") + "/chat/completions"
    body = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": "Balas hanya: OK"}],
        "max_tokens": 15,
        "stream": False,
    }).encode()
    req = urllib.request.Request(url, data=body, method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("Authorization", f"Bearer {key}")
    req.add_header("User-Agent", ua)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            d = json.loads(r.read().decode())
            content = d.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
            return f"OK  {model}: HTTP 200 model={d.get('model', '?')} reply={content[:30]!r}"
    except urllib.error.HTTPError as e:
        detail = e.read().decode()[:100] if e.fp else ""
        return f"ERR {model}: HTTP {e.code} {detail}"
    except Exception as e:
        return f"ERR {model}: {type(e).__name__}: {str(e)[:90]}"


def main() -> None:
    args = sys.argv[1:]
    if len(args) < 2:
        print(__doc__)
        sys.exit(1)
    base_url = args[0]
    models = args[1:]
    env = load_env(os.environ.get("ENV_PATH", ENV_PATH))
    key_env = os.environ.get("KEY_ENV", "")
    key = os.environ.get(key_env) or env.get(key_env, "")
    if not key:
        print(f"Key kosong: set KEY_ENV=<nama var> (dibaca dari {ENV_PATH})")
        sys.exit(2)
    ua = os.environ.get("UA", "hermes-agent/0.19.0")
    print(f"probe {base_url} | UA={ua} | key_env={key_env}")
    for m in models:
        print(probe(base_url, m, key, ua))


if __name__ == "__main__":
    main()
