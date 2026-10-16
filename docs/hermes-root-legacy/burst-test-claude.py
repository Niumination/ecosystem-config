#!/usr/bin/env python3
"""Burst test for working Claude models."""
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

print("=== BURST TEST FOR TOP CLAUDE MODELS ===\n")

ENV = Path.home() / '.hermes' / '.env'
env = load_env(ENV)
key = env.get('NINE_ROUTER_API_KEY', '')
UA = 'hermes-agent/0.19.0'

if not key:
    print("❌ No API key"); sys.exit(1)

base = 'http://localhost:20128/v1'

# Test these proven models
test_models = [
    'kr/claude-haiku-4.5',
    'kr/claude-sonnet-4',
    'ag/claude-opus-4-6-thinking',
    'ag/claude-sonnet-4-6',
]

for model in test_models:
    print(f"Testing {model}...")
    results = []
    
    for i in range(8):  # 8 burst requests
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
                if i < 3 or i == 7:  # Show first 3 and last
                    print(f"  {i+1}/8: ✅ {ms}ms")
        except Exception as e:
            results.append(('FAIL', 0))
            print(f"  {i+1}/8: ❌ {type(e).__name__}")
        
        time.sleep(0.05)  # 50ms delay
    
    # Calculate stats
    ok_count = sum(1 for s, _ in results if s == 'OK')
    ms_values = [ms for s, ms in results if s == 'OK']
    avg_ms = sum(ms_values) / len(ms_values) if ms_values else 0
    
    # Burst limit check (>= 9/10 is long limit)
    burst_score = ok_count / len(results) * 10
    
    print(f"  Result: {ok_count}/8 ({burst_score:.1f}/10 burst) | Avg: {avg_ms:.0f}ms")
    print(f"  Verdict: {'✅ LONG LIMIT' if burst_score >= 9 else '⚠️ PARTIAL' if burst_score >= 7 else '❌ UNSTABLE'}\n")
