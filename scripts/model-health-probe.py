#!/usr/bin/env python3
"""Model Health Probe — check latency & availability of models in 9router catalog."""

import json
import time
import sys
import os
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path

CATALOG_URL = "http://localhost:20128/v1/models"
CHAT_URL = "http://localhost:20128/v1/chat/completions"

# Read API key from environment or .env
API_KEY = os.environ.get("NINE_ROUTER_API_KEY", "")
if not API_KEY or API_KEY == "***":
    env_file = Path.home() / ".hermes" / ".env"
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            if line.startswith("NINE_ROUTER_API_KEY="):
                API_KEY = line.split("=", 1)[1].strip()
                break

if not API_KEY or API_KEY == "***":
    print("ERROR: NINE_ROUTER_API_KEY not found in environment or ~/.hermes/.env")
    sys.exit(1)

TEST_PROMPT = "Reply with: OK"

def load_models():
    """Load model list from 9router catalog."""
    try:
        req = urllib.request.Request(CATALOG_URL)
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
        return [m["id"] for m in data.get("data", [])]
    except Exception as e:
        print(f"ERROR: Failed to load catalog: {e}", file=sys.stderr)
        return []

def probe_model(model_id):
    """Probe a single model and return metrics."""
    payload = {
        "model": model_id,
        "messages": [{"role": "user", "content": TEST_PROMPT}],
        "max_tokens": 10,
        "temperature": 0,
        "stream": False
    }
    
    body = json.dumps(payload).encode()
    req = urllib.request.Request(
        CHAT_URL,
        data=body,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}"
        }
    )
    
    start = time.time()
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            resp_body = resp.read().decode()
            elapsed = (time.time() - start) * 1000  # ms
            
            # Handle potential streaming response (take first JSON line)
            try:
                resp_data = json.loads(resp_body)
            except json.JSONDecodeError:
                # Try first line only (streaming format)
                first_line = resp_body.split('\n')[0].strip()
                if first_line.startswith('data: '):
                    first_line = first_line[6:]
                resp_data = json.loads(first_line)
            
            usage = resp_data.get("usage", {})
            output_tokens = usage.get("completion_tokens", 0)
            return {
                "model": model_id,
                "status": "ok",
                "latency_ms": round(elapsed, 1),
                "tokens": output_tokens,
                "tps": round(output_tokens / (elapsed / 1000), 1) if elapsed > 0 else 0
            }
    except urllib.error.HTTPError as e:
        elapsed = (time.time() - start) * 1000
        return {
            "model": model_id,
            "status": f"http_{e.code}",
            "latency_ms": round(elapsed, 1),
            "tokens": 0,
            "tps": 0
        }
    except Exception as e:
        elapsed = (time.time() - start) * 1000
        return {
            "model": model_id,
            "status": "error",
            "latency_ms": round(elapsed, 1),
            "tokens": 0,
            "tps": 0,
            "error": str(e)[:100]
        }

def main():
    now = datetime.now()
    print(f"Model Health Probe — {now.strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    models = load_models()
    if not models:
        print("No models found or catalog unreachable.")
        return
    
    print(f"Total models in catalog: {len(models)}")
    print("Probing... (this may take a few minutes)\n")
    
    results = []
    for i, model_id in enumerate(models, 1):
        result = probe_model(model_id)
        results.append(result)
        
        status_icon = "OK" if result["status"] == "ok" else "FAIL"
        print(f"  [{i:3d}/{len(models)}] {status_icon} {model_id}: {result['latency_ms']:.0f}ms ({result['status']})")
    
    ok_results = [r for r in results if r["status"] == "ok"]
    failed_results = [r for r in results if r["status"] != "ok"]
    
    # Categorize failures
    capacity_errors = [r for r in failed_results if "503" in r["status"]]
    auth_errors = [r for r in failed_results if "401" in r["status"] or "403" in r["status"]]
    timeout_errors = [r for r in failed_results if r["latency_ms"] > 29000]
    parse_errors = [r for r in failed_results if "Extra data" in r.get("error", "")]
    other_errors = [r for r in failed_results if r not in capacity_errors + auth_errors + timeout_errors + parse_errors]
    
    print(f"\n{'=' * 60}")
    print(f"SUMMARY: {len(ok_results)} OK, {len(failed_results)} failed, {len(results)} total")
    
    if ok_results:
        sorted_ok = sorted(ok_results, key=lambda x: x["latency_ms"])
        print(f"\nTOP 10 BY SPEED:")
        for i, r in enumerate(sorted_ok[:10], 1):
            print(f"  {i:2d}. {r['model']:<45} {r['latency_ms']:>6.0f}ms  {r['tps']:.0f} tps")
    
    print(f"\nFAILURE BREAKDOWN:")
    print(f"  503 (capacity/rate limit): {len(capacity_errors)}")
    print(f"  401/403 (auth error):     {len(auth_errors)}")
    print(f"  Timeout (>30s):           {len(timeout_errors)}")
    print(f"  Parse error (streaming):  {len(parse_errors)}")
    print(f"  Other errors:             {len(other_errors)}")
    
    if other_errors:
        print(f"\nISSUES (showing up to 10):")
        for r in other_errors[:10]:
            err = r.get("error", r["status"])
            print(f"  FAIL {r['model']:<45} {err[:50]}")
    
    output_dir = Path.home() / ".hermes" / "cron" / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output = {
        "timestamp": now.isoformat(),
        "total": len(results),
        "ok": len(ok_results),
        "failed": len(failed_results),
        "results": results
    }
    
    output_file = output_dir / f"model-probe-{now.strftime('%Y%m%d-%H%M%S')}.json"
    with open(output_file, "w") as f:
        json.dump(output, f, indent=2)
    
    print(f"\nResults saved to: {output_file}")

if __name__ == "__main__":
    main()
