#!/usr/bin/env python3
"""Test ALL available models to find best alternatives for kiro."""
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

print("=== MODEL PERFORMANCE TEST ===\n")

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

print(f"Testing {len(models)} models...\n")

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
        with urllib.request.urlopen(req, timeout=8) as r:
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

# Run tests with limited parallelism
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(test_model, m) for m in models]
    for i, future in enumerate(concurrent.futures.as_completed(futures), 1):
        result = future.result()
        model, status, ms, resp = result
        results.append(result)
        if i % 10 == 0:
            print(f"Progress: {i}/{len(models)}")

# Sort results
ok_models = [(m, ms, r) for m, s, ms, r in results if s == 'OK']
fail_models = [(m, ms, r) for m, s, ms, r in results if s != 'OK']

print(f"\n=== RESULTS ===")
print(f"✅ Working: {len(ok_models)}/{len(models)}")
print(f"❌ Failed: {len(fail_models)}/{len(models)}\n")

# Group by prefix
print("=== WORKING MODELS BY PREFIX ===\n")
by_prefix = {}
for model, ms, resp in ok_models:
    prefix = model.split('/')[0]
    by_prefix.setdefault(prefix, []).append((model, ms, resp))

for prefix in sorted(by_prefix.keys()):
    items = by_prefix[prefix]
    avg_ms = sum(ms for _, ms, _ in items) / len(items)
    print(f"{prefix}: {len(items)} models (avg {avg_ms:.0f}ms)")
    
    # Show fastest 3
    sorted_items = sorted(items, key=lambda x: x[1])[:3]
    for model, ms, resp in sorted_items:
        print(f"  ⚡ {ms}ms  {model}")
    print()

print("\n=== TOP 10 FASTEST MODELS ===\n")
fastest = sorted(ok_models, key=lambda x: x[1])[:10]
for i, (model, ms, resp) in enumerate(fastest, 1):
    print(f"{i}. {ms}ms  {model}")

# Save results
output = {
    'total': len(models),
    'working': len(ok_models),
    'failed': len(fail_models),
    'by_prefix': {p: len(items) for p, items in by_prefix.items()},
    'fastest': [{'model': m, 'ms': ms} for m, ms, _ in fastest]
}
(Path.home() / '.hermes' / 'model-performance-test.json').write_text(json.dumps(output, indent=2))
print(f"\n💾 Results saved to ~/.hermes/model-performance-test.json")
