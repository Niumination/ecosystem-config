#!/usr/bin/env python3
"""Rapid provider scan - single chat probe per candidate model, 8s timeout."""
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

KEYS = {
    '9router':      ('NINE_ROUTER_API_KEY',  'http://localhost:20128/v1'),
    'openrouter':   ('OPENROUTER_API_KEY',   'https://openrouter.ai/api/v1'),
    'opencode-zen': ('OPENCODE_ZEN_API_KEY', 'https://opencode.ai/zen/v1'),
}
UA = 'hermes-agent/0.19.0'

def probe(provider, key, base, model):
    body = json.dumps({
        'model': model, 'messages': [{'role': 'user', 'content': 'Reply: OK'}],
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
                    ln = ln.strip()
                    if ln.startswith('data:'):
                        try:
                            obj = json.loads(ln[5:].strip())
                            c = obj.get('choices',[{}])[0].get('delta',{}).get('content','')
                            if c: parts.append(c)
                        except: pass
                resp = ''.join(parts) if parts else '(empty SSE)'
            else:
                data = json.loads(raw)
                resp = data.get('choices',[{}])[0].get('message',{}).get('content','')[:40]
            ms = int((time.time()-t0)*1000)
            return ('OK', ms, resp)
    except urllib.error.HTTPError as e:
        return ('ERR', e.code, e.reason)
    except Exception as e:
        return ('ERR', 0, f'{type(e).__name__}: {str(e)[:60]}')

# Phase 1: get model lists
print("=== MODEL LISTS ===")
for pname, (kenv, base) in KEYS.items():
    key = env.get(kenv, '')
    if not key:
        print(f"{pname}: NO KEY"); continue
    try:
        req = urllib.request.Request(base+'/models', headers={'Authorization': f'Bearer {key}', 'User-Agent': UA})
        with urllib.request.urlopen(req, timeout=8) as r:
            data = json.loads(r.read())
            models = [m['id'] for m in data.get('data',[])]
            print(f"\n{pname}: {len(models)} models")
            for m in models: print(f"  - {m}")
    except Exception as e:
        print(f"{pname}: ERROR {e}")

# Phase 2: test candidates per provider
print("\n=== CANDIDATE PROBE ===")
candidates_9router = [
    'gh/gpt-4o-mini', 'gh/gpt-5-mini', 'gh/gpt-5.4-mini-free-auto',
    'gh/gpt-5.6-luna-free-auto', 'gh/claude-haiku-4.5',
    'ag/gemini-3.7-flash-medium', 'ag/gemini-3.7-flash-low',
    'ag/gemini-3.5-flash-extra-low', 'ag/gemini-3.5-flash-low',
    'ag/gemini-3-flash-agent',
    'kimi/kimi-k3', 'kimi/kimi-k2.5', 'kimi/kimi-for-coding',
    'gemini/gemma-4-31b-it',
    'ollama/minimax-m3', 'ollama/glm-4.7-flash', 'ollama/qwen3.5',
    'nvidia/minimaxai/minimax-m3',
]
candidates_openrouter = [
    'google/gemma-4-31b-it:free', 'google/gemma-4-26b-a4b-it:free',
    'nvidia/nemotron-3-ultra-550b-a55b:free', 'nvidia/nemotron-3.5-lightning:free',
    'nvidia/nemotron-3-super-120b-a12b:free',
    'poolside/laguna-s-2.1:free', 'poolside/laguna-xs-2.1:free',
    'cohere/north-mini-code:free',
    'openai/gpt-oss-20b:free',
    'minimax/minimax-m3:free', 'minimax/minimax-m2.7:free',
    'dots-studio/dots-3-note-preview:free',
    'z-ai/glm-5.2:free',
]
candidates_zen = [
    'hy3-free', 'nemotron-3-ultra-free', 'nemotron-3.5-lightning-free',
    'laguna-s-2.1-free', 'laguna-xs-2.1-free',
    'big-pickle', 'deepseek-v4-flash-free',
]

def test_group(name, models, provider, base, key):
    print(f"\n--- {name} ({provider}) ---")
    results = []
    for m in models:
        status, code, resp = probe(provider, key, base, m)
        tag = f"✅ {code}ms" if status == 'OK' else f"❌ {code}"
        results.append((m, status, code, resp))
        print(f"  {tag}  {m}")
    # rank
    ok_list = [(m,s,c,r) for m,s,c,r in results if s=='OK']
    bad_list = [(m,s,c,r) for m,s,c,r in results if s=='ERR']
    print(f"  >> {len(ok_list)}/{len(models)} OK")
    for m,_,c,_ in sorted(ok_list, key=lambda x:x[1]):
        print(f"     {c}ms  {m}")
    return ok_list, bad_list

all_ok = []
for pname, (kenv, base) in [('9router','NINE_ROUTER_API_KEY','http://localhost:20128/v1'),
                              ('openrouter','OPENROUTER_API_KEY','https://openrouter.ai/api/v1'),
                              ('opencode-zen','OPENCODE_ZEN_API_KEY','https://opencode.ai/zen/v1')]:
    key = env.get(kenv,'')
    if not key: continue
    if pname == '9router':
        ok, bad = test_group('9router candidates', candidates_9router, pname, base, key)
    elif pname == 'openrouter':
        ok, bad = test_group('OpenRouter candidates', candidates_openrouter, pname, base, key)
    else:
        ok, bad = test_group('Zen candidates', candidates_zen, pname, base, key)
    all_ok.extend([(pname,m,c,r) for m,s,c,r in ok])

print("\n" + "="*60)
print("FINAL RECOMMENDATIONS (all OK, sorted by speed)")
print("="*60)
for prov, m, ms, _ in sorted(all_ok, key=lambda x: x[2]):
    print(f"  {prov:15s} {m:50s} {ms}ms")
