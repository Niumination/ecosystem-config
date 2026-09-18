#!/usr/bin/env python3
"""
Model Status Report Generator.
Reads the latest model-status JSON and generates a concise Telegram-friendly report.
"""

import json
from pathlib import Path

OUTPUT_DIR = Path.home() / ".hermes" / "cron" / "output"

def main():
    files = sorted([f for f in OUTPUT_DIR.glob("model-status-*.json") if "cache" not in f.name])
    
    d = None
    latest_file = None
    
    if files:
        latest_file = files[-1]
        with open(latest_file) as f:
            d = json.load(f)
    else:
        cache = OUTPUT_DIR / "model-status-cache.json"
        if cache.exists():
            with open(cache) as f:
                cache_data = json.load(f)
            d = cache_data.get("report", cache_data)
            latest_file = cache
    
    if not d:
        print("No model status report found.")
        return
    
    s = d.get('summary', {})
    ts = d.get('timestamp', '')[:16].replace('T', ' ')
    
    lines = []
    lines.append("📊 MODEL STATUS REPORT")
    lines.append(f"⏰ {ts} WIB")
    lines.append("")
    lines.append(f"• OpenRouter: {s.get('openrouter_free_available', 0)} free models available")
    lines.append(f"• 9router: {s.get('9router_total', 0)} models")
    lines.append(f"• Hermes Config: {s.get('critical_ok', 0)} OK, {s.get('critical_failed', 0)} failed, {s.get('critical_skipped', 0)} skipped")
    lines.append("")
    
    if d.get('issues'):
        lines.append("⚠️ ISSUES:")
        for i in d['issues']:
            lines.append(f"  • {i}")
        lines.append("")
    
    if d.get('recommendations'):
        lines.append("💡 REKOMENDASI:")
        for r in d['recommendations']:
            lines.append(f"  • {r}")
        lines.append("")
    
    free = d.get('providers', {}).get('openrouter', {}).get('free_models', [])
    if free:
        lines.append("🆓 FREE MODELS (OpenRouter, top 10):")
        for m in free[:10]:
            lines.append(f"  • {m['id']}")
        lines.append("")
    
    probes = d.get('probe_results', {})
    if probes:
        lines.append("🔍 CRITICAL MODEL STATUS:")
        for model, result in probes.items():
            status = result['status']
            if status == 'ok':
                icon = '✅'
            elif status == 'internal_route':
                icon = '🔄'
            elif status in ('internal_namespace', 'no_key', 'no_base_url'):
                icon = '⏭️'
            else:
                icon = '❌'
            lines.append(f"  {icon} {model}: {status} ({result['latency_ms']:.0f}ms)")
    
    report = "\n".join(lines)
    print(report)
    
    if latest_file:
        report_file = OUTPUT_DIR / f"model-status-short-{latest_file.stem.split('-', 2)[-1]}.txt"
        with open(report_file, "w") as f:
            f.write(report)

if __name__ == "__main__":
    main()
