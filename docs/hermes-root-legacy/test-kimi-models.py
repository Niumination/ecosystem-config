#!/usr/bin/env python3
"""Test all Kimi models on 9router for free tier availability."""
import json, os, time, urllib.error, urllib.request
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

ENV = Path.home() / '.hermes' / '.env'
env = load_env(ENV)
UA = 'hermes-agent/0.19.0'
key = env.get('NINE_ROUTER_API_KEY', '')

if not key:
    print("❌ No NINE_ROUTER_API_KEY found"); exit(1)

# All kimi models from 9router
kimi_models = [
    'kimi/kimi-k3',
    'kimi/k3',
    'kimi/kimi-for-coding',
    'kimi/kimi-for-coding-highspeed',
    'kimi/kimi-k2.7-code',
    'kimi/kimi-k2.7-code-highspeed',
    'kimi/kimi-k2.6',
    'kimi/kimi-k2.5',
    'kimi/kimi-k2.5-thinking',
    'kimi/kimi-latest',
]

base = 'http://localhost:20128/v1'

print("=== KIMI MODELS ON 9ROUTER ===\n")

results = []
for model in kimi_models:
    body = json.dumps({'model': model, 'messages': [{'role': 'user', 'content': 'OK'}], 'max_tokens': 5, 'stream': False}).encode()
    req = urllib.request.Request(base+'/chat/completions', data=body, method='POST')
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
                resp = ''.join(parts) if parts else '(empty SSE)'
            else:
                data = json.loads(raw)
                resp = data.get('choices',[{}])[0].get('message',{}).get('content','')[:40]
            ms = int((time.time()-t0)*1000)
            results.append((model, 'OK', ms, resp))
            print(f"✅ {ms}ms  {model}")
    except urllib.error.HTTPError as e:
        results.append((model, 'ERR', e.code, e.reason))
        print(f"❌ HTTP {e.code}  {model}")
    except Exception as e:
        results.append((model, 'ERR', 0, str(e)[:50]))
        print(f"❌ {type(e).__name__}  {model}")

print("\n=== SUMMARY ===")
ok_models = [m for m, s, _, _ in results if s == 'OK']
err_models = [m for m, s, _, _ in results if s == 'ERR']

print(f"✅ Working: {len(ok_models)}/{len(kimi_models)}")
for m in ok_models:
    print(f"   - {m}")

print(f"\n❌ Failed: {len(err_models)}/{len(kimi_models)}")
for m in err_models:
    status = next((s for mod, s, _, _ in results if mod == m), '?')
    print(f"   - {m} ({status})")

# Check if there's a pattern
print("\n=== ANALYSIS ===")
print(f"Total kimi models on 9router: {len(kimi_models)}")
print(f"Working: {len(ok_models)} ({100*len(ok_models)/len(kimi_models):.0f}%)")
print(f"Failed: {len(err_models)} ({100*len(err_models)/len(kimi_models):.0f}%)")
