#!/usr/bin/env python3
"""
Model Status Checker — Hybrid 3-Tier approach
Tier 1: Static data from public APIs (0 token)
Tier 2: Minimal probe for critical models only
Tier 3: Full report generation

Usage: python3 scripts/model_status_checker.py
Output: ~/.hermes/cron/output/model-status-YYYYMMDD-HHMMSS.json + stdout
"""

import json
import time
import os
import sys
import urllib.request
import urllib.error
from datetime import datetime, timedelta
from pathlib import Path

HERMES_HOME = Path.home() / ".hermes"
CONFIG_FILE = HERMES_HOME / "config.yaml"
ENV_FILE = HERMES_HOME / ".env"
OUTPUT_DIR = HERMES_HOME / "cron" / "output"
CACHE_FILE = OUTPUT_DIR / "model-status-cache.json"
API_TIMEOUT = 10
PROBE_TIMEOUT = 15
CACHE_TTL = 24

OPENROUTER_MODELS_URL = "https://openrouter.ai/api/v1/models"
ROUTER9_LOCAL_URL = "http://localhost:20128/v1/models"

HERMES_PROVIDERS = {
    "9router": "http://localhost:20128/v1",
    "agentrouter": "https://agentrouter.org/v1",
    "huancheng": "https://api.hcnsec.cn/v1",
    "nous": "http://localhost:20128/v1",
}

def load_env_vars():
    keys = {}
    for key in ["NINE_ROUTER_API_KEY", "AGENTROUTER_API_KEY", "HUANCHENG_API_KEY", "OPENROUTER_API_KEY"]:
        val = os.environ.get(key, "")
        if val:
            keys[key] = val
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text().splitlines():
            line = line.strip()
            if line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            k = k.strip()
            v = v.strip().strip('"').strip("'")
            if k not in keys:
                keys[k] = v
    return keys

def load_hermes_config():
    config = {"default_model": None, "default_provider": None, "providers": {}, "channel_overrides": {}}
    if not CONFIG_FILE.exists():
        return config
    try:
        import yaml
        with open(CONFIG_FILE) as f:
            data = yaml.safe_load(f)
        if not data:
            return config
        model_section = data.get("model", {})
        if model_section:
            config["default_model"] = model_section.get("default")
            config["default_provider"] = model_section.get("provider")
        providers = data.get("providers", {})
        for name, pdata in providers.items():
            config["providers"][name] = {"base_url": pdata.get("base_url", ""), "key_env": pdata.get("key_env", "")}
        platforms = data.get("platforms", {})
        telegram = platforms.get("telegram", {})
        channel_overrides = telegram.get("channel_overrides", {})
        for channel, cdata in channel_overrides.items():
            config["channel_overrides"][channel] = {"model": cdata.get("model"), "provider": cdata.get("provider")}
        cron = data.get("cron", {})
        if cron:
            config["cron_model"] = cron.get("model")
            config["cron_provider"] = cron.get("model_provider") or cron.get("provider")
    except ImportError:
        pass
    except Exception as e:
        print(f"WARNING: Could not parse config.yaml: {e}", file=sys.stderr)
    return config

def fetch_json(url, timeout=API_TIMEOUT):
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode())
    except Exception:
        return None

def load_openrouter_models():
    data = fetch_json(OPENROUTER_MODELS_URL)
    if not data:
        return []
    models = data.get("data", [])
    result = []
    for m in models:
        pricing = m.get("pricing", {})
        is_free = pricing.get("prompt") == "0" and pricing.get("completion") == "0"
        result.append({"id": m.get("id", ""), "name": m.get("name", ""), "provider": "openrouter", "is_free": is_free, "context_length": m.get("context_length", 0)})
    return result

def load_9router_models():
    data = fetch_json(ROUTER9_LOCAL_URL)
    if not data:
        return []
    models = data.get("data", [])
    result = []
    for m in models:
        mid = m.get("id", "")
        ns = mid.split("/")[0] if "/" in mid else "unknown"
        result.append({"id": mid, "name": mid, "provider": "9router", "namespace": ns, "is_free": None})
    return result

def probe_model_quick(model_id, base_url, api_key, timeout=PROBE_TIMEOUT):
    payload = {"model": model_id, "messages": [{"role": "user", "content": "OK"}], "max_tokens": 1, "temperature": 0, "stream": False}
    body = json.dumps(payload).encode()
    req = urllib.request.Request(f"{base_url}/chat/completions", data=body, headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"})
    start = time.time()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            resp.read()
            elapsed = (time.time() - start) * 1000
            return {"status": "ok", "latency_ms": round(elapsed, 1)}
    except urllib.error.HTTPError as e:
        elapsed = (time.time() - start) * 1000
        return {"status": f"http_{e.code}", "latency_ms": round(elapsed, 1)}
    except Exception as e:
        elapsed = (time.time() - start) * 1000
        return {"status": "error", "latency_ms": round(elapsed, 1), "error": str(e)[:50]}

def main():
    now = datetime.now()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    config = load_hermes_config()
    keys = load_env_vars()
    report = {"timestamp": now.isoformat(), "providers": {}, "hermes_config": config, "issues": [], "recommendations": []}
    
    print("Tier 1: Collecting static data...")
    or_models = load_openrouter_models()
    or_free = [m for m in or_models if m["is_free"]]
    report["providers"]["openrouter"] = {"total": len(or_models), "free": len(or_free), "free_models": [{"id": m["id"], "name": m["name"]} for m in or_free]}
    print(f"  OpenRouter: {len(or_models)} total, {len(or_free)} free")
    
    r9_models = load_9router_models()
    r9_ns = {}
    for m in r9_models:
        r9_ns.setdefault(m["namespace"], []).append(m["id"])
    report["providers"]["9router"] = {"total": len(r9_models), "namespaces": {k: len(v) for k, v in r9_ns.items()}, "sample": [m["id"] for m in r9_models[:10]]}
    print(f"  9router: {len(r9_models)} total, namespaces: {list(r9_ns.keys())}")
    
    critical_models = set()
    if config["default_model"]:
        critical_models.add((config["default_model"], config["default_provider"]))
    for ch, ov in config["channel_overrides"].items():
        if ov["model"]:
            critical_models.add((ov["model"], ov["provider"]))
    if config.get("cron_model"):
        critical_models.add((config["cron_model"], config.get("cron_provider", "9router")))
    report["critical_models"] = [{"model": m, "provider": p} for m, p in critical_models]
    print(f"\nCritical models from config: {len(critical_models)}")
    
    print("\nTier 2: Probing critical models...")
    nine_router_key = keys.get("NINE_ROUTER_API_KEY", "")
    probe_results = {}
    
    for model_id, provider in critical_models:
        if model_id.startswith("explabs/"):
            probe_results[model_id] = {"status": "internal_namespace", "latency_ms": 0}
            print(f"  SKIP {model_id} (Hermes internal namespace)")
            continue
        probe_provider = "9router" if provider == "nous" else provider
        base_url = HERMES_PROVIDERS.get(probe_provider, "")
        if not base_url:
            probe_results[model_id] = {"status": "no_base_url", "latency_ms": 0}
            continue
        key = nine_router_key
        if not key:
            probe_results[model_id] = {"status": "no_key", "latency_ms": 0}
            print(f"  SKIP {model_id} (no API key)")
            continue
        result = probe_model_quick(model_id, base_url, key)
        probe_results[model_id] = result
        icon = "OK" if result["status"] == "ok" else "FAIL"
        print(f"  {icon} {model_id} via {probe_provider}: {result['latency_ms']:.0f}ms ({result['status']})")
    
    report["probe_results"] = probe_results
    
    print("\nTier 3: Generating recommendations...")
    ok_critical = [m for m, r in probe_results.items() if r["status"] == "ok"]
    failed_critical = [m for m, r in probe_results.items() if r["status"] not in ("ok", "internal_namespace", "no_key", "no_base_url")]
    skipped = [m for m, r in probe_results.items() if r["status"] in ("internal_namespace", "no_key", "no_base_url")]
    
    report["summary"] = {"critical_ok": len(ok_critical), "critical_failed": len(failed_critical), "critical_skipped": len(skipped), "openrouter_free_available": len(or_free), "9router_total": len(r9_models)}
    if failed_critical:
        report["issues"].append(f"{len(failed_critical)} critical model(s) failed: {', '.join(failed_critical[:5])}")
    if config["default_model"] and config["default_model"] in ok_critical:
        report["recommendations"].append(f"Default model '{config['default_model']}' is healthy — no change needed")
    elif config["default_model"] and config["default_model"] in failed_critical:
        report["recommendations"].append(f"WARNING: Default model '{config['default_model']}' is failing — consider switching")
    if or_free:
        report["recommendations"].append(f"{len(or_free)} free OpenRouter models available as fallback")
    
    report_file = OUTPUT_DIR / f"model-status-{now.strftime('%Y%m%d-%H%M%S')}.json"
    with open(report_file, "w") as f:
        json.dump(report, f, indent=2, default=str)
    cache_data = {"timestamp": now.isoformat(), "expires": (now + timedelta(hours=CACHE_TTL)).isoformat(), "report": report}
    with open(CACHE_FILE, "w") as f:
        json.dump(cache_data, f, indent=2, default=str)
    
    print("\n" + "=" * 60)
    print("📊 MODEL STATUS REPORT")
    print(f"⏰ {now.strftime('%Y-%m-%d %H:%M:%S WIB')}")
    print("=" * 60)
    print()
    print(f"OpenRouter: {len(or_free)} free / {len(or_models)} total")
    print(f"9router: {len(r9_models)} total ({', '.join(f'{k}:{v}' for k, v in r9_ns.items())})")
    print()
    print(f"✅ Critical OK: {len(ok_critical)}")
    if failed_critical:
        print(f"❌ Critical Failed: {len(failed_critical)}")
        for m in failed_critical:
            r = probe_results[m]
            print(f"   • {m}: {r['status']} ({r['latency_ms']:.0f}ms)")
    if skipped:
        print(f"⏭️  Skipped: {len(skipped)}")
    print()
    if report["recommendations"]:
        for rec in report["recommendations"]:
            print(f"💡 {rec}")
    print()
    print(f"📁 Saved: {report_file}")

if __name__ == "__main__":
    main()
