#!/usr/bin/env python3
"""
Rapid single-chat probe per candidate model across multiple providers.
Usage: python3 rapid-probe.py
Output: table of provider/model/latency_ms/status
"""
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

def probe(base, key, model):
    body = json.dumps({
        'model': model, 'messages': [{'role': 'user', 'content': 'OK'}],
        'max_tokens': 5, 'stream': False
    }).encode()
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
                return int((time.time()-t0)*1000), 'OK'
            data = json.loads(raw)
            return int((time.time()-t0)*1000), 'OK'
    except urllib.error.HTTPError as e:
        return e.code, f'HTTP_{e.code}'
    except Exception as e:
        return 0, f'{type(e).__name__}'

# Candidates from 29 Ags scan
candidates = [
    # (provider_name, key_env, base_url, model)
    ('9router', 'NINE_ROUTER_API_KEY', 'http://localhost:20128/v1', 'ag/gemini-3.5-flash-extra-low'),
    ('9router', 'NINE_ROUTER_API_KEY', 'http://localhost:20128/v1', 'ag/gemini-3-flash-agent'),
    ('9router', 'NINE_ROUTER_API_KEY', 'http://localhost:20128/v1', 'ag/gemini-3.7-flash-low'),
    ('9router', 'NINE_ROUTER_API_KEY', 'http://localhost:20128/v1', 'gh/gpt-4o-mini'),
    ('9router', 'NINE_ROUTER_API_KEY', 'http://localhost:20128/v1', 'gemini/gemma-4-31b-it'),
    ('openrouter', 'OPENROUTER_API_KEY', 'https://openrouter.ai/api/v1', 'nvidia/nemotron-3-super-120b-a12b:free'),
    ('openrouter', 'OPENROUTER_API_KEY', 'https://openrouter.ai/api/v1', 'google/gemma-4-26b-a4b-it:free'),
    ('opencode-zen', 'OPENCODE_ZEN_API_KEY', 'https://opencode.ai/zen/v1', 'big-pickle'),
    ('opencode-zen', 'OPENCODE_ZEN_API_KEY', 'https://opencode.ai/zen/v1', 'hy3-free'),
    ('opencode-zen', 'OPENCODE_ZEN_API_KEY', 'https://opencode.ai/zen/v1', 'laguna-s-2.1-free'),
]

print(f"{'Provider':15s} {'Model':50s} {'ms':>6s}  Status")
print('-'*80)
for pname, kenv, base, model in candidates:
    key = env.get(kenv, '')
    if not key:
        print(f"{pname:15s} {model:50s} {'---':>6s}  NO_KEY")
        continue
    ms, status = probe(base, key, model)
    flag = '✅' if status == 'OK' else '❌'
    print(f"{pname:15s} {model:50s} {ms:>6d}  {flag} {status}")
