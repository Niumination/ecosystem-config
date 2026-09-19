#!/usr/bin/env python3
"""Probe provider models for the two things a Hermes session actually needs:
HTTP 200 AND a returned tool call.

Why tool-calling: cron jobs, Telegram channels and delegation run with toolsets, so a model
that answers text but never returns `tool_calls` fails in real sessions.

Token sources (pick exactly one):
  --auth-json <provider>  live credential from ~/.hermes/auth.json credential_pool
                          (OAuth providers such as nous never use an API key)
  --key-env <VAR>         read the key from the environment (~/.hermes/.env)

The token is never printed.

Usage:
  python3 probe-tool-calling.py --base-url https://inference-api.nousresearch.com/v1 \
      --auth-json nous inclusionai/ling-3.0-flash-fin:free meituan/longcat-2.0:free
  set -a; . ~/.hermes/.env; set +a
  python3 probe-tool-calling.py --base-url http://127.0.0.1:20128/v1 \
      --key-env NINE_ROUTER_API_KEY gemini/gemini-3.8-flash

Exit code 0 only when every model returned a tool call.
"""
import argparse
import json
import os
import pathlib
import sys
import urllib.error
import urllib.request

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "terminal",
            "description": "Run a shell command",
            "parameters": {
                "type": "object",
                "properties": {"command": {"type": "string"}},
                "required": ["command"],
            },
        },
    }
]

PROMPT = "Run the shell command: pwd. Use the tool."


def token_from_auth_json(provider: str) -> str:
    path = pathlib.Path.home() / ".hermes" / "auth.json"
    if not path.exists():
        sys.exit(f"{path} not found")
    data = json.loads(path.read_text())
    pool = (data.get("credential_pool") or {}).get(provider) or []
    if not pool:
        available = ", ".join(sorted(data.get("credential_pool") or {})) or "(none)"
        sys.exit(f"no credential_pool entry for '{provider}'; available: {available}")
    entry = pool[0]
    tok = entry.get("agent_key") or entry.get("access_token") or ""
    if not tok:
        sys.exit(f"credential_pool.{provider}[0] has no agent_key/access_token")
    return tok


def token_from_env(var: str) -> str:
    val = os.environ.get(var)
    if not val:
        sys.exit(f"{var} is not set - run `set -a; . ~/.hermes/.env; set +a` first")
    return val


def probe(base_url: str, token: str, model: str, timeout: int, max_tokens: int) -> str:
    body = json.dumps(
        {
            "model": model,
            "stream": False,
            "max_tokens": max_tokens,
            "messages": [{"role": "user", "content": PROMPT}],
            "tools": TOOLS,
        }
    ).encode()
    req = urllib.request.Request(
        f"{base_url.rstrip('/')}/chat/completions",
        data=body,
        method="POST",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            payload = json.load(resp)
    except urllib.error.HTTPError as exc:
        detail = exc.read()[:140].decode(errors="replace").replace("\n", " ")
        return f"HTTP {exc.code} - {detail}"
    except Exception as exc:  # noqa: BLE001 - report any transport failure verbatim
        return f"FAILED - {type(exc).__name__}: {exc}"
    message = (payload.get("choices") or [{}])[0].get("message") or {}
    if message.get("tool_calls"):
        return "HTTP 200 . TOOL-CALL OK"
    if message.get("content"):
        return "HTTP 200 . text only (NO tool call) - risky for cron/channel sessions"
    return "HTTP 200 . EMPTY (reasoning model? raise --max-tokens)"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base-url", required=True)
    ap.add_argument("--auth-json", metavar="PROVIDER")
    ap.add_argument("--key-env", metavar="VAR")
    ap.add_argument("--timeout", type=int, default=60)
    ap.add_argument("--max-tokens", type=int, default=80)
    ap.add_argument("models", nargs="+")
    args = ap.parse_args()
    if bool(args.auth_json) == bool(args.key_env):
        sys.exit("pick exactly one token source: --auth-json PROVIDER or --key-env VAR")
    token = (
        token_from_auth_json(args.auth_json)
        if args.auth_json
        else token_from_env(args.key_env)
    )
    failures = 0
    for model in args.models:
        result = probe(args.base_url, token, model, args.timeout, args.max_tokens)
        print(f"{model:46} {result}")
        if "TOOL-CALL OK" not in result:
            failures += 1
    print(f"\n{len(args.models) - failures}/{len(args.models)} models return a tool call")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
