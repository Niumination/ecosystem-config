#!/usr/bin/env python3
"""Test kr/ prefix models - might have kimi-like models."""
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

# Test some kr/ models that might be good alternatives
test_models = [
    'kr/deepseek-3.2',
    'kr/glm-5',
    'kr/minimax-m2.5',
    'kr/qwen3-coder-next',
    'kr/claude-haiku-4.5',
    'kr/claude-sonnet-4',
]

base = 'http://localhost:20128/v1'

print("=== TESTING KR/ PREFIX MODELS ===\n")

results = []
for model in test_models:
    body = json.dumps({'model': model, 'messages': [{'role': 'user', 'content': 'OK'}], 'max_tokens': 5, 'stream': False}).encode()
    req = urllib.request.Request(base+'/chat/completions', data=body, method='POST')
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
ok = [m for m,s,_,_ in results if s=='OK']
print(f"Working: {len(ok)}/{len(test_models)}")
for m in ok:
    print(f"  - {m}")
