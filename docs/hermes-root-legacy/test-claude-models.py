#!/usr/bin/env python3
"""Test all available Claude models to find the best opus/sonnet variants."""
import json, urllib.request, sys, time
from pathlib import Path
import concurrent.futures

def load_env(path):
    d = {}
    if not path.exists(): return d
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith('#') or '=' not in line: continue
        k, v = line.split('=', 1)
        d[k.strip()] = v.strip().strip('"').strip("'")
    return d

print("=== TESTING CLAUDE MODELS ===\n")

ENV = Path.home() / '.hermes' / '.env'
env = load_env(ENV)
key = env.get('NINE_ROUTER_API_KEY', '')
UA = 'hermes-agent/0.19.0'

if not key:
    print("❌ No API key"); sys.exit(1)

base = 'http://localhost:20128/v1'

# Get all models
req = urllib.request.Request(
    base + '/models',
    headers={'Authorization': f'Bearer {key}', 'User-Agent': UA}
)
with urllib.request.urlopen(req, timeout=10) as r:
    data = json.load(r)
    models = [m['id'] for m in data['data']]

# Filter Claude models
claude_models = [m for m in models if 'claude' in m.lower()]
print(f"Found {len(claude_models)} Claude models:\n")
for m in sorted(claude_models):
    print(f"  - {m}")

print(f"\nTesting each model...\n")

# Test each model
results = []
def test_model(model):
    body = json.dumps({
        'model': model,
        'messages': [{'role': 'user', 'content': 'Say OK'}],
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
        with urllib.request.urlopen(req, timeout=10) as r:
            raw = r.read().decode()
            if 'data:' in raw:
                parts = []
                for ln in raw.splitlines():
                    if ln.strip().startswith('data:'):
                        try:
                            c = json.loads(ln[5:].strip()).get('choices',[{}])[0].get('delta',{}).get('content','')
                            if c: parts.append(c)
                        except: pass
                resp = ''.join(parts) if parts else '(empty)'
            else:
                d = json.loads(raw)
                resp = d.get('choices',[{}])[0].get('message',{}).get('content','')[:30]
            ms = int((time.time()-t0)*1000)
            return (model, 'OK', ms, resp)
    except Exception as e:
        return (model, 'FAIL', 0, str(e)[:50])

# Run tests
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(test_model, m) for m in claude_models]
    for future in concurrent.futures.as_completed(futures):
        result = future.result()
        results.append(result)
        model, status, ms, resp = result
        icon = "✅" if status == 'OK' else "❌"
        print(f"{icon} {ms}ms  {model}")

# Summary
print(f"\n=== SUMMARY ===")
ok_models = [(m, ms, r) for m, s, ms, r in results if s == 'OK']
fail_models = [(m, ms, r) for m, s, ms, r in results if s != 'OK']

print(f"✅ Working: {len(ok_models)}/{len(claude_models)}")
print(f"❌ Failed: {len(fail_models)}/{len(claude_models)}\n")

if ok_models:
    print("=== WORKING CLAUDE MODELS (sorted by speed) ===\n")
    for model, ms, resp in sorted(ok_models, key=lambda x: x[1]):
        print(f"⚡ {ms}ms  {model}")
