#!/usr/bin/env python3
"""Test kimi models with different ID formats."""
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

# Try different possible kimi model IDs
test_models = [
    # From models list (ollama prefix)
    'ollama/kimi-k2.5',
    'ollama/glm-5',
    # Nvidia prefix
    'nvidia/moonshotai/kimi-k2.6',
    # Direct
    'kimi-k2.5',
    'kimi-k2.6',
    'kimi-k3',
    # With provider prefix
    '9router/kimi-k2.5',
]

base = 'http://localhost:20128/v1'

print("=== TESTING KIMI MODEL VARIANTS ===\n")

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
            print(f"✅ {ms}ms  {model} -> {resp}")
    except urllib.error.HTTPError as e:
        print(f"❌ HTTP {e.code}  {model}")
    except Exception as e:
        print(f"❌ {type(e).__name__}  {model}")
