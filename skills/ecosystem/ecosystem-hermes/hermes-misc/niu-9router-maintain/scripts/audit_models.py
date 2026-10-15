#!/usr/bin/env python3
"""Audit model access on 9router — DRY-RUN by default, transient-aware.

Why this shape (learned the hard way):
  * A single probe per model under parallel load reports healthy providers as dead. Real
    case: `gemini` was judged 0/1 OK and got disabled, while its usageHistory showed a
    successful 1,060-token call the day before. The failure was a transient timeout.
  * Treating every non-200 as fatal makes the script disable working providers.
  * Writing to the DB on the first run removes the chance to review.

Rules this script follows:
  1. NEVER writes to the DB unless --apply is passed explicitly.
  2. Retries each model (default 3 attempts, backoff) and classifies OK / transient / permanent.
  3. Only PERMANENT failures (400/401/402/403/404/410) are candidate removals. 429/5xx/timeouts
     are transient and may recover — they are reported, never acted on.
  4. max_tokens must be >= 16: several upstream models reject smaller values with a 400 that
     looks like a permanent model failure but is really a bad probe payload.

Usage:
    python3 audit_models.py                 # dry-run, report only
    python3 audit_models.py --json out.json # also write machine-readable results
    python3 audit_models.py --apply         # ONLY after reviewing a dry-run
"""
import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor

ROUTER = "http://127.0.0.1:20128/v1"
DB = os.path.expanduser("~/.9router/db/data.sqlite")

# Permanent: the model is not available to this credential/account. Safe to stop showing.
PERMANENT_CODES = {400, 401, 402, 403, 404, 410}
# Transient: the model may answer on a later attempt. Never act on these.
TRANSIENT_CODES = {408, 425, 429, 500, 502, 503, 504}

MAX_TOKENS = 64  # >= 16: smaller payloads 400 on models that clamp output (e.g. muse)
ATTEMPTS = 3


def api_key() -> str:
    key = os.environ.get("NINE_ROUTER_API_KEY", "")
    if key:
        return key
    with open(os.path.expanduser("~/.hermes/.env")) as fh:
        for line in fh:
            if line.startswith("NINE_ROUTER_API_KEY="):
                return line.strip().split("=", 1)[1].strip().strip('"').strip("'")
    return ""


KEY = api_key()


def fetch_models() -> list[str]:
    req = urllib.request.Request(f"{ROUTER}/models",
                                 headers={"Authorization": f"Bearer {KEY}"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        return sorted(m["id"] for m in json.load(resp)["data"])


def probe(mid: str) -> tuple[str, str, str]:
    """Return (model, verdict, detail). verdict is ok | transient | permanent."""
    body = json.dumps({
        "model": mid,
        "messages": [{"role": "user", "content": "Say OK"}],
        "max_tokens": MAX_TOKENS,
        "stream": False,
    }).encode()
    detail = ""
    for attempt in range(ATTEMPTS):
        req = urllib.request.Request(
            f"{ROUTER}/chat/completions", data=body,
            headers={"Content-Type": "application/json",
                     "Authorization": f"Bearer {KEY}"})
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                if resp.status == 200:
                    return mid, "ok", ""
                detail = f"HTTP {resp.status}"
        except urllib.error.HTTPError as exc:
            raw = ""
            try:
                raw = exc.read(400).decode("utf-8", "replace")
            except Exception:
                pass
            detail = f"HTTP {exc.code} {raw[:200]}"
            if exc.code in PERMANENT_CODES:
                return mid, "permanent", detail
        except Exception as exc:  # timeout, reset, DNS
            detail = f"{type(exc).__name__}: {exc}"
        if attempt < ATTEMPTS - 1:
            time.sleep(2 + 3 * attempt)
    return mid, "transient", detail


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true",
                    help="disable providers whose models are ALL permanent failures")
    ap.add_argument("--json", dest="json_path", default=None)
    args = ap.parse_args()

    try:
        ids = fetch_models()
    except Exception as exc:
        print(f"9router unreachable: {exc}")
        print("restart: launchctl kickstart -k gui/$(id -u)/com.9router.autostart")
        return 1

    print(f"probing {len(ids)} models (attempts={ATTEMPTS}, max_tokens={MAX_TOKENS})")
    results: dict[str, dict] = {}
    with ThreadPoolExecutor(max_workers=4) as pool:
        for i, (mid, verdict, detail) in enumerate(pool.map(probe, ids), 1):
            results[mid] = {"verdict": verdict, "detail": detail}
            if i % 25 == 0:
                print(f"  {i}/{len(ids)}", flush=True)

    ok = [m for m, v in results.items() if v["verdict"] == "ok"]
    transient = [m for m, v in results.items() if v["verdict"] == "transient"]
    permanent = [m for m, v in results.items() if v["verdict"] == "permanent"]

    by_provider: dict[str, dict[str, int]] = {}
    for mid, v in results.items():
        prov = mid.split("/")[0]
        bucket = by_provider.setdefault(prov, {"ok": 0, "transient": 0, "permanent": 0})
        bucket[v["verdict"]] += 1

    print(f"\nOK {len(ok)} | transient {len(transient)} | permanent {len(permanent)}")
    print("\nper provider (ok/transient/permanent):")
    for prov in sorted(by_provider):
        b = by_provider[prov]
        print(f"  {prov:14s} {b['ok']:3d}/{b['transient']:3d}/{b['permanent']:3d}")

    print("\nNOTE: 9router often wraps an upstream code inside a 503 body. Grep the detail\n"
          "      strings for the REAL code before treating a 503 as transient.\n"
          "      Also: a 401 on every model of one provider = dead credential, not dead models.")

    if args.json_path:
        with open(args.json_path, "w") as fh:
            json.dump({"generated_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
                       "total": len(ids), "ok": ok, "transient": transient,
                       "permanent": permanent, "by_provider": by_provider,
                       "results": results}, fh, indent=2)
        print(f"written: {args.json_path}")

    if not args.apply:
        print("\nDRY-RUN — nothing written. Review, then re-run with --apply if warranted.")
        return 0

    # --apply: only a provider with ZERO ok AND ZERO transient is safe to disable.
    import sqlite3
    con = sqlite3.connect(DB)
    disabled = []
    for prov, b in sorted(by_provider.items()):
        if b["ok"] == 0 and b["transient"] == 0 and b["permanent"] > 0:
            n = con.execute("UPDATE providerConnections SET isActive=0 WHERE provider=?",
                            (prov,)).rowcount
            disabled.append(f"{prov} ({n} connection(s))")
    con.commit()
    con.close()
    print("\ndisabled:" if disabled else "\nnothing disabled (no provider was fully dead)")
    for d in disabled:
        print(f"  {d}")
    print("restart: launchctl kickstart -k gui/$(id -u)/com.9router.autostart")
    return 0


if __name__ == "__main__":
    sys.exit(main())
