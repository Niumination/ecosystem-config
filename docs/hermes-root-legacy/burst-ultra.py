#!/usr/bin/env python3
"""Ultra-fast burst: 4 bursts per candidate, 3s timeout."""
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

def chat_once(base, key, model):
    body = json.dumps({'model': model, 'messages': [{'role': 'user', 'content': 'OK'}], 'max_tokens': 5, 'stream': False}).encode()
    req = urllib.request.Request(base+'/chat/completions', data=body, method='POST')
    req.add_header('Content-Type', 'application/json')
    req.add_header('Authorization', f'Bearer {key}')
    req.add_header('User-Agent', UA)
    try:
        t0 = time.time()
        with urllib.request.urlopen(req, timeout=3) as r:
            raw = r.read().decode()
            if 'data:' in raw:
                parts = []
                for ln in raw.splitlines():
                    if ln.strip().startswith('data:'):
                        try:
                            c = json.loads(ln[5:].strip()).get('choices',[{}])[0].get('delta',{}).get('content','')
                            if c: parts.append(c)
                        except: pass
                return ('OK', int((time.time()-t0)*1000))
            data = json.loads(raw)
            return ('OK', int((time.time()-t0)*1000))
    except urllib.error.HTTPError as e:
        return ('ERR', e.code)
    except Exception:
        return ('ERR', 0)

top = [
    ('9router',       'NINE_ROUTER_API_KEY',  'http://localhost:20128/v1',
     ['ag/gemini-3.5-flash-extra-low', 'ag/gemini-3-flash-agent',
      'gh/gpt-4o-mini', 'ag/gemini-3.7-flash-low']),
    ('openrouter',    'OPENROUTER_API_KEY',   'https://openrouter.ai/api/v1',
     ['nvidia/nemotron-3-super-120b-a12b:free',
      'google/gemma-4-26b-a4b-it:free']),
    ('opencode-zen',  'OPENCODE_ZEN_API_KEY', 'https://opencode.ai/zen/v1',
     ['big-pickle', 'hy3-free']),
]

B = 4
print(f"Burst test ({B} bursts each):\n")
for pname, kenv, base, models in top:
    key = env.get(kenv,'')
    if not key: print(f"[{pname}] NO KEY\n"); continue
    print(f"--- {pname} ---")
    for m in models:
        ok = sum(1 for _ in range(B) if chat_once(base, key, m)[0]=='OK')
        print(f"  {ok}/{B}  {m}")
