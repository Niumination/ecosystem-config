#!/usr/bin/env python3
"""Test kiro model kr/claude-opus-5 on 9router."""
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

print("=== TESTING KIRO MODEL: kr/claude-opus-5 ===\n")

ENV = Path.home() / '.hermes' / '.env'
env = load_env(ENV)
key = env.get('NINE_ROUTER_API_KEY', '')
UA = 'hermes-agent/0.19.0'

if not key:
    print("❌ No API key"); sys.exit(1)

base = 'http://localhost:20128/v1'
model = 'kr/claude-opus-5'

# Test 1: Single chat completion
print("Test 1: Single Chat Completion")
body = json.dumps({
    'model': model,
    'messages': [{'role': 'user', 'content': 'Hello, say OK'}],
    'max_tokens': 10
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
        if 'data:' in raw:
            parts = []
            for ln in raw.splitlines():
                if ln.strip().startswith('data:'):
                    try:
                        c = json.loads(ln[5:].strip()).get('choices',[{}])[0].get('delta',{}).get('content','')
                        if c: parts.append(c)
                    except: pass
            resp = ''.join(parts) if parts else '(empty SSE)'
        else:
            d = json.loads(raw)
            resp = d.get('choices',[{}])[0].get('message',{}).get('content','')
        ms = int((time.time()-t0)*1000)
        print(f"✅ SUCCESS: {ms}ms")
        print(f"Response: {resp}")
except Exception as e:
    print(f"❌ FAILED: {type(e).__name__}: {e}")
    sys.exit(1)

# Test 2: Burst test (5 requests)
print(f"\nTest 2: Burst Test (5 requests)")
results = []
for i in range(5):
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
            print(f"  {i+1}/5: ✅ {ms}ms")
    except Exception as e:
        results.append(('FAIL', 0))
        print(f"  {i+1}/5: ❌ {type(e).__name__}")
    time.sleep(0.1)  # 100ms delay

# Summary
ok_count = sum(1 for s, _ in results if s == 'OK')
ms_values = [ms for s, ms in results if s == 'OK']
avg_ms = sum(ms_values) / len(ms_values) if ms_values else 0

print(f"\n=== SUMMARY ===")
print(f"Model: {model}")
print(f"Burst Success: {ok_count}/5 ({100*ok_count/5:.0f}%)")
print(f"Avg Latency: {avg_ms:.0f}ms")
print(f"Status: {'✅ WORKING' if ok_count >= 4 else '⚠️ PARTIAL' if ok_count >= 1 else '❌ FAILED'}")
