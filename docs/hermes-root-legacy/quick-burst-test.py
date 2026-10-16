#!/usr/bin/env python3
"""Quick burst test for top Claude models."""
import json, urllib.request, sys, time
from pathlib import Path

def load_env(path):
    d = {}
    if not path.exists(): return d
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith('#') or '=' not in line: continue
        k, v = line.split('=', 1)
        d[k.strip()] = v.strip().strip('"').strip("'")
    return d

print("=== QUICK BURST TEST ===\n")

ENV = Path.home() / '.hermes' / '.env'
env = load_env(ENV)
key = env.get('NINE_ROUTER_API_KEY', '')
UA = 'hermes-agent/0.19.0'

if not key:
    print("❌ No API key"); sys.exit(1)

base = 'http://localhost:20128/v1'

# Test the best 3 models
test_models = [
    ('kr/claude-haiku-4.5', 'Fast'),
    ('kr/claude-sonnet-4', 'Balanced'),
    ('ag/claude-opus-4-6-thinking', 'Opus'),
]

for model, desc in test_models:
    print(f"Testing {model} ({desc})...")
    results = []
    
    for i in range(10):
        body = json.dumps({
            'model': model,
            'messages': [{'role': 'user', 'content': 'OK'}],
            'max_tokens': 5
        }).encode()
        req = urllib.request.Request(
            base + '/chat/completions',
            data=body,
            method='POST'
        )
        req.add_header('Content-Type', 'application/json')
        req.add_header('Authorization', f'Bearer {key}')
        req.add_header('User-Agent', UA)
        
        try:
            t0 = time.time()
            with urllib.request.urlopen(req, timeout=15) as r:
                raw = r.read().decode()
                ms = int((time.time()-t0)*1000)
                results.append(('OK', ms))
        except:
            results.append(('FAIL', 0))
        
        time.sleep(0.05)
    
    ok_count = sum(1 for s, _ in results if s == 'OK')
    ms_values = [ms for s, ms in results if s == 'OK']
    avg_ms = sum(ms_values) / len(ms_values) if ms_values else 0
    
    status = '✅ LONG LIMIT' if ok_count >= 9 else '⚠️ PARTIAL' if ok_count >= 7 else '❌ UNSTABLE'
    print(f"  Result: {ok_count}/10 ({status}) | Avg: {avg_ms:.0f}ms\n")
